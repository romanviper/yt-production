#!/usr/bin/env python3
"""Contract and deterministic evidence handoff for one section's story design."""

from __future__ import annotations

from copy import deepcopy
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, word_count, write_json
    from scripts.outline_contract import MAX_SECTION_WORDS, valid_word_range
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import read_json, sha256, word_count, write_json
    from outline_contract import MAX_SECTION_WORDS, valid_word_range


ROLE_NAMES = ("narrated", "support", "guardrail", "omit")
STORY_PLAN_SCHEMA_VERSION = 2
BEAT_FUNCTION_PATTERN = r"[a-z][a-z0-9_]{0,31}"


def empty_story_plan(section: str, target_words: dict[str, int] | None = None) -> dict[str, Any]:
    return {
        "schema_version": STORY_PLAN_SCHEMA_VERSION,
        "section": section,
        "status": "not_started",
        "governing_idea": "",
        "audience_question": "",
        "audience_payoff": "",
        "structure_shape": "",
        "word_budget": {
            "recommended": dict(target_words or {"min": 0, "max": 0}),
            "rationale": "",
        },
        "evidence_roles": {name: [] for name in ROLE_NAMES},
        "claim_use": {},
        "beats": [],
        "terminology": [],
        "opening_move": "",
        "ending_move": "",
        "comprehension_test": "",
    }


def normalize_story_plan(plan: dict[str, Any], current_target_words: dict[str, int] | None = None) -> dict[str, Any]:
    """Read an already-approved v1 plan through the v2 contract without changing its hash."""

    if plan.get("schema_version") != 1:
        return plan
    value = deepcopy(plan)
    value["schema_version"] = STORY_PLAN_SCHEMA_VERSION
    value.setdefault(
        "structure_shape",
        "Legacy approved beat sequence retained until explicit human feedback reopens story design.",
    )
    budget = current_target_words if valid_word_range(current_target_words) else {"min": 1, "max": 1}
    value.setdefault(
        "word_budget",
        {
            "recommended": deepcopy(budget),
            "rationale": "Legacy approved section budget retained until an explicit story-design revision.",
        },
    )
    return value


