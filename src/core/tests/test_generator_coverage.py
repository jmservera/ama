"""Gap routing is engineering metadata, never generator or owner acceptance."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic.coverage import build_baseline, check_register_labels

ROOT = Path(__file__).resolve().parents[3]
INVENTORY = ROOT / "docs/reference/research/retrofit-synthetic-data/needs-inventory.json"


class GeneratorCoverageTests(unittest.TestCase):
    def test_merged_baseline_preserves_all_rows_and_pending_items(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        report = build_baseline(inventory)
        self.assertEqual(report["coverage_counts"], {"covered": 2, "partial": 11, "missing": 0})
        self.assertEqual(
            report["needs"],
            [
                {key: row[key] for key in ("id", "need", "coverage", "gap_closure")}
                for row in inventory["needs"]
            ],
        )
        self.assertEqual(report["inventory_version"], inventory["version"])
        self.assertEqual(report["review_date"], inventory["review_date"])
        self.assertEqual(report["inventory_status"], "draft-awaiting-owner-review")
        self.assertEqual(report["open_items"], inventory["open_items"])
        self.assertEqual(
            report["declared_generator_conventions"], inventory["generator_conventions"]
        )
        self.assertNotIn("routing_validated", report)
        self.assertIs(report["routing_shape_validated"], True)
        self.assertEqual(report["issue_existence"], "not-assessed")
        self.assertEqual(report["open_gaps"], [])
        self.assertEqual(report["generator_output_conformance"], "not-assessed")
        self.assertEqual(report["owner_approval"], "not-established")
        self.assertEqual(report["application_acceptance"], "not-assessed")

    def test_report_does_not_mutate_inventory_and_orders_rows_and_issues(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        for need in inventory["needs"][:2]:
            need["coverage"] = "missing"
        original = copy.deepcopy(inventory)
        expected = build_baseline(inventory)
        self.assertEqual(expected["open_gaps"], ["SN-01", "SN-02"])
        self.assertEqual(inventory, original)
        inventory["needs"].reverse()
        for need in inventory["needs"]:
            need["gap_closure"]["issues"].reverse()
        self.assertEqual(build_baseline(inventory), expected)

    def test_child_delivered_and_justified_deferral(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        inventory["needs"][0]["coverage"] = "missing"
        inventory["needs"][0]["gap_closure"] = {
            "kind": "deferred",
            "issues": [],
            "note": "Constructed test rationale only; not an owner decision.",
        }
        report = build_baseline(inventory)
        self.assertEqual(report["coverage_counts"], {"covered": 2, "partial": 10, "missing": 1})
        self.assertEqual(report["open_gaps"], ["SN-01"])

    def test_covered_and_delivered_must_agree_in_both_directions(self) -> None:
        for coverage, kind in (
            ("covered", "child"),
            ("covered", "deferred"),
            ("partial", "delivered"),
            ("missing", "delivered"),
        ):
            with self.subTest(coverage=coverage, kind=kind):
                inventory = json.loads(INVENTORY.read_text())
                inventory["needs"][0]["coverage"] = coverage
                inventory["needs"][0]["gap_closure"]["kind"] = kind
                with self.assertRaisesRegex(ValueError, "SN-01:.*delivered"):
                    build_baseline(inventory)

    def test_review_mutations_have_honest_reports_and_cli_exit_status(self) -> None:
        inventory = json.loads(INVENTORY.read_text())
        unknown = copy.deepcopy(inventory)
        unknown["needs"][0]["gap_closure"]["issues"] = ["#99999"]
        deferred = copy.deepcopy(inventory)
        deferred["needs"][0]["gap_closure"] = {
            "kind": "deferred",
            "issues": [],
            "note": "Constructed test deferral, not owner approval.",
        }
        covered_child = copy.deepcopy(inventory)
        covered_child["needs"][0]["coverage"] = "covered"
        missing = copy.deepcopy(inventory)
        missing["needs"][0]["coverage"] = "missing"
        command = [sys.executable, "-m", "zava_forward.core.synthetic.coverage"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metadata.json"
            for label, value, exit_code, gaps in (
                ("unknown route", unknown, 0, []),
                ("partial deferral", deferred, 1, ["SN-01"]),
                ("covered child", covered_child, 1, None),
                ("missing child", missing, 1, ["SN-01"]),
            ):
                with self.subTest(mutation=label):
                    path.write_text(json.dumps(value), encoding="utf-8")
                    result = subprocess.run([*command, str(path)], capture_output=True, check=False)
                    self.assertEqual(result.returncode, exit_code)
                    if gaps is None:
                        with self.assertRaisesRegex(ValueError, "covered.*delivered"):
                            build_baseline(value)
                        self.assertEqual(result.stdout, b"")
                        self.assertIn(b"coverage:", result.stderr)
                    else:
                        report = build_baseline(value)
                        self.assertEqual(json.loads(result.stdout), report)
                        self.assertEqual(report["open_gaps"], gaps)
                        self.assertNotIn("routing_validated", report)
                        self.assertIs(report["routing_shape_validated"], True)
                        self.assertEqual(report["issue_existence"], "not-assessed")
                        self.assertEqual(result.stderr, b"")

    def test_rejects_invalid_rows(self) -> None:
        mutations: tuple[tuple[str, object], ...] = (
            ("id", "SN-00"),
            ("id", "SN-1"),
            ("id", "SN-02"),
            ("id", None),
            ("need", " \n"),
            ("coverage", "approved"),
            ("coverage", None),
            ("gap_closure", None),
        )
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                inventory = json.loads(INVENTORY.read_text())
                inventory["needs"][0][field] = value
                with self.assertRaises(ValueError):
                    build_baseline(inventory)

    def test_rejects_invalid_closure_and_unjustified_deferral(self) -> None:
        mutations: tuple[tuple[str, object], ...] = (
            ("kind", "approved"),
            ("kind", "delivered"),
            ("note", ""),
            ("note", " \n"),
            ("issues", []),
            ("issues", "#168"),
            ("issues", [168]),
            ("issues", ["#0"]),
            ("issues", ["168"]),
            ("issues", ["https://example.test/issues/168"]),
            ("issues", ["#168", "#168"]),
        )
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                inventory = json.loads(INVENTORY.read_text())
                inventory["needs"][0]["gap_closure"][field] = value
                with self.assertRaises(ValueError):
                    build_baseline(inventory)
        inventory = json.loads(INVENTORY.read_text())
        inventory["needs"][0]["gap_closure"] = {"kind": "deferred", "issues": [], "note": " "}
        with self.assertRaisesRegex(ValueError, "SN-01.gap_closure.note"):
            build_baseline(inventory)

    def test_rejects_invalid_top_level_metadata_and_conventions(self) -> None:
        mutations: tuple[tuple[str, object], ...] = (
            ("version", " "),
            ("review_date", "2026-02-30"),
            ("review_date", "20261015"),
            ("status", None),
            ("needs", []),
            ("needs", {}),
            ("needs", [None]),
            ("open_items", None),
            ("open_items", [" "]),
            ("generator_conventions", {}),
        )
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                inventory = json.loads(INVENTORY.read_text())
                inventory[field] = value
                with self.assertRaises(ValueError):
                    build_baseline(inventory)
        for field in ("reuse_rule", "seed", "identifiers", "is_synthetic"):
            inventory = json.loads(INVENTORY.read_text())
            inventory["generator_conventions"][field] = " "
            with self.subTest(convention=field), self.assertRaises(ValueError):
                build_baseline(inventory)
        for value in (None, [], {1: "not a JSON object key"}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build_baseline(value)

    def test_cli_success_is_repeatable_and_bad_input_has_no_success_output(self) -> None:
        command = [sys.executable, "-m", "zava_forward.core.synthetic.coverage"]
        first = subprocess.run([*command, str(INVENTORY)], capture_output=True, check=True)
        second = subprocess.run([*command, str(INVENTORY)], capture_output=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(
            json.loads(first.stdout), build_baseline(json.loads(INVENTORY.read_text()))
        )
        self.assertEqual(first.stderr, b"")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "metadata.json"
            for payload in (b"not json", b"\xff", b"{}", b'{"needs": []}'):
                path.write_bytes(payload)
                failed = subprocess.run([*command, str(path)], capture_output=True, check=False)
                self.assertNotEqual(failed.returncode, 0)
                self.assertEqual(failed.stdout, b"")
                self.assertIn(b"coverage:", failed.stderr)
            path.unlink()
            missing = subprocess.run([*command, str(path)], capture_output=True, check=False)
            self.assertNotEqual(missing.returncode, 0)
            self.assertEqual(missing.stdout, b"")
            self.assertIn(b"coverage:", missing.stderr)


class RegisterLabelTests(unittest.TestCase):
    def _csv(self, text: str) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "register.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_all_rows_labelled(self) -> None:
        path = self._csv("synthetic_home_id,is_synthetic\nSYN-1,True\nSYN-2,true\n")
        result = check_register_labels(path)
        self.assertEqual(
            result,
            {"rows": 2, "labelled": 2, "unlabelled": 0, "missing_column": False, "conforms": True},
        )

    def test_unlabelled_missing_column_and_empty_do_not_conform(self) -> None:
        mixed = check_register_labels(self._csv("id,is_synthetic\nA,True\nB,False\nC,\n"))
        self.assertEqual((mixed["labelled"], mixed["unlabelled"], mixed["conforms"]), (1, 2, False))
        no_column = check_register_labels(self._csv("id\nA\n"))
        self.assertIs(no_column["missing_column"], True)
        self.assertIs(no_column["conforms"], False)
        self.assertIs(check_register_labels(self._csv("id,is_synthetic\n"))["conforms"], False)

    def test_duplicate_column_names_are_rejected(self) -> None:
        path = self._csv("id,is_synthetic,is_synthetic\nSYN-1,False,True\n")
        with self.assertRaises(ValueError):
            check_register_labels(path)

    def test_unterminated_quote_is_rejected(self) -> None:
        path = self._csv('id,note,is_synthetic\nA,"open,True\nB,x,False\n')
        with self.assertRaises(ValueError):
            check_register_labels(path)

    def test_malformed_header_and_row_width_are_rejected(self) -> None:
        for text in (
            'id,"is_synthetic\nA,True\n',
            "id,note,is_synthetic\nSYN-1,unquoted,True,False\n",
            "id,note,is_synthetic\nSYN-1,True\n",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                check_register_labels(self._csv(text))

    def test_cli_reports_aggregate_only_and_fails_on_nonconforming(self) -> None:
        command = [sys.executable, "-m", "zava_forward.core.synthetic.coverage", str(INVENTORY)]
        good = self._csv("id,is_synthetic\nSECRET-A,True\n")
        ok = subprocess.run([*command, "--register", str(good)], capture_output=True, check=False)
        self.assertEqual(ok.returncode, 0)
        self.assertIs(json.loads(ok.stdout)["register_label_conformance"]["conforms"], True)
        self.assertNotIn(b"SECRET-A", ok.stdout)
        bad = self._csv("id,is_synthetic\nSECRET-B,False\n")
        failed = subprocess.run(
            [*command, "--register", str(bad)], capture_output=True, check=False
        )
        self.assertEqual(failed.returncode, 1)
        self.assertIn("register-is_synthetic", json.loads(failed.stdout)["open_gaps"])
        self.assertNotIn(b"SECRET-B", failed.stdout)


if __name__ == "__main__":
    unittest.main()
