#!/usr/bin/env python3
"""Structural verifier for Phase 1 benchmark readiness.

This verifier can establish artifact consistency and dispatch readiness. It cannot
certify aesthetic validity, owner alignment, audio quality, or held-out transfer.
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
        "quality_schema": ROOT / "schemas/output-quality.schema.json",
        "decision_schema": ROOT / "schemas/decision-record.schema.json",
        "worker_schema": ROOT / "schemas/phase1-worker-iteration.schema.json",
        "benchmark": ROOT / "benchmarks/p01/benchmark-set.json",
        "manifest": ROOT / "benchmarks/p01/source-manifest.json",
        "craft": ROOT / "benchmarks/p01/craft-corpus.json",
        "owner_cal": ROOT / "benchmarks/p01/owner-calibration.json",
        "legacy_readme": ROOT / "benchmarks/p01/evaluations/README.md",
        "worker_loop": ROOT / "docs/phase1/WORKER-LOOP.md",
        "work_order": ROOT / "docs/phase1/ITERATION-01-WORK-ORDER.md",
    }
    for name, path in paths.items():
        if not path.exists():
            errors.append(f"missing required artifact: {name} -> {path.relative_to(ROOT)}")

    if errors:
        print(json.dumps({"status": "NOT_READY", "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    contract = paths["contract"].read_text(encoding="utf-8")
    schema_text = paths["quality_schema"].read_text(encoding="utf-8")
    benchmark = load_json(paths["benchmark"])
    manifest = load_json(paths["manifest"])
    craft = load_json(paths["craft"])
    owner_cal = load_json(paths["owner_cal"])
    load_json(paths["quality_schema"])
    load_json(paths["decision_schema"])
    load_json(paths["worker_schema"])

    # Contract regression checks: no known overfit/scalar shortcuts from v1.0.
    forbidden_contract_fragments = [
        "15 - 25 âm tiết",
        "dài quá 40 từ",
        "NEAR`: Đã đạt",
        "MODERATE`: Mạch truyện",
        "Mỗi đoạn kết thúc đều để lại",
        "giải quyết trọn vẹn nghịch lý thị giác",
    ]
    for frag in forbidden_contract_fragments:
        if frag in contract:
            errors.append(f"contract retains uncalibrated/overfit rule: {frag!r}")

    required_contract_terms = [
        "anonymized pairwise preference",
        "DEFECT",
        "TEXT_PREDICTION",
        "DEV",
        "CALIBRATION",
        "HOLDOUT",
    ]
    upper_contract = contract.upper()
    for term in required_contract_terms:
        if term.upper() not in upper_contract:
            errors.append(f"contract missing required design concept: {term}")

    # Schema must separate pairwise results, defects and diagnostic hypotheses.
    for term in ["pairwise_criteria", "defect_annotations", "spoken_comprehension", "diagnostic_hypothesis"]:
        if term not in schema_text:
            errors.append(f"quality schema missing {term}")
    if "suspect_upstream_regions" in schema_text:
        errors.append("failure signature still embeds upstream blame")

    # Benchmark partitions and aliases.
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
        alias = str(sample.get("reviewer_alias", ""))
        if not re.fullmatch(r"PX-\d{2}", alias):
            errors.append(f"reviewer alias leaks semantics or has unexpected format: {alias}")
    if not all(partitions.values()):
        errors.append("DEV/CALIBRATION/HOLDOUT must all be non-empty")
    if partitions["DEV"] & partitions["CALIBRATION"] or partitions["DEV"] & partitions["HOLDOUT"] or partitions["CALIBRATION"] & partitions["HOLDOUT"]:
        errors.append("dataset partitions overlap")

    # Calibration labels: real owner preference must not be fabricated.
    for pair in benchmark.get("calibration_pairs", []):
        pair_id = pair.get("pair_id", "")
        left, right = pair.get("left"), pair.get("right")
        if left not in partitions["CALIBRATION"] or right not in partitions["CALIBRATION"]:
            errors.append(f"calibration pair {pair_id} references non-calibration sample")
        same = left == right
        label = pair.get("owner_label")
        if same:
            if label != "TIE_EXPECTED_CONTROL":
                errors.append(f"same-text control {pair_id} missing mechanical tie expectation")
        elif label is not None:
            errors.append(f"owner preference appears fabricated/pre-filled for {pair_id}")

    holdout = benchmark.get("holdout_policy", {})
    if not isinstance(holdout.get("scored"), bool):
        errors.append("holdout scored flag must be boolean")
    if holdout.get("exposed_to_contract_tuning") is not False:
        errors.append("holdout is exposed to contract tuning")

    # Source manifest consistency and craft-only boundary.
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

    # Craft corpus coverage and exact anchor validity.
    excerpts = craft.get("excerpts", [])
    if not 6 <= len(excerpts) <= 10:
        errors.append(f"craft corpus should contain 6-10 excerpts, found {len(excerpts)}")
    episodes = {x.get("episode") for x in excerpts}
    if len(episodes) < 2:
        errors.append("craft corpus needs at least two episodes")
    required_functions = {"opening_investigation", "mechanism_explanation", "scale_change", "uncertainty", "transition", "local_payoff"}
    observed_functions = {f for x in excerpts for f in x.get("functions", [])}
    missing_functions = required_functions - observed_functions
    if missing_functions:
        errors.append(f"craft corpus missing functions: {sorted(missing_functions)}")
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
        if ex.get("medium") == "AUDIO_VERIFIED" and not ex.get("audio_start"):
            errors.append(f"excerpt {ex.get('id')} claims audio verification without timestamp")

    # Owner calibration state: no aesthetic self-certification.
    non_control = [p for p in owner_cal.get("pairs", []) if "DUP" not in p.get("pair_id", "")]
    real_owner_labels = [p for p in non_control if p.get("owner_result") in {"A", "B", "TIE", "UNCERTAIN"}]
    judge_runs_complete = bool(non_control) and all(p.get("judge_runs") and p.get("position_control_complete") is True for p in non_control)
    human_calibrated = len(real_owner_labels) == len(non_control) and judge_runs_complete

    # Legacy v1.0 evaluations must be explicitly quarantined.
    legacy_note = paths["legacy_readme"].read_text(encoding="utf-8")
    if "NOT" not in legacy_note or "gold" not in legacy_note.lower():
        errors.append("legacy evaluation quarantine is not explicit")

    if errors:
        status = "NOT_READY"
        exit_code = 1
    elif human_calibrated and holdout.get("scored") is True:
        status = "READY_FOR_EXIT_REVIEW"
        exit_code = 0
    else:
        status = "READY_FOR_HUMAN_CALIBRATION"
        exit_code = 0
        if not human_calibrated:
            warnings.append("Owner/judge calibration is not completed; Phase 1 cannot close.")
        if holdout.get("scored") is False:
            warnings.append("Holdout transfer is intentionally unscored; Phase 1 cannot close.")

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
        "limitations": [
            "Structural verification does not prove aesthetic validity.",
            "Transcript-only craft references do not establish audio listenability.",
            "Human preference calibration and held-out transfer remain external evidence gates."
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
