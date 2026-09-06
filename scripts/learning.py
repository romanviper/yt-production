#!/usr/bin/env python3
"""Owner-first MVP controller with two Writers and Owner-approved time budgets.

The controller does not execute model hosts. It prepares/freeze-binds packets,
records operator/host-observed timing, enforces budget state transitions, and
stops for the Owner. Writer workspaces remain broker-scoped only; this is not an
OS sandbox and it does not prove model context isolation when a host grants other
filesystem, shell, or network capabilities.
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
SCHEMA_VERSION = "OWNER_FIRST_MVP_2"

ACTORS = ("sol_repo", "writer_gemini", "writer_sol")
WRITERS = {
    "writer_gemini": {
        "session_id": "writer-gemini-001",
        "requested_model": "Gemini 3.8 Flash",
        "sample": "A",
    },
    "writer_sol": {
        "session_id": "writer-sol-001",
        "requested_model": "GPT-5.6 Sol",
        "sample": "B",
    },
}
SOL_SESSION = "sol-repo-001"
BUDGET_UNIT = "CUMULATIVE_AGENT_SESSION_SECONDS"


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


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LearningError("TIMESTAMP_INVALID", f"invalid ISO timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise LearningError("TIMESTAMP_TZ_REQUIRED", f"timestamp must include timezone: {value}")
    return parsed.astimezone(timezone.utc)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LearningError("FILE_MISSING", "required file does not exist", path=path) from exc
    except json.JSONDecodeError as exc:
        raise LearningError("JSON_INVALID", str(exc), path=path) from exc
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


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            out.append(value)
    return out


def make_read_only(path: Path) -> None:
    try:
        path.chmod(0o444)
    except OSError:
        pass


def _safe_relative(value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or not rel.parts or ".." in rel.parts:
        raise LearningError("PATH_ESCAPE_DENIED", "path must stay inside the declared role workspace")
    return rel


def _within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


class WorkspaceBroker:
    """Resolved-path role boundary when supplied as the host's sole FS surface."""

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
        allowed = [
            (self.root / "output").resolve(),
            (self.root / "scratch").resolve(),
        ] if write else [
            (self.root / "input").resolve(),
            (self.root / "output").resolve(),
            (self.root / "scratch").resolve(),
        ]
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
            raise LearningError("OUTPUT_OVERWRITE_DENIED", "accepted role outputs are write-once", path=path)
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
        "budget": run_root / "control" / "budget.json",
        "budget_events": run_root / "control" / "budget-events.jsonl",
        "work_intervals": run_root / "control" / "work-intervals.jsonl",
        "cost_items": run_root / "control" / "cost-items.jsonl",
        "feedback": run_root / "control" / "owner-feedback.json",
        "sol_brief": run_root / "agents" / "sol_repo" / SOL_SESSION / "input" / "brief.json",
        "plan_output": run_root / "agents" / "sol_repo" / SOL_SESSION / "output" / "plan.json",
        "writer_gemini_packet": run_root / "agents" / "writer_gemini" / WRITERS["writer_gemini"]["session_id"] / "input" / "packet.json",
        "writer_sol_packet": run_root / "agents" / "writer_sol" / WRITERS["writer_sol"]["session_id"] / "input" / "packet.json",
        "writer_gemini_output": run_root / "agents" / "writer_gemini" / WRITERS["writer_gemini"]["session_id"] / "output" / "draft.md",
        "writer_sol_output": run_root / "agents" / "writer_sol" / WRITERS["writer_sol"]["session_id"] / "output" / "draft.md",
        "owner_sample_a": run_root / "owner" / "sample-A.md",
        "owner_sample_b": run_root / "owner" / "sample-B.md",
    }


def _writer_paths(run_root: Path, actor: str) -> tuple[Path, Path, Path]:
    if actor not in WRITERS:
        raise LearningError("WRITER_UNKNOWN", f"unknown Writer actor: {actor}")
    paths = _run_paths(run_root)
    if actor == "writer_gemini":
        return paths["writer_gemini_packet"], paths["writer_gemini_output"], paths["owner_sample_a"]
    return paths["writer_sol_packet"], paths["writer_sol_output"], paths["owner_sample_b"]


def _load_state(run_root: Path) -> dict[str, Any]:
    state = read_json(_run_paths(run_root)["state"])
    if state.get("schema_version") != SCHEMA_VERSION:
        raise LearningError("STATE_VERSION_MISMATCH", "unsupported owner-first MVP state")
    return state


def _save_state(run_root: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    atomic_write_json(_run_paths(run_root)["state"], state)


def _verify_frozen(path: Path, expected_sha: str, label: str) -> None:
    if not path.is_file():
        raise LearningError("FROZEN_ARTIFACT_MISSING", f"{label} is missing", path=path)
    observed = sha256_file(path)
    if observed != expected_sha:
        raise LearningError("FROZEN_ARTIFACT_CHANGED", f"{label} changed after freeze: expected {expected_sha}, observed {observed}", path=path)


def _verify_authority_snapshot(run_root: Path, state: dict[str, Any]) -> None:
    manifest = read_json(_run_paths(run_root)["authority_manifest"])
    for item in manifest.get("files", []):
        _verify_frozen(run_root / item["snapshot_ref"], item["sha256"], item["snapshot_ref"])
    _verify_frozen(_run_paths(run_root)["authority_manifest"], state["authority_manifest_sha256"], "control/authority.json")


def _workspace_dirs(run_root: Path) -> None:
    roles = [("sol_repo", SOL_SESSION)] + [(actor, meta["session_id"]) for actor, meta in WRITERS.items()]
    for role, session in roles:
        for name in ("input", "output", "scratch"):
            (run_root / "agents" / role / session / name).mkdir(parents=True, exist_ok=True)
    (run_root / "control" / "authority").mkdir(parents=True, exist_ok=True)
    (run_root / "owner").mkdir(parents=True, exist_ok=True)
    for name in ("access-events.jsonl", "handoffs.jsonl", "budget-events.jsonl", "work-intervals.jsonl", "cost-items.jsonl"):
        (run_root / "control" / name).touch()


def prepare_run(
    run_root: Path,
    *,
    owner_request: str,
    overlay_path: Path = DEFAULT_OVERLAY,
    substrate_path: Path = DEFAULT_SUBSTRATE,
    test_only: bool = False,
    code_ref: str | None = None,
) -> dict[str, Any]:
    """Prepare authority + Sol brief only. No agent is dispatchable before budget approval."""
    run_root = run_root.resolve()
    if run_root.exists() and any(run_root.iterdir()):
        raise LearningError("RUN_ALREADY_EXISTS", "run directory must be new and empty", path=run_root)
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
        snapshots.append({"source_ref": source_ref, "snapshot_ref": destination.relative_to(run_root).as_posix(), "sha256": sha256_file(destination)})

    authority_manifest = {
        "schema_version": SCHEMA_VERSION,
        "section": "P01",
        "files": snapshots,
        "validated_links": True,
        "captured_at": utc_now(),
    }
    atomic_write_json(_run_paths(run_root)["authority_manifest"], authority_manifest)
    make_read_only(_run_paths(run_root)["authority_manifest"])

    sol_brief = {
        "schema_version": SCHEMA_VERSION,
        "role": "sol_repo",
        "session_id": SOL_SESSION,
        "owner_request": owner_request,
        "section": "P01",
        "task": "Prepare one short Plan for the two Writers; do not write production prose or select a winning Writer.",
        "suggested_reading_size_words": {"min": 450, "max": 650, "hard_gate": False},
        "authority": {"overlay": overlay, "historical_substrate": substrate},
        "required_plan_fields": ["section", "telling_scope", "source_refs", "stop_condition"],
        "source_refs_allowed": ["overlay:P01", *overlay["historical_substrate_ids"]],
        "boundaries": [
            "No separate Planner, reviewer, time-auditor, or coordinator agent.",
            "Do not expand evidence beyond this brief.",
            "Do not write either Writer draft or choose a winner.",
            "No fixed hook/beat/story grammar is required.",
        ],
    }
    atomic_write_json(_run_paths(run_root)["sol_brief"], sol_brief)
    make_read_only(_run_paths(run_root)["sol_brief"])

    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_root.name,
        "test_only": test_only,
        "code_ref": code_ref,
        "state": "AWAITING_OWNER_BUDGET_APPROVAL",
        "resume_state": "READY_FOR_SOL_PLAN",
        "waiting_for": "Owner",
        "artifact_to_open": str(_run_paths(run_root)["sol_brief"]),
        "next_action": "Owner defines and approves a time budget before Sol repo or either Writer is dispatched.",
        "sessions": {
            "sol_repo": SOL_SESSION,
            "writer_gemini": WRITERS["writer_gemini"]["session_id"],
            "writer_sol": WRITERS["writer_sol"]["session_id"],
        },
        "authority_manifest_sha256": sha256_file(_run_paths(run_root)["authority_manifest"]),
        "sol_brief_sha256": sha256_file(_run_paths(run_root)["sol_brief"]),
        "plan_sha256": None,
        "writer_common_content_sha256": None,
        "writer_packet_sha256": {"writer_gemini": None, "writer_sol": None},
        "draft_sha256": {"writer_gemini": None, "writer_sol": None},
        "writer_status": {"writer_gemini": "NOT_STARTED", "writer_sol": "NOT_STARTED"},
        "writer_identity": {actor: {"requested_model": meta["requested_model"], "actual_model": None, "actual_config": None} for actor, meta in WRITERS.items()},
        "owner_feedback_sha256": None,
        "owner_request": owner_request,
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "limitations": [
            "Manual budget/approval records are operator-entered and are not an authentication system.",
            "Manual session windows are not active inference time.",
            "WorkspaceBroker boundaries hold only when the host grants the broker as the sole filesystem surface.",
            "No live model execution, model-quality claim, or default Writer selection is created by this controller.",
        ],
    }
    atomic_write_json(_run_paths(run_root)["state"], state)
    return state


