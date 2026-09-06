from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any

from .artifacts import artifact_identity, normalize_text, snapshot_file, verify_artifact_identity, write_json
from .phase3 import run_phase3, verify_run_bundle
from .run import REPO_ROOT


class FeedbackError(ValueError):
    def __init__(self, code: str, *, artifact: str, field: str = "", expected: Any = None, observed: Any = None):
        self.code = code
        self.artifact = artifact
        self.field = field
        self.expected = expected
        self.observed = observed
        super().__init__(f"{code}: {artifact}.{field}: expected={expected!r} observed={observed!r}")

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "artifact": self.artifact, "field": self.field, "expected": self.expected, "observed": self.observed}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _type_ok(value: Any, type_name: str) -> bool:
    if type_name == "null":
        return value is None
    if type_name == "object":
        return isinstance(value, dict)
    if type_name == "array":
        return isinstance(value, list)
    if type_name == "string":
        return isinstance(value, str)
    if type_name == "boolean":
        return isinstance(value, bool)
    if type_name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def validate_instance(instance: Any, schema: dict[str, Any], *, path: str = "$", root_schema: dict[str, Any] | None = None) -> list[str]:
    root_schema = root_schema or schema
    errors: list[str] = []
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return [f"{path}: unsupported external $ref {ref}"]
        target: Any = root_schema
        for part in ref[2:].split("/"):
            target = target[part]
        return validate_instance(instance, target, path=path, root_schema=root_schema)
    if "anyOf" in schema:
        branches = [validate_instance(instance, sub, path=path, root_schema=root_schema) for sub in schema["anyOf"]]
        if not any(not branch for branch in branches):
            errors.append(f"{path}: does not satisfy anyOf")
        return errors
    if "oneOf" in schema:
        valid_count = sum(1 for sub in schema["oneOf"] if not validate_instance(instance, sub, path=path, root_schema=root_schema))
        if valid_count != 1:
            errors.append(f"{path}: expected exactly one matching oneOf branch, got {valid_count}")
        return errors

    declared_type = schema.get("type")
    if declared_type is not None:
        types = declared_type if isinstance(declared_type, list) else [declared_type]
        if not any(_type_ok(instance, t) for t in types):
            return [f"{path}: expected type {types}, got {type(instance).__name__}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"{path}: string does not match pattern {schema['pattern']}")
    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path}: array longer than maxItems {schema['maxItems']}")
        if schema.get("uniqueItems") and len({json.dumps(v, sort_keys=True, ensure_ascii=False) for v in instance}) != len(instance):
            errors.append(f"{path}: array items are not unique")
        if "items" in schema:
            for index, value in enumerate(instance):
                errors.extend(validate_instance(value, schema["items"], path=f"{path}[{index}]", root_schema=root_schema))
    if isinstance(instance, dict):
        for required in schema.get("required", []):
            if required not in instance:
                errors.append(f"{path}: missing required property {required}")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate_instance(value, properties[key], path=f"{path}.{key}", root_schema=root_schema))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key}")
    return errors


def _safe_path(root: Path, ref: str) -> Path:
    path = Path(ref)
    if path.is_absolute() or ".." in path.parts:
        raise FeedbackError("UNSAFE_SOURCE_REF", artifact=ref, expected="repository-relative path", observed=ref)
    resolved = root / path
    if not resolved.exists() or not resolved.is_file():
        raise FeedbackError("SOURCE_NOT_FOUND", artifact=ref, expected="existing file", observed=None)
    return resolved


def _select_json(value: Any, selector: str) -> Any:
    current = value
    if selector and "." in selector:
        for part in selector.split("."):
            if not isinstance(current, dict) or part not in current:
                raise FeedbackError("JSON_SELECTOR_NOT_FOUND", artifact="json", field=selector, expected=part, observed=current)
            current = current[part]
        return current
    if isinstance(current, dict) and selector in current:
        return current[selector]
    if isinstance(current, dict):
        for collection in ("beat_execution", "beats"):
            items = current.get(collection)
            if isinstance(items, list):
                for item in items:
                    if item.get("beat_id") == selector or item.get("id") == selector:
                        if "candidate_quote" in item:
                            return item["candidate_quote"]
                        return item
    raise FeedbackError("JSON_SELECTOR_NOT_FOUND", artifact="json", field=selector, expected="resolvable selector", observed=None)


