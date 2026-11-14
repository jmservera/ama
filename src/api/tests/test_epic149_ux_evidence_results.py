"""Epic #149 criterion 3: every UX surface maps to executable tests, and human gates stay pending.

This module verifies that the accessibility, content and usability claims of the epic are backed by
existing test modules rather than prose. Automated results are engineering evidence on constructed
data. They are not WCAG conformance, assistive-technology acceptance (#155) or staff comprehension
evidence (#215 criterion 5), which stay with named human testers.
"""

import ast
import re
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parents[2]
UX = ROOT / "docs" / "reference" / "research" / "ux"

# Surface -> {test module: test names that must exist in it}.
SURFACES: dict[str, dict[str, tuple[str, ...]]] = {
    "Fluent 2 design tokens and components": {
        "test_design_system": (
            "test_tokens_defined_and_used",
            "test_every_defined_token_is_documented",
            "test_fluent_foundation_mapping_and_consumption",
            "test_status_signals_have_non_colour_cue",
        ),
    },
    "WCAG 2.2 AA static and structural guards": {
        "test_accessibility_baseline": (
            "test_pages_declare_language_and_allow_zoom",
            "test_text_contrast_meets_aa",
            "test_non_text_contrast_meets_aa",
            "test_focus_indicator_is_two_tone_and_never_removed",
            "test_audit_record_names_target_gaps_and_makes_no_conformance_claim",
        ),
        "test_role_screens_conformance": (
            "test_interactive_controls_are_native_and_keyboard_operable",
            "test_tables_have_caption_and_column_scope",
        ),
        "test_chat_widget_focus": (),
    },
    "Plain-language content standard": {
        "test_content_standard": (
            "test_no_internal_terms_in_web_copy",
            "test_every_served_script_and_page_is_audited",
            "test_ai_label_is_exact_and_never_implies_approval",
            "test_blocked_reasons_have_reason_owner_and_next_action",
        ),
    },
    "Safety screens": {"test_safety_screens": (), "test_safety_panel_ux": ()},
    "Procurement screens": {"test_procurement_screens": ()},
    "Resident screens": {"test_resident_choice_screen": ()},
    "Regulatory chat and regulatory UX": {
        "test_regulatory_chat_api": (),
        "test_regulatory_ux_check": (),
    },
}

HUMAN_GATE_RECORD = UX / "production-ux-acceptance-protocol.md"
BASELINE = UX / "wcag-conformance-baseline.md"


def test_names(module: str) -> set[str]:
    tree = ast.parse((TESTS / f"{module}.py").read_text())
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test")
    }


class SurfaceCoverage(unittest.TestCase):
    def test_every_surface_names_executable_tests(self) -> None:
        for surface, modules in SURFACES.items():
            with self.subTest(surface=surface):
                self.assertTrue(modules, surface)
                for module, required in modules.items():
                    path = TESTS / f"{module}.py"
                    self.assertTrue(path.is_file(), f"{surface}: {path.name} is missing")
                    names = test_names(module)
                    self.assertTrue(names, f"{surface}: {module} defines no tests")
                    missing = [name for name in required if name not in names]
                    self.assertEqual(missing, [], f"{surface}: {module} lost pinned tests")

    def test_modules_are_found_by_unittest_discovery(self) -> None:
        for modules in SURFACES.values():
            for module in modules:
                self.assertRegex(f"{module}.py", r"^test.*\.py$")

    def test_no_surface_module_is_disabled(self) -> None:
        for modules in SURFACES.values():
            for module in modules:
                text = (TESTS / f"{module}.py").read_text()
                self.assertNotRegex(text, r"@unittest\.skip\b|skipTest\(", module)
                self.assertNotRegex(text, r"^__test__\s*=\s*False", module)


class RenderedChecksAreOptIn(unittest.TestCase):
    def test_rendered_axe_and_keyboard_checks_exist_but_are_not_counted_here(self) -> None:
        for name in ("design_system_browser_check", "case_view_ux_browser_check"):
            self.assertTrue((TESTS.parent / "checks" / f"{name}.py").is_file(), name)
        self.assertTrue((TESTS / "test_specialist_keyboard_check.py").is_file())


class HumanGatesStayPending(unittest.TestCase):
    def test_assistive_technology_record_has_no_fabricated_result(self) -> None:
        text = HUMAN_GATE_RECORD.read_text()
        record = text.split("## Record", 1)[1].split("## Closing issue", 1)[0]
        rows = [line for line in record.splitlines() if line.startswith("|")]
        data = [row for row in rows if not re.match(r"\|\s*(-+|Surface|Journey)\s*\|", row)]
        self.assertGreaterEqual(len(data), 4)
        for row in data:
            for cell in row.strip("|").split("|")[1:]:
                if cell.strip() != "Not run":
                    self.assertRegex(cell, r"\d{4}-\d{2}-\d{2}", row)
                    self.assertIn("tester", cell.lower(), row)

    def test_baseline_says_automated_checks_are_not_conformance_or_human_acceptance(self) -> None:
        text = " ".join(BASELINE.read_text().split())
        self.assertIn("Automated checks are not conformance evidence", text)
        self.assertIn("not WCAG 2.2 conformance, assistive-technology acceptance", text)
        self.assertIn("#155", text)

    def test_epic_status_keeps_human_validation_as_unmet(self) -> None:
        text = " ".join(BASELINE.read_text().split())
        self.assertIn("manual screen-reader and keyboard checks", text)
        self.assertIn("Synthetic walkthroughs are not user validation", text)


if __name__ == "__main__":
    unittest.main()
