"""#215: keyboard, focus return, live regions, provenance and outcome cues for alerts and chat.

Static source checks only, not screen reader, assistive technology or staff comprehension evidence.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()


def function_body(source: str, signature: str) -> str:
    start = source.index(signature)
    return source[start : source.index("\n    }\n", start)]


class NativeControlTests(unittest.TestCase):
    def test_no_script_builds_a_fake_button_or_clickable_non_control(self) -> None:
        for name, source in (("chat.js", CHAT), ("chat-widget.js", WIDGET)):
            with self.subTest(script=name):
                self.assertNotRegex(source, r'role: ?"button"|role="button"')
                self.assertNotRegex(source, r'h\("(?:div|span|p|li)", \{[^}]*onclick')
                self.assertNotIn("tabindex: -1", source.replace('"tabindex": "-1"', ""))

    def test_every_alert_and_lookup_button_has_an_explicit_type(self) -> None:
        buttons = re.findall(r'h\("button", \{([^}]*)\}', CHAT)
        self.assertGreaterEqual(len(buttons), 3)
        for attributes in buttons:
            self.assertRegex(attributes, r'type: "(?:button|submit)"')

    def test_source_links_are_native_anchors_that_name_the_new_tab(self) -> None:
        self.assertEqual(len(re.findall(r'h\("a", \{ href: [^}]*rel: "noopener"', CHAT)), 2)
        self.assertIn("(source record, opens new tab)", CHAT)

    def test_alert_refresh_returns_focus_after_the_reload_disables_it(self) -> None:
        self.assertIn('h("button", { type: "button", class: "alt", onclick: load }', CHAT)
        self.assertIn("if (held && !moved && document.activeElement === document.body)", CHAT)
        self.assertIn("refresh.focus()", CHAT)


class WidgetKeyboardTests(unittest.TestCase):
    def test_launcher_exposes_expanded_controls_and_dialog_state(self) -> None:
        self.assertIn('launcher.setAttribute("aria-controls", id)', WIDGET)
        self.assertIn('launcher.setAttribute("aria-haspopup", "dialog")', WIDGET)
        self.assertIn('launcher.setAttribute("aria-expanded", "true")', WIDGET)
        self.assertEqual(WIDGET.count('launcher.setAttribute("aria-expanded", "false")'), 3)
        self.assertIn('role: "dialog", "aria-labelledby": `${id}-title`', WIDGET)

    def test_escape_and_close_share_the_focus_returning_hide(self) -> None:
        self.assertIn("close.onclick = () => hide();", WIDGET)
        self.assertRegex(
            WIDGET,
            r'event\.key === "Escape"\) \{ event\.preventDefault\(\); hide\(\); \}',
        )
        hide = WIDGET[WIDGET.index("function hide(") : WIDGET.index("function open()")]
        self.assertIn("root.hidden = true", hide)
        # A docked panel hides the launcher; it must be shown before it can take focus.
        self.assertLess(hide.index("launcher.hidden = false"), hide.index("launcher.focus()"))
        self.assertIn("if (returnFocus && active) launcher.focus()", hide)

    def test_toggle_opens_to_the_heading_and_outside_focus_does_not_steal_it(self) -> None:
        self.assertIn("launcher.onclick = () => root.hidden ? open() : hide();", WIDGET)
        self.assertIn("heading.focus()", WIDGET)
        self.assertIn("if (!stayOpen) hide(false);", WIDGET)

    def test_input_and_send_are_native_and_enter_submits_without_trapping_shift(self) -> None:
        self.assertIn('node("textarea", "", {', WIDGET)
        self.assertIn('node("button", "Send", { type: "submit" })', WIDGET)
        self.assertIn('event.key === "Enter" && !event.shiftKey && !event.isComposing', WIDGET)
        self.assertIn("form.requestSubmit()", WIDGET)
        self.assertIn('"aria-label": questionLabel', WIDGET)

    def test_unsupported_tools_are_disabled_with_a_visible_reason(self) -> None:
        self.assertEqual(WIDGET.count('"aria-describedby": reason.id'), 2)
        self.assertIn("Attachments and voice input are not supported in this chat", WIDGET)

    def test_log_status_and_error_are_live_regions_and_the_log_is_keyboard_reachable(self) -> None:
        self.assertIn('role: "log", "aria-live": "polite"', WIDGET)
        self.assertIn('tabindex: "0" });\n    const form', WIDGET)
        self.assertIn('role: "status", "aria-live": "polite", "aria-atomic": "true"', WIDGET)
        self.assertIn('role: "alert", "aria-live": "polite", "aria-atomic": "true"', WIDGET)

    def test_busy_state_keeps_focus_on_the_input_and_marks_the_form(self) -> None:
        self.assertIn("document.activeElement === send && !root.hidden) input.focus()", WIDGET)
        self.assertIn('form.setAttribute("aria-busy", String(value))', WIDGET)


class RegulatoryDisclosureTests(unittest.TestCase):
    def test_lookup_is_a_native_disclosure_with_escape_returning_to_the_summary(self) -> None:
        self.assertIn('const root = h("details", { id: "regulatory-chat" }, summary);', CHAT)
        body = CHAT[CHAT.index('root.addEventListener("keydown"') :][:200]
        self.assertIn('event.key !== "Escape" || !root.open', body)
        self.assertLess(body.index("root.open = false"), body.index("summary.focus()"))

    def test_lookup_and_alert_outcomes_are_announced(self) -> None:
        self.assertIn('const status = h("p", { role: "status" });', CHAT)
        self.assertIn('{ role: "status", "aria-atomic": "true" }', CHAT)
        self.assertIn('"aria-live": "polite", "aria-atomic": "true" },', CHAT)
        self.assertIn('role: "log", "aria-live": "polite"', CHAT)

    def test_doubt_route_stays_focusable_while_busy_and_announces_the_result(self) -> None:
        start = CHAT.index("const doubt = h(")
        body = CHAT[start : CHAT.index("if (answer.escalation)", start)]
        self.assertIn('doubt.setAttribute("aria-disabled", "true")', body)
        self.assertNotIn("doubt.disabled", body)
        self.assertIn("status.textContent = `${receipt.label}: sent to", body)
        self.assertIn("No legal approval or resident message.", body)


class ProvenanceAndOutcomeTests(unittest.TestCase):
    def test_each_reply_names_its_source_of_answer(self) -> None:
        for cue in (
            "Generative model suggestion (unapproved; check cited sources; no record changed)",
            "Deterministic decision or workflow rule (not generative AI; no record changed)",
            "Withheld. Cited sources did not support a stated status or figure (no record changed)",
            "Workflow-only help, no record changed",
            "generative AI model (${answer.model})",
            "AI-generated content may be incorrect.",
            "Model calls: ${receipt.model_calls}",
        ):
            with self.subTest(cue=cue):
                self.assertIn(cue, CHAT)
        self.assertIn("Skill: ${answer.skill}.", CHAT)

    def test_sources_disclosure_shows_a_count_and_a_no_source_warning(self) -> None:
        self.assertIn("`Sources (${sources.length})`", WIDGET)
        self.assertIn("No supporting source was provided. Check with a person", WIDGET)
        for tag in ("[Workflow rule]", "[Decision rule]", "[Case record]"):
            self.assertIn(tag, CHAT)
        self.assertIn("No source held for this answer.", CHAT)

    def test_outcomes_use_words_not_colour_for_every_reply_kind(self) -> None:
        names = re.search(r"const outcomeNames = \{([^}]*)\}", CHAT)
        self.assertIsNotNone(names)
        assert names is not None
        for kind in ("answer", "withheld", "abstain", "refused", "fallback"):
            self.assertRegex(names.group(1), rf"\b{kind}: ")
        self.assertIn("outcome: outcomeNames[answer.kind]", CHAT)
        self.assertIn("`Outcome: ${outcome}`", WIDGET)
        self.assertIn("chat-widget-outcome", WIDGET)

    def test_status_text_differs_for_answer_withheld_refused_and_fallback(self) -> None:
        body = function_body(CHAT, "function statusFor(kind)")
        messages = re.findall(r'return "([^"]+)"', body)
        self.assertEqual(len(messages), len(set(messages)))
        self.assertGreaterEqual(len(messages), 4)
        self.assertRegex(body, r'kind === "fallback"\) return "Workflow-only help added\.')
        self.assertIn("Reply withheld.", body)
        self.assertIn("Request refused.", body)
        self.assertIn("Answer added. Check the sources before relying on it.", body)

    def test_lookup_turn_shows_status_text_and_a_human_review_route(self) -> None:
        self.assertIn("`Lookup status: ${answer.kind}`", CHAT)
        self.assertIn("Sending does not approve or decide anything", CHAT)
        self.assertIn("synthetic-demo: not legal advice or approval", CHAT)

    def test_chat_says_in_plain_words_it_cannot_approve_or_change_records(self) -> None:
        self.assertIn("Chat cannot approve or change records.", CHAT)
        self.assertIn("Chat cannot approve, send, book or change records.", CHAT)
        self.assertIn("The assistant cannot change a record, approve, send or book anything", CHAT)
        self.assertIn('"employee-chat-entry-warning employee-chat-error"', CHAT)
        self.assertIn("AI suggestion, not approved", CHAT)

    def test_aria_invalid_sites_are_not_added_to_chat_scripts(self) -> None:
        self.assertNotIn("aria-invalid", CHAT)
        self.assertNotIn("aria-invalid", WIDGET)


if __name__ == "__main__":
    unittest.main()
