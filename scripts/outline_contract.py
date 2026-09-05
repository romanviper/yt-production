#!/usr/bin/env python3
"""Historical-Substrate-aware outline contract with legacy compatibility.

Legacy approved outlines remain readable during bounded section migration.
Whole outlines that explicitly adopt Historical Substrate contract v1 must use
historical-world section fields directly; bounded overlays are validated by the
section-overlay/runtime contracts instead of silently rewriting the base file.
"""

from __future__ import annotations

from typing import Any

try:
    import scripts.outline_contract_legacy as _legacy
    from scripts.outline_contract_legacy import *  # noqa: F401,F403
except ModuleNotFoundError:  # pragma: no cover
    import outline_contract_legacy as _legacy
    from outline_contract_legacy import *  # type: ignore # noqa: F401,F403


_EVIDENCE_WORLD_MARKERS = (
    "bằng chứng", "evidence", "catalogue", "catalog ", "corpus",
    "surviving evidence", "preserved evidence", "artifact shows", "hiện vật cho thấy",
)


def _historical_world_change_errors(value: Any, prefix: str) -> list[str]:
    errors = list(_legacy.validate_historical_change_semantics(value, prefix))
    if not isinstance(value, dict):
        return errors
    combined = f"{value.get('from', '')} {value.get('to', '')}".lower()
    markers = sorted({marker for marker in _EVIDENCE_WORLD_MARKERS if marker in combined})
    if markers:
        errors.append(
            f"{prefix} historical_change must describe historical-world state, not evidence-state: "
            + ", ".join(markers)
        )
    return errors


def validate_historical_change_semantics(value: Any, prefix: str) -> list[str]:
    """Public strict semantic validator for new Historical Substrate contracts."""
    return _historical_world_change_errors(value, prefix)


def validate_outline_contract(
    outline: dict[str, Any],
    known_claim_ids: set[str] | None = None,
    product_target: dict[str, Any] | None = None,
    require_current: bool = False,
) -> list[str]:
    errors = list(
        _legacy.validate_outline_contract(
            outline,
            known_claim_ids,
            product_target,
            require_current=require_current,
        )
    )
    architecture = outline.get("script_architecture", {}) if isinstance(outline, dict) else {}
    hs_version = architecture.get("historical_substrate_contract_version") if isinstance(architecture, dict) else None
    if hs_version is None:
        return errors
    if hs_version != 1:
        errors.append("outline script_architecture.historical_substrate_contract_version must be 1")
        return errors

    for item in outline.get("sections", []):
        if not isinstance(item, dict):
            continue
        section_id = item.get("id", "?")
        territory = item.get("historical_territory")
        if not isinstance(territory, str) or not territory.strip():
            errors.append(f"outline section {section_id} historical_territory is required under Historical Substrate contract")
        elif "?" in territory:
            errors.append(f"outline section {section_id} historical_territory must be declarative, not question-shaped")
        ids = item.get("historical_substrate_ids")
        if not isinstance(ids, list) or not ids or not all(isinstance(value, str) and value for value in ids):
            errors.append(f"outline section {section_id} historical_substrate_ids must be a non-empty list")
        elif len(ids) != len(set(ids)):
            errors.append(f"outline section {section_id} historical_substrate_ids must be unique")
        change = item.get("historical_change")
        if not isinstance(change, dict) or not str(change.get("from") or "").strip() or not str(change.get("to") or "").strip():
            errors.append(f"outline section {section_id} historical_change requires non-empty from/to states")
        else:
            errors.extend(_historical_world_change_errors(change, f"outline section {section_id}"))
        mission = item.get("mission")
        if isinstance(mission, str) and "?" in mission:
            errors.append(f"outline section {section_id} mission must not be answer-shaped under Historical Substrate contract")
    return errors
