#!/usr/bin/env python3
"""Human-facing semantic rework: reopen intent, supersede routing, and create a fresh canonical task."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.approval import start_new_cycle
    from scripts.common import load_registry, read_json
    from scripts.lifecycle import (
        RESEARCH_REWORK_OPERATIONS,
        cancel_active_task,
        prepare_research_rework,
        prepare_section_rework,
    )
    from scripts.task import create_task
except ModuleNotFoundError:  # Direct execution: python scripts/rework.py
    from approval import start_new_cycle
    from common import load_registry, read_json
    from lifecycle import RESEARCH_REWORK_OPERATIONS, cancel_active_task, prepare_research_rework, prepare_section_rework
    from task import create_task


SECTION_REWORK_OPERATIONS = {"design_section", "draft_section", "review_section", "revise_section"}


def _write_outline_rework_request(product_dir: Path, request: str) -> None:
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    if outline.get("status") == "approved":
        start_new_cycle(product_dir, request)
        return

    product = read_json(product_dir / "product.json")
    cycle_id = product.get("production_cycle", {}).get("id", "current-cycle")
    (product_dir / "02_outline" / "outline-change-request.md").write_text(
        f"# Outline Change Request — {cycle_id}\n\n"
        f"Requested by: user\n\nRequested at: {datetime.now(timezone.utc).isoformat()}\n\n"
        f"## Required architecture change\n\n{request.strip()}\n",
        encoding="utf-8",
    )


def _ensure_outline_invalidated_for_research(product_dir: Path, request: str) -> None:
    outline_path = product_dir / "02_outline" / "outline.json"
    if not outline_path.is_file():
        return
    outline = read_json(outline_path)
    if outline.get("status") == "approved":
        start_new_cycle(product_dir, "Research was reopened before the next outline. " + request.strip())


def _resolve_research_unit(product_dir: Path, unit: str | None) -> tuple[str, bool]:
    plan = read_json(product_dir / "01_research" / "plan.json")
    units = [str(item["id"]) for item in plan.get("workstreams", []) if item.get("id")]
    if not units:
        raise ValueError("Approved research plan has no workstreams.")
    if unit:
        if unit not in units:
            raise ValueError(f"Workstream {unit} is not declared in the approved research plan.")
        return unit, False
    return units[0], True


def _record_rework(
    product_dir: Path,
    *,
    operation: str,
    section: str | None,
    unit: str | None,
    request: str,
    writer_outcome: str | None,
    method_authority: str | None,
    superseded_task: str | None,
    new_task: str,
) -> None:
    record = {
        "schema_version": 2,
        "requested_by": "user",
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "target": {"section": section, "unit": unit},
        "request": request.strip(),
        "writer_outcome": writer_outcome.strip() if isinstance(writer_outcome, str) else None,
        "method_authority": method_authority,
        "superseded_task": superseded_task,
        "new_task": new_task,
    }
    with (product_dir / "rework-requests.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def rework(
    product_dir: Path,
    operation: str,
    *,
    section: str | None,
    unit: str | None,
    request: str,
    writer_outcome: str | None = None,
    lock_method: bool = False,
    execution_runtime: str | None = None,
) -> dict:
    product_dir = product_dir.resolve()
    registry = load_registry()
    if operation not in registry:
        raise ValueError(f"Unknown operation: {operation}")
    spec = registry[operation]
    if spec.get("compatibility_only"):
        raise ValueError(
            f"{operation} is compatibility-only and cannot be reopened through semantic rework. "
            "Route story/material architecture changes to outline, evidence gaps to research, or prose changes to draft_section."
        )
    if not request.strip():
        raise ValueError("Human rework request cannot be empty.")
    if operation == "draft_section" and (not isinstance(writer_outcome, str) or not writer_outcome.strip()):
        raise ValueError(
            "Draft rework requires writer_outcome: describe the observed failure and desired audience outcome "
            "without prescribing a repair method. Use lock_method only for an explicit one-task owner directive."
        )
    if lock_method and operation != "draft_section":
        raise ValueError("lock_method is available only for draft_section rework.")

    target_kind = spec["target_kind"]
    all_workstreams = False
    if operation == "research_workstream":
        unit, all_workstreams = _resolve_research_unit(product_dir, unit)
    elif target_kind == "section" and not section:
        raise ValueError(f"{operation} requires --section P##")
    elif target_kind == "unit" and not unit:
        raise ValueError(f"{operation} requires --unit")
    if target_kind == "product" and (section or unit):
        raise ValueError(f"{operation} targets the product; omit --section/--unit")

    superseded = cancel_active_task(product_dir, reason=f"human rework: {operation}: {request.strip()}")

    if operation in SECTION_REWORK_OPERATIONS:
        prepare_section_rework(
            product_dir,
            operation,
            str(section),
            request,
            writer_outcome=writer_outcome,
            lock_method=lock_method,
        )
    elif operation == "outline":
        _write_outline_rework_request(product_dir, request)
    elif operation in RESEARCH_REWORK_OPERATIONS:
        _ensure_outline_invalidated_for_research(product_dir, request)
        unit = prepare_research_rework(
            product_dir,
            operation,
            request,
            unit=unit,
            all_units=all_workstreams,
        )

    work = create_task(product_dir, operation, section, unit, False, execution_runtime)
    _record_rework(
        product_dir,
        operation=operation,
        section=section,
        unit=unit,
        request=request,
        writer_outcome=writer_outcome if operation == "draft_section" else None,
        method_authority=(
            "owner_locked_for_single_task" if lock_method else "writer_owned"
        ) if operation == "draft_section" else None,
        superseded_task=superseded,
        new_task=work["id"],
    )
    return work


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("operation", choices=sorted(load_registry()))
    parser.add_argument("--section")
    parser.add_argument(
        "--unit",
        help="Optional for research_workstream; omit it to rework the whole workstream layer from the first declared unit.",
    )
    parser.add_argument("--request", required=True)
    parser.add_argument(
        "--writer-outcome",
        help="Required for draft_section: observed failure and desired audience outcome, without a repair recipe.",
    )
    parser.add_argument(
        "--lock-method",
        action="store_true",
        help="For draft_section only: expose --request as an owner-locked method for this task.",
    )
    parser.add_argument("--runtime", choices=["legacy", "dsh"])
    args = parser.parse_args()
    try:
        work = rework(
            args.product,
            args.operation,
            section=args.section,
            unit=args.unit,
            request=args.request,
            writer_outcome=args.writer_outcome,
            lock_method=args.lock_method,
            execution_runtime=args.runtime,
        )
    except (ValueError, FileNotFoundError, FileExistsError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(work, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
