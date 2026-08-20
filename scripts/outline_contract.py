#!/usr/bin/env python3
"""Single executable contract shared by outline creation, approval and materialization."""

from __future__ import annotations

from copy import deepcopy
import re
from typing import Any


OUTLINE_SCHEMA_VERSION = 4
LEGACY_ADAPTIVE_SCHEMA_VERSION = 3
MAX_SECTION_WORDS = 3000
ACT_ROLES = ("opening", "body", "ending")


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


def valid_word_range(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and isinstance(value.get("min"), int)
        and not isinstance(value.get("min"), bool)
        and isinstance(value.get("max"), int)
        and not isinstance(value.get("max"), bool)
        and value.get("min", 0) > 0
        and value.get("max", 0) >= value.get("min", 0)
    )


def target_word_envelope(target: dict[str, Any]) -> dict[str, int] | None:
    """Convert product duration and narration rate into its total word envelope."""

    duration = target.get("duration_minutes") if isinstance(target, dict) else None
    wpm = target.get("narration_wpm") if isinstance(target, dict) else None
    if (
        not isinstance(duration, dict)
        or not isinstance(duration.get("min"), (int, float))
        or isinstance(duration.get("min"), bool)
        or not isinstance(duration.get("max"), (int, float))
        or isinstance(duration.get("max"), bool)
        or not isinstance(wpm, (int, float))
        or isinstance(wpm, bool)
        or duration["min"] <= 0
        or duration["max"] < duration["min"]
        or wpm <= 0
    ):
        return None
    return {"min": round(duration["min"] * wpm), "max": round(duration["max"] * wpm)}


def normalize_outline_contract(outline: dict[str, Any], product_target: dict[str, Any] | None = None) -> dict[str, Any]:
    """Expose approved v2 products through the v3 interface without rewriting their artifacts."""

    if outline.get("schema_version") != 2:
        return outline
    value = deepcopy(outline)
    value["schema_version"] = LEGACY_ADAPTIVE_SCHEMA_VERSION
    sections = value.get("sections", [])
    section_ids = [item.get("id") for item in sections if isinstance(item, dict) and item.get("id")]
    envelope = target_word_envelope(product_target) if product_target is not None else None
    if envelope is None:
        envelope = value.get("target_total_words")
    if not valid_word_range(envelope):
        budgets = [item.get("target_words") for item in sections if isinstance(item, dict)]
        valid_budgets = [item for item in budgets if valid_word_range(item)]
        envelope = {
            "min": sum(item["min"] for item in valid_budgets) or 1,
            "max": sum(item["max"] for item in valid_budgets) or 1,
        }
    audience_promise = str(value.get("proposed_answer") or value.get("central_question") or "Legacy approved arc.")
    value["script_architecture"] = {
        "audience_promise": audience_promise,
        "design_rationale": "Legacy v2 outline exposed as one compatibility movement; revise the outline before changing its macro architecture.",
        "total_word_envelope": envelope,
        "movements": [
            {
                "id": "M01",
                "order": 1,
                "title": "Legacy approved arc",
                "narrative_job": audience_promise,
                "entry_state": str(sections[0].get("entry_state", "Legacy entry state.")) if sections else "Legacy entry state.",
                "exit_state": str(sections[-1].get("exit_state", "Legacy exit state.")) if sections else "Legacy exit state.",
                "section_ids": section_ids,
            }
        ],
    }
    for section in sections:
        if not isinstance(section, dict):
            continue
        narrative_job = str(section.get("narrative_job") or "Legacy section transition.")
        section.setdefault("movement_id", "M01")
        section.setdefault("structural_role", narrative_job)
        section.setdefault("budget_rationale", "Legacy approved allocation retained until an explicit outline revision.")
        section.setdefault("planned_moves", [narrative_job])
    return value


