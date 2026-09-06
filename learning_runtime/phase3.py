from __future__ import annotations

import argparse
import json
from pathlib import Path

from .run import REPO_ROOT, run_scenario
from .whitebox import diagnose_failure, write_trace


def _load_json(ref: str) -> dict:
    return json.loads((REPO_ROOT / ref).read_text(encoding="utf-8"))


def run_phase3(name: str, out_dir: Path, force: bool = False) -> dict:
    spec_path = Path(__file__).resolve().parent / "scenarios" / f"{name}.phase3.json"
    if not spec_path.exists():
        raise FileNotFoundError(f"unknown phase3 scenario: {name}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    base = run_scenario(spec["base_scenario"], out_dir, force=force)
    plan = _load_json(spec["plan_ref"])
    writer_report = _load_json(spec["writer_report_ref"])
    failure = _load_json(spec["failure_ref"])
    diagnosis = diagnose_failure(plan=plan, writer_report=writer_report, failure=failure)

    plan_events = [e for e in diagnosis.observations if e["kind"] in {"PLAN_MAPPING", "PLAN_SYMPTOM_OBSERVATION"}]
    write_events = [e for e in diagnosis.observations if e["kind"] in {"OUTPUT_FAILURE", "WRITER_MAPPING", "REALIZATION_ALIGNMENT"}]
    write_trace(out_dir / "plan" / "trace.jsonl", plan_events)
    write_trace(out_dir / "write" / "trace.jsonl", write_events)

    diagnosis_payload = {
        "phase": 3,
        "scenario": name,
        "failure_id": diagnosis.failure_id,
        "beat_id": diagnosis.beat_id,
        "classification": diagnosis.classification,
        "confidence": diagnosis.confidence,
        "observations": diagnosis.observations,
        "root_cause_status": "BOUNDED_REGION_NOT_FINAL_CAUSAL_PROOF",
        "next_intervention_ref": spec["intervention_ref"],
    }
    (out_dir / "diagnosis.json").write_text(json.dumps(diagnosis_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "runtime_version": "0.2.0",
        "phase": 3,
        "scenario": name,
        "base_run_id": base["run_id"],
        "status": "WHITEBOX_TRACE_COMPLETE",
        "diagnosis": diagnosis.classification,
        "diagnosis_confidence": diagnosis.confidence,
        "trace_files": ["plan/trace.jsonl", "write/trace.jsonl"],
        "diagnosis_file": "diagnosis.json",
        "intervention_ref": spec["intervention_ref"],
        "live_rerun_status": "NOT_EXECUTED_NO_LIVE_AGENT_ADAPTER",
    }
    (out_dir / "phase3-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 3 white-box MVP")
    parser.add_argument("scenario", help="phase3 scenario name, e.g. p01-rootcause-01")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    manifest = run_phase3(args.scenario, args.out, force=args.force)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
