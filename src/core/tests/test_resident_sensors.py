"""Own-home sensor projection over constructed generator-shaped readings, never private data."""

import json
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import Mock

from test_resident_showcase import row
from zava_forward.core import resident_showcase as rs
from zava_forward.core import resident_showcase_sql as sql


def reading(home: str = "HOME-A", **over: Any) -> dict[str, Any]:
    return {
        "home_id": home,
        "observed_at": "2026-10-25T12:00:00Z",
        "temperature_c": 19.5,
        "humidity_pct": 62.0,
        "source_type": "SYNTHETIC",
        "injected_fault": "",
        **over,
    }


class SensorProjectionTests(unittest.TestCase):
    def test_numeric_history_is_chronological_and_strips_internal_fields(self) -> None:
        history = rs.parse_sensors(
            [reading(), reading(observed_at="2026-10-25T11:00:00Z", temperature_c=18)], "HOME-A"
        )
        view = rs.showcase_view(row(sensor_home_id="HOME-A", sensors=history))["sensors"]
        self.assertTrue(view["synthetic"])
        self.assertEqual([r["temperature_c"] for r in view["history"]], [18, 19.5])
        self.assertIn("not live", view["note"])
        self.assertNotIn("HOME-A", json.dumps(view))
        self.assertEqual(
            set(view["history"][0]),
            {
                "observed_at",
                "temperature_c",
                "humidity_pct",
                "temperature_status",
                "humidity_status",
            },
        )

    def test_foreign_case_distinct_and_non_synthetic_rows_are_denied(self) -> None:
        for item in (
            reading("HOME-B"),
            reading("home-a"),
            reading("HOME-A "),
            reading(source_type="LIVE"),
            reading(source_type="SYNTHETIC "),
        ):
            with self.subTest(item=item), self.assertRaises(rs.ShowcaseDenied):
                rs.parse_sensors([item], "HOME-A")
        with self.assertRaises(rs.ShowcaseDenied):
            rs.parse_sensors([reading()], None)

    def test_invalid_envelope_and_timestamps_are_denied(self) -> None:
        bad: Any
        for bad in (
            {},
            [reading()] * 49,
            [dict(reading(), extra="secret")],
            [reading(observed_at="2026-02-30T12:00:00Z")],
            [reading(observed_at="2026-10-25T12:00:00+01:00")],
            [reading(temperature_c=True)],
            [reading(temperature_c="19.5")],
            [reading(injected_fault="unknown")],
            [reading(), reading()],
        ):
            with self.subTest(bad=bad), self.assertRaises(rs.ShowcaseDenied):
                rs.parse_sensors(bad, "HOME-A")

    def test_null_and_invalid_channels_keep_latest_timestamp_and_sibling(self) -> None:
        for temperature, status in (
            (None, "Not recorded"),
            (float("nan"), "Outside demo range"),
            (float("inf"), "Outside demo range"),
            (-11, "Outside demo range"),
            (46, "Outside demo range"),
        ):
            [item] = rs.parse_sensors([reading(temperature_c=temperature)], "HOME-A")
            self.assertIsNone(item.temperature_c)
            self.assertEqual(item.temperature_status, status)
            self.assertEqual(item.humidity_pct, 62)
        for humidity in (-1, 101):
            [item] = rs.parse_sensors([reading(humidity_pct=humidity)], "HOME-A")
            self.assertIsNone(item.humidity_pct)
            self.assertEqual(item.temperature_c, 19.5)

    def test_faults_never_produce_normal_gauge_values_or_older_fallback(self) -> None:
        for fault in ("OUTLIER", "STUCK"):
            history = rs.parse_sensors(
                [
                    reading(observed_at="2026-10-25T11:00:00Z"),
                    reading(injected_fault=fault),
                ],
                "HOME-A",
            )
            latest = history[-1]
            self.assertIsNone(latest.temperature_c)
            self.assertIsNone(latest.humidity_pct)
            self.assertTrue(latest.temperature_status.startswith("Demo fault:"))

    def test_empty_and_plot_bounds_are_supported(self) -> None:
        self.assertEqual(rs.parse_sensors([], None), ())
        for temperature, humidity in ((-10, 0), (45, 100)):
            [item] = rs.parse_sensors(
                [reading(temperature_c=temperature, humidity_pct=humidity)], "HOME-A"
            )
            self.assertEqual((item.temperature_c, item.humidity_pct), (temperature, humidity))

    def test_reader_shapes_only_fixed_view_columns_and_parameterises_case(self) -> None:
        data = {k: getattr(row(), k) for k in rs.ROW_KEYS}
        data.pop("measures")
        data.pop("sensors")
        data.pop("documents")
        data.update(
            measures_json='["Loft insulation"]',
            measures_text=None,
            sensor_home_id="HOME-A",
            sensors_json=json.dumps([reading()]),
            documents_json='{"requests":null,"documents":null}',
        )
        cursor = Mock()
        cursor.description = [(key,) for key in sql.COLUMNS]
        cursor.fetchmany.return_value = [tuple(data[k] for k in sql.COLUMNS)]
        conn = Mock()
        conn.cursor.return_value = cursor
        reader = sql.ShowcaseReader(lambda: conn)
        found = reader.fetch_case("C-1' OR 1=1")
        self.assertIsNotNone(found)
        assert found is not None
        self.assertEqual(found.sensors[0].temperature_c, 19.5)
        cursor.execute.assert_called_once_with(sql.ONE_SQL, ("C-1' OR 1=1",))
        conn.close.assert_called_once()
        for invalid in ("not json", "null", json.dumps([reading("HOME-B")])):
            data["sensors_json"] = invalid
            cursor.fetchmany.return_value = [tuple(data[k] for k in sql.COLUMNS)]
            with self.assertRaises(rs.ShowcaseDenied):
                reader.fetch_case("C-1")

    def test_sql_source_guards_every_identity_and_preserves_nulls(self) -> None:
        text = (Path(__file__).resolve().parents[3] / "infra/sql/resident-showcase.sql").read_text()
        for fragment in (
            "IF OBJECT_ID(N'dbo.sensor_register'",
            "OBJECT_ID(N'dbo.sensor_reading'",
            "s.sensor_id COLLATE Latin1_General_100_BIN2 = r.sensor_id",
            "s.home_id COLLATE Latin1_General_100_BIN2 =",
            "r.home_id COLLATE Latin1_General_100_BIN2 =",
            "s.source_type COLLATE Latin1_General_100_BIN2 = ''SYNTHETIC''",
            "r.source_type COLLATE Latin1_General_100_BIN2 = ''SYNTHETIC''",
            "SELECT TOP (48)",
            "INCLUDE_NULL_VALUES",
            "N''[]'' AS sensors_json",
        ):
            self.assertIn(fragment, text)
        self.assertEqual(text.count("GRANT "), 1)
        self.assertNotIn("GRANT SELECT ON OBJECT::dbo.sensor", text)

    def test_sql_identity_guards_are_length_sensitive_after_common_conversion(self) -> None:
        text = (Path(__file__).resolve().parents[3] / "infra/sql/resident-showcase.sql").read_text()
        compact = " ".join(text.split())
        stock_length = "DATALENGTH(JSON_VALUE(k.body, ''$.home.stock_id''))"
        for left, right in (
            ("s.sensor_id", "DATALENGTH(CONVERT(NVARCHAR(MAX), r.sensor_id))"),
            ("s.home_id", stock_length),
            ("r.home_id", stock_length),
            ("s.source_type", "DATALENGTH(N''SYNTHETIC'')"),
            ("r.source_type", "DATALENGTH(N''SYNTHETIC'')"),
        ):
            self.assertIn(f"DATALENGTH(CONVERT(NVARCHAR(MAX), {left})) = {right}", compact)
        history = text.split("SET @history =", 1)[1].split("DECLARE @view", 1)[0]
        self.assertNotIn("TRIM", history)