def validate_outline_contract(
    outline: dict[str, Any],
    known_claim_ids: set[str] | None = None,
    product_target: dict[str, Any] | None = None,
    require_current: bool = False,
) -> list[str]:
    errors: list[str] = []
    schema_version = outline.get("schema_version")
    if schema_version in {2, LEGACY_ADAPTIVE_SCHEMA_VERSION} and require_current:
        errors.append(f"outline schema_version must be {OUTLINE_SCHEMA_VERSION} for new or revised output")
    if schema_version not in {2, LEGACY_ADAPTIVE_SCHEMA_VERSION, OUTLINE_SCHEMA_VERSION}:
        errors.append(f"outline schema_version must be {OUTLINE_SCHEMA_VERSION}")
    outline = normalize_outline_contract(outline, product_target)
    current_contract = outline.get("schema_version") == OUTLINE_SCHEMA_VERSION
    if current_contract and not re.fullmatch(r"C\d{3}", str(outline.get("cycle_id", ""))):
        errors.append("outline cycle_id must use C### format")
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

    architecture = outline.get("script_architecture")
    if not isinstance(architecture, dict):
        errors.append("outline script_architecture must be an object")
        architecture = {}
    architecture_fields = ["audience_promise", "design_rationale"]
    if current_contract:
        architecture_fields.append("central_question")
    for field in architecture_fields:
        if not isinstance(architecture.get(field), str) or not architecture[field].strip():
            errors.append(f"outline script_architecture.{field} is required")
    envelope = architecture.get("total_word_envelope")
    if not valid_word_range(envelope):
        errors.append("outline script_architecture.total_word_envelope is invalid")
        envelope = None
    expected_envelope = target_word_envelope(product_target) if product_target is not None else None
    if product_target is not None and expected_envelope is None:
        errors.append("product target cannot be converted into a word envelope")
    elif expected_envelope is not None and envelope is not None and (
        envelope["min"] < expected_envelope["min"] or envelope["max"] > expected_envelope["max"]
    ):
        errors.append(
            "outline total_word_envelope must stay within product duration and narration rate "
            f"({expected_envelope['min']}–{expected_envelope['max']})"
        )

    movements = architecture.get("movements")
    if not isinstance(movements, list) or not movements:
        errors.append("outline script_architecture requires at least one narrative movement")
        movements = []

    section_ids: set[str] = set()
    orders: set[int] = set()
    ordered_section_ids: list[str] = []
    allocated_min = 0
    allocated_max = 0
    required = ["title", "narrative_job", "entry_state", "exit_state", "claim_ids", "target_words"]
    if current_contract:
        required.append("movement_ids")
    else:
        required += ["movement_id", "structural_role", "budget_rationale", "planned_moves", "boundary"]
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
        ordered_section_ids.append(section_id)

        order = section.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1 or order in orders:
            errors.append(f"outline section {section_id or '?'} has invalid or duplicate order: {order!r}")
        else:
            orders.add(order)

        missing = [field for field in required if section.get(field) is None or section.get(field) == ""]
        if missing:
            errors.append(f"outline section {section_id or '?'} missing: {', '.join(missing)}")
        if not current_contract:
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
        if not isinstance(claim_ids, list) or not all(isinstance(item, str) and item for item in claim_ids):
            errors.append(f"outline section {section_id or '?'} claim_ids must be a list of claim IDs")
        elif not current_contract and not claim_ids:
            errors.append(f"outline section {section_id or '?'} claim_ids must be a non-empty list")
        elif known_claim_ids is not None:
            unknown = [claim_id for claim_id in claim_ids if claim_id not in known_claim_ids]
            if unknown:
                errors.append(f"outline section {section_id or '?'} references unknown claims: {', '.join(unknown)}")

        budget = section.get("target_words")
        if not valid_word_range(budget):
            errors.append(f"outline section {section_id or '?'} has invalid word budget")
        else:
            allocated_min += budget["min"]
            allocated_max += budget["max"]
            if budget["max"] > MAX_SECTION_WORDS:
                errors.append(
                    f"outline section {section_id or '?'} exceeds the {MAX_SECTION_WORDS}-word production-unit cap; "
                    "split the work unit without inventing a new audience-facing chapter"
                )
        if not current_contract:
            if not isinstance(section.get("budget_rationale"), str) or not section["budget_rationale"].strip():
                errors.append(f"outline section {section_id or '?'} budget_rationale is required")
            planned_moves = section.get("planned_moves")
            if (
                not isinstance(planned_moves, list)
                or not 1 <= len(planned_moves) <= 10
                or not all(isinstance(item, str) and item.strip() for item in planned_moves)
            ):
                errors.append(f"outline section {section_id or '?'} planned_moves must contain one to ten story moves")

        dependencies = section.get("dependencies", [])
        if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies):
            errors.append(f"outline section {section_id or '?'} dependencies must be a list")
        anchors = section.get("anchor_requirements", [])
        if not isinstance(anchors, (str, list)):
            errors.append(f"outline section {section_id or '?'} anchor_requirements must be text or a list")

    expected_orders = set(range(1, len(sections) + 1))
    if orders != expected_orders:
        errors.append("outline section orders must form a complete 1..N sequence")
    if envelope is not None and (allocated_max < envelope["min"] or allocated_min > envelope["max"]):
        errors.append(
            f"outline section budgets allocate {allocated_min}–{allocated_max} words with no feasible total inside the "
            f"{envelope['min']}–{envelope['max']} word envelope"
        )

    movement_ids: set[str] = set()
    movement_orders: set[int] = set()
    ordered_movement_ids: list[str] = []
    flattened_sections: list[str] = []
    movement_membership: dict[str, str] = {}
    current_membership: dict[str, list[str]] = {section_id: [] for section_id in ordered_section_ids}
    movement_windows: list[tuple[int, int]] = []
    for index, movement in enumerate(movements):
        if not isinstance(movement, dict):
            errors.append(f"outline movement #{index + 1} must be an object")
            continue
        movement_id = movement.get("id", "")
        if not re.fullmatch(r"M\d{2}", movement_id):
            errors.append(f"outline movement #{index + 1} has invalid id: {movement_id or '?'}")
        elif movement_id in movement_ids:
            errors.append(f"outline has duplicate movement id: {movement_id}")
        movement_ids.add(movement_id)
        ordered_movement_ids.append(movement_id)
        order = movement.get("order")
        if not isinstance(order, int) or isinstance(order, bool) or order < 1 or order in movement_orders:
            errors.append(f"outline movement {movement_id or '?'} has invalid or duplicate order: {order!r}")
        else:
            movement_orders.add(order)
        missing = [
            field
            for field in ["title", "narrative_job", "entry_state", "exit_state"]
            if not isinstance(movement.get(field), str) or not movement[field].strip()
        ]
        if missing:
            errors.append(f"outline movement {movement_id or '?'} missing: {', '.join(missing)}")
        if current_contract and (not isinstance(movement.get("act_id"), str) or not movement["act_id"]):
            errors.append(f"outline movement {movement_id or '?'} act_id is required")
        members = movement.get("section_ids")
        if not isinstance(members, list) or not members or not all(isinstance(item, str) for item in members):
            errors.append(f"outline movement {movement_id or '?'} section_ids must be a non-empty list")
            continue
        unknown_members = [section_id for section_id in members if section_id not in section_ids]
        if unknown_members:
            errors.append(f"outline movement {movement_id or '?'} references missing sections: {', '.join(unknown_members)}")
        if current_contract:
            member_indexes = [ordered_section_ids.index(section_id) for section_id in members if section_id in section_ids]
            if member_indexes:
                expected_indexes = list(range(min(member_indexes), max(member_indexes) + 1))
                if member_indexes != expected_indexes:
                    errors.append(f"outline movement {movement_id or '?'} sections must be contiguous and ordered")
                movement_windows.append((min(member_indexes), max(member_indexes)))
            for section_id in members:
                if section_id in current_membership:
                    current_membership[section_id].append(movement_id)
        else:
            for section_id in members:
                if section_id in movement_membership:
                    errors.append(
                        f"outline section {section_id} belongs to both {movement_membership[section_id]} and {movement_id}"
                    )
                movement_membership[section_id] = movement_id
            flattened_sections.extend(members)
    if movement_orders != set(range(1, len(movements) + 1)):
        errors.append("outline movement orders must form a complete 1..N sequence")
    if not current_contract and flattened_sections != ordered_section_ids:
        errors.append("outline movements must cover every section exactly once, contiguously and in section order")
    if current_contract:
        uncovered = [section_id for section_id, memberships in current_membership.items() if not memberships]
        if uncovered:
            errors.append("outline movements leave sections uncovered: " + ", ".join(uncovered))
        for previous, current in zip(movement_windows, movement_windows[1:]):
            if current[0] < previous[0] or current[1] < previous[1]:
                errors.append("outline movement-to-section windows must progress in section order")
                break

    act_ids: set[str] = set()
    movement_to_act: dict[str, str] = {}
    if current_contract:
        acts = architecture.get("acts")
        if not isinstance(acts, list) or len(acts) != 3:
            errors.append("outline script_architecture must contain exactly three acts")
            acts = []
        flattened_movements: list[str] = []
        for index, act in enumerate(acts):
            expected_id = f"A{index + 1:02d}"
            expected_role = ACT_ROLES[index]
            if not isinstance(act, dict):
                errors.append(f"outline act #{index + 1} must be an object")
                continue
            act_id = act.get("id")
            if act_id != expected_id:
                errors.append(f"outline act #{index + 1} id must be {expected_id}")
            elif act_id in act_ids:
                errors.append(f"outline has duplicate act id: {act_id}")
            act_ids.add(str(act_id))
            if act.get("role") != expected_role:
                errors.append(f"outline act {expected_id} role must be {expected_role}")
            missing = [
                field
                for field in ["title", "narrative_job", "entry_state", "exit_state"]
                if not isinstance(act.get(field), str) or not act[field].strip()
            ]
            if missing:
                errors.append(f"outline act {expected_id} missing: {', '.join(missing)}")
            members = act.get("movement_ids")
            if not isinstance(members, list) or not members or not all(isinstance(item, str) for item in members):
                errors.append(f"outline act {expected_id} movement_ids must be a non-empty list")
                continue
            for movement_id in members:
                if movement_id in movement_to_act:
                    errors.append(f"outline movement {movement_id} belongs to multiple acts")
                movement_to_act[movement_id] = expected_id
            flattened_movements.extend(members)
        if flattened_movements != ordered_movement_ids:
            errors.append("outline acts must cover every movement exactly once, contiguously and in movement order")
        for movement in movements:
            if not isinstance(movement, dict):
                continue
            movement_id = movement.get("id", "?")
            if movement.get("act_id") != movement_to_act.get(movement_id):
                errors.append(f"outline movement {movement_id} act_id conflicts with act membership")

    for section in sections:
        if not isinstance(section, dict):
            continue
        section_id = section.get("id", "?")
        if current_contract:
            memberships = section.get("movement_ids")
            if not isinstance(memberships, list) or not memberships or not all(isinstance(item, str) for item in memberships):
                errors.append(f"outline section {section_id} movement_ids must be a non-empty list")
            elif memberships != current_membership.get(section_id):
                errors.append(f"outline section {section_id} movement_ids conflict with movement membership")
            elif any(movement_id not in movement_ids for movement_id in memberships):
                errors.append(f"outline section {section_id} references a missing movement")
            elif len({movement_to_act.get(movement_id) for movement_id in memberships}) != 1:
                errors.append(f"outline section {section_id} cannot cross whole-script act boundaries")
        else:
            movement_id = section.get("movement_id")
            if movement_id not in movement_ids:
                errors.append(f"outline section {section_id} references missing movement: {movement_id or '?'}")
            elif movement_membership.get(section_id) != movement_id:
                errors.append(f"outline section {section_id} movement_id conflicts with movement membership")
        for dependency in section.get("dependencies", []) if isinstance(section.get("dependencies", []), list) else []:
            if dependency not in section_ids:
                errors.append(f"outline section {section_id} references missing dependency: {dependency}")
            elif dependency == section_id:
                errors.append(f"outline section {section_id} cannot depend on itself")
    return errors
