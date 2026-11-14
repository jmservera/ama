"""Today's briefing announces loading and states rule versus AI provenance (issue 531)."""

import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
APP = (WEB / "app.js").read_text()
CSS = (WEB / "style.css").read_text()


class BriefingLoadingProvenanceTests(unittest.TestCase):
    def test_busy_is_on_the_body_not_an_ancestor_of_the_status(self) -> None:
        self.assertIn('content.setAttribute("aria-busy", "true");', APP)
        self.assertIn('content.removeAttribute("aria-busy");', APP)
        self.assertNotIn(
            'box.setAttribute("aria-busy"',
            APP.split("const load = async")[1].split("box.append(status")[0],
        )
        self.assertIn("box.append(status, dismiss, mode, content);", APP)

    def test_loading_status_is_plain_language_and_polite(self) -> None:
        self.assertIn("Reading case summaries... Your case list is still available.", APP)
        self.assertIn(
            "Reading case summaries... Refreshing today's briefing; "
            "the current text stays visible until the new one is ready.",
            APP,
        )
        self.assertIn('role: "status", "aria-live": "polite", class: "briefing-status"', APP)

    def test_status_space_is_reserved_to_avoid_layout_shift(self) -> None:
        self.assertIn(".briefing-status{min-height:", CSS)

    def test_provenance_separates_rule_priority_from_ai_wording(self) -> None:
        for fragment in (
            "Set by fixed rules, not by AI.",
            "Summarised by AI. Check it against the sources.",
            "Written by rules and templates. No AI was used.",
            "Open any case from the list or the sources below.",
            "Why listed: one of the first permitted open cases in the fixed ranking.",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, APP)


if __name__ == "__main__":
    unittest.main()
