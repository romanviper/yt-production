"""Single source of truth for research-plan structure and workstream brief handoff."""

from __future__ import annotations

from typing import Any


SHARED_PROTOCOL_FIELDS = [
    "chronology",
    "terminology",
    "case_selection",
    "cross_cutting_ownership",
    "handoff_contract",
]


def validate_research_plan_contract(plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    workstreams = plan.get("workstreams", [])
    if not workstreams:
        errors.append("research plan has no workstreams")
    ids = [item.get("id") for item in workstreams]
    if len(ids) != len(set(ids)):
        errors.append("research plan has duplicate workstream IDs")

    protocol = plan.get("shared_research_protocol")
    if not isinstance(protocol, dict):
        errors.append("research plan requires shared_research_protocol")
        protocol = {}
    for field in SHARED_PROTOCOL_FIELDS:
        if not protocol.get(field):
            errors.append(f"shared_research_protocol missing: {field}")

    required = [
        "id",
        "title",
        "question",
        "in_scope",
        "out_of_scope",
        "ownership",
        "required_evidence",
        "completion_criteria",
        "synthesis_handoff",
    ]
    for item in workstreams:
        missing = [field for field in required if not item.get(field)]
        if missing:
            errors.append(f"research workstream {item.get('id', '?')} missing: {', '.join(missing)}")
    return errors


def bullet_list(items: list[Any]) -> str:
    return "\n".join(f"- {item}" for item in items) or "- Chưa xác định."


def render_shared_protocol(protocol: dict[str, Any]) -> str:
    ownership = protocol.get("cross_cutting_ownership", {})
    ownership_lines = "\n".join(f"- **{key}:** {value}" for key, value in ownership.items()) or "- Chưa xác định."
    return (
        "## Shared research protocol\n\n"
        "### Chronology\n\n"
        f"{bullet_list(protocol.get('chronology', []))}\n\n"
        "### Terminology\n\n"
        f"{bullet_list(protocol.get('terminology', []))}\n\n"
        "### Case selection\n\n"
        f"{bullet_list(protocol.get('case_selection', []))}\n\n"
        "### Cross-cutting ownership\n\n"
        f"{ownership_lines}\n\n"
        "### Common handoff contract\n\n"
        f"{bullet_list(protocol.get('handoff_contract', []))}"
    )
