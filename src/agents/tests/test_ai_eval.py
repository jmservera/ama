import copy
import json
import tempfile
import unittest
from unittest import mock

from zava_forward.agents import ai_eval
from zava_forward.core.store import Store


class AiEvalTests(unittest.TestCase):
    def scenario(self, index):
        return copy.deepcopy(json.loads(ai_eval.GOLDEN.read_text())["scenarios"][index])

    def evaluate(self, sc):
        with tempfile.TemporaryDirectory() as tmp:
            failures, measures = ai_eval.run_scenario(sc, tmp)
        return failures, measures, ai_eval.summarise([dict(name=sc["name"], measures=measures)])

    def test_golden_run_and_scenario_denominators_reconcile(self):
        report = ai_eval.run_eval()
        summary = report["summary"]
        priority = [r["measures"] for r in report["results"] if r["measures"]]
        rows = [run for m in priority for run in m["run_results"]]
        self.assertTrue(report["passed"], report["results"])
        self.assertEqual(summary["recommendation_runs"], len(rows))
        self.assertEqual(summary["recommendation_runs"], sum(m["runs"] for m in priority))
        self.assertEqual(summary["recommendation_runs"], 14)
        self.assertEqual(summary["ai_runs"], sum(r["source"] == "ai" for r in rows))
        self.assertEqual(summary["template_runs"], sum(r["source"] == "template" for r in rows))
        self.assertEqual((summary["ai_runs"], summary["template_runs"]), (8, 6))
        self.assertEqual(summary["priority_scenarios"], len(priority))
        self.assertEqual((summary["priority_scenarios"], report["scenarios"]), (10, 11))
        self.assertEqual((summary["ai_scenarios"], summary["template_scenarios"]), (4, 6))
        self.assertEqual(summary["latency_ms"]["runs"], len(rows))
        self.assertEqual(sum(summary["reviewer"]["counts"].values()), len(priority))

    def test_five_output_scenario_retains_each_returned_identity_and_latency(self):
        sc = self.scenario(-2)
        real, returned = Store.ai_priority, []

        def identified(store, user, n=5, mode=None):
            rec = real(store, user, n, mode)
            if mode != "workflow":
                i = len(returned) + 1
                rec.update(model=f"returned-model-{i}", prompt_version=f"returned-prompt-{i}", latency_ms=i * 11.5)
                returned.append(copy.deepcopy(rec))
            return rec

        with mock.patch.object(Store, "ai_priority", identified):
            failures, measures, summary = self.evaluate(sc)
        self.assertEqual(failures, [])
        rows = measures["run_results"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(len({r["recommendation_id"] for r in rows}), 5)
        for i, (row, rec) in enumerate(zip(rows, returned), 1):
            self.assertEqual(row["run"], i)
            self.assertEqual(row["recommendation_id"], rec["id"])
            for key in ("source", "model", "prompt_version"):
                self.assertEqual(row[key], rec[key])
            self.assertEqual(row["model_latency_ms"], rec["latency_ms"])
            self.assertEqual(row["latency_ms"], measures["latency_ms"][i - 1])
        self.assertEqual(measures["model_latency_ms"], [r["model_latency_ms"] for r in rows])
        self.assertEqual(summary["models"], sorted(r["model"] for r in returned))
        self.assertEqual(summary["prompt_versions"], sorted(r["prompt_version"] for r in returned))
        self.assertEqual((summary["recommendation_runs"], summary["ai_runs"]), (5, 5))
        self.assertEqual(summary["priority_scenarios"], 1)
        self.assertEqual(summary["reviewer"]["counts"], dict(accept=0, edit=1, reject=0))
        self.assertEqual(measures["review"]["reviewer"], ai_eval.OWNER["email"])
        self.assertEqual(measures["review"]["recommendation_id"], returned[-1]["id"])
        self.assertEqual(measures["review"]["reason"], sc["answer"]["reason"])

    def test_mixed_ai_and_fallback_runs_are_counted_in_both_orders(self):
        real = Store.ai_priority
        for ai_first in (True, False):
            with self.subTest(ai_first=ai_first):
                sc = self.scenario(1)
                valid = sc.pop("model_output")
                sc["model_outputs"] = [valid, "invalid JSON"] if ai_first else ["invalid JSON", valid]
                sc["expect"] = {}
                returned = []

                def identified(store, user, n=5, mode=None):
                    rec = real(store, user, n, mode)
                    if mode != "workflow":
                        rec["model"] = "actual-returned-label" if rec["source"] == "ai" else None
                        rec["prompt_version"] = f"returned-prompt-{len(returned) + 1}"
                        returned.append(copy.deepcopy(rec))
                    return rec

                with mock.patch.object(Store, "ai_priority", identified):
                    failures, measures, summary = self.evaluate(sc)
                self.assertEqual(failures, [])
                rows = measures["run_results"]
                self.assertEqual([r["source"] for r in rows], [r["source"] for r in returned])
                self.assertEqual([r["model"] for r in rows], [r["model"] for r in returned])
                self.assertEqual((summary["recommendation_runs"], summary["ai_runs"], summary["template_runs"]), (2, 1, 1))
                self.assertEqual((summary["priority_scenarios"], summary["ai_scenarios"], summary["template_scenarios"]), (1, 1, 1))
                self.assertEqual(summary["models"], ["actual-returned-label"])
                self.assertEqual(summary["prompt_versions"], ["returned-prompt-1", "returned-prompt-2"])
                self.assertEqual(measures["source"], returned[-1]["source"])
                self.assertEqual(summary["added_value"]["scenarios"], 0 if ai_first else 1)
                self.assertEqual(sum(summary["reviewer"]["counts"].values()), 1)
                self.assertEqual(measures["review"]["recommendation_id"], returned[-1]["id"])

    def test_template_only_repetitions_keep_unknown_model_and_single_review(self):
        sc = self.scenario(0)
        sc["runs"] = 3
        failures, measures, summary = self.evaluate(sc)
        self.assertEqual(failures, [])
        self.assertEqual([r["source"] for r in measures["run_results"]], ["template"] * 3)
        self.assertEqual([r["model"] for r in measures["run_results"]], [None] * 3)
        self.assertEqual((summary["recommendation_runs"], summary["ai_runs"], summary["template_runs"]), (3, 0, 3))
        self.assertEqual((summary["priority_scenarios"], summary["ai_scenarios"], summary["template_scenarios"]), (1, 0, 1))
        self.assertEqual(summary["models"], [])
        self.assertEqual(summary["latency_ms"]["runs"], 3)
        self.assertEqual(sum(summary["reviewer"]["counts"].values()), 1)

    def test_repetition_preserves_final_only_quality_scope(self):
        sc = self.scenario(-2)
        failures, measures, summary = self.evaluate(sc)
        single = copy.deepcopy(sc)
        single["model_outputs"] = [sc["model_outputs"][-1]]
        single_failures, last, last_summary = self.evaluate(single)
        self.assertEqual((failures, single_failures), ([], []))
        for key in ("overlap", "spearman", "recall"):
            self.assertEqual(measures[key], last[key])
        for key in ("mean_overlap", "mean_spearman", "added_value"):
            self.assertEqual(summary[key], last_summary[key])
        self.assertIn("final recommendation", summary["quality_scope"])
        self.assertEqual(summary["critical_misses"], 0)
        self.assertEqual(summary["citation_validity"], 1.0)

    def test_early_critical_miss_still_fails_after_valid_repetition(self):
        sc = self.scenario(1)
        valid = sc.pop("model_output")
        sc["model_outputs"] = [
            json.dumps([dict(case_id="G-1", reason="Short wait", cites=["Days in stage: 5"])]),
            valid,
        ]
        sc["expect"] = {}
        with mock.patch.object(ai_eval.ai_tasks, "critical_misses", return_value=[]):
            failures, measures, summary = self.evaluate(sc)
        self.assertTrue(any("critical miss" in f for f in failures))
        self.assertEqual(summary["critical_misses"], 1)
        self.assertEqual((measures["runs"], summary["ai_runs"]), (2, 2))
        self.assertEqual(measures["source"], "ai")

    def test_early_bad_citation_still_fails_after_valid_repetition(self):
        sc = self.scenario(1)
        valid = sc.pop("model_output")
        sc["model_outputs"] = [
            json.dumps([dict(case_id="G-3", reason="Unsupported stage", cites=["Stage: Survey booked"])]),
            valid,
        ]
        sc["expect"] = {}
        with mock.patch.object(ai_eval.ai_tasks, "resolve", return_value=True):
            failures, measures, summary = self.evaluate(sc)
        self.assertTrue(any("citation does not exist" in f for f in failures))
        self.assertLess(summary["citation_validity"], 1.0)
        self.assertEqual((measures["runs"], summary["ai_runs"]), (2, 2))

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
