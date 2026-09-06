#!/usr/bin/env python3
"""Writer-side self-report contract for the Owner-first MVP.

Writers produce their own execution-report.json next to draft.md. The repo
controller validates and freezes that declaration; it does not invent model,
session, timing, status, issues, or over-budget rationale on the Writer's behalf.

Self-reported timing is provenance, not host-attested inference time.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from scripts import learning

REPORT_SCHEMA = "WRITER_SELF_REPORT_1"
FORBIDDEN_REASONING_KEYS = {
    "chain_of_thought",
    "raw_chain_of_thought",
    "private_reasoning",
    "internal_monologue",
    "hidden_reasoning",
    "scratchpad_reasoning",
}
SELF_REPORTED_SOURCES = {
    "WRITER_SELF_REPORTED_SESSION_WINDOW",
    "WRITER_SELF_REPORTED_DURATION",
}


def _report_paths(run_root: Path, actor: str) -> tuple[Path, Path]:
    session_id = learning.WRITERS[actor]["session_id"]
    root = run_root / "agents" / actor / session_id
    return root / "input" / "self-report-contract.json", root / "output" / "execution-report.json"


def _contains_forbidden_reasoning(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).casefold() in FORBIDDEN_REASONING_KEYS:
                return True
            if _contains_forbidden_reasoning(child):
                return True
    elif isinstance(value, list):
        return any(_contains_forbidden_reasoning(item) for item in value)
    return False


def prepare_report_contracts(run_root: Path) -> dict[str, Any]:
    """Materialize the report schema into each Writer input workspace."""
    run_root = run_root.resolve()
    state = learning._load_state(run_root)
    if state["state"] != "AWAITING_WRITERS":
        raise learning.LearningError("STATE_TRANSITION_DENIED", f"cannot prepare Writer report contracts from {state['state']}")
    budget = learning.budget_summary(run_root)
    if not budget.get("approved"):
        raise learning.LearningError("BUDGET_NOT_APPROVED", "Owner-approved budget is required before Writer dispatch")

    created: dict[str, Any] = {}
    for actor, meta in learning.WRITERS.items():
        packet_path, _, _ = learning._writer_paths(run_root, actor)
        learning._verify_frozen(packet_path, state["writer_packet_sha256"][actor], f"{actor} packet")
        contract_path, _ = _report_paths(run_root, actor)
        if contract_path.exists():
            raise learning.LearningError("REPORT_CONTRACT_ALREADY_EXISTS", f"{actor} report contract is write-once", path=contract_path)
        contract = {
            "schema_version": REPORT_SCHEMA,
            "role": actor,
            "session_id": meta["session_id"],
            "requested_model": meta["requested_model"],
            "packet_sha256": state["writer_packet_sha256"][actor],
            "common_content_sha256": state["writer_common_content_sha256"],
            "approved_budget_seconds": budget["actors"][actor]["allocated_seconds"],
            "required_outputs": ["output/draft.md", "output/execution-report.json"],
            "required_report_fields": [
                "schema_version",
                "actor",
                "session_id",
                "packet_sha256",
                "common_content_sha256",
                "actual_model",
                "actual_config",
                "attempt",
                "status",
                "work_summary",
                "issues_encountered",
                "uncertainty",
                "timing",
                "draft_sha256",
                "budget_extension",
            ],
            "timing_contract": {
                "allowed_sources": sorted(SELF_REPORTED_SOURCES),
                "meaning": "Writer-declared session timing; not host-attested active inference time.",
                "unknown_rule": "If timing cannot be measured, leave start/end/duration null and explain the issue; repo records UNKNOWN and stops new work.",
            },
            "budget_extension_contract": {
                "rule": "If the declared Writer duration exceeds remaining approved budget, explain why and request explicit Owner approval.",
                "fields": ["requested_seconds", "reason", "remaining_work_if_approved"],
                "owner_is_only_approver": True,
            },
            "reasoning_boundary": "Report declared operational/editorial decisions and observable issues only. Do not dump private chain-of-thought or hidden reasoning.",
        }
        learning.atomic_write_json(contract_path, contract)
        learning.make_read_only(contract_path)
        created[actor] = {
            "ref": contract_path.relative_to(run_root).as_posix(),
            "sha256": learning.sha256_file(contract_path),
        }
    return {"schema_version": REPORT_SCHEMA, "contracts": created}


def _validate_report(run_root: Path, report_file: Path) -> tuple[dict[str, Any], dict[str, Any], str]:
    report = learning.read_json(report_file)
    if report.get("schema_version") != REPORT_SCHEMA:
        raise learning.LearningError("WRITER_REPORT_SCHEMA_INVALID", f"expected {REPORT_SCHEMA}")
    if _contains_forbidden_reasoning(report):
        raise learning.LearningError("PRIVATE_REASONING_FIELD_FORBIDDEN", "Writer report must not contain private chain-of-thought fields")
    session_id = report.get("session_id")
    if not isinstance(session_id, str):
        raise learning.LearningError("SESSION_MISMATCH", "Writer report must declare session_id")
    state = learning._load_state(run_root)
    actor = learning._actor_from_session(state, session_id)
    if report.get("actor") != actor:
        raise learning.LearningError("WRITER_REPORT_ACTOR_MISMATCH", f"session {session_id} belongs to {actor}")
    if report.get("attempt") != 1:
        raise learning.LearningError("WRITER_REPORT_ATTEMPT_INVALID", "Owner-first MVP accepts content attempt 1 only")
    status = str(report.get("status") or "").upper()
    if status not in {"COMPLETED", "FAILED", "TIMEOUT"}:
        raise learning.LearningError("WRITER_REPORT_STATUS_INVALID", "status must be COMPLETED, FAILED, or TIMEOUT")
    if not isinstance(report.get("actual_model"), str) or not report["actual_model"].strip():
        raise learning.LearningError("MODEL_IDENTITY_REQUIRED", "Writer must declare the actual model used")
    if report.get("actual_config") is not None and not isinstance(report.get("actual_config"), str):
        raise learning.LearningError("MODEL_CONFIG_INVALID", "actual_config must be a string or null")
    for field in ("work_summary", "uncertainty"):
        if not isinstance(report.get(field), str) or not report[field].strip():
            raise learning.LearningError("WRITER_REPORT_FIELD_REQUIRED", f"{field} must be a non-empty string")
    issues = report.get("issues_encountered")
    if not isinstance(issues, list) or not all(isinstance(item, str) for item in issues):
        raise learning.LearningError("WRITER_REPORT_ISSUES_INVALID", "issues_encountered must be a string list; use [] when none")
    packet_path, _, _ = learning._writer_paths(run_root, actor)
    learning._verify_frozen(packet_path, state["writer_packet_sha256"][actor], f"{actor} packet")
    if report.get("packet_sha256") != state["writer_packet_sha256"][actor]:
        raise learning.LearningError("WRITER_REPORT_PACKET_MISMATCH", "report is not bound to the frozen Writer packet")
    if report.get("common_content_sha256") != state["writer_common_content_sha256"]:
        raise learning.LearningError("WRITER_COMMON_CONTENT_CHANGED", "report common-content hash does not match the run")

    timing = report.get("timing")
    if not isinstance(timing, dict):
        raise learning.LearningError("WRITER_REPORT_TIMING_REQUIRED", "timing object is required")
    timestamp_source = timing.get("timestamp_source")
    if timestamp_source not in SELF_REPORTED_SOURCES:
        raise learning.LearningError("WRITER_REPORT_TIMING_SOURCE_INVALID", f"timestamp_source must be one of {sorted(SELF_REPORTED_SOURCES)}")
    start_utc = timing.get("start_utc")
    end_utc = timing.get("end_utc")
    duration_seconds = timing.get("duration_seconds")
    if duration_seconds is not None and (not isinstance(duration_seconds, (int, float)) or float(duration_seconds) < 0):
        raise learning.LearningError("TIMING_DURATION_INVALID", "duration_seconds must be a non-negative number or null")
    if timestamp_source == "WRITER_SELF_REPORTED_SESSION_WINDOW" and (not isinstance(start_utc, str) or not isinstance(end_utc, str)):
        raise learning.LearningError("WRITER_REPORT_WINDOW_INCOMPLETE", "self-reported session window requires start_utc and end_utc")
    if timestamp_source == "WRITER_SELF_REPORTED_DURATION" and duration_seconds is None:
        raise learning.LearningError("WRITER_REPORT_DURATION_REQUIRED", "self-reported duration source requires duration_seconds")

    current = learning.budget_summary(run_root)
    row = current["actors"][actor]
    declared_duration: float | None = None
    if duration_seconds is not None:
        declared_duration = float(duration_seconds)
    elif isinstance(start_utc, str) and isinstance(end_utc, str):
        declared_duration = (learning._parse_utc(end_utc) - learning._parse_utc(start_utc)).total_seconds()
        if declared_duration < 0:
            raise learning.LearningError("TIMING_CLOCK_REVERSED", "Writer report end precedes start")
    predicted_overrun = 0.0
    if declared_duration is not None and row["remaining_seconds"] is not None:
        predicted_overrun = max(0.0, declared_duration - float(row["remaining_seconds"]))
    extension = report.get("budget_extension")
    if predicted_overrun > 0:
        if not isinstance(extension, dict):
            raise learning.LearningError("WRITER_OVERRUN_EXPLANATION_REQUIRED", "over-budget Writer must explain the overrun and request Owner approval")
        requested = extension.get("requested_seconds")
        if not isinstance(requested, (int, float)) or float(requested) < predicted_overrun:
            raise learning.LearningError("WRITER_EXTENSION_AMOUNT_INSUFFICIENT", "requested_seconds must cover at least the declared overrun")
        for field in ("reason", "remaining_work_if_approved"):
            if not isinstance(extension.get(field), str) or not extension[field].strip():
                raise learning.LearningError("WRITER_OVERRUN_EXPLANATION_REQUIRED", f"budget_extension.{field} is required")
    elif extension not in (None, {}):
        raise learning.LearningError("WRITER_EXTENSION_NOT_NEEDED", "Writer may request extension here only when its declared work exceeds approved remaining budget")
    return report, state, actor


def accept_writer_submission(run_root: Path, *, report_file: Path, draft_file: Path | None = None) -> dict[str, Any]:
    """Freeze one Writer's self-declared result and enforce budget consequences."""
    run_root = run_root.resolve()
    report, state, actor = _validate_report(run_root, report_file)
    if state["state"] != "AWAITING_WRITERS":
        raise learning.LearningError("STATE_TRANSITION_DENIED", f"cannot accept Writer submission from {state['state']}")
    if state["writer_status"][actor] in {"ACCEPTED", "PENDING_BUDGET_REVIEW"}:
        raise learning.LearningError("OUTPUT_OVERWRITE_DENIED", f"{actor} already produced an accepted/pending output")
    learning._require_budget_to_start(run_root, actor)
    learning._verify_authority_snapshot(run_root, state)
    learning._verify_frozen(learning._run_paths(run_root)["plan_output"], state["plan_sha256"], "Plan output")

    contract_path, frozen_report_path = _report_paths(run_root, actor)
    if not contract_path.is_file():
        raise learning.LearningError("WRITER_REPORT_CONTRACT_MISSING", "prepare Writer self-report contracts before dispatch", path=contract_path)
    packet_path, output_path, _ = learning._writer_paths(run_root, actor)
    contract = learning.read_json(contract_path)
    if contract.get("packet_sha256") != state["writer_packet_sha256"][actor]:
        raise learning.LearningError("WRITER_REPORT_CONTRACT_STALE", "self-report contract is not bound to the current packet")
    if frozen_report_path.exists():
        raise learning.LearningError("OUTPUT_OVERWRITE_DENIED", f"{actor} execution report already exists", path=frozen_report_path)

    status = str(report["status"]).upper()
    if status == "COMPLETED":
        if draft_file is None or not draft_file.is_file() or not draft_file.read_text(encoding="utf-8").strip():
            raise learning.LearningError("DRAFT_MISSING", "COMPLETED Writer report requires a non-empty draft")
        declared_sha = report.get("draft_sha256")
        if not isinstance(declared_sha, str) or declared_sha != learning.sha256_file(draft_file):
            raise learning.LearningError("WRITER_REPORT_DRAFT_HASH_MISMATCH", "Writer-declared draft_sha256 must match the submitted draft")
    elif draft_file is not None and draft_file.exists():
        raise learning.LearningError("FAILED_WRITER_HAS_DRAFT", "FAILED/TIMEOUT report must not be accepted as a completed draft")

    frozen_report_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(report_file, frozen_report_path)
    learning.make_read_only(frozen_report_path)
    report_sha = learning.sha256_file(frozen_report_path)

    if status == "COMPLETED":
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(draft_file, output_path)
        learning.make_read_only(output_path)

    timing = report["timing"]
    interval = learning._record_freeze_interval(
        run_root,
        actor=actor,
        session_id=report["session_id"],
        task="write_draft",
        start_utc=timing.get("start_utc"),
        end_utc=timing.get("end_utc"),
        duration_seconds=timing.get("duration_seconds"),
        timestamp_source=timing["timestamp_source"],
        status=status,
        reason=report["work_summary"],
        evidence_ref=frozen_report_path.relative_to(run_root).as_posix(),
    )
    state["writer_identity"][actor] = {
        "requested_model": learning.WRITERS[actor]["requested_model"],
        "actual_model": report["actual_model"],
        "actual_config": report.get("actual_config"),
        "identity_match": report["actual_model"].casefold() == learning.WRITERS[actor]["requested_model"].casefold(),
        "self_report_ref": frozen_report_path.relative_to(run_root).as_posix(),
        "self_report_sha256": report_sha,
    }

    if status == "COMPLETED":
        state["writer_status"][actor] = "PENDING_BUDGET_REVIEW"
        learning.append_jsonl(learning._run_paths(run_root)["handoffs"], {
            "schema_version": learning.SCHEMA_VERSION,
            "role": actor,
            "session_id": report["session_id"],
            "input_sha256": state["writer_packet_sha256"][actor],
            "common_content_sha256": state["writer_common_content_sha256"],
            "output_ref": output_path.relative_to(run_root).as_posix(),
            "output_sha256": learning.sha256_file(output_path),
            "execution_report_ref": frozen_report_path.relative_to(run_root).as_posix(),
            "execution_report_sha256": report_sha,
            "issues_encountered": report["issues_encountered"],
            "uncertainty": report["uncertainty"],
            "requested_model": learning.WRITERS[actor]["requested_model"],
            "actual_model": report["actual_model"],
            "actual_config": report.get("actual_config"),
            "timing_interval_id": interval["interval_id"],
            "validation": "PENDING_BUDGET_CHECK",
        })
    else:
        state["writer_status"][actor] = status

    learning._save_state(run_root, state)
    summary = learning.budget_summary(run_root)
    row = summary["actors"][actor]
    if row["unknown_intervals"]:
        state = learning._load_state(run_root)
        state["resume_state"] = "AWAITING_WRITERS"
        state.update({
            "state": "AWAITING_OWNER_BUDGET_APPROVAL",
            "waiting_for": "Owner",
            "artifact_to_open": str(frozen_report_path),
            "next_action": f"{actor} self-reported UNKNOWN timing. Preserve artifacts and let Owner decide; controller must not infer zero runtime.",
        })
        learning._save_state(run_root, state)
        return state

    overrun = max(float(row["overrun_seconds"] or 0.0), float(summary["total_overrun_seconds"] or 0.0))
    if overrun > 0:
        extension = report["budget_extension"]
        return learning.request_budget_extension(
            run_root,
            actor=actor,
            requested_seconds=float(extension["requested_seconds"]),
            scope="write_draft",
            reason=extension["reason"],
            evidence=f"{frozen_report_path.relative_to(run_root).as_posix()} | remaining_work={extension['remaining_work_if_approved']}",
        )

    state = learning._load_state(run_root)
    if status == "COMPLETED":
        learning._publish_writer_output(run_root, state, actor)
        if all(state["draft_sha256"].values()):
            learning._set_owner_gate(run_root, state)
        else:
            state.update({
                "state": "AWAITING_WRITERS",
                "resume_state": None,
                "waiting_for": "Writer Gemini + Writer Sol",
                "next_action": "One Writer result is frozen; wait for the other Writer. Do not reveal either draft to the unfinished Writer.",
            })
    else:
        state.update({
            "state": "AWAITING_WRITERS",
            "resume_state": None,
            "waiting_for": "Owner" if any(state["draft_sha256"].values()) else "Writer Gemini + Writer Sol",
            "next_action": f"{actor} {status.lower()}; pair remains incomplete. Keep evidence and do not substitute another Writer or old output.",
        })
    learning._save_state(run_root, state)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare/accept Writer self-reports for the Owner-first MVP")
    parser.add_argument("--runs-root", type=Path, default=learning.DEFAULT_RUNS_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("prepare", help="write self-report contract into both Writer input workspaces")
    p.add_argument("--run", required=True)

    a = sub.add_parser("accept", help="accept Writer-authored execution-report.json and optional completed draft")
    a.add_argument("--run", required=True)
    a.add_argument("--report", type=Path, required=True)
    a.add_argument("--draft", type=Path)

    args = parser.parse_args()
    run_root = learning._resolve_run(args.run, args.runs_root).resolve()
    try:
        result = prepare_report_contracts(run_root) if args.command == "prepare" else accept_writer_submission(run_root, report_file=args.report, draft_file=args.draft)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except learning.LearningError as exc:
        print(json.dumps({"status": "ERROR", "code": exc.code, "message": str(exc), "path": str(exc.path) if exc.path else None, "repair": exc.repair}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
