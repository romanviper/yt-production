#!/usr/bin/env python3
"""Deterministically assemble human-approved section drafts."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.common import narration_text, read_json, sha256, word_count, write_json
    from scripts.outline_contract import OUTLINE_SCHEMA_VERSION, normalize_outline_contract
except ModuleNotFoundError:
    from common import narration_text, read_json, sha256, word_count, write_json
    from outline_contract import OUTLINE_SCHEMA_VERSION, normalize_outline_contract


def assemble_product(product_dir: Path, partial: bool = False, write: bool = True) -> dict:
    product_dir = product_dir.resolve()
    product = read_json(product_dir / "product.json")
    outline = read_json(product_dir / "02_outline" / "outline.json")
    outline = normalize_outline_contract(outline, product.get("target"))
    current_contract = outline.get("schema_version") == OUTLINE_SCHEMA_VERSION
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

    movements = {
        item["id"]: item
        for item in outline.get("script_architecture", {}).get("movements", [])
        if isinstance(item, dict) and item.get("id")
    }
    acts = {
        item["id"]: item
        for item in outline.get("script_architecture", {}).get("acts", [])
        if isinstance(item, dict) and item.get("id")
    }
    blocks = [f"# {product['working_title']}", ""]
    records = []
    total = 0
    current_movement = None
    current_act = None
    for item in selected:
        draft = product_dir / "03_sections" / item["id"] / "draft.md"
        if not draft.is_file():
            raise FileNotFoundError(f"Missing draft for {item['id']}")
        text = narration_text(draft.read_text(encoding="utf-8"), item["id"])
        words = word_count(text)
        total += words
        if current_contract:
            movement_ids = item["movement_ids"]
            act_id = movements[movement_ids[0]]["act_id"]
            if act_id != current_act:
                blocks.extend([f"## {acts[act_id]['title']}", ""])
                current_act = act_id
            record_scope = {"act_id": act_id, "movement_ids": movement_ids}
        else:
            movement_id = item["movement_id"]
            if movement_id != current_movement:
                movement = movements[movement_id]
                blocks.extend([f"## {movement['title']}", ""])
                current_movement = movement_id
            record_scope = {"movement_id": movement_id}
        blocks.extend([f"<!-- production-unit: {item['id']} — {item['title']} -->", "", text, ""])
        records.append(
            {
                "id": item["id"],
                **record_scope,
                "source": str(draft.relative_to(product_dir)),
                "sha256": sha256(draft),
                "words": words,
            }
        )
    manifest = {
        "schema_version": 3 if current_contract else 2,
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
