"""Exact snapshot bytes, source provenance and refresh protection, without private data."""

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from zava_forward.core.synthetic import provenance
from zava_forward.core.synthetic import scale_fixture as sf
from zava_forward.core.synthetic import sensor_backfill as sb


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.name: p.read_bytes() for p in sorted(root.iterdir())}


class SyntheticDeterminismTests(unittest.TestCase):
    def assert_manifest(self, root: Path, seed: int, as_of: str) -> None:
        manifest = json.loads((root / "manifest.json").read_text())
        self.assertEqual(manifest["seed"], seed)
        self.assertEqual(manifest["as_of"], as_of)
        self.assertTrue(manifest["version"])
        self.assertRegex(manifest["generator_revision"], r"^sha256:[0-9a-f]{64}$")
        payloads = {name: data for name, data in snapshot(root).items() if name != "manifest.json"}
        self.assertEqual(
            manifest["file_sha256"],
            {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()},
        )

    def test_scale_all_files_reproduce_and_seed_changes_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, seed in (("a", 7), ("b", 7), ("c", 8)):
                sf.write(root / name, n=12, per_home=3, seed=seed, as_of="2026-10-15")
                self.assert_manifest(root / name, seed, "2026-10-15")
            self.assertEqual(snapshot(root / "a"), snapshot(root / "b"))
            self.assertNotEqual(
                (root / "a/homes.jsonl").read_bytes(), (root / "c/homes.jsonl").read_bytes()
            )
            sf.write(root / "later", n=12, per_home=3, seed=7, as_of="2027-01-01")
            self.assertNotEqual(
                (root / "a/manifest.json").read_bytes(), (root / "later/manifest.json").read_bytes()
            )
            for name in ("homes", "households", "events"):
                self.assertEqual(
                    (root / f"a/{name}.jsonl").read_bytes(),
                    (root / f"later/{name}.jsonl").read_bytes(),
                )
            events = [
                json.loads(line) for line in (root / "a/events.jsonl").read_text().splitlines()
            ]
            self.assertTrue(all(row["day"].startswith("2026-") for row in events))

    def test_sensor_all_shards_reproduce_and_date_and_seed_change_readings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, patch.object(sb, "SHARD_HOMES", 2):
            root = Path(tmp)
            for name, seed, as_of in (
                ("a", 7, "2026-10-15"),
                ("b", 7, "2026-10-15"),
                ("c", 8, "2026-10-15"),
                ("d", 7, "2026-10-16"),
            ):
                sb.write(root / name, homes=5, seed=seed, days=2, cadence=360, as_of=as_of)
                self.assert_manifest(root / name, seed, as_of)
            self.assertEqual(snapshot(root / "a"), snapshot(root / "b"))
            self.assertEqual(len(list((root / "a").glob("readings-*.csv"))), 3)
            for name in ("c", "d"):
                self.assertNotEqual(
                    (root / "a/readings-0000.csv").read_bytes(),
                    (root / name / "readings-0000.csv").read_bytes(),
                )
            manifest = json.loads((root / "a/manifest.json").read_text())
            self.assertEqual(manifest["stock_seed"], sf.SEED)
            start = datetime(2026, 10, 13, tzinfo=UTC)
            end = datetime(2026, 10, 15, tzinfo=UTC)
            self.assertEqual(manifest["start"], start.isoformat())
            self.assertEqual(manifest["end_exclusive"], end.isoformat())
            count = 0
            for shard in (root / "a").glob("readings-*.csv"):
                with shard.open(newline="") as payload:
                    for row in csv.DictReader(payload):
                        observed = datetime.fromisoformat(row["observed_at"])
                        self.assertLessEqual(start, observed)
                        self.assertLess(observed, end)
                        self.assertEqual((observed - start).total_seconds() % (360 * 60), 0)
                        self.assertEqual(row["source_type"], "SYNTHETIC")
                        count += 1
            self.assertEqual(manifest["rows"], count)

    def test_historical_payloads_are_unchanged(self) -> None:
        expected = {
            "scale": {
                "events.jsonl": "32157fc81abf5c9d6a12dfe564283ec1f067736ea6cf1f1f5864e5cf64e70e60",
                "homes.jsonl": "7a40714ae50da64be9733c4fa0a39e1c8db71acdac31996b449f42feb907763f",
                "households.jsonl": (
                    "12ccc7a2ad73f235748ee7f005547e9a7fc684f604a1b1b319776ad47e02cfea"
                ),
            },
            "sensor": {
                "readings-0000.csv": (
                    "657ff373107807b34bd4bb6720dec534fcef13134292c5d753ef24bdbd723549"
                ),
                "sensors.csv": "1bb5907d55570685a40f0603abd9086def4bd3540726d5f13316d6816b99c400",
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sf.write(root / "scale", n=12, per_home=3)
            sb.write(root / "sensor", homes=12, days=3)
            for generator, hashes in expected.items():
                for name, digest in hashes.items():
                    self.assertEqual(
                        hashlib.sha256((root / generator / name).read_bytes()).hexdigest(), digest
                    )
            manifest = json.loads((root / "sensor/manifest.json").read_text())
            self.assertEqual(manifest["start"], sb.START.isoformat())
            self.assertEqual(manifest["as_of"], "2024-10-04")
            self.assertEqual(sb.resolve_window(730, 60)[1].date().isoformat(), "2026-10-01")

    def test_estimate_and_cli_use_requested_window(self) -> None:
        with (
            tempfile.TemporaryDirectory() as tmp,
            patch.object(sb, "estimate", wraps=sb.estimate) as estimate,
        ):
            root = Path(tmp)
            sb.write(root, homes=5, days=2, cadence=360, as_of="2026-10-15")
            self.assertEqual(estimate.call_args.kwargs["start"], datetime(2026, 10, 13, tzinfo=UTC))
            manifest = json.loads((root / "manifest.json").read_text())
            self.assertEqual(json.loads((root / "estimate.json").read_text()), manifest["estimate"])
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "zava_forward.core.synthetic.sensor_backfill",
                    "--estimate-only",
                    "--homes",
                    "5",
                    "--days",
                    "2",
                    "--cadence",
                    "360",
                    "--as-of",
                    "2026-10-15",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(result.stdout), manifest["estimate"])

    def test_invalid_inputs_leave_destination_absent_or_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name, value in (
                ("homes", 0),
                ("days", 0),
                ("days", 9999999999),
                ("cadence", 0),
                ("cadence", 61),
                ("as_of", "not-a-date"),
                ("as_of", "20261015"),
                ("as_of", "0001-01-01"),
            ):
                for exists in (False, True):
                    out = root / f"{name}-{value}-{exists}"
                    if exists:
                        out.mkdir()
                    with self.subTest(name=name, value=value, exists=exists):
                        with self.assertRaises(ValueError):
                            sb.write(
                                out,
                                homes=0 if name == "homes" else 1,
                                days=value if name == "days" and isinstance(value, int) else 2,
                                cadence=value
                                if name == "cadence" and isinstance(value, int)
                                else 360,
                                as_of=value if name == "as_of" and isinstance(value, str) else None,
                            )
                        self.assertEqual(out.exists(), exists)
                        if exists:
                            self.assertEqual(snapshot(out), {})
            for n, per_home, as_of in ((0, 1, sf.AS_OF), (1, 0, sf.AS_OF), (1, 1, "bad")):
                out = root / f"scale-{n}-{per_home}-{as_of}"
                with self.assertRaises(ValueError):
                    sf.write(out, n=n, per_home=per_home, as_of=as_of)
                self.assertFalse(out.exists())
            sb.write(root / "valid-boundary", homes=1, days=1, as_of="0001-01-02")
            with (root / "valid-boundary/readings-0000.csv").open(newline="") as payload:
                rows = list(csv.DictReader(payload))
            self.assertTrue(rows)
            self.assertEqual(
                datetime.fromisoformat(rows[0]["observed_at"]), datetime(1, 1, 1, tzinfo=UTC)
            )

    def test_nonempty_refresh_refused_without_changing_any_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sf.write(root / "scale", n=2, per_home=1)
            sb.write(root / "sensor", homes=2, days=1)
            before = {name: snapshot(root / name) for name in ("scale", "sensor")}
            with self.assertRaisesRegex(FileExistsError, "new snapshot"):
                sf.write(root / "scale", n=1, per_home=1, seed=99)
            with self.assertRaisesRegex(FileExistsError, "new snapshot"):
                sb.write(root / "sensor", homes=1, seed=99, days=1)
            for name in before:
                self.assertEqual(snapshot(root / name), before[name])
            (root / "alias").symlink_to(root / "sensor", target_is_directory=True)
            with self.assertRaisesRegex(FileExistsError, "symlink"):
                provenance.prepare_output(root / "alias")

    def test_revision_tracks_each_dependency_without_path_or_order_dependence(self) -> None:
        original = Path.read_bytes
        for generator in (sf, sb):
            sources = generator.revision_sources()
            expected = {"scale_fixture.py", "provenance.py", "__init__.py", "insights.py"}
            if generator is sb:
                expected.update(
                    {
                        "sensor_backfill.py",
                        "sensor_stock.py",
                        "stock_fabric.py",
                        "indoor_projection.py",
                    }
                )
            self.assertEqual({p.name for p in sources}, expected)
            base = provenance.source_revision(sources)
            for source in sources:

                def changed(path: Path, selected: Path = source) -> bytes:
                    return original(path) + (b"\n# changed dependency" if path == selected else b"")

                with patch.object(Path, "read_bytes", changed):
                    self.assertNotEqual(provenance.source_revision(sources), base)
            with patch.object(Path, "read_bytes", return_value=b"fixed source"):
                self.assertEqual(
                    provenance.source_revision(reversed(sources)),
                    provenance.source_revision(Path("/other/root") / p.name for p in sources),
                )
        with self.assertRaisesRegex(ValueError, "unique"):
            provenance.source_revision([Path("/one/a.py"), Path("/two/a.py")])
