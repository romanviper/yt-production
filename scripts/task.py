#!/usr/bin/env python3
"""Create, inspect, and verify atomic AI work orders."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.common import load_registry, product_relative, read_json, sha256, word_count, write_json
    from scripts.context_packet import compile_packet
    from scripts.operator_brief import empty_brief, render_brief, validate_brief_file
    from scripts.research_plan_contract import validate_research_plan_contract
except ModuleNotFoundError:  # Direct execution: python scripts/task.py
    from common import load_registry, product_relative, read_json, sha256, word_count, write_json
    from context_packet import compile_packet
    from operator_brief import empty_brief, render_brief, validate_brief_file
    from research_plan_contract import validate_research_plan_contract


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


def create_task(product_dir: Path, operation: str, section: str | None, unit: str | None, replace: bool) -> dict:
    product_dir = product_dir.resolve()
    active_file = active_path(product_dir)
    if active_file.is_file() and not replace:
        active = read_json(active_file)
        existing = product_dir / active["work_order"]
        if existing.is_file() and read_json(existing).get("state") in {"ready", "in_progress"}:
            raise ValueError(f"Task {active['task_id']} còn active; close/cancel hoặc dùng --replace có chủ đích.")

    task_id = next_task_id(product_dir, operation, section, unit)
    task_dir = product_dir / "tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=False)
    packet, context = compile_packet(product_dir, operation, task_id, section, unit)
    packet_path = task_dir / "packet.json"
    context_path = task_dir / "context.md"
    write_json(packet_path, packet)
    context_path.write_text(context, encoding="utf-8")
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
        "acceptance_criteria": packet["acceptance_criteria"],
        "outputs": packet["operation_outputs"],
        "report_path": packet["report_path"],
        "operator_brief_path": packet["operator_brief_path"],
    }
    work_path = task_dir / "work-order.json"
    write_json(work_path, work_order)
    write_json(active_file, {"task_id": task_id, "work_order": product_relative(product_dir, work_path), "context_packet": product_relative(product_dir, context_path)})
    return work_order


def verify_task(product_dir: Path, task_id: str) -> list[str]:
    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    work = read_json(task_dir / "work-order.json")
    packet = read_json(task_dir / "packet.json")
    errors: list[str] = []
    for record in packet["inputs"]:
        path = product_dir / record["path"]
        if not path.is_file():
            errors.append(f"missing input: {record['path']}")
        elif sha256(path) != record["sha256"]:
            errors.append(f"stale input: {record['path']}")
    if packet["estimated_context_tokens"] > packet["max_context_tokens"]:
        errors.append("context budget exceeded")
    if work["allowed_write_paths"] != packet["allowed_write_paths"]:
        errors.append("work-order scope differs from packet")
    if work.get("authority") != "product_agent" or work.get("authority") != packet.get("authority"):
        errors.append("invalid or mismatched product task authority")
    return errors


def submit_task(product_dir: Path, task_id: str) -> list[str]:
    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    work_path = task_dir / "work-order.json"
    work = read_json(work_path)
    packet = read_json(task_dir / "packet.json")
    errors = verify_task(product_dir, task_id)
    changed_outputs = 0
    for record in packet.get("output_baselines", []):
        path = product_dir / record["path"]
        if not path.is_file():
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
    write_json(work_path, work)
    section = work.get("target", {}).get("section")
    if section:
        state_path = product_dir / "03_sections" / section / "section.json"
        state = read_json(state_path)
        if work["operation"] in {"draft_section", "revise_section"}:
            state["status"] = "ready_for_review"
        elif work["operation"] == "review_section":
            state["status"] = "review_complete"
        write_json(state_path, state)
    return []


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
            if "Status: complete" not in (root / "synthesis.md").read_text(encoding="utf-8"):
                errors.append("workstream synthesis status must be complete")
            if word_count((root / "synthesis.md").read_text(encoding="utf-8")) > 2500:
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
            sections = outline.get("sections", [])
            if not sections:
                errors.append("outline has no sections")
            if outline.get("section_count_target") and len(sections) != outline["section_count_target"]:
                errors.append("outline section count differs from target")
            required = ["id", "order", "title", "narrative_job", "entry_state", "exit_state", "question_payoff", "claim_ids", "target_words", "boundary"]
            for item in sections:
                missing = [field for field in required if not item.get(field)]
                if missing:
                    errors.append(f"outline section {item.get('id', '?')} missing: {', '.join(missing)}")
                budget = item.get("target_words", {})
                if not isinstance(budget, dict) or not isinstance(budget.get("min"), int) or not isinstance(budget.get("max"), int) or budget.get("min", 0) <= 0 or budget.get("max", 0) < budget.get("min", 0):
                    errors.append(f"outline section {item.get('id', '?')} has invalid word budget")
            if outline.get("status") == "approved":
                errors.append("Agent may not self-approve outline")
        elif operation in {"draft_section", "revise_section"}:
            section = target["section"]
            root = product_dir / "03_sections" / section
            state = read_json(root / "section.json")
            draft_words = word_count((root / "draft.md").read_text(encoding="utf-8"))
            budget = state["target_words"]
            if not int(budget["min"]) <= draft_words <= int(budget["max"]):
                errors.append(f"draft word count {draft_words} outside {budget['min']}–{budget['max']}")
            if word_count((root / "handoff.md").read_text(encoding="utf-8")) > 500:
                errors.append("section handoff exceeds 500 words")
        elif operation == "review_section":
            section = target["section"]
            review = product_dir / "03_sections" / section / "review.md"
            if word_count(review.read_text(encoding="utf-8")) < 5:
                errors.append("section review is empty or non-diagnostic")
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


def set_task_state(product_dir: Path, task_id: str, state: str) -> None:
    work_path = product_dir.resolve() / "tasks" / task_id / "work-order.json"
    work = read_json(work_path)
    work["state"] = state
    work["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(work_path, work)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("product", type=Path)
    create.add_argument("operation", choices=sorted(load_registry()))
    create.add_argument("--section")
    create.add_argument("--unit")
    create.add_argument("--replace", action="store_true")
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
            work = create_task(args.product, args.operation, args.section, args.unit, args.replace)
        except (ValueError, FileNotFoundError, FileExistsError, json.JSONDecodeError) as exc:
            parser.error(str(exc))
        print(json.dumps(work, ensure_ascii=False, indent=2))
        return 0
    if args.command == "show":
        active = read_json(active_path(args.product.resolve()))
        context = args.product.resolve() / active["context_packet"]
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
            task_id = read_json(active_path(product))["task_id"]
        path = product / "tasks" / task_id / "operator-brief.json"
        errors = validate_brief_file(path)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print(render_brief(read_json(path)), end="")
        return 0
    if args.command == "state":
        set_task_state(args.product, args.task_id, args.value)
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
