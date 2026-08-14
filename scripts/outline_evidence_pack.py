#!/usr/bin/env python3
"""Build the compact, deterministic claim catalog used by outline tasks."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
except ModuleNotFoundError:
    from common import read_json, sha256, write_json


PACK_PATH = Path("01_research/outline-evidence-pack.json")
CLAIM_FIELDS = ("id", "statement", "type", "confidence", "status", "sources")


def compact_claim(claim: dict[str, Any]) -> dict[str, Any]:
    """Keep only fields needed to allocate evidence during architecture design."""

    return {field: claim.get(field) for field in CLAIM_FIELDS}


def expected_pack(product_dir: Path) -> dict[str, Any]:
    ledger_path = product_dir / "01_research" / "claim-ledger.json"
    ledger = read_json(ledger_path)
    if ledger.get("status") != "complete":
        raise ValueError("Claim ledger must be complete before building the outline evidence pack.")
    return {
        "schema_version": 1,
        "product": ledger.get("product", product_dir.name),
        "status": "complete",
        "claim_ledger_sha256": sha256(ledger_path),
        "claims": [compact_claim(item) for item in ledger.get("claims", [])],
        "contradiction_register": ledger.get("contradiction_register", []),
        "scope_note": (
            "This catalog is for architecture allocation. Claim provenance and research detail remain "
            "authoritative in claim-ledger.json and source-index.json outside the creative prompt."
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
