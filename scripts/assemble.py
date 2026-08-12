#!/usr/bin/env python3
"""Deterministically assemble human-approved section drafts."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.common import read_json, sha256, word_count, write_json
except ModuleNotFoundError:
    from common import read_json, sha256, word_count, write_json


def assemble_product(product_dir: Path, partial: bool = False, write: bool = True) -> dict:
    product_dir = product_dir.resolve()
    product = read_json(product_dir / "product.json")
    outline = read_json(product_dir / "02_outline" / "outline.json")
    selected = []
    unapproved = []
    for item in sorted(outline.get("sections", []), key=lambda value: value["order"]):
        state_path = product_dir / "03_sections" / item["id"] / "section.json"
        state = read_json(state_path)
        if state.get("status") == "approved" and state.get("human_approved") is True:
            selected.append(item)
        else:
            unapproved.append(item["id"])
    if unapproved and not partial:
        raise ValueError("Unapproved sections: " + ", ".join(unapproved))
    if not selected:
        raise ValueError("No human-approved section available for assembly.")

    blocks = [f"# {product['working_title']}", ""]
    records = []
    total = 0
    for item in selected:
        draft = product_dir / "03_sections" / item["id"] / "draft.md"
        if not draft.is_file():
            raise FileNotFoundError(f"Missing draft for {item['id']}")
        text = draft.read_text(encoding="utf-8").strip()
        words = word_count(text)
        total += words
        blocks.extend([f"## {item['id']} — {item['title']}", "", text, ""])
        records.append({"id": item["id"], "source": str(draft.relative_to(product_dir)), "sha256": sha256(draft), "words": words})
    manifest = {
        "schema_version": 2,
        "product": product["slug"],
        "mode": "partial" if partial else "full",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sections": records,
        "total_words": total,
        "estimated_minutes": round(total / int(product["target"]["narration_wpm"]), 1),
    }
    script = "\n".join(blocks).rstrip() + "\n"
    if write:
        delivery = product_dir / "05_delivery"
        delivery.mkdir(parents=True, exist_ok=True)
        (delivery / "script.md").write_text(script, encoding="utf-8")
        write_json(delivery / "assembly-manifest.json", manifest)
    return {"script": script, "manifest": manifest}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--partial", action="store_true")
    args = parser.parse_args()
    try:
        result = assemble_product(args.product, args.partial)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        parser.error(str(exc))
    manifest = result["manifest"]
    print(f"Assembled {len(manifest['sections'])} section(s), {manifest['total_words']} words.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
