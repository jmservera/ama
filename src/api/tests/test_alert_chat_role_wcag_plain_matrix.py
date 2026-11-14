"""#215 criterion 3 matrix: seven role groups, non-colour cues, plain-language mode, live regions.

Static source checks only. Not screen reader, assistive technology, staff comprehension or
manual acceptance evidence, and no WCAG conformance claim.
"""

import re
import unittest
from pathlib import Path

from zava_forward.core.projection import STAFF_ROLES

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()
CSS = (WEB / "style.css").read_text()
BANNED = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)

# The seven #215 role groups. Data handlers and suppliers have no staff role of their own.
ROLE_GROUPS = {
    "repairs and intake": ("Resident Liaison Officer", "Repairs and intake:"),
    "Building Safety": ("Building Safety Liaison", "Building Safety:"),
    "assessor": ("Quality Inspector", "Assessment and quality:"),
    "coordinator": ("Retrofit Coordinator", "Assessment and coordination:"),
    "programme": ("Retrofit Programme Manager", "Programme:"),
    "finance and grants": ("Grants and Evidence Officer", "Finance and grants:"),
}


def role_help() -> dict[str, str]:
    block = CHAT[CHAT.index("const regulatoryRoleHelp") : CHAT.index("function regulatoryGuidance")]
    return dict(re.findall(r'"([^"]+)": "([^"]+)"', block))


def guidance_body() -> str:
    start = CHAT.index("function regulatoryGuidance")
    return CHAT[start : CHAT.index("function regulatoryPlainMode")]


class RoleCoverageTests(unittest.TestCase):
    def test_every_staff_role_has_its_own_plain_guidance_line(self) -> None:
        helps = role_help()
        self.assertEqual(set(STAFF_ROLES), set(helps))
        for role in STAFF_ROLES:
            with self.subTest(role=role):
                self.assertIn(role, helps)
                self.assertTrue(helps[role].strip())

    def test_each_role_group_opens_with_its_visible_label_and_a_stated_limit(self) -> None:
        helps = role_help()
        for group, (role, label) in ROLE_GROUPS.items():
            with self.subTest(group=group):
                self.assertTrue(helps[role].startswith(label))
                self.assertRegex(helps[role], r"(?i)\b(?:not|no|only|unverified|do not)\b")

    def test_role_copy_is_plain_ascii_without_internal_terms(self) -> None:
        for role, text in role_help().items():
            with self.subTest(role=role):
                self.assertIsNone(BANNED.search(text))
                self.assertTrue(text.isascii())
                self.assertNotIn("\u2014", text)

    def test_data_handlers_and_suppliers_get_shared_guidance_that_grants_nothing(self) -> None:
        body = guidance_body()
        self.assertIn("For everyone handling data:", body)
        self.assertIn("ask the DPO owner if unsure", body)
        # Suppliers are not staff roles, so they reach the fallback line.
        self.assertNotIn("Contractor", " ".join(STAFF_ROLES))
        self.assertIn("regulatoryRoleHelp[role] || ", body)
        self.assertIn("This guidance grants no additional permissions.", body)
        self.assertIsNone(BANNED.search(body))
        self.assertTrue(body.isascii())

    def test_alerts_panel_passes_the_signed_in_role_to_the_guidance(self) -> None:
        self.assertIn("regulatoryGuidance(me.user.role)", CHAT)


