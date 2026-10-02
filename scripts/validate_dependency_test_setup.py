#!/usr/bin/env python3
"""Check that declared optional dependencies are represented in requirements.lock."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)")
LOCKED_PACKAGE = re.compile(
    r"^([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\[[^\]]+\])?\s*(?:==|@)", re.MULTILINE
)


def normalized_name(requirement: str) -> str:
    match = PACKAGE_NAME.match(requirement.strip())
    if match is None:
        raise ValueError(f"cannot read dependency name from {requirement!r}")
    return re.sub(r"[-_.]+", "-", match.group(1)).lower()


def validate(root: Path = ROOT) -> list[str]:
    pyproject_path = root / "pyproject.toml"
    lock_path = root / "requirements.lock"
    project = tomllib.loads(pyproject_path.read_text())
    groups = project.get("project", {}).get("optional-dependencies", {})
    if not groups:
        return []
    if not lock_path.is_file():
        return ["requirements.lock is missing for declared optional dependencies"]

    locked = {normalized_name(name) for name in LOCKED_PACKAGE.findall(lock_path.read_text())}
    problems = []
    for group, requirements in sorted(groups.items()):
        for requirement in requirements:
            name = normalized_name(requirement)
            if name not in locked:
                problems.append(f"{group}: {name} is missing from requirements.lock")
    return problems


def main() -> int:
    problems = validate()
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        return 1
    print("Optional dependencies are represented in requirements.lock")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
