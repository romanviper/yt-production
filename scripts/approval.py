#!/usr/bin/env python3
"""Record explicit human approvals or section change requests."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.common import read_json, write_json
    from scripts.outline_contract import validate_outline_contract
    from scripts.research_plan_contract import validate_research_plan_contract
    from scripts.story_plan_contract import build_narration_pack, validate_story_plan
    from scripts.validate import validate_product
    from scripts.voice_profile_contract import set_voice_profile_status, validate_voice_profile
except ModuleNotFoundError:
    from common import read_json, write_json
    from outline_contract import validate_outline_contract
    from research_plan_contract import validate_research_plan_contract
    from story_plan_contract import build_narration_pack, validate_story_plan
    from validate import validate_product
    from voice_profile_contract import set_voice_profile_status, validate_voice_profile


def update_stage(product_dir: Path, stage: str, value: str) -> None:
    path = product_dir / "product.json"
    product = read_json(path)
    product.setdefault("stages", {})[stage] = value
    write_json(path, product)


def approve_plan(product_dir: Path) -> None:
    path = product_dir / "01_research" / "plan.json"
    plan = read_json(path)
    contract_errors = validate_research_plan_contract(plan)
    if contract_errors:
        raise ValueError("Cannot approve research plan: " + "; ".join(contract_errors))
    plan["status"] = "approved"
    plan["approved_by"] = "user"
    plan["approved_at"] = datetime.now(timezone.utc).isoformat()
    write_json(path, plan)
    update_stage(product_dir, "research_plan", "approved")


def approve_outline(product_dir: Path) -> None:
    path = product_dir / "02_outline" / "outline.json"
    outline = read_json(path)
    contract_errors = validate_outline_contract(outline)
    if contract_errors:
        raise ValueError("Cannot approve outline: " + "; ".join(contract_errors))
    voice_path = product_dir / "02_outline" / "voice-profile.md"
    voice = voice_path.read_text(encoding="utf-8")
    voice_errors = validate_voice_profile(voice)
    if voice_errors:
        raise ValueError("Cannot approve voice profile: " + "; ".join(voice_errors))
    outline["status"] = "approved"
    outline["approved_by"] = "user"
    outline["approved_at"] = datetime.now(timezone.utc).isoformat()
    write_json(path, outline)
    original_voice = voice
    voice_path.write_text(set_voice_profile_status(voice, "approved"), encoding="utf-8")
    errors = [issue for issue in validate_product(product_dir) if issue.level == "ERROR"]
    # Ignore the expected materialization errors until materialize_sections runs.
    structural = [issue for issue in errors if "requires materialized section" not in issue.message]
    if structural:
        outline["status"] = "draft"
        outline.pop("approved_by", None)
        outline.pop("approved_at", None)
        write_json(path, outline)
        voice_path.write_text(original_voice, encoding="utf-8")
        raise ValueError("Outline validation failed: " + "; ".join(issue.message for issue in structural))
    update_stage(product_dir, "outline", "approved")


def approve_section(product_dir: Path, section: str) -> None:
    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)
    if state.get("status") not in {"ready_for_review", "review_complete"}:
        raise ValueError(f"Section {section} is not ready for human approval.")
    for name in ["draft.md", "handoff.md"]:
        if not (root / name).is_file():
            raise ValueError(f"Missing {section}/{name}")
    state.update(
        {
            "status": "approved",
            "human_approved": True,
            "approved_by": "user",
            "approved_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    write_json(state_path, state)


def approve_story_plan(product_dir: Path, section: str) -> None:
    root = product_dir / "03_sections" / section
    plan_path = root / "story-plan.json"
    plan = read_json(plan_path)
    evidence = read_json(root / "evidence-pack.json")
    claim_ids = {item.get("id") for item in evidence.get("claims", []) if item.get("id")}
    errors = validate_story_plan(plan, claim_ids)
    if errors:
        raise ValueError("Cannot approve story plan: " + "; ".join(errors))
    plan["status"] = "approved"
    plan["approved_by"] = "user"
    plan["approved_at"] = datetime.now(timezone.utc).isoformat()
    write_json(plan_path, plan)
    build_narration_pack(product_dir, section)
    state_path = root / "section.json"
    state = read_json(state_path)
    state.update({"status": "ready_for_draft", "human_approved": False})
    write_json(state_path, state)


def request_changes(product_dir: Path, section: str, request: str) -> None:
    if not request.strip():
        raise ValueError("Change request cannot be empty.")
    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)
    if state.get("status") not in {"ready_for_review", "review_complete", "approved"}:
        raise ValueError(f"Section {section} is not in a reviewable state.")
    (root / "change-request.md").write_text(
        f"# Change Request — {section}\n\n"
        f"Requested by: user\n\nRequested at: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"## Approved revision scope\n\n{request.strip()}\n",
        encoding="utf-8",
    )
    state.update({"status": "changes_requested", "human_approved": False})
    state.pop("approved_by", None)
    state.pop("approved_at", None)
    write_json(state_path, state)


def request_story_plan_changes(product_dir: Path, section: str, request: str) -> None:
    if not request.strip():
        raise ValueError("Story-plan change request cannot be empty.")
    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)
    if state.get("status") != "story_plan_review":
        raise ValueError(f"Story plan {section} is not awaiting human review.")
    (root / "story-plan-change-request.md").write_text(
        f"# Story Plan Change Request — {section}\n\n"
        f"Requested by: user\n\nRequested at: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"## Required changes\n\n{request.strip()}\n",
        encoding="utf-8",
    )
    state.update({"status": "story_plan_changes_requested", "human_approved": False})
    state.pop("approved_by", None)
    state.pop("approved_at", None)
    write_json(state_path, state)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ["approve-plan", "approve-outline"]:
        item = sub.add_parser(command)
        item.add_argument("product", type=Path)
    for command in ["approve-story-plan", "approve-section"]:
        section = sub.add_parser(command)
        section.add_argument("product", type=Path)
        section.add_argument("section")
    changes = sub.add_parser("request-changes")
    changes.add_argument("product", type=Path)
    changes.add_argument("section")
    changes.add_argument("--request", required=True)
    story_changes = sub.add_parser("request-story-plan-changes")
    story_changes.add_argument("product", type=Path)
    story_changes.add_argument("section")
    story_changes.add_argument("--request", required=True)
    args = parser.parse_args()
    product = args.product.resolve()
    try:
        if args.command == "approve-plan":
            approve_plan(product)
        elif args.command == "approve-outline":
            approve_outline(product)
        elif args.command == "approve-story-plan":
            approve_story_plan(product, args.section)
        elif args.command == "approve-section":
            approve_section(product, args.section)
        elif args.command == "request-changes":
            request_changes(product, args.section, args.request)
        else:
            request_story_plan_changes(product, args.section, args.request)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Recorded user action: {args.command}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
