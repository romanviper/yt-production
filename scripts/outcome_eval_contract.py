#!/usr/bin/env python3
"""Minimal contract for post-draft outcome evaluation."""

from __future__ import annotations

import json

try:
    from scripts.common import word_count
except ModuleNotFoundError:
    from common import word_count


VERDICTS = {"pass", "changes_requested", "blocked"}
BASE_HEADINGS = ["## Outcome judgment", "## Issues", "## Routing"]
MISSION_OUTCOME_HEADINGS = ["## Mission answerability", "## Historical progression"]
GATE_START = "<!-- production-gate:start -->"
GATE_END = "<!-- production-gate:end -->"
HARD_GATES = [
    "evidence_integrity",
    "mission_and_exit",
    "adjacent_section_boundary",
    "one_hearing_narration",
]
STORY_DIMENSIONS = [
    "hook_and_audience_promise",
    "historical_progression",
    "causal_clarity",
    "concrete_specificity",
    "narrative_momentum_and_stakes",
    "supported_human_work_orientation",
    "explanatory_economy",
    "spoken_rhythm_and_clarity",
    "ending_payoff_and_transition",
]
GATE_STATUSES = {"pass", "fail", "blocked"}
EVIDENCE_SCOPES = {"full", "limited"}


def review_verdict(text: str) -> str | None:
    for line in text.splitlines():
        if line.lower().startswith("verdict:"):
            value = line.split(":", 1)[1].strip().lower()
            return value or None
    return None


def _heading_body(text: str, heading: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return ""
    body: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body).strip()


def production_gate_data(text: str) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    if text.count(GATE_START) != 1 or text.count(GATE_END) != 1:
        return None, ["outcome review requires exactly one production gate marker pair"]
    start = text.index(GATE_START) + len(GATE_START)
    end = text.index(GATE_END)
    if end <= start:
        return None, ["outcome review production gate markers are out of order"]
    payload = text[start:end].strip()
    if payload.startswith("```json") and payload.endswith("```"):
        payload = payload[len("```json") : -len("```")].strip()
    try:
        gate = json.loads(payload)
    except json.JSONDecodeError as exc:
        return None, [f"outcome review production gate is invalid JSON: {exc}"]
    if not isinstance(gate, dict):
        return None, ["outcome review production gate must be a JSON object"]
    if gate.get("schema_version") != 1:
        errors.append("outcome review production gate schema_version must be 1")
    hard = gate.get("hard_gates")
    dimensions = gate.get("dimensions")
    if not isinstance(hard, dict):
        errors.append("outcome review production gate hard_gates must be an object")
    elif set(hard) != set(HARD_GATES):
        errors.append("outcome review production gate must contain exactly the four canonical hard gates")
    else:
        for name in HARD_GATES:
            record = hard[name]
            if not isinstance(record, dict) or set(record) != {"status", "basis"}:
                errors.append(f"hard gate {name} requires exactly status and basis")
                continue
            if record.get("status") not in GATE_STATUSES:
                errors.append(f"hard gate {name} status must be pass, fail or blocked")
            if not isinstance(record.get("basis"), str) or word_count(record["basis"]) < 6:
                errors.append(f"hard gate {name} requires an observable basis of at least 6 words")
    if not isinstance(dimensions, dict):
        errors.append("outcome review production gate dimensions must be an object")
    elif set(dimensions) != set(STORY_DIMENSIONS):
        errors.append("outcome review production gate must contain exactly the nine canonical story dimensions")
    else:
        for name in STORY_DIMENSIONS:
            record = dimensions[name]
            if not isinstance(record, dict) or set(record) != {"score", "evidence_scope", "basis"}:
                errors.append(f"story dimension {name} requires exactly score, evidence_scope and basis")
                continue
            score = record.get("score")
            if not isinstance(score, int) or isinstance(score, bool) or not 1 <= score <= 10:
                errors.append(f"story dimension {name} score must be an integer from 1 to 10")
            if record.get("evidence_scope") not in EVIDENCE_SCOPES:
                errors.append(f"story dimension {name} evidence_scope must be full or limited")
            if not isinstance(record.get("basis"), str) or word_count(record["basis"]) < 6:
                errors.append(f"story dimension {name} requires an observable basis of at least 6 words")
    return gate, errors


def validate_outcome_review(
    text: str,
    *,
    require_mission_outcomes: bool = False,
    require_production_gate: bool = False,
) -> list[str]:
    """Validate review structure; canonical review tasks require the mission outcome pair."""

    errors: list[str] = []
    count = word_count(text)
    if not 40 <= count <= 1800:
        errors.append(f"outcome review must contain 40–1,800 words, found {count}")
    verdict = review_verdict(text)
    if verdict not in VERDICTS:
        errors.append("outcome review verdict must be pass, changes_requested or blocked")
    headings = BASE_HEADINGS + (MISSION_OUTCOME_HEADINGS if require_mission_outcomes else [])
    for heading in headings:
        if heading not in text:
            errors.append(f"outcome review missing heading: {heading}")
        elif not _heading_body(text, heading):
            errors.append(f"outcome review heading has no judgment: {heading}")
    if require_production_gate:
        gate, gate_errors = production_gate_data(text)
        errors.extend(gate_errors)
        if gate is not None and not gate_errors and verdict in VERDICTS:
            hard = gate["hard_gates"]
            dimensions = gate["dimensions"]
            statuses = [hard[name]["status"] for name in HARD_GATES]
            scores = [dimensions[name]["score"] for name in STORY_DIMENSIONS]
            derived = (
                "blocked"
                if "blocked" in statuses
                else "changes_requested"
                if "fail" in statuses or any(score < 8 for score in scores)
                else "pass"
            )
            if verdict != derived:
                errors.append(
                    f"outcome review verdict {verdict!r} contradicts production gate; derived verdict is {derived!r}"
                )
    return errors


def outcome_review_template(section: str) -> str:
    hard = {
        name: {"status": "fail", "basis": "Replace this placeholder with an observable draft-specific gate judgment."}
        for name in HARD_GATES
    }
    dimensions = {
        name: {
            "score": 7,
            "evidence_scope": "full",
            "basis": "Replace this placeholder with an observable evidence-adjusted scoring basis.",
        }
        for name in STORY_DIMENSIONS
    }
    gate = json.dumps(
        {"schema_version": 1, "hard_gates": hard, "dimensions": dimensions},
        ensure_ascii=False,
        indent=2,
    )
    return (
        f"# Outcome Evaluation — {section}\n\n"
        "Verdict: changes_requested\n\n"
        "## Outcome judgment\n\n"
        "Judge the section by listener outcome, continuity and evidence integrity.\n\n"
        "## Mission answerability\n\n"
        "Can the audience answer the section mission in their own words after hearing the section? State why.\n\n"
        "## Historical progression\n\n"
        "Can the audience retell the historical path that led to that answer? State why.\n\n"
        "## Production gate\n\n"
        f"{GATE_START}\n{gate}\n{GATE_END}\n\n"
        "## Issues\n\n"
        "For each material issue: location, observation, impact, responsible layer, revision scope and acceptance test.\n\n"
        "## Routing\n\n"
        "Route the result to prose_execution, product_architecture or evidence. Diagnose method only after an outcome problem is established.\n"
    )
