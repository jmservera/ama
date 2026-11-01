"""Bounded synthetic sensor exercises, not a diagnosis or approved analytics method."""

import argparse
import csv
import json
import math
import platform
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path

from . import provenance, sensor_backfill, sensor_faults

VERSION = "sensor-scenarios-exercise-v1"
METHOD_VERSION = "sensor-comparator-exercise-v1"
START = datetime(2024, 1, 1, tzinfo=UTC)
DAYS = 28
SLOTS = DAYS * 24
SEED = 190
HOUR = timedelta(hours=1)
CLASSIFICATION = "SYNTHETIC EXERCISE ONLY; not installed devices or real home conditions"
NO_SIGNAL = "NO_EXERCISE_SIGNAL"
REVIEW = "REVIEW_CANDIDATE"
INSUFFICIENT = "INSUFFICIENT"
RULES = {
    "classification": "Every threshold, duration and range is an exercise value",
    "humidity_threshold_pct": 75.0,
    "consecutive_hours": 12,
    "overnight_utc": "[00:00,06:00) grouped by UTC calendar date",
    "overnight_high_hours": 3,
    "overnight_count": 3,
    "minimum_coverage_per_day_and_window": 0.9,
    "flatline_hours": 24,
    "temperature_domain_c": [-10.0, 45.0],
    "humidity_domain_pct": [0.0, 100.0],
}


@dataclass(frozen=True)
class Window:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        for value in (self.start, self.end):
            if (
                not isinstance(value, datetime)
                or value.utcoffset() != timedelta(0)
                or any((value.hour, value.minute, value.second, value.microsecond))
            ):
                raise ValueError("Window boundaries must be UTC-aware midnight instants")
        if not timedelta(days=1) <= self.end - self.start <= timedelta(days=DAYS):
            raise ValueError("Window must span 1..28 whole UTC days")

    @property
    def expected(self) -> int:
        return int((self.end - self.start) / HOUR)


@dataclass(frozen=True)
class Analysis:
    status: str
    expected: int
    present: int
    valid: int
    coverage: float
    reasons: tuple[str, ...]
    longest_high_hours: int
    high_nights: int
    longest_flatline_hours: int
    mean_temperature_c: float | None
    mean_humidity_pct: float | None


@dataclass(frozen=True)
class Truth:
    case_id: str
    family: str
    label: str
    seed: int
    rng_key: str
    expected_outcome: str
    temperature_delta_c: float = 0.0
    humidity_delta_points: float = 0.0
    delay_days: int = 0


@dataclass(frozen=True)
class Case:
    case_id: str
    rows: tuple[dict[str, str], ...]
    truth: Truth


def _result(value: Analysis) -> dict[str, object]:
    return {**asdict(value), "reasons": list(value.reasons)}


def _stamp(value: datetime) -> str:
    return value.isoformat(timespec="seconds").replace("+00:00", "Z")


def _time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() != timedelta(0) or _stamp(parsed) != value:
        raise ValueError("Observation time must be canonical whole-second UTC")
    return parsed


def _threshold(value: float) -> None:
    if isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 100:
        raise ValueError("Exercise humidity threshold must be finite in [0,100]")


