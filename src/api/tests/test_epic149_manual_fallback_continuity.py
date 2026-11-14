"""Epic #149: manual path continuity and plain-language degraded-AI cues.

Source-level engineering evidence on constructed data. It shows that staff and resident journeys
keep a manual route with text status cues when AI is disabled, withheld or unavailable. It is not
WCAG conformance, assistive-technology acceptance or comprehension evidence, which stay with human
testers.
"""

import re
import unittest
from pathlib import Path

API = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api"


def read(rel: str) -> str:
    return (API / rel).read_text(encoding="utf-8")


class StaffManualContinuity(unittest.TestCase):
    def test_case_advance_is_a_manual_button_with_text_gate_reasons(self) -> None:
        app = read("web/app.js")
        self.assertIn("/advance", app)
        self.assertIn("Ready to book the installation", app)
        self.assertIn("This case cannot move on yet:", app)
        self.assertIn('h("li", {}, x)', app)
        self.assertIn('act == "advance"', read("server.py"))

    def test_evidence_checklist_states_are_words_with_a_glyph_not_colour_alone(self) -> None:
        app = read("web/app.js")
        self.assertIn('`${x.present ? "Have" : "Need"}: ${x.kind}`', app)
        self.assertIn("Still needed:", app)
        self.assertIn("All evidence is in.", app)
        css = read("web/style.css")
        self.assertRegex(css, r"\.flag\.danger:before[^{]*\{content:\"\\26A0")

    def test_ai_unavailable_states_keep_manual_work_and_use_status_roles(self) -> None:
        js = read("web/assistants.js")
        self.assertGreaterEqual(js.count("AI assistance unavailable. Work continues manually."), 3)
        self.assertIn("Ordinary case controls remain available.", js)
        self.assertIn("Use the ordinary case controls; no one is waiting on a suggestion.", js)
        self.assertIn("Continue ordinary case work manually", js)
        self.assertIn("Continue manual case work", js)
        self.assertIn("Withheld: monitoring consent is not granted now", js)
        self.assertIn('role: "alert"', js)
        self.assertIn('role: "status"', js)
        self.assertIn("Owner: your team manager. Next action:", js)

    def test_case_workspace_announces_unavailable_ai_count_politely(self) -> None:
        js = read("web/case-workspace.js")
        self.assertIn('role: "status", "aria-live": "polite"', js)
        self.assertIn("AI review count unavailable.", js)

    def test_server_degraded_errors_name_the_manual_route(self) -> None:
        server = read("server.py")
        self.assertGreaterEqual(server.count("continue ordinary case work manually"), 2)
        self.assertIn("continue the ordinary quality check manually", server)
        self.assertIn("use the manual route: manual-sensor-review", server)


class ResidentManualContinuity(unittest.TestCase):
    def test_manual_callback_form_works_without_chat_or_ai(self) -> None:
        js = read("resident_demo/web/assistant.js")
        self.assertIn("Use this manual form without chat or AI.", js)
        self.assertIn("Use the manual callback form", js)
        self.assertIn("phone your housing officer using your usual number", js)
        self.assertIn("Ask a person about access needs or adjustments.", js)

    def test_chat_load_failure_is_an_alert_with_a_manual_way_forward(self) -> None:
        js = read("resident_demo/web/assistant.js")
        match = re.search(r"Chat could not load\.[^\"]*", js)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertIn("The manual callback form is still available.", match.group(0))
        self.assertIn('setAttribute("role", "alert")', js)

    def test_ai_summary_falls_back_to_rules_with_a_plain_reason(self) -> None:
        js = read("resident_demo/web/demo.js")
        self.assertIn("AI summary is not available right now (", js)
        self.assertIn("Showing the rules-based summary from your recorded case facts instead.", js)
        self.assertIn('"AI is not enabled"', js)
        self.assertIn('"the assistant could not be reached"', js)
        self.assertIn("It is a suggestion, not approved.", js)

    def test_unavailable_features_are_listed_in_words(self) -> None:
        js = read("resident_demo/web/demo.js")
        self.assertIn("Not available in this showcase", js)
        self.assertIn("missing or unavailable", js)


class NoColourOnlyOrJargonCues(unittest.TestCase):
    def test_degraded_copy_has_no_colour_only_instruction(self) -> None:
        for rel in (
            "web/assistants.js",
            "resident_demo/web/assistant.js",
            "resident_demo/web/demo.js",
        ):
            for line in read(rel).splitlines():
                if "unavailable" in line.lower() or "manual" in line.lower():
                    self.assertNotRegex(
                        line, r"(?i)\b(red|green|amber)\b", f"{rel}: {line.strip()[:80]}"
                    )


if __name__ == "__main__":
    unittest.main()
