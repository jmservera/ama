"""Pinned public reanalysis, strict admission and exact UTC subsampling for #178."""

import copy
import hashlib
import json
import math
import unittest
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.synthetic.climate_history import ClimateHistory

ROOT = Path(__file__).resolve().parents[3]
PACK = ROOT / "docs/reference/research/climate-paired-source-178"
RAW = PACK / "open-meteo-era5-durham-2023-2024-raw.json"
METADATA = PACK / "open-meteo-era5-durham-2023-2024-metadata.json"
RAW_SHA = "af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e"
META_SHA = "628e05cb4a8ce6731800dd3a587be8180f4a3a5e04f62b8577e5020d79cf48b4"
NASA_SHA = "cba9cf308878e9a4b2f2847cbbc4e66f06d14a1b734d4da48be0133fef9c6db1"


class ClimateHistoryTests(unittest.TestCase):
    history: ClimateHistory
    payload: dict[str, Any]
    metadata: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(RAW.read_bytes())
        cls.metadata = json.loads(METADATA.read_bytes())
        cls.history = ClimateHistory.read(
            RAW, METADATA, expected_sha256=RAW_SHA, expected_metadata_sha256=META_SHA
        )

    def read_mutation(
        self, payload: dict[str, Any], metadata: dict[str, Any] | None = None
    ) -> ClimateHistory:
        contract = copy.deepcopy(self.metadata if metadata is None else metadata)
        raw = json.dumps(payload).encode()
        contract["input"]["sha256"] = hashlib.sha256(raw).hexdigest()
        contract["input"]["bytes"] = len(raw)
        with patch.object(Path, "read_bytes", side_effect=[raw, json.dumps(contract).encode()]):
            return ClimateHistory.read(RAW, METADATA)

    def test_committed_two_year_coverage_and_record_derived_bounds(self) -> None:
        self.assertEqual(self.history.start, datetime(2023, 1, 1, tzinfo=UTC))
        self.assertEqual(self.history.end_exclusive, datetime(2025, 1, 1, tzinfo=UTC))
        pairs = self.history.series(self.history.start, 731, 60)
        self.assertEqual(len(pairs), 17544)
        self.assertEqual(
            pairs,
            list(
                zip(
                    self.payload["hourly"]["temperature_2m"],
                    self.payload["hourly"]["relative_humidity_2m"],
                    strict=True,
                )
            ),
        )
        self.assertEqual(
            self.history.manifest()["bounds"],
            {
                "temperature_c": {"minimum": -5.3, "maximum": 26.9},
                "relative_humidity_pct": {"minimum": 36.0, "maximum": 100.0},
                "dew_point_c": {"minimum": -7.1, "maximum": 19.6},
            },
        )
        self.assertNotEqual(pairs[:24], pairs[8760:8784])
        self.assertEqual(self.payload["hourly"]["time"].count("2024-02-29T00:00"), 1)

    def test_exact_timestamp_subsampling_across_year_and_leap_day(self) -> None:
        for start in (
            datetime(2023, 12, 31, 3, tzinfo=UTC),
            datetime(2024, 2, 28, 1, tzinfo=UTC),
        ):
            for cadence in (60, 120, 180, 360, 1440):
                with self.subTest(start=start, cadence=cadence):
                    pairs = self.history.series(start, 2, cadence)
                    self.assertEqual(len(pairs), 2 * 1440 // cadence)
                    for index, pair in enumerate(pairs):
                        stamp = start + timedelta(minutes=index * cadence)
                        offset = self.payload["hourly"]["time"].index(
                            stamp.strftime("%Y-%m-%dT%H:%M")
                        )
                        self.assertEqual(
                            pair,
                            (
                                self.payload["hourly"]["temperature_2m"][offset],
                                self.payload["hourly"]["relative_humidity_2m"][offset],
                            ),
                        )
        last = self.history.series(datetime(2024, 12, 31, tzinfo=UTC), 1, 60)
        self.assertEqual(last[-1], (8.7, 82.0))

    def test_reproducibility_and_detached_manifest(self) -> None:
        other = ClimateHistory.read(RAW, METADATA)
        first = self.history.series(self.history.start, 731, 360)
        self.assertEqual(first, other.series(other.start, 731, 360))
        first[0] = (999.0, 999.0)
        self.assertNotEqual(first, self.history.series(self.history.start, 731, 360))
        manifest = self.history.manifest()
        self.assertEqual(manifest["input_sha256"], RAW_SHA)
        self.assertEqual(manifest["metadata_sha256"], META_SHA)
        self.assertEqual(manifest, other.manifest())
        self.assertEqual(json.loads(json.dumps(manifest, allow_nan=False)), manifest)
        manifest["source"] = {}
        self.assertNotEqual(manifest, self.history.manifest())

    def test_raw_and_metadata_hash_pins_and_byte_counts(self) -> None:
        for kwargs in (
            {"expected_sha256": "0" * 64},
            {"expected_metadata_sha256": "0" * 64},
            {"expected_sha256": "not a digest"},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                ClimateHistory.read(RAW, METADATA, **kwargs)
        raw, meta = RAW.read_bytes(), METADATA.read_bytes()
        with patch.object(Path, "read_bytes", side_effect=[raw + b" ", meta]):
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                ClimateHistory.read(RAW, METADATA)
        contract = copy.deepcopy(self.metadata)
        contract["input"]["bytes"] += 1
        with patch.object(Path, "read_bytes", side_effect=[raw, json.dumps(contract).encode()]):
            with self.assertRaisesRegex(ValueError, "byte count"):
                ClimateHistory.read(RAW, METADATA)

    def test_null_nonnumeric_nonfinite_and_invalid_humidity(self) -> None:
        for key in ("temperature_2m", "relative_humidity_2m", "dew_point_2m"):
            for value in (None, True, "6", float("nan"), float("inf"), 10**400):
                with self.subTest(key=key, value=value):
                    payload = copy.deepcopy(self.payload)
                    payload["hourly"][key][0] = value
                    with self.assertRaises(ValueError):
                        self.read_mutation(payload)
        for value in (-999, -0.01, 100.01):
            payload = copy.deepcopy(self.payload)
            payload["hourly"]["relative_humidity_2m"][0] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "0..100"):
                self.read_mutation(payload)
        for value in (7.0, -243.04):
            payload = copy.deepcopy(self.payload)
            payload["hourly"]["dew_point_2m"][0] = value
            with self.subTest(dew=value), self.assertRaises(ValueError):
                self.read_mutation(payload)
        payload = copy.deepcopy(self.payload)
        payload["hourly"]["relative_humidity_2m"][0] = 50
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            self.read_mutation(payload)

    def test_gaps_duplicates_misalignment_and_incomplete_columns(self) -> None:
        for value in (
            "2023-01-01T02:00",
            "2023-01-01T00:00",
            "2023-01-01T01:30",
            "2023-01-01T01:00Z",
            None,
        ):
            payload = copy.deepcopy(self.payload)
            payload["hourly"]["time"][1] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.read_mutation(payload)
        for key in ("time", "temperature_2m", "relative_humidity_2m", "dew_point_2m"):
            payload = copy.deepcopy(self.payload)
            payload["hourly"][key].pop()
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "incomplete"):
                self.read_mutation(payload)
        payload = copy.deepcopy(self.payload)
        for key in payload["hourly"]:
            payload["hourly"][key].reverse()
        with self.assertRaisesRegex(ValueError, "misaligned"):
            self.read_mutation(payload)

    def test_units_and_non_utc_response_rejected(self) -> None:
        for key in ("time", "temperature_2m", "relative_humidity_2m", "dew_point_2m"):
            payload = copy.deepcopy(self.payload)
            payload["hourly_units"][key] = "incorrect"
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "units"):
                self.read_mutation(payload)
        for key, value in (
            ("utc_offset_seconds", 3600),
            ("utc_offset_seconds", False),
            ("timezone", "Europe/London"),
            ("timezone_abbreviation", "BST"),
        ):
            payload = copy.deepcopy(self.payload)
            payload[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "UTC"):
                self.read_mutation(payload)

    def test_series_rejects_non_exact_or_uncovered_windows(self) -> None:
        for days, cadence in (
            (0, 60),
            (-1, 60),
            (True, 60),
            (1, True),
            (1, 30),
            (1, 90),
            (1, 420),
            (1, 0),
            (1, -60),
            (1, 60.0),
            (1.0, 60),
            (732, 60),
            (10**20, 60),
        ):
            with self.subTest(days=days, cadence=cadence), self.assertRaises(ValueError):
                self.history.series(self.history.start, days, cadence)  # type: ignore[arg-type]
        for start in (
            datetime(2023, 1, 1),
            datetime(2023, 1, 1, tzinfo=timezone(timedelta(hours=1))),
            self.history.start.replace(minute=1),
            self.history.start.replace(second=1),
            self.history.start.replace(microsecond=1),
            self.history.start - timedelta(hours=1),
            self.history.end_exclusive,
        ):
            with self.subTest(start=start), self.assertRaises(ValueError):
                self.history.series(start, 1, 60)

    def test_metadata_coverage_bounds_and_structure_are_validated(self) -> None:
        mutations: tuple[tuple[str, str, object], ...] = (
            ("coverage", "start", "2023-01-02T00:00Z"),
            ("coverage", "end_exclusive", "2024-12-31T23:00Z"),
            ("coverage", "records", 17543),
            ("coverage", "records", True),
            ("coverage", "step_seconds", 7200),
            ("coverage", "timezone", "Europe/London"),
            ("bounds", "temperature_c", {"minimum": -1, "maximum": 26.9}),
            ("validation", "rh_tolerance_points", 2),
            ("units", "temperature_2m", "K"),
        )
        for block, key, value in mutations:
            metadata = copy.deepcopy(self.metadata)
            metadata[block][key] = value
            with self.subTest(block=block, key=key), self.assertRaises(ValueError):
                self.read_mutation(self.payload, metadata)
        for block in ("input", "source", "coverage", "bounds", "validation", "units"):
            for value in (None, [], "missing"):
                metadata = copy.deepcopy(self.metadata)
                metadata[block] = value
                if block == "input":
                    with patch.object(
                        Path,
                        "read_bytes",
                        side_effect=[RAW.read_bytes(), json.dumps(metadata).encode()],
                    ):
                        with self.assertRaises(ValueError):
                            ClimateHistory.read(RAW, METADATA)
                else:
                    with self.subTest(block=block, value=value), self.assertRaises(ValueError):
                        self.read_mutation(self.payload, metadata)

    def test_source_request_retrieval_version_resolution_and_grid_contract(self) -> None:
        mutations: tuple[tuple[str, object], ...] = (
            ("provider", "NASA"),
            ("model", "ERA5-Land"),
            ("dataset_version", ""),
            ("api_version", None),
            ("retrieved_on", "27/10/2026"),
            ("resolution", {"temporal_seconds": 3600, "grid_degrees": 0.1}),
            ("resolution_reference", ""),
            ("request_url", self.metadata["source"]["request_url"].replace("https:", "http:")),
            (
                "request_url",
                self.metadata["source"]["request_url"].replace("2024-12-31", "2023-12-31"),
            ),
            ("request_url", self.metadata["source"]["request_url"].replace("era5&", "era5_land&")),
            ("request_url", self.metadata["source"]["request_url"].replace("54.775", "54.768")),
            ("returned_grid", {"latitude": 54.75, "longitude": -1.5, "elevation": 98}),
        )
        for key, value in mutations:
            metadata = copy.deepcopy(self.metadata)
            metadata["source"][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.read_mutation(self.payload, metadata)

    def test_malformed_json_and_duplicate_keys_are_rejected(self) -> None:
        for raw in (b"[]", b"null", b"{", b'{"hourly": {}, "hourly": {}}', b"\xff"):
            metadata = copy.deepcopy(self.metadata)
            metadata["input"].update(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
            with patch.object(Path, "read_bytes", side_effect=[raw, json.dumps(metadata).encode()]):
                with self.subTest(raw=raw), self.assertRaises(ValueError):
                    ClimateHistory.read(RAW, METADATA)
        with patch.object(
            Path,
            "read_bytes",
            side_effect=[RAW.read_bytes(), b'{"schema_version":1,"schema_version":2}'],
        ):
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                ClimateHistory.read(RAW, METADATA)

    def test_retained_nasa_sensitivity_hash_bounds_comparison_and_approval_scope(self) -> None:
        raw = (PACK / "nasa-power-merra2-durham-2023-raw.json").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), NASA_SHA)
        nasa = json.loads(raw)
        report = json.loads((PACK / "nasa-power-merra2-durham-2023-sensitivity.json").read_bytes())
        self.assertEqual(report["source"]["sha256"], NASA_SHA)
        self.assertEqual(report["source"]["api"], nasa["header"]["api"])
        self.assertEqual(nasa["header"]["time_standard"], "UTC")
        series = nasa["properties"]["parameter"]
        keys = list(series["T2M"])
        self.assertEqual(keys, list(series["RH2M"]))
        expected = [
            (self.history.start + index * timedelta(hours=1)).strftime("%Y%m%d%H")
            for index in range(8760)
        ]
        self.assertEqual(keys, expected)
        for field, label, primary_field in (
            ("T2M", "temperature_c", "temperature_2m"),
            ("RH2M", "relative_humidity_pct", "relative_humidity_2m"),
        ):
            values = list(series[field].values())
            self.assertTrue(all(math.isfinite(v) and v != -999 for v in values))
            if field == "RH2M":
                self.assertTrue(all(0 <= v <= 100 for v in values))
            self.assertEqual(
                report["bounds"][label], {"minimum": min(values), "maximum": max(values)}
            )
            differences = [
                primary - secondary
                for primary, secondary in zip(
                    self.payload["hourly"][primary_field][:8760], values, strict=True
                )
            ]
            comparison = report["new_primary_2023_comparison"][
                "temperature_degC" if field == "T2M" else "relative_humidity_percent"
            ]
            self.assertEqual(comparison["mean_difference"], round(sum(differences) / 8760, 3))
        self.assertEqual(report["new_primary_input_sha256"], RAW_SHA)
        self.assertFalse(report["attribution_and_terms"]["licence_verified"])
        self.assertEqual(self.metadata["owner_approval"]["key"], "owner-approvals-2026-10-27-b")
        self.assertFalse(
            self.metadata["owner_approval"]["underlying_legal_or_production_terms_verified"]
        )


if __name__ == "__main__":
    unittest.main()
