"""The handover verifier exits 0 only for a literal passed True; null and empty never pass."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from zava_forward.api import sensor_handover_verify as verify


def run_main(rows: str, result: object) -> tuple[int, str]:
    out = io.StringIO()
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "reference.csv"
        path.write_text(rows)
        with (
            mock.patch.object(verify, "open_existing_store", lambda writable=False: object()),
            mock.patch.object(verify, "run", lambda *args, **kwargs: result),
            contextlib.redirect_stdout(out),
        ):
            code = verify.main(["--reference", str(path), "--handover", "2026-11-09T10:00:00Z"])
    return code, out.getvalue()


class FailClosedTests(unittest.TestCase):
    def test_only_a_literal_true_passes(self) -> None:
        self.assertEqual(run_main("home_id\n", {"passed": True})[0], 0)
        for result in (None, {}, {"passed": 1}, {"passed": "true"}, {"passed": None}, [True]):
            with self.subTest(result=result):
                code, text = run_main("home_id\n", result)
                self.assertEqual(code, 2, text)
                self.assertFalse(json.loads(text.splitlines()[0])["passed"])

    def test_empty_reference_is_refused(self) -> None:
        out = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reference.csv"
            path.write_text("")
            with (
                mock.patch.object(verify, "open_existing_store", lambda writable=False: object()),
                contextlib.redirect_stdout(out),
            ):
                code = verify.main(["--reference", str(path), "--handover", "2026-11-09T10:00:00Z"])
        self.assertNotEqual(code, 0)
        self.assertFalse(json.loads(out.getvalue())["passed"])


if __name__ == "__main__":
    unittest.main()
