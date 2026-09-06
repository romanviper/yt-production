from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalize_text(value: str) -> str:
    """Canonical text view for span comparison only.

    Raw bytes remain independently hashed. This normalization intentionally changes
    only newline representation; it does not trim, case-fold, collapse whitespace,
    or otherwise hide content changes.
    """
    return value.replace("\r\n", "\n").replace("\r", "\n")


def normalized_text_bytes(data: bytes) -> bytes:
    return normalize_text(data.decode("utf-8-sig")).encode("utf-8")


def artifact_identity(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    result: dict[str, Any] = {
        "raw_sha256": sha256_bytes(data),
        "bytes": len(data),
    }
    try:
        normalized = normalized_text_bytes(data)
    except UnicodeDecodeError:
        result.update({"text_sha256": None, "text_normalization": None})
    else:
        result.update(
            {
                "text_sha256": sha256_bytes(normalized),
                "text_normalization": "UTF8_BOM_OPTIONAL_CRLF_CR_TO_LF_ONLY",
            }
        )
    return result


def verify_artifact_identity(path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    observed = artifact_identity(path)
    if expected.get("raw_sha256") == observed.get("raw_sha256"):
        return {"status": "RAW_MATCH", "expected": expected, "observed": observed}
    if (
        expected.get("text_sha256")
        and observed.get("text_sha256")
        and expected.get("text_sha256") == observed.get("text_sha256")
    ):
        return {
            "status": "TEXT_MATCH_RAW_DIFF_ALLOWED_NORMALIZATION",
            "expected": expected,
            "observed": observed,
        }
    return {"status": "CONTENT_MISMATCH", "expected": expected, "observed": observed}


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def canonical_json_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def write_json(path: Path, value: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_json_bytes(value)
    path.write_bytes(data)
    return sha256_bytes(data)


def write_bytes(path: Path, data: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return sha256_bytes(data)


def write_text(path: Path, value: str) -> str:
    return write_bytes(path, value.encode("utf-8"))


def snapshot_file(source: Path, destination: Path) -> dict[str, Any]:
    data = source.read_bytes()
    write_bytes(destination, data)
    return {
        "source": artifact_identity(source),
        "snapshot": artifact_identity(destination),
    }


class ArtifactStore:
    """Small file-backed store for one learning run."""

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