def propose_budget(
    run_root: Path,
    *,
    budget_id: str,
    initial_cap_seconds: float,
    allocations: dict[str, float],
    scope: str,
    code_ref: str,
    attempts_allowed: dict[str, int] | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if _run_paths(run_root)["budget"].exists():
        raise LearningError("BUDGET_ALREADY_PROPOSED", "initial budget is write-once")
    if not budget_id.strip() or not scope.strip() or not code_ref.strip():
        raise LearningError("BUDGET_FIELDS_REQUIRED", "budget id, scope, and code_ref are required")
    if initial_cap_seconds <= 0:
        raise LearningError("BUDGET_CAP_INVALID", "initial cap must be positive")
    if set(allocations) != set(ACTORS) or any(float(allocations[a]) <= 0 for a in ACTORS):
        raise LearningError("BUDGET_ALLOCATIONS_INVALID", f"allocations must contain positive seconds for exactly {ACTORS}")
    if sum(float(allocations[a]) for a in ACTORS) > float(initial_cap_seconds) + 1e-9:
        raise LearningError("BUDGET_ALLOCATIONS_EXCEED_CAP", "actor allocations exceed the initial total cap")
    attempts = attempts_allowed or {actor: 1 for actor in ACTORS}
    if set(attempts) != set(ACTORS) or any(int(attempts[a]) != 1 for a in ACTORS):
        raise LearningError("ATTEMPT_SCOPE_INVALID", "MVP allows exactly one content attempt per Sol/Writer actor")
    budget = {
        "schema_version": SCHEMA_VERSION,
        "budget_id": budget_id,
        "request_id": f"{budget_id}:initial",
        "run_id": state["run_id"],
        "unit": BUDGET_UNIT,
        "scope": scope,
        "code_ref": code_ref,
        "attempts_allowed": attempts,
        "initial_cap_seconds": float(initial_cap_seconds),
        "allocations_seconds": {actor: float(allocations[actor]) for actor in ACTORS},
        "created_at": utc_now(),
    }
    atomic_write_json(_run_paths(run_root)["budget"], budget)
    make_read_only(_run_paths(run_root)["budget"])
    state["artifact_to_open"] = str(_run_paths(run_root)["budget"])
    state["next_action"] = f"Owner approves or rejects budget request {budget['request_id']}; no agent dispatch is permitted before approval."
    _save_state(run_root, state)
    return budget


def _initial_approval(events: list[dict[str, Any]], request_id: str) -> dict[str, Any] | None:
    matches = [e for e in events if e.get("type") == "INITIAL_BUDGET_DECISION" and e.get("request_id") == request_id]
    return matches[-1] if matches else None


def _extension_requests(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {e["request_id"]: e for e in events if e.get("type") == "EXTENSION_REQUEST" and isinstance(e.get("request_id"), str)}


def _extension_decisions(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {e["request_id"]: e for e in events if e.get("type") == "EXTENSION_DECISION" and isinstance(e.get("request_id"), str)}


def _timing_summary(run_root: Path, *, as_of: str | None = None) -> dict[str, Any]:
    intervals = read_jsonl(_run_paths(run_root)["work_intervals"])
    work = [x for x in intervals if x.get("kind") == "WORK"]
    waits = [x for x in intervals if x.get("kind") == "WAIT"]
    known_work = [x for x in work if isinstance(x.get("duration_seconds"), (int, float))]
    unknown_work = [x for x in work if x.get("duration_seconds") is None]
    total_work = sum(float(x["duration_seconds"]) for x in known_work)
    actor_used = {actor: sum(float(x["duration_seconds"]) for x in known_work if x.get("actor") == actor) for actor in ACTORS}
    actor_unknown = {actor: sum(1 for x in unknown_work if x.get("actor") == actor) for actor in ACTORS}
    wait_known = [x for x in waits if isinstance(x.get("duration_seconds"), (int, float))]
    waiting_seconds = sum(float(x["duration_seconds"]) for x in wait_known)

    state = _load_state(run_root)
    end = _parse_utc(as_of or state.get("updated_at") or utc_now())
    start = _parse_utc(state["created_at"])
    elapsed = max(0.0, (end - start).total_seconds())

    writer_intervals = [x for x in known_work if x.get("actor") in WRITERS and x.get("start_utc") and x.get("end_utc")]
    pair_elapsed: float | None = None
    if writer_intervals:
        pair_start = min(_parse_utc(x["start_utc"]) for x in writer_intervals)
        pair_end = max(_parse_utc(x["end_utc"]) for x in writer_intervals)
        pair_elapsed = max(0.0, (pair_end - pair_start).total_seconds())
    return {
        "elapsed_seconds": elapsed,
        "total_work_seconds": total_work,
        "waiting_seconds": waiting_seconds,
        "unknown_work_intervals": len(unknown_work),
        "actor_used_seconds": actor_used,
        "actor_unknown_intervals": actor_unknown,
        "writer_pair_elapsed_seconds": pair_elapsed,
    }


def budget_summary(run_root: Path, *, as_of: str | None = None) -> dict[str, Any]:
    paths = _run_paths(run_root)
    if not paths["budget"].is_file():
        return {
            "status": "NOT_PROPOSED",
            "unit": BUDGET_UNIT,
            "approved": False,
            "timing": _timing_summary(run_root, as_of=as_of),
        }
    budget = read_json(paths["budget"])
    events = read_jsonl(paths["budget_events"])
    initial = _initial_approval(events, budget["request_id"])
    approved = bool(initial and initial.get("decision") == "APPROVED")
    allocations = {actor: (float(budget["allocations_seconds"][actor]) if approved else 0.0) for actor in ACTORS}
    extension_approved_total = 0.0
    extension_approved_by_actor = {actor: 0.0 for actor in ACTORS}
    requests = _extension_requests(events)
    decisions = _extension_decisions(events)
    for request_id, decision in decisions.items():
        if decision.get("decision") != "APPROVED" or request_id not in requests:
            continue
        seconds = float(decision.get("approved_seconds") or 0.0)
        actor = requests[request_id]["actor"]
        allocations[actor] += seconds
        extension_approved_by_actor[actor] += seconds
        extension_approved_total += seconds
    timing = _timing_summary(run_root, as_of=as_of)
    used = timing["actor_used_seconds"]
    unknown = timing["actor_unknown_intervals"]
    actor_rows = {}
    for actor in ACTORS:
        remaining = None if unknown[actor] else allocations[actor] - used[actor]
        actor_rows[actor] = {
            "allocated_seconds": allocations[actor],
            "used_seconds": used[actor],
            "unknown_intervals": unknown[actor],
            "remaining_seconds": remaining,
            "overrun_seconds": None if remaining is None else max(0.0, -remaining),
            "extension_approved_seconds": extension_approved_by_actor[actor],
        }
    total_approved = (float(budget["initial_cap_seconds"]) if approved else 0.0) + extension_approved_total
    total_remaining = None if timing["unknown_work_intervals"] else total_approved - timing["total_work_seconds"]
    pending_requests = [r for rid, r in requests.items() if rid not in decisions or decisions[rid].get("decision") not in {"APPROVED", "REJECTED"}]
    return {
        "status": "APPROVED" if approved else (initial.get("decision") if initial else "PENDING_OWNER_APPROVAL"),
        "approved": approved,
        "budget_id": budget["budget_id"],
        "request_id": budget["request_id"],
        "unit": budget["unit"],
        "scope": budget["scope"],
        "code_ref": budget["code_ref"],
        "initial_cap_seconds": float(budget["initial_cap_seconds"]),
        "total_approved_seconds": total_approved,
        "total_used_seconds": timing["total_work_seconds"],
        "total_remaining_seconds": total_remaining,
        "total_overrun_seconds": None if total_remaining is None else max(0.0, -total_remaining),
        "actors": actor_rows,
        "pending_extension_requests": pending_requests,
        "timing": timing,
    }


def record_budget_decision(
    run_root: Path,
    *,
    request_id: str,
    decision: str,
    owner_text: str,
    source_ref: str,
    actor: str | None = None,
    scope: str | None = None,
    approved_seconds: float | None = None,
) -> dict[str, Any]:
    """Record an Owner decision. Manual entry is preserved verbatim, not authenticated."""
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if not owner_text.strip() or not source_ref.strip():
        raise LearningError("OWNER_APPROVAL_EVIDENCE_REQUIRED", "verbatim Owner text and source_ref are required")
    decision = decision.upper()
    if decision not in {"APPROVED", "REJECTED"}:
        raise LearningError("OWNER_DECISION_INVALID", "decision must be APPROVED or REJECTED")
    budget = read_json(_run_paths(run_root)["budget"])
    events = read_jsonl(_run_paths(run_root)["budget_events"])
    if request_id == budget["request_id"]:
        if _initial_approval(events, request_id) is not None:
            raise LearningError("BUDGET_DECISION_ALREADY_RECORDED", "initial budget decision is immutable")
        event = {
            "schema_version": SCHEMA_VERSION,
            "type": "INITIAL_BUDGET_DECISION",
            "run_id": state["run_id"],
            "request_id": request_id,
            "decision": decision,
            "owner_text": owner_text,
            "source_ref": source_ref,
            "recorded_at": utc_now(),
        }
        append_jsonl(_run_paths(run_root)["budget_events"], event)
        if decision == "APPROVED":
            state.update({
                "state": "READY_FOR_SOL_PLAN",
                "resume_state": None,
                "waiting_for": "Sol repo",
                "artifact_to_open": str(_run_paths(run_root)["sol_brief"]),
                "next_action": "Sol repo prepares the single Plan within the approved budget, then freeze-plan records it. No separate Planner is used.",
            })
        else:
            state.update({
                "state": "AWAITING_OWNER_BUDGET_APPROVAL",
                "waiting_for": "Owner",
                "next_action": "Budget was rejected; no agent work may be dispatched until Owner approves a new owner-authorized budget in a new run.",
            })
        _save_state(run_root, state)
        return event

    requests = _extension_requests(events)
    if request_id not in requests:
        raise LearningError("EXTENSION_REQUEST_NOT_FOUND", f"no extension request {request_id} exists")
    request = requests[request_id]
    if request_id in _extension_decisions(events):
        raise LearningError("EXTENSION_DECISION_ALREADY_RECORDED", "extension decision is immutable")
    if actor != request["actor"] or scope != request["scope"]:
        raise LearningError("EXTENSION_APPROVAL_SCOPE_MISMATCH", "approval actor/scope must exactly match the pending request")
    if decision == "APPROVED":
        if approved_seconds is None or approved_seconds <= 0 or approved_seconds > float(request["requested_seconds"]):
            raise LearningError("EXTENSION_AMOUNT_INVALID", "approved_seconds must be >0 and no greater than the requested amount")
    elif approved_seconds not in (None, 0):
        raise LearningError("REJECTED_EXTENSION_HAS_AMOUNT", "rejected extension cannot grant seconds")
    event = {
        "schema_version": SCHEMA_VERSION,
        "type": "EXTENSION_DECISION",
        "run_id": state["run_id"],
        "request_id": request_id,
        "actor": actor,
        "scope": scope,
        "decision": decision,
        "approved_seconds": float(approved_seconds or 0.0),
        "owner_text": owner_text,
        "source_ref": source_ref,
        "recorded_at": utc_now(),
    }
    append_jsonl(_run_paths(run_root)["budget_events"], event)
    if decision == "APPROVED":
        summary = budget_summary(run_root)
        row = summary["actors"][actor]
        if row["remaining_seconds"] is not None and row["remaining_seconds"] >= 0 and summary["total_remaining_seconds"] is not None and summary["total_remaining_seconds"] >= 0:
            resume = state.get("resume_state") or "AWAITING_WRITERS"
            state["state"] = resume
            state["resume_state"] = None
            if resume == "AWAITING_WRITERS":
                _publish_pending_writer_outputs(run_root, state)
                if all(state["draft_sha256"].values()):
                    _set_owner_gate(run_root, state)
                else:
                    state["waiting_for"] = "Writer Gemini + Writer Sol"
                    state["next_action"] = "Resume only the already-authorized unfinished Writer work; no extra content attempt was granted."
            elif resume == "READY_FOR_SOL_PLAN":
                state["waiting_for"] = "Sol repo"
        else:
            state["state"] = "AWAITING_OWNER_BUDGET_APPROVAL"
            state["waiting_for"] = "Owner"
            state["next_action"] = "Approved extension is insufficient to clear the recorded overrun/unknown accounting; do not resume agent work."
    else:
        state["state"] = "AWAITING_OWNER_BUDGET_APPROVAL"
        state["waiting_for"] = "Owner"
        state["next_action"] = "Extension was rejected; preserve artifacts and do not resume agent work."
    _save_state(run_root, state)
    return event


def request_budget_extension(
    run_root: Path,
    *,
    actor: str,
    requested_seconds: float,
    scope: str,
    reason: str,
    evidence: str,
    request_id: str | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if actor not in ACTORS or requested_seconds <= 0 or not scope.strip() or not reason.strip() or not evidence.strip():
        raise LearningError("EXTENSION_REQUEST_INVALID", "actor, positive seconds, scope, reason and evidence are required")
    summary = budget_summary(run_root)
    if not summary.get("approved"):
        raise LearningError("BUDGET_NOT_APPROVED", "initial budget is not approved")
    request_id = request_id or f"{summary['budget_id']}:extension:{len(_extension_requests(read_jsonl(_run_paths(run_root)['budget_events']))) + 1:03d}"
    if request_id in _extension_requests(read_jsonl(_run_paths(run_root)["budget_events"])):
        raise LearningError("EXTENSION_REQUEST_DUPLICATE", f"request {request_id} already exists")
    actor_row = summary["actors"][actor]
    event = {
        "schema_version": SCHEMA_VERSION,
        "type": "EXTENSION_REQUEST",
        "run_id": state["run_id"],
        "request_id": request_id,
        "actor": actor,
        "scope": scope,
        "initial_cap_seconds": summary["initial_cap_seconds"],
        "approved_extensions_seconds": summary["total_approved_seconds"] - summary["initial_cap_seconds"],
        "total_used_seconds": summary["total_used_seconds"],
        "remaining_seconds": summary["total_remaining_seconds"],
        "actor_remaining_seconds": actor_row["remaining_seconds"],
        "actual_overrun_seconds": actor_row["overrun_seconds"],
        "requested_seconds": float(requested_seconds),
        "reason": reason,
        "evidence": evidence,
        "requested_at": utc_now(),
    }
    append_jsonl(_run_paths(run_root)["budget_events"], event)
    if state["state"] != "AWAITING_OWNER_BUDGET_APPROVAL":
        state["resume_state"] = state["state"]
    state.update({
        "state": "AWAITING_OWNER_BUDGET_APPROVAL",
        "waiting_for": "Owner",
        "artifact_to_open": str(_run_paths(run_root)["budget_events"]),
        "next_action": f"Owner decides extension {request_id}. Rejection or silence does not resume work.",
    })
    _save_state(run_root, state)
    return event


def _record_interval(
    run_root: Path,
    *,
    actor: str,
    session_id: str,
    task: str,
    attempt: int,
    kind: str = "WORK",
    start_utc: str | None = None,
    end_utc: str | None = None,
    duration_seconds: float | None = None,
    timestamp_source: str = "UNKNOWN",
    status: str = "COMPLETED",
    reason: str = "",
    evidence_ref: str | None = None,
    interval_id: str | None = None,
) -> dict[str, Any]:
    if actor not in (*ACTORS, "owner_wait", "host_queue"):
        raise LearningError("TIMING_ACTOR_INVALID", f"unsupported timing actor {actor}")
    kind = kind.upper()
    if kind not in {"WORK", "WAIT"}:
        raise LearningError("TIMING_KIND_INVALID", "timing kind must be WORK or WAIT")
    if attempt < 0:
        raise LearningError("TIMING_ATTEMPT_INVALID", "attempt must be non-negative")
    computed: float | None = None
    start_dt = _parse_utc(start_utc) if start_utc is not None else None
    end_dt = _parse_utc(end_utc) if end_utc is not None else None
    if start_dt is not None and end_dt is not None:
        computed = (end_dt - start_dt).total_seconds()
        if computed < 0:
            raise LearningError("TIMING_CLOCK_REVERSED", "end precedes start")
    if duration_seconds is not None:
        if duration_seconds < 0:
            raise LearningError("TIMING_DURATION_INVALID", "duration must be non-negative")
        if computed is not None and abs(computed - duration_seconds) > 0.01:
            raise LearningError("TIMING_DURATION_MISMATCH", "declared duration disagrees with wall timestamps")
        computed = float(duration_seconds)
    if computed is None:
        status = "UNKNOWN"
    if timestamp_source == "OPERATOR_OBSERVED_SESSION_WINDOW" and (start_dt is None or end_dt is None):
        raise LearningError("OPERATOR_WINDOW_INCOMPLETE", "operator-observed windows require start and end")

    existing = read_jsonl(_run_paths(run_root)["work_intervals"])
    if start_dt is not None and end_dt is not None:
        for old in existing:
            if old.get("actor") != actor or old.get("kind") != kind or not old.get("start_utc") or not old.get("end_utc"):
                continue
            old_start = _parse_utc(old["start_utc"])
            old_end = _parse_utc(old["end_utc"])
            if max(start_dt, old_start) < min(end_dt, old_end):
                raise LearningError("TIMING_OVERLAP_DENIED", f"overlapping {kind} intervals for actor {actor} would double count time")
    interval_id = interval_id or f"I{len(existing) + 1:04d}"
    if any(x.get("interval_id") == interval_id for x in existing):
        raise LearningError("TIMING_INTERVAL_DUPLICATE", f"interval id {interval_id} already exists")
    event = {
        "schema_version": SCHEMA_VERSION,
        "interval_id": interval_id,
        "run_id": _load_state(run_root)["run_id"],
        "kind": kind,
        "actor": actor,
        "session_id": session_id,
        "task": task,
        "attempt": attempt,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "duration_seconds": computed,
        "timestamp_source": timestamp_source,
        "status": status,
        "reason": reason,
        "evidence_ref": evidence_ref,
        "recorded_at": utc_now(),
    }
    append_jsonl(_run_paths(run_root)["work_intervals"], event)
    return event


def record_wait_interval(run_root: Path, **kwargs: Any) -> dict[str, Any]:
    kwargs["kind"] = "WAIT"
    return _record_interval(run_root, **kwargs)


def _require_budget_to_start(run_root: Path, actor: str) -> dict[str, Any]:
    summary = budget_summary(run_root)
    if not summary.get("approved"):
        raise LearningError("BUDGET_NOT_APPROVED", "Owner-approved budget is required before agent work")
    row = summary["actors"][actor]
    if row["unknown_intervals"]:
        raise LearningError("BUDGET_ACCOUNTING_UNKNOWN", f"{actor} has UNKNOWN timing; do not start more work")
    if row["remaining_seconds"] is None or row["remaining_seconds"] <= 0:
        raise LearningError("BUDGET_EXHAUSTED", f"{actor} has no approved seconds remaining")
    if summary["total_remaining_seconds"] is None or summary["total_remaining_seconds"] <= 0:
        raise LearningError("BUDGET_EXHAUSTED", "round has no approved seconds remaining")
    return summary


def _validate_plan(plan: dict[str, Any], sol_brief: dict[str, Any]) -> None:
    if plan.get("section") != "P01":
        raise LearningError("PLAN_SECTION_INVALID", "plan.section must be P01")
    for field in ("telling_scope", "stop_condition"):
        if not isinstance(plan.get(field), str) or not plan[field].strip():
            raise LearningError("PLAN_FIELD_REQUIRED", f"plan.{field} must be non-empty")
    refs = plan.get("source_refs")
    if not isinstance(refs, list) or not refs or not all(isinstance(x, str) for x in refs):
        raise LearningError("PLAN_SOURCE_REFS_REQUIRED", "plan.source_refs must be a non-empty string list")
    extra = sorted(set(refs) - set(sol_brief["source_refs_allowed"]))
    if extra:
        raise LearningError("PLAN_AUTHORITY_EXPANSION", f"plan cites unauthorized refs: {extra}")


def _record_freeze_interval(run_root: Path, *, actor: str, session_id: str, task: str, start_utc: str | None, end_utc: str | None, duration_seconds: float | None, timestamp_source: str, status: str, reason: str, evidence_ref: str | None) -> dict[str, Any]:
    return _record_interval(run_root, actor=actor, session_id=session_id, task=task, attempt=1, start_utc=start_utc, end_utc=end_utc, duration_seconds=duration_seconds, timestamp_source=timestamp_source, status=status, reason=reason, evidence_ref=evidence_ref)


def _budget_block_after_interval(run_root: Path, state: dict[str, Any], actor: str, *, scope: str, evidence: str) -> bool:
    summary = budget_summary(run_root)
    row = summary["actors"][actor]
    if row["unknown_intervals"]:
        if state["state"] != "AWAITING_OWNER_BUDGET_APPROVAL":
            state["resume_state"] = state["state"]
        state.update({
            "state": "AWAITING_OWNER_BUDGET_APPROVAL",
            "waiting_for": "Owner",
            "next_action": f"Timing for {actor} is UNKNOWN; preserve artifacts and do not start new work until Owner decides how to proceed.",
        })
        _save_state(run_root, state)
        return True
    actor_over = float(row["overrun_seconds"] or 0.0)
    total_over = float(summary["total_overrun_seconds"] or 0.0)
    if actor_over > 0 or total_over > 0:
        _save_state(run_root, state)
        request_budget_extension(
            run_root,
            actor=actor,
            requested_seconds=max(actor_over, total_over, 0.001),
            scope=scope,
            reason="Recorded work exceeded the Owner-approved budget; request covers the observed overrun only.",
            evidence=evidence,
        )
        return True
    return False


def freeze_plan(
    run_root: Path,
    *,
    session_id: str,
    source_file: Path,
    declared_reason: str,
    uncertainty: str,
    start_utc: str | None = None,
    end_utc: str | None = None,
    duration_seconds: float | None = None,
    timestamp_source: str = "UNKNOWN",
    agent_created_at: str | None = None,
    host_log: Path | None = None,
) -> dict[str, Any]:
    del agent_created_at
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "READY_FOR_SOL_PLAN":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot freeze Plan from state {state['state']}")
    if session_id != state["sessions"]["sol_repo"]:
        raise LearningError("SESSION_MISMATCH", f"expected {state['sessions']['sol_repo']}, received {session_id}")
    _require_budget_to_start(run_root, "sol_repo")
    _verify_authority_snapshot(run_root, state)
    _verify_frozen(_run_paths(run_root)["sol_brief"], state["sol_brief_sha256"], "Sol repo brief")
    if _run_paths(run_root)["plan_output"].exists():
        raise LearningError("OUTPUT_OVERWRITE_DENIED", "Plan output was already accepted")
    plan = read_json(source_file)
    _validate_plan(plan, read_json(_run_paths(run_root)["sol_brief"]))
    _run_paths(run_root)["plan_output"].parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_file, _run_paths(run_root)["plan_output"])
    make_read_only(_run_paths(run_root)["plan_output"])
    plan_sha = sha256_file(_run_paths(run_root)["plan_output"])
    host_ref = None
    if host_log is not None:
        if not host_log.is_file():
            raise LearningError("HOST_LOG_MISSING", "declared host log does not exist", path=host_log)
        target = run_root / "control" / "host-logs" / f"sol_repo-{session_id}{host_log.suffix or '.log'}"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(host_log, target)
        make_read_only(target)
        host_ref = target.relative_to(run_root).as_posix()
    interval = _record_freeze_interval(
        run_root,
        actor="sol_repo",
        session_id=session_id,
        task="prepare_plan",
        start_utc=start_utc,
        end_utc=end_utc,
        duration_seconds=duration_seconds,
        timestamp_source=timestamp_source,
        status="COMPLETED",
        reason=declared_reason,
        evidence_ref=host_ref,
    )
    append_jsonl(_run_paths(run_root)["handoffs"], {
        "schema_version": SCHEMA_VERSION,
        "role": "sol_repo",
        "session_id": session_id,
        "input_sha256": state["sol_brief_sha256"],
        "output_ref": _run_paths(run_root)["plan_output"].relative_to(run_root).as_posix(),
        "output_sha256": plan_sha,
        "declared_reason": declared_reason,
        "uncertainty": uncertainty,
        "timing_interval_id": interval["interval_id"],
        "validation": "ACCEPTED",
    })
    state["plan_sha256"] = plan_sha
    state["resume_state"] = "READY_FOR_WRITER_PACKETS"
    state["state"] = "READY_FOR_WRITER_PACKETS"
    if _budget_block_after_interval(run_root, state, "sol_repo", scope="prepare_plan", evidence=_run_paths(run_root)["plan_output"].relative_to(run_root).as_posix()):
        return _load_state(run_root)
    _create_writer_packets(run_root, state, plan)
    _save_state(run_root, state)
    return state


def _create_writer_packets(run_root: Path, state: dict[str, Any], plan: dict[str, Any]) -> None:
    _require_budget_to_start(run_root, "writer_gemini")
    _require_budget_to_start(run_root, "writer_sol")
    authority_manifest = read_json(_run_paths(run_root)["authority_manifest"])
    overlay = read_json(run_root / authority_manifest["files"][0]["snapshot_ref"])
    substrate = read_json(run_root / authority_manifest["files"][1]["snapshot_ref"])
    common_payload = {
        "schema_version": SCHEMA_VERSION,
        "owner_request": state["owner_request"],
        "section": "P01",
        "task": "Write one standalone Vietnamese historical-podcast excerpt from the frozen Plan and authority. Stop after this single attempt; do not self-review or reroll.",
        "suggested_reading_size_words": {"min": 450, "max": 650, "hard_gate": False},
        "frozen_plan": plan,
        "frozen_plan_sha256": state["plan_sha256"],
        "authority": {
            "overlay": overlay,
            "historical_substrate": substrate,
            "source_hashes": {item["snapshot_ref"]: item["sha256"] for item in authority_manifest["files"]},
        },
        "boundaries": [
            "Use only the frozen Plan and authority in this packet.",
            "Choose the telling freely; no required hook, beat count, or narrative grammar.",
            "Do not change the Plan, expand evidence, inspect the other Writer, self-review, reroll, or call another role.",
            "A weak draft is still a valid artifact for Owner comparison.",
        ],
        "required_output": {"format": "UTF-8 Markdown prose", "one_content_attempt_only": True},
    }
    common_sha = canonical_sha256(common_payload)
    state["writer_common_content_sha256"] = common_sha
    for actor, meta in WRITERS.items():
        packet_path, _, _ = _writer_paths(run_root, actor)
        packet = {
            "schema_version": SCHEMA_VERSION,
            "role": actor,
            "session_id": meta["session_id"],
            "requested_model": meta["requested_model"],
            "common_content_sha256": common_sha,
            "common": common_payload,
            "session_metadata": {"sample": meta["sample"], "actual_model": None, "actual_config": None},
        }
        atomic_write_json(packet_path, packet)
        make_read_only(packet_path)
        state["writer_packet_sha256"][actor] = sha256_file(packet_path)
    state.update({
        "state": "AWAITING_WRITERS",
        "resume_state": None,
        "waiting_for": "Writer Gemini + Writer Sol",
        "artifact_to_open": [str(_run_paths(run_root)["writer_gemini_packet"]), str(_run_paths(run_root)["writer_sol_packet"])],
        "next_action": "Dispatch each packet to its separate Writer session. The first draft does not end the round and must not be shown to the other Writer.",
    })


def _actor_from_session(state: dict[str, Any], session_id: str) -> str:
    matches = [actor for actor in WRITERS if state["sessions"][actor] == session_id]
    if len(matches) != 1:
        raise LearningError("SESSION_MISMATCH", f"session {session_id} is not one of the two Writer sessions")
    return matches[0]


def _publish_writer_output(run_root: Path, state: dict[str, Any], actor: str) -> None:
    _, output_path, owner_path = _writer_paths(run_root, actor)
    if not output_path.is_file():
        return
    draft_sha = sha256_file(output_path)
    if owner_path.exists():
        _verify_frozen(owner_path, draft_sha, f"Owner sample {WRITERS[actor]['sample']}")
    else:
        shutil.copyfile(output_path, owner_path)
        make_read_only(owner_path)
    if sha256_file(owner_path) != draft_sha:
        raise LearningError("OWNER_HANDOFF_HASH_MISMATCH", f"Owner sample for {actor} does not match Writer output")
    state["draft_sha256"][actor] = draft_sha
    state["writer_status"][actor] = "ACCEPTED"
    append_jsonl(_run_paths(run_root)["handoffs"], {
        "schema_version": SCHEMA_VERSION,
        "role": actor,
        "session_id": state["sessions"][actor],
        "input_sha256": state["writer_packet_sha256"][actor],
        "output_ref": output_path.relative_to(run_root).as_posix(),
        "output_sha256": draft_sha,
        "owner_copy_ref": owner_path.relative_to(run_root).as_posix(),
        "owner_copy_sha256": sha256_file(owner_path),
        "validation": "ACCEPTED",
    })


def _publish_pending_writer_outputs(run_root: Path, state: dict[str, Any]) -> None:
    for actor in WRITERS:
        if state["writer_status"].get(actor) == "PENDING_BUDGET_REVIEW":
            _publish_writer_output(run_root, state, actor)


def _set_owner_gate(run_root: Path, state: dict[str, Any]) -> None:
    state.update({
        "state": "AWAITING_OWNER_FEEDBACK",
        "resume_state": None,
        "waiting_for": "Owner",
        "artifact_to_open": [str(_run_paths(run_root)["owner_sample_a"]), str(_run_paths(run_root)["owner_sample_b"])],
        "next_action": "Owner reads both samples, may choose A/B/TIE/UNSELECTED, and records verbatim feedback. Do not rerun either Writer or auto-select a model.",
    })


def freeze_draft(
    run_root: Path,
    *,
    session_id: str,
    source_file: Path,
    declared_reason: str,
    uncertainty: str,
    actual_model: str | None = None,
    actual_config: str | None = None,
    start_utc: str | None = None,
    end_utc: str | None = None,
    duration_seconds: float | None = None,
    timestamp_source: str = "UNKNOWN",
    agent_created_at: str | None = None,
    host_log: Path | None = None,
) -> dict[str, Any]:
    del agent_created_at
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "AWAITING_WRITERS":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot freeze draft from state {state['state']}")
    actor = _actor_from_session(state, session_id)
    if state["writer_status"][actor] in {"ACCEPTED", "PENDING_BUDGET_REVIEW"}:
        raise LearningError("OUTPUT_OVERWRITE_DENIED", f"{actor} already produced an accepted/pending output")
    _require_budget_to_start(run_root, actor)
    _verify_authority_snapshot(run_root, state)
    _verify_frozen(_run_paths(run_root)["plan_output"], state["plan_sha256"], "Plan output")
    packet_path, output_path, _ = _writer_paths(run_root, actor)
    _verify_frozen(packet_path, state["writer_packet_sha256"][actor], f"{actor} packet")
    packet = read_json(packet_path)
    if packet["common_content_sha256"] != state["writer_common_content_sha256"]:
        raise LearningError("WRITER_COMMON_CONTENT_CHANGED", "Writer common content hash changed")
    if not source_file.is_file() or not source_file.read_text(encoding="utf-8").strip():
        raise LearningError("DRAFT_MISSING", "Writer draft is missing or empty", path=source_file)
    if not actual_model:
        raise LearningError("MODEL_IDENTITY_REQUIRED", "actual host model/config identity must be recorded; do not label an unknown model as Gemini/Sol")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_file, output_path)
    make_read_only(output_path)
    host_ref = None
    if host_log is not None:
        if not host_log.is_file():
            raise LearningError("HOST_LOG_MISSING", "declared host log does not exist", path=host_log)
        target = run_root / "control" / "host-logs" / f"{actor}-{session_id}{host_log.suffix or '.log'}"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(host_log, target)
        make_read_only(target)
        host_ref = target.relative_to(run_root).as_posix()
    interval = _record_freeze_interval(
        run_root,
        actor=actor,
        session_id=session_id,
        task="write_draft",
        start_utc=start_utc,
        end_utc=end_utc,
        duration_seconds=duration_seconds,
        timestamp_source=timestamp_source,
        status="COMPLETED",
        reason=declared_reason,
        evidence_ref=host_ref,
    )
    state["writer_identity"][actor] = {
        "requested_model": WRITERS[actor]["requested_model"],
        "actual_model": actual_model,
        "actual_config": actual_config,
        "identity_match": actual_model.casefold() == WRITERS[actor]["requested_model"].casefold(),
    }
    state["writer_status"][actor] = "PENDING_BUDGET_REVIEW"
    append_jsonl(_run_paths(run_root)["handoffs"], {
        "schema_version": SCHEMA_VERSION,
        "role": actor,
        "session_id": session_id,
        "input_sha256": state["writer_packet_sha256"][actor],
        "common_content_sha256": state["writer_common_content_sha256"],
        "output_ref": output_path.relative_to(run_root).as_posix(),
        "output_sha256": sha256_file(output_path),
        "declared_reason": declared_reason,
        "uncertainty": uncertainty,
        "requested_model": WRITERS[actor]["requested_model"],
        "actual_model": actual_model,
        "actual_config": actual_config,
        "timing_interval_id": interval["interval_id"],
        "validation": "PENDING_BUDGET_CHECK",
    })
    state["resume_state"] = "AWAITING_WRITERS"
    if _budget_block_after_interval(run_root, state, actor, scope="write_draft", evidence=output_path.relative_to(run_root).as_posix()):
        return _load_state(run_root)
    _publish_writer_output(run_root, state, actor)
    if all(state["draft_sha256"].values()):
        _set_owner_gate(run_root, state)
    else:
        state.update({
            "state": "AWAITING_WRITERS",
            "waiting_for": "Writer Gemini + Writer Sol",
            "artifact_to_open": [str(_run_paths(run_root)["writer_gemini_packet"]), str(_run_paths(run_root)["writer_sol_packet"])],
            "next_action": "One Writer result is frozen; wait for the other Writer. Do not pass the first draft or Owner feedback into the unfinished Writer.",
        })
    _save_state(run_root, state)
    return state


def record_writer_failure(
    run_root: Path,
    *,
    session_id: str,
    status: str,
    reason: str,
    start_utc: str | None = None,
    end_utc: str | None = None,
    duration_seconds: float | None = None,
    timestamp_source: str = "UNKNOWN",
    evidence_ref: str | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "AWAITING_WRITERS":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot record Writer failure from state {state['state']}")
    actor = _actor_from_session(state, session_id)
    _require_budget_to_start(run_root, actor)
    status = status.upper()
    if status not in {"FAILED", "TIMEOUT"}:
        raise LearningError("WRITER_FAILURE_STATUS_INVALID", "status must be FAILED or TIMEOUT")
    _record_freeze_interval(
        run_root,
        actor=actor,
        session_id=session_id,
        task="write_draft",
        start_utc=start_utc,
        end_utc=end_utc,
        duration_seconds=duration_seconds,
        timestamp_source=timestamp_source,
        status=status,
        reason=reason,
        evidence_ref=evidence_ref,
    )
    state["writer_status"][actor] = status
    state["next_action"] = f"{actor} {status.lower()}; keep any other valid sample, report pair incomplete, and do not substitute an old or third Writer output."
    state["waiting_for"] = "Owner" if any(state["draft_sha256"].values()) else "Writer Gemini + Writer Sol"
    if _budget_block_after_interval(run_root, state, actor, scope="write_draft", evidence=evidence_ref or reason):
        return _load_state(run_root)
    _save_state(run_root, state)
    return state


def record_owner_feedback(
    run_root: Path,
    *,
    feedback_text: str,
    selection: str = "UNSELECTED",
    primary_writer: str | None = None,
) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    if state["state"] != "AWAITING_OWNER_FEEDBACK":
        raise LearningError("STATE_TRANSITION_DENIED", f"cannot record Owner feedback from state {state['state']}")
    if not feedback_text.strip():
        raise LearningError("OWNER_FEEDBACK_REQUIRED", "Owner feedback must be non-empty")
    selection = selection.upper()
    if selection not in {"A", "B", "TIE", "UNSELECTED"}:
        raise LearningError("OWNER_SELECTION_INVALID", "selection must be A, B, TIE, or UNSELECTED")
    if primary_writer is not None and primary_writer not in WRITERS:
        raise LearningError("PRIMARY_WRITER_INVALID", "primary_writer must be writer_gemini or writer_sol")
    if _run_paths(run_root)["feedback"].exists():
        raise LearningError("OWNER_FEEDBACK_ALREADY_RECORDED", "Owner feedback is immutable in this run")
    for actor in WRITERS:
        _, output_path, owner_path = _writer_paths(run_root, actor)
        expected = state["draft_sha256"][actor]
        if not expected:
            raise LearningError("WRITER_PAIR_INCOMPLETE", "Owner feedback comparison requires both frozen samples")
        _verify_frozen(output_path, expected, f"{actor} output")
        _verify_frozen(owner_path, expected, f"Owner sample {WRITERS[actor]['sample']}")
    feedback = {
        "schema_version": SCHEMA_VERSION,
        "authority": "OWNER",
        "samples": {
            "A": {"writer": "writer_gemini", "ref": _run_paths(run_root)["owner_sample_a"].relative_to(run_root).as_posix(), "sha256": state["draft_sha256"]["writer_gemini"]},
            "B": {"writer": "writer_sol", "ref": _run_paths(run_root)["owner_sample_b"].relative_to(run_root).as_posix(), "sha256": state["draft_sha256"]["writer_sol"]},
        },
        "verbatim_feedback": feedback_text,
        "selection": selection,
        "primary_writer_decision": primary_writer,
        "model_generalization": "NOT_PERFORMED",
        "recorded_at": utc_now(),
        "interpretation": "NOT_PERFORMED",
    }
    atomic_write_json(_run_paths(run_root)["feedback"], feedback)
    make_read_only(_run_paths(run_root)["feedback"])
    state.update({
        "state": "OWNER_FEEDBACK_RECORDED",
        "waiting_for": "Owner",
        "next_action": "STOP. Owner chooses any later architecture/content change and budget in a new work item; this run does not auto-rerun or set a default Writer.",
        "artifact_to_open": str(_run_paths(run_root)["feedback"]),
        "owner_feedback_sha256": sha256_file(_run_paths(run_root)["feedback"]),
    })
    _save_state(run_root, state)
    return state


def record_cost_item(
    run_root: Path,
    *,
    work_item_id: str,
    phase: str,
    kind: str,
    actor: str,
    task: str,
    code_scope: str,
    estimate_seconds: float | None = None,
    observed_seconds: float | None = None,
    expected_runtime_impact: str | None = None,
    confidence: str | None = None,
    commit_ref: str | None = None,
    evidence: str | None = None,
) -> dict[str, Any]:
    phase = phase.upper()
    kind = kind.upper()
    if phase not in {"ESTIMATE", "OBSERVED"}:
        raise LearningError("COST_PHASE_INVALID", "phase must be ESTIMATE or OBSERVED")
    if kind not in {"ROUND_EXECUTION", "ARCHITECTURE_REPAIR"}:
        raise LearningError("COST_KIND_INVALID", "kind must separate round execution from architecture repair")
    if actor not in ACTORS:
        raise LearningError("COST_ACTOR_INVALID", f"actor must be one of {ACTORS}")
    if phase == "ESTIMATE" and (estimate_seconds is None or expected_runtime_impact is None or confidence is None):
        raise LearningError("COST_ESTIMATE_FIELDS_REQUIRED", "estimate requires seconds, expected runtime impact and confidence")
    if phase == "OBSERVED" and (observed_seconds is None or commit_ref is None or evidence is None):
        raise LearningError("COST_OBSERVED_FIELDS_REQUIRED", "observed record requires seconds, commit_ref and evidence")
    event = {
        "schema_version": SCHEMA_VERSION,
        "work_item_id": work_item_id,
        "phase": phase,
        "kind": kind,
        "actor": actor,
        "task": task,
        "code_scope": code_scope,
        "estimate_seconds": estimate_seconds,
        "observed_seconds": observed_seconds,
        "expected_runtime_impact": expected_runtime_impact,
        "confidence": confidence,
        "commit_ref": commit_ref,
        "evidence": evidence,
        "recorded_at": utc_now(),
    }
    append_jsonl(_run_paths(run_root)["cost_items"], event)
    return event


def status(run_root: Path, *, as_of: str | None = None) -> dict[str, Any]:
    run_root = run_root.resolve()
    state = _load_state(run_root)
    _verify_authority_snapshot(run_root, state)
    if state.get("sol_brief_sha256"):
        _verify_frozen(_run_paths(run_root)["sol_brief"], state["sol_brief_sha256"], "Sol repo brief")
    if state.get("plan_sha256"):
        _verify_frozen(_run_paths(run_root)["plan_output"], state["plan_sha256"], "Plan output")
    for actor in WRITERS:
        packet_sha = state.get("writer_packet_sha256", {}).get(actor)
        if packet_sha:
            _verify_frozen(_writer_paths(run_root, actor)[0], packet_sha, f"{actor} packet")
        draft_sha = state.get("draft_sha256", {}).get(actor)
        if draft_sha:
            _verify_frozen(_writer_paths(run_root, actor)[1], draft_sha, f"{actor} draft")
            _verify_frozen(_writer_paths(run_root, actor)[2], draft_sha, f"Owner sample {WRITERS[actor]['sample']}")
    if state.get("owner_feedback_sha256"):
        _verify_frozen(_run_paths(run_root)["feedback"], state["owner_feedback_sha256"], "Owner feedback")

    budget = budget_summary(run_root, as_of=as_of)
    table = []
    actor_tasks = {"sol_repo": "prepare_plan", "writer_gemini": "write_draft", "writer_sol": "write_draft"}
    if budget.get("approved"):
        for actor in ACTORS:
            row = budget["actors"][actor]
            table.append({
                "actor_task": f"{actor}/{actor_tasks[actor]}",
                "allocated_seconds": row["allocated_seconds"],
                "used_seconds": row["used_seconds"],
                "overrun_seconds": row["overrun_seconds"],
                "unknown_intervals": row["unknown_intervals"],
                "waiting_for": state["waiting_for"],
            })
    return {
        "run_id": state["run_id"],
        "state": state["state"],
        "waiting_for": state["waiting_for"],
        "artifact_to_open": state["artifact_to_open"],
        "next_action": state["next_action"],
        "test_only": state["test_only"],
        "writer_status": state["writer_status"],
        "writer_identity": state["writer_identity"],
        "writer_common_content_sha256": state.get("writer_common_content_sha256"),
        "budget": budget,
        "budget_table": table,
        "cost_items": read_jsonl(_run_paths(run_root)["cost_items"]),
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
    parser = argparse.ArgumentParser(description="Owner-first MVP: one Sol repo Plan, two Writer samples, Owner-approved time budget")
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("prepare", help="snapshot P01 authority and prepare the Sol repo brief; no agent dispatch yet")
    p.add_argument("--run", required=True)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--request")
    group.add_argument("--request-file", type=Path)
    p.add_argument("--overlay", type=Path, default=DEFAULT_OVERLAY)
    p.add_argument("--substrate", type=Path, default=DEFAULT_SUBSTRATE)
    p.add_argument("--test-only", action="store_true")
    p.add_argument("--code-ref")

    b = sub.add_parser("budget-propose", help="write the initial budget proposal; Owner approval is still required")
    b.add_argument("--run", required=True)
    b.add_argument("--budget-id", required=True)
    b.add_argument("--cap-seconds", type=float, required=True)
    b.add_argument("--sol-seconds", type=float, required=True)
    b.add_argument("--gemini-seconds", type=float, required=True)
    b.add_argument("--writer-sol-seconds", type=float, required=True)
    b.add_argument("--scope", required=True)
    b.add_argument("--code-ref", required=True)

    d = sub.add_parser("budget-decision", help="record verbatim Owner approval/rejection for initial or extension request")
    d.add_argument("--run", required=True)
    d.add_argument("--request-id", required=True)
    d.add_argument("--decision", choices=["APPROVED", "REJECTED"], required=True)
    d.add_argument("--owner-text", required=True)
    d.add_argument("--source-ref", required=True)
    d.add_argument("--actor")
    d.add_argument("--scope")
    d.add_argument("--approved-seconds", type=float)

    e = sub.add_parser("request-extension", help="pause and request Owner-approved extra seconds")
    e.add_argument("--run", required=True)
    e.add_argument("--actor", choices=ACTORS, required=True)
    e.add_argument("--seconds", type=float, required=True)
    e.add_argument("--scope", required=True)
    e.add_argument("--reason", required=True)
    e.add_argument("--evidence", required=True)
    e.add_argument("--request-id")

    q = sub.add_parser("freeze-plan", help="accept the Sol repo Plan and prepare two equal-content Writer packets")
    q.add_argument("--run", required=True)
    q.add_argument("--session", required=True)
    q.add_argument("--file", type=Path, required=True)
    q.add_argument("--reason", required=True)
    q.add_argument("--uncertainty", required=True)
    q.add_argument("--start-utc")
    q.add_argument("--end-utc")
    q.add_argument("--duration-seconds", type=float)
    q.add_argument("--timestamp-source", default="UNKNOWN")
    q.add_argument("--host-log", type=Path)

    r = sub.add_parser("freeze-draft", help="accept one Writer result; pair completes only after both are valid")
    r.add_argument("--run", required=True)
    r.add_argument("--session", required=True)
    r.add_argument("--file", type=Path, required=True)
    r.add_argument("--reason", required=True)
    r.add_argument("--uncertainty", required=True)
    r.add_argument("--actual-model", required=True)
    r.add_argument("--actual-config")
    r.add_argument("--start-utc")
    r.add_argument("--end-utc")
    r.add_argument("--duration-seconds", type=float)
    r.add_argument("--timestamp-source", default="UNKNOWN")
    r.add_argument("--host-log", type=Path)

    f = sub.add_parser("feedback", help="record verbatim Owner comparison feedback and stop")
    f.add_argument("--run", required=True)
    fg = f.add_mutually_exclusive_group(required=True)
    fg.add_argument("--text")
    fg.add_argument("--file", type=Path)
    f.add_argument("--selection", choices=["A", "B", "TIE", "UNSELECTED"], default="UNSELECTED")
    f.add_argument("--primary-writer", choices=list(WRITERS))

    s = sub.add_parser("status", help="show Owner gate, timing, budget, overrun/UNKNOWN and cost evidence")
    s.add_argument("--run", required=True)

    args = parser.parse_args()
    try:
        run_root = _resolve_run(args.run, args.runs_root).resolve()
        if args.command == "prepare":
            owner_request = args.request if args.request is not None else args.request_file.read_text(encoding="utf-8")
            result = prepare_run(run_root, owner_request=owner_request, overlay_path=args.overlay, substrate_path=args.substrate, test_only=args.test_only, code_ref=args.code_ref)
        elif args.command == "budget-propose":
            result = propose_budget(run_root, budget_id=args.budget_id, initial_cap_seconds=args.cap_seconds, allocations={"sol_repo": args.sol_seconds, "writer_gemini": args.gemini_seconds, "writer_sol": args.writer_sol_seconds}, scope=args.scope, code_ref=args.code_ref)
        elif args.command == "budget-decision":
            result = record_budget_decision(run_root, request_id=args.request_id, decision=args.decision, owner_text=args.owner_text, source_ref=args.source_ref, actor=args.actor, scope=args.scope, approved_seconds=args.approved_seconds)
        elif args.command == "request-extension":
            result = request_budget_extension(run_root, actor=args.actor, requested_seconds=args.seconds, scope=args.scope, reason=args.reason, evidence=args.evidence, request_id=args.request_id)
        elif args.command == "freeze-plan":
            result = freeze_plan(run_root, session_id=args.session, source_file=args.file, declared_reason=args.reason, uncertainty=args.uncertainty, start_utc=args.start_utc, end_utc=args.end_utc, duration_seconds=args.duration_seconds, timestamp_source=args.timestamp_source, host_log=args.host_log)
        elif args.command == "freeze-draft":
            result = freeze_draft(run_root, session_id=args.session, source_file=args.file, declared_reason=args.reason, uncertainty=args.uncertainty, actual_model=args.actual_model, actual_config=args.actual_config, start_utc=args.start_utc, end_utc=args.end_utc, duration_seconds=args.duration_seconds, timestamp_source=args.timestamp_source, host_log=args.host_log)
        elif args.command == "feedback":
            result = record_owner_feedback(run_root, feedback_text=_feedback_from_args(args), selection=args.selection, primary_writer=args.primary_writer)
        else:
            result = status(run_root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except LearningError as exc:
        print(json.dumps({"status": "ERROR", "code": exc.code, "message": str(exc), "path": str(exc.path) if exc.path else None, "repair": exc.repair}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
