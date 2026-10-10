import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch

from properwarm_mvp import exercise, programme
from properwarm_mvp.sqlstore import SqlStore


class ProgrammeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        data = exercise.dataset()
        original = data["cases"][0]
        data["cases"] = [dict(original, id=f"CASE-{i:04d}") for i in range(980)]
        seed = root / "cases.json"
        seed.write_text(json.dumps(data))
        self.store = SqlStore(str(seed), str(root / "test.sqlite"))
        self.addCleanup(self.store.db.close)
        self.path = root / "stock.csv"
        keys = ["synthetic_home_id", "local_authority", "epc_need_group_model",
                "map_address", "latitude", "longitude", "is_synthetic"]
        with self.path.open("w", newline="") as source:
            writer = csv.DictWriter(source, fieldnames=keys)
            writer.writeheader()
            for i in range(60000):
                writer.writerow(dict(synthetic_home_id=f"STOCK-{i:05d}",
                    local_authority="Area A" if i % 2 == 0 else "Area B",
                    epc_need_group_model="Below C" if i % 3 == 0 else "C or above",
                    map_address=f"Constructed address {i}", latitude=55 + (i % 20) / 100,
                    longitude=-1.5 - (i % 30) / 100, is_synthetic="true"))
        self.source = programme.import_stock(self.store, self.path, "baseline-hash", "2026-10-08")
        self.user = dict(role="Retrofit Programme Manager")

    def test_exact_counts_filter_map_and_page_reconciliation(self):
        result = programme.page_stock(self.store, self.user, {})
        self.assertEqual(result["total"], 60000)
        self.assertEqual(len(result["records"]), 50)
        self.assertEqual(sum(c["count"] for c in result["clusters"]), 60000)
        self.assertEqual(self.source["stock_sha256"], hashlib.sha256(self.path.read_bytes()).hexdigest())
        filtered = programme.page_stock(self.store, self.user, {"area": "Area A", "epc_group": "Below C"})
        self.assertEqual(filtered["total"], 10000)
        self.assertEqual(sum(c["count"] for c in filtered["clusters"]), 10000)
        second = programme.page_stock(self.store, self.user, {}, offset=50)
        self.assertFalse({r["synthetic_home_id"] for r in result["records"]}
                         & {r["synthetic_home_id"] for r in second["records"]})

    def test_idempotent_import_preserves_case_and_audit_content(self):
        before = self.store.db.execute("SELECT id,body FROM cases ORDER BY id").fetchall()
        programme.import_stock(self.store, self.path, "baseline-hash", "2026-10-08")
        self.assertEqual(before, self.store.db.execute("SELECT id,body FROM cases ORDER BY id").fetchall())
        with self.assertRaisesRegex(ValueError, "lineage differs"):
            programme.import_stock(self.store, self.path, "different", "2026-10-08")
        self.assertEqual(self.store.db.execute("SELECT COUNT(*) FROM stock").fetchone()[0], 60000)

    def test_permissions_invalid_pages_and_literal_search(self):
        for role in ("Contractor", "unknown"):
            with self.assertRaises(PermissionError):
                programme.page_stock(self.store, dict(role=role), {})
        with self.assertRaises(ValueError):
            programme.page_stock(self.store, self.user, {}, limit=101)
        self.assertEqual(programme.page_stock(self.store, self.user, {"q": "%"})["total"], 0)
        self.assertEqual(programme.page_stock(self.store, self.user, {"q": "STOCK-00001"})["total"], 1)

    def test_generated_case_enrichment_preserves_history_and_requires_review(self):
        case = deepcopy(self.store.cases["CASE-0000"])
        case.pop("exercise")
        original = deepcopy(case)
        metadata = programme.workbench_metadata(case, self.source)
        self.assertEqual(case, original)
        self.assertEqual(metadata["lifecycle"], "Intake")
        self.assertEqual(metadata["evidence"][1]["raw_text"], f"epc_band: {case['home']['epc']}\n")
        self.assertNotIn("fund_events", metadata)
        self.assertNotIn("milestones", metadata)
        case["exercise"] = metadata
        self.store.cases[case["id"]] = case
        actor = dict(exercise.dataset()["staff"][0])
        actor["role"] = "Retrofit Programme Manager"
        self.store.staff[actor["email"]] = actor
        created = self.store.exercise_action(actor, case["id"], dict(action="create-form", form_type="competitive"))
        self.assertEqual(len(created["case"]["forms"]), 1)
        self.assertFalse(created["case"]["forms"]["FORM-001"]["fields"]["eligibility"]["candidates"])
        with patch.dict("os.environ", {"PW_PROGRAMME": "1"}, clear=True):
            case["exercise"] = metadata
            self.store.cases = {case["id"]: case}
            status = self.store.exercise_status(self.user)
        self.assertEqual(status["forecast"], {})
        self.assertEqual(status["analytical"]["cases"], 1)
        self.assertEqual(status["stories"][0]["id"], case["id"])


if __name__ == "__main__":
    unittest.main()
