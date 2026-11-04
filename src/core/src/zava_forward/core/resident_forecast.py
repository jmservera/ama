"""Deterministic 24-hour synthetic sensor estimate for the resident showcase (#462).

A transparent rule, not a model: the latest stored value moves toward the trailing 24-hour
mean, adds a clamped drift and the generator's daily pattern, and is clamped to the display
bounds. It is descriptive only. It is not a weather forecast, a live measurement or advice.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime, timedelta
from typing import Any

HORIZON_HOURS = 24
CADENCE_HOURS = 4
MIN_READINGS = 6
STALE_AFTER = timedelta(hours=24)

NOTE = (
    "Simple 24-hour synthetic forecast (estimate): calculated from your home's recent "
    "synthetic readings and typical daily pattern. It is not a weather forecast or a live "
    "sensor feed."
)
REASON_FEW = "A 24-hour forecast needs at least 6 stored readings. Only stored readings are shown."
REASON_STALE = (
    "No 24-hour forecast is shown because the latest stored reading is more than 24 hours old."
)
REASON_MISSING = "No 24-hour forecast is shown because the latest stored reading is missing."

# key, drift clamp per 24 hours, daily-pattern amplitude (sensor_backfill), display bounds
CHANNELS = (
    ("temperature_c", 1.5, -1.2, -10.0, 45.0),
    ("humidity_pct", 5.0, 1.8, 0.0, 100.0),
)


def _daily(amplitude: float, hour: float) -> float:
    return amplitude * math.cos(2 * math.pi * (hour - 3) / 24)


def _hour(stamp: datetime) -> float:
    return stamp.hour + stamp.minute / 60


def is_stale(history: list[dict[str, Any]], now: datetime) -> bool:
    if not history:
        return False
    return now - _stamp(history[-1]["observed_at"]) > STALE_AFTER


def _stamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _channel_points(
    history: list[dict[str, Any]], key: str, clamp: float, amplitude: float, low: float, high: float
) -> list[float] | None:
    latest = history[-1][key]
    last_at = _stamp(history[-1]["observed_at"])
    if latest is None:
        return None
    window = [
        (_stamp(r["observed_at"]), r[key])
        for r in history
        if r[key] is not None and last_at - _stamp(r["observed_at"]) <= STALE_AFTER
    ]
    if len(window) < MIN_READINGS:
        return None
    values = [v for _, v in window]
    mean = sum(values) / len(values)
    half = len(values) // 2
    older = sum(values[:half]) / half
    newer = sum(values[half:]) / (len(values) - half)
    span = max((window[-1][0] - window[0][0]).total_seconds() / 3600, 1.0)
    drift = max(-clamp, min(clamp, (newer - older) * HORIZON_HOURS / span))
    points = []
    for step in range(1, HORIZON_HOURS // CADENCE_HOURS + 1):
        hours = step * CADENCE_HOURS
        share = hours / HORIZON_HOURS
        target = last_at + timedelta(hours=hours)
        value = (
            latest
            + (mean - latest) * share
            + drift * share
            + _daily(amplitude, _hour(target))
            - _daily(amplitude, _hour(last_at))
        )
        points.append(round(max(low, min(high, value)), 1))
    return points


def forecast(history: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    out: dict[str, Any] = {
        "synthetic": True,
        "horizon_hours": HORIZON_HOURS,
        "cadence_hours": CADENCE_HOURS,
        "note": NOTE,
        "points": [],
        "reason": "",
    }
    if not history:
        return out
    if is_stale(history, now):
        out["reason"] = REASON_STALE
        return out
    series = {
        key: _channel_points(history, key, clamp, amplitude, low, high)
        for key, clamp, amplitude, low, high in CHANNELS
    }
    if all(values is None for values in series.values()):
        enough = sum(1 for r in history if any(r[k] is not None for k, *_ in CHANNELS))
        out["reason"] = REASON_FEW if enough < MIN_READINGS else REASON_MISSING
        return out
    last_at = _stamp(history[-1]["observed_at"])
    for index in range(HORIZON_HOURS // CADENCE_HOURS):
        point: dict[str, Any] = {
            "forecast_at": (last_at + timedelta(hours=(index + 1) * CADENCE_HOURS))
            .isoformat()
            .replace("+00:00", "Z")
        }
        for key, values in series.items():
            point[key] = None if values is None else values[index]
        out["points"].append(point)
    return out
