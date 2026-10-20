"""Structural checks for the DRAFT cohort manifest (#222). Not an evaluation.

Reads only the committed synthetic JSON and the registry. It proves the draft stays
labelled unapproved and internally consistent; it runs no model and approves nothing.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "src/agents/evals/cohort_manifest_draft.json"
TEXT = PATH.read_text(encoding="utf-8")
M = json.loads(TEXT)
REG = json.loads((ROOT / "src/agents/evals/registry.json").read_text(encoding="utf-8"))


class CohortManifestDraftTests(unittest.TestCase):
    def test_status_literals_and_registry_agree(self):
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

    def test_wording_and_characters(self):
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

    def test_scenarios_pairs_and_links(self):
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
                keys = set(s["baseline"]) | set(s["variant"])
                differing = {
                    k for k in keys if k != "id" and s["baseline"].get(k) != s["variant"].get(k)
                }
                factors = set(s["varied_factor"].split("_and_"))
                self.assertTrue(factors <= differing <= factors | {"support"}, (s["id"], differing))
            for d in s["defect_seeds"] + s["critical_error_seeds"]:
                self.assertIn(d, seeds)
        for d in M["defect_seeds"]:
            self.assertIn(d["scenario"], ids)
            self.assertIn(
                d["id"], next(s for s in M["scenarios"] if s["id"] == d["scenario"])["defect_seeds"]
            )
        self.assertTrue(any(d["critical"] for d in M["defect_seeds"]))
        self.assertEqual(seeds["SD-01"]["status"], "candidate_unconfirmed")

    def test_reconciliation_arithmetic_and_threshold_states(self):
        props = {p["name"]: p for p in M["proposals"]["items"]}
        min_n, max_rate = (
            props["minimum_arm_denominator"]["value"],
            props["max_arm_error_rate"]["value"],
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

    def test_proposals_are_labelled_and_need_approval(self):
        for p in M["proposals"]["items"]:
            for k in ("value", "rationale", "basis", "requires_approval", "approver_role"):
                self.assertIn(k, p)
            self.assertIs(p["requires_approval"], True)

    def test_every_acceptance_criterion_is_not_met(self):
        self.assertEqual([a["ac"] for a in M["acceptance_trace"]], [f"AC{n}" for n in range(1, 7)])
        for a in M["acceptance_trace"]:
            self.assertEqual(a["status"], "Not met")
            self.assertTrue(a["manifest_keys"] and a["would_be_met_by"])


if __name__ == "__main__":
    unittest.main()
