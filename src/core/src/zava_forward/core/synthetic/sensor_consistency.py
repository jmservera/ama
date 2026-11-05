"""Strict synthetic handover evidence, not sensor calibration or live acceptance."""

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from statistics import mean, pstdev, pvariance

from ..sensor_consumer import LIVE_FIELDS, SensorConsumer, utc
from . import live_readings
from .sensor_faults import READING_FIELDS

CHANNELS = ("temperature_c", "humidity_pct")


@dataclass(frozen=True)
class Tolerance:
    point: float = 0.0
    mean_step: float = 0.0
    stddev: float = 0.0

    def __post_init__(self) -> None:
        if any(
            type(value) not in (int, float) or not math.isfinite(value) or value < 0
            for value in (self.point, self.mean_step, self.stddev)
        ):
            raise ValueError("INVALID_HANDOVER_TOLERANCE")


ZERO_TOLERANCE = Tolerance()

WEATHER_CHANNELS = ("temperature_c", "humidity_pct", "sunlight_wm2")
WEATHER_UNITS = ("degC", "percent", live_readings.SUNLIGHT_UNIT)
WEATHER_VERSION = "synthetic-weather-continuity-v1"
WEATHER_TOLERANCE_STATUS = (
    "engineering bound derived from declared generator constants; "
    "not an approved operational tolerance"
)
_ROUNDING = 0.02  # two reading values, each rounded to 2 decimals
_SUNLIGHT_CAP = 1400.0


def _weather_tolerance(point: float) -> "Tolerance":
    # Triangle inequality: mean-step <= 2*point and stddev difference <= point. Clamps are
    # 1-Lipschitz, so the bounds still hold at the 0..100 and non-negative limits.
    return Tolerance(point=point, mean_step=2 * point, stddev=point)


WEATHER_TOLERANCES = {
    "temperature_c": _weather_tolerance(
        2 * (live_readings.OFFSET_TEMPERATURE_C + live_readings.NOISE_TEMPERATURE_C) + _ROUNDING
    ),
    "humidity_pct": _weather_tolerance(
        2 * (live_readings.OFFSET_HUMIDITY_PCT + live_readings.NOISE_HUMIDITY_PCT) + _ROUNDING
    ),
    "sunlight_wm2": _weather_tolerance(
        _SUNLIGHT_CAP
        * (
            (1 + live_readings.OFFSET_SUNLIGHT_FRACTION)
            * (1 + live_readings.NOISE_SUNLIGHT_FRACTION)
            - (1 - live_readings.OFFSET_SUNLIGHT_FRACTION)
            * (1 - live_readings.NOISE_SUNLIGHT_FRACTION)
        )
        + _ROUNDING
    ),
}


def _stddev_within_limit(
    values: Sequence[Decimal], baseline: Sequence[Decimal], limit: float
) -> bool:
    variance = pvariance([Fraction(value) for value in values])
    ref_variance = pvariance([Fraction(value) for value in baseline])
    residual = variance + ref_variance - Fraction(str(limit)) ** 2
    # |sqrt(a) - sqrt(b)| <= t iff a+b-t*t <= 2*sqrt(a*b).
    # Only square a positive residual, so the comparison remains equivalent.
    return residual <= 0 or residual**2 <= 4 * variance * ref_variance


def _index(
    rows: Sequence[Mapping[str, str]],
) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        if SensorConsumer._shape(dict(row)) is not None or (
            row["temperature_unit"],
            row["humidity_unit"],
            row["calibrated"],
        ) != ("degC", "percent", "true"):
            raise ValueError("INVALID_HANDOVER_OBSERVATION")
        key = (row["home_id"], row["sensor_id"], row["observed_at"])
        if key in result:
            raise ValueError("DUPLICATE_HANDOVER_SLOT")
        result[key] = dict(row)
    if not result:
        raise ValueError("EMPTY_HANDOVER_SERIES")
    identities = [(row["sensor_id"], row["reading_id"]) for row in result.values()]
    if len(set(identities)) != len(identities):
        raise ValueError("DUPLICATE_HANDOVER_IDENTITY")
    return result


