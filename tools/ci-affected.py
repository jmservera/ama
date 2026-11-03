#!/usr/bin/env python3
"""Select which src-ci jobs a change needs, from the changed file list.

Reads EVENT_NAME, BASE_SHA and HEAD_SHA from the environment, diffs
BASE_SHA..HEAD_SHA and writes the matrix, namespace and mssql outputs to
GITHUB_OUTPUT. Any doubt (non pull request event, git failure, unknown path)
selects everything, so filtering can only remove work that is provably
unaffected.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

PROJECTS: dict[str, dict[str, object]] = {
    "core": {"dist": "zava-forward-core", "deps": "", "image": False},
    "api": {
        "dist": "zava-forward-api",
        "deps": "-e ../core -e ../agents",
        "image": True,
    },
    "agents": {"dist": "zava-forward-agents", "deps": "-e ../core", "image": True},
    "orchestrator": {
        "dist": "zava-forward-orchestrator",
        "deps": "-e ../core",
        "image": True,
    },
    "importer": {"dist": "zava-forward-import", "deps": "-e ../core", "image": True},
}

# A change to the key also needs the listed projects (they install or test against it).
DEPENDENTS: dict[str, set[str]] = {
    "core": set(PROJECTS),
    "agents": {"agents", "api"},
    "api": {"api"},
    "orchestrator": {"orchestrator"},
    "importer": {"importer"},
}

# The mssql job installs these distributions and runs the api store tests.
MSSQL_PROJECTS = {"core", "agents", "api", "orchestrator"}

# Tooling that only the namespace job exercises.
NAMESPACE_ONLY = (
    "tools/rpi-checks.py",
    "tools/test_rpi_checks.py",
    "tools/rename-zava",
)

DOC_SUFFIXES = (".md", ".mdx")


def is_dependency_manifest(path: str) -> bool:
    """Packaging and pinned requirement files affect every project, so never filter them."""
    name = path.rsplit("/", 1)[-1]
    return (
        name == "pyproject.toml"
        or name == "build-requirements.txt"
        or (name.startswith("requirements") and name.endswith(".txt"))
    )


def select(files: list[str] | None) -> dict[str, object]:
    """Return the selected projects, namespace and mssql flags; None means run all."""
    everything = {
        "projects": set(PROJECTS),
        "namespace": True,
        "mssql": True,
    }
    if files is None:
        return everything
    projects: set[str] = set()
    namespace = False
    for path in files:
        if path.startswith("src/"):
            if is_dependency_manifest(path):
                return everything
            parts = path.split("/")
            if path.endswith(DOC_SUFFIXES) and (len(parts) == 2 or parts[1] in PROJECTS):
                continue
            if len(parts) > 2 and parts[1] in PROJECTS:
                projects |= DEPENDENTS[parts[1]]
                namespace = True
                continue
            return everything
        if path.startswith(NAMESPACE_ONLY):
            namespace = True
            continue
        return everything
    return {
        "projects": projects,
        "namespace": namespace,
        "mssql": bool(projects & MSSQL_PROJECTS),
    }


def matrix(projects: set[str]) -> dict[str, list[dict[str, object]]]:
    return {
        "include": [
            {"project": name, **info, "run": name in projects} for name, info in PROJECTS.items()
        ]
    }


def changed_files(base: str, head: str) -> list[str] | None:
    if not base or not head or set(base) == {"0"}:
        return None
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{base}..{head}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    event = os.environ.get("EVENT_NAME", "")
    files = None
    if event == "pull_request":
        files = changed_files(os.environ.get("BASE_SHA", ""), os.environ.get("HEAD_SHA", ""))
    selection = select(files)
    projects = selection["projects"]
    assert isinstance(projects, set)
    outputs = {
        "matrix": json.dumps(matrix(projects), separators=(",", ":")),
        "namespace": str(selection["namespace"]).lower(),
        "mssql": str(selection["mssql"]).lower(),
    }
    target = os.environ.get("GITHUB_OUTPUT")
    lines = [f"{key}={value}" for key, value in outputs.items()]
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")
    print(f"event={event} files={'all' if files is None else len(files)}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
