#!/usr/bin/env python3
"""Structural verifier for Phase 1 benchmark readiness.

This verifier establishes artifact consistency and dispatch readiness only. It
cannot certify aesthetic validity, owner alignment, audio quality, or transfer.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re

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
        "product_schema": ROOT / "schemas/output-quality.schema.json",
        "truth_schema": ROOT / "schemas/truth-gate.schema.json",
        "target_schema": ROOT / "schemas/target-gap.schema.json",
        "decision_schema": ROOT / "schemas/decision-record.schema.json",
        "worker_schema": ROOT / "schemas/phase1-worker-iteration.schema.json",
        "benchmark": ROOT / "benchmarks/p01/benchmark-set.json",
        "manifest": ROOT / "benchmarks/p01/source-manifest.json",
        "craft": ROOT / "benchmarks/p01/craft-corpus.json",
        "owner_cal": ROOT / "benchmarks/p01/owner-calibration.json",
        "legacy_readme": ROOT / "benchmarks/p01/evaluations/README.md",
        "worker_loop": ROOT / "docs/phase1/WORKER-LOOP.md",
        "iteration_1": ROOT / "benchmarks/p01/iterations/iteration-01.json",
    }
    for name, path in paths.items():
        if not path.exists():
            errors.append(f"missing required artifact: {name} -> {path.relative_to(ROOT)}")

    if errors:
        print(json.dumps({"status": "NOT_READY", "structural_errors": errors}, ensure_ascii=False, indent=2))
        return 1

    contract = paths["contract"].read_text(encoding="utf-8")
    protocol = paths["protocol"].read_text(encoding="utf-8")
    product_schema_text = paths["product_schema"].read_text(encoding="utf-8")
    truth_schema_text = paths["truth_schema"].read_text(encoding="utf-8")
    target_schema_text = paths["target_schema"].read_text(encoding="utf-8")
    benchmark = load_json(paths["benchmark"])
    manifest = load_json(paths["manifest"])
    craft = load_json(paths["craft"])
    owner_cal = load_json(paths["owner_cal"])
    for p in ["product_schema", "truth_schema", "target_schema", "decision_schema", "worker_schema", "iteration_1"]:
        load_json(paths[p])

    # Contract regression checks.
    for frag in [
        "15 - 25 âm tiết", "dài quá 40 từ", "NEAR`: Đã đạt",
        "MODERATE`: Mạch truyện", "Mỗi đoạn kết thúc đều để lại",
        "giải quyết trọn vẹn nghịch lý thị giác",
    ]:
        if frag in contract:
            errors.append(f"contract retains uncalibrated/overfit rule: {frag!r}")
    for term in ["pairwise", "TEXT_PREDICTION", "DEV", "CALIBRATION", "HOLDOUT", "failure signature"]:
        if term.upper() not in contract.upper():
            errors.append(f"contract missing required design concept: {term}")

    # Three-lane separation.
    for phrase in [
        "MUST NOT receive:\n\n- FoC or other craft-reference excerpts",
        "begins only AFTER Lane B pairwise preference has been frozen",
        "Lane A — Truth / scope gate",
        "Lane B — Product pairwise preference",
        "Lane C — Target-gap analysis",
    ]:
        if phrase not in protocol:
            errors.append(f"protocol missing measurement-lane invariant: {phrase}")

    if "absolute_gates" in product_schema_text or '"target_gap"' in product_schema_text:
        errors.append("Product pairwise schema still contains truth-gate or target-gap fields")
    for term in ["pairwise_criteria", "defect_annotations", "spoken_comprehension", '"A"', '"B"']:
        if term not in product_schema_text:
            errors.append(f"Product pairwise schema missing {term}")
    if "TRUTH|" in product_schema_text or "suspect_upstream_regions" in product_schema_text:
        errors.append("Product output still embeds truth taxonomy or upstream blame")

    if "P01_HISTORICAL_AUTHORITY_ONLY_NO_CRAFT_REFERENCES" not in truth_schema_text:
        errors.append("Truth schema does not enforce the no-craft-reference authority boundary")
    if "CRAFT_ONLY_NOT_TRUTH" in truth_schema_text:
        errors.append("Truth schema unexpectedly includes craft-reference authority")

    for term in ["CRAFT_ONLY_NOT_TRUTH", "matched_function", "product_evaluation_frozen", "remaining_gaps", "medium_limitation"]:
        if term not in target_schema_text:
            errors.append(f"Target-gap schema missing {term}")

    # Benchmark partitions and reviewer aliases.
    samples = benchmark.get("samples", [])
    ids = [s.get("id") for s in samples]
    aliases = [s.get("reviewer_alias") for s in samples]
    if len(ids) != len(set(ids)):
        errors.append("duplicate benchmark sample ids")
    if len(aliases) != len(set(aliases)):
        errors.append("duplicate reviewer aliases")
    partitions = {"DEV": set(), "CALIBRATION": set(), "HOLDOUT": set()}
    for sample in samples:
        part = sample.get("partition")
        if part not in partitions:
            errors.append(f"sample {sample.get('id')} has invalid partition {part}")
            continue
        partitions[part].add(sample.get("id"))
        if not re.fullmatch(r"PX-\d{2}", str(sample.get("reviewer_alias", ""))):
            errors.append(f"reviewer alias leaks semantics or has unexpected format: {sample.get('reviewer_alias')}")
    if not all(partitions.values()):
        errors.append("DEV/CALIBRATION/HOLDOUT must all be non-empty")
    if any(partitions[a] & partitions[b] for a, b in [("DEV", "CALIBRATION"), ("DEV", "HOLDOUT"), ("CALIBRATION", "HOLDOUT")]):
        errors.append("dataset partitions overlap")

    # Calibration labels and controls.
    for pair in benchmark.get("calibration_pairs", []):
        pair_id = pair.get("pair_id", "")
        left, right = pair.get("left"), pair.get("right")
        if left not in partitions["CALIBRATION"] or right not in partitions["CALIBRATION"]:
            errors.append(f"calibration pair {pair_id} references non-calibration sample")
        if left == right:
            if pair.get("owner_label") != "TIE_EXPECTED_CONTROL":
                errors.append(f"same-text control {pair_id} missing mechanical tie expectation")
        elif pair.get("owner_label") is not None:
            errors.append(f"owner preference appears pre-filled for {pair_id}")

    holdout = benchmark.get("holdout_policy", {})
    if holdout.get("exposed_to_contract_tuning") is not False:
        errors.append("holdout is exposed to contract tuning")
    if holdout.get("reliability") != "FRESH_EXPOSED_NOT_BLIND":
        errors.append("holdout reliability must state FRESH_EXPOSED_NOT_BLIND while stored in shared repo")
    if holdout.get("access_enforcement") != "SHARED_REPO_NOT_SEQUESTERED":
        errors.append("holdout access limitation is not explicit")

    # Source manifest and craft-only boundary.
    manifest_samples = {x["sample_id"]: x for x in manifest.get("product_samples", [])}
    for sid in ids:
        if sid not in manifest_samples:
            errors.append(f"sample {sid} missing from source manifest")
    craft_sources = {x["source_id"]: x for x in manifest.get("craft_sources", [])}
    for source in craft_sources.values():
        if source.get("authority") != "CRAFT_ONLY_NOT_TRUTH":
            errors.append(f"craft source {source.get('source_id')} not marked CRAFT_ONLY_NOT_TRUTH")
        source_path = ROOT / source["locator"]
        if not source_path.exists():
            errors.append(f"craft source file missing: {source['locator']}")
        elif source.get("git_blob_sha1") and git_blob_sha1(source_path) != source["git_blob_sha1"]:
            errors.append(f"craft source blob identity changed: {source['source_id']}")

    # Craft corpus coverage and anchors.
    excerpts = craft.get("excerpts", [])
    episodes = {x.get("episode") for x in excerpts}
    required_functions = {"opening_investigation", "mechanism_explanation", "scale_change", "uncertainty", "transition", "local_payoff"}
    observed_functions = {f for x in excerpts for f in x.get("functions", [])}
    if not 6 <= len(excerpts) <= 10:
        errors.append(f"craft corpus should contain 6-10 excerpts, found {len(excerpts)}")
    if len(episodes) < 2:
        errors.append("craft corpus needs at least two episodes")
    if required_functions - observed_functions:
        errors.append(f"craft corpus missing functions: {sorted(required_functions - observed_functions)}")
    for ex in excerpts:
        source_id = ex.get("source_ref")
        if source_id not in craft_sources:
            errors.append(f"excerpt {ex.get('id')} references unknown craft source {source_id}")
            continue
        text = (ROOT / craft_sources[source_id]["locator"]).read_text(encoding="utf-8-sig")
        start, end = ex.get("start_anchor", ""), ex.get("end_anchor", "")
        if not start or start not in text:
            errors.append(f"excerpt {ex.get('id')} start anchor not found")
        if not end or end not in text:
            errors.append(f"excerpt {ex.get('id')} end anchor not found")
        if start in text and end in text and text.index(start) > text.index(end):
            errors.append(f"excerpt {ex.get('id')} anchor order invalid")

    # Owner calibration remains an external gate.
    non_control = [p for p in owner_cal.get("pairs", []) if "DUP" not in p.get("pair_id", "")]
    real_owner_labels = [p for p in non_control if p.get("owner_result") in {"A", "B", "TIE", "UNCERTAIN"}]
    judge_runs_complete = bool(non_control) and all(p.get("judge_runs") and p.get("position_control_complete") is True for p in non_control)
    human_calibrated = len(real_owner_labels) == len(non_control) and judge_runs_complete

    legacy_note = paths["legacy_readme"].read_text(encoding="utf-8")
    if "NOT" not in legacy_note or "gold" not in legacy_note.lower():
        errors.append("legacy evaluation quarantine is not explicit")

    if errors:
        status, exit_code = "NOT_READY", 1
    elif human_calibrated and holdout.get("scored") is True:
        status, exit_code = "READY_FOR_EXIT_REVIEW", 0
    else:
        status, exit_code = "READY_FOR_HUMAN_CALIBRATION", 0
        if not human_calibrated:
            warnings.append("Owner/judge calibration is incomplete; Phase 1 cannot close.")
        if holdout.get("scored") is False:
            warnings.append("Fresh-exposed transfer sample remains unscored; Phase 1 cannot close.")

    result = {
        "status": status,
        "structural_errors": errors,
        "warnings": warnings,
        "counts": {
            "dev_samples": len(partitions["DEV"]),
            "calibration_samples": len(partitions["CALIBRATION"]),
            "holdout_samples": len(partitions["HOLDOUT"]),
            "calibration_pairs": len(benchmark.get("calibration_pairs", [])),
            "craft_excerpts": len(excerpts),
            "craft_episodes": len(episodes),
            "owner_labels_recorded": len(real_owner_labels),
            "owner_labels_required": len(non_control),
        },
        "measurement_lanes": ["TRUTH_GATE", "PRODUCT_PAIRWISE", "TARGET_GAP"],
        "limitations": [
            "Structural verification does not prove aesthetic validity.",
            "Transcript-only craft references do not establish audio listenability.",
            "Shared-repo holdout is fresh/exposed, not sequestered blind.",
            "Human preference calibration and transfer remain external evidence gates."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
