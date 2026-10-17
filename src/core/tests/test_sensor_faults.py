"""Opt-in synthetic corruption and evaluator truth; only fictional stock."""

import csv
import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from zava_forward.core.synthetic import sensor_backfill as sb
from zava_forward.core.synthetic import sensor_faults as sf
from zava_forward.core.synthetic import sensor_stock


def stock() -> sensor_stock.Selection:
    return sensor_stock.select(
        [
            dict(
                synthetic_home_id=f"fictional-{i}",
                is_synthetic="true",
                monitoring_consent=choice,
            )
            for i, choice in enumerate(["granted"] * 3 + ["declined", "unknown"])
        ],
        5,
    )


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def truth(root: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for path in sorted((root / "truth").glob("truth-*.jsonl"))
        for line in path.read_text().splitlines()
    ]


def snapshot(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def clean() -> list[dict[str, str]]:
    return [
        dict(
            sensor_id="S",
            reading_id=f"S-{i}",
            home_id="fictional-0",
            observed_at=f"2026-10-16T0{i}:00:00Z",
            temperature_c=str(20 + i),
            humidity_pct=str(50 + i),
            source_type="SYNTHETIC",
            scenario="BACKFILL_2Y",
            seed="7",
            schema_version="reading-v1",
            injected_fault="",
        )
        for i in range(4)
    ]


class SensorFaultTests(unittest.TestCase):
    def test_each_class_has_observable_corruption_and_clean_truth(self) -> None:
        for name in sf.FAULTS:
            with self.subTest(name=name):
                source = clean()
                packets = list(sf.packets(source, sf.configure({name: 1.0}), 7, "S"))
                self.assertEqual([p.label for p in packets], [name, name])
                self.assertEqual(source, clean())
                packet = packets[0]
                self.assertEqual(packet.clean[0]["temperature_c"], "20")
                emitted = packet.rows
                self.assertEqual(
                    len(emitted), 0 if name == "gap" else 4 if name == "duplicate" else 2
                )
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    manifest = sb.write(
                        root, homes=1, seed=7, days=1, cadence=360, fault_rates={name: 1}
                    )
                    events = truth(root)
                    self.assertEqual([event["label"] for event in events], [name, name])
                    self.assertEqual(manifest["rows"], 2 * len(emitted))
                    estimate = manifest["estimate"]
                    assert isinstance(estimate, dict)
                    self.assertEqual(estimate["estimated_rows"], manifest["rows"])
                if name == "gap":
                    continue
                self.assertNotIn("injected_fault", emitted[0])
                if name == "duplicate":
                    self.assertEqual(emitted[0], emitted[1])
                    self.assertEqual(emitted[2], emitted[3])
                elif name == "out_of_order":
                    self.assertEqual([r["reading_id"] for r in emitted], ["S-1", "S-0"])
                    self.assertGreater(emitted[0]["observed_at"], emitted[1]["observed_at"])
                elif name == "unmapped":
                    self.assertNotEqual(emitted[0]["sensor_id"], "S")
                elif name == "wrong_unit":
                    self.assertEqual(emitted[0]["temperature_unit"], "degF")
                    self.assertEqual(float(emitted[0]["temperature_c"]), 68.0)
                elif name == "clock_skewed":
                    delta = datetime.fromisoformat(
                        emitted[0]["observed_at"]
                    ) - datetime.fromisoformat(source[0]["observed_at"])
                    self.assertEqual(delta.total_seconds(), 86400)
                elif name == "uncalibrated":
                    self.assertEqual(emitted[0]["calibrated"], "false")
                elif name == "outlier":
                    self.assertEqual(float(emitted[0]["temperature_c"]), 45.0)
                elif name == "stuck":
                    self.assertEqual(emitted[0]["temperature_c"], emitted[1]["temperature_c"])
                    self.assertEqual(emitted[0]["humidity_pct"], emitted[1]["humidity_pct"])
                elif name == "drift":
                    self.assertEqual(float(emitted[0]["temperature_c"]), 20.05)
                    self.assertEqual(float(packets[1].rows[1]["temperature_c"]), 23.20)

    def test_zero_rates_are_clean_valid_and_no_legacy_labels(self) -> None:
        packets = list(sf.packets(clean(), sf.configure({}), 7, "S"))
        self.assertEqual([p.label for p in packets], ["valid", "valid"])
        for packet in packets:
            self.assertEqual(packet.rows, packet.clean)
            for row in packet.rows:
                self.assertEqual(row["temperature_unit"], "degC")
                self.assertEqual(row["humidity_unit"], "percent")
                self.assertEqual(row["calibrated"], "true")
                self.assertNotIn("injected_fault", row)

    def test_rates_seed_order_and_empirical_coverage(self) -> None:
        # Repeated clean pairs isolate fault assignment from the indoor generator seed.
        source = clean() * 1000
        a = sf.configure({"duplicate": 0.2, "gap": 0.3})
        b = sf.configure({"gap": 0.3, "duplicate": 0.2})

        def labels(config: sf.Config, seed: int) -> list[str]:
            return [p.label for p in sf.packets(source, config, seed, "S")]

        selected = labels(a, 7)
        self.assertEqual(selected, labels(a, 7))
        self.assertEqual(selected, labels(b, 7))
        self.assertNotEqual(selected, labels(a, 8))
        self.assertNotEqual(selected, [p.label for p in sf.packets(source, a, 7, "OTHER")])
        for name, rate in (("duplicate", 0.2), ("gap", 0.3), ("valid", 0.5)):
            self.assertLess(abs(selected.count(name) / 2000 - rate), 0.04)

    def test_invalid_rates_and_window_fail_before_output(self) -> None:
        invalid: list[dict[str, float]] = [
            {"unknown": 0.1},
            {"gap": -0.1},
            {"gap": 1.1},
            {"gap": float("nan")},
            {"gap": float("inf")},
            {"gap": True},
            {"gap": 0.6, "duplicate": 0.5},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i, rates in enumerate(invalid):
                with self.subTest(rates=rates), self.assertRaises(ValueError):
                    sb.write(root / str(i), homes=1, days=1, fault_rates=rates)
                self.assertFalse((root / str(i)).exists())
            with self.assertRaisesRegex(ValueError, "even"):
                sb.write(root / "odd", homes=1, days=1, cadence=1440, fault_rates={})
            self.assertFalse((root / "odd").exists())
        for specs in (["gap=0.1", "gap=0.2"], ["gap"], ["gap=no"], ["=1"]):
            with self.subTest(specs=specs), self.assertRaises(ValueError):
                sf.parse_rates(specs)

    def test_writer_truth_positions_cross_sensors_shards_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(sb, "SHARD_HOMES", 2):
            root = Path(tmp) / "new"
            manifest = sb.write(
                root,
                stock=stock(),
                seed=7,
                days=10,
                fault_rates={"gap": 0.2, "duplicate": 0.2, "out_of_order": 0.2},
            )
            payloads = {
                path.name: rows(path) for path in (root / "analysis").glob("readings-*.csv")
            }
            self.assertEqual(len(payloads), 2)
            claimed: set[tuple[str, int]] = set()
            classes: set[str] = set()
            for event in truth(root):
                label = str(event["label"])
                classes.add(label)
                nominal = event["clean"]
                emitted = event["emitted_rows"]
                self.assertIsInstance(nominal, list)
                self.assertIsInstance(emitted, list)
                assert isinstance(nominal, list) and isinstance(emitted, list)
                self.assertEqual(len(nominal), 2)
                expected = (
                    []
                    if label == "gap"
                    else [nominal[0], nominal[0], nominal[1], nominal[1]]
                    if label == "duplicate"
                    else list(reversed(nominal))
                    if label == "out_of_order"
                    else nominal
                )
                self.assertEqual(len(emitted), len(expected))
                for pos, nominal_row in zip(emitted, expected, strict=True):
                    key = (str(event["shard"]), int(pos))
                    self.assertNotIn(key, claimed)
                    claimed.add(key)
                    self.assertEqual(payloads[key[0]][key[1]], nominal_row)
            self.assertEqual(classes, {"valid", "gap", "duplicate", "out_of_order"})
            self.assertEqual(
                claimed,
                {(name, i) for name, values in payloads.items() for i in range(len(values))},
            )
            self.assertEqual(manifest["rows"], sum(map(len, payloads.values())))
            for folder in ("analysis", "truth"):
                receipt = json.loads((root / folder / "manifest.json").read_text())
                self.assertEqual(
                    receipt["file_sha256"],
                    {
                        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in (root / folder).iterdir()
                        if p.name != "manifest.json"
                    },
                )

    def test_analysis_has_no_truth_profile_config_or_clean_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sb.write(root, stock=stock(), days=1, fault_rates={"outlier": 1})
            for path in (root / "analysis").iterdir():
                data = path.read_text()
                for forbidden in (
                    "injected_fault",
                    "fault_profile",
                    "fault_rates",
                    '"clean"',
                    "truth",
                ):
                    self.assertNotIn(forbidden, data, path.name)
            self.assertEqual(
                {r["home_id"] for r in rows(root / "analysis/sensors.csv")},
                {f"fictional-{i}" for i in range(3)},
            )
            self.assertEqual(len(truth(root)), 36)

    def test_replay_shards_estimate_and_option_order_do_not_change_assignments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = {"gap": 0.2, "duplicate": 0.2}
            for name in ("a", "b"):
                sb.write(root / name, stock=stock(), seed=7, days=2, fault_rates=config)
            self.assertEqual(snapshot(root / "a"), snapshot(root / "b"))
            sb.estimate(stock=stock(), seed=7, days=2, fault_rates=config)
            with patch.object(sb, "SHARD_HOMES", 1):
                sb.write(
                    root / "c",
                    stock=stock(),
                    seed=7,
                    days=2,
                    fault_rates=dict(reversed(list(config.items()))),
                )

            def assignments(path: Path) -> list[tuple[str, str, object]]:
                return sorted(
                    (str(e["sensor_id"]), str(e["packet"]), e["label"]) for e in truth(path)
                )

            self.assertEqual(assignments(root / "a"), assignments(root / "c"))
            self.assertEqual(
                rows(root / "a/analysis/sensors.csv"), rows(root / "c/analysis/sensors.csv")
            )
            self.assertIn(Path(sf.__file__), sb.revision_sources(faults=True))
            receipt = json.loads((root / "a/truth/manifest.json").read_text())
            self.assertEqual(
                receipt["analysis_manifest_sha256"],
                hashlib.sha256((root / "a/analysis/manifest.json").read_bytes()).hexdigest(),
            )

    def test_empty_choice_and_nonempty_output_safety(self) -> None:
        declined = sensor_stock.select(
            [
                dict(
                    synthetic_home_id="fictional-x",
                    is_synthetic="true",
                    monitoring_consent="declined",
                )
            ],
            1,
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "new"
            manifest = sb.write(root, stock=declined, days=1, fault_rates={"gap": 1})
            self.assertEqual(manifest["rows"], 0)
            self.assertEqual(truth(root), [])
            self.assertEqual(rows(root / "analysis/sensors.csv"), [])
            before = snapshot(root)
            with self.assertRaises(FileExistsError):
                sb.write(root, stock=declined, days=1, fault_rates={})
            self.assertEqual(before, snapshot(root))
            alias = Path(tmp) / "alias"
            alias.symlink_to(root, target_is_directory=True)
            with self.assertRaises((ValueError, FileExistsError)):
                sb.write(alias, stock=declined, days=1, fault_rates={})

    def test_loader_refuses_new_schema_before_database_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, sqlite3.connect(":memory:") as conn:
            root = Path(tmp)
            sb.write(root, homes=1, days=1, fault_rates={})
            for path in (root, root / "analysis"):
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, "fault"):
                    sb.load_into(conn, path)
                self.assertEqual(conn.execute("SELECT name FROM sqlite_master").fetchall(), [])

    def test_cli_tiny_register_replay_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            register = root / "register.csv"
            register.write_text(
                "synthetic_home_id,is_synthetic,monitoring_consent\n"
                "fictional-a,true,granted\nfictional-b,true,declined\nfictional-c,true,unknown\n"
            )
            command = [
                sys.executable,
                "-m",
                "zava_forward.core.synthetic.sensor_backfill",
                "--register",
                str(register),
                "--homes",
                "3",
                "--days",
                "2",
                "--cadence",
                "360",
                "--as-of",
                "2026-10-17",
                "--seed",
                "7",
            ]
            for name, specs in (
                ("a", ["gap=0.2", "duplicate=0.2"]),
                ("b", ["duplicate=0.2", "gap=0.2"]),
            ):
                args = [x for spec in specs for x in ("--fault-rate", spec)]
                result = subprocess.run(
                    [*command, *args, "--out", str(root / name)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(json.loads(result.stdout)["homes_covered"], 1)
            self.assertEqual(snapshot(root / "a"), snapshot(root / "b"))
            estimated = subprocess.run(
                [
                    *command,
                    "--fault-rate",
                    "gap=0.2",
                    "--fault-rate",
                    "duplicate=0.2",
                    "--estimate-only",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                json.loads(estimated.stdout),
                json.loads((root / "a/analysis/estimate.json").read_text()),
            )
            result = subprocess.run(
                [*command, "--fault-rate", "gap=nan", "--out", str(root / "bad")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("finite", result.stderr)
            self.assertFalse((root / "bad").exists())
