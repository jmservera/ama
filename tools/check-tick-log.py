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
import sqlite3
import sys
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SESSION_CAP = 8
CLOSURE_BATCH_MAX = 5
OPTIONAL_COLUMNS = (
    "closure_batch",
    "approvals_granted",
    "approvals_expired",
    "reclassified",
    "global_stop",
)


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


def check_ticks(rows: list[dict[str, Any]], require_extended: bool = False) -> list[Violation]:
    violations: list[Violation] = []
    ordered = sorted(rows, key=lambda r: r.get("tick") if isinstance(r.get("tick"), int) else -1)
    seen_items: set[str] = set()
    streak = 0
    seen_ticks: set[int] = set()
    for row in ordered:
        tick = row.get("tick")
        if not isinstance(tick, int) or isinstance(tick, bool):
            violations.append(Violation(tick, "schema", "tick must be an integer"))
        elif tick in seen_ticks:
            violations.append(Violation(tick, "duplicate-tick", "tick number appears twice"))
        else:
            seen_ticks.add(tick)
        if not isinstance(row.get("counts"), dict):
            violations.append(Violation(tick, "schema", "counts object is required"))
        if require_extended:
            missing = [c for c in OPTIONAL_COLUMNS if c not in row]
            if missing:
                violations.append(
                    Violation(tick, "schema", f"extended fields missing: {', '.join(missing)}")
                )
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
        if (
            "closure_batch" in row
            and not batch
            and _count(row, "unassessed") > 0
            and _count(row, "running") < SESSION_CAP
        ):
            violations.append(
                Violation(
                    tick,
                    "closure-progress",
                    "capacity is free and closure items are unassessed but none was reviewed",
                )
            )

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
    for task in sorted(expired_allowed & granted_allowed):
        found.append(
            Violation(tick, "approval-conflict", f"task {task} both expired and granted this tick")
        )
    for move in moves:
        if move.get("to") == "ready" and str(move.get("task")) in expired_allowed:
            found.append(
                Violation(
                    tick, "approval-conflict", f"task {move.get('task')} made ready after expiry"
                )
            )
    for move in moves:
        task = str(move.get("task"))
        if move.get("to") == "human-blocked" and task not in expired_allowed:
            found.append(Violation(tick, "approval", f"task {task} blocked without an expiry"))
        if move.get("to") == "ready" and task not in granted_allowed and not move.get("scope"):
            found.append(Violation(tick, "approval", f"task {task} made ready without a scope"))
    return found


def load_sqlite(path: Path) -> list[dict[str, Any]]:
    """Read the coordinator session `tick_log` table (read-only) into checker rows."""
    if not path.is_file():
        raise ValueError(f"no such file: {path}")
    try:
        with closing(sqlite3.connect(f"file:{path}?mode=ro", uri=True)) as db:
            present = {r[1] for r in db.execute("PRAGMA table_info(tick_log)")}
            extras = [c for c in OPTIONAL_COLUMNS if c in present]
            records = db.execute(
                "SELECT id, ready_count, running_count, dep_blocked_count, human_blocked_count,"
                " unknown_count, action_taken, evidence"
                + "".join(f", {c}" for c in extras)
                + " FROM tick_log ORDER BY id"
            ).fetchall()
    except sqlite3.Error as error:
        raise ValueError(f"cannot read tick_log: {error}") from error
    rows = [
        {
            "tick": tick,
            "counts": {
                "ready": ready,
                "running": running,
                "dependency_blocked": dep,
                "human_blocked": human,
                "unassessed": unknown,
            },
            "action": action,
            "evidence": evidence,
        }
        for tick, ready, running, dep, human, unknown, action, evidence, *_ in records
    ]
    for row, record in zip(rows, records, strict=True):
        for column, value in zip(extras, record[8:], strict=True):
            row[column] = _decode_column(column, value)
    return rows


def _decode_column(column: str, value: object) -> object:
    if column == "global_stop":
        return bool(value)
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [value] if value.strip() else []
    return [] if value is None else value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "path", type=Path, help="tick_log export (JSON array, JSON lines) or a session .db file"
    )
    parser.add_argument(
        "--require-extended",
        action="store_true",
        help="fail rows lacking closure_batch, approval, reclassified or global_stop fields",
    )
    args = parser.parse_args(argv)
    try:
        if args.path.suffix == ".db":
            rows = load_sqlite(args.path)
        else:
            rows = load_rows(args.path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    violations = check_ticks(rows, args.require_extended)
    for violation in violations:
        print(violation)
    print(f"{len(rows)} ticks, {len(violations)} violations")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
