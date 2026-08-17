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
    from scripts.lifecycle import cancel_active_task, prepare_section_rework
    from scripts.task import create_task
except ModuleNotFoundError:  # Direct execution: python scripts/rework.py
    from approval import start_new_cycle
    from common import load_registry, read_json
    from lifecycle import cancel_active_task, prepare_section_rework
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


def _record_rework(
    product_dir: Path,
    *,
    operation: str,
    section: str | None,
    unit: str | None,
    request: str,
    superseded_task: str | None,
    new_task: str,
) -> None:
    record = {
        "schema_version": 1,
        "requested_by": "user",
        "requested_at": datetime.now(timezone.utc).isoformat(),
        "operation": operation,
        "target": {"section": section, "unit": unit},
        "request": request.strip(),
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
    execution_runtime: str | None = None,
) -> dict:
    product_dir = product_dir.resolve()
    registry = load_registry()
    if operation not in registry:
        raise ValueError(f"Unknown operation: {operation}")
    if not request.strip():
        raise ValueError("Human rework request cannot be empty.")

    target_kind = registry[operation]["target_kind"]
    if target_kind == "section" and not section:
        raise ValueError(f"{operation} requires --section P##")
    if target_kind == "unit" and not unit:
        raise ValueError(f"{operation} requires --unit WS##")
    if target_kind == "product" and (section or unit):
        raise ValueError(f"{operation} targets the product; omit --section/--unit")

    superseded = cancel_active_task(product_dir, reason=f"human rework: {operation}: {request.strip()}")

    if operation in SECTION_REWORK_OPERATIONS:
        prepare_section_rework(product_dir, operation, str(section), request)
    elif operation == "outline":
        _write_outline_rework_request(product_dir, request)

    work = create_task(product_dir, operation, section, unit, False, execution_runtime)
    _record_rework(
        product_dir,
        operation=operation,
        section=section,
        unit=unit,
        request=request,
        superseded_task=superseded,
        new_task=work["id"],
    )
    return work


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("operation", choices=sorted(load_registry()))
    parser.add_argument("--section")
    parser.add_argument("--unit")
    parser.add_argument("--request", required=True)
    parser.add_argument("--runtime", choices=["legacy", "dsh"])
    args = parser.parse_args()
    try:
        work = rework(
            args.product,
            args.operation,
            section=args.section,
            unit=args.unit,
            request=args.request,
            execution_runtime=args.runtime,
        )
    except (ValueError, FileNotFoundError, FileExistsError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(work, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
