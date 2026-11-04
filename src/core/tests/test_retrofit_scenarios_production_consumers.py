"""Retrofit exercise scenarios through the production #111 and #133 code (Refs #193).

Exercise values only. Unlike test_retrofit_scenario_consumers, which uses test-local oracles,
this drives sensor_analysis.derive_signal (#111) and AftercareRegister (#133) directly.
"""

import unittest
from datetime import timedelta
from typing import Any, ClassVar, cast

from zava_forward.core import sensor_analysis as sa
from zava_forward.core.aftercare import AftercareRegister
from zava_forward.core.synthetic import sensor_scenarios as ss

OWNER = "Aftercare Lead"
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))


def rows_of(scenario: dict[str, Any]) -> list[dict[str, str]]:
    return cast(list[dict[str, str]], scenario["rows"])


def home_of(scenario: dict[str, Any]) -> str:
    return str(scenario["rows"][0]["home_id"])


class RetrofitScenarioSensorSignalTests(unittest.TestCase):
    scenarios: ClassVar[tuple[dict[str, Any], ...]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = tuple(ss.retrofit_exercise_scenarios())

    def test_every_scenario_yields_a_labelled_signal_without_priority_effect(self) -> None:
        self.assertEqual(len(self.scenarios), 4)
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                signal = sa.derive_signal(home_of(s), rows_of(s), WINDOW, WINDOW.end, "granted")
                self.assertEqual(signal.sufficiency, sa.SUFFICIENT)
                self.assertTrue(signal.threshold_label.startswith("EXERCISE VALUE"))
                self.assertEqual(signal.priority_effect, "NONE")
                self.assertFalse(signal.diagnoses_hazard)
                self.assertEqual(s["value_status"], ss.EXERCISE_LABEL)
                self.assertIsNone(sa.review_task_candidate(signal))

    def test_signal_ignores_expected_labels_and_is_reproducible(self) -> None:
        for s, again in zip(self.scenarios, ss.retrofit_exercise_scenarios(), strict=True):
            with self.subTest(case=s["label"]):
                first = sa.derive_signal(home_of(s), rows_of(s), WINDOW, WINDOW.end, "granted")
                second = sa.derive_signal(home_of(s), rows_of(again), WINDOW, WINDOW.end, "granted")
                self.assertEqual(first, second)
                self.assertNotIn(str(s["expected_direction"]), repr(first))

    def test_missing_consent_and_truncated_readings_fail_closed(self) -> None:
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                for consent in ("declined", "unknown"):
                    signal = sa.derive_signal(home_of(s), rows_of(s), WINDOW, WINDOW.end, consent)
                    self.assertEqual(signal.outcome, sa.INSUFFICIENT)
                    self.assertEqual(signal.priority_effect, "NONE")
                short = sa.derive_signal(
                    home_of(s), rows_of(s)[: 24 * 2], WINDOW, WINDOW.end, "granted"
                )
                self.assertNotEqual(short.sufficiency, sa.SUFFICIENT)
                self.assertEqual(short.priority_effect, "NONE")


class RetrofitScenarioAftercareTests(unittest.TestCase):
    def test_scenario_context_never_dismisses_a_household_concern(self) -> None:
        reg = AftercareRegister()
        homes = []
        for s in ss.retrofit_exercise_scenarios():
            home = home_of(s)
            homes.append(home)
            signal = sa.derive_signal(home, rows_of(s), WINDOW, WINDOW.end, "granted")
            cid = str(
                reg.raise_concern(
                    "digital",
                    "household",
                    home,
                    "discomfort",
                    "The living room stays cold in the evening.",
                    OWNER,
                    "2026-12-01",
                    sensor_context={"signal": signal.outcome, "label": signal.threshold_label},
                )["id"]
            )
            with self.subTest(case=s["label"]):
                rec = reg.concerns[cid]
                self.assertFalse(rec["dismissed_by_sensor"])
                self.assertEqual(rec["investigation"], "received")
                self.assertIn(cid, [r["id"] for r in reg.unresolved(home)])
                self.assertNotIn("sensor_context", reg.view(cid))
        view = reg.evaluator_view(homes)
        self.assertEqual(view["concerns_raised"], 4)
        self.assertEqual(view["concerns_by_outcome"]["no_outcome_yet"], 4)
        self.assertIn("Baseline coverage is unknown.", view["unknowns"])

    def test_evaluator_view_states_baseline_denominator_for_scenario_homes(self) -> None:
        scenarios = ss.retrofit_exercise_scenarios()
        homes = [home_of(s) for s in scenarios]
        view = AftercareRegister().evaluator_view(homes, baseline_homes=homes[:3])
        self.assertEqual(view["homes_handed_over"], 4)
        self.assertEqual(view["homes_baseline_unknown"], 1)
        self.assertNotIn("Baseline coverage is unknown.", view["unknowns"])
        self.assertIn("not a promise of savings", str(view["notice"]).lower())


if __name__ == "__main__":
    unittest.main()
