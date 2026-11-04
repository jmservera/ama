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
    def test_every_registered_screen_is_traced(self) -> None:
        registered = re.findall(r"registerRoleScreen\(\{\s*id: \"([a-z-]+)\"", SCREENS)
        self.assertGreaterEqual(len(registered), 12)
        for ident in registered:
            self.assertIn(f"`{ident}`", TRACE, ident)

    def test_no_role_simulator_in_user_views(self) -> None:
        self.assertNotRegex(SCREENS, r"(?i)simulat|impersonat|act as role|switch role")

    def test_every_class_used_is_defined_in_the_design_system(self) -> None:
        used = {c for group in re.findall(r'class: "([^"]+)"', SCREENS) for c in group.split()}
        for name in used:
            self.assertRegex(CSS, r"\." + re.escape(name) + r"(?![\w-])", name)

    def test_interactive_controls_are_native_and_keyboard_operable(self) -> None:
        self.assertNotIn("innerHTML", SCREENS)
        self.assertNotRegex(SCREENS, r'h\("(?:div|span|li|p|td)", \{[^}]*on(?:click|keydown)')
        for handler in re.finditer(r"onclick:", SCREENS):
            window = SCREENS[max(0, handler.start() - 120) : handler.start()]
            self.assertIn('h("button"', window)
        for region in re.findall(r'role: "region"[^)]*', SCREENS):
            self.assertIn('"aria-label"', region)
            self.assertIn("tabindex: 0", region)

    def test_tables_have_caption_and_column_scope(self) -> None:
        self.assertIn('h("caption"', SCREENS)
        self.assertIn('scope: "col"', SCREENS)

    def test_state_is_text_and_not_colour_or_inline_style(self) -> None:
        self.assertNotRegex(SCREENS, r'\bstyle: ["`](?!currency)|\.style\.|(?<!\w)color:')
        self.assertIn("Cannot confirm readiness", SCREENS)
        self.assertIn('role: "alert"', SCREENS)
        self.assertIn('role: "status"', SCREENS)

    def test_screen_styles_add_no_motion(self) -> None:
        rules = re.findall(r"^\.screen-[^{]*\{[^}]*\}", CSS, re.MULTILINE)
        self.assertTrue(rules)
        for rule in rules:
            self.assertNotRegex(rule, r"animation|transition")
        self.assertNotRegex(SCREENS, r"setTimeout|setInterval|requestAnimationFrame|\.animate\(")

    def test_screens_state_no_action_is_taken(self) -> None:
        self.assertIn("No message, approval or record change is made from this screen.", SCREENS)

    def test_withheld_disclosure_is_on_both_tension_screens(self) -> None:
        for ident in ("programme-queue", "resident-choice"):
            start = SCREENS.index(f'id: "{ident}"')
            end = SCREENS.index("registerRoleScreen({", start)
            self.assertIn("screenWithheld(", SCREENS[start:end], ident)
        start = SCREENS.index('id: "programme-queue"')
        overview = SCREENS[start : SCREENS.index("async load(c)", start)]
        self.assertIn("screenWithheld(", overview)
        start = SCREENS.index('id: "resident-choice"')
        summary = SCREENS[start : SCREENS.index("render(c) {", start)]
        self.assertIn("screenWithheld(", summary)
        self.assertIn('screenPanel("Not shown for this role"', SCREENS)
        self.assertIn("is not authorisation", SCREENS)
        self.assertIn("Proposed rule; rendered behaviour and conformance not assessed", TRACE)

    def test_utilisation_versus_choice_is_stated_on_package_screen(self) -> None:
        start = SCREENS.index('id: "procurement-packages"')
        block = SCREENS[start : SCREENS.index("registerRoleScreen({", start)]
        self.assertIn('screenPanel("Offered capacity and resident choice"', block)
        self.assertIn("not a booking and not a promise", block)
        self.assertIn("never ranked by utilisation or headroom", block)
        self.assertIn(".sort((x, y) => String(x.id).localeCompare(String(y.id)))", block)

    def test_choice_screen_states_precedence_over_offered_capacity(self) -> None:
        start = SCREENS.index('id: "resident-choice"')
        block = SCREENS[start : SCREENS.index("registerRoleScreen({", start)]
        render = block[block.index("render(c) {") :]
        panel = render.index('screenPanel("Choice comes before offered capacity"')
        self.assertLess(render.index('screenPanel("Choice for each measure"'), panel)
        self.assertLess(render.index('screenPanel("Paused or withdrawn by the resident"'), panel)
        self.assertIn("takes precedence over any offered contractor slot", render)
        self.assertIn("not a booking and not a promise to the resident", render)
        self.assertNotIn("headroom", render)
        self.assertNotIn("utilisation", render)


if __name__ == "__main__":
    unittest.main()
