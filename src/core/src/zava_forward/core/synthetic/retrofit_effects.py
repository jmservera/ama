"""Dated synthetic fabric-loss effects, not measured retrofit performance."""

import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

VERSION = "retrofit-effects-exercise-v1"
LOSS_MULTIPLIERS = {
    "Loft insulation": 0.90,
    "Cavity wall": 0.85,
    "Solid wall insulation": 0.80,
    "Glazing": 0.95,
}
PARAMETERS = {
    "version": VERSION,
    "classification": "All supported measures and multipliers are exercise values.",
    "equation": "effective_loss = baseline_loss * product(active measure multipliers)",
    "activation": "Matching stock home ID and observed_at >= recorded completion UTC instant.",
    "direction": "Lower fabric loss; not a guaranteed temperature or humidity improvement.",
    "unknown_measures": "Explicit error, never a silently invented effect.",
    "missing_history": "Empty history means no modelled step, not evidence that no works occurred.",
}


def _identifier(value: str, name: str) -> None:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value.encode("utf-16-le")) // 2 > 128
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise ValueError(f"{name} must be a nonblank stock-style identifier <=128 UTF-16 units")


def _utc(value: datetime) -> None:
    if not isinstance(value, datetime):
        raise ValueError("Timestamp must be a UTC datetime")
    offset = value.utcoffset()
    if offset is None or offset.total_seconds() != 0 or value.microsecond:
        raise ValueError("Timestamp must be UTC-aware with whole-second precision")


@dataclass(frozen=True)
class Measure:
    measure_id: str
    home_id: str
    kind: str
    completed_at: datetime
    is_synthetic: bool

    def __post_init__(self) -> None:
        _identifier(self.measure_id, "measure_id")
        _identifier(self.home_id, "home_id")
        if not isinstance(self.kind, str) or self.kind not in LOSS_MULTIPLIERS:
            raise ValueError("Unsupported exercise measure kind")
        _utc(self.completed_at)
        if self.is_synthetic is not True:
            raise ValueError("Only explicitly synthetic measure records are supported")


@dataclass(frozen=True)
class Effect:
    loss_multiplier: float
    active_measure_ids: tuple[str, ...]
    version: str = VERSION


def effect(home_id: str, observed_at: datetime, measures: Sequence[Measure]) -> Effect:
    """Evaluate explicit dated history; never infer measures from a boolean flag."""
    _identifier(home_id, "home_id")
    _utc(observed_at)
    if any(not isinstance(measure, Measure) for measure in measures):
        raise ValueError("Measure records must use the validated synthetic contract")
    ids = [measure.measure_id for measure in measures]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate measure IDs are ambiguous")
    active = sorted(
        (
            measure
            for measure in measures
            if measure.home_id == home_id and measure.completed_at <= observed_at
        ),
        key=lambda measure: (measure.completed_at, measure.measure_id),
    )
    multiplier = math.prod(LOSS_MULTIPLIERS[measure.kind] for measure in active)
    return Effect(float(multiplier), tuple(measure.measure_id for measure in active))


def apply_loss(
    baseline_loss: float, home_id: str, observed_at: datetime, measures: Sequence[Measure]
) -> float:
    if (
        type(baseline_loss) not in (int, float)
        or not math.isfinite(baseline_loss)
        or baseline_loss <= 0
    ):
        raise ValueError("Baseline exercise fabric loss must be finite and positive")
    return baseline_loss * effect(home_id, observed_at, measures).loss_multiplier
