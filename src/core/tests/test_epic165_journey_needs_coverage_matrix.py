"""Epic #165: scenario manifest entries resolve against the needs inventory and seeds."""

import csv
import json
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import scale_fixture
from zava_forward.core.synthetic.scenario_manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
WORKBENCH = ROOT / "src/api/checks/workbench-manifest.json"
FIXTURE_SOURCE = ROOT / "src/core/tests/dataset.py"
SEED_SIZE = 50


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_csv(name: str) -> list[dict[str, str]]:
    with (PACK / name).open(newline="") as handle:
        return list(csv.DictReader(handle))


def coverage_tables() -> dict[str, Any]:
    manifest = load_json(PACK / "scenario-manifest.json")
    inventory = load_json(PACK / manifest["inventory"]["path"])
    register = load_json(PACK / "provenance-register.json")
    workbench = load_json(WORKBENCH)
    need_ids = [need["id"] for need in inventory["needs"]]
    datasets = {d["id"] for d in register["datasets"]}
    scenarios = [
        {
            "kind": kind,
            "id": entry["id"],
            "evidence_index": entry["evidence_index"],
            "perspective": entry.get("perspective"),
            "case_ids": (manifest["profile_defaults"].get(entry["id"]) or {}).get("ids")
            if kind == "profiles"
            else None,
        }
        for kind in ("profiles", "workflows")
        for entry in manifest[kind]
    ]
    return {
        "scenarios": scenarios,
        "reviewed_rows": manifest["inventory"]["reviewed_rows"],
        "need_ids": need_ids,
        "need_datasets": {
            n["id"]: sorted(set(n["dataset_ids"]) & datasets) for n in inventory["needs"]
        },
        "roles": sorted(r["role"] for r in workbench["roles"]),
        "role_defaults": sorted(r["role"] for r in manifest["fixture_contract"]["role_defaults"]),
        "properties": sorted(r["property_id"] for r in load_csv("property-register.csv")),
        "journey_properties": sorted(r["property_ref"] for r in load_csv("resident-journey.csv")),
    }


class JourneyNeedsCoverageMatrixTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = load_json(PACK / "scenario-manifest.json")
        self.inventory = load_json(PACK / "needs-inventory.json")
        self.register = load_json(PACK / "provenance-register.json")
        self.workbench = load_json(WORKBENCH)

    def test_manifest_validates_and_binds_every_inventory_need(self) -> None:
        validate_manifest(self.manifest, ROOT)
        need_ids = [n["id"] for n in self.inventory["needs"]]
        self.assertEqual(self.manifest["inventory"]["reviewed_rows"], need_ids)
        self.assertEqual(len(need_ids), len(set(need_ids)))
        covered = {
            n["id"] for n in self.inventory["needs"] if "DS-SCENARIO-MANIFEST" in n["dataset_ids"]
        }
        self.assertEqual(covered, {"SN-11"})

    def test_no_dangling_need_references(self) -> None:
        need_ids = {n["id"] for n in self.inventory["needs"]}
        known_datasets = {d["id"] for d in self.register["datasets"]}
        for need in self.inventory["needs"]:
            self.assertLessEqual(set(need["dataset_ids"]), known_datasets, need["id"])
        for dataset in self.register["datasets"]:
            for ref in dataset.get("need_ids", dataset.get("needs", [])):
                self.assertIn(ref, need_ids, dataset["id"])
        text = json.dumps(self.manifest)
        for ref in {
            w for w in text.replace('"', " ").replace(",", " ").split() if w.startswith("SN-")
        }:
            self.assertIn(ref.rstrip(".;:"), need_ids)

    def test_every_scenario_resolves_without_orphans(self) -> None:
        for kind, workbench_kind in (("profiles", "profiles"), ("workflows", "workflows")):
            entries = self.manifest[kind]
            ids = [e["id"] for e in entries]
            self.assertEqual(len(ids), len(set(ids)), kind)
            self.assertEqual(
                sorted(e["evidence_index"] for e in entries),
                list(range(len(self.workbench[workbench_kind]))),
                kind,
            )
        self.assertEqual(
            set(self.manifest["profile_defaults"]),
            {e["id"] for e in self.manifest["profiles"]},
        )
        perspectives = [e["perspective"] for e in self.manifest["profiles"]]
        self.assertEqual(
            perspectives,
            [p["perspective"] for p in self.workbench["profiles"]],
        )

    def test_role_perspectives_and_fixture_cases_resolve(self) -> None:
        roles = {r["role"] for r in self.workbench["roles"]}
        defaults = self.manifest["fixture_contract"]["role_defaults"]
        self.assertEqual({r["role"] for r in defaults}, roles)
        case_ids = set(self.manifest["fixture_contract"]["case_ids"])
        self.assertEqual(case_ids, set(self.workbench["all_case_ids"]))
        source = FIXTURE_SOURCE.read_text()
        for case_id in case_ids:
            self.assertIn(f'"{case_id}"', source)
        for row in defaults:
            self.assertLessEqual(set(row["ids"]), case_ids, row["role"])
        for profile_id, default in self.manifest["profile_defaults"].items():
            if default:
                self.assertLessEqual(set(default["ids"]), case_ids, profile_id)

    def test_synthetic_property_and_case_seeds_have_no_orphans(self) -> None:
        properties = [r["property_id"] for r in load_csv("property-register.csv")]
        self.assertEqual(len(properties), len(set(properties)))
        for row in load_csv("resident-journey.csv"):
            self.assertIn(row["property_ref"], properties, row["candidate_id"])
        homes = {h["id"] for h in scale_fixture.homes(SEED_SIZE)}  # type: ignore[no-untyped-call]
        households = list(scale_fixture.households(SEED_SIZE))  # type: ignore[no-untyped-call]
        self.assertEqual({h["home_id"] for h in households}, homes)
        events = list(scale_fixture.events(SEED_SIZE))  # type: ignore[no-untyped-call]
        self.assertEqual({e["case"] for e in events}, homes)

    def test_cross_reference_tables_are_deterministic(self) -> None:
        first = coverage_tables()
        self.assertEqual(first, coverage_tables())
        self.assertEqual(
            json.dumps(first, sort_keys=True), json.dumps(coverage_tables(), sort_keys=True)
        )
        self.assertEqual(first["reviewed_rows"], first["need_ids"])
        self.assertEqual(len(first["scenarios"]), 20)
        for need_id, datasets in first["need_datasets"].items():
            self.assertTrue(datasets, need_id)
        self.assertEqual(first["roles"], first["role_defaults"])
        self.assertLessEqual(set(first["journey_properties"]), set(first["properties"]))


if __name__ == "__main__":
    unittest.main()
