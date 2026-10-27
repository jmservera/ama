"""Register-backed synthetic backfill contracts; no private source records."""

import contextlib
import csv
import hashlib
import io
import json
import random
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import Mock, patch

from zava_forward.core.synthetic import provenance, sensor_identity, stock_fabric
from zava_forward.core.synthetic import sensor_backfill as sb
from zava_forward.core.synthetic import sensor_stock as ss


def register() -> list[dict[str, str]]:
    return [
        dict(
            synthetic_home_id=f"opaque-home-{i:03d}",
            building_form_osm=form,
            locality_theme=f"Locality {'ABC'[i % 3]}",
            is_synthetic="true",
            monitoring_consent="granted",
            private_note="NEVER COPY THIS FIELD",
        )
        for i, form in enumerate(
            ("apartments", "terrace", "detached", "bungalow", "semidetached_house")
        )
    ]


def snapshot(root: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in root.iterdir()}


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def write_register(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class SensorStockTests(unittest.TestCase):
    def test_compact_sensor_collisions_fail_without_reassigning_home_keys(self) -> None:
        selection = ss.select(register(), 5)
        with patch.object(sensor_identity, "sensor_key", return_value="SAAAAAAAAAA"):
            with self.assertRaisesRegex(ValueError, "collision"):
                selection.sensors(7)
        self.assertEqual(
            [row["synthetic_home_id"] for row in selection.rows],
            [row["synthetic_home_id"] for row in register()],
        )

    def test_canonical_export_preserves_full_stock_key_domain(self) -> None:
        for home_id in ("hôme-α-Case", "hôme-α-case", "H" * 64, "H" * 65, "H" * 128):
            with self.subTest(home_id=home_id):
                rows = register()[:1]
                rows[0]["synthetic_home_id"] = home_id
                selection = ss.select(rows, 1)
                sensor = selection.sensors(7)[0]
                self.assertEqual(sensor["home_id"], home_id)
                self.assertEqual(len(str(sensor["sensor_id"])), 11)

    def test_fabric_parity_and_full_opaque_sensor_ids(self) -> None:
        rows = register()
        rows[0]["synthetic_home_id"] = "one-same-tail"
        rows[1]["synthetic_home_id"] = "two-same-tail"
        selection = ss.select(rows, 5)
        sensors = {s["home_id"]: s for s in selection.sensors(sb.SEED)}
        self.assertEqual(len({s["sensor_id"] for s in sensors.values()}), 5)
        for row in rows:
            fabric = stock_fabric.fabric(row)
            sensor = sensors[row["synthetic_home_id"]]
            self.assertEqual(sensor["dwelling_type"], ss.DWELLING[fabric["dwelling_type"]])
            self.assertEqual(
                sensor["construction_loss"], ss.CONSTRUCTION_LOSS[fabric["construction"]]
            )
            self.assertEqual(len(str(sensor["sensor_id"])), 11)
            self.assertFalse(sensor["retrofitted"])
        self.assertEqual(
            [r["build_year"] for r in selection.fabric_rows()],
            [stock_fabric.fabric(r)["build_year"] for r in selection.rows],
        )

    def test_selection_precedes_choice_and_order_does_not_matter(self) -> None:
        rows = register()
        rows[0]["monitoring_consent"] = "declined"
        del rows[1]["monitoring_consent"]
        a = ss.select(rows, 3)
        self.assertEqual(a, ss.select(list(reversed(rows)), 3))
        coverage = a.coverage()
        self.assertEqual(coverage["selected_homes"], 3)
        self.assertEqual(coverage["unselected_homes"], 2)
        self.assertEqual(coverage["monitored_homes"], 1)
        self.assertEqual(coverage["declined_homes"], 1)
        self.assertEqual(coverage["unknown_homes"], 1)
        self.assertEqual([s["home_id"] for s in a.sensors(7)], [rows[2]["synthetic_home_id"]])

    def test_invalid_register_and_counts_rejected(self) -> None:
        for count in (None, 0, -1, 6):
            with self.subTest(count=count), self.assertRaises(ValueError):
                ss.select(register(), count)
        for key, value in (
            ("synthetic_home_id", ""),
            ("synthetic_home_id", " padded"),
            ("synthetic_home_id", "X" * 129),
            ("synthetic_home_id", "line\nbreak"),
            ("is_synthetic", "false"),
            ("monitoring_consent", "yes"),
        ):
            rows = register()
            rows[-1][key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                ss.select(rows, 1)
        rows = register()
        rows[1]["synthetic_home_id"] = rows[0]["synthetic_home_id"]
        with self.assertRaises(ValueError):
            ss.select(rows, 1)

    def test_csv_allowlist_validation_and_private_field_independence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "stock.csv"
            rows = register()
            write_register(path, rows)
            a = ss.read_register(path, 3)
            rows[0]["private_note"] = "DIFFERENT PRIVATE FIELD"
            write_register(path, rows)
            self.assertEqual(a, ss.read_register(path, 3))
            self.assertNotIn("private_note", a.rows[0])
            for content in (
                "synthetic_home_id,synthetic_home_id,is_synthetic\nX,X,true\n",
                "synthetic_home_id,is_synthetic\nX\n",
                "synthetic_home_id,is_synthetic\nX,true,extra\n",
                "synthetic_home_id\nX\n",
            ):
                path.write_text(content)
                with self.subTest(content=content), self.assertRaises(ValueError):
                    ss.read_register(path, 1)

    def test_repeat_bytes_seed_and_date_variation_and_shards(self) -> None:
        stock = ss.select(register(), 5)
        with tempfile.TemporaryDirectory() as tmp, patch.object(sb, "SHARD_HOMES", 2):
            root = Path(tmp)
            for name, seed, as_of in (
                ("a", 7, "2026-10-15"),
                ("b", 7, "2026-10-15"),
                ("seed", 8, "2026-10-15"),
                ("date", 7, "2026-10-16"),
            ):
                sb.write(root / name, stock=stock, seed=seed, days=3, as_of=as_of)
            self.assertEqual(snapshot(root / "a"), snapshot(root / "b"))
            self.assertEqual(len(list((root / "a").glob("readings-*.csv"))), 3)
            for name in ("seed", "date"):
                self.assertNotEqual(
                    snapshot(root / "a")["readings-0000.csv"],
                    snapshot(root / name)["readings-0000.csv"],
                )

    def test_full_730_day_window_and_register_reconciliation(self) -> None:
        stock = ss.select(register(), 3)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = sb.write(root, stock=stock, days=730, cadence=360, as_of="2026-10-15")
            rows = csv_rows(root / "readings-0000.csv")
            ids = {row["synthetic_home_id"] for row in stock.rows}
            self.assertEqual({r["home_id"] for r in rows}, ids)
            self.assertEqual(manifest["homes_covered"], 3)
            self.assertEqual(manifest["stock_homes_declared"], 5)
            self.assertEqual(manifest["days"], 730)
            start = datetime(2024, 10, 15, tzinfo=UTC)
            end = datetime(2026, 10, 15, tzinfo=UTC)
            for row in rows:
                observed = datetime.fromisoformat(row["observed_at"])
                self.assertLessEqual(start, observed)
                self.assertLess(observed, end)
                self.assertEqual((observed - start).total_seconds() % 21600, 0)
                self.assertEqual(row["source_type"], "SYNTHETIC")
            self.assertEqual(manifest["rows"], len(rows))

    def test_declined_and_unknown_have_no_sensors_or_readings(self) -> None:
        rows = register()
        rows[0]["monitoring_consent"] = "declined"
        rows[1]["monitoring_consent"] = "unknown"
        stock = ss.select(rows, 3)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = sb.write(root, stock=stock, days=3)
            self.assertEqual(manifest["homes_covered"], 1)
            self.assertEqual(
                {r["home_id"] for r in csv_rows(root / "sensors.csv")},
                {rows[2]["synthetic_home_id"]},
            )
            self.assertEqual(
                {r["home_id"] for r in csv_rows(root / "readings-0000.csv")},
                {rows[2]["synthetic_home_id"]},
            )

    def test_all_excluded_is_explicit_empty_output(self) -> None:
        rows = register()
        for row in rows:
            row["monitoring_consent"] = "declined"
        stock = ss.select(rows, 3)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = sb.write(root, stock=stock, days=2)
            self.assertEqual(manifest["rows"], 0)
            estimate = manifest["estimate"]
            self.assertIsInstance(estimate, dict)
            assert isinstance(estimate, dict)
            self.assertEqual(estimate["estimated_rows"], 0)
            self.assertEqual(estimate["homes"], 0)
            self.assertEqual(csv_rows(root / "sensors.csv"), [])
            self.assertEqual(list(root.glob("readings-*.csv")), [])
            self.assertEqual(manifest["coverage"], stock.coverage())
            with sqlite3.connect(":memory:") as conn:
                self.assertEqual(
                    sb.load_into(conn, root, stock=stock), dict(inserted=0, rejected={})
                )

    def test_estimate_is_actual_sample_and_precedes_output(self) -> None:
        stock = ss.select(register(), 3)
        original = sb.estimate
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "new"
            estimate = sb.estimate(stock=stock, days=3)
            self.assertEqual(estimate["homes"], 3)
            with (
                patch.object(sb, "estimate", wraps=original) as measured,
                patch.object(
                    provenance, "prepare_output", wraps=provenance.prepare_output
                ) as prepare,
            ):
                calls = Mock()
                calls.attach_mock(measured, "estimate")
                calls.attach_mock(prepare, "prepare")
                manifest = sb.write(root, stock=stock, days=3)
                self.assertEqual(measured.call_count, 1)
                self.assertEqual([call[0] for call in calls.mock_calls], ["estimate", "prepare"])
            self.assertEqual(estimate, manifest["estimate"])
            self.assertEqual(estimate["estimated_rows"], manifest["rows"])
            self.assertEqual(json.loads((root / "estimate.json").read_text()), estimate)

    def test_manifest_hashes_sanitized_fabric_and_input(self) -> None:
        stock = ss.select(register(), 3)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = sb.write(root, stock=stock, days=2)
            self.assertEqual(manifest["stock_input_sha256"], stock.input_sha256)
            self.assertEqual(manifest["stock_seed"], stock_fabric.SEED)
            self.assertEqual(manifest["stock_fabric_version"], stock_fabric.VERSION)
            self.assertEqual(manifest["ddl_contract"], "stock-reading-v1")
            self.assertEqual(
                manifest["file_sha256"],
                {
                    name: hashlib.sha256(content).hexdigest()
                    for name, content in snapshot(root).items()
                    if name != "manifest.json"
                },
            )
            payload = b"".join(snapshot(root).values())
            self.assertNotIn(b"NEVER COPY", payload)
            self.assertNotIn(b"private_note", payload)
            self.assertNotIn(tmp.encode(), payload)
            self.assertEqual(len(csv_rows(root / "stock-fabric.csv")), 3)

    def test_construction_factor_changes_projection_not_authority(self) -> None:
        sensor = ss.select(register(), 1).sensors(7)[0]
        at = datetime(2025, 1, 1, 18, tzinfo=UTC)
        a = sb._indoor({**sensor, "construction_loss": 0.75}, random.Random(1), at, 0, 80)
        b = sb._indoor({**sensor, "construction_loss": 1.20}, random.Random(1), at, 0, 80)
        self.assertLess(b[0], a[0])
        self.assertGreater(b[1], a[1])

    def test_long_ids_sql_widths_portable_parameters_and_local_idempotency(self) -> None:
        rows = register()
        rows[0]["synthetic_home_id"] = "L" * 128
        stock = ss.select(rows, 5)
        self.assertIn("sensor_id VARCHAR(73)", sb.STOCK_SQL_DDL)
        self.assertIn("home_id NVARCHAR(128)", sb.STOCK_SQL_DDL)
        self.assertIn("reading_id VARCHAR(96)", sb.STOCK_SQL_DDL)
        self.assertIn("sensor_id VARCHAR(20)", sb.SQL_DDL)
        seen: list[tuple[str, list[object]]] = []

        class Cursor:
            rowcount = 1

        class Connection:
            def execute(self, sql: str, params: list[object]) -> Cursor:
                seen.append((sql, params))
                return Cursor()

            def commit(self) -> None:
                pass

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = sb.write(root, stock=stock, days=1, cadence=360)
            sb.load_into(Connection(), root, create_schema=None, stock=stock)
            with sqlite3.connect(":memory:") as conn:
                first = sb.load_into(conn, root, stock=stock)
                self.assertEqual(
                    first["inserted"] + sum(first["rejected"].values()), manifest["rows"]
                )
                self.assertEqual(sb.load_into(conn, root, stock=stock)["inserted"], 0)
            for sql, params in seen:
                self.assertTrue(sql.startswith("INSERT INTO"))
                self.assertIn("WHERE NOT EXISTS", sql)
                self.assertNotIn("OR IGNORE", sql)
                self.assertIn(
                    params[1],
                    {r["synthetic_home_id"] for r in stock.rows}
                    | {r["reading_id"] for r in csv_rows(root / "readings-0000.csv")},
                )
            for row in csv_rows(root / "readings-0000.csv"):
                self.assertLessEqual(len(row["sensor_id"]), 73)
                self.assertLessEqual(len(row["reading_id"]), 96)

    def test_destination_and_refresh_refusal_precede_payload_writes(self) -> None:
        stock = ss.select(register(), 1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sb.write(root / "snapshot", stock=stock, days=1)
            before = snapshot(root / "snapshot")
            with self.assertRaises(FileExistsError):
                sb.write(root / "snapshot", stock=stock, days=1)
            self.assertEqual(before, snapshot(root / "snapshot"))
            (root / "alias").symlink_to(root / "snapshot", target_is_directory=True)
            with self.assertRaises(ValueError):
                sb.write(root / "alias", stock=stock, days=1)
            with self.assertRaises(ValueError):
                sb.write(root / "invalid", stock=stock, days=0)
            self.assertFalse((root / "invalid").exists())
            with self.assertRaises(ValueError):
                sb.write(root / "count", stock=stock, homes=1, days=1)
            self.assertFalse((root / "count").exists())
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            sb.write(Path(__file__).parents[1] / "forbidden-sensor-output", stock=stock, days=1)

    def test_cli_estimate_write_parity_and_missing_count_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "input.csv"
            write_register(path, register())
            args = ["--register", str(path), "--homes", "3", "--days", "2", "--cadence", "360"]
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                sb.main([*args, "--estimate-only"])
            estimate = json.loads(buffer.getvalue())
            with contextlib.redirect_stdout(io.StringIO()):
                sb.main([*args, "--out", str(root / "output")])
            manifest = json.loads((root / "output/manifest.json").read_text())
            self.assertEqual(estimate, manifest["estimate"])
            result = subprocess.run(
                [sys.executable, "-m", sb.__name__, "--register", str(path), "--estimate-only"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("explicit positive homes subset", result.stderr)


if __name__ == "__main__":
    unittest.main()
