#!/usr/bin/env python3
"""Accept dynamic Writer self-reported submissions for Owner-first MVP v3."""

from __future__ import annotations
import argparse, json
from pathlib import Path
from scripts import learning

REPORT_SCHEMA = learning.WRITER_REPORT_SCHEMA

def main() -> int:
    parser = argparse.ArgumentParser(description="Accept one dynamic Writer submission")
    parser.add_argument("--runs-root", type=Path, default=learning.DEFAULT_RUNS_ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    t = sub.add_parser("template", help="print a Writer execution-report template")
    t.add_argument("--run", required=True)
    t.add_argument("--submission-id", default="writer-001")
    a = sub.add_parser("accept", help="freeze a Writer-authored report and optional completed draft")
    a.add_argument("--run", required=True)
    a.add_argument("--report", type=Path, required=True)
    a.add_argument("--draft", type=Path)
    args = parser.parse_args()
    run_root = learning._resolve_run(args.run, args.runs_root).resolve()
    try:
        result = learning.submission_template(run_root, submission_id=args.submission_id) if args.command == "template" else learning.accept_writer_submission(run_root, report_file=args.report, draft_file=args.draft)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except learning.LearningError as exc:
        print(json.dumps({"status":"ERROR","code":exc.code,"message":str(exc)}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
