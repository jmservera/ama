"""Pure generator of live synthetic home readings from daily average climate (issue 184).

Input is only an hourly anchor profile for the day (24 temperature, humidity and sunlight values
built from daily averages). Output is one reading per home per 5-minute UTC slot: smooth
interpolation between hour anchors, a small bounded smoothed noise, and a bounded per-home offset.
Everything is a pure function of (seed, home_id, slot), so a run is reproducible. No transport,
credential, clock, store or AI call is made here. Readings are synthetic and labelled SYNTHETIC;
they never represent an installed real device.
"""

import hashlib
import json
import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from . import sensor_identity

VERSION = "live-sim-generator-v1"
SCHEMA_VERSION = "live-sim-reading-v1"
SLOT_SECONDS = 300
SLOTS_PER_DAY = 86400 // SLOT_SECONDS
SUNLIGHT_UNIT = "W/m2"  # global horizontal irradiance, watts per square metre
NOISE_TEMPERATURE_C = 0.4
NOISE_HUMIDITY_PCT = 2.0
NOISE_SUNLIGHT_FRACTION = 0.05
OFFSET_TEMPERATURE_C = 1.0
OFFSET_HUMIDITY_PCT = 3.0
OFFSET_SUNLIGHT_FRACTION = 0.10
NOISE_KNOT_MINUTES = 30
LABEL = "SYNTHETIC simulated reading; not a real device"
MAX_BODY_BYTES = 1024


class LiveReadingError(ValueError):
    """Only fixed error codes are raised."""


@dataclass(frozen=True)
class DailyAverages:
    temperature_c: float
    humidity_pct: float
    sunlight_wm2: float

    def validate(self) -> None:
        values = (self.temperature_c, self.humidity_pct, self.sunlight_wm2)
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
            raise LiveReadingError("INVALID_DAILY_AVERAGES")
        if (
            not -40 <= self.temperature_c <= 50
            or not 0 <= self.humidity_pct <= 100
            or not 0 <= self.sunlight_wm2 <= 1400
        ):
            raise LiveReadingError("INVALID_DAILY_AVERAGES")


@dataclass(frozen=True)
class HourlyAnchors:
    temperature_c: tuple[float, ...]
    humidity_pct: tuple[float, ...]
    sunlight_wm2: tuple[float, ...]

    def validate(self) -> None:
        for series in (self.temperature_c, self.humidity_pct, self.sunlight_wm2):
            if len(series) != 24 or any(
                type(v) not in (int, float) or not math.isfinite(v) for v in series
            ):
                raise LiveReadingError("INVALID_HOURLY_ANCHORS")
        if any(not 0 <= v <= 100 for v in self.humidity_pct) or any(
            v < 0 for v in self.sunlight_wm2
        ):
            raise LiveReadingError("INVALID_HOURLY_ANCHORS")


AnchorSource = Callable[[date], HourlyAnchors]

# Illustrative UK-like monthly daily averages: a synthetic assumption, not measured data.
# (temperature degC, relative humidity %, 24-hour mean global horizontal irradiance W/m2)
MONTHLY_AVERAGES = (
    (5.0, 87.0, 20.0),
    (5.5, 84.0, 40.0),
    (7.5, 79.0, 80.0),
    (9.5, 73.0, 130.0),
    (12.5, 72.0, 180.0),
    (15.5, 72.0, 200.0),
    (17.5, 72.0, 190.0),
    (17.2, 74.0, 160.0),
    (14.5, 79.0, 110.0),
    (11.5, 85.0, 60.0),
    (8.0, 88.0, 28.0),
    (5.5, 88.0, 15.0),
)
TEMPERATURE_SWING_C = 3.0  # peak at 15:00, trough at 03:00
HUMIDITY_SWING_PCT = 8.0  # opposite phase to temperature


def seasonal_averages(day: date) -> DailyAverages:
    temperature, humidity, sunlight = MONTHLY_AVERAGES[day.month - 1]
    return DailyAverages(temperature, humidity, sunlight)


