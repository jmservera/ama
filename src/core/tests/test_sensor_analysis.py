"""Deterministic versioned sensor analysis: exercise values, no task writes (Refs #111)."""

import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import ClassVar

from zava_forward.core import sensor_analysis as sa
from zava_forward.core.synthetic import sensor_scenarios as ss

WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
AS_OF = WINDOW.end
APPROVAL = sa.RuleApproval(sa.RULE_ID, sa.ANALYSIS_VERSION, "Exercise reviewer", "EX-APPROVAL-1")
APPROVED = sa.AnalysisPolicy(approval=APPROVAL)


class SensorAnalysisTests(unittest.TestCase):
    cases: ClassVar[dict[str, ss.Case]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = {c.truth.label: c for c in ss.generate() if c.truth.family == "damp"}

    def derive(
        self,
        label: str,
        consent: str = "granted",
        policy: sa.AnalysisPolicy | None = None,
        as_of: datetime = AS_OF,
    ) -> sa.Signal:
        case = self.cases[label]
        return sa.derive_signal(case.rows[0]["home_id"], case.rows, WINDOW, as_of, consent, policy)

    def test_outcomes_match_labelled_exercise_scenarios(self) -> None:
        for label, case in self.cases.items():
            with self.subTest(label=label):
                expected = case.truth.expected_outcome
                signal = self.derive(label)
                self.assertEqual(signal.outcome, expected)
                self.assertEqual(
                    signal.sufficiency,
                    sa.INSUFFICIENT if expected == sa.INSUFFICIENT else sa.SUFFICIENT,
                )

    def test_reproducible_from_retained_readings_and_order_independent_digest(self) -> None:
        case = self.cases["sustained_high_humidity"]
        first = self.derive("sustained_high_humidity")
        self.assertEqual(first, self.derive("sustained_high_humidity"))
        home = case.rows[0]["home_id"]
        shuffled = sa.derive_signal(home, list(reversed(case.rows)), WINDOW, AS_OF, "granted")
        self.assertEqual(first.input_digest, shuffled.input_digest)
        changed = [dict(r) for r in case.rows]
        changed[5]["humidity_pct"] = "10.00"
        self.assertNotEqual(
            first.input_digest,
            sa.derive_signal(home, changed, WINDOW, AS_OF, "granted").input_digest,
        )

    def test_versions_and_labels_are_recorded(self) -> None:
        signal = self.derive("normal")
        self.assertEqual(signal.analysis_version, sa.ANALYSIS_VERSION)
        self.assertEqual(signal.policy_version, sa.ANALYSIS_VERSION)
        self.assertTrue(signal.threshold_label.startswith("EXERCISE VALUE"))
        with self.assertRaises(ValueError):
            replace(APPROVED, threshold_label="plausible").validate()

    def test_declined_unknown_stale_and_missing_never_lower_priority(self) -> None:
        declined = self.derive("sustained_high_humidity", consent="declined")
        unknown = self.derive("sustained_high_humidity", consent="unknown")
        stale = self.derive("sustained_high_humidity", as_of=AS_OF + timedelta(days=10))
        missing = self.derive("missing_data")
        self.assertEqual(declined.sufficiency, sa.DECLINED)
        self.assertEqual(unknown.reasons, ("CONSENT_NOT_CONFIRMED",))
        self.assertEqual(stale.sufficiency, sa.STALE)
        for signal in (declined, unknown, stale, missing):
            with self.subTest(reasons=signal.reasons):
                self.assertEqual(signal.outcome, sa.INSUFFICIENT)
                self.assertEqual(signal.priority_effect, "NONE")
                self.assertFalse(signal.diagnoses_hazard)
                self.assertIsNone(sa.review_task_candidate(signal, APPROVED))

    def test_empty_series_is_stale_not_normal(self) -> None:
        signal = sa.derive_signal("ZF-1", [], WINDOW, AS_OF, "granted")
        self.assertEqual((signal.sufficiency, signal.outcome), (sa.STALE, sa.INSUFFICIENT))

    def test_no_candidate_without_approved_rule(self) -> None:
        signal = self.derive("sustained_high_humidity")
        self.assertEqual(signal.outcome, sa.REVIEW)
        self.assertIsNone(sa.review_task_candidate(signal))
        wrong = replace(APPROVAL, rule_id="OTHER")
        self.assertIsNone(sa.review_task_candidate(signal, replace(APPROVED, approval=wrong)))
        old = replace(APPROVAL, policy_version="older-v0")
        self.assertIsNone(sa.review_task_candidate(signal, replace(APPROVED, approval=old)))

    def test_approved_review_signal_proposes_only_a_human_task(self) -> None:
        signal = self.derive("repeated_overnight_peaks", policy=APPROVED)
        candidate = sa.review_task_candidate(signal, APPROVED)
        assert candidate is not None
        self.assertEqual(candidate.task_type, "SENSOR_REVIEW_DUE")
        self.assertEqual(candidate.queue, "condition-assessment")
        self.assertEqual(candidate.status, "PROPOSED")
        self.assertTrue(candidate.resident_report_unaffected)
        for flag in ("changes_ranking", "starts_clock", "releases_hold", "diagnoses_hazard"):
            self.assertFalse(getattr(candidate, flag))
        self.assertEqual(candidate, sa.review_task_candidate(signal, APPROVED))

    def test_no_signal_never_proposes_a_task(self) -> None:
        for label in ("normal", "seasonal_shift"):
            signal = self.derive(label, policy=APPROVED)
            self.assertEqual(signal.outcome, sa.NO_SIGNAL)
            self.assertIsNone(sa.review_task_candidate(signal, APPROVED))

    def test_outputs_carry_no_raw_readings_or_sensor_identifiers(self) -> None:
        signal = self.derive("repeated_overnight_peaks", policy=APPROVED)
        candidate = sa.review_task_candidate(signal, APPROVED)
        assert candidate is not None
        sensor = self.cases["repeated_overnight_peaks"].rows[0]["sensor_id"]
        for value in (sa.as_dict(signal), sa.as_dict(candidate)):
            text = repr(value)
            self.assertNotIn(sensor, text)
            self.assertNotIn("temperature_c", text)
            self.assertNotIn("humidity_pct", text)

    def test_rows_for_other_homes_are_ignored(self) -> None:
        mixed = [r for c in self.cases.values() for r in c.rows]
        home = self.cases["normal"].rows[0]["home_id"]
        alone = sa.derive_signal(home, self.cases["normal"].rows, WINDOW, AS_OF, "granted")
        self.assertEqual(alone, sa.derive_signal(home, mixed, WINDOW, AS_OF, "granted"))

    def test_invalid_inputs_are_refused(self) -> None:
        rows = self.cases["normal"].rows
        with self.assertRaises(ValueError):
            sa.derive_signal("H", rows, WINDOW, AS_OF, "maybe")
        with self.assertRaises(ValueError):
            sa.derive_signal("H", rows, WINDOW, datetime(2024, 2, 1), "granted")
        with self.assertRaises(ValueError):
            sa.derive_signal(
                "H",
                rows,
                WINDOW,
                datetime(2024, 2, 1, tzinfo=UTC),
                "granted",
                sa.AnalysisPolicy(max_staleness_hours=0),
            )


if __name__ == "__main__":
    unittest.main()
