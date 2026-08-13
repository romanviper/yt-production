#!/usr/bin/env python3
"""Validate the compact, product-specific narrative voice profile."""

from __future__ import annotations

try:
    from scripts.common import word_count
except ModuleNotFoundError:
    from common import word_count


REQUIRED_HEADINGS = [
    "## Product voice",
    "## Borrowed functions",
    "## Original expression",
    "## Prohibited imitation",
    "## Draft tests",
]


def validate_voice_profile(text: str) -> list[str]:
    errors: list[str] = []
    count = word_count(text)
    if not 250 <= count <= 900:
        errors.append(f"voice profile must contain 250–900 words, found {count}")
    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"voice profile missing heading: {heading}")
    status_line = next((line for line in text.splitlines() if line.startswith("Status:")), "")
    if status_line not in {"Status: draft", "Status: approved", "Status: active"}:
        errors.append("voice profile status must be draft, approved or active")
    return errors


def set_voice_profile_status(text: str, status: str) -> str:
    if status not in {"draft", "approved", "active"}:
        raise ValueError(f"Unsupported voice profile status: {status}")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("Status:"):
            lines[index] = f"Status: {status}"
            return "\n".join(lines).rstrip() + "\n"
    raise ValueError("Voice profile is missing Status line")
