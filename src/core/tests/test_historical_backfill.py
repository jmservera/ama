"""Composed writer contracts with constructed weather, never private stock."""

import csv
import gzip
import hashlib
import json
import random
import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, store_at
from zava_forward.core.sensor_consumer import SensorConsumer
from zava_forward.core.synthetic import (
    household_conditions as hc,
)
from zava_forward.core.synthetic import (
    indoor_projection as ip,
)
from zava_forward.core.synthetic import (
    retrofit_effects as re,
)
from zava_forward.core.synthetic import (
    sensor_backfill as sb,
)
from zava_forward.core.synthetic import (
    sensor_stock as ss,
)

START = datetime(2024, 10, 1, tzinfo=UTC)


class ConstructedClimate:
    def series(self, start: datetime, days: int, cadence: int) -> list[tuple[float, float]]:
        return [(2.0, 70.0)] * (days * 1440 // cadence)

    def manifest(self) -> dict[str, object]:
        return {"source": "CONSTRUCTED UNIT TEST ONLY", "sha256": "a" * 64}


def selection() -> ss.Selection:
    return ss.select(
        [
            dict(
                synthetic_home_id=key,
                is_synthetic="true",
                monitoring_consent=choice,
                building_form_osm="terrace",
            )
            for key, choice in (
                ("ZF-1", "granted"),
                ("stock-home-0000000000002", "granted"),
                ("declined-home", "declined"),
                ("unknown-home", "unknown"),
            )
        ],
        4,
    )


def files(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()
    }


class HistoricalBackfillTests(unittest.TestCase):
    def test_composed_fields_have_independent_effects_and_valid_domains(self) -> None:
        sensor = selection().sensors(183)[0]
        condition = hc.Condition(str(sensor["home_id"]), START, True, 20.0, 1.0, 1.0)

        def project(value: hc.Condition, loss: float = 1.0) -> tuple[float, float]:
            return ip.project_composed(sensor, random.Random(7), START, 2.0, 70.0, value, loss)

        baseline = project(condition)
        warmer = project(replace(condition, setpoint_c=22.0))
        ventilated = project(replace(condition, ventilation_multiplier=1.2))
        wetter = project(replace(condition, moisture_increment_hpa=2.0))
        improved = project(condition, 0.1)
        self.assertGreater(warmer[0], baseline[0])
        self.assertEqual(ventilated[0], baseline[0])
        self.assertLess(ventilated[1], baseline[1])
        self.assertGreater(wetter[1], baseline[1])
        self.assertGreater(improved[0], baseline[0])
        for changed in (
            replace(condition, home_id="other"),
            replace(condition, observed_at=START + timedelta(seconds=1)),
            replace(condition, ventilation_multiplier=0),
            replace(condition, source_type="REAL"),
        ):
            with self.assertRaises(ValueError):
                project(changed)
        with self.assertRaises(ValueError):
            project(condition, 0)

    def test_dated_effect_exact_boundary_and_other_home_neutrality(self) -> None:
        sensor = selection().sensors(183)[0]
        measure = re.Measure(
            "M1", str(sensor["home_id"]), "Loft insulation", START + timedelta(hours=1), True
        )
        kwargs = dict(
            sensor=sensor, seed=7, days=1, outdoor=[(2.0, 70.0)] * 3, start=START, composed=True
        )
        baseline = list(sb.readings(**kwargs))
        changed = list(sb.readings(**kwargs, measures=(measure,)))
        self.assertEqual(baseline[0], changed[0])
        self.assertNotEqual(baseline[1]["humidity_pct"], changed[1]["humidity_pct"])
        other = replace(measure, home_id="another-home")
        self.assertEqual(baseline, list(sb.readings(**kwargs, measures=(other,))))

    def test_compressed_bytes_repeat_and_manifest_binds_all_models(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("a", "b"):
                manifest = sb.write(
                    root / name,
                    stock=selection(),
                    climate=ConstructedClimate(),
                    days=2,
                    cadence=720,
                    compress=True,
                )
            self.assertEqual(files(root / "a"), files(root / "b"))
            self.assertEqual(manifest["rows"], 8)
            self.assertEqual(manifest["homes_covered"], 2)
            self.assertEqual(manifest["schema_version"], "sensor-fault-input-v1")
            composed, household, retrofit = (
                manifest[key] for key in ("composed_model", "household_model", "retrofit_model")
            )
            assert isinstance(composed, dict)
            assert isinstance(household, dict)
            assert isinstance(retrofit, dict)
            self.assertEqual(composed["version"], ip.COMPOSED_VERSION)
            self.assertEqual(household["version"], hc.VERSION)
            self.assertEqual(retrofit["version"], re.VERSION)
            self.assertEqual(manifest["climate_source"], ConstructedClimate().manifest())
            with gzip.open(root / "a/readings-0000.csv.gz", "rt") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual({row["home_id"] for row in rows}, {"ZF-1", "stock-home-0000000000002"})
            self.assertTrue(all(row["source_type"] == "SYNTHETIC" for row in rows))
            self.assertTrue(all("injected_fault" not in row for row in rows))
            hashes = manifest["file_sha256"]
            assert isinstance(hashes, dict)
            for name, digest in hashes.items():
                self.assertEqual(
                    hashlib.sha256((root / "a" / name).read_bytes()).hexdigest(), digest
                )

    def test_manifest_binds_explicit_dated_input_and_refuses_bad_history(self) -> None:
        measure = re.Measure("M1", "ZF-1", "Glazing", START, True)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = sb.write(root / "a", stock=selection(), climate=ConstructedClimate(), days=1)
            changed = sb.write(
                root / "b",
                stock=selection(),
                climate=ConstructedClimate(),
                measures=(measure,),
                days=1,
            )
            self.assertNotEqual(
                baseline["retrofit_history_sha256"], changed["retrofit_history_sha256"]
            )
            history = changed["retrofit_history"]
            assert isinstance(history, list)
            self.assertEqual(history[0]["home_id"], "ZF-1")
            for history in ((measure, measure), (replace(measure, home_id="missing"),)):
                with self.assertRaises(ValueError):
                    sb.write(
                        root / "bad",
                        stock=selection(),
                        climate=ConstructedClimate(),
                        measures=history,
                        days=1,
                    )
                self.assertFalse((root / "bad").exists())

    def test_fault_truth_is_separate_and_compressed_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("a", "b"):
                sb.write(
                    root / name,
                    stock=selection(),
                    climate=ConstructedClimate(),
                    days=2,
                    cadence=720,
                    fault_rates={"unmapped": 1.0},
                    compress=True,
                )
            self.assertEqual(files(root / "a"), files(root / "b"))
            with gzip.open(root / "a/analysis/readings-0000.csv.gz", "rt") as stream:
                rows = list(csv.DictReader(stream))
            with gzip.open(root / "a/truth/truth-0000.jsonl.gz", "rt") as stream:
                truth = [json.loads(line) for line in stream]
            self.assertTrue(all(len(row["sensor_id"]) == 20 for row in rows))
            self.assertTrue(all("label" not in row for row in rows))
            self.assertTrue(all(packet["label"] == "unmapped" for packet in truth))

    def test_verified_writer_load_uses_real_consumer_and_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stock = ss.select(
                [dict(synthetic_home_id="ZF-1", is_synthetic="true", monitoring_consent="granted")],
                1,
            )
            climate = ConstructedClimate()
            sb.write(root / "history", stock=stock, climate=climate, days=1, cadence=720)
            store = store_at(str(root))
            self.addCleanup(store.db.close)
            consumer = SensorConsumer(store)
            consumer.configure(
                POLICY, [replace(CONTROL, sensor_id=str(stock.sensors(183)[0]["sensor_id"]))]
            )
            result = sb.load_with_consumer(
                consumer,
                root / "history",
                stock=stock,
                climate=climate,
                received_at=RECEIVED,
                max_rows=2,
            )
            self.assertEqual(result, {"rows": 2, "outcomes": {"ACCEPTED": 1, "CLOCK_SKEW": 1}})
            self.assertEqual(
                sb.load_with_consumer(
                    consumer, root / "history", stock=stock, climate=climate, received_at=RECEIVED
                ),
                result,
            )
            self.assertEqual(
                store.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0], 1
            )
            payload = root / "history/readings-0000.csv"
            payload.write_text(payload.read_text().replace("SYNTHETIC", "REAL"))
            with patch.object(consumer, "process") as process:
                with self.assertRaisesRegex(ValueError, "differs"):
                    sb.load_with_consumer(
                        consumer,
                        root / "history",
                        stock=stock,
                        climate=climate,
                        received_at=RECEIVED,
                    )
                process.assert_not_called()

    def test_replay_count_and_actual_budget_refused_before_scratch_or_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stock, climate = selection(), ConstructedClimate()
            sb.write(root / "history", stock=stock, climate=climate, days=1, cadence=60)
            manifest_path = root / "history/manifest.json"
            original = json.loads(manifest_path.read_text())
            store = store_at(str(root))
            self.addCleanup(store.db.close)
            consumer = SensorConsumer(store)
            for overrides, budget, reason in (
                ({"homes_covered": 1}, 24, "Stock selection differs"),
                ({"homes_covered": 0}, 24, "Stock selection differs"),
                ({"homes_covered": 3}, 72, "Stock selection differs"),
                ({}, 47, "Replay budget exceeded"),
                ({"days": 730}, 2_000, "Replay budget exceeded"),
                ({"cadence_minutes": 1440}, 3, "Replay budget exceeded"),
            ):
                with self.subTest(overrides=overrides, budget=budget):
                    manifest_path.write_text(json.dumps({**original, **overrides}))
                    with (
                        patch(
                            "zava_forward.core.synthetic.sensor_backfill.tempfile.TemporaryDirectory"
                        ) as scratch,
                        patch.object(sb, "write") as write,
                        patch.object(climate, "series") as series,
                        patch.object(consumer, "process") as process,
                    ):
                        with self.assertRaisesRegex(ValueError, reason):
                            sb.load_with_consumer(
                                consumer,
                                root / "history",
                                stock=stock,
                                climate=climate,
                                received_at=RECEIVED,
                                max_rows=budget,
                            )
                        scratch.assert_not_called()
                        write.assert_not_called()
                        series.assert_not_called()
                        process.assert_not_called()

    def test_zero_granted_replay_preserves_metadata_budget(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stock = ss.select(
                [{**row, "monitoring_consent": "declined"} for row in selection().rows], 4
            )
            climate = ConstructedClimate()
            sb.write(root / "history", stock=stock, climate=climate, days=1, cadence=60)
            store = store_at(str(root))
            self.addCleanup(store.db.close)
            consumer = SensorConsumer(store)
            with (
                patch(
                    "zava_forward.core.synthetic.sensor_backfill.tempfile.TemporaryDirectory"
                ) as scratch,
                patch.object(sb, "write") as write,
                patch.object(consumer, "process") as process,
            ):
                with self.assertRaisesRegex(ValueError, "Replay budget exceeded"):
                    sb.load_with_consumer(
                        consumer,
                        root / "history",
                        stock=stock,
                        climate=climate,
                        received_at=RECEIVED,
                        max_rows=3,
                    )
                scratch.assert_not_called()
                write.assert_not_called()
                process.assert_not_called()
            self.assertEqual(
                sb.load_with_consumer(
                    consumer,
                    root / "history",
                    stock=stock,
                    climate=climate,
                    received_at=RECEIVED,
                    max_rows=4,
                ),
                {"rows": 0, "outcomes": {}},
            )

    def test_model_failure_precedes_output_and_hourly_estimate_is_measured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "missing"
            with self.assertRaises(ValueError):
                sb.write(target, homes=1, climate=ConstructedClimate())
            self.assertFalse(target.exists())
            est = sb.estimate(stock=selection(), climate=ConstructedClimate(), days=730, cadence=60)
            self.assertEqual(est["readings_per_home_nominal"], 17520)
            self.assertEqual(est["estimated_rows"], 35040)
            self.assertGreater(est["bytes_per_row_csv"], 100)
