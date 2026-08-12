#!/usr/bin/env python3
"""Report the smallest transitive chapter set affected by a claim or chapter change."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


def calculate_impact(product_dir: Path, claim_id: str | None, chapter_id: str | None) -> dict:
    product_dir = product_dir.resolve()
    claims_doc = json.loads((product_dir / "01_research" / "claim-ledger.json").read_text(encoding="utf-8"))
    manifest = json.loads((product_dir / "03_outline" / "manifest.json").read_text(encoding="utf-8"))
    chapters = {chapter["id"]: chapter for chapter in manifest["chapters"]}
    downstream: dict[str, set[str]] = defaultdict(set)
    for chapter in chapters.values():
        for dependency in chapter.get("depends_on", []):
            downstream[dependency].add(chapter["id"])

    direct: set[str] = set()
    if claim_id:
        claim = next((item for item in claims_doc.get("claims", []) if item.get("id") == claim_id), None)
        if not claim:
            raise ValueError(f"Không tìm thấy claim {claim_id}.")
        direct.update(claim.get("used_by", []))
        direct.update(
            chapter["id"] for chapter in chapters.values() if claim_id in chapter.get("claims", [])
        )
    if chapter_id:
        if chapter_id not in chapters:
            raise ValueError(f"Không tìm thấy chapter {chapter_id}.")
        direct.add(chapter_id)

    affected = set(direct)
    queue = deque(direct)
    while queue:
        current = queue.popleft()
        for dependent in downstream[current]:
            if dependent not in affected:
                affected.add(dependent)
                queue.append(dependent)

    ordered = [chapter["id"] for chapter in manifest["chapters"] if chapter["id"] in affected]
    files: list[str] = []
    for current in ordered:
        chapter = chapters[current]
        files.extend(path for path in [chapter.get("brief"), chapter.get("draft")] if path)
    return {
        "trigger": claim_id or chapter_id,
        "direct_chapters": sorted(direct),
        "affected_chapters": ordered,
        "candidate_files": files,
        "note": "Đây là phạm vi cần review, không phải quyền tự động rewrite.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--claim")
    group.add_argument("--chapter")
    args = parser.parse_args()
    try:
        result = calculate_impact(args.product, args.claim, args.chapter)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

