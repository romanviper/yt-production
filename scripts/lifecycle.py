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

RESEARCH_REWORK_OPERATIONS = {"research_plan", "research_workstream", "research_synthesis"}
RESEARCH_REWORK_STATE_PATH = Path("01_research/rework-state.json")
RESEARCH_REWORK_REQUEST_PATH = Path("01_research/rework-request.md")


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


def _research_units(product_dir: Path) -> list[str]:
    plan = read_json(product_dir / "01_research" / "plan.json")
    return [str(item["id"]) for item in plan.get("workstreams", []) if item.get("id")]


def _mark_json_status(path: Path, status: str) -> None:
    if not path.is_file():
        return
    document = read_json(path)
    document["status"] = status
    write_json(path, document)


def _mark_markdown_status(path: Path, status: str) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith("Status:"):
            lines[index] = f"Status: {status}"
            replaced = True
            break
    if not replaced:
        lines.insert(0, f"Status: {status}")
        lines.insert(1, "")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _mark_workstream_rework_pending(product_dir: Path, unit: str) -> None:
    root = product_dir / "01_research" / "workstreams" / unit
    _mark_json_status(root / "sources.json", "rework_pending")
    _mark_json_status(root / "claims.json", "rework_pending")
    _mark_json_status(root / "materials.json", "rework_pending")
    _mark_markdown_status(root / "synthesis.md", "rework_pending")


def _mark_global_synthesis_rework_pending(product_dir: Path) -> None:
    _mark_markdown_status(product_dir / "01_research" / "research-synthesis.md", "rework_pending")
    map_path = product_dir / "01_research" / "story-material-map.json"
    if map_path.is_file():
        _mark_json_status(map_path, "rework_pending")


def _write_research_request(
    product_dir: Path,
    *,
    operation: str,
    request: str,
    unit: str | None,
    all_units: bool,
) -> None:
    scope = "all declared workstreams" if operation == "research_workstream" and all_units else (unit or operation)
    path = product_dir / RESEARCH_REWORK_REQUEST_PATH
    path.write_text(
        "# Research Rework Request\n\n"
        "Requested by: user\n\n"
        f"Requested at: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"Start operation: `{operation}`\n\n"
        f"Scope: `{scope}`\n\n"
        "## Request\n\n"
        f"{request.strip()}\n",
        encoding="utf-8",
    )


