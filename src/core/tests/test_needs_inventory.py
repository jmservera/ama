"""Synthetic inventory integrity and the versioned scenario-review binding."""

import copy
import json
import unittest
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
INVENTORY = json.loads((PACK / "needs-inventory.json").read_text())
REGISTER = json.loads((PACK / "provenance-register.json").read_text())
MANIFEST = json.loads((PACK / "scenario-manifest.json").read_text())
REQUIRED = ("id", "need", "source_reference", "consuming_issues", "volume", "owner", "coverage")


class NeedsInventoryTests(unittest.TestCase):
    def test_rows_are_complete_and_unique(self) -> None:
        ids = [n["id"] for n in INVENTORY["needs"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), {f"SN-{i:02d}" for i in range(1, 14)})
        for n in INVENTORY["needs"]:
            for field in REQUIRED:
                self.assertTrue(n[field], (n["id"], field))
            self.assertIn(n["coverage"], INVENTORY["coverage_values"], n["id"])

    def test_datasets_exist_in_provenance_register(self) -> None:
        known = {d["id"] for d in REGISTER["datasets"]}
        for n in INVENTORY["needs"]:
            self.assertTrue(n["dataset_ids"], n["id"])
            self.assertLessEqual(set(n["dataset_ids"]), known, n["id"])

    def test_sensor_need_is_partial_and_gate_rule_recorded(self) -> None:
        sensor = next(n for n in INVENTORY["needs"] if n["id"] == "SN-09")
        self.assertEqual(sensor["coverage"], "partial")
        self.assertIn("inventory row", INVENTORY["gate_rule"])
        self.assertIn("before work starts", INVENTORY["gate_rule"])
        self.assertIn("owner decision on volume and scope", INVENTORY["gate_rule"])
        self.assertTrue(INVENTORY["open_items"])

    def test_gated_epics_have_rows(self) -> None:
        cited = {i for n in INVENTORY["needs"] for i in n["consuming_issues"]}
        self.assertTrue({"#109", "#157", "#104"} <= cited)

    def test_every_gap_has_child_story_or_deferral(self) -> None:
        for n in INVENTORY["needs"]:
            gap = n["gap_closure"]
            self.assertIn(gap["kind"], ("child", "delivered", "deferred"), n["id"])
            self.assertTrue(gap["issues"] or gap["kind"] == "deferred", n["id"])
            self.assertTrue(gap["note"], n["id"])
            if n["coverage"] != "covered":
                self.assertNotEqual(gap["kind"], "delivered", n["id"])

    def test_generator_conventions_recorded(self) -> None:
        conv = INVENTORY["generator_conventions"]
        for key in ("reuse_rule", "seed", "identifiers", "is_synthetic"):
            self.assertTrue(conv[key], key)

    def assert_review_binding(self, manifest: dict[str, Any], inventory: dict[str, Any]) -> None:
        review = manifest["inventory"]
        self.assertEqual(review["path"], "needs-inventory.json")
        self.assertEqual(inventory["scenario_manifest"], "scenario-manifest.json")
        self.assertEqual(review["version"], inventory["version"])
        self.assertEqual(review["review_date"], inventory["review_date"])
        self.assertEqual(
            date.fromisoformat(review["review_date"]).isoformat(), review["review_date"]
        )
        self.assertEqual(set(review["reviewed_rows"]), {n["id"] for n in inventory["needs"]})
        self.assertEqual(len(review["reviewed_rows"]), len(set(review["reviewed_rows"])))
        self.assertEqual(review["review_kind"], "automated-engineering-review")
        self.assertTrue(review["reviewer"])
        self.assertEqual(review["owner_review"], "pending")
        self.assertEqual(inventory["status"], "draft-awaiting-owner-review")
        self.assertIs(manifest["is_synthetic"], True)
        for field in ("review_notes", "next_iteration"):
            self.assertTrue(review[field], field)
        for field in (
            "version",
            "iteration",
            "active_slice",
            "applicable_checks",
            "deferred_checks",
        ):
            self.assertTrue(manifest[field], field)

    def test_scenario_manifest_binds_reviewed_inventory(self) -> None:
        self.assert_review_binding(MANIFEST, INVENTORY)
        self.assertEqual(json.loads((PACK / MANIFEST["inventory"]["path"]).read_text()), INVENTORY)
        self.assertEqual(json.loads((PACK / INVENTORY["scenario_manifest"]).read_text()), MANIFEST)

    def test_review_rejects_stale_or_incomplete_binding(self) -> None:
        mutations = {
            "stale version": ("version", "0.0.0"),
            "stale date": ("review_date", "2026-10-14"),
            "missing row": ("reviewed_rows", MANIFEST["inventory"]["reviewed_rows"][:-1]),
            "duplicate row": (
                "reviewed_rows",
                [*MANIFEST["inventory"]["reviewed_rows"], "SN-01"],
            ),
            "unknown row": ("reviewed_rows", [*MANIFEST["inventory"]["reviewed_rows"], "SN-99"]),
            "broken path": ("path", "missing-inventory.json"),
            "empty reviewer": ("reviewer", ""),
            "owner approval claim": ("owner_review", "approved"),
            "human review claim": ("review_kind", "owner-approved"),
        }
        for label, (field, value) in mutations.items():
            with self.subTest(label=label):
                manifest = copy.deepcopy(MANIFEST)
                manifest["inventory"][field] = value
                with self.assertRaises(AssertionError):
                    self.assert_review_binding(manifest, INVENTORY)

    def test_review_rejects_broken_backlink_and_false_acceptance(self) -> None:
        for field, value in (
            ("scenario_manifest", "missing-scenario.json"),
            ("status", "approved"),
        ):
            with self.subTest(field=field):
                inventory = copy.deepcopy(INVENTORY)
                inventory[field] = value
                with self.assertRaises(AssertionError):
                    self.assert_review_binding(MANIFEST, inventory)
        manifest = copy.deepcopy(MANIFEST)
        manifest["is_synthetic"] = False
        with self.assertRaises(AssertionError):
            self.assert_review_binding(manifest, INVENTORY)

    def test_scenario_scope_keeps_full_application_evidence_deferred(self) -> None:
        self.assertEqual(MANIFEST["status"], "partial-inventory-integration")
        for key, count in (("profiles", 11), ("workflows", 9)):
            entries = MANIFEST[key]
            self.assertEqual(len(entries), count)
            self.assertEqual(len({entry["id"] for entry in entries}), count)
            self.assertTrue(all(entry["status"] == "deferred" for entry in entries))
        for path in MANIFEST["fixture_references"]:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_scenario_manifest_registered_as_public_metadata(self) -> None:
        entry = next(d for d in REGISTER["datasets"] if d["id"] == "DS-SCENARIO-MANIFEST")
        self.assertEqual(entry["visibility"], "public")
        self.assertEqual(ROOT / entry["location"], PACK / "scenario-manifest.json")


if __name__ == "__main__":
    unittest.main()
