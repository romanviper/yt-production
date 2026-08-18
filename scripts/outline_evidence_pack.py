#!/usr/bin/env python3
"""Build the compact, deterministic evidence and story-material catalog used by outline tasks."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
except ModuleNotFoundError:
    from common import read_json, sha256, write_json


PACK_PATH = Path("01_research/outline-evidence-pack.json")
CLAIM_LEDGER_PATH = Path("01_research/claim-ledger.json")
MATERIAL_LEDGER_PATH = Path("01_research/material-ledger.json")
MATERIAL_MAP_PATH = Path("01_research/story-material-map.json")
CLAIM_FIELDS = (
    "id",
    "statement",
    "type",
    "confidence",
    "status",
    "sources",
    "counterevidence",
    "narrative_implication",
)
MATERIAL_FIELDS = (
    "id",
    "kind",
    "label",
    "what_audience_follows",
    "sequence",
    "claim_ids",
    "source_refs",
    "representativeness",
    "limitations",
)


def compact_claim(claim: dict[str, Any]) -> dict[str, Any]:
    """Keep fields needed to allocate claims without loading the full research ledger."""

    return {field: claim.get(field) for field in CLAIM_FIELDS if claim.get(field) not in (None, "", [])}


def compact_material(material: dict[str, Any]) -> dict[str, Any]:
    """Keep reconstructable carrier detail and its evidence boundaries."""

    return {field: material.get(field) for field in MATERIAL_FIELDS if material.get(field) not in (None, "", [])}


def _validate_material_map(material_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if material_map.get("schema_version") != 1:
        errors.append("story material map schema_version must be 1")
    if material_map.get("status") != "complete":
        errors.append("story material map status must be complete")
    phases = material_map.get("phases")
    if not isinstance(phases, list) or not phases:
        errors.append("story material map requires at least one phase")
        phases = []
    phase_ids: set[str] = set()
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            errors.append(f"story material phase #{index + 1} must be an object")
            continue
        phase_id = phase.get("id")
        if not isinstance(phase_id, str) or not phase_id.strip() or phase_id in phase_ids:
            errors.append(f"story material phase #{index + 1} requires a unique id")
        else:
            phase_ids.add(phase_id)
        for field in ["story_function", "state_change", "evidence_strength"]:
            if not isinstance(phase.get(field), str) or not phase[field].strip():
                errors.append(f"story material phase {phase_id or index + 1} missing {field}")
        material_ids = phase.get("material_ids")
        if not isinstance(material_ids, list) or not all(isinstance(item, str) and item for item in material_ids):
            errors.append(f"story material phase {phase_id or index + 1} material_ids must be a list")
        gap = phase.get("gap")
        if gap is not None and not isinstance(gap, str):
            errors.append(f"story material phase {phase_id or index + 1} gap must be text or null")
    for field in ["opening_candidates", "reversal_candidates", "ending_candidates"]:
        values = material_map.get(field)
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            errors.append(f"story material map {field} must be a list of material IDs")
    gaps = material_map.get("gaps")
    if not isinstance(gaps, list) or not all(isinstance(item, str) and item.strip() for item in gaps):
        errors.append("story material map gaps must be a list of strings")
    return errors


def _material_ids_from_map(material_map: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for phase in material_map.get("phases", []):
        if not isinstance(phase, dict):
            continue
        for material_id in phase.get("material_ids", []):
            if isinstance(material_id, str) and material_id and material_id not in ids:
                ids.append(material_id)
    for field in ["opening_candidates", "reversal_candidates", "ending_candidates"]:
        for material_id in material_map.get(field, []):
            if isinstance(material_id, str) and material_id and material_id not in ids:
                ids.append(material_id)
    return ids


def expected_pack(product_dir: Path) -> dict[str, Any]:
    claim_path = product_dir / CLAIM_LEDGER_PATH
    material_path = product_dir / MATERIAL_LEDGER_PATH
    map_path = product_dir / MATERIAL_MAP_PATH
    claims_doc = read_json(claim_path)
    materials_doc = read_json(material_path)
    material_map = read_json(map_path)
    if claims_doc.get("status") != "complete":
        raise ValueError("Claim ledger must be complete before building the outline evidence pack.")
    if materials_doc.get("status") != "complete":
        raise ValueError("Material ledger must be complete before building the outline evidence pack.")
    map_errors = _validate_material_map(material_map)
    if map_errors:
        raise ValueError("Invalid story material map: " + "; ".join(map_errors))

    materials_by_id = {
        item.get("id"): item
        for item in materials_doc.get("materials", [])
        if isinstance(item, dict) and item.get("id")
    }
    selected_ids = _material_ids_from_map(material_map)
    unknown = [material_id for material_id in selected_ids if material_id not in materials_by_id]
    if unknown:
        raise ValueError("Story material map references unknown material IDs: " + ", ".join(unknown))

    return {
        "schema_version": 2,
        "product": claims_doc.get("product", product_dir.name),
        "status": "complete",
        "claim_ledger_sha256": sha256(claim_path),
        "material_ledger_sha256": sha256(material_path),
        "story_material_map_sha256": sha256(map_path),
        "claims": [compact_claim(item) for item in claims_doc.get("claims", [])],
        "materials": [compact_material(materials_by_id[material_id]) for material_id in selected_ids],
        "story_material_map": material_map,
        "contradiction_register": claims_doc.get("contradiction_register", []),
        "scope_note": (
            "This pack is for architecture design. Claims define what may be asserted; materials preserve the concrete "
            "objects/actions/processes that may carry story movement. Full provenance remains authoritative in the global ledgers."
        ),
    }


def build_outline_evidence_pack(product_dir: Path) -> Path:
    product_dir = product_dir.resolve()
    path = product_dir / PACK_PATH
    write_json(path, expected_pack(product_dir))
    return path


def verify_outline_evidence_pack(product_dir: Path) -> list[str]:
    product_dir = product_dir.resolve()
    path = product_dir / PACK_PATH
    if not path.is_file():
        return [f"missing outline evidence pack: {PACK_PATH}"]
    try:
        actual = read_json(path)
        expected = expected_pack(product_dir)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        return [f"invalid outline evidence pack: {exc}"]
    return [] if actual == expected else ["outline evidence pack is stale or not deterministically generated"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    args = parser.parse_args()
    path = build_outline_evidence_pack(args.product)
    print(f"Built {path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
