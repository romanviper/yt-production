#!/usr/bin/env python3
"""Preflight gates for canonical Historical Substrate section tasks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256
    from scripts.historical_substrate_contract import verify_writer_section_substrate
    from scripts.section_overlay_contract import resolve_section_spec
except ModuleNotFoundError:  # pragma: no cover
    from common import read_json, sha256
    from historical_substrate_contract import verify_writer_section_substrate
    from section_overlay_contract import resolve_section_spec


def verify_canonical_section_state(product_dir: Path, section: str) -> list[str]:
    """Require section state + Writer projection to reproduce from canonical inputs."""

    product_dir = product_dir.resolve()
    state_path = product_dir / "03_sections" / section / "section.json"
    outline_path = product_dir / "02_outline" / "outline.json"
    if not state_path.is_file():
        return [f"missing 03_sections/{section}/section.json"]
    if not outline_path.is_file():
        return ["missing 02_outline/outline.json"]

    state = read_json(state_path)
    if int(state.get("historical_substrate_contract_version") or 0) < 1:
        return [f"section {section} does not declare Historical Substrate contract version"]

    try:
        resolved, authority = resolve_section_spec(product_dir, section, outline_path=outline_path)
    except ValueError as exc:
        return [str(exc)]

    errors: list[str] = []
    expected_fields: dict[str, Any] = {
        "historical_territory": resolved.get("historical_territory"),
        "mission": resolved.get("historical_territory"),
        "historical_change": resolved.get("historical_change"),
        "historical_substrate_ids": resolved.get("historical_substrate_ids"),
        "outline_sha256": sha256(outline_path),
    }
    for field, expected in expected_fields.items():
        if state.get(field) != expected:
            errors.append(f"section {section} state field {field} is stale relative to canonical architecture")

    actual_authority = state.get("architecture_authority")
    if actual_authority != authority:
        errors.append(f"section {section} architecture_authority is stale or missing")

    projection_errors = verify_writer_section_substrate(product_dir, section)
    errors.extend(projection_errors)
    return errors


def require_canonical_section_state(product_dir: Path, section: str) -> None:
    errors = verify_canonical_section_state(product_dir, section)
    if errors:
        raise ValueError(
            "Historical Substrate preflight failed; regenerate canonical section materialization: "
            + "; ".join(errors)
        )
