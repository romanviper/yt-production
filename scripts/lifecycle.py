#!/usr/bin/env python3
"""Canonical lifecycle rules for task routing, section operations, and human rework."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    from scripts.common import read_json, write_json
    from scripts.story_plan_contract import is_direct_authorship_outline, verify_narration_pack
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import read_json, write_json
    from story_plan_contract import is_direct_authorship_outline, verify_narration_pack


TASK_LIVE_STATES = {"ready", "in_progress"}
TASK_TERMINAL_STATES = {"closed", "cancelled"}
TASK_SUBMITTED_STATES = {"ready_for_review"}
TASK_STATES = TASK_LIVE_STATES | TASK_SUBMITTED_STATES | TASK_TERMINAL_STATES

SECTION_OPERATION_ENTRY_STATES = {
    "design_section": {"needs_story_plan", "story_plan_changes_requested"},
    "draft_section": {"ready_for_draft"},
    "evidence_resolution": {"needs_evidence_resolution", "ready_for_draft"},
    "review_section": {"ready_for_review"},
    "revise_section": {"changes_requested"},
}

SECTION_OPERATION_SUBMISSION_STATES = {
    "design_section": "story_plan_review",
    "draft_section": "ready_for_review",
    "evidence_resolution": "ready_for_draft",
    "review_section": "review_complete",
    "revise_section": "ready_for_review",
}

SECTION_OPERATION_REWORK_STATES = {
    "design_section": "story_plan_changes_requested",
    "draft_section": "ready_for_draft",
    "evidence_resolution": "needs_evidence_resolution",
    "review_section": "ready_for_review",
    "revise_section": "changes_requested",
}

SECTION_OPERATIONS = set(SECTION_OPERATION_ENTRY_STATES)
RESEARCH_REWORK_OPERATIONS = {"research_plan", "research_workstream", "research_synthesis"}
RESEARCH_REWORK_STATE_PATH = Path("01_research/rework-state.json")
RESEARCH_REWORK_REQUEST_PATH = Path("01_research/rework-request.md")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def task_scope_key(operation: str, target: dict[str, Any] | None) -> tuple[str, str | None]:
    target = target or {}
    section = target.get("section")
    if section:
        return ("section", str(section))
    unit = target.get("unit")
    if unit:
        return ("unit", str(unit))
    return ("product", None)


def scopes_conflict(left: tuple[str, str | None], right: tuple[str, str | None]) -> bool:
    if left[0] == "product" or right[0] == "product":
        return True
    return left == right


def _work_orders(product_dir: Path) -> Iterable[tuple[Path, dict[str, Any]]]:
    tasks_dir = product_dir.resolve() / "tasks"
    if not tasks_dir.is_dir():
        return []
    items: list[tuple[Path, dict[str, Any]]] = []
    for work_path in sorted(tasks_dir.glob("T*/work-order.json")):
        try:
            work = read_json(work_path)
        except (json.JSONDecodeError, ValueError, OSError):
            continue
        items.append((work_path, work))
    return items


def live_task_lifecycle_compatible(product_dir: Path, work: dict[str, Any]) -> bool:
    if work.get("state") not in TASK_LIVE_STATES:
        return False
    operation = str(work.get("operation") or "")
    if operation not in SECTION_OPERATIONS:
        return True
    section = work.get("target", {}).get("section")
    if not section:
        return False
    state_path = product_dir.resolve() / "03_sections" / str(section) / "section.json"
    if not state_path.is_file():
        return False
    try:
        state = read_json(state_path)
    except (json.JSONDecodeError, ValueError, OSError):
        return False
    return section_operation_state_error(operation, state.get("status"), str(section)) is None


def _terminalize_work_order(
    work_path: Path,
    work: dict[str, Any],
    *,
    state: str,
    reason: str,
    superseded_by: str | None = None,
) -> None:
    if state not in TASK_TERMINAL_STATES:
        raise ValueError(f"Task settlement requires a terminal state; got {state!r}.")
    if work.get("state") in TASK_TERMINAL_STATES:
        return
    now = _now()
    work["state"] = state
    work["updated_at"] = now
    if state == "closed":
        work["closed_at"] = now
        work["close_reason"] = reason
    else:
        work["cancel_reason"] = reason
    if superseded_by:
        work["superseded_by"] = superseded_by
    write_json(work_path, work)


def live_task_conflicts(product_dir: Path, operation: str, section: str | None, unit: str | None) -> list[str]:
    product_dir = product_dir.resolve()
    desired = task_scope_key(operation, {"section": section, "unit": unit})
    conflicts: list[str] = []
    for work_path, work in _work_orders(product_dir):
        if work.get("state") not in TASK_LIVE_STATES:
            continue
        if not live_task_lifecycle_compatible(product_dir, work):
            _terminalize_work_order(
                work_path,
                work,
                state="cancelled",
                reason="routing self-heal: task no longer matches authoritative section lifecycle",
            )
            continue
        if scopes_conflict(desired, task_scope_key(str(work.get("operation") or ""), work.get("target"))):
            conflicts.append(str(work.get("id") or work_path.parent.name))
    return conflicts


def cancel_live_task_conflicts(
    product_dir: Path,
    operation: str,
    section: str | None,
    unit: str | None,
    *,
    reason: str,
    replacement: str | None = None,
) -> list[str]:
    product_dir = product_dir.resolve()
    desired = task_scope_key(operation, {"section": section, "unit": unit})
    cancelled: list[str] = []
    for work_path, work in _work_orders(product_dir):
        if work.get("state") not in TASK_LIVE_STATES:
            continue
        if not live_task_lifecycle_compatible(product_dir, work):
            _terminalize_work_order(
                work_path,
                work,
                state="cancelled",
                reason="routing self-heal: task no longer matches authoritative section lifecycle",
            )
            continue
        if not scopes_conflict(desired, task_scope_key(str(work.get("operation") or ""), work.get("target"))):
            continue
        task_id = str(work.get("id") or work_path.parent.name)
        _terminalize_work_order(work_path, work, state="cancelled", reason=reason, superseded_by=replacement)
        cancelled.append(task_id)
        clear_active_pointer(product_dir, task_id, reason=reason)
    return cancelled


def _write_idle_pointer(product_dir: Path, reason: str | None = None, **metadata: Any) -> None:
    path = product_dir.resolve() / "tasks" / "ACTIVE.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    idle: dict[str, Any] = {"task_id": None, "status": "idle", "updated_at": _now()}
    if reason:
        idle["reason"] = reason
    idle.update({key: value for key, value in metadata.items() if value is not None})
    write_json(path, idle)


def clear_active_pointer(product_dir: Path, task_id: str | None = None, *, reason: str | None = None) -> None:
    product_dir = product_dir.resolve()
    path = product_dir / "tasks" / "ACTIVE.json"
    if not path.is_file():
        return
    try:
        active = read_json(path)
    except (json.JSONDecodeError, ValueError, OSError):
        _write_idle_pointer(product_dir, reason or "routing metadata reset")
        return
    if task_id is not None and active.get("task_id") != task_id:
        return
    _write_idle_pointer(product_dir, reason)


def heal_active_pointer(product_dir: Path) -> str | None:
    product_dir = product_dir.resolve()
    path = product_dir / "tasks" / "ACTIVE.json"
    if not path.is_file():
        return None
    try:
        active = read_json(path)
    except (json.JSONDecodeError, ValueError, OSError):
        _write_idle_pointer(product_dir, "routing self-heal: invalid ACTIVE metadata")
        return None
    task_id = active.get("task_id")
    if not task_id:
        return None
    task_id = str(task_id)
    work_path = product_dir / "tasks" / task_id / "work-order.json"
    if not work_path.is_file():
        _write_idle_pointer(product_dir, "routing self-heal: referenced task is missing")
        return None
    try:
        work = read_json(work_path)
    except (json.JSONDecodeError, ValueError, OSError):
        _write_idle_pointer(product_dir, "routing self-heal: referenced work order is unreadable")
        return None
    if work.get("state") not in TASK_LIVE_STATES:
        _write_idle_pointer(product_dir, f"routing self-heal: task {task_id} is {work.get('state')}")
        return None
    if not live_task_lifecycle_compatible(product_dir, work):
        _terminalize_work_order(
            work_path,
            work,
            state="cancelled",
            reason="routing self-heal: task no longer matches authoritative section lifecycle",
        )
        _write_idle_pointer(product_dir, f"routing self-heal: task {task_id} lifecycle advanced")
        return None
    return task_id


def settle_related_tasks(
    product_dir: Path,
    *,
    section: str | None = None,
    unit: str | None = None,
    operations: set[str] | None = None,
    final_state: str,
    reason: str,
    superseded_by: str | None = None,
) -> list[str]:
    product_dir = product_dir.resolve()
    settled: list[str] = []
    for work_path, work in _work_orders(product_dir):
        if work.get("state") in TASK_TERMINAL_STATES:
            continue
        if operations is not None and work.get("operation") not in operations:
            continue
        target = work.get("target", {})
        if section is not None and target.get("section") != section:
            continue
        if unit is not None and target.get("unit") != unit:
            continue
        task_id = str(work.get("id") or work_path.parent.name)
        _terminalize_work_order(
            work_path,
            work,
            state=final_state,
            reason=reason,
            superseded_by=superseded_by,
        )
        settled.append(task_id)
        clear_active_pointer(product_dir, task_id, reason=reason)
    return settled


def sync_section_progress(product_dir: Path) -> str | None:
    product_dir = product_dir.resolve()
    outline_path = product_dir / "02_outline" / "outline.json"
    product_path = product_dir / "product.json"
    if not outline_path.is_file() or not product_path.is_file():
        return None
    outline = read_json(outline_path)
    section_ids = [str(item["id"]) for item in outline.get("sections", []) if isinstance(item, dict) and item.get("id")]
    if not section_ids:
        return None
    states: list[dict[str, Any]] = []
    for section_id in section_ids:
        state_path = product_dir / "03_sections" / section_id / "section.json"
        if state_path.is_file():
            states.append(read_json(state_path))
    if not states:
        summary = "not_started"
    elif len(states) == len(section_ids) and all(
        state.get("status") == "approved" and state.get("human_approved") is True for state in states
    ):
        summary = "approved"
    elif len(states) == len(section_ids) and all(state.get("status") == "ready_for_draft" for state in states):
        summary = "ready_for_draft"
    else:
        summary = "in_progress"
    product = read_json(product_path)
    product.setdefault("stages", {})["sections"] = summary
    write_json(product_path, product)
    return summary


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


def _write_research_request(product_dir: Path, *, operation: str, request: str, unit: str | None, all_units: bool) -> None:
    scope = "all declared workstreams" if operation == "research_workstream" and all_units else (unit or operation)
    path = product_dir / RESEARCH_REWORK_REQUEST_PATH
    path.write_text(
        "# Research Rework Request\n\n"
        "Requested by: user\n\n"
        f"Requested at: {_now()}\n\n"
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
    if operation not in RESEARCH_REWORK_OPERATIONS:
        raise ValueError(f"Operation {operation} is not a research rework operation.")
    if not request.strip():
        raise ValueError("Human rework request cannot be empty.")

    product_dir = product_dir.resolve()
    product_path = product_dir / "product.json"
    product = read_json(product_path)
    stages = product.setdefault("stages", {})
    now = _now()
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

    _write_research_request(product_dir, operation=operation, request=request, unit=selected_unit, all_units=all_units)
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
    sync_section_progress(product_dir)


def cancel_active_task(product_dir: Path, *, reason: str, replacement: str | None = None) -> str | None:
    product_dir = product_dir.resolve()
    heal_active_pointer(product_dir)
    path = product_dir / "tasks" / "ACTIVE.json"
    if not path.is_file():
        return None
    try:
        active = read_json(path)
    except (json.JSONDecodeError, ValueError, OSError):
        _write_idle_pointer(product_dir, reason)
        return None
    task_id = active.get("task_id")
    if not task_id:
        clear_active_pointer(product_dir, reason=reason)
        return None

    work_path = product_dir / "tasks" / str(task_id) / "work-order.json"
    if work_path.is_file():
        work = read_json(work_path)
        if work.get("state") not in TASK_TERMINAL_STATES:
            _terminalize_work_order(work_path, work, state="cancelled", reason=reason, superseded_by=replacement)
    clear_active_pointer(product_dir, str(task_id), reason=reason)
    return str(task_id)


def _write_request(path: Path, title: str, request: str) -> None:
    path.write_text(
        f"# {title}\n\n"
        f"Requested by: user\n\n"
        f"Requested at: {_now()}\n\n"
        f"## Request\n\n{request.strip()}\n",
        encoding="utf-8",
    )


def _write_draft_rework_request(
    path: Path,
    section: str,
    writer_outcome: str,
    *,
    locked_method: str | None = None,
) -> None:
    method_authority = "owner_locked_for_single_task" if locked_method is not None else "writer_owned"
    blocks = [
        f"# Draft Rework — {section}",
        "",
        "Requested by: user",
        "",
        f"Requested at: {_now()}",
        "",
        "## Observed failure and desired outcome",
        "",
        writer_outcome.strip(),
        "",
        "## Method authority",
        "",
        method_authority,
        "",
    ]
    if locked_method is None:
        blocks.extend(
            [
                "The writer owns the repair method. Examples and hypotheses from evaluation or conversation are not instructions and are intentionally absent from this packet.",
                "",
            ]
        )
    else:
        blocks.extend(
            [
                "## Owner-locked method for this task only",
                "",
                locked_method.strip(),
                "",
                "This lock expires with this task and must not be promoted into the reusable writer harness.",
                "",
            ]
        )
    path.write_text("\n".join(blocks), encoding="utf-8")


def prepare_section_rework(
    product_dir: Path,
    operation: str,
    section: str,
    request: str,
    *,
    writer_outcome: str | None = None,
    lock_method: bool = False,
) -> None:
    if operation not in SECTION_OPERATION_REWORK_STATES:
        raise ValueError(f"Operation {operation} is not a section rework operation.")
    if not request.strip():
        raise ValueError("Human rework request cannot be empty.")

    product_dir = product_dir.resolve()
    outline = read_json(product_dir / "02_outline" / "outline.json")
    if outline.get("status") != "approved":
        raise ValueError("Section rework requires a human-approved outline.")
    direct_authorship = is_direct_authorship_outline(outline)

    root = product_dir / "03_sections" / section
    state_path = root / "section.json"
    state = read_json(state_path)

    if operation == "design_section":
        if direct_authorship:
            raise ValueError("Current direct-authoring sections have no story-plan layer; route architecture changes to outline.")
        plan_path = root / "story-plan.json"
        plan = read_json(plan_path)
        plan["status"] = "draft"
        plan.pop("approved_by", None)
        plan.pop("approved_at", None)
        write_json(plan_path, plan)
        _write_request(root / "story-plan-change-request.md", f"Story Plan Rework — {section}", request)
    elif operation == "draft_section":
        if not direct_authorship:
            plan = read_json(root / "story-plan.json")
            if plan.get("status") != "approved":
                raise ValueError("Legacy draft rework requires an approved story plan.")
        pack_errors = verify_narration_pack(product_dir, section)
        if pack_errors:
            raise ValueError("Draft rework requires a valid narration pack: " + "; ".join(pack_errors))
        outcome = writer_outcome.strip() if isinstance(writer_outcome, str) and writer_outcome.strip() else request.strip()
        _write_draft_rework_request(
            root / "draft-rework-request.md",
            section,
            outcome,
            locked_method=request if lock_method else None,
        )
    elif operation == "review_section":
        pack_errors = verify_narration_pack(product_dir, section)
        if pack_errors:
            raise ValueError("Review rework requires a valid narration pack: " + "; ".join(pack_errors))
        if not (root / "draft.md").is_file():
            raise FileNotFoundError(f"Review rework requires {section}/draft.md.")
    elif operation == "evidence_resolution":
        _write_request(
            root / "evidence-resolution-request.md",
            f"Evidence Resolution Rework — {section}",
            request,
        )
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
