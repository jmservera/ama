"""Synthetic data needs inventory: structure, coverage values and register links."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
INVENTORY = json.loads((PACK / "needs-inventory.json").read_text())
REGISTER = json.loads((PACK / "provenance-register.json").read_text())
REQUIRED = ("id", "need", "source_reference", "consuming_issues", "volume", "owner", "coverage")


class NeedsInventoryTests(unittest.TestCase):
    def test_rows_are_complete_and_unique(self):
        ids = [n["id"] for n in INVENTORY["needs"]]
        self.assertEqual(len(ids), len(set(ids)))
        for n in INVENTORY["needs"]:
            for field in REQUIRED:
                self.assertTrue(n[field], (n["id"], field))
            self.assertIn(n["coverage"], INVENTORY["coverage_values"], n["id"])

    def test_datasets_exist_in_provenance_register(self):
        known = {d["id"] for d in REGISTER["datasets"]}
        for n in INVENTORY["needs"]:
            self.assertLessEqual(set(n["dataset_ids"]), known, n["id"])

    def test_sensor_need_is_missing_and_gate_rule_recorded(self):
        sensor = next(n for n in INVENTORY["needs"] if n["id"] == "SN-09")
        self.assertEqual(sensor["coverage"], "missing")
        self.assertIn("inventory row", INVENTORY["gate_rule"])
        self.assertTrue(INVENTORY["open_items"])

    def test_gated_epics_have_rows(self):
        cited = {i for n in INVENTORY["needs"] for i in n["consuming_issues"]}
        self.assertTrue({"#109", "#157", "#104"} <= cited)

    def test_every_gap_has_child_story_or_deferral(self):
        for n in INVENTORY["needs"]:
            gap = n["gap_closure"]
            self.assertIn(gap["kind"], ("child", "delivered", "deferred"), n["id"])
            self.assertTrue(gap["issues"] or gap["kind"] == "deferred", n["id"])
            self.assertTrue(gap["note"], n["id"])
            if n["coverage"] != "covered":
                self.assertNotEqual(gap["kind"], "delivered", n["id"])

    def test_generator_conventions_recorded(self):
        conv = INVENTORY["generator_conventions"]
        for key in ("reuse_rule", "seed", "identifiers", "is_synthetic"):
            self.assertTrue(conv[key], key)


if __name__ == "__main__":
    unittest.main()
