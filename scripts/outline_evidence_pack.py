#!/usr/bin/env python3
"""Build the compact deterministic truth/evidence catalog used by outline tasks."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
except ModuleNotFoundError:
    from common import read_json, sha256, write_json


PACK_PATH = Path("01_research/outline-evidence-pack.json")
CLAIM_LEDGER_PATH = Path("01_research/claim-ledger.json")
SOURCE_INDEX_PATH = Path("01_research/source-index.json")
CLAIM_FIELDS = (
    "id",
    "statement",
    "type",
    "confidence",
    "status",
    "sources",
    "counterevidence",
)
SOURCE_FIELDS = (
    "id",
    "title",
    "author",
    "year",
    "type",
    "authority",
    "status",
)


def compact_claim(claim: dict[str, Any]) -> dict[str, Any]:
    """Keep only truth/evidence fields needed to allocate section evidence territory."""

    return {field: claim.get(field) for field in CLAIM_FIELDS if claim.get(field) not in (None, "", [])}


def compact_source(source: dict[str, Any]) -> dict[str, Any]:
    """Keep source identity/authority without turning source detail into a story recommendation."""

    return {field: source.get(field) for field in SOURCE_FIELDS if source.get(field) not in (None, "", [])}


def expected_pack(product_dir: Path) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    claim_path = product_dir / CLAIM_LEDGER_PATH
    source_path = product_dir / SOURCE_INDEX_PATH
    claims_doc = read_json(claim_path)
    sources_doc = read_json(source_path)
    if claims_doc.get("status") != "complete":
        raise ValueError("Claim ledger must be complete before building the outline evidence pack.")
    if sources_doc.get("status") != "complete":
        raise ValueError("Source index must be complete before building the outline evidence pack.")

    source_ids = {
        item.get("id")
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict) and item.get("id")
    }
    for claim in claims_doc.get("claims", []):
        if not isinstance(claim, dict):
            raise ValueError("Claim ledger entries must be objects.")
        unknown = [source_id for source_id in claim.get("sources", []) if source_id not in source_ids]
        if unknown:
            raise ValueError(f"Claim {claim.get('id', '?')} references unknown sources: {', '.join(unknown)}")

    return {
        "schema_version": 4,
        "product": claims_doc.get("product", product_dir.name),
        "status": "complete",
        "claim_ledger_sha256": sha256(claim_path),
        "source_index_sha256": sha256(source_path),
        "claims": [compact_claim(item) for item in claims_doc.get("claims", [])],
        "sources": [compact_source(item) for item in sources_doc.get("sources", [])],
        "contradiction_register": claims_doc.get("contradiction_register", []),
        "scope_note": (
            "This pack supports architecture and evidence-scope decisions only. Claims define the approved truth territory; "
            "sources identify supporting authority. It intentionally does not prescribe story carriers, narrative routes, "
            "opening/reversal/ending material or prose mechanics."
        ),
    }


def build_outline_evidence_pack(product_dir: Path) -> Path:
    product_dir = product_dir.resolve()
    path = product_dir / PACK_PATH
    write_json(path, expected_pack(product_dir))
    return path


def verify_outline_evidence_pack(product_dir: Path) -> list[str]:
    product_dir = product_dir.resolve()
    path = product_dir / PACK_PATH
    if not path.is_file():
        return [f"missing outline evidence pack: {PACK_PATH}"]
    try:
        actual = read_json(path)
        expected = expected_pack(product_dir)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        return [f"invalid outline evidence pack: {exc}"]
    return [] if actual == expected else ["outline evidence pack is stale or not deterministically generated"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    args = parser.parse_args()
    path = build_outline_evidence_pack(args.product)
    print(f"Built {path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