def anchors_from_averages(averages: DailyAverages, day: date) -> HourlyAnchors:
    """Shape 24 hourly anchors whose means equal the supplied daily averages.

    Temperature and humidity follow a day cycle that sums to zero over 24 hours. Sunlight is a
    daylight bell for the day of year, scaled so the 24-hour mean equals the average. Humidity is
    clamped to 0..100 after shaping, which can move its mean only near saturation.
    """
    averages.validate()
    hours = range(24)
    phase = [math.cos(2 * math.pi * (h - 15) / 24) for h in hours]
    temperature = tuple(averages.temperature_c + TEMPERATURE_SWING_C * p for p in phase)
    humidity = tuple(
        min(100.0, max(0.0, averages.humidity_pct - HUMIDITY_SWING_PCT * p)) for p in phase
    )
    half_day = 6.1 + 2.1 * math.cos(2 * math.pi * (day.timetuple().tm_yday - 172) / 365)
    bell = [
        max(0.0, math.cos(math.pi / 2 * (h + 0.5 - 12) / half_day))
        if abs(h + 0.5 - 12) < half_day
        else 0.0
        for h in hours
    ]
    total = sum(bell)
    scale = averages.sunlight_wm2 * 24 / total if total else 0.0
    return HourlyAnchors(temperature, humidity, tuple(b * scale for b in bell))


def seasonal_anchors(day: date) -> HourlyAnchors:
    return anchors_from_averages(seasonal_averages(day), day)


