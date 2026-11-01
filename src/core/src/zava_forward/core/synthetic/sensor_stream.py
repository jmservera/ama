"""Finite synthetic replay of the existing seasonal backfill, never device discovery."""

import asyncio
import copy
import hashlib
import json
import math
import time
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol

from . import (
    household_conditions,
    indoor_projection,
    retrofit_effects,
    sensor_backfill,
    sensor_faults,
    sensor_stock,
)

VERSION = "synthetic-stream-v2"
FAULTS = frozenset(
    {
        "valid",
        "duplicate",
        "out_of_order",
        "unmapped",
        "wrong_unit",
        "clock_skewed",
        "uncalibrated",
        "gap",
        "disconnect",
        "burst",
    }
)


class StreamError(RuntimeError):
    """Only fixed error codes may cross the transport boundary."""


class Climate(Protocol):
    def series(self, start: datetime, days: int, cadence: int) -> list[tuple[float, float]]: ...
    def manifest(self) -> dict[str, object]: ...


def wire(row: Mapping[str, str]) -> bytes:
    body = json.dumps(dict(row), sort_keys=True, ensure_ascii=True).encode("utf-8")
    if len(body) > 4096:
        raise StreamError("STREAM_MESSAGE_TOO_LARGE")
    return body


@dataclass(frozen=True)
class Replay:
    seed: int = 183
    origin: datetime = datetime(2024, 10, 1, tzinfo=UTC)
    days: int = 2
    cadence_minutes: int = 480
    first_slot: int = 0
    end_slot: int | None = None
    fault: str = "valid"

    def bounds(self) -> tuple[int, int, int]:
        if (
            type(self.seed) is not int
            or abs(self.seed) > 2**63 - 1
            or type(self.days) is not int
            or not 1 <= self.days <= 3660
            or type(self.cadence_minutes) is not int
            or self.cadence_minutes <= 0
            or 1440 % self.cadence_minutes
            or self.origin.tzinfo != UTC
            or self.origin.microsecond
            or self.fault not in FAULTS
        ):
            raise StreamError("INVALID_REPLAY")
        slots = self.days * 1440 // self.cadence_minutes
        end = slots if self.end_slot is None else self.end_slot
        if type(self.first_slot) is not int or type(end) is not int:
            raise StreamError("INVALID_REPLAY_WINDOW")
        if not 0 <= self.first_slot < end <= slots:
            raise StreamError("INVALID_REPLAY_WINDOW")
        try:
            self.origin + timedelta(days=self.days + 1)
        except OverflowError:
            raise StreamError("INVALID_REPLAY") from None
        return slots, self.first_slot, end


@dataclass(frozen=True)
class Frame:
    device_id: str
    slot: int
    row: dict[str, str]
    truth: str
    selected_stock_sha256: str
    nominal_at: datetime

    @property
    def reference(self) -> str:
        return hashlib.sha256(wire(self.row)).hexdigest()


@dataclass(frozen=True)
class RunBudget:
    owner: str
    cost_reference: str
    alert_reference: str
    max_messages: int = 100
    max_seconds: float = 60.0
    max_per_second: float = 1.0
    daily_used_units: int = 0
    reserved_headroom_units: int = 40000

    def validate(self, frames: tuple[Frame, ...]) -> int:
        if any(
            not isinstance(s, str) or not s.strip() or len(s) > 160
            for s in (
                self.owner,
                self.cost_reference,
                self.alert_reference,
            )
        ):
            raise StreamError("RUN_OWNER_COST_ALERT_REQUIRED")
        for value in (self.max_seconds, self.max_per_second):
            if type(value) not in (int, float) or not math.isfinite(value):
                raise StreamError("INVALID_RUN_LIMIT")
        if not 1 <= self.max_seconds <= 3600 or not 0 < self.max_per_second <= 100:
            raise StreamError("INVALID_RUN_LIMIT")
        if (
            type(self.max_messages) is not int
            or not 1 <= self.max_messages <= 100000
            or type(self.daily_used_units) is not int
            or self.daily_used_units < 0
            or type(self.reserved_headroom_units) is not int
            or not 40000 <= self.reserved_headroom_units <= 400000
            or not frames
            or len(frames) > self.max_messages
        ):
            raise StreamError("RUN_MESSAGE_LIMIT")
        # Reserve 1 KiB for message properties as well as each actual body.
        units = sum(math.ceil((len(wire(frame.row)) + 1024) / 4096) for frame in frames)
        if units + self.daily_used_units + self.reserved_headroom_units > 400000:
            raise StreamError("B1_QUOTA_HEADROOM")
        return units


def _selected(
    selection: sensor_stock.Selection, spec: Replay
) -> tuple[sensor_stock.Selection, list[dict[str, object]]]:
    slots, _, _ = spec.bounds()
    # Validate actual selected records, not just caller-provided summary counts.
    checked = sensor_stock.select(selection.rows, len(selection.rows))
    sensors = checked.sensors(spec.seed)
    if not 1 <= len(sensors) <= 100 or slots * len(sensors) > 100000:
        raise StreamError("REPLAY_SCALE_LIMIT")
    return checked, sensors


