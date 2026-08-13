#!/usr/bin/env python3
"""Compile the smallest self-contained context packet for one operation."""

from __future__ import annotations

import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import (
        REPO_ROOT,
        estimate_tokens,
        expand_inputs,
        expand_optional_inputs,
        load_registry,
        product_relative,
        read_json,
        render_pattern,
        repo_relative,
        sha256,
        write_json,
    )
    from scripts.consolidate_research import verify_consolidation
    from scripts.packet_contract import PACKET_COMPILER, PACKET_SCHEMA_VERSION
    from scripts.story_plan_contract import verify_narration_pack
except ModuleNotFoundError:  # Direct execution: python scripts/context_packet.py
    from common import (
        REPO_ROOT,
        estimate_tokens,
        expand_inputs,
        expand_optional_inputs,
        load_registry,
        product_relative,
        read_json,
        render_pattern,
        repo_relative,
        sha256,
        write_json,
    )
    from consolidate_research import verify_consolidation
    from packet_contract import PACKET_COMPILER, PACKET_SCHEMA_VERSION
    from story_plan_contract import verify_narration_pack


HARNESS_PATH = REPO_ROOT / "system" / "harness.json"


def load_harness() -> dict[str, Any]:
    value = read_json(HARNESS_PATH)
    if value.get("schema_version") != 1 or not isinstance(value.get("profiles"), dict):
        raise ValueError("Invalid system/harness.json")
    return value


def validate_prompt_layers(
    instruction_paths: list[Path],
    profile: dict[str, Any],
    harness: dict[str, Any],
) -> None:
    relative_paths = {repo_relative(path) for path in instruction_paths}
    excluded = relative_paths.intersection(harness.get("prompt_excluded_files", []))
    if excluded:
        raise ValueError("Hard-policy files must stay outside task prompts: " + ", ".join(sorted(excluded)))
    eval_only = relative_paths.intersection(harness.get("eval_only_files", []))
    if eval_only and profile.get("kind") != "evaluation":
        raise ValueError("Evaluation-only files cannot enter a creative prompt: " + ", ".join(sorted(eval_only)))


def validate_target(operation: str, spec: dict[str, Any], section: str | None, unit: str | None) -> None:
    kind = spec["target_kind"]
    if kind == "section" and not section:
        raise ValueError(f"{operation} requires --section P##")
    if kind == "unit" and not unit:
        raise ValueError(f"{operation} requires --unit WS##")
    if kind == "product" and (section or unit):
        raise ValueError(f"{operation} targets the product; omit --section/--unit")


