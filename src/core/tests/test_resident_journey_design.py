"""Regression checks that the resident and representative design (#154) keeps its required content.

These tests read the design document only. They prove the specified coverage stays present; they
do not prove usability, accessibility or a resident-facing implementation.
"""

import re
import unittest
from pathlib import Path

DOC = (
    Path(__file__).resolve().parents[3]
    / "docs/reference/research/ux/customer-journeys/residents.md"
)
JOURNEYS = {
    "J1": "Choose each proposed measure",
    "J2": "Pause, withdraw or ask for more time",
    "J3": "Compare appointment offers and confirmations",
    "J4": "Know who will update you and when",
    "J5": "Handover, practise controls and get aftercare",
    "J6": "Challenge, complain and follow a remedy",
    "R1": "Task-limited representative briefing and actions",
}


def section(code: str) -> str:
    text = DOC.read_text(encoding="utf-8")
    heading = f"### {code}: {JOURNEYS[code]}"
    start = text.index(heading)
    match = re.search(r"^#{2,3} ", text[start + len(heading) :], re.MULTILINE)
    end = start + len(heading) + match.start() if match else len(text)
    return " ".join(text[start:end].split())


class ResidentJourneyDesign(unittest.TestCase):
    def test_every_required_topic_has_a_journey(self) -> None:
        for code in JOURNEYS:
            self.assertTrue(section(code), code)

    def test_each_journey_has_a_non_digital_equivalent(self) -> None:
        for code in JOURNEYS:
            self.assertIn("Non-digital equivalent:", section(code), code)

    def test_shared_frame_forbids_incapacity_inference_and_covers_needs(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        for phrase in (
            "Do not infer incapacity",
            "language, format, channel, contact times and adjustments",
            "Easy Read",
            "interpreting",
            "without a portal or smartphone",
        ):
            self.assertIn(phrase, text)

    def test_offers_are_distinct_from_confirmed_commitments(self) -> None:
        j3 = section("J3")
        for status in ("Offered - not booked", "Waiting for confirmation", "Visit confirmed"):
            self.assertIn(status, j3)
        self.assertIn("only after current resident/authorised representative", j3)
        self.assertIn("Changed offer/capacity returns to waiting", j3)

    def test_choice_is_per_measure_and_withdrawal_is_scoped(self) -> None:
        self.assertIn("no bundle-wide acceptance", section("J1"))
        self.assertIn("Your other choices have not changed", section("J2"))

    def test_remedy_status_stays_separate_from_response(self) -> None:
        j6 = section("J6")
        self.assertIn("A completed response is not a completed remedy", j6)
        self.assertIn("open remedy stays visible", j6)

    def test_representative_authority_is_task_limited_and_expires(self) -> None:
        r1 = section("R1")
        for phrase in (
            "never agree to works",
            "never receive the union of each other's permissions",
            "unavailable from that date",
            "Check authority again at each access/action",
            "Missing, unclear, disputed, expired or revoked authority",
            "No case details in denied response",
        ):
            self.assertIn(phrase, r1)

    def test_no_live_contact_and_validation_pending(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        flat = " ".join(text.split())
        self.assertIn("Do not paste it into live letters", flat)
        self.assertIn("neither builds it nor sends messages", flat)
        scripts = text[text.index("### Validation handoff and issue acceptance") :]
        self.assertGreaterEqual(scripts.count("| Not run |"), 7)


if __name__ == "__main__":
    unittest.main()
