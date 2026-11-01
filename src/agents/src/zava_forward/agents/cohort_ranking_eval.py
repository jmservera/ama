"""Offline cohort and missing-data evaluation of the ranking policy (FR-054, AC-073, #222).

Paired constructed cohorts go through the real ``ranking.rank`` and the pure
``cohort_eval.evaluate``. Each pair is identical on every ranking input and differs in one
factor: sensor completeness, accessibility need, source completeness or appointment history.
Expected outcomes are an explicit, hand-stated rank order, not a call to the ranker.

Observed outcome per case: absent from the ranking is ``excluded``; ranked beyond its expected
position is ``deprioritised``; carrying the ``support_unknown`` reason is ``review``; otherwise
``ranked``. Seeded defects drop or demote chosen cases and must all be detected.

The manifest is a developer fixture, not owner approved (OQ-018). Without ``approved=True`` the
record stays blocked on unapproved thresholds; with it, the named owners are fictional. Results
on these synthetic cohorts are never fairness evidence.

Run: python3 -m zava_forward.agents.cohort_ranking_eval [--json] [--defects]
"""

import copy
import json
import sys
from typing import Any

from zava_forward.core import cohort_eval, ranking

Case = dict[str, Any]

STAGE = "Survey booked"
PAIRS = 6
BASELINE = {
    "sensor_completeness": "complete",
    "support_need": "none",
    "source_completeness": "complete",
    "appointment_history": "regular",
}
VARIANT = {
    "sensor_completeness": "partial",
    "support_need": "declared",
    "source_completeness": "partial",
    "appointment_history": "missed",
}
SEEDED_DROPPED = ("sensor-1-b", "sensor-4-b")
SEEDED_DEMOTED = ("history-2-b", "history-3-b")


def _resident(support_need: str, source: str) -> dict[str, Any]:
    if support_need == "declared":
        return {"adjustment": "Large print", "priority_support": False}
    if source == "partial":
        return {"adjustment": "Unknown", "priority_support": None}
    return {"adjustment": "None", "priority_support": False}


def _case(case_id: str, days: int, cohorts: dict[str, str]) -> Case:
    return {
        "id": case_id,
        "stage": STAGE,
        "days_in_stage": days,
        "hazards": [],
        "resident": _resident(cohorts["support_need"], cohorts["source_completeness"]),
        "cohorts": cohorts,
    }


def _units() -> list[list[tuple[str, dict[str, str]]]]:
    """Rank-ordered units: cases in one unit share every ranking input, so may swap by id."""

    def only(factor: str, name: str, i: int) -> list[tuple[str, dict[str, str]]]:
        base, var = dict(BASELINE), {**BASELINE, factor: VARIANT[factor]}
        return [(f"{name}-{i}-a", base), (f"{name}-{i}-b", var)]

    units = [[(f"access-yes-{i}", {**BASELINE, "support_need": "declared"})] for i in range(PAIRS)]
    for i in range(PAIRS):
        units.append([(f"access-no-{i}", dict(BASELINE))])
        units.append(only("sensor_completeness", "sensor", i))
        units.append(only("source_completeness", "source", i))
        units.append(only("appointment_history", "history", i))
    return units


def build() -> tuple[list[Case], dict[str, Any]]:
    """Return (cases fed to the ranker, manifest). Days are unique per unit, highest first."""
    cases: list[Case] = []
    manifest_cases: list[dict[str, Any]] = []
    position = 0
    units = _units()
    for u, unit in enumerate(units):
        position += len(unit)
        for case_id, cohorts in unit:
            cases.append(_case(case_id, 1000 - u, cohorts))
            partial_source = cohorts["source_completeness"] == "partial"
            manifest_cases.append(
                {
                    "id": case_id,
                    "cohorts": cohorts,
                    "expected": "review" if partial_source else "ranked",
                    "expected_rank_max": position,
                }
            )
    manifest = {
        "task_id": "ranking-policy",
        "subject_version": ranking.CURRENT["version"],
        "synthetic": True,
        "missing_data_treatment": "unknown support routes to human review, never exclusion or "
        "demotion; sensor completeness and appointment history do not change rank",
        "cohorts": {k: [BASELINE[k], VARIANT[k]] for k in BASELINE},
        "thresholds": {
            "min_sample": PAIRS,
            "max_error_rate": 0.1,
            "max_exclusion_gap": 0.1,
            "max_review_burden_gap": 1.0,
        },
        "justified_reasons": [],
        "cases": manifest_cases,
        "seeded_defects": [],
    }
    return cases, manifest


def _inject(cases: list[Case]) -> list[Case]:
    out = []
    for c in copy.deepcopy(cases):
        if c["id"] in SEEDED_DROPPED:
            continue
        if c["id"] in SEEDED_DEMOTED:
            c["days_in_stage"] = 1
        out.append(c)
    return out


def observe(cases: list[Case], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    ranked = {e["id"]: e for e in ranking.rank(cases, as_of="2026-11-01")}
    observed = []
    for m in manifest["cases"]:
        entry = ranked.get(m["id"])
        if entry is None:
            outcome = "excluded"
        elif entry["rank"] > m["expected_rank_max"]:
            outcome = "deprioritised"
        elif "support_unknown" in entry["reason_codes"]:
            outcome = "review"
        else:
            outcome = "ranked"
        observed.append({"id": m["id"], "outcome": outcome})
    return observed


def run(defects: bool = False, approved: bool = False) -> dict[str, Any]:
    cases, manifest = build()
    if approved:
        manifest["approval"] = {
            "cohorts_owner": "Data lead (fictional)",
            "thresholds_owner": "RAI owner (fictional)",
        }
    if defects:
        manifest["seeded_defects"] = sorted(SEEDED_DROPPED + SEEDED_DEMOTED)
        cases = _inject(cases)
    return dict(cohort_eval.evaluate(manifest, observe(cases, manifest)))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    record = run(defects="--defects" in args, approved="--approved" in args)
    if "--json" in args:
        print(json.dumps(record, indent=2))
        return 0
    print(f"status {record['status']}, activation allowed {record['activation_allowed']}")
    for dim, body in record["dimensions"].items():
        for label, row in body["cohorts"].items():
            print(
                f"{dim}/{label}: n={row['n']} errors={row['errors']} "
                f"sufficient={row['sufficient']} review_burden={row['review_burden']}"
            )
    print(f"seeded {record['seeded_defects']}, detected {record['detected_defects']}")
    for b in record["blockers"]:
        print(f"blocker {b['code']}: {b['detail']}")
    print(record["authority_gap"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
