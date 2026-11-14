"""Safety lead and hazard triage screens give state meaning in text and are keyboard reachable."""

import json
import re
import unittest
from pathlib import Path

from test_safety_screens import SAFE, find_all, hazard, run, string_leaves

CSS = (Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/style.css").read_text()


class SafetyScreenWcagKeyboard(unittest.TestCase):
    def test_every_state_cue_is_plain_language_text(self) -> None:
        past = "2020-01-01T00:00:00+00:00"
        items = [
            hazard(response_due_at=past),
            hazard(response_due_at="2999-01-01T00:00:00+00:00"),
            hazard(
                responded_at=past, hold={"scope": "Home", "case_id": "C-1", "status": "Released"}
            ),
            hazard(state="Escalated", destination=SAFE),
        ]
        for screen in run(items).values():
            text = " ".join(string_leaves(screen["tree"]))
            for phrase in (
                "Stop-work indicator: retrofit work is paused",
                "Stop-work indicator: released",
                "Overdue service response",
                "Awaiting service response",
                "Service responded",
                "Service response clock: no due time recorded",
                "Escalation state: Escalated",
                "Urgent",
            ):
                self.assertIn(phrase, text)
            summary = " ".join(string_leaves(screen["summary"]))
            self.assertIn("Escalation state: Sent", summary)

    def test_sections_are_headed_landmarks_with_keyboard_jump_links(self) -> None:
        for screen in run([hazard()]).values():
            tree = screen["tree"]
            (nav,) = find_all(tree, "nav")
            self.assertEqual(nav["attrs"]["aria-label"], "Sections on this screen")
            links = find_all(nav, "a")
            self.assertEqual(len(links), 4)
            sections = find_all(tree, "section")
            self.assertEqual(len(sections), 4)
            for section in sections:
                (heading,) = [k for k in section["kids"] if k.get("tag") == "h2"]
                self.assertEqual(section["attrs"]["aria-labelledby"], heading["attrs"]["id"])
                self.assertEqual(heading["attrs"]["tabindex"], -1)
            self.assertEqual(find_all(tree, "button"), [])

    def test_focus_indicator_is_visible_and_skip_link_exists(self) -> None:
        self.assertRegex(CSS, r"(?m)^:focus-visible\{outline:")
        self.assertNotRegex(CSS, r":focus(-visible)?\s*\{[^}]*outline:\s*(none|0)\b")
        index = (
            Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/index.html"
        ).read_text()
        self.assertTrue(re.search(r'class="skip-link" href="#app"', index))

    def test_status_is_not_colour_only(self) -> None:
        payload = json.dumps(run([hazard()])["safety-lead"]["tree"])
        self.assertNotRegex(payload, r"\"style\"|\"color\"")


if __name__ == "__main__":
    unittest.main()
