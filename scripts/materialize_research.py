#!/usr/bin/env python3
"""Materialize independent research workstream workspaces from an approved plan."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from scripts.common import read_json, write_json
except ModuleNotFoundError:
    from common import read_json, write_json


def materialize(product_dir: Path) -> list[Path]:
    product_dir = product_dir.resolve()
    plan = read_json(product_dir / "01_research" / "plan.json")
    if plan.get("status") != "approved":
        raise ValueError("Research plan must be human-approved before materialization.")
    created: list[Path] = []
    for unit in plan.get("workstreams", []):
        unit_id = unit.get("id", "")
        if not re.fullmatch(r"WS\d{2}", unit_id):
            raise ValueError(f"Invalid workstream ID: {unit_id}")
        root = product_dir / "01_research" / "workstreams" / unit_id
        root.mkdir(parents=True, exist_ok=True)
        brief = root / "brief.md"
        if not brief.exists():
            evidence = "\n".join(f"- {item}" for item in unit.get("required_evidence", [])) or "- Chưa xác định."
            criteria = "\n".join(f"- {item}" for item in unit.get("completion_criteria", [])) or "- Chưa xác định."
            brief.write_text(
                f"# {unit_id} — {unit['title']}\n\n"
                f"## Question\n\n{unit['question']}\n\n"
                f"## In scope\n\n{unit.get('in_scope', '')}\n\n"
                f"## Out of scope\n\n{unit.get('out_of_scope', '')}\n\n"
                f"## Required evidence\n\n{evidence}\n\n"
                f"## Completion criteria\n\n{criteria}\n",
                encoding="utf-8",
            )
            created.append(brief)
        for name, value in [
            ("sources.json", {"schema_version": 1, "workstream": unit_id, "status": "not_started", "sources": []}),
            ("claims.json", {"schema_version": 1, "workstream": unit_id, "status": "not_started", "claims": []}),
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
