"""Epic #165: fixed-seed synthetic fixtures rebuild identically and carry no real-data patterns."""

import json
import re
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from zava_forward.core.insights import STAGE_ORDER
from zava_forward.core.synthetic import privacy, scale_fixture, sensor_backfill, stock_register

SEED = 165
AS_OF = "2026-09-30"
UPRN = re.compile(r"(?<!\d)\d{12}(?!\d)")
# The PAS 2035 case fixture is the scale fixture's retrofit case events (stage, contact, decision).
Records = Callable[..., Any]
homes_of = cast(Records, scale_fixture.homes)
households_of = cast(Records, scale_fixture.households)
events_of = cast(Records, scale_fixture.events)
CASE_KINDS = set(scale_fixture.KINDS)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _build(builder: Callable[[Path], object]) -> tuple[dict[str, bytes], object]:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out"
        result = builder(out)
        return _snapshot(out), result


def _stock(out: Path) -> object:
    return stock_register.write(out, n=25, seed=SEED, as_of=AS_OF)


def _scale(out: Path) -> object:
    return scale_fixture.write(out, n=20, per_home=3, seed=SEED, as_of=AS_OF)


def _readings(out: Path) -> object:
    return sensor_backfill.write(out, homes=3, seed=SEED, days=2, cadence=360, as_of=AS_OF)


BUILDERS = {"stock": _stock, "scale": _scale, "readings": _readings}


def _text(files: dict[str, bytes]) -> str:
    return "\n".join(
        data.decode("utf-8") for name, data in files.items() if name != "manifest.json"
    )


class RepeatedSeedRunsTest(unittest.TestCase):
    def test_each_fixture_is_byte_identical_across_runs(self) -> None:
        for name, builder in BUILDERS.items():
            with self.subTest(fixture=name):
                first, first_manifest = _build(builder)
                second, second_manifest = _build(builder)
                self.assertTrue(first)
                self.assertEqual(first, second)
                self.assertEqual(first_manifest, second_manifest)

    def test_a_different_seed_changes_the_stock_and_household_content(self) -> None:
        base, _ = _build(_scale)
        other, _ = _build(
            lambda out: scale_fixture.write(out, n=20, per_home=3, seed=SEED + 1, as_of=AS_OF)
        )
        self.assertNotEqual(base["households.jsonl"], other["households.jsonl"])
        self.assertNotEqual(base["events.jsonl"], other["events.jsonl"])

    def test_generators_are_record_identical_without_touching_disk(self) -> None:
        self.assertEqual(stock_register.rows(25, SEED), stock_register.rows(25, SEED))
        for generator in (homes_of, households_of):
            self.assertEqual(list(generator(20, SEED)), list(generator(20, SEED)))
        self.assertEqual(list(events_of(20, 3, SEED)), list(events_of(20, 3, SEED)))


class SyntheticProvenanceTest(unittest.TestCase):
    def test_manifests_declare_synthetic_provenance_and_the_seed(self) -> None:
        for name, builder in BUILDERS.items():
            with self.subTest(fixture=name):
                _, manifest = _build(builder)
                self.assertIsInstance(manifest, dict)
                assert isinstance(manifest, dict)
                self.assertEqual(manifest["source_type"], "SYNTHETIC")
                self.assertEqual(manifest["seed"], SEED)
                self.assertTrue(
                    re.fullmatch(r"sha256:[0-9a-f]{64}", manifest["generator_revision"])
                )
                if name != "readings":
                    self.assertRegex(manifest["synthetic_label"], r"(?i)fictional")

    def test_every_stock_household_and_case_record_is_labelled_synthetic(self) -> None:
        files, _ = _build(_scale)
        for name in ("homes.jsonl", "households.jsonl", "events.jsonl"):
            records = [json.loads(line) for line in files[name].decode().splitlines()]
            self.assertEqual(len(records), 20 if name != "events.jsonl" else 60)
            for record in records:
                self.assertIs(record["is_synthetic"], True)
                self.assertEqual(
                    privacy.record_issues(record, scale_home=name == "homes.jsonl"), []
                )
        for record in stock_register.rows(25, SEED):
            self.assertRegex(record["synthetic_home_id"], r"^SYN-\d{5}$")

    def test_case_events_use_pas_2035_style_stages_and_synthetic_references(self) -> None:
        files, _ = _build(_scale)
        stages = set(STAGE_ORDER)
        for line in files["homes.jsonl"].decode().splitlines():
            self.assertIn(json.loads(line)["stage"], stages)
        for line in files["events.jsonl"].decode().splitlines():
            event = json.loads(line)
            self.assertIn(event["kind"], CASE_KINDS)
            self.assertRegex(event["case"], r"^ZF-\d{5}$")
        for line in files["households.jsonl"].decode().splitlines():
            household = json.loads(line)
            for key in ("household_ref", "resident_ref", "tenancy_ref"):
                self.assertIn("-SYN-", household[key])


class NoRealDataPatternsTest(unittest.TestCase):
    def test_no_real_postcode_uprn_or_personal_data_pattern_in_any_fixture(self) -> None:
        for name, builder in BUILDERS.items():
            with self.subTest(fixture=name):
                files, _ = _build(builder)
                text = _text(files)
                self.assertIsNone(UPRN.search(text))
                for label, pattern in privacy.PATTERNS.items():
                    for match in pattern.finditer(text):
                        # Only the reserved fictional TE0-TE8 1ST postcodes may appear.
                        self.assertEqual(label, "uk_postcode")
                        self.assertRegex(match.group(0), r"^TE[0-8] 1ST$")

    def test_scale_postcodes_and_names_are_fictional_only(self) -> None:
        for home in homes_of(60, SEED):
            self.assertRegex(home["postcode"], r"^TE[0-8] 1ST$")
            self.assertTrue(home["address"].endswith("Test Road"))
        for household in households_of(60, SEED):
            self.assertIn(household["lead_resident"], scale_fixture.NAMES)

    def test_privacy_scanner_rejects_real_looking_values(self) -> None:
        for value in ("SW1A 1AA", "AB123456C", "jo@example.org", "07700 900123"):
            self.assertNotEqual(privacy.pattern_issues({"value": value}), [], value)
        self.assertIsNotNone(UPRN.search("uprn 100023336956"))


if __name__ == "__main__":
    unittest.main()
