"""Shared, dependency-free repository utilities."""

from __future__ import annotations

import glob
import hashlib
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "system" / "operations" / "registry.json"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def estimate_tokens(text: str) -> int:
    # Conservative language-agnostic estimate for budget enforcement, not billing.
    return max(1, (len(text) + 2) // 3)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ỹ]+\b", text, flags=re.UNICODE))


def load_registry() -> dict[str, Any]:
    return read_json(REGISTRY_PATH)["operations"]


def render_pattern(pattern: str, section: str | None, unit: str | None) -> str:
    if "{section}" in pattern:
        if not section:
            raise ValueError(f"Operation requires --section for {pattern}")
        pattern = pattern.replace("{section}", section)
    if "{unit}" in pattern:
        if not unit:
            raise ValueError(f"Operation requires --unit for {pattern}")
        pattern = pattern.replace("{unit}", unit)
    return pattern


def expand_inputs(product_dir: Path, patterns: list[str], section: str | None, unit: str | None) -> list[Path]:
    paths: list[Path] = []
    for raw in patterns:
        pattern = render_pattern(raw, section, unit)
        matches = [Path(item) for item in glob.glob(str(product_dir / pattern))]
        if not matches:
            raise FileNotFoundError(f"Missing required input: {pattern}")
        paths.extend(sorted(matches))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def expand_optional_inputs(product_dir: Path, patterns: list[str], section: str | None, unit: str | None) -> list[Path]:
    paths: list[Path] = []
    for raw in patterns:
        pattern = render_pattern(raw, section, unit)
        paths.extend(Path(item).resolve() for item in sorted(glob.glob(str(product_dir / pattern))))
    return list(dict.fromkeys(paths))


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def product_relative(product_dir: Path, path: Path) -> str:
    return str(path.resolve().relative_to(product_dir.resolve()))

