"""Authoritative material evidence contract and validation rules."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


VALID_MATERIAL_KINDS = {
    "object",
    "actor",
    "place",
    "process",
    "record",
    "trace",
}

VALID_SOURCE_RELATIONS = {
    "contemporary_material",
    "contemporary_interested_account",
    "later_copy",
    "retrospective_literature",
    "cultural_tradition",
    "modern_hypothesis",
}

EPISTEMIC_LAYERS = (
    "observed",
    "functional_inference",
    "representative_reconstruction",
    "qualified_live_hypothesis",
    "prohibited_or_rejected_inference",
)

FORBIDDEN_CREATIVE_FIELDS = {
    "opening",
    "hook",
    "focal_carrier",
    "reversal",
    "climax",
    "ending",
    "emotional_beat",
    "story_role",
    "narrative_route",
    "narratability_score",
}

ALLOWED_FACTUAL_FIELDS = {
    "id",
    "kind",
    "label",
    "claim_ids",
    "source_refs",
    "source_relation",
    "actor",
    "object_or_trace",
    "documented_action",
    "explicit_sequence",
    "time",
    "place",
    "physical_description",
    "measurement",
    "spatial_relation",
    "unresolved_question",
    "later_evidence",
    "limitations",
    "representativeness",
    "provenance",
    "details",
    "material",
    "epistemic_layers",
}


def validate_material_record(
    item: Any,
    allowed_claim_ids: set[str] | None = None,
    allowed_source_ids: set[str] | None = None,
    require_source_relation: bool = False,
    prefix: str = "material",
    require_epistemic_layers: bool = False,
) -> list[str]:
    """Validate a single material record against the evidence contract."""
    if not isinstance(item, dict):
        return [f"{prefix} entries must be objects"]

    errors: list[str] = []
    material_id = item.get("id")
    label = f"{prefix} {material_id or '?'}"

    if not isinstance(material_id, str) or not material_id.strip():
        errors.append(f"{prefix} entry missing required string ID")
        material_id = "?"

    for key in item:
        if key in FORBIDDEN_CREATIVE_FIELDS:
            errors.append(f"{label} contains forbidden creative-authority field: {key}")

    kind = item.get("kind")
    if kind is not None and kind not in VALID_MATERIAL_KINDS:
        errors.append(f"{label} invalid kind: {kind}")

    label_text = item.get("label")
    if label_text is not None and (not isinstance(label_text, str) or not label_text.strip()):
        errors.append(f"{label} label must be a non-empty string")

    refs = item.get("source_refs")
    if refs is not None:
        if not isinstance(refs, list):
            errors.append(f"{label} source_refs must be a list")
        else:
            for ref in refs:
                if not isinstance(ref, dict):
                    errors.append(f"{label} source_refs entry must be an object")
                    continue
                source_id = ref.get("source_id")
                if not isinstance(source_id, str) or not source_id.strip():
                    errors.append(f"{label} source_ref missing string source_id")
                elif allowed_source_ids is not None and source_id not in allowed_source_ids:
                    errors.append(f"{label} references unknown source: {source_id}")
                locators = ref.get("locators")
                if locators is not None:
                    if not isinstance(locators, list) or not all(isinstance(loc, str) and loc.strip() for loc in locators):
                        errors.append(f"{label} source_ref locators must be strings")

    claims = item.get("claim_ids")
    if claims is not None:
        if not isinstance(claims, list):
            errors.append(f"{label} claim_ids must be a list")
        else:
            for claim_id in claims:
                if not isinstance(claim_id, str) or not claim_id.strip():
                    errors.append(f"{label} contains invalid claim ID")
                elif allowed_claim_ids is not None and claim_id not in allowed_claim_ids:
                    errors.append(f"{label} references unknown claim: {claim_id}")

    relation = item.get("source_relation")
    if relation is not None:
        if relation not in VALID_SOURCE_RELATIONS:
            errors.append(f"{label} invalid source_relation: {relation}")
    elif require_source_relation:
        errors.append(f"{label} missing required source_relation")

    limitations = item.get("limitations")
    if limitations is not None and (
        not isinstance(limitations, list)
        or not all(isinstance(value, str) and value.strip() for value in limitations)
    ):
        errors.append(f"{label} limitations must be a list of strings")

    seq = item.get("explicit_sequence")
    if seq is not None and (
        not isinstance(seq, list)
        or not all(isinstance(step, str) and step.strip() for step in seq)
    ):
        errors.append(f"{label} explicit_sequence must be a list of strings")

    layers = item.get("epistemic_layers")
    if layers is None and not require_epistemic_layers:
        pass
    elif not isinstance(layers, dict):
        errors.append(f"{label} missing required epistemic_layers object")
    else:
        unknown_layers = sorted(set(layers) - set(EPISTEMIC_LAYERS))
        if unknown_layers:
            errors.append(f"{label} has unknown epistemic layers: {', '.join(unknown_layers)}")
        for layer in EPISTEMIC_LAYERS:
            entries = layers.get(layer)
            if not isinstance(entries, list):
                errors.append(f"{label} epistemic layer {layer} must be a list")
                continue
            for index, entry in enumerate(entries, 1):
                if not isinstance(entry, dict) or not isinstance(entry.get("statement"), str) or not entry["statement"].strip():
                    errors.append(f"{label} {layer} entry #{index} requires a statement")
                    continue
                if layer != "observed" and (
                    not isinstance(entry.get("qualification"), str) or not entry["qualification"].strip()
                ):
                    errors.append(f"{label} {layer} entry #{index} requires qualification")
        if not layers.get("observed"):
            errors.append(f"{label} requires at least one observed material statement")

        reconstruction_text = " ".join(
            str(entry.get("statement", "")).strip().lower()
            for entry in layers.get("representative_reconstruction", [])
            if isinstance(entry, dict)
        )
        documented = item.get("documented_action")
        if isinstance(documented, str) and documented.strip() and documented.strip().lower() in reconstruction_text:
            errors.append(f"{label} documented_action duplicates representative reconstruction")
        if require_epistemic_layers and item.get("explicit_sequence"):
            errors.append(f"{label} schema-v2 explicit_sequence must be classified inside epistemic_layers")

    if isinstance(item.get("representativeness"), str) and item["representativeness"].strip():
        represented = []
        if isinstance(layers, dict):
            represented = (
                (layers.get("functional_inference") if isinstance(layers.get("functional_inference"), list) else [])
                + (layers.get("qualified_live_hypothesis") if isinstance(layers.get("qualified_live_hypothesis"), list) else [])
            )
        if not represented:
            errors.append(f"{label} representativeness must be qualified in an inference layer")

    return errors


def validate_materials_collection(
    materials: Any,
    allowed_claim_ids: set[str] | None = None,
    allowed_source_ids: set[str] | None = None,
    require_source_relation: bool = False,
    prefix: str = "material",
    require_epistemic_layers: bool = False,
) -> list[str]:
    """Validate a list of material records."""
    if not isinstance(materials, list):
        return [f"{prefix} list must be an array"]

    errors: list[str] = []
    seen_ids: set[str] = set()

    for item in materials:
        record_errors = validate_material_record(
            item,
            allowed_claim_ids=allowed_claim_ids,
            allowed_source_ids=allowed_source_ids,
            require_source_relation=require_source_relation,
            prefix=prefix,
            require_epistemic_layers=require_epistemic_layers,
        )
        errors.extend(record_errors)
        if isinstance(item, dict):
            mid = item.get("id")
            if isinstance(mid, str) and mid.strip():
                if mid in seen_ids:
                    errors.append(f"duplicate {prefix} ID: {mid}")
                seen_ids.add(mid)

    return errors


def validate_materials_file(
    path: Path,
    allowed_claim_ids: set[str] | None = None,
    allowed_source_ids: set[str] | None = None,
    require_source_relation: bool = False,
    prefix: str = "material",
) -> list[str]:
    """Validate a materials.json or material-ledger.json file."""
    if not path.is_file():
        return [f"material file does not exist: {path}"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        return [f"invalid material JSON file {path}: {exc}"]

    if isinstance(data, list):
        materials = data
    elif isinstance(data, dict):
        materials = data.get("materials", [])
    else:
        return [f"material file root must be an object or array: {path}"]

    require_layers = isinstance(data, dict) and int(data.get("schema_version", 1)) >= 2
    return validate_materials_collection(
        materials,
        allowed_claim_ids=allowed_claim_ids,
        allowed_source_ids=allowed_source_ids,
        require_source_relation=require_source_relation,
        prefix=prefix,
        require_epistemic_layers=require_layers,
    )
