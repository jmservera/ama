#!/usr/bin/env python3
"""Run one deterministic shard of a project's unittest suite.

Usage: ci-test-shard.py SHARD SHARDS [unittest args...], run from a project directory
(for example src/api). Every test module under ./tests is assigned to exactly one shard by
a greedy weighted split, so the union of the shards is the full suite and no module is
skipped. Unknown modules weigh DEFAULT_WEIGHT seconds; WEIGHTS records measured slow ones.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_WEIGHT = 3
# Approximate seconds per module measured in the hosted src-api run of 2026-11-23.
WEIGHTS = {
    "test_chat_panel": 173,
    "test_quality_sensors": 93,
    "test_quality_sensors_e1": 68,
    "test_document_controls": 67,
    "test_ai_consumption_api": 58,
    "test_staff_intake_api": 58,
    "test_quality_simulation_lane": 57,
    "test_quality_sensors_c7": 50,
    "test_employee_acceptance_check": 47,
    "test_quality_sensors_e2": 36,
    "test_resident_chat_api": 35,
    "test_resident_demo_api": 33,
    "test_assistants": 29,
    "test_procurement_api": 27,
    "test_progress_dashboard": 26,
}


def modules(tests: Path) -> list[str]:
    return sorted(path.stem for path in tests.glob("test*.py"))


def split(names: list[str], shards: int) -> list[list[str]]:
    buckets: list[list[str]] = [[] for _ in range(shards)]
    loads = [0] * shards
    for name in sorted(names, key=lambda n: (-WEIGHTS.get(n, DEFAULT_WEIGHT), n)):
        target = loads.index(min(loads))
        buckets[target].append(name)
        loads[target] += WEIGHTS.get(name, DEFAULT_WEIGHT)
    return buckets


def main(argv: list[str]) -> int:
    shard, shards = int(argv[1]), int(argv[2])
    if not 1 <= shard <= shards:
        print(f"shard {shard} outside 1..{shards}", file=sys.stderr)
        return 2
    tests = Path("tests")
    names = modules(tests)
    if not names:
        print("no test modules found under tests", file=sys.stderr)
        return 2
    chosen = split(names, shards)[shard - 1]
    print(f"shard {shard}/{shards}: {len(chosen)} of {len(names)} modules")
    command = [sys.executable, "-m", "unittest", "-v", *argv[3:], *chosen]
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(tests.resolve()), env.get("PYTHONPATH", "")) if part
    )
    return subprocess.run(command, check=False, env=env).returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv))
