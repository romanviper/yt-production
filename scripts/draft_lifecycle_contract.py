#!/usr/bin/env python3
"""Task provenance and evidence-trace checks for canonical section prose."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

try:
    from scripts.common import read_json, sha256, write_json
except ModuleNotFoundError:
    from common import read_json, sha256, write_json


LIVE_TASK_STATES = {"ready", "in_progress"}
SUBMITTED_TASK_STATES = {"ready_for_review", "closed"}
PROSE_OPERATIONS = {"draft_section", "revise_section"}
BOUND_PROSE_PROVENANCE_SCHEMA = 2
BOUND_PACKET_SCHEMA = 5
ROUTE_FIRST_EVIDENCE_INTERFACE_VERSION = 2
MIN_ROUTE_INTENT_CHARS = 200
MAX_ROUTE_INTENT_CHARS = 2000
ROUTE_INTENT_COPY_WINDOW_WORDS = 10


def _json_hash(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _route_first_presentation_order(task_id: str, ids: list[str]) -> list[str]:
    return sorted(
        ids,
        key=lambda item: hashlib.sha256(f"{task_id}\0{item}".encode("utf-8")).hexdigest(),
    )


def _route_intent_error(value: Any, evidence: dict[str, Any]) -> str | None:
    if not isinstance(value, str):
        return "route_intent must be text"
    intent = value.strip()
    if not MIN_ROUTE_INTENT_CHARS <= len(intent) <= MAX_ROUTE_INTENT_CHARS:
        return f"route_intent must be {MIN_ROUTE_INTENT_CHARS}-{MAX_ROUTE_INTENT_CHARS} characters"
    if re.search(r"\b(?:CLM|SRC)-\d{4}\b", intent, flags=re.IGNORECASE):
        return "route_intent must not contain claim or source ids"

    intent_words = re.findall(r"[\wÀ-ỹ]+", intent.casefold(), flags=re.UNICODE)
    intent_windows = {
        tuple(intent_words[index : index + ROUTE_INTENT_COPY_WINDOW_WORDS])
        for index in range(max(0, len(intent_words) - ROUTE_INTENT_COPY_WINDOW_WORDS + 1))
    }
    for claim in evidence.get("claims", []):
        statement = claim.get("statement") if isinstance(claim, dict) else None
        if not isinstance(statement, str):
            continue
        words = re.findall(r"[\wÀ-ỹ]+", statement.casefold(), flags=re.UNICODE)
        for index in range(max(0, len(words) - ROUTE_INTENT_COPY_WINDOW_WORDS + 1)):
            if tuple(words[index : index + ROUTE_INTENT_COPY_WINDOW_WORDS]) in intent_windows:
                return "route_intent copies claim prose"
    return None


def validate_evidence_trace(product_dir: Path, task_id: str) -> list[str]:
    """An absent trace means retrieval was unused; a present trace must be reconstructable."""

    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    try:
        packet = read_json(task_dir / "packet.json")
        work = read_json(task_dir / "work-order.json")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return [f"cannot audit evidence trace for {task_id}: {exc}"]

    access = packet.get("evidence_access")
    if not isinstance(access, dict):
        return []
    trace_rel = access.get("trace_path")
    if not isinstance(trace_rel, str) or not trace_rel:
        return [f"task {task_id} evidence access is missing trace_path"]
    trace_path = product_dir / trace_rel
    if not trace_path.is_file():
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
    return errors


def validate_required_evidence_resolution(product_dir: Path, task_id: str) -> list[str]:
    """Require an audited whole-scope claim resolution only when the packet declares it."""

    product_dir = product_dir.resolve()
    task_dir = product_dir / "tasks" / task_id
    try:
        packet = read_json(task_dir / "packet.json")
        work = read_json(task_dir / "work-order.json")
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return [f"cannot validate required evidence resolution for {task_id}: {exc}"]
    access = packet.get("evidence_access")
    requirements = access.get("required_before_submit", []) if isinstance(access, dict) else []
    if "resolve_claims" not in requirements:
        return []

    section = str(work.get("target", {}).get("section") or "")
    narration_path = product_dir / "03_sections" / section / "narration-pack.json"
    evidence_path = product_dir / "03_sections" / section / "evidence-pack.json"
    trace_path = product_dir / str(access.get("trace_path") or "")
    if not narration_path.is_file():
        return [f"task {task_id} cannot resolve claims without narration pack"]
    narration = read_json(narration_path)
    evidence = read_json(evidence_path) if evidence_path.is_file() else {"claims": []}
    if narration.get("schema_version") == 4:
        scope = narration.get("retrieval_scope", {})
        expected = scope.get("claim_ids", []) if isinstance(scope, dict) else []
    else:
        expected = [
            item.get("id")
            for field in ["core_claims", "optional_claims"]
            for item in narration.get(field, [])
            if isinstance(item, dict) and item.get("id")
        ]
    expected_ids = list(dict.fromkeys(expected))
    if not trace_path.is_file():
        return [f"task {task_id} must call resolve_claims before submission"]

    route_first = (
        work.get("operation") == "draft_section"
        and access.get("interface_version") == ROUTE_FIRST_EVIDENCE_INTERFACE_VERSION
    )
    for line in trace_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = record.get("response")
        resolved_ids = response.get("resolved_claim_ids") if isinstance(response, dict) else None
        resolved_scope_matches = (
            resolved_ids == _route_first_presentation_order(task_id, expected_ids)
            if route_first
            else resolved_ids == expected_ids
        )
        whole_scope_resolution = (
            record.get("capability") == "resolve_claims"
            and record.get("error") is None
            and isinstance(response, dict)
            and resolved_scope_matches
        )
        if not whole_scope_resolution:
            continue
        if route_first:
            arguments = record.get("arguments")
            if not isinstance(arguments, dict) or set(arguments) != {"route_intent"}:
                continue
            intent = arguments.get("route_intent")
            if _route_intent_error(intent, evidence) is not None:
                continue
            assert isinstance(intent, str)
            normalized_intent = intent.strip()
            attestation = response.get("route_intent_attestation")
            composition = response.get("composition_contract")
            claim_records = response.get("claim_records")
            if (
                record.get("response_sha256") != _json_hash(response)
                or not isinstance(composition, dict)
                or composition.get("sequence_authority") != "none"
                or composition.get("presentation_order") != "deterministic_task_hash_with_no_story_authority"
                or not isinstance(attestation, dict)
                or attestation.get("status") != "recorded_before_claim_resolution"
                or attestation.get("sha256") != hashlib.sha256(normalized_intent.encode("utf-8")).hexdigest()
                or attestation.get("characters") != len(normalized_intent)
                or attestation.get("authority") != "creative_route_only_not_evidence"
                or not isinstance(claim_records, dict)
                or set(claim_records) != set(expected_ids)
                or "claims" in response
            ):
                continue
            return []
        return []
    if route_first:
        return [f"task {task_id} must resolve every scoped claim with a valid pre-claim route_intent"]
    return [f"task {task_id} must successfully resolve every scoped claim before submission"]


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
    errors.extend(validate_evidence_trace(product_dir, task_id))
    if not live:
        errors.extend(validate_required_evidence_resolution(product_dir, task_id))
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
    task_dir = product_dir / "tasks" / task_id
    work = read_json(task_dir / "work-order.json")
    packet_path = task_dir / "packet.json"
    packet = read_json(packet_path)
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
    submitted_at = work.get("submitted_at")
    if not isinstance(submitted_at, str) or not submitted_at:
        raise ValueError(f"Submitted prose task {task_id} is missing submitted_at")
    provenance = {
        "task_id": task_id,
        "operation": operation,
        "submitted_at": submitted_at,
        "draft_sha256": sha256(draft),
        "handoff_sha256": sha256(handoff),
    }
    if packet.get("schema_version") == BOUND_PACKET_SCHEMA:
        provenance.update(
            {
                "schema_version": BOUND_PROSE_PROVENANCE_SCHEMA,
                "packet_schema_version": BOUND_PACKET_SCHEMA,
                "task_packet_sha256": sha256(packet_path),
            }
        )
    state["prose_provenance"] = provenance
    if operation == "revise_section":
        cycle_id = state.get("cycle_id")
        prior = state.get("revision_pass")
        prior_count = (
            int(prior.get("count", 0))
            if isinstance(prior, dict) and prior.get("cycle_id") == cycle_id
            else 0
        )
        state["revision_pass"] = {"cycle_id": cycle_id, "count": prior_count + 1}
    write_json(state_path, state)


def submitted_prose_errors(product_dir: Path, section: str, state: dict[str, Any]) -> list[str]:
    provenance = state.get("prose_provenance")
    if not isinstance(provenance, dict):
        return [f"{section} canonical draft is missing submitted task provenance"]
    task_id = provenance.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        return [f"{section} canonical draft provenance is missing task_id"]
    errors = _task_scope_errors(product_dir, task_id, section, live=False)
    task_dir = product_dir / "tasks" / task_id
    try:
        work = read_json(task_dir / "work-order.json")
        packet_path = task_dir / "packet.json"
        packet = read_json(packet_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"{section} cannot verify submitted prose provenance binding: {exc}")
        work = {}
        packet = {}
        packet_path = task_dir / "packet.json"
    provenance_schema = provenance.get("schema_version")
    if provenance_schema == BOUND_PROSE_PROVENANCE_SCHEMA:
        expected_keys = {
            "schema_version",
            "task_id",
            "operation",
            "submitted_at",
            "draft_sha256",
            "handoff_sha256",
            "packet_schema_version",
            "task_packet_sha256",
        }
        if set(provenance) != expected_keys:
            errors.append(f"{section} bound prose provenance has an invalid shape")
        if (
            provenance.get("packet_schema_version") != BOUND_PACKET_SCHEMA
            or packet.get("schema_version") != BOUND_PACKET_SCHEMA
            or provenance.get("task_packet_sha256") != (sha256(packet_path) if packet_path.is_file() else None)
        ):
            errors.append(f"{section} prose provenance packet binding has changed")
        if provenance.get("submitted_at") != work.get("submitted_at"):
            errors.append(f"{section} prose provenance timestamp differs from submitted work order")
    elif provenance_schema is not None:
        errors.append(f"{section} prose provenance schema is unsupported")
    elif packet.get("schema_version") == BOUND_PACKET_SCHEMA:
        errors.append(f"{section} schema-v5 prose task requires bound provenance")
    root = product_dir / "03_sections" / section
    draft = root / "draft.md"
    handoff = root / "handoff.md"
    if draft.is_file() and provenance.get("draft_sha256") != sha256(draft):
        errors.append(f"{section} draft differs from submitted task provenance")
    if handoff.is_file() and provenance.get("handoff_sha256") != sha256(handoff):
        errors.append(f"{section} handoff differs from submitted task provenance")
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
