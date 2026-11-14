"""UX traceability matrix (#149): each journey row resolves to real files, tests and requirements.

Source-level checks only. They record that the references exist and that human evidence stays
pending; they are not accessibility conformance, assistive-technology or usability results.
"""

import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web"
SERVER = (ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "server.py").read_text()
SCREENS = (WEB / "role-screens.js").read_text()
PANELS = (WEB / "panels.js").read_text()
DOC = (ROOT / "docs" / "reference" / "research" / "ux" / "design-system.md").read_text()
PRD = (ROOT / "docs" / "prds" / "zava-forward-retrofit-programme-demonstrator.md").read_text()
BRD = (ROOT / "docs" / "brds" / "agentic-retrofit-programme-brd.md").read_text()
HEADING = "## Journey to requirement to design to test traceability"
COLUMNS = 6


def matrix_rows() -> list[list[str]]:
    section = DOC.split(HEADING, 1)[1].split("\n## ", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| ")]
    return [[c.strip() for c in line.strip("|").split(" | ")] for line in rows[2:]]


def tokens(cell: str) -> list[str]:
    return re.findall(r"`([^`]+)`", cell)


class UxDesignTraceability(unittest.TestCase):
    def test_matrix_rows_are_complete(self) -> None:
        rows = matrix_rows()
        self.assertGreaterEqual(len(rows), 10)
        for row in rows:
            self.assertEqual(len(row), COLUMNS, row[0])
            for cell in row[1:5]:
                self.assertTrue(tokens(cell), (row[0], cell))

    def test_referenced_files_exist(self) -> None:
        for row in matrix_rows():
            for token in tokens(row[0]) + tokens(row[2]) + tokens(row[4]):
                if token.startswith(("docs/", "src/")):
                    self.assertTrue((ROOT / token.split("::")[0]).is_file(), token)

    def test_web_surfaces_exist(self) -> None:
        for row in matrix_rows():
            for token in tokens(row[3]):
                kind, _, name = token.partition(":")
                if kind == "screen":
                    self.assertIn(f'id: "{name}"', SCREENS, token)
                elif kind == "panel":
                    self.assertIn(f"function {name}(", PANELS, token)
                elif kind == "route":
                    self.assertIn(f'"{name}"', SERVER, token)
                elif kind == "web":
                    self.assertTrue((WEB / name).is_file(), token)
                else:
                    self.fail(f"Unknown surface kind: {token}")

    def test_every_registered_role_screen_is_in_the_matrix(self) -> None:
        registered = set(re.findall(r'^registerRoleScreen\(\{\n  id: "([\w-]+)"', SCREENS, re.M))
        self.assertGreaterEqual(len(registered), 13)
        traced = {
            t.split(":", 1)[1]
            for r in matrix_rows()
            for t in tokens(r[3])
            if t.startswith("screen:")
        }
        self.assertEqual(registered - traced, set())

    def test_automated_tests_exist(self) -> None:
        for row in matrix_rows():
            for token in tokens(row[4]):
                path, _, target = token.partition("::")
                tree = ast.parse((ROOT / path).read_text())
                if not target:
                    continue
                klass, method = target.split("::")
                node = next(
                    (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == klass), None
                )
                self.assertIsNotNone(node, token)
                assert node is not None
                names = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
                self.assertIn(method, names, token)

    def test_requirement_ids_exist_in_prd_or_brd(self) -> None:
        for row in matrix_rows():
            for token in tokens(row[1]):
                source, _, rid = token.rpartition(":")
                if source == "BRD":
                    self.assertIn(f"| {rid} |", BRD, token)
                else:
                    self.assertRegex(PRD, rf"\b{re.escape(rid)}\b", token)

    def test_human_evidence_is_never_asserted(self) -> None:
        for row in matrix_rows():
            self.assertTrue(row[5].startswith("pending human test"), row[0])
        section = DOC.split(HEADING, 1)[1].split("\n## ", 1)[0].lower()
        self.assertIn("no acceptance criterion is ticked", section)
        self.assertNotRegex(
            section, r"conforms to wcag|wcag.{0,20}(passed|conformant)|users? (passed|validated)"
        )


if __name__ == "__main__":
    unittest.main()
