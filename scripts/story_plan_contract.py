#!/usr/bin/env python3
"""Legacy story-plan compatibility plus deterministic narration handoff."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, word_count, write_json
    from scripts.outline_contract import MAX_SECTION_WORDS, valid_word_range
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import read_json, sha256, word_count, write_json
    from outline_contract import MAX_SECTION_WORDS, valid_word_range


STORY_PLAN_SCHEMA_VERSION = 3
MATERIAL_AWARE_NARRATION_SCHEMA_VERSION = 3
ROLE_NAMES = ("core", "optional", "guardrail", "exclude")
LEGACY_ROLE_MAP = {
    "narrated": "core",
    "support": "optional",
    "guardrail": "guardrail",
    "omit": "exclude",
}


def empty_story_plan(section: str, target_words: dict[str, int] | None = None) -> dict[str, Any]:
    return {
        "schema_version": STORY_PLAN_SCHEMA_VERSION,
        "section": section,
        "status": "not_started",
        "audience_shift": "",
        "story_strategy": "",
        "word_budget": {
            "recommended": dict(target_words or {"min": 0, "max": 0}),
            "rationale": "",
        },
        "evidence_roles": {name: [] for name in ROLE_NAMES},
        "design_risks": [],
    }


def normalize_story_plan(
    plan: dict[str, Any],
    current_target_words: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Expose approved v1/v2 plans through the lean v3 interface without rewriting them."""

    if plan.get("schema_version") == STORY_PLAN_SCHEMA_VERSION:
        return plan
    if plan.get("schema_version") not in {1, 2}:
        return plan

    value = deepcopy(plan)
    budget = value.get("word_budget")
    if not isinstance(budget, dict):
        target = current_target_words if valid_word_range(current_target_words) else {"min": 1, "max": 1}
        budget = {
            "recommended": deepcopy(target),
            "rationale": "Legacy approved range retained until story design is explicitly reopened.",
        }

    legacy_roles = value.get("evidence_roles", {})
    roles = {
        current: list(legacy_roles.get(legacy, []))
        if isinstance(legacy_roles.get(legacy, []), list)
        else []
        for legacy, current in LEGACY_ROLE_MAP.items()
    }
    strategy = str(value.get("structure_shape") or "").strip()
    beats = value.get("beats")
    if not strategy and isinstance(beats, list):
        strategy = " ".join(
            str(item.get("purpose", "")).strip()
            for item in beats
            if isinstance(item, dict) and str(item.get("purpose", "")).strip()
        )
    if not strategy:
        strategy = "Legacy approved design retained until explicit human feedback reopens it."

    return {
        "schema_version": STORY_PLAN_SCHEMA_VERSION,
        "section": value.get("section"),
        "status": value.get("status"),
        "audience_shift": str(value.get("audience_payoff") or value.get("governing_idea") or "").strip(),
        "story_strategy": strategy,
        "word_budget": budget,
        "evidence_roles": roles,
        "design_risks": [],
        **{
            key: value[key]
            for key in ["approved_by", "approved_at"]
            if key in value
        },
    }


