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


O16_BUNDLES = tuple(b.key for b in BUNDLES.values() if "O16" in b.atlas_ids)


def run_report(run: dict[str, Any]) -> dict[str, Any]:
    """Validate a recorded run's metadata, then compare its arms.

    A run is ``{"bundle", "o16_counted_under", "representative_data_retained", "cases"}``.
    ``o16_counted_under`` is required for bundles that share O16 so effort is counted once.
    """
    bundle = BUNDLES.get(str(run.get("bundle")))
    if bundle is None:
        raise ValueError(f"Unknown bundle {run.get('bundle')!r}.")
    if run.get("representative_data_retained") is not False:
        raise ValueError("State representative_data_retained as false; retention awaits the DPO.")
    owner = run.get("o16_counted_under")
    if "O16" in bundle.atlas_ids and owner not in O16_BUNDLES:
        raise ValueError(f"State which bundle counts O16: {', '.join(O16_BUNDLES)}.")
    if "O16" not in bundle.atlas_ids and owner is not None:
        raise ValueError("o16_counted_under applies only to bundles that include O16.")
    report = compare_bundle(bundle.key, run.get("cases", []))
    report["o16_counted_under"] = owner
    return report


def reconcile_o16(runs: list[dict[str, Any]]) -> str | None:
    """Return the single bundle that counts O16 across runs; reject conflicting claims."""
    owners: set[str] = set()
    for r in runs:
        bundle = BUNDLES.get(str(r.get("bundle")))
        if bundle is None:
            raise ValueError(f"Unknown bundle {r.get('bundle')!r}.")
        owner = r.get("o16_counted_under")
        if "O16" in bundle.atlas_ids:
            if owner not in O16_BUNDLES:
                raise ValueError(f"State which bundle counts O16: {', '.join(O16_BUNDLES)}.")
            owners.add(owner)
        elif owner is not None:
            raise ValueError("o16_counted_under applies only to bundles that include O16.")
    if len(owners) > 1:
        raise ValueError(
            "Runs disagree on which bundle counts O16; effort would be double counted."
        )
    return next(iter(owners), None)


def render_report(report: dict[str, Any]) -> str:
    """Plain-language text for a facilitator; a stop is stated before any effort figure."""
    lines = [f"Bundle: {report['bundle']} (comparator: {report['comparator_description']})"]
    if report["stop"]:
        lines.append("STOP: " + ", ".join(report["breaches"]) + " (target zero).")
    else:
        lines.append("Stop rule: no breach recorded.")
    for arm in ARMS:
        s = report[arm]
        lines.append(
            f"{arm}: {s['cases']} cases, median {s['median_minutes']:g} min, "
            f"range {s['min_minutes']:g} to {s['max_minutes']:g} min"
        )
    lines += [
        "Median difference (workflow minus comparator): "
        f"{report['median_difference_minutes']:g} min ({report['direction']}).",
        f"Evidence: {report['evidence_label']}.",
        report["capacity_note"],
        report["assistance_note"],
    ]
    if report.get("o16_counted_under"):
        lines.append(f"O16 counted under: {report['o16_counted_under']}.")
    return "\n".join(lines)
