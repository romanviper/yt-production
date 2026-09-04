#!/usr/bin/env python3
"""Canonical bounded section-architecture overlays.

A section overlay is a first-class migration authority that sits after an
approved outline and before section materialization. It may update only the
history-facing contract of one section; it cannot silently rewrite unrelated
outline authority such as claim territory, dependencies, word budget or
continuity.
"""

from __future__ import annotations

from copy import deepcopy
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256
except ModuleNotFoundError:  # pragma: no cover - direct execution fallback
    from common import read_json, sha256


SECTION_OVERLAY_SCHEMA_VERSION = 1
HISTORICAL_SUBSTRATE_CONTRACT_VERSION = 1
ALLOWED_OVERLAY_FIELDS = {
    "schema_version",
    "section",
    "status",
    "base_outline_sha256",
    "historical_substrate_contract_version",
    "historical_territory",
    "historical_change",
    "historical_substrate_ids",
    "audience_discovery",
    "authority_note",
}


def overlay_path(product_dir: Path, section: str) -> Path:
    return product_dir.resolve() / "02_outline" / "section-overlays" / f"{section}.json"


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_nonempty(item) for item in value)


def _outline_section(outline: dict[str, Any], section: str) -> dict[str, Any] | None:
    matches = [
        item
        for item in outline.get("sections", [])
        if isinstance(item, dict) and item.get("id") == section
    ]
    return matches[0] if len(matches) == 1 else None


def validate_section_overlay(
    overlay: dict[str, Any],
    outline: dict[str, Any],
    outline_path: Path,
) -> list[str]:
    errors: list[str] = []
    if overlay.get("schema_version") != SECTION_OVERLAY_SCHEMA_VERSION:
        errors.append(
            f"section overlay schema_version must be {SECTION_OVERLAY_SCHEMA_VERSION}"
        )
    unknown_fields = sorted(set(overlay) - ALLOWED_OVERLAY_FIELDS)
    if unknown_fields:
        errors.append("section overlay contains non-authoritative fields: " + ", ".join(unknown_fields))

    section = overlay.get("section")
    if not _nonempty(section) or not re.fullmatch(r"P\d{2}", str(section)):
        errors.append("section overlay section must use P## format")
        section = "?"
    elif _outline_section(outline, str(section)) is None:
        errors.append(f"section overlay target {section} must exist exactly once in approved outline")

    if overlay.get("status") != "approved_migration":
        errors.append("section overlay status must be approved_migration")

    adoption_version = overlay.get("historical_substrate_contract_version")
    if adoption_version is not None and adoption_version != HISTORICAL_SUBSTRATE_CONTRACT_VERSION:
        errors.append(
            f"section overlay historical_substrate_contract_version must be {HISTORICAL_SUBSTRATE_CONTRACT_VERSION} when present"
        )

    expected_outline_hash = sha256(outline_path)
    if overlay.get("base_outline_sha256") != expected_outline_hash:
        errors.append("section overlay base_outline_sha256 does not match current approved outline")

    territory = overlay.get("historical_territory")
    if not _nonempty(territory):
        errors.append("section overlay historical_territory is required")
    elif "?" in str(territory):
        errors.append("section overlay historical_territory must be declarative, not question-shaped")

    change = overlay.get("historical_change")
    if not isinstance(change, dict) or not _nonempty(change.get("from")) or not _nonempty(change.get("to")):
        errors.append("section overlay historical_change requires non-empty from/to states")

    ids = overlay.get("historical_substrate_ids")
    if not _string_list(ids):
        errors.append("section overlay historical_substrate_ids must be a non-empty list")
    elif len(ids) != len(set(ids)):
        errors.append("section overlay historical_substrate_ids must be unique")

    discovery = overlay.get("audience_discovery")
    if discovery is not None and not _nonempty(discovery):
        errors.append("section overlay audience_discovery must be non-empty when present")
    return errors


def resolve_section_spec(
    product_dir: Path,
    section: str,
    *,
    outline: dict[str, Any] | None = None,
    outline_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Resolve canonical section contract and return authority provenance."""

    product_dir = product_dir.resolve()
    outline_path = (outline_path or product_dir / "02_outline" / "outline.json").resolve()
    outline = outline or read_json(outline_path)
    base = _outline_section(outline, section)
    if base is None:
        raise ValueError(f"Approved outline must contain section {section} exactly once.")

    path = overlay_path(product_dir, section)
    if not path.is_file():
        return deepcopy(base), {
            "kind": "approved_outline",
            "outline_sha256": sha256(outline_path),
            "overlay_sha256": None,
            "historical_substrate_contract_version": None,
        }

    overlay = read_json(path)
    errors = validate_section_overlay(overlay, outline, outline_path)
    if errors:
        raise ValueError("Invalid section overlay: " + "; ".join(errors))

    resolved = deepcopy(base)
    resolved["historical_territory"] = overlay["historical_territory"].strip()
    resolved["historical_change"] = deepcopy(overlay["historical_change"])
    resolved["historical_substrate_ids"] = list(overlay["historical_substrate_ids"])
    if _nonempty(overlay.get("audience_discovery")):
        resolved["audience_discovery"] = overlay["audience_discovery"].strip()
    else:
        resolved.pop("audience_discovery", None)
    resolved["mission"] = resolved["historical_territory"]
    resolved.pop("earned_meaning", None)

    return resolved, {
        "kind": "approved_section_overlay",
        "outline_sha256": sha256(outline_path),
        "overlay_path": str(path.relative_to(product_dir)),
        "overlay_sha256": sha256(path),
        "historical_substrate_contract_version": overlay.get(
            "historical_substrate_contract_version"
        ),
        "authority_note": overlay.get("authority_note"),
    }
