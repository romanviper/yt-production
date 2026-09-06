from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifacts import ArtifactStore, artifact_identity, write_bytes, write_json

STAGE_ORDER = ("plan", "write", "truth", "product")
ALLOWED_KINDS = {"import_json", "import_text", "reference_only"}


@dataclass(frozen=True)
class StageResult:
    stage: str
    node_id: str
    output_path: str
    output_sha256: str
    manifest_sha256: str
    output_identity: dict[str, Any]


def validate_scenario(scenario: dict[str, Any]) -> None:
    order = tuple(scenario.get("stage_order", []))
    if order != STAGE_ORDER:
        raise ValueError(f"stage_order must be exactly {STAGE_ORDER}, got {order}")
    stages = scenario.get("stages", {})
    if set(stages) != set(STAGE_ORDER):
        raise ValueError("scenario must define exactly plan/write/truth/product")
    for stage in STAGE_ORDER:
        spec = stages[stage]
        kind = spec.get("kind")
        if kind not in ALLOWED_KINDS:
            raise ValueError(f"unsupported kind for {stage}: {kind}")
        source = spec.get("source_ref")
        if not source or Path(source).is_absolute() or ".." in Path(source).parts:
            raise ValueError(f"invalid source_ref for {stage}: {source}")
        if not spec.get("fixture_trust"):
            raise ValueError(f"fixture_trust is required for {stage}")


def run_stage(
    *,
    stage: str,
    spec: dict[str, Any],
    repo_root: Path,
    store: ArtifactStore,
    run_id: str,
    parent_node_id: str | None,
    previous_output_sha256: str | None,
    runtime_phase: int = 2,
) -> StageResult:
    source_ref = spec["source_ref"]
    source_path = repo_root / source_ref
    if not source_path.exists() or not source_path.is_file():
        raise FileNotFoundError(f"missing fixture source for {stage}: {source_ref}")

    source_identity = artifact_identity(source_path)
    node_id = f"{run_id}:{stage}"
    input_payload = {
        "stage": stage,
        "node_id": node_id,
        "parent_node_id": parent_node_id,
        "previous_output_sha256": previous_output_sha256,
        "executor_kind": spec["kind"],
        "source_ref": source_ref,
        "source_identity": source_identity,
        "fixture_trust": spec["fixture_trust"],
    }
    input_sha = store.write_input(stage, input_payload)

    kind = spec["kind"]
    stage_dir = store.stage_dir(stage)
    if kind == "import_json":
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        output_path = stage_dir / "output.json"
        output_sha = write_json(
            output_path,
            {
                "fixture_source_ref": source_ref,
                "fixture_source_identity": source_identity,
                "fixture_trust": spec["fixture_trust"],
                "payload": payload,
            },
        )
    elif kind == "import_text":
        output_path = stage_dir / "output.md"
        output_sha = write_bytes(output_path, source_path.read_bytes())
    else:
        output_path = stage_dir / "output.json"
        output_sha = write_json(
            output_path,
            {
                "status": "REFERENCE_ONLY_NOT_REEVALUATED",
                "fixture_source_ref": source_ref,
                "fixture_source_identity": source_identity,
                "fixture_trust": spec["fixture_trust"],
                "note": spec.get("note", "Referenced only to prove the stage boundary."),
            },
        )

    output_identity = artifact_identity(output_path)
    manifest = {
        "node_id": node_id,
        "parent_node_id": parent_node_id,
        "stage": stage,
        "runtime_phase": runtime_phase,
        "executor_kind": kind,
        "input_sha256": input_sha,
        "output_file": output_path.name,
        "output_sha256": output_sha,
        "output_identity": output_identity,
        "fixture_source_ref": source_ref,
        "fixture_source_identity": source_identity,
        "fixture_trust": spec["fixture_trust"],
        "materialized": True,
        "trace_available": False,
    }
    manifest_sha = store.write_manifest(stage, manifest)
    return StageResult(stage, node_id, str(output_path.relative_to(store.root)), output_sha, manifest_sha, output_identity)
