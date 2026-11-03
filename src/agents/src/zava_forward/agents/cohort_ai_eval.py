"""Offline cohort and missing-data evaluation of the AI priority recommendation (#222).

The same paired constructed cohorts as ``cohort_ranking_eval`` go through the real
``Store.ai_priority`` task with a scripted provider, in groups of ten cases (the task's
maximum). Cases keep their expected order, so each pair stays in one group.

Modes:

* ``faithful``: the scripted model returns the deterministic order.
* ``biased``: negative control; the scripted model silently drops cases, which must be detected
  as unjustified exclusions.
* ``unavailable``: no model, the task falls back and the deterministic ranking is the manual
  path. Every group must record a fallback reason and leave the ranking unchanged.

The manifest is a developer fixture, not owner approved (OQ-018); the runner never supplies
approval, so the record stays blocked. Synthetic results are never fairness evidence.

Run: python3 -m zava_forward.agents.cohort_ai_eval [--json] [--biased | --unavailable]
"""

import copy
import json
import os
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from zava_forward.core import ai_prompts, cohort_eval, ranking
from zava_forward.core.store import Store

from zava_forward.agents import ai_eval, cohort_ranking_eval

GROUP = 10
MODES = ("faithful", "biased", "unavailable")
DROPPED = ("sensor-1-b", "source-2-b", "history-3-b")
Case = dict[str, Any]
harness: Any = ai_eval  # the offline harness is untyped


def _store_case(case: Case) -> Case:
    built: Case = harness.build_case({"id": case["id"], "days": case["days_in_stage"]})
    built["stage"] = case["stage"]
    built["resident"] = {**built["resident"], **case["resident"]}
    return built


def _model_output(group: list[Case], mode: str) -> str | None:
    if mode == "unavailable":
        return None
    kept = [c for c in group if not (mode == "biased" and c["id"] in DROPPED)]
    return json.dumps(
        [
            {
                "case_id": c["id"],
                "reason": "Waiting time and declared support need.",
                "cites": [f"Days in stage: {c['days_in_stage']}"],
            }
            for c in kept
        ]
    )


def _group_rows(group: list[Case], mode: str, workdir: str) -> list[dict[str, Any]]:
    data = {"staff": [harness.OWNER, harness.OTHER], "cases": [_store_case(c) for c in group]}
    path = Path(workdir) / "eval.json"
    path.write_text(json.dumps(data))
    store = Store(
        str(path), os.path.join(workdir, "live.json"), os.path.join(workdir, "audit.jsonl")
    )
    output = _model_output(group, mode)
    harness._scripted(store, None if output is None else [output])
    before = {i: e["rank"] for i, e in store._ranking().items()}
    rec = store.ai_priority(harness.OWNER, len(group))
    if {i: e["rank"] for i, e in store._ranking().items()} != before:
        raise AssertionError("the AI task changed the deterministic ranking")
    if rec["status"] != "Proposed":
        raise AssertionError("the AI recommendation must stay Proposed")
    if mode == "unavailable":
        if rec["source"] != "template" or not rec["fallback_reason"]:
            raise AssertionError("AI unavailable must fall back with a reason")
        order = [i for i, _ in sorted(before.items(), key=lambda kv: kv[1])]
    else:
        order = [i["case_id"] for i in rec["items"]]
    entries = store._ranking()
    return [{"id": i, "reason_codes": list(entries[i]["reason_codes"])} for i in order]


def make_rank_fn(mode: str) -> Callable[[list[Case]], list[dict[str, Any]]]:
    def rank_fn(cases: list[Case]) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for start in range(0, len(cases), GROUP):
            with tempfile.TemporaryDirectory() as tmp:
                rows += _group_rows(cases[start : start + GROUP], mode, tmp)
        return [{**row, "rank": pos} for pos, row in enumerate(rows, 1)]

    return rank_fn


def _run(mode: str, approval: dict[str, str] | None = None) -> dict[str, Any]:
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    cases, manifest = cohort_ranking_eval.build()
    manifest["task_id"] = "ai-priority-recommendation"
    manifest["subject_version"] = (
        f"{ranking.CURRENT['version']}+prompt-{ai_prompts.version('priority')}"
    )
    manifest["missing_data_treatment"] = (
        "the recommendation may not drop or demote a case for missing sensor, source or "
        "appointment data; unknown support stays a human-review flag from the ranking"
    )
    if mode == "biased":
        manifest["seeded_defects"] = sorted(DROPPED)
    manifest["inputs"] = copy.deepcopy(cases)
    if approval:
        cohort_eval.approve(manifest, approval)
    return dict(
        cohort_eval.evaluate(
            manifest, cohort_ranking_eval.observe(cases, manifest, make_rank_fn(mode))
        )
    )


def run(mode: str = "faithful") -> dict[str, Any]:
    """Evaluate the developer fixture; it never carries approval, so activation stays blocked."""
    return _run(mode)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    mode = (
        "biased" if "--biased" in args else "unavailable" if "--unavailable" in args else "faithful"
    )
    record = run(mode)
    if "--json" in args:
        print(json.dumps(record, indent=2))
        return 0
    print(
        f"AI priority task, mode {mode} (synthetic): status {record['status']}, "
        f"activation allowed {record['activation_allowed']}"
    )
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
