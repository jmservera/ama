"""Fresh-process checks that the nomination test bootstrap keeps module identity (#1847)."""

from __future__ import annotations

import json
import os
import shutil
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

def family():
    return {n: id(m) for n, m in sys.modules.items()
            if n == "zava_forward" or n.startswith("zava_forward.")}

before = list(sys.path)
snapshot = family()
try:
    import test_nomination_route
    outcome = "imported"
except ImportError as exc:
    outcome = "rejected: " + str(exc)
try:
    import test_nomination_route
    second = "imported"
except ImportError as exc:
    second = "rejected: " + str(exc)
print(json.dumps({
    "family_unchanged": family() == snapshot,
    "second_matches_first": second == outcome,
    "outcome": outcome,
    "foreign_kept": sys.modules["zava_forward.core.store"] is foreign,
    "path_unchanged": sys.path == before,
    "nomination_loaded": "test_nomination_route" in sys.modules,
}))
"""

_COPY_BULK_FIRST = """
import json, sys
def family():
    return {n: id(m) for n, m in sys.modules.items()
            if n == "zava_forward" or n.startswith("zava_forward.")}
before = list(sys.path)
try:
    import test_bulk_edits as b
except ImportError as exc:
    print(json.dumps({"bulk_rejected": str(exc)}))
    raise SystemExit(0)
snapshot = family()
try:
    import test_nomination_route
    outcome = "imported"
except ImportError as exc:
    outcome = "rejected: " + str(exc)
store = sys.modules["zava_forward.core.store"]
print(json.dumps({
    "outcome": outcome,
    "family_unchanged": family() == snapshot,
    "path_unchanged": sys.path == before,
    "store_file": store.__file__,
    "conflict_file": sys.modules[b.ConflictError.__module__].__file__,
    "foreign_kept": b.Store is store.Store,
    "nomination_loaded": "test_nomination_route" in sys.modules,
}))
"""


class NominationBootstrapIdentityTests(unittest.TestCase):
    def _run(self, code: str, *roots: Path, isolated: bool = False) -> dict[str, object]:
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env["PYTHONPATH"] = os.pathsep.join(str(r) for r in roots)
        done = subprocess.run(
            [sys.executable, *(["-S"] if isolated else []), "-c", code],
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
        self.assertTrue(result["family_unchanged"])
        self.assertTrue(result["second_matches_first"])
        self.assertTrue(result["path_unchanged"])
        self.assertFalse(result["nomination_loaded"])

    def test_editable_style_pth_layout_both_orders(self) -> None:
        # An editable install exposes src/ through a .pth file in a site directory; -S keeps
        # the ambient site-packages (possibly another checkout's editable install) out.
        for nomination_first in (False, True):
            with (
                self.subTest(nomination_first=nomination_first),
                tempfile.TemporaryDirectory() as tmp,
            ):
                (Path(tmp) / "zava-editable.pth").write_text(
                    f"{_CORE_SRC}\n{_AGENTS_SRC}\n", encoding="utf-8"
                )
                code = _IDENTITY.format(first="")
                if nomination_first:
                    code = code.replace(
                        "import test_bulk_edits as b\nimport test_nomination_route as n\n",
                        "import test_nomination_route as n\nimport test_bulk_edits as b\n",
                    )
                code = f"import site; site.addsitedir({tmp!r})\n" + code
                self._assert_source_identity(self._run(code, _TESTS, isolated=True))

    def test_editable_dist_info_layout_reports_metadata_and_source_origins(self) -> None:
        probe = (
            "import importlib.metadata as md, json, sys\n"
            "for name in {order}:\n"
            "    __import__(name)\n"
            "n = sys.modules['test_nomination_route']\n"
            "b = sys.modules['test_bulk_edits']\n"
            "print(json.dumps({{\n"
            "    'conflict': n.ConflictError is b.ConflictError,\n"
            "    'gate': n.GateError is sys.modules[n.GateError.__module__].GateError,\n"
            "    'store': n.Store is b.Store,\n"
            "    'patch_target': b.bulk_edits is sys.modules['zava_forward.core.bulk_edits'],\n"
            "    'store_file': sys.modules['zava_forward.core.store'].__file__,\n"
            "    'gate_file': sys.modules[n.GateError.__module__].__file__,\n"
            "    'meta_version': md.version('zava-forward-core'),\n"
            "}}))\n"
        )
        orders = (
            ["test_bulk_edits", "test_nomination_route"],
            ["test_nomination_route", "test_bulk_edits"],
        )
        for order in orders:
            with self.subTest(order=order), tempfile.TemporaryDirectory() as tmp:
                info = Path(tmp) / "zava_forward_core-0.1.0.dist-info"
                info.mkdir()
                (info / "METADATA").write_text(
                    "Metadata-Version: 2.1\nName: zava-forward-core\nVersion: 0.1.0\n",
                    encoding="utf-8",
                )
                (Path(tmp) / "zava-editable.pth").write_text(
                    f"{_CORE_SRC}\n{_AGENTS_SRC}\n", encoding="utf-8"
                )
                code = f"import site; site.addsitedir({tmp!r})\n" + probe.format(order=order)
                result = self._run(code, _TESTS, isolated=True)
                self._assert_source_identity(result)
                self.assertEqual(result["meta_version"], "0.1.0")
                self.assertTrue(Path(str(result["gate_file"])).is_relative_to(_TESTS.parents[1]))

    def _noneditable_copy(self, tmp: str) -> Path:
        shutil.copytree(
            _CORE_SRC / "zava_forward",
            Path(tmp) / "zava_forward",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        return Path(tmp)

    def test_noneditable_copy_layout_both_orders(self) -> None:
        nomination_first = _IDENTITY.format(first="").replace(
            "import test_bulk_edits as b\nimport test_nomination_route as n\n",
            "import test_nomination_route as n\nimport test_bulk_edits as b\n",
        )
        with tempfile.TemporaryDirectory() as tmp:
            site = self._noneditable_copy(tmp)
            roots = (site, _AGENTS_SRC, _TESTS)
            self._assert_source_identity(self._run(nomination_first, *roots))
            result = self._run(_COPY_BULK_FIRST, *roots)
            self.assertNotIn("bulk_rejected", result)
            self.assertTrue(str(result["outcome"]).startswith("rejected: unsupported layout"))
            for key in ("store_file", "conflict_file"):
                self.assertTrue(Path(str(result[key])).is_relative_to(site), key)
            self.assertTrue(result["foreign_kept"])
            self.assertTrue(result["family_unchanged"])
            self.assertTrue(result["path_unchanged"])
            self.assertFalse(result["nomination_loaded"])


if __name__ == "__main__":
    unittest.main()
