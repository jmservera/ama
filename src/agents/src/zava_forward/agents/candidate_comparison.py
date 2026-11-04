"""Offline comparison of AI model, routing or caching candidates on the same cases.

Scores recorded per-proposal observations only. It reports cost per accepted
proposal beside quality, latency, refusal rate and token spread. A cheaper
candidate that raises critical misses, unsupported claims, overrides or
reopened cases, or drops a proposal the baseline had accepted, is a failure,
not a saving. Without a dated price source cost is Unknown. No price, budget or
target is set here and no outcome approves a model change or spend; scripted or
synthetic observations are not actual-model or human evidence.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime
from math import isfinite
from statistics import mean, pstdev
from typing import Any

PRICE_KEYS = ("id", "as_of", "currency", "input_per_million", "output_per_million")
BOOLS = ("accepted", "critical_miss", "unsupported_claim", "overridden", "reopened", "refused")
NUMBERS = ("latency_ms", "input_tokens", "output_tokens")
LEVERS = ("model", "routing", "caching", "prompt")
REGRESSIONS = (
    "critical_misses",
    "unsupported_claims",
    "overrides",
    "reopened_cases",
    "dropped_accepted_proposals",
)


def _number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and isfinite(value)


def invalid_observation(row: Mapping[str, Any]) -> str | None:
    """Return the reason a proposal observation cannot be scored, or None."""
    if not isinstance(row.get("case_id"), str) or not row["case_id"].strip():
        return "case_id missing"
    for key in BOOLS:
        if not isinstance(row.get(key), bool):
            return f"{key} not recorded as true or false"
    for key in NUMBERS:
        if not _number(row.get(key)) or row[key] < 0:
            return f"{key} not a non-negative number"
    return None


def _price_gaps(price: Mapping[str, Any] | None, now: datetime) -> list[str]:
    if not price:
        return ["no dated price source"]
    gaps = [f"price_source.{key} missing" for key in PRICE_KEYS if price.get(key) is None]
    if price.get("as_of") is not None:
        try:
            if date.fromisoformat(str(price["as_of"])) > now.date():
                gaps.append("price_source.as_of is in the future")
        except ValueError:
            gaps.append("price_source.as_of not an ISO date")
    for key in ("input_per_million", "output_per_million"):
        if price.get(key) is not None and not (_number(price[key]) and price[key] >= 0):
            gaps.append(f"price_source.{key} not a non-negative number")
    return gaps


def _tokens(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    totals = [row["input_tokens"] + row["output_tokens"] for row in rows]
    return dict(
        per_proposal_mean=mean(totals),
        per_proposal_min=min(totals),
        per_proposal_max=max(totals),
        per_proposal_stdev=pstdev(totals),
        input_total=sum(row["input_tokens"] for row in rows),
        output_total=sum(row["output_tokens"] for row in rows),
    )


def _cost(
    rows: Sequence[Mapping[str, Any]], price: Mapping[str, Any] | None, now: datetime
) -> dict[str, Any]:
    accepted = sum(1 for row in rows if row["accepted"])
    missing = _price_gaps(price, now)
    if accepted == 0:
        missing.append("no accepted proposals to divide by")
    result: dict[str, Any] = dict(
        cost="Unknown",
        cost_per_invocation="Unknown",
        cost_per_accepted_proposal="Unknown",
        missing_inputs=missing,
    )
    if missing or price is None:
        return result
    total = (
        sum(row["input_tokens"] for row in rows) * price["input_per_million"]
        + sum(row["output_tokens"] for row in rows) * price["output_per_million"]
    ) / 1_000_000
    result.update(
        cost=total,
        cost_per_invocation=total / len(rows),
        cost_per_accepted_proposal=total / accepted,
        currency=price["currency"],
        price_source_id=price["id"],
        price_as_of=price["as_of"],
    )
    return result


def _measure(candidate: Mapping[str, Any], now: datetime) -> dict[str, Any]:
    rows = candidate["observations"]
    latencies = [row["latency_ms"] for row in rows]
    count = len(rows)
    return dict(
        id=candidate["id"],
        proposals=count,
        accepted=sum(1 for row in rows if row["accepted"]),
        refusal_rate=sum(1 for row in rows if row["refused"]) / count,
        critical_misses=sum(1 for row in rows if row["critical_miss"]),
        unsupported_claims=sum(1 for row in rows if row["unsupported_claim"]),
        overrides=sum(1 for row in rows if row["overridden"]),
        reopened_cases=sum(1 for row in rows if row["reopened"]),
        latency_ms=dict(mean=mean(latencies), max=max(latencies)),
        tokens=_tokens(rows),
        economics=_cost(rows, candidate.get("price_source"), now),
        dropped_accepted_proposals=0,
    )


def _screen(candidate: Mapping[str, Any]) -> str | None:
    """Return why a candidate cannot be scored, or None."""
    rows = candidate.get("observations")
    if not isinstance(candidate.get("id"), str) or not candidate["id"].strip():
        return "candidate id missing"
    if not isinstance(rows, list) or not rows:
        return "no observations"
    for index, row in enumerate(rows):
        reason = invalid_observation(row) if isinstance(row, Mapping) else "not an object"
        if reason:
            return f"observation {index}: {reason}"
    ids = [row["case_id"] for row in rows]
    if len(set(ids)) != len(ids):
        return "duplicate case_id; one observation per held-out case"
    return None


def _verdict(measure: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    worse = [key for key in REGRESSIONS if measure[key] > base[key]]
    cheaper: bool | str = "Unknown"
    mine = measure["economics"]["cost_per_accepted_proposal"]
    theirs = base["economics"]["cost_per_accepted_proposal"]
    if mine != "Unknown" and theirs != "Unknown":
        cheaper = mine < theirs
    if worse:
        outcome = "failure"
        note = "raises " + ", ".join(worse) + " on the same cases; any lower cost is not a saving"
    elif cheaper == "Unknown":
        outcome = "no saving claimed"
        note = "cost per accepted proposal is Unknown for this candidate or the baseline"
    elif cheaper:
        outcome = "cheaper without a recorded regression"
        note = "observed on these cases only; not a held-out, actual-model or net-benefit claim"
    else:
        outcome = "not cheaper"
        note = "cost per accepted proposal is not below the baseline"
    return dict(outcome=outcome, regressions=worse, cheaper_per_accepted=cheaper, note=note)


def compare_candidates(
    baseline: Mapping[str, Any],
    candidates: Sequence[Mapping[str, Any]],
    now: datetime | None = None,
) -> dict[str, Any]:
    """Compare each candidate with the recorded baseline on the same case ids.

    A candidate states the single lever it changes (model, routing, caching or
    prompt) in ``changes``; any other shape is not comparable.
    """
    now = now or datetime.now(UTC)
    report: dict[str, Any] = dict(
        baseline=None,
        candidates=[],
        not_comparable=[],
        note="Offline accounting over recorded observations; "
        "no price, budget, target or approval is set or implied.",
    )
    reason = _screen(baseline)
    if reason:
        report["not_comparable"] = [
            dict(id=str(c.get("id")), reason=f"baseline invalid: {reason}") for c in candidates
        ]
        report["baseline"] = dict(id=str(baseline.get("id")), invalid=reason)
        return report
    base = _measure(baseline, now)
    report["baseline"] = base
    base_cases = {row["case_id"] for row in baseline["observations"]}
    base_accepted = {row["case_id"] for row in baseline["observations"] if row["accepted"]}
    for candidate in candidates:
        reason = _screen(candidate)
        changes = candidate.get("changes")
        if reason is None and not (
            isinstance(changes, list) and len(changes) == 1 and changes[0] in LEVERS
        ):
            reason = "changes must name exactly one lever: " + ", ".join(LEVERS)
        if reason is None and {row["case_id"] for row in candidate["observations"]} != base_cases:
            reason = "not measured on the same cases as the baseline"
        if reason:
            report["not_comparable"].append(dict(id=str(candidate.get("id")), reason=reason))
            continue
        measure = _measure(candidate, now)
        measure["dropped_accepted_proposals"] = sum(
            1
            for row in candidate["observations"]
            if row["case_id"] in base_accepted and not row["accepted"]
        )
        measure["lever"] = candidate["changes"][0]
        measure["verdict"] = _verdict(measure, base)
        report["candidates"].append(measure)
    return report
