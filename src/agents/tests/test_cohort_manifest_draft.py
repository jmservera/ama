"""Structural checks for the DRAFT cohort manifest (#222). Not an evaluation.

Reads only the committed synthetic JSON and the registry. It proves the draft stays
labelled unapproved and internally consistent; it runs no model and approves nothing.
"""

import json
import math
import re
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import ranking

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "src/agents/evals/cohort_manifest_draft.json"
TEXT = PATH.read_text(encoding="utf-8")
M = json.loads(TEXT)
REG = json.loads((ROOT / "src/agents/evals/registry.json").read_text(encoding="utf-8"))

# The support exemption exists only because a support_state pair changes the derived support
# flag and the adjustment text that feed it; no other factor may change them.
SUPPORT_STATE_EXTRAS = {"support", "adjustment"}


def isolation_violations(scenario: dict[str, Any]) -> set[str]:
    """Fields that differ in a pair beyond its declared varied factor."""
    base, var = scenario["baseline"], scenario["variant"]
    differing = {k for k in set(base) | set(var) if k != "id" and base.get(k) != var.get(k)}
    factors = set(scenario["varied_factor"].split("_and_"))
    allowed = factors | (SUPPORT_STATE_EXTRAS if factors == {"support_state"} else set())
    return (factors - differing) | (differing - allowed)


def _case(
    case_id: str,
    days: int,
    support_state: str = "No",
    hazard: bool = False,
    adjustment: str | None = None,
) -> dict[str, Any]:
    resident = {
        "Yes": {
            "priority_support": adjustment in (None, "None"),
            "adjustment": adjustment or "None",
        },
        "No": {"priority_support": False, "adjustment": "None"},
        "Unknown": {"priority_support": None, "adjustment": None},
    }[support_state]
    return {
        "id": case_id,
        "stage": ranking.CURRENT["stage_order"][0],
        "days_in_stage": days,
        "hazards": [{"released": False}] if hazard else [],
        "resident": resident,
    }


