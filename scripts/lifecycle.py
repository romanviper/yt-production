#!/usr/bin/env python3
"""Canonical lifecycle rules for task routing, section operations, and human rework."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.common import read_json, write_json
    from scripts.story_plan_contract import verify_narration_pack
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import read_json, write_json
    from story_plan_contract import verify_narration_pack


TASK_LIVE_STATES = {"ready", "in_progress"}
TASK_TERMINAL_STATES = {"closed", "cancelled"}
TASK_STATES = TASK_LIVE_STATES | {"ready_for_review"} | TASK_TERMINAL_STATES

SECTION_OPERATION_ENTRY_STATES = {
    "design_section": {"needs_story_plan", "story_plan_changes_requested"},
    "draft_section": {"ready_for_draft"},
    "review_section": {"ready_for_review"},
    "revise_section": {"changes_requested"},
}

SECTION_OPERATION_SUBMISSION_STATES = {
    "design_section": "story_plan_review",
    "draft_section": "ready_for_review",
    "review_section": "review_complete",
    "revise_section": "ready_for_review",
}

SECTION_OPERATION_REWORK_STATES = {
    "design_section": "story_plan_changes_requested",
    "draft_section": "ready_for_draft",
    "review_section": "ready_for_review",
    "revise_section": "changes_requested",
}


def section_operation_state_error(operation: str, status: str | None, section: str | None) -> str | None:
    expected = SECTION_OPERATION_ENTRY_STATES.get(operation)
    if expected is None:
        return None
    if status not in expected:
        allowed = ", ".join(sorted(expected))
        return f"{section} status {status!r} does not allow {operation}; expected one of: {allowed}."
    return None


def task_transition_errors(current: str | None, target: str) -> list[str]:
    if current not in TASK_STATES:
        return [f"unknown task state: {current!r}"]
    if target not in TASK_STATES:
        return [f"unknown target task state: {target!r}"]
    if current in TASK_TERMINAL_STATES and target != current:
        return [f"terminal task state {current!r} cannot be reopened; create a fresh task or use semantic rework"]
    if target in TASK_LIVE_STATES and current not in TASK_LIVE_STATES:
        return [f"task state {current!r} cannot transition to {target!r}; create a fresh task or use semantic rework"]
    if target == "ready_for_review" and current not in TASK_LIVE_STATES | {"ready_for_review"}:
        return [f"task state {current!r} cannot become ready_for_review"]
    return []


def task_submit_errors(state: str | None) -> list[str]:
    if state not in TASK_LIVE_STATES:
        return [f"task state {state!r} cannot submit; create a fresh task or use semantic rework"]
    return []


def clear_human_approval(state: dict) -> None:
    state["human_approved"] = False
    for key in ["approved_by", "approved_at", "approval_basis"]:
        state.pop(key, None)


def apply_section_submission(product_dir: Path, operation: str, section: str | None) -> None:
    if not section or operation not in SECTION_OPERATION_SUBMISSION_STATES:
        return
    state_path = product_dir / "03_sections" / section / "section.json"
    state = read_json(state_path)
    state["status"] = SECTION_OPERATION_SUBMISSION_STATES[operation]
    write_json(state_path, state)
    if operation == "draft_section":
        (state_path.parent / "draft-rework-request.md").unlink(missing_ok=True)


def clear_active_pointer(product_dir: Path, task_id: str | None = None, *, reason: str | None = None) -> None:
    path = product_dir / "tasks" / "ACTIVE.json"
    if not path.is_file():
        return
    active = read_json(path)
    if task_id is not None and active.get("task_id") != task_id:
        return
    now = datetime.now(timezone.utc).isoformat()
    idle = {"task_id": None, "status": "idle", "updated_at": now}
    if reason:
        idle["reason"] = reason
    write_json(path, idle)


def cancel_active_task(
    product_dir: Path,
    *,
    reason: str,
    replacement: str | None = None,
) -> str | None:
    """Cancel the routed task, then clear ACTIVE. Task validity lives in work-order state, not the pointer."""

    product_dir = product_dir.resolve()
    path = product_dir / "tasks" / "ACTIVE.json"
    if not path.is_file():
        return None
    active = read_json(path)
    task_id = active.get("task_id")
    if not task_id:
        clear_active_pointer(product_dir, reason=reason)
        return None

    work_path = product_dir / "tasks" / str(task_id) / "work-order.json"
    if work_path.is_file():
        work = read_json(work_path)
        if work.get("state") not in TASK_TERMINAL_STATES:
            work["state"] = "cancelled"
            work["updated_at"] = datetime.now(timezone.utc).isoformat()
            work["cancel_reason"] = reason
            if replacement:
                work["superseded_by"] = replacement
            write_json(work_path, work)
    clear_active_pointer(product_dir, str(task_id), reason=reason)
    return str(task_id)


def _write_request(path: Path, title: str, request: str) -> None:
    path.write_text(
        f"# {title}\n\n"
        f"Requested by: user\n\n"
        f"Requested at: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"## Request\n\n{request.strip()}\n",
        encoding="utf-8",
    )


def prepare_section_rework(product_dir: Path, operation: str, section: str, request: str) -> None:
    """Reopen one section operation from any downstream state while preserving upstream authority."""

    if operation not in SECTION_OPERATION_REWORK_STATES:
        raise ValueError(f"Operation {operation} is not a section rework operation.")
    if not request.strip():
        raise ValueError("Human rework request cannot be empty.")

    product_dir = product_dir.resolve()
    outline = read_json(product_dir / "02_outline" / "outline.json")
    if outline.get("status") != "approved":
        raise ValueError("Section rework requires a human-approved outline.")

    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)

    if operation == "design_section":
        plan_path = root / "story-plan.json"
        plan = read_json(plan_path)
        plan["status"] = "draft"
        plan.pop("approved_by", None)
        plan.pop("approved_at", None)
        write_json(plan_path, plan)
        _write_request(root / "story-plan-change-request.md", f"Story Plan Rework — {section}", request)
    elif operation == "draft_section":
        plan = read_json(root / "story-plan.json")
        if plan.get("status") != "approved":
            raise ValueError("Draft rework requires an approved story plan.")
        pack_errors = verify_narration_pack(product_dir, section)
        if pack_errors:
            raise ValueError("Draft rework requires a valid narration pack: " + "; ".join(pack_errors))
        _write_request(root / "draft-rework-request.md", f"Draft Rework — {section}", request)
    elif operation == "review_section":
        pack_errors = verify_narration_pack(product_dir, section)
        if pack_errors:
            raise ValueError("Review rework requires a valid narration pack: " + "; ".join(pack_errors))
        if not (root / "draft.md").is_file():
            raise FileNotFoundError(f"Review rework requires {section}/draft.md.")
    elif operation == "revise_section":
        pack_errors = verify_narration_pack(product_dir, section)
        if pack_errors:
            raise ValueError("Revision rework requires a valid narration pack: " + "; ".join(pack_errors))
        for name in ["draft.md", "review.md"]:
            if not (root / name).is_file():
                raise FileNotFoundError(f"Revision rework requires {section}/{name}.")
        _write_request(root / "change-request.md", f"Change Request — {section}", request)

    state["status"] = SECTION_OPERATION_REWORK_STATES[operation]
    clear_human_approval(state)
    write_json(state_path, state)

    product_path = product_dir / "product.json"
    product = read_json(product_path)
    stages = product.setdefault("stages", {})
    stages["sections"] = "in_progress"
    stages["integration"] = "not_started"
    stages["delivery"] = "not_started"
    write_json(product_path, product)
