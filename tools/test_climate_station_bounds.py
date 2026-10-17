"""Wholly synthetic tiny fixtures for the offline monthly station analysis."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from climate_station_bounds import analyze


HEADER = """Synthetic Test Site
Location: 0E 0N, Lat 0 Lon 0, 0 metres amsl
Estimated data is marked with a * after the value.
Missing data is marked by ---.
Sunshine sensor marker is #.
yyyy mm tmax tmin af rain sun
degC degC days mm hours
"""


def report(rows: str, **overrides) -> dict:
    raw = (HEADER + rows).encode()
    options = {
        "source_url": "https://example.invalid/synthetic.txt",
        "retrieved_on": "2026-10-17",
        "expected_sha256": hashlib.sha256(raw).hexdigest(),
        "start_year": 2000, "end_year": 2000,
    }
    options.update(overrides)
    return analyze(raw, **options)


class StationBoundsTests(unittest.TestCase):
    def test_extrema_ties_pairing_and_provenance(self):
        result = report(
            "1999 12 8 1 0 0 0\n"
            "2000 1 4 -2 0 0 0\n"
            "2000 2 4 -2 0 0 0\n"
            "2000 3 10 2 0 0 0\n"
        )
        self.assertEqual(result["window"]["expected_months"], 12)
        self.assertEqual(result["window"]["present_months"], 3)
        self.assertEqual(result["window"]["outside_window_rows"], 1)
        self.assertEqual(len(result["window"]["absent_months"]), 9)
        self.assertFalse(result["window"]["calendar_complete"])
        tmin = result["temperature"]["tmin"]["minimum"]
        self.assertEqual(tmin["value"], -2)
        self.assertEqual(tmin["occurrences"], [
            {"month": "2000-01", "source_line": 9},
            {"month": "2000-02", "source_line": 10},
        ])
        self.assertEqual(result["temperature"]["midpoint"]["maximum"]["value"], 6)
        self.assertEqual(result["source"]["station"], "Synthetic Test Site")
        self.assertEqual(result["source"]["retrieved_on"], "2026-10-17")
        self.assertEqual(result["humidity"]["status"], "unavailable")
        self.assertEqual(result["owner_reuse_approval"], "UNMET")
        self.assertEqual(result, report(
            "1999 12 8 1 0 0 0\n2000 1 4 -2 0 0 0\n"
            "2000 2 4 -2 0 0 0\n2000 3 10 2 0 0 0\n"
        ))
        json.dumps(result, allow_nan=False)

    def test_quality_counts_are_exclusive_and_fields_independent(self):
        result = report(
            "2000 1 10* 2 0 0 0\n"
            "2000 2 8 --- 0 0 0\n"
            "2000 3 --- 2* 0 0 0 Provisional\n"
            "2000 4 --- 1* 0 0 0\n"
            "2000 5 8 2 0 0 0\n"
        )
        self.assertEqual(result["temperature"]["tmax"]["counts"], {
            "valid": 2, "estimated": 1, "missing": 1, "provisional": 1,
        })
        self.assertEqual(result["temperature"]["tmin"]["counts"], {
            "valid": 2, "estimated": 1, "missing": 1, "provisional": 1,
        })
        for key in ("tmax", "tmin"):
            self.assertEqual(sum(result["temperature"][key]["counts"].values()), 5)
        self.assertEqual(result["temperature"]["midpoint"]["counts"],
                         {"valid": 1, "excluded": 4})
        self.assertEqual(result["temperature"]["midpoint"]["minimum"]["value"], 5)

    def test_empty_field_and_pair_are_explicitly_unavailable(self):
        result = report("2000 1 --- 1 0 0 0\n2000 2 --- 2 0 0 0\n")
        for key in ("tmax", "midpoint"):
            self.assertEqual(result["temperature"][key]["status"], "unavailable")
            self.assertIsNone(result["temperature"][key]["minimum"])
            self.assertIsNone(result["temperature"][key]["maximum"])
        self.assertEqual(result["temperature"]["tmin"]["counts"]["valid"], 2)

    def test_complete_calendar_does_not_imply_valid_coverage(self):
        result = report("".join(f"2000 {m} --- --- 0 0 0\n" for m in range(1, 13)))
        self.assertTrue(result["window"]["calendar_complete"])
        self.assertEqual(result["window"]["absent_months"], [])
        self.assertEqual(result["temperature"]["tmax"]["counts"]["missing"], 12)
        self.assertEqual(result["temperature"]["midpoint"]["counts"]["valid"], 0)

    def test_invalid_rows_fail_explicitly(self):
        for rows in (
            "2000 13 8 2 0 0 0\n", "2000 0 8 2 0 0 0\n",
            "2000 1 NaN 2 0 0 0\n", "2000 1 inf 2 0 0 0\n",
            f"2000 1 {'9' * 400} 2 0 0 0\n",
            "2000 1 8# 2 0 0 0\n", "2000 1 8 2 0 0 0 Unknown\n",
            "2000 1 8 2 0 0\n", "2000 1 2 8 0 0 0\n",
            "2000 1 8 2 0 0 0\n2000 1 8 2 0 0 0\n",
        ):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                report(rows)

    def test_hash_date_window_and_empty_selection_guards(self):
        for overrides in (
            {"expected_sha256": "0" * 64}, {"retrieved_on": "2026-02-30"},
            {"retrieved_on": "20261017"}, {"start_year": 2001},
            {"start_year": 0}, {"source_url": "http://example.invalid/data"},
        ):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                report("2000 1 8 2 0 0 0\n", **overrides)
        with self.assertRaisesRegex(ValueError, "No records"):
            report("1999 1 8 2 0 0 0\n")

    def test_headers_and_units_are_validated(self):
        for raw in (
            b"<html>Login required</html>",
            (HEADER.replace("degC degC", "degF degF") + "2000 1 8 2 0 0 0\n").encode(),
            (HEADER.replace("Location:", "Unknown:") + "2000 1 8 2 0 0 0\n").encode(),
        ):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                analyze(raw, source_url="https://example.invalid/data",
                        retrieved_on="2026-10-17",
                        expected_sha256=hashlib.sha256(raw).hexdigest(),
                        start_year=2000, end_year=2000)

    def test_cli_success_and_hash_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tiny.txt"
            raw = (HEADER + "2000 1 8 2 0 0 0\n").encode()
            path.write_bytes(raw)
            command = [
                sys.executable, str(Path(__file__).with_name("climate_station_bounds.py")),
                str(path), "--source-url", "https://example.invalid/data",
                "--retrieved-on", "2026-10-17", "--start-year", "2000",
                "--end-year", "2000", "--expected-sha256",
                hashlib.sha256(raw).hexdigest(),
            ]
            success = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(success.returncode, 0, success.stderr)
            self.assertEqual(json.loads(success.stdout)["source"]["bytes"], len(raw))
            command[-1] = "0" * 64
            failure = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(failure.returncode, 2)
            self.assertEqual(failure.stdout, "")
            self.assertIn("SHA-256 mismatch", failure.stderr)


if __name__ == "__main__":
    unittest.main()
