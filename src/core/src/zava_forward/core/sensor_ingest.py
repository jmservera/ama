"""Window ingestion and handover continuity over the retained per-home series (issue 188).

Synthetic evidence only: the check compares retained backfill and live-sim rows against a
declared tolerance. It is not sensor calibration, physical accuracy or live acceptance.
"""

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from decimal import Decimal

from .sensor_consumer import ConsumerError, Observation, SensorConsumer, preflight, utc
from .synthetic.live_readings import LIVE_VERSIONS
from .synthetic.sensor_consistency import CHANNELS, Tolerance

VERSION = "sensor-ingest-handover-v1"


@dataclass(frozen=True)
class WindowReceipt:
    accepted: int = 0
    replayed: int = 0
    rejected: Mapping[str, int] = field(default_factory=dict)

    @property
    def clean(self) -> bool:
        return not self.rejected


def ingest_window(
    consumer: SensorConsumer, rows: Iterable[Observation], received_at: str
) -> WindowReceipt:
    """Admit a window of rows through the consumer; re-running the same rows adds nothing.

    Idempotence comes from the consumer's per-sensor reading identity: an identical row is a
    replay, a changed value in an existing slot is an IDENTITY_CONFLICT rejection.
    """
    utc(received_at)
    batch = list(rows)
    if not batch:
        return WindowReceipt()
    accepted = replayed = 0
    rejected: dict[str, int] = {}
    for row in preflight(batch):
        receipt = consumer.process(row, received_at)
        if receipt.status == "accepted":
            if receipt.replay:
                replayed += 1
            else:
                accepted += 1
        else:
            rejected[receipt.reason] = rejected.get(receipt.reason, 0) + 1
    return WindowReceipt(accepted, replayed, dict(sorted(rejected.items())))


def home_series(
    consumer: SensorConsumer,
    home_id: str,
    window: tuple[str, str] | None = None,
) -> list[dict[str, str]]:
    """Backfill and live rows of one home in one time-ordered series, never double counted."""
    rows = consumer.retained_envelopes([home_id], None if window is None else {home_id: window})
    rows.sort(key=lambda row: (utc(row["observed_at"]), row["sensor_id"]))
    seen: set[tuple[str, str]] = set()
    for row in rows:
        slot = (row["sensor_id"], row["observed_at"])
        if row["home_id"] != home_id or slot in seen:
            raise ConsumerError("SENSOR_OUTCOME_MALFORMED")
        seen.add(slot)
    return rows


def _mean(rows: Sequence[Mapping[str, str]], channel: str) -> Decimal:
    return sum((Decimal(row[channel]) for row in rows), Decimal(0)) / len(rows)


def _indoor_series(rows: Sequence[Mapping[str, str]]) -> list[tuple[datetime, Mapping[str, str]]]:
    """One home, one sensor, one indoor calibrated schema and unit set, unique slots, sorted."""
    if not rows:
        raise ValueError("INSUFFICIENT_HANDOVER_SAMPLES")
    first = rows[0]
    if first.get("schema_version") in LIVE_VERSIONS:
        raise ValueError("HANDOVER_SCHEMA_UNSUPPORTED")
    identity = ("home_id", "sensor_id", "schema_version", "temperature_unit", "humidity_unit")
    stamped: list[tuple[datetime, Mapping[str, str]]] = []
    slots: set[datetime] = set()
    for row in rows:
        if row.get("calibrated") != "true" or any(
            row.get(key) is None or row.get(key) != first.get(key) for key in identity
        ):
            raise ValueError("INVALID_HANDOVER_OBSERVATION")
        try:
            moment = utc(row["observed_at"])
        except (KeyError, ValueError):
            raise ValueError("INVALID_HANDOVER_OBSERVATION") from None
        if moment in slots:
            raise ValueError("INVALID_HANDOVER_OBSERVATION")
        slots.add(moment)
        stamped.append((moment, row))
    stamped.sort(key=lambda item: item[0])
    return stamped


def handover_continuity(
    rows: Sequence[Mapping[str, str]],
    *,
    handover: str,
    window_minutes: int,
    temperature: Tolerance,
    humidity: Tolerance,
) -> dict[str, object]:
    """Check one home's combined series for a discontinuity at the handover instant.

    Rows before handover are the backfill side and rows at or after it the live side, each
    bounded to window_minutes. Per channel, the mean step between the sides must be within
    tolerance.mean_step and the nearest-sample step within tolerance.point (inclusive, in C or
    relative-humidity points). Tolerances are declared by the caller, never defaulted.
    """
    if type(window_minutes) is not int or window_minutes <= 0:
        raise ValueError("INVALID_HANDOVER_CONFIGURATION")
    if not isinstance(temperature, Tolerance) or not isinstance(humidity, Tolerance):
        raise ValueError("INVALID_HANDOVER_CONFIGURATION")
    boundary = utc(handover)
    span = timedelta(minutes=window_minutes)
    stamped = _indoor_series(rows)
    before = [r for t, r in stamped if boundary - span <= t < boundary]
    after = [r for t, r in stamped if boundary <= t < boundary + span]
    if not before or not after:
        raise ValueError("INSUFFICIENT_HANDOVER_SAMPLES")
    last, first = before[-1], after[0]
    metrics: dict[str, object] = {}
    passed = True
    for channel, tolerance in zip(CHANNELS, (temperature, humidity), strict=True):
        mean_step = abs(_mean(after, channel) - _mean(before, channel))
        point_step = abs(Decimal(first[channel]) - Decimal(last[channel]))
        checks = {
            "mean_step": mean_step <= Decimal(str(tolerance.mean_step)),
            "point": point_step <= Decimal(str(tolerance.point)),
        }
        passed = passed and all(checks.values())
        metrics[channel] = {
            "mean_step": float(mean_step),
            "point_step": float(point_step),
            "tolerance": {"mean_step": tolerance.mean_step, "point": tolerance.point},
            "checks": checks,
        }
    return {
        "version": VERSION,
        "source_type": "SYNTHETIC",
        "handover": handover,
        "window_minutes": window_minutes,
        "before_count": len(before),
        "after_count": len(after),
        "passed": passed,
        "metrics": metrics,
    }