def prepare_research_rework(
    product_dir: Path,
    operation: str,
    request: str,
    *,
    unit: str | None = None,
    all_units: bool = False,
) -> str | None:
    """Reopen research at one semantic layer and invalidate every downstream stage.

    For a stage-level research_workstream request, all declared workstreams become
    pending and the first unit is returned for routing. Existing evidence content
    remains available as a baseline, while status markers prevent stale downstream
    synthesis or outline tasks from being treated as current.
    """

    if operation not in RESEARCH_REWORK_OPERATIONS:
        raise ValueError(f"Operation {operation} is not a research rework operation.")
    if not request.strip():
        raise ValueError("Human rework request cannot be empty.")

    product_dir = product_dir.resolve()
    product_path = product_dir / "product.json"
    product = read_json(product_path)
    stages = product.setdefault("stages", {})
    now = datetime.now(timezone.utc).isoformat()
    selected_unit = unit
    units: list[str] = []
    pending_units: list[str] = []

    if operation == "research_plan":
        if stages.get("direction") != "approved":
            raise ValueError("Research-plan rework requires approved product direction.")
        plan_path = product_dir / "01_research" / "plan.json"
        plan = read_json(plan_path)
        plan["status"] = "draft"
        plan.pop("approved_by", None)
        plan.pop("approved_at", None)
        write_json(plan_path, plan)
        stages["research_plan"] = "changes_requested"
        stages["research"] = "not_started"
        _mark_global_synthesis_rework_pending(product_dir)
    else:
        plan = read_json(product_dir / "01_research" / "plan.json")
        if plan.get("status") != "approved":
            raise ValueError("Research rework requires a human-approved research plan.")
        units = _research_units(product_dir)
        if operation == "research_workstream":
            if not units:
                raise ValueError("Approved research plan has no workstreams.")
            if all_units:
                pending_units = list(units)
                selected_unit = selected_unit or units[0]
            else:
                if not selected_unit:
                    raise ValueError("Specific workstream rework requires a unit.")
                if selected_unit not in units:
                    raise ValueError(f"Workstream {selected_unit} is not declared in the approved research plan.")
                pending_units = [selected_unit]
            if selected_unit not in units:
                raise ValueError(f"Workstream {selected_unit} is not declared in the approved research plan.")
            for pending_unit in pending_units:
                _mark_workstream_rework_pending(product_dir, pending_unit)
            _mark_global_synthesis_rework_pending(product_dir)
        elif operation == "research_synthesis":
            _mark_global_synthesis_rework_pending(product_dir)
        stages["research"] = "in_progress"

    stages["outline"] = "changes_requested"
    stages["sections"] = "paused"
    stages["integration"] = "not_started"
    stages["delivery"] = "not_started"
    product["status"] = "research_rework"
    cycle = product.setdefault("production_cycle", {})
    cycle["status"] = "research_rework"
    cycle["reason"] = request.strip()
    write_json(product_path, product)

    _write_research_request(
        product_dir,
        operation=operation,
        request=request,
        unit=selected_unit,
        all_units=all_units,
    )
    write_json(
        product_dir / RESEARCH_REWORK_STATE_PATH,
        {
            "schema_version": 1,
            "status": "in_progress",
            "requested_operation": operation,
            "requested_at": now,
            "scope": "all_workstreams" if operation == "research_workstream" and all_units else "single_target",
            "selected_unit": selected_unit,
            "declared_units": units,
            "pending_units": pending_units,
            "completed_units": [],
            "request": request.strip(),
        },
    )
    return selected_unit


def research_rework_blocker(product_dir: Path) -> str | None:
    """Return why downstream outline/synthesis must wait, if semantic research rework is active."""

    path = product_dir / RESEARCH_REWORK_STATE_PATH
    if not path.is_file():
        return None
    state = read_json(path)
    operation = state.get("requested_operation")
    pending = state.get("pending_units", [])
    if operation == "research_workstream" and pending:
        return "research workstream rework still has pending units: " + ", ".join(str(item) for item in pending)
    if state.get("status") == "in_progress" and operation != "research_synthesis":
        return f"research rework is still active from {operation}"
    return None


def apply_research_submission(product_dir: Path, operation: str, unit: str | None) -> None:
    """Advance control-plane research rework state after a validated task submission."""

    if operation not in RESEARCH_REWORK_OPERATIONS:
        return
    product_dir = product_dir.resolve()
    state_path = product_dir / RESEARCH_REWORK_STATE_PATH
    state = read_json(state_path) if state_path.is_file() else None
    product_path = product_dir / "product.json"
    product = read_json(product_path)
    stages = product.setdefault("stages", {})

    if operation == "research_plan":
        stages["research_plan"] = "ready_for_review"
    elif operation == "research_workstream":
        stages["research"] = "in_progress"
        if state and state.get("requested_operation") == "research_workstream" and unit:
            pending = [item for item in state.get("pending_units", []) if item != unit]
            completed = list(state.get("completed_units", []))
            if unit not in completed:
                completed.append(unit)
            state["pending_units"] = pending
            state["completed_units"] = completed
            state["status"] = "workstreams_complete" if not pending else "in_progress"
            write_json(state_path, state)
    elif operation == "research_synthesis":
        stages["research"] = "complete"
        if state_path.is_file():
            state_path.unlink()
        (product_dir / RESEARCH_REWORK_REQUEST_PATH).unlink(missing_ok=True)

    write_json(product_path, product)


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
