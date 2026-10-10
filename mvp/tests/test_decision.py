"""Fake-only contract tests; no provider calls, resources or live acceptance."""

from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from hashlib import sha256
import json
import math
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import uuid
import unittest
import urllib.error
from unittest.mock import patch

from properwarm_mvp.decision import (
    API_PATH, DecisionClient, DecisionConfig, InferenceConfig, InferenceGuard, NO_MATCH,
    PROTECTED_FIELDS, inference_allowed, inference_guard, load_registry, reserve_inference_charge,
)


TASK = "form_candidate_selection"
PERMISSIONS = ("evidence.read", "forms.assist")
ENDPOINT = "https://fictional.services.ai.azure.com"
CONFIG = DecisionConfig(
    endpoint=ENDPOINT, deployment="exercise-decision", metadata_reviewed=True,
    metadata_endpoint=ENDPOINT, metadata_deployment="exercise-decision",
    metadata_model="microsoft-decision-1", metadata_model_version="1",
    deployment_type="DataZoneStandard", region="fictional-test-region",
)
INFERENCE = InferenceConfig(
    authorized=True, access_reviewed=True, terms_reviewed=True,
    cost_reviewed=True, quota_reviewed=True, price_known=True,
    spend_paused=False, enabled_tasks=(TASK, "evidence_support"),
    accrued_usd=100.0, max_call_charge_usd=0.01,
)
TEXT = "EPC band C. Alternative report: EPC band D."
SOURCES = [{
    "id": "epc-1", "case_id": "EX-1", "version": "2",
    "hash": sha256(TEXT.encode()).hexdigest(), "locator": "line:1",
    "kind": "form_evidence", "text": TEXT,
}]
CANDIDATES = [
    {"id": "candidate-c", "source_id": "epc-1", "text": "EPC band C"},
    {"id": "candidate-d", "source_id": "epc-1", "text": "EPC band D"},
]


def choice_payload(
    choice: str = "candidate-c", probabilities: dict[str, float] | None = None,
) -> dict:
    return {
        "model": "microsoft-decision-1",
        "usage": {"input_tokens": 32, "output_tokens": 4, "total_tokens": 36},
        "answers": {"candidate": {
            "type": "choice", "choice": choice,
            "probabilities": probabilities if probabilities is not None else {
                "candidate-c": 0.94, "candidate-d": 0.04, NO_MATCH: 0.02,
            },
        }},
    }


def support_payload(probability: float = 0.97) -> dict:
    return {
        "model": "microsoft-decision-1", "usage": {"tokens": 35},
        "answers": {"evidence_supported": {"type": "noul", "probability": probability}},
    }


