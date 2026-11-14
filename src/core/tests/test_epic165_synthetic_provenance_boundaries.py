"""Epic #165: synthetic-only provenance, documented boundaries and leak-free benchmark splits."""

import hashlib
import json
import re
import unittest
from collections import defaultdict
from pathlib import Path
from typing import Any

from zava_forward.core.synthetic import scale_fixture, sensor_scenarios
from zava_forward.core.synthetic.scenario_manifest import validate_manifest

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
MANIFEST = json.loads((PACK / "scenario-manifest.json").read_text())
REGISTER = json.loads((PACK / "provenance-register.json").read_text())
EVAL_REGISTRY = json.loads((ROOT / "src/agents/evals/registry.json").read_text())

UPRN = re.compile(r"(?<!\d)\d{11,12}(?!\d)")
POSTCODE = re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}\b")
SYNTHETIC_POSTCODE = re.compile(r"^TE\d 1ST$")
SYNTHETIC_ADDRESS = re.compile(r"^\d+ Test Road$")

SEED = 165
SIZE = 600
CATEGORIES = (
    "normal",
    "exception",
    "safety_escalation",
    "accessibility_language_support",
    "resident_refusal",
    "degraded_telemetry",
)
SUPPORT_ADJUSTMENTS = {"Large print", "Interpreter", "BSL", "Communication support"}


def _category(home: dict[str, Any], household: dict[str, Any]) -> str:
    # Fixed precedence so every case has exactly one category.
    if home["open_safety_issue"]:
        return "safety_escalation"
    if household["works_consent_state"] in ("Declined", "Withdrawn"):
        return "resident_refusal"
    if household["adjustment"] in SUPPORT_ADJUSTMENTS:
        return "accessibility_language_support"
    if (
        household["works_consent_state"] == "Pending"
        or household["representative_state"] == "Claimed - unverified"
    ):
        return "exception"
    return "normal"


def _split(case_id: str) -> str:
    digest = hashlib.sha256(f"{SEED}:{case_id}".encode()).digest()
    return "evaluation" if digest[0] % 2 else "development"


def benchmark(seed: int = SEED) -> list[dict[str, str]]:
    homes = list(scale_fixture.homes(SIZE, seed))  # type: ignore[no-untyped-call]
    households = list(scale_fixture.households(SIZE, seed))  # type: ignore[no-untyped-call]
    cases = [
        {"id": h["id"], "category": _category(h, hh), "split": _split(h["id"])}
        for h, hh in zip(homes, households, strict=True)
    ]
    # Few telemetry cases exist, so alternate them rather than hash them into one split.
    for index, case in enumerate(sensor_scenarios.generate(seed)):
        degraded = case.truth.label in ("sensor_fault", "missing_data")
        cases.append(
            {
                "id": f"SENSOR-{case.case_id}",
                "category": "degraded_telemetry" if degraded else "normal",
                "split": "evaluation" if index % 2 else "development",
            }
        )
    return cases


def _text(path: Path) -> str:
    return path.read_text()


class ProvenanceMetadataTests(unittest.TestCase):
    def test_scenario_manifest_is_synthetic_only_with_documented_boundaries(self) -> None:
        validate_manifest(MANIFEST, ROOT)
        self.assertIs(MANIFEST["is_synthetic"], True)
        self.assertIs(MANIFEST["contains_real_data"], False)
        for field in ("warning", "fixture_provenance", "evidence_semantics", "coverage_note"):
            self.assertTrue(MANIFEST[field].strip(), field)
        self.assertIn("No personal data", MANIFEST["warning"])
        self.assertIn("synthetic", MANIFEST["fixture_provenance"].lower())
        self.assertIn("No private stock, real map anchors", MANIFEST["fixture_provenance"])
        self.assertEqual(MANIFEST["inventory_authority"]["customer_approval"], "not-established")
        self.assertEqual(MANIFEST["inventory_authority"]["owner_approval"], "not-established")

    def test_every_scenario_entry_states_its_boundary(self) -> None:
        entries = MANIFEST["profiles"] + MANIFEST["workflows"]
        self.assertTrue(entries)
        ids = [e["id"] for e in entries]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in entries:
            with self.subTest(entry["id"]):
                self.assertEqual(entry["status"], "unavailable")
                for field in ("reason", "safe_endpoint", "path"):
                    self.assertTrue(entry[field], field)
                self.assertIsInstance(entry["evidence_index"], int)
                self.assertNotRegex(json.dumps(entry), r"(?i)\bapproved\b(?! priority)")

    def test_every_dataset_entry_declares_visibility_and_personal_data_stance(self) -> None:
        datasets = REGISTER["datasets"]
        ids = [d["id"] for d in datasets]
        self.assertEqual(len(ids), len(set(ids)))
        for dataset in datasets:
            with self.subTest(dataset["id"]):
                self.assertIn(dataset["visibility"], ("public", "private"))
                self.assertTrue(dataset["data_dictionary"])
                self.assertTrue(dataset["personal_data"].strip())
                if dataset["visibility"] == "public":
                    self.assertNotIn("potentially personal", dataset["personal_data"].lower())
        for dataset_id in ("DS-SCENARIO-MANIFEST", "DS-COHORT-MANIFEST-DRAFT", "DS-SCALE-FIXTURE"):
            self.assertIn(dataset_id, ids)

    def test_registered_evaluation_datasets_contain_no_real_data(self) -> None:
        self.assertTrue(EVAL_REGISTRY["datasets"])
        for dataset in EVAL_REGISTRY["datasets"]:
            with self.subTest(dataset["id"]):
                self.assertIs(dataset["contains_real_data"], False)
                self.assertTrue(dataset["owner"] and dataset["purpose"] and dataset["version"])
        draft = json.loads((ROOT / "src/agents/evals/cohort_manifest_draft.json").read_text())
        self.assertIs(draft["is_synthetic"], True)
        self.assertIs(draft["fairness_evidence"], False)

    def test_published_metadata_has_no_uprn_real_postcode_or_address(self) -> None:
        paths = [
            PACK / "scenario-manifest.json",
            PACK / "provenance-register.json",
            PACK / "needs-inventory.json",
            ROOT / "src/agents/evals/cohort_manifest_draft.json",
        ]
        for path in paths:
            text = _text(path)
            with self.subTest(path.name):
                self.assertIsNone(UPRN.search(text))
                self.assertEqual(POSTCODE.findall(text), [])

    def test_generated_fixture_identifiers_are_fictional(self) -> None:
        for home in scale_fixture.homes(SIZE, SEED):  # type: ignore[no-untyped-call]
            self.assertIs(home["is_synthetic"], True)
            self.assertRegex(home["address"], SYNTHETIC_ADDRESS)
            self.assertRegex(home["postcode"], SYNTHETIC_POSTCODE)
            self.assertIn(home["resident"], scale_fixture.NAMES)
            self.assertIsNone(UPRN.search(json.dumps(home)))
        for household in scale_fixture.households(SIZE, SEED):  # type: ignore[no-untyped-call]
            self.assertIs(household["is_synthetic"], True)
            for key in ("household_ref", "resident_ref", "tenancy_ref"):
                self.assertIn("SYN", household[key])


