#!/usr/bin/env python3
"""Validate the active guided-review artifact against its actual schema and sources."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from learning_runtime.feedback import validate_guided_artifact  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Phase 1/3 guided owner-review artifact")
    parser.add_argument(
        "--session",
        default="benchmarks/p01/review-sessions/owner-pilot-01-guided.json",
        help="repository-relative guided review session/comparison path",
    )
    args = parser.parse_args()
    session_path = ROOT / args.session
    if not session_path.exists():
        result = {"status": "NOT_READY", "errors": [f"missing session: {args.session}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    try:
        validation = validate_guided_artifact(session_path, root=ROOT)
    except Exception as exc:
        result = {"status": "NOT_READY", "session": args.session, "errors": [f"verifier exception: {type(exc).__name__}: {exc}"]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    errors = validation["errors"]
    result = {
        "status": "STRUCTURALLY_READY" if not errors else "NOT_READY",
        "session": args.session,
        "format": validation["format"],
        "errors": errors,
        "owner_measurement_pending": validation["owner_measurement_pending"],
        "measurement_claim": "AWAITING_OWNER" if validation["owner_measurement_pending"] else "MEASUREMENT_PRESENT_NOT_PROMOTED_TO_BLIND_EVIDENCE",
        "limitations": [
            "Schema/source validity does not establish aesthetic quality.",
            "Guided results remain diagnostic evidence only, never blind calibration evidence.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