class DecisionTests(unittest.TestCase):
    def test_shared_liability_reservations_survive_processes_and_provider_failures(self):
        root = Path.cwd() / ".exercise-test-state" / uuid.uuid4().hex
        root.mkdir(parents=True)
        try:
            first = reserve_inference_charge(TASK, replace(INFERENCE, accrued_usd=400, max_call_charge_usd=2),
                                             str(root))
            self.assertTrue(first["allowed"])
            self.assertEqual(first["projected_usd"], 402)
            program = """
import json,sys
from properwarm_mvp.decision import InferenceConfig,reserve_inference_charge
config=InferenceConfig(accrued_usd=400,max_call_charge_usd=2)
print(json.dumps(reserve_inference_charge('source_narrative',config,sys.argv[1])))
"""
            child = subprocess.run([sys.executable, "-c", program, str(root)], check=True,
                                   capture_output=True, text=True, timeout=15)
            self.assertEqual(json.loads(child.stdout)["projected_usd"], 404)
            third = reserve_inference_charge(TASK, replace(INFERENCE, accrued_usd=0, max_call_charge_usd=1),
                                             str(root))
            self.assertFalse(third["allowed"], "A different process/provider cannot lower the recorded baseline.")
            self.assertEqual(third["projected_usd"], 405)
            with sqlite3.connect(root / "inference-liabilities.sqlite") as db:
                self.assertEqual(db.execute("SELECT SUM(amount) FROM reservations").fetchone()[0], 4_000_000)
        finally:
            shutil.rmtree(root)
            try:
                root.parent.rmdir()
            except OSError:
                pass

    def test_shared_ledger_denial_prevents_scoring_transport(self):
        with patch.dict("os.environ", {"PW_EXERCISE": "1", "PW_STATE": ""}, clear=True):
            client = self.client()
            with patch.object(client, "transport", side_effect=AssertionError("No billable call")):
                result = self.propose(client)
            self.assertEqual(result["status"], "disabled")
            self.assertEqual(result["reason"], "shared_liability_ledger_unavailable")

    def test_concurrent_liability_reservations_cannot_overrun_pause(self):
        root = Path.cwd() / ".exercise-test-state" / uuid.uuid4().hex
        root.mkdir(parents=True)
        try:
            config = replace(INFERENCE, accrued_usd=400, max_call_charge_usd=1)
            with ThreadPoolExecutor(max_workers=20) as pool:
                outcomes = list(pool.map(lambda _: reserve_inference_charge(TASK, config, str(root)), range(20)))
            self.assertEqual(sum(result["allowed"] for result in outcomes), 4)
            self.assertTrue(all(result["projected_usd"] < 405 for result in outcomes if result["allowed"]))
            self.assertTrue(all(result["reason"] == "shared_liability_pause" for result in outcomes if not result["allowed"]))
            with sqlite3.connect(root / "inference-liabilities.sqlite") as db:
                self.assertEqual(db.execute("SELECT SUM(amount) FROM reservations").fetchone()[0], 4_000_000)
        finally:
            shutil.rmtree(root)

    def test_shared_ledger_denial_prevents_generating_or_reading_transport(self):
        from properwarm_mvp.ai import Ai
        with patch.dict("os.environ", {"PW_EXERCISE": "1", "PW_STATE": "", "AI_ENDPOINT": ENDPOINT}, clear=True):
            ai = Ai()
            with patch.object(ai, "_exercise_guard", return_value=InferenceGuard(True, "authorized")), \
                 patch("properwarm_mvp.ai.InferenceConfig.from_env", return_value=INFERENCE), \
                 patch.object(ai, "_chat", side_effect=AssertionError("No billable call")) as chat:
                generated = ai.run("source_bound_narrative", "System", "Fictional facts", "Manual review")
                read = ai.look_at("fictional.txt", b"EPC: C", "text/plain")
            self.assertFalse(generated["provider_success"])
            self.assertIn("shared_liability_ledger_unavailable", generated["reason"])
            self.assertFalse(read["provider_success"])
            self.assertEqual(read["reason"], "shared_liability_ledger_unavailable")
            chat.assert_not_called()

    def test_provider_catalog_model_casing_preserves_exact_model_identity(self):
        result = self.propose(self.client(config=replace(CONFIG, metadata_model="Microsoft-Decision-1")))
        self.assertEqual(result["status"], "proposed")
        wrong = self.propose(self.client(config=replace(CONFIG, metadata_model="Microsoft-Decision-2")))
        self.assertEqual(wrong["reason"], "deployment_metadata_unverified")

    def setUp(self) -> None:
        self.calls: list[tuple] = []
        self.tokens: list[bool] = []
        self.payload = choice_payload()
        self.error: Exception | None = None
        self.tick = 0

    def transport(self, request, timeout):
        self.calls.append((request, timeout))
        if self.error:
            raise self.error
        return self.payload

    def token(self) -> str:
        self.tokens.append(True)
        return "fake-test-only-token"

    def clock(self) -> float:
        self.tick += 1
        return self.tick * 0.125

    def client(self, **kwargs) -> DecisionClient:
        return DecisionClient(
            kwargs.pop("config", CONFIG),
            inference=kwargs.pop("inference", INFERENCE),
            transport=self.transport, token=self.token, clock=self.clock, **kwargs,
        )

    def propose(self, client=None, **kwargs):
        params = {
            "case_id": "EX-1", "case_version": "5", "sources": deepcopy(SOURCES),
            "candidates": deepcopy(CANDIDATES), "permissions": PERMISSIONS,
            "field": "epc_band", "workflow": "funding-forms",
        }
        params.update(kwargs)
        task = params.pop("task", TASK)
        return (client or self.client()).propose(task, **params)

    def guard(self, **kwargs):
        params = {
            "config": INFERENCE, "permissions": PERMISSIONS, "source_kinds": ["form_evidence"],
            "source_count": 1, "text_chars": 100, "field": "epc_band", "workflow": "funding-forms",
        }
        params.update(kwargs)
        task = params.pop("task", TASK)
        capability = params.pop("capability", "decision-scoring")
        return inference_guard(task, capability, **params)

    def test_registry_defaults_versions_reviewers_and_thresholds(self):
        registry = load_registry()
        self.assertEqual(registry["version"], "2026-10-10.1")
        for task in registry["tasks"].values():
            self.assertIs(task["approved"], True)
            self.assertIs(task["enabled"], False)
            for key in ("version", "question_version", "instructions", "reviewer", "permissions",
                        "field_scope", "workflow_scope", "source_kinds", "fallback"):
                self.assertTrue(task[key])
        self.assertEqual(registry["tasks"][TASK]["probability_threshold"], 0.9)
        self.assertEqual(registry["tasks"]["evidence_support"]["probability_threshold"], 0.95)
        self.assertEqual(registry["tasks"][TASK]["margin_threshold"], 0.2)

    def test_malformed_reviewed_registry_denied_by_shared_guard(self):
        for key, value in (
            ("version", None), ("reviewer", True), ("permissions", []),
            ("source_kinds", "form_evidence"), ("max_sources", True),
            ("question_version", ""), ("probability_threshold", math.nan),
            ("margin_threshold", 0), ("enabled", "true"), ("question_type", "score"),
        ):
            registry = load_registry()
            registry["tasks"][TASK][key] = value
            self.assertEqual(self.guard(registry=registry).reason, "invalid_registry")
        self.assertEqual(self.calls, [])

    def test_exact_public_request_and_unapproved_provenance(self):
        result = self.propose()
        request, timeout = self.calls[0]
        body = json.loads(request.data)
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.full_url, ENDPOINT + API_PATH)
        self.assertEqual(request.get_header("Authorization"), "Bearer fake-test-only-token")
        self.assertEqual(timeout, 30)
        self.assertEqual(set(body), {"model", "state", "questions"})
        self.assertEqual(body["model"], "exercise-decision")
        self.assertEqual(set(body["questions"]), {"candidate"})
        question = body["questions"]["candidate"]
        self.assertEqual(set(question), {"type", "instructions", "criteria"})
        self.assertEqual(question["type"], "choice")
        self.assertEqual(set(question["criteria"]), {"candidate-c", "candidate-d", NO_MATCH})
        self.assertEqual(body["state"]["evidence"], [{"source_id": "epc-1", "text": TEXT}])
        self.assertNotIn("resident", body["state"])
        self.assertNotIn("EX-1", json.dumps(body))
        self.assertEqual(result["status"], "proposed")
        self.assertEqual(result["approval"], "Not reviewed")
        self.assertIs(result["validated"], True)
        self.assertEqual(result["selected_candidate"], "candidate-c")
        self.assertEqual(result["probabilities"], self.payload["answers"]["candidate"]["probabilities"])
        self.assertAlmostEqual(result["margin"], 0.9)
        self.assertEqual(result["latency_ms"], 125)
        self.assertEqual(result["task_version"], "1")
        self.assertEqual(result["case_version"], "5")
        self.assertEqual(result["sources"][0]["version"], "2")
        self.assertNotIn("text", result["sources"][0])
        self.assertEqual(result["model"], "microsoft-decision-1")
        self.assertEqual(result["model_version"], "1")
        self.assertEqual(result["model_version_source"], "reviewed_deployment_metadata")
        self.assertIsNone(result["returned_model_version"])
        self.assertEqual(result["usage"], self.payload["usage"])
        self.assertEqual(result["deployment"], "exercise-decision")
        self.assertEqual(result["reserved_upper_charge_usd"], 0.01)
        self.assertIsNone(result["actual_charge_usd"])
        for key in ("input_hash", "request_hash", "source_hash", "question_hash", "prompt_hash"):
            self.assertEqual(len(result[key]), 64)
        self.assertIn("not a model rationale", result["explanation"])
        self.assertNotIn("fake-test-only-token", json.dumps(result))

    def test_hashes_bind_source_versions_case_and_question(self):
        first = self.propose()
        sources = deepcopy(SOURCES)
        sources[0]["version"] = "3"
        second = self.propose(sources=sources, case_version="6")
        self.assertNotEqual(first["source_hash"], second["source_hash"])
        self.assertNotEqual(first["input_hash"], second["input_hash"])
        self.assertEqual(first["request_hash"], second["request_hash"])
        self.assertNotEqual(first["case_version"], second["case_version"])
        candidates = deepcopy(CANDIDATES)
        candidates[0]["text"] = "band C"
        third = self.propose(candidates=candidates)
        self.assertNotEqual(first["question_hash"], third["question_hash"])
        self.assertNotEqual(first["input_hash"], third["input_hash"])

    def test_noul_request_and_support_is_not_authority(self):
        self.payload = support_payload()
        result = self.propose(task="evidence_support", candidates=[], claim="EPC band C is recorded.")
        body = json.loads(self.calls[0][0].data)
        self.assertEqual(set(body["questions"]), {"evidence_supported"})
        self.assertEqual(body["questions"]["evidence_supported"]["type"], "noul")
        self.assertEqual(body["questions"]["evidence_supported"]["criteria"],
                         {"true": "Explicit support in supplied evidence", "false": "Contradiction, insufficient or missing support"})
        self.assertEqual(result["status"], "proposed")
        self.assertIs(result["supported"], True)
        self.assertIsNone(result["selected_candidate"])
        self.assertEqual(result["probability"], 0.97)
        self.assertIsNone(result["probabilities"])
        self.assertEqual(result["approval"], "Not reviewed")

    def test_choice_low_confidence_margin_ties_and_no_match(self):
        examples = [
            ("candidate-c", {"candidate-c": 0.89, "candidate-d": 0.09, NO_MATCH: 0.02}),
            ("candidate-c", {"candidate-c": 0.5, "candidate-d": 0.48, NO_MATCH: 0.02}),
            ("candidate-c", {"candidate-c": 0.5, "candidate-d": 0.5, NO_MATCH: 0.0}),
            (NO_MATCH, {"candidate-c": 0.02, "candidate-d": 0.01, NO_MATCH: 0.97}),
        ]
        for selected, probabilities in examples:
            with self.subTest(selected=selected, probabilities=probabilities):
                self.payload = choice_payload(selected, probabilities)
                result = self.propose()
                self.assertEqual(result["status"], "no_match")
                self.assertIs(result["validated"], True)
                self.assertIsNone(result["selected_candidate"])
                self.assertEqual(result["probabilities"], probabilities)
                self.assertEqual(result["approval"], "Not reviewed")

    def test_exact_selection_and_support_probability_boundaries(self):
        self.payload = choice_payload(probabilities={"candidate-c": 0.9, "candidate-d": 0.08, NO_MATCH: 0.02})
        self.assertEqual(self.propose()["status"], "proposed")
        for p in (0.95, 1.0):
            self.payload = support_payload(p)
            self.assertEqual(self.propose(task="evidence_support", candidates=[], claim="band C")["status"], "proposed")
        for p in (0.9499, 0.0, 0.3, 0.5):
            self.payload = support_payload(p)
            result = self.propose(task="evidence_support", candidates=[], claim="band C")
            self.assertEqual(result["status"], "no_match")
            self.assertIsNone(result["supported"])
            self.assertEqual(result["approval"], "Not reviewed")
            self.assertNotIn("all clear", result["explanation"])

    def assert_malformed(self, payload, **kwargs):
        self.payload = payload
        result = self.propose(**kwargs)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["reason"], "malformed_response")
        self.assertEqual(result["error_class"], "DecisionContractError")
        self.assertIs(result["validated"], False)
        self.assertIsNone(result["selected_candidate"])
        self.assertIsNone(result["supported"])
        self.assertIsNone(result["model"])
        self.assertIsNone(result["usage"])

    def test_bad_top_level_answer_question_and_usage_contracts(self):
        mutations = [
            lambda p: p.update(extra="provider-secret"),
            lambda p: p.pop("model"),
            lambda p: p.update(model="other-model"),
            lambda p: p.update(model="exercise-decision"),
            lambda p: p.update(answers=[]),
            lambda p: p.update(answers={}),
            lambda p: p["answers"].update(extra={"type": "noul", "probability": 0.99}),
            lambda p: p["answers"].update(candidate=[]),
            lambda p: p["answers"]["candidate"].update(type="score"),
            lambda p: p["answers"]["candidate"].update(rationale="provider-secret"),
            lambda p: p["answers"]["candidate"].pop("choice"),
            lambda p: p["answers"]["candidate"].update(choice=True),
            lambda p: p["answers"]["candidate"].update(choice="injected"),
            lambda p: p["answers"]["candidate"].update(choice="candidate-d"),
            lambda p: p.update(usage={}),
            lambda p: p.update(usage=[]),
            lambda p: p.update(usage={"tokens": True}),
            lambda p: p.update(usage={"tokens": -1}),
            lambda p: p.update(usage={"tokens": math.nan}),
            lambda p: p.update(usage={"tokens": 10 ** 1000}),
            lambda p: p.update(usage={"text": "provider-secret"}),
            lambda p: p.update(usage={"details": {"tokens": 1}}),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                payload = choice_payload()
                mutation(payload)
                self.assert_malformed(payload)
        for payload in (None, [], "bad JSON", 1):
            self.assert_malformed(payload)

    def test_nonfinite_bool_out_of_bounds_missing_and_unnormalized_probabilities(self):
        for p in (math.nan, math.inf, -math.inf, True, False, -0.01, 1.01, "0.94", None, 10 ** 1000):
            with self.subTest(p=str(p)[:30]):
                payload = choice_payload()
                payload["answers"]["candidate"]["probabilities"]["candidate-c"] = p
                self.assert_malformed(payload)
        for probabilities in (
            {"candidate-c": 0.94, "candidate-d": 0.04},
            {"candidate-c": 0.94, "candidate-d": 0.04, NO_MATCH: 0.02, "extra": 0},
            {"candidate-c": 0.94, "candidate-d": 0.02, NO_MATCH: 0.02},
            {"candidate-c": 0.94, "candidate-d": 0.04, NO_MATCH: 0.04},
            [0.94, 0.04, 0.02],
        ):
            self.assert_malformed(choice_payload(probabilities=probabilities))
        payload = choice_payload()
        payload["answers"]["candidate"]["probabilities"] = None
        self.assert_malformed(payload)
        # No silent repair even when all values are individually valid.
        self.assert_malformed(choice_payload(probabilities={"candidate-c": 0.9, "candidate-d": 0.05, NO_MATCH: 0.01}))

    def test_rounding_tolerance_does_not_normalize_raw_values(self):
        probabilities = {"candidate-c": 0.94, "candidate-d": 0.04, NO_MATCH: 0.0200001}
        self.payload = choice_payload(probabilities=probabilities)
        result = self.propose()
        self.assertEqual(result["status"], "proposed")
        self.assertEqual(result["probabilities"], probabilities)

    def test_default_transport_fake_bytes_reject_duplicate_keys_invalid_json_and_oversize(self):
        client = DecisionClient(CONFIG, inference=INFERENCE, token=self.token)
        for raw in (
            b'{"model":"other","model":"microsoft-decision-1","answers":{},"usage":{}}',
            b"not JSON", b"\xff", b"x" * 1_000_001,
        ):
            with patch("properwarm_mvp.decision.urllib.request.urlopen") as urlopen:
                urlopen.return_value.__enter__.return_value.read.return_value = raw
                result = self.propose(client)
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["reason"], "malformed_response")
                self.assertEqual(urlopen.call_count, 1)
        with patch("properwarm_mvp.decision.urllib.request.urlopen") as urlopen:
            urlopen.return_value.__enter__.return_value.read.return_value = json.dumps(choice_payload()).encode()
            self.assertEqual(self.propose(client)["status"], "proposed")
        self.assertEqual(self.calls, [])

    def test_noul_exact_keys_type_and_finite_range(self):
        for probability in (True, False, math.nan, math.inf, -0.1, 1.1, "0.97", None):
            self.assert_malformed(support_payload(probability), task="evidence_support", candidates=[], claim="band C")
        for mutation in (
            lambda p: p["answers"]["evidence_supported"].update(type="choice"),
            lambda p: p["answers"]["evidence_supported"].pop("probability"),
            lambda p: p["answers"]["evidence_supported"].update(probabilities={"true": 0.97}),
        ):
            payload = support_payload()
            mutation(payload)
            self.assert_malformed(payload, task="evidence_support", candidates=[], claim="band C")

    def test_default_no_authorization_and_endpoint_alone_zero_calls(self):
        with patch.dict("os.environ", {"AI_ENDPOINT": ENDPOINT}, clear=True):
            for client in (self.client(inference=InferenceConfig()), DecisionClient(CONFIG, transport=self.transport, token=self.token)):
                result = self.propose(client)
                self.assertEqual(result["status"], "disabled")
                self.assertEqual(result["reason"], "operator_authorization_required")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.tokens, [])
        self.assertFalse(inference_allowed(TASK, "decision-scoring"))

    def test_explicit_environment_flags_and_unknown_numbers(self):
        env = {
            "PW_INFERENCE_AUTHORIZED": "true", "PW_INFERENCE_ACCESS_REVIEWED": "true",
            "PW_INFERENCE_TERMS_REVIEWED": "true", "PW_INFERENCE_COST_REVIEWED": "true",
            "PW_INFERENCE_QUOTA_REVIEWED": "true", "PW_INFERENCE_PRICE_KNOWN": "true",
            "PW_INFERENCE_SPEND_PAUSED": "false", "PW_INFERENCE_TASKS": TASK,
            "PW_INFERENCE_ACCRUED_USD": "100", "PW_INFERENCE_MAX_CALL_CHARGE_USD": "0.01",
        }
        self.assertTrue(self.guard(config=InferenceConfig.from_env(env)).allowed)
        for key in env:
            missing = dict(env)
            missing.pop(key)
            self.assertFalse(self.guard(config=InferenceConfig.from_env(missing)).allowed)
        for value in ("nan", "inf", "-1", "nope"):
            for key in ("PW_INFERENCE_ACCRUED_USD", "PW_INFERENCE_MAX_CALL_CHARGE_USD", "PW_INFERENCE_CAP_USD"):
                invalid = dict(env)
                invalid[key] = value
                self.assertFalse(self.guard(config=InferenceConfig.from_env(invalid)).allowed)

    def test_operator_review_and_task_disable_zero_calls(self):
        configs = [replace(INFERENCE, **{flag: False}) for flag in (
            "authorized", "access_reviewed", "terms_reviewed", "cost_reviewed", "quota_reviewed", "price_known",
        )]
        configs.extend((replace(INFERENCE, spend_paused=True), replace(INFERENCE, enabled_tasks=())))
        for config in configs:
            self.assertEqual(self.propose(self.client(inference=config))["status"], "disabled")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.tokens, [])

    def test_unregistered_unapproved_wrong_capability_sources_and_workflow_zero_calls(self):
        self.assertEqual(self.propose(task="unknown")["reason"], "unregistered_or_unapproved_task")
        self.assertEqual(self.propose(task="summary")["reason"], "wrong_capability")
        registry = load_registry()
        registry["tasks"][TASK]["approved"] = False
        self.assertEqual(self.propose(self.client(registry=registry))["reason"], "unregistered_or_unapproved_task")
        self.assertEqual(self.propose(permissions=("evidence.read",))["reason"], "source_permission_denied")
        self.assertEqual(self.propose(workflow="hazard-release")["reason"], "wrong_workflow")
        sources = deepcopy(SOURCES)
        sources[0]["kind"] = "resident_profile"
        self.assertEqual(self.propose(sources=sources)["reason"], "source_scope_denied")
        sources[0]["kind"] = "form_evidence"
        sources[0]["text"] += "x" * 6000
        self.assertEqual(self.propose(sources=sources)["reason"], "source_scope_denied")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.tokens, [])

    def test_source_count_and_size_limits(self):
        for params in (
            {"source_count": 0}, {"source_count": 9}, {"source_count": True},
            {"text_chars": 6001}, {"text_chars": 0}, {"text_chars": True},
            {"source_kinds": []}, {"source_kinds": ["form_evidence", "form_evidence"]},
        ):
            self.assertFalse(self.guard(**params).allowed)

    def test_legacy_guard_all_registered_tasks_and_generic_narrative(self):
        registry = load_registry()
        for name, task in registry["tasks"].items():
            if task["capability"] != "generative-drafting":
                continue
            cfg = replace(INFERENCE, enabled_tasks=(name,))
            result = inference_guard(
                name, "generative-drafting", config=cfg, registry=registry,
                permissions=("evidence.read", "drafts.assist"),
                source_kinds=[task["source_kinds"][0]], source_count=1, text_chars=50,
                field="narrative", workflow=task["workflow_scope"][0],
            )
            self.assertTrue(result.allowed, name)
            self.assertFalse(inference_guard(
                name, "generative-drafting", config=InferenceConfig(),
                permissions=("evidence.read", "drafts.assist"), source_kinds=[task["source_kinds"][0]],
                source_count=1, text_chars=50,
            ).allowed)
        self.assertEqual(self.calls, [])

    def test_invalid_metadata_endpoints_and_timeouts_zero_calls(self):
        configs = [
            DecisionConfig(), replace(CONFIG, metadata_reviewed=False),
            replace(CONFIG, metadata_deployment="other"), replace(CONFIG, metadata_model="other"),
            replace(CONFIG, metadata_model_version="2"), replace(CONFIG, expected_model_version="2"),
            replace(CONFIG, metadata_endpoint="https://other.services.ai.azure.com"),
            replace(CONFIG, deployment_type="unverified"), replace(CONFIG, region=""),
            replace(CONFIG, endpoint="http://fictional.services.ai.azure.com"),
            replace(CONFIG, endpoint="https://fictional.services.ai.azure.com/providers/microsoft/v1/systemone"),
            replace(CONFIG, endpoint="https://secret@fictional.services.ai.azure.com"),
            replace(CONFIG, endpoint=ENDPOINT + "?secret=token"),
            replace(CONFIG, endpoint="https://third-party.invalid"),
            replace(CONFIG, endpoint=ENDPOINT + ":9999"),
            replace(CONFIG, endpoint=ENDPOINT + ":wrong-port"),
            replace(CONFIG, timeout_seconds=math.nan), replace(CONFIG, timeout_seconds=True),
            replace(CONFIG, timeout_seconds=0), replace(CONFIG, timeout_seconds=121),
        ]
        for config in configs:
            with self.subTest(config=config):
                result = self.propose(self.client(config=config))
                self.assertIn(result["status"], ("unconfigured", "failed"))
                self.assertIsNone(result["reserved_upper_charge_usd"])
        self.assertEqual(self.calls, [])
        self.assertEqual(self.tokens, [])

    def test_invalid_source_candidate_snapshots_zero_calls(self):
        variants = [
            {"case_id": "EX-2"}, {"case_version": ""},
            {"sources": []}, {"candidates": []}, {"claim": "Unexpected choice claim"},
        ]
        for mutation in (
            lambda s: s.update(case_id="EX-2"), lambda s: s.update(hash="bad"),
            lambda s: s.update(text=""), lambda s: s.update(version=True),
            lambda s: s.update(resident={"health": "private"}), lambda s: s.pop("locator"),
        ):
            sources = deepcopy(SOURCES)
            mutation(sources[0])
            variants.append({"sources": sources})
        variants.append({"sources": SOURCES * 2})
        for mutation in (
            lambda c: c.update(id=NO_MATCH), lambda c: c.update(id=True),
            lambda c: c.update(source_id="other-source"), lambda c: c.update(text="unsourced"),
            lambda c: c.update(approval=True),
        ):
            candidates = deepcopy(CANDIDATES)
            mutation(candidates[0])
            variants.append({"candidates": candidates})
        variants.append({"candidates": CANDIDATES * 2})
        for variant in variants:
            self.assertEqual(self.propose(**variant)["reason"], "invalid_source_or_candidate_snapshot")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.tokens, [])

    def test_failure_envelopes_safe_statuses_and_no_success_fallback(self):
        errors = [
            (TimeoutError("provider-secret"), "timeout", "TimeoutError", None),
            (urllib.error.URLError(TimeoutError("provider-secret")), "timeout", "TimeoutError", None),
            (urllib.error.URLError("provider-secret"), "transport_unavailable", "URLError", None),
            (PermissionError("provider-secret"), "authentication", "PermissionError", None),
            (ValueError("provider-secret"), "malformed_response", "DecisionContractError", None),
            (RuntimeError("provider-secret"), "provider_failure", "ProviderError", None),
        ]
        for code, reason in ((401, "authentication"), (403, "authentication"),
                             (429, "rate_limited"), (400, "provider_http"), (422, "provider_http"), (500, "provider_http")):
            errors.append((urllib.error.HTTPError(ENDPOINT, code, "provider-secret", {}, None), reason, "HTTPError", code))
        for error, reason, error_class, code in errors:
            with self.subTest(reason=reason, code=code):
                self.error = error
                result = self.propose()
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["reason"], reason)
                self.assertEqual(result["error_class"], error_class)
                self.assertEqual(result["http_status"], code)
                self.assertIs(result["validated"], False)
                self.assertIsNone(result["selected_candidate"])
                self.assertIsNone(result["model"])
                self.assertIsNone(result["usage"])
                self.assertNotIn("provider-secret", json.dumps(result))
                self.assertNotIn("fake-test-only-token", json.dumps(result))
                self.assertEqual(result["approval"], "Not reviewed")
                self.assertTrue(result["manual_route"])
                self.assertEqual(result["reserved_upper_charge_usd"], 0.01)

    def test_empty_token_never_calls_transport(self):
        client = self.client()
        client.token = lambda: ""
        self.assertEqual(self.propose(client)["reason"], "authentication")
        self.assertEqual(self.calls, [])

    def test_finite_price_cap_unknown_liabilities_and_pause(self):
        invalid_configs = []
        for field in ("max_call_charge_usd", "monthly_cap_usd", "pause_at_usd", "accrued_usd"):
            for value in (None, math.nan, math.inf, -1, True):
                invalid_configs.append(replace(INFERENCE, **{field: value}))
        invalid_configs.extend((
            replace(INFERENCE, max_call_charge_usd=0),
            replace(INFERENCE, monthly_cap_usd=451), replace(INFERENCE, pause_at_usd=406),
            replace(INFERENCE, accrued_usd=405), replace(INFERENCE, accrued_usd=404.995),
            replace(INFERENCE, accrued_usd=450), replace(INFERENCE, monthly_cap_usd=200, pause_at_usd=405),
        ))
        for config in invalid_configs:
            self.assertEqual(self.propose(self.client(inference=config))["status"], "disabled")
        self.assertEqual(self.calls, [])
        self.assertEqual(self.tokens, [])

    def test_reservations_retained_on_timeout_prevent_followup_over_cap(self):
        client = self.client(inference=replace(INFERENCE, accrued_usd=404.98, max_call_charge_usd=0.011))
        self.error = TimeoutError()
        self.assertEqual(self.propose(client)["reason"], "timeout")
        self.error = None
        self.assertEqual(self.propose(client)["reason"], "spend_limit")
        self.assertEqual(len(self.calls), 1)

    def test_protected_authority_fields_denied_and_inputs_never_mutated(self):
        original_sources = deepcopy(SOURCES)
        original_candidates = deepcopy(CANDIDATES)
        for field in PROTECTED_FIELDS:
            self.assertEqual(self.propose(field=field)["reason"], "prohibited_field")
        self.assertEqual(self.calls, [])
        for payload in (choice_payload(), choice_payload(NO_MATCH, {"candidate-c": 0.01, "candidate-d": 0.01, NO_MATCH: 0.98})):
            self.payload = payload
            result = self.propose(sources=original_sources, candidates=original_candidates)
            self.assertEqual(result["approval"], "Not reviewed")
            for authority_key in ("consent", "approved", "payment", "signature", "ranking", "hazard_release"):
                self.assertNotIn(authority_key, result)
        self.assertEqual(original_sources, SOURCES)
        self.assertEqual(original_candidates, CANDIDATES)


if __name__ == "__main__":
    unittest.main()
