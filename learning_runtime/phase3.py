from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .artifacts import artifact_identity, snapshot_file, verify_artifact_identity, write_json
from .run import REPO_ROOT, run_scenario
from .whitebox import Diagnosis, EvidenceError, diagnose_failure, write_trace


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _new_run_id(name: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"phase3-{name}-{stamp}-{uuid.uuid4().hex[:8]}"


def _snapshot_inputs(spec: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    snapshot_dir = out_dir / "input-snapshot"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    refs = {
        "plan": spec["plan_ref"],
        "writer_report": spec["writer_report_ref"],
        "failure": spec["failure_ref"],
        "intervention": spec["intervention_ref"],
    }
    identities: dict[str, Any] = {}
    for key, ref in refs.items():
        source = REPO_ROOT / ref
        destination = snapshot_dir / ("plan.json" if key == "plan" else f"{key.replace('_', '-')}.json")
        identities[key] = {
            "source_ref": ref,
            **snapshot_file(source, destination),
            "snapshot_ref": str(destination.relative_to(out_dir)),
        }

    candidate_source = out_dir / "write" / "output.md"
    candidate_destination = snapshot_dir / "candidate.md"
    identities["candidate"] = {
        "source_ref": "write/output.md",
        **snapshot_file(candidate_source, candidate_destination),
        "snapshot_ref": str(candidate_destination.relative_to(out_dir)),
    }
    return identities


def _update_trace_manifests(out_dir: Path, trace_paths: dict[str, Path]) -> None:
    root_manifest_path = out_dir / "manifest.json"
    root = _load_json(root_manifest_path)
    node_by_stage = {node["stage"]: node for node in root.get("nodes", [])}
    for stage, trace_path in trace_paths.items():
        manifest_path = out_dir / stage / "manifest.json"
        manifest = _load_json(manifest_path)
        manifest["runtime_phase"] = 3
        manifest["trace_available"] = True
        manifest["trace_file"] = trace_path.name
        manifest["trace_identity"] = artifact_identity(trace_path)
        manifest_sha = write_json(manifest_path, manifest)
        if stage in node_by_stage:
            node_by_stage[stage]["manifest_sha256"] = manifest_sha
    root["phase"] = 3
    root["phase3_ready_surface"]["white_box_trace"] = True
    write_json(root_manifest_path, root)


def _write_bundle(out_dir: Path, paths: list[Path], metadata: dict[str, Any]) -> dict[str, Any]:
    artifacts: dict[str, Any] = {}
    for path in paths:
        if path.exists():
            artifacts[str(path.relative_to(out_dir))] = artifact_identity(path)
    bundle = {
        "schema_version": "1.0.0",
        "metadata": metadata,
        "artifacts": artifacts,
        "self_hash_policy": "bundle.json is intentionally excluded to avoid circular self-reference",
    }
    write_json(out_dir / "bundle.json", bundle)
    return bundle


def verify_run_bundle(out_dir: Path) -> dict[str, Any]:
    bundle_path = out_dir / "bundle.json"
    if not bundle_path.exists():
        return {"status": "INVALID", "errors": [{"code": "BUNDLE_MISSING", "artifact": "bundle.json"}]}
    bundle = _load_json(bundle_path)
    errors: list[dict[str, Any]] = []
    normalized_matches: list[str] = []
    for rel, expected in bundle.get("artifacts", {}).items():
        rel_path = Path(rel)
        if rel_path.is_absolute() or ".." in rel_path.parts:
            errors.append({"code": "UNSAFE_BUNDLE_PATH", "artifact": rel})
            continue
        path = out_dir / rel_path
        if not path.exists():
            errors.append({"code": "BUNDLE_ARTIFACT_MISSING", "artifact": rel})
            continue
        result = verify_artifact_identity(path, expected)
        if result["status"] == "CONTENT_MISMATCH":
            errors.append({"code": "BUNDLE_ARTIFACT_CHANGED", "artifact": rel, "expected": expected, "observed": result["observed"]})
        elif result["status"] == "TEXT_MATCH_RAW_DIFF_ALLOWED_NORMALIZATION":
            normalized_matches.append(rel)
    return {
        "status": "VALID" if not errors else "INVALID",
        "errors": errors,
        "normalized_text_matches": normalized_matches,
        "artifact_count": len(bundle.get("artifacts", {})),
    }


def _diagnosis_payload(name: str, diagnosis: Diagnosis, identities: dict[str, Any], intervention_ref: str) -> dict[str, Any]:
    return {
        "phase": 3,
        "scenario": name,
        "status": "VALIDATED_MAPPING_WITH_BOUNDED_ATTRIBUTION",
        "failure_id": diagnosis.failure_id,
        "beat_id": diagnosis.beat_id,
        "mapping_status": diagnosis.mapping_status,
        "mapping_confidence": diagnosis.mapping_confidence,
        "attribution_status": diagnosis.attribution_status,
        "classification": diagnosis.classification,
        "attribution_confidence": diagnosis.confidence,
        "suspected_regions": diagnosis.suspected_regions,
        "observations": diagnosis.observations,
        "limitations": diagnosis.limitations,
        "input_identities": identities,
        "root_cause_status": "BOUNDED_HYPOTHESIS_NOT_CAUSAL_PROOF",
        "next_intervention_ref": intervention_ref,
    }


def run_phase3(name: str, out_dir: Path, force: bool = False) -> dict[str, Any]:
    spec_path = Path(__file__).resolve().parent / "scenarios" / f"{name}.phase3.json"
    if not spec_path.exists():
        raise FileNotFoundError(f"unknown phase3 scenario: {name}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    run_id = _new_run_id(name)
    base = run_scenario(spec["base_scenario"], out_dir, force=force, run_id_override=run_id, runtime_phase=3)
    identities = _snapshot_inputs(spec, out_dir)

    snapshot_dir = out_dir / "input-snapshot"
    candidate_text = (snapshot_dir / "candidate.md").read_text(encoding="utf-8-sig")
    plan = _load_json(snapshot_dir / "plan.json")
    writer_report = _load_json(snapshot_dir / "writer-report.json")
    failure = _load_json(snapshot_dir / "failure.json")

    try:
        diagnosis = diagnose_failure(candidate_text=candidate_text, plan=plan, writer_report=writer_report, failure=failure)
        diagnosis_payload = _diagnosis_payload(name, diagnosis, identities, spec["intervention_ref"])
        plan_events = [e for e in diagnosis.observations if e["kind"].startswith("PLAN_") or e["kind"] == "BOUNDED_ATTRIBUTION"]
        write_events = [e for e in diagnosis.observations if e["kind"].startswith("WRITER_") or e["kind"] == "OUTPUT_IDENTITY_AND_SPAN"]
        plan_trace = out_dir / "plan" / "trace.jsonl"
        write_trace_path = out_dir / "write" / "trace.jsonl"
        write_trace(plan_trace, plan_events)
        write_trace(write_trace_path, write_events)
        _update_trace_manifests(out_dir, {"plan": plan_trace, "write": write_trace_path})
        status = "WHITEBOX_TRACE_COMPLETE"
    except EvidenceError as exc:
        diagnosis_payload = {
            "phase": 3,
            "scenario": name,
            "status": "INVALID_EVIDENCE",
            "error": exc.as_dict(),
            "input_identities": identities,
            "root_cause_status": "NOT_AVAILABLE_INVALID_EVIDENCE",
        }
        status = "INVALID_EVIDENCE"

    diagnosis_path = out_dir / "diagnosis.json"
    write_json(diagnosis_path, diagnosis_payload)
    phase3_manifest = {
        "runtime_version": "0.3.0",
        "phase": 3,
        "scenario": name,
        "run_id": run_id,
        "source_commit": base.get("source_commit"),
        "base_run_id": base["run_id"],
        "status": status,
        "mapping_status": diagnosis_payload.get("mapping_status"),
        "attribution": diagnosis_payload.get("classification"),
        "mapping_confidence": diagnosis_payload.get("mapping_confidence"),
        "attribution_confidence": diagnosis_payload.get("attribution_confidence"),
        "trace_files": ["plan/trace.jsonl", "write/trace.jsonl"] if status == "WHITEBOX_TRACE_COMPLETE" else [],
        "diagnosis_file": "diagnosis.json",
        "intervention_ref": spec["intervention_ref"],
        "live_rerun_status": "NOT_EXECUTED_BY_PHASE3_TRACE_COMMAND",
        "input_snapshot": {k: v["snapshot_ref"] for k, v in identities.items()},
    }
    phase3_manifest_path = out_dir / "phase3-manifest.json"
    write_json(phase3_manifest_path, phase3_manifest)

    critical = [
        out_dir / "manifest.json",
        out_dir / "plan" / "manifest.json",
        out_dir / "write" / "manifest.json",
        out_dir / "truth" / "manifest.json",
        out_dir / "product" / "manifest.json",
        diagnosis_path,
        phase3_manifest_path,
        *snapshot_dir.glob("*"),
    ]
    if status == "WHITEBOX_TRACE_COMPLETE":
        critical.extend([out_dir / "plan" / "trace.jsonl", out_dir / "write" / "trace.jsonl"])
    _write_bundle(out_dir, critical, {"run_id": run_id, "source_commit": base.get("source_commit"), "runtime_version": "0.3.0"})
    phase3_manifest["bundle_verification"] = verify_run_bundle(out_dir)
    write_json(phase3_manifest_path, phase3_manifest)
    # phase3-manifest changed after the first bundle write; refresh bundle once, excluding bundle itself.
    _write_bundle(out_dir, critical, {"run_id": run_id, "source_commit": base.get("source_commit"), "runtime_version": "0.3.0"})
    return phase3_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 3 white-box MVP")
    parser.add_argument("scenario", nargs="?", help="phase3 scenario name, e.g. p01-rootcause-01")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--verify-run", type=Path, help="verify hashes/provenance for an existing frozen run bundle")
    args = parser.parse_args()

    if args.verify_run:
        result = verify_run_bundle(args.verify_run)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if result["status"] == "VALID" else 1
    if not args.scenario or not args.out:
        parser.error("scenario and --out are required unless --verify-run is used")
    manifest = run_phase3(args.scenario, args.out, force=args.force)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0 if manifest["status"] == "WHITEBOX_TRACE_COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