def analyse(
    rows: Sequence[Mapping[str, str]], window: Window, *, humidity_threshold: float = 75.0
) -> Analysis:
    """Read observations only; never consult labels, seeds or expected outcomes."""
    _threshold(humidity_threshold)
    reasons: set[str] = set()
    samples: dict[datetime, tuple[float, float]] = {}
    seen_times: set[datetime] = set()
    reading_ids: set[str] = set()
    identities: set[tuple[str, str]] = set()
    previous: datetime | None = None
    for row in rows:
        if set(row) != set(sensor_faults.READING_FIELDS) or not all(
            isinstance(value, str) for value in row.values()
        ):
            reasons.add("SCHEMA_FIELDS")
            continue
        try:
            at = _time(row["observed_at"])
            temperature, humidity = float(row["temperature_c"]), float(row["humidity_pct"])
        except (ValueError, OverflowError):
            reasons.add("INVALID_VALUE_OR_TIME")
            continue
        identities.add((row["sensor_id"], row["home_id"]))
        if not window.start <= at < window.end or (at - window.start) % HOUR:
            reasons.add("OUTSIDE_WINDOW_OR_OFF_GRID")
            continue
        if at in seen_times or row["reading_id"] in reading_ids:
            reasons.add("DUPLICATE")
        if previous is not None and at <= previous:
            reasons.add("OUT_OF_ORDER")
        seen_times.add(at)
        reading_ids.add(row["reading_id"])
        previous = at
        if (
            row["source_type"] != "SYNTHETIC"
            or row["schema_version"] != sensor_faults.SCHEMA_VERSION
            or row["temperature_unit"] != "degC"
            or row["humidity_unit"] != "percent"
            or row["calibrated"] != "true"
            or not row["sensor_id"]
            or not row["home_id"]
            or not row["reading_id"]
            or not math.isfinite(temperature)
            or not math.isfinite(humidity)
            or not -10 <= temperature <= 45
            or not 0 <= humidity <= 100
        ):
            reasons.add("INVALID_OBSERVATION")
            continue
        samples[at] = temperature, humidity
    if len(identities) > 1:
        reasons.add("MIXED_SERIES")
    coverage = len(samples) / window.expected
    if coverage < 0.9:
        reasons.add("WINDOW_COVERAGE")
    high_run = longest_high = flat_run = longest_flat = high_nights = 0
    prior_sample: tuple[float, float] | None = None
    for day in range((window.end - window.start).days):
        day_start = window.start + timedelta(days=day)
        day_valid = night_valid = night_high = 0
        for hour in range(24):
            sample = samples.get(day_start + hour * HOUR)
            if sample is None:
                high_run = flat_run = 0
                prior_sample = None
                continue
            day_valid += 1
            high = sample[1] >= humidity_threshold
            high_run = high_run + 1 if high else 0
            longest_high = max(longest_high, high_run)
            flat_run = flat_run + 1 if sample == prior_sample else 1
            longest_flat = max(longest_flat, flat_run)
            prior_sample = sample
            if hour < 6:
                night_valid += 1
                night_high += high
        if day_valid / 24 < 0.9:
            reasons.add("DAY_COVERAGE")
        if night_valid / 6 < 0.9:
            reasons.add("NIGHT_COVERAGE")
        if night_high >= 3:
            high_nights += 1
    if longest_flat >= 24:
        reasons.add("FLATLINE")
    status = (
        INSUFFICIENT if reasons else REVIEW if longest_high >= 12 or high_nights >= 3 else NO_SIGNAL
    )
    sufficient = status != INSUFFICIENT
    return Analysis(
        status,
        window.expected,
        len(seen_times),
        len(samples),
        round(coverage, 6),
        tuple(sorted(reasons)),
        longest_high,
        high_nights,
        longest_flat,
        sum(t for t, _ in samples.values()) / len(samples) if sufficient else None,
        sum(h for _, h in samples.values()) / len(samples) if sufficient else None,
    )


