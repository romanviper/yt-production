#!/usr/bin/env python3
"""Compile a read-only, non-canonical writer packet for one section excerpt."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import REPO_ROOT, estimate_tokens, read_json, sha256
    from scripts.draft_evidence import build_narrative_writer_brief
except ModuleNotFoundError:  # Direct execution from scripts/
    from common import REPO_ROOT, estimate_tokens, read_json, sha256
    from draft_evidence import build_narrative_writer_brief


EXCERPT_PACKET_SCHEMA_VERSION = 1
EXCERPT_POSITIONS = {"opening", "middle", "ending"}
MIN_EXCERPT_WORDS = 100
MAX_EXCERPT_WORDS = 800
MAX_EXCERPT_CLAIMS = 3
MAX_EXCERPT_INSTRUCTION_TOKENS = 1500
INSTRUCTION_PATHS = [
    REPO_ROOT / "system" / "core" / "creative-boundaries.md",
    REPO_ROOT / "system" / "operations" / "draft-excerpt.md",
]


def _json_hash(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _bounded_text(value: Any, *, field: str, minimum: int, maximum: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be text")
    normalized = value.strip()
    if not minimum <= len(normalized) <= maximum:
        raise ValueError(f"{field} must be {minimum}-{maximum} characters")
    return normalized


def _word_range(value: Any, *, field: str) -> dict[str, int]:
    if not isinstance(value, dict) or set(value) != {"min", "max"}:
        raise ValueError(f"{field} must contain exactly min and max")
    minimum = value.get("min")
    maximum = value.get("max")
    if (
        not isinstance(minimum, int)
        or isinstance(minimum, bool)
        or not isinstance(maximum, int)
        or isinstance(maximum, bool)
        or minimum <= 0
        or maximum < minimum
    ):
        raise ValueError(f"{field} must be a positive ordered integer range")
    return {"min": minimum, "max": maximum}


def compile_excerpt_packet(
    product_dir: Path,
    section: str,
    *,
    position: str,
    target_words: dict[str, int],
    local_job: str,
    completion_rule: str,
    claim_ids: list[str],
    completes_section: bool = False,
) -> tuple[dict[str, Any], str]:
    """Return a machine packet and the exact packet-only context shown to the writer."""

    product_dir = product_dir.resolve()
    if re.fullmatch(r"P\d{2}", section) is None:
        raise ValueError("section must match P##")
    if position not in EXCERPT_POSITIONS:
        raise ValueError("position must be opening, middle or ending")
    if not isinstance(completes_section, bool):
        raise ValueError("completes_section must be boolean")

    excerpt_words = _word_range(target_words, field="target_words")
    if (
        excerpt_words["min"] < MIN_EXCERPT_WORDS
        or excerpt_words["max"] > MAX_EXCERPT_WORDS
    ):
        raise ValueError(
            f"excerpt target must stay within {MIN_EXCERPT_WORDS}-{MAX_EXCERPT_WORDS} words"
        )
    local_job = _bounded_text(local_job, field="local_job", minimum=40, maximum=1000)
    completion_rule = _bounded_text(
        completion_rule,
        field="completion_rule",
        minimum=20,
        maximum=800,
    )

    if (
        not isinstance(claim_ids, list)
        or not claim_ids
        or len(claim_ids) > MAX_EXCERPT_CLAIMS
        or len(set(claim_ids)) != len(claim_ids)
        or not all(isinstance(item, str) and re.fullmatch(r"CLM-\d{4}", item) for item in claim_ids)
    ):
        raise ValueError(f"claim_ids must contain 1-{MAX_EXCERPT_CLAIMS} unique CLM-#### ids")

    product_path = product_dir / "product.json"
    product = read_json(product_path)
    output_language = _bounded_text(
        product.get("language"), field="product.language", minimum=2, maximum=20
    )

    root = product_dir / "03_sections" / section
    section_path = root / "section.json"
    narration_path = root / "narration-pack.json"
    evidence_path = root / "evidence-pack.json"
    state = read_json(section_path)
    narration = read_json(narration_path)
    evidence = read_json(evidence_path)
    if (
        state.get("id") != section
        or narration.get("section") != section
        or evidence.get("section") != section
    ):
        raise ValueError("section, narration and evidence bindings do not match")
    if narration.get("schema_version") != 4:
        raise ValueError("excerpt probes require a direct-authorship narration pack")
    if narration.get("evidence_pack_sha256") != sha256(evidence_path):
        raise ValueError("evidence pack is stale relative to narration authority")

    scope = narration.get("retrieval_scope")
    allowed_claim_ids = scope.get("claim_ids") if isinstance(scope, dict) else None
    if not isinstance(allowed_claim_ids, list):
        raise ValueError("narration pack is missing a valid claim retrieval scope")
    outside = [item for item in claim_ids if item not in allowed_claim_ids]
    if outside:
        raise ValueError("excerpt claim is outside approved section scope: " + ", ".join(outside))

    evidence_claim_ids = {
        item.get("id")
        for item in evidence.get("claims", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    missing = [item for item in claim_ids if item not in evidence_claim_ids]
    if missing:
        raise ValueError("excerpt claim is missing from evidence pack: " + ", ".join(missing))

    section_words = _word_range(state.get("target_words"), field="section.target_words")
    if not completes_section and excerpt_words["max"] >= section_words["max"]:
        raise ValueError("a non-completing excerpt must be smaller than the full section target")

    writer_brief = build_narrative_writer_brief(evidence, claim_ids)
    projected_claim_count = len(writer_brief["materials"]) + len(writer_brief["redlines"])
    if projected_claim_count != len(claim_ids):
        raise ValueError("selected evidence could not be projected completely into the writer brief")

    excerpt_contract: dict[str, Any] = {
        "operation": "draft_excerpt",
        "canonical_output": False,
        "section": section,
        "section_title": state.get("title"),
        "output_language": output_language,
        "position": position,
        "whole_section_target_words": section_words,
        "excerpt_target_words": excerpt_words,
        "local_job": local_job,
        "local_completion_rule": completion_rule,
        "completes_section": completes_section,
        "scope_rule": (
            "This target is one contiguous slice of the longer section, not a compressed target for the whole section."
        ),
    }
    if position == "opening":
        excerpt_contract["starting_audience_assumption"] = state.get("entry_state")
    if completes_section:
        excerpt_contract["whole_section_mission"] = state.get("mission")
        excerpt_contract["whole_section_exit_state"] = state.get("exit_state")
    else:
        excerpt_contract["stop_rule"] = (
            "Leave the whole section mission and exit state unresolved; do not survey later section material."
        )

    instruction_blocks: list[str] = []
    instruction_hashes: dict[str, str] = {}
    for path in INSTRUCTION_PATHS:
        if not path.is_file():
            raise FileNotFoundError(f"missing excerpt instruction: {path}")
        relative = path.relative_to(REPO_ROOT).as_posix()
        content = path.read_text(encoding="utf-8").rstrip()
        instruction_hashes[relative] = sha256(path)
        instruction_blocks.extend(
            [
                f"# BEGIN INSTRUCTION: {relative}",
                content,
                f"# END INSTRUCTION: {relative}",
                "",
            ]
        )
    instruction_tokens = estimate_tokens("\n".join(instruction_blocks))
    if instruction_tokens > MAX_EXCERPT_INSTRUCTION_TOKENS:
        raise ValueError(
            f"excerpt instruction estimate {instruction_tokens} exceeds {MAX_EXCERPT_INSTRUCTION_TOKENS}"
        )

    context = "\n".join(
        [
            f"# Context Packet — excerpt-probe-{section}",
            "",
            "Only this packet is context. Do not inspect the repository or any previous draft.",
            "Output only the requested passage; do not write product files, reports or approvals.",
            "",
            *instruction_blocks,
            "# BEGIN EXCERPT CONTRACT",
            json.dumps(excerpt_contract, ensure_ascii=False, indent=2),
            "# END EXCERPT CONTRACT",
            "",
            "# BEGIN COMPACT EVIDENCE SUBSET",
            json.dumps(writer_brief, ensure_ascii=False, indent=2),
            "# END COMPACT EVIDENCE SUBSET",
            "",
        ]
    )
    packet = {
        "schema_version": EXCERPT_PACKET_SCHEMA_VERSION,
        "operation": "draft_excerpt",
        "canonical_output": False,
        "section": section,
        "output_language": output_language,
        "position": position,
        "target_words": excerpt_words,
        "local_job": local_job,
        "completion_rule": completion_rule,
        "completes_section": completes_section,
        "selected_claim_ids": list(claim_ids),
        "selected_scope_sha256": _json_hash({"claim_ids": sorted(claim_ids)}),
        "input_hashes": {
            "product.json": sha256(product_path),
            f"03_sections/{section}/section.json": sha256(section_path),
            f"03_sections/{section}/narration-pack.json": sha256(narration_path),
            f"03_sections/{section}/evidence-pack.json": sha256(evidence_path),
            **instruction_hashes,
        },
        "instruction_tokens": instruction_tokens,
        "estimated_context_tokens": estimate_tokens(context),
        "context_sha256": hashlib.sha256(context.encode("utf-8")).hexdigest(),
    }
    return packet, context


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product_dir", type=Path)
    parser.add_argument("section")
    parser.add_argument("--position", choices=sorted(EXCERPT_POSITIONS), required=True)
    parser.add_argument("--min-words", type=int, required=True)
    parser.add_argument("--max-words", type=int, required=True)
    parser.add_argument("--local-job", required=True)
    parser.add_argument("--completion-rule", required=True)
    parser.add_argument("--claim", action="append", dest="claim_ids", required=True)
    parser.add_argument("--completes-section", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    packet, context = compile_excerpt_packet(
        args.product_dir,
        args.section,
        position=args.position,
        target_words={"min": args.min_words, "max": args.max_words},
        local_job=args.local_job,
        completion_rule=args.completion_rule,
        claim_ids=args.claim_ids,
        completes_section=args.completes_section,
    )
    if args.as_json:
        print(json.dumps({"packet": packet, "context": context}, ensure_ascii=False, indent=2))
    else:
        print(context, end="")


if __name__ == "__main__":
    main()
