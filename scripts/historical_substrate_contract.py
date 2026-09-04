#!/usr/bin/env python3
"""Executable authority contract for Historical Substrate.

This module owns three separations:
1. evidence authority -> product Historical Substrate;
2. approved outline + bounded section overlay -> canonical section binding;
3. canonical section binding -> deterministic Writer-facing projection.

The Writer projection hides claim/source IDs while retaining deterministic
provenance and truth boundaries.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
    from scripts.section_overlay_contract import resolve_section_spec
except ModuleNotFoundError:  # pragma: no cover
    from common import read_json, sha256, write_json
    from section_overlay_contract import resolve_section_spec


HISTORICAL_SUBSTRATE_SCHEMA_VERSION = 1
SECTION_SUBSTRATE_SCHEMA_VERSION = 1
HISTORICAL_SUBSTRATE_CONTRACT_VERSION = 1

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
FORBIDDEN_NARRATIVE_FIELDS = {
    "opening", "hook", "carrier", "scene", "beat", "reveal", "climax",
    "ending", "emotional_turn", "camera", "story_role", "recommended_order",
    "paragraph_order", "narrative_route",
}
_EVIDENCE_WORLD_MARKERS = (
    "bằng chứng", "evidence", "catalogue", "catalog ", "corpus",
    "hiện vật cho thấy", "artifact shows", "surviving evidence", "preserved evidence",
)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, allow_empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(_nonempty(item) for item in value)
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def binding_sha256(section_spec: dict[str, Any]) -> str:
    value = {
        "id": section_spec.get("id"),
        "historical_territory": section_spec.get("historical_territory"),
        "historical_change": section_spec.get("historical_change"),
        "historical_substrate_ids": section_spec.get("historical_substrate_ids", []),
    }
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _claim_map(doc: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(doc, dict):
        return {}
    return {
        item["id"]: item
        for item in doc.get("claims", [])
        if isinstance(item, dict) and _nonempty(item.get("id"))
    }


def _source_map(doc: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not isinstance(doc, dict):
        return {}
    return {
        item["id"]: item
        for item in doc.get("sources", [])
        if isinstance(item, dict) and _nonempty(item.get("id"))
    }


def validate_historical_substrate(
    document: dict[str, Any],
    claims_doc: dict[str, Any] | None = None,
    sources_doc: dict[str, Any] | None = None,
    *,
    require_product_complete: bool = False,
    required_sections: set[str | None] | None = None,
) -> list[str]:
    """Validate authority, coverage and route-neutrality.

    ``required_sections`` lets bounded section migrations pass only for the
    sections explicitly declared by ``coverage.covered_sections``. Operations
    that rebuild whole-product architecture must use ``require_product_complete``.
    """

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
    covered_sections = coverage.get("covered_sections", [])
    if not _string_list(covered_sections, allow_empty=True):
        errors.append("historical substrate coverage.covered_sections must be a list of section IDs")
        covered_sections = []
    if require_product_complete and mode != "product":
        errors.append("outline creation requires product-complete historical substrate coverage")
    if required_sections:
        requested = {item for item in required_sections if isinstance(item, str) and item}
        if mode == "section_migration":
            missing = sorted(requested - set(covered_sections))
            if missing:
                errors.append(
                    "historical substrate section_migration does not cover required sections: "
                    + ", ".join(missing)
                )

    records = document.get("records")
    if not isinstance(records, list) or not records:
        errors.append("historical substrate records must be a non-empty list")
        return errors

    claims = _claim_map(claims_doc)
    sources = _source_map(sources_doc)
    seen: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"historical substrate record #{index + 1}"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        forbidden = sorted(FORBIDDEN_NARRATIVE_FIELDS.intersection(record))
        if forbidden:
            errors.append(f"{prefix} contains narrative-authority fields: {', '.join(forbidden)}")

        record_id = record.get("id")
        if not _nonempty(record_id) or not re.fullmatch(r"HS-[A-Z0-9]+-\d{4}", str(record_id)):
            errors.append(f"{prefix} id must use HS-<SCOPE>-#### format")
        elif record_id in seen:
            errors.append(f"historical substrate has duplicate id: {record_id}")
        else:
            seen.add(str(record_id))

        if record.get("kind") not in ALLOWED_KINDS:
            errors.append(f"{prefix} kind is invalid: {record.get('kind')!r}")
        if not _nonempty(record.get("statement")):
            errors.append(f"{prefix} statement is required")
        if record.get("epistemic_status") not in ALLOWED_EPISTEMIC_STATUS:
            errors.append(f"{prefix} epistemic_status is invalid")
        if not _nonempty(record.get("time_scope")):
            errors.append(f"{prefix} time_scope is required")
        if not _nonempty(record.get("place_scope")):
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
        referenced_sources: set[str] = set()
        for ref_index, ref in enumerate(source_refs):
            ref_prefix = f"{prefix} source_ref #{ref_index + 1}"
            if not isinstance(ref, dict) or not _nonempty(ref.get("source_id")):
                errors.append(f"{ref_prefix} requires source_id")
                continue
            referenced_sources.add(str(ref["source_id"]))
            if ref.get("locator") is not None and not _nonempty(ref.get("locator")):
                errors.append(f"{ref_prefix} locator must be non-empty when present")

        limitations = record.get("limitations", [])
        if not _string_list(limitations, allow_empty=True):
            errors.append(f"{prefix} limitations must be a list of non-empty strings")

        if claims:
            unknown_claims = [claim_id for claim_id in claim_ids if claim_id not in claims]
            if unknown_claims:
                errors.append(f"{prefix} references unknown claims: {', '.join(unknown_claims)}")
            not_ready = [
                claim_id for claim_id in claim_ids
                if claim_id in claims and claims[claim_id].get("status") not in {"supported", "qualified"}
            ]
            if not_ready:
                errors.append(f"{prefix} references claims not writing-ready: {', '.join(not_ready)}")
            allowed_sources = {
                source_id
                for claim_id in claim_ids if claim_id in claims
                for source_id in claims[claim_id].get("sources", [])
                if isinstance(source_id, str)
            }
            outside = sorted(referenced_sources - allowed_sources)
            if outside:
                errors.append(
                    f"{prefix} source refs exceed referenced claim authority: {', '.join(outside)}"
                )
        if sources:
            unknown_sources = sorted(referenced_sources - sources.keys())
            if unknown_sources:
                errors.append(f"{prefix} references unknown sources: {', '.join(unknown_sources)}")
            unreviewed = sorted(
                source_id for source_id in referenced_sources
                if source_id in sources and sources[source_id].get("status") != "reviewed"
            )
            if unreviewed:
                errors.append(f"{prefix} references unreviewed sources: {', '.join(unreviewed)}")
    return errors


def validate_section_binding(section_spec: dict[str, Any], substrate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    section_id = str(section_spec.get("id") or "?")
    territory = section_spec.get("historical_territory")
    if not _nonempty(territory):
        errors.append(f"section {section_id} historical_territory is required")
    elif "?" in str(territory):
        errors.append(f"section {section_id} historical_territory must not be an answer-shaped question")

    change = section_spec.get("historical_change")
    if not isinstance(change, dict) or not _nonempty(change.get("from")) or not _nonempty(change.get("to")):
        errors.append(
            f"section {section_id} historical_change must contain non-empty historical-world from/to states"
        )
    else:
        combined = f"{change['from']} {change['to']}".lower()
        markers = sorted({marker for marker in _EVIDENCE_WORLD_MARKERS if marker in combined})
        if markers:
            errors.append(
                f"section {section_id} historical_change describes evidence-state rather than historical-world state: "
                + ", ".join(markers)
            )

    selected = section_spec.get("historical_substrate_ids")
    if not _string_list(selected):
        errors.append(f"section {section_id} historical_substrate_ids must be a non-empty list")
        return errors
    if len(selected) != len(set(selected)):
        errors.append(f"section {section_id} historical_substrate_ids must be unique")

    coverage = substrate.get("coverage", {}) if isinstance(substrate, dict) else {}
    if coverage.get("mode") == "section_migration" and section_id not in set(coverage.get("covered_sections", [])):
        errors.append(f"section {section_id} is outside section_migration substrate coverage")

    records = {
        item.get("id"): item
        for item in substrate.get("records", [])
        if isinstance(item, dict) and _nonempty(item.get("id"))
    }
    unknown = [item for item in selected if item not in records]
    if unknown:
        errors.append(
            f"section {section_id} references unknown historical substrate records: {', '.join(unknown)}"
        )

    claim_ceiling = {
        item for item in section_spec.get("claim_ids", []) if isinstance(item, str) and item
    }
    if claim_ceiling:
        substrate_claims = {
            claim_id
            for record_id in selected if record_id in records
            for claim_id in records[record_id].get("claim_ids", [])
            if isinstance(claim_id, str)
        }
        outside = sorted(substrate_claims - claim_ceiling)
        if outside:
            errors.append(
                f"section {section_id} substrate exceeds approved outline claim territory: {', '.join(outside)}"
            )
    return errors


def build_writer_section_substrate(
    product_substrate_path: Path,
    section_spec: dict[str, Any],
    outline_path: Path,
    *,
    architecture_authority: dict[str, Any] | None = None,
) -> dict[str, Any]:
    substrate = read_json(product_substrate_path)
    records = {
        item["id"]: item
        for item in substrate.get("records", [])
        if isinstance(item, dict) and _nonempty(item.get("id"))
    }
    selected = [records[item_id] for item_id in section_spec.get("historical_substrate_ids", [])]
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
        for item in selected if item.get("limitations")
    ]
    authority = architecture_authority or {
        "kind": "approved_outline",
        "outline_sha256": sha256(outline_path),
        "overlay_sha256": None,
    }
    return {
        "schema_version": SECTION_SUBSTRATE_SCHEMA_VERSION,
        "contract_version": HISTORICAL_SUBSTRATE_CONTRACT_VERSION,
        "section": section_spec.get("id"),
        "historical_territory": section_spec.get("historical_territory"),
        "historical_change": section_spec.get("historical_change"),
        "primitives": primitives,
        "boundaries": boundaries,
        "authority_binding": {
            "product_substrate_sha256": sha256(product_substrate_path),
            "outline_sha256": sha256(outline_path),
            "section_overlay_sha256": authority.get("overlay_sha256"),
            "section_binding_sha256": binding_sha256(section_spec),
        },
        "writer_contract": (
            "Historical Substrate is the primary history model. Evidence lookup is secondary: use it only "
            "to verify, sharpen or qualify a telling already chosen from this historical model."
        ),
    }


def _canonical_section(product_dir: Path, section: str) -> tuple[dict[str, Any], dict[str, Any], Path]:
    product_dir = product_dir.resolve()
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    resolved, authority = resolve_section_spec(
        product_dir, section, outline=outline, outline_path=outline_path
    )
    return resolved, authority, outline_path


def verify_writer_section_substrate(product_dir: Path, section: str) -> list[str]:
    product_dir = product_dir.resolve()
    product_substrate_path = product_dir / "01_research" / "historical-substrate.json"
    section_path = product_dir / "03_sections" / section / "historical-substrate.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    for path, label in (
        (product_substrate_path, "01_research/historical-substrate.json"),
        (claims_path, "01_research/claim-ledger.json"),
        (sources_path, "01_research/source-index.json"),
        (section_path, f"03_sections/{section}/historical-substrate.json"),
    ):
        if not path.is_file():
            return [f"missing {label}"]

    substrate = read_json(product_substrate_path)
    authority_errors = validate_historical_substrate(
        substrate,
        read_json(claims_path),
        read_json(sources_path),
        required_sections={section},
    )
    if authority_errors:
        return authority_errors
    try:
        resolved, authority, outline_path = _canonical_section(product_dir, section)
    except ValueError as exc:
        return [str(exc)]
    binding_errors = validate_section_binding(resolved, substrate)
    if binding_errors:
        return binding_errors
    expected = build_writer_section_substrate(
        product_substrate_path,
        resolved,
        outline_path,
        architecture_authority=authority,
    )
    actual = read_json(section_path)
    if actual != expected:
        return [f"section {section} historical substrate projection is stale or edited"]
    return []


def materialize_writer_section_substrate(product_dir: Path, section: str) -> Path:
    product_dir = product_dir.resolve()
    product_substrate_path = product_dir / "01_research" / "historical-substrate.json"
    claims_path = product_dir / "01_research" / "claim-ledger.json"
    sources_path = product_dir / "01_research" / "source-index.json"
    substrate = read_json(product_substrate_path)
    errors = validate_historical_substrate(
        substrate,
        read_json(claims_path),
        read_json(sources_path),
        required_sections={section},
    )
    if errors:
        raise ValueError("Invalid historical substrate: " + "; ".join(errors))
    resolved, authority, outline_path = _canonical_section(product_dir, section)
    binding_errors = validate_section_binding(resolved, substrate)
    if binding_errors:
        raise ValueError("Invalid historical substrate section binding: " + "; ".join(binding_errors))
    output = product_dir / "03_sections" / section / "historical-substrate.json"
    write_json(
        output,
        build_writer_section_substrate(
            product_substrate_path,
            resolved,
            outline_path,
            architecture_authority=authority,
        ),
    )
    return output
