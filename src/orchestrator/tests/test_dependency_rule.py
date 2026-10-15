import ast
import tempfile
import unittest
from pathlib import Path

PROJECT = "orchestrator"
ALLOWED = {"orchestrator", "core"}
ROOT = Path(__file__).resolve().parents[1]


def imported_projects(path: Path) -> set[str]:
    """Return the zava_forward sub-packages that a source file imports."""
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module, *(f"{node.module}.{alias.name}" for alias in node.names)]
        for name in names:
            parts = name.split(".")
            if parts[0] == "zava_forward" and len(parts) > 1:
                found.add(parts[1])
    return found


class DependencyRuleTests(unittest.TestCase):
    def test_project_imports_only_allowed_projects(self) -> None:
        files = [*(ROOT / "src").rglob("*.py"), *(ROOT / "tests").rglob("*.py")]
        self.assertTrue(files)
        for path in files:
            with self.subTest(file=path.relative_to(ROOT).as_posix()):
                self.assertLessEqual(imported_projects(path), ALLOWED)

    def test_detector_reports_forbidden_imports(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            sample = Path(folder) / "sample.py"
            sample.write_text(
                "import zava_forward.api\nfrom zava_forward import importer\n"
                "from zava_forward.core.x import y\n",
                encoding="utf-8",
            )
            self.assertEqual(imported_projects(sample), {"api", "importer", "core"})
            self.assertFalse(imported_projects(sample) <= ALLOWED)


if __name__ == "__main__":
    unittest.main()
