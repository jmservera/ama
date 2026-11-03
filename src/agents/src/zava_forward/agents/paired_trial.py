"""Paired staff trial scoring: chat versus deterministic rule cards with provision links.

Scores observations only. Missing, invalid or unthresholded evidence keeps the
cards-only recommendation; no outcome here approves shipment or spend.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime
from math import isfinite
from typing import Any

from zava_forward.agents.regulatory_gates import OWNER, authorise_model_run

ARMS = ("cards", "chat")
ROLES = ("repairs", "housing", "grants")
BOOLS = ("completed", "comprehension_correct", "accepted", "hazard_missed")
SECONDS = ("elapsed_seconds", "review_seconds")
THRESHOLD_KEYS = (
    "owner",
    "agreed_on",
    "min_pairs_per_role",
    "min_completion_gain",
    "min_comprehension_gain",
    "max_elapsed_ratio",
)
PRICE_KEYS = ("id", "as_of", "currency", "input_per_million", "output_per_million")
COST_INPUTS = (
    "accepted_check_definition",
    "price_source",
    "allocation_basis",
    "usage",
    "authority",
)
USAGE_KEYS = ("model_calls", "input_tokens", "output_tokens")


def _number(value: Any) -> bool:
    return isinstance(value, int | float) and not isinstance(value, bool) and isfinite(value)


def valid_observation(row: Mapping[str, Any]) -> str | None:
    """Return the reason an observation cannot be scored, or None."""
    for key in ("participant", "task"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            return f"{key} missing"
    if row.get("role") not in ROLES:
        return "role not repairs, housing or grants"
    if row.get("arm") not in ARMS:
        return "arm not cards or chat"
    for key in BOOLS:
        if not isinstance(row.get(key), bool):
            return f"{key} not recorded as true or false"
    for key in SECONDS:
        if not _number(row.get(key)) or row[key] < 0:
            return f"{key} not a non-negative number"
    return None


def _rate(rows: list[Mapping[str, Any]], key: str) -> float:
    return sum(1 for row in rows if row[key]) / len(rows)


def _mean(rows: list[Mapping[str, Any]], key: str) -> float:
    return float(sum(row[key] for row in rows)) / len(rows)


def _pairs(rows: list[Mapping[str, Any]]) -> tuple[list[tuple[Any, Any]], list[str]]:
    by_key: dict[tuple[str, str], dict[str, list[Mapping[str, Any]]]] = {}
    for row in rows:
        by_key.setdefault((row["participant"], row["task"]), {}).setdefault(row["arm"], []).append(
            row
        )
    pairs, unpaired = [], []
    for (participant, task), arms in sorted(by_key.items()):
        if len(arms.get("cards", [])) == 1 and len(arms.get("chat", [])) == 1:
            pairs.append((arms["cards"][0], arms["chat"][0]))
        else:
            unpaired.append(f"{participant}/{task}")
    return pairs, unpaired


def _measure(pairs: list[tuple[Any, Any]]) -> dict[str, Any]:
    cards, chat = [p[0] for p in pairs], [p[1] for p in pairs]
    return dict(
        pairs=len(pairs),
        completion_gain=_rate(chat, "completed") - _rate(cards, "completed"),
        comprehension_gain=_rate(chat, "comprehension_correct")
        - _rate(cards, "comprehension_correct"),
        elapsed_ratio=_mean(chat, "elapsed_seconds") / _mean(cards, "elapsed_seconds")
        if _mean(cards, "elapsed_seconds") > 0
        else None,
        chat_review_seconds=_mean(chat, "review_seconds"),
        cards_review_seconds=_mean(cards, "review_seconds"),
        chat_accepted=sum(1 for row in chat if row["accepted"]),
        cards_accepted=sum(1 for row in cards if row["accepted"]),
    )


def _threshold_gaps(thresholds: Mapping[str, Any] | None) -> list[str]:
    if not thresholds:
        return ["no owner-agreed thresholds recorded"]
    gaps = [f"{key} missing" for key in THRESHOLD_KEYS if thresholds.get(key) is None]
    owner = thresholds.get("owner")
    if owner is not None and (not isinstance(owner, str) or not owner.strip()):
        gaps.append("owner not a named person")
    try:
        datetime.fromisoformat(str(thresholds.get("agreed_on")))
    except ValueError:
        gaps.append("agreed_on not an ISO date")
    for key in THRESHOLD_KEYS[2:]:
        if thresholds.get(key) is not None and not (
            _number(thresholds[key]) and thresholds[key] >= 0
        ):
            gaps.append(f"{key} not a non-negative number")
    return gaps


def cost_per_accepted_check(
    accepted: int, cost_inputs: Mapping[str, Any] | None, now: datetime
) -> dict[str, Any]:
    """AI cost per accepted chat check, or Unknown with every missing input named."""
    inputs = cost_inputs or {}
    missing = [f"{key} missing" for key in COST_INPUTS if not inputs.get(key)]
    if accepted <= 0:
        missing.append("no human-accepted chat checks to divide by")
    price, usage = inputs.get("price_source") or {}, inputs.get("usage") or {}
    missing += [f"price_source.{key} missing" for key in PRICE_KEYS if price.get(key) is None]
    missing += [f"usage.{key} missing" for key in USAGE_KEYS if usage.get(key) is None]
    cost: float | None = None
    if not missing:
        try:
            cost = (
                usage["input_tokens"] * price["input_per_million"]
                + usage["output_tokens"] * price["output_per_million"]
            ) / 1_000_000
        except TypeError:
            missing.append("price or usage values not numeric")
    result: dict[str, Any] = dict(
        cost="Unknown",
        ai_cost_per_accepted_check="Unknown",
        missing_inputs=missing,
        accepted_checks=accepted,
        note="No price, budget or spend authority is set or implied here.",
    )
    if missing or cost is None:
        return result
    decision = authorise_model_run(
        inputs["authority"],
        dict(
            model_calls=usage["model_calls"],
            tokens=usage["input_tokens"] + usage["output_tokens"],
            budget=cost,
        ),
        now,
    )
    result["authority_decision"] = decision
    if decision["allowed"]:
        result.update(
            cost=cost,
            ai_cost_per_accepted_check=cost / accepted,
            currency=price["currency"],
            price_source_id=price["id"],
            price_as_of=price["as_of"],
        )
    else:
        result["missing_inputs"] = ["authority did not cover the recorded usage"]
    return result


def evaluate_paired_trial(
    observations: Iterable[Mapping[str, Any]],
    *,
    thresholds: Mapping[str, Any] | None = None,
    cost_inputs: Mapping[str, Any] | None = None,
    now: datetime,
) -> dict[str, Any]:
    """Score a staff trial per check; chat ships alone only after measured, owner-agreed value."""
    valid, invalid = [], []
    for index, row in enumerate(observations):
        reason = valid_observation(row)
        (invalid.append(dict(index=index, reason=reason)) if reason else valid.append(row))
    pairs, unpaired = _pairs(valid)
    gaps = _threshold_gaps(thresholds)
    per_role: dict[str, Any] = {}
    for role in ROLES:
        role_pairs = [pair for pair in pairs if pair[0]["role"] == role]
        per_role[role] = (
            _measure(role_pairs) if role_pairs else dict(pairs=0, status="not_evaluated")
        )
    chat_rows = [pair[1] for pair in pairs]
    misses = [row["participant"] + "/" + row["task"] for row in chat_rows if row["hazard_missed"]]
    hazard = dict(
        name="chat_hazard_misses",
        misses=len(misses),
        failed_case_ids=misses,
        failure_severity="critical",
        status="not_evaluated" if not chat_rows else "failed" if misses else "no_misses_observed",
    )
    reasons = list(gaps)
    if invalid or unpaired:
        reasons.append("invalid or unpaired observations excluded; trial must be repaired")
    if misses:
        reasons.append("a chat hazard miss is critical")
    if not gaps and thresholds:
        for role, found in per_role.items():
            if not found["pairs"] or found["pairs"] < thresholds["min_pairs_per_role"]:
                reasons.append(f"{role}: fewer than the agreed minimum pairs")
                continue
            ratio = found["elapsed_ratio"]
            if found["completion_gain"] < thresholds["min_completion_gain"]:
                reasons.append(f"{role}: completion gain below agreed threshold")
            if found["comprehension_gain"] < thresholds["min_comprehension_gain"]:
                reasons.append(f"{role}: comprehension gain below agreed threshold")
            if ratio is None or ratio > thresholds["max_elapsed_ratio"]:
                reasons.append(f"{role}: elapsed time above agreed ratio")
    accepted = sum(1 for row in chat_rows if row["accepted"])
    value_measured = not reasons
    return dict(
        check="paired_staff_comparison",
        status="measured" if pairs else "not_evaluated",
        baseline="same role-scoped deterministic cards with provision links",
        pairs=len(pairs),
        per_role=per_role,
        invalid_observations=invalid,
        unpaired=unpaired,
        hazard_misses=hazard,
        threshold=dict(
            value=dict(thresholds) if not gaps and thresholds else None,
            status="owner_agreed" if not gaps else "unset_pending_owner_agreement",
            gaps=gaps,
            owner=OWNER,
        ),
        economics=cost_per_accepted_check(accepted, cost_inputs, now),
        ship_recommendation="chat_value_measured_owner_decision_required"
        if value_measured
        else "cards_only",
        reasons=reasons,
        approval="Recommendation only; shipment, spend and source approval stay with named owners.",
    )