def _compare(
    actual: Mapping[tuple[str, str, str], Mapping[str, str]],
    expected: Mapping[tuple[str, str, str], Mapping[str, str]],
    channels: Sequence[str],
    tolerances: Sequence[Tolerance],
    boundary: datetime,
    cadence_minutes: int,
) -> tuple[list[dict[str, object]], bool]:
    groups = sorted({key[:2] for key in expected})
    homes = [home for home, _ in groups]
    if len(set(homes)) != len(homes) or len({sensor for _, sensor in groups}) != len(groups):
        raise ValueError("AMBIGUOUS_HANDOVER_MAPPING")
    series: list[dict[str, object]] = []
    passed = True
    for home, sensor in groups:
        keys = sorted(key for key in expected if key[:2] == (home, sensor))
        stamps = [utc(key[2]) for key in keys]
        if (
            any(
                later - earlier != timedelta(minutes=cadence_minutes)
                for earlier, later in zip(stamps, stamps[1:], strict=False)
            )
            or boundary not in stamps
        ):
            raise ValueError("HANDOVER_CADENCE_MISMATCH")
        split = stamps.index(boundary)
        if split < 2 or len(keys) - split < 2:
            raise ValueError("INSUFFICIENT_HANDOVER_SAMPLES")
        metrics: dict[str, object] = {}
        for channel, tolerance in zip(channels, tolerances, strict=True):
            values = [Decimal(actual[key][channel]) for key in keys]
            baseline = [Decimal(expected[key][channel]) for key in keys]
            means = [mean(part) for part in (values[:split], values[split:])]
            ref_means = [mean(part) for part in (baseline[:split], baseline[split:])]
            deviations = [pstdev(part) for part in (values[:split], values[split:])]
            ref_deviations = [pstdev(part) for part in (baseline[:split], baseline[split:])]
            point_error = max(abs(a - b) for a, b in zip(values, baseline, strict=True))
            step_numerator = abs(
                (sum(values[split:], Decimal(0)) - sum(baseline[split:], Decimal(0))) * split
                - (sum(values[:split], Decimal(0)) - sum(baseline[:split], Decimal(0)))
                * (len(keys) - split)
            )
            step_scale = split * (len(keys) - split)
            stddev_error = max(abs(a - b) for a, b in zip(deviations, ref_deviations, strict=True))
            checks = {
                "point": point_error <= Decimal(str(tolerance.point)),
                "mean_step": step_numerator <= Decimal(str(tolerance.mean_step)) * step_scale,
                "stddev": all(
                    _stddev_within_limit(part, ref_part, tolerance.stddev)
                    for part, ref_part in zip(
                        (values[:split], values[split:]),
                        (baseline[:split], baseline[split:]),
                        strict=True,
                    )
                ),
            }
            step_error = step_numerator / step_scale
            passed = passed and all(checks.values())
            metrics[channel] = {
                "mean_before": float(means[0]),
                "mean_after": float(means[1]),
                "reference_mean_before": float(ref_means[0]),
                "reference_mean_after": float(ref_means[1]),
                "stddev_before": float(deviations[0]),
                "stddev_after": float(deviations[1]),
                "reference_stddev_before": float(ref_deviations[0]),
                "reference_stddev_after": float(ref_deviations[1]),
                "max_point_error": float(point_error),
                "mean_step_error": float(step_error),
                "max_stddev_error": float(stddev_error),
                "checks": checks,
            }
        series.append(
            {
                "home_id": home,
                "sensor_id": sensor,
                "before_count": split,
                "after_count": len(keys) - split,
                "metrics": metrics,
            }
        )
    return series, passed


def report(
    observed: Sequence[Mapping[str, str]],
    reference: Sequence[Mapping[str, str]],
    *,
    handover: str,
    cadence_minutes: int = 480,
    temperature: Tolerance = ZERO_TOLERANCE,
    humidity: Tolerance = ZERO_TOLERANCE,
) -> dict[str, object]:
    """Compare complete per-home windows with an independently generated reference.

    Mean-step error subtracts the reference's expected seasonal/works step.
    Point and per-side population-standard-deviation errors prevent cancellation.
    All thresholds are inclusive, in C or relative-humidity percentage points.
    """
    boundary = utc(handover)
    if (
        type(cadence_minutes) is not int
        or cadence_minutes <= 0
        or 1440 % cadence_minutes
        or not isinstance(temperature, Tolerance)
        or not isinstance(humidity, Tolerance)
    ):
        raise ValueError("INVALID_HANDOVER_CONFIGURATION")
    actual, expected = _index(observed), _index(reference)
    if actual.keys() != expected.keys():
        raise ValueError("HANDOVER_COVERAGE_MISMATCH")
    for key in expected:
        if any(
            actual[key][field] != expected[key][field]
            for field in READING_FIELDS
            if field not in CHANNELS
        ):
            raise ValueError("HANDOVER_METADATA_MISMATCH")
    series, passed = _compare(
        actual, expected, CHANNELS, (temperature, humidity), boundary, cadence_minutes
    )
    return {
        "version": "synthetic-handover-v1",
        "source_type": "SYNTHETIC",
        "handover": handover,
        "cadence_minutes": cadence_minutes,
        "tolerances": {
            channel: {
                "point": tolerance.point,
                "mean_step": tolerance.mean_step,
                "stddev": tolerance.stddev,
                "unit": unit,
            }
            for channel, tolerance, unit in zip(
                CHANNELS, (temperature, humidity), ("degC", "percent"), strict=True
            )
        },
        "passed": passed,
        "series": series,
    }