class BenchmarkSplitTests(unittest.TestCase):
    def test_benchmark_is_deterministic(self) -> None:
        first, second = benchmark(), benchmark()
        self.assertEqual(first, second)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_both_splits_cover_every_required_category(self) -> None:
        coverage: dict[str, set[str]] = defaultdict(set)
        for case in benchmark():
            coverage[case["split"]].add(case["category"])
        for split in ("development", "evaluation"):
            self.assertEqual(coverage[split], set(CATEGORIES), split)

    def test_no_cross_leakage_between_splits_or_categories(self) -> None:
        cases = benchmark()
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        by_split: dict[str, set[str]] = defaultdict(set)
        for case in cases:
            by_split[case["split"]].add(case["id"])
        self.assertFalse(by_split["development"] & by_split["evaluation"])
        self.assertEqual(len(by_split["development"] | by_split["evaluation"]), len(ids))
        self.assertTrue({c["category"] for c in cases} <= set(CATEGORIES))

    def test_home_assignment_is_stable_when_the_cohort_grows(self) -> None:
        small = {c["id"]: c for c in benchmark() if not c["id"].startswith("SENSOR-")}
        homes = list(scale_fixture.homes(SIZE + 50, SEED))  # type: ignore[no-untyped-call]
        for home in homes[:SIZE]:
            self.assertEqual(small[home["id"]]["split"], _split(home["id"]))

    def test_category_rules_follow_documented_fixture_fields(self) -> None:
        homes = {h["id"]: h for h in scale_fixture.homes(SIZE, SEED)}  # type: ignore[no-untyped-call]
        households = {
            h["home_id"]: h
            for h in scale_fixture.households(SIZE, SEED)  # type: ignore[no-untyped-call]
        }
        for case in benchmark():
            if case["id"].startswith("SENSOR-"):
                continue
            home, household = homes[case["id"]], households[case["id"]]
            if case["category"] == "safety_escalation":
                self.assertTrue(home["open_safety_issue"])
            elif case["category"] == "resident_refusal":
                self.assertIn(household["works_consent_state"], ("Declined", "Withdrawn"))
                self.assertFalse(home["open_safety_issue"])
            elif case["category"] == "accessibility_language_support":
                self.assertIn(household["adjustment"], SUPPORT_ADJUSTMENTS)
            elif case["category"] == "normal":
                self.assertEqual(
                    household["works_consent_state"] in ("Declined", "Withdrawn"), False
                )
                self.assertFalse(home["open_safety_issue"])
                self.assertEqual(household["adjustment"] in SUPPORT_ADJUSTMENTS, False)

    def test_degraded_telemetry_cases_come_from_declared_faults(self) -> None:
        degraded = {
            f"SENSOR-{c.case_id}"
            for c in sensor_scenarios.generate(SEED)
            if c.truth.expected_outcome == sensor_scenarios.INSUFFICIENT
        }
        self.assertTrue(degraded)
        found = {c["id"] for c in benchmark() if c["category"] == "degraded_telemetry"}
        self.assertEqual(found, degraded)
        self.assertEqual(sensor_scenarios.generate(SEED), sensor_scenarios.generate(SEED))


if __name__ == "__main__":
    unittest.main()
