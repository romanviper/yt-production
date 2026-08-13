#!/usr/bin/env python3
"""Deterministically consolidate local research ledgers before AI synthesis."""

from __future__ import annotations

import argparse
import copy
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import product_relative, read_json, sha256, write_json
except ModuleNotFoundError:  # Direct execution: python scripts/consolidate_research.py
    from common import product_relative, read_json, sha256, write_json


GENERATOR = "scripts/consolidate_research.py"
MANIFEST_PATH = Path("01_research/consolidation.json")
SOURCE_INDEX_PATH = Path("01_research/source-index.json")
CLAIM_LEDGER_PATH = Path("01_research/claim-ledger.json")


def _list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    return list(value) if isinstance(value, list) else [value]


def _union(left: list[Any], right: list[Any]) -> list[Any]:
    result = copy.deepcopy(left)
    for item in right:
        if item not in result:
            result.append(copy.deepcopy(item))
    return result


def _normalized_text(value: Any) -> str:
    return " ".join(str(value or "").split()).casefold()


def _source_key(source: dict[str, Any]) -> tuple[str, ...]:
    url = str(source.get("url") or "").strip().rstrip("/").casefold()
    if url:
        return ("url", url)
    return (
        "metadata",
        _normalized_text(source.get("title")),
        _normalized_text(source.get("author")),
        _normalized_text(source.get("year")),
    )


