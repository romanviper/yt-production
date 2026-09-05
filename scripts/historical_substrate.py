#!/usr/bin/env python3
"""Validate Historical Substrate authority and materialize Writer-facing section views."""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    from scripts.common import read_json
    from scripts.historical_substrate_contract import (
        materialize_writer_section_substrate,
        validate_historical_substrate,
        verify_writer_section_substrate,
    )
except ModuleNotFoundError:  # Direct execution
    from common import read_json
    from historical_substrate_contract import (
        materialize_writer_section_substrate,
        validate_historical_substrate,
        verify_writer_section_substrate,
    )


def validate_product(product_dir: Path, *, require_product_complete: bool = False) -> list[str]:
    product_dir = product_dir.resolve()
    substrate_path = product_dir / "01_research" / "historical-substrate.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    if not substrate_path.is_file():
        return ["missing 01_research/historical-substrate.json"]
    if not claims_path.is_file():
        return ["missing 01_research/claim-ledger.json"]
    if not sources_path.is_file():
        return ["missing 01_research/source-index.json"]
    return validate_historical_substrate(
        read_json(substrate_path),
        read_json(claims_path),
        read_json(sources_path),
        require_product_complete=require_product_complete,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    validate_parser = sub.add_parser("validate", help="validate product-level Historical Substrate")
    validate_parser.add_argument("product", type=Path)
    validate_parser.add_argument("--require-product-complete", action="store_true")

    materialize_parser = sub.add_parser("materialize-section", help="build one Writer-facing section substrate")
    materialize_parser.add_argument("product", type=Path)
    materialize_parser.add_argument("section")

    verify_parser = sub.add_parser("verify-section", help="verify one Writer-facing section substrate")
    verify_parser.add_argument("product", type=Path)
    verify_parser.add_argument("section")

    args = parser.parse_args()
    if args.command == "validate":
        errors = validate_product(args.product, require_product_complete=args.require_product_complete)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Historical Substrate: valid")
        return 0

    if args.command == "materialize-section":
        path = materialize_writer_section_substrate(args.product, args.section)
        print(path)
        return 0

    errors = verify_writer_section_substrate(args.product, args.section)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Historical Substrate section {args.section}: current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
