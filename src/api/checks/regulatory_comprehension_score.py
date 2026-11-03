"""Score a staff comprehension round for regulatory alerts against the predeclared thresholds.

Input is a JSON list of anonymous records:
{"participant": "P01", "group": "repairs", "task": 1, "correct": true, "critical_error": false}
The script only applies the arithmetic. Reviewers still score against the frozen answer key and
a human owner decides on any staff-use change. A pass here is not acceptance.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

GROUPS = ("repairs", "housing", "grants")
TASKS = (1, 2, 3, 4, 5)
MIN_PARTICIPANTS = 3
OVERALL_MIN = 0.90
GROUP_MIN = 0.80


def _rate(correct: int, total: int) -> float | None:
    return correct / total if total else None


def score(records: list[dict[str, Any]]) -> dict[str, Any]:
    problems: list[str] = []
    seen: set[tuple[str, int]] = set()
    people: dict[str, set[str]] = {group: set() for group in GROUPS}
    totals = {group: [0, 0] for group in GROUPS}
    critical: list[dict[str, Any]] = []
    for record in records:
        group, person, task = record.get("group"), record.get("participant"), record.get("task")
        if group not in totals or not isinstance(person, str) or not person:
            problems.append(f"Unusable group or participant: {record!r}")
            continue
        if task not in TASKS or not isinstance(record.get("correct"), bool):
            problems.append(f"Unusable task or correct flag for {person}: {record!r}")
            continue
        if (person, task) in seen:
            problems.append(f"Duplicate record for {person} task {task}")
            continue
        seen.add((person, task))
        people[group].add(person)
        totals[group][1] += 1
        totals[group][0] += int(record["correct"])
        if record.get("critical_error") is True:
            critical.append({"participant": person, "task": task})
    for person in {p for members in people.values() for p in members}:
        missing = [task for task in TASKS if (person, task) not in seen]
        if missing:
            problems.append(f"{person} has no record for tasks {missing}")
    counts = {group: len(members) for group, members in people.items()}
    short = [group for group, count in counts.items() if count < MIN_PARTICIPANTS]
    if short:
        problems.append(f"Fewer than {MIN_PARTICIPANTS} participants in: {', '.join(short)}")
    overall = _rate(sum(t[0] for t in totals.values()), sum(t[1] for t in totals.values()))
    by_group = {group: _rate(*totals[group]) for group in GROUPS}
    met = (
        not problems
        and not critical
        and overall is not None
        and overall >= OVERALL_MIN
        and all(rate is not None and rate >= GROUP_MIN for rate in by_group.values())
    )
    return {
        "participants": counts,
        "answers": {group: {"correct": t[0], "total": t[1]} for group, t in totals.items()},
        "overall_rate": overall,
        "group_rates": by_group,
        "critical_errors": critical,
        "problems": problems,
        "thresholds_met": met,
        "note": "Thresholds met is not acceptance; the human owner decides on staff use.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="JSON file of anonymous scored records")
    args = parser.parse_args(argv)
    data = json.loads(args.records.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("Records must be a JSON list", file=sys.stderr)
        return 2
    result = score(data)
    print(json.dumps(result, indent=2))
    return 0 if result["thresholds_met"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
