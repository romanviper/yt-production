#!/usr/bin/env python3
"""Create, inspect, and verify atomic AI work orders."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.common import load_registry, narration_text, product_relative, read_json, sha256, word_count, write_json
    from scripts.consolidate_research import ensure_consolidated
    from scripts.context_packet import compile_packet
    from scripts.draft_lifecycle_contract import (
        record_submitted_prose,
        validate_evidence_trace,
        validate_required_evidence_resolution,
    )
    from scripts.lifecycle import (
        apply_research_submission,
        apply_section_submission,
        cancel_live_task_conflicts,
        clear_active_pointer,
        heal_active_pointer,
        live_task_conflicts,
        task_submit_errors,
        task_transition_errors,
    )
    from scripts.draft_evidence import preflight_section_materials
    from scripts.operator_brief import empty_brief, render_brief, validate_brief_file
    from scripts.outcome_eval_contract import validate_outcome_review
    from scripts.outline_contract import MAX_SECTION_WORDS, validate_outline_contract
    from scripts.packet_contract import validate_packet_contract
    from scripts.research_plan_contract import validate_research_plan_contract
    from scripts.story_plan_contract import is_direct_authorship_outline, validate_story_plan
    from scripts.voice_profile_contract import validate_voice_profile
except ModuleNotFoundError:  # Direct execution: python scripts/task.py
    from common import load_registry, narration_text, product_relative, read_json, sha256, word_count, write_json
    from consolidate_research import ensure_consolidated
    from context_packet import compile_packet
    from draft_evidence import preflight_section_materials
    from draft_lifecycle_contract import record_submitted_prose, validate_evidence_trace, validate_required_evidence_resolution
    from lifecycle import (
        apply_research_submission,
        apply_section_submission,
        cancel_live_task_conflicts,
        clear_active_pointer,
        heal_active_pointer,
        live_task_conflicts,
        task_submit_errors,
        task_transition_errors,
    )
    from operator_brief import empty_brief, render_brief, validate_brief_file
    from outcome_eval_contract import validate_outcome_review
    from outline_contract import MAX_SECTION_WORDS, validate_outline_contract
    from packet_contract import validate_packet_contract
    from research_plan_contract import validate_research_plan_contract
    from story_plan_contract import is_direct_authorship_outline, validate_story_plan
    from voice_profile_contract import validate_voice_profile


def next_task_id(product_dir: Path, operation: str, section: str | None, unit: str | None) -> str:
    tasks_dir = product_dir / "tasks"
    numbers = []
    if tasks_dir.is_dir():
        for path in tasks_dir.iterdir():
            match = re.match(r"T(\d{4})-", path.name)
            if match:
                numbers.append(int(match.group(1)))
    suffix = section or unit or operation.replace("_", "-")
    return f"T{max(numbers, default=0) + 1:04d}-{operation.replace('_', '-')}-{suffix}"


def active_path(product_dir: Path) -> Path:
    return product_dir / "tasks" / "ACTIVE.json"


def revision_passes_used_in_current_cycle(section_state: dict) -> int:
    usage = section_state.get("revision_pass")
    if not isinstance(usage, dict) or usage.get("cycle_id") != section_state.get("cycle_id"):
        return 0
    return int(usage.get("count", 0))


def create_task(
    product_dir: Path,
    operation: str,
    section: str | None,
    unit: str | None,
    replace: bool,
    execution_runtime: str | None = None,
) -> dict:
    product_dir = product_dir.resolve()
    heal_active_pointer(product_dir)

    if operation == "revise_section" and section:
        section_state = read_json(product_dir / "03_sections" / section / "section.json")
        if revision_passes_used_in_current_cycle(section_state) >= 1:
            raise ValueError(
                f"Section {section} already used its one diagnosed revision pass; route a blocker or start a new production cycle."
            )

    if operation == "draft_section" and section:
        outline_path = product_dir / "02_outline" / "outline.json"
        if outline_path.is_file():
            outline = read_json(outline_path)
            if is_direct_authorship_outline(outline):
                preflight = preflight_section_materials(product_dir, section)
                status = preflight.get("status")
                if status != "material_ready":
                    if status == "needs_evidence_resolution":
                        raise ValueError(
                            f"Section {section} material readiness preflight failed (needs_evidence_resolution): "
                            "route evidence_resolution before creating a draft_section task."
                        )
                    raise ValueError(
                        f"Section {section} material readiness preflight blocked: {preflight.get('reason', 'insufficient evidence')}"
                    )

    if operation == "research_synthesis":
        ensure_consolidated(product_dir)

    task_id = next_task_id(product_dir, operation, section, unit)
    packet, context = compile_packet(product_dir, operation, task_id, section, unit, execution_runtime)

    conflicts = live_task_conflicts(product_dir, operation, section, unit)
    if conflicts and not replace:
        raise ValueError(
            "Live task conflict on requested scope: "
            + ", ".join(conflicts)
            + ". Close/cancel it or use --replace intentionally."
        )
    if conflicts:
        cancel_live_task_conflicts(
            product_dir,
            operation,
            section,
            unit,
            reason=f"router replacement by {task_id}",
            replacement=task_id,
        )

    task_dir = product_dir / "tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=False)
    packet_path = task_dir / "packet.json"
    context_path = task_dir / "context.md"
    write_json(packet_path, packet)
    with context_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(context)
    operator_brief_path = product_dir / packet["operator_brief_path"]
    write_json(operator_brief_path, empty_brief())

    work_order = {
        "schema_version": 1,
        "authority": packet["authority"],
        "id": task_id,
        "product": product_dir.name,
        "operation": operation,
        "target": {"section": section, "unit": unit},
        "state": "ready",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "context_packet": product_relative(product_dir, context_path),
        "packet_manifest": product_relative(product_dir, packet_path),
        "allowed_write_paths": packet["allowed_write_paths"],
        "outputs": packet["operation_outputs"],
        "optional_outputs": packet.get("optional_operation_outputs", []),
        "report_path": packet["report_path"],
        "operator_brief_path": packet["operator_brief_path"],
    }
    if "evidence_access" in packet:
        work_order["evidence_access"] = packet["evidence_access"]
        if "material_snapshot_sha256" in packet["evidence_access"]:
            work_order["material_snapshot_sha256"] = packet["evidence_access"]["material_snapshot_sha256"]
    if "review_contract_version" in packet:
        work_order["review_contract_version"] = packet["review_contract_version"]
    if "execution_runtime" in packet:
        work_order["execution_runtime"] = packet["execution_runtime"]
        work_order["runtime_owned_paths"] = packet.get("runtime_owned_paths", [])
    work_path = task_dir / "work-order.json"
    write_json(work_path, work_order)
    errors = verify_task(product_dir, task_id)
    if errors:
        raise ValueError("Router produced invalid task artifacts: " + "; ".join(errors))
    write_json(
        active_path(product_dir),
        {
            "task_id": task_id,
            "work_order": product_relative(product_dir, work_path),
            "context_packet": product_relative(product_dir, context_path),
        },
    )
    return work_order


def verify_task(product_dir: Path, task_id: str, *, state_override: str | None = None) -> list[str]:
    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    work = read_json(task_dir / "work-order.json")
    packet = read_json(task_dir / "packet.json")
    errors = validate_packet_contract(packet, task_dir / "context.md")
    if errors:
        return errors
    effective_state = state_override or work.get("state")
    task_owned_paths = set(packet.get("operation_outputs", [])) | set(packet.get("optional_operation_outputs", []))
    if effective_state in {"ready", "in_progress"}:
        for record in packet["inputs"]:
            if record["path"] in task_owned_paths:
                continue
            path = product_dir / record["path"]
            if not path.is_file():
                errors.append(f"missing input: {record['path']}")
            elif sha256(path) != record["sha256"]:
                errors.append(f"stale input: {record['path']}")
    if packet["estimated_context_tokens"] > packet["max_context_tokens"]:
        errors.append("context budget exceeded")
    if work["allowed_write_paths"] != packet["allowed_write_paths"]:
        errors.append("work-order scope differs from packet")
    if work.get("outputs") != packet.get("operation_outputs"):
        errors.append("work-order required outputs differ from packet")
    if work.get("optional_outputs", []) != packet.get("optional_operation_outputs", []):
        errors.append("work-order optional outputs differ from packet")
    if work.get("evidence_access") != packet.get("evidence_access"):
        errors.append("work-order evidence access differs from packet")
    if work.get("review_contract_version") != packet.get("review_contract_version"):
        errors.append("work-order review contract version differs from packet")
    if work.get("authority") != "product_agent" or work.get("authority") != packet.get("authority"):
        errors.append("invalid or mismatched product task authority")
    expected_manifest = f"tasks/{task_id}/packet.json"
    expected_context = f"tasks/{task_id}/context.md"
    if work.get("id") != task_id or packet.get("task_id") != task_id:
        errors.append("task id differs between task directory, work order and packet")
    if work.get("product") != product_dir.name or packet.get("product") != product_dir.name:
        errors.append("product differs between directory, work order and packet")
    if work.get("operation") != packet.get("operation") or work.get("target") != packet.get("target"):
        errors.append("operation target differs between work order and packet")
    if work.get("execution_runtime") != packet.get("execution_runtime"):
        errors.append("execution runtime differs between work order and packet")
    if work.get("runtime_owned_paths", []) != packet.get("runtime_owned_paths", []):
        errors.append("runtime-owned paths differ between work order and packet")
    if work.get("packet_manifest") != expected_manifest or work.get("context_packet") != expected_context:
        errors.append("work order must point to its router-generated packet and context")
    expected_snapshot_hash = work.get("material_snapshot_sha256")
    if expected_snapshot_hash:
        section = work.get("target", {}).get("section")
        snapshot_path = product_dir / "03_sections" / str(section) / "material-snapshot.json"
        if not snapshot_path.is_file():
            errors.append(f"task {task_id} material snapshot is missing")
        elif sha256(snapshot_path) != expected_snapshot_hash:
            errors.append(f"task {task_id} material snapshot is stale / mutated since task creation")
    return errors


def verify_active_pointer(product_dir: Path, task_id: str) -> list[str]:
    """Validate routing metadata only. ACTIVE.json is never task execution authority."""

    product_dir = product_dir.resolve()
    path = active_path(product_dir)
    if not path.is_file():
        return ["task is not routed: missing tasks/ACTIVE.json"]
    try:
        active = read_json(path)
    except (json.JSONDecodeError, ValueError, OSError) as exc:
        return [f"invalid tasks/ACTIVE.json: {exc}"]

    errors: list[str] = []
    if active.get("task_id") != task_id:
        errors.append(f"task {task_id} is not the routed task")
    expected_work = f"tasks/{task_id}/work-order.json"
    expected_context = f"tasks/{task_id}/context.md"
    if active.get("work_order") != expected_work or active.get("context_packet") != expected_context:
        errors.append("ACTIVE.json must point to the task's router-generated work order and context")
    return errors


def submit_task(product_dir: Path, task_id: str) -> list[str]:
    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    work_path = task_dir / "work-order.json"
    work = read_json(work_path)
    packet = read_json(task_dir / "packet.json")
    errors = task_submit_errors(work.get("state"))
    errors.extend(verify_task(product_dir, task_id))
    if work.get("operation") in {"draft_section", "review_section", "revise_section"}:
        errors.extend(validate_evidence_trace(product_dir, task_id))
    if work.get("operation") in {"draft_section", "review_section", "revise_section"}:
        errors.extend(validate_required_evidence_resolution(product_dir, task_id))
    if errors:
        return errors
    changed_outputs = 0
    for record in packet.get("output_baselines", []):
        path = product_dir / record["path"]
        required = record.get("required", True)
        if not path.is_file():
            if required:
                errors.append(f"missing output: {record['path']}")
        elif sha256(path) != record.get("sha256"):
            changed_outputs += 1
    report = task_dir / "report.md"
    if not report.is_file():
        errors.append(f"missing output: tasks/{task_id}/report.md")
    operator_brief = product_dir / packet["operator_brief_path"]
    errors.extend(validate_brief_file(operator_brief))
    if operator_brief.is_file():
        try:
            if read_json(operator_brief).get("status") != "ready_for_review":
                errors.append("submitted task operator brief status must be ready_for_review")
        except (json.JSONDecodeError, ValueError):
            pass
    if not changed_outputs:
        errors.append("no declared artifact changed from its task baseline")
    errors.extend(validate_output_contract(product_dir, work))
    if errors:
        return errors
    work["state"] = "ready_for_review"
    work["submitted_at"] = datetime.now(timezone.utc).isoformat()
    work["updated_at"] = work["submitted_at"]
    write_json(work_path, work)
    apply_research_submission(product_dir, work["operation"], work.get("target", {}).get("unit"))
    apply_section_submission(product_dir, work["operation"], work.get("target", {}).get("section"))
    if work.get("operation") == "review_section":
        section = str(work.get("target", {}).get("section") or "")
        state_path = product_dir / "03_sections" / section / "section.json"
        state = read_json(state_path)
        review_path = product_dir / "03_sections" / section / "review.md"
        state["review_provenance"] = {
            "task_id": task_id,
            "contract_version": int(work.get("review_contract_version", 1)),
            "review_sha256": sha256(review_path),
        }
        write_json(state_path, state)
    if work.get("operation") in {"draft_section", "revise_section"}:
        record_submitted_prose(product_dir, task_id)
    clear_active_pointer(product_dir, task_id, reason="task submitted; routing returned to idle")
    return []


def _validate_optional_materials(root: Path, unit: str, source_ids: list[str], claim_ids: list[str]) -> list[str]:
    errors: list[str] = []
    path = root / "materials.json"
    if not path.is_file():
        return errors
    document = read_json(path)
    if document.get("status") == "not_started":
        return errors
    if document.get("status") != "complete":
        return ["optional workstream materials status must be complete or not_started"]
    materials = document.get("materials", [])
    if not isinstance(materials, list):
        return ["optional workstream materials must be a list"]
    expected_material = re.compile(rf"{re.escape(unit)}-MAT-\d{{3}}")
    seen: set[str] = set()
    for item in materials:
        if not isinstance(item, dict):
            errors.append("optional material must be an object")
            continue
        material_id = item.get("id", "")
        if not expected_material.fullmatch(material_id) or material_id in seen:
            errors.append(f"invalid or duplicate namespaced material ID: {material_id or '?'}")
            continue
        seen.add(material_id)
        for claim_id in item.get("claim_ids", []) if isinstance(item.get("claim_ids", []), list) else []:
            if claim_id not in claim_ids:
                errors.append(f"material {material_id} references unknown local claim: {claim_id}")
        refs = item.get("source_refs", [])
        if refs is not None and not isinstance(refs, list):
            errors.append(f"material {material_id} source_refs must be a list")
            refs = []
        for ref in refs:
            if not isinstance(ref, dict) or ref.get("source_id") not in source_ids:
                errors.append(f"material {material_id} references unknown local source")
                continue
            locators = ref.get("locators", [])
            if not isinstance(locators, list) or not all(isinstance(loc, str) and loc.strip() for loc in locators):
                errors.append(f"material {material_id} source_ref locators must be strings")
        limitations = item.get("limitations", [])
        if limitations is not None and (
            not isinstance(limitations, list)
            or not all(isinstance(value, str) and value.strip() for value in limitations)
        ):
            errors.append(f"material {material_id} limitations must be a list of strings")
    return errors


def validate_output_contract(product_dir: Path, work: dict) -> list[str]:
    operation = work["operation"]
    target = work.get("target", {})
    errors: list[str] = []
    try:
        if operation == "research_plan":
            plan = read_json(product_dir / "01_research" / "plan.json")
            errors.extend(validate_research_plan_contract(plan))
            if plan.get("status") == "approved":
                errors.append("Agent may not self-approve research plan")
        elif operation == "research_workstream":
            unit = target["unit"]
            root = product_dir / "01_research" / "workstreams" / unit
            sources_doc = read_json(root / "sources.json")
            claims_doc = read_json(root / "claims.json")
            sources = sources_doc.get("sources", [])
            claims = claims_doc.get("claims", [])
            if sources_doc.get("status") != "complete":
                errors.append("workstream sources status must be complete")
            if claims_doc.get("status") != "complete":
                errors.append("workstream claims status must be complete")
            if not sources:
                errors.append("workstream must contain at least one source")
            if not claims:
                errors.append("workstream must contain at least one claim")
            source_ids = [item.get("id") for item in sources]
            expected_source = re.compile(rf"{re.escape(unit)}-SRC-\d{{3}}")
            for item in sources:
                source_id = item.get("id", "")
                if not expected_source.fullmatch(source_id):
                    errors.append(f"invalid namespaced source ID: {source_id or '?'}")
                missing = [field for field in ["title", "type", "authority", "locators", "status", "limitations"] if not item.get(field)]
                if missing:
                    errors.append(f"source {source_id or '?'} missing: {', '.join(missing)}")
            if len(source_ids) != len(set(source_ids)):
                errors.append("workstream has duplicate source IDs")
            expected_claim = re.compile(rf"{re.escape(unit)}-CLM-\d{{3}}")
            for item in claims:
                claim_id = item.get("id", "")
                if not expected_claim.fullmatch(claim_id):
                    errors.append(f"invalid namespaced claim ID: {claim_id or '?'}")
                missing = [field for field in ["statement", "type", "confidence", "status", "counterevidence"] if item.get(field) is None or item.get(field) == ""]
                if missing:
                    errors.append(f"claim {claim_id or '?'} missing: {', '.join(missing)}")
                for source_id in item.get("sources", []):
                    if source_id not in source_ids:
                        errors.append(f"claim {claim_id or '?'} references unknown local source: {source_id}")
                if item.get("status") in {"supported", "qualified"} and not item.get("sources"):
                    errors.append(f"claim {claim_id or '?'} needs sources for status {item.get('status')}")
            claim_ids = [item.get("id") for item in claims]
            if len(claim_ids) != len(set(claim_ids)):
                errors.append("workstream has duplicate claim IDs")
            errors.extend(_validate_optional_materials(root, str(unit), source_ids, claim_ids))
            synthesis_text = (root / "synthesis.md").read_text(encoding="utf-8")
            if "Status: complete" not in synthesis_text:
                errors.append("workstream synthesis status must be complete")
            if word_count(synthesis_text) > 2500:
                errors.append("workstream synthesis exceeds 2,500 words")
        elif operation == "research_synthesis":
            sources_doc = read_json(product_dir / "01_research" / "source-index.json")
            claims_doc = read_json(product_dir / "01_research" / "claim-ledger.json")
            if sources_doc.get("status") != "complete":
                errors.append("global source index status must be complete")
            if claims_doc.get("status") != "complete":
                errors.append("global claim ledger status must be complete")
            for item in sources_doc.get("sources", []):
                if not item.get("provenance"):
                    errors.append(f"global source {item.get('id', '?')} missing workstream provenance")
            for item in claims_doc.get("claims", []):
                if not item.get("provenance"):
                    errors.append(f"global claim {item.get('id', '?')} missing workstream provenance")
            if "Status: complete" not in (product_dir / "01_research" / "research-synthesis.md").read_text(encoding="utf-8"):
                errors.append("research synthesis status must be complete")
        elif operation == "outline":
            outline = read_json(product_dir / "02_outline" / "outline.json")
            product = read_json(product_dir / "product.json")
            claims_doc = read_json(product_dir / "01_research" / "claim-ledger.json")
            known_claim_ids = {item.get("id") for item in claims_doc.get("claims", []) if item.get("id")}
            errors.extend(validate_outline_contract(outline, known_claim_ids, product.get("target"), require_current=True))
            expected_cycle = product.get("production_cycle", {}).get("id")
            if expected_cycle and outline.get("cycle_id") != expected_cycle:
                errors.append(f"outline cycle_id must match current product cycle {expected_cycle}")
            architecture = outline.get("script_architecture", {})
            if architecture.get("writer_authorship_contract_version") != 1:
                errors.append("new/revised outline must set script_architecture.writer_authorship_contract_version=1")
            for section in outline.get("sections", []):
                if not isinstance(section.get("transition"), str) or not section["transition"].strip():
                    errors.append(f"outline section {section.get('id', '?')} transition is required")
            voice_profile = (product_dir / "02_outline" / "voice-profile.md").read_text(encoding="utf-8")
            errors.extend(validate_voice_profile(voice_profile))
            if outline.get("status") == "approved":
                errors.append("Agent may not self-approve outline")
            if "Status: approved" in voice_profile:
                errors.append("Agent may not self-approve voice profile")
        elif operation == "design_section":
            section = target["section"]
            root = product_dir / "03_sections" / section
            story_plan = read_json(root / "story-plan.json")
            evidence = read_json(root / "evidence-pack.json")
            state = read_json(root / "section.json")
            claim_ids = {item.get("id") for item in evidence.get("claims", []) if item.get("id")}
            errors.extend(validate_story_plan(story_plan, claim_ids, state.get("target_words"), require_current=True))
            if story_plan.get("status") == "approved":
                errors.append("Agent may not self-approve story plan")
        elif operation in {"draft_section", "revise_section"}:
            section = target["section"]
            root = product_dir / "03_sections" / section
            draft_words = word_count(narration_text((root / "draft.md").read_text(encoding="utf-8"), section))
            if not 1 <= draft_words <= MAX_SECTION_WORDS:
                errors.append(f"draft word count must stay inside the 1–{MAX_SECTION_WORDS} production-unit hard cap")
            if word_count((root / "handoff.md").read_text(encoding="utf-8")) > 500:
                errors.append("section handoff exceeds 500 words")
        elif operation == "review_section":
            section = target["section"]
            review = product_dir / "03_sections" / section / "review.md"
            review_contract_version = int(work.get("review_contract_version", 1))
            strict_review = review_contract_version >= 2
            errors.extend(
                validate_outcome_review(
                    review.read_text(encoding="utf-8"),
                    require_mission_outcomes=strict_review,
                    require_production_gate=strict_review,
                    contract_version=review_contract_version,
                    section=section,
                )
            )
        elif operation == "integration_review":
            review = product_dir / "04_integration" / "review.md"
            change_map = read_json(product_dir / "04_integration" / "change-map.json")
            if word_count(review.read_text(encoding="utf-8")) < 20:
                errors.append("integration review is empty or non-diagnostic")
            if not isinstance(change_map.get("issues"), list):
                errors.append("integration change map requires an issues list")
        elif operation == "final_audit":
            audit = product_dir / "04_integration" / "final-audit.md"
            if word_count(audit.read_text(encoding="utf-8")) < 20:
                errors.append("final audit is empty or non-diagnostic")
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"output contract error: {exc}")
    return errors


def set_task_state(product_dir: Path, task_id: str, state: str) -> list[str]:
    product_dir = product_dir.resolve()
    work_path = product_dir / "tasks" / task_id / "work-order.json"
    work = read_json(work_path)
    errors = task_transition_errors(work.get("state"), state)
    if state in {"ready", "in_progress"}:
        errors.extend(verify_task(product_dir, task_id, state_override=state))
    if errors:
        return errors

    work["state"] = state
    work["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(work_path, work)
    if state in {"closed", "cancelled"}:
        clear_active_pointer(product_dir, task_id, reason=f"task {state}")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("product", type=Path)
    create.add_argument("operation", choices=sorted(load_registry()))
    create.add_argument("--section")
    create.add_argument("--unit")
    create.add_argument("--replace", action="store_true")
    create.add_argument("--runtime", choices=["legacy", "dsh"])
    show = sub.add_parser("show")
    show.add_argument("product", type=Path)
    verify = sub.add_parser("verify")
    verify.add_argument("product", type=Path)
    verify.add_argument("task_id")
    submit = sub.add_parser("submit")
    submit.add_argument("product", type=Path)
    submit.add_argument("task_id")
    brief = sub.add_parser("brief")
    brief.add_argument("product", type=Path)
    brief.add_argument("task_id", nargs="?")
    state = sub.add_parser("state")
    state.add_argument("product", type=Path)
    state.add_argument("task_id")
    state.add_argument("value", choices=["ready", "in_progress", "closed", "cancelled"])
    listing = sub.add_parser("list")
    listing.add_argument("product", type=Path)
    args = parser.parse_args()

    if args.command == "create":
        try:
            work = create_task(args.product, args.operation, args.section, args.unit, args.replace, args.runtime)
        except (ValueError, FileNotFoundError, FileExistsError, json.JSONDecodeError) as exc:
            parser.error(str(exc))
        print(json.dumps(work, ensure_ascii=False, indent=2))
        return 0
    if args.command == "show":
        heal_active_pointer(args.product.resolve())
        active = read_json(active_path(args.product.resolve()))
        context_ref = active.get("context_packet")
        if not context_ref:
            parser.error("No routed live task in tasks/ACTIVE.json")
        context = args.product.resolve() / context_ref
        print(context.read_text(encoding="utf-8"))
        return 0
    if args.command == "list":
        tasks_dir = args.product.resolve() / "tasks"
        for work_path in sorted(tasks_dir.glob("T*/work-order.json")) if tasks_dir.is_dir() else []:
            work = read_json(work_path)
            print(f"{work['id']}\t{work['state']}\t{work['operation']}\t{work.get('target', {})}")
        return 0
    if args.command == "brief":
        product = args.product.resolve()
        task_id = args.task_id
        if not task_id:
            heal_active_pointer(product)
            task_id = read_json(active_path(product)).get("task_id") if active_path(product).is_file() else None
        if not task_id:
            parser.error("No routed live task in tasks/ACTIVE.json")
        path = product / "tasks" / task_id / "operator-brief.json"
        errors = validate_brief_file(path)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print(render_brief(read_json(path)), end="")
        return 0
    if args.command == "state":
        errors = set_task_state(args.product, args.task_id, args.value)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print(f"{args.task_id}: {args.value}")
        return 0
    errors = submit_task(args.product, args.task_id) if args.command == "submit" else verify_task(args.product, args.task_id)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.command == "submit":
        brief_path = args.product.resolve() / "tasks" / args.task_id / "operator-brief.json"
        print(render_brief(read_json(brief_path)), end="")
    else:
        print("Task packet is fresh and within budget.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