def validate_story_plan(
    plan: dict[str, Any],
    evidence_claim_ids: set[str],
    current_target_words: dict[str, int] | None = None,
    require_current: bool = False,
) -> list[str]:
    errors: list[str] = []
    schema_version = plan.get("schema_version")
    if schema_version == 1 and require_current:
        errors.append(f"story plan schema_version must be {STORY_PLAN_SCHEMA_VERSION} for new or revised output")
    if schema_version not in {1, STORY_PLAN_SCHEMA_VERSION}:
        errors.append(f"story plan schema_version must be {STORY_PLAN_SCHEMA_VERSION}")
    plan = normalize_story_plan(plan, current_target_words)
    if not isinstance(plan.get("section"), str) or not plan["section"]:
        errors.append("story plan section is required")
    if plan.get("status") not in {"draft", "approved"}:
        errors.append("story plan status must be draft or approved")

    for field, limit in [
        ("governing_idea", 45),
        ("audience_question", 35),
        ("audience_payoff", 45),
        ("structure_shape", 65),
        ("opening_move", 60),
        ("ending_move", 60),
        ("comprehension_test", 45),
    ]:
        value = plan.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"story plan {field} is required")
        elif word_count(value) > limit:
            errors.append(f"story plan {field} exceeds {limit} words")

    word_budget = plan.get("word_budget")
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
    elif word_count(rationale) > 60:
        errors.append("story plan word_budget.rationale exceeds 60 words")
    if current_target_words is not None and not valid_word_range(current_target_words):
        errors.append("section current target_words is invalid")

    roles = plan.get("evidence_roles")
    assigned: list[str] = []
    if not isinstance(roles, dict):
        errors.append("story plan evidence_roles must be an object")
        roles = {}
    for name in ROLE_NAMES:
        values = roles.get(name)
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            errors.append(f"story plan evidence_roles.{name} must be a list of claim IDs")
            continue
        assigned.extend(values)
    narrated = roles.get("narrated", []) if isinstance(roles.get("narrated"), list) else []
    support = roles.get("support", []) if isinstance(roles.get("support"), list) else []
    if not 1 <= len(narrated) <= 5:
        errors.append("story plan must narrate one to five claims")
    if len(support) > 5:
        errors.append("story plan support role may contain at most five claims")
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

    claim_use = plan.get("claim_use")
    expected_use = set(narrated + support)
    if not isinstance(claim_use, dict):
        errors.append("story plan claim_use must map narrated/support claim IDs to reasons")
        claim_use = {}
    if set(claim_use) != expected_use:
        missing_use = sorted(expected_use - set(claim_use))
        extra_use = sorted(set(claim_use) - expected_use)
        if missing_use:
            errors.append("story plan claim_use missing: " + ", ".join(missing_use))
        if extra_use:
            errors.append("story plan claim_use contains non-narrative claims: " + ", ".join(extra_use))
    for claim_id, reason in claim_use.items():
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"story plan claim_use.{claim_id} requires a reason")
        elif word_count(reason) > 35:
            errors.append(f"story plan claim_use.{claim_id} exceeds 35 words")

    beats = plan.get("beats")
    referenced: set[str] = set()
    functions: list[str] = []
    if not isinstance(beats, list) or not 2 <= len(beats) <= 12:
        errors.append("story plan requires two to twelve beats")
        beats = []
    narrative_ids = set(narrated + support)
    for index, beat in enumerate(beats):
        if not isinstance(beat, dict):
            errors.append(f"story beat #{index + 1} must be an object")
            continue
        expected_id = f"B{index + 1:02d}"
        if beat.get("id") != expected_id:
            errors.append(f"story beat #{index + 1} id must be {expected_id}")
        function = beat.get("function")
        if not isinstance(function, str) or not re.fullmatch(BEAT_FUNCTION_PATTERN, function):
            errors.append(f"story beat {expected_id} has invalid function: {function!r}")
        else:
            functions.append(function)
        purpose = beat.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            errors.append(f"story beat {expected_id} purpose is required")
        elif word_count(purpose) > 45:
            errors.append(f"story beat {expected_id} purpose exceeds 45 words")
        audience_change = beat.get("audience_change")
        if not isinstance(audience_change, str) or not audience_change.strip():
            errors.append(f"story beat {expected_id} audience_change is required")
        elif word_count(audience_change) > 35:
            errors.append(f"story beat {expected_id} audience_change exceeds 35 words")
        claim_ids = beat.get("claim_ids", [])
        if not isinstance(claim_ids, list) or not all(isinstance(item, str) for item in claim_ids):
            errors.append(f"story beat {expected_id} claim_ids must be a list")
            continue
        invalid = [item for item in claim_ids if item not in narrative_ids]
        if invalid:
            errors.append(f"story beat {expected_id} uses non-narrative claims: {', '.join(invalid)}")
        referenced.update(claim_ids)
    if "payoff" not in functions:
        errors.append("story plan requires a payoff beat")
    unreferenced = [claim_id for claim_id in narrated if claim_id not in referenced]
    if unreferenced:
        errors.append("narrated claims must appear in at least one beat: " + ", ".join(unreferenced))

    terminology = plan.get("terminology")
    if not isinstance(terminology, list) or len(terminology) > 5:
        errors.append("story plan terminology must be a list of at most five items")
        terminology = []
    for index, item in enumerate(terminology):
        if not isinstance(item, dict) or not str(item.get("term", "")).strip() or not str(item.get("plain_language", "")).strip():
            errors.append(f"story plan terminology item #{index + 1} requires term and plain_language")
    return errors


def build_narration_pack(product_dir: Path, section: str) -> dict[str, Any]:
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
    roles = plan["evidence_roles"]
    prose_claim_ids = roles["narrated"] + roles["support"]
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
        "schema_version": 1,
        "section": section,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "story_plan_sha256": sha256(plan_path),
        "evidence_pack_sha256": sha256(evidence_path),
        "narrated_claims": [claims[claim_id] for claim_id in roles["narrated"]],
        "support_claims": [claims[claim_id] for claim_id in roles["support"]],
        "claim_use": plan["claim_use"],
        "guardrails": [
            {
                "id": claim_id,
                "constraint": claims[claim_id].get("narrative_implication") or claims[claim_id].get("statement"),
                "counterevidence": claims[claim_id].get("counterevidence", ""),
            }
            for claim_id in roles["guardrail"]
        ],
        "omitted_claim_ids": roles["omit"],
        "sources": [sources[source_id] for source_id in sorted(selected_sources)],
        "rule": (
            "This pack is a ceiling, not a checklist. Narrated claims may appear only where assigned to a story beat. "
            "Support claims are optional precision. Guardrails constrain wording and are not exposition. Omitted claims stay out."
        ),
    }
    write_json(root / "narration-pack.json", pack)
    return pack


def verify_narration_pack(product_dir: Path, section: str) -> list[str]:
    root = product_dir.resolve() / "03_sections" / section
    try:
        plan = read_json(root / "story-plan.json")
        pack = read_json(root / "narration-pack.json")
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
    return errors
