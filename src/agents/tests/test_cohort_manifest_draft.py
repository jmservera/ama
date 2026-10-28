"""Structural checks for the DRAFT cohort manifest (#222). Not an evaluation.

Reads only the committed synthetic JSON and the registry. It proves the draft stays
labelled unapproved and internally consistent; it runs no model and approves nothing.
"""

import json
import math
import re
import unittest
from collections.abc import Callable
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
# Varied factors that rank() has no input for. They are preserved on each case, not erased.
PASSTHROUGH_FIELDS = ("sensor_data", "source_record", "appointment_history", "contact_need")


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
    case = _case(case_id, inputs["days"], state, inputs.get("hazard", False), adjustment)
    # Carried so a ranker or wrapper that reads them is exercised; rank() ignores unknown keys.
    case.update({k: inputs[k] for k in PASSTHROUGH_FIELDS if k in inputs})
    return case


NEIGHBOURS = [
    _case("N-1", 90, hazard=True),
    _case("N-2", 40, "Yes"),
    _case("N-3", 25),
    _case("N-4", 5),
]


NEIGHBOURS_NON_HAZARD_RANK = 3  # first non-hazard neighbour in the fixed set below


def _rank_pair(
    scenario: dict[str, Any],
    rank_fn: Callable[[list[dict[str, Any]]], list[dict[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    rank_fn = rank_fn or ranking.rank
    runs: list[dict[str, Any]] = []
    for side in ("baseline", "variant"):
        cases = [*NEIGHBOURS, _from_inputs("UNDER-TEST", scenario[side])]
        entry = next((e for e in rank_fn(cases) if e["id"] == "UNDER-TEST"), None)
        assert entry is not None, f"{scenario['id']} {side} case missing from the ranking"
        runs.append(entry)
    return runs


def check_binding(
    scenario: dict[str, Any],
    rank_fn: Callable[[list[dict[str, Any]]], list[dict[str, Any]]] | None = None,
) -> None:
    """Raise AssertionError when the claimed ranking binding does not hold for the pair."""
    binding = scenario["deterministic_expected"]["ranking_binding"]
    base, var = _rank_pair(scenario, rank_fn)
    same = base["rank"] == var["rank"] and base["reason_codes"] == var["reason_codes"]
    if binding in ("same_position_same_reason_codes", "hazard_ahead_of_non_hazard"):
        assert same, scenario["id"]
        if binding == "hazard_ahead_of_non_hazard":
            assert "safety_open" in var["reason_codes"], scenario["id"]
            assert var["rank"] < NEIGHBOURS_NON_HAZARD_RANK, scenario["id"]
    elif binding == "variant_ranks_ahead":
        assert var["rank"] < base["rank"], scenario["id"]
    elif binding == "ties_with_no_adds_support_unknown_reason":
        assert base["rank"] == var["rank"], scenario["id"]
        assert set(var["reason_codes"]) == set(base["reason_codes"]) | {"support_unknown"}, scenario["id"]
    else:
        raise AssertionError(f"unknown binding {binding}")


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
            check_binding(s)
            factors = set(s["varied_factor"].split("_and_"))
            base_case = _from_inputs("X", s["baseline"])
            var_case = _from_inputs("X", s["variant"])
            if factors <= set(PASSTHROUGH_FIELDS) | {"sensor_data", "source_record"}:
                self.assertTrue(all(base_case.get(f) != var_case.get(f) for f in factors), s["id"])
            else:
                self.assertNotEqual(base_case, var_case, s["id"])
        self.assertEqual(len(checked), 5)

    def test_binding_check_rejects_missing_data_exclusion_and_appointment_penalty(self) -> None:
        by_id = {s["id"]: s for s in M["scenarios"]}
        for sid in ("CM-S01", "CM-S02", "CM-H01", "CM-H02", "CM-C01", "CM-C02"):
            base, var = (
                _from_inputs("X", by_id[sid]["baseline"]),
                _from_inputs("X", by_id[sid]["variant"]),
            )
            self.assertNotEqual(base, var, sid)

        def exclude_missing(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
            kept = [
                c
                for c in cases
                if {c.get("sensor_data"), c.get("source_record")}.isdisjoint({"missing", "stale"})
            ]
            return list(ranking.rank(kept))

        def penalise_appointments(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
            bad = {"prior_no_access", "rescheduled_by_resident"}
            good = [c for c in cases if c.get("appointment_history") not in bad]
            tail = [c for c in cases if c.get("appointment_history") in bad]
            out = list(ranking.rank(good))
            return out + [dict(e, rank=len(out) + i) for i, e in enumerate(ranking.rank(tail), 1)]

        for sid in ("CM-S01", "CM-S02", "CM-C01", "CM-C02"):
            with self.assertRaises(AssertionError, msg=sid):
                check_binding(by_id[sid], exclude_missing)
        for sid in ("CM-H01", "CM-H02"):
            with self.assertRaises(AssertionError, msg=sid):
                check_binding(by_id[sid], penalise_appointments)
        for sid in ("CM-S01", "CM-H01", "CM-C01"):
            check_binding(by_id[sid])

    def test_open_safety_order_support_before_waiting_days(self) -> None:
        cases = [
            _case("A", 10, hazard=True),
            _case("B", 1, "Yes", hazard=True),
            _case("C", 99),
            _case("D", 50, "Yes"),
        ]
        order = [e["id"] for e in ranking.rank(cases)]
        self.assertEqual(order, ["B", "A", "D", "C"])
        # Rank 2 for the CM-C01 case is specific to the fixed neighbours, not a policy rule.
        with_supported = [*NEIGHBOURS, _case("S", 1, "Yes", hazard=True)]
        entry = next(e for e in ranking.rank(with_supported) if e["id"] == "N-1")
        self.assertEqual(entry["rank"], 2)

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