def slot_floor(moment: datetime) -> datetime:
    """Align an aware instant to the start of its 5-minute UTC slot."""
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise LiveReadingError("UTC_TIME_REQUIRED")
    utc = moment.astimezone(UTC)
    return utc.replace(
        minute=utc.minute - utc.minute % (SLOT_SECONDS // 60), second=0, microsecond=0
    )


def next_slot(moment: datetime) -> datetime:
    return slot_floor(moment) + timedelta(seconds=SLOT_SECONDS)


def _unit(*parts: object) -> float:
    """Deterministic value in [-1, 1] from the parts."""
    digest = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / (2**63) - 1.0


def _ease(fraction: float) -> float:
    return fraction * fraction * (3 - 2 * fraction)


def _blend(low: float, high: float, fraction: float) -> float:
    return low + (high - low) * _ease(fraction)


@dataclass(frozen=True)
class Reading:
    home_id: str
    sensor_id: str
    device_id: str
    observed_at: datetime
    temperature_c: float
    humidity_pct: float
    sunlight_wm2: float
    seed: int

    @property
    def reading_id(self) -> str:
        return f"LIVE-{self.sensor_id}-{self.observed_at:%Y%m%dT%H%M}Z"

    def row(self) -> dict[str, str]:
        return {
            "sensor_id": self.sensor_id,
            "reading_id": self.reading_id,
            "home_id": self.home_id,
            "observed_at": self.observed_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "temperature_c": f"{self.temperature_c:.2f}",
            "humidity_pct": f"{self.humidity_pct:.2f}",
            "sunlight_wm2": f"{self.sunlight_wm2:.2f}",
            "temperature_unit": "degC",
            "humidity_unit": "percent",
            "sunlight_unit": SUNLIGHT_UNIT,
            "source_type": "SYNTHETIC",
            "scenario": "live-simulator",
            "seed": str(self.seed),
            "schema_version": SCHEMA_VERSION,
            "injected_fault": "none",
            "label": LABEL,
        }

    def body(self) -> bytes:
        text = json.dumps(self.row(), sort_keys=True, ensure_ascii=True, separators=(",", ":"))
        data = text.encode("ascii")
        if len(data) > MAX_BODY_BYTES:
            raise LiveReadingError("MESSAGE_TOO_LARGE")
        return data


class Generator:
    def __init__(self, seed: int = 184, anchors: AnchorSource = seasonal_anchors) -> None:
        if type(seed) is not int or abs(seed) > 2**63 - 1:
            raise LiveReadingError("INVALID_SEED")
        self.seed = seed
        self._anchors = anchors
        self._cache: dict[date, HourlyAnchors] = {}

    def anchors(self, day: date) -> HourlyAnchors:
        cached = self._cache.get(day)
        if cached is None:
            cached = self._anchors(day)
            cached.validate()
            if len(self._cache) > 4:
                self._cache.clear()
            self._cache[day] = cached
        return cached

    def baseline(self, moment: datetime) -> tuple[float, float, float]:
        """Interpolated anchors for a slot start; hour 23 blends toward the next day's 00:00."""
        slot = slot_floor(moment)
        minutes = slot.hour * 60 + slot.minute
        hour, minute = divmod(minutes, 60)
        fraction = minute / 60
        today = self.anchors(slot.date())
        if hour == 23:
            after = self.anchors(slot.date() + timedelta(days=1))
            ends = (after.temperature_c[0], after.humidity_pct[0], after.sunlight_wm2[0])
        else:
            ends = (
                today.temperature_c[hour + 1],
                today.humidity_pct[hour + 1],
                today.sunlight_wm2[hour + 1],
            )
        starts = (today.temperature_c[hour], today.humidity_pct[hour], today.sunlight_wm2[hour])
        t, h, s = (_blend(a, b, fraction) for a, b in zip(starts, ends, strict=True))
        return t, h, s

    def _knot(self, home_id: str, channel: str, day: date, index: int) -> float:
        if index == 24 * 60 // NOISE_KNOT_MINUTES:
            day, index = day + timedelta(days=1), 0
        return _unit(self.seed, home_id, day.isoformat(), channel, index)

    def noise(self, home_id: str, channel: str, moment: datetime) -> float:
        """Smoothed noise in [-1, 1]: seeded knots every 30 minutes, eased between them."""
        slot = slot_floor(moment)
        minutes = slot.hour * 60 + slot.minute
        index, rest = divmod(minutes, NOISE_KNOT_MINUTES)
        low = self._knot(home_id, channel, slot.date(), index)
        high = self._knot(home_id, channel, slot.date(), index + 1)
        return _blend(low, high, rest / NOISE_KNOT_MINUTES)

    def offsets(self, home_id: str) -> tuple[float, float, float]:
        """Constant per-home offsets: degC, humidity points, sunlight factor."""
        return (
            OFFSET_TEMPERATURE_C * _unit(self.seed, home_id, "offset", "temperature"),
            OFFSET_HUMIDITY_PCT * _unit(self.seed, home_id, "offset", "humidity"),
            1.0 + OFFSET_SUNLIGHT_FRACTION * _unit(self.seed, home_id, "offset", "sunlight"),
        )

    def reading(self, home_id: str, moment: datetime) -> Reading:
        if not sensor_identity.home_key(home_id):
            raise LiveReadingError("INVALID_HOME_ID")
        slot = slot_floor(moment)
        base_t, base_h, base_s = self.baseline(slot)
        off_t, off_h, off_s = self.offsets(home_id)
        temperature = (
            base_t + off_t + NOISE_TEMPERATURE_C * self.noise(home_id, "temperature", slot)
        )
        humidity = base_h + off_h + NOISE_HUMIDITY_PCT * self.noise(home_id, "humidity", slot)
        sunlight = (
            base_s * off_s * (1 + NOISE_SUNLIGHT_FRACTION * self.noise(home_id, "sunlight", slot))
        )
        sensor_id = sensor_identity.sensor_key(home_id)
        return Reading(
            home_id,
            sensor_id,
            "SYN-" + sensor_id,
            slot,
            temperature,
            min(100.0, max(0.0, humidity)),
            max(0.0, sunlight),
            self.seed,
        )