class NonColourSignalTests(unittest.TestCase):
    states = (
        "breach-risk",
        "attention",
        "unknown",
        "clear",
        "not-applicable",
        "answer",
        "refused",
        "conflict",
        "no-source",
        "sent",
    )

    def test_every_state_pairs_a_distinct_glyph_with_a_border_shape(self) -> None:
        glyphs = dict(re.findall(r"\.state-([\w-]+):before\{content:\"([^\"]+)\"", CSS))
        for state in self.states:
            self.assertIn(state, glyphs)
        outcome_glyphs = [
            glyphs[s] for s in ("breach-risk", "attention", "unknown", "clear", "not-applicable")
        ]
        self.assertEqual(len(set(outcome_glyphs)), len(outcome_glyphs))
        self.assertRegex(CSS, r"\.regulatory-state\{border-left:4px solid currentColor")
        self.assertRegex(CSS, r"\.state-no-source\{border-left-style:dotted\}")

    def test_glyphs_are_decorative_with_an_empty_alternative(self) -> None:
        contents = re.findall(r"\.state-[\w-]+:before\{content:\"[^\"]+\"( / \"\")?", CSS)
        self.assertGreaterEqual(len(contents), len(self.states))
        self.assertTrue(all(contents))

    def test_alert_and_lookup_headings_carry_a_visible_text_label(self) -> None:
        self.assertIn("`Status: ${alert.result}`", CHAT)
        self.assertIn("`Lookup status: ${answer.kind}`", CHAT)
        self.assertIn("No source held for this answer.", CHAT)

    def test_unknown_values_fall_back_to_the_unknown_cue_not_to_no_cue(self) -> None:
        self.assertIn('regulatoryStates.has(value) ? value.replace(" ", "-") : "unknown"', CHAT)

    def test_loading_and_failure_status_keep_the_unknown_cue_with_a_next_step(self) -> None:
        self.assertIn('status.className = "regulatory-state state-unknown"', CHAT)
        self.assertIn("Next action: reload to check again.", CHAT)
        self.assertIn("Use the existing human emergency or hazard service", CHAT)


class PlainLanguageToggleTests(unittest.TestCase):
    def test_toggle_is_a_native_labelled_checkbox_on_by_default(self) -> None:
        body = CHAT[
            CHAT.index("function regulatoryPlainMode") : CHAT.index("const regulatoryStates")
        ]
        self.assertIn('h("input", { type: "checkbox", id, checked: true })', body)
        self.assertIn('h("label", { class: "regulatory-mode", for: id }', body)
        self.assertIn("Plain-language explanations", body)
        self.assertIn('root.classList.toggle("plain-language", input.checked)', body)
        self.assertNotIn("onclick", body)

    def test_alerts_and_lookup_each_get_a_distinct_toggle_id(self) -> None:
        self.assertIn('regulatoryPlainMode(root, "alerts-plain-mode")', CHAT)
        self.assertIn('regulatoryPlainMode(root, "chat-plain-mode")', CHAT)

    def test_css_hides_plain_copy_only_when_the_mode_is_off(self) -> None:
        self.assertIn(".regulatory .plain-explanation{display:none}", CSS)
        self.assertIn(".regulatory.plain-language .plain-explanation{display:block}", CSS)
        self.assertRegex(
            CSS, r"\.regulatory\.plain-language li\.plain-explanation\{display:list-item\}"
        )

    def test_plain_copy_has_no_internal_terms_or_non_ascii(self) -> None:
        copy = re.findall(r'"(In plain words:[^"]*)"', CHAT)
        self.assertGreaterEqual(len(copy), 5)
        for text in copy:
            with self.subTest(text=text[:40]):
                self.assertIsNone(BANNED.search(text))
                self.assertTrue(text.isascii())

    def test_every_alert_outcome_has_a_plain_meaning_in_ascii(self) -> None:
        block = CHAT[CHAT.index("const meanings") : CHAT.index("const refresh = h(")]
        for state in ("breach risk", "attention", "unknown", "clear", "not applicable"):
            with self.subTest(state=state):
                self.assertRegex(block, rf'(?m)^\s+(?:"{state}"|{state}): "[^"]+\.",?$')
        self.assertTrue(block.isascii())
        self.assertIsNone(BANNED.search(block))


