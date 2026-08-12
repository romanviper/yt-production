#!/usr/bin/env python3
"""Enforce authority boundaries between product work and system architecture."""

from __future__ import annotations

import argparse
import fnmatch
import subprocess
from pathlib import Path
from typing import Any

try:
    from scripts.common import REPO_ROOT, read_json
except ModuleNotFoundError:  # Direct execution: python scripts/governance.py
    from common import REPO_ROOT, read_json


GOVERNANCE_PATH = REPO_ROOT / "system" / "governance.json"


def load_governance() -> dict[str, Any]:
    return read_json(GOVERNANCE_PATH)


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def classify_paths(paths: list[str], governance: dict[str, Any] | None = None) -> dict[str, list[str]]:
    policy = governance or load_governance()
    protected = sorted(path for path in paths if matches_any(path, policy["protected_system_paths"]))
    product = sorted(path for path in paths if matches_any(path, policy["product_paths"]))
    return {"system": protected, "product": product}


def product_task_violations(
    product_dir: Path,
    work: dict[str, Any],
    changed_paths: list[str],
    governance: dict[str, Any] | None = None,
) -> list[str]:
    policy = governance or load_governance()
    if work.get("authority") != "product_agent":
        return [f"Unexpected task authority: {work.get('authority')}"]
    prefix = str(product_dir.resolve().relative_to(REPO_ROOT))
    allowed = [f"{prefix}/{path}" for path in work["allowed_write_paths"]]
    allowed.append(f"{prefix}/tasks/{work['id']}/*")
    allowed.append(f"{prefix}/tasks/ACTIVE.json")
    section = work.get("target", {}).get("section")
    if section:
        allowed.append(f"{prefix}/03_sections/{section}/section.json")

    violations: list[str] = []
    for path in changed_paths:
        if matches_any(path, policy["protected_system_paths"]):
            violations.append(f"protected system path: {path}")
        elif matches_any(path, policy["product_paths"]) and not matches_any(path, allowed):
            violations.append(f"outside product task scope: {path}")
    return violations


def commit_scope_errors(paths: list[str], governance: dict[str, Any] | None = None) -> list[str]:
    classified = classify_paths(paths, governance)
    if classified["system"] and classified["product"]:
        return [
            "System architecture and product content cannot change in the same commit: "
            f"system={classified['system']}, product={classified['product']}"
        ]
    return []


def changed_paths(base: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..HEAD"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commits_in_range(base: str, head: str) -> list[str]:
    result = subprocess.run(
        ["git", "rev-list", "--reverse", "--no-merges", f"{base}..{head}"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def commit_paths(commit: str) -> list[str]:
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    commit = sub.add_parser("commit-scope")
    commit.add_argument("--base", default="HEAD^")
    commit_range = sub.add_parser("commit-range")
    commit_range.add_argument("--base", required=True)
    commit_range.add_argument("--head", default="HEAD")
    args = parser.parse_args()
    if args.command == "commit-range":
        errors = []
        commits = commits_in_range(args.base, args.head)
        for sha in commits:
            errors.extend(f"commit {sha}: {error}" for error in commit_scope_errors(commit_paths(sha)))
    else:
        errors = commit_scope_errors(changed_paths(args.base))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Governance scope OK: system and product content are not mixed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
