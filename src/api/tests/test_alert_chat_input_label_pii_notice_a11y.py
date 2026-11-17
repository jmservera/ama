"""Accessible names, PII guardrail and Enter-to-send for alert and chat inputs (#215)."""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()

NOTICE = (
    "Do not enter personal or sensitive resident information. "
    "Chat cannot approve or change records."
)


def _block(source: str, start: str, end: str) -> str:
    begin = source.index(start)
    return source[begin : source.index(end, begin)]


class EmployeeChatInputTests(unittest.TestCase):
    def test_prompt_and_skill_selector_have_explicit_accessible_names(self) -> None:
        self.assertRegex(WIDGET, r'id: `\$\{id\}-question`.*"aria-label": questionLabel')
        self.assertRegex(WIDGET, r'id: `\$\{id\}-skill`.*"aria-label": skillLabel')
        self.assertIn('questionLabel: "Your work question", skillLabel: "Agent skill"', CHAT)

    def test_prompt_disables_autocomplete_and_caps_length(self) -> None:
        textarea = re.search(r'node\("textarea".*', WIDGET)
        assert textarea is not None
        self.assertIn('autocomplete: "off"', textarea.group(0))
        self.assertIn("maxlength: String(maxLength)", textarea.group(0))

    def test_plain_language_guardrail_is_described_by_the_prompt(self) -> None:
        self.assertIn(NOTICE, CHAT)
        self.assertIn('{ id: "employee-chat-entry-warning", class: "chat-widget-meta" }', CHAT)
        describes = re.findall(r'input\.setAttribute\("aria-describedby", "([^"]+)"', CHAT)
        self.assertGreaterEqual(len(describes), 2)
        for value in describes:
            ids = value.split()
            self.assertIn("employee-chat-entry-warning", ids)
            self.assertIn("employee-chat-error", ids)

    def test_notice_sits_before_the_prompt_in_reading_order(self) -> None:
        self.assertIn("form.append(beforeInput, input, keys, tools, reason)", WIDGET)
        self.assertIn("ui.beforeInput.append(", CHAT)

    def test_empty_submission_is_announced_and_returns_focus(self) -> None:
        self.assertIn(
            'if (!question) { ui.fail("Type a question first."); ui.focusInput(); return; }', CHAT
        )
        self.assertRegex(WIDGET, r'id: `\$\{id\}-error`, role: "alert"')

    def test_enter_sends_but_shift_enter_and_composition_keep_multiline(self) -> None:
        handler = _block(WIDGET, 'input.addEventListener("keydown"', "return {")
        self.assertIn('event.key === "Enter"', handler)
        self.assertIn("!event.shiftKey", handler)
        self.assertIn("!event.isComposing", handler)
        self.assertIn("event.keyCode !== 229", handler)
        self.assertIn("form.requestSubmit()", handler)
        self.assertIn('rows: "2"', WIDGET)


class RegulatoryPanelControlTests(unittest.TestCase):
    def test_cited_lookup_prompt_has_label_and_described_privacy_notice(self) -> None:
        self.assertIn('h("label", { for: "regulatory-question" }, "Cited source question")', CHAT)
        self.assertIn('id: "regulatory-question"', CHAT)
        self.assertIn('"aria-describedby": "regulatory-privacy"', CHAT)
        self.assertIn('id: "regulatory-privacy"', CHAT)
        self.assertIn("Do not enter resident personal or special-category details.", CHAT)

    def test_cited_lookup_prompt_keeps_autocomplete_off_and_announces_empty_input(self) -> None:
        textarea = re.search(r'h\("textarea", \{ id: "regulatory-question".*', CHAT)
        assert textarea is not None
        self.assertIn('autocomplete: "off"', textarea.group(0))
        self.assertIn('maxlength: "1000"', textarea.group(0))
        self.assertIn('status.textContent = "Enter a source question."; input.focus();', CHAT)
        # The only key handler is Escape on the disclosure; Enter and Shift+Enter stay native.
        self.assertEqual(CHAT.count('event.key === "Enter"'), 0)

    def test_alert_controls_are_named_and_the_alert_panel_states_the_boundary(self) -> None:
        mode = _block(CHAT, "function regulatoryPlainMode", "const regulatoryStates")
        self.assertIn('h("div", { class: "regulatory-mode" },', mode)
        self.assertIn(
            'h("label", { for: id }, input, " Plain-language explanations")',
            mode,
        )
        self.assertIn('type: "checkbox", id', mode)
        panel = _block(CHAT, "function regulatoryAlertsPanel", "const lookupMeanings")
        self.assertIn(
            'h("button", { type: "button", class: "alt", onclick: load }, "Refresh alerts")', panel
        )
        self.assertIn("This panel cannot acknowledge, decide compliance", panel)
        self.assertIn('role: "status"', panel)
        self.assertNotRegex(panel, r"<input|h\(\"(?:input|select|textarea)\"")


if __name__ == "__main__":
    unittest.main()
