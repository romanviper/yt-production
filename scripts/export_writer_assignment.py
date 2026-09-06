#!/usr/bin/env python3
"""Export one Writer's frozen live assignment as a portable handoff bundle.

`runs/` is intentionally runtime-local and gitignored. This helper bridges that
runtime boundary for an Owner who launches Writers manually: it copies only the
selected Writer's frozen packet and self-report contract into a standalone
directory, plus a hash-bound manifest and launch note. It never exports the
other Writer's packet or draft.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from scripts import learning
from scripts import writer_submission

EXPORT_SCHEMA = "PORTABLE_WRITER_ASSIGNMENT_1"


def export_assignment(run_root: Path, *, actor: str, out_dir: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    out_dir = out_dir.resolve()
    if actor not in learning.WRITERS:
        raise learning.LearningError("WRITER_UNKNOWN", f"unknown Writer actor: {actor}")

    state = learning._load_state(run_root)
    if state["state"] != "AWAITING_WRITERS":
        raise learning.LearningError("STATE_TRANSITION_DENIED", f"cannot export Writer assignment from {state['state']}")
    learning._require_budget_to_start(run_root, actor)
    learning._verify_authority_snapshot(run_root, state)
    learning._verify_frozen(learning._run_paths(run_root)["plan_output"], state["plan_sha256"], "Plan output")

    packet_path, _, _ = learning._writer_paths(run_root, actor)
    learning._verify_frozen(packet_path, state["writer_packet_sha256"][actor], f"{actor} packet")

    contract_path, _ = writer_submission._report_paths(run_root, actor)
    if not contract_path.is_file():
        # The operation is idempotent at the run level only when contracts do not
        # exist yet; prepare both role-local contracts, then export exactly one.
        writer_submission.prepare_report_contracts(run_root)
    contract = learning.read_json(contract_path)
    if contract.get("packet_sha256") != state["writer_packet_sha256"][actor]:
        raise learning.LearningError("WRITER_REPORT_CONTRACT_STALE", "self-report contract is not bound to the current packet")

    if out_dir.exists() and any(out_dir.iterdir()):
        raise learning.LearningError("EXPORT_DIR_NOT_EMPTY", "portable assignment destination must be new and empty", path=out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    exported_packet = out_dir / "packet.json"
    exported_contract = out_dir / "self-report-contract.json"
    shutil.copyfile(packet_path, exported_packet)
    shutil.copyfile(contract_path, exported_contract)
    learning.make_read_only(exported_packet)
    learning.make_read_only(exported_contract)

    budget = learning.budget_summary(run_root)
    manifest = {
        "schema_version": EXPORT_SCHEMA,
        "run_id": state["run_id"],
        "actor": actor,
        "session_id": learning.WRITERS[actor]["session_id"],
        "requested_model": learning.WRITERS[actor]["requested_model"],
        "code_ref": state.get("code_ref"),
        "packet_sha256": learning.sha256_file(exported_packet),
        "self_report_contract_sha256": learning.sha256_file(exported_contract),
        "common_content_sha256": state["writer_common_content_sha256"],
        "approved_budget_seconds": budget["actors"][actor]["allocated_seconds"],
        "attempt": 1,
        "other_writer_assignment_exported": False,
        "launch_rule": "Give this directory to this Writer. Do not ask the Writer to discover tasks in the repository.",
    }
    learning.atomic_write_json(out_dir / "assignment-manifest.json", manifest)
    learning.make_read_only(out_dir / "assignment-manifest.json")

    note = f"""# START HERE — {actor}\n\nThis is the complete live assignment handoff for this Writer session.\n\nRead only:\n- `packet.json`\n- `self-report-contract.json`\n- `assignment-manifest.json`\n\nDo not scan the repository for `ACTIVE.json`, old production tasks, previous drafts,\nother Writer workspaces, or Sol-repo context. Those are not authority for this run.\n\nProduce exactly one content attempt and return:\n- `draft.md` when status is COMPLETED;\n- `execution-report.json` following `self-report-contract.json`.\n\nRequested model: {learning.WRITERS[actor]['requested_model']}\nLogical session: {learning.WRITERS[actor]['session_id']}\nApproved Writer budget: {budget['actors'][actor]['allocated_seconds']} seconds\n\nIf your own declared duration exceeds the approved Writer budget, preserve the draft/report,\nexplain the actual reason in `budget_extension`, request additional seconds, and stop for Owner approval.\n"""
    (out_dir / "START-HERE.md").write_text(note, encoding="utf-8")
    learning.make_read_only(out_dir / "START-HERE.md")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Export one portable Writer assignment from a live Owner-first run")
    parser.add_argument("--runs-root", type=Path, default=learning.DEFAULT_RUNS_ROOT)
    parser.add_argument("--run", required=True)
    parser.add_argument("--actor", choices=list(learning.WRITERS), required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        run_root = learning._resolve_run(args.run, args.runs_root).resolve()
        result = export_assignment(run_root, actor=args.actor, out_dir=args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except learning.LearningError as exc:
        print(json.dumps({"status": "ERROR", "code": exc.code, "message": str(exc), "path": str(exc.path) if exc.path else None, "repair": exc.repair}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
