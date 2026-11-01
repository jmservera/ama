"""Operator check of live-versus-backfill consistency on the configured SQL store.

Read-only unless --replay-check is given. Opens the store from ZF_STORE
(sqlite or mssql), so the same command works on a local store and on Azure SQL.
It reports numbers; it does not approve sensor accuracy.
"""

import argparse
import csv
import json
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.sensor_consumer import ConsumerError, SensorConsumer
from zava_forward.core.synthetic.sensor_consistency import ZERO_TOLERANCE, Tolerance, report

from zava_forward.api.sensor_ingestion import BatchStopped, SensorIngestion


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
    homes = sorted({row["home_id"] for row in reference})
    result: dict[str, object] = report(
        consumer.observed_series(homes),
        reference,
        handover=handover,
        cadence_minutes=cadence_minutes,
        temperature=temperature,
        humidity=humidity,
    )
    if replay_check:
        before = consumer.observed_series(homes)
        stamp = received_at or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        receipts = SensorIngestion(store).consume(
            [dict(row) for row in reference], received_at=stamp
        )
        result["idempotent"] = (
            all(item.reason == "ACCEPTED" and item.replay for item in receipts)
            and consumer.observed_series(homes) == before
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
        from zava_forward.core.factory import open_store

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
            open_store(),
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
