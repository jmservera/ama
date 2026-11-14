"""Repository-side guard for Issue #201: private mvp/data stays outside git.

Reads only git metadata and tracked documentation; no private dataset is opened.
Owner confirmation of the external backup remains a human gate, not tested here.
"""

import importlib.util
import re
import subprocess
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATHS = ROOT / "src/core/src/zava_forward/core/data_paths.py"


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=check
    )


def _load_data_paths():
    spec = importlib.util.spec_from_file_location("zf_data_paths", DATA_PATHS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrivateMvpDataExclusionTest(unittest.TestCase):
    def test_no_mvp_data_files_are_tracked(self) -> None:
        tracked = _git("ls-files", "--", "mvp/data").stdout.splitlines()
        self.assertEqual([], tracked)

    def test_gitignore_excludes_private_runtime_datasets(self) -> None:
        lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("/mvp/data/", lines)
        self.assertIn("/src/**/data/", lines)
        for probe in ("mvp/data/zavaforward.json", "src/api/data/zavaforward.json"):
            result = _git("check-ignore", "-q", "--no-index", probe, check=False)
            self.assertEqual(0, result.returncode, f"{probe} is not ignored")

    def test_zf_data_defaults_outside_repository(self) -> None:
        home = Path("/home/example-user")
        module = _load_data_paths()
        with unittest.mock.patch.object(module.Path, "home", return_value=home):
            default = module.data_file({})
        self.assertEqual(home / ".zava-forward/data/zavaforward.json", default)
        self.assertFalse(default.is_relative_to(ROOT))

    def test_documentation_states_external_data_location(self) -> None:
        src_readme = (ROOT / "src/README.md").read_text(encoding="utf-8")
        self.assertIn("never under `src/`", src_readme)
        self.assertIn("`/src/**/data/` gitignore entry", src_readme)
        self.assertTrue((ROOT / "README.md").is_file())

    def test_owner_backup_confirmation_is_an_external_gate(self) -> None:
        # Git cannot prove an external backup exists; the docs must not claim one.
        text = (ROOT / "src/README.md").read_text(encoding="utf-8")
        flat = re.sub(r"\s+", " ", text)
        self.assertIn("does not assert new Azure deployment, private backup", flat)


if __name__ == "__main__":
    unittest.main()
