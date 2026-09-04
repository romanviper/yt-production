#!/usr/bin/env python3
"""Validate product state, hard boundaries, and active context packets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from scripts.common import read_json, sha256
    from scripts.draft_lifecycle_contract import validate_canonical_draft_lifecycle
    from scripts.material_contract import validate_materials_file
    from scripts.outline_contract import validate_outline_contract
    from scripts.story_plan_contract import is_direct_authorship_outline, verify_narration_pack
    from scripts.task import verify_active_pointer, verify_task
    from scripts.voice_profile_contract import validate_voice_profile
except ModuleNotFoundError:
    from common import read_json, sha256
    from draft_lifecycle_contract import validate_canonical_draft_lifecycle
    from material_contract import validate_materials_file
    from outline_contract import validate_outline_contract
    from story_plan_contract import is_direct_authorship_outline, verify_narration_pack
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

    material_path = product_dir / "01_research" / "material-ledger.json"
    if material_path.is_file():
        for error in validate_materials_file(
            material_path,
            allowed_claim_ids=claim_ids,
            allowed_source_ids=source_ids,
            require_source_relation=False,
            prefix="global material",
        ):
            issues.append(Issue("ERROR", str(material_path), error))

    outline = safe_json(outline_path, issues)
    if outline.get("sections"):
        for message in validate_outline_contract(outline, claim_ids, product.get("target")):
            issues.append(Issue("ERROR", str(outline_path), message))
    section_ids = {
        section.get("id")
        for section in outline.get("sections", [])
        if isinstance(section, dict) and section.get("id")
    }
    direct_authorship = is_direct_authorship_outline(outline)
    outline_cycle = outline.get("cycle_id")

    section_root = product_dir / "03_sections"
    if outline.get("status") == "approved":
        if not voice_profile_path.is_file():
            issues.append(Issue("ERROR", str(voice_profile_path), "Approved outline requires voice profile."))
        else:
            for message in validate_voice_profile(voice_profile_path.read_text(encoding="utf-8")):
                issues.append(Issue("ERROR", str(voice_profile_path), message))

        full_materialization_expected = (
            product.get("status") == "sections_materialized"
            or product.get("production_cycle", {}).get("status") == "sections_materialized"
        )
        for section_id in section_ids:
            root = section_root / str(section_id)
            required = ["section.json", "brief.md", "evidence-pack.json", "continuity-in.md"]
            required += ["narration-pack.json"] if direct_authorship else ["story-plan.json"]
            materialized = any((root / name).is_file() for name in required)
            if not materialized:
                if full_materialization_expected:
                    for name in required:
                        issues.append(Issue("ERROR", str(root / name), "Declared full materialization is missing section artifact."))
                continue
            for name in required:
                if not (root / name).is_file():
                    issues.append(Issue("ERROR", str(root / name), "Materialized section is incomplete."))
            state_path = root / "section.json"
            if not state_path.is_file():
                continue
            state = safe_json(state_path, issues)
            if direct_authorship:
                mission = state.get("mission")
                if not isinstance(mission, str) or not mission.strip():
                    issues.append(Issue("ERROR", str(state_path), "Direct-authorship section requires a non-empty mission."))
                if state.get("cycle_id") != outline_cycle:
                    issues.append(
                        Issue(
                            "ERROR",
                            str(state_path),
                            f"Materialized section must match current outline cycle {outline_cycle}; found {state.get('cycle_id')}.",
                        )
                    )
                elif state.get("outline_sha256") != sha256(outline_path):
                    issues.append(Issue("ERROR", str(state_path), "Materialized section is stale relative to approved outline."))
                for message in validate_canonical_draft_lifecycle(product_dir, str(section_id), state):
                    issues.append(Issue("ERROR", str(root / "draft.md"), message))
            if state.get("status") == "approved" and state.get("human_approved") is not True:
                issues.append(Issue("ERROR", str(state_path), "Approved section requires human_approved=true."))
            if state.get("status") in {"ready_for_draft", "ready_for_review", "review_complete", "approved"}:
                for message in verify_narration_pack(product_dir, str(section_id)):
                    issues.append(Issue("ERROR", str(root / "narration-pack.json"), message))
            section_materials_path = root / "materials.json"
            if section_materials_path.is_file():
                ep_path = root / "evidence-pack.json"
                sec_claims = claim_ids
                sec_sources = source_ids
                if ep_path.is_file():
                    try:
                        ep_doc = read_json(ep_path)
                        sec_claims = {c["id"] for c in ep_doc.get("claims", []) if isinstance(c, dict) and "id" in c}
                        sec_sources = {s["id"] for s in ep_doc.get("sources", []) if isinstance(s, dict) and "id" in s}
                    except Exception:
                        pass
                for error in validate_materials_file(
                    section_materials_path,
                    allowed_claim_ids=sec_claims,
                    allowed_source_ids=sec_sources,
                    require_source_relation=False,
                    prefix=f"section {section_id} material",
                ):
                    issues.append(Issue("ERROR", str(section_materials_path), error))
            snapshot_path = root / "material-snapshot.json"
            if snapshot_path.is_file():
                try:
                    snap = read_json(snapshot_path)
                    if snap.get("schema_version") != 1:
                        issues.append(Issue("ERROR", str(snapshot_path), "material snapshot schema_version must be 1"))
                    if snap.get("section") != section_id:
                        issues.append(Issue("ERROR", str(snapshot_path), f"material snapshot section must be {section_id}"))
                    expected_mat_hash = snap.get("materials_sha256")
                    if section_materials_path.is_file():
                        actual_mat_hash = sha256(section_materials_path)
                        if expected_mat_hash != actual_mat_hash:
                            issues.append(Issue("ERROR", str(snapshot_path), f"material snapshot hash mismatch: snapshot has {expected_mat_hash}, materials.json has {actual_mat_hash}"))
                except Exception as exc:
                    issues.append(Issue("ERROR", str(snapshot_path), f"invalid material snapshot: {exc}"))

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
