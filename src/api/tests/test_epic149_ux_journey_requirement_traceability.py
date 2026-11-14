"""Epic #149: UX artefacts trace to requirements and journeys, and control claims map to tests.

Repository-side completeness check on the Markdown under docs/reference/research/ux/. It shows that
the artefacts resolve to real BRD/PRD requirement IDs, journeys and runnable test modules. It is
not WCAG conformance, assistive-technology acceptance or comprehension evidence, which stay with
named human testers.
"""

import ast
import re
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parents[2]
# Same directories the documented PYTHONPATH exposes for test discovery.
TEST_DIRS = (TESTS, ROOT / "src" / "core" / "tests", ROOT / "src" / "agents" / "tests")
UX = ROOT / "docs" / "reference" / "research" / "ux"
BASELINE = UX / "wcag-conformance-baseline.md"
CONTENT = UX / "content-standard.md"
DESIGN = UX / "design-system.md"
MATRIX_HEADING = "## Journey to requirement to design to test traceability"

SPEC_FILES = (
    ROOT / "docs" / "prds" / "zava-forward-retrofit-programme-demonstrator.md",
    ROOT / "docs" / "prds" / "proper-warm-retrofit-programme-demonstrator.md",
    ROOT / "docs" / "brds" / "agentic-retrofit-programme-brd.md",
)
REQ_ID = re.compile(r"\b(?:FR|NFR|AC|SA|OD)-\d+\b")
JOURNEY = re.compile(r"journey", re.IGNORECASE)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
TEST_MODULE = re.compile(r"\b(test_[a-z0-9_]+)\.py\b")

# Artefacts that carry neither their own requirement ID nor a row in the design-system matrix.
# This list may only shrink: tracing one of them makes the test ask for its removal.
UNTRACED_GAPS = frozenset(
    {
        "briefing-hax-design-note.md",
        "map-tile-provider-options.md",
        "prototype-learnings-and-simplicity-review.md",
        "regulatory-literacy-for-journeys.md",
        "regulatory-ux-acceptance-protocol.md",
        "resident-chat-learning-record.md",
        "supported-devices-proposal.md",
    }
)

# Control family -> modules that must back the claims in the two records.
CONTROLS: dict[str, tuple[Path, tuple[str, ...]]] = {
    "accessibility": (BASELINE, ("test_accessibility_baseline", "test_handoff_waiting_view")),
    "plain-language content": (
        CONTENT,
        ("test_content_standard", "test_hazard_referral", "test_document_controls"),
    ),
}
MANUAL_FALLBACK_MODULE = "test_epic149_manual_fallback_continuity"


def artefacts() -> list[Path]:
    return sorted(UX.rglob("*.md"))


def rel(path: Path) -> str:
    return path.relative_to(UX).as_posix()


def matrix_text() -> str:
    return DESIGN.read_text().split(MATRIX_HEADING, 1)[1].split("\n## ", 1)[0]


def matrix_artefacts() -> set[str]:
    return set(re.findall(r"docs/reference/research/ux/([\w./-]+\.md)", matrix_text()))


def locate(module: str) -> Path:
    for directory in TEST_DIRS:
        if (directory / f"{module}.py").is_file():
            return directory / f"{module}.py"
    return TESTS / f"{module}.py"


def test_names(module: str) -> set[str]:
    tree = ast.parse(locate(module).read_text())
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test")
    }


def assert_runnable(case: unittest.TestCase, module: str) -> None:
    path = locate(module)
    case.assertTrue(path.is_file(), f"{module}.py is missing")
    text = path.read_text()
    compile(text, str(path), "exec")
    case.assertTrue(test_names(module), f"{module} defines no tests")
    case.assertNotRegex(text, r"@unittest\.skip\b", module)
    case.assertNotRegex(text, r"^__test__\s*=\s*False", module)


