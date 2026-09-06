#!/usr/bin/env python3
"""Owner-first MVP handoff controller.

This module intentionally does not execute Planner or Writer agents. It freezes
role packets and accepts artifacts returned from separate agent sessions or a
host integration. Manual transfers remain labelled manual.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OVERLAY = REPO_ROOT / "products/sumer-writing/02_outline/section-overlays/P01.json"
DEFAULT_SUBSTRATE = REPO_ROOT / "products/sumer-writing/03_sections/P01/historical-substrate.json"
DEFAULT_RUNS_ROOT = REPO_ROOT / "runs"
SCHEMA_VERSION = "OWNER_FIRST_MVP_1"


class LearningError(RuntimeError):
    def __init__(self, code: str, message: str, *, path: Path | None = None, repair: str | None = None):
        self.code = code
        self.path = path
        self.repair = repair
        detail = f"{code}: {message}"
        if path is not None:
            detail += f" [path={path}]"
        if repair:
            detail += f" [repair={repair}]"
        super().__init__(detail)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LearningError("FILE_MISSING", "required file does not exist", path=path, repair="restore the declared artifact") from exc
    except json.JSONDecodeError as exc:
        raise LearningError("JSON_INVALID", str(exc), path=path, repair="fix the JSON without changing the declared session") from exc
    if not isinstance(value, dict):
        raise LearningError("JSON_OBJECT_REQUIRED", "expected a JSON object", path=path)
    return value


def atomic_write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")


def make_read_only(path: Path) -> None:
    try:
        path.chmod(0o444)
    except OSError:
        pass


def _safe_relative(value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise LearningError("PATH_ESCAPE_DENIED", "path must stay inside the declared role workspace", repair="use a role-relative input/output/scratch path")
    return rel


def _within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


class WorkspaceBroker:
    """Resolved-path boundary for a host that grants only this filesystem surface.

    This is not an OS sandbox. It is effective only when the host does not also
    grant shell, network or general filesystem access to the same role session.
    """

    def __init__(self, run_root: Path, role: str, session_id: str):
        self.run_root = run_root.resolve()
        self.role = role
        self.session_id = session_id
        self.root = (self.run_root / "agents" / role / session_id).resolve()
        if not self.root.exists():
            raise LearningError("WORKSPACE_MISSING", "role workspace does not exist", path=self.root)
        self.log = self.run_root / "control" / "access-events.jsonl"

    def _record(self, action: str, attempted: str, resolved: Path | None, result: str, code: str | None = None) -> None:
        append_jsonl(self.log, {
            "schema_version": SCHEMA_VERSION,
            "role": self.role,
            "session_id": self.session_id,
            "action": action,
            "attempted_path": attempted,
            "resolved_path": str(resolved) if resolved else None,
            "result": result,
            "code": code,
            "observed_at": utc_now(),
        })

    def _resolve(self, relative: str, *, write: bool) -> Path:
        action = "WRITE" if write else "READ"
        try:
            rel = _safe_relative(relative)
        except LearningError as exc:
            self._record(action, relative, None, "DENIED", exc.code)
            raise
        candidate = self.root / rel
        resolved = candidate.resolve(strict=False)
        if write:
            allowed = [(self.root / "output").resolve(), (self.root / "scratch").resolve()]
        else:
            allowed = [(self.root / "input").resolve(), (self.root / "output").resolve(), (self.root / "scratch").resolve()]
        if not any(_within(resolved, root) for root in allowed):
            self._record(action, relative, resolved, "DENIED", "ROLE_PATH_DENIED")
            raise LearningError("ROLE_PATH_DENIED", "resolved path is outside the role workspace", path=resolved)
        self._record(action, relative, resolved, "ALLOWED")
        return resolved

    def read_text(self, relative: str) -> str:
        path = self._resolve(relative, write=False)
        if not path.is_file():
            raise LearningError("FILE_MISSING", "role input does not exist", path=path)
        return path.read_text(encoding="utf-8")

    def write_text(self, relative: str, text: str) -> Path:
        path = self._resolve(relative, write=True)
        if path.exists() and relative.startswith("output/"):
            raise LearningError("OUTPUT_OVERWRITE_DENIED", "accepted/final role outputs are write-once", path=path, repair="write a new version in scratch or start a new owner-authorized session")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


def validate_authority(overlay: dict[str, Any], substrate: dict[str, Any]) -> None:
    if overlay.get("section") != "P01" or substrate.get("section") != "P01":
        raise LearningError("SECTION_MISMATCH", "owner-first MVP is bounded to P01")
    overlay_ids = overlay.get("historical_substrate_ids")
    primitives = substrate.get("primitives")
    if not isinstance(overlay_ids, list) or not isinstance(primitives, list):
        raise LearningError("AUTHORITY_MALFORMED", "P01 overlay/substrate IDs are missing")
    primitive_ids = {p.get("id") for p in primitives if isinstance(p, dict)}
    missing = [item for item in overlay_ids if item not in primitive_ids]
    if missing:
        raise LearningError("AUTHORITY_LINK_BROKEN", f"overlay references missing substrate primitives: {missing}")
    if overlay.get("historical_territory") != substrate.get("historical_territory"):
        raise LearningError("AUTHORITY_TERRITORY_MISMATCH", "overlay and substrate historical territory differ")
    if overlay.get("historical_change") != substrate.get("historical_change"):
        raise LearningError("AUTHORITY_CHANGE_MISMATCH", "overlay and substrate historical change differ")


def _run_paths(run_root: Path) -> dict[str, Path]:
    return {
        "state": run_root / "control" / "state.json",
        "authority_manifest": run_root / "control" / "authority.json",
        "handoffs": run_root / "control" / "handoffs.jsonl",
        "feedback": run_root / "control" / "owner-feedback.json",
        "planner_packet": run_root / "agents" / "plan" / "plan-001" / "input" / "packet.json",
        "plan_output": run_root / "agents" / "plan" / "plan-001" / "output" / "plan.json",
        "writer_packet": run_root / "agents" / "writer" / "writer-001" / "input" / "packet.json",
        "writer_output": run_root / "agents" / "writer" / "writer-001" / "output" / "draft.md",
        "owner_draft": run_root / "owner" / "draft.md",
    }


def _load_state(run_root: Path) -> dict[str, Any]:
    state = read_json(_run_paths(run_root)["state"])
    if state.get("schema_version") != SCHEMA_VERSION:
        raise LearningError("STATE_VERSION_MISMATCH", "unsupported owner-first MVP state", path=_run_paths(run_root)["state"])
    return state


def _verify_frozen(path: Path, expected_sha: str, label: str) -> None:
    if not path.is_file():
        raise LearningError("FROZEN_ARTIFACT_MISSING", f"{label} is missing", path=path, repair="restore the exact frozen artifact")
    observed = sha256_file(path)
    if observed != expected_sha:
        raise LearningError("FROZEN_ARTIFACT_CHANGED", f"{label} changed after freeze: expected {expected_sha}, observed {observed}", path=path, repair="restore the exact frozen bytes or start a new run")


def _verify_authority_snapshot(run_root: Path, state: dict[str, Any]) -> None:
    manifest = read_json(_run_paths(run_root)["authority_manifest"])
    for item in manifest.get("files", []):
        target = run_root / item["snapshot_ref"]
        _verify_frozen(target, item["sha256"], item["snapshot_ref"])
    expected = state.get("authority_manifest_sha256")
    if expected:
        _verify_frozen(_run_paths(run_root)["authority_manifest"], expected, "control/authority.json")


def _workspace_dirs(run_root: Path) -> None:
    for role, session in (("plan", "plan-001"), ("writer", "writer-001")):
        for name in ("input", "output", "scratch"):
            (run_root / "agents" / role / session / name).mkdir(parents=True, exist_ok=True)
    (run_root / "control" / "authority").mkdir(parents=True, exist_ok=True)
    (run_root / "owner").mkdir(parents=True, exist_ok=True)
    (run_root / "control" / "access-events.jsonl").touch()
    (run_root / "control" / "handoffs.jsonl").touch()


def prepare_run(
    run_root: Path,
    *,
    owner_request: str,
    overlay_path: Path = DEFAULT_OVERLAY,
    substrate_path: Path = DEFAULT_SUBSTRATE,
    test_only: bool = False,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    if run_root.exists() and any(run_root.iterdir()):
        raise LearningError("RUN_ALREADY_EXISTS", "run directory must be new and empty", path=run_root, repair="choose a new run id")
    if not owner_request.strip():
        raise LearningError("OWNER_REQUEST_REQUIRED", "owner request must be non-empty")
    overlay = read_json(overlay_path)
    substrate = read_json(substrate_path)
    validate_authority(overlay, substrate)
    _workspace_dirs(run_root)

    snapshots = []
    repo_root_resolved = REPO_ROOT.resolve()
    for source, name in ((overlay_path, "P01-overlay.json"), (substrate_path, "P01-historical-substrate.json")):
        destination = run_root / "control" / "authority" / name
        shutil.copyfile(source, destination)
        make_read_only(destination)
        source_resolved = source.resolve()
        source_ref = source_resolved.relative_to(repo_root_resolved).as_posix() if _within(source_resolved, repo_root_resolved) else str(source_resolved)
        snapshots.append({
            "source_ref": source_ref,
            "snapshot_ref": destination.relative_to(run_root).as_posix(),
            "sha256": sha256_file(destination),
        })

    authority_manifest = {
        "schema_version": SCHEMA_VERSION,
        "section": "P01",
        "files": snapshots,
        "validated_links": True,
        "captured_at": utc_now(),
    }
    atomic_write_json(_run_paths(run_root)["authority_manifest"], authority_manifest)
    make_read_only(_run_paths(run_root)["authority_manifest"])

    planner_packet = {
        "schema_version": SCHEMA_VERSION,
        "role": "planner",
        "session_id": "plan-001",
        "execution_mode": "MANUAL_PACKET_TRANSFER_OR_BOUNDED_HOST",
        "test_only": test_only,
        "owner_request": owner_request,
        "section": "P01",
        "suggested_reading_size_words": {"min": 450, "max": 650, "hard_gate": False},
        "task": "Create one short Plan that states what this excerpt will tell, which authorized sources it uses, and where it stops.",
        "authority": {
            "overlay": overlay,
            "historical_substrate": substrate,
            "source_hashes": {item["snapshot_ref"]: item["sha256"] for item in snapshots},
        },
        "boundaries": [
            "Do not expand evidence beyond this packet.",
            "Do not use B03, EXPLANATION_BEFORE_NEED, old benchmark verdicts, or reviewer predictions as a default target.",
            "Do not call Writer or approve the story plan.",
            "No fixed hook/beat/story grammar is required.",
        ],
        "required_output": {
            "format": "JSON object",
            "fields": ["section", "telling_scope", "source_refs", "stop_condition"],
            "source_refs_allowed": ["overlay:P01", *overlay["historical_substrate_ids"]],
        },
    }
    atomic_write_json(_run_paths(run_root)["planner_packet"], planner_packet)
    make_read_only(_run_paths(run_root)["planner_packet"])

    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_root.name,
        "test_only": test_only,
        "state": "AWAITING_PLANNER",
        "waiting_for": "Planner",
        "next_action": f"Give {_run_paths(run_root)['planner_packet']} to a separate Planner session, then freeze its output with scripts/learning.py freeze-plan.",
        "artifact_to_open": str(_run_paths(run_root)["planner_packet"]),
        "sessions": {"plan": "plan-001", "writer": "writer-001"},
        "authority_manifest_sha256": sha256_file(_run_paths(run_root)["authority_manifest"]),
        "planner_packet_sha256": sha256_file(_run_paths(run_root)["planner_packet"]),
        "writer_packet_sha256": None,
        "plan_sha256": None,
        "draft_sha256": None,
        "owner_feedback_sha256": None,
        "owner_request": owner_request,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "limitations": [
            "Manual packet transfer does not prove fresh-agent context isolation.",
            "WorkspaceBroker boundaries are enforced only when a host grants that broker as the sole filesystem surface.",
            "No live agent execution or causal quality claim is created by this controller.",
        ],
    }
    atomic_write_json(_run_paths(run_root)["state"], state)
    return state


def _validate_plan(plan: dict[str, Any], planner_packet: dict[str, Any]) -> None:
    if plan.get("section") != "P01":
        raise LearningError("PLAN_SECTION_INVALID", "plan.section must be P01")
    for field in ("telling_scope", "stop_condition"):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            raise LearningError("PLAN_FIELD_REQUIRED", f"plan.{field} must be a non-empty string")
    refs = plan.get("source_refs")
    if not isinstance(refs, list) or not refs or not all(isinstance(x, str) for x in refs):
        raise LearningError("PLAN_SOURCE_REFS_REQUIRED", "plan.source_refs must be a non-empty string list")
    allowed = set(planner_packet["required_output"]["source_refs_allowed"])
    extra = sorted(set(refs) - allowed)
    if extra:
        raise LearningError("PLAN_AUTHORITY_EXPANSION", f"plan cites unauthorized source refs: {extra}", repair="use only refs listed in the frozen Planner packet")


def _capture_optional_host_log(run_root: Path, role: str, session_id: str, host_log: Path | None) -> dict[str, Any] | None:
    if host_log is None:
        return None
    if not host_log.is_file():
        raise LearningError("HOST_LOG_MISSING", "declared host log does not exist", path=host_log)
    target = run_root / "control" / "host-logs" / f"{role}-{session_id}{host_log.suffix or '.log'}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(host_log, target)
    make_read_only(target)
    return {"ref": target.relative_to(run_root).as_posix(), "sha256": sha256_file(target)}


def freeze_plan(
    run_root: Path,
    *,
    session_id: str,
    source_file: Path,
    declared_reason: str,
    uncertainty: str,
    agent_created_at: str | None = None,
    host_log: Path | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "AWAITING_PLANNER":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot freeze Plan from state {state['state']}")
    if session_id != state["sessions"]["plan"]:
        raise LearningError("SESSION_MISMATCH", f"expected {state['sessions']['plan']}, received {session_id}")
    _verify_authority_snapshot(run_root, state)
    _verify_frozen(_run_paths(run_root)["planner_packet"], state["planner_packet_sha256"], "Planner packet")
    if _run_paths(run_root)["plan_output"].exists():
        raise LearningError("OUTPUT_OVERWRITE_DENIED", "Plan output was already accepted", path=_run_paths(run_root)["plan_output"])
    plan = read_json(source_file)
    planner_packet = read_json(_run_paths(run_root)["planner_packet"])
    _validate_plan(plan, planner_packet)
    _run_paths(run_root)["plan_output"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_file, _run_paths(run_root)["plan_output"])
    make_read_only(_run_paths(run_root)["plan_output"])
    plan_sha = sha256_file(_run_paths(run_root)["plan_output"])
    host_log_record = _capture_optional_host_log(run_root, "plan", session_id, host_log)

    authority_manifest = read_json(_run_paths(run_root)["authority_manifest"])
    overlay = read_json(run_root / authority_manifest["files"][0]["snapshot_ref"])
    substrate = read_json(run_root / authority_manifest["files"][1]["snapshot_ref"])
    writer_packet = {
        "schema_version": SCHEMA_VERSION,
        "role": "writer",
        "session_id": state["sessions"]["writer"],
        "execution_mode": "MANUAL_PACKET_TRANSFER_OR_BOUNDED_HOST",
        "test_only": state["test_only"],
        "owner_request": state["owner_request"],
        "section": "P01",
        "task": "Write one standalone Vietnamese historical-podcast excerpt from the frozen Plan and authority. Stop after this draft; do not self-review or reroll.",
        "suggested_reading_size_words": {"min": 450, "max": 650, "hard_gate": False},
        "frozen_plan": plan,
        "frozen_plan_sha256": plan_sha,
        "authority": {
            "overlay": overlay,
            "historical_substrate": substrate,
            "source_hashes": {item["snapshot_ref"]: item["sha256"] for item in authority_manifest["files"]},
        },
        "boundaries": [
            "Use only the frozen Plan and authority in this packet.",
            "Choose the telling freely inside those bounds; no required hook, beat count, or narrative grammar.",
            "Do not change the Plan, expand evidence, self-review, reroll, or call another role.",
            "A weak draft is still a valid artifact for Owner feedback.",
        ],
        "required_output": {"format": "UTF-8 Markdown prose", "one_draft_only": True},
    }
    atomic_write_json(_run_paths(run_root)["writer_packet"], writer_packet)
    make_read_only(_run_paths(run_root)["writer_packet"])

    received_at = utc_now()
    append_jsonl(_run_paths(run_root)["handoffs"], {
        "schema_version": SCHEMA_VERSION,
        "role": "planner",
        "session_id": session_id,
        "execution_mode": "MANUAL_PACKET_TRANSFER" if host_log_record is None else "HOST_LOG_ATTACHED_UNVERIFIED_CONTEXT_ISOLATION",
        "input_sha256": state["planner_packet_sha256"],
        "output_ref": _run_paths(run_root)["plan_output"].relative_to(run_root).as_posix(),
        "output_sha256": plan_sha,
        "declared_reason": declared_reason,
        "uncertainty": uncertainty,
        "agent_created_at": agent_created_at,
        "operator_received_at": received_at,
        "validation": "ACCEPTED",
        "host_log": host_log_record,
    })
    state.update({
        "state": "AWAITING_WRITER",
        "waiting_for": "Writer",
        "next_action": f"Give {_run_paths(run_root)['writer_packet']} to a separate Writer session, then freeze its output with scripts/learning.py freeze-draft.",
        "artifact_to_open": str(_run_paths(run_root)["writer_packet"]),
        "plan_sha256": plan_sha,
        "writer_packet_sha256": sha256_file(_run_paths(run_root)["writer_packet"]),
        "updated_at": received_at,
    })
    atomic_write_json(_run_paths(run_root)["state"], state)
    return state


def freeze_draft(
    run_root: Path,
    *,
    session_id: str,
    source_file: Path,
    declared_reason: str,
    uncertainty: str,
    agent_created_at: str | None = None,
    host_log: Path | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "AWAITING_WRITER":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot freeze draft from state {state['state']}")
    if session_id != state["sessions"]["writer"]:
        raise LearningError("SESSION_MISMATCH", f"expected {state['sessions']['writer']}, received {session_id}")
    _verify_authority_snapshot(run_root, state)
    _verify_frozen(_run_paths(run_root)["planner_packet"], state["planner_packet_sha256"], "Planner packet")
    _verify_frozen(_run_paths(run_root)["plan_output"], state["plan_sha256"], "Plan output")
    _verify_frozen(_run_paths(run_root)["writer_packet"], state["writer_packet_sha256"], "Writer packet")
    if _run_paths(run_root)["writer_output"].exists() or _run_paths(run_root)["owner_draft"].exists():
        raise LearningError("OUTPUT_OVERWRITE_DENIED", "draft was already accepted", repair="wait for Owner feedback or start a new owner-authorized run")
    if not source_file.is_file():
        raise LearningError("DRAFT_MISSING", "Writer draft does not exist", path=source_file)
    draft = source_file.read_text(encoding="utf-8")
    if not draft.strip():
        raise LearningError("DRAFT_EMPTY", "Writer draft is empty")
    _run_paths(run_root)["writer_output"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_file, _run_paths(run_root)["writer_output"])
    make_read_only(_run_paths(run_root)["writer_output"])
    draft_sha = sha256_file(_run_paths(run_root)["writer_output"])
    _run_paths(run_root)["owner_draft"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_run_paths(run_root)["writer_output"], _run_paths(run_root)["owner_draft"])
    make_read_only(_run_paths(run_root)["owner_draft"])
    if sha256_file(_run_paths(run_root)["owner_draft"]) != draft_sha:
        raise LearningError("OWNER_HANDOFF_HASH_MISMATCH", "owner copy does not match frozen Writer output")
    host_log_record = _capture_optional_host_log(run_root, "writer", session_id, host_log)
    received_at = utc_now()
    append_jsonl(_run_paths(run_root)["handoffs"], {
        "schema_version": SCHEMA_VERSION,
        "role": "writer",
        "session_id": session_id,
        "execution_mode": "MANUAL_PACKET_TRANSFER" if host_log_record is None else "HOST_LOG_ATTACHED_UNVERIFIED_CONTEXT_ISOLATION",
        "input_sha256": state["writer_packet_sha256"],
        "output_ref": _run_paths(run_root)["writer_output"].relative_to(run_root).as_posix(),
        "output_sha256": draft_sha,
        "owner_copy_ref": _run_paths(run_root)["owner_draft"].relative_to(run_root).as_posix(),
        "declared_reason": declared_reason,
        "uncertainty": uncertainty,
        "agent_created_at": agent_created_at,
        "operator_received_at": received_at,
        "validation": "ACCEPTED",
        "host_log": host_log_record,
    })
    state.update({
        "state": "AWAITING_OWNER_FEEDBACK",
        "waiting_for": "Owner",
        "next_action": f"Owner reads {_run_paths(run_root)['owner_draft']} and records verbatim feedback with scripts/learning.py feedback. Do not rerun Writer or Reviewer.",
        "artifact_to_open": str(_run_paths(run_root)["owner_draft"]),
        "draft_sha256": draft_sha,
        "updated_at": received_at,
    })
    atomic_write_json(_run_paths(run_root)["state"], state)
    return state


def record_owner_feedback(run_root: Path, *, feedback_text: str) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "AWAITING_OWNER_FEEDBACK":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot record Owner feedback from state {state['state']}")
    _verify_frozen(_run_paths(run_root)["writer_output"], state["draft_sha256"], "Writer draft")
    _verify_frozen(_run_paths(run_root)["owner_draft"], state["draft_sha256"], "Owner draft copy")
    if _run_paths(run_root)["feedback"].exists():
        raise LearningError("OWNER_FEEDBACK_ALREADY_RECORDED", "Owner feedback is immutable in this MVP run", path=_run_paths(run_root)["feedback"])
    if not feedback_text.strip():
        raise LearningError("OWNER_FEEDBACK_REQUIRED", "Owner feedback must be non-empty")
    feedback = {
        "schema_version": SCHEMA_VERSION,
        "authority": "OWNER",
        "draft_ref": _run_paths(run_root)["owner_draft"].relative_to(run_root).as_posix(),
        "draft_sha256": state["draft_sha256"],
        "verbatim_feedback": feedback_text,
        "recorded_at": utc_now(),
        "interpretation": "NOT_PERFORMED",
        "next_change": "OWNER_NOT_YET_SELECTED",
    }
    atomic_write_json(_run_paths(run_root)["feedback"], feedback)
    make_read_only(_run_paths(run_root)["feedback"])
    state.update({
        "state": "OWNER_FEEDBACK_RECORDED",
        "waiting_for": "Owner",
        "next_action": "Owner chooses the next change. This run does not create a new Plan, draft, reviewer verdict, symptom label, or causal conclusion automatically.",
        "artifact_to_open": str(_run_paths(run_root)["feedback"]),
        "owner_feedback_sha256": sha256_file(_run_paths(run_root)["feedback"]),
        "updated_at": utc_now(),
    })
    atomic_write_json(_run_paths(run_root)["state"], state)
    return state


def status(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state.get("planner_packet_sha256"):
        _verify_frozen(_run_paths(run_root)["planner_packet"], state["planner_packet_sha256"], "Planner packet")
    if state.get("writer_packet_sha256"):
        _verify_frozen(_run_paths(run_root)["writer_packet"], state["writer_packet_sha256"], "Writer packet")
    if state.get("draft_sha256"):
        _verify_frozen(_run_paths(run_root)["owner_draft"], state["draft_sha256"], "Owner draft copy")
    if state.get("owner_feedback_sha256"):
        _verify_frozen(_run_paths(run_root)["feedback"], state["owner_feedback_sha256"], "Owner feedback")
    return {
        "run_id": state["run_id"],
        "state": state["state"],
        "waiting_for": state["waiting_for"],
        "artifact_to_open": state["artifact_to_open"],
        "next_action": state["next_action"],
        "test_only": state["test_only"],
        "limitations": state["limitations"],
    }


def _resolve_run(run_arg: str, runs_root: Path) -> Path:
    candidate = Path(run_arg)
    if candidate.is_absolute() or len(candidate.parts) > 1:
        return candidate
    return runs_root / candidate


def _feedback_from_args(args: argparse.Namespace) -> str:
    if args.file is not None:
        return args.file.read_text(encoding="utf-8")
    if args.text is not None:
        return args.text
    raise LearningError("OWNER_FEEDBACK_REQUIRED", "provide --text or --file")


def main() -> int:
    parser = argparse.ArgumentParser(description="Owner-first MVP: freeze Planner/Writer handoffs and stop for Owner feedback")
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("prepare", help="snapshot P01 authority and prepare Planner packet")
    p.add_argument("--run", required=True)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--request")
    group.add_argument("--request-file", type=Path)
    p.add_argument("--overlay", type=Path, default=DEFAULT_OVERLAY)
    p.add_argument("--substrate", type=Path, default=DEFAULT_SUBSTRATE)
    p.add_argument("--test-only", action="store_true")

    for command, help_text in (("freeze-plan", "accept and freeze Planner output"), ("freeze-draft", "accept and freeze Writer draft")):
        q = sub.add_parser(command, help=help_text)
        q.add_argument("--run", required=True)
        q.add_argument("--session", required=True)
        q.add_argument("--file", type=Path, required=True)
        q.add_argument("--reason", required=True)
        q.add_argument("--uncertainty", required=True)
        q.add_argument("--agent-created-at")
        q.add_argument("--host-log", type=Path)

    f = sub.add_parser("feedback", help="record verbatim Owner feedback and stop")
    f.add_argument("--run", required=True)
    fg = f.add_mutually_exclusive_group(required=True)
    fg.add_argument("--text")
    fg.add_argument("--file", type=Path)

    s = sub.add_parser("status", help="show current state, artifact to open, and who is awaited")
    s.add_argument("--run", required=True)

    args = parser.parse_args()
    try:
        run_root = _resolve_run(args.run, args.runs_root).resolve()
        if args.command == "prepare":
            owner_request = args.request if args.request is not None else args.request_file.read_text(encoding="utf-8")
            result = prepare_run(run_root, owner_request=owner_request, overlay_path=args.overlay, substrate_path=args.substrate, test_only=args.test_only)
        elif args.command == "freeze-plan":
            result = freeze_plan(run_root, session_id=args.session, source_file=args.file, declared_reason=args.reason, uncertainty=args.uncertainty, agent_created_at=args.agent_created_at, host_log=args.host_log)
        elif args.command == "freeze-draft":
            result = freeze_draft(run_root, session_id=args.session, source_file=args.file, declared_reason=args.reason, uncertainty=args.uncertainty, agent_created_at=args.agent_created_at, host_log=args.host_log)
        elif args.command == "feedback":
            result = record_owner_feedback(run_root, feedback_text=_feedback_from_args(args))
        else:
            result = status(run_root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except LearningError as exc:
        print(json.dumps({
            "status": "ERROR",
            "code": exc.code,
            "message": str(exc),
            "path": str(exc.path) if exc.path else None,
            "repair": exc.repair,
        }, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
