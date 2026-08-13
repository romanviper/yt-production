#!/usr/bin/env python3
"""Contract and deterministic evidence handoff for one section's story design."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, word_count, write_json
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import read_json, sha256, word_count, write_json


ROLE_NAMES = ("narrated", "support", "guardrail", "omit")
BEAT_FUNCTIONS = {"hook", "orientation", "tension", "reveal", "consequence", "payoff", "bridge"}


def empty_story_plan(section: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "section": section,
        "status": "not_started",
        "governing_idea": "",
        "audience_question": "",
        "audience_payoff": "",
        "evidence_roles": {name: [] for name in ROLE_NAMES},
        "claim_use": {},
        "beats": [],
        "terminology": [],
        "opening_move": "",
        "ending_move": "",
        "comprehension_test": "",
    }


def validate_story_plan(plan: dict[str, Any], evidence_claim_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != 1:
        errors.append("story plan schema_version must be 1")
    if not isinstance(plan.get("section"), str) or not plan["section"]:
        errors.append("story plan section is required")
    if plan.get("status") not in {"draft", "approved"}:
        errors.append("story plan status must be draft or approved")

    for field, limit in [
        ("governing_idea", 45),
        ("audience_question", 35),
        ("audience_payoff", 45),
        ("opening_move", 60),
        ("ending_move", 60),
        ("comprehension_test", 45),
    ]:
        value = plan.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"story plan {field} is required")
        elif word_count(value) > limit:
            errors.append(f"story plan {field} exceeds {limit} words")

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
    if not isinstance(beats, list) or not 4 <= len(beats) <= 8:
        errors.append("story plan requires four to eight beats")
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
        if function not in BEAT_FUNCTIONS:
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
    for required_function in ["tension", "payoff", "bridge"]:
        if required_function not in functions:
            errors.append(f"story plan requires a {required_function} beat")
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
    claims = {item["id"]: item for item in evidence.get("claims", [])}
    errors = validate_story_plan(plan, set(claims))
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
    except (FileNotFoundError, ValueError) as exc:
        return [f"invalid narration pack: {exc}"]
    errors: list[str] = []
    if plan.get("status") != "approved":
        errors.append("story plan is not human-approved")
    if pack.get("story_plan_sha256") != sha256(root / "story-plan.json"):
        errors.append("narration pack is stale relative to story plan")
    if pack.get("evidence_pack_sha256") != sha256(root / "evidence-pack.json"):
        errors.append("narration pack is stale relative to evidence pack")
    return errors
