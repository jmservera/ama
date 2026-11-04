"""Comparison record for the discovery assistant against non-agent methods (Refs #125)."""

import itertools
import unittest

from zava_forward.core import discovery_assistant_evaluation as dae


def results(
    measures: tuple[str, ...] = dae.MEASURE_KEYS, methods: tuple[str, ...] = dae.METHODS
) -> list[dae.MeasureResult]:
    return [
        dae.MeasureResult(m, x, f"EX-RES-{i}", "Evaluation owner")
        for i, (m, x) in enumerate(itertools.product(measures, methods))
    ]


class CompareTests(unittest.TestCase):
    def test_empty_has_nothing_comparable_and_criterion_unmet(self) -> None:
        report = dae.compare_methods([])
        self.assertEqual(report.comparable, ())
        self.assertEqual(set(report.incomplete), set(dae.MEASURE_KEYS))
        self.assertFalse(report.criterion_met)

    def test_missing_comparator_blocks_measure(self) -> None:
        for comparator in dae.COMPARATORS:
            with self.subTest(comparator=comparator):
                rows = [r for r in results() if r.method != comparator]
                report = dae.compare_methods(rows)
                self.assertEqual(report.comparable, ())
                self.assertEqual(report.incomplete["traceability"], (comparator,))

    def test_complete_never_prefers_assistant_or_approves(self) -> None:
        report = dae.compare_methods(results())
        self.assertEqual(report.comparable, dae.MEASURE_KEYS)
        self.assertFalse(report.criterion_met)
        self.assertFalse(report.assistant_preferred)
        self.assertFalse(report.approved_solution)
        self.assertIn("Manual analysis", report.manual_path)

    def test_invalid_entries_are_reported_and_not_counted(self) -> None:
        bad = [
            dae.MeasureResult("nope", "assistant", "EX-RES-1", "Owner"),
            dae.MeasureResult("traceability", "assistant", "TBD", "Owner"),
            dae.MeasureResult("traceability", "manual-analysis", "EX-RES-2", "Owner"),
            dae.MeasureResult("traceability", "manual-analysis", "EX-RES-3", "Owner"),
        ]
        report = dae.compare_methods(bad)
        self.assertEqual(len(report.invalid), 3)
        self.assertEqual(report.comparable, ())

    def test_partial_measure_reports_only_that_measure_complete(self) -> None:
        report = dae.compare_methods(results(("review-effort",)))
        self.assertEqual(report.comparable, ("review-effort",))
        self.assertNotIn("review-effort", report.incomplete)


class RepeatabilityTests(unittest.TestCase):
    def test_deterministic_calculation_is_identical(self) -> None:
        out = dae.check_repeatability(lambda d: {"days": sum(d)}, [1, 2, 3])
        self.assertTrue(out.identical)
        self.assertEqual(out.runs, 3)

    def test_non_deterministic_calculation_is_flagged(self) -> None:
        counter = itertools.count()
        out = dae.check_repeatability(lambda d: next(counter), [1])
        self.assertFalse(out.identical)

    def test_single_run_rejected(self) -> None:
        with self.assertRaises(ValueError):
            dae.check_repeatability(lambda d: d, [1], runs=1)


if __name__ == "__main__":
    unittest.main()
