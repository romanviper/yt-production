#!/usr/bin/env python3
"""Record explicit human approvals or section change requests."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re

try:
    from scripts.common import narration_text, read_json, sha256, word_count, write_json
    from scripts.lifecycle import heal_active_pointer, settle_related_tasks, sync_section_progress
    from scripts.outline_contract import MAX_SECTION_WORDS, validate_outline_contract
    from scripts.outcome_eval_contract import review_verdict, validate_outcome_review
    from scripts.research_plan_contract import validate_research_plan_contract
    from scripts.story_plan_contract import build_narration_pack, validate_story_plan, verify_narration_pack
    from scripts.validate import validate_product
    from scripts.voice_profile_contract import set_voice_profile_status, validate_voice_profile
except ModuleNotFoundError:
    from common import narration_text, read_json, sha256, word_count, write_json
    from lifecycle import heal_active_pointer, settle_related_tasks, sync_section_progress
    from outline_contract import MAX_SECTION_WORDS, validate_outline_contract
    from outcome_eval_contract import review_verdict, validate_outcome_review
    from research_plan_contract import validate_research_plan_contract
    from story_plan_contract import build_narration_pack, validate_story_plan, verify_narration_pack
    from validate import validate_product
    from voice_profile_contract import set_voice_profile_status, validate_voice_profile


OUTLINE_HUMAN_EDIT_PATHS = {
    "outline.json": "02_outline/outline.json",
    "story-bible.md": "02_outline/story-bible.md",
    "voice-profile.md": "02_outline/voice-profile.md",
}
SECTION_HUMAN_EDIT_FILES = {"story-plan.json", "draft.md", "handoff.md"}


def update_stage(product_dir: Path, stage: str, value: str) -> None:
    path = product_dir / "product.json"
    product = read_json(path)
    product.setdefault("stages", {})[stage] = value
    write_json(path, product)


def _complete_human_approval(
    product_dir: Path,
    *,
    reason: str,
    operations: set[str],
    section: str | None = None,
    sync_sections: bool = False,
) -> None:
    """Finish approval bookkeeping without making routing metadata authoritative."""

    settle_related_tasks(
        product_dir,
        section=section,
        operations=operations,
        final_state="closed",
        reason=reason,
    )
    # ACTIVE is disposable routing metadata. Heal stale/terminal pointers, but
    # preserve a genuinely live unrelated owner for conflict detection.
    heal_active_pointer(product_dir)
    if sync_sections:
        sync_section_progress(product_dir)


def _amendment_id() -> str:
    return "HA-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def _require_human_request(request: str) -> str:
    value = request.strip()
    if not value:
        raise ValueError("Human amendment request cannot be empty.")
    return value


def _supersede_active_task(product_dir: Path, amendment_id: str, approved_at: str) -> str | None:
    """Clear router state that a direct human amendment intentionally supersedes."""

    active_path = product_dir / "tasks" / "ACTIVE.json"
    if not active_path.is_file():
        return None
    active = read_json(active_path)
    task_id = active.get("task_id")
    if task_id:
        work_path = product_dir / "tasks" / task_id / "work-order.json"
        if work_path.is_file():
            work = read_json(work_path)
            if work.get("state") not in {"closed", "cancelled"}:
                work["state"] = "cancelled"
                work["updated_at"] = approved_at
                work["superseded_by"] = amendment_id
                write_json(work_path, work)
    write_json(
        active_path,
        {
            "task_id": None,
            "status": "idle",
            "updated_at": approved_at,
            "superseded_by": amendment_id,
        },
    )
    return str(task_id) if task_id else None


def _record_human_amendment(
    product_dir: Path,
    amendment_id: str,
    target_kind: str,
    request: str,
    selected: list[Path],
    approved_at: str,
    section: str | None = None,
    superseded_task: str | None = None,
) -> dict:
    record = {
        "schema_version": 1,
        "id": amendment_id,
        "target_kind": target_kind,
        "section": section,
        "request": request,
        "approved_by": "user",
        "approved_at": approved_at,
        "accepted_files": [
            {
                "path": path.resolve().relative_to(product_dir.resolve()).as_posix(),
                "sha256": sha256(path),
            }
            for path in selected
        ],
        "superseded_task": superseded_task,
    }
    log_path = product_dir / "human-amendments.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return record


def _resolve_outline_human_paths(product_dir: Path, names: list[str]) -> list[Path]:
    if not names:
        raise ValueError("Human outline amendment requires at least one --path.")
    selected: list[Path] = []
    for name in names:
        relative = OUTLINE_HUMAN_EDIT_PATHS.get(name, name)
        if relative not in OUTLINE_HUMAN_EDIT_PATHS.values():
            raise ValueError(f"Human outline edit path is outside the allowed output scope: {name}")
        path = product_dir / relative
        if not path.is_file():
            raise FileNotFoundError(f"Missing human-edited output: {relative}")
        selected.append(path)
    return list(dict.fromkeys(selected))


def _resolve_section_human_paths(product_dir: Path, section: str, names: list[str]) -> list[Path]:
    if not re.fullmatch(r"P\d{2}", section):
        raise ValueError(f"Invalid section ID: {section}")
    if not names:
        raise ValueError("Human section amendment requires at least one --path.")
    selected: list[Path] = []
    prefix = f"03_sections/{section}/"
    for name in names:
        filename = name.removeprefix(prefix)
        if filename not in SECTION_HUMAN_EDIT_FILES or "/" in filename:
            raise ValueError(f"Human section edit path is outside the allowed output scope: {name}")
        path = product_dir / prefix / filename
        if not path.is_file():
            raise FileNotFoundError(f"Missing human-edited output: {prefix}{filename}")
        selected.append(path)
    return list(dict.fromkeys(selected))


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
    _complete_human_approval(
        product_dir,
        reason="human approved research plan",
        operations={"research_plan"},
    )


def approve_outline(product_dir: Path) -> None:
    path = product_dir / "02_outline" / "outline.json"
    outline = read_json(path)
    product = read_json(product_dir / "product.json")
    expected_cycle = product.get("production_cycle", {}).get("id")
    if expected_cycle and outline.get("cycle_id") != expected_cycle:
        raise ValueError(f"Cannot approve outline: cycle_id must match current product cycle {expected_cycle}")
    contract_errors = validate_outline_contract(outline, product_target=product.get("target"), require_current=True)
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
    _complete_human_approval(
        product_dir,
        reason="human approved outline",
        operations={"outline"},
    )


def human_amend_outline(product_dir: Path, request: str, paths: list[str]) -> dict:
    """Accept an explicitly user-directed outline edit without creating an AI task."""

    product_dir = product_dir.resolve()
    request = _require_human_request(request)
    selected = _resolve_outline_human_paths(product_dir, paths)
    selected_names = {path.name for path in selected}
    outline_path = product_dir / "02_outline" / "outline.json"
    voice_path = product_dir / "02_outline" / "voice-profile.md"
    story_bible_path = product_dir / "02_outline" / "story-bible.md"
    outline = read_json(outline_path)
    product_path = product_dir / "product.json"
    product = read_json(product_path)
    claims = read_json(product_dir / "01_research" / "claim-ledger.json")
    claim_ids = {item.get("id") for item in claims.get("claims", []) if item.get("id")}
    expected_cycle = product.get("production_cycle", {}).get("id")
    if expected_cycle and outline.get("cycle_id") != expected_cycle:
        raise ValueError(f"Human outline edit must match current product cycle {expected_cycle}.")
    contract_errors = validate_outline_contract(outline, claim_ids, product.get("target"), require_current=True)
    if contract_errors:
        raise ValueError("Cannot accept human outline edit: " + "; ".join(contract_errors))
    if not story_bible_path.read_text(encoding="utf-8").strip():
        raise ValueError("Cannot accept human outline edit: story bible is empty.")
    approved_voice = set_voice_profile_status(voice_path.read_text(encoding="utf-8"), "approved")
    voice_errors = validate_voice_profile(approved_voice)
    if voice_errors:
        raise ValueError("Cannot accept human voice-profile edit: " + "; ".join(voice_errors))

    approved_at = datetime.now(timezone.utc).isoformat()
    amendment_id = _amendment_id()
    outline.update(
        {
            "status": "approved",
            "approved_by": "user",
            "approved_at": approved_at,
            "last_human_amendment": amendment_id,
        }
    )
    write_json(outline_path, outline)
    voice_path.write_text(approved_voice, encoding="utf-8")

    product.setdefault("stages", {})["outline"] = "approved"
    product["status"] = "outline_approved"
    product.setdefault("production_cycle", {})["status"] = "outline_approved"
    if "outline.json" in selected_names:
        current_states: list[Path] = []
        for state_path in sorted((product_dir / "03_sections").glob("P??/section.json")):
            state = read_json(state_path)
            if expected_cycle and state.get("cycle_id") != expected_cycle:
                continue
            state.update(
                {
                    "status": "outline_amended",
                    "human_approved": False,
                    "outline_amendment": amendment_id,
                }
            )
            state.pop("approved_by", None)
            state.pop("approved_at", None)
            write_json(state_path, state)
            current_states.append(state_path)
        product["stages"]["sections"] = "human_sync_required" if current_states else "ready_to_materialize"
        product["stages"]["integration"] = "not_started"
        product["stages"]["delivery"] = "not_started"
    write_json(product_path, product)

    superseded_task = _supersede_active_task(product_dir, amendment_id, approved_at)
    return _record_human_amendment(
        product_dir,
        amendment_id,
        "outline",
        request,
        selected,
        approved_at,
        superseded_task=superseded_task,
    )


def approve_section(product_dir: Path, section: str) -> None:
    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)
    if state.get("status") != "review_complete":
        raise ValueError(f"Section {section} requires a completed outcome review before human approval.")
    review_path = root / "review.md"
    review_text = review_path.read_text(encoding="utf-8")
    review_provenance = state.get("review_provenance")
    review_contract_version = (
        int(review_provenance.get("contract_version", 1))
        if isinstance(review_provenance, dict)
        else 1
    )
    if isinstance(review_provenance, dict) and review_provenance.get("review_sha256") != sha256(review_path):
        raise ValueError(f"Section {section} outcome review differs from submitted review provenance.")
    strict_review = review_contract_version >= 2
    review_errors = validate_outcome_review(
        review_text,
        require_mission_outcomes=strict_review,
        require_production_gate=strict_review,
        contract_version=review_contract_version,
        section=section,
    )
    if review_errors:
        raise ValueError("Section outcome review is invalid: " + "; ".join(review_errors))
    if review_verdict(review_text) != "pass":
        raise ValueError(f"Section {section} outcome review has not passed.")
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
    _complete_human_approval(
        product_dir,
        reason=f"human approved section {section}",
        operations={"draft_section", "revise_section", "review_section"},
        section=section,
        sync_sections=True,
    )


def approve_story_plan(product_dir: Path, section: str) -> None:
    root = product_dir / "03_sections" / section
    plan_path = root / "story-plan.json"
    plan = read_json(plan_path)
    evidence = read_json(root / "evidence-pack.json")
    state_path = root / "section.json"
    state = read_json(state_path)
    claim_ids = {item.get("id") for item in evidence.get("claims", []) if item.get("id")}
    errors = validate_story_plan(plan, claim_ids, state.get("target_words"), require_current=True)
    if errors:
        raise ValueError("Cannot approve story plan: " + "; ".join(errors))
    approved_at = datetime.now(timezone.utc).isoformat()
    recommended = plan["word_budget"]["recommended"]
    current_budget = state["target_words"]
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    resized_outline = deepcopy(outline)
    resized_state = deepcopy(state)
    if recommended != current_budget:
        matching = [item for item in resized_outline.get("sections", []) if item.get("id") == section]
        if len(matching) != 1:
            raise ValueError(f"Cannot resize {section}: outline section is missing or duplicated.")
        if matching[0].get("target_words") != current_budget:
            raise ValueError(f"Cannot resize {section}: section and outline budgets are out of sync.")
        reason = plan["word_budget"]["rationale"].strip()
        matching[0]["target_words"] = recommended
        matching[0]["budget_rationale"] = reason
        architecture = resized_outline.setdefault("script_architecture", {})
        architecture.setdefault("budget_revisions", []).append(
            {
                "section": section,
                "from": current_budget,
                "to": recommended,
                "reason": reason,
                "approved_by": "user",
                "approved_at": approved_at,
            }
        )
        resized_state["target_words"] = recommended
        resized_state["budget_rationale"] = reason
        product = read_json(product_dir / "product.json")
        outline_errors = validate_outline_contract(resized_outline, product_target=product.get("target"))
        if outline_errors:
            raise ValueError("Cannot apply story-plan word budget: " + "; ".join(outline_errors))
        plan["word_budget"]["accepted_resize_from"] = current_budget
    plan["status"] = "approved"
    plan["approved_by"] = "user"
    plan["approved_at"] = approved_at
    if resized_outline != outline:
        write_json(outline_path, resized_outline)
        write_json(state_path, resized_state)
    write_json(plan_path, plan)
    build_narration_pack(product_dir, section)
    state = read_json(state_path)
    state.update({"status": "ready_for_draft", "human_approved": False})
    write_json(state_path, state)
    _complete_human_approval(
        product_dir,
        reason=f"human approved story plan for {section}",
        operations={"design_section"},
        section=section,
        sync_sections=True,
    )


def human_amend_section(product_dir: Path, section: str, request: str, paths: list[str]) -> dict:
    """Accept user-directed story-plan or prose edits without design/review tasks."""

    product_dir = product_dir.resolve()
    request = _require_human_request(request)
    selected = _resolve_section_human_paths(product_dir, section, paths)
    selected_names = {path.name for path in selected}
    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)
    approved_at = datetime.now(timezone.utc).isoformat()
    amendment_id = _amendment_id()

    if "story-plan.json" in selected_names:
        plan_path = root / "story-plan.json"
        plan = read_json(plan_path)
        plan["status"] = "draft"
        plan.pop("approved_by", None)
        plan.pop("approved_at", None)
        write_json(plan_path, plan)
        approve_story_plan(product_dir, section)

    prose_changed = bool(selected_names & {"draft.md", "handoff.md"})
    if prose_changed:
        pack_errors = verify_narration_pack(product_dir, section)
        if pack_errors:
            raise ValueError(
                "Cannot accept human prose edit until the story plan and narration pack are valid: "
                + "; ".join(pack_errors)
            )
        draft_path = root / "draft.md"
        handoff_path = root / "handoff.md"
        if not draft_path.is_file() or not handoff_path.is_file():
            raise FileNotFoundError(f"Human prose amendment requires both {section}/draft.md and {section}/handoff.md.")
        draft_words = word_count(narration_text(draft_path.read_text(encoding="utf-8"), section))
        if not 1 <= draft_words <= MAX_SECTION_WORDS:
            raise ValueError(f"Human-edited draft must stay inside the 1–{MAX_SECTION_WORDS} production-unit hard cap.")
        if word_count(handoff_path.read_text(encoding="utf-8")) > 500:
            raise ValueError("Human-edited section handoff exceeds 500 words.")
        state = read_json(state_path)
        state.update(
            {
                "status": "approved",
                "human_approved": True,
                "approved_by": "user",
                "approved_at": approved_at,
                "approval_basis": "human_direct_edit",
                "last_human_amendment": amendment_id,
            }
        )
        write_json(state_path, state)

        product_path = product_dir / "product.json"
        product = read_json(product_path)
        outline = read_json(product_dir / "02_outline" / "outline.json")
        section_ids = [item.get("id") for item in outline.get("sections", []) if item.get("id")]
        all_approved = bool(section_ids)
        for section_id in section_ids:
            candidate = product_dir / "03_sections" / section_id / "section.json"
            if not candidate.is_file():
                all_approved = False
                break
            candidate_state = read_json(candidate)
            if candidate_state.get("status") != "approved" or candidate_state.get("human_approved") is not True:
                all_approved = False
                break
        product.setdefault("stages", {})["sections"] = "approved" if all_approved else "in_progress"
        write_json(product_path, product)
    elif "story-plan.json" in selected_names:
        state = read_json(state_path)
        state["last_human_amendment"] = amendment_id
        write_json(state_path, state)

    superseded_task = _supersede_active_task(product_dir, amendment_id, approved_at)
    return _record_human_amendment(
        product_dir,
        amendment_id,
        "section",
        request,
        selected,
        approved_at,
        section=section,
        superseded_task=superseded_task,
    )


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


def start_new_cycle(product_dir: Path, request: str) -> str:
    """Reopen whole-product architecture after an explicit owner decision."""

    if not request.strip():
        raise ValueError("Production-cycle request cannot be empty.")
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    if outline.get("status") != "approved":
        raise ValueError("A new production cycle can start only from an approved outline.")

    product_path = product_dir / "product.json"
    product = read_json(product_path)
    previous_id = product.get("production_cycle", {}).get("id", "C001")
    match = re.fullmatch(r"C(\d{3})", str(previous_id))
    if not match:
        raise ValueError(f"Invalid current production cycle: {previous_id}")
    cycle_id = f"C{int(match.group(1)) + 1:03d}"
    started_at = datetime.now(timezone.utc).isoformat()

    (product_dir / "02_outline" / "outline-change-request.md").write_text(
        f"# Outline Change Request — {cycle_id}\n\n"
        f"Requested by: user\n\nRequested at: {started_at}\n\n"
        f"Previous cycle: {previous_id}\n\n"
        f"## Required architecture change\n\n{request.strip()}\n",
        encoding="utf-8",
    )

    outline["status"] = "draft"
    outline["cycle_id"] = cycle_id
    outline.pop("approved_by", None)
    outline.pop("approved_at", None)
    write_json(outline_path, outline)

    voice_path = product_dir / "02_outline" / "voice-profile.md"
    voice_path.write_text(set_voice_profile_status(voice_path.read_text(encoding="utf-8"), "draft"), encoding="utf-8")

    product["production_cycle"] = {
        "id": cycle_id,
        "status": "outline_design",
        "previous": previous_id,
        "started_at": started_at,
        "reason": request.strip(),
    }
    product["status"] = "outline_redesign"
    product.setdefault("stages", {})["outline"] = "changes_requested"
    product["stages"]["sections"] = "paused"
    product["stages"]["integration"] = "not_started"
    product["stages"]["delivery"] = "not_started"
    write_json(product_path, product)
    return cycle_id


def request_story_plan_changes(product_dir: Path, section: str, request: str) -> None:
    if not request.strip():
        raise ValueError("Story-plan change request cannot be empty.")
    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)
    reviewable_states = {"story_plan_review", "ready_for_review", "review_complete", "approved"}
    if state.get("status") not in reviewable_states:
        raise ValueError(f"Story plan {section} is not at a human review checkpoint.")
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
    plan_path = root / "story-plan.json"
    plan = read_json(plan_path)
    plan["status"] = "draft"
    plan.pop("approved_by", None)
    plan.pop("approved_at", None)
    write_json(plan_path, plan)


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
    cycle = sub.add_parser("start-new-cycle")
    cycle.add_argument("product", type=Path)
    cycle.add_argument("--request", required=True)
    outline_edit = sub.add_parser("human-amend-outline")
    outline_edit.add_argument("product", type=Path)
    outline_edit.add_argument("--request", required=True)
    outline_edit.add_argument("--path", action="append", required=True)
    section_edit = sub.add_parser("human-amend-section")
    section_edit.add_argument("product", type=Path)
    section_edit.add_argument("section")
    section_edit.add_argument("--request", required=True)
    section_edit.add_argument("--path", action="append", required=True)
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
        elif args.command == "start-new-cycle":
            start_new_cycle(product, args.request)
        elif args.command == "human-amend-outline":
            human_amend_outline(product, args.request, args.path)
        elif args.command == "human-amend-section":
            human_amend_section(product, args.section, args.request, args.path)
        else:
            request_story_plan_changes(product, args.section, args.request)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Recorded user action: {args.command}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
