#!/usr/bin/env python3
"""Find the smallest section review set affected by a claim or section change."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path

try:
    from scripts.common import read_json
except ModuleNotFoundError:
    from common import read_json


def calculate_impact(product_dir: Path, claim_id: str | None, section_id: str | None) -> dict:
    product_dir = product_dir.resolve()
    outline = read_json(product_dir / "02_outline" / "outline.json")
    sections = {item["id"]: item for item in outline.get("sections", [])}
    downstream: dict[str, set[str]] = defaultdict(set)
    for item in sections.values():
        for dependency in item.get("dependencies", []):
            downstream[dependency].add(item["id"])
    direct: set[str] = set()
    if claim_id:
        direct.update(item["id"] for item in sections.values() if claim_id in item.get("claim_ids", []))
        if not direct:
            raise ValueError(f"No section uses claim {claim_id}")
    if section_id:
        if section_id not in sections:
            raise ValueError(f"Unknown section {section_id}")
        direct.add(section_id)
    affected = set(direct)
    queue = deque(direct)
    while queue:
        current = queue.popleft()
        for dependent in downstream[current]:
            if dependent not in affected:
                affected.add(dependent)
                queue.append(dependent)
    ordered = [item["id"] for item in outline["sections"] if item["id"] in affected]
    return {
        "trigger": claim_id or section_id,
        "direct_sections": sorted(direct),
        "review_sections": ordered,
        "note": "Review scope only; revisions still require section-specific change requests.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--claim")
    group.add_argument("--section")
    args = parser.parse_args()
    try:
        result = calculate_impact(args.product, args.claim, args.section)
    except (ValueError, FileNotFoundError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
