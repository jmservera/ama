"""Versioned exercise projection; not calibrated physics or historical climate."""

import math
import random
from collections.abc import Mapping
from datetime import datetime

from .household_conditions import Condition

VERSION = "indoor-projection-exercise-v2"
COMPOSED_VERSION = "indoor-projection-composed-exercise-v2"
TEMPERATURE_SIGMA_C = 0.3
HUMIDITY_SIGMA_PCT = 1.5
NOISE_LIMIT_SIGMAS = 3.0
NOISE_PARAMETERS = {
    "classification": "Noise scales and tail cap are exercise values, not confidence intervals.",
    "temperature_sigma_c": TEMPERATURE_SIGMA_C,
    "humidity_sigma_pct": HUMIDITY_SIGMA_PCT,
    "limit_sigmas": NOISE_LIMIT_SIGMAS,
    "residual": "clip(Normal(0,sigma), -limit_sigmas*sigma, limit_sigmas*sigma)",
}
OUTPUT_BOUNDS = {
    "basis": "Per supplied outdoor temperature/RH pair and dwelling model; not calibrated physics.",
    "temperature_c": "[B - 3*0.3, B + 3*0.3], B = noiseless indoor temperature",
    "humidity_pct": "clip([100*V/sat(B+3*0.3)-3*1.5,"
    " 100*V/sat(B-3*0.3)+3*1.5], 0, 100), V = model vapour",
    "relative_humidity_domain": "0..100 percent, including saturation;"
    " not a healthy-home threshold",
    "scope": "Nominal projection before injected sensor faults; CSV rounding may differ by 0.005.",
}
COMPOSED_PARAMETERS = {
    "version": COMPOSED_VERSION,
    "classification": "Uncalibrated synthetic exercise composition, not measured performance.",
    "loss": "dwelling * age * construction * active dated measure multiplier",
    "temperature": "B + bounded residual(sigma=0.3),"
    " B = household setpoint + min(0,(outdoor-5)*0.08*loss)"
    " + max(0,(outdoor-16)*0.35)",
    "vapour": "sat(outdoor)*RH/100 + household moisture*loss/ventilation",
    "humidity": "clip(100*vapour/sat(indoor) + bounded residual(sigma=1.5), 0, 100)",
    "noise": NOISE_PARAMETERS,
    "output_bounds": OUTPUT_BOUNDS,
    "legacy_retrofit_flag": "Not used; explicit dated history only",
}
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
    "temperature": "B + bounded residual(sigma=0.3),"
    " B = setpoint + min(0,(outdoor-5)*0.08*loss) + max(0,(outdoor-16)*0.35)",
    "humidity": "clip(100*(sat(outdoor)*RH/100 + moisture*loss)/sat(indoor)"
    " + bounded residual(sigma=1.5), 0, 100)",
    "noise": NOISE_PARAMETERS,
    "output_bounds": OUTPUT_BOUNDS,
    "saturation_hpa": "6.112 * exp(17.62*T/(243.12+T)); coefficients retained as exercise values",
    "heating": "all_day 07-23; morning_evening 06-09/17-22; low 17-21 (UTC, end exclusive)",
    "setpoint_c": "20.5 when scheduled and outdoor <15; otherwise 17",
    "moisture_hpa": "1.6 when scheduled; otherwise 1.2",
    "historical_bounds": "Derived per supplied pair; default outdoor series is synthetic."
    " Historical source provenance belongs to the caller's climate manifest.",
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


def _bounded_noise(rng: random.Random, sigma: float) -> float:
    limit = NOISE_LIMIT_SIGMAS * sigma
    return max(-limit, min(limit, rng.gauss(0, sigma)))


def _project(
    rng: random.Random,
    t_out: float,
    rh_out: float,
    loss: float,
    setpoint: float,
    moisture_hpa: float,
) -> tuple[float, float]:
    base = setpoint + min(0.0, (t_out - 5) * 0.08 * loss) + max(0.0, (t_out - 16) * 0.35)
    temperature = base + _bounded_noise(rng, TEMPERATURE_SIGMA_C)
    vapour = saturation_pressure(t_out) * rh_out / 100 + moisture_hpa
    humidity = max(
        0.0,
        min(
            100.0,
            100 * vapour / saturation_pressure(temperature)
            + _bounded_noise(rng, HUMIDITY_SIGMA_PCT),
        ),
    )
    return temperature, humidity


def project(
    sensor: Mapping[str, object],
    rng: random.Random,
    at: datetime,
    outdoor_temperature: float,
    outdoor_humidity: float,
) -> tuple[float, float]:
    """Derive a nominal indoor envelope from each outdoor pair and exercise dwelling."""
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
    return _project(rng, t_out, rh_out, loss, setpoint, (1.6 if heated else 1.2) * loss)


def project_composed(
    sensor: Mapping[str, object],
    rng: random.Random,
    at: datetime,
    outdoor_temperature: float,
    outdoor_humidity: float,
    household: Condition,
    loss_multiplier: float,
) -> tuple[float, float]:
    """Apply explicit household conditions and dated effects without legacy enum coercion."""
    offset = at.utcoffset()
    if offset is None or offset.total_seconds() != 0:
        raise ValueError("Projection time must be UTC-aware")
    if household.home_id != sensor.get("home_id") or household.observed_at != at:
        raise ValueError("Household condition must match the canonical home and observation")
    if household.source_type != "SYNTHETIC":
        raise ValueError("Only synthetic household conditions are supported")
    t_out = _number(outdoor_temperature, -80.0, 60.0, "outdoor temperature")
    rh_out = _number(outdoor_humidity, 0.0, 100.0, "outdoor humidity")
    dwelling, age = sensor.get("dwelling_type"), sensor.get("age_band")
    if not isinstance(dwelling, str) or dwelling not in DWELLINGS:
        raise ValueError("Unsupported exercise dwelling type")
    if not isinstance(age, str) or age not in AGE_BANDS:
        raise ValueError("Unsupported exercise age band")
    construction = _number(sensor.get("construction_loss", 1.0), 0.75, 1.2, "construction")
    if construction not in CONSTRUCTION_FACTORS:
        raise ValueError("Unsupported exercise construction factor")
    multiplier = _number(loss_multiplier, 0.0, 1.0, "dated loss multiplier")
    if multiplier <= 0:
        raise ValueError("Dated loss multiplier must be positive")
    setpoint = _number(household.setpoint_c, 16.0, 22.0, "household setpoint")
    ventilation = _number(household.ventilation_multiplier, 0.8, 1.2, "ventilation")
    moisture = _number(household.moisture_increment_hpa, 0.0, 2.4, "moisture")
    loss = DWELLINGS[dwelling] * AGE_BANDS[age] * construction * multiplier
    return _project(rng, t_out, rh_out, loss, setpoint, moisture * loss / ventilation)
