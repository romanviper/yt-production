from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from .artifacts import ArtifactStore
from .stages import STAGE_ORDER, run_stage, validate_scenario

REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = Path(__file__).resolve().parent / "scenarios"


def current_source_commit() -> str | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return proc.stdout.strip() or None


def load_scenario(name: str) -> dict[str, Any]:
    path = SCENARIO_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"unknown scenario: {name}")
    scenario = json.loads(path.read_text(encoding="utf-8"))
    validate_scenario(scenario)
    return scenario


def run_scenario(
    name: str,
    out_dir: Path,
    force: bool = False,
    *,
    run_id_override: str | None = None,
    runtime_phase: int = 2,
) -> dict[str, Any]:
    scenario = load_scenario(name)
    store = ArtifactStore(out_dir)
    store.prepare(force=force)

    run_id = run_id_override or scenario["run_id"]
    results = []
    parent_node_id = None
    previous_output_sha256 = None

    for stage in STAGE_ORDER:
        result = run_stage(
            stage=stage,
            spec=scenario["stages"][stage],
            repo_root=REPO_ROOT,
            store=store,
            run_id=run_id,
            parent_node_id=parent_node_id,
            previous_output_sha256=previous_output_sha256,
            runtime_phase=runtime_phase,
        )
        results.append(result)
        parent_node_id = result.node_id
        previous_output_sha256 = result.output_sha256

    manifest = {
        "runtime_version": "0.3.0" if runtime_phase >= 3 else "0.1.1",
        "phase": runtime_phase,
        "scenario": name,
        "run_id": run_id,
        "source_commit": current_source_commit(),
        "mode": scenario["mode"],
        "stage_order": list(STAGE_ORDER),
        "status": "SMOKE_REPLAY_COMPLETE",
        "nodes": [
            {
                "stage": r.stage,
                "node_id": r.node_id,
                "output_path": r.output_path,
                "output_sha256": r.output_sha256,
                "output_identity": r.output_identity,
                "manifest_sha256": r.manifest_sha256,
            }
            for r in results
        ],
        "limitations": scenario.get("limitations", []),
        "phase3_ready_surface": {
            "node_manifests": True,
            "input_output_hashes": True,
            "white_box_trace": False,
            "live_agent_execution": False,
        },
    }
    store.write_run_manifest(manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal learning runtime")
    parser.add_argument("scenario", help="scenario name, e.g. p01-mvp")
    parser.add_argument("--out", type=Path, default=None, help="output directory")
    parser.add_argument("--force", action="store_true", help="allow writing into an existing non-empty run directory")
    args = parser.parse_args()

    out_dir = args.out or (REPO_ROOT / "runs" / "phase2" / args.scenario)
    manifest = run_scenario(args.scenario, out_dir, force=args.force)
    print(json.dumps({"status": manifest["status"], "run_id": manifest["run_id"], "out": str(out_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