def resolve_source_ref(root: Path, source_ref: str) -> dict[str, Any]:
    if " -> " in source_ref:
        file_ref, selector = source_ref.split(" -> ", 1)
    else:
        file_ref, selector = source_ref, None
    path = _safe_path(root, file_ref)
    identity = artifact_identity(path)
    if selector is None:
        try:
            selected: Any = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            raise FeedbackError("SOURCE_NOT_TEXT", artifact=file_ref, observed=str(exc)) from exc
    else:
        selected = _select_json(load_json(path), selector)
    if isinstance(selected, dict):
        selected_text = json.dumps(selected, ensure_ascii=False, sort_keys=True)
    elif isinstance(selected, str):
        selected_text = selected
    else:
        raise FeedbackError("SOURCE_SELECTION_NOT_TEXT", artifact=file_ref, field=selector or "", observed=type(selected).__name__)
    return {"path": path, "file_ref": file_ref, "selector": selector, "text": selected_text, "identity": identity}


def resolve_single_sample_locator(root: Path, sample_source_ref: str, locator: str, excerpt: str) -> dict[str, Any]:
    source = resolve_source_ref(root, sample_source_ref)
    text = normalize_text(source["text"])
    fragment = text
    match = re.search(r"paragraph\s+(\d+)", locator, flags=re.IGNORECASE)
    if match:
        paragraphs = text.split("\n\n")
        index = int(match.group(1)) - 1
        if index < 0 or index >= len(paragraphs):
            raise FeedbackError("LOCATOR_OUT_OF_RANGE", artifact=sample_source_ref, field="source_locator", expected=f"paragraph 1..{len(paragraphs)}", observed=locator)
        fragment = paragraphs[index]
    normalized_excerpt = normalize_text(excerpt)
    if not normalized_excerpt or normalized_excerpt not in fragment:
        raise FeedbackError("EXCERPT_NOT_IN_LOCATOR", artifact=sample_source_ref, field="candidate_excerpt", expected=normalized_excerpt, observed=fragment[:240])
    return source


def validate_guided_artifact(session_path: Path, *, root: Path = REPO_ROOT) -> dict[str, Any]:
    session = load_json(session_path)
    profile_path = root / "benchmarks/p01/review-profiles/foc-functional-targets.json"
    target_ids = {item.get("target_id") for item in load_json(profile_path).get("targets", [])}
    if "micro_units" in session:
        schema = load_json(root / "schemas/owner-guided-review.schema.json")
        errors = validate_instance(session, schema)
        if not errors:
            for unit in session["micro_units"]:
                try:
                    resolve_single_sample_locator(root, session["sample_source_ref"], unit["source_locator"], unit["candidate_excerpt"])
                except FeedbackError as exc:
                    errors.append(f"{exc.code}: {exc.artifact}.{exc.field}")
                for card in unit["feature_comparisons"]:
                    if card["target_behavior_ref"] not in target_ids:
                        errors.append(f"unknown target behavior ref: {card['target_behavior_ref']}")
        return {"format": "SINGLE_SAMPLE", "errors": errors, "owner_measurement_pending": True}

    schema = load_json(root / "schemas/owner-guided-comparison.schema.json")
    errors = validate_instance(session, schema)
    if not errors:
        for side in ("old", "new"):
            try:
                source = resolve_source_ref(root, session[side]["source_ref"])
                excerpt = normalize_text(session[side]["excerpt"])
                if not excerpt or excerpt not in normalize_text(source["text"]):
                    errors.append(f"{side}: excerpt not grounded in source_ref")
            except FeedbackError as exc:
                errors.append(f"{exc.code}: {side}.{exc.field}")
        for card in session.get("feature_cards", []):
            if card["target_behavior_ref"] not in target_ids:
                errors.append(f"unknown target behavior ref: {card['target_behavior_ref']}")
    pending = session.get("owner_summary_question", {}).get("result") is None
    return {"format": "COMPARISON", "errors": errors, "owner_measurement_pending": pending}


