#!/usr/bin/env python3
"""Check git worktree changes against the active task's declared scope."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
from pathlib import Path

try:
    from scripts.common import REPO_ROOT, read_json
except ModuleNotFoundError:
    from common import REPO_ROOT, read_json


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, check=True, text=True, capture_output=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--base")
    args = parser.parse_args()
    product = args.product.resolve()
    active = read_json(product / "tasks" / "ACTIVE.json")
    work = read_json(product / active["work_order"])
    prefix = str(product.relative_to(REPO_ROOT))
    allowed = [f"{prefix}/{path}" for path in work["allowed_write_paths"]]
    allowed.append(f"{prefix}/tasks/{work['id']}/*")
    section = work.get("target", {}).get("section")
    if section:
        allowed.append(f"{prefix}/03_sections/{section}/section.json")
    allowed.append(f"{prefix}/tasks/ACTIVE.json")
    if args.base:
        changed = git_lines("diff", "--name-only", f"{args.base}...HEAD")
    else:
        changed = sorted(
            set(git_lines("diff", "--name-only"))
            | set(git_lines("diff", "--cached", "--name-only"))
            | set(git_lines("ls-files", "--others", "--exclude-standard"))
        )
    relevant = [path for path in changed if path.startswith(prefix + "/")]
    violations = [path for path in relevant if not matches(path, allowed)]
    if violations:
        print("Write-scope violations:")
        for path in violations:
            print(f"- {path}")
        return 1
    print(f"Scope OK: {len(relevant)} product file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

