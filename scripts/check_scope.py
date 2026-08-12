#!/usr/bin/env python3
"""Ensure current git changes stay inside a product work order's write scope."""

from __future__ import annotations

import argparse
import fnmatch
import json
import subprocess
from pathlib import Path


def run_git(repo_root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def matches(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/**") and (path == pattern[:-3] or path.startswith(pattern[:-2])):
            return True
        if fnmatch.fnmatchcase(path, pattern):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("product", type=Path)
    parser.add_argument("--base", help="So diff với ref này thay vì worktree hiện tại.")
    args = parser.parse_args()
    product_dir = args.product.resolve()
    try:
        repo_root = Path(
            subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                cwd=product_dir,
                check=True,
                text=True,
                capture_output=True,
            ).stdout.strip()
        )
    except subprocess.CalledProcessError:
        print("SKIP: không ở trong git worktree.")
        return 0

    work = json.loads((product_dir / "work-order.json").read_text(encoding="utf-8"))
    patterns = work.get("allowed_write_paths", [])
    if args.base:
        changed = run_git(repo_root, "diff", "--name-only", f"{args.base}...HEAD")
    else:
        changed = sorted(
            set(run_git(repo_root, "diff", "--name-only"))
            | set(run_git(repo_root, "diff", "--cached", "--name-only"))
            | set(run_git(repo_root, "ls-files", "--others", "--exclude-standard"))
        )
    violations = [path for path in changed if not matches(path, patterns)]
    if violations:
        print("Write-scope violations:")
        for path in violations:
            print(f"- {path}")
        return 1
    print(f"Scope OK: {len(changed)} changed file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

