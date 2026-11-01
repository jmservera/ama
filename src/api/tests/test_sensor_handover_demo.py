"""Local handover demo: clean pass, idempotent replay, and a seam that must fail."""

import contextlib
import io
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "checks"))

import sensor_handover_demo as demo  # type: ignore[import-not-found]  # noqa: E402


def run(*args: str) -> tuple[int, dict[str, object]]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = demo.main(list(args))
    return code, json.loads(out.getvalue())


class HandoverDemoTests(unittest.TestCase):
    def test_clean_handover_passes_and_replay_is_idempotent(self) -> None:
        code, result = run()
        self.assertEqual(code, 0, result)
        self.assertTrue(result["passed"] and result["idempotent"])
        self.assertIn("not live Hub", str(result["evidence"]))

    def test_seam_fails_at_zero_tolerance_and_passes_within_declared_limit(self) -> None:
        code, result = run("--seam", "1.5")
        self.assertEqual(code, 1)
        self.assertFalse(result["passed"])
        code, result = run("--seam", "1.5", "--tolerance", "2.0")
        self.assertEqual(code, 0, result)

    def test_invalid_tolerance_is_a_structured_refusal(self) -> None:
        for value in ("-1", "nan", "inf"):
            code, result = run("--tolerance", value)
            self.assertEqual(code, 2, value)
            self.assertFalse(result["passed"])
            self.assertIn("tolerance", str(result["refusal"]))

    def test_sql_mode_is_refused(self) -> None:
        with mock.patch.dict(os.environ, {"ZF_SENSOR_MSSQL": "1"}):
            code, result = run()
        self.assertEqual(code, 2)
        self.assertIn("SQLite-only", str(result["refusal"]))


if __name__ == "__main__":
    unittest.main()
