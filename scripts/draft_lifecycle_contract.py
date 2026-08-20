#!/usr/bin/env python3
"""Task provenance and evidence-trace checks for canonical section prose."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
except ModuleNotFoundError:
    from common import read_json, sha256, write_json


LIVE_TASK_STATES = {"ready", "in_progress"}
SUBMITTED_TASK_STATES = {"ready_for_review", "closed"}
PROSE_OPERATIONS = {"draft_section", "revise_section"}


def _json_hash(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _requires_brokered_claim_resolution(product_dir: Path, work: dict[str, Any]) -> bool:
    """Direct-authorship drafts must resolve claim IDs through the bounded evidence broker."""

    if work.get("operation") != "draft_section":
        return False
    outline_path = product_dir / "02_outline" / "outline.json"
    if not outline_path.is_file():
        return False
    try:
        outline = read_json(outline_path)
    except (ValueError, json.JSONDecodeError, OSError):
        return False
    architecture = outline.get("script_architecture")
    return isinstance(architecture, dict) and architecture.get("writer_authorship_contract_version") == 1


def validate_evidence_trace(
    product_dir: Path,
    task_id: str,
    *,
    require_resolution: bool = True,
) -> list[str]:
    """Validate trace integrity and, on submission, require brokered claim resolution for direct drafts."""

    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    try:
        packet = read_json(task_dir / "packet.json")
        work = read_json(task_dir / "work-order.json")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return [f"cannot audit evidence trace for {task_id}: {exc}"]

    resolution_required = require_resolution and _requires_brokered_claim_resolution(product_dir, work)
    access = packet.get("evidence_access")
    if not isinstance(access, dict):
        if resolution_required:
            return [f"task {task_id} direct-authorship draft requires bounded evidence access"]
        return []
    trace_rel = access.get("trace_path")
    if not isinstance(trace_rel, str) or not trace_rel:
        return [f"task {task_id} evidence access is missing trace_path"]
    trace_path = product_dir / trace_rel
    if not trace_path.is_file():
        if resolution_required:
            return [
                f"task {task_id} direct-authorship draft must resolve approved claims through bounded evidence access before submission"
            ]
        return []

    section = str(work.get("target", {}).get("section") or "")
    evidence_path = product_dir / "03_sections" / section / "evidence-pack.json"
    if not evidence_path.is_file():
        return [f"task {task_id} trace cannot be audited without section evidence pack"]
    expected_evidence_hash = sha256(evidence_path)
    allowed_capabilities = set(access.get("capabilities", []))
    lines = [line for line in trace_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return [f"task {task_id} evidence trace exists but is empty"]

    errors: list[str] = []
    successful_capabilities: set[str] = set()
    for index, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"task {task_id} evidence trace line {index} is invalid JSON: {exc}")
            continue
        if record.get("task_id") != task_id:
            errors.append(f"task {task_id} evidence trace line {index} has wrong task_id")
        if record.get("section") != section:
            errors.append(f"task {task_id} evidence trace line {index} has wrong section")
        capability = record.get("capability")
        if capability not in allowed_capabilities:
            errors.append(f"task {task_id} evidence trace line {index} uses undeclared capability {capability!r}")
        if record.get("evidence_pack_sha256") != expected_evidence_hash:
            errors.append(f"task {task_id} evidence trace line {index} is stale relative to evidence pack")
        if record.get("truth_ceiling_unchanged") is not True:
            errors.append(f"task {task_id} evidence trace line {index} does not preserve truth ceiling")
        response = record.get("response")
        expected_response_hash = _json_hash(response) if response is not None else None
        if record.get("response_sha256") != expected_response_hash:
            errors.append(f"task {task_id} evidence trace line {index} response hash is invalid")
        if capability in allowed_capabilities and record.get("error") is None and response is not None:
            successful_capabilities.add(str(capability))

    if resolution_required and "claims" not in successful_capabilities:
        errors.append(
            f"task {task_id} direct-authorship draft must inspect approved claims through the bounded 'claims' capability before submission"
        )
    return errors


def _task_scope_errors(product_dir: Path, task_id: str, section: str, *, live: bool) -> list[str]:
    task_dir = product_dir / "tasks" / task_id
    try:
        work = read_json(task_dir / "work-order.json")
        packet = read_json(task_dir / "packet.json")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return [f"draft provenance task {task_id} is invalid: {exc}"]

    errors: list[str] = []
    if work.get("operation") not in PROSE_OPERATIONS or packet.get("operation") != work.get("operation"):
        errors.append(f"task {task_id} is not a valid prose task")
    if work.get("target", {}).get("section") != section or packet.get("target", {}).get("section") != section:
        errors.append(f"task {task_id} targets the wrong section")
    state = work.get("state")
    allowed_states = LIVE_TASK_STATES if live else SUBMITTED_TASK_STATES
    if state not in allowed_states:
        errors.append(f"task {task_id} state {state!r} is not valid for {'live' if live else 'submitted'} prose provenance")
    expected_outputs = {f"03_sections/{section}/draft.md", f"03_sections/{section}/handoff.md"}
    if not expected_outputs.issubset(set(packet.get("allowed_write_paths", []))):
        errors.append(f"task {task_id} does not own draft and handoff write scope")
    if work.get("allowed_write_paths") != packet.get("allowed_write_paths"):
        errors.append(f"task {task_id} work-order scope differs from packet")
    errors.extend(validate_evidence_trace(product_dir, task_id, require_resolution=not live))
    return errors


def active_prose_task(product_dir: Path, section: str, status: str | None) -> tuple[str | None, list[str]]:
    """Return the live prose task that owns this section; ACTIVE.json is irrelevant to authority."""

    product_dir = product_dir.resolve()
    expected_operation = "draft_section" if status == "ready_for_draft" else "revise_section" if status == "changes_requested" else None
    if expected_operation is None:
        return None, []

    tasks_dir = product_dir / "tasks"
    if not tasks_dir.is_dir():
        return None, []

    owners: list[str] = []
    errors: list[str] = []
    for work_path in sorted(tasks_dir.glob("T*/work-order.json")):
        try:
            work = read_json(work_path)
        except (json.JSONDecodeError, ValueError, OSError) as exc:
            errors.append(f"invalid live prose work order {work_path.parent.name}: {exc}")
            continue
        if work.get("state") not in LIVE_TASK_STATES:
            continue
        if work.get("operation") != expected_operation:
            continue
        if work.get("target", {}).get("section") != section:
            continue
        task_id = str(work.get("id") or work_path.parent.name)
        task_errors = _task_scope_errors(product_dir, task_id, section, live=True)
        if task_errors:
            errors.extend(task_errors)
        else:
            owners.append(task_id)

    if errors:
        return None, errors
    if len(owners) > 1:
        return None, [f"{section} has multiple live prose tasks: {', '.join(owners)}"]
    return (owners[0], []) if owners else (None, [])


def record_submitted_prose(product_dir: Path, task_id: str) -> None:
    product_dir = product_dir.resolve()
    work = read_json(product_dir / "tasks" / task_id / "work-order.json")
    operation = work.get("operation")
    if operation not in PROSE_OPERATIONS:
        return
    section = str(work.get("target", {}).get("section") or "")
    root = product_dir / "03_sections" / section
    draft = root / "draft.md"
    handoff = root / "handoff.md"
    if not draft.is_file() or not handoff.is_file():
        raise FileNotFoundError(f"Submitted prose task {task_id} requires draft.md and handoff.md")
    state_path = root / "section.json"
    state = read_json(state_path)
    state["prose_provenance"] = {
        "task_id": task_id,
        "operation": operation,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "draft_sha256": sha256(draft),
        "handoff_sha256": sha256(handoff),
    }
    write_json(state_path, state)


def submitted_prose_errors(product_dir: Path, section: str, state: dict[str, Any]) -> list[str]:
    provenance = state.get("prose_provenance")
    if not isinstance(provenance, dict):
        return [f"{section} canonical draft is missing submitted task provenance"]
    task_id = provenance.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        return [f"{section} canonical draft provenance is missing task_id"]
    errors = _task_scope_errors(product_dir, task_id, section, live=False)
    root = product_dir / "03_sections" / section
    draft = root / "draft.md"
    handoff = root / "handoff.md"
    if draft.is_file() and provenance.get("draft_sha256") != sha256(draft):
        errors.append(f"{section} draft differs from submitted task provenance")
    if handoff.is_file() and provenance.get("handoff_sha256") != sha256(handoff):
        errors.append(f"{section} handoff differs from submitted task provenance")
    task_dir = product_dir / "tasks" / task_id
    if not (task_dir / "report.md").is_file():
        errors.append(f"{section} submitted prose task is missing report.md")
    if not (task_dir / "operator-brief.json").is_file():
        errors.append(f"{section} submitted prose task is missing operator-brief.json")
    return errors


def validate_canonical_draft_lifecycle(product_dir: Path, section: str, state: dict[str, Any]) -> list[str]:
    product_dir = product_dir.resolve()
    root = product_dir / "03_sections" / section
    draft = root / "draft.md"
    handoff = root / "handoff.md"
    if not draft.is_file() and not handoff.is_file():
        return []
    if draft.is_file() != handoff.is_file():
        return [f"{section} canonical prose requires both draft.md and handoff.md"]

    if state.get("approval_basis") == "human_direct_edit" and state.get("human_approved") is True:
        if not state.get("last_human_amendment"):
            return [f"{section} human-direct prose is missing amendment provenance"]
        return []

    live_task_id, live_errors = active_prose_task(product_dir, section, state.get("status"))
    if live_errors:
        return live_errors
    if live_task_id:
        return []
    return submitted_prose_errors(product_dir, section, state)
