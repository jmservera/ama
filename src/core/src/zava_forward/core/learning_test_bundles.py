"""Net-effort comparison for the five journey learning-test bundles (#129, NFR-009).

Deterministic and pure: it sums recorded effort minutes per arm, reports the median and range,
applies each bundle's stop rule to its "target zero" counts and labels saved minutes as capacity.
It runs no experiment, uses no AI and holds no representative data; inputs are constructed cases.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Any

COMPONENTS = (
    "preparation",
    "checking",
    "correction",
    "coordination",
    "resident_effort",
    "support_cost",
)
ARMS = ("comparator", "workflow")
OUT_OF_SCOPE = frozenset({"O10", "O18", "O19", "O20"})
EVIDENCE_LABEL = "constructed-case evidence"
CAPACITY_NOTE = "Saved minutes are capacity until Finance validates them; not cash or benefit."


@dataclass(frozen=True)
class Bundle:
    key: str
    atlas_ids: tuple[str, ...]
    comparator: str
    zero_measures: tuple[str, ...]


BUNDLES: dict[str, Bundle] = {
    b.key: b
    for b in (
        Bundle(
            "story-once",
            ("O01", "O02", "O03", "O15"),
            "Manual re-asking and chase log",
            ("authority_or_consent_breaches", "promises_without_owner"),
        ),
        Bundle(
            "pre-visit-pack",
            ("O06", "O08", "O09"),
            "Current visit preparation",
            ("offers_misread_as_commitments",),
        ),
        Bundle(
            "change-impact",
            ("O07", "O16"),
            "Manual dependency check",
            ("approvals_wrongly_carried_over",),
        ),
        Bundle(
            "handover-aftercare",
            ("O13", "O14"),
            "Paper handover",
            ("open_remedies_hidden",),
        ),
        Bundle(
            "funding-evidence",
            ("O16", "O17"),
            "Manual evidence pack",
            ("inferred_submissions",),
        ),
    )
}


def case_net_effort(efforts: dict[str, float]) -> float:
    """Sum all six components; a missing or negative component is rejected, not defaulted."""
    unknown = set(efforts) - set(COMPONENTS)
    missing = [c for c in COMPONENTS if c not in efforts]
    if unknown or missing:
        raise ValueError(f"Effort needs exactly {', '.join(COMPONENTS)}.")
    if any(v < 0 for v in efforts.values()):
        raise ValueError("Effort minutes cannot be negative.")
    return float(sum(efforts.values()))


def _summary(totals: list[float]) -> dict[str, Any]:
    return {
        "cases": len(totals),
        "median_minutes": statistics.median(totals),
        "min_minutes": min(totals),
        "max_minutes": max(totals),
    }


def compare_bundle(bundle_key: str, cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare the arms of one bundle over the same constructed cases.

    Each case is ``{"case": id, "arms": {arm: {"effort": {...}, "counts": {...}}}}``.
    """
    bundle = BUNDLES.get(bundle_key)
    if bundle is None:
        raise ValueError(f"Unknown bundle {bundle_key!r}.")
    if OUT_OF_SCOPE & set(bundle.atlas_ids):
        raise ValueError("Out-of-scope opportunities cannot be tested.")
    if not cases:
        raise ValueError("At least one constructed case is required.")
    totals: dict[str, list[float]] = {arm: [] for arm in ARMS}
    breaches: list[str] = []
    for case in cases:
        arms = case.get("arms", {})
        if set(arms) != set(ARMS):
            raise ValueError("Every case needs both arms on the same case.")
        for arm in ARMS:
            data = arms[arm]
            totals[arm].append(case_net_effort(data["effort"]))
            counts = data.get("counts", {})
            for measure in bundle.zero_measures:
                if counts.get(measure) is None:
                    raise ValueError(f"Missing count {measure} for {arm}.")
                if counts[measure] != 0:
                    breaches.append(f"{case.get('case')}/{arm}/{measure}")
    comp, flow = _summary(totals["comparator"]), _summary(totals["workflow"])
    delta = flow["median_minutes"] - comp["median_minutes"]
    return {
        "bundle": bundle_key,
        "comparator_description": bundle.comparator,
        "evidence_label": EVIDENCE_LABEL,
        "comparator": comp,
        "workflow": flow,
        "median_difference_minutes": delta,
        "direction": "workflow lower" if delta < 0 else "comparator lower or equal",
        "stop": bool(breaches),
        "breaches": breaches,
        "capacity_note": CAPACITY_NOTE,
        "assistance_note": "Assistance not available is a valid arm; manual path stays complete.",
    }