class RelativeLinks(unittest.TestCase):
    def test_every_relative_markdown_link_resolves(self) -> None:
        self.assertGreaterEqual(len(artefacts()), 25)
        for doc in artefacts():
            for target in LINK.findall(doc.read_text()):
                if re.match(r"[a-z][a-z0-9+.-]*:|#|/", target, re.IGNORECASE):
                    continue
                path = target.split("#", 1)[0]
                if path:
                    with self.subTest(doc=rel(doc), target=target):
                        self.assertTrue((doc.parent / path).exists(), "broken relative link")


class RequirementAndJourneyTraceability(unittest.TestCase):
    def test_cited_requirement_ids_exist_in_the_brd_or_prd(self) -> None:
        corpus = "\n".join(p.read_text() for p in SPEC_FILES)
        for doc in artefacts():
            for req in sorted(set(REQ_ID.findall(doc.read_text()))):
                with self.subTest(doc=rel(doc), requirement=req):
                    self.assertRegex(corpus, rf"\b{req}\b")

    def test_every_artefact_traces_to_a_requirement_and_a_journey(self) -> None:
        in_matrix = matrix_artefacts()
        for doc in artefacts():
            name = rel(doc)
            text = doc.read_text()
            own = bool(REQ_ID.search(text)) and bool(JOURNEY.search(text))
            traced = own or name in in_matrix
            if name in UNTRACED_GAPS:
                with self.subTest(gap=name):
                    self.assertFalse(traced, f"{name} is traced now; remove it from UNTRACED_GAPS")
            else:
                with self.subTest(doc=name):
                    self.assertTrue(traced, f"{name} has no requirement ID and journey")

    def test_known_gaps_name_existing_artefacts(self) -> None:
        names = {rel(doc) for doc in artefacts()}
        self.assertEqual(UNTRACED_GAPS - names, set())

    def test_matrix_rows_cite_ids_and_a_journey_artefact(self) -> None:
        rows = [line for line in matrix_text().splitlines() if line.startswith("| ")][2:]
        self.assertGreaterEqual(len(rows), 10)
        for row in rows:
            cells = [c.strip() for c in row.strip("|").split(" | ")]
            with self.subTest(journey=cells[0]):
                self.assertRegex(cells[1], REQ_ID.pattern)
                self.assertIn("docs/reference/research/ux/", cells[0] + cells[2])
                self.assertIn("pending human", cells[5])


class ControlClaimsMapToTests(unittest.TestCase):
    def test_every_test_module_named_in_the_ux_docs_exists_and_runs(self) -> None:
        for doc in artefacts():
            for module in sorted(set(TEST_MODULE.findall(doc.read_text()))):
                with self.subTest(doc=rel(doc), module=module):
                    assert_runnable(self, module)

    def test_baseline_and_content_standard_claims_cite_their_modules(self) -> None:
        for family, (record, modules) in CONTROLS.items():
            text = record.read_text()
            for module in modules:
                with self.subTest(family=family, module=module):
                    self.assertIn(f"{module}.py", text, "claim no longer cites its test")
                    assert_runnable(self, module)

    def test_baseline_and_content_standard_name_executable_checks(self) -> None:
        for record in (BASELINE, CONTENT):
            text = record.read_text()
            self.assertRegex(text, r"## Automated checks|Automated by `src/api/tests/")

    def test_manual_fallback_usability_controls_have_a_runnable_module(self) -> None:
        assert_runnable(self, MANUAL_FALLBACK_MODULE)
        names = test_names(MANUAL_FALLBACK_MODULE)
        self.assertTrue(any("manual" in n for n in names))
        self.assertTrue(any("ai_unavailable" in n or "degraded" in n for n in names))

    def test_human_gates_are_not_recorded_as_passed_by_these_checks(self) -> None:
        self.assertIn("pending human test", matrix_text())
        self.assertNotIn("conformance achieved", BASELINE.read_text().lower())


if __name__ == "__main__":
    unittest.main()