def _from_inputs(case_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
    state = inputs.get("support_state") or ("Yes" if inputs.get("support") else "No")
    adjustment = inputs.get("adjustment")
    return _case(case_id, inputs["days"], state, inputs.get("hazard", False), adjustment)


NEIGHBOURS = [
    _case("N-1", 90, hazard=True),
    _case("N-2", 40, "Yes"),
    _case("N-3", 25),
    _case("N-4", 5),
]


def _rank_pair(scenario: dict[str, Any]) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for side in ("baseline", "variant"):
        cases = [*NEIGHBOURS, _from_inputs("UNDER-TEST", scenario[side])]
        entry = next(e for e in ranking.rank(cases) if e["id"] == "UNDER-TEST")
        runs.append(entry)
    return runs


class CohortManifestDraftTests(unittest.TestCase):
    def test_status_literals_and_registry_agree(self) -> None:
        self.assertEqual(
            (M["status"], M["approval"], M["execution"]), ("DRAFT", "UNAPPROVED", "NOT EXECUTED")
        )
        self.assertIs(M["is_synthetic"], True)
        self.assertIs(M["fairness_evidence"], False)
        self.assertEqual(M["held_out_split"]["status"], "NOT CREATED")
        entry = next(d for d in REG["datasets"] if d["id"] == "cohort-manifest-draft")
        self.assertEqual(entry["version"], M["version"])
        for word in ("DRAFT", "UNAPPROVED", "NOT EXECUTED", "not held-out"):
            self.assertIn(word, entry["purpose"])

    def test_wording_and_characters(self) -> None:
        TEXT.encode("ascii")
        self.assertNotIn("\u2014", TEXT)
        for pattern in (r"\boracle\b", r"\bgold\b", r"ground truth", r"\bAPPROVED\b"):
            self.assertIsNone(
                re.search(pattern, TEXT, re.I if pattern != r"\bAPPROVED\b" else 0), pattern
            )
        self.assertIsNone(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", TEXT), "email-like text")
        self.assertIsNone(
            re.search(r"\b[A-Z]{1,2}\d{1,2} ?\d[A-Z]{2}\b", TEXT), "postcode-like text"
        )

    def test_scenarios_pairs_and_links(self) -> None:
        ids = [s["id"] for s in M["scenarios"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(re.fullmatch(r"CM-[A-Z]\d\d", i) for i in ids))
        self.assertEqual({s["family"] for s in M["scenarios"]}, set(M["factor_families"]))
        seeds = {d["id"]: d for d in M["defect_seeds"]}
        self.assertEqual(len(seeds), len(M["defect_seeds"]))
        reconciles = {r["id"] for r in M["reconciliation"]}
        for s in M["scenarios"]:
            self.assertEqual(s["ai_expected"]["status"], "unlabelled", s["id"])
            self.assertTrue(s["deterministic_expected"]["justification"], s["id"])
            if s["baseline"] is None:
                self.assertEqual(s["variant"], None, s["id"])
                self.assertIn(s["reconciliation_ref"], reconciles, s["id"])
            else:
                self.assertEqual(isolation_violations(s), set(), s["id"])
            for d in s["defect_seeds"] + s["critical_error_seeds"]:
                self.assertIn(d, seeds)
        for d in M["defect_seeds"]:
            self.assertIn(d["scenario"], ids)
            self.assertIn(
                d["id"], next(s for s in M["scenarios"] if s["id"] == d["scenario"])["defect_seeds"]
            )
        self.assertTrue(any(d["critical"] for d in M["defect_seeds"]))
        self.assertEqual(seeds["SD-01"]["status"], "candidate_unconfirmed")

    def test_reconciliation_arithmetic_and_threshold_states(self) -> None:
        sel = M["proposals"]["template_reference_selection"]
        self.assertEqual(sel["decision_rule"], "ED-1")
        sample = next(
            o
            for p in M["proposals"]["items"]
            if p["id"] == "PR-01"
            for o in p["options"]
            if o["id"] == sel["sample_option"]
        )
        max_rate, min_n = sample["target_upper_bound"], sample["min_evaluated"]
        for p in M["proposals"]["items"]:
            for o in p.get("options", []):
                if "target_upper_bound" in o:
                    self.assertEqual(
                        o["min_evaluated"],
                        math.ceil(math.log(0.05) / math.log(1 - o["target_upper_bound"])),
                        o["id"],
                    )
        for r in M["reconciliation"]:
            pooled_errors = pooled_n = 0
            for arm, c in r["arms"].items():
                self.assertEqual(
                    c["eligible"],
                    c["evaluated"] + c["excluded_with_reason"] + c["not_evaluable"],
                    (r["id"], arm),
                )
                self.assertLessEqual(c["errors"], c["evaluated"])
                self.assertLessEqual(c["review_required"], c["eligible"])
                burden = (
                    f"{c['review_required']}/{c['eligible']}" if c["eligible"] else "not_computable"
                )
                self.assertEqual(r["expected_review_burden"][arm], burden, (r["id"], arm))
                if c["evaluated"] < min_n:
                    state = "insufficient"
                else:
                    state = "breach" if c["errors"] / c["evaluated"] > max_rate else "sufficient"
                self.assertEqual(r["expected_state"][arm], state, (r["id"], arm))
                pooled_errors += c["errors"]
                pooled_n += c["evaluated"]
            if r.get("pooled_expected"):
                self.assertLessEqual(pooled_errors / pooled_n, max_rate)
                self.assertIn("breach", r["expected_state"].values())

    def test_proposals_are_labelled_and_need_approval(self) -> None:
        for p in M["proposals"]["items"]:
            for k in ("basis", "requires_approval", "approver_role"):
                self.assertIn(k, p)
            self.assertIs(p["requires_approval"], True)
        critical = next(p for p in M["proposals"]["items"] if p["id"] == "PR-03")
        self.assertEqual(critical["value"], 0)
        self.assertIn("not an activated threshold", critical["status"])
        self.assertIn("POLICY PROPOSAL ONLY", M["policy_proposals"]["status"])
        self.assertTrue(
            all(p["implementation"].startswith("None") for p in M["policy_proposals"]["items"])
        )

    def test_held_out_roles_unfilled_and_fresh_ids_required(self) -> None:
        held = M["held_out_split"]
        self.assertEqual(set(held["roles"].values()), {"UNFILLED"})
        self.assertIn("NEW IDs", held["fresh_scenario_rule"])
        self.assertNotIn("held_out_scenarios", M)

    def test_expectations_match_unchanged_ranking_semantics(self) -> None:
        checked = set()
        for s in M["scenarios"]:
            binding = s["deterministic_expected"].get("ranking_binding")
            if not binding:
                continue
            checked.add(binding)
            if binding == "none_no_contact_input":
                self.assertEqual(s["deterministic_expected"]["type"], "representation_pending")
                continue
            base, var = _rank_pair(s)
            if binding == "same_position_same_reason_codes":
                self.assertEqual(base["rank"], var["rank"], s["id"])
                self.assertEqual(base["reason_codes"], var["reason_codes"], s["id"])
            elif binding == "variant_ranks_ahead":
                self.assertLess(var["rank"], base["rank"], s["id"])
            elif binding == "hazard_ahead_of_non_hazard":
                self.assertEqual(base["rank"], var["rank"], s["id"])
                self.assertEqual(base["reason_codes"], var["reason_codes"], s["id"])
                self.assertEqual(base["rank"], 2, s["id"])  # behind only the older open safety case
                self.assertIn("safety_open", var["reason_codes"], s["id"])
            elif binding == "ties_with_no_adds_support_unknown_reason":
                self.assertEqual(base["rank"], var["rank"], s["id"])
                self.assertEqual(
                    set(var["reason_codes"]) - set(base["reason_codes"]), {"support_unknown"}
                )
            else:
                self.fail(f"unknown binding {binding}")
        self.assertEqual(len(checked), 5)

    def test_isolation_check_rejects_unrelated_support_change(self) -> None:
        s = json.loads(json.dumps(next(x for x in M["scenarios"] if x["id"] == "CM-S01")))
        self.assertEqual(isolation_violations(s), set())
        s["variant"]["support"] = True
        self.assertEqual(isolation_violations(s), {"support"})
        a = next(x for x in M["scenarios"] if x["id"] == "CM-A01")
        self.assertEqual(isolation_violations(a), set())

    def test_every_acceptance_criterion_is_not_met(self) -> None:
        self.assertEqual([a["ac"] for a in M["acceptance_trace"]], [f"AC{n}" for n in range(1, 7)])
        for a in M["acceptance_trace"]:
            self.assertEqual(a["status"], "Not met")
            self.assertTrue(a["manifest_keys"] and a["would_be_met_by"])


if __name__ == "__main__":
    unittest.main()