def validate_story_plan(
    plan: dict[str, Any],
    evidence_claim_ids: set[str],
    current_target_words: dict[str, int] | None = None,
    require_current: bool = False,
) -> list[str]:
    """Legacy compatibility validator. New material-aware sections do not depend on this artifact."""

    errors: list[str] = []
    schema_version = plan.get("schema_version")
    if schema_version in {1, 2} and require_current:
        errors.append(f"story plan schema_version must be {STORY_PLAN_SCHEMA_VERSION} for new or revised output")
    if schema_version not in {1, 2, STORY_PLAN_SCHEMA_VERSION}:
        errors.append(f"story plan schema_version must be {STORY_PLAN_SCHEMA_VERSION}")
        return errors

    value = normalize_story_plan(plan, current_target_words)
    if not isinstance(value.get("section"), str) or not value["section"]:
        errors.append("story plan section is required")
    if value.get("status") not in {"draft", "approved"}:
        errors.append("story plan status must be draft or approved")

    audience_shift = value.get("audience_shift")
    if not isinstance(audience_shift, str) or not audience_shift.strip():
        errors.append("story plan audience_shift is required")
    elif word_count(audience_shift) > 80:
        errors.append("story plan audience_shift exceeds 80 words")

    strategy = value.get("story_strategy")
    if not isinstance(strategy, str) or not strategy.strip():
        errors.append("story plan story_strategy is required")
    elif word_count(strategy) > 220:
        errors.append("story plan story_strategy exceeds 220 words")

    word_budget = value.get("word_budget")
    if not isinstance(word_budget, dict):
        errors.append("story plan word_budget must be an object")
        word_budget = {}
    recommended = word_budget.get("recommended")
    if not valid_word_range(recommended):
        errors.append("story plan word_budget.recommended is invalid")
    elif recommended["max"] > MAX_SECTION_WORDS:
        errors.append(f"story plan word budget exceeds the {MAX_SECTION_WORDS}-word production-unit cap")
    rationale = word_budget.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append("story plan word_budget.rationale is required")
    elif word_count(rationale) > 80:
        errors.append("story plan word_budget.rationale exceeds 80 words")
    if current_target_words is not None and not valid_word_range(current_target_words):
        errors.append("section current target_words is invalid")

    roles = value.get("evidence_roles")
    assigned: list[str] = []
    if not isinstance(roles, dict):
        errors.append("story plan evidence_roles must be an object")
        roles = {}
    for name in ROLE_NAMES:
        claim_ids = roles.get(name)
        if not isinstance(claim_ids, list) or not all(isinstance(item, str) and item for item in claim_ids):
            errors.append(f"story plan evidence_roles.{name} must be a list of claim IDs")
            continue
        assigned.extend(claim_ids)

    selected = []
    for name in ("core", "optional"):
        if isinstance(roles.get(name), list):
            selected.extend(roles[name])
    if evidence_claim_ids and not selected:
        errors.append("story plan must select at least one core or optional claim")
    if len(assigned) != len(set(assigned)):
        errors.append("each evidence claim must have exactly one story role")
    assigned_set = set(assigned)
    if assigned_set != evidence_claim_ids:
        missing = sorted(evidence_claim_ids - assigned_set)
        unknown = sorted(assigned_set - evidence_claim_ids)
        if missing:
            errors.append("story plan leaves evidence claims unclassified: " + ", ".join(missing))
        if unknown:
            errors.append("story plan classifies unknown claims: " + ", ".join(unknown))

    risks = value.get("design_risks", [])
    if not isinstance(risks, list) or len(risks) > 8 or not all(isinstance(item, str) and item.strip() for item in risks):
        errors.append("story plan design_risks must be a list of at most eight non-empty strings")
    return errors


def _compact_claim(claim: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "id",
        "statement",
        "type",
        "confidence",
        "status",
        "counterevidence",
        "narrative_implication",
        "sources",
    ]
    return {key: claim[key] for key in keys if key in claim and claim[key] not in (None, "", [])}


def _compact_source(source: dict[str, Any]) -> dict[str, Any]:
    keys = ["id", "title", "author", "year", "locators"]
    return {key: source[key] for key in keys if key in source and source[key] not in (None, "", [])}


def _outline_section(outline: dict[str, Any], section: str) -> dict[str, Any]:
    matches = [item for item in outline.get("sections", []) if isinstance(item, dict) and item.get("id") == section]
    if len(matches) != 1:
        raise ValueError(f"Outline must contain exactly one section {section}.")
    return matches[0]


def _is_material_aware(outline: dict[str, Any]) -> bool:
    return outline.get("script_architecture", {}).get("story_material_contract_version") == 1


