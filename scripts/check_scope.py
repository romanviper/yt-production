#!/usr/bin/env python3
"""Check git worktree changes against the active task's declared scope."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

try:
    from scripts.common import REPO_ROOT, read_json
    from scripts.governance import product_task_violations
except ModuleNotFoundError:
    from common import REPO_ROOT, read_json
    from governance import product_task_violations


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, check=True, text=True, capture_output=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--base")
    args = parser.parse_args()
    product = args.product.resolve()
    active = read_json(product / "tasks" / "ACTIVE.json")
    work = read_json(product / active["work_order"])
    if args.base:
        changed = git_lines("diff", "--name-only", f"{args.base}...HEAD")
    else:
        changed = sorted(
            set(git_lines("diff", "--name-only"))
            | set(git_lines("diff", "--cached", "--name-only"))
            | set(git_lines("ls-files", "--others", "--exclude-standard"))
        )
    violations = product_task_violations(product, work, changed)
    if violations:
        print("Write-scope violations:")
        for path in violations:
            print(f"- {path}")
        return 1
    print(f"Scope OK: {len(changed)} changed file(s), no protected system writes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
