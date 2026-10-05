import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from prototype.properwarm.agents import (
    AgentError, AzureModel, evidence_tools, run_agent, safe_snapshot, validate_proposal,
)
from prototype.properwarm.storage import Store

script = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_agent.py"
spec = importlib.util.spec_from_file_location("agent_evaluation", script)
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


class AgentTests(unittest.TestCase):
    def test_offline_paired_scenarios_are_labelled_and_all_pass(self):
        report = evaluation.evaluate(evaluation.ContractDouble())
        self.assertEqual(report["execution"], "offline-contract-only")
        self.assertEqual(report["contract_pass_rate"], 1)
        self.assertEqual(report["cases"], 6)

    def test_agent_does_not_modify_input_or_domain_state(self):
        case = evaluation.evaluation_cases()[0][1]
        before = copy.deepcopy(case)
        run = run_agent(case, evaluation.ContractDouble())
        self.assertEqual(run["state"], "awaiting_review")
        self.assertEqual(case, before)
        self.assertEqual(run["tool_calls"], 3)

    def test_model_write_tool_is_rejected(self):
        class WriteModel(evaluation.ContractDouble):
            def complete(self, messages, *, final):
                result = super().complete(messages, final=final)
                result["choices"][0]["message"]["tool_calls"][0]["function"]["name"] = "advance_case"
                return result
        run = run_agent(evaluation.evaluation_cases()[0][1], WriteModel())
        self.assertEqual(run["state"], "failed")
        self.assertIn("unauthorized", run["error"])
        self.assertIsNone(run["proposal"])

    def test_tool_budget_rejects_nonproductive_loop(self):
        class LoopModel(evaluation.ContractDouble):
            def complete(self, messages, *, final):
                result = super().complete(messages, final=False)
                result["choices"][0]["message"]["tool_calls"] = result["choices"][0]["message"]["tool_calls"][:1]
                return result
        run = run_agent(evaluation.evaluation_cases()[0][1], LoopModel())
        self.assertEqual(run["state"], "failed")
        self.assertIn("step limit", run["error"])

    def test_missing_safety_blocker_and_fabricated_citations_rejected(self):
        case = evaluation.evaluation_cases()[2][1]
        run = run_agent(case, evaluation.ContractDouble())
        tools = evidence_tools(safe_snapshot(case))
        proposal = copy.deepcopy(run["proposal"])
        proposal["findings"] = [item for item in proposal["findings"] if item["kind"] != "safety_hold"]
        with self.assertRaises(AgentError):
            validate_proposal(proposal, tools)
        proposal = copy.deepcopy(run["proposal"])
        proposal["findings"][0]["evidence_ids"] = ["fabricated:1"]
        with self.assertRaises(AgentError):
            validate_proposal(proposal, tools)

    def test_failure_never_returns_a_success_shaped_proposal(self):
        class DownModel(evaluation.ContractDouble):
            def complete(self, messages, *, final):
                raise AgentError("Inference unavailable.")
        run = run_agent(evaluation.evaluation_cases()[0][1], DownModel())
        self.assertEqual(run["state"], "failed")
        self.assertIsNone(run["proposal"])
        self.assertIn("unavailable", run["error"])

    def test_closed_episode_cannot_receive_a_gate_progression_finding(self):
        case = evaluation.evaluation_cases()[4][1]
        run = run_agent(case, evaluation.ContractDouble())
        proposal = copy.deepcopy(run["proposal"])
        proposal["findings"].append({
            "kind": "gate_missing", "evidence_ids": ["control:transition_gates"],
            "next_action": "Incorrect additional finding.",
        })
        with self.assertRaisesRegex(AgentError, "expected.*closed_case"):
            validate_proposal(proposal, evidence_tools(safe_snapshot(case)))

    def test_real_input_is_rejected_before_model_call(self):
        for marker in (False, "false", "true", 1, None):
            case = {**evaluation.evaluation_cases()[0][1], "is_synthetic": marker}
            with self.assertRaises(ValueError):
                run_agent(case, evaluation.ContractDouble())

    def test_endpoint_cannot_send_bearer_to_non_azure_host(self):
        for endpoint in ("http://localhost", "https://example.com", "https://a.openai.azure.com@evil.com", "https://a.openai.azure.com?secret=1"):
            with self.assertRaises(ValueError):
                AzureModel(endpoint, "model")

    def test_proposal_review_is_atomic_stale_checked_and_does_not_advance(self):
        source = Path(__file__).resolve().parents[1] / "seed" / "container-source"
        with tempfile.TemporaryDirectory() as temp:
            store = Store(Path(temp) / "test.sqlite3", source)
            case = store.get_case(store.list_cases()[0]["candidate_id"])
            run = store.save_agent_run(run_agent(case, evaluation.ContractDouble()), "Local reviewer")
            self.assertEqual(run["state"], "awaiting_review")
            store.update_threshold(4, "Local reviewer")
            with self.assertRaisesRegex(ValueError, "stale"):
                store.review_agent_run(case["candidate_id"], run["run_id"], "accepted", "Local reviewer")
            reviewed = store.review_agent_run(case["candidate_id"], run["run_id"], "rejected", "Local reviewer")
            self.assertEqual(reviewed["state"], "rejected")
            self.assertEqual(store.get_case(case["candidate_id"])["scenario_stage"], case["scenario_stage"])
            self.assertEqual(len(store.export_bundle()["agent_runs"]), 1)
            with self.assertRaisesRegex(ValueError, "unreviewed"):
                store.review_agent_run(case["candidate_id"], run["run_id"], "accepted", "Local reviewer")

    def test_started_run_is_durable_and_only_completed_once(self):
        source = Path(__file__).resolve().parents[1] / "seed" / "container-source"
        with tempfile.TemporaryDirectory() as temp:
            store = Store(Path(temp) / "test.sqlite3", source)
            case = store.get_case(store.list_cases()[0]["candidate_id"])

            def started(run):
                store.save_agent_run(run, "Local reviewer")
                persisted = store.get_case(case["candidate_id"])["agent_runs"][0]
                self.assertEqual(persisted["state"], "running")
                self.assertIsNone(persisted["proposal"])

            run = run_agent(case, evaluation.ContractDouble(), on_started=started)
            saved = store.save_agent_run(run, "Local reviewer")
            self.assertEqual(saved["state"], "awaiting_review")
            self.assertEqual(len(store.export_bundle()["agent_runs"]), 1)
            queued = next(item for item in store.list_cases() if item["candidate_id"] == case["candidate_id"])
            self.assertEqual(queued["pending_agent_reviews"], 1)
            store.review_agent_run(case["candidate_id"], run["run_id"], "accepted", "Local reviewer")
            queued = next(item for item in store.list_cases() if item["candidate_id"] == case["candidate_id"])
            self.assertEqual(queued["pending_agent_reviews"], 0)
            with self.assertRaisesRegex(ValueError, "completed once"):
                store.save_agent_run(run, "Local reviewer")


if __name__ == "__main__":
    unittest.main()
