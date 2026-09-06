#!/usr/bin/env python3
"""Structural checks for the Phase 1 owner-guided review UX.

This does not certify product quality. It checks only separation and artifact shape.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    schema_path = ROOT / "schemas/owner-guided-review.schema.json"
    profile_path = ROOT / "benchmarks/p01/review-profiles/foc-functional-targets.json"
    session_path = ROOT / "benchmarks/p01/review-sessions/owner-pilot-01-guided.json"
    blind_packet_path = ROOT / "benchmarks/p01/calibration/owner-packets/owner-cal-01.json"

    for p in [schema_path, profile_path, session_path, blind_packet_path]:
        if not p.exists():
            errors.append(f"missing artifact: {p.relative_to(ROOT)}")

    if errors:
        print(json.dumps({"status": "NOT_READY", "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    session = json.loads(session_path.read_text(encoding="utf-8"))
    blind = json.loads(blind_packet_path.read_text(encoding="utf-8"))

    if session.get("mode") != "GUIDED_TARGET_DIAGNOSTIC":
        errors.append("guided session has wrong mode")
    if session.get("benchmark_evidence_eligible") is not False:
        errors.append("guided session must be benchmark_evidence_eligible=false")
    if session.get("session_summary", {}).get("scalar_score") is not None:
        errors.append("guided session introduced a scalar score")

    allowed_features = {
        "INFORMATION_RELEASE",
        "LISTENER_ORIENTATION",
        "FORWARD_PRESSURE",
        "CONCRETENESS_FUNCTION",
        "NARRATOR_STANCE",
        "LOCAL_TRANSFORMATION",
        "SPOKEN_LOAD",
    }
    target_ids = {x.get("target_id") for x in profile.get("targets", [])}

    for unit in session.get("micro_units", []):
        if not unit.get("source_locator"):
            errors.append(f"{unit.get('unit_id')} missing source_locator")
        if len(unit.get("feature_comparisons", [])) > 5:
            errors.append(f"{unit.get('unit_id')} has too many feature cards")
        for comp in unit.get("feature_comparisons", []):
            if comp.get("feature") not in allowed_features:
                errors.append(f"unknown guided feature: {comp.get('feature')}")
            if comp.get("target_behavior_ref") not in target_ids:
                errors.append(f"unknown target behavior ref: {comp.get('target_behavior_ref')}")

    blind_text = json.dumps(blind, ensure_ascii=False)
    for forbidden in [
        "MATCHES_TARGET",
        "MISSES_TARGET",
        "WRONG_TARGET",
        "INFORMATION_RELEASE",
        "NARRATOR_STANCE",
        "FOC-T-",
        "foc-functional-targets"
    ]:
        if forbidden in blind_text:
            errors.append(f"blind packet leaks guided-review material: {forbidden}")

    if profile.get("authority") != "CRAFT_ONLY_NOT_TRUTH":
        errors.append("guided target profile does not preserve craft-only authority")

    schema_text = json.dumps(schema, ensure_ascii=False)
    if '"scalar_score"' not in schema_text or '"const": false' not in schema_text:
        errors.append("guided schema does not enforce no-score/non-benchmark boundaries")

    result = {
        "status": "STRUCTURALLY_READY" if not errors else "NOT_READY",
        "errors": errors,
        "micro_units": len(session.get("micro_units", [])),
        "target_behaviors": len(profile.get("targets", [])),
        "limitations": [
            "Structural readiness does not validate owner preference or FoC target correctness.",
            "Guided results are diagnostic UX evidence only, not blind calibration evidence."
        ]
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
