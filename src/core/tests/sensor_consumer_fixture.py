"""Independent fictional control values; observations come only from Packet.rows."""

import copy
import json
import os
from dataclasses import replace
from pathlib import Path

import dataset
from zava_forward.core.sensor_consumer import ExercisePolicy, Observation, SensorControl
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic import sensor_backfill, sensor_faults

RECEIVED = "2024-10-01T02:00:00Z"
POLICY = ExercisePolicy(
    window_start="2024-10-01T00:00:00Z",
    window_end="2024-10-02T00:00:00Z",
    max_past_seconds=7200,
    max_future_seconds=0,
    temperature_min=-10,
    temperature_max=45,
    humidity_min=0,
    humidity_max=100,
    accountable_role="exercise-data-quality-review",
    manual_route="manual-sensor-review",
    reviewer="Fixture Reviewer",
)
CONTROL = SensorControl(
    sensor_id="SENS-SYN-1",
    home_id="ZF-1",
    mapping_start="2024-10-01T00:00:00Z",
    mapping_end="2024-10-02T00:00:00Z",
    consent="granted",
    calibration_start="2024-10-01T00:00:00Z",
    calibration_end="2024-10-02T00:00:00Z",
    calibration_confirmed=True,
    temperature_unit="degC",
    humidity_unit="percent",
)


def observations(fault: str | None = None) -> list[Observation]:
    sensor = sensor_backfill.sensor_for({"id": "ZF-1"})
    sensor["fault_profile"] = "none"
    source = sensor_backfill.readings(
        sensor, outdoor=[(10.0, 70.0), (11.0, 72.0)], days=1, cadence=60
    )
    packet = next(
        sensor_faults.packets(
            source, sensor_faults.configure({fault: 1.0} if fault else {}), 183, "SENS-SYN-1"
        )
    )
    return [dict(row) for row in packet.rows]


def store_at(directory: str, *, reset: bool = False) -> SqlStore:
    path = Path(directory)
    seed = path / "constructed.json"
    data = copy.deepcopy(dataset.DATA)
    seed.write_text(json.dumps(data))
    if os.environ.get("ZF_SENSOR_MSSQL") == "1":
        from zava_forward.core.mssqlstore import MssqlStore, _Conn, connection_string

        if reset:
            db = _Conn(connection_string())
            try:
                db.execute("IF OBJECT_ID(N'cases', N'U') IS NOT NULL DELETE FROM cases")
            finally:
                db.close()

        return MssqlStore(str(seed), state_dir=directory)
    return SqlStore(str(seed), str(path / "constructed.sqlite"))


WIDE_POLICY = replace(POLICY, max_past_seconds=86400, max_future_seconds=86400)
