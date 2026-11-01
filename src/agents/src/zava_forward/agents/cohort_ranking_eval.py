"""Offline cohort and missing-data evaluation of the ranking policy (FR-054, AC-073, #222).

Paired constructed cohorts go through the real ``ranking.rank`` and the pure
``cohort_eval.evaluate``. Each pair is identical on every ranking input and differs in one
factor: sensor completeness, accessibility need, source completeness or appointment history.
Expected outcomes are an explicit, hand-stated rank order, not a call to the ranker.

Observed outcome per case: absent from the ranking is ``excluded``; ranked beyond its expected
position is ``deprioritised``; carrying the ``support_unknown`` reason is ``review``; otherwise
``ranked``. Seeded defects drop or demote chosen cases and must all be detected.

The manifest is a developer fixture, not owner approved (OQ-018). The runner never supplies
approval, so the record stays blocked on unapproved thresholds. Tests alone add a fictional
approval (``_run``) to exercise evaluator mechanics. Results on these synthetic cohorts are
never fairness evidence.

Run: python3 -m zava_forward.agents.cohort_ranking_eval [--json] [--defects]
"""

import copy
import json
import sys
from collections import Counter
from collections.abc import Callable
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
MOCK_APPROVAL = {
    "cohorts_owner": "Data lead (fictional)",
    "thresholds_owner": "RAI owner (fictional)",
}
# Ranking-neutral fields carried so a ranker that reads them is exercised.
SENSOR = {"complete": "present", "partial": "missing"}
SOURCE = {"complete": "complete", "partial": "stale"}
HISTORY = {"regular": "regular", "missed": "prior_no_access"}
ACCESS_DAYS = 100
Ranker = Callable[[list[Case]], list[dict[str, Any]]]


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
        "sensor_data": SENSOR[cohorts["sensor_completeness"]],
        "source_record": SOURCE[cohorts["source_completeness"]],
        "appointment_history": HISTORY[cohorts["appointment_history"]],
        "cohorts": cohorts,
    }


Unit = tuple[int, list[tuple[str, dict[str, str]]]]


def _units() -> list[Unit]:
    """Rank-ordered units of (days, cases). Cases in one unit share every ranking input.

    Declared-support cases and their no-support partners share the same low waiting days, so
    only the support rule puts the declared cases first; a ranker without it moves them last.
    """

    def only(factor: str, name: str, i: int) -> list[tuple[str, dict[str, str]]]:
        base, var = dict(BASELINE), {**BASELINE, factor: VARIANT[factor]}
        return [(f"{name}-{i}-a", base), (f"{name}-{i}-b", var)]

    declared = {**BASELINE, "support_need": "declared"}
    units: list[Unit] = [(ACCESS_DAYS - i, [(f"access-yes-{i}", declared)]) for i in range(PAIRS)]
    rows = 0
    for i in range(PAIRS):
        for factor, name in (
            ("sensor_completeness", "sensor"),
            ("source_completeness", "source"),
            ("appointment_history", "history"),
        ):
            units.append((1000 - 10 * rows, only(factor, name, i)))
            rows += 1
    units += [(ACCESS_DAYS - i, [(f"access-no-{i}", dict(BASELINE))]) for i in range(PAIRS)]
    return units


def build() -> tuple[list[Case], dict[str, Any]]:
    """Return (cases fed to the ranker, manifest)."""
    cases: list[Case] = []
    manifest_cases: list[dict[str, Any]] = []
    position = 0
    for days, unit in _units():
        position += len(unit)
        for case_id, cohorts in unit:
            cases.append(_case(case_id, days, cohorts))
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


def observe(
    cases: list[Case], manifest: dict[str, Any], rank_fn: Ranker | None = None
) -> list[dict[str, Any]]:
    """Compare precedence among retained cases, so an exclusion cannot hide a demotion."""
    rows = list((rank_fn or _rank)(cases))
    raw = [
        e
        for e in rows
        if isinstance(e, dict)
        and isinstance(e.get("id"), str)
        and isinstance(e.get("reason_codes"), (list, tuple))
    ]
    bad_rows = [f"malformed-row:{i}" for i, e in enumerate(rows, 1) if e not in raw]
    ranked = {e["id"]: e for e in raw}
    manifest_ids = {m["id"] for m in manifest["cases"]}
    stray = [e["id"] for e in raw if e["id"] not in manifest_ids]
    repeated = [i for i, n in Counter(e["id"] for e in raw).items() if n > 1 and i in manifest_ids]
    retained = [m for m in manifest["cases"] if m["id"] in ranked]
    bad_ranks = [
        f"malformed-rank:{e['id']}"
        for pos, e in enumerate(raw, 1)
        if type(e.get("rank")) is not int or e["rank"] != pos
    ]
    observed = []
    for m in manifest["cases"]:
        entry = ranked.get(m["id"])
        if entry is None:
            outcome = "excluded"
        else:
            overtaken = not bad_ranks and any(
                r["expected_rank_max"] > m["expected_rank_max"]
                and ranked[r["id"]]["rank"] < entry["rank"]
                for r in retained
            )
            if overtaken:
                outcome = "deprioritised"
            elif "support_unknown" in entry["reason_codes"]:
                outcome = "review"
            else:
                outcome = "ranked"
        row = {"id": m["id"], "outcome": outcome}
        if entry is not None and "support_unknown" in entry["reason_codes"]:
            row["review_required"] = True
        observed.append(row)
    # Malformed ranker output stays visible so the evaluator blocks on it.
    observed += [{"id": i, "outcome": "ranked"} for i in stray + repeated + bad_ranks + bad_rows]
    return observed


def _rank(cases: list[Case]) -> list[dict[str, Any]]:
    return list(ranking.rank(cases, as_of="2026-11-01"))


def _run(
    defects: bool = False, rank_fn: Ranker | None = None, approval: dict[str, str] | None = None
) -> dict[str, Any]:
    cases, manifest = build()
    if approval:
        manifest["approval"] = dict(approval)
    if defects:
        manifest["seeded_defects"] = sorted(SEEDED_DROPPED + SEEDED_DEMOTED)
        cases = _inject(cases)
    manifest["inputs"] = copy.deepcopy(cases)
    return dict(cohort_eval.evaluate(manifest, observe(cases, manifest, rank_fn)))


def run(defects: bool = False, rank_fn: Ranker | None = None) -> dict[str, Any]:
    """Evaluate the developer fixture; it never carries approval, so activation stays blocked."""
    return _run(defects, rank_fn)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    record = run(defects="--defects" in args)
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
