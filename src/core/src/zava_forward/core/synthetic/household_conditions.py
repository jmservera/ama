"""Neutral synthetic household variation, never inferred resident conduct."""

import random
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

VERSION = "household-conditions-exercise-v1"
SCHEDULES = ("morning_evening", "extended_day", "evening")
OCCUPANCY = ("daytime", "morning_evening", "variable")
DISTRIBUTIONS = {
    "classification": "Every distribution and schedule is an exercise assumption.",
    "heating_schedule": "Equal probability morning_evening, extended_day, evening.",
    "occupancy_pattern": "Equal probability daytime, morning_evening, variable.",
    "setpoint_c": "Uniform [18,22]; outside heating schedule 16 C.",
    "ventilation_multiplier": "Uniform [0.8,1.2].",
    "occupied_moisture_hpa": "Uniform [0.8,1.6]; when absent 0.4 hPa.",
    "drying_increment_hpa": "Uniform [0.2,0.8] during one uniformly selected UTC hour.",
    "variable_occupancy": "Independent seeded Bernoulli(0.5) per UTC hour.",
    "schedule_hours_utc": "Heating 06-09/17-22, 07-23, 17-22;"
    " occupancy daytime 08-20 or morning/evening 06-09/17-23. Ends exclusive.",
    "interpretation": "Fictional variation, not resident assessment, blame"
    " or monitoring authority.",
}


@dataclass(frozen=True)
class Profile:
    heating_schedule: str
    occupancy_pattern: str
    setpoint_c: float
    ventilation_multiplier: float
    occupied_moisture_hpa: float
    drying_increment_hpa: float
    drying_hour_utc: int


@dataclass(frozen=True)
class Condition:
    home_id: str
    observed_at: datetime
    occupied: bool
    setpoint_c: float
    ventilation_multiplier: float
    moisture_increment_hpa: float
    source_type: str = "SYNTHETIC"
    model_version: str = VERSION


def _validate(home_id: str, seed: int, monitoring_consent: str, is_synthetic: bool) -> None:
    if (
        not isinstance(home_id, str)
        or not home_id
        or home_id != home_id.strip()
        or len(home_id.encode("utf-16-le")) // 2 > 128
        or any(ord(char) < 32 or ord(char) == 127 for char in home_id)
    ):
        raise ValueError("A nonblank stock home ID <=128 UTF-16 units is required")
    if type(seed) is not int or abs(seed) > 2**63 - 1:
        raise ValueError("Seed must be an integer with magnitude <=2^63-1")
    if monitoring_consent not in ("granted", "declined", "unknown"):
        raise ValueError("Monitoring choice must be granted, declined or unknown")
    if is_synthetic is not True:
        raise ValueError("Only explicitly synthetic fixture inputs are supported")


def profile(
    home_id: str, seed: int, monitoring_consent: str, *, is_synthetic: bool
) -> Profile | None:
    _validate(home_id, seed, monitoring_consent, is_synthetic)
    if monitoring_consent != "granted":
        return None
    rng = random.Random(f"{seed}-{VERSION}-{home_id}-profile")
    return Profile(
        rng.choice(SCHEDULES),
        rng.choice(OCCUPANCY),
        rng.uniform(18.0, 22.0),
        rng.uniform(0.8, 1.2),
        rng.uniform(0.8, 1.6),
        rng.uniform(0.2, 0.8),
        rng.randrange(24),
    )


def conditions(
    home_id: str,
    seed: int,
    monitoring_consent: str,
    timestamps: Sequence[datetime],
    *,
    is_synthetic: bool,
) -> tuple[Condition, ...]:
    """Produce canonical exercise conditions only for explicitly granted fixtures."""
    household = profile(home_id, seed, monitoring_consent, is_synthetic=is_synthetic)
    if household is None:
        return ()
    for at in timestamps:
        if not isinstance(at, datetime):
            raise ValueError("Condition timestamps must be UTC datetime values")
        offset = at.utcoffset()
        if offset is None or offset.total_seconds() != 0 or at.microsecond:
            raise ValueError("Condition timestamps must be UTC-aware whole seconds")
    if len(set(timestamps)) != len(timestamps):
        raise ValueError("Duplicate observation timestamps")
    result: list[Condition] = []
    for at in sorted(timestamps):
        hour = at.hour
        heating = {
            "morning_evening": 6 <= hour < 9 or 17 <= hour < 22,
            "extended_day": 7 <= hour < 23,
            "evening": 17 <= hour < 22,
        }[household.heating_schedule]
        if household.occupancy_pattern == "variable":
            occupied = (
                random.Random(f"{seed}-{VERSION}-{home_id}-occupancy-{at:%Y-%m-%dT%H}").random()
                < 0.5
            )
        elif household.occupancy_pattern == "daytime":
            occupied = 8 <= hour < 20
        else:
            occupied = 6 <= hour < 9 or 17 <= hour < 23
        moisture = household.occupied_moisture_hpa if occupied else 0.4
        if hour == household.drying_hour_utc:
            moisture += household.drying_increment_hpa
        result.append(
            Condition(
                home_id,
                at,
                occupied,
                household.setpoint_c if heating else 16.0,
                household.ventilation_multiplier,
                moisture,
            )
        )
    return tuple(result)
