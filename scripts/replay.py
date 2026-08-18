#!/usr/bin/env python3
"""Replay a bounded production path without exposing lifecycle bookkeeping to the operator."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, write_json
    from scripts.materialize_sections import archive_previous_cycle, materialize
    from scripts.rework import rework
    from scripts.task import create_task
except ModuleNotFoundError:  # Direct execution: python scripts/replay.py
    from common import read_json, write_json
    from materialize_sections import archive_previous_cycle, materialize
    from rework import rework
    from task import create_task


REPLAY_STEPS = ("outline", "design_section", "draft_section")
STATE_PATH = "replay-state.json"
LOG_PATH = "replay-requests.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _state_path(product_dir: Path) -> Path:
    return product_dir.resolve() / STATE_PATH


def _log(product_dir: Path, record: dict[str, Any]) -> None:
    with (product_dir.resolve() / LOG_PATH).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _step_range(start: str, through: str) -> list[str]:
    if start not in REPLAY_STEPS or through not in REPLAY_STEPS:
        raise ValueError("Replay supports outline, design_section and draft_section.")
    start_index = REPLAY_STEPS.index(start)
    end_index = REPLAY_STEPS.index(through)
    if end_index < start_index:
        raise ValueError("--through must be at or downstream of --from.")
    return list(REPLAY_STEPS[start_index : end_index + 1])


def _require_section(steps: list[str], section: str | None) -> None:
    if any(step != "outline" for step in steps) and not section:
        raise ValueError("Replay through section work requires --section P##.")


def _work_state(product_dir: Path, task_id: str) -> str | None:
    path = product_dir / "tasks" / task_id / "work-order.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing replay task work order: {task_id}")
    return read_json(path).get("state")


def _write_state(product_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    state["updated_at"] = _now()
    write_json(_state_path(product_dir), state)
    return state


def _record_event(state: dict[str, Any], event: str, **details: Any) -> None:
    state.setdefault("history", []).append({"at": _now(), "event": event, **details})


def _route_step(
    product_dir: Path,
    step: str,
    *,
    section: str | None,
    request: str,
    first: bool,
    execution_runtime: str | None,
) -> dict[str, Any]:
    if first:
        return rework(
            product_dir,
            step,
            section=section if step != "outline" else None,
            unit=None,
            request=request,
            execution_runtime=execution_runtime if step == "outline" else None,
        )
    return create_task(
        product_dir,
        step,
        section if step != "outline" else None,
        None,
        False,
        execution_runtime if step == "outline" else None,
    )


def start_replay(
    product_dir: Path,
    *,
    start: str,
    through: str,
    section: str | None,
    request: str,
    execution_runtime: str | None = None,
) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    if not request.strip():
        raise ValueError("Replay request cannot be empty.")
    steps = _step_range(start, through)
    _require_section(steps, section)
    if start == "outline":
        outline = read_json(product_dir / "02_outline" / "outline.json")
        if outline.get("status") != "approved":
            raise ValueError(
                "Replay from outline requires an approved baseline; finish the current outline or use rework.py."
            )

    existing_path = _state_path(product_dir)
    if existing_path.is_file():
        existing = read_json(existing_path)
        if existing.get("status") == "active":
            raise ValueError(
                f"Replay {existing.get('id', '?')} is already active; finish or cancel it before starting another."
            )

    replay_id = "RP-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    work = _route_step(
        product_dir,
        steps[0],
        section=section,
        request=request,
        first=True,
        execution_runtime=execution_runtime,
    )
    state: dict[str, Any] = {
        "schema_version": 1,
        "id": replay_id,
        "status": "active",
        "requested_by": "user",
        "created_at": _now(),
        "updated_at": _now(),
        "request": request.strip(),
        "section": section,
        "steps": steps,
        "current_index": 0,
        "current_step": steps[0],
        "current_task": work["id"],
        "execution_runtime": execution_runtime,
        "history": [],
    }
    _record_event(state, "started", step=steps[0], task_id=work["id"])
    _write_state(product_dir, state)
    _log(
        product_dir,
        {
            "schema_version": 1,
            "id": replay_id,
            "requested_by": "user",
            "requested_at": state["created_at"],
            "request": state["request"],
            "section": section,
            "steps": steps,
            "initial_task": work["id"],
        },
    )
    return state


def _archive_if_needed(product_dir: Path) -> list[str]:
    product = read_json(product_dir / "product.json")
    current_cycle = product.get("production_cycle", {}).get("id")
    section_root = product_dir / "03_sections"
    if not section_root.is_dir():
        return []
    stale = []
    for path in sorted(section_root.glob("P??/section.json")):
        section = read_json(path)
        if current_cycle and section.get("cycle_id") != current_cycle:
            stale.append(path)
    if not stale:
        return []
    return [str(path.relative_to(product_dir)) for path in archive_previous_cycle(product_dir)]


def _outline_ready(product_dir: Path) -> bool:
    return read_json(product_dir / "02_outline" / "outline.json").get("status") == "approved"


def _design_ready(product_dir: Path, section: str) -> bool:
    root = product_dir / "03_sections" / section
    plan = read_json(root / "story-plan.json")
    state = read_json(root / "section.json")
    return plan.get("status") == "approved" and state.get("status") == "ready_for_draft"


def continue_replay(product_dir: Path) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    path = _state_path(product_dir)
    if not path.is_file():
        raise FileNotFoundError("No replay state exists for this product.")
    state = read_json(path)
    if state.get("status") != "active":
        return state

    current_step = str(state["current_step"])
    current_task = str(state["current_task"])
    task_state = _work_state(product_dir, current_task)
    if task_state in {"ready", "in_progress"}:
        state["blocked_on"] = "task_completion"
        return _write_state(product_dir, state)

    section = state.get("section")
    if current_step == "outline" and not _outline_ready(product_dir):
        state["blocked_on"] = "outline_approval"
        return _write_state(product_dir, state)
    if current_step == "design_section":
        if not section:
            raise ValueError("Replay design step is missing section.")
        if not _design_ready(product_dir, str(section)):
            state["blocked_on"] = "story_plan_approval"
            return _write_state(product_dir, state)

    next_index = int(state["current_index"]) + 1
    steps = list(state["steps"])
    if next_index >= len(steps):
        state["status"] = "completed"
        state["blocked_on"] = None
        state["completed_at"] = _now()
        _record_event(state, "completed", step=current_step, task_id=current_task)
        return _write_state(product_dir, state)

    next_step = steps[next_index]
    if current_step == "outline":
        archived = _archive_if_needed(product_dir)
        created = [str(path.relative_to(product_dir)) for path in materialize(product_dir)]
        _record_event(state, "sections_materialized", archived=archived, created=created)

    work = _route_step(
        product_dir,
        next_step,
        section=str(section) if section else None,
        request=str(state["request"]),
        first=False,
        execution_runtime=state.get("execution_runtime"),
    )
    state["current_index"] = next_index
    state["current_step"] = next_step
    state["current_task"] = work["id"]
    state["blocked_on"] = None
    _record_event(state, "advanced", step=next_step, task_id=work["id"])
    return _write_state(product_dir, state)


def cancel_replay(product_dir: Path, reason: str) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    path = _state_path(product_dir)
    if not path.is_file():
        raise FileNotFoundError("No replay state exists for this product.")
    state = read_json(path)
    if state.get("status") == "active":
        state["status"] = "cancelled"
        state["cancelled_at"] = _now()
        state["cancel_reason"] = reason.strip() or "cancelled by user"
        _record_event(state, "cancelled", reason=state["cancel_reason"])
        _write_state(product_dir, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start")
    start.add_argument("product", type=Path)
    start.add_argument("--from", dest="start", choices=REPLAY_STEPS, required=True)
    start.add_argument("--through", choices=REPLAY_STEPS, required=True)
    start.add_argument("--section")
    start.add_argument("--request", required=True)
    start.add_argument("--runtime", choices=["legacy", "dsh"])

    cont = sub.add_parser("continue")
    cont.add_argument("product", type=Path)

    status = sub.add_parser("status")
    status.add_argument("product", type=Path)

    cancel = sub.add_parser("cancel")
    cancel.add_argument("product", type=Path)
    cancel.add_argument("--reason", default="cancelled by user")

    args = parser.parse_args()
    try:
        if args.command == "start":
            result = start_replay(
                args.product,
                start=args.start,
                through=args.through,
                section=args.section,
                request=args.request,
                execution_runtime=args.runtime,
            )
        elif args.command == "continue":
            result = continue_replay(args.product)
        elif args.command == "cancel":
            result = cancel_replay(args.product, args.reason)
        else:
            result = read_json(_state_path(args.product))
    except (ValueError, FileNotFoundError, FileExistsError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
