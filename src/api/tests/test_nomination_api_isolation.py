"""Fresh-process checks that API nomination tests run on this checkout only (#1847)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_API = Path(__file__).resolve().parents[1]
_SRC = _API.parent
_ROOTS = (
    _API / "src",
    _API / "tests",
    _SRC / "core" / "src",
    _SRC / "agents" / "src",
    _SRC / "core" / "tests",
    _SRC / "agents" / "tests",
)

_SOURCE = """
import json, sys
{imports}
mod = sys.modules["zava_forward.core.store"]
srv = sys.modules["zava_forward.api.server"]
print(json.dumps({{
    "conflict": n.ConflictError is mod.ConflictError,
    "gate": n.GateError is mod.GateError,
    "store": n.Store is mod.Store,
    "store_file": mod.__file__,
    "server_file": srv.__file__,
}}))
"""

_FOREIGN_FIRST = """
import json, sys
import zava_forward.core.store as foreign

def family():
    return {n: id(m) for n, m in sys.modules.items()
            if n == "zava_forward" or n.startswith("zava_forward.")}

path = list(sys.path)
snapshot = family()
outcomes = []
for _ in range(2):
    try:
        import tests.test_nomination_api_routes
        outcomes.append("imported")
    except ImportError as exc:
        outcomes.append("rejected: " + str(exc))
print(json.dumps({
    "outcomes": outcomes,
    "family_unchanged": all(family().get(k) == v for k, v in snapshot.items()),
    "foreign_kept": sys.modules["zava_forward.core.store"] is foreign,
    "path_unchanged": sys.path == path,
}))
"""

_IMPORT_PAIRS = {
    "api_first": (
        "import tests.test_nomination_api_routes as a\nimport test_nomination_route as n\n"
    ),
    "core_first": (
        "import test_nomination_route as n\nimport tests.test_nomination_api_routes as a\n"
    ),
}


class NominationApiIsolationTests(unittest.TestCase):
    def _run(self, code: str, *roots: Path) -> dict[str, object]:
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env["PYTHONPATH"] = os.pathsep.join(str(r) for r in roots)
        done = subprocess.run(
            [sys.executable, "-c", code],
            cwd=_API,
            env=env,
            capture_output=True,
            text=True,
            timeout=300,
        )
        self.assertEqual(done.returncode, 0, done.stderr[-2000:])
        return dict(json.loads(done.stdout.strip().splitlines()[-1]))

    def test_source_layout_both_orders_share_identity_and_origin(self) -> None:
        for order, imports in _IMPORT_PAIRS.items():
            with self.subTest(order=order):
                result = self._run(_SOURCE.format(imports=imports), *_ROOTS)
                for key in ("conflict", "gate", "store"):
                    self.assertTrue(result[key], key)
                for key in ("store_file", "server_file"):
                    self.assertTrue(Path(str(result[key])).is_relative_to(_SRC), key)

    def test_foreign_module_loaded_first_is_rejected_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pkg = Path(tmp) / "zava_forward" / "core"
            pkg.mkdir(parents=True)
            shutil.copy(
                _SRC / "core" / "src" / "zava_forward" / "core" / "store.py", pkg / "store.py"
            )
            result = self._run(_FOREIGN_FIRST, Path(tmp), *_ROOTS)
        outcomes = [str(o) for o in result["outcomes"]]  # type: ignore[attr-defined]
        for outcome in outcomes:
            self.assertTrue(outcome.startswith("rejected: unsupported layout"), outcome)
        self.assertEqual(outcomes[0], outcomes[1])
        self.assertTrue(result["foreign_kept"])
        self.assertTrue(result["family_unchanged"])
        self.assertTrue(result["path_unchanged"])


if __name__ == "__main__":
    unittest.main()
