#!/usr/bin/env python3
"""Explicit adoption boundary for Historical Substrate architecture.

Historical Substrate is not inferred from direct-authorship, operation names, or
file presence. A whole outline/cycle adopts it only through an explicit version
marker. A bounded section migration may adopt it independently through its
approved section overlay.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json
    from scripts.section_overlay_contract import overlay_path
except ModuleNotFoundError:  # pragma: no cover
    from common import read_json
    from section_overlay_contract import overlay_path


HISTORICAL_SUBSTRATE_CONTRACT_VERSION = 1


def _version(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def outline_adopts_historical_substrate(
    product_dir: Path,
    *,
    product: dict[str, Any] | None = None,
    outline: dict[str, Any] | None = None,
) -> bool:
    """Return whether the whole current product/cycle explicitly adopts v1."""

    product_dir = product_dir.resolve()
    if product is None:
        product_path = product_dir / "product.json"
        product = read_json(product_path) if product_path.is_file() else {}
    if outline is None:
        outline_path = product_dir / "02_outline" / "outline.json"
        outline = read_json(outline_path) if outline_path.is_file() else {}

    cycle = product.get("production_cycle", {}) if isinstance(product, dict) else {}
    architecture = outline.get("script_architecture", {}) if isinstance(outline, dict) else {}
    return (
        _version(cycle.get("historical_substrate_contract_version"))
        == HISTORICAL_SUBSTRATE_CONTRACT_VERSION
        or _version(architecture.get("historical_substrate_contract_version"))
        == HISTORICAL_SUBSTRATE_CONTRACT_VERSION
    )


def section_adopts_historical_substrate(
    product_dir: Path,
    section: str,
    *,
    product: dict[str, Any] | None = None,
    outline: dict[str, Any] | None = None,
) -> bool:
    """Return whether one section explicitly adopts v1.

    Whole-product adoption covers every section. Otherwise only an approved
    bounded overlay carrying the explicit contract marker may adopt a section.
    File presence alone is not adoption.
    """

    product_dir = product_dir.resolve()
    if outline_adopts_historical_substrate(product_dir, product=product, outline=outline):
        return True

    path = overlay_path(product_dir, section)
    if not path.is_file():
        return False
    overlay = read_json(path)
    return (
        overlay.get("status") == "approved_migration"
        and overlay.get("section") == section
        and _version(overlay.get("historical_substrate_contract_version"))
        == HISTORICAL_SUBSTRATE_CONTRACT_VERSION
    )


def adoption_scope(
    product_dir: Path,
    *,
    section: str | None = None,
    product: dict[str, Any] | None = None,
    outline: dict[str, Any] | None = None,
) -> str:
    """Return ``none``, ``section`` or ``product`` for diagnostics/tests."""

    if outline_adopts_historical_substrate(product_dir, product=product, outline=outline):
        return "product"
    if section and section_adopts_historical_substrate(
        product_dir, section, product=product, outline=outline
    ):
        return "section"
    return "none"