def _build_material_aware_narration_pack(product_dir: Path, section: str) -> dict[str, Any]:
    root = product_dir.resolve() / "03_sections" / section
    outline_path = product_dir / "02_outline" / "outline.json"
    outline = read_json(outline_path)
    if outline.get("status") != "approved":
        raise ValueError("Material-aware narration pack requires a human-approved outline.")
    section_spec = _outline_section(outline, section)
    state = read_json(root / "section.json")
    evidence_path = root / "evidence-pack.json"
    material_path = root / "material-pack.json"
    brief_path = root / "brief.md"
    evidence = read_json(evidence_path)
    material = read_json(material_path)

    cycle_id = outline.get("cycle_id")
    if state.get("cycle_id") != cycle_id:
        raise ValueError(f"Section {section} cycle does not match outline cycle {cycle_id}.")
    if evidence.get("cycle_id") != cycle_id or material.get("cycle_id") != cycle_id:
        raise ValueError(f"Section {section} handoff artifacts do not match outline cycle {cycle_id}.")

    claims = evidence.get("claims", [])
    claim_ids = [item.get("id") for item in claims if isinstance(item, dict) and item.get("id")]
    expected_claim_ids = list(section_spec.get("claim_ids", []))
    if claim_ids != expected_claim_ids:
        raise ValueError("Evidence pack claim order/content differs from approved outline allowance.")

    material_ids = [item.get("id") for item in material.get("materials", []) if isinstance(item, dict) and item.get("id")]
    expected_material_ids = list(section_spec.get("material_ids", []))
    if material_ids != expected_material_ids:
        raise ValueError("Material pack differs from approved outline material selection.")

    sources = {item["id"]: item for item in evidence.get("sources", []) if isinstance(item, dict) and item.get("id")}
    selected_sources = {
        source_id
        for claim in claims
        for source_id in claim.get("sources", [])
        if isinstance(source_id, str)
    }
    missing_sources = selected_sources - sources.keys()
    if missing_sources:
        raise ValueError("Narration claims reference missing sources: " + ", ".join(sorted(missing_sources)))

    qualifications = []
    for claim in claims:
        if claim.get("status") == "qualified" or claim.get("counterevidence"):
            qualifications.append(
                {
                    "id": claim.get("id"),
                    "constraint": claim.get("narrative_implication") or claim.get("statement"),
                    "counterevidence": claim.get("counterevidence", ""),
                }
            )

    guardrails = []
    non_goal = section_spec.get("non_goal")
    if isinstance(non_goal, str) and non_goal.strip():
        guardrails.append({"source": "outline.non_goal", "constraint": non_goal.strip()})
    for item in material.get("materials", []):
        for limitation in item.get("limitations", []):
            guardrails.append(
                {
                    "source": item.get("id"),
                    "constraint": limitation,
                }
            )

    pack = {
        "schema_version": MATERIAL_AWARE_NARRATION_SCHEMA_VERSION,
        "section": section,
        "cycle_id": cycle_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "outline_sha256": sha256(outline_path),
        "brief_sha256": sha256(brief_path),
        "evidence_pack_sha256": sha256(evidence_path),
        "material_pack_sha256": sha256(material_path),
        "permitted_claims": [_compact_claim(claim) for claim in claims],
        "qualifications": qualifications,
        "guardrails": guardrails,
        "excluded_claim_ids": [],
        "exclusion_rule": "Any substantive historical claim not listed in permitted_claims is excluded by default.",
        "source_refs": [_compact_source(sources[source_id]) for source_id in sorted(selected_sources)],
        "writer_contract": (
            "Story material is the primary source for narrative movement. Claims define the evidence ceiling. "
            "Qualifications and guardrails constrain wording; they are silent unless needed to prevent a material misconception."
        ),
    }
    write_json(root / "narration-pack.json", pack)
    return pack


def _build_legacy_narration_pack(product_dir: Path, section: str) -> dict[str, Any]:
    root = product_dir.resolve() / "03_sections" / section
    plan_path = root / "story-plan.json"
    evidence_path = root / "evidence-pack.json"
    plan = read_json(plan_path)
    evidence = read_json(evidence_path)
    state = read_json(root / "section.json")
    claims = {item["id"]: item for item in evidence.get("claims", [])}
    errors = validate_story_plan(plan, set(claims), state.get("target_words"))
    if errors:
        raise ValueError("Invalid story plan: " + "; ".join(errors))
    if plan.get("status") != "approved":
        raise ValueError("Story plan must be human-approved before building narration pack.")

    normalized = normalize_story_plan(plan, state.get("target_words"))
    roles = normalized["evidence_roles"]
    prose_claim_ids = roles["core"] + roles["optional"]
    selected_sources = {
        source_id
        for claim_id in prose_claim_ids
        for source_id in claims[claim_id].get("sources", [])
    }
    sources = {item["id"]: item for item in evidence.get("sources", [])}
    missing_sources = selected_sources - sources.keys()
    if missing_sources:
        raise ValueError("Narration claims reference missing sources: " + ", ".join(sorted(missing_sources)))

    pack = {
        "schema_version": 2,
        "section": section,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "story_plan_sha256": sha256(plan_path),
        "evidence_pack_sha256": sha256(evidence_path),
        "core_claims": [_compact_claim(claims[claim_id]) for claim_id in roles["core"]],
        "optional_claims": [_compact_claim(claims[claim_id]) for claim_id in roles["optional"]],
        "guardrails": [
            {
                "id": claim_id,
                "constraint": claims[claim_id].get("narrative_implication") or claims[claim_id].get("statement"),
                "counterevidence": claims[claim_id].get("counterevidence", ""),
            }
            for claim_id in roles["guardrail"]
        ],
        "excluded_claim_ids": roles["exclude"],
        "source_refs": [_compact_source(sources[source_id]) for source_id in sorted(selected_sources)],
        "writer_contract": (
            "Core claims are anchors, not mandatory paragraphs. Optional claims appear only when needed. "
            "Guardrails constrain wording without becoming exposition. Excluded claims stay out."
        ),
    }
    write_json(root / "narration-pack.json", pack)
    return pack


def build_narration_pack(product_dir: Path, section: str) -> dict[str, Any]:
    outline = read_json(product_dir.resolve() / "02_outline" / "outline.json")
    if _is_material_aware(outline):
        return _build_material_aware_narration_pack(product_dir, section)
    return _build_legacy_narration_pack(product_dir, section)


