"""Synthetic generator coverage without requiring private geography or billable services."""
from datetime import date
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from zavaforward_mvp import insights
from zavaforward_mvp.sqlstore import SqlStore

GENERATOR = Path(__file__).resolve().parents[2] / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"
sys.path.insert(0, str(GENERATOR))
builder = importlib.import_module("build_mvp_dataset")


def register():
    rows = []
    for locality in ("A", "B", "C"):
        for form in ("apartments", "bungalow", "terrace", "semidetached_house", "detached"):
            for i in range(400):
                rows.append(dict(synthetic_home_id=f"TEST-{locality}-{form}-{i}",
                    portfolio_category="General needs - social rent", postcode="TEST 1",
                    address_street_or_place="Fictional Test Street", address_house_number=str(i + 1),
                    address_locality="Fictional Test Town", local_authority="Test Authority",
                    locality_theme=f"Locality {locality}", building_form_osm=form, latitude="54.9", longitude="-1.5"))
    return rows


class GeneratedDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.path = Path(cls.tmp.name) / "seed.json"
        with patch.object(builder, "load_register", return_value=register()):
            with patch.object(sys, "argv", ["builder", "--seed", "20260901", "--as-of", "2026-10-13", "--out", str(cls.path)]):
                builder.main()
        cls.data = json.loads(cls.path.read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_same_seed_date_and_register_are_byte_deterministic(self):
        second = Path(self.tmp.name) / "second.json"
        with patch.object(builder, "load_register", return_value=register()):
            with patch.object(sys, "argv", ["builder", "--seed", "20260901", "--as-of", "2026-10-13", "--out", str(second)]):
                builder.main()
        self.assertEqual(self.path.read_bytes(), second.read_bytes())
        self.assertEqual(self.data["as_of"], "2026-10-13")
        self.assertEqual(len(self.data["cases"]), 980)

    def test_visible_visit_cohort_owner_partition_and_history_contrasts(self):
        cases = self.data["cases"]
        cohort = [(c, a) for c in cases for a in c["appointments"] if a.get("fixture") == "forward-visit"]
        self.assertEqual(len(cohort), 6)
        self.assertEqual(sum("2026-10-12" <= a["date"] <= "2026-10-18" for _, a in cohort), 4)
        visits = insights.visits(cases)
        for c, a in cohort:
            self.assertFalse(c["closed"])
            self.assertFalse(insights.has_hazard(c))
            self.assertFalse(c["resident"]["unavailable"])
            self.assertTrue(any(v["id"] == c["id"] and v["date"] == a["date"] for v in visits))
            self.assertTrue(any(v["id"] == c["id"] for v in insights.visits(cases, c["owner_code"])))
        contrasts = [a for c in cases for a in c["appointments"] if a.get("fixture") == "historical-visit"]
        self.assertEqual({a["outcome"] for a in contrasts}, {"Attended", "No access", "Cancelled"})
        self.assertTrue(all(c["history"] for c in cases))
        self.assertTrue(all(a["who"] and a["person"] and date.fromisoformat(a["date"]) for c in cases for a in c["appointments"]))

    def test_queues_resolve_references_and_do_not_invent_approvals(self):
        data = self.data
        cases = {c["id"]: c for c in data["cases"]}
        people = {p["code"]: p for p in data["staff"]}
        package = data["procurement"]["packages"][0]
        orders = data["procurement"]["work_orders"]
        self.assertTrue(orders)
        self.assertEqual(len({w["id"] for w in orders}), len(orders))
        for order in orders:
            self.assertIn(order["case_id"], cases)
            self.assertEqual(order["contractor"], cases[order["case_id"]]["contractor"]["name"])
            self.assertEqual(order["package"], package["id"])
        for contractor, capacity in package["capacity"].items():
            used = sum(w["contractor"] == contractor for w in orders)
            self.assertGreaterEqual(capacity["committed"], used)
            self.assertGreaterEqual(capacity["offered"], capacity["committed"])
        filled = [c for c in cases.values() if c.get("finance")]
        self.assertEqual(len(filled), 12)
        for c in filled:
            self.assertIn(c["owner_code"], people)
            self.assertEqual(c["finance"]["budget"]["status"], "Proposed")
            self.assertIsNone(c["finance"]["budget"]["approved_by"])
            self.assertEqual(c["finance"]["invoices"][0]["payment_status"], "Not payable yet")
            self.assertEqual(c["grants"][0]["state"], "Not recorded")
            self.assertEqual(c["quality"][0]["state"], "Submitted")
            self.assertNotIn("accepted_by", c["quality"][0])
            self.assertNotIn("technical", c)
            self.assertNotIn("measure_decisions", c)
            if c.get("handoff"):
                self.assertIn(c["handoff"]["to_code"], people)
                self.assertEqual(c["handoff"]["state"], "Offered")

    def test_generated_queues_survive_sql_seed_and_restart(self):
        db = Path(self.tmp.name) / "coverage.sqlite"
        first = SqlStore(str(self.path), str(db))
        try:
            count = len(insights.visits(list(first.cases.values())))
            self.assertGreater(count, 6)
            self.assertEqual(first.data["procurement"], self.data["procurement"])
            self.assertEqual(len(first.finance_queue(next(p for p in first.staff.values() if p["code"] == "PM-01"))), 12)
            reopened = SqlStore(str(self.path), str(db))
            try:
                self.assertEqual(reopened.as_of, self.data["as_of"])
                self.assertEqual(len(insights.visits(list(reopened.cases.values()))), count)
                self.assertEqual(reopened.data["procurement"], first.data["procurement"])
            finally:
                reopened.db.close()
        finally:
            first.db.close()