def _replace_only_beat(plan: dict[str, Any], beat_patch: dict[str, Any], allowed_beat_id: str) -> tuple[dict[str, Any], list[str]]:
    if beat_patch.get("id") != allowed_beat_id:
        raise FeedbackError("PLAN_SCOPE_VIOLATION", artifact="revised-plan", field="beat.id", expected=allowed_beat_id, observed=beat_patch.get("id"))
    revised = copy.deepcopy(plan)
    changed: list[str] = []
    found = False
    new_beats = []
    for beat in revised.get("beats", []):
        if beat.get("id") == allowed_beat_id:
            found = True
            new_beats.append(copy.deepcopy(beat_patch))
            if beat != beat_patch:
                changed.append(allowed_beat_id)
        else:
            new_beats.append(beat)
    if not found:
        raise FeedbackError("PLAN_PATCH_TARGET_NOT_FOUND", artifact="revised-plan", field="beat.id", expected=allowed_beat_id, observed=None)
    revised["beats"] = new_beats
    return revised, changed


def _case_bundle(case_dir: Path, paths: list[Path], *, case_id: str) -> dict[str, Any]:
    artifacts_map = {str(path.relative_to(case_dir)): artifact_identity(path) for path in paths if path.exists()}
    bundle = {"schema_version": "1.1.0", "case_id": case_id, "artifacts": artifacts_map, "self_hash_policy": "case-bundle.json excluded; current.json and immutable measurement ledger verified separately"}
    write_json(case_dir / "case-bundle.json", bundle)
    return bundle


def _measurement_files(case_dir: Path) -> list[Path]:
    root = case_dir / "measurements"
    return sorted(root.glob("*.json")) if root.exists() else []


def _feedback_files(case_dir: Path) -> list[Path]:
    root = case_dir / "feedback"
    return sorted(path for path in root.glob("*.json") if path.name != "initial.json") if root.exists() else []


def _verify_measurement_state(case_dir: Path) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    current_path = case_dir / "current.json"
    if not current_path.exists():
        return [{"code": "CURRENT_STATE_MISSING", "artifact": "current.json"}]
    current = load_json(current_path)
    measurement_ids = current.get("measurement_ids", [])
    observed_measurements = [path.stem for path in _measurement_files(case_dir)]
    observed_feedback = [path.stem for path in _feedback_files(case_dir)]
    if sorted(measurement_ids) != sorted(observed_measurements):
        errors.append({"code": "MEASUREMENT_LEDGER_MISMATCH", "expected": sorted(measurement_ids), "observed": sorted(observed_measurements)})
    if sorted(measurement_ids) != sorted(observed_feedback):
        errors.append({"code": "FEEDBACK_LEDGER_MISMATCH", "expected": sorted(measurement_ids), "observed": sorted(observed_feedback)})
    current_id = current.get("current_measurement_id")
    if current_id is not None and current_id not in measurement_ids:
        errors.append({"code": "CURRENT_MEASUREMENT_UNKNOWN", "observed": current_id})
    return errors


def verify_case_bundle(case_dir: Path) -> dict[str, Any]:
    bundle_path = case_dir / "case-bundle.json"
    if not bundle_path.exists():
        return {"status": "INVALID", "errors": [{"code": "CASE_BUNDLE_MISSING"}]}
    bundle = load_json(bundle_path)
    errors: list[dict[str, Any]] = []
    normalized: list[str] = []
    for rel, expected in bundle.get("artifacts", {}).items():
        path = case_dir / rel
        if not path.exists():
            errors.append({"code": "CASE_ARTIFACT_MISSING", "artifact": rel})
            continue
        check = verify_artifact_identity(path, expected)
        if check["status"] == "CONTENT_MISMATCH":
            errors.append({"code": "CASE_ARTIFACT_CHANGED", "artifact": rel})
        elif check["status"] == "TEXT_MATCH_RAW_DIFF_ALLOWED_NORMALIZATION":
            normalized.append(rel)
    trace_result = verify_run_bundle(case_dir / "trace-run")
    if trace_result["status"] != "VALID":
        errors.append({"code": "TRACE_BUNDLE_INVALID", "details": trace_result["errors"]})
    errors.extend(_verify_measurement_state(case_dir))
    return {"status": "VALID" if not errors else "INVALID", "errors": errors, "normalized_text_matches": normalized}


