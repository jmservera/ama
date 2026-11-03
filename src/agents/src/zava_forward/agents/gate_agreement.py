"""Apply an owner threshold agreement to the citation and refusal gate results.

A pure check. Without a complete record from a named owner, bound to the exact
graded and adversarial case set and a named independent grader, each gate stays
`unset_pending_owner_agreement` and the provisional development target is never
treated as agreed. Results are per check; there is no overall pass, and nothing
here approves a release, spend or source.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from math import isfinite
from typing import Any

GATES = ("citation_validity", "refusal_accuracy")
UNSET = "unset_pending_owner_agreement"


def _named(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _count(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def agreement_gaps(agreement: Mapping[str, Any] | None, case_set_sha256: str | None) -> list[str]:
    """Name every reason the agreement cannot be applied to this case set."""
    if not agreement:
        return ["no owner threshold agreement recorded"]
    gaps = [
        f"{key} not a named person"
        for key in ("owner", "independent_grader")
        if not _named(agreement.get(key))
    ]
    if _named(agreement.get("owner")) and agreement.get("owner") == agreement.get(
        "independent_grader"
    ):
        gaps.append("independent_grader must differ from owner")
    try:
        when = datetime.fromisoformat(str(agreement.get("agreed_on")))
    except ValueError:
        when = None
    if when is None:
        gaps.append("agreed_on not an ISO date")
    if not _named(agreement.get("case_set_sha256")):
        gaps.append("case_set_sha256 missing")
    elif agreement["case_set_sha256"] != case_set_sha256:
        gaps.append("agreement bound to a different case set")
    for key in ("min_graded_cases", "min_adversarial_cases"):
        if not _count(agreement.get(key)):
            gaps.append(f"{key} not a positive whole number")
    thresholds = agreement.get("min_rates")
    for gate in GATES:
        rate = thresholds.get(gate) if isinstance(thresholds, Mapping) else None
        if not (
            isinstance(rate, int | float)
            and not isinstance(rate, bool)
            and isfinite(rate)
            and 0 < rate <= 1
        ):
            gaps.append(f"min_rates.{gate} not a rate above 0 and at most 1")
    return gaps


def apply_owner_agreement(
    checks: Mapping[str, Mapping[str, Any]],
    *,
    case_set_sha256: str | None,
    graded_cases: int,
    adversarial_cases: int,
    agreement: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return one outcome per gate; unmet or unset is never reported as passed."""
    gaps = agreement_gaps(agreement, case_set_sha256)
    agreed = not gaps and agreement is not None
    results = []
    for gate in GATES:
        check = checks.get(gate, {})
        reasons = list(gaps)
        total, matched = check.get("total") or 0, check.get("matched") or 0
        if total == 0:
            reasons.append("gate not measured")
        if agreed and agreement is not None:
            if graded_cases < agreement["min_graded_cases"]:
                reasons.append("fewer graded cases than the agreed minimum")
            if adversarial_cases < agreement["min_adversarial_cases"]:
                reasons.append("fewer adversarial cases than the agreed minimum")
            if total and matched / total < agreement["min_rates"][gate]:
                reasons.append("measured rate below the agreed minimum")
            if check.get("failed_case_ids"):
                reasons.append("failed cases remain")
        results.append(
            dict(
                name=gate,
                status=UNSET
                if gaps
                else "owner_threshold_not_met"
                if reasons
                else "owner_threshold_met",
                matched=matched,
                total=total,
                rate=matched / total if total else None,
                reasons=reasons,
            )
        )
    return dict(
        checks=results,
        graded_cases=graded_cases,
        adversarial_cases=adversarial_cases,
        agreement=dict(status="owner_agreed" if agreed else UNSET, gaps=gaps),
        overall_pass=None,
        approval=(
            "Measurement against owner thresholds only; "
            "release, spend and sources stay with named owners."
        ),
    )
