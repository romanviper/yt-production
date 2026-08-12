#!/usr/bin/env python3
"""Create a product workspace from the versioned template."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE_ROOT = REPO_ROOT / "templates" / "product"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def output_name(name: str) -> str:
    return name.replace(".template.", ".")


def create_product(
    products_root: Path,
    slug: str,
    title: str,
    template_root: Path = DEFAULT_TEMPLATE_ROOT,
) -> Path:
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("Slug chỉ được gồm chữ thường, số và dấu gạch ngang.")
    if not title.strip():
        raise ValueError("Title không được để trống.")
    if not template_root.is_dir():
        raise FileNotFoundError(f"Không tìm thấy template: {template_root}")

    destination = products_root / slug
    if destination.exists():
        raise FileExistsError(f"Product đã tồn tại: {destination}")

    values = {
        "SLUG": slug,
        "TITLE": title.strip(),
        "DATE": date.today().isoformat(),
    }

    for source in sorted(template_root.rglob("*")):
        relative = source.relative_to(template_root)
        rendered_parts = [output_name(render(part, values)) for part in relative.parts]
        target = destination.joinpath(*rendered_parts)
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() in {".md", ".json", ".txt"}:
            target.write_text(render(source.read_text(encoding="utf-8"), values), encoding="utf-8")
        else:
            shutil.copy2(source, target)

    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--title", required=True)
    parser.add_argument("--products-root", type=Path, default=REPO_ROOT / "products")
    args = parser.parse_args()
    try:
        path = create_product(args.products_root, args.slug, args.title)
    except (ValueError, FileExistsError, FileNotFoundError) as exc:
        parser.error(str(exc))
    print(f"Created {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

