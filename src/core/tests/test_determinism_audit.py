"""The determinism audit passes for in-repo generators and never hides the absent register."""

import json
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.synthetic import determinism_audit as da


class DeterminismAuditTests(unittest.TestCase):
    def test_all_in_repo_generators_replay_with_complete_manifests(self) -> None:
        report = da.audit()
        results = report["results"]
        assert isinstance(results, list)
        self.assertEqual(
            {r["generator"] for r in results},
            {"scale-fixture", "sensor-backfill", "sensor-scenarios", "stock-fabric"},
        )
        for r in results:
            self.assertEqual(r["status"], "PASS", r)
            self.assertTrue(r["byte_identical"])
            self.assertEqual(r["manifest_missing"], [])
        self.assertTrue(report["all_available_pass"])

    def test_original_stock_register_is_reported_unavailable(self) -> None:
        report = da.audit()
        unavailable = report["unavailable"]
        assert isinstance(unavailable, dict)
        self.assertIn("stock-register", unavailable)

    def test_nondeterministic_generator_fails(self) -> None:
        counter = iter(range(100))

        def drift(out: Path) -> Path:
            out.mkdir(parents=True)
            (out / "manifest.json").write_text(
                '{"seed": 7, "version": "v", "generator_revision": "sha256:' + "a" * 64 + '"}'
            )
            (out / "data.txt").write_text(str(next(counter)))
            return out / "manifest.json"

        self.assertEqual(da._check("drift", drift)["status"], "FAIL")

    def test_truncated_revision_fails_even_when_output_is_identical(self) -> None:
        for revision in ("sha256:", "sha256:ab", "sha256:" + "g" * 64, "sha256:" + "a" * 65):

            def fixed(out: Path, revision: str = revision) -> Path:
                out.mkdir(parents=True)
                manifest = {"seed": 7, "version": "v", "generator_revision": revision}
                (out / "manifest.json").write_text(json.dumps(manifest))
                return out / "manifest.json"

            result = da._check("fixed", fixed)
            self.assertEqual(result["status"], "FAIL", revision)
            self.assertEqual(result["manifest_missing"], ["generator_revision"])

    def test_valid_revision_passes(self) -> None:
        def fixed(out: Path) -> Path:
            out.mkdir(parents=True)
            manifest = {"seed": 7, "version": "v", "generator_revision": "sha256:" + "a" * 64}
            (out / "manifest.json").write_text(json.dumps(manifest))
            return out / "manifest.json"

        self.assertEqual(da._check("fixed", fixed)["status"], "PASS")

    def test_scenario_reports_intrinsic_window_not_as_of(self) -> None:
        results: list[dict[str, Any]] = da.audit()["results"]  # type: ignore[assignment]
        windows = {r["generator"]: r["window"] for r in results}
        self.assertEqual(windows["sensor-scenarios"]["basis"], "intrinsic")
        self.assertEqual(windows["sensor-scenarios"]["start"], "2024-01-01")
        self.assertNotIn("as_of", windows["sensor-scenarios"])
        self.assertEqual(windows["scale-fixture"], {"basis": "as_of", "as_of": da.AS_OF})

    def test_missing_manifest_fields_fail(self) -> None:
        def bare(out: Path) -> Path:
            out.mkdir(parents=True)
            (out / "manifest.json").write_text('{"seed": 1}')
            return out / "manifest.json"

        result = da._check("bare", bare)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["manifest_missing"], ["seed", "version", "generator_revision"])

    def test_cli_exit_code_follows_replay_result(self) -> None:
        with patch.object(da, "audit", return_value={"all_available_pass": False}):
            with self.assertRaises(SystemExit) as ctx:
                da.main([])
        self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