def _input_records(product_dir: Path) -> list[dict[str, Any]]:
    plan = read_json(product_dir / "01_research" / "plan.json")
    records: list[dict[str, Any]] = []
    for unit in plan.get("workstreams", []):
        unit_id = unit.get("id", "")
        for name in ["sources.json", "claims.json"]:
            path = product_dir / "01_research" / "workstreams" / unit_id / name
            if not path.is_file():
                raise FileNotFoundError(f"Missing research ledger: {product_relative(product_dir, path)}")
            records.append(
                {
                    "path": product_relative(product_dir, path),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    return records


def validate_global_ledgers(product_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        sources_doc = read_json(product_dir / SOURCE_INDEX_PATH)
        claims_doc = read_json(product_dir / CLAIM_LEDGER_PATH)
    except (FileNotFoundError, ValueError) as exc:
        return [f"invalid consolidated research ledger: {exc}"]
    if sources_doc.get("status") != "complete":
        errors.append("global source index status must be complete")
    if claims_doc.get("status") != "complete":
        errors.append("global claim ledger status must be complete")
    source_ids: set[str] = set()
    for item in sources_doc.get("sources", []):
        source_id = item.get("id", "")
        if not re.fullmatch(r"SRC-\d{4}", source_id):
            errors.append(f"invalid global source ID: {source_id or '?'}")
        if source_id in source_ids:
            errors.append(f"duplicate global source ID: {source_id}")
        source_ids.add(source_id)
        if not item.get("provenance"):
            errors.append(f"global source {source_id or '?'} missing workstream provenance")
    claim_ids: set[str] = set()
    for item in claims_doc.get("claims", []):
        claim_id = item.get("id", "")
        if not re.fullmatch(r"CLM-\d{4}", claim_id):
            errors.append(f"invalid global claim ID: {claim_id or '?'}")
        if claim_id in claim_ids:
            errors.append(f"duplicate global claim ID: {claim_id}")
        claim_ids.add(claim_id)
        if not item.get("provenance"):
            errors.append(f"global claim {claim_id or '?'} missing workstream provenance")
        for source_id in item.get("sources", []):
            if source_id not in source_ids:
                errors.append(f"global claim {claim_id or '?'} references unknown source: {source_id}")
    return errors


def _manifest(product_dir: Path, mode: str) -> dict[str, Any]:
    outputs = []
    for relative in [SOURCE_INDEX_PATH, CLAIM_LEDGER_PATH]:
        path = product_dir / relative
        outputs.append({"path": relative.as_posix(), "sha256": sha256(path), "bytes": path.stat().st_size})
    return {
        "schema_version": 1,
        "generator": GENERATOR,
        "mode": mode,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "inputs": _input_records(product_dir),
        "outputs": outputs,
    }


def verify_consolidation(product_dir: Path) -> list[str]:
    product_dir = product_dir.resolve()
    manifest_path = product_dir / MANIFEST_PATH
    if not manifest_path.is_file():
        return ["missing deterministic research consolidation manifest"]
    try:
        manifest = read_json(manifest_path)
        expected_inputs = _input_records(product_dir)
    except (FileNotFoundError, ValueError) as exc:
        return [f"invalid research consolidation: {exc}"]
    errors: list[str] = []
    if manifest.get("generator") != GENERATOR:
        errors.append(f"research consolidation generator must be {GENERATOR}")
    if manifest.get("inputs") != expected_inputs:
        errors.append("research consolidation is stale relative to workstream ledgers")
    expected_outputs = {SOURCE_INDEX_PATH.as_posix(), CLAIM_LEDGER_PATH.as_posix()}
    output_records = manifest.get("outputs")
    if (
        not isinstance(output_records, list)
        or not all(isinstance(item, dict) for item in output_records)
        or {item.get("path") for item in output_records} != expected_outputs
    ):
        errors.append("research consolidation must declare the global source and claim ledgers")
    else:
        for record in output_records:
            path = product_dir / record["path"]
            if not path.is_file() or sha256(path) != record.get("sha256") or path.stat().st_size != record.get("bytes"):
                errors.append(f"stale consolidated research output: {record['path']}")
    errors.extend(validate_global_ledgers(product_dir))
    return errors


def consolidate(product_dir: Path) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    plan = read_json(product_dir / "01_research" / "plan.json")
    source_records: list[dict[str, Any]] = []
    claim_records: list[dict[str, Any]] = []
    source_by_key: dict[tuple[str, ...], dict[str, Any]] = {}
    claim_by_statement: dict[str, dict[str, Any]] = {}
    local_source_map: dict[tuple[str, str], str] = {}

    for unit in plan.get("workstreams", []):
        unit_id = unit.get("id", "")
        root = product_dir / "01_research" / "workstreams" / unit_id
        sources_doc = read_json(root / "sources.json")
        claims_doc = read_json(root / "claims.json")
        if sources_doc.get("status") != "complete" or claims_doc.get("status") != "complete":
            raise ValueError(f"Incomplete workstream ledgers: {unit_id}")
        if "Status: complete" not in (root / "synthesis.md").read_text(encoding="utf-8"):
            raise ValueError(f"Incomplete workstream synthesis: {unit_id}")

        local_source_ids: set[str] = set()
        for source in sources_doc.get("sources", []):
            local_id = source.get("id", "")
            if not re.fullmatch(rf"{re.escape(unit_id)}-SRC-\d{{3}}", local_id) or local_id in local_source_ids:
                raise ValueError(f"Invalid or duplicate local source ID: {local_id or '?'}")
            if not source.get("title"):
                raise ValueError(f"Local source {local_id} is missing a title")
            local_source_ids.add(local_id)
            key = _source_key(source)
            record = source_by_key.get(key)
            if record is None:
                record = copy.deepcopy(source)
                record["id"] = f"SRC-{len(source_records) + 1:04d}"
                record["locators"] = _list(record.get("locators"))
                record["limitations"] = _list(record.get("limitations"))
                record["notes"] = _list(record.get("notes"))
                record["provenance"] = []
                source_records.append(record)
                source_by_key[key] = record
            else:
                for field in ["locators", "limitations", "notes"]:
                    record[field] = _union(_list(record.get(field)), _list(source.get(field)))
            record["provenance"] = _union(record["provenance"], [{"workstream": unit_id, "local_id": local_id}])
            local_source_map[(unit_id, local_id)] = record["id"]

        local_claim_ids: set[str] = set()
        for claim in claims_doc.get("claims", []):
            local_id = claim.get("id", "")
            if not re.fullmatch(rf"{re.escape(unit_id)}-CLM-\d{{3}}", local_id) or local_id in local_claim_ids:
                raise ValueError(f"Invalid or duplicate local claim ID: {local_id or '?'}")
            if not claim.get("statement"):
                raise ValueError(f"Local claim {local_id} is missing a statement")
            local_claim_ids.add(local_id)
            mapped_sources = []
            for source_id in claim.get("sources", []):
                mapped = local_source_map.get((unit_id, source_id))
                if not mapped:
                    raise ValueError(f"Claim {local_id} references unknown local source: {source_id}")
                if mapped not in mapped_sources:
                    mapped_sources.append(mapped)
            key = _normalized_text(claim.get("statement"))
            record = claim_by_statement.get(key)
            if record is None:
                record = copy.deepcopy(claim)
                record["id"] = f"CLM-{len(claim_records) + 1:04d}"
                record["sources"] = mapped_sources
                record["provenance"] = []
                claim_records.append(record)
                claim_by_statement[key] = record
            else:
                record["sources"] = _union(record.get("sources", []), mapped_sources)
                for field in ["type", "confidence", "status", "counterevidence", "narrative_implication"]:
                    if claim.get(field) is not None and claim.get(field) != "" and claim.get(field) != record.get(field):
                        variants = record.setdefault("merge_variants", {}).setdefault(field, [])
                        record["merge_variants"][field] = _union(variants, [record.get(field), claim.get(field)])
            record["provenance"] = _union(record["provenance"], [{"workstream": unit_id, "local_id": local_id}])

    write_json(
        product_dir / SOURCE_INDEX_PATH,
        {"schema_version": 1, "product": product_dir.name, "status": "complete", "sources": source_records},
    )
    write_json(
        product_dir / CLAIM_LEDGER_PATH,
        {"schema_version": 1, "product": product_dir.name, "status": "complete", "claims": claim_records},
    )
    manifest = _manifest(product_dir, "deterministic")
    write_json(product_dir / MANIFEST_PATH, manifest)
    return manifest


def adopt(product_dir: Path) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    errors = validate_global_ledgers(product_dir)
    if errors:
        raise ValueError("Cannot adopt invalid global ledgers: " + "; ".join(errors))
    manifest = _manifest(product_dir, "adopted")
    write_json(product_dir / MANIFEST_PATH, manifest)
    return manifest


def ensure_consolidated(product_dir: Path) -> dict[str, Any]:
    product_dir = product_dir.resolve()
    if not verify_consolidation(product_dir):
        return read_json(product_dir / MANIFEST_PATH)
    return consolidate(product_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--adopt", action="store_true", help="Register already-reviewed global ledgers without rewriting them.")
    args = parser.parse_args()
    try:
        manifest = adopt(args.product) if args.adopt else consolidate(args.product)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        parser.error(str(exc))
    print(
        f"Research ledgers ready: {len(manifest['inputs'])} inputs -> "
        f"{', '.join(item['path'] for item in manifest['outputs'])}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
