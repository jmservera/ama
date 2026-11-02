"""Static conformance of the registered role screens to the UX guardrails (Refs #233).

Source-level checks only: no rendered, assistive-technology or user evidence. They do not
establish WCAG 2.2 conformance (#151) or design-system acceptance (#150).
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web"
SCREENS = (WEB / "role-screens.js").read_text()
CSS = (WEB / "style.css").read_text()
TRACE = (ROOT / "docs" / "reference" / "research" / "ux" / "atlas-screen-trace.md").read_text()


class RoleScreenConformance(unittest.TestCase):
    def test_every_registered_screen_is_traced(self):
        registered = re.findall(r"registerRoleScreen\(\{\s*id: \"([a-z-]+)\"", SCREENS)
        self.assertGreaterEqual(len(registered), 12)
        for ident in registered:
            self.assertIn(f"`{ident}`", TRACE, ident)

    def test_no_role_simulator_in_user_views(self):
        self.assertNotRegex(SCREENS, r"(?i)simulat|impersonat|act as role|switch role")

    def test_every_class_used_is_defined_in_the_design_system(self):
        used = {c for group in re.findall(r'class: "([^"]+)"', SCREENS) for c in group.split()}
        for name in used:
            self.assertRegex(CSS, r"\." + re.escape(name) + r"(?![\w-])", name)

    def test_interactive_controls_are_native_and_keyboard_operable(self):
        self.assertNotIn("innerHTML", SCREENS)
        self.assertNotRegex(SCREENS, r'h\("(?:div|span|li|p|td)", \{[^}]*on(?:click|keydown)')
        for handler in re.finditer(r"onclick:", SCREENS):
            window = SCREENS[max(0, handler.start() - 120) : handler.start()]
            self.assertIn('h("button"', window)
        for region in re.findall(r'role: "region"[^)]*', SCREENS):
            self.assertIn('"aria-label"', region)
            self.assertIn("tabindex: 0", region)

    def test_tables_have_caption_and_column_scope(self):
        self.assertIn('h("caption"', SCREENS)
        self.assertIn('scope: "col"', SCREENS)

    def test_state_is_text_and_not_colour_or_inline_style(self):
        self.assertNotRegex(SCREENS, r'\bstyle: ["`](?!currency)|\.style\.|(?<!\w)color:')
        self.assertIn("Cannot confirm readiness", SCREENS)
        self.assertIn('role: "alert"', SCREENS)
        self.assertIn('role: "status"', SCREENS)

    def test_screen_styles_add_no_motion(self):
        rules = re.findall(r"^\.screen-[^{]*\{[^}]*\}", CSS, re.MULTILINE)
        self.assertTrue(rules)
        for rule in rules:
            self.assertNotRegex(rule, r"animation|transition")
        self.assertNotRegex(SCREENS, r"setTimeout|setInterval|requestAnimationFrame|\.animate\(")

    def test_screens_state_no_action_is_taken(self):
        self.assertIn("No message, approval or record change is made from this screen.", SCREENS)

    def test_withheld_text_rule_is_still_only_proposed(self):
        if "Not shown for this role" not in SCREENS:
            self.assertIn("Proposed rule; conformance of these screens not assessed", TRACE)


if __name__ == "__main__":
    unittest.main()
