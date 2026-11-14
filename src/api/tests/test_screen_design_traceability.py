"""Screen to journey, task flow and design artefact matrix (#156).

Source-level checks only: references exist and no human acceptance is asserted.
"""

import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
UX = ROOT / "docs" / "reference" / "research" / "ux"
DOC = (UX / "screen-design-traceability.md").read_text()
SCREENS = (ROOT / "src/api/src/zava_forward/api/web/role-screens.js").read_text()
ISSUES = {225, 226, 227, 228, 229, 230, 231, 232, 233, 159, 215}
LINK = re.compile(r"\]\((\./[^)#]+\.md)(?:#([^)]+))?\)")


def slug(heading: str) -> str:
    text = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return re.sub(r"\s", "-", text)


def anchors(path: Path) -> set[str]:
    return {slug(m.group(1)) for m in re.finditer(r"^#{1,6} (.+)$", path.read_text(), re.M)}


def rows() -> list[list[str]]:
    section = DOC.split("## Screen matrix", 1)[1].split("\n## ", 1)[0]
    lines = [x for x in section.splitlines() if x.startswith("| ")][2:]
    return [[c.strip() for c in x.strip("|").split(" | ")] for x in lines]


class ScreenDesignTraceability(unittest.TestCase):
    def test_rows_are_complete_and_cover_every_issue(self) -> None:
        seen = set()
        for row in rows():
            self.assertEqual(len(row), 7, row[0])
            self.assertTrue(all(row), row)
            match = re.search(r"#(\d+)\]", row[0])
            self.assertIsNotNone(match, row[0])
            assert match is not None
            seen.add(int(match.group(1)))
        self.assertEqual(ISSUES - seen, set())

    def test_every_registered_role_screen_has_a_row(self) -> None:
        registered = set(re.findall(r'^registerRoleScreen\(\{\n  id: "([\w-]+)"', SCREENS, re.M))
        traced = {t for r in rows() for t in re.findall(r"`([\w-]+)`", r[1])}
        self.assertGreaterEqual(len(registered), 13)
        self.assertEqual(registered - traced, set())

    def test_links_and_anchors_resolve(self) -> None:
        for row in rows():
            for cell in row[2:5]:
                for rel, anchor in LINK.findall(cell):
                    target = (UX / rel).resolve()
                    self.assertTrue(target.is_file(), rel)
                    if anchor:
                        self.assertIn(anchor, anchors(target), (rel, anchor))
                self.assertTrue(
                    LINK.search(cell) or "No written" in cell or "No wireframe" in cell,
                    cell,
                )

    def test_tests_exist(self) -> None:
        for row in rows():
            parts = row[5].strip("`").split("::")
            self.assertEqual(len(parts), 3, f"{row[5]} must be path::Class::method")
            path, klass, method = parts
            self.assertTrue((ROOT / path).is_file(), path)
            tree = ast.parse((ROOT / path).read_text())
            target_cls = next(
                (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == klass),
                None,
            )
            self.assertIsNotNone(target_cls, f"{klass} not found in {path}")
            assert target_cls is not None
            self.assertIn(
                method, {n.name for n in target_cls.body if isinstance(n, ast.FunctionDef)}
            )

    def test_no_human_acceptance_is_claimed(self) -> None:
        self.assertIn("ticks no acceptance criterion", DOC)
        self.assertNotRegex(
            DOC.lower(), r"conforms to wcag|users? (passed|validated)|design (is )?accepted"
        )


if __name__ == "__main__":
    unittest.main()
