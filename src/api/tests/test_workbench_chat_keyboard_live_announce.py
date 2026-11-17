"""#159 criterion: workbench chat panel keyboard operation and live announcements.

Static source checks only, not screen reader or assistive technology evidence.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
WIDGET = (WEB / "chat-widget.js").read_text()
CHAT = (WEB / "chat.js").read_text()
INDEX = (WEB / "index.html").read_text()


class LiveAnnouncementTests(unittest.TestCase):
    def test_transcript_is_a_polite_log_announcing_additions_and_text(self) -> None:
        self.assertRegex(
            WIDGET,
            r'role: "log", "aria-live": "polite", "aria-relevant": "additions"',
        )
        self.assertNotIn('"aria-live": "assertive"', WIDGET)

    def test_exactly_one_status_region_in_the_panel(self) -> None:
        self.assertEqual(len(re.findall(r'role: "status"', WIDGET)), 1)

    def test_every_reply_kind_has_a_status_announcement(self) -> None:
        body = CHAT[CHAT.index("function statusFor(") : CHAT.index("const outcomeNames")]
        for text in (
            "Reply withheld",
            "Request refused",
            "Workflow-only help added",
            "Answer added",
        ):
            self.assertIn(text, body)
        self.assertIn("ui.setStatus(statusFor(answer.kind))", CHAT)

    def test_workbench_alerts_keep_a_single_status_element(self) -> None:
        start = CHAT.index('id: "regulatory-alerts"')
        end = CHAT.index("function regulatoryChatPanel", start)
        self.assertEqual(CHAT[start:end].count('role: "status"'), 1)


class KeyboardOperationTests(unittest.TestCase):
    def test_launcher_is_a_native_button_with_dialog_state(self) -> None:
        self.assertIn('<button id="employee-chat-launcher" type="button"', INDEX)
        self.assertIn('"aria-expanded"', WIDGET)
        self.assertIn('"aria-controls"', WIDGET)

    def test_escape_closes_and_returns_focus_to_the_launcher(self) -> None:
        self.assertIn('event.key === "Escape"', WIDGET)
        self.assertIn("if (returnFocus && active) launcher.focus();", WIDGET)

    def test_enter_submits_and_shift_enter_keeps_newline(self) -> None:
        self.assertRegex(WIDGET, r'event\.key === "Enter" && !event\.shiftKey')
        self.assertIn("form.requestSubmit()", WIDGET)
        self.assertIn('node("textarea"', WIDGET)

    def test_transcript_is_keyboard_scrollable_and_controls_are_native(self) -> None:
        self.assertIn('tabindex: "0"', WIDGET)
        self.assertIn('node("summary"', WIDGET)
        self.assertNotIn('tabindex: "1', WIDGET)
        self.assertNotIn("aria-invalid", WIDGET)


if __name__ == "__main__":
    unittest.main()
