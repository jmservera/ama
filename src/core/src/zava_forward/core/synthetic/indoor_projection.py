"""Versioned exercise projection; not calibrated physics or historical climate."""

import math
import random
from collections.abc import Mapping
from datetime import datetime

VERSION = "indoor-projection-exercise-v1"
DWELLINGS = {
    "apartments": 0.7,
    "terrace": 1.0,
    "semidetached_house": 1.15,
    "detached": 1.3,
    "bungalow": 1.2,
}
AGE_BANDS = {
    "pre-1919": 1.3,
    "1919-1944": 1.2,
    "1945-1979": 1.1,
    "1980-2002": 0.95,
    "2003+": 0.8,
}
CONSTRUCTION_FACTORS = frozenset((0.75, 0.85, 0.9, 1.0, 1.1, 1.15, 1.2))
PARAMETERS = {
    "version": VERSION,
    "classification": "Every coefficient, schedule, noise scale and domain is an exercise value.",
    "outdoor_api_domain": {"temperature_c": [-80.0, 60.0], "humidity_pct": [0.0, 100.0]},
    "loss": "dwelling * age * (0.75 if legacy retrofit flag else 1) * construction",
    "temperature": "max(8, setpoint + min(0,(outdoor-5)*0.08*loss)"
    " + max(0,(outdoor-16)*0.35) + Normal(0,0.3))",
    "humidity": "clip(100*(sat(outdoor)*RH/100 + moisture*loss)/sat(indoor)"
    " + Normal(0,1.5), 15, 98)",
    "saturation_hpa": "6.112 * exp(17.62*T/(243.12+T)); coefficients retained as exercise values",
    "heating": "all_day 07-23; morning_evening 06-09/17-22; low 17-21 (UTC, end exclusive)",
    "setpoint_c": "20.5 when scheduled and outdoor <15; otherwise 17",
    "moisture_hpa": "1.6 when scheduled; otherwise 1.2",
    "historical_bounds": "Not established: no approved paired outdoor record is supplied.",
}


def _number(value: object, low: float, high: float, name: str) -> float:
    if type(value) not in (int, float):
        raise ValueError(f"{name} must be a finite number in [{low}, {high}]")
    assert isinstance(value, (int, float))
    if not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"{name} must be a finite number in [{low}, {high}]")
    return float(value)


def saturation_pressure(temperature: float) -> float:
    temperature = _number(temperature, -80.0, 60.0, "temperature")
    return 6.112 * math.exp(17.62 * temperature / (243.12 + temperature))


def project(
    sensor: Mapping[str, object],
    rng: random.Random,
    at: datetime,
    outdoor_temperature: float,
    outdoor_humidity: float,
) -> tuple[float, float]:
    """Preserve the legacy equation/RNG order over its supported exercise domain."""
    offset = at.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise ValueError("Projection time must be UTC-aware")
    t_out = _number(outdoor_temperature, -80.0, 60.0, "outdoor temperature")
    rh_out = _number(outdoor_humidity, 0.0, 100.0, "outdoor humidity")
    dwelling, age = sensor.get("dwelling_type"), sensor.get("age_band")
    if not isinstance(dwelling, str) or dwelling not in DWELLINGS:
        raise ValueError("Unsupported exercise dwelling type")
    if not isinstance(age, str) or age not in AGE_BANDS:
        raise ValueError("Unsupported exercise age band")
    retrofitted = sensor.get("retrofitted")
    if type(retrofitted) is not bool:
        raise ValueError("Legacy retrofitted flag must be boolean, not evidence of dated works")
    construction = _number(sensor.get("construction_loss", 1.0), 0.75, 1.2, "construction")
    if construction not in CONSTRUCTION_FACTORS:
        raise ValueError("Unsupported exercise construction factor")
    pattern = sensor.get("heating_pattern")
    hour = at.hour
    schedules = {
        "all_day": 7 <= hour < 23,
        "morning_evening": 6 <= hour < 9 or 17 <= hour < 22,
        "low": 17 <= hour < 21,
    }
    if not isinstance(pattern, str) or pattern not in schedules:
        raise ValueError("Unsupported exercise heating schedule")
    loss = DWELLINGS[dwelling] * AGE_BANDS[age] * (0.75 if retrofitted else 1.0)
    loss *= construction
    heated = schedules[pattern]
    setpoint = 20.5 if heated and t_out < 15 else 17.0
    base = setpoint + min(0.0, (t_out - 5) * 0.08 * loss) + max(0.0, (t_out - 16) * 0.35)
    t_in = max(8.0, base + rng.gauss(0, 0.3))
    vapour = saturation_pressure(t_out) * rh_out / 100 + (1.6 * loss if heated else 1.2 * loss)
    rh_in = max(15.0, min(98.0, 100 * vapour / saturation_pressure(t_in) + rng.gauss(0, 1.5)))
    return t_in, rh_in
