"""Focused offline tests for tools/check-design-trace.py (Refs #156)."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).with_name("check-design-trace.py")
spec = importlib.util.spec_from_file_location("check_design_trace", TOOL)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ISSUE = "https://github.com/jmservera/ama/issues/%d"


def doc(rows: list[str]) -> str:
    return (
        "## S\n\n"
        + mod.HEADING
        + "\n\n| h | h | h | h | h |\n| - | - | - | - | - |\n"
        + "\n".join(rows)
        + "\n\n### Next\n\n[j]: ./a.md#x\n"
    )


def row(n: int, journey: str = "[J][j]", design: str = "NOT SUPPLIED") -> str:
    return f"| [#{n}]({ISSUE % n}#acceptance-criteria) O: x | {journey} | flow | {design} | role |"


class CheckTests(unittest.TestCase):
    def run_check(self, text: str) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "a.md").write_text("x", encoding="utf-8")
            return mod.check(text, Path(tmp))

    def test_blocked_when_design_not_supplied(self) -> None:
        report = self.run_check(doc([row(1), row(2, design="v1 design")]))
        self.assertEqual(report["verdict"], "blocked")
        self.assertEqual(report["not_supplied_issues"], [1])
        self.assertEqual(report["design_supplied"], 1)

    def test_pass_when_all_supplied(self) -> None:
        report = self.run_check(doc([row(1, design="v1 design")]))
        self.assertEqual(report["verdict"], "pass")

    def test_undefined_reference_is_malformed(self) -> None:
        report = self.run_check(doc([row(1, journey="[J][nope]")]))
        self.assertEqual(report["verdict"], "malformed")

    def test_missing_file_link_is_malformed(self) -> None:
        report = self.run_check(doc([row(1, journey="[J](./gone.md#a)")]))
        self.assertEqual(report["verdict"], "malformed")

    def test_journey_without_link_or_gap_is_malformed(self) -> None:
        report = self.run_check(doc([row(1, journey="plain text")]))
        self.assertEqual(report["verdict"], "malformed")

    def test_duplicate_and_empty_register(self) -> None:
        self.assertEqual(self.run_check(doc([row(1), row(1)]))["verdict"], "malformed")
        self.assertEqual(self.run_check("nothing")["verdict"], "malformed")

    def test_real_register_is_wellformed_and_blocked(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = mod.main(["--json"])
        report = json.loads(out.getvalue())
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["screen_issues"], 74)
        self.assertEqual(code, 1)
        self.assertEqual(report["verdict"], "blocked")


if __name__ == "__main__":
    unittest.main()
