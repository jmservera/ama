import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.synthetic import scale_fixture
from zava_forward.core.synthetic import sensor_backfill as sb

DAYS = 3


def build(out, seed=sb.SEED, homes=12):
    return sb.write(out, homes=homes, seed=seed, days=DAYS)


class SensorBackfillTests(unittest.TestCase):
    def test_same_seed_is_byte_identical_and_other_seed_differs(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b, tempfile.TemporaryDirectory() as c:
            ma, mb, mc = build(a), build(b), build(c, seed=999)
            self.assertEqual(ma, mb)
            self.assertEqual(Path(a, "readings-0000.csv").read_bytes(), Path(b, "readings-0000.csv").read_bytes())
            self.assertNotEqual(ma["readings_sha256"], mc["readings_sha256"])

    def test_every_series_resolves_to_register_and_sensor_register(self):
        with tempfile.TemporaryDirectory() as d:
            build(d)
            stock = {h["id"] for h in scale_fixture.homes()}
            sensors = {r["sensor_id"]: r for r in csv.DictReader(open(Path(d, "sensors.csv")))}
            rows = list(csv.DictReader(open(Path(d, "readings-0000.csv"))))
            self.assertTrue(rows)
            for r in rows:
                self.assertIn(r["home_id"], stock)
                self.assertEqual(sensors[r["sensor_id"]]["home_id"], r["home_id"])
                self.assertEqual(r["source_type"], "SYNTHETIC")

    def test_manifest_and_estimate_recorded_before_generation(self):
        with tempfile.TemporaryDirectory() as d:
            m = build(d)
            self.assertEqual(json.loads(Path(d, "estimate.json").read_text()), m["estimate"])
            for key in ("seed", "version", "schema_version", "climate_source", "parameters", "synthetic_label"):
                self.assertIn(key, m)
            self.assertLessEqual(m["rows"], m["estimate"]["estimated_rows"])
        full = sb.estimate(days=DAYS)
        self.assertEqual(full["homes"], 60000)
        self.assertGreater(full["estimated_rows"], 60000 * DAYS * 20)

    def test_load_reuses_validation_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            m = build(d)
            conn = sqlite3.connect(":memory:")
            first = sb.load_into(conn, d)
            second = sb.load_into(conn, d)
            self.assertEqual(first["inserted"], m["rows"])
            self.assertEqual(second["inserted"], 0)
            self.assertEqual(first["rejected"], {})
            ids = {"S"}
            bad = dict(schema_version="reading-v1", sensor_id="X", source_type="SYNTHETIC", temperature_c="20", humidity_pct="50")
            self.assertEqual(sb.validate_reading(bad, ids), "unmapped_sensor")
            self.assertEqual(sb.validate_reading({**bad, "sensor_id": "S", "humidity_pct": "150"}, ids), "out_of_range_humidity_pct")

    def test_load_sql_is_portable_to_azure_sql(self):
        seen = []

        class Cur:
            rowcount = 1

        class Conn:
            def execute(self, sql, params=()):
                seen.append(sql)
                return Cur()

            def commit(self):
                pass

        with tempfile.TemporaryDirectory() as d:
            build(d)
            sb.load_into(Conn(), d, create_schema=None)
        self.assertTrue(seen)
        for sql in seen:
            self.assertNotIn("OR IGNORE", sql.upper())
            self.assertTrue(sql.startswith("INSERT INTO"))
            self.assertIn("WHERE NOT EXISTS", sql)
        self.assertNotIn("CREATE", " ".join(seen).upper())


if __name__ == "__main__":
    unittest.main()
