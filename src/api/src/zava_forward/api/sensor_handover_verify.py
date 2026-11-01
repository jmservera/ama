"""Operator check of live-versus-backfill consistency on the configured SQL store.

Read-only unless --replay-check is given: the store is opened without schema
migration or other initialization writes. ZF_STORE (sqlite or mssql) selects the
store, so the same command works on a local store and on Azure SQL. Readings are
bounded to the reference window per home. --replay-check re-feeds the retained
stored payloads for that window, in batches of 100, and needs write access.
It reports numbers; it does not approve sensor accuracy.
"""

import argparse
import csv
import json
import os
import sqlite3
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.mssqlstore import MssqlStore
from zava_forward.core.sensor_consumer import ConsumerError, SensorConsumer
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic.sensor_consistency import ZERO_TOLERANCE, Tolerance, report

from zava_forward.api.sensor_ingestion import BatchStopped, SensorIngestion

BATCH = 100


class _ReadOnlySqlite(SqlStore):
    """Skips SqlStore initialization; connections are read-only unless writable."""

    def __init__(self, path: str, writable: bool = False) -> None:
        self.db_path = path
        self.writable = writable

    def assistant_connection(self) -> sqlite3.Connection:
        mode = "rw" if self.writable else "ro"
        db = sqlite3.connect(f"file:{self.db_path}?mode={mode}", uri=True, isolation_level=None)
        db.execute("PRAGMA busy_timeout=5000")
        return db


class _UninitializedMssql(MssqlStore):
    """Skips schema creation and migration; the verifier only selects unless replaying."""

    def __init__(self, env: Mapping[str, str]) -> None:
        self._env = env


def open_existing_store(
    env: Mapping[str, str] | None = None, *, writable: bool = False
) -> SqlStore:
    from zava_forward.core.factory import sqlite_path

    env = os.environ if env is None else env
    kind = (env.get("ZF_STORE") or "json").lower()
    if kind == "sqlite":
        path = sqlite_path(env)
        if not os.path.exists(path):
            raise ValueError("SENSOR_STORE_NOT_FOUND")
        return _ReadOnlySqlite(path, writable)
    if kind == "mssql":
        return _UninitializedMssql(env)
    raise ValueError("SQL_STORE_REQUIRED")


def _windows(reference: Sequence[dict[str, str]]) -> dict[str, tuple[str, str]]:
    spans: dict[str, tuple[str, str]] = {}
    for row in reference:
        if any(type(row.get(name)) is not str for name in ("home_id", "observed_at")):
            raise ValueError("REFERENCE_ROW_INCOMPLETE")
        low, high = spans.get(row["home_id"], (row["observed_at"], row["observed_at"]))
        spans[row["home_id"]] = (min(low, row["observed_at"]), max(high, row["observed_at"]))
    return spans


def run(
    store: object,
    reference: Sequence[dict[str, str]],
    *,
    handover: str,
    cadence_minutes: int = 480,
    temperature: Tolerance = ZERO_TOLERANCE,
    humidity: Tolerance = ZERO_TOLERANCE,
    replay_check: bool = False,
    received_at: str | None = None,
) -> dict[str, object]:
    consumer = SensorConsumer(store)
    windows = _windows(reference)
    homes = sorted(windows)
    result: dict[str, object] = report(
        consumer.observed_series(homes, windows),
        reference,
        handover=handover,
        cadence_minutes=cadence_minutes,
        temperature=temperature,
        humidity=humidity,
    )
    if replay_check:
        before = consumer.observed_series(homes, windows)
        stamp = received_at or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        ingestion = SensorIngestion(store)
        receipts = [
            item
            for start in range(0, len(before), BATCH)
            for item in ingestion.consume(before[start : start + BATCH], received_at=stamp)
        ]
        result["idempotent"] = (
            len(receipts) == len(before)
            and all(item.reason == "ACCEPTED" and item.replay for item in receipts)
            and consumer.observed_series(homes, windows) == before
        )
        result["passed"] = bool(result["passed"]) and result["idempotent"]
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True, help="backfill readings CSV")
    parser.add_argument("--handover", required=True, help="UTC handover slot, ...Z")
    parser.add_argument("--cadence-minutes", type=int, default=480)
    for channel in ("temperature", "humidity"):
        for metric in ("point", "mean-step", "stddev"):
            parser.add_argument(f"--{channel}-{metric}", type=float, default=0.0)
    parser.add_argument("--replay-check", action="store_true", help="re-run the window (writes)")
    parser.add_argument("--received-at", help="receipt time for --replay-check, default now")
    args = parser.parse_args(argv)
    try:
        with args.reference.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        tolerances = {
            channel: Tolerance(
                point=getattr(args, f"{channel}_point"),
                mean_step=getattr(args, f"{channel}_mean_step"),
                stddev=getattr(args, f"{channel}_stddev"),
            )
            for channel in ("temperature", "humidity")
        }
        result = run(
            open_existing_store(writable=args.replay_check),
            rows,
            handover=args.handover,
            cadence_minutes=args.cadence_minutes,
            replay_check=args.replay_check,
            received_at=args.received_at,
            **tolerances,
        )
    except (ValueError, KeyError, OSError, ConsumerError, BatchStopped) as error:
        print(json.dumps({"passed": False, "refused": str(error)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
