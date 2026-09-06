from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_json_bytes(value)
    path.write_bytes(data)
    return sha256_bytes(data)


def write_text(path: Path, value: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value.encode("utf-8")
    path.write_bytes(data)
    return sha256_bytes(data)


class ArtifactStore:
    """Small file-backed store for one learning run.

    Phase 2 records only inputs, outputs and manifests. It deliberately does not
    provide trace/event APIs; those arrive in Phase 3.
    """

    def __init__(self, root: Path):
        self.root = root

    def prepare(self, force: bool = False) -> None:
        if self.root.exists() and any(self.root.iterdir()) and not force:
            raise FileExistsError(f"run directory already exists and is non-empty: {self.root}")
        self.root.mkdir(parents=True, exist_ok=True)

    def stage_dir(self, stage: str) -> Path:
        path = self.root / stage
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_input(self, stage: str, payload: dict[str, Any]) -> str:
        return write_json(self.stage_dir(stage) / "input.json", payload)

    def write_manifest(self, stage: str, payload: dict[str, Any]) -> str:
        return write_json(self.stage_dir(stage) / "manifest.json", payload)

    def write_run_manifest(self, payload: dict[str, Any]) -> str:
        return write_json(self.root / "manifest.json", payload)
