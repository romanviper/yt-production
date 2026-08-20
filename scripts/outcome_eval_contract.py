#!/usr/bin/env python3
"""Minimal contract for post-draft outcome evaluation."""

from __future__ import annotations

try:
    from scripts.common import word_count
except ModuleNotFoundError:
    from common import word_count


VERDICTS = {"pass", "changes_requested", "blocked"}
REQUIRED_HEADINGS = [
    "## Outcome judgment",
    "## Mission answerability",
    "## Historical progression",
    "## Issues",
    "## Routing",
]


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
        elif not _heading_body(text, heading):
            errors.append(f"outcome review heading has no judgment: {heading}")
    return errors


def outcome_review_template(section: str) -> str:
    return (
        f"# Outcome Evaluation — {section}\n\n"
        "Verdict: changes_requested\n\n"
        "## Outcome judgment\n\n"
        "Judge the section by listener outcome, continuity and evidence integrity.\n\n"
        "## Mission answerability\n\n"
        "Can the audience answer the section mission in their own words after hearing the section? State why.\n\n"
        "## Historical progression\n\n"
        "Can the audience retell the historical path that led to that answer? State why.\n\n"
        "## Issues\n\n"
        "For each material issue: location, observation, impact, responsible layer, revision scope and acceptance test.\n\n"
        "## Routing\n\n"
        "Route the result to prose_execution, product_architecture or evidence. Diagnose method only after an outcome problem is established.\n"
    )
