import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from zava_forward.agents import chat_eval

GOLDEN: dict[str, Any] = json.loads(chat_eval.GOLDEN.read_text(encoding="utf-8"))


def run(spec: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "golden.json"
        path.write_text(json.dumps(spec), encoding="utf-8")
        report: dict[str, Any] = chat_eval.run_eval(path)
        return report


def without(*ids: str) -> dict[str, Any]:
    spec: dict[str, Any] = copy.deepcopy(GOLDEN)
    spec["scenarios"] = [s for s in spec["scenarios"] if s["id"] not in ids]
    return spec


class RevocationAndConsentCoverageTests(unittest.TestCase):
    report: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = chat_eval.run_eval()

    def test_required_scenarios_exist_and_pass(self) -> None:
        chat = self.report["summary"]["chat_specific"]
        for key, required in (
            ("revocation_no_retained_authority", chat_eval.REVOCATION_SCENARIOS),
            ("no_manufactured_approval_or_consent", chat_eval.NO_MANUFACTURED_APPROVAL_SCENARIOS),
        ):
            with self.subTest(key):
                self.assertEqual(chat[key]["required"], list(required))
                self.assertEqual(chat[key]["missing"], [])
                self.assertEqual(chat[key]["failing"], [])
                self.assertTrue(chat[key]["passed"])

    def test_revocation_scenarios_withdraw_authority_mid_thread(self) -> None:
        for sid in chat_eval.REVOCATION_SCENARIOS:
            sc = next(s for s in GOLDEN["scenarios"] if s["id"] == sid)
            with self.subTest(sid):
                self.assertGreaterEqual(len(sc["turns"]), 2)
                self.assertTrue(
                    any(
                        {"prompt_forbid", "cited_forbid", "forbid", "isolation_forbid"}
                        & set(t.get("expect", {}))
                        or t.get("expect", {}).get("kind") in ("abstain", "refused", "withheld")
                        or t.get("expect", {}).get("error")
                        for t in sc["turns"][1:]
                    )
                )

    def test_missing_required_scenario_is_a_gap_never_a_pass(self) -> None:
        report = run(without("permission-case-removed-mid-thread"))
        chat = report["summary"]["chat_specific"]["revocation_no_retained_authority"]
        self.assertEqual(chat["missing"], ["permission-case-removed-mid-thread"])
        self.assertFalse(chat["passed"])
        self.assertIn(
            "complete revocation no retained authority scenario coverage",
            report["enablement"]["missing_evidence"],
        )
        self.assertNotEqual(report["enablement"]["outcome"], "pass")

    def test_failing_revocation_scenario_fails_enablement(self) -> None:
        spec = copy.deepcopy(GOLDEN)
        sc = next(s for s in spec["scenarios"] if s["id"] == chat_eval.REVOCATION_SCENARIOS[0])
        sc["turns"][-1]["expect"]["model_called"] = True
        report = run(spec)
        chat = report["summary"]["chat_specific"]["revocation_no_retained_authority"]
        self.assertEqual(chat["failing"], [chat_eval.REVOCATION_SCENARIOS[0]])
        self.assertFalse(chat["passed"])
        self.assertEqual(report["enablement"]["outcome"], "fail")

    def test_failing_consent_scenario_fails_enablement(self) -> None:
        sid = chat_eval.NO_MANUFACTURED_APPROVAL_SCENARIOS[0]
        spec = copy.deepcopy(GOLDEN)
        sc = next(s for s in spec["scenarios"] if s["id"] == sid)
        sc["turns"][-1]["expect"]["kind"] = "answer"
        report = run(spec)
        chat = report["summary"]["chat_specific"]["no_manufactured_approval_or_consent"]
        self.assertEqual(chat["failing"], [sid])
        self.assertEqual(report["enablement"]["outcome"], "fail")

    def test_authority_check_fails_closed_only_on_failures(self) -> None:
        self.assertTrue(chat_eval.authority_requirements_met({}))
        failing = dict(chat_specific=dict(revocation_no_retained_authority=dict(failing=["x"])))
        self.assertFalse(chat_eval.authority_requirements_met(failing))

    def test_golden_run_still_never_enables(self) -> None:
        self.assertEqual(self.report["enablement"]["state"], "disabled")
        self.assertEqual(self.report["enablement"]["outcome"], "insufficient")


class SeparateReportingTests(unittest.TestCase):
    report: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = chat_eval.run_eval()

    def test_chat_failures_are_counted_apart_from_single_turn_results(self) -> None:
        chat = self.report["summary"]["chat_specific"]
        self.assertIn("single-turn task results are reported by ai_eval", chat["scope"])
        self.assertEqual(chat["failures"], self.report["summary"]["failures"])
        self.assertEqual(sum(chat["failures_by_category"].values()), chat["failures"])
        self.assertEqual(set(chat["failures_by_category"]), set(chat_eval.CRITICAL_CATEGORIES))

    def test_chat_failures_are_attributed_to_their_category(self) -> None:
        sid = "out-of-scope-approve"
        spec = copy.deepcopy(GOLDEN)
        sc = next(s for s in spec["scenarios"] if s["id"] == sid)
        sc["turns"][-1]["expect"]["kind"] = "answer"
        chat = run(spec)["summary"]["chat_specific"]
        self.assertGreater(chat["failures_by_category"]["out-of-scope"], 0)
        self.assertEqual(chat["failures_by_category"]["permission"], 0)
        self.assertEqual(chat["failures"], sum(chat["failures_by_category"].values()))

    def test_review_effort_is_complete_unmeasured_and_makes_no_saving_claim(self) -> None:
        effort = self.report["summary"]["review_effort"]
        self.assertEqual(effort["status"], "not measured")
        self.assertIsNone(effort["minutes"])
        self.assertEqual(effort["missing_inputs"], list(chat_eval.REVIEW_EFFORT_INPUTS))
        self.assertIn("non-AI", effort["comparator"])
        self.assertIn("not permitted", effort["saving_claim"])

    def test_review_workload_counts_come_from_scripted_outcomes(self) -> None:
        rows = [o for r in self.report["results"] for o in r["outcomes"]]
        effort = self.report["summary"]["review_effort"]
        self.assertEqual(
            effort["reviewable_answer_turns"], sum(o["expected"] == "answer" for o in rows)
        )
        self.assertGreater(effort["reviewable_answer_turns"], 0)
        self.assertGreater(effort["withheld_or_refused_turns"], 0)

    def test_effort_is_not_folded_into_economics_or_failures(self) -> None:
        summary = self.report["summary"]
        self.assertNotIn("review_effort", summary["economics"])
        self.assertIn("complete human review effort", summary["economics"]["missing_cost_inputs"])
        self.assertNotIn("review_effort", summary["chat_specific"])

    def test_empty_results_give_no_rates_or_effort(self) -> None:
        effort = chat_eval.review_effort([])
        self.assertEqual(effort["reviewable_answer_turns"], 0)
        self.assertIsNone(effort["minutes"])
        chat = chat_eval.chat_specific([])
        self.assertEqual(chat["failures"], 0)
        self.assertFalse(chat["revocation_no_retained_authority"]["passed"])


if __name__ == "__main__":
    unittest.main()
