import unittest
from unittest import mock

from zavaforward_mvp import ai_eval
from zavaforward_mvp.store import Store


class AiEvalTests(unittest.TestCase):
    def test_golden_scenarios_pass(self):
        rep = ai_eval.run_eval()
        self.assertGreaterEqual(rep["scenarios"], 5)
        self.assertTrue(rep["passed"], rep["results"])

    def test_harness_catches_an_ai_that_changes_ranking_or_cases(self):
        real = Store.ai_priority

        def bad(self, user, n=5):
            rec = real(self, user, n)
            top = self.cases[rec["items"][0]["case_id"]]
            top["days_in_stage"] = 1000
            self.version += 1
            return rec
        with mock.patch.object(Store, "ai_priority", bad):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        text = " ".join(f for r in rep["results"] for f in r["failures"])
        self.assertIn("ranking changed", text)
        self.assertIn("case data changed", text)

    def test_harness_catches_an_ai_that_acts_without_approval(self):
        real = Store.ai_priority

        def auto(self, user, n=5):
            rec = real(self, user, n)
            self.resolve_priority(user, rec["id"], "accept")
            return rec
        with mock.patch.object(Store, "ai_priority", auto):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertIn("Proposed", " ".join(f for r in rep["results"] for f in r["failures"]))

    def test_harness_catches_a_model_answer_that_is_not_checked(self):
        with mock.patch("zavaforward_mvp.ai.Ai.run", lambda self, task, s, u, t, strong=False, check=None:
                        dict(text='[{"case_id": "G-999", "reason": "x"}]', source="ai", model="m", validated=True, task=task)):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
