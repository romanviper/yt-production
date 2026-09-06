#!/usr/bin/env python3
"""Export the frozen common Writer assignment without pre-registering a Writer/model."""

from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from scripts import learning

EXPORT_SCHEMA = "DYNAMIC_WRITER_ASSIGNMENT_EXPORT_1"

def export_assignment(run_root: Path, out_dir: Path) -> dict:
    run_root = run_root.resolve()
    state = learning._load_state(run_root)
    if state["state"] not in {"AWAITING_WRITER_SUBMISSIONS", "AWAITING_OWNER_FEEDBACK", "OWNER_FEEDBACK_RECORDED"}:
        raise learning.LearningError("ASSIGNMENT_NOT_READY", "freeze Plan before exporting Writer assignment")
    assignment = learning._run_paths(run_root)["assignment"]
    learning._verify_frozen(assignment, state["writer_assignment_sha256"], "Writer assignment")
    out_dir = out_dir.resolve()
    if out_dir.exists() and any(out_dir.iterdir()):
        raise learning.LearningError("EXPORT_DESTINATION_NOT_EMPTY", "export destination must be empty")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(assignment, out_dir / "assignment.json")
    learning.atomic_write_json(out_dir / "execution-report-template.json", learning.submission_template(run_root, submission_id="replace-with-unique-id"))
    (out_dir / "START-HERE.md").write_text(
        "# Dynamic Writer assignment\n\n"
        "Write exactly one content attempt. You do not need to be pre-registered in the repo. "
        "Use assignment.json when following the frozen round assignment, then return draft.md plus execution-report.json. "
        "Declare the actual model/provider you observed; use UNKNOWN when genuinely unavailable. "
        "Timing is telemetry only and may be UNKNOWN. Do not self-review/reroll or inspect other Writer submissions/Owner feedback.\n",
        encoding="utf-8",
    )
    manifest = {
        "schema_version": EXPORT_SCHEMA,
        "assignment_sha256": state["writer_assignment_sha256"],
        "assignment_ref": "assignment.json",
        "writer_registration_required": False,
        "writer_time_budget": "NOT_APPLICABLE",
    }
    learning.atomic_write_json(out_dir / "assignment-manifest.json", manifest)
    return manifest

def main() -> int:
    parser = argparse.ArgumentParser(description="Export a generic Writer assignment bundle")
    parser.add_argument("--runs-root", type=Path, default=learning.DEFAULT_RUNS_ROOT)
    parser.add_argument("--run", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        run_root = learning._resolve_run(args.run, args.runs_root).resolve()
        print(json.dumps(export_assignment(run_root, args.out), ensure_ascii=False, indent=2))
        return 0
    except learning.LearningError as exc:
        print(json.dumps({"status":"ERROR","code":exc.code,"message":str(exc)}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
