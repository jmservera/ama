"""Strict synthetic handover evidence, not sensor calibration or live acceptance."""

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from fractions import Fraction
from statistics import mean, pstdev, pvariance

from ..sensor_consumer import SensorConsumer, utc
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
        for channel, tolerance in zip(CHANNELS, (temperature, humidity), strict=True):
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
