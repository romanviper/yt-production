#!/usr/bin/env python3
"""Validate product contracts without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


GATE_STATES = {
    "not_started",
    "in_progress",
    "ready_for_review",
    "approved",
    "changes_requested",
    "blocked",
}
EXPECTED_GATES = {f"G{number}" for number in range(8)}
WORK_STATES = {"ready", "in_progress", "blocked", "review", "closed"}
CHAPTER_STATES = {
    "planned",
    "brief_ready",
    "drafting",
    "review",
    "approved",
    "changes_requested",
    "omitted",
}
CLAIM_STATES = {"open", "supported", "qualified", "rejected", "blocked"}
CLAIM_TYPES = {"fact", "inference", "contested", "unknown"}
CONFIDENCE_LEVELS = {"high", "medium", "low", "unrated"}
SOURCE_STATES = {"discovered", "queued", "reviewed", "rejected", "inaccessible"}


@dataclass(frozen=True)
class Issue:
    level: str
    location: str
    message: str


def load_json(path: Path, issues: list[Issue]) -> dict:
    if not path.is_file():
        issues.append(Issue("ERROR", str(path), "Thiếu file bắt buộc."))
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        issues.append(Issue("ERROR", str(path), f"JSON không hợp lệ: {exc}"))
        return {}
    if not isinstance(value, dict):
        issues.append(Issue("ERROR", str(path), "Root JSON phải là object."))
        return {}
    return value


def require_keys(data: dict, keys: set[str], path: Path, issues: list[Issue]) -> None:
    for key in sorted(keys - data.keys()):
        issues.append(Issue("ERROR", str(path), f"Thiếu key `{key}`."))


def detect_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    active: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in active:
            start = active.index(node)
            cycles.append(active[start:] + [node])
            return
        if node in visited:
            return
        active.append(node)
        for dependency in graph.get(node, []):
            visit(dependency)
        active.pop()
        visited.add(node)

    for node in graph:
        visit(node)
    return cycles


def validate_product(product_dir: Path) -> list[Issue]:
    product_dir = product_dir.resolve()
    issues: list[Issue] = []

    product_path = product_dir / "product.json"
    work_path = product_dir / "work-order.json"
    source_path = product_dir / "01_research" / "source-index.json"
    claim_path = product_dir / "01_research" / "claim-ledger.json"
    manifest_path = product_dir / "03_outline" / "manifest.json"

    product = load_json(product_path, issues)
    work = load_json(work_path, issues)
    sources_doc = load_json(source_path, issues)
    claims_doc = load_json(claim_path, issues)
    manifest = load_json(manifest_path, issues)

    if product:
        require_keys(
            product,
            {"schema_version", "slug", "working_title", "language", "target", "gates"},
            product_path,
            issues,
        )
        if product.get("slug") != product_dir.name:
            issues.append(Issue("ERROR", str(product_path), "`slug` phải trùng tên thư mục product."))
        gates = product.get("gates", {})
        if not isinstance(gates, dict):
            issues.append(Issue("ERROR", str(product_path), "`gates` phải là object."))
        else:
            missing = EXPECTED_GATES - gates.keys()
            extra = gates.keys() - EXPECTED_GATES
            for gate in sorted(missing):
                issues.append(Issue("ERROR", str(product_path), f"Thiếu gate {gate}."))
            for gate in sorted(extra):
                issues.append(Issue("WARNING", str(product_path), f"Gate không nhận diện: {gate}."))
            for gate, state in gates.items():
                if state not in GATE_STATES:
                    issues.append(Issue("ERROR", str(product_path), f"{gate} có state không hợp lệ: {state}."))

    if work:
        require_keys(
            work,
            {
                "schema_version",
                "id",
                "product",
                "task_type",
                "state",
                "objective",
                "required_reads",
                "allowed_write_paths",
                "acceptance_criteria",
                "blocked_by",
            },
            work_path,
            issues,
        )
        if product and work.get("product") != product.get("slug"):
            issues.append(Issue("ERROR", str(work_path), "Work order trỏ sai product."))
        if work.get("state") not in WORK_STATES:
            issues.append(Issue("ERROR", str(work_path), f"Work state không hợp lệ: {work.get('state')}."))
        repo_root = product_dir.parents[1]
        for required in work.get("required_reads", []):
            candidate = repo_root / required
            if not candidate.exists():
                issues.append(Issue("ERROR", str(work_path), f"required_reads không tồn tại: {required}."))

    sources = sources_doc.get("sources", []) if sources_doc else []
    if not isinstance(sources, list):
        issues.append(Issue("ERROR", str(source_path), "`sources` phải là array."))
        sources = []
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        location = f"{source_path}#sources[{index}]"
        if not isinstance(source, dict):
            issues.append(Issue("ERROR", location, "Source phải là object."))
            continue
        source_id = source.get("id", "")
        if not re.fullmatch(r"SRC-\d{4}", source_id):
            issues.append(Issue("ERROR", location, f"Source ID không hợp lệ: {source_id!r}."))
        if source_id in source_ids:
            issues.append(Issue("ERROR", location, f"Source ID trùng: {source_id}."))
        source_ids.add(source_id)
        if source.get("status") not in SOURCE_STATES:
            issues.append(Issue("ERROR", location, f"Source status không hợp lệ: {source.get('status')}."))
        if source.get("status") == "reviewed" and not source.get("locators"):
            issues.append(Issue("ERROR", location, "Source `reviewed` phải có locator."))

    claims = claims_doc.get("claims", []) if claims_doc else []
    if not isinstance(claims, list):
        issues.append(Issue("ERROR", str(claim_path), "`claims` phải là array."))
        claims = []
    claim_ids: set[str] = set()
    claims_by_id: dict[str, dict] = {}
    for index, claim in enumerate(claims):
        location = f"{claim_path}#claims[{index}]"
        if not isinstance(claim, dict):
            issues.append(Issue("ERROR", location, "Claim phải là object."))
            continue
        claim_id = claim.get("id", "")
        if not re.fullmatch(r"CLM-\d{4}", claim_id):
            issues.append(Issue("ERROR", location, f"Claim ID không hợp lệ: {claim_id!r}."))
        if claim_id in claim_ids:
            issues.append(Issue("ERROR", location, f"Claim ID trùng: {claim_id}."))
        claim_ids.add(claim_id)
        claims_by_id[claim_id] = claim
        if claim.get("type") not in CLAIM_TYPES:
            issues.append(Issue("ERROR", location, f"Claim type không hợp lệ: {claim.get('type')}."))
        if claim.get("confidence") not in CONFIDENCE_LEVELS:
            issues.append(Issue("ERROR", location, f"Confidence không hợp lệ: {claim.get('confidence')}."))
        if claim.get("status") not in CLAIM_STATES:
            issues.append(Issue("ERROR", location, f"Claim status không hợp lệ: {claim.get('status')}."))
        for source_id in claim.get("sources", []):
            if source_id not in source_ids:
                issues.append(Issue("ERROR", location, f"Claim tham chiếu source chưa tồn tại: {source_id}."))
        if claim.get("status") in {"supported", "qualified"} and not claim.get("sources"):
            issues.append(Issue("ERROR", location, "Claim đã support/qualify phải có source."))

    chapters = manifest.get("chapters", []) if manifest else []
    if product and manifest and manifest.get("product") != product.get("slug"):
        issues.append(Issue("ERROR", str(manifest_path), "Manifest trỏ sai product."))
    if not isinstance(chapters, list):
        issues.append(Issue("ERROR", str(manifest_path), "`chapters` phải là array."))
        chapters = []

    chapter_ids: set[str] = set()
    graph: dict[str, list[str]] = {}
    min_words = 0
    max_words = 0
    for index, chapter in enumerate(chapters):
        location = f"{manifest_path}#chapters[{index}]"
        if not isinstance(chapter, dict):
            issues.append(Issue("ERROR", location, "Chapter phải là object."))
            continue
        chapter_id = chapter.get("id", "")
        if not re.fullmatch(r"CH\d{2}", chapter_id):
            issues.append(Issue("ERROR", location, f"Chapter ID không hợp lệ: {chapter_id!r}."))
        if chapter_id in chapter_ids:
            issues.append(Issue("ERROR", location, f"Chapter ID trùng: {chapter_id}."))
        chapter_ids.add(chapter_id)
        graph[chapter_id] = list(chapter.get("depends_on", []))
        if chapter.get("status") not in CHAPTER_STATES:
            issues.append(Issue("ERROR", location, f"Chapter status không hợp lệ: {chapter.get('status')}."))
        brief = chapter.get("brief")
        if not brief or not (product_dir / brief).is_file():
            issues.append(Issue("ERROR", location, f"Thiếu chapter brief: {brief}."))
        draft = chapter.get("draft")
        if chapter.get("status") in {"drafting", "review", "approved", "changes_requested"}:
            if not draft or not (product_dir / draft).is_file():
                issues.append(Issue("ERROR", location, f"Trạng thái {chapter.get('status')} cần draft: {draft}."))
        for claim_id in chapter.get("claims", []):
            if claim_id not in claim_ids:
                issues.append(Issue("ERROR", location, f"Chapter tham chiếu claim chưa tồn tại: {claim_id}."))
            elif chapter.get("status") in {"review", "approved"} and claims_by_id[claim_id].get("status") in {"open", "blocked", "rejected"}:
                issues.append(Issue("ERROR", location, f"Chapter {chapter.get('status')} dùng claim chưa sẵn sàng: {claim_id}."))
        budget = chapter.get("target_words", {})
        try:
            low, high = int(budget.get("min", 0)), int(budget.get("max", 0))
            if low <= 0 or high < low:
                raise ValueError
            min_words += low
            max_words += high
        except (TypeError, ValueError):
            issues.append(Issue("ERROR", location, "`target_words` cần min > 0 và max >= min."))

    for chapter_id, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in chapter_ids:
                issues.append(Issue("ERROR", str(manifest_path), f"{chapter_id} phụ thuộc chapter chưa tồn tại: {dependency}."))
    for cycle in detect_cycles(graph):
        issues.append(Issue("ERROR", str(manifest_path), "Dependency cycle: " + " -> ".join(cycle)))

    if product and chapters:
        target = product.get("target", {})
        duration = target.get("duration_minutes", {})
        wpm = target.get("narration_wpm", 0)
        try:
            expected_min = int(duration["min"]) * int(wpm)
            expected_max = int(duration["max"]) * int(wpm)
            if min_words > expected_max or max_words < expected_min:
                issues.append(
                    Issue(
                        "WARNING",
                        str(manifest_path),
                        f"Word budget {min_words}–{max_words} không giao với target {expected_min}–{expected_max}.",
                    )
                )
        except (KeyError, TypeError, ValueError):
            issues.append(Issue("ERROR", str(product_path), "Target duration/narration_wpm không hợp lệ."))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("products", nargs="+", type=Path)
    args = parser.parse_args()
    error_count = 0
    for product in args.products:
        issues = validate_product(product)
        print(f"\n[{product}]")
        if not issues:
            print("OK")
            continue
        for issue in issues:
            print(f"{issue.level}: {issue.location}: {issue.message}")
            error_count += issue.level == "ERROR"
    if error_count:
        print(f"\nValidation failed with {error_count} error(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

