"""The shared browser harness keeps bytecode and scratch out of the checkout when asked."""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from checks import design_system_browser_check as harness


class HarnessScratchTests(unittest.TestCase):
    def test_default_scratch_parent_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as owned:
            root = Path(owned)
            with patch.object(harness, "ROOT", root), patch.dict(os.environ, {}, clear=True):
                self.assertEqual(harness.scratch_parent(), root / ".venv")
            self.assertTrue((root / ".venv").is_dir())

    def test_external_scratch_parent_is_used_and_created(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            wanted = Path(outside) / "scratch"
            with patch.dict(os.environ, {"ZF_BROWSER_SCRATCH": str(wanted)}, clear=True):
                self.assertEqual(harness.scratch_parent(), wanted)
            self.assertTrue(wanted.is_dir())

    def test_relative_or_in_checkout_scratch_is_refused(self) -> None:
        for bad in ("relative/dir", str(harness.ROOT / "src" / "scratch")):
            with patch.dict(os.environ, {"ZF_BROWSER_SCRATCH": bad}, clear=True):
                with self.assertRaises(ValueError):
                    harness.scratch_parent()
        self.assertFalse((harness.ROOT / "src" / "scratch").exists())

    def test_child_env_passes_bytecode_controls_only_when_set(self) -> None:
        with patch.dict(os.environ, {"PATH": "/bin", "ZF_PASSWORD": "leak"}, clear=True):
            env = harness.child_env()
        self.assertEqual(env, {"PATH": "/bin"})
        with patch.dict(
            os.environ,
            {"PATH": "/bin", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": "/x"},
            clear=True,
        ):
            env = harness.child_env()
        self.assertEqual(env["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertEqual(env["PYTHONPYCACHEPREFIX"], "/x")
        self.assertNotIn("ZF_PASSWORD", env)


if __name__ == "__main__":
    unittest.main()
