#!/usr/bin/env python3
"""Structural verifier for Phase 1 Benchmark V1.3 architecture freeze.

This verifier checks public-repository structure and invariants only. It cannot
certify owner preference validity, aesthetic quality, LLM judge reliability,
private sequestered evidence, or topic transfer.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: pathlib.Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    paths = {
        "contract": ROOT / "docs/quality/output-quality-contract.md",
        "protocol": ROOT / "docs/quality/product-trial-protocol.md",
        "start": ROOT / "docs/phase1/START.md",
        "work_order": ROOT / "docs/phase1/ITERATION-04-WORK-ORDER.md",
        "eval_unit_schema": ROOT / "schemas/eval-unit.schema.json",
        "pairwise_schema": ROOT / "schemas/pairwise-preference.schema.json",
        "failure_schema": ROOT / "schemas/failure-signature.schema.json",
        "truth_schema": ROOT / "schemas/truth-gate.schema.json",
        "spoken_schema": ROOT / "schemas/spoken-observation.schema.json",
        "target_schema": ROOT / "schemas/target-gap.schema.json",
        "judge_schema": ROOT / "schemas/judge-reliability.schema.json",
        "legacy_output_schema": ROOT / "schemas/output-quality.schema.json",
        "worker_schema": ROOT / "schemas/phase1-worker-iteration.schema.json",
        "benchmark": ROOT / "benchmarks/p01/benchmark-set.json",
        "manifest": ROOT / "benchmarks/p01/source-manifest.json",
        "craft": ROOT / "benchmarks/p01/craft-corpus.json",
        "taxonomy": ROOT / "benchmarks/p01/taxonomy.json",
        "owner_state": ROOT / "benchmarks/p01/owner-calibration.json",
        "judge_state": ROOT / "benchmarks/p01/judge-reliability.json",
        "sequestered": ROOT / "benchmarks/p01/sequestered-manifest.json",
        "pilot_eval_unit": ROOT / "benchmarks/p01/eval-units/eu-p01-pilot-mechanism-01.json",
        "dispatch_map": ROOT / "benchmarks/p01/calibration/dispatch-map.json",
        "post_vote_owner": ROOT / "benchmarks/p01/calibration/post-vote-owner-diagnostics.json",
        "pilot_1": ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-01.json",
        "pilot_2": ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-02.json",
        "pilot_3": ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-03.json",
    }

    for name, path in paths.items():
        if not path.exists():
            errors.append(f"missing required artifact: {name} -> {path.relative_to(ROOT)}")

    if errors:
        print(json.dumps({"status": "NOT_READY", "structural_errors": errors}, ensure_ascii=False, indent=2))
        return 1

    json_keys = [
        "eval_unit_schema", "pairwise_schema", "failure_schema", "truth_schema",
        "spoken_schema", "target_schema", "judge_schema", "legacy_output_schema",
        "worker_schema", "benchmark", "manifest", "craft", "taxonomy",
        "owner_state", "judge_state", "sequestered", "pilot_eval_unit",
        "dispatch_map", "post_vote_owner", "pilot_1", "pilot_2", "pilot_3",
    ]
    parsed: dict[str, object] = {}
    for key in json_keys:
        try:
            parsed[key] = load_json(paths[key])
        except Exception as exc:
            errors.append(f"invalid JSON: {paths[key].relative_to(ROOT)} -> {exc}")

    if errors:
        print(json.dumps({"status": "NOT_READY", "structural_errors": errors}, ensure_ascii=False, indent=2))
        return 1

    contract = paths["contract"].read_text(encoding="utf-8")
    protocol = paths["protocol"].read_text(encoding="utf-8")
    start = paths["start"].read_text(encoding="utf-8")
    pairwise_schema_text = paths["pairwise_schema"].read_text(encoding="utf-8")
    failure_schema_text = paths["failure_schema"].read_text(encoding="utf-8")
    truth_schema_text = paths["truth_schema"].read_text(encoding="utf-8")
    spoken_schema_text = paths["spoken_schema"].read_text(encoding="utf-8")
    target_schema_text = paths["target_schema"].read_text(encoding="utf-8")
    judge_schema_text = paths["judge_schema"].read_text(encoding="utf-8")

    benchmark = parsed["benchmark"]
    manifest = parsed["manifest"]
    craft = parsed["craft"]
    taxonomy = parsed["taxonomy"]
    owner_state = parsed["owner_state"]
    judge_state = parsed["judge_state"]
    sequestered = parsed["sequestered"]
    pilot_eval_unit = parsed["pilot_eval_unit"]
    post_vote_owner = parsed["post_vote_owner"]
    pilots = [parsed["pilot_1"], parsed["pilot_2"], parsed["pilot_3"]]

    # Frozen construct and architecture boundaries.
    for term in [
        "OWNER_PRODUCT_FIT", "BOTH_FAIL", "SHADOW_ONLY", "FUNCTION_CLIP",
        "SECTION_SENTINEL", "EPISODE_SENTINEL", "SEQUESTERED", "root_cause",
    ]:
        if term not in contract:
            errors.append(f"contract missing frozen Benchmark V1 concept: {term}")

    for phrase in [
        "defect taxonomy before the vote",
        "first-pass preference is recorded and frozen",
        "FoC is hidden from the primary vote",
        "SHADOW_ONLY",
        "The public repo contains only",
    ]:
        if phrase not in protocol:
            errors.append(f"protocol missing freeze/isolation invariant: {phrase}")

    if "schemas/output-quality.schema.json` is deprecated" not in start:
        errors.append("Phase 1 START does not explicitly deprecate the monolithic output schema")

    # Pairwise preference must be holistic and preference-first.
    for term in ["BOTH_FAIL", "confidence", "preference_frozen", "blind_to_reference", "LLM_SHADOW_JUDGE"]:
        if term not in pairwise_schema_text:
            errors.append(f"pairwise preference schema missing {term}")
    for legacy_field in ['"pairwise_criteria"', '"continue"', '"movement"', '"payoff"', '"target_gap"', '"absolute_gates"']:
        if legacy_field in pairwise_schema_text:
            errors.append(f"pairwise preference schema still embeds legacy/other-lane field {legacy_field}")

    # Failure signature is output-side only and supports macro scope/unresolved diagnostics.
    for term in ["SPAN", "MULTI_SPAN", "UNIT_GLOBAL", "UNRESOLVED", '"root_cause"', '"type": "null"']:
        if term not in failure_schema_text:
            errors.append(f"failure-signature schema missing {term}")
    for forbidden in ["planner_fault", "writer_fault", "suspect_upstream_regions"]:
        if forbidden in failure_schema_text:
            errors.append(f"failure-signature schema contains upstream blame field: {forbidden}")

    expected_families = {
        "NARRATIVE_FUNCTION", "EXPOSITION_LOAD", "SPOKEN_COMPREHENSION",
        "GROUNDING_SPECIFICITY", "VOICE_STANCE", "REDUNDANCY",
    }
    taxonomy_families = set(taxonomy.get("families", {}).keys())
    if taxonomy_families != expected_families:
        errors.append(f"taxonomy families differ from frozen six-family set: {sorted(taxonomy_families)}")
    if taxonomy.get("status") != "FROZEN_FOR_PILOT":
        errors.append("taxonomy is not marked FROZEN_FOR_PILOT")

    # Evaluation unit primitive and three granularities.
    eval_schema_text = paths["eval_unit_schema"].read_text(encoding="utf-8")
    for granularity in ["FUNCTION_CLIP", "SECTION_SENTINEL", "EPISODE_SENTINEL"]:
        if granularity not in eval_schema_text:
            errors.append(f"eval-unit schema missing granularity {granularity}")
    if pilot_eval_unit.get("granularity") != "FUNCTION_CLIP":
        errors.append("pilot evaluation unit is not FUNCTION_CLIP")

    # Truth semantic audit.
    for term in [
        "IMPLIED_PREMISE", "CAUSAL", "VERIFIABLE", "PARTLY_VERIFIABLE",
        "SUPPORTS", "QUALIFIES", "CONFLICTS", "ABSENT", "release_blocker",
        "P01_HISTORICAL_AUTHORITY_ONLY_NO_CRAFT_REFERENCES",
    ]:
        if term not in truth_schema_text:
            errors.append(f"truth schema missing semantic audit concept: {term}")
    if "CRAFT_ONLY_NOT_TRUTH" in truth_schema_text:
        errors.append("truth schema unexpectedly admits craft-reference authority")

    # Spoken lane evidence levels.
    for term in ["TEXT_PREDICTION", "AUDIO_OBSERVATION", "LISTENER_REPORT"]:
        if term not in spoken_schema_text:
            errors.append(f"spoken schema missing evidence mode {term}")

    # Target gap must remain post-vote, function-based, and non-stylistic.
    for term in [
        "product_preference_frozen", "reference_visible_during_primary_vote",
        "CRAFT_ONLY_NOT_TRUTH", "matched_editorial_function",
        "style_similarity_used_as_score", "imitation_risk",
        "retroactive_preference_change",
    ]:
        if term not in target_schema_text:
            errors.append(f"target-gap schema missing {term}")

    # LLM judge is shadow-only at architecture freeze.
    for term in [
        "SHADOW_ONLY", "owner_agreement", "position_reversal_consistency",
        "duplicate_consistency", "evidence_span_validity", "abstention_rate",
        "eligible_for_optimization_loop",
    ]:
        if term not in judge_schema_text:
            errors.append(f"judge reliability schema missing {term}")
    if judge_state.get("mode") != "SHADOW_ONLY" or judge_state.get("eligible_for_optimization_loop") is not False:
        errors.append("current judge state is not SHADOW_ONLY / ineligible")
    if judge_state.get("pre_registered_tolerance_ref") is not None:
        warnings.append("Judge tolerance is populated; verify it was pre-registered before sequestered labels were opened.")

    # Historical P01 material in this public repo must all be DEV.
    samples = benchmark.get("samples", [])
    ids = [s.get("id") for s in samples]
    if len(ids) != len(set(ids)):
        errors.append("duplicate benchmark sample ids")
    for sample in samples:
        if sample.get("partition") != "DEV":
            errors.append(f"public historical P01 sample is not DEV: {sample.get('id')} -> {sample.get('partition')}")

    for pair in benchmark.get("pilot_pairs", []):
        if pair.get("left") not in ids or pair.get("right") not in ids:
            errors.append(f"pilot pair references unknown sample: {pair.get('pair_id')}")

    if benchmark.get("calibration_plan", {}).get("status") != "NOT_POPULATED":
        errors.append("fresh calibration corpus is incorrectly marked populated during architecture freeze")
    agg = benchmark.get("aggregation_policy", {})
    if agg.get("global_quality_score") is not False or agg.get("bradley_terry_required") is not False or agg.get("elo_required") is not False:
        errors.append("Benchmark V1 aggregation policy reintroduced scalar/BT/Elo requirements")

    # Sequestered evidence must not be committed to the public repo.
    if sequestered.get("public_repo_contains_payload") is not False or sequestered.get("public_repo_contains_labels") is not False:
        errors.append("sequestered manifest claims private payload/labels are present in public repo")
    if sequestered.get("status") != "NOT_CREATED_PRIVATE_PAYLOAD":
        warnings.append("Private sequestered set status changed; verify no payload/labels entered the public repository.")

    # Primary owner packets contain only first-pass material; post-vote prompts live separately.
    expected_post_vote_ref = "benchmarks/p01/calibration/post-vote-owner-diagnostics.json"
    for packet in pilots:
        packet_id = packet.get("packet_id", "UNKNOWN")
        if packet.get("role") != "PILOT_ONLY_NOT_CALIBRATION_EVIDENCE":
            errors.append(f"{packet_id} is not explicitly PILOT_ONLY_NOT_CALIBRATION_EVIDENCE")
        if packet.get("eval_unit_id") != pilot_eval_unit.get("eval_unit_id"):
            errors.append(f"{packet_id} references unexpected eval_unit_id")
        first = packet.get("first_pass", {})
        if "BOTH_FAIL" not in first.get("allowed_results", []):
            errors.append(f"{packet_id} does not offer BOTH_FAIL")
        if set(first.get("confidence_options", [])) != {"LOW", "MEDIUM", "HIGH"}:
            errors.append(f"{packet_id} confidence options are incomplete")
        if "freeze" not in str(first.get("freeze_rule", "")).lower() and "không sửa" not in str(first.get("freeze_rule", "")).lower():
            errors.append(f"{packet_id} does not make first-pass freeze explicit")
        if packet.get("post_vote_artifact_ref") != expected_post_vote_ref:
            errors.append(f"{packet_id} does not reference the separate post-vote diagnostic artifact")
        if "post_vote_optional" in packet or "optional_feedback_prompts" in packet:
            errors.append(f"{packet_id} embeds post-vote prompts in the first-pass packet")
        packet_text = json.dumps(packet, ensure_ascii=False).lower()
        for leak in ["craft_reference", "foc_reference", "historical_verdict", "intended_winner", "writer_process", "planner_process"]:
            if leak in packet_text:
                errors.append(f"{packet_id} contains forbidden reviewer metadata token {leak}")

    if post_vote_owner.get("visibility_gate") != "ONLY_AFTER_PAIRWISE_PREFERENCE_FROZEN":
        errors.append("post-vote owner diagnostics are not gated after preference freeze")
    if post_vote_owner.get("allow_unresolved") is not True:
        errors.append("post-vote owner diagnostics do not permit unresolved taxonomy mapping")

    if owner_state.get("status") != "PILOT_READY_NOT_CALIBRATION":
        errors.append("owner state is not PILOT_READY_NOT_CALIBRATION")
    if set(owner_state.get("allowed_owner_results", [])) != {"A", "B", "TIE", "BOTH_FAIL", "UNCERTAIN"}:
        errors.append("owner state allowed results do not match frozen preference enum")
    shadow_policy = owner_state.get("shadow_judge_policy", {})
    if shadow_policy.get("mode") != "SHADOW_ONLY" or shadow_policy.get("may_drive_optimization") is not False:
        errors.append("owner state does not enforce shadow-only judge policy")

    # Source manifest and craft-only boundary.
    manifest_samples = {x["sample_id"]: x for x in manifest.get("product_samples", [])}
    for sid in ids:
        if sid not in manifest_samples:
            errors.append(f"sample {sid} missing from source manifest")
    for item in manifest.get("product_samples", []):
        if not str(item.get("benchmark_role", "")).startswith("DEV"):
            errors.append(f"source manifest exposes non-DEV public P01 role: {item.get('sample_id')}")

    craft_sources = {x["source_id"]: x for x in manifest.get("craft_sources", [])}
    for source in craft_sources.values():
        if source.get("authority") != "CRAFT_ONLY_NOT_TRUTH":
            errors.append(f"craft source {source.get('source_id')} not marked CRAFT_ONLY_NOT_TRUTH")
        source_path = ROOT / source["locator"]
        if not source_path.exists():
            errors.append(f"craft source file missing: {source['locator']}")
        elif source.get("git_blob_sha1") and git_blob_sha1(source_path) != source["git_blob_sha1"]:
            errors.append(f"craft source blob identity changed: {source['source_id']}")

    excerpts = craft.get("excerpts", [])
    episodes = {x.get("episode") for x in excerpts}
    if not 6 <= len(excerpts) <= 10:
        errors.append(f"craft corpus should contain 6-10 excerpts, found {len(excerpts)}")
    if len(episodes) < 2:
        errors.append("craft corpus needs at least two episodes")
    for ex in excerpts:
        source_id = ex.get("source_ref")
        if source_id not in craft_sources:
            errors.append(f"excerpt {ex.get('id')} references unknown craft source {source_id}")
            continue
        text = (ROOT / craft_sources[source_id]["locator"]).read_text(encoding="utf-8-sig")
        start_anchor, end_anchor = ex.get("start_anchor", ""), ex.get("end_anchor", "")
        if not start_anchor or start_anchor not in text:
            errors.append(f"excerpt {ex.get('id')} start anchor not found")
        if not end_anchor or end_anchor not in text:
            errors.append(f"excerpt {ex.get('id')} end anchor not found")
        if start_anchor in text and end_anchor in text and text.index(start_anchor) > text.index(end_anchor):
            errors.append(f"excerpt {ex.get('id')} anchor order invalid")

    deprecated_schema = parsed["legacy_output_schema"]
    if deprecated_schema.get("deprecated") is not True:
        errors.append("legacy schemas/output-quality.schema.json is not marked deprecated")

    if errors:
        status, exit_code = "NOT_READY", 1
    else:
        status, exit_code = "ARCHITECTURE_FROZEN_READY_FOR_PILOT", 0
        warnings.extend([
            "Pilot packets use historical DEV prose and cannot establish benchmark validity.",
            "Fresh calibration corpus has not been collected.",
            "No private/restricted sequestered payload exists yet.",
            "LLM judge remains SHADOW_ONLY and unvalidated.",
            "Structural verification cannot establish aesthetic validity, owner calibration validity, spoken quality, or transfer."
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
        "measurement_surfaces": [
            "EVALUATION_UNIT", "PRODUCT_PREFERENCE", "FAILURE_SIGNATURE",
            "TRUTH", "SPOKEN", "TARGET_GAP", "JUDGE_RELIABILITY",
        ],
        "phase1_complete": False,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