def _standard_binding() -> tuple[dict[str, Any], list[Path]]:
    brief_ref = "learning_runtime/briefs/p01-rootcause-01.json"
    product_ref = "docs/quality/output-quality-contract.md"
    target_ref = "benchmarks/p01/review-profiles/foc-functional-targets.json"
    paths = [REPO_ROOT / brief_ref, REPO_ROOT / product_ref, REPO_ROOT / target_ref]
    standard = {
        "brief": {"ref": brief_ref, "identity": artifact_identity(paths[0])},
        "product_contract": {"ref": product_ref, "identity": artifact_identity(paths[1])},
        "target_profile": {"ref": target_ref, "identity": artifact_identity(paths[2])},
        "product_review_blinding": "DIAGNOSTIC_HYPOTHESIS_HIDDEN_PRE_VOTE",
    }
    return standard, paths


def prepare_case(name: str, case_dir: Path) -> dict[str, Any]:
    if case_dir.exists() and any(case_dir.iterdir()):
        raise FileExistsError(f"case directory already exists and is non-empty: {case_dir}")
    case_dir.mkdir(parents=True, exist_ok=True)
    if name != "p01-rootcause-01":
        raise FeedbackError("UNKNOWN_FEEDBACK_CASE", artifact=name)

    trace_dir = case_dir / "trace-run"
    trace_manifest = run_phase3(name, trace_dir)
    if trace_manifest["status"] != "WHITEBOX_TRACE_COMPLETE":
        raise FeedbackError("TRACE_NOT_VALID", artifact="trace-run", observed=trace_manifest)
    diagnosis = load_json(trace_dir / "diagnosis.json")
    failure = load_json(trace_dir / "input-snapshot/failure.json")
    baseline_plan = load_json(trace_dir / "input-snapshot/plan.json")

    patch_ref = "learning_runtime/reruns/p01-rootcause-01/revised-plan-b03.json"
    output_ref = "learning_runtime/reruns/p01-rootcause-01/writer-output.md"
    report_ref = "learning_runtime/reruns/p01-rootcause-01/writer-report.json"
    template_ref = "benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json"
    patch = load_json(REPO_ROOT / patch_ref)
    intervention_source = REPO_ROOT / "learning_runtime/interventions/p01-rootcause-01-plan-only.json"
    intervention = load_json(intervention_source)
    if patch.get("source_beat_id") != "B03" or patch.get("change_scope") != "PLAN_ONLY":
        raise FeedbackError("PLAN_SCOPE_VIOLATION", artifact=patch_ref, expected="PLAN_ONLY:B03", observed={"beat": patch.get("source_beat_id"), "scope": patch.get("change_scope")})
    revised_plan, changed_beats = _replace_only_beat(baseline_plan, patch["beat"], "B03")
    if changed_beats != ["B03"]:
        raise FeedbackError("PLAN_SCOPE_VIOLATION", artifact=patch_ref, expected=["B03"], observed=changed_beats)

    revised_plan_path = case_dir / "revised-plan.full.json"
    write_json(revised_plan_path, revised_plan)
    revised_output_path = case_dir / "revised-output.md"
    snapshot_file(REPO_ROOT / output_ref, revised_output_path)
    revised_report_path = case_dir / "revised-writer-report.json"
    snapshot_file(REPO_ROOT / report_ref, revised_report_path)
    intervention_path = case_dir / "intervention.json"
    snapshot_file(intervention_source, intervention_path)

    standard, standard_sources = _standard_binding()
    standard_dir = case_dir / "standard"
    standard_dir.mkdir(parents=True, exist_ok=True)
    standard_snapshots: list[Path] = []
    for source in standard_sources:
        destination = standard_dir / source.name
        snapshot_file(source, destination)
        standard_snapshots.append(destination)

    baseline_candidate_path = trace_dir / "input-snapshot/candidate.md"
    baseline_identity = artifact_identity(baseline_candidate_path)
    candidate_identity = artifact_identity(revised_output_path)
    comparison = copy.deepcopy(load_json(REPO_ROOT / template_ref))
    comparison["schema_version"] = "1.1.0"
    comparison["case_id"] = "P3-B03-P3-I01"
    comparison["measurement_status"] = "AWAITING_MEASUREMENT"
    comparison["old"]["source_ref"] = "trace-run/input-snapshot/candidate.md"
    comparison["old"]["source_identity"] = baseline_identity
    comparison["new"]["source_ref"] = "revised-output.md"
    comparison["new"]["source_identity"] = candidate_identity
    comparison_path = case_dir / "comparison-card.json"
    write_json(comparison_path, comparison)

    case = {
        "schema_version": "1.1.0",
        "case_id": "P3-B03-P3-I01",
        "source_run_id": trace_manifest["run_id"],
        "source_commit": trace_manifest.get("source_commit"),
        "standard": standard,
        "baseline": {"id": "ROUND01-B03", "source_ref": "trace-run/input-snapshot/candidate.md", "identity": baseline_identity},
        "candidate": {"id": "P3-I01-MANUAL-B03", "source_ref": "revised-output.md", "identity": candidate_identity, "independence": "NONE"},
        "symptom": {"id": failure["symptom"], "failure_id": failure["failure_id"], "baseline_quote": failure["candidate_quote"]},
        "trace": {
            "mapping_status": diagnosis["mapping_status"],
            "mapping_confidence": diagnosis["mapping_confidence"],
            "suspected_regions": diagnosis["suspected_regions"],
            "attribution_confidence": diagnosis["attribution_confidence"],
            "authority": "BOUNDED_DIAGNOSTIC_HYPOTHESIS_NOT_CAUSAL_PROOF",
        },
        "intervention": {"id": intervention["intervention_id"], "scope": "PLAN_ONLY:B03", "identity": artifact_identity(intervention_path)},
        "plan_change": {"allowed_beat_ids": ["B03"], "changed_beat_ids": changed_beats, "materialized_plan_ref": "revised-plan.full.json"},
        "evidence_ceiling": "UNCHANGED_FROM_BASELINE_TRACE_FIXTURE",
        "measurement_scope": "B03_MICRO_UNIT_ONLY",
        "invariants": {
            "truth": "NOT_MEASURED",
            "artifact_clarity": "NOT_MEASURED",
            "sequence_continuity": "NOT_MEASURED",
            "whole_section_quality": "OUT_OF_SCOPE",
        },
        "acceptance_rule": "Preference and symptom observation are separate evidence. Guided owner measurement cannot establish blind benchmark gain, whole-section improvement, or causal proof. Missing invariants remain explicit.",
        "comparison_ref": "comparison-card.json",
        "measurement_status": "AWAITING_MEASUREMENT",
    }
    schema_errors = validate_instance(case, load_json(REPO_ROOT / "schemas/feedback-case.schema.json"))
    if schema_errors:
        raise FeedbackError("CASE_SCHEMA_INVALID", artifact="case.json", observed=schema_errors)
    case_path = case_dir / "case.json"
    write_json(case_path, case)

    (case_dir / "measurements").mkdir(parents=True, exist_ok=True)
    (case_dir / "feedback").mkdir(parents=True, exist_ok=True)
    initial_feedback = build_feedback(case, measurement=None)
    initial_feedback_path = case_dir / "feedback/initial.json"
    write_json(initial_feedback_path, initial_feedback)
    write_json(case_dir / "current.json", {
        "schema_version": "1.0.0",
        "case_id": case["case_id"],
        "status": "AWAITING_MEASUREMENT",
        "measurement_ids": [],
        "current_measurement_id": None,
        "current_feedback_ref": "feedback/initial.json",
        "resolution": "NO_MEASUREMENT",
    })
    frozen_paths = [case_path, comparison_path, revised_plan_path, revised_output_path, revised_report_path, intervention_path, initial_feedback_path, *standard_snapshots]
    _case_bundle(case_dir, frozen_paths, case_id=case["case_id"])
    return {"status": "AWAITING_MEASUREMENT", "case_id": case["case_id"], "case_dir": str(case_dir), "comparison_ref": "comparison-card.json", "verification": verify_case_bundle(case_dir)}


