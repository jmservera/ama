"""Seed manifest, digest reproducibility and pre-write validation (issue #162)."""

import json
import random
import tempfile
import unittest
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.synthetic import generator_pipeline as gp

CONFIG = gp.GeneratorConfig("demo", "1.0.0", seed=162, as_of="2026-11-14", params={"n": 5})


def generate(config: gp.GeneratorConfig, rnd: random.Random) -> gp.Records:
    return {"rows.jsonl": [{"i": i, "v": rnd.random()} for i in range(config.params["n"])]}


def non_empty(records: gp.Records) -> list[str]:
    return [] if records["rows.jsonl"] else ["rows.jsonl is empty"]


def clock_at(hour: int) -> Callable[[], datetime]:
    return lambda: datetime(2026, 11, 14, hour, tzinfo=UTC)


class GeneratorPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, self.tmp, True)

    def test_same_seed_and_config_give_identical_digests_despite_timestamp(self) -> None:
        a = gp.run(CONFIG, generate, self.tmp / "a", validators=[non_empty], clock=clock_at(1))
        b = gp.run(CONFIG, generate, self.tmp / "b", validators=[non_empty], clock=clock_at(9))
        self.assertEqual(a["output_sha256"], b["output_sha256"])
        self.assertEqual(a["file_sha256"], b["file_sha256"])
        self.assertNotEqual(a["generated_at"], b["generated_at"])

    def test_manifest_records_seed_config_version_and_timestamp(self) -> None:
        gp.run(CONFIG, generate, self.tmp / "a", clock=clock_at(3))
        manifest = json.loads((self.tmp / "a" / gp.MANIFEST_NAME).read_text())
        self.assertEqual(manifest["seed"], 162)
        self.assertEqual(manifest["config_version"], "1.0.0")
        self.assertEqual(manifest["config_sha256"], CONFIG.digest())
        self.assertEqual(manifest["generated_at"], "2026-11-14T03:00:00+00:00")

    def test_different_seed_or_params_change_digests(self) -> None:
        base = gp.run(CONFIG, generate, self.tmp / "a")
        seed = gp.GeneratorConfig("demo", "1.0.0", 163, "2026-11-14", {"n": 5})
        more = gp.GeneratorConfig("demo", "1.0.0", 162, "2026-11-14", {"n": 6})
        self.assertNotEqual(
            base["output_sha256"], gp.run(seed, generate, self.tmp / "b")["output_sha256"]
        )
        self.assertNotEqual(base["config_sha256"], more.digest())

    def test_failed_validation_writes_nothing(self) -> None:
        empty = gp.GeneratorConfig("demo", "1.0.0", 1, "2026-11-14", {"n": 0})
        out = self.tmp / "never"
        with self.assertRaises(gp.PipelineValidationError) as caught:
            gp.run(empty, generate, out, validators=[non_empty])
        self.assertEqual(caught.exception.failures, ("rows.jsonl is empty",))
        self.assertFalse(out.exists())

    def test_naive_timestamp_and_bad_config_are_rejected_before_write(self) -> None:
        with self.assertRaises(ValueError):
            gp.run(CONFIG, generate, self.tmp / "n", clock=lambda: datetime(2026, 11, 14))
        self.assertFalse((self.tmp / "n").exists())
        with self.assertRaises(ValueError):
            gp.run(gp.GeneratorConfig("demo", "", 1, "2026-11-14"), generate, self.tmp / "v")

    def test_verify_detects_tampering_and_config_drift(self) -> None:
        out = self.tmp / "a"
        gp.run(CONFIG, generate, out)
        self.assertEqual(gp.verify(out, CONFIG, generate), [])
        (out / "rows.jsonl").write_bytes(b"{}\n")
        self.assertTrue(any("bytes differ" in p for p in gp.verify(out, CONFIG, generate)))
        drift = gp.GeneratorConfig("demo", "1.0.1", 162, "2026-11-14", {"n": 5})
        self.assertTrue(any("config_version" in p for p in gp.verify(out, drift, generate)))

    def test_existing_output_is_not_replaced(self) -> None:
        out = self.tmp / "a"
        gp.run(CONFIG, generate, out)
        with self.assertRaises(FileExistsError):
            gp.run(CONFIG, generate, out)


if __name__ == "__main__":
    unittest.main()
