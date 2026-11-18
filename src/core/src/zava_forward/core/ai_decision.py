"""Deterministic continue, narrow, pause or retire decision per AI feature (issue 222).

Each feature has explicit criteria for four dimensions: safety, accuracy, reviewer effort and
cost. A dimension maps its observed value to one of the four outcomes through ordered limits;
the feature outcome is the most severe dimension outcome. Missing, malformed, non-finite or
under-sampled evidence never yields `continue`: it yields `pause`, the safe default. Criteria
that are not approved by a named human are advisory and cannot authorise live reliance. The
module recommends only; a named accountable person decides and records the action.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

CONTINUE = "continue"
NARROW = "narrow"
PAUSE = "pause"
RETIRE = "retire"
OUTCOMES = (CONTINUE, NARROW, PAUSE, RETIRE)
DIMENSIONS = ("safety", "accuracy", "reviewer_effort", "cost")
# higher_is_worse: safety failures, reviewer minutes, cost; accuracy is a pass rate, lower is worse.
DIRECTIONS = {
    "safety": "higher_is_worse",
    "accuracy": "lower_is_worse",
    "reviewer_effort": "higher_is_worse",
    "cost": "higher_is_worse",
}
UNITS = {
    "safety": "critical failures",
    "accuracy": "pass rate 0..1",
    "reviewer_effort": "reviewer minutes per item",
    "cost": "cost per item",
}
LIMIT_KEYS = ("continue_limit", "narrow_limit", "pause_limit")
_RANK = {name: i for i, name in enumerate(OUTCOMES)}


def _num(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value) if math.isfinite(value) else None


def criteria_problems(criteria: Any) -> list[str]:
    """Why criteria are unusable; empty when every dimension has coherent ordered limits."""
    if not isinstance(criteria, Mapping):
        return ["criteria must be a mapping"]
    problems: list[str] = []
    min_n = criteria.get("min_samples")
    if isinstance(min_n, bool) or not isinstance(min_n, int) or min_n < 1:
        problems.append("min_samples must be a positive integer")
    for dim in DIMENSIONS:
        spec = criteria.get(dim)
        if not isinstance(spec, Mapping):
            problems.append(f"{dim}: missing")
            continue
        limits = [_num(spec.get(k)) for k in LIMIT_KEYS]
        if any(v is None for v in limits):
            problems.append(f"{dim}: continue_limit, narrow_limit and pause_limit must be numbers")
            continue
        a, b, c = (float(v) for v in limits if v is not None)
        ordered = a <= b <= c if DIRECTIONS[dim] == "higher_is_worse" else a >= b >= c
        if not ordered:
            problems.append(f"{dim}: limits must tighten from continue to pause")
        if dim == "accuracy" and not all(0.0 <= v <= 1.0 for v in (a, b, c)):
            problems.append("accuracy: limits must lie within 0..1")
        if dim != "accuracy" and a < 0:
            problems.append(f"{dim}: limits must not be negative")
        if dim == "safety" and a != 0:
            problems.append("safety: continue_limit must be 0 critical failures")
    return problems


def _band(dim: str, value: float, spec: Mapping[str, Any]) -> str:
    a, b, c = (float(spec[k]) for k in LIMIT_KEYS)
    if DIRECTIONS[dim] == "higher_is_worse":
        steps = (value <= a, value <= b, value <= c)
    else:
        steps = (value >= a, value >= b, value >= c)
    for outcome, ok in zip(OUTCOMES, steps, strict=False):
        if ok:
            return outcome
    return RETIRE


def evaluate(
    feature_id: str, criteria: Mapping[str, Any], observed: Mapping[str, Any]
) -> dict[str, Any]:
    """Recommend an outcome for one feature from its criteria and observed window values.

    `observed` holds `samples` plus one numeric value per dimension. The result lists every
    dimension with its value, outcome and reason; `decision` is the most severe outcome.
    """
    problems = criteria_problems(criteria)
    if problems:
        return {
            "feature_id": feature_id,
            "decision": PAUSE,
            "basis": "invalid-criteria",
            "dimensions": [],
            "problems": problems,
            "advisory": True,
        }
    samples = observed.get("samples") if isinstance(observed, Mapping) else None
    enough = isinstance(samples, int) and not isinstance(samples, bool)
    enough = enough and samples >= criteria["min_samples"]
    rows: list[dict[str, Any]] = []
    for dim in DIMENSIONS:
        value = _num(observed.get(dim)) if isinstance(observed, Mapping) else None
        if value is None:
            outcome, reason = PAUSE, "evidence missing or not a finite number"
        elif not enough:
            outcome, reason = PAUSE, "insufficient samples for a decision"
        elif dim == "accuracy" and not 0.0 <= value <= 1.0:
            outcome, reason = PAUSE, "pass rate outside 0..1"
        elif value < 0:
            outcome, reason = PAUSE, "negative value"
        else:
            outcome = _band(dim, value, criteria[dim])
            reason = f"{value:g} against {UNITS[dim]} limits"
        rows.append({"dimension": dim, "value": value, "outcome": outcome, "reason": reason})
    decision = max((r["outcome"] for r in rows), key=_RANK.__getitem__)
    approved = bool(criteria.get("approved_by")) and bool(criteria.get("approved_on"))
    return {
        "feature_id": feature_id,
        "decision": decision,
        "basis": "evidence" if enough else "insufficient-evidence",
        "dimensions": rows,
        "binding_dimensions": [r["dimension"] for r in rows if r["outcome"] == decision],
        "problems": [],
        "advisory": not approved,
        "note": "Recommendation only; a named accountable person decides and records the action.",
    }


def evaluate_all(
    criteria_by_feature: Mapping[str, Mapping[str, Any]],
    observed_by_feature: Mapping[str, Mapping[str, Any]],
    registered: tuple[str, ...] = (),
) -> dict[str, dict[str, Any]]:
    """One record per feature in sorted order; a registered feature without criteria is paused."""
    out: dict[str, dict[str, Any]] = {}
    for fid in sorted(set(criteria_by_feature) | set(registered)):
        criteria = criteria_by_feature.get(fid)
        if criteria is None:
            out[fid] = {
                "feature_id": fid,
                "decision": PAUSE,
                "basis": "no-criteria",
                "dimensions": [],
                "problems": ["no decision criteria defined for this feature"],
                "advisory": True,
            }
        else:
            out[fid] = evaluate(fid, criteria, observed_by_feature.get(fid, {}))
    return out
