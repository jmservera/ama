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

    @unittest.expectedFailure
    def test_policy_identity_binds_threshold(self) -> None:
        # Measured gap (Refs #111): a changed threshold keeps the same policy_version, so an
        # approval of that version would cover any threshold. Remove the decorator once fixed.
        default = self.derive("normal")
        strict = self.derive("normal", policy=sa.AnalysisPolicy(humidity_threshold_pct=40.0))
        self.assertNotEqual(default.outcome, strict.outcome)
        self.assertNotEqual(default.policy_version, strict.policy_version)

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

    def test_reproduce_tolerates_malformed_observed_at(self) -> None:
        rows = [dict(r) for r in self.cases[next(iter(self.cases))].rows]
        clean = sa.reproduce_sensor_analysis(rows)
        rows.append({**rows[0], "observed_at": "not-a-time"})
        rows.append({k: v for k, v in rows[0].items() if k != "observed_at"})
        result = sa.reproduce_sensor_analysis(rows)
        self.assertEqual(result["analysis_version"], clean["analysis_version"])
        self.assertIsInstance(result["signal"], dict)
        with self.assertRaisesRegex(ValueError, "NO_VALID_OBSERVATIONS"):
            sa.reproduce_sensor_analysis([{**rows[0], "observed_at": "bad"}])

    def test_reproduce_review_task_is_deterministic_with_version_provenance(self) -> None:
        rows = [dict(r) for r in self.cases["sustained_high_humidity"].rows]
        first = sa.reproduce_review_task(rows, APPROVED)
        again = sa.reproduce_review_task(list(reversed(rows)), APPROVED)
        self.assertEqual(first, again)
        analysis = sa.reproduce_sensor_analysis(rows, APPROVED)
        self.assertEqual(analysis["provenance"], first["provenance"])
        self.assertEqual(analysis["signal"], first["signal"])
        self.assertEqual(analysis["review_task"], first["review_task"])
        self.assertEqual(analysis["output_digest"], first["provenance"]["output_digest"])
        task = first["review_task"]
        assert task is not None
        provenance = first["provenance"]
        self.assertEqual(task["input_digest"], provenance["input_digest"])
        self.assertEqual(task["policy_version"], provenance["policy_version"])
        self.assertEqual(provenance["analysis_version"], sa.ANALYSIS_VERSION)
        self.assertEqual(provenance["comparator_version"], "sensor-comparator-exercise-v1")
        self.assertEqual(provenance["schema_version"], "sensor-fault-input-v1")
        self.assertEqual(provenance["approver_role"], "Exercise reviewer")
        self.assertEqual(provenance["approval_reference"], "EX-APPROVAL-1")
        self.assertTrue(provenance["rule_approved"])
        self.assertRegex(provenance["policy_digest"], r"^[0-9a-f]{64}$")
        self.assertRegex(provenance["output_digest"], r"^[0-9a-f]{64}$")
        sensor = rows[0]["sensor_id"]
        reading_id = rows[0]["reading_id"]
        prov_text = repr(provenance)
        self.assertNotIn(sensor, prov_text)
        self.assertNotIn(reading_id, prov_text)
        self.assertNotIn("temperature_c", prov_text)
        unapproved = sa.reproduce_review_task(rows)
        self.assertIsNone(unapproved["review_task"])
        self.assertFalse(unapproved["provenance"]["rule_approved"])
        self.assertIsNone(unapproved["provenance"]["approver_role"])
        self.assertIsNone(unapproved["provenance"]["approval_reference"])
        self.assertEqual(unapproved["provenance"]["input_digest"], provenance["input_digest"])
        self.assertNotEqual(unapproved["provenance"]["policy_digest"], provenance["policy_digest"])
        self.assertNotEqual(unapproved["provenance"]["output_digest"], provenance["output_digest"])
        mismatched = sa.AnalysisPolicy(approval=replace(APPROVAL, rule_id="OTHER-RULE"))
        masked = sa.reproduce_review_task(rows, mismatched)
        self.assertIsNone(masked["review_task"])
        self.assertFalse(masked["provenance"]["rule_approved"])
        self.assertIsNone(masked["provenance"]["approver_role"])
        self.assertIsNone(masked["provenance"]["approval_reference"])
        strict = sa.reproduce_review_task(rows, replace(APPROVED, humidity_threshold_pct=99.0))
        self.assertEqual(strict["provenance"]["input_digest"], provenance["input_digest"])
        self.assertNotEqual(strict["provenance"]["policy_digest"], provenance["policy_digest"])
        self.assertIsNone(strict["review_task"])
        quiet = sa.reproduce_review_task([dict(r) for r in self.cases["normal"].rows], APPROVED)
        self.assertIsNone(quiet["review_task"])

    def test_reproduce_handles_empty_window_and_rejects_missing_or_mixed_home(self) -> None:
        empty = sa.reproduce_review_task([], APPROVED, home_id="ZF-EMPTY-1", window=WINDOW)
        self.assertEqual(empty["signal"]["sufficiency"], sa.STALE)
        self.assertEqual(empty["signal"]["outcome"], sa.INSUFFICIENT)
        self.assertEqual(empty["signal"]["reasons"], ("NO_READINGS_IN_WINDOW",))
        self.assertEqual(empty["signal"]["priority_effect"], "NONE")
        self.assertIsNone(empty["review_task"])
        self.assertEqual(empty["provenance"]["home_id"], "ZF-EMPTY-1")
        with self.assertRaisesRegex(ValueError, "SINGLE_HOME_REQUIRED"):
            sa.reproduce_review_task([])
        with self.assertRaisesRegex(ValueError, "NO_VALID_OBSERVATIONS"):
            sa.reproduce_review_task([], home_id="ZF-EMPTY-1")
        sample = dict(self.cases["normal"].rows[0])
        for bad_home in ("", " ZF-1 "):
            with self.assertRaisesRegex(ValueError, "SINGLE_HOME_REQUIRED"):
                sa.reproduce_review_task([{**sample, "home_id": bad_home}])
        missing_home = {k: v for k, v in sample.items() if k != "home_id"}
        with self.assertRaisesRegex(ValueError, "SINGLE_HOME_REQUIRED"):
            sa.reproduce_review_task([missing_home])
        with self.assertRaisesRegex(ValueError, "SINGLE_HOME_REQUIRED"):
            sa.reproduce_review_task([sample], home_id="ZF-OTHER")
        signal = self.derive("sustained_high_humidity", policy=APPROVED)
        self.assertIsNone(
            sa.review_task_candidate(replace(signal, analysis_version="older-v0"), APPROVED)
        )
        self.assertIsNone(
            sa.review_task_candidate(
                replace(signal, threshold_label="SOURCED: different"), APPROVED
            )
        )
        with self.assertRaisesRegex(ValueError, "CANDIDATE_MISMATCH"):
            sa.version_provenance(signal, APPROVED, candidate=None)

    def test_digest_changes_with_calibration_flag(self) -> None:
        rows = [dict(r) for r in self.cases[next(iter(self.cases))].rows]
        base = sa.derive_signal(rows[0]["home_id"], rows, WINDOW, AS_OF, "granted")
        rows[0]["calibrated"] = "false"
        flipped = sa.derive_signal(rows[0]["home_id"], rows, WINDOW, AS_OF, "granted")
        self.assertNotEqual(base.input_digest, flipped.input_digest)

    def test_digest_detects_reading_id_schema_shape_and_cross_row_swaps(self) -> None:
        base_rows = [dict(r) for r in self.cases["normal"].rows[:4]]
        home = base_rows[0]["home_id"]
        base = sa.derive_signal(home, base_rows, WINDOW, AS_OF, "granted")
        renamed_id = [dict(r) for r in base_rows]
        renamed_id[0]["reading_id"] = "R-MUTATED"
        self.assertNotEqual(
            base.input_digest,
            sa.derive_signal(home, renamed_id, WINDOW, AS_OF, "granted").input_digest,
        )
        extra_field = [dict(r) for r in base_rows]
        extra_field[0]["extra_key"] = "unexpected"
        self.assertNotEqual(
            base.input_digest,
            sa.derive_signal(home, extra_field, WINDOW, AS_OF, "granted").input_digest,
        )
        recent = dict(self.cases["normal"].rows[-1])
        dup_a = [
            {**recent, "reading_id": "R-1", "temperature_c": "20.00", "calibrated": "true"},
            {**recent, "reading_id": "R-2", "temperature_c": "999.00", "calibrated": "false"},
        ]
        dup_b = [
            {**recent, "reading_id": "R-1", "temperature_c": "999.00", "calibrated": "true"},
            {**recent, "reading_id": "R-2", "temperature_c": "20.00", "calibrated": "false"},
        ]
        sig_a = sa.derive_signal(home, dup_a, WINDOW, AS_OF, "granted")
        sig_b = sa.derive_signal(home, dup_b, WINDOW, AS_OF, "granted")
        self.assertNotEqual(sig_a.valid, sig_b.valid)
        self.assertNotEqual(sig_a.input_digest, sig_b.input_digest)


if __name__ == "__main__":
    unittest.main()