def _weather_index(
    rows: Sequence[Mapping[str, str]], scenario: str
) -> dict[tuple[str, str, str], dict[str, str]]:
    result: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        if (
            set(row) != set(LIVE_FIELDS)
            or SensorConsumer._live_shape(dict(row)) is not None
            or row["schema_version"] != live_readings.SCHEMA_VERSION
            or (row["temperature_unit"], row["humidity_unit"], row["sunlight_unit"])
            != WEATHER_UNITS
            or row["scenario"] != scenario
        ):
            raise ValueError("INVALID_HANDOVER_OBSERVATION")
        key = (row["home_id"], row["sensor_id"], row["observed_at"])
        if key in result:
            raise ValueError("DUPLICATE_HANDOVER_SLOT")
        result[key] = dict(row)
    if not result:
        raise ValueError("EMPTY_HANDOVER_SERIES")
    identities = [(row["sensor_id"], row["reading_id"]) for row in result.values()]
    if len(set(identities)) != len(identities):
        raise ValueError("DUPLICATE_HANDOVER_IDENTITY")
    return result


def weather_report(
    observed: Sequence[Mapping[str, str]],
    reference: Sequence[Mapping[str, str]],
    *,
    handover: str,
    cadence_minutes: int = live_readings.SLOT_SECONDS // 60,
) -> dict[str, object]:
    """Constructed continuity check of live simulated weather against synthetic weather history.

    Both sides are live-sim-reading-v1 rows for the same homes and slots; only the seed and the
    scenario (live-simulator versus weather-backfill-v1) differ. Tolerances are engineering bounds
    from the declared generator constants, not an approved tolerance, and the result is not
    witnessed Azure continuity, physical accuracy, indoor evidence or calibration.
    """
    boundary = utc(handover)
    if type(cadence_minutes) is not int or cadence_minutes <= 0 or 1440 % cadence_minutes:
        raise ValueError("INVALID_HANDOVER_CONFIGURATION")
    actual = _weather_index(observed, live_readings.SCENARIO)
    expected = _weather_index(reference, live_readings.WEATHER_REFERENCE_SCENARIO)
    if actual.keys() != expected.keys():
        raise ValueError("HANDOVER_COVERAGE_MISMATCH")
    provenance = {"scenario", "seed"}
    for key in expected:
        if any(
            actual[key][field] != expected[key][field]
            for field in LIVE_FIELDS
            if field not in WEATHER_CHANNELS and field not in provenance
        ):
            raise ValueError("HANDOVER_METADATA_MISMATCH")
    series, passed = _compare(
        actual,
        expected,
        WEATHER_CHANNELS,
        [WEATHER_TOLERANCES[channel] for channel in WEATHER_CHANNELS],
        boundary,
        cadence_minutes,
    )
    return {
        "version": WEATHER_VERSION,
        "source_type": "SYNTHETIC",
        "evidence": "constructed-distribution-check",
        "handover": handover,
        "cadence_minutes": cadence_minutes,
        "tolerance_status": WEATHER_TOLERANCE_STATUS,
        "generator": {
            "version": live_readings.VERSION,
            "reference_scenario": live_readings.WEATHER_REFERENCE_SCENARIO,
            "live_scenario": live_readings.SCENARIO,
            "same_anchors_assumed": True,
        },
        "tolerances": {
            channel: {
                "point": WEATHER_TOLERANCES[channel].point,
                "mean_step": WEATHER_TOLERANCES[channel].mean_step,
                "stddev": WEATHER_TOLERANCES[channel].stddev,
                "unit": unit,
            }
            for channel, unit in zip(WEATHER_CHANNELS, WEATHER_UNITS, strict=True)
        },
        "passed": passed,
        "series": series,
    }
