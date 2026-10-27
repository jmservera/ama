"""Synthetic engineering checks; actual #111/#133 integration is not claimed."""

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from typing import ClassVar

from zava_forward.core.synthetic import sensor_faults
from zava_forward.core.synthetic import sensor_scenarios as ss


def files(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()
    }


class SensorScenarioTests(unittest.TestCase):
    cases: ClassVar[tuple[ss.Case, ...]]
    window: ClassVar[ss.Window]

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = ss.generate()
        cls.window = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))

    def test_inventory_seeds_labels_and_outcomes(self) -> None:
        self.assertEqual(len(self.cases), 11)
        self.assertEqual(
            {case.truth.label for case in self.cases},
            {
                "normal",
                "condensation_prone",
                "sustained_high_humidity",
                "repeated_overnight_peaks",
                "sensor_fault",
                "missing_data",
                "seasonal_shift",
                "improvement",
                "no_change",
                "delayed_effect",
                "adverse_effect",
            },
        )
        for case in self.cases:
            with self.subTest(case=case.truth.label):
                self.assertEqual(case.truth.seed, ss.SEED)
                self.assertTrue(case.truth.rng_key)
                self.assertTrue(case.truth.expected_outcome)
                if case.truth.family == "damp":
                    self.assertEqual(
                        ss.analyse(case.rows, self.window).status, case.truth.expected_outcome
                    )

    def test_same_seed_repeats_and_different_seed_changes_observations(self) -> None:
        self.assertEqual(self.cases, ss.generate())
        self.assertNotEqual(self.cases[0].rows, ss.generate(191)[0].rows)

    def test_observation_contract_and_truth_independence(self) -> None:
        for case in self.cases:
            for row in case.rows:
                self.assertEqual(set(row), set(sensor_faults.READING_FIELDS))
                self.assertEqual(row["source_type"], "SYNTHETIC")
                self.assertEqual(row["seed"], str(ss.SEED))
                self.assertEqual(row["scenario"], "SCENARIO_PACK")
        original = self.cases[2]
        changed = [
            {
                **row,
                "home_id": "OTHER",
                "sensor_id": "OTHER",
                "seed": "999",
                "reading_id": f"OTHER-{index}",
                "scenario": "OTHER",
            }
            for index, row in enumerate(original.rows)
        ]
        self.assertEqual(ss.analyse(original.rows, self.window), ss.analyse(changed, self.window))
        modified = replace(original, truth=replace(original.truth, expected_outcome=ss.NO_SIGNAL))
        evaluation = ss.report((modified,))
        checks = evaluation["checks"]
        assert isinstance(checks, list)
        self.assertEqual(checks[0]["status"], "FAIL")
        self.assertEqual(checks[0]["observed"]["status"], ss.REVIEW)

    def test_confusion_population_and_sensitivity_use_fixed_truth(self) -> None:
        evaluation = ss.report(self.cases)
        confusion = evaluation["confusion"]
        assert isinstance(confusion, dict)
        for key, value in {
            "total": 7,
            "eligible": 5,
            "binary_classified": 5,
            "abstained": 0,
            "expected_insufficient": 2,
            "correct_insufficient": 2,
            "incorrect_insufficient": 0,
            "tp": 3,
            "tn": 2,
            "fp": 0,
            "fn": 0,
        }.items():
            self.assertEqual(confusion[key], value, key)
        checks, sensitivity = evaluation["checks"], evaluation["sensitivity"]
        assert isinstance(checks, list) and isinstance(sensitivity, list)
        self.assertEqual(len(checks), 15)
        self.assertTrue(all(check["status"] == "PASS" for check in checks))
        self.assertEqual([x["humidity_threshold_pct"] for x in sensitivity], [70, 75, 85])
        self.assertGreater(sensitivity[-1]["confusion"]["fn"], 0)
        self.assertEqual(sensitivity[-1]["confusion"]["eligible"], 5)

    def test_confusion_miss_false_alert_abstention_and_wrong_sufficiency(self) -> None:
        counts = ss.confusion(
            [ss.REVIEW, ss.NO_SIGNAL, ss.REVIEW, ss.INSUFFICIENT],
            [ss.NO_SIGNAL, ss.REVIEW, ss.INSUFFICIENT, ss.NO_SIGNAL],
        )
        self.assertEqual(
            {
                key: counts[key]
                for key in (
                    "total",
                    "eligible",
                    "fp",
                    "fn",
                    "abstained",
                    "incorrect_insufficient",
                    "binary_classified",
                )
            },
            {
                "total": 4,
                "eligible": 3,
                "fp": 1,
                "fn": 1,
                "abstained": 1,
                "incorrect_insufficient": 1,
                "binary_classified": 2,
            },
        )
        self.assertEqual(counts["miss_rate_among_classified_positives"], 1)
        self.assertEqual(counts["false_alert_rate_among_classified_negatives"], 1)
        for expected, predicted in (([], []), ([ss.REVIEW], [ss.INSUFFICIENT])):
            empty = ss.confusion(expected, predicted)
            self.assertIsNone(empty["miss_rate_among_classified_positives"])
            self.assertIsNone(empty["false_alert_rate_among_classified_negatives"])
        for expected, predicted in (([ss.REVIEW], []), (["UNKNOWN"], [ss.REVIEW])):
            with self.assertRaises(ValueError):
                ss.confusion(expected, predicted)

    def test_fault_missing_and_invalid_observations_never_reassure(self) -> None:
        for index, reason in ((4, "FLATLINE"), (5, "WINDOW_COVERAGE")):
            result = ss.analyse(self.cases[index].rows, self.window)
            self.assertEqual(result.status, ss.INSUFFICIENT)
            self.assertIn(reason, result.reasons)
            self.assertIsNone(result.mean_temperature_c)
        rows = list(self.cases[0].rows)
        mutations = (
            {"temperature_c": "nan"},
            {"humidity_pct": "101"},
            {"temperature_unit": "degF"},
            {"calibrated": "false"},
            {"source_type": "REAL"},
            {"schema_version": "unknown"},
            {"observed_at": "bad"},
            {"observed_at": "2023-01-01T00:00:00Z"},
            {"observed_at": "2024-01-01T00:01:00Z"},
            {"temperature_c": "1e9999"},
            {"sensor_id": "different"},
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                broken = [{**rows[0], **mutation}, *rows[1:]]
                self.assertEqual(ss.analyse(broken, self.window).status, ss.INSUFFICIENT)
        for candidate in ((rows[0], *rows), tuple(reversed(rows)), ({}, *rows[1:]), ()):
            self.assertEqual(ss.analyse(candidate, self.window).status, ss.INSUFFICIENT)

    def test_gap_distribution_changes_sufficiency_not_just_overall_coverage(self) -> None:
        rows = list(self.cases[0].rows)
        distributed = [row for index, row in enumerate(rows) if index % 24 != 12]
        concentrated = rows[28:]
        a = ss.analyse(distributed, self.window)
        b = ss.analyse(concentrated, self.window)
        self.assertEqual(a.valid, b.valid)
        self.assertGreater(b.coverage, 0.9)
        self.assertEqual(a.status, ss.NO_SIGNAL)
        self.assertEqual(b.status, ss.INSUFFICIENT)
        self.assertIn("DAY_COVERAGE", b.reasons)
        overnight_gap = rows[:1] + rows[2:]
        self.assertIn("NIGHT_COVERAGE", ss.analyse(overnight_gap, self.window).reasons)

    def test_persistence_exact_boundary_and_gap_breaks_run(self) -> None:
        window = ss.Window(ss.START, ss.START + timedelta(days=1))
        baseline = list(self.cases[0].rows[:24])
        rows = [
            {**row, "humidity_pct": "75.00" if 6 <= index < 18 else "55.00"}
            for index, row in enumerate(baseline)
        ]
        exact = ss.analyse(rows, window)
        self.assertEqual(exact.longest_high_hours, 12)
        self.assertEqual(exact.status, ss.REVIEW)
        self.assertEqual(ss.analyse(rows, window, humidity_threshold=75.01).status, ss.NO_SIGNAL)
        broken = ss.analyse(rows[:12] + rows[13:], window)
        self.assertEqual(broken.status, ss.NO_SIGNAL)
        self.assertEqual(broken.longest_high_hours, 6)

    def test_overnight_utc_boundaries_and_repeat_count(self) -> None:
        window = ss.Window(ss.START, ss.START + timedelta(days=3))
        baseline = self.cases[0].rows[:72]
        for hours, expected in (((0, 1, 5), ss.REVIEW), ((0, 1, 6), ss.NO_SIGNAL)):
            rows = [
                {**row, "humidity_pct": "80" if index % 24 in hours else "55"}
                for index, row in enumerate(baseline)
            ]
            result = ss.analyse(rows, window)
            self.assertEqual(result.status, expected)
            self.assertEqual(result.high_nights, 3 if expected == ss.REVIEW else 0)

    def test_retrofit_deltas_exact_activation_delay_and_no_change(self) -> None:
        measure_at = ss.START + timedelta(days=14)
        for case in self.cases[7:]:
            with self.subTest(case=case.truth.label):
                result = ss.retrofit_comparison(case.rows, measure_at)
                self.assertEqual(result["status"], "SUFFICIENT")
                deltas = result["deltas"]
                assert isinstance(deltas, dict)
                for name in ("early", "late"):
                    expected_t = case.truth.temperature_delta_c
                    expected_h = case.truth.humidity_delta_points
                    if name == "early" and case.truth.delay_days:
                        expected_t = expected_h = 0.0
                    self.assertAlmostEqual(deltas[name]["temperature_c"], expected_t, delta=0.02)
                    self.assertAlmostEqual(deltas[name]["humidity_points"], expected_h, delta=0.02)
                activation = (14 + case.truth.delay_days) * 24
                before, after = case.rows[activation - 1], case.rows[activation]
                prior_before, prior_after = (
                    case.rows[activation - 1 - 168],
                    case.rows[activation - 168],
                )
                self.assertEqual(before["temperature_c"], prior_before["temperature_c"])
                self.assertAlmostEqual(
                    float(after["temperature_c"]) - float(prior_after["temperature_c"]),
                    case.truth.temperature_delta_c,
                    delta=0.02,
                )

    def test_retrofit_insufficient_week_has_null_deltas(self) -> None:
        case = self.cases[7]
        rows = case.rows[: 14 * 24] + case.rows[15 * 24 :]
        result = ss.retrofit_comparison(rows, ss.START + timedelta(days=14))
        self.assertEqual(result["status"], ss.INSUFFICIENT)
        whole = result["whole"]
        assert isinstance(whole, dict)
        self.assertGreater(whole["coverage"], 0.9)
        self.assertEqual(result["deltas"], {"early": None, "late": None})
        malformed = ss.retrofit_comparison(({}, *case.rows[1:]), ss.START + timedelta(days=14))
        self.assertEqual(malformed["status"], ss.INSUFFICIENT)
        self.assertEqual(malformed["deltas"], {"early": None, "late": None})

    def test_snapshot_bytes_hashes_schema_and_no_truth_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = ss.write(root / "a")
            ss.write(root / "b")
            self.assertEqual(files(root / "a"), files(root / "b"))
            self.assertEqual(json.loads((root / "a/truth/report.json").read_text()), first)
            manifest = json.loads((root / "a/truth/manifest.json").read_text())
            self.assertEqual(manifest["rows"], 6888)
            self.assertEqual(manifest["case_count"], 11)
            self.assertIn("NOT the ERA5", manifest["weather"])
            self.assertTrue(manifest["generator_revision"].startswith("sha256:"))
            for name, digest in manifest["file_sha256"].items():
                self.assertEqual(
                    hashlib.sha256((root / "a" / name).read_bytes()).hexdigest(), digest
                )
            for name, payload in files(root / "a/analysis").items():
                for case in self.cases:
                    self.assertNotIn(case.truth.label, name)
                    self.assertNotIn(case.truth.label.encode(), payload)
                self.assertNotIn(b"expected", payload)
                self.assertNotIn(b"rng_key", payload)
            with (root / "a/analysis/C01.csv").open() as stream:
                reader = csv.DictReader(stream)
                self.assertEqual(reader.fieldnames, list(sensor_faults.READING_FIELDS))
                retained = list(reader)
            self.assertEqual(
                ss.analyse(retained, self.window), ss.analyse(self.cases[0].rows, self.window)
            )
            changed = ss.write(root / "c", humidity_threshold=85)
            self.assertNotEqual(first["rules"], changed["rules"])
            self.assertNotEqual(first["confusion"], changed["confusion"])
            self.assertEqual(first["input_sha256"], changed["input_sha256"])

    def test_output_refuses_repositories_worktrees_files_nonempty_and_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            worktree = root / "worktree"
            repo.mkdir()
            (repo / ".git").mkdir()
            worktree.mkdir()
            (worktree / ".git").write_text("gitdir: fictional\n")
            occupied = root / "occupied"
            occupied.mkdir()
            (occupied / "keep").write_text("unchanged")
            regular = root / "file"
            regular.write_text("unchanged")
            link = root / "link"
            link.symlink_to(root / "target", target_is_directory=True)
            for path in (repo / "out", worktree / "out", occupied, regular, link, link / "out"):
                with self.subTest(path=path), self.assertRaises((ValueError, FileExistsError)):
                    ss.write(path)
            self.assertEqual((occupied / "keep").read_text(), "unchanged")
            self.assertEqual(regular.read_text(), "unchanged")
            self.assertFalse((repo / "out").exists())
            self.assertFalse((worktree / "out").exists())
            self.assertFalse((root / "target").exists())

    def test_bad_parameters_fail_before_creating_output(self) -> None:
        for seed in (-1, 2**63, True, 1.2):
            with self.assertRaises(ValueError):
                ss.generate(seed)  # type: ignore[arg-type]
        for start, end in (
            (ss.START.replace(tzinfo=None), ss.START + timedelta(days=1)),
            (ss.START, ss.START),
            (ss.START, ss.START + timedelta(days=29)),
            (ss.START, ss.START + timedelta(hours=25)),
        ):
            with self.assertRaises(ValueError):
                ss.Window(start, end)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out"
            for threshold in (-1, 101, float("nan"), float("inf"), True):
                with self.assertRaises(ValueError):
                    ss.write(out, humidity_threshold=threshold)
                self.assertFalse(out.exists())

    def test_installed_cli_success_failure_and_check_failure_exit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            command = [sys.executable, "-m", "zava_forward.core.synthetic.sensor_scenarios"]
            success = subprocess.run(
                [*command, "--out", str(root / "good")], capture_output=True, text=True, check=False
            )
            self.assertEqual(success.returncode, 0, success.stderr)
            payload = json.loads(success.stdout)
            self.assertEqual(len(payload["checks"]), 15)
            failed_check = subprocess.run(
                [*command, "--out", str(root / "sensitive"), "--humidity-threshold", "85"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(failed_check.returncode, 1)
            self.assertTrue((root / "sensitive/truth/report.json").is_file())
            bad = subprocess.run(
                [*command, "--out", str(root / "bad"), "--seed", "-1"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(bad.returncode, 2)
            self.assertIn("Seed must", bad.stderr)
            self.assertFalse((root / "bad").exists())


if __name__ == "__main__":
    unittest.main()
