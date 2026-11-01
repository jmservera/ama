"""Local demo of live-versus-backfill handover on a constructed SQLite store (#188).

Builds a throwaway store, writes the composed backfill, admits its prefix through
the #110 consumer, decodes the streamed suffix from actual SDK events, then runs
the operator verifier with a window replay. Constructed climate only: this is not
a live Hub run, Azure SQL proof or sensor accuracy approval. Needs the test
fixtures on PYTHONPATH (see src/api/README.md).
"""

import argparse
import csv
import json
import math
import os
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path

import test_sensor_handover as fixture
from azure.eventhub import EventData
from sensor_consumer_fixture import CONTROL, POLICY, store_at
from zava_forward.core.sensor_consumer import SensorConsumer
from zava_forward.core.sqlstore import CASE_COLS
from zava_forward.core.synthetic import sensor_backfill
from zava_forward.core.synthetic.sensor_consistency import Tolerance
from zava_forward.core.synthetic.sensor_stream import Replay, replay, wire

from zava_forward.api.iot_stream import AUTH, DEVICE, Binding, decode
from zava_forward.api.sensor_handover_verify import run as verify
from zava_forward.api.sensor_ingestion import SensorIngestion

SECOND_HOME = "stock-home-0000000000002"
END = "2024-10-05T00:00:00Z"
EVIDENCE = "constructed local SQLite; not live Hub, Azure SQL or sensor accuracy"


def demo(seam: float = 0.0, tolerance: float = 0.0) -> dict[str, object]:
    selected, climate, measures = (
        fixture.selection(),
        fixture.ConstructedClimate(),
        fixture.measures(),
    )
    if os.environ.get("ZF_SENSOR_MSSQL") == "1":
        raise ValueError("the demo is SQLite-only; unset ZF_SENSOR_MSSQL")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be a finite, non-negative number")
    spec = Replay(days=4)
    with tempfile.TemporaryDirectory(prefix="zf-handover-demo-") as tmp:
        store = store_at(tmp)
        try:
            original = store.db.execute("SELECT body FROM cases WHERE id='ZF-1'").fetchone()
            assert original is not None
            case = json.loads(str(original[0]))
            case["id"] = SECOND_HOME
            columns = ", ".join(column for column in CASE_COLS if column != "body")
            store.db.execute(
                f"INSERT INTO cases(id,seq,body,{columns}) "
                f"SELECT ?,seq,?,{columns} FROM cases WHERE id='ZF-1'",
                (SECOND_HOME, json.dumps(case)),
            )
            SensorConsumer(store).configure(
                replace(POLICY, window_end=END, max_past_seconds=4 * 86400),
                [
                    replace(
                        CONTROL,
                        sensor_id=str(sensor["sensor_id"]),
                        home_id=str(sensor["home_id"]),
                        mapping_end=END,
                        calibration_end=END,
                    )
                    for sensor in selected.sensors(spec.seed)
                ],
            )
            history = Path(tmp) / "history"
            sensor_backfill.write(
                history,
                stock=selected,
                climate=climate,
                measures=measures,
                seed=spec.seed,
                days=spec.days,
                cadence=spec.cadence_minutes,
            )
            with (history / "readings-0000.csv").open(newline="") as stream:
                reference = list(csv.DictReader(stream))
            ingestion = SensorIngestion(store)
            prefix = [dict(r) for r in reference if r["observed_at"] < fixture.HANDOVER]
            ingestion.consume(prefix, received_at="2024-10-04T16:00:00Z")
            frames = replay(
                selected, replace(spec, first_slot=6), climate=climate, measures=measures
            )
            bindings = {
                f.device_id: Binding(f.device_id, f.row["sensor_id"], f.row["home_id"])
                for f in frames
            }
            for frame in frames:
                row = dict(frame.row)
                if seam:
                    row["temperature_c"] = f"{float(row['temperature_c']) + seam:.2f}"
                event = EventData(wire(row))
                event.properties = {
                    DEVICE: frame.device_id.encode(),
                    AUTH: b'{"scope":"device","type":"x509"}',
                }
                ingestion.consume([decode(event, bindings)], received_at=row["observed_at"])
            limit = Tolerance(point=tolerance, mean_step=tolerance, stddev=tolerance)
            result = verify(
                store,
                reference,
                handover=fixture.HANDOVER,
                temperature=limit,
                replay_check=True,
                received_at="2024-10-04T16:00:00Z",
            )
        finally:
            store.db.close()
    result["evidence"] = EVIDENCE
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seam", type=float, default=0.0, help="shift live temperature (C)")
    parser.add_argument("--tolerance", type=float, default=0.0, help="temperature limit (C)")
    args = parser.parse_args(argv)
    try:
        result = demo(args.seam, args.tolerance)
    except ValueError as error:
        print(json.dumps({"passed": False, "refusal": str(error), "evidence": EVIDENCE}, indent=2))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
