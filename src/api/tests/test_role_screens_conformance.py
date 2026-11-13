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


REVOKE_TIMER = "setTimeout(() => URL.revokeObjectURL(started), 1000)"
FOCUS_TIMER = (
    "setTimeout(() => { if (button.isConnected && !button.disabled && "
    "document.activeElement === document.body) button.focus(); }, 0)"
)


def timer_calls(source: str) -> list[tuple[str, str]]:
    """Complete setTimeout calls with the text just before each, using balanced parentheses."""
    calls = []
    for found in re.finditer(r"setTimeout\(", source):
        depth, index = 0, found.end() - 1
        while index < len(source):
            depth += {"(": 1, ")": -1}.get(source[index], 0)
            if depth == 0:
                break
            index += 1
        calls.append(
            (source[max(0, found.start() - 14) : found.start()], source[found.start() : index + 1])
        )
    return calls


def timer_findings(source: str) -> list[str]:
    """Reasons a timer is not the export-URL release or the guarded focus restoration."""
    calls = timer_calls(source)
    found = []
    if len(re.findall(r"\bsetTimeout\b", source)) != len(calls):
        found.append("setTimeout is used other than as a direct call")
    for before, call in calls:
        if call == FOCUS_TIMER:
            if before != "if (hadFocus) ":
                found.append("focus restoration is not limited to a control that had focus")
        elif call != REVOKE_TIMER:
            found.append(f"unexpected timer {call}")
    if sorted(call for _, call in calls) != sorted([FOCUS_TIMER, REVOKE_TIMER]):
        found.append("the timers are not exactly the revoke and focus restoration")
    return found


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
        self.assertNotRegex(SCREENS, r"setInterval|requestAnimationFrame|\.animate\(")
        # Timers: the delayed object-URL release of the exception summary download and the
        # guarded return of focus to the saved-copy check button (accessibility, not motion).
        self.assertEqual(timer_findings(SCREENS), [])

    def test_timer_guard_rejects_motion_and_unguarded_focus_timers(self) -> None:
        focus_body = "button.focus(); }, 0)"
        changed = {
            "motion after focus": SCREENS.replace(
                focus_body, 'button.focus(); button.classList.add("fade"); }, 0)'
            ),
            "long delay": SCREENS.replace(focus_body, "button.focus(); }, 300)"),
            "non-literal delay": SCREENS.replace(focus_body, "button.focus(); }, delay)"),
            "string callback": SCREENS + '\nsetTimeout("fade()", 0);',
            "extra animation timer": SCREENS + '\nsetTimeout(() => el.classList.add("fade"), 300);',
            "alias": SCREENS + "\nconst later = setTimeout;",
            "unguarded focus": SCREENS.replace("if (hadFocus) setTimeout", "setTimeout"),
        }
        for name, source in changed.items():
            self.assertNotEqual(source, SCREENS, name)
            self.assertNotEqual(timer_findings(source), [], name)

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
        self.assertIn(
            "engineering check only; conformance, AT and user validation not assessed", TRACE
        )

    def test_withheld_disclosure_is_on_evidence_screens(self) -> None:
        for ident in ("technical-queue", "quality-queue"):
            start = SCREENS.index(f'id: "{ident}"')
            end = SCREENS.index("registerRoleScreen({", start)
            block = SCREENS[start:end]
            self.assertIn("screenWithheld([", block, ident)
            self.assertIn("Funding amounts and claim values", block, ident)

    def test_utilisation_versus_choice_is_stated_on_package_screen(self) -> None:
        start = SCREENS.index('id: "procurement-packages"')
        block = SCREENS[start : SCREENS.index("registerRoleScreen({", start)]
        self.assertIn('screenPanel("Offered capacity and resident choice"', block)
        self.assertIn("not a booking and not a promise", block)
        self.assertIn("never ranked by utilisation or headroom", block)
        self.assertIn(".sort((x, y) => String(x.id).localeCompare(String(y.id)))", block)


if __name__ == "__main__":
    unittest.main()
