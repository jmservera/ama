import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core import chat_panel

from zava_forward.agents import chat_eval

GOLDEN = json.loads(chat_eval.GOLDEN.read_text(encoding="utf-8"))


def run(spec: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "golden.json"
        path.write_text(json.dumps(spec), encoding="utf-8")
        return chat_eval.run_eval(path)


def scenario(sid: str) -> dict[str, Any]:
    found = next(s for s in GOLDEN["scenarios"] if s["id"] == sid)
    return copy.deepcopy(found)


class GoldenRunTests(unittest.TestCase):
    report: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = chat_eval.run_eval()

    def test_golden_run_passes_with_no_open_gap(self) -> None:
        self.assertTrue(self.report["passed"], self.report["failures"])
        self.assertEqual(self.report["summary"]["failures"], 0)
        self.assertEqual(self.report["summary"]["open_critical_gaps"], [])

    def test_unsupported_claim_with_a_valid_citation_is_withheld(self) -> None:
        result = next(
            r
            for r in self.report["results"]
            if r["id"] == "grounding-unsupported-claim-with-valid-citation"
        )
        self.assertTrue(result["passed"], result["failures"])
        self.assertIsNone(result["known_gap"])
        self.assertEqual(
            chat_panel.unsupported_claims("Funding is secured.", ["Survey booked"]),
            ["secured"],
        )
        self.assertEqual(chat_panel.unsupported_claims("Survey booked.", ["Survey booked"]), [])
        self.assertEqual(
            chat_panel.unsupported_claims("It is 12 weeks.", ["Survey booked"]), ["12"]
        )

    def test_support_matches_whole_tokens(self) -> None:
        self.assertEqual(
            chat_panel.unsupported_claims("Funding is secured.", ["Funding is unsecured."]),
            ["secured"],
        )
        self.assertEqual(
            chat_panel.unsupported_claims("It is 12 weeks.", ["It is 120 weeks."]), ["12"]
        )

    def test_signs_and_leading_decimals_are_preserved(self) -> None:
        self.assertEqual(
            chat_panel.unsupported_claims("The adjustment is £-40.5m.", ["Adjustment: £40.5m."]),
            ["-40.5m"],
        )
        self.assertEqual(
            chat_panel.unsupported_claims("The grant is £.5m.", ["Grant: £5m."]), [".5m"]
        )
        self.assertEqual(
            chat_panel.unsupported_claims("The adjustment is £-40.5m.", ["Adjustment: £-40.5m."]),
            [],
        )
        self.assertEqual(chat_panel.unsupported_claims("The grant is £.5m.", ["Grant: £.5m."]), [])

    def test_amounts_after_ellipses_are_checked(self) -> None:
        for text in (
            "The amount is\u202640m.",
            "The amount is...40m.",
            "The amount is\u2026 \u00a340m.",
        ):
            self.assertEqual(chat_panel.unsupported_claims(text, ["Survey booked"]), ["40m"], text)
        self.assertEqual(
            chat_panel.unsupported_claims("Grant...\u00a3.5m.", ["Grant: \u00a3.5m."]), []
        )

    def test_currency_codes_and_signs_before_symbols(self) -> None:
        for text in ("Funding totals GBP40m.", "Funding totals GBP40.5m.", "Funding is GBP40000."):
            self.assertTrue(chat_panel.unsupported_claims(text, ["Survey booked"]), text)
        self.assertEqual(
            chat_panel.unsupported_claims("The adjustment is -£40.5m.", ["Adjustment: £40.5m."]),
            ["-40.5m"],
        )
        self.assertEqual(
            chat_panel.unsupported_claims("The adjustment is -£40.5m.", ["Adjustment: -£40.5m."]),
            [],
        )

    def test_numeric_forms_are_tokenised_completely(self) -> None:
        for text, token in (
            ("It costs £40m.", "40m"),
            ("About 12k homes.", "12k"),
            ("Area is 12m2.", "12m2"),
            ("It is £1e6.", "1e6"),
            ("It is £40.5m.", "40.5m"),
        ):
            self.assertEqual(chat_panel.unsupported_claims(text, ["40 homes"]), [token], text)
        self.assertEqual(chat_panel.unsupported_claims("It is 40 homes.", ["40 homes"]), [])

    def test_grounding_guard_changes_policy_version(self) -> None:
        raw = b"{}"
        before = chat_eval.bindings(raw)["policy_version"]
        with patch.object(chat_panel, "UNGROUNDED", "changed"):
            self.assertNotEqual(before, chat_eval.bindings(raw)["policy_version"])

    def test_scenarios_are_multi_turn_and_cover_every_required_area(self) -> None:
        cats = {r["category"] for r in self.report["results"]}
        self.assertEqual(
            cats,
            {"grounding", "permission", "out-of-scope", "prompt-injection", "memory-poisoning"},
        )
        multi = [r for r in self.report["results"] if r["turns"] >= 2]
        self.assertGreaterEqual(len(multi), 15)
        ids = {r["id"] for r in self.report["results"]}
        for needle in ("abstain", "conflicting", "source-changes", "role-and-staff-revoked"):
            self.assertTrue(any(needle in i for i in ids), needle)

    def test_each_out_of_scope_ask_is_refused_with_a_route_and_no_model_call(self) -> None:
        kinds = set()
        for sc in GOLDEN["scenarios"]:
            for turn in sc["turns"]:
                if turn.get("expect", {}).get("kind") == "refused":
                    self.assertIs(turn["expect"]["model_called"], False)
                    kinds.add(sc["id"])
        self.assertTrue(kinds >= {i for i in kinds if i.startswith("out-of-scope")})
        self.assertGreaterEqual(len(kinds), 4)

    def test_stale_history_and_lexical_action_claim_scenarios_really_pass(self) -> None:
        for sid in (
            "grounding-stale-answer-stays-in-history",
            "injection-obeyed-in-plain-prose",
        ):
            result = next(r for r in self.report["results"] if r["id"] == sid)
            self.assertTrue(result["passed"], result["failures"])
            self.assertIsNone(result["known_gap"])

    def test_all_assistant_turns_are_excluded_but_user_questions_remain(self) -> None:
        sc = scenario("grounding-cited-follow-ups")
        sc["turns"][1]["expect"]["prompt_forbid"] = ["assistant:", "The stage is Survey booked."]
        report = run(dict(version="t", scenarios=[sc]))
        self.assertTrue(report["passed"], report["failures"])

    def test_comparison_with_the_non_ai_path_is_recorded(self) -> None:
        s = self.report["summary"]
        self.assertGreater(s["answer_turns"], 0)
        # Stored threads fall back to the rules-based case answer when AI is unavailable (#749).
        self.assertGreater(s["non_ai_panel_answers"], 0)
        self.assertEqual(s["card_could_answer"], s["answer_turns"])
        self.assertIn("not permitted", self.report["evidence"]["benefit_claim"])

    def test_report_binds_versions_and_states_what_is_not_evaluated(self) -> None:
        b = self.report["bindings"]
        for key in ("golden_sha256", "prompt_version", "policy_version", "source_version"):
            self.assertTrue(b[key])
        self.assertIn("not evaluated", self.report["evidence"]["actual_model_evaluation"])
        self.assertIn("not evaluated", self.report["evidence"]["human_effectiveness"])
        self.assertIn("not produced", self.report["evidence"]["held_out"])
        self.assertEqual(self.report, chat_eval.run_eval())

    def test_enablement_is_never_granted_by_this_evidence(self) -> None:
        e = self.report["enablement"]
        self.assertEqual(
            (e["outcome"], e["state"], e["thresholds"]),
            ("insufficient", "disabled", "not approved"),
        )
        self.assertIn("approved thresholds", e["missing_evidence"])
        approved = chat_eval.enablement_decision(self.report, dict(approved_by="someone"))
        self.assertEqual((approved["outcome"], approved["state"]), ("insufficient", "disabled"))
        self.assertEqual(e["blocking_gaps"], [])

    def test_chat_task_is_registered_disabled_with_reviewer_and_unapproved_thresholds(self) -> None:
        from zava_forward.core import ai_registry

        t = ai_registry.get(chat_eval.TASK)
        assert t is not None
        self.assertEqual((t["enabled"], t["state"]), (False, "disabled"))
        self.assertEqual(t["accountable_function"], "Retrofit Programme Manager")
        self.assertEqual(t["accountable_individual"], ai_registry.UNKNOWN)
        self.assertEqual(t["thresholds"]["status"], "proposed")
        self.assertIsNone(t["thresholds"]["approved_by"])
        self.assertFalse(ai_registry.authorizes_live(chat_eval.TASK))
        e = self.report["enablement"]
        self.assertTrue(e["registered"])
        self.assertEqual(e["accountable_function"], t["accountable_function"])

    def test_per_category_gates_are_explicit_and_insufficient_when_absent(self) -> None:
        gates = {g["category"]: g for g in self.report["enablement"]["gates"]}
        self.assertEqual(
            set(gates), {"prompt-injection", "memory-poisoning", "permission", "out-of-scope"}
        )
        for g in gates.values():
            self.assertGreater(g["scenarios"], 0)
        report = run(dict(version="t", scenarios=[scenario("grounding-cited-follow-ups")]))
        absent = {g["category"]: g["outcome"] for g in report["enablement"]["gates"]}
        self.assertEqual(set(absent.values()), {"insufficient"})
        self.assertEqual(report["enablement"]["outcome"], "insufficient")

    def test_a_failing_injection_gate_fails_enablement(self) -> None:
        report = copy.deepcopy(self.report)
        report["summary"]["open_critical_gaps"] = []
        report["summary"]["critical_failures"] = 0
        report["passed"] = True
        report["summary"]["by_category"]["prompt-injection"]["passed"] = 0
        e = chat_eval.enablement_decision(report, dict(approved_by="someone"))
        self.assertEqual((e["outcome"], e["state"]), ("fail", "disabled"))

    def test_open_critical_gaps_block_even_if_aggregate_success_is_inconsistent(self) -> None:
        report = copy.deepcopy(self.report)
        report["summary"]["open_critical_gaps"] = [dict(id="x", category="grounding", gap="g")]
        result = chat_eval.enablement_decision(report, dict(approved_by="someone"))
        self.assertEqual(result["outcome"], "fail")
        self.assertTrue(result["blocking_gaps"])

    def test_gap_free_development_evidence_remains_insufficient(self) -> None:
        report = run(dict(version="t", scenarios=[scenario("grounding-cited-follow-ups")]))
        self.assertTrue(report["passed"])
        self.assertEqual(report["enablement"]["outcome"], "insufficient")
        self.assertEqual(report["enablement"]["blocking_gaps"], [])

    def test_consumption_is_reported_per_turn_scenario_and_runtime_answer(self) -> None:
        summary = self.report["summary"]["economics"]
        self.assertEqual(summary["actual_model_calls"], 0)
        self.assertIsNone(summary["tokens"])
        self.assertEqual(summary["cost"], "Unknown")
        calls = 0
        for result in self.report["results"]:
            calls += result["economics"]["scripted_calls"]
            for receipt in result["consumption"]:
                self.assertIn(receipt["model_calls"], (0, 1))
                self.assertFalse(receipt["memory_used"])
                self.assertNotIn("Question", json.dumps(receipt))
        self.assertEqual(calls, summary["scripted_calls"])
        self.assertGreater(summary["calls_per_runtime_accepted_answer"], 0)
        self.assertIsNone(summary["human_accepted_answers"])


class NegativeControlTests(unittest.TestCase):
    """Break one property at a time and expect the harness to notice."""

    def failing(self, sc: dict[str, Any], check: str) -> None:
        report = run(dict(version="t", scenarios=[sc]))
        self.assertFalse(report["passed"])
        self.assertIn(check, {f["check"] for f in report["failures"]})
        self.assertEqual(report["enablement"]["outcome"], "fail")

    def test_wrong_expected_kind_is_a_failure(self) -> None:
        sc = scenario("grounding-cited-follow-ups")
        sc["turns"][0]["expect"]["kind"] = "abstain"
        self.failing(sc, "kind")

    def test_uncited_model_reply_that_is_expected_to_answer_is_a_failure(self) -> None:
        sc = scenario("grounding-cited-follow-ups")
        sc["turns"][0]["script"]["citations"] = []
        self.failing(sc, "kind")

    def test_a_refusal_that_calls_the_model_is_a_failure(self) -> None:
        sc = scenario("out-of-scope-approve")
        sc["turns"][0]["say"] = "What stage is it?"
        self.failing(sc, "model_called")

    def test_leaked_reason_in_the_prompt_is_a_failure(self) -> None:
        sc = scenario("permission-reason-access-lost-mid-thread")
        sc["turns"][1]["before"] = []
        self.failing(sc, "prompt_forbid")

    def test_a_closed_known_gap_must_be_unmarked(self) -> None:
        sc = scenario("grounding-cited-follow-ups")
        sc["known_gap"] = "claimed open"
        report = run(dict(version="t", scenarios=[sc]))
        self.assertFalse(report["passed"])
        self.assertEqual(report["failures"][0]["check"], "known_gap_closed")

    def test_each_critical_category_gap_is_a_failure_and_an_explicit_blocker(self) -> None:
        for category in chat_eval.CRITICAL_CATEGORIES:
            with self.subTest(category=category):
                sc = scenario("grounding-cited-follow-ups")
                sc["category"] = category
                sc["known_gap"] = "seeded critical miss"
                sc["turns"][0]["expect"]["kind"] = "withheld"
                report = run(dict(version="t", scenarios=[sc]))
                self.assertFalse(report["passed"])
                self.assertGreater(report["summary"]["critical_failures"], 0)
                self.assertEqual(report["summary"]["by_category"][category]["passed"], 0)
                self.assertEqual(report["enablement"]["outcome"], "fail")
                self.assertEqual(report["enablement"]["blocking_gaps"][0]["id"], sc["id"])

    def test_unexpected_exception_is_a_failure(self) -> None:
        sc = scenario("grounding-cited-follow-ups")
        sc["turns"][0]["before"] = [dict(op="no-such-op")]
        self.failing(sc, "unexpected")

    def test_memory_that_should_be_rejected_but_is_stored_is_a_failure(self) -> None:
        sc = scenario("memory-special-category-rejected")
        sc["turns"][0]["before"][0]["content"] = "Prefers short bullet summaries"
        self.failing(sc, "memory_rejected")


class CliTests(unittest.TestCase):
    def test_record_writes_the_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(chat_eval.main(["--record", str(out)]), 0)
            report = json.loads(out.read_text())
            self.assertEqual(report["version"], GOLDEN["version"])
            self.assertTrue(report["passed"])
            self.assertFalse(report["summary"]["open_critical_gaps"])

    def test_json_cli_passes_but_enablement_stays_insufficient(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(chat_eval.main(["--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["enablement"]["outcome"], "insufficient")

    def test_plain_cli_reports_no_open_gap_and_disabled_task(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(chat_eval.main([]), 0)
        self.assertNotIn("open critical gap", output.getvalue())
        self.assertIn("enablement: insufficient (task disabled)", output.getvalue())

    def test_gap_free_cli_returns_zero_but_never_enables(self) -> None:
        report = run(dict(version="t", scenarios=[scenario("grounding-cited-follow-ups")]))
        with patch.object(chat_eval, "run_eval", return_value=report):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(chat_eval.main(["--json"]), 0)
        self.assertEqual(report["enablement"]["state"], "disabled")


if __name__ == "__main__":
    unittest.main()
