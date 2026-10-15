import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

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

    def test_golden_passes_with_no_unexpected_failure(self) -> None:
        self.assertTrue(self.report["passed"], self.report["failures"])
        self.assertEqual(self.report["summary"]["failures"], 0)
        self.assertEqual(self.report["summary"]["critical_failures"], 0)

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

    def test_known_gaps_are_recorded_not_hidden(self) -> None:
        gaps = {g["id"] for g in self.report["summary"]["known_gaps"]}
        self.assertEqual(
            gaps,
            {
                "grounding-stale-answer-stays-in-history",
                "grounding-unsupported-claim-with-valid-citation",
                "injection-obeyed-in-plain-prose",
            },
        )
        recorded = [f for f in self.report["failures"] if f["severity"] == "known_gap"]
        self.assertTrue(recorded)
        self.assertTrue(all(f["scenario"] in gaps for f in recorded))

    def test_comparison_with_the_non_ai_path_is_recorded(self) -> None:
        s = self.report["summary"]
        self.assertGreater(s["answer_turns"], 0)
        self.assertEqual(s["non_ai_panel_answers"], 0)
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
            self.assertEqual(json.loads(out.read_text())["version"], GOLDEN["version"])


if __name__ == "__main__":
    unittest.main()