def _next_action(preference: str | None, symptom: str) -> str:
    if preference is None:
        return "OWNER_MEASURE_COMPARISON_CARD"
    if preference == "WRONG_TARGET":
        return "REVISIT_TARGET_DEFINITION_KEEP_OUTPUT_FROZEN"
    if preference == "UNCERTAIN":
        return "CLARIFY_OR_COLLECT_MORE_OBSERVATION_KEEP_INTERVENTION"
    if symptom == "NOT_REDUCED":
        return "REJECT_OR_REVISE_BOUNDED_INTERVENTION"
    if symptom == "REDUCED" and preference == "YES":
        return "KEEP_BOUNDED_HYPOTHESIS_FOR_NEXT_INDEPENDENT_TEST"
    if symptom == "REDUCED" and preference in {"NO", "BOTH_FAIL"}:
        return "INSPECT_TRADEOFF_OR_REGRESSION_BEFORE_ANY_GENERAL_CHANGE"
    return "COLLECT_SYMPTOM_OBSERVATION_KEEP_INTERVENTION"


def build_feedback(case: dict[str, Any], measurement: dict[str, Any] | None) -> dict[str, Any]:
    if measurement is None:
        measurement_id = None
        preference = None
        symptom = "AWAITING_MEASUREMENT"
        authority = "NONE"
        invariants = dict(case["invariants"])
        regressions: list[str] = []
    else:
        measurement_id = measurement["measurement_id"]
        preference = measurement["preference_result"]
        symptom = measurement.get("symptom_observation") or "NOT_MEASURED"
        authority = "TEST_ONLY" if measurement["trust_mode"] == "TEST_ONLY" else "GUIDED_OWNER_DIRECTIONAL"
        invariants = dict(case["invariants"])
        invariants.update(measurement.get("invariants") or {})
        regressions = list(measurement.get("regressions") or [])
    return {
        "schema_version": "1.1.0",
        "case_id": case["case_id"],
        "measurement_id": measurement_id,
        "status": "AWAITING_MEASUREMENT" if measurement is None else "MEASUREMENT_INGESTED",
        "evidence_integrity": "VERIFIED_AT_PREPARE_TIME",
        "trace_status": {
            "mapping": case["trace"]["mapping_status"],
            "mapping_confidence": case["trace"]["mapping_confidence"],
            "attribution_confidence": case["trace"]["attribution_confidence"],
        },
        "suspected_region": case["trace"]["suspected_regions"],
        "preference_result": preference,
        "symptom_observation": symptom,
        "invariant_state": invariants,
        "regressions": regressions,
        "measurement_authority": authority,
        "improvement": "NOT_ESTABLISHED",
        "limitations": [
            "Preference is not evidence that the named symptom changed.",
            "Lexical disappearance of the baseline sentence is not evidence that the symptom is resolved.",
            "Guided owner measurement is directional diagnostic evidence, not blind benchmark gain.",
            "Manual same-agent rerun has independence NONE.",
            "Unmeasured Truth/regression/continuity invariants remain open and prevent overall gain claims.",
        ],
        "next_action": _next_action(preference, symptom),
    }


