#!/usr/bin/env python3
"""Create isolated section workspaces, evidence pools, and story-plan seeds."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, write_json
    from scripts.outline_contract import render_outline_value, render_section_question_payoff, validate_outline_contract
    from scripts.story_plan_contract import empty_story_plan
except ModuleNotFoundError:
    from common import read_json, write_json
    from outline_contract import render_outline_value, render_section_question_payoff, validate_outline_contract
    from story_plan_contract import empty_story_plan


def materialize(product_dir: Path) -> list[Path]:
    product_dir = product_dir.resolve()
    outline = read_json(product_dir / "02_outline" / "outline.json")
    if outline.get("status") != "approved":
        raise ValueError("Outline must be human-approved before section materialization.")
    claims_doc = read_json(product_dir / "01_research" / "claim-ledger.json")
    sources_doc = read_json(product_dir / "01_research" / "source-index.json")
    claims = {item["id"]: item for item in claims_doc.get("claims", [])}
    sources = {item["id"]: item for item in sources_doc.get("sources", [])}
    contract_errors = validate_outline_contract(outline, set(claims))
    if contract_errors:
        raise ValueError("Invalid approved outline: " + "; ".join(contract_errors))
    sections = outline.get("sections", [])
    created: list[Path] = []

    for item in sections:
        section_id = item.get("id", "")
        if not re.fullmatch(r"P\d{2}", section_id):
            raise ValueError(f"Invalid section ID: {section_id}")
        root = product_dir / "03_sections" / section_id
        root.mkdir(parents=True, exist_ok=True)
        section_path = root / "section.json"
        if not section_path.exists():
            write_json(
                section_path,
                {
                    "schema_version": 1,
                    "id": section_id,
                    "title": item["title"],
                    "order": item["order"],
                    "status": "needs_story_plan",
                    "human_approved": False,
                    "dependencies": item.get("dependencies", []),
                    "target_words": item["target_words"],
                },
            )
            created.append(section_path)
        brief = root / "brief.md"
        if not brief.exists():
            brief.write_text(
                f"# {section_id} — {item['title']}\n\n"
                f"## Narrative job\n\n{item['narrative_job']}\n\n"
                f"## Entry state\n\n{item['entry_state']}\n\n"
                f"## Exit state\n\n{item['exit_state']}\n\n"
                f"{render_section_question_payoff(item)}\n\n"
                f"## Anchor requirements\n\n{render_outline_value(item.get('anchor_requirements'))}\n\n"
                f"## Bridge in\n\n{item.get('bridge_in', '')}\n\n"
                f"## Bridge out\n\n{item.get('bridge_out', '')}\n\n"
                f"## Boundary\n\n{item.get('boundary', '')}\n\n"
                f"## Risk\n\n{item.get('risk', '')}\n",
                encoding="utf-8",
            )
            created.append(brief)

        selected_claims: list[dict[str, Any]] = []
        selected_source_ids: set[str] = set()
        for claim_id in item.get("claim_ids", []):
            if claim_id not in claims:
                raise ValueError(f"{section_id} references missing claim {claim_id}")
            claim = claims[claim_id]
            if claim.get("status") not in {"supported", "qualified"}:
                raise ValueError(f"{section_id} claim is not writing-ready: {claim_id}")
            selected_claims.append(claim)
            selected_source_ids.update(claim.get("sources", []))
        missing_sources = selected_source_ids - sources.keys()
        if missing_sources:
            raise ValueError(f"{section_id} claims reference missing sources: {sorted(missing_sources)}")
        unreviewed = [source_id for source_id in selected_source_ids if sources[source_id].get("status") != "reviewed"]
        if unreviewed:
            raise ValueError(f"{section_id} sources are not reviewed: {sorted(unreviewed)}")
        evidence_path = root / "evidence-pack.json"
        if not evidence_path.exists():
            write_json(
                evidence_path,
                {
                    "schema_version": 1,
                    "section": section_id,
                    "claims": selected_claims,
                    "sources": [sources[source_id] for source_id in sorted(selected_source_ids)],
                    "rule": "Only claims in this pack may appear as substantive historical claims in the draft.",
                },
            )
            created.append(evidence_path)
        story_plan_path = root / "story-plan.json"
        if not story_plan_path.exists():
            write_json(story_plan_path, empty_story_plan(section_id))
            created.append(story_plan_path)
        continuity = root / "continuity-in.md"
        if not continuity.exists():
            dependencies = ", ".join(item.get("dependencies", [])) or "Không có."
            continuity.write_text(
                f"# Continuity Input — {section_id}\n\n"
                f"Dependencies: {dependencies}\n\n"
                "## Prior handoff\n\nChưa có hoặc sẽ được task owner cập nhật trước drafting.\n\n"
                "## Canonical terms required here\n\nTham chiếu story bible.\n",
                encoding="utf-8",
            )
            created.append(continuity)
    return created
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    args = parser.parse_args()
    try:
        created = materialize(args.product)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Materialized {len(created)} section artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
