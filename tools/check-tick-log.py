"""Validate an exported coordinator `tick_log` against the Issue #1204 tick contract.

Input is a JSON array or JSON lines of tick rows (synthetic or exported from the
coordinator session SQL). Row fields:

* `tick`: integer sequence number (rows are checked in this order)
* `counts`: object with `ready`, `running`, `unassessed`, `human_blocked`,
  `dependency_blocked`
* `action`, `evidence`: strings; a tick missing either is no-progress
* `recovery`: true when the tick executed the bounded recovery action
* `closure_batch`: list of closure-review item ids assessed in the tick
* `approvals_granted`, `approvals_expired`: lists of `{"scope", "tasks"}` objects
* `reclassified`: list of `{"task", "to", "scope"}` objects
* `global_stop`: true when the tick declared the whole backlog stopped

Offline, standard library only. Exit status 1 when any violation is found.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SESSION_CAP = 8
CLOSURE_BATCH_MAX = 5


@dataclass(frozen=True)
class Violation:
    tick: object
    rule: str
    message: str

    def __str__(self) -> str:
        return f"tick {self.tick}: {self.rule}: {self.message}"


def load_rows(text: str) -> list[dict[str, Any]]:
    stripped = text.strip()
    if not stripped:
        return []
    if stripped.startswith("["):
        data = json.loads(stripped)
    else:
        data = [json.loads(line) for line in stripped.splitlines() if line.strip()]
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError("tick_log must be a list of objects")
    return data


def _count(row: dict[str, Any], key: str) -> int:
    counts = row.get("counts")
    value = counts.get(key, 0) if isinstance(counts, dict) else 0
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: object) -> list[Any]:
    return value if isinstance(value, list) else []


def has_action(row: dict[str, Any]) -> bool:
    return _text(row.get("action")) and _text(row.get("evidence"))


def check_ticks(rows: list[dict[str, Any]]) -> list[Violation]:
    violations: list[Violation] = []
    ordered = sorted(rows, key=lambda r: r.get("tick") if isinstance(r.get("tick"), int) else -1)
    seen_items: set[str] = set()
    streak = 0
    for row in ordered:
        tick = row.get("tick")
        if not isinstance(tick, int) or isinstance(tick, bool):
            violations.append(Violation(tick, "schema", "tick must be an integer"))
        if not isinstance(row.get("counts"), dict):
            violations.append(Violation(tick, "schema", "counts object is required"))
        pending = _count(row, "ready") + _count(row, "unassessed")
        acted = has_action(row)

        if not acted and pending and _count(row, "running") < SESSION_CAP:
            violations.append(
                Violation(
                    tick, "no-progress", "no action and evidence while work is ready or unassessed"
                )
            )
        if streak >= 2 and pending and not (acted and row.get("recovery") is True):
            violations.append(
                Violation(
                    tick, "recovery", "two no-progress ticks need a recovery action this tick"
                )
            )
        streak = 0 if acted else streak + 1

        batch = [str(item) for item in _list(row.get("closure_batch"))]
        if len(batch) > CLOSURE_BATCH_MAX:
            violations.append(
                Violation(tick, "closure-batch", f"{len(batch)} items exceeds {CLOSURE_BATCH_MAX}")
            )
        repeats = sorted(set(batch) & seen_items)
        if repeats or len(set(batch)) != len(batch):
            violations.append(
                Violation(
                    tick, "closure-repeat", f"item reassessed without new evidence: {repeats}"
                )
            )
        seen_items.update(batch)

        violations.extend(_check_approvals(row, tick))

        if row.get("global_stop") is True and pending:
            violations.append(
                Violation(tick, "global-stop", "backlog declared stopped while work remains")
            )
    return violations


def _check_approvals(row: dict[str, Any], tick: object) -> list[Violation]:
    found: list[Violation] = []
    moves = [m for m in _list(row.get("reclassified")) if isinstance(m, dict)]
    for key, target in (("approvals_expired", "human-blocked"), ("approvals_granted", "ready")):
        allowed: set[str] = set()
        for approval in _list(row.get(key)):
            if not isinstance(approval, dict):
                continue
            scope = approval.get("scope")
            for task in _list(approval.get("tasks")):
                allowed.add(str(task))
                moved = [
                    m for m in moves if str(m.get("task")) == str(task) and m.get("to") == target
                ]
                if not any(m.get("scope") == scope for m in moved):
                    found.append(
                        Violation(
                            tick,
                            "approval",
                            f"task {task} not reclassified to {target} for scope {scope!r}",
                        )
                    )
        if key == "approvals_expired":
            expired_allowed = allowed
        else:
            granted_allowed = allowed
    for move in moves:
        task = str(move.get("task"))
        if move.get("to") == "human-blocked" and task not in expired_allowed:
            found.append(Violation(tick, "approval", f"task {task} blocked without an expiry"))
        if move.get("to") == "ready" and task not in granted_allowed and not move.get("scope"):
            found.append(Violation(tick, "approval", f"task {task} made ready without a scope"))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", type=Path, help="tick_log export (JSON array or JSON lines)")
    args = parser.parse_args(argv)
    try:
        rows = load_rows(args.path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    violations = check_ticks(rows)
    for violation in violations:
        print(violation)
    print(f"{len(rows)} ticks, {len(violations)} violations")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
