"""Consumer contract: damp scenarios for #111 signals and #133 concerns (exercise values)."""

import unittest
from datetime import timedelta
from typing import ClassVar

from zava_forward.core.synthetic import sensor_scenarios as ss

PRIORITY = {ss.INSUFFICIENT: 3, ss.REVIEW: 2, ss.NO_SIGNAL: 1}


def concern_route(resident_reported: bool, sensor_signal: str) -> str:
    """Test oracle: a sensor reading never dismisses a resident report."""
    if resident_reported:
        return "HUMAN_INVESTIGATION"
    return "SENSOR_REVIEW" if sensor_signal == ss.REVIEW else "NONE"


class DampConsumerContractTests(unittest.TestCase):
    cases: ClassVar[tuple[ss.Case, ...]]
    window: ClassVar[ss.Window]

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = tuple(c for c in ss.generate() if c.truth.family == "damp")
        cls.window = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))

    def derive(self, case: ss.Case) -> str:
        return ss.analyse(case.rows, self.window).status

    def test_each_damp_case_derives_expected_signal_from_observations_only(self) -> None:
        for case in self.cases:
            with self.subTest(case=case.truth.label):
                self.assertEqual(self.derive(case), case.truth.expected_outcome)

    def test_derivation_is_reproducible_from_retained_readings(self) -> None:
        again = {c.truth.label: self.derive(c) for c in ss.generate()}
        for case in self.cases:
            with self.subTest(case=case.truth.label):
                self.assertEqual(self.derive(case), again[case.truth.label])
                self.assertEqual(
                    ss.analyse(case.rows, self.window), ss.analyse(case.rows, self.window)
                )

    def test_missing_or_faulty_data_is_insufficient_and_never_lowers_priority(self) -> None:
        for case in self.cases:
            if case.truth.label not in {"sensor_fault", "missing_data"}:
                continue
            with self.subTest(case=case.truth.label):
                outcome = self.derive(case)
                self.assertEqual(outcome, ss.INSUFFICIENT)
                self.assertGreaterEqual(PRIORITY[outcome], PRIORITY[ss.NO_SIGNAL])

    def test_resident_report_is_never_dismissed_by_a_normal_sensor(self) -> None:
        for case in self.cases:
            with self.subTest(case=case.truth.label):
                self.assertEqual(
                    concern_route(True, self.derive(case)),
                    "HUMAN_INVESTIGATION",
                )
        normal = next(c for c in self.cases if c.truth.label == "normal")
        self.assertEqual(concern_route(False, self.derive(normal)), "NONE")


if __name__ == "__main__":
    unittest.main()