class DoubtAndNoSourceTests(unittest.TestCase):
    def test_no_source_state_is_text_glyph_and_dotted_border_with_a_plain_next_step(self) -> None:
        self.assertIn('class: "regulatory-state state-no-source"', CHAT)
        self.assertIn("Do not infer a duty or terms; ask the named human owner.", CHAT)
        self.assertIn("In plain words: the lookup found nothing it can show.", CHAT)

    def test_doubt_button_stays_focusable_and_changes_its_text_when_sent(self) -> None:
        self.assertEqual(CHAT.count('doubt.setAttribute("aria-disabled", "true")'), 2)
        self.assertNotIn("doubt.disabled", CHAT)
        self.assertEqual(
            CHAT.count('doubt.textContent = "Sent to exercise owner; awaiting human review"'), 2
        )
        self.assertEqual(CHAT.count('doubt.classList.add("regulatory-state", "state-sent")'), 2)
        self.assertIn('doubt.removeAttribute("aria-disabled")', CHAT)

    def test_doubt_outcomes_are_announced_through_a_status_region_with_a_next_step(self) -> None:
        self.assertIn('const status = h("p", { role: "status" });', CHAT)
        self.assertIn("No legal approval or resident message.", CHAT)
        self.assertIn("Doubt route failed:", CHAT)
        self.assertIn("Next action: try again, or ask Juan Manuel Servera directly.", CHAT)

    def test_doubt_label_names_the_human_owner(self) -> None:
        self.assertIn('"In doubt: send this turn to Juan Manuel Servera"', CHAT)


class LiveRegionRoleTests(unittest.TestCase):
    def test_no_chat_script_region_combines_role_alert_with_polite_in_chat_js(self) -> None:
        self.assertNotRegex(CHAT, r'role: "alert"[^}]*aria-live')
        self.assertNotRegex(CHAT, r'aria-live[^}]*role: "alert"')

    def test_chat_js_routine_updates_use_role_status_or_a_polite_log(self) -> None:
        self.assertGreaterEqual(CHAT.count('role: "status"'), 3)
        self.assertIn('role: "log", "aria-live": "polite"', CHAT)
        self.assertEqual(CHAT.count('"aria-live": "assertive"'), 0)

    def test_widget_routine_status_is_role_status_with_polite(self) -> None:
        status = re.search(r"const status = node\((.*)\);", WIDGET)
        self.assertIsNotNone(status)
        attrs = status.group(1) if status else ""
        self.assertIn('role: "status"', attrs)
        self.assertIn('"aria-live": "polite"', attrs)
        self.assertNotIn("alert", attrs)

    def test_widget_log_is_polite_and_keyboard_reachable(self) -> None:
        log = re.search(r"const log = node\((.*)\);", WIDGET)
        attrs = log.group(1) if log else ""
        self.assertIn('role: "log"', attrs)
        self.assertIn('"aria-live": "polite"', attrs)
        self.assertIn('tabindex: "0"', attrs)

    def test_widget_alert_role_is_reserved_for_the_one_hidden_until_needed_error(self) -> None:
        self.assertEqual(WIDGET.count('role: "alert"'), 1)
        self.assertIn("error.hidden = true;", WIDGET)
        self.assertIn(
            'error.textContent = text; error.hidden = false; status.textContent = "";', WIDGET
        )
        self.assertIn('error.textContent = ""; error.hidden = true;', WIDGET)

    def test_widget_error_keeps_its_polite_pairing_pinned_by_existing_browser_checks(self) -> None:
        # Decision 2026-11-14: left unchanged. test_chat_widget_focus.py asserts aria-live="polite"
        # on the error and test_chat_panel.py locates it by role alert, so splitting the pair
        # would break those checks. Routed as a follow-up in the review artifact.
        error = re.search(r"const error = node\((.*)\);", WIDGET)
        attrs = error.group(1) if error else ""
        self.assertIn('role: "alert"', attrs)
        self.assertIn('"aria-live": "polite"', attrs)
        self.assertIn('tabindex: "-1"', attrs)


if __name__ == "__main__":
    unittest.main()
