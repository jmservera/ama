"""Offline comparison of the four model options on one shared test set (issue #219).

Options run from simplest to most complex: workflow-only, rule-cards, small-model,
large-model. Each is scored on the same cases for accuracy, safety, latency and
cost. The simplest option that meets every bar is selected. A tier with missing,
duplicate or mismatched cases, or with unknown cost under a cost bar, is not
eligible. No bar is set here; the caller supplies it, and no outcome approves a
model change or spend. Scripted or synthetic observations are not actual-model
or human evidence.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from math import ceil, isfinite
from typing import Any

OPTIONS = ("workflow-only", "rule-cards", "small-model", "large-model")


@dataclass(frozen=True)
class Bar:
    """Thresholds an option must meet. A None threshold is not applied."""

    min_accuracy: float
    max_unsafe_cases: int = 0
    max_p95_latency_ms: float | None = None
    max_cost_per_case: float | None = None


def _num(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and isfinite(value)


def invalid_observation(row: Mapping[str, Any]) -> str | None:
    """Return the reason an observation cannot be scored, or None."""
    case_id = row.get("case_id")
    if not isinstance(case_id, str) or not case_id.strip():
        return "case_id missing"
    for key in ("correct", "unsafe"):
        if not isinstance(row.get(key), bool):
            return f"{key} not recorded as true or false"
    latency = row.get("latency_ms")
    if not isinstance(latency, int | float) or not _num(latency) or latency < 0:
        return "latency_ms not a non-negative number"
    cost = row.get("cost")
    if cost is not None and (not isinstance(cost, int | float) or not _num(cost) or cost < 0):
        return "cost not a non-negative number or null"
    return None


def _p95(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[max(0, ceil(0.95 * len(ordered)) - 1)]


def _score(rows: Sequence[Mapping[str, Any]], case_ids: set[str], bar: Bar) -> dict[str, Any]:
    gaps: list[str] = []
    for row in rows:
        reason = invalid_observation(row)
        if reason:
            gaps.append(f"{row.get('case_id')!r}: {reason}")
    ids = [r.get("case_id") for r in rows]
    if gaps:
        return {"scored": False, "gaps": gaps, "meets_bar": False, "failures": ["invalid data"]}
    if len(ids) != len(set(ids)):
        gaps.append("duplicate case_id")
    if set(ids) != case_ids:
        gaps.append("cases differ from the shared test set")
    if gaps:
        return {"scored": False, "gaps": gaps, "meets_bar": False, "failures": ["invalid data"]}
    n = len(rows)
    accuracy = sum(r["correct"] for r in rows) / n
    unsafe = sum(r["unsafe"] for r in rows)
    p95 = _p95([float(r["latency_ms"]) for r in rows])
    costs = [r["cost"] for r in rows]
    cost_per_case = None if any(c is None for c in costs) else sum(costs) / n
    failures: list[str] = []
    if accuracy < bar.min_accuracy:
        failures.append("accuracy below bar")
    if unsafe > bar.max_unsafe_cases:
        failures.append("unsafe cases above bar")
    if bar.max_p95_latency_ms is not None and p95 > bar.max_p95_latency_ms:
        failures.append("p95 latency above bar")
    if bar.max_cost_per_case is not None:
        if cost_per_case is None:
            failures.append("cost unknown")
        elif cost_per_case > bar.max_cost_per_case:
            failures.append("cost above bar")
    return {
        "scored": True,
        "cases": n,
        "accuracy": accuracy,
        "unsafe_cases": unsafe,
        "p95_latency_ms": p95,
        "cost_per_case": cost_per_case,
        "gaps": [],
        "meets_bar": not failures,
        "failures": failures,
    }


def compare_options(
    observations: Mapping[str, Sequence[Mapping[str, Any]]], bar: Bar
) -> dict[str, Any]:
    """Score every option on the shared test set and select the simplest meeting the bar.

    The shared test set is the case ids of the first option with observations;
    every other option must cover exactly the same ids.
    """
    unknown = sorted(set(observations) - set(OPTIONS))
    if unknown:
        raise ValueError(f"unknown model option: {', '.join(unknown)}")
    if not (_num(bar.min_accuracy) and 0 <= bar.min_accuracy <= 1):
        raise ValueError("min_accuracy must be between 0 and 1")
    reference = next((observations[o] for o in OPTIONS if observations.get(o)), [])
    case_ids = {r["case_id"] for r in reference if isinstance(r.get("case_id"), str)}
    options = {
        o: _score(observations[o], case_ids, bar)
        if observations.get(o)
        else {"scored": False, "gaps": ["no observations"], "meets_bar": False, "failures": []}
        for o in OPTIONS
    }
    selected = next((o for o in OPTIONS if options[o]["meets_bar"]), None)
    return {
        "options": options,
        "selected": selected,
        "reason": (
            f"{selected} is the simplest option that meets the bar"
            if selected
            else "no option meets the bar; keep the current manual route"
        ),
    }