def generate(seed: int = SEED) -> tuple[Case, ...]:
    """Exercise profiles overlay clean backfill; default backfill behavior is untouched."""
    if type(seed) is not int or not 0 <= seed <= 2**63 - 1:
        raise ValueError("Seed must be an integer in [0,2**63-1]")
    definitions = (
        ("damp", "normal", NO_SIGNAL, 0.0, 0.0, 0),
        ("damp", "condensation_prone", REVIEW, 0.0, 0.0, 0),
        ("damp", "sustained_high_humidity", REVIEW, 0.0, 0.0, 0),
        ("damp", "repeated_overnight_peaks", REVIEW, 0.0, 0.0, 0),
        ("damp", "sensor_fault", INSUFFICIENT, 0.0, 0.0, 0),
        ("damp", "missing_data", INSUFFICIENT, 0.0, 0.0, 0),
        ("damp", "seasonal_shift", NO_SIGNAL, 0.0, 0.0, 0),
        ("retrofit", "improvement", "IMPROVEMENT", 2.0, -10.0, 0),
        ("retrofit", "no_change", "NO_CHANGE", 0.0, 0.0, 0),
        ("retrofit", "delayed_effect", "DELAYED_EFFECT", 1.5, -6.0, 7),
        ("retrofit", "adverse_effect", "ADVERSE_EFFECT", -1.0, 8.0, 0),
    )
    cases = []
    for index, (family, label, expected, delta_t, delta_h, delay) in enumerate(definitions):
        case_id = f"C{index + 1:02d}"
        home_id = f"SCENARIO-{index + 1:02d}"
        sensor = {
            "sensor_id": f"SYN{index + 1:03d}",
            "home_id": home_id,
            "dwelling_type": "terrace",
            "age_band": "1945-1979",
            "retrofitted": False,
            "heating_pattern": "all_day",
            "fault_profile": "none",
        }
        source = list(
            sensor_backfill.readings(  # type: ignore[no-untyped-call]
                sensor, seed, days=DAYS, cadence=60, outdoor=[(2.0, 70.0)] * SLOTS, start=START
            )
        )
        # A weekly repeated residual gives matched periods, not a weather-adjusted causal estimate.
        residual_t = [float(row["temperature_c"]) for row in source[:168]]
        residual_h = [float(row["humidity_pct"]) for row in source[:168]]
        mean_t, mean_h = sum(residual_t) / 168, sum(residual_h) / 168
        rows = []
        for slot, raw in enumerate(source):
            row = sensor_faults.observation(raw)
            temperature = 20 + 0.15 * (residual_t[slot % 168] - mean_t)
            humidity = 55 + 0.15 * (residual_h[slot % 168] - mean_h)
            hour, day = slot % 24, slot // 24
            if label == "condensation_prone":
                temperature -= 5
                humidity += 37
            elif label == "sustained_high_humidity":
                humidity += 27
            elif label == "repeated_overnight_peaks" and hour < 6:
                humidity += 30
            elif label == "seasonal_shift":
                temperature -= 2 * slot / (SLOTS - 1)
                humidity += 8 * slot / (SLOTS - 1)
            if family == "retrofit" and day >= 14 + delay:
                temperature += delta_t
                humidity += delta_h
            if label == "sensor_fault" and slot < 48:
                temperature, humidity = 20.0, 55.0
            if label == "missing_data" and slot % 4:
                continue
            row.update(
                temperature_c=f"{temperature:.2f}",
                humidity_pct=f"{humidity:.2f}",
                scenario="SCENARIO_PACK",
            )
            rows.append(row)
        truth = Truth(
            case_id,
            family,
            label,
            seed,
            f"{seed}-series-{home_id}",
            expected,
            delta_t,
            delta_h,
            delay,
        )
        cases.append(Case(case_id, tuple(rows), truth))
    return tuple(cases)


def confusion(expected: Sequence[str], predicted: Sequence[str]) -> dict[str, int | float | None]:
    """One damp case per trial; abstentions and expected insufficiency stay visible."""
    outcomes = {NO_SIGNAL, REVIEW, INSUFFICIENT}
    if len(expected) != len(predicted) or any(x not in outcomes for x in (*expected, *predicted)):
        raise ValueError("Confusion inputs require aligned known exercise outcomes")
    counts = dict(
        total=len(expected),
        eligible=0,
        binary_classified=0,
        abstained=0,
        expected_insufficient=0,
        correct_insufficient=0,
        incorrect_insufficient=0,
        tp=0,
        tn=0,
        fp=0,
        fn=0,
    )
    for actual, prediction in zip(expected, predicted, strict=True):
        if actual == INSUFFICIENT:
            counts["expected_insufficient"] += 1
            counts[
                "correct_insufficient" if prediction == INSUFFICIENT else "incorrect_insufficient"
            ] += 1
            continue
        counts["eligible"] += 1
        if prediction == INSUFFICIENT:
            counts["abstained"] += 1
            continue
        counts["binary_classified"] += 1
        cell = (
            ("tp" if prediction == REVIEW else "fn")
            if actual == REVIEW
            else ("fp" if prediction == REVIEW else "tn")
        )
        counts[cell] += 1
    positives = counts["tp"] + counts["fn"]
    negatives = counts["tn"] + counts["fp"]
    return {
        **counts,
        "miss_rate_among_classified_positives": counts["fn"] / positives if positives else None,
        "false_alert_rate_among_classified_negatives": counts["fp"] / negatives
        if negatives
        else None,
    }


