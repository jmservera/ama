"""Seeded two-observation fault packets, with evaluator truth kept out of inputs."""

import math
import random
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta

VERSION = "sensor-fault-packets-v1"
SCHEMA_VERSION = "sensor-fault-input-v1"
FAULTS = (
    "outlier",
    "stuck",
    "drift",
    "gap",
    "duplicate",
    "out_of_order",
    "unmapped",
    "wrong_unit",
    "clock_skewed",
    "uncalibrated",
)
READING_FIELDS = (
    "sensor_id",
    "reading_id",
    "home_id",
    "observed_at",
    "temperature_c",
    "humidity_pct",
    "source_type",
    "scenario",
    "seed",
    "schema_version",
    "temperature_unit",
    "humidity_unit",
    "calibrated",
)
EXERCISE_VALUES = {
    "outlier_offset_c": 25.0,
    "drift_c_per_nominal_slot": 0.05,
    "clock_skew_hours": 24,
    "stuck": "Hold first packet observation for both samples",
    "classification": "Fictional exercise values, not scientific or operational bounds",
}


@dataclass(frozen=True)
class Config:
    rates: tuple[tuple[str, float], ...]

    def choose(self, rng: random.Random) -> str:
        draw = rng.random()
        cumulative = 0.0
        for name, rate in self.rates:
            cumulative += rate
            if draw < cumulative:
                return name
        return "valid"


def configure(rates: Mapping[str, float]) -> Config:
    if set(rates) - set(FAULTS):
        raise ValueError(f"Unknown fault type; choose from {', '.join(FAULTS)}")
    for rate in rates.values():
        if isinstance(rate, bool) or not math.isfinite(rate) or not 0 <= rate <= 1:
            raise ValueError("Fault rates must be finite numbers in [0, 1]")
    if math.fsum(rates.values()) > 1:
        raise ValueError("Sum of exclusive fault rates must be <= 1; remainder is valid")
    return Config(tuple((name, float(rates.get(name, 0))) for name in FAULTS))


def parse_rates(specs: Sequence[str]) -> dict[str, float]:
    rates: dict[str, float] = {}
    for spec in specs:
        name, separator, value = spec.partition("=")
        if not separator or name in rates:
            raise ValueError("Use unique --fault-rate NAME=RATE options")
        try:
            rates[name] = float(value)
        except ValueError as exc:
            raise ValueError("Use --fault-rate NAME=RATE with a numeric rate") from exc
    configure(rates)
    return rates


def validate_window(config: Config, slots: int, end: datetime) -> None:
    if slots < 2 or slots % 2:
        raise ValueError("Fault mode requires an even number of at least two nominal slots")
    if dict(config.rates)["clock_skewed"]:
        try:
            end + timedelta(days=1)
        except OverflowError as exc:
            raise ValueError("Clock-skew exercise exceeds supported calendar dates") from exc


@dataclass(frozen=True)
class Packet:
    index: int
    label: str
    clean: tuple[dict[str, str], dict[str, str]]
    rows: tuple[dict[str, str], ...]


def _input(row: Mapping[str, object]) -> dict[str, str]:
    result = {key: str(row[key]) for key in READING_FIELDS[:9]}
    result.update(
        schema_version=SCHEMA_VERSION,
        temperature_unit="degC",
        humidity_unit="percent",
        calibrated="true",
    )
    return result


def packets(
    source: Iterable[Mapping[str, object]], config: Config, seed: int, sensor_id: str
) -> Iterator[Packet]:
    """Rates select exclusive two-row packets; identities and truth never use fault labels."""
    rng = random.Random(f"{seed}-fault-packets-{sensor_id}")
    iterator = iter(source)
    index = 0
    while (first := next(iterator, None)) is not None:
        second = next(iterator, None)
        if second is None:
            raise ValueError("Fault packets require an even clean observation count")
        clean = (_input(first), _input(second))
        label = config.choose(rng)
        emitted = [dict(row) for row in clean]
        for offset, row in enumerate(emitted):
            temperature = float(row["temperature_c"])
            if label == "outlier":
                row["temperature_c"] = f"{temperature + 25:.2f}"
            elif label == "stuck":
                row["temperature_c"] = clean[0]["temperature_c"]
                row["humidity_pct"] = clean[0]["humidity_pct"]
            elif label == "drift":
                row["temperature_c"] = f"{temperature + 0.05 * (index * 2 + offset + 1):.2f}"
            elif label == "unmapped":
                row["sensor_id"] = "UNMAPPED-" + sensor_id
            elif label == "wrong_unit":
                row["temperature_c"] = f"{temperature * 1.8 + 32:.2f}"
                row["temperature_unit"] = "degF"
            elif label == "clock_skewed":
                shifted = datetime.fromisoformat(row["observed_at"]) + timedelta(days=1)
                row["observed_at"] = shifted.isoformat(timespec="seconds").replace("+00:00", "Z")
            elif label == "uncalibrated":
                row["calibrated"] = "false"
        if label == "gap":
            emitted = []
        elif label == "duplicate":
            emitted = [dict(row) for row in emitted for _ in range(2)]
        elif label == "out_of_order":
            emitted.reverse()
        yield Packet(index, label, clean, tuple(emitted))
        index += 1
