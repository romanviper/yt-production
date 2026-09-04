#!/usr/bin/env python3
"""Materialize canonical section state from approved outline + bounded overlays.

Historical-Substrate products may be materialized either as a whole product when
coverage is product-complete, or as one explicitly covered section when the
substrate is a bounded ``section_migration``. This keeps migrated P01 state
reproducible without pretending P02-P08 were rebuilt under the new contract.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
    from scripts.historical_substrate_contract import (
        build_writer_section_substrate,
        validate_historical_substrate,
        validate_section_binding,
    )
    from scripts.outline_contract import OUTLINE_SCHEMA_VERSION, normalize_outline_contract, validate_outline_contract
    from scripts.section_overlay_contract import resolve_section_spec
    from scripts.story_plan_contract import build_narration_pack, empty_story_plan, is_direct_authorship_outline
    from scripts import materialize_sections_legacy as legacy
except ModuleNotFoundError:  # pragma: no cover
    from common import read_json, sha256, write_json
    from historical_substrate_contract import (
        build_writer_section_substrate,
        validate_historical_substrate,
        validate_section_binding,
    )
    from outline_contract import OUTLINE_SCHEMA_VERSION, normalize_outline_contract, validate_outline_contract
    from section_overlay_contract import resolve_section_spec
    from story_plan_contract import build_narration_pack, empty_story_plan, is_direct_authorship_outline
    import materialize_sections_legacy as legacy


def _render(value: Any, fallback: str = "Không có.") -> str:
    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
        return "\n".join(f"- {item}" for item in items) if items else fallback
    text = str(value or "").strip()
    return text or fallback


def _coverage_allows(substrate: dict[str, Any], section: str) -> bool:
    coverage = substrate.get("coverage", {}) if isinstance(substrate, dict) else {}
    if coverage.get("mode") == "product":
        return True
    return section in set(coverage.get("covered_sections", []))


def _materialize_direct_section(
    product_dir: Path,
    outline: dict[str, Any],
    outline_path: Path,
    product: dict[str, Any],
    claims_doc: dict[str, Any],
    sources_doc: dict[str, Any],
    substrate: dict[str, Any],
    section_id: str,
) -> list[Path]:
    if not re.fullmatch(r"P\d{2}", section_id):
        raise ValueError(f"Invalid section ID: {section_id}")
    if not _coverage_allows(substrate, section_id):
        raise ValueError(
            f"Historical Substrate coverage does not authorize materializing {section_id}."
        )

    resolved, architecture_authority = resolve_section_spec(
        product_dir, section_id, outline=outline, outline_path=outline_path
    )
    binding_errors = validate_section_binding(resolved, substrate)
    if binding_errors:
        raise ValueError(
            f"Historical Substrate binding is invalid for {section_id}: " + "; ".join(binding_errors)
        )

    root = product_dir / "03_sections" / section_id
    root.mkdir(parents=True, exist_ok=True)
    section_path = root / "section.json"
    if section_path.is_file():
        existing = read_json(section_path)
        if existing.get("status") not in {"outline_amended", "ready_for_draft", "needs_story_plan"}:
            raise ValueError(
                f"Existing {section_id} is already in production state {existing.get('status')!r}; "
                "do not overwrite it through architecture migration."
            )

    cycle_id = product.get("production_cycle", {}).get("id")
    state = {
        "schema_version": 5,
        "id": section_id,
        "title": resolved["title"],
        "order": resolved["order"],
        "status": "ready_for_draft",
        "human_approved": False,
        "dependencies": resolved.get("dependencies", []),
        "narrative_job": resolved["narrative_job"],
        "entry_state": resolved["entry_state"],
        "exit_state": resolved["exit_state"],
        "target_words": resolved["target_words"],
        "cycle_id": cycle_id,
        "outline_sha256": sha256(outline_path),
        "historical_substrate_contract_version": 1,
        "historical_territory": resolved["historical_territory"],
        "mission": resolved["historical_territory"],
        "historical_change": resolved["historical_change"],
        "historical_substrate_ids": list(resolved["historical_substrate_ids"]),
        "architecture_authority": architecture_authority,
    }
    for field in ("transition", "movement_ids"):
        if resolved.get(field) not in (None, "", []):
            state[field] = resolved[field]
    write_json(section_path, state)

    brief_path = root / "brief.md"
    brief_path.write_text(
        f"# {section_id} — {resolved['title']}\n\n"
        f"Cycle: `{cycle_id}`\n\n"
        f"## Historical territory\n\n{resolved['historical_territory']}\n\n"
        f"## Historical change\n\n"
        f"- From: {resolved['historical_change']['from']}\n"
        f"- To: {resolved['historical_change']['to']}\n\n"
        f"## Section objective\n\n{resolved['narrative_job']}\n\n"
        f"## Entry state\n\n{resolved['entry_state']}\n\n"
        f"## Exit state\n\n{resolved['exit_state']}\n\n"
        f"## Historical Substrate selection\n\n{_render(resolved['historical_substrate_ids'])}\n\n"
        f"## Truth ceiling\n\n{_render(resolved.get('claim_ids'))}\n\n"
        f"## Transition\n\n{_render(resolved.get('transition'))}\n\n"
        f"## Non-goal\n\n{_render(resolved.get('non_goal'))}\n",
        encoding="utf-8",
    )

    claim_map = {
        item["id"]: item
        for item in claims_doc.get("claims", [])
        if isinstance(item, dict) and item.get("id")
    }
    source_map = {
        item["id"]: item
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict) and item.get("id")
    }
    selected_claims: list[dict[str, Any]] = []
    source_ids: set[str] = set()
    for claim_id in resolved.get("claim_ids", []):
        claim = claim_map.get(claim_id)
        if claim is None:
            raise ValueError(f"{section_id} references missing claim {claim_id}")
        if claim.get("status") not in {"supported", "qualified"}:
            raise ValueError(f"{section_id} claim is not writing-ready: {claim_id}")
        selected_claims.append(claim)
        source_ids.update(item for item in claim.get("sources", []) if isinstance(item, str))
    missing_sources = sorted(source_ids - source_map.keys())
    if missing_sources:
        raise ValueError(f"{section_id} claims reference missing sources: {missing_sources}")
    unreviewed = sorted(
        source_id for source_id in source_ids if source_map[source_id].get("status") != "reviewed"
    )
    if unreviewed:
        raise ValueError(f"{section_id} sources are not reviewed: {unreviewed}")

    evidence_path = root / "evidence-pack.json"
    write_json(
        evidence_path,
        {
            "schema_version": 3,
            "section": section_id,
            "cycle_id": cycle_id,
            "outline_sha256": sha256(outline_path),
            "claim_ids": list(resolved.get("claim_ids", [])),
            "source_ids": sorted(source_ids),
            "claims": selected_claims,
            "sources": [source_map[source_id] for source_id in sorted(source_ids)],
            "rule": (
                "This is secondary evidence authority. Historical Substrate is the primary history model; "
                "evidence lookup verifies or sharpens a chosen telling and does not define the story route."
            ),
        },
    )

    section_substrate_path = root / "historical-substrate.json"
    product_substrate_path = product_dir / "01_research" / "historical-substrate.json"
    write_json(
        section_substrate_path,
        build_writer_section_substrate(
            product_substrate_path,
            resolved,
            outline_path,
            architecture_authority=architecture_authority,
        ),
    )

    narration_path = root / "narration-pack.json"
    build_narration_pack(product_dir, section_id)

    continuity_path = root / "continuity-in.md"
    if not continuity_path.exists():
        dependencies = ", ".join(resolved.get("dependencies", [])) or "Không có."
        continuity_path.write_text(
            f"# Continuity Input — {section_id}\n\nCycle: `{cycle_id}`\n\n"
            f"Dependencies: {dependencies}\n\n"
            "## Prior handoff\n\nChưa có hoặc sẽ được task owner cập nhật trước drafting.\n",
            encoding="utf-8",
        )

    return [
        section_path,
        brief_path,
        evidence_path,
        section_substrate_path,
        narration_path,
        continuity_path,
    ]


def materialize(product_dir: Path, section: str | None = None) -> list[Path]:
    product_dir = product_dir.resolve()
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    product_path = product_dir / "product.json"
    product = read_json(product_path)
    if outline.get("status") != "approved":
        raise ValueError("Outline must be human-approved before section materialization.")

    if not is_direct_authorship_outline(outline):
        if section is not None:
            raise ValueError("Legacy materialization does not support bounded --section migration.")
        return legacy.materialize(product_dir)

    claims_doc = read_json(product_dir / "01_research" / "claim-ledger.json")
    sources_doc = read_json(product_dir / "01_research" / "source-index.json")
    contract_errors = validate_outline_contract(
        outline,
        {item.get("id") for item in claims_doc.get("claims", []) if isinstance(item, dict) and item.get("id")},
        product.get("target"),
    )
    if contract_errors:
        raise ValueError("Invalid approved outline: " + "; ".join(contract_errors))
    outline = normalize_outline_contract(outline, product.get("target"))
    if outline.get("schema_version") != OUTLINE_SCHEMA_VERSION:
        raise ValueError("Historical Substrate materialization requires current outline contract.")

    substrate_path = product_dir / "01_research" / "historical-substrate.json"
    if not substrate_path.is_file():
        raise ValueError("Direct-authorship materialization requires 01_research/historical-substrate.json.")
    substrate = read_json(substrate_path)
    substrate_errors = validate_historical_substrate(
        substrate,
        claims_doc,
        sources_doc,
        require_product_complete=section is None,
        required_sections={section} if section else None,
    )
    if substrate_errors:
        scope = "whole-product" if section is None else f"section {section}"
        raise ValueError(f"Historical Substrate is not ready for {scope} materialization: " + "; ".join(substrate_errors))

    if section is None:
        targets = [item["id"] for item in outline.get("sections", []) if isinstance(item, dict)]
    else:
        targets = [section]

    created: list[Path] = []
    for section_id in targets:
        created.extend(
            _materialize_direct_section(
                product_dir,
                outline,
                outline_path,
                product,
                claims_doc,
                sources_doc,
                substrate,
                section_id,
            )
        )

    if section is None:
        product.setdefault("stages", {})["sections"] = "ready_for_draft"
        product["status"] = "sections_materialized"
        product.setdefault("production_cycle", {})["status"] = "sections_materialized"
        write_json(product_path, product)
    return created


def archive_previous_cycle(product_dir: Path) -> list[Path]:
    return legacy.archive_previous_cycle(product_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--section", help="Materialize one covered migrated section (P##).")
    parser.add_argument("--archive-previous-cycle", action="store_true")
    args = parser.parse_args()
    try:
        archived = archive_previous_cycle(args.product) if args.archive_previous_cycle else []
        created = materialize(args.product, section=args.section)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Archived {len(archived)} old section workspace(s); materialized {len(created)} artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