def verify_narration_pack(product_dir: Path, section: str) -> list[str]:
    root = product_dir.resolve() / "03_sections" / section
    try:
        pack = read_json(root / "narration-pack.json")
    except (FileNotFoundError, ValueError) as exc:
        return [f"invalid narration pack: {exc}"]

    if pack.get("schema_version") == MATERIAL_AWARE_NARRATION_SCHEMA_VERSION:
        errors: list[str] = []
        try:
            outline_path = product_dir.resolve() / "02_outline" / "outline.json"
            outline = read_json(outline_path)
            state = read_json(root / "section.json")
            evidence_path = root / "evidence-pack.json"
            material_path = root / "material-pack.json"
            brief_path = root / "brief.md"
            evidence = read_json(evidence_path)
            material = read_json(material_path)
            section_spec = _outline_section(outline, section)
        except (FileNotFoundError, ValueError) as exc:
            return [f"invalid material-aware narration pack: {exc}"]

        cycle_id = outline.get("cycle_id")
        if outline.get("status") != "approved":
            errors.append("current outline is not human-approved")
        if not _is_material_aware(outline):
            errors.append("material-aware narration pack requires story_material_contract_version=1")
        for label, value in [
            ("section state", state.get("cycle_id")),
            ("evidence pack", evidence.get("cycle_id")),
            ("material pack", material.get("cycle_id")),
            ("narration pack", pack.get("cycle_id")),
        ]:
            if value != cycle_id:
                errors.append(f"{label} cycle {value!r} does not match outline cycle {cycle_id!r}")

        if pack.get("outline_sha256") != sha256(outline_path):
            errors.append("narration pack is stale relative to outline")
        if pack.get("brief_sha256") != sha256(brief_path):
            errors.append("narration pack is stale relative to section brief")
        if pack.get("evidence_pack_sha256") != sha256(evidence_path):
            errors.append("narration pack is stale relative to evidence pack")
        if pack.get("material_pack_sha256") != sha256(material_path):
            errors.append("narration pack is stale relative to material pack")
        if material.get("outline_sha256") != sha256(outline_path):
            errors.append("material pack is stale relative to outline")
        if evidence.get("outline_sha256") != sha256(outline_path):
            errors.append("evidence pack is stale relative to outline")

        expected_claim_ids = list(section_spec.get("claim_ids", []))
        evidence_claim_ids = [item.get("id") for item in evidence.get("claims", []) if isinstance(item, dict)]
        permitted_ids = [item.get("id") for item in pack.get("permitted_claims", []) if isinstance(item, dict)]
        if evidence_claim_ids != expected_claim_ids or permitted_ids != expected_claim_ids:
            errors.append("section claim allowance differs from approved outline")

        expected_material_ids = list(section_spec.get("material_ids", []))
        material_ids = [item.get("id") for item in material.get("materials", []) if isinstance(item, dict)]
        if material_ids != expected_material_ids:
            errors.append("section material selection differs from approved outline")
        return errors

    try:
        plan = read_json(root / "story-plan.json")
        evidence = read_json(root / "evidence-pack.json")
        state = read_json(root / "section.json")
    except (FileNotFoundError, ValueError) as exc:
        return [f"invalid narration pack: {exc}"]

    errors: list[str] = []
    evidence_claim_ids = {item.get("id") for item in evidence.get("claims", []) if item.get("id")}
    errors.extend(validate_story_plan(plan, evidence_claim_ids, state.get("target_words")))
    if plan.get("status") != "approved":
        errors.append("story plan is not human-approved")
    if pack.get("story_plan_sha256") != sha256(root / "story-plan.json"):
        errors.append("narration pack is stale relative to story plan")
    if pack.get("evidence_pack_sha256") != sha256(root / "evidence-pack.json"):
        errors.append("narration pack is stale relative to evidence pack")

    pack_version = pack.get("schema_version")
    if pack_version not in {1, 2}:
        errors.append("unsupported narration pack schema")
    if plan.get("schema_version") == STORY_PLAN_SCHEMA_VERSION and pack_version != 2:
        errors.append("current story plan requires compact narration pack schema 2")
    if pack_version == 2:
        normalized = normalize_story_plan(plan, state.get("target_words"))
        roles = normalized["evidence_roles"]
        core_ids = [item.get("id") for item in pack.get("core_claims", [])]
        optional_ids = [item.get("id") for item in pack.get("optional_claims", [])]
        if core_ids != roles["core"]:
            errors.append("narration pack core claims differ from story plan")
        if optional_ids != roles["optional"]:
            errors.append("narration pack optional claims differ from story plan")
        if pack.get("excluded_claim_ids") != roles["exclude"]:
            errors.append("narration pack exclusions differ from story plan")
    return errors
