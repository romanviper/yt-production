#!/usr/bin/env python3
"""Verify the active Phase 1 measurement surface against actual artifacts.

This remains a structural/evidence-integrity verifier. It cannot certify owner
preference validity, aesthetic quality, judge reliability or transfer.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from learning_runtime.artifacts import normalize_text  # noqa: E402
from learning_runtime.feedback import FeedbackError, resolve_source_ref, validate_instance  # noqa: E402


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: pathlib.Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def selected_text_sha256(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def validate_named_instance(errors: list[str], name: str, instance: object, schema: dict) -> None:
    for error in validate_instance(instance, schema):
        errors.append(f"{name} schema: {error}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    paths = {
        "contract": ROOT / "docs/quality/output-quality-contract.md",
        "protocol": ROOT / "docs/quality/product-trial-protocol.md",
        "start": ROOT / "docs/phase1/START.md",
        "eval_unit_schema": ROOT / "schemas/eval-unit.schema.json",
        "pairwise_schema": ROOT / "schemas/pairwise-preference.schema.json",
        "failure_schema": ROOT / "schemas/failure-signature.schema.json",
        "truth_schema": ROOT / "schemas/truth-gate.schema.json",
        "spoken_schema": ROOT / "schemas/spoken-observation.schema.json",
        "target_schema": ROOT / "schemas/target-gap.schema.json",
        "judge_schema": ROOT / "schemas/judge-reliability.schema.json",
        "legacy_output_schema": ROOT / "schemas/output-quality.schema.json",
        "worker_schema": ROOT / "schemas/phase1-worker-iteration.schema.json",
        "guided_schema": ROOT / "schemas/owner-guided-review.schema.json",
        "guided_comparison_schema": ROOT / "schemas/owner-guided-comparison.schema.json",
        "benchmark": ROOT / "benchmarks/p01/benchmark-set.json",
        "manifest": ROOT / "benchmarks/p01/source-manifest.json",
        "craft": ROOT / "benchmarks/p01/craft-corpus.json",
        "taxonomy": ROOT / "benchmarks/p01/taxonomy.json",
        "owner_state": ROOT / "benchmarks/p01/owner-calibration.json",
        "judge_state": ROOT / "benchmarks/p01/judge-reliability.json",
        "sequestered": ROOT / "benchmarks/p01/sequestered-manifest.json",
        "pilot_eval_unit": ROOT / "benchmarks/p01/eval-units/eu-p01-pilot-mechanism-01.json",
        "post_vote_owner": ROOT / "benchmarks/p01/calibration/post-vote-owner-diagnostics.json",
        "pilot_1": ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-01.json",
        "pilot_2": ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-02.json",
        "pilot_3": ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-03.json",
        "guided_owner": ROOT / "benchmarks/p01/review-sessions/owner-pilot-01-guided.json",
        "guided_phase3": ROOT / "benchmarks/p01/review-sessions/phase3-p3-f01-rerun-guided.json",
    }
    for name, path in paths.items():
        if not path.exists():
            errors.append(f"missing required artifact: {name} -> {path.relative_to(ROOT)}")
    if errors:
        print(json.dumps({"status": "NOT_READY", "structural_errors": errors}, ensure_ascii=False, indent=2))
        return 1

    json_names = [name for name, path in paths.items() if path.suffix == ".json"]
    parsed: dict[str, object] = {}
    for name in json_names:
        try:
            parsed[name] = load_json(paths[name])
        except Exception as exc:
            errors.append(f"invalid JSON: {paths[name].relative_to(ROOT)} -> {exc}")
    if errors:
        print(json.dumps({"status": "NOT_READY", "structural_errors": errors}, ensure_ascii=False, indent=2))
        return 1

    contract = paths["contract"].read_text(encoding="utf-8")
    protocol = paths["protocol"].read_text(encoding="utf-8")
    start = paths["start"].read_text(encoding="utf-8")
    benchmark = parsed["benchmark"]
    manifest = parsed["manifest"]
    craft = parsed["craft"]
    taxonomy = parsed["taxonomy"]
    owner_state = parsed["owner_state"]
    judge_state = parsed["judge_state"]
    sequestered = parsed["sequestered"]
    pilot_eval_unit = parsed["pilot_eval_unit"]
    pilots = [parsed["pilot_1"], parsed["pilot_2"], parsed["pilot_3"]]

    # Validate actual active instances rather than merely searching schema text.
    validate_named_instance(errors, "pilot_eval_unit", pilot_eval_unit, parsed["eval_unit_schema"])
    validate_named_instance(errors, "judge_state", judge_state, parsed["judge_schema"])
    validate_named_instance(errors, "guided_owner", parsed["guided_owner"], parsed["guided_schema"])
    validate_named_instance(errors, "guided_phase3", parsed["guided_phase3"], parsed["guided_comparison_schema"])

    # Frozen architecture invariants retained from Benchmark V1.
    for term in ["OWNER_PRODUCT_FIT", "BOTH_FAIL", "SHADOW_ONLY", "FUNCTION_CLIP", "SECTION_SENTINEL", "EPISODE_SENTINEL", "SEQUESTERED", "root_cause"]:
        if term not in contract:
            errors.append(f"contract missing frozen Benchmark V1 concept: {term}")
    for phrase in ["defect taxonomy before the vote", "first-pass preference is recorded and frozen", "FoC is hidden from the primary vote", "SHADOW_ONLY", "The public repo contains only"]:
        if phrase not in protocol:
            errors.append(f"protocol missing freeze/isolation invariant: {phrase}")
    if "schemas/output-quality.schema.json` is deprecated" not in start:
        errors.append("Phase 1 START does not explicitly deprecate the monolithic output schema")

    pairwise_schema_text = paths["pairwise_schema"].read_text(encoding="utf-8")
    for term in ["BOTH_FAIL", "confidence", "preference_frozen", "blind_to_reference", "LLM_SHADOW_JUDGE"]:
        if term not in pairwise_schema_text:
            errors.append(f"pairwise preference schema missing {term}")
    for legacy_field in ['"pairwise_criteria"', '"continue"', '"movement"', '"payoff"', '"target_gap"', '"absolute_gates"']:
        if legacy_field in pairwise_schema_text:
            errors.append(f"pairwise preference schema still embeds legacy field {legacy_field}")

    failure_schema_text = paths["failure_schema"].read_text(encoding="utf-8")
    for term in ["SPAN", "MULTI_SPAN", "UNIT_GLOBAL", "UNRESOLVED", '"root_cause"', '"type": "null"']:
        if term not in failure_schema_text:
            errors.append(f"failure-signature schema missing {term}")
    for forbidden in ["planner_fault", "writer_fault", "suspect_upstream_regions"]:
        if forbidden in failure_schema_text:
            errors.append(f"failure-signature schema contains upstream blame field: {forbidden}")

    expected_families = {"NARRATIVE_FUNCTION", "EXPOSITION_LOAD", "SPOKEN_COMPREHENSION", "GROUNDING_SPECIFICITY", "VOICE_STANCE", "REDUNDANCY"}
    if set(taxonomy.get("families", {}).keys()) != expected_families:
        errors.append("taxonomy families differ from frozen six-family set")
    if taxonomy.get("status") != "FROZEN_FOR_PILOT":
        errors.append("taxonomy is not marked FROZEN_FOR_PILOT")

    truth_schema_text = paths["truth_schema"].read_text(encoding="utf-8")
    for term in ["IMPLIED_PREMISE", "CAUSAL", "VERIFIABLE", "PARTLY_VERIFIABLE", "SUPPORTS", "QUALIFIES", "CONFLICTS", "ABSENT", "release_blocker", "P01_HISTORICAL_AUTHORITY_ONLY_NO_CRAFT_REFERENCES"]:
        if term not in truth_schema_text:
            errors.append(f"truth schema missing semantic audit concept: {term}")
    if "CRAFT_ONLY_NOT_TRUTH" in truth_schema_text:
        errors.append("truth schema unexpectedly admits craft-reference authority")

    spoken_schema_text = paths["spoken_schema"].read_text(encoding="utf-8")
    for term in ["TEXT_PREDICTION", "AUDIO_OBSERVATION", "LISTENER_REPORT"]:
        if term not in spoken_schema_text:
            errors.append(f"spoken schema missing evidence mode {term}")

    target_schema_text = paths["target_schema"].read_text(encoding="utf-8")
    for term in ["product_preference_frozen", "reference_visible_during_primary_vote", "CRAFT_ONLY_NOT_TRUTH", "matched_editorial_function", "style_similarity_used_as_score", "imitation_risk", "retroactive_preference_change"]:
        if term not in target_schema_text:
            errors.append(f"target-gap schema missing {term}")

    if judge_state.get("mode") != "SHADOW_ONLY" or judge_state.get("eligible_for_optimization_loop") is not False:
        errors.append("current judge state is not SHADOW_ONLY / ineligible")
    if judge_state.get("pre_registered_tolerance_ref") is not None:
        warnings.append("Judge tolerance is populated; verify it was pre-registered before sequestered labels were opened.")

    samples = benchmark.get("samples", [])
    ids = [sample.get("id") for sample in samples]
    if len(ids) != len(set(ids)):
        errors.append("duplicate benchmark sample ids")
    for sample in samples:
        if sample.get("partition") != "DEV":
            errors.append(f"public historical P01 sample is not DEV: {sample.get('id')} -> {sample.get('partition')}")
    for pair in benchmark.get("pilot_pairs", []):
        if pair.get("left") not in ids or pair.get("right") not in ids:
            errors.append(f"pilot pair references unknown sample: {pair.get('pair_id')}")
    if benchmark.get("calibration_plan", {}).get("status") != "NOT_POPULATED":
        errors.append("fresh calibration corpus is incorrectly marked populated")
    agg = benchmark.get("aggregation_policy", {})
    if agg.get("global_quality_score") is not False or agg.get("bradley_terry_required") is not False or agg.get("elo_required") is not False:
        errors.append("Benchmark V1 reintroduced scalar/BT/Elo aggregation")

    if sequestered.get("public_repo_contains_payload") is not False or sequestered.get("public_repo_contains_labels") is not False:
        errors.append("sequestered manifest claims private payload/labels are present in public repo")

    # Validate first-pass owner packets and keep post-vote diagnostics isolated.
    expected_post_vote_ref = "benchmarks/p01/calibration/post-vote-owner-diagnostics.json"
    for packet in pilots:
        packet_id = packet.get("packet_id", "UNKNOWN")
        if packet.get("role") != "PILOT_ONLY_NOT_CALIBRATION_EVIDENCE":
            errors.append(f"{packet_id} has wrong role")
        first = packet.get("first_pass", {})
        if "BOTH_FAIL" not in first.get("allowed_results", []):
            errors.append(f"{packet_id} does not offer BOTH_FAIL")
        if set(first.get("confidence_options", [])) != {"LOW", "MEDIUM", "HIGH"}:
            errors.append(f"{packet_id} confidence options incomplete")
        if packet.get("post_vote_artifact_ref") != expected_post_vote_ref:
            errors.append(f"{packet_id} does not reference separate post-vote diagnostics")
        if "post_vote_optional" in packet or "optional_feedback_prompts" in packet:
            errors.append(f"{packet_id} embeds post-vote prompts")

    if owner_state.get("status") != "PILOT_READY_NOT_CALIBRATION":
        errors.append("owner state is not PILOT_READY_NOT_CALIBRATION")
    if set(owner_state.get("allowed_owner_results", [])) != {"A", "B", "TIE", "BOTH_FAIL", "UNCERTAIN"}:
        errors.append("owner allowed results do not match frozen enum")

    # Product identities: resolve the actual file/JSON field and verify current content.
    manifest_samples = {item["sample_id"]: item for item in manifest.get("product_samples", [])}
    for sample_id in ids:
        if sample_id not in manifest_samples:
            errors.append(f"sample {sample_id} missing from source manifest")
    for item in manifest.get("product_samples", []):
        sample_id = item.get("sample_id")
        if not str(item.get("benchmark_role", "")).startswith("DEV"):
            errors.append(f"source manifest exposes non-DEV role: {sample_id}")
        try:
            resolved = resolve_source_ref(ROOT, item["locator"])
        except FeedbackError as exc:
            errors.append(f"product source resolve failed {sample_id}: {exc.code} {exc.artifact}.{exc.field}")
            continue
        kind = item.get("identity_kind")
        expected = item.get("identity")
        if kind == "SHA256_TEXT":
            observed = selected_text_sha256(resolved["text"])
            if observed != expected:
                errors.append(f"product sample text identity changed: {sample_id} expected={expected} observed={observed}")
        elif kind == "GIT_BLOB_SHA1":
            if resolved["selector"] is not None:
                errors.append(f"GIT_BLOB_SHA1 sample must resolve whole file: {sample_id}")
            else:
                observed = git_blob_sha1(resolved["path"])
                if observed != expected:
                    errors.append(f"product sample blob identity changed: {sample_id} expected={expected} observed={observed}")
        else:
            errors.append(f"unsupported product identity kind: {sample_id} -> {kind}")

    craft_sources = {item["source_id"]: item for item in manifest.get("craft_sources", [])}
    for source in craft_sources.values():
        if source.get("authority") != "CRAFT_ONLY_NOT_TRUTH":
            errors.append(f"craft source {source.get('source_id')} not CRAFT_ONLY_NOT_TRUTH")
        source_path = ROOT / source["locator"]
        if not source_path.exists():
            errors.append(f"craft source missing: {source['locator']}")
        elif source.get("git_blob_sha1") and git_blob_sha1(source_path) != source["git_blob_sha1"]:
            errors.append(f"craft source blob identity changed: {source['source_id']}")

    excerpts = craft.get("excerpts", [])
    episodes = {item.get("episode") for item in excerpts}
    if not 6 <= len(excerpts) <= 10:
        errors.append(f"craft corpus should contain 6-10 excerpts, found {len(excerpts)}")
    if len(episodes) < 2:
        errors.append("craft corpus needs at least two episodes")
    for excerpt in excerpts:
        source_id = excerpt.get("source_ref")
        if source_id not in craft_sources:
            errors.append(f"excerpt {excerpt.get('id')} references unknown craft source {source_id}")
            continue
        text = (ROOT / craft_sources[source_id]["locator"]).read_text(encoding="utf-8-sig")
        start_anchor = excerpt.get("start_anchor", "")
        end_anchor = excerpt.get("end_anchor", "")
        if not start_anchor or start_anchor not in text:
            errors.append(f"excerpt {excerpt.get('id')} start anchor not found")
        if not end_anchor or end_anchor not in text:
            errors.append(f"excerpt {excerpt.get('id')} end anchor not found")
        if start_anchor in text and end_anchor in text and text.index(start_anchor) > text.index(end_anchor):
            errors.append(f"excerpt {excerpt.get('id')} anchor order invalid")

    if parsed["legacy_output_schema"].get("deprecated") is not True:
        errors.append("legacy output-quality schema is not marked deprecated")

    status = "NOT_READY" if errors else "ARCHITECTURE_FROZEN_READY_FOR_PILOT"
    if not errors:
        warnings.extend([
            "Historical DEV prose cannot establish benchmark validity.",
            "Owner labels may still be null; structurally valid pending measurement is not a gain claim.",
            "LLM judge remains SHADOW_ONLY and unvalidated.",
            "Structural/evidence verification cannot establish aesthetic or transfer validity.",
        ])
    result = {
        "status": status,
        "structural_errors": errors,
        "warnings": warnings,
        "counts": {
            "public_dev_samples": len(samples),
            "pilot_pairs": len(benchmark.get("pilot_pairs", [])),
            "pilot_owner_packets": len(pilots),
            "craft_excerpts": len(excerpts),
            "craft_episodes": len(episodes),
        },
        "verified_surfaces": ["ACTIVE_SCHEMA_INSTANCES", "PRODUCT_SOURCE_IDENTITIES", "CRAFT_SOURCE_IDENTITIES", "OWNER_PACKET_ISOLATION", "SHADOW_JUDGE_BOUNDARY"],
        "phase1_complete": false
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
