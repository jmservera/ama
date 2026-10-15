import unittest
from unittest import mock

from zavaforward_mvp import ai_eval
from zava_forward.core.store import Store


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
        with mock.patch("zava_forward.core.ai.Ai.run", lambda self, task, s, u, t, strong=False, check=None:
                        dict(text='[{"case_id": "G-999", "reason": "x"}]', source="ai", model="m", validated=True, task=task)):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])

    def test_evidence_gate_refuses_benefit_and_records_open_items(self):
        rep = ai_eval.run_eval()
        ev = rep["evidence"]
        self.assertEqual(len(ev["golden_sha256"]), 64)
        self.assertTrue(ev["benefit_claim"].startswith("not permitted"))
        self.assertTrue(ev["actual_model_evaluation"].startswith("not evaluated"))
        self.assertTrue(ev["calibration"].startswith("not applicable"))
        self.assertTrue(any("quota" in o for o in ev["open_items"]))
        self.assertTrue(rep["prompt_version"] and "latency_ms" in rep["summary"] and rep["summary"]["reviewer"])

    def test_a_critical_miss_fails_the_run(self):
        real = ai_eval.summarise

        def missed(results):
            s = real(results)
            s["critical_misses"] = 1
            return s
        with mock.patch.object(ai_eval, "summarise", missed):
            self.assertFalse(ai_eval.run_eval()["passed"])
