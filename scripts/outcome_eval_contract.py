#!/usr/bin/env python3
"""Minimal contract for post-draft outcome evaluation."""

from __future__ import annotations

try:
    from scripts.common import word_count
except ModuleNotFoundError:
    from common import word_count


VERDICTS = {"pass", "changes_requested", "blocked"}
REQUIRED_HEADINGS = ["## Outcome judgment", "## Issues", "## Routing"]


def review_verdict(text: str) -> str | None:
    for line in text.splitlines():
        if line.lower().startswith("verdict:"):
            value = line.split(":", 1)[1].strip().lower()
            return value or None
    return None


def validate_outcome_review(text: str) -> list[str]:
    errors: list[str] = []
    count = word_count(text)
    if not 40 <= count <= 1800:
        errors.append(f"outcome review must contain 40–1,800 words, found {count}")
    verdict = review_verdict(text)
    if verdict not in VERDICTS:
        errors.append("outcome review verdict must be pass, changes_requested or blocked")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"outcome review missing heading: {heading}")
    return errors


def outcome_review_template(section: str) -> str:
    return (
        f"# Outcome Evaluation — {section}\n\n"
        "Verdict: changes_requested\n\n"
        "## Outcome judgment\n\n"
        "Judge the listener progression, authorship, section objective, causal clarity, continuity and evidence integrity.\n\n"
        "## Issues\n\n"
        "For each material issue: location, observation, impact, responsible layer, revision scope and acceptance test.\n\n"
        "## Routing\n\n"
        "Route the result to prose_execution, product_architecture or evidence. Diagnose method only after an outcome problem is established.\n"
    )
