"""Static ARIA semantics for the regulatory alert banner and grounded chat panel (Refs #215).

These checks read the shipped markup and scripts only. They do not replace
assistive-technology or human usability testing, which stays open on #215.
"""

import re
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
INDEX = (WEB / "index.html").read_text()
CHAT = (WEB / "chat.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()


def function_body(source: str, name: str) -> str:
    start = source.index(f"function {name}(")
    end = source.find("\nfunction ", start + 1)
    return source[start : end if end != -1 else len(source)]


ALERTS = function_body(CHAT, "regulatoryAlertsPanel")
PANEL = function_body(CHAT, "regulatoryChatPanel")


class RegulatoryChatLiveRegionSemantics(unittest.TestCase):
    def test_alert_banner_and_chat_panel_are_named_regions(self) -> None:
        self.assertIn('"aria-labelledby": "regulatory-alerts-title"', ALERTS)
        self.assertIn('h("h2", { id: "regulatory-alerts-title" }', ALERTS)
        self.assertIn('h("section", { class: "card", id: "regulatory-alerts"', ALERTS)
        self.assertIn('h("details", { id: "regulatory-chat" }', PANEL)
        self.assertIn('h("summary", {}, "Cited regulatory lookup', PANEL)
        self.assertIn('<main id="app"', INDEX)
        self.assertIn('<nav id="nav" aria-label="Workbench"', INDEX)

    def test_polite_status_regions_do_not_use_assertive_semantics(self) -> None:
        for source in (ALERTS, PANEL):
            self.assertIn('role: "status"', source)
            self.assertNotIn("assertive", source)
            self.assertNotIn('role: "alert"', source)
        self.assertIn('role: "log", "aria-live": "polite"', PANEL)
        self.assertIn('"aria-live": "polite", "aria-atomic": "true"', PANEL)
        self.assertNotIn("assertive", INDEX + WIDGET)

    def test_urgent_errors_are_separate_from_polite_status(self) -> None:
        alerts = re.findall(r'<[^>]*role="alert"[^>]*>', INDEX)
        self.assertEqual(1, len(alerts))
        self.assertIn('id="account-error"', alerts[0])
        self.assertNotIn("aria-live", alerts[0])
        for tag in re.findall(r'<[^>]*role="status"[^>]*>', INDEX):
            self.assertNotIn('role="alert"', tag)

    def test_chat_controls_have_explicit_accessible_names(self) -> None:
        self.assertIn('h("label", { for: "regulatory-question" }, "Cited source question")', PANEL)
        self.assertIn('id: "regulatory-question"', PANEL)
        self.assertIn('h("button", { type: "submit" }, "Look up cited sources")', PANEL)
        self.assertIn('}, "Refresh alerts")', ALERTS)
        self.assertIn('"aria-label": "Cited regulatory updates"', PANEL)
        self.assertIn('"aria-label": "Cited regulatory turns"', PANEL)
        self.assertIn('id="employee-chat-launcher" type="button" aria-label="Chat"', INDEX)
        self.assertIn('"aria-label": questionLabel', WIDGET)
        self.assertIn('"aria-label": skillLabel', WIDGET)

    def test_no_positive_tabindex_focus_order_traps(self) -> None:
        for name, source in (("index.html", INDEX), ("chat.js", CHAT), ("chat-widget.js", WIDGET)):
            values = re.findall(r"""tabindex["']?\s*[=:]\s*["']?(-?\d+)""", source, re.IGNORECASE)
            self.assertTrue(all(int(value) <= 0 for value in values), f"{name}: {values}")

    def test_usability_testing_remains_open(self) -> None:
        self.assertNotIn("closes #215", (INDEX + CHAT + WIDGET).lower())


if __name__ == "__main__":
    unittest.main()
