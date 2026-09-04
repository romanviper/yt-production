#!/usr/bin/env python3
"""Executable contract for source-backed historical-world representations.

Historical Substrate is intentionally neither an evidence ledger nor a story plan.
It converts approved evidence authority into bounded statements about historical
states, practices, processes, relations, changes, and object affordances.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
except ModuleNotFoundError:  # Direct execution: python scripts/historical_substrate_contract.py
    from common import read_json, sha256, write_json


HISTORICAL_SUBSTRATE_SCHEMA_VERSION = 1
SECTION_SUBSTRATE_SCHEMA_VERSION = 1

ALLOWED_KINDS = {
    "practice",
    "state",
    "process",
    "relation",
    "change",
    "object_affordance",
    "actor_role",
    "constraint",
}
ALLOWED_EPISTEMIC_STATUS = {
    "documented",
    "qualified_inference",
    "bounded_reconstruction",
}

# Historical Substrate may describe historical reality, but it must never decide
# how narration should be staged or sequenced.
FORBIDDEN_NARRATIVE_FIELDS = {
    "opening",
    "hook",
    "carrier",
    "scene",
    "beat",
    "reveal",
    "climax",
    "ending",
    "emotional_turn",
    "camera",
    "story_role",
    "recommended_order",
    "paragraph_order",
    "narrative_route",
}

_EVIDENCE_WORLD_MARKERS = (
    "bằng chứng",
    "evidence",
    "catalogue",
    "catalog ",
    "corpus",
    "hiện vật cho thấy",
    "artifact shows",
    "surviving evidence",
    "preserved evidence",
)


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def binding_sha256(section_spec: dict[str, Any]) -> str:
    """Hash only the history-facing section contract, not prose/editorial metadata."""

    value = {
        "id": section_spec.get("id"),
        "historical_territory": section_spec.get("historical_territory"),
        "historical_change": section_spec.get("historical_change"),
        "historical_substrate_ids": section_spec.get("historical_substrate_ids", []),
    }
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _claim_map(claims_doc: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(claims_doc, dict):
        return {}
    return {
        item["id"]: item
        for item in claims_doc.get("claims", [])
        if isinstance(item, dict) and _nonempty_text(item.get("id"))
    }


def _source_map(sources_doc: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(sources_doc, dict):
        return {}
    return {
        item["id"]: item
        for item in sources_doc.get("sources", [])
        if isinstance(item, dict) and _nonempty_text(item.get("id"))
    }


def validate_historical_substrate(
    document: dict[str, Any],
    claims_doc: dict[str, Any] | None = None,
    sources_doc: dict[str, Any] | None = None,
    *,
    require_product_complete: bool = False,
) -> list[str]:
    """Validate substrate shape, authority linkage, and narrative-route neutrality."""

    errors: list[str] = []
    if document.get("schema_version") != HISTORICAL_SUBSTRATE_SCHEMA_VERSION:
        errors.append(
            f"historical substrate schema_version must be {HISTORICAL_SUBSTRATE_SCHEMA_VERSION}"
        )

    coverage = document.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("historical substrate coverage must be an object")
        coverage = {}
    mode = coverage.get("mode")
    if mode not in {"product", "section_migration"}:
        errors.append("historical substrate coverage.mode must be product or section_migration")
    if require_product_complete and mode != "product":
        errors.append("outline creation requires product-complete historical substrate coverage")
    covered_sections = coverage.get("covered_sections", [])
    if not _string_list(covered_sections, allow_empty=True):
        errors.append("historical substrate coverage.covered_sections must be a list of section IDs")

    records = document.get("records")
    if not isinstance(records, list) or not records:
        errors.append("historical substrate records must be a non-empty list")
        return errors

    claims = _claim_map(claims_doc)
    sources = _source_map(sources_doc)
    seen_ids: set[str] = set()

    for index, record in enumerate(records):
        prefix = f"historical substrate record #{index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue

        forbidden = sorted(FORBIDDEN_NARRATIVE_FIELDS.intersection(record))
        if forbidden:
            errors.append(f"{prefix} contains narrative-authority fields: {', '.join(forbidden)}")

        record_id = record.get("id")
        if not _nonempty_text(record_id) or not re.fullmatch(r"HS-[A-Z0-9]+-\d{4}", str(record_id)):
            errors.append(f"{prefix} id must use HS-<SCOPE>-#### format")
        elif record_id in seen_ids:
            errors.append(f"historical substrate has duplicate id: {record_id}")
        else:
            seen_ids.add(str(record_id))

        if record.get("kind") not in ALLOWED_KINDS:
            errors.append(f"{prefix} kind is invalid: {record.get('kind')!r}")
        if not _nonempty_text(record.get("statement")):
            errors.append(f"{prefix} statement is required")
        if record.get("epistemic_status") not in ALLOWED_EPISTEMIC_STATUS:
            errors.append(f"{prefix} epistemic_status is invalid")
        if not _nonempty_text(record.get("time_scope")):
            errors.append(f"{prefix} time_scope is required")
        if not _nonempty_text(record.get("place_scope")):
            errors.append(f"{prefix} place_scope is required")

        claim_ids = record.get("claim_ids")
        if not _string_list(claim_ids):
            errors.append(f"{prefix} claim_ids must be a non-empty list")
            claim_ids = []
        elif len(claim_ids) != len(set(claim_ids)):
            errors.append(f"{prefix} claim_ids must be unique")

        source_refs = record.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{prefix} source_refs must be a non-empty list")
            source_refs = []
        referenced_source_ids: set[str] = set()
        for ref_index, ref in enumerate(source_refs):
            ref_prefix = f"{prefix} source_ref #{ref_index + 1}"
            if not isinstance(ref, dict) or not _nonempty_text(ref.get("source_id")):
                errors.append(f"{ref_prefix} requires source_id")
                continue
            referenced_source_ids.add(str(ref["source_id"]))
            locator = ref.get("locator")
            if locator is not None and not _nonempty_text(locator):
                errors.append(f"{ref_prefix} locator must be non-empty when present")

        limitations = record.get("limitations", [])
        if not _string_list(limitations, allow_empty=True):
            errors.append(f"{prefix} limitations must be a list of non-empty strings")

        if claims:
            unknown_claims = [claim_id for claim_id in claim_ids if claim_id not in claims]
            if unknown_claims:
                errors.append(f"{prefix} references unknown claims: {', '.join(unknown_claims)}")
            not_ready = [
                claim_id
                for claim_id in claim_ids
                if claim_id in claims and claims[claim_id].get("status") not in {"supported", "qualified"}
            ]
            if not_ready:
                errors.append(f"{prefix} references claims not writing-ready: {', '.join(not_ready)}")

            allowed_sources = {
                source_id
                for claim_id in claim_ids
                if claim_id in claims
                for source_id in claims[claim_id].get("sources", [])
                if isinstance(source_id, str)
            }
            outside = sorted(referenced_source_ids - allowed_sources)
            if outside:
                errors.append(
                    f"{prefix} source refs exceed referenced claim authority: {', '.join(outside)}"
                )

        if sources:
            unknown_sources = sorted(referenced_source_ids - sources.keys())
            if unknown_sources:
                errors.append(f"{prefix} references unknown sources: {', '.join(unknown_sources)}")
            unreviewed = sorted(
                source_id
                for source_id in referenced_source_ids
                if source_id in sources and sources[source_id].get("status") != "reviewed"
            )
            if unreviewed:
                errors.append(f"{prefix} references unreviewed sources: {', '.join(unreviewed)}")

    return errors


def validate_section_binding(
    section_spec: dict[str, Any],
    substrate: dict[str, Any],
) -> list[str]:
    """Ensure a section is bound to historical reality rather than evidence-state prose."""

    errors: list[str] = []
    section_id = str(section_spec.get("id") or "?")
    territory = section_spec.get("historical_territory")
    if not _nonempty_text(territory):
        errors.append(f"section {section_id} historical_territory is required")
    elif "?" in str(territory):
        errors.append(f"section {section_id} historical_territory must not be an answer-shaped question")

    historical_change = section_spec.get("historical_change")
    if (
        not isinstance(historical_change, dict)
        or not _nonempty_text(historical_change.get("from"))
        or not _nonempty_text(historical_change.get("to"))
    ):
        errors.append(
            f"section {section_id} historical_change must contain non-empty historical-world from/to states"
        )
    else:
        combined = f"{historical_change['from']} {historical_change['to']}".lower()
        markers = [marker for marker in _EVIDENCE_WORLD_MARKERS if marker in combined]
        if markers:
            errors.append(
                f"section {section_id} historical_change describes evidence-state rather than historical-world state: "
                + ", ".join(sorted(set(markers)))
            )

    selected_ids = section_spec.get("historical_substrate_ids")
    if not _string_list(selected_ids):
        errors.append(f"section {section_id} historical_substrate_ids must be a non-empty list")
        return errors
    if len(selected_ids) != len(set(selected_ids)):
        errors.append(f"section {section_id} historical_substrate_ids must be unique")

    known_records = {
        item.get("id"): item
        for item in substrate.get("records", [])
        if isinstance(item, dict) and _nonempty_text(item.get("id"))
    }
    unknown = [item for item in selected_ids if item not in known_records]
    if unknown:
        errors.append(f"section {section_id} references unknown historical substrate records: {', '.join(unknown)}")

    outline_claim_ids = {
        item for item in section_spec.get("claim_ids", []) if isinstance(item, str) and item
    }
    if outline_claim_ids:
        substrate_claim_ids = {
            claim_id
            for record_id in selected_ids
            if record_id in known_records
            for claim_id in known_records[record_id].get("claim_ids", [])
            if isinstance(claim_id, str)
        }
        outside = sorted(substrate_claim_ids - outline_claim_ids)
        if outside:
            errors.append(
                f"section {section_id} substrate exceeds approved outline claim territory: {', '.join(outside)}"
            )

    return errors


def build_writer_section_substrate(
    product_substrate_path: Path,
    section_spec: dict[str, Any],
    outline_path: Path,
) -> dict[str, Any]:
    """Project validated history into a Writer-facing view without research-ledger payloads."""

    substrate = read_json(product_substrate_path)
    selected_ids = list(section_spec.get("historical_substrate_ids", []))
    records = {
        item["id"]: item
        for item in substrate.get("records", [])
        if isinstance(item, dict) and _nonempty_text(item.get("id"))
    }
    selected = [records[item_id] for item_id in selected_ids]

    primitives = [
        {
            "id": item["id"],
            "kind": item["kind"],
            "statement": item["statement"],
            "epistemic_status": item["epistemic_status"],
            "time_scope": item["time_scope"],
            "place_scope": item["place_scope"],
        }
        for item in selected
    ]
    boundaries = [
        {"id": item["id"], "limitations": list(item.get("limitations", []))}
        for item in selected
        if item.get("limitations")
    ]

    return {
        "schema_version": SECTION_SUBSTRATE_SCHEMA_VERSION,
        "section": section_spec.get("id"),
        "historical_territory": section_spec.get("historical_territory"),
        "historical_change": section_spec.get("historical_change"),
        "primitives": primitives,
        "boundaries": boundaries,
        "authority_binding": {
            "product_substrate_sha256": sha256(product_substrate_path),
            "outline_sha256": sha256(outline_path),
            "section_binding_sha256": binding_sha256(section_spec),
        },
        "writer_contract": (
            "Author from the historical world represented by primitives and historical_change. "
            "Boundaries are claim limits, not lines that must be narrated. Use bounded evidence lookup only "
            "to verify or sharpen a telling you have already chosen."
        ),
    }


def verify_writer_section_substrate(
    product_dir: Path,
    section: str,
) -> list[str]:
    """Verify a section projection is current and deterministically reproducible."""

    product_dir = product_dir.resolve()
    product_substrate_path = product_dir / "01_research" / "historical-substrate.json"
    outline_path = product_dir / "02_outline" / "outline.json"
    section_path = product_dir / "03_sections" / section / "historical-substrate.json"
    if not product_substrate_path.is_file():
        return ["missing 01_research/historical-substrate.json"]
    if not outline_path.is_file():
        return ["missing 02_outline/outline.json"]
    if not section_path.is_file():
        return [f"missing 03_sections/{section}/historical-substrate.json"]

    outline = read_json(outline_path)
    matches = [
        item
        for item in outline.get("sections", [])
        if isinstance(item, dict) and item.get("id") == section
    ]
    if len(matches) != 1:
        return [f"outline must contain section {section} exactly once"]
    expected = build_writer_section_substrate(product_substrate_path, matches[0], outline_path)
    actual = read_json(section_path)
    if actual != expected:
        return [f"section {section} historical substrate projection is stale or edited"]
    return []


def materialize_writer_section_substrate(product_dir: Path, section: str) -> Path:
    """Validate authority + section binding, then write the deterministic Writer projection."""

    product_dir = product_dir.resolve()
    substrate_path = product_dir / "01_research" / "historical-substrate.json"
    outline_path = product_dir / "02_outline" / "outline.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    substrate = read_json(substrate_path)
    claims = read_json(claims_path)
    sources = read_json(sources_path)
    errors = validate_historical_substrate(substrate, claims, sources)
    if errors:
        raise ValueError("Invalid historical substrate: " + "; ".join(errors))

    outline = read_json(outline_path)
    matches = [
        item
        for item in outline.get("sections", [])
        if isinstance(item, dict) and item.get("id") == section
    ]
    if len(matches) != 1:
        raise ValueError(f"Outline must contain section {section} exactly once.")
    section_spec = matches[0]
    binding_errors = validate_section_binding(section_spec, substrate)
    if binding_errors:
        raise ValueError("Invalid historical substrate section binding: " + "; ".join(binding_errors))

    output = product_dir / "03_sections" / section / "historical-substrate.json"
    write_json(output, build_writer_section_substrate(substrate_path, section_spec, outline_path))
    return output
