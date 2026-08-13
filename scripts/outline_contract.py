#!/usr/bin/env python3
"""Single executable contract shared by outline creation, approval and materialization."""

from __future__ import annotations

import re
from typing import Any


def outline_section_count(outline: dict[str, Any]) -> int | None:
    """Return the canonical section count while accepting the v1 field during migration."""

    current = outline.get("section_count")
    legacy = outline.get("section_count_target")
    return current if current is not None else legacy


def render_section_question_payoff(section: dict[str, Any]) -> str:
    """Render canonical split fields or the legacy combined field without losing meaning."""

    question = section.get("question")
    payoff = section.get("payoff")
    if isinstance(question, str) and question.strip() and isinstance(payoff, str) and payoff.strip():
        return f"## Question\n\n{question.strip()}\n\n## Payoff\n\n{payoff.strip()}"
    combined = section.get("question_payoff", "")
    return f"## Question and payoff\n\n{str(combined).strip()}"


def render_outline_value(value: Any, fallback: str = "Không có.") -> str:
    """Render scalar or list-valued outline fields as readable Markdown."""

    if isinstance(value, list):
        items = [str(item).strip() for item in value if str(item).strip()]
        return "\n".join(f"- {item}" for item in items) if items else fallback
    text = str(value or "").strip()
    return text or fallback


def validate_outline_contract(outline: dict[str, Any], known_claim_ids: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    sections = outline.get("sections")
    if not isinstance(sections, list) or not sections:
        return ["outline must contain at least one section"]

    current_count = outline.get("section_count")
    legacy_count = outline.get("section_count_target")
    if current_count is not None and legacy_count is not None and current_count != legacy_count:
        errors.append("outline section_count conflicts with legacy section_count_target")
    count = outline_section_count(outline)
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        errors.append("outline section_count must be a positive integer")
    elif len(sections) != count:
        errors.append(f"outline declares {count} sections but contains {len(sections)}")

    section_ids: set[str] = set()
    orders: set[int] = set()
    required = ["title", "narrative_job", "entry_state", "exit_state", "claim_ids", "target_words", "boundary"]
    for index, section in enumerate(sections):
        if not isinstance(section, dict):
            errors.append(f"outline section #{index + 1} must be an object")
            continue
        section_id = section.get("id", "")
        if not re.fullmatch(r"P\d{2}", section_id):
            errors.append(f"outline section #{index + 1} has invalid id: {section_id or '?'}")
        elif section_id in section_ids:
            errors.append(f"outline has duplicate section id: {section_id}")
        section_ids.add(section_id)

        order = section.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1 or order in orders:
            errors.append(f"outline section {section_id or '?'} has invalid or duplicate order: {order!r}")
        else:
            orders.add(order)

        missing = [field for field in required if section.get(field) is None or section.get(field) == ""]
        if missing:
            errors.append(f"outline section {section_id or '?'} missing: {', '.join(missing)}")
        question = section.get("question")
        payoff = section.get("payoff")
        combined = section.get("question_payoff")
        split_complete = isinstance(question, str) and bool(question.strip()) and isinstance(payoff, str) and bool(payoff.strip())
        legacy_complete = isinstance(combined, str) and bool(combined.strip())
        if not split_complete and not legacy_complete:
            errors.append(f"outline section {section_id or '?'} requires question and payoff")
        if (question or payoff) and not split_complete:
            errors.append(f"outline section {section_id or '?'} must provide both question and payoff")

        claim_ids = section.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids or not all(isinstance(item, str) and item for item in claim_ids):
            errors.append(f"outline section {section_id or '?'} claim_ids must be a non-empty list")
        elif known_claim_ids is not None:
            unknown = [claim_id for claim_id in claim_ids if claim_id not in known_claim_ids]
            if unknown:
                errors.append(f"outline section {section_id or '?'} references unknown claims: {', '.join(unknown)}")

        budget = section.get("target_words")
        if (
            not isinstance(budget, dict)
            or not isinstance(budget.get("min"), int)
            or isinstance(budget.get("min"), bool)
            or not isinstance(budget.get("max"), int)
            or isinstance(budget.get("max"), bool)
            or budget.get("min", 0) <= 0
            or budget.get("max", 0) < budget.get("min", 0)
        ):
            errors.append(f"outline section {section_id or '?'} has invalid word budget")

        dependencies = section.get("dependencies", [])
        if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies):
            errors.append(f"outline section {section_id or '?'} dependencies must be a list")
        anchors = section.get("anchor_requirements", [])
        if not isinstance(anchors, (str, list)):
            errors.append(f"outline section {section_id or '?'} anchor_requirements must be text or a list")

    expected_orders = set(range(1, len(sections) + 1))
    if orders != expected_orders:
        errors.append("outline section orders must form a complete 1..N sequence")
    for section in sections:
        if not isinstance(section, dict):
            continue
        section_id = section.get("id", "?")
        for dependency in section.get("dependencies", []) if isinstance(section.get("dependencies", []), list) else []:
            if dependency not in section_ids:
                errors.append(f"outline section {section_id} references missing dependency: {dependency}")
            elif dependency == section_id:
                errors.append(f"outline section {section_id} cannot depend on itself")
    return errors
