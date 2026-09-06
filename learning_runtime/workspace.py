from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Any

from .artifacts import artifact_identity, write_json
from .run import REPO_ROOT


POLICY_VERSION = "PHASE3-WORKSPACE-PROTOTYPE-1"
SUPPORTED_ROLES = {"plan", "writer", "truth", "review", "audit", "system_architect"}


class WorkspaceError(PermissionError):
    def __init__(self, code: str, *, action: str, attempted: str, resolved: str | None = None):
        self.code = code
        self.action = action
        self.attempted = attempted
        self.resolved = resolved
        super().__init__(f"{code}: action={action} attempted={attempted} resolved={resolved}")


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def _is_within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _safe_rel(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise WorkspaceError("PATH_ESCAPE_DENIED", action="RESOLVE", attempted=value)
    return path


def role_safe_brief(full_brief: dict[str, Any], role: str) -> dict[str, Any]:
    if role not in SUPPORTED_ROLES:
        raise ValueError(f"unsupported role: {role}")
    visible = full_brief.get("role_visibility", {}).get(role)
    if not isinstance(visible, list):
        raise ValueError(f"brief has no visibility policy for role {role}")
    safe = {
        "schema_version": full_brief.get("schema_version"),
        "brief_id": full_brief.get("brief_id"),
        "role": role,
        "visibility": visible,
    }
    for key in visible:
        if key in full_brief:
            safe[key] = full_brief[key]
    if role == "review" and "diagnostic_hypothesis" in safe:
        raise ValueError("review brief leaked diagnostic_hypothesis")
    return safe


def create_workspace_run(root: Path, run_id: str, role_executions: dict[str, str], full_brief: dict[str, Any]) -> Path:
    run_root = root / run_id
    if run_root.exists() and any(run_root.iterdir()):
        raise FileExistsError(f"workspace run already exists and is non-empty: {run_root}")
    control = run_root / "control"
    control.mkdir(parents=True, exist_ok=True)
    (control / "measurements").mkdir(parents=True, exist_ok=True)
    (control / "access-events.jsonl").write_text("", encoding="utf-8")
    (control / "handoffs.jsonl").write_text("", encoding="utf-8")

    roles: dict[str, Any] = {}
    for role, execution_id in role_executions.items():
        if role not in SUPPORTED_ROLES:
            raise ValueError(f"unsupported role: {role}")
        execution_root = run_root / "agents" / role / execution_id
        for name in ("input", "output", "scratch"):
            (execution_root / name).mkdir(parents=True, exist_ok=True)
        safe_brief = role_safe_brief(full_brief, role)
        brief_path = execution_root / "input" / "common-brief.json"
        write_json(brief_path, safe_brief)
        try:
            brief_path.chmod(0o444)
        except OSError:
            pass
        roles[role] = {
            "execution_id": execution_id,
            "read": ["input/**", "output/**", "scratch/**"],
            "write": ["output/**", "scratch/**"],
            "deny": ["control/**", "agents/<other-role>/**", "../**", "absolute paths", "resolved symlink escapes"],
        }

    policy = {
        "schema_version": "1.0.0",
        "policy_version": POLICY_VERSION,
        "run_id": run_id,
        "enforcement_level": "FILE_BROKER_ONLY_NO_SHELL_OR_NETWORK_SURFACE",
        "read_isolation": "ENFORCED_ONLY_WHEN_AGENT_RECEIVES_THIS_BROKER_AS_ITS_SOLE_FILESYSTEM_SURFACE",
        "host_process_isolation": "NOT_PROVEN",
        "roles": roles,
    }
    write_json(control / "role-policy.json", policy)
    write_json(control / "frozen-standard.json", full_brief)
    return run_root


class RoleWorkspaceBroker:
    def __init__(self, run_root: Path, role: str, execution_id: str):
        self.run_root = run_root.resolve()
        self.role = role
        self.execution_id = execution_id
        self.execution_root = (self.run_root / "agents" / role / execution_id).resolve()
        if not self.execution_root.exists():
            raise FileNotFoundError(self.execution_root)
        self.event_log = self.run_root / "control" / "access-events.jsonl"

    def _log(self, action: str, attempted: str, resolved: Path | None, result: str, code: str | None = None) -> None:
        _append_jsonl(self.event_log, {
            "policy_version": POLICY_VERSION,
            "run_id": self.run_root.name,
            "role": self.role,
            "execution_id": self.execution_id,
            "action": action,
            "attempted_path": attempted,
            "resolved_path": str(resolved) if resolved else None,
            "result": result,
            "code": code,
        })

    def _resolve(self, relative: str, *, write: bool) -> Path:
        action = "WRITE" if write else "READ"
        try:
            rel = _safe_rel(relative)
        except WorkspaceError as exc:
            self._log(action, relative, None, "DENIED", exc.code)
            raise
        candidate = self.execution_root / rel
        if write:
            parent = candidate.parent.resolve(strict=False)
            resolved = parent / candidate.name
            allowed_roots = [(self.execution_root / "output").resolve(), (self.execution_root / "scratch").resolve()]
        else:
            resolved = candidate.resolve(strict=False)
            allowed_roots = [
                (self.execution_root / "input").resolve(),
                (self.execution_root / "output").resolve(),
                (self.execution_root / "scratch").resolve(),
            ]
        if not any(_is_within(resolved, root) for root in allowed_roots):
            self._log(action, relative, resolved, "DENIED", "ROLE_PATH_DENIED")
            raise WorkspaceError("ROLE_PATH_DENIED", action=action, attempted=relative, resolved=str(resolved))
        self._log(action, relative, resolved, "ALLOWED")
        return resolved

    def read_text(self, relative: str) -> str:
        path = self._resolve(relative, write=False)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(path)
        return path.read_text(encoding="utf-8")

    def write_text(self, relative: str, value: str) -> Path:
        path = self._resolve(relative, write=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path


def handoff_copy(run_root: Path, *, source_role: str, source_execution: str, source_rel: str, dest_role: str, dest_execution: str, dest_name: str) -> dict[str, Any]:
    run_root = run_root.resolve()
    source_root = (run_root / "agents" / source_role / source_execution / "output").resolve()
    destination_root = (run_root / "agents" / dest_role / dest_execution / "input").resolve()
    source_rel_path = _safe_rel(source_rel)
    dest_rel_path = _safe_rel(dest_name)
    source = (source_root / source_rel_path).resolve(strict=True)
    destination = (destination_root / dest_rel_path).resolve(strict=False)
    if not _is_within(source, source_root):
        raise WorkspaceError("HANDOFF_SOURCE_DENIED", action="HANDOFF", attempted=source_rel, resolved=str(source))
    if not _is_within(destination, destination_root):
        raise WorkspaceError("HANDOFF_DESTINATION_DENIED", action="HANDOFF", attempted=dest_name, resolved=str(destination))
    if destination.exists():
        raise FileExistsError(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    try:
        destination.chmod(0o444)
    except OSError:
        pass
    source_identity = artifact_identity(source)
    destination_identity = artifact_identity(destination)
    if source_identity["raw_sha256"] != destination_identity["raw_sha256"]:
        raise RuntimeError("handoff hash mismatch")
    record = {
        "policy_version": POLICY_VERSION,
        "run_id": run_root.name,
        "source": {"role": source_role, "execution_id": source_execution, "path": source_rel, "identity": source_identity},
        "destination": {"role": dest_role, "execution_id": dest_execution, "path": dest_name, "identity": destination_identity},
        "result": "COPIED_READ_ONLY_HASH_MATCH",
    }
    _append_jsonl(run_root / "control" / "handoffs.jsonl", record)
    return record


def workspace_manifest(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    policy = json.loads((run_root / "control" / "role-policy.json").read_text(encoding="utf-8"))
    handoffs = (run_root / "control" / "handoffs.jsonl").read_text(encoding="utf-8").splitlines()
    access = (run_root / "control" / "access-events.jsonl").read_text(encoding="utf-8").splitlines()
    return {
        "run_id": run_root.name,
        "policy": policy,
        "handoff_count": len([line for line in handoffs if line.strip()]),
        "access_event_count": len([line for line in access if line.strip()]),
        "limitations": [
            "This prototype enforces paths only when the agent receives RoleWorkspaceBroker as its sole filesystem surface.",
            "It does not prove host-level process isolation or protect against an independently granted shell/network/filesystem tool.",
        ],
    }


def smoke_workspace(out: Path) -> dict[str, Any]:
    brief = json.loads((REPO_ROOT / "learning_runtime/briefs/p01-rootcause-01.json").read_text(encoding="utf-8"))
    run_root = create_workspace_run(
        out,
        "WORKSPACE-SMOKE-01",
        {"writer": "W1", "truth": "T1", "review": "R1"},
        brief,
    )
    writer = RoleWorkspaceBroker(run_root, "writer", "W1")
    writer.read_text("input/common-brief.json")
    source = writer.write_text("output/candidate.md", "workspace smoke candidate\n")

    denied: list[dict[str, str]] = []
    for attempted, action in [
        ("../../review/R1/input/common-brief.json", "READ"),
        ("input/common-brief.json", "WRITE"),
    ]:
        try:
            if action == "READ":
                writer.read_text(attempted)
            else:
                writer.write_text(attempted, "tamper")
        except WorkspaceError as exc:
            denied.append({"attempted": attempted, "action": action, "code": exc.code})
        else:
            raise RuntimeError(f"workspace smoke expected DENY for {action} {attempted}")

    handoff = handoff_copy(
        run_root,
        source_role="writer",
        source_execution="W1",
        source_rel="candidate.md",
        dest_role="truth",
        dest_execution="T1",
        dest_name="candidate.md",
    )
    truth = RoleWorkspaceBroker(run_root, "truth", "T1")
    if truth.read_text("input/candidate.md") != "workspace smoke candidate\n":
        raise RuntimeError("handoff destination content mismatch")
    try:
        truth.write_text("input/candidate.md", "tamper")
    except WorkspaceError as exc:
        denied.append({"attempted": "input/candidate.md", "action": "WRITE", "code": exc.code})
    else:
        raise RuntimeError("workspace smoke expected destination input write DENY")

    review_packet = json.loads((run_root / "agents/review/R1/input/common-brief.json").read_text(encoding="utf-8"))
    if "diagnostic_hypothesis" in review_packet:
        raise RuntimeError("review packet leaked diagnostic hypothesis")

    result = {
        "status": "WORKSPACE_SMOKE_PASS",
        "run_root": str(run_root),
        "denied": denied,
        "handoff": handoff,
        "review_diagnostic_hidden": True,
        "manifest": workspace_manifest(run_root),
    }
    write_json(run_root / "control/smoke-result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 3 bounded role workspace prototype")
    sub = parser.add_subparsers(dest="command", required=True)
    smoke = sub.add_parser("smoke")
    smoke.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "smoke":
        print(json.dumps(smoke_workspace(args.out), ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
