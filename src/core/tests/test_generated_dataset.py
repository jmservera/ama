"""Synthetic generator coverage without requiring private geography or billable services."""
from datetime import date
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from zava_forward.core import insights
from zava_forward.core.sqlstore import SqlStore

GENERATOR = Path(__file__).resolve().parents[3] / "support/synthetic-data/retrofit-flow/zava-forward-year-one/generator"
sys.path.insert(0, str(GENERATOR))
builder = importlib.import_module("build_mvp_dataset")
pack = importlib.import_module("generate_pack")
fabric = importlib.import_module("zf_stock_fabric")
epc = importlib.import_module("zf_stock_epc")

builder_band = importlib.import_module("zf_model").band_from_sap


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

    def test_every_case_links_to_one_stock_home_or_is_reported_unlinked(self):
        link = self.data["stock_link"]
        ids = {r["synthetic_home_id"] for r in register()}
        linked = [c for c in self.data["cases"] if c["synthetic_stock_anchor_id"] in ids]
        self.assertEqual(link["linked_cases"] + link["unlinked_cases"], len(self.data["cases"]))
        self.assertEqual(link["linked_cases"], len(linked))
        self.assertEqual(link["unlinked_cases"], len(link["unlinked_case_ids"]))
        for c in linked:
            self.assertTrue(c["stock_fabric"]["fabric_is_synthetic"])
        missing = fabric.link_report([dict(id="ZF-X", synthetic_stock_anchor_id="NOPE")], register())
        self.assertEqual(missing["unlinked_case_ids"], ["ZF-X"])

    def test_stock_fabric_is_seeded_labelled_and_reproducible(self):
        rows = register()[:50]
        one, two = fabric.fabric_rows(rows, 1), fabric.fabric_rows(rows, 1)
        self.assertEqual(one, two)
        self.assertNotEqual(one, fabric.fabric_rows(rows, 2))
        for r in one:
            self.assertTrue(r["fabric_is_synthetic"])
            lo, hi = fabric.AGE_BANDS[r["age_band"]]
            self.assertTrue(lo <= r["build_year"] <= hi)
        summary = fabric.summary(one, 1)
        self.assertIn("not a company fact", summary["label"])
        self.assertIn("age_band_weights_by_locality", summary["assumptions"])

    def test_epc_and_survey_fields_reconcile_to_fabric_and_conflicts_are_manifested(self):
        rows = register()
        recs = epc.epc_rows(rows, 1)
        self.assertEqual(recs, epc.epc_rows(rows, 1))
        self.assertNotEqual(recs, epc.epc_rows(rows, 2))
        fab = {f["synthetic_home_id"]: f for f in fabric.fabric_rows(rows)}
        manifest = {m["synthetic_home_id"]: m for m in epc.conflict_manifest(recs)}
        self.assertTrue(manifest)
        self.assertEqual(len(manifest), sum(1 for r in recs if r["conflict_type"]))
        surveyed = 0
        for r in recs:
            f = fab[r["synthetic_home_id"]]
            self.assertTrue(r["epc_is_synthetic"])
            self.assertEqual(r["epc_band"], builder_band(r["epc_sap"]))
            self.assertEqual(r["epc_dwelling_type"], f["dwelling_type"])
            self.assertLessEqual(r["epc_lodged"], r["epc_expires"])
            pairs = (("epc_build_age_band", "surveyed_build_age_band", "age_band"),
                     ("epc_construction", "surveyed_construction", "construction"),
                     ("epc_heating", "surveyed_heating", "heating"))
            if r["survey_status"] != "Surveyed":
                self.assertEqual(r["conflict_type"], "")
                self.assertEqual((r["epc_build_age_band"], r["epc_construction"], r["epc_heating"]),
                                 (f["age_band"], f["construction"], f["heating"]))
                continue
            surveyed += 1
            for e, s, k in pairs:
                self.assertEqual(r[s], f[k])
            self.assertEqual(r["surveyed_band"], builder_band(r["surveyed_sap"]))
            if r["conflict_type"]:
                self.assertIn(r["synthetic_home_id"], manifest)
                self.assertNotEqual(manifest[r["synthetic_home_id"]]["epc_value"],
                                    manifest[r["synthetic_home_id"]]["surveyed_value"])
            else:
                self.assertLessEqual(abs(r["epc_sap"] - r["surveyed_sap"]), 3)
                for e, s, k in pairs:
                    self.assertEqual(r[e], r[s])
                self.assertEqual(r["epc_band"] == r["surveyed_band"] or abs(r["epc_sap"] - r["surveyed_sap"]) <= 3, True)
        self.assertTrue(surveyed)
        self.assertIn("not a lodged EPC", epc.summary(recs, 1)["label"])

    def test_cases_carry_epc_record_matching_their_stock_fabric(self):
        for c in self.data["cases"]:
            if "stock_fabric" in c:
                e = c["stock_epc"]
                self.assertTrue(e["epc_is_synthetic"])
                if not e["conflict_type"]:
                    self.assertEqual(e["epc_construction"], c["stock_fabric"]["construction"])
                    self.assertEqual(e["epc_heating"], c["stock_fabric"]["heating"])

    def test_mvp_output_and_receipt_record_seed_version_and_revision(self):
        self.assertEqual(self.data["seed"], 20260901)
        self.assertEqual(self.data["generator_version"], "operational-coverage-v1")
        self.assertRegex(self.data["generator_revision"], r"^sha256:[0-9a-f]{16}$")
        receipt = json.loads(Path(str(self.path) + ".coverage.json").read_text())
        for key in ("seed", "as_of", "generator_version", "generator_revision"):
            self.assertEqual(receipt[key], self.data[key])

    def test_pack_generator_is_byte_deterministic_with_manifest(self):
        def run(name):
            root = Path(self.tmp.name) / name
            argv = ["pack", "--seed", "1341953496", "--as-of", "2026-09-30",
                    "--pack-dir", str(root / "pack"), "--key-dir", str(root / "key")]
            with patch.object(sys, "argv", argv), patch("sys.stdout"):
                pack.main()
            return root
        one, two = run("one"), run("two")
        names = sorted(p.name for p in (one / "pack").iterdir())
        self.assertIn("manifest.json", names)
        for name in names:
            self.assertEqual((one / "pack" / name).read_bytes(), (two / "pack" / name).read_bytes(), name)
        for name in sorted(p.name for p in (one / "key").iterdir()):
            self.assertEqual((one / "key" / name).read_bytes(), (two / "key" / name).read_bytes(), name)
        manifest = json.loads((one / "pack" / "manifest.json").read_text())
        self.assertEqual(manifest["seed"], 1341953496)
        self.assertEqual(manifest["generated_at"], "2026-09-30T00:00:00")
        self.assertEqual(manifest["version"], "2.0.0")
        self.assertRegex(manifest["generator_revision"], r"^sha256:[0-9a-f]{16}$")
        self.assertEqual(set(manifest["file_sha256"]), set(manifest["row_counts"]))

    def test_stock_fabric_and_epc_generators_are_byte_deterministic_with_revision(self):
        import csv
        reg = Path(self.tmp.name) / "register.csv"
        with reg.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, list(register()[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(register())

        def run(name):
            root = Path(self.tmp.name) / name
            root.mkdir()
            fabric.main(["--seed", "7", "--register", str(reg), "--out", str(root / "fab.csv"),
                         "--summary", str(root / "fab.json")])
            epc.main(["--seed", "8", "--register", str(reg), "--out", str(root / "epc.csv"),
                      "--manifest", str(root / "conf.csv"), "--summary", str(root / "epc.json")])
            return root
        one, two = run("stock1"), run("stock2")
        for name in sorted(p.name for p in one.iterdir()):
            self.assertEqual((one / name).read_bytes(), (two / name).read_bytes(), name)
        for name, seed in (("fab.json", 7), ("epc.json", 8)):
            summary = json.loads((one / name).read_text())
            self.assertEqual(summary["seed"], seed)
            self.assertIn("version", summary)
            self.assertRegex(summary["generator_revision"], r"^sha256:[0-9a-f]{16}$")

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
        filled = [c for c in cases.values() if c.get("grants")]
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

    def test_lifecycle_coverage_seeds_or_defers_every_state_without_outcomes(self):
        life = json.loads(Path(str(self.path) + ".coverage.json").read_text())["lifecycle"]
        seeded = life["seeded"]
        self.assertEqual(set(seeded["work order"]), {"Issued", "Completed"})
        self.assertEqual(set(seeded["budget"]), {"Proposed"})
        self.assertEqual(set(seeded["commitment"]), {"Raised"})
        self.assertIn("Valuation: Received", seeded["invoice"])
        self.assertEqual(set(seeded["payment"]), {"Not payable yet"})
        self.assertEqual(set(seeded["grant"]), {"Not recorded"})
        self.assertEqual(set(seeded["quality"]), {"Submitted"})
        self.assertEqual(seeded["resident decision"], {})
        self.assertTrue(seeded["safety hold"].get("Open") and seeded["safety hold"].get("Released"))
        for outcome in ("Approved",):
            self.assertIn(outcome, life["deferred"]["budget"])
        for key in ("grant", "quality", "resident decision", "payment"):
            self.assertFalse(set(seeded[key]) & set(life["deferred"][key]), key)
        self.assertTrue(all(i["payment_status"] == "Not payable yet" for c in self.data["cases"]
                            for i in c.get("finance", {}).get("invoices", [])))

    def test_generated_queues_survive_sql_seed_and_restart(self):
        db = Path(self.tmp.name) / "coverage.sqlite"
        first = SqlStore(str(self.path), str(db))
        try:
            count = len(insights.visits(list(first.cases.values())))
            self.assertGreater(count, 6)
            self.assertEqual(first.data["procurement"], self.data["procurement"])
            self.assertEqual(len(first.finance_queue(next(p for p in first.staff.values() if p["code"] == "PM-01"))), 13)
            reopened = SqlStore(str(self.path), str(db))
            try:
                self.assertEqual(reopened.as_of, self.data["as_of"])
                self.assertEqual(len(insights.visits(list(reopened.cases.values()))), count)
                self.assertEqual(reopened.data["procurement"], first.data["procurement"])
            finally:
                reopened.db.close()
        finally:
            first.db.close()
