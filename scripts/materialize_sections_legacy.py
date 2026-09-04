#!/usr/bin/env python3
"""Create cycle-safe section workspaces and deterministic route-neutral writer handoffs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
    from scripts.historical_substrate_contract import (
        materialize_writer_section_substrate,
        validate_historical_substrate,
        validate_section_binding,
    )
    from scripts.outline_contract import (
        OUTLINE_SCHEMA_VERSION,
        normalize_outline_contract,
        render_outline_value,
        render_section_question_payoff,
        validate_outline_contract,
    )
    from scripts.story_plan_contract import build_narration_pack, empty_story_plan, is_direct_authorship_outline
except ModuleNotFoundError:
    from common import read_json, sha256, write_json
    from historical_substrate_contract import (
        materialize_writer_section_substrate,
        validate_historical_substrate,
        validate_section_binding,
    )
    from outline_contract import (
        OUTLINE_SCHEMA_VERSION,
        normalize_outline_contract,
        render_outline_value,
        render_section_question_payoff,
        validate_outline_contract,
    )
    from story_plan_contract import build_narration_pack, empty_story_plan, is_direct_authorship_outline


def materialize(product_dir: Path) -> list[Path]:
    product_dir = product_dir.resolve()
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    product_path = product_dir / "product.json"
    product = read_json(product_path)
    if outline.get("status") != "approved":
        raise ValueError("Outline must be human-approved before section materialization.")

    claims_doc = read_json(product_dir / "01_research" / "claim-ledger.json")
    sources_doc = read_json(product_dir / "01_research" / "source-index.json")
    claims = {item["id"]: item for item in claims_doc.get("claims", []) if isinstance(item, dict) and item.get("id")}
    sources = {item["id"]: item for item in sources_doc.get("sources", []) if isinstance(item, dict) and item.get("id")}

    contract_errors = validate_outline_contract(outline, set(claims), product.get("target"))
    if contract_errors:
        raise ValueError("Invalid approved outline: " + "; ".join(contract_errors))
    outline = normalize_outline_contract(outline, product.get("target"))
    current_contract = outline.get("schema_version") == OUTLINE_SCHEMA_VERSION
    direct_authorship = is_direct_authorship_outline(outline)

    historical_substrate: dict[str, Any] | None = None
    if direct_authorship:
        substrate_path = product_dir / "01_research" / "historical-substrate.json"
        if not substrate_path.is_file():
            raise ValueError(
                "Direct-authorship materialization requires 01_research/historical-substrate.json."
            )
        historical_substrate = read_json(substrate_path)
        substrate_errors = validate_historical_substrate(
            historical_substrate,
            claims_doc,
            sources_doc,
            require_product_complete=True,
        )
        if substrate_errors:
            raise ValueError("Historical Substrate is not ready for whole-outline materialization: " + "; ".join(substrate_errors))

    cycle_id = product.get("production_cycle", {}).get("id")
    if current_contract and cycle_id and outline.get("cycle_id") != cycle_id:
        raise ValueError(f"Outline cycle {outline.get('cycle_id')} does not match product cycle {cycle_id}.")

    sections = outline.get("sections", [])
    acts = {
        item["id"]: item
        for item in outline.get("script_architecture", {}).get("acts", [])
        if isinstance(item, dict) and item.get("id")
    }
    movements = {
        item["id"]: item
        for item in outline.get("script_architecture", {}).get("movements", [])
        if isinstance(item, dict) and item.get("id")
    }
    created: list[Path] = []

    for item in sections:
        section_id = item.get("id", "")
        if not re.fullmatch(r"P\d{2}", section_id):
            raise ValueError(f"Invalid section ID: {section_id}")
        root = product_dir / "03_sections" / section_id
        root.mkdir(parents=True, exist_ok=True)
        section_movements = (
            [movements[movement_id] for movement_id in item["movement_ids"]]
            if current_contract
            else [movements[item["movement_id"]]]
        )
        section_path = root / "section.json"
        existing_state: dict[str, Any] | None = None
        if section_path.exists() and current_contract:
            existing_state = read_json(section_path)
            if existing_state.get("cycle_id") != cycle_id:
                raise ValueError(
                    f"Existing {section_id} belongs to an earlier production cycle; archive it before materializing {cycle_id}."
                )
            if existing_state.get("status") not in {"outline_amended", "ready_for_draft", "needs_story_plan"}:
                raise ValueError(
                    f"Existing {section_id} is already in production state {existing_state.get('status')!r}; "
                    "do not overwrite it with a rematerialization."
                )

        mission: str | None = None
        historical_territory: str | None = None
        if direct_authorship:
            assert historical_substrate is not None
            binding_errors = validate_section_binding(item, historical_substrate)
            if binding_errors:
                raise ValueError(
                    f"Direct-authorship section {section_id} is not bound to Historical Substrate: "
                    + "; ".join(binding_errors)
                )
            historical_territory = str(item["historical_territory"]).strip()
            # mission is a compatibility alias only. Never propagate an old answer-shaped
            # question into the Writer-facing section state.
            mission = historical_territory

        state = {
            "schema_version": 4 if direct_authorship else (2 if current_contract else 1),
            "id": section_id,
            "title": item["title"],
            "order": item["order"],
            "status": "ready_for_draft" if direct_authorship else "needs_story_plan",
            "human_approved": False,
            "dependencies": item.get("dependencies", []),
            "narrative_job": item["narrative_job"],
            "entry_state": item["entry_state"],
            "exit_state": item["exit_state"],
            "target_words": item["target_words"],
            "cycle_id": cycle_id,
            "outline_sha256": sha256(outline_path),
        }
        if mission is not None:
            state["historical_substrate_contract_version"] = 1
            state["historical_territory"] = historical_territory
            state["mission"] = mission
            state["historical_substrate_ids"] = list(item["historical_substrate_ids"])
        if isinstance(item.get("transition"), str) and item["transition"].strip():
            state["transition"] = item["transition"].strip()
        hist_change = item.get("historical_change") or item.get("historical_movement")
        if hist_change is not None:
            state["historical_change"] = hist_change
        # audience_discovery / earned_meaning may remain in section state for owner/reviewer
        # evaluation, but canonical Writer projection does not expose them.
        audience_discovery = item.get("audience_discovery")
        if isinstance(audience_discovery, str) and audience_discovery.strip():
            state["audience_discovery"] = audience_discovery.strip()
        elif isinstance(item.get("earned_meaning"), str) and item["earned_meaning"].strip():
            state["audience_discovery"] = item["earned_meaning"].strip()
        if current_contract:
            section_acts = list(dict.fromkeys(movement["act_id"] for movement in section_movements))
            state["movement_ids"] = [movement["id"] for movement in section_movements]
            state["macro_movements"] = [
                {
                    "id": movement["id"],
                    "title": movement["title"],
                    "narrative_job": movement["narrative_job"],
                    "entry_state": movement["entry_state"],
                    "exit_state": movement["exit_state"],
                }
                for movement in section_movements
            ]
            state["acts"] = [
                {"id": acts[act_id]["id"], "role": acts[act_id]["role"], "title": acts[act_id]["title"]}
                for act_id in section_acts
            ]
        else:
            movement = section_movements[0]
            state.update(
                {
                    "movement_id": item["movement_id"],
                    "macro_movement": {
                        "id": movement["id"],
                        "title": movement["title"],
                        "narrative_job": movement["narrative_job"],
                        "entry_state": movement["entry_state"],
                        "exit_state": movement["exit_state"],
                    },
                    "structural_role": item["structural_role"],
                    "planned_moves": item["planned_moves"],
                    "budget_rationale": item["budget_rationale"],
                }
            )
        write_json(section_path, state)
        created.append(section_path)

        brief = root / "brief.md"
        if current_contract:
            section_acts = list(dict.fromkeys(movement["act_id"] for movement in section_movements))
            act_lines = [f"{acts[act_id]['role']} — {acts[act_id]['title']}" for act_id in section_acts]
            movement_lines = [f"{movement['id']} — {movement['title']}" for movement in section_movements]
            transition = render_outline_value(item.get("transition"), "Section kế tiếp theo whole-product progression.")
            evidence_territory = render_outline_value(item.get("claim_ids"), "Không có claim allowance.")
            historical_block = ""
            if direct_authorship:
                historical_block = (
                    f"\n\n## Historical territory\n\n{historical_territory}"
                    f"\n\n## Historical change\n\n"
                    f"From: {item['historical_change']['from']}\n\nTo: {item['historical_change']['to']}"
                    f"\n\n## Historical Substrate IDs\n\n{render_outline_value(item.get('historical_substrate_ids'))}"
                )
            legacy_anchor_block = ""
            if not direct_authorship:
                legacy_anchor_block = f"\n\n## Anchor options\n\n{render_outline_value(item.get('anchor_options'))}"
            text = (
                f"# {section_id} — {item['title']}\n\n"
                f"Cycle: `{cycle_id}`\n\n"
                f"## Whole-script acts\n\n{render_outline_value(act_lines)}\n\n"
                f"## Macro movements\n\n{render_outline_value(movement_lines)}\n\n"
                f"## Section objective\n\n{item['narrative_job']}"
                f"{historical_block}\n\n"
                f"## Entry state\n\n{item['entry_state']}\n\n"
                f"## Exit state\n\n{item['exit_state']}\n\n"
                f"## Evidence authority\n\n{evidence_territory}"
                f"{legacy_anchor_block}\n\n"
                f"## Transition\n\n{transition}\n\n"
                f"## Continuity in\n\n{render_outline_value(item.get('continuity_in'))}\n\n"
                f"## Continuity out\n\n{render_outline_value(item.get('continuity_out'))}\n\n"
                f"## Non-goal\n\n{render_outline_value(item.get('non_goal'))}\n"
            )
        else:
            movement = section_movements[0]
            text = (
                f"# {section_id} — {item['title']}\n\n"
                f"## Macro movement\n\n{movement['id']} — {movement['title']}\n\n"
                f"## Structural role\n\n{item['structural_role']}\n\n"
                f"## Narrative job\n\n{item['narrative_job']}\n\n"
                f"## Entry state\n\n{item['entry_state']}\n\n"
                f"## Exit state\n\n{item['exit_state']}\n\n"
                f"{render_section_question_payoff(item)}\n\n"
                f"## Planned shape\n\n{render_outline_value(item.get('planned_moves'))}\n\n"
                f"## Anchor requirements\n\n{render_outline_value(item.get('anchor_requirements'))}\n\n"
                f"## Bridge in\n\n{item.get('bridge_in', '')}\n\n"
                f"## Bridge out\n\n{item.get('bridge_out', '')}\n\n"
                f"## Boundary\n\n{item.get('boundary', '')}\n\n"
                f"## Risk\n\n{item.get('risk', '')}\n"
            )
        brief.write_text(text, encoding="utf-8")
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
        evidence_doc = {
            "schema_version": 3 if direct_authorship else 1,
            "section": section_id,
            "claims": selected_claims,
            "sources": [sources[source_id] for source_id in sorted(selected_source_ids)],
            "rule": (
                "These claims define the section truth territory. Writer may use any subset and any narrative route. "
                "Source-level resolution may increase through bounded retrieval; new interpretation/generalization requires evidence authority."
            ),
        }
        if direct_authorship:
            evidence_doc.update(
                {
                    "cycle_id": cycle_id,
                    "outline_sha256": sha256(outline_path),
                    "claim_ids": list(item.get("claim_ids", [])),
                    "source_ids": sorted(selected_source_ids),
                }
            )
        write_json(evidence_path, evidence_doc)
        created.append(evidence_path)

        if direct_authorship:
            section_substrate_path = materialize_writer_section_substrate(product_dir, section_id)
            created.append(section_substrate_path)
            narration_path = root / "narration-pack.json"
            build_narration_pack(product_dir, section_id)
            created.append(narration_path)
        else:
            story_plan_path = root / "story-plan.json"
            if not story_plan_path.exists():
                write_json(story_plan_path, empty_story_plan(section_id, item["target_words"]))
                created.append(story_plan_path)

        continuity = root / "continuity-in.md"
        if not continuity.exists():
            dependencies = ", ".join(item.get("dependencies", [])) or "Không có."
            continuity.write_text(
                f"# Continuity Input — {section_id}\n\n"
                f"Cycle: `{cycle_id}`\n\n"
                f"Dependencies: {dependencies}\n\n"
                "## Prior handoff\n\nChưa có hoặc sẽ được task owner cập nhật trước drafting.\n\n"
                "## Canonical terms required here\n\nTham chiếu story bible.\n",
                encoding="utf-8",
            )
            created.append(continuity)

    if direct_authorship:
        product.setdefault("stages", {})["sections"] = "ready_for_draft"
        product["status"] = "sections_materialized"
        product.setdefault("production_cycle", {})["status"] = "sections_materialized"
        write_json(product_path, product)
    return created


def archive_previous_cycle(product_dir: Path) -> list[Path]:
    """Move superseded section workspaces into a recoverable product-local history tree."""

    product_dir = product_dir.resolve()
    product = read_json(product_dir / "product.json")
    cycle = product.get("production_cycle", {})
    current_id = cycle.get("id")
    previous_id = cycle.get("previous")
    if not current_id or not previous_id:
        raise ValueError("Product does not declare a previous production cycle to archive.")

    section_root = product_dir / "03_sections"
    history_root = section_root / "_history" / previous_id
    moved: list[Path] = []
    candidates = sorted(path for path in section_root.iterdir() if path.is_dir() and re.fullmatch(r"P\d{2}", path.name))
    for source in candidates:
        state_path = source / "section.json"
        if state_path.is_file() and read_json(state_path).get("cycle_id") == current_id:
            continue
        destination = history_root / source.name
        if destination.exists():
            raise ValueError(f"Archive destination already exists: {destination.relative_to(product_dir)}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.rename(destination)
        moved.append(destination)
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--archive-previous-cycle", action="store_true")
    args = parser.parse_args()
    try:
        archived = archive_previous_cycle(args.product) if args.archive_previous_cycle else []
        created = materialize(args.product)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Archived {len(archived)} old section workspace(s); materialized {len(created)} artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
