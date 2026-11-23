"""Read-through view of one connection for the assistant forecast (issue #2304).

The forecast evaluates every open case for every assistant. Each evaluation used to issue its own
per-case and repeated global statements, so a live Azure SQL run made thousands of round trips and
never answered. This view answers a repeated statement once and serves the per-case lookups from a
few bulk reads, so the statement count stays flat as open cases grow. Every answer equals what the
single statement would have returned; anything not recognised passes through unchanged.
"""

from __future__ import annotations

import time
from collections import defaultdict
from collections.abc import Iterable, Sequence
from typing import Any

CHUNK = 500


class ForecastTimeout(RuntimeError):
    """The forecast did not finish within its time budget; nothing was written."""


class _Rows:
    def __init__(self, rows: Iterable[Sequence[Any]]) -> None:
        self._rows = list(rows)

    def fetchone(self) -> Sequence[Any] | None:
        return self._rows[0] if self._rows else None

    def fetchall(self) -> list[Sequence[Any]]:
        return list(self._rows)


class ForecastReads:
    def __init__(self, db: Any, mssql: bool, budget: float | None) -> None:
        self._db = db
        self._mssql = mssql
        self._deadline = time.monotonic() + budget if budget else None
        self._memo: dict[Any, list[Sequence[Any]]] = {}
        self._schedule: dict[tuple[Any, Any], tuple[Any, ...]] | None = None
        self._known: dict[str, tuple[Any, ...] | None] = {}
        self._adopted: set[str] = set()
        self._adopt_bound = 0
        self._adoptable: dict[tuple[Any, Any], list[Any]] = defaultdict(list)
        self._homes: dict[str, set[str] | Exception] = {}
        self.statements = 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self._db, name)

    def check(self) -> None:
        if self._deadline is not None and time.monotonic() > self._deadline:
            raise ForecastTimeout("The forecast did not finish within its time budget.")

    def _run(self, sql: str, params: Sequence[Any] = ()) -> list[Sequence[Any]]:
        self.check()
        self.statements += 1
        return list(self._db.execute(sql, params).fetchall())

    def execute(self, sql: str, params: Sequence[Any] = ()) -> Any:
        key = " ".join(sql.split())
        args = tuple(params)
        if key.startswith(
            "SELECT scope,signature,task_id,at,replaced,seen,paused_at FROM assistant_schedule"
        ):
            slot = self._slot(*args)
            return _Rows([slot] if slot else [])
        if key == "SELECT 1 FROM assistant_tasks WHERE id=?":
            return _Rows([(1,)] if self._task(args[0]) else [])
        if key == "SELECT state,attempts FROM assistant_tasks WHERE id=?":
            found = self._task(args[0])
            return _Rows([found[:2]] if found else [])
        if key == "SELECT state,attempts,body FROM assistant_tasks WHERE id=?":
            found = self._task(args[0])
            return _Rows([found] if found else [])
        if "FROM assistant_tasks WHERE capability=? AND case_id=? AND attempts>0" in key:
            return _Rows(self._adopt_page(sql, args))
        absent = self._absent_home(key, args)
        if absent:
            return _Rows([])
        if key.startswith("SELECT") and not key.startswith("SELECT 1 "):
            if (key, args) not in self._memo:
                self._memo[(key, args)] = self._run(sql, args)
            return _Rows(self._memo[(key, args)])
        self.check()
        self.statements += 1
        return self._db.execute(sql, params)

    def _slot(self, cap: str, case_id: str) -> tuple[Any, ...] | None:
        self._load_schedule()
        assert self._schedule is not None
        return self._schedule.get((cap, case_id))

    def _load_schedule(self) -> None:
        if self._schedule is None:
            self._schedule = {
                (r[0], r[1]): tuple(r[2:])
                for r in self._run(
                    "SELECT capability,case_id,scope,signature,task_id,at,replaced,seen,paused_at"
                    " FROM assistant_schedule"
                )
            }

    def has_slot(self, cap: str, case_id: str) -> bool:
        return self._slot(cap, case_id) is not None

    def slot_task_ids(self) -> set[str]:
        self._load_schedule()
        return {s[2] for s in (self._schedule or {}).values() if s[2]}

    def load_tasks(self, ids: Iterable[str]) -> None:
        """Read the named proposals by primary key in chunks; any other id is asked for singly."""
        wanted = sorted(set(ids) - set(self._known))
        for start in range(0, len(wanted), CHUNK):
            part = wanted[start : start + CHUNK]
            marks = ",".join("?" * len(part))
            for tid, state, attempts, body in self._run(
                f"SELECT id,state,attempts,body FROM assistant_tasks WHERE id IN ({marks})",
                tuple(part),
            ):
                self._known[tid] = (state, attempts, body)
        for tid in wanted:
            self._known.setdefault(tid, None)

    def _task(self, task_id: str) -> tuple[Any, ...] | None:
        if task_id not in self._known:
            self.load_tasks([task_id])
        return self._known[task_id]

    def prefetch_adoptions(self, case_ids: Iterable[str], bound: int) -> None:
        """Newest dispatched proposals per assistant and case, at most `bound` each."""
        ids = sorted(set(case_ids) - self._adopted)
        for start in range(0, len(ids), CHUNK):
            part = ids[start : start + CHUNK]
            marks = ",".join("?" * len(part))
            for tid, raw, own, cap, case_id in self._run(
                "SELECT id,body,signature,capability,case_id FROM ("
                "SELECT id,body,signature,capability,case_id,ROW_NUMBER() OVER ("
                "PARTITION BY capability,case_id ORDER BY dispatched DESC, revision DESC, id) AS rn"
                f" FROM assistant_tasks WHERE attempts>0 AND case_id IN ({marks})) t"
                " WHERE rn<=? ORDER BY capability,case_id,rn",
                (*part, bound),
            ):
                self._adoptable[(cap, case_id)].append((tid, raw, own))
        self._adopted.update(ids)
        self._adopt_bound = bound

    def _adopt_page(self, sql: str, args: Sequence[Any]) -> Sequence[Sequence[Any]]:
        cap, case_id, first, second = args
        limit, offset = (second, first) if self._mssql else (first, second)
        if case_id not in self._adopted or offset + limit > self._adopt_bound:
            return self._run(sql, args)
        return self._adoptable[(cap, case_id)][offset : offset + limit]

    def _absent_home(self, key: str, args: Sequence[Any]) -> bool:
        """True when a per-home sensor lookup is certain to be empty (one distinct-home read)."""
        for table, marker in (
            ("sensor_reading", "FROM sensor_reading WHERE home_id=?"),
            ("sensor_consumer_control_home", "FROM sensor_consumer_control_home WHERE home_id=?"),
        ):
            if marker in key and args:
                if table not in self._homes:
                    try:
                        extra = (
                            " WHERE source_type='SYNTHETIC'" if table == "sensor_reading" else ""
                        )
                        self._homes[table] = {
                            str(r[0])
                            for r in self._run(f"SELECT DISTINCT home_id FROM {table}{extra}")
                        }
                    except Exception as exc:
                        self._homes[table] = exc
                known = self._homes[table]
                if isinstance(known, Exception):
                    # A store that cannot answer one home cannot answer any; repeat the failure.
                    raise known
                return str(args[0]) not in known
        return False
