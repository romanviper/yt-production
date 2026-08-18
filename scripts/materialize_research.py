#!/usr/bin/env python3
"""Materialize independent research workstream workspaces from an approved plan."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from scripts.common import read_json, write_json
    from scripts.research_plan_contract import bullet_list, render_shared_protocol, validate_research_plan_contract
except ModuleNotFoundError:
    from common import read_json, write_json
    from research_plan_contract import bullet_list, render_shared_protocol, validate_research_plan_contract


def materialize(product_dir: Path) -> list[Path]:
    product_dir = product_dir.resolve()
    plan = read_json(product_dir / "01_research" / "plan.json")
    if plan.get("status") != "approved":
        raise ValueError("Research plan must be human-approved before materialization.")
    contract_errors = validate_research_plan_contract(plan)
    if contract_errors:
        raise ValueError("Invalid approved research plan: " + "; ".join(contract_errors))
    shared_protocol = render_shared_protocol(plan["shared_research_protocol"])
    created: list[Path] = []
    for unit in plan.get("workstreams", []):
        unit_id = unit.get("id", "")
        if not re.fullmatch(r"WS\d{2}", unit_id):
            raise ValueError(f"Invalid workstream ID: {unit_id}")
        root = product_dir / "01_research" / "workstreams" / unit_id
        root.mkdir(parents=True, exist_ok=True)
        brief = root / "brief.md"
        if not brief.exists():
            evidence = bullet_list(unit.get("required_evidence", []))
            criteria = bullet_list(unit.get("completion_criteria", []))
            handoff = bullet_list(unit.get("synthesis_handoff", []))
            brief.write_text(
                f"# {unit_id} — {unit['title']}\n\n"
                f"## Question\n\n{unit['question']}\n\n"
                f"## In scope\n\n{unit.get('in_scope', '')}\n\n"
                f"## Out of scope\n\n{unit.get('out_of_scope', '')}\n\n"
                f"## Ownership\n\n{unit.get('ownership', '')}\n\n"
                f"## Required evidence\n\n{evidence}\n\n"
                f"## Completion criteria\n\n{criteria}\n\n"
                f"## Required synthesis handoff\n\n{handoff}\n\n"
                f"{shared_protocol}\n",
                encoding="utf-8",
            )
            created.append(brief)
        for name, value in [
            ("sources.json", {"schema_version": 1, "workstream": unit_id, "status": "not_started", "sources": []}),
            ("claims.json", {"schema_version": 1, "workstream": unit_id, "status": "not_started", "claims": []}),
            ("materials.json", {"schema_version": 1, "workstream": unit_id, "status": "not_started", "materials": []}),
        ]:
            path = root / name
            if not path.exists():
                write_json(path, value)
                created.append(path)
        synthesis = root / "synthesis.md"
        if not synthesis.exists():
            synthesis.write_text(
                f"# Synthesis — {unit_id}\n\nStatus: not_started\n\n"
                "## Answer\n\nChưa research.\n\n"
                "## Mechanism and chronology\n\nChưa research.\n\n"
                "## Strongest evidence\n\nChưa research.\n\n"
                "## Story material candidates\n\nChưa research. Khi có candidate, gọi bằng ID từ materials.json.\n\n"
                "## Contradictions and unknowns\n\nChưa research.\n\n"
                "## Handoff to global synthesis\n\nChưa research.\n",
                encoding="utf-8",
            )
            created.append(synthesis)
    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    args = parser.parse_args()
    try:
        created = materialize(args.product)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Materialized {len(created)} research artifact(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
