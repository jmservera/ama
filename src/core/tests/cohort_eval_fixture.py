"""Constructed synthetic cohorts for the cohort evaluation; not fairness evidence."""

from __future__ import annotations

import copy
import itertools
from typing import Any

from zava_forward.core import cohort_eval

SOURCE = ("complete", "partial")
SUPPORT = ("none", "declared")
HISTORY = ("regular", "missed")


def manifest() -> dict[str, Any]:
    cases = []
    combos = itertools.product(SOURCE, SUPPORT, HISTORY)
    for n, (src, sup, hist) in enumerate((c for c in combos for _ in range(3)), start=1):
        cases.append(
            {
                "id": f"c{n:02d}",
                "cohorts": {
                    "source_completeness": src,
                    "support_need": sup,
                    "appointment_history": hist,
                },
                "expected": "review" if src == "partial" else "ranked",
            }
        )
    m = {
        "task_id": "ranking-v1",
        "subject_version": "ranking-policy-1",
        "synthetic": True,
        "missing_data_treatment": "partial sources route to human review, never exclusion",
        "cohorts": {
            "source_completeness": list(SOURCE),
            "support_need": list(SUPPORT),
            "appointment_history": list(HISTORY),
        },
        "thresholds": {
            "min_sample": 6,
            "max_error_rate": 0.1,
            "max_exclusion_gap": 0.1,
            "max_review_burden_gap": 1.0,
        },
        "justified_reasons": ["resident_opted_out"],
        "cases": cases,
        "seeded_defects": [],
    }
    return approved(m)


def approved(m: dict[str, Any]) -> dict[str, Any]:
    return cohort_eval.approve(
        m,
        {
            "cohorts_owner": "Data lead (fictional)",
            "lawful_fields_owner": "DPO (fictional)",
            "thresholds_owner": "RAI owner (fictional)",
        },
    )


def clean_observed(m: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"id": c["id"], "outcome": c["expected"]} for c in m["cases"]]


def seeded() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    m = copy.deepcopy(manifest())
    obs = clean_observed(m)
    by_id = {o["id"]: o for o in obs}
    by_id["c03"]["outcome"] = "excluded"
    by_id["c10"]["outcome"] = "deprioritised"
    m["seeded_defects"] = ["c03", "c10"]
    return approved(m), obs
