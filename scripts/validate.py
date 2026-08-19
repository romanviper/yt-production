#!/usr/bin/env python3
"""Validate product state, modular boundaries, and active context packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.common import read_json, sha256
    from scripts.outline_contract import validate_outline_contract
    from scripts.story_plan_contract import verify_narration_pack
    from scripts.task import verify_active_pointer, verify_task
    from scripts.voice_profile_contract import validate_voice_profile
except ModuleNotFoundError:
    from common import read_json, sha256
    from outline_contract import validate_outline_contract
    from story_plan_contract import verify_narration_pack
    from task import verify_active_pointer, verify_task
    from voice_profile_contract import validate_voice_profile


@dataclass(frozen=True)
class Issue:
    level: str
    location: str
    message: str


def safe_json(path: Path, issues: list[Issue]) -> dict:
    if not path.is_file():
        issues.append(Issue("ERROR", str(path), "Missing required file."))
        return {}
    try:
        return read_json(path)
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        issues.append(Issue("ERROR", str(path), f"Invalid JSON: {exc}"))
        return {}


def _material_aware_outline_errors(product_dir: Path, outline: dict, claim_ids: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    architecture = outline.get("script_architecture", {})
    if architecture.get("story_material_contract_version") != 1:
        return issues

    material_path = product_dir / "01_research" / "material-ledger.json"
    if not material_path.is_file():
        return [Issue("ERROR", str(material_path), "Material-aware outline requires a material ledger.")]
    try:
        material_doc = read_json(material_path)
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        return [Issue("ERROR", str(material_path), f"Invalid material ledger: {exc}")]
    materials = {
        item.get("id"): item
        for item in material_doc.get("materials", [])
        if isinstance(item, dict) and item.get("id")
    }
    if material_doc.get("status") != "complete":
        issues.append(Issue("ERROR", str(material_path), "Material-aware outline requires a complete material ledger."))

    for section in outline.get("sections", []):
        if not isinstance(section, dict):
            continue
        section_id = section.get("id", "?")
        for field in ["audience_experience", "transition"]:
            if not isinstance(section.get(field), str) or not section[field].strip():
                issues.append(Issue("ERROR", f"02_outline/outline.json#{section_id}", f"Material-aware section requires {field}."))
        material_ids = section.get("material_ids")
        if not isinstance(material_ids, list) or not material_ids or not all(isinstance(item, str) and item for item in material_ids):
            issues.append(Issue("ERROR", f"02_outline/outline.json#{section_id}", "Material-aware section requires material_ids."))
            continue
        unknown = [material_id for material_id in material_ids if material_id not in materials]
        if unknown:
            issues.append(Issue("ERROR", f"02_outline/outline.json#{section_id}", "Unknown material IDs: " + ", ".join(unknown)))
        section_claims = set(section.get("claim_ids", []))
        unknown_claims = sorted(section_claims - claim_ids)
        if unknown_claims:
            issues.append(Issue("ERROR", f"02_outline/outline.json#{section_id}", "Unknown claim IDs: " + ", ".join(unknown_claims)))
        for material_id in material_ids:
            material = materials.get(material_id)
            if not material:
                continue
            linked = set(material.get("claim_ids", []))
            unknown_links = sorted(linked - claim_ids)
            if unknown_links:
                issues.append(
                    Issue(
                        "ERROR",
                        f"01_research/material-ledger.json#{material_id}",
                        "Material references unknown claims: " + ", ".join(unknown_links),
                    )
                )
            if linked and not linked.intersection(section_claims):
                issues.append(
                    Issue(
                        "ERROR",
                        f"02_outline/outline.json#{section_id}",
                        f"Material {material_id} has no linked claim inside the section evidence ceiling.",
                    )
                )
    return issues


def validate_product(product_dir: Path) -> list[Issue]:
    product_dir = product_dir.resolve()
    issues: list[Issue] = []
    product_path = product_dir / "product.json"
    brief_path = product_dir / "00_brief" / "product-brief.md"
    benchmark_path = product_dir / "00_brief" / "benchmark.md"
    plan_path = product_dir / "01_research" / "plan.json"
    source_path = product_dir / "01_research" / "source-index.json"
    claim_path = product_dir / "01_research" / "claim-ledger.json"
    outline_path = product_dir / "02_outline" / "outline.json"
    bible_path = product_dir / "02_outline" / "story-bible.md"
    voice_profile_path = product_dir / "02_outline" / "voice-profile.md"

    product = safe_json(product_path, issues)
    for path in [brief_path, benchmark_path, bible_path]:
        if not path.is_file():
            issues.append(Issue("ERROR", str(path), "Missing required artifact."))
    if product and product.get("slug") != product_dir.name:
        issues.append(Issue("ERROR", str(product_path), "Product slug must equal directory name."))
    if product and "target" not in product:
        issues.append(Issue("ERROR", str(product_path), "Missing target duration/wpm."))

    plan = safe_json(plan_path, issues)
    unit_ids: set[str] = set()
    for index, unit in enumerate(plan.get("workstreams", [])):
        unit_id = unit.get("id", "")
        if not re.fullmatch(r"WS\d{2}", unit_id):
            issues.append(Issue("ERROR", f"{plan_path}#{index}", f"Invalid workstream ID: {unit_id}"))
        if unit_id in unit_ids:
            issues.append(Issue("ERROR", f"{plan_path}#{index}", f"Duplicate workstream: {unit_id}"))
        unit_ids.add(unit_id)

    sources_doc = safe_json(source_path, issues)
    claims_doc = safe_json(claim_path, issues)
    source_ids: set[str] = set()
    for index, source in enumerate(sources_doc.get("sources", [])):
        source_id = source.get("id", "")
        if not re.fullmatch(r"SRC-\d{4}", source_id):
            issues.append(Issue("ERROR", f"{source_path}#{index}", f"Invalid source ID: {source_id}"))
        if source_id in source_ids:
            issues.append(Issue("ERROR", f"{source_path}#{index}", f"Duplicate source ID: {source_id}"))
        source_ids.add(source_id)
        if source.get("status") == "reviewed" and not source.get("locators"):
            issues.append(Issue("ERROR", f"{source_path}#{index}", "Reviewed source requires locators."))

    claim_ids: set[str] = set()
    for index, claim in enumerate(claims_doc.get("claims", [])):
        claim_id = claim.get("id", "")
        if not re.fullmatch(r"CLM-\d{4}", claim_id):
            issues.append(Issue("ERROR", f"{claim_path}#{index}", f"Invalid claim ID: {claim_id}"))
        if claim_id in claim_ids:
            issues.append(Issue("ERROR", f"{claim_path}#{index}", f"Duplicate claim ID: {claim_id}"))
        claim_ids.add(claim_id)
        for source_id in claim.get("sources", []):
            if source_id not in source_ids:
                issues.append(Issue("ERROR", f"{claim_path}#{index}", f"Missing source: {source_id}"))
        if claim.get("status") in {"supported", "qualified"} and not claim.get("sources"):
            issues.append(Issue("ERROR", f"{claim_path}#{index}", "Supported/qualified claim requires sources."))

    outline = safe_json(outline_path, issues)
    if outline.get("sections"):
        for message in validate_outline_contract(outline, claim_ids, product.get("target")):
            issues.append(Issue("ERROR", str(outline_path), message))
    issues.extend(_material_aware_outline_errors(product_dir, outline, claim_ids))
    section_ids = {section.get("id") for section in outline.get("sections", []) if isinstance(section, dict) and section.get("id")}
    material_aware = outline.get("script_architecture", {}).get("story_material_contract_version") == 1
    outline_cycle = outline.get("cycle_id")

    section_root = product_dir / "03_sections"
    if outline.get("status") == "approved":
        if not voice_profile_path.is_file():
            issues.append(Issue("ERROR", str(voice_profile_path), "Approved outline requires voice profile."))
        else:
            for message in validate_voice_profile(voice_profile_path.read_text(encoding="utf-8")):
                issues.append(Issue("ERROR", str(voice_profile_path), message))

        sections_need_sync = product.get("stages", {}).get("sections") in {"human_sync_required", "ready_to_materialize"}
        if not sections_need_sync:
            for section_id in section_ids:
                root = section_root / section_id
                required = ["section.json", "brief.md", "evidence-pack.json", "continuity-in.md"]
                required += ["material-pack.json", "narration-pack.json"] if material_aware else ["story-plan.json"]
                for name in required:
                    if not (root / name).is_file():
                        issues.append(Issue("ERROR", str(root / name), "Approved outline requires materialized section."))
                state_path = root / "section.json"
                if not state_path.is_file():
                    continue
                state = safe_json(state_path, issues)
                if material_aware:
                    if state.get("cycle_id") != outline_cycle:
                        issues.append(
                            Issue(
                                "ERROR",
                                str(state_path),
                                f"Approved outline requires materialized section for current cycle {outline_cycle}; found {state.get('cycle_id')}.",
                            )
                        )
                    elif state.get("outline_sha256") != sha256(outline_path):
                        issues.append(Issue("ERROR", str(state_path), "Materialized section is stale relative to approved outline."))
                if state.get("status") == "approved" and state.get("human_approved") is not True:
                    issues.append(Issue("ERROR", str(state_path), "Approved section requires human_approved=true."))
                if state.get("status") in {"ready_for_draft", "ready_for_review", "review_complete", "approved"}:
                    for message in verify_narration_pack(product_dir, section_id):
                        issues.append(Issue("ERROR", str(root / "narration-pack.json"), message))

    validated_task_ids: set[str] = set()
    active_path = product_dir / "tasks" / "ACTIVE.json"
    if active_path.is_file():
        active = safe_json(active_path, issues)
        task_id = active.get("task_id")
        if task_id:
            try:
                for message in verify_active_pointer(product_dir, task_id):
                    issues.append(Issue("ERROR", str(active_path), message))
                for message in verify_task(product_dir, task_id):
                    issues.append(Issue("ERROR", str(active_path), message))
                validated_task_ids.add(task_id)
            except (FileNotFoundError, KeyError, json.JSONDecodeError, ValueError) as exc:
                issues.append(Issue("ERROR", str(active_path), f"Invalid active task: {exc}"))

    tasks_dir = product_dir / "tasks"
    if tasks_dir.is_dir():
        for work_path in sorted(tasks_dir.glob("T*/work-order.json")):
            task_id = work_path.parent.name
            if task_id in validated_task_ids:
                continue
            try:
                work = read_json(work_path)
            except (json.JSONDecodeError, ValueError, OSError) as exc:
                issues.append(Issue("ERROR", str(work_path), f"Invalid task work order: {exc}"))
                continue
            if work.get("state") != "ready_for_review":
                continue
            try:
                for message in verify_task(product_dir, task_id):
                    issues.append(Issue("ERROR", str(work_path), message))
            except (FileNotFoundError, KeyError, json.JSONDecodeError, ValueError) as exc:
                issues.append(Issue("ERROR", str(work_path), f"Invalid submitted task: {exc}"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("products", nargs="+", type=Path)
    args = parser.parse_args()
    errors = 0
    for product in args.products:
        issues = validate_product(product)
        print(f"\n[{product}]")
        if not issues:
            print("OK")
        for issue in issues:
            print(f"{issue.level}: {issue.location}: {issue.message}")
            errors += issue.level == "ERROR"
    if errors:
        print(f"\nValidation failed with {errors} error(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
