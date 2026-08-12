#!/usr/bin/env python3
"""Assemble approved chapter sources into a deterministic delivery artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ỹ]+\b", text, flags=re.UNICODE))


def assemble_product(product_dir: Path, partial: bool = False, write: bool = True) -> dict:
    product_dir = product_dir.resolve()
    product = json.loads((product_dir / "product.json").read_text(encoding="utf-8"))
    manifest = json.loads((product_dir / "03_outline" / "manifest.json").read_text(encoding="utf-8"))
    active = [chapter for chapter in manifest["chapters"] if chapter["status"] != "omitted"]
    unapproved = [chapter["id"] for chapter in active if chapter["status"] != "approved"]
    if unapproved and not partial:
        raise ValueError("Chưa thể assemble full delivery; chapter chưa approved: " + ", ".join(unapproved))

    selected = [chapter for chapter in active if chapter["status"] == "approved"]
    if not selected:
        raise ValueError("Không có chapter approved để assemble.")

    sections: list[str] = [f"# {product['working_title']}", ""]
    chapter_records: list[dict] = []
    total_words = 0
    for chapter in selected:
        path = product_dir / chapter["draft"]
        if not path.is_file():
            raise FileNotFoundError(f"Thiếu draft của {chapter['id']}: {path}")
        content = path.read_text(encoding="utf-8").strip()
        count = word_count(content)
        total_words += count
        sections.extend([f"## {chapter['id']} — {chapter['title']}", "", content, ""])
        chapter_records.append(
            {
                "id": chapter["id"],
                "source": chapter["draft"],
                "sha256": sha256(path),
                "words": count,
            }
        )

    wpm = int(product["target"]["narration_wpm"])
    output = "\n".join(sections).rstrip() + "\n"
    build = {
        "schema_version": 1,
        "product": product["slug"],
        "mode": "partial" if partial else "full",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "chapters": chapter_records,
        "total_words": total_words,
        "estimated_minutes": round(total_words / wpm, 1),
    }
    if write:
        delivery = product_dir / "06_delivery"
        delivery.mkdir(parents=True, exist_ok=True)
        (delivery / "script.md").write_text(output, encoding="utf-8")
        (delivery / "assembly-manifest.json").write_text(
            json.dumps(build, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    return {"script": output, "manifest": build}


def check_freshness(product_dir: Path) -> list[str]:
    product_dir = product_dir.resolve()
    build_path = product_dir / "06_delivery" / "assembly-manifest.json"
    if not build_path.is_file():
        return ["Chưa có assembly-manifest.json."]
    build = json.loads(build_path.read_text(encoding="utf-8"))
    stale: list[str] = []
    for chapter in build.get("chapters", []):
        source = product_dir / chapter["source"]
        if not source.is_file():
            stale.append(f"Thiếu source: {chapter['source']}")
        elif sha256(source) != chapter["sha256"]:
            stale.append(f"Đã thay đổi sau assembly: {chapter['id']}")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--partial", action="store_true", help="Preview chỉ với chapter đã approved.")
    parser.add_argument("--check", action="store_true", help="Chỉ kiểm tra build có stale không.")
    args = parser.parse_args()
    if args.check:
        stale = check_freshness(args.product)
        if stale:
            for item in stale:
                print(f"STALE: {item}")
            return 1
        print("Assembly is fresh.")
        return 0
    try:
        result = assemble_product(args.product, partial=args.partial)
    except (ValueError, FileNotFoundError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    manifest = result["manifest"]
    print(
        f"Assembled {len(manifest['chapters'])} chapter(s), "
        f"{manifest['total_words']} words, ~{manifest['estimated_minutes']} minutes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

