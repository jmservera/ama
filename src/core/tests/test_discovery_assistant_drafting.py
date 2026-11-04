"""Deterministic calculation with draft-only narrative (Refs #125)."""

import unittest
from collections.abc import Mapping

from zava_forward.core import discovery_assistant_drafting as dad


def events() -> list[dad.StageEvent]:
    return [
        dad.StageEvent("P1", "survey", "2026-01-01T00:00:00+00:00", "SRC-1"),
        dad.StageEvent("P1", "design", "2026-01-02T12:00:00+00:00", "SRC-2"),
        dad.StageEvent("P1", "install", "2026-01-03T12:00:00+00:00", "SRC-3"),
    ]


class CalculationTests(unittest.TestCase):
    def test_durations_are_deterministic_and_sorted(self) -> None:
        out = dad.calculate_stage_durations(list(reversed(events())))
        self.assertEqual(out.hours, {"design": 24.0, "survey": 36.0})
        self.assertEqual(out.source_references, ("SRC-1", "SRC-2", "SRC-3"))
        self.assertEqual(out, dad.calculate_stage_durations(events()))

    def test_bad_events_are_gaps_not_guesses(self) -> None:
        bad = [
            dad.StageEvent("P2", "survey", "not a date", "SRC-9"),
            dad.StageEvent("P2", "design", "2026-01-01T00:00:00", "SRC-9"),
            dad.StageEvent("P2", "install", "2026-01-01T00:00:00+00:00", " "),
        ]
        out = dad.calculate_stage_durations(bad)
        self.assertEqual(out.hours, {})
        self.assertEqual(len(out.gaps), 3)


class DraftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.durations = dad.calculate_stage_durations(events())

    def test_no_drafter_uses_plain_text_and_manual_path(self) -> None:
        report = dad.draft_evidence(self.durations)
        self.assertFalse(report.model_used)
        self.assertEqual(report.rejected_reason, "NO_DRAFTER")
        self.assertIn("survey: 36 hours", report.text)
        self.assertIn("SRC-1", report.text)
        self.assertIn("Manual analysis", report.manual_path)
        self.assertEqual(report.status, dad.DRAFT_FOR_HUMAN_REVIEW)
        self.assertFalse(report.validated_finding)

    def test_good_draft_is_accepted_but_stays_a_draft(self) -> None:
        def drafter(hours: Mapping[str, float], refs: tuple[str, ...]) -> str:
            return f"Survey took {hours['survey']:g} hours (see {refs[0]})."

        report = dad.draft_evidence(self.durations, drafter)
        self.assertTrue(report.model_used)
        self.assertEqual(report.rejected_reason, "")
        self.assertEqual(report.status, dad.DRAFT_FOR_HUMAN_REVIEW)
        self.assertFalse(report.validated_finding)

    def test_invented_number_is_rejected_and_falls_back(self) -> None:
        def drafter(hours: Mapping[str, float], refs: tuple[str, ...]) -> str:
            return "Survey took 99 hours (SRC-1)."

        report = dad.draft_evidence(self.durations, drafter)
        self.assertFalse(report.model_used)
        self.assertEqual(report.rejected_reason, "NUMBER_NOT_CALCULATED")
        self.assertNotIn("99", report.text)

    def test_uncited_and_empty_drafts_are_rejected(self) -> None:
        def fixed(text: str) -> dad.Drafter:
            def drafter(hours: Mapping[str, float], refs: tuple[str, ...]) -> str:
                return text

            return drafter

        for text, reason in (("Survey took 36 hours.", "NO_SOURCE_CITED"), (" ", "EMPTY_DRAFT")):
            with self.subTest(text=text):
                report = dad.draft_evidence(self.durations, fixed(text))
                self.assertFalse(report.model_used)
                self.assertEqual(report.rejected_reason, reason)

    def test_unavailable_model_still_gives_deterministic_result(self) -> None:
        def drafter(hours: Mapping[str, float], refs: tuple[str, ...]) -> str:
            raise TimeoutError("model offline")

        report = dad.draft_evidence(self.durations, drafter)
        self.assertEqual(report.rejected_reason, "DRAFTER_UNAVAILABLE")
        self.assertIn("design: 24 hours", report.text)

    def test_no_durations_gives_plain_statement(self) -> None:
        report = dad.draft_evidence(dad.calculate_stage_durations([]))
        self.assertIn("No stage durations", report.text)


if __name__ == "__main__":
    unittest.main()