def _validate_measurement(case: dict[str, Any], measurement: dict[str, Any]) -> None:
    schema_errors = validate_instance(measurement, load_json(REPO_ROOT / "schemas/feedback-measurement.schema.json"))
    if schema_errors:
        raise FeedbackError("MEASUREMENT_SCHEMA_INVALID", artifact="measurement", observed=schema_errors)
    if measurement["case_id"] != case["case_id"]:
        raise FeedbackError("MEASUREMENT_CASE_MISMATCH", artifact="measurement", field="case_id", expected=case["case_id"], observed=measurement["case_id"])
    expected_hash = case["candidate"]["identity"]["text_sha256"]
    if measurement["candidate_text_sha256"] != expected_hash:
        raise FeedbackError("STALE_MEASUREMENT_CANDIDATE", artifact="measurement", field="candidate_text_sha256", expected=expected_hash, observed=measurement["candidate_text_sha256"])
    if measurement["scope"] != case["measurement_scope"]:
        raise FeedbackError("MEASUREMENT_SCOPE_MISMATCH", artifact="measurement", field="scope", expected=case["measurement_scope"], observed=measurement["scope"])


def _update_current(case_dir: Path, measurement: dict[str, Any], feedback_ref: str) -> dict[str, Any]:
    current = load_json(case_dir / "current.json")
    measurement_id = measurement["measurement_id"]
    supersedes = measurement.get("supersedes")
    ids = list(current.get("measurement_ids", []))
    prior_current = current.get("current_measurement_id")
    ids.append(measurement_id)
    if prior_current is None and len(ids) == 1:
        current_id = measurement_id
        resolution = "CURRENT_SINGLE_MEASUREMENT"
    elif supersedes:
        if supersedes not in ids[:-1]:
            raise FeedbackError("SUPERSEDES_UNKNOWN_MEASUREMENT", artifact="measurement", field="supersedes", expected=ids[:-1], observed=supersedes)
        current_id = measurement_id
        resolution = "CURRENT_SUPERSEDING_MEASUREMENT"
    else:
        current_id = None
        resolution = "MULTIPLE_MEASUREMENTS_UNRESOLVED"
    updated = {
        "schema_version": "1.0.0",
        "case_id": current["case_id"],
        "status": "MEASURED" if current_id is not None else "MEASUREMENTS_REQUIRE_RESOLUTION",
        "measurement_ids": ids,
        "current_measurement_id": current_id,
        "current_feedback_ref": feedback_ref if current_id == measurement_id else None,
        "resolution": resolution,
    }
    write_json(case_dir / "current.json", updated)
    return updated