def replay(
    selection: sensor_stock.Selection,
    spec: Replay,
    *,
    climate: Climate | None = None,
    measures: tuple[retrofit_effects.Measure, ...] = (),
) -> tuple[Frame, ...]:
    checked, sensors = _selected(selection, spec)
    sensor_backfill._validate_model(checked, climate, measures)
    slots, first, end = spec.bounds()
    outdoor = (
        climate.series(spec.origin, spec.days, spec.cadence_minutes)
        if climate is not None
        else sensor_backfill.outdoor_series(spec.seed, spec.days, spec.cadence_minutes, spec.origin)
    )
    if len(outdoor) != slots:
        raise StreamError("REPLAY_CLIMATE_COVERAGE")
    frames: list[Frame] = []
    for sensor in sensors:
        source = sensor_backfill.readings(
            {**sensor, "fault_profile": "none"},
            spec.seed,
            spec.days,
            spec.cadence_minutes,
            outdoor,
            spec.origin,
            composed=climate is not None,
            measures=measures,
        )
        clean = [sensor_faults.observation(row) for row in source]
        for slot in range(first, end):
            # Selection uses nominal slots, never an injected timestamp.
            index = slot
            if spec.fault == "out_of_order":
                index = slot + 1 if slot % 2 == 0 and slot + 1 < slots else slot - 1
                if slots % 2 and slot == slots - 1:
                    index = slot
            row = dict(clean[index])
            if spec.fault == "unmapped":
                row["sensor_id"] = "UNMAPPED-" + row["sensor_id"]
            elif spec.fault == "wrong_unit":
                row["temperature_unit"] = "degF"
                row["temperature_c"] = f"{float(row['temperature_c']) * 1.8 + 32:.2f}"
            elif spec.fault == "clock_skewed":
                stamp = datetime.fromisoformat(row["observed_at"]) + timedelta(days=1)
                row["observed_at"] = stamp.isoformat(timespec="seconds").replace("+00:00", "Z")
            elif spec.fault == "uncalibrated":
                row["calibrated"] = "false"
            if spec.fault == "gap":
                continue
            frame = Frame(
                "SYN-" + str(sensor["sensor_id"]),
                slot,
                row,
                spec.fault,
                checked.input_sha256,
                spec.origin + timedelta(minutes=slot * spec.cadence_minutes),
            )
            wire(frame.row)
            frames.append(frame)
            if spec.fault == "duplicate":
                frames.append(
                    Frame(
                        frame.device_id,
                        slot,
                        dict(row),
                        spec.fault,
                        checked.input_sha256,
                        frame.nominal_at,
                    )
                )
    return tuple(sorted(frames, key=lambda frame: frame.slot))


def descriptor(
    selection: sensor_stock.Selection,
    spec: Replay,
    *,
    climate: Climate | None = None,
    measures: tuple[retrofit_effects.Measure, ...] = (),
) -> dict[str, object]:
    checked, sensors = _selected(selection, spec)
    sensor_backfill._validate_model(checked, climate, measures)
    result: dict[str, object] = {
        "source_type": "SYNTHETIC",
        "version": VERSION,
        "model": sensor_backfill.VERSION,
        "schema_version": sensor_faults.SCHEMA_VERSION,
        "stock_version": sensor_stock.VERSION,
        "climate": sensor_backfill.CLIMATE_SOURCE,
        "stock_sha256": selection.input_sha256,
        "selected_stock_sha256": checked.input_sha256,
        "selected_home_ids": [row["synthetic_home_id"] for row in checked.rows],
        "selected_homes": len(checked.rows),
        "monitored_homes": len(sensors),
        "seed": spec.seed,
        "origin": spec.origin.isoformat(),
        "days": spec.days,
        "cadence_minutes": spec.cadence_minutes,
        "first_slot": spec.first_slot,
        "end_slot": spec.end_slot,
        "fault": spec.fault,
        "fault_profile": "none; explicit transport exercise only",
    }
    if climate is not None:
        history = [
            {**asdict(measure), "completed_at": measure.completed_at.isoformat()}
            for measure in sorted(
                measures, key=lambda value: (value.home_id, value.completed_at, value.measure_id)
            )
        ]
        result.update(
            model=sensor_backfill.COMPOSED_VERSION,
            climate=copy.deepcopy(climate.manifest()),
            composed_model=copy.deepcopy(indoor_projection.COMPOSED_PARAMETERS),
            household_model={
                "version": household_conditions.VERSION,
                "distributions": dict(household_conditions.DISTRIBUTIONS),
            },
            retrofit_model=copy.deepcopy(retrofit_effects.PARAMETERS),
            retrofit_history=history,
            retrofit_history_sha256=hashlib.sha256(
                json.dumps(history, sort_keys=True).encode()
            ).hexdigest(),
        )
    return result


class Pacer:
    def __init__(
        self,
        budget: RunBudget,
        *,
        speed: float = 1.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if type(speed) not in (int, float) or not math.isfinite(speed) or not 0 < speed <= 1000:
            raise StreamError("INVALID_REPLAY_SPEED")
        self.speed = speed
        self.clock = clock
        self.deadline = clock() + budget.max_seconds
        self.max_per_second = budget.max_per_second
        self.paused = False
        self.stopped = False
        self.next_send = clock()
        self.last_send: float | None = None

    async def wait(self, nominal_seconds: float) -> None:
        await self._wait_until(self.clock() + nominal_seconds / self.speed)

    async def admit_send(self) -> None:
        while True:
            await self._wait_until(self.next_send)
            if self.clock() >= self.next_send:
                break
        self.last_send = self.clock()
        self.next_send = self.last_send + 1 / self.max_per_second

    def set_max_per_second(self, rate: float) -> None:
        self.max_per_second = rate
        if self.last_send is not None:
            self.next_send = self.last_send + 1 / rate

    async def _wait_until(self, target: float) -> None:
        while True:
            now = self.clock()
            if self.stopped:
                raise StreamError("RUN_STOPPED")
            if now >= self.deadline:
                raise StreamError("RUN_DEADLINE")
            if not self.paused and now >= target:
                return
            delay = min(0.05, self.deadline - now)
            if not self.paused:
                delay = min(delay, target - now)
            await asyncio.sleep(delay)
