#!/usr/bin/env python3
"""Validate and render the concise human-facing brief for one Agent task."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, word_count
except ModuleNotFoundError:  # Direct execution: python scripts/operator_brief.py
    from common import read_json, word_count


MAX_RENDERED_WORDS = 140
MAX_POINTS = 3
MAX_OPTIONS = 3
VALID_STATUSES = {"in_progress", "completed", "ready_for_review", "blocked"}
STATUS_LABELS = {
    "in_progress": "Đang thực hiện",
    "completed": "Kết quả",
    "ready_for_review": "Chờ bạn duyệt",
    "blocked": "Đang bị chặn",
}


def empty_brief() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "status": "in_progress",
        "headline": "",
        "material_points": [],
        "decision": {
            "required": False,
            "question": "",
            "recommendation": "",
            "options": [],
        },
        "next_step": "",
    }


def render_brief(document: dict[str, Any], validate: bool = True) -> str:
    if validate:
        errors = validate_brief(document, check_render=False)
        if errors:
            raise ValueError("; ".join(errors))
    status = document["status"]
    lines = [f"**{STATUS_LABELS[status]}:** {document['headline'].strip()}"]
    points = document.get("material_points", [])
    if points:
        lines.extend(["", *[f"- {item.strip()}" for item in points]])
    decision = document.get("decision", {})
    if decision.get("required"):
        lines.extend(["", f"**Khuyến nghị:** {decision['recommendation'].strip()}"])
        lines.extend(["", f"**Cần bạn quyết định:** {decision['question'].strip()}"])
        for option in decision.get("options", []):
            lines.append(f"- **{option['label'].strip()}:** {option['effect'].strip()}")
    else:
        lines.extend(["", f"**Tiếp theo:** {document['next_step'].strip()}"])
    return "\n".join(lines).strip() + "\n"


def validate_brief(document: dict[str, Any], check_render: bool = True) -> list[str]:
    errors: list[str] = []
    if document.get("schema_version") != 1:
        errors.append("operator brief schema_version must be 1")
    status = document.get("status")
    if status not in VALID_STATUSES:
        errors.append(f"invalid operator brief status: {status}")
    headline = document.get("headline")
    if not isinstance(headline, str) or not headline.strip():
        errors.append("operator brief headline is required")
    elif word_count(headline) > 35:
        errors.append("operator brief headline exceeds 35 words")

    points = document.get("material_points")
    if not isinstance(points, list):
        errors.append("operator brief material_points must be a list")
        points = []
    elif len(points) > MAX_POINTS:
        errors.append(f"operator brief has more than {MAX_POINTS} material points")
    for index, point in enumerate(points):
        if not isinstance(point, str) or not point.strip():
            errors.append(f"operator brief material point {index + 1} is empty")
        elif word_count(point) > 30:
            errors.append(f"operator brief material point {index + 1} exceeds 30 words")

    decision = document.get("decision")
    if not isinstance(decision, dict) or not isinstance(decision.get("required"), bool):
        errors.append("operator brief decision.required must be boolean")
        decision = {"required": False}
    required = decision.get("required", False)
    question = decision.get("question", "")
    recommendation = decision.get("recommendation", "")
    options = decision.get("options", [])
    next_step = document.get("next_step", "")
    if required:
        if not isinstance(question, str) or not question.strip():
            errors.append("decision question is required")
        elif word_count(question) > 30:
            errors.append("decision question exceeds 30 words")
        if not isinstance(recommendation, str) or not recommendation.strip():
            errors.append("decision recommendation is required")
        elif word_count(recommendation) > 30:
            errors.append("decision recommendation exceeds 30 words")
        if not isinstance(options, list) or not 1 <= len(options) <= MAX_OPTIONS:
            errors.append(f"decision requires one to {MAX_OPTIONS} options")
            options = []
        for index, option in enumerate(options):
            if not isinstance(option, dict) or not str(option.get("label", "")).strip() or not str(option.get("effect", "")).strip():
                errors.append(f"decision option {index + 1} requires label and effect")
                continue
            if word_count(str(option["label"])) + word_count(str(option["effect"])) > 30:
                errors.append(f"decision option {index + 1} exceeds 30 words")
        if isinstance(next_step, str) and next_step.strip():
            errors.append("next_step must be empty when a decision is required")
    else:
        if any(isinstance(value, str) and value.strip() for value in [question, recommendation]) or options:
            errors.append("decision fields must be empty when no decision is required")
        if not isinstance(next_step, str) or not next_step.strip():
            errors.append("next_step is required when no decision is required")
        elif word_count(next_step) > 30:
            errors.append("next_step exceeds 30 words")

    if status == "ready_for_review" and not required:
        errors.append("ready_for_review requires an explicit user decision")

    if check_render and not errors:
        rendered = render_brief(document, validate=False)
        if word_count(rendered) > MAX_RENDERED_WORDS:
            errors.append(f"rendered operator brief exceeds {MAX_RENDERED_WORDS} words")
    return errors


def validate_brief_file(path: Path) -> list[str]:
    try:
        return validate_brief(read_json(path))
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        return [f"invalid operator brief: {exc}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ["validate", "render"]:
        item = sub.add_parser(command)
        item.add_argument("path", type=Path)
    args = parser.parse_args()
    try:
        document = read_json(args.path)
        errors = validate_brief(document)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.command == "render":
        print(render_brief(document), end="")
    else:
        print("Operator brief is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