def ingest_measurement(case_dir: Path, measurement_path: Path) -> dict[str, Any]:
    verify = verify_case_bundle(case_dir)
    if verify["status"] != "VALID":
        raise FeedbackError("CASE_BUNDLE_INVALID", artifact=str(case_dir), observed=verify["errors"])
    case = load_json(case_dir / "case.json")
    measurement = load_json(measurement_path)
    _validate_measurement(case, measurement)
    measurement_id = measurement["measurement_id"]
    measurement_snapshot = case_dir / "measurements" / f"{measurement_id}.json"
    feedback_path = case_dir / "feedback" / f"{measurement_id}.json"
    if measurement_snapshot.exists() or feedback_path.exists():
        raise FeedbackError("MEASUREMENT_ID_ALREADY_EXISTS", artifact=measurement_id, expected="new immutable measurement id", observed=measurement_id)

    supersedes = measurement.get("supersedes")
    if supersedes and not (case_dir / "measurements" / f"{supersedes}.json").exists():
        raise FeedbackError("SUPERSEDES_UNKNOWN_MEASUREMENT", artifact=measurement_id, field="supersedes", observed=supersedes)

    snapshot_file(measurement_path, measurement_snapshot)
    feedback = build_feedback(case, measurement)
    schema_errors = validate_instance(feedback, load_json(REPO_ROOT / "schemas/feedback-result.schema.json"))
    if schema_errors:
        measurement_snapshot.unlink(missing_ok=True)
        raise FeedbackError("FEEDBACK_SCHEMA_INVALID", artifact=str(feedback_path), observed=schema_errors)
    write_json(feedback_path, feedback)
    _update_current(case_dir, measurement, f"feedback/{measurement_id}.json")
    post_verify = verify_case_bundle(case_dir)
    if post_verify["status"] != "VALID":
        raise FeedbackError("POST_INGEST_BUNDLE_INVALID", artifact=str(case_dir), observed=post_verify["errors"])
    return feedback


def show_state(case_dir: Path) -> dict[str, Any]:
    verify = verify_case_bundle(case_dir)
    current = load_json(case_dir / "current.json")
    result: dict[str, Any] = {"verification": verify, "current": current}
    ref = current.get("current_feedback_ref")
    if ref:
        result["current_feedback"] = load_json(case_dir / ref)
    result["measurements"] = [load_json(path) for path in _measurement_files(case_dir)]
    return result


def _main_prepare(args: argparse.Namespace) -> int:
    print(json.dumps(prepare_case(args.name, args.out), ensure_ascii=False, indent=2))
    return 0


def _main_ingest(args: argparse.Namespace) -> int:
    try:
        result = ingest_measurement(args.case_dir, args.measurement)
    except FeedbackError as exc:
        print(json.dumps({"status": "REJECTED", "error": exc.as_dict()}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded feedback loop for Phase 3 MVP")
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("name")
    prepare.add_argument("--out", type=Path, required=True)
    prepare.set_defaults(func=_main_prepare)
    ingest = sub.add_parser("ingest")
    ingest.add_argument("--case-dir", type=Path, required=True)
    ingest.add_argument("--measurement", type=Path, required=True)
    ingest.set_defaults(func=_main_ingest)
    verify = sub.add_parser("verify")
    verify.add_argument("--case-dir", type=Path, required=True)
    show = sub.add_parser("show")
    show.add_argument("--case-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "verify":
        result = verify_case_bundle(args.case_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "VALID" else 1
    if args.command == "show":
        print(json.dumps(show_state(args.case_dir), ensure_ascii=False, indent=2))
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
