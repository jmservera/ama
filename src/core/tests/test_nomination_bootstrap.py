"""Fresh-process checks that the nomination test bootstrap keeps module identity (#1847)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_TESTS = Path(__file__).resolve().parent
_CORE_SRC = _TESTS.parent / "src"
_AGENTS_SRC = _TESTS.parents[1] / "agents" / "src"

_IDENTITY = """
import json, sys
import test_bulk_edits as b
import test_nomination_route as n
{first}
mod = sys.modules["zava_forward.core.store"]
bulk = sys.modules["zava_forward.core.bulk_edits"]
print(json.dumps({{
    "conflict": n.ConflictError is b.ConflictError is mod.ConflictError,
    "gate": n.GateError is mod.GateError,
    "store": n.Store is b.Store is mod.Store,
    "patch_target": b.bulk_edits is bulk,
    "store_file": mod.__file__,
}}))
"""

_FOREIGN_FIRST = """
import json, sys
import zava_forward.core.store as foreign
before = list(sys.path)
try:
    import test_nomination_route
    outcome = "imported"
except ImportError as exc:
    outcome = "rejected: " + str(exc)
print(json.dumps({
    "outcome": outcome,
    "foreign_kept": sys.modules["zava_forward.core.store"] is foreign,
    "path_unchanged": sys.path == before,
    "nomination_loaded": "test_nomination_route" in sys.modules,
}))
"""


class NominationBootstrapIdentityTests(unittest.TestCase):
    def _run(self, code: str, *roots: Path) -> dict[str, object]:
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env["PYTHONPATH"] = os.pathsep.join(str(r) for r in roots)
        done = subprocess.run(
            [sys.executable, "-c", code],
            cwd=_TESTS,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr[-2000:])
        return dict(json.loads(done.stdout.strip().splitlines()[-1]))

    def _assert_source_identity(self, result: dict[str, object]) -> None:
        for key in ("conflict", "gate", "store", "patch_target"):
            self.assertTrue(result[key], key)
        self.assertTrue(Path(str(result["store_file"])).is_relative_to(_TESTS.parents[1]))

    def _foreign_root(self, tmp: str) -> Path:
        pkg = Path(tmp) / "zava_forward" / "core"
        pkg.mkdir(parents=True)
        (pkg / "store.py").write_text("FOREIGN = True\n", encoding="utf-8")
        return Path(tmp)

    def test_source_layout_both_orders_share_identity(self) -> None:
        roots = (_CORE_SRC, _AGENTS_SRC, _TESTS)
        for first in ("import test_bulk_edits", "import test_nomination_route"):
            with self.subTest(first=first):
                code = _IDENTITY.format(first=first)
                if first.endswith("nomination_route"):
                    code = code.replace(
                        "import test_bulk_edits as b\nimport test_nomination_route as n\n",
                        "import test_nomination_route as n\nimport test_bulk_edits as b\n",
                    )
                self._assert_source_identity(self._run(code, *roots))

    def test_foreign_layout_nomination_first_uses_source_only(self) -> None:
        code = _IDENTITY.format(first="").replace(
            "import test_bulk_edits as b\nimport test_nomination_route as n\n",
            "import test_nomination_route as n\nimport test_bulk_edits as b\n",
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(code, _TESTS, self._foreign_root(tmp))
        self._assert_source_identity(result)

    def test_foreign_module_loaded_first_is_rejected_without_purge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(
                _FOREIGN_FIRST, self._foreign_root(tmp), _TESTS, _CORE_SRC, _AGENTS_SRC
            )
        self.assertTrue(str(result["outcome"]).startswith("rejected: unsupported layout"))
        self.assertTrue(result["foreign_kept"])
        self.assertTrue(result["path_unchanged"])
        self.assertFalse(result["nomination_loaded"])


if __name__ == "__main__":
    unittest.main()
