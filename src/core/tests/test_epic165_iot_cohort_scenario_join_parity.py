"""Epic #165: IoT sensor, cohort, stage and scenario fixtures join losslessly on home/case ids."""

import csv
import json
import tempfile
import unittest
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from dataset import DATA
from zava_forward.core.insights import STAGE_ORDER
from zava_forward.core.synthetic import privacy, scale_fixture, sensor_backfill

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/retrofit-synthetic-data"
SEEDS = (165, 166)
SIZE = 12
AS_OF = "2026-09-30"
Records = Callable[..., Any]
homes_of = cast(Records, scale_fixture.homes)
households_of = cast(Records, scale_fixture.households)
events_of = cast(Records, scale_fixture.events)
sensor_for = cast(Records, sensor_backfill.sensor_for)


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _pack(name: str) -> list[dict[str, str]]:
    return _csv(PACK / name)


def _streams(seed: int) -> tuple[dict[str, bytes], list[dict[str, str]], list[dict[str, str]]]:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out"
        sensor_backfill.write(out, homes=SIZE, seed=seed, days=2, cadence=360, as_of=AS_OF)
        files = {p.name: p.read_bytes() for p in sorted(out.iterdir())}
        sensors = _csv(out / "sensors.csv")
        readings = [row for p in sorted(out.glob("readings-*.csv")) for row in _csv(p)]
    return files, sensors, readings


def _cohort(seed: int) -> dict[str, Any]:
    homes = list(homes_of(SIZE, seed))
    return {
        "homes": homes,
        "households": list(households_of(SIZE, seed)),
        "events": list(events_of(SIZE, 3, seed)),
        "sensors": [sensor_for(h, seed) for h in homes],
    }


class SensorCohortJoinTests(unittest.TestCase):
    def test_every_stream_joins_a_home_with_no_orphans_or_gaps(self) -> None:
        for seed in SEEDS:
            with self.subTest(seed=seed):
                cohort = _cohort(seed)
                _, sensors, readings = _streams(seed)
                home_ids = [h["id"] for h in cohort["homes"]]
                self.assertEqual(len(home_ids), len(set(home_ids)))
                self.assertEqual([s["home_id"] for s in sensors], home_ids)
                self.assertEqual([h["home_id"] for h in cohort["households"]], home_ids)
                self.assertEqual({e["case"] for e in cohort["events"]}, set(home_ids))
                sensor_ids = {s["sensor_id"] for s in sensors}
                self.assertEqual(len(sensor_ids), SIZE)
                self.assertEqual({r["sensor_id"] for r in readings}, sensor_ids)
                by_sensor = {s["sensor_id"]: s["home_id"] for s in sensors}
                self.assertTrue(readings)
                for row in readings:
                    self.assertEqual(row["home_id"], by_sensor[row["sensor_id"]], row["reading_id"])
                self.assertEqual({r["home_id"] for r in readings}, set(home_ids))
                self.assertEqual(
                    {r["source_type"] for r in readings} | {s["source_type"] for s in sensors},
                    {"SYNTHETIC"},
                )

    def test_sensor_register_matches_the_cohort_fabric_draw(self) -> None:
        for seed in SEEDS:
            with self.subTest(seed=seed):
                _, sensors, _ = _streams(seed)
                for drawn, written in zip(_cohort(seed)["sensors"], sensors, strict=True):
                    for key in ("sensor_id", "home_id", "dwelling_type", "age_band"):
                        self.assertEqual(written[key], drawn[key], key)

    def test_pas_2035_stage_state_is_valid_and_travels_with_each_home(self) -> None:
        cohort = _cohort(SEEDS[0])
        for home in cohort["homes"]:
            self.assertIn(home["stage"], STAGE_ORDER, home["id"])
            self.assertTrue(home["is_synthetic"])
        self.assertEqual({e["kind"] for e in cohort["events"]} - set(scale_fixture.KINDS), set())
        counts = Counter(e["case"] for e in cohort["events"])
        self.assertEqual(set(counts.values()), {3})


class ArchetypeAndScenarioJoinTests(unittest.TestCase):
    def test_property_archetypes_and_epc_bands_are_consistent_and_joined(self) -> None:
        properties = _pack("property-register.csv")
        ids = [r["property_id"] for r in properties]
        self.assertEqual(len(ids), len(set(ids)))
        labels: dict[str, set[str]] = {}
        for row in properties:
            labels.setdefault(row["archetype_id"], set()).add(row["archetype_label"])
            self.assertIn(row["current_epc"].strip().upper(), set("ABCDEFG"), row["property_id"])
            self.assertEqual(row["is_synthetic"], "true")
        self.assertTrue(all(len(v) == 1 for v in labels.values()), labels)
        for journey in _pack("resident-journey.csv"):
            self.assertIn(journey["property_ref"], ids, journey["candidate_id"])

    def test_manifest_cases_needs_and_datasets_resolve_without_orphans(self) -> None:
        manifest = json.loads((PACK / "scenario-manifest.json").read_text())
        inventory = json.loads((PACK / "needs-inventory.json").read_text())
        register = json.loads((PACK / "provenance-register.json").read_text())
        fixture = {c["id"]: c for c in DATA["cases"]}
        case_ids = manifest["fixture_contract"]["case_ids"]
        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertLessEqual(set(case_ids), set(fixture))
        for case_id in case_ids:
            self.assertIn(fixture[case_id]["stage"], STAGE_ORDER, case_id)
        generated = {h["id"] for h in homes_of(SIZE, SEEDS[0])}
        self.assertFalse(set(case_ids) & generated)
        need_ids = [n["id"] for n in inventory["needs"]]
        self.assertEqual(manifest["inventory"]["reviewed_rows"], need_ids)
        datasets = {d["id"] for d in register["datasets"]}
        for need in inventory["needs"]:
            self.assertTrue(need["dataset_ids"], need["id"])
            self.assertLessEqual(set(need["dataset_ids"]), datasets, need["id"])
        sensor_need = next(n for n in inventory["needs"] if n["id"] == "SN-09")
        self.assertTrue(set(sensor_need["dataset_ids"]) & datasets)


class PrivacyAndReplayTests(unittest.TestCase):
    def test_generated_records_and_pack_rows_carry_no_real_person_patterns(self) -> None:
        cohort = _cohort(SEEDS[0])
        _, sensors, readings = _streams(SEEDS[0])
        self.assertEqual(privacy.pattern_issues(sensors), [])
        self.assertEqual(privacy.pattern_issues(readings), [])
        for key in ("households", "events", "sensors"):
            self.assertEqual(privacy.pattern_issues(cohort[key]), [], key)
        for home in cohort["homes"]:
            self.assertEqual(privacy.pattern_issues(home, scale_home=True), [], home["id"])
        for name in ("property-register.csv", "resident-journey.csv"):
            self.assertEqual(privacy.pattern_issues(_pack(name)), [], name)

    def test_replay_is_deterministic_per_seed_and_differs_across_seeds(self) -> None:
        first, second, other = (_streams(s)[0] for s in (SEEDS[0], SEEDS[0], SEEDS[1]))
        self.assertEqual(first, second)
        self.assertNotEqual(first["readings-0000.csv"], other["readings-0000.csv"])
        self.assertEqual(_cohort(SEEDS[0]), _cohort(SEEDS[0]))
        one, two = _cohort(SEEDS[0]), _cohort(SEEDS[1])
        self.assertNotEqual(one["homes"], two["homes"])
        self.assertEqual([h["id"] for h in one["homes"]], [h["id"] for h in two["homes"]])


if __name__ == "__main__":
    unittest.main()
