import unittest

from prototype.properwarm.domain import (
    CASE_STAGES,
    check_transition,
    escalation_status,
    is_eligible_no_access,
    validate_threshold,
)


class DomainTests(unittest.TestCase):
    def test_threshold_is_strictly_greater_than_configured_value(self) -> None:
        events = [
            {"outcome": "resident_no_access_verified", "appointment_confirmed": True}
            for _ in range(6)
        ]

        self.assertFalse(escalation_status(events[:5], 5).required)
        status = escalation_status(events, 5)
        self.assertTrue(status.required)
        self.assertEqual(status.eligible_count, 6)

    def test_only_confirmed_verified_resident_no_access_is_eligible(self) -> None:
        self.assertTrue(is_eligible_no_access("resident_no_access_verified", True))
        for outcome, confirmed in (
            ("resident_no_access_verified", False),
            ("provider_no_show", True),
            ("cancelled", True),
            ("rescheduled", True),
            ("attended", True),
        ):
            with self.subTest(outcome=outcome, confirmed=confirmed):
                self.assertFalse(is_eligible_no_access(outcome, confirmed))

    def test_closed_episode_events_are_excluded_from_active_count(self) -> None:
        events = [
            {"outcome": "resident_no_access_verified", "appointment_confirmed": True},
            {"outcome": "resident_no_access_verified", "appointment_confirmed": True},
            {"outcome": "case_closed", "appointment_confirmed": False},
            {"outcome": "case_reopened", "appointment_confirmed": False},
            {"outcome": "resident_no_access_verified", "appointment_confirmed": True},
        ]

        self.assertEqual(escalation_status(events, 0).eligible_count, 1)
        self.assertEqual(escalation_status(events, 0, active=False).eligible_count, 0)

    def test_stage_transition_fails_closed_for_missing_gate_and_safety_hold(self) -> None:
        stage, missing = check_transition(CASE_STAGES[0], {}, safety_hold_active=False)
        self.assertIsNone(stage)
        self.assertIn("Named owner", missing)

        stage, missing = check_transition(
            CASE_STAGES[0], {"named_owner": True}, safety_hold_active=True
        )
        self.assertIsNone(stage)
        self.assertIn("Active safety hold", missing)

        stage, missing = check_transition(
            CASE_STAGES[0], {"named_owner": True}, safety_hold_active=False
        )
        self.assertEqual(stage, CASE_STAGES[1])
        self.assertEqual(missing, [])

    def test_threshold_rejects_non_integer_and_out_of_range_values(self) -> None:
        for value in (-1, 101, 5.5, True, "not-a-number"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_threshold(value)


if __name__ == "__main__":
    unittest.main()