def retrofit_comparison(
    rows: Sequence[Mapping[str, str]], measure_at: datetime
) -> dict[str, object]:
    """Observed baseline/early/late means; no truth, causal claim or resident assessment."""
    windows = {
        "baseline": Window(measure_at - timedelta(days=14), measure_at - timedelta(days=7)),
        "early": Window(measure_at, measure_at + timedelta(days=7)),
        "late": Window(measure_at + timedelta(days=7), measure_at + timedelta(days=14)),
    }
    # Validate the whole supplied sequence first so slicing cannot hide invalid/order faults.
    whole = analyse(rows, Window(measure_at - timedelta(days=14), measure_at + timedelta(days=14)))
    results = {
        name: analyse(
            [
                row
                for row in rows
                if isinstance(row.get("observed_at"), str)
                and _stamp(w.start) <= row["observed_at"] < _stamp(w.end)
            ],
            w,
        )
        for name, w in windows.items()
    }
    deltas: dict[str, object] = {}
    for name in ("early", "late"):
        baseline, outcome = results["baseline"], results[name]
        valid = whole.status != INSUFFICIENT and all(
            value is not None
            for value in (
                baseline.mean_temperature_c,
                outcome.mean_temperature_c,
                baseline.mean_humidity_pct,
                outcome.mean_humidity_pct,
            )
        )
        if valid:
            assert (
                baseline.mean_temperature_c is not None and outcome.mean_temperature_c is not None
            )
            assert baseline.mean_humidity_pct is not None and outcome.mean_humidity_pct is not None
            deltas[name] = {
                "temperature_c": round(outcome.mean_temperature_c - baseline.mean_temperature_c, 6),
                "humidity_points": round(outcome.mean_humidity_pct - baseline.mean_humidity_pct, 6),
            }
        else:
            deltas[name] = None
    return {
        "status": INSUFFICIENT
        if whole.status == INSUFFICIENT or None in deltas.values()
        else "SUFFICIENT",
        "whole": _result(whole),
        "windows": {name: _result(value) for name, value in results.items()},
        "deltas": deltas,
        "interpretation": "Descriptive exercise only; not causation, blame or a savings promise",
    }


def report(cases: Sequence[Case], *, humidity_threshold: float = 75.0) -> dict[str, object]:
    """Join fixed evaluator truth only after observations-only predictions."""
    _threshold(humidity_threshold)
    window = Window(START, START + timedelta(days=DAYS))
    damp = [case for case in cases if case.truth.family == "damp"]
    predictions = [
        analyse(case.rows, window, humidity_threshold=humidity_threshold) for case in damp
    ]
    checks: list[dict[str, object]] = []
    for case, prediction in zip(damp, predictions, strict=True):
        checks.append(
            {
                "case_id": case.case_id,
                "check": "damp_outcome",
                "label": case.truth.label,
                "expected": case.truth.expected_outcome,
                "observed": _result(prediction),
                "status": "PASS" if prediction.status == case.truth.expected_outcome else "FAIL",
            }
        )
    for case in cases:
        if case.truth.family != "retrofit":
            continue
        comparison = retrofit_comparison(case.rows, START + timedelta(days=14))
        for name in ("early", "late"):
            expected_t = case.truth.temperature_delta_c
            expected_h = case.truth.humidity_delta_points
            if name == "early" and case.truth.delay_days:
                expected_t = expected_h = 0.0
            deltas = comparison["deltas"]
            assert isinstance(deltas, dict)
            observed = deltas[name]
            passed = isinstance(observed, dict) and (
                abs(observed["temperature_c"] - expected_t) <= 0.02
                and abs(observed["humidity_points"] - expected_h) <= 0.02
            )
            checks.append(
                {
                    "case_id": case.case_id,
                    "check": f"retrofit_{name}",
                    "label": case.truth.label,
                    "expected": {"temperature_c": expected_t, "humidity_points": expected_h},
                    "observed": comparison,
                    "status": "PASS" if passed else "FAIL",
                }
            )
    expected = [case.truth.expected_outcome for case in damp]
    sensitivity = []
    for threshold in (70.0, 75.0, 85.0):
        observed = [
            analyse(case.rows, window, humidity_threshold=threshold).status for case in damp
        ]
        sensitivity.append(
            {
                "humidity_threshold_pct": threshold,
                "confusion": confusion(expected, observed),
            }
        )
    return {
        "version": VERSION,
        "method_version": METHOD_VERSION,
        "source_type": "SYNTHETIC",
        "classification": CLASSIFICATION,
        "rules": {**RULES, "humidity_threshold_pct": humidity_threshold},
        "checks": checks,
        "confusion": confusion(expected, [value.status for value in predictions]),
        "sensitivity": sensitivity,
        "limits": [
            "Hand-designed case counts are not operational prevalence or predictive accuracy",
            "No agreed R3 false-alert/miss limit or competent R2 method approval",
            "Air temperature/RH alone cannot establish surface condensation or mould",
            "No tasks, clocks, ranking, consent, resident reports or holds changed",
            "Actual #111/#133 integration and live #184 execution remain unperformed",
        ],
    }