def validate_preconditions(product_dir: Path, operation: str, section: str | None, unit: str | None) -> None:
    product = read_json_local(product_dir / "product.json")
    stages = product.get("stages", {})
    if operation == "research_plan" and stages.get("direction") != "approved":
        raise ValueError("Product direction must be human-approved before research planning.")
    if operation in {"research_workstream", "research_synthesis"}:
        plan = read_json_local(product_dir / "01_research" / "plan.json")
        if plan.get("status") != "approved":
            raise ValueError("Research plan must be human-approved first.")
        declared_units = {item.get("id") for item in plan.get("workstreams", []) if item.get("id")}
        if operation == "research_workstream" and unit not in declared_units:
            raise ValueError(f"Workstream {unit} is not declared in the approved research plan.")
    if operation == "research_synthesis":
        for expected_unit in sorted(declared_units):
            root = product_dir / "01_research" / "workstreams" / str(expected_unit)
            sources = read_json_local(root / "sources.json")
            claims = read_json_local(root / "claims.json")
            synthesis = root / "synthesis.md"
            if sources.get("status") != "complete" or claims.get("status") != "complete":
                raise ValueError(f"Incomplete workstream ledgers: {expected_unit}")
            if "Status: complete" not in synthesis.read_text(encoding="utf-8"):
                raise ValueError(f"Incomplete workstream synthesis: {synthesis.relative_to(product_dir)}")
        consolidation_errors = verify_consolidation(product_dir)
        if consolidation_errors:
            raise ValueError("Research ledgers must be consolidated before synthesis: " + "; ".join(consolidation_errors))
    if operation == "outline":
        sources = read_json_local(product_dir / "01_research" / "source-index.json")
        claims = read_json_local(product_dir / "01_research" / "claim-ledger.json")
        if sources.get("status") != "complete" or claims.get("status") != "complete":
            raise ValueError("Source index and claim ledger must be complete before outline.")
        synthesis = product_dir / "01_research" / "research-synthesis.md"
        if "Status: complete" not in synthesis.read_text(encoding="utf-8"):
            raise ValueError("Research synthesis must be complete before outline.")
    if operation in {"design_section", "draft_section", "review_section", "revise_section"}:
        outline = read_json_local(product_dir / "02_outline" / "outline.json")
        if outline.get("status") != "approved":
            raise ValueError("Outline must be human-approved first.")
        state = read_json_local(product_dir / "03_sections" / str(section) / "section.json")
        expected = {
            "design_section": {"needs_story_plan", "story_plan_changes_requested"},
            "draft_section": {"ready_for_draft"},
            "review_section": {"ready_for_review"},
            "revise_section": {"changes_requested"},
        }[operation]
        if state.get("status") not in expected:
            raise ValueError(f"{section} status {state.get('status')!r} does not allow {operation}.")
    if operation in {"draft_section", "review_section", "revise_section"}:
        narration_errors = verify_narration_pack(product_dir, str(section))
        if narration_errors:
            raise ValueError("Narration pack is not ready: " + "; ".join(narration_errors))
    if operation == "integration_review":
        outline = read_json_local(product_dir / "02_outline" / "outline.json")
        if outline.get("status") != "approved":
            raise ValueError("Outline must be human-approved before integration review.")
        for item in outline.get("sections", []):
            section_id = item["id"]
            root = product_dir / "03_sections" / section_id
            state = read_json_local(root / "section.json")
            if state.get("status") != "approved" or state.get("human_approved") is not True:
                raise ValueError(f"Integration review requires human-approved section: {section_id}")
            if not (root / "handoff.md").is_file():
                raise ValueError(f"Integration review requires handoff: {section_id}")
    if operation == "final_audit":
        manifest = read_json_local(product_dir / "05_delivery" / "assembly-manifest.json")
        outline = read_json_local(product_dir / "02_outline" / "outline.json")
        expected = [item["id"] for item in sorted(outline.get("sections", []), key=lambda value: value["order"])]
        assembled = [item.get("id") for item in manifest.get("sections", [])]
        if manifest.get("mode") != "full" or assembled != expected:
            raise ValueError("Final audit requires a full assembly matching the approved outline.")
        for record in manifest.get("sections", []):
            draft = product_dir / record["source"]
            state = read_json_local(draft.parent / "section.json")
            if state.get("status") != "approved" or state.get("human_approved") is not True:
                raise ValueError(f"Final audit requires human-approved section: {record.get('id')}.")
            if not draft.is_file() or sha256(draft) != record.get("sha256"):
                raise ValueError(f"Assembly is stale for section {record.get('id')}.")