def _destination(out: str | Path) -> Path:
    path = Path(out).expanduser().absolute()
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError("Scenario output cannot use symlink components")
    path = path.resolve()
    if any((part / ".git").exists() for part in (path, *path.parents)):
        raise ValueError("Scenario output must be outside repositories and worktrees")
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise FileExistsError("Choose a new or empty scenario output directory")
    return path


def _json(path: Path, payload: object) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8"
    )


def write(
    out: str | Path, seed: int = SEED, *, humidity_threshold: float = 75.0
) -> dict[str, object]:
    destination = _destination(out)
    cases = generate(seed)
    evaluation = report(cases, humidity_threshold=humidity_threshold)
    revision = provenance.source_revision(
        (
            *sensor_backfill.revision_sources(faults=True),
            Path(__file__),
        )
    )
    root = provenance.prepare_output(destination)
    analysis, truth = root / "analysis", root / "truth"
    analysis.mkdir()
    truth.mkdir()
    for case in cases:
        with (analysis / f"{case.case_id}.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(
                stream, fieldnames=sensor_faults.READING_FIELDS, lineterminator="\n"
            )
            writer.writeheader()
            writer.writerows(case.rows)
    _json(
        analysis / "windows.json",
        {
            "schema_version": VERSION,
            "source_type": "SYNTHETIC",
            "start": _stamp(START),
            "end_exclusive": _stamp(START + timedelta(days=DAYS)),
            "cadence_minutes": 60,
            "cases": [
                {
                    "case_id": case.case_id,
                    "file": f"{case.case_id}.csv",
                    "measure_at": _stamp(START + timedelta(days=14))
                    if case.truth.family == "retrofit"
                    else None,
                }
                for case in cases
            ],
        },
    )
    hashes = {
        f"analysis/{name}": digest
        for name, digest in provenance.file_hashes(analysis.iterdir()).items()
    }
    evaluation["input_sha256"] = dict(hashes)
    _json(truth / "report.json", evaluation)
    _json(truth / "cases.json", [asdict(case.truth) for case in cases])
    hashes.update(
        {
            f"truth/{name}": digest
            for name, digest in provenance.file_hashes(truth.iterdir()).items()
        }
    )
    manifest = {
        "schema_version": VERSION,
        "version": VERSION,
        "method_version": METHOD_VERSION,
        "source_type": "SYNTHETIC",
        "classification": CLASSIFICATION,
        "seed": seed,
        "generator_revision": revision,
        "python_version": platform.python_version(),
        "window": {
            "start": _stamp(START),
            "end_exclusive": _stamp(START + timedelta(days=DAYS)),
            "cadence_minutes": 60,
            "nominal_slots_per_case": SLOTS,
        },
        "weather": "CONSTRUCTED constant outdoor 2 degC/70 percent RH; NOT the ERA5 source",
        "parameters": {
            "baseline_c": 20,
            "baseline_humidity_pct": 55,
            "residual_scale": 0.15,
            "repeat_residual_hours": 168,
            "condensation_offsets": {"temperature_c": -5, "humidity_points": 37},
            "sustained_humidity_offset_points": 27,
            "overnight_offset_points": 30,
            "fault_hold_hours": 48,
            "missing_keep_every_nth_hour": 4,
            "seasonal_change": {"temperature_c": -2, "humidity_points": 8},
            "measure_day": 14,
            "comparison_days": 7,
            "delta_tolerance": 0.02,
            "rules": evaluation["rules"],
        },
        "case_count": len(cases),
        "rows": sum(len(case.rows) for case in cases),
        "file_sha256": hashes,
    }
    _json(truth / "manifest.json", manifest)
    return evaluation


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", required=True, help="New/empty external synthetic snapshot directory"
    )
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--humidity-threshold", type=float, default=75.0, help="Exercise RH percent"
    )
    args = parser.parse_args(argv)
    try:
        evaluation = write(args.out, args.seed, humidity_threshold=args.humidity_threshold)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"sensor-scenarios: {exc}\n")
    print(json.dumps(evaluation, sort_keys=True, allow_nan=False))
    checks = evaluation["checks"]
    assert isinstance(checks, list)
    if any(check["status"] != "PASS" for check in checks):
        parser.exit(
            1, "sensor-scenarios: one or more exercise checks failed; inspect truth/report.json\n"
        )


if __name__ == "__main__":
    main()