def read_json_local(path: Path) -> dict[str, Any]:
    import json

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def compile_packet(
    product_dir: Path,
    operation: str,
    task_id: str,
    section: str | None = None,
    unit: str | None = None,
) -> tuple[dict[str, Any], str]:
    product_dir = product_dir.resolve()
    registry = load_registry()
    if operation not in registry:
        raise ValueError(f"Unknown operation: {operation}")
    spec = registry[operation]
    harness = load_harness()
    profile_name = spec.get("context_profile")
    profile = harness["profiles"].get(profile_name)
    if not isinstance(profile, dict):
        raise ValueError(f"Operation {operation} has no valid context profile")
    validate_target(operation, spec, section, unit)
    validate_preconditions(product_dir, operation, section, unit)

    instruction_paths = [(REPO_ROOT / item).resolve() for item in spec["instruction_files"]]
    for path in instruction_paths:
        if not path.is_file():
            raise FileNotFoundError(f"Missing instruction: {repo_relative(path)}")
    validate_prompt_layers(instruction_paths, profile, harness)
    input_paths = expand_inputs(product_dir, spec["required_inputs"], section, unit)
    input_paths += expand_optional_inputs(product_dir, spec.get("optional_inputs", []), section, unit)
    if spec.get("include_dependency_handoffs") and section:
        state = read_json_local(product_dir / "03_sections" / section / "section.json")
        for dependency in state.get("dependencies", []):
            dependency_root = product_dir / "03_sections" / dependency
            dependency_state_path = dependency_root / "section.json"
            dependency_handoff = dependency_root / "handoff.md"
            if dependency_state_path.is_file() and dependency_handoff.is_file():
                dependency_state = read_json_local(dependency_state_path)
                if dependency_state.get("status") == "approved" and dependency_state.get("human_approved") is True:
                    input_paths.append(dependency_handoff.resolve())
    input_paths = list(dict.fromkeys(input_paths))

    blocks: list[str] = []
    instruction_blocks: list[str] = []
    input_blocks: list[str] = []
    input_records: list[dict[str, Any]] = []
    for path in instruction_paths:
        content = path.read_text(encoding="utf-8")
        block = [f"# BEGIN INSTRUCTION: {repo_relative(path)}", content.rstrip(), f"# END INSTRUCTION: {repo_relative(path)}", ""]
        blocks.extend(block)
        instruction_blocks.extend(block)
    instruction_tokens = estimate_tokens("\n".join(instruction_blocks))
    instruction_budget = int(profile["max_instruction_tokens"])
    if instruction_tokens > instruction_budget:
        raise ValueError(
            f"Instruction estimate {instruction_tokens} exceeds {profile_name} budget {instruction_budget}; "
            "move hard policy or evaluation logic out of the prompt."
        )
    for path in input_paths:
        content = path.read_text(encoding="utf-8")
        relative = product_relative(product_dir, path)
        input_records.append({"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size})
        block = [f"# BEGIN INPUT: {relative}", content.rstrip(), f"# END INPUT: {relative}", ""]
        blocks.extend(block)
        input_blocks.extend(block)
    input_tokens = estimate_tokens("\n".join(input_blocks))

    outputs = [render_pattern(item, section, unit) for item in spec["outputs"]]
    output_baselines = []
    for relative in outputs:
        path = product_dir / relative
        output_baselines.append(
            {
                "path": relative,
                "sha256": sha256(path) if path.is_file() else None,
            }
        )
    report_path = f"tasks/{task_id}/report.md"
    operator_brief_path = f"tasks/{task_id}/operator-brief.json"
    allowed = outputs + [report_path, operator_brief_path]
    header = [
        f"# Context Packet — {task_id}",
        "",
        f"- Product: `{product_dir.name}`",
        f"- Operation: `{operation}`",
        f"- Context profile: `{profile_name}`",
        f"- Section: `{section or '-'}`",
        f"- Unit: `{unit or '-'}`",
        f"- Allowed writes: {', '.join(f'`{item}`' for item in allowed)}",
        "",
        "## Acceptance criteria",
        "",
        *[f"- {item}" for item in spec["acceptance"]],
        "",
        "## Local autonomy",
        "",
        profile["autonomy"],
        "",
        "Write full operational detail to `report.md`. Write only decision-relevant summary to `operator-brief.json`.",
        "The final chat response must use the rendered operator brief, not the task report.",
        "",
        "Only the material inside this packet is task context. Do not scan the repository.",
        "",
    ]
    packet_text = "\n".join(header + blocks).rstrip() + "\n"
    tokens = estimate_tokens(packet_text)
    budget = int(spec["max_context_tokens"])
    if tokens > budget:
        raise ValueError(f"Context packet estimate {tokens} exceeds budget {budget}; compact an upstream artifact.")

    packet = {
        "schema_version": PACKET_SCHEMA_VERSION,
        "compiler": PACKET_COMPILER,
        "context_sha256": hashlib.sha256(packet_text.encode("utf-8")).hexdigest(),
        "authority": "product_agent",
        "task_id": task_id,
        "product": product_dir.name,
        "operation": operation,
        "target": {"section": section, "unit": unit},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "context_profile": profile_name,
        "max_context_tokens": budget,
        "estimated_context_tokens": tokens,
        "prompt_instruction_tokens": instruction_tokens,
        "input_tokens": input_tokens,
        "boundary_enforcement": harness["boundary_enforcement"],
        "evaluation_gate": profile.get("evaluation_gate"),
        "instruction_files": [repo_relative(path) for path in instruction_paths],
        "inputs": input_records,
        "operation_outputs": outputs,
        "output_baselines": output_baselines,
        "allowed_write_paths": allowed,
        "report_path": report_path,
        "operator_brief_path": operator_brief_path,
        "acceptance_criteria": spec["acceptance"],
        "validation": [
            f"python scripts/validate.py products/{product_dir.name}",
            f"python scripts/task.py verify products/{product_dir.name} {task_id}",
            f"python scripts/check_scope.py products/{product_dir.name}",
            f"python scripts/operator_brief.py validate products/{product_dir.name}/{operator_brief_path}",
        ],
    }
    return packet, packet_text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("operation")
    parser.add_argument("task_id")
    parser.add_argument("--section")
    parser.add_argument("--unit")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    packet, text = compile_packet(args.product, args.operation, args.task_id, args.section, args.unit)
    output = args.out or args.product / "tasks" / args.task_id / "context.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    write_json(output.with_name("packet.json"), packet)
    print(f"Compiled {output} (~{packet['estimated_context_tokens']} tokens / {packet['max_context_tokens']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
