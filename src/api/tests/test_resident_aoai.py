"""Focused inference contracts. No cloud, credential discovery or real resident data."""

import json
import unittest
from unittest.mock import Mock, patch

from zava_forward.core.resident_assistant import CaseProgress, Topic

from zava_forward.api.resident_demo import chat
from zava_forward.api.resident_demo.aoai import (
    MAX_COST_USD,
    MAX_PAYLOAD,
    AzureAdvisor,
    SqlAccounting,
    configured_advisor,
    resident_key,
)
from zava_forward.api.resident_demo.assistant import EXPIRES

ENDPOINT = "https://aoai-resident-test.openai.azure.com"
CASE = CaseProgress("Your survey is being arranged.", "Your officer will contact you.")


def reply(ids: object = None, **extra: object) -> bytes:
    return json.dumps(
        {
            "usage": {"prompt_tokens": 400, "completion_tokens": 20},
            "choices": [
                {
                    "finish_reason": "stop",
                    "message": {"content": json.dumps({"guidance": ids or ["contact"]})},
                }
            ],
            **extra,
        }
    ).encode()


def question_reply(
    answer: str = "You mentioned a dead-rat smell. Your survey update does not explain its cause. "
    "Ask your housing officer how to report the smell, where it is and when it started.",
    sources: object = ("guidance", "case"),
) -> bytes:
    body = json.loads(reply())
    body["choices"][0]["message"]["content"] = json.dumps({"answer": answer, "sources": sources})
    return json.dumps(body).encode()


class AzureAdvisorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.events: list[str] = []
        self.accounting = Mock()

        def reserve(resident: str) -> str:
            self.events.append("reserve")
            return "ticket"

        def token() -> str:
            self.events.append("token")
            return "FAKE-TOKEN"

        def transport(url: str, data: bytes, credential: str) -> bytes:
            self.events.append("transport")
            return reply()

        self.accounting.reserve.side_effect = reserve
        self.token = Mock(side_effect=token)
        self.transport = Mock(side_effect=transport)
        self.advisor = AzureAdvisor(
            ENDPOINT,
            self.accounting,
            self.token,
            transport=self.transport,
            clock=lambda: EXPIRES - 10,
        )

    def answer(self, topic: Topic = Topic.STATUS, case: CaseProgress = CASE) -> object:
        return self.advisor.answer(topic, case, resident_key("C-1"))

    def test_exact_bounded_payload_and_precommitted_accounting(self) -> None:
        result = self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertEqual(self.events, ["reserve", "token", "transport"])
        self.assertEqual(result.label, "AI suggestion, not approved")
        self.assertIn(CASE.progress, result.answer)
        url, data, token = self.transport.call_args.args
        self.assertIn("/resident-mini/", url)
        self.assertLessEqual(len(data), MAX_PAYLOAD)
        self.assertLess(MAX_COST_USD, 0.01)
        payload = json.loads(data)
        self.assertEqual(payload["max_tokens"], 256)
        self.assertEqual(payload["n"], 1)
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["response_format"]["type"], "json_schema")
        self.assertNotIn("tools", payload)
        for value in ("C-1", resident_key("C-1"), "FAKE-TOKEN", "example.com", "address"):
            self.assertNotIn(value, data.decode())
        self.assertEqual(token, "FAKE-TOKEN")
        self.accounting.complete.assert_called_once_with("ticket", 400, 20)

    def test_cap_and_rate_denial_use_rules_before_credentials(self) -> None:
        self.accounting.reserve.side_effect = None
        self.accounting.reserve.return_value = None
        result = self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertIn("Summary by rules", result.label)
        self.assertIn(CASE.progress, result.answer)
        self.token.assert_not_called()
        self.transport.assert_not_called()

    def test_timeout_and_accounting_outage_fall_back_without_retries_or_refund(self) -> None:
        for failing in (self.transport, self.accounting.reserve, self.accounting.complete):
            with self.subTest(failing=failing):
                failing.side_effect = OSError("DO-NOT-LOG")
                with self.assertLogs("zava_forward.api.resident_demo.aoai") as captured:
                    result = self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
                self.assertIn("Summary by rules", result.label)
                self.assertNotIn("DO-NOT-LOG", str(captured.output))
                failing.side_effect = None
                failing.return_value = reply() if failing is self.transport else "ticket"

    def test_output_injection_and_unrelated_ids_are_never_rendered(self) -> None:
        for raw in (
            reply(["closed"]),
            reply(["SECRET"]),
            reply(["contact", "contact"]),
            reply({"answer": "SECRET"}),
            reply(choices=[]),
            reply(usage={"prompt_tokens": True, "completion_tokens": 1}),
            b"not-json",
            b"x" * 4097,
            reply(choices=[{"finish_reason": "stop", "message": None}]),
        ):
            self.transport.side_effect = None
            self.transport.return_value = raw
            result = self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
            self.assertIn("Summary by rules", result.label)
            self.assertNotIn("SECRET", result.answer)

    def test_all_topics_and_context_sensitive_guidance_preserve_mandatory_facts(self) -> None:
        for topic, case, ids, expected in (
            (Topic.STATUS, CASE, ["contact"], CASE.next_step),
            (Topic.STATUS, CaseProgress("Progress", "Next", "Closed"), ["closed"], "Closed"),
            (
                Topic.STATUS,
                CaseProgress("We do not have a plain-language update.", "Ask your officer."),
                ["unknown"],
                "missing from this view",
            ),
            (Topic.DOCUMENTS, CASE, ["confirm", "privacy"], "cannot tell you what to send"),
            (Topic.FORMS, CASE, ["explain", "check"], "Do not guess"),
        ):
            self.transport.side_effect = None
            self.transport.return_value = reply(ids)
            result = self.advisor.answer(topic, case, resident_key("C-1"))
            self.assertEqual(result.label, "AI suggestion, not approved")
            self.assertIn(expected, result.answer)
            self.assertIn("housing officer", result.help)

    def test_expiry_before_reservation_and_during_credentials_and_response(self) -> None:
        for times, calls in (
            ([EXPIRES], 0),
            ([EXPIRES - 1, EXPIRES], 0),
            ([EXPIRES - 1, EXPIRES - 1, EXPIRES], 1),
        ):
            self.transport.reset_mock()
            self.advisor.clock = Mock(side_effect=times)
            result = self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
            self.assertIn("Summary by rules", result.label)
            self.assertEqual(self.transport.call_count, calls)

    def test_oversized_prompt_never_reserves_or_calls_model(self) -> None:
        result = self.advisor.answer(
            Topic.STATUS, CaseProgress("x" * 5000, ""), resident_key("C-1")
        )
        self.assertIn("Summary by rules", result.label)
        self.accounting.reserve.assert_not_called()
        self.transport.assert_not_called()

    def test_stable_resident_key_and_separate_resident_allowances(self) -> None:
        self.assertEqual(resident_key("C-1"), resident_key("C-1"))
        self.assertNotEqual(resident_key("C-1"), resident_key("C-2"))
        self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.advisor.answer(Topic.STATUS, CASE, resident_key("C-2"))
        self.assertNotEqual(
            self.accounting.reserve.call_args_list[0], self.accounting.reserve.call_args_list[1]
        )

    def test_usage_logs_have_counts_only(self) -> None:
        with self.assertLogs("zava_forward.api.resident_demo.aoai", level="INFO") as captured:
            self.advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
        text = str(captured.output)
        self.assertIn("prompt_tokens=400 completion_tokens=20", text)
        for private in (CASE.progress, "C-1", resident_key("C-1"), "FAKE-TOKEN"):
            self.assertNotIn(private, text)

    def test_factory_defaults_off_and_uses_only_explicit_managed_identity(self) -> None:
        connect = Mock()
        self.assertIsNone(configured_advisor({}, connect))
        with patch("zava_forward.api.resident_demo.aoai.ManagedIdentityCredential") as credential:
            advisor = configured_advisor(
                {
                    "ZF_DEMO_ASSISTANT_ENABLED": "true",
                    "ZF_DEMO_ASSISTANT_ENDPOINT": ENDPOINT,
                    "ZF_SQL_CLIENT_ID": "existing-identity",
                },
                connect,
            )
            credential.assert_called_once_with(client_id="existing-identity")
            self.assertIsNotNone(advisor)
            assert advisor is not None
            advisor.token()
            credential.return_value.get_token.assert_called_once_with(
                "https://cognitiveservices.azure.com/.default"
            )
        connect.assert_not_called()
        for env in (
            {"ZF_DEMO_ASSISTANT_ENABLED": "yes"},
            {"ZF_DEMO_ASSISTANT_KEY": "not-allowed"},
            {"ZF_DEMO_ASSISTANT_ENABLED": "true", "ZF_SQL_AUTH": "password"},
        ):
            with self.assertRaises(ValueError):
                configured_advisor(env, connect)

    def test_sql_adapter_uses_fixed_procedures_and_retains_completion(self) -> None:
        conn = Mock()
        conn.cursor.return_value.fetchone.return_value = [1]
        accounting = SqlAccounting(lambda: conn)
        ticket = accounting.reserve(resident_key("C-1"))
        assert ticket is not None
        accounting.complete(ticket, 10, 2)
        self.assertEqual(conn.close.call_count, 2)
        self.assertEqual(
            conn.cursor.return_value.execute.call_args.args,
            ("EXEC resident_ai.complete @reservation=?, @prompt=?, @completion=?", (ticket, 10, 2)),
        )

    def test_question_generates_prose_with_projected_grounding_and_prepaid_cost(self) -> None:
        self.transport.side_effect = None
        self.transport.return_value = question_reply()
        base = chat.answer("repair", {})
        result = self.advisor.answer_question(
            "My home smells like a dead rat", CASE, resident_key("C-1"), base
        )
        self.assertEqual(self.events, ["reserve", "token"])
        self.assertEqual(result.label, "AI-generated")
        self.assertIn("dead-rat smell", result.answer)
        self.assertNotEqual(result.answer, base.answer)
        self.assertIn("Your case: Where things are", result.sources)
        self.assertEqual(result.help, base.help)
        payload = json.loads(self.transport.call_args.args[1])
        content = json.loads(payload["messages"][1]["content"])
        self.assertEqual(content["question"], "My home smells like a dead rat")
        self.assertIn(CASE.progress, content["sources"]["case"])
        self.assertEqual(content["sources"]["guidance"], base.answer)
        self.assertEqual(payload["response_format"]["json_schema"]["name"], "resident_answer")
        self.assertEqual(payload["max_tokens"], 256)
        self.assertLessEqual(len(self.transport.call_args.args[1]), MAX_PAYLOAD)
        self.accounting.complete.assert_called_once_with("ticket", 400, 20)
        for forbidden in ("C-1", resident_key("C-1"), "FAKE-TOKEN", "example.com"):
            self.assertNotIn(forbidden, json.dumps(payload))

    def test_question_invalid_outputs_have_explicit_rules_fallback(self) -> None:
        base = chat.answer("repair", {})
        invalid = [
            question_reply("", ["case"]),
            question_reply("x" * 1601),
            question_reply("Unsafe\x00text"),
            question_reply(sources=[]),
            question_reply(sources=["invented"]),
            question_reply(sources=["case", "case"]),
            question_reply(sources="case"),
            reply(["contact"]),
            b"not-json",
            b"x" * 4097,
            reply(choices=[{"finish_reason": "length", "message": {"content": "{}"}}]),
            reply(usage={"prompt_tokens": True, "completion_tokens": 1}),
        ]
        self.transport.side_effect = None
        for raw in invalid:
            with self.subTest(raw=raw[:80]):
                self.transport.return_value = raw
                result = self.advisor.answer_question("A smell", CASE, resident_key("C-1"), base)
                self.assertIn("AI unavailable", result.label)
                self.assertEqual(result.answer, base.answer)
                self.assertEqual(result.sources, base.sources)

    def test_question_expiry_budget_outage_and_limits_do_not_bypass_accounting(self) -> None:
        base = chat.answer("repair", {})
        for failure in ("expired", "budget", "transport", "accounting", "oversize"):
            with self.subTest(failure=failure):
                self.setUp()
                if failure == "expired":
                    self.advisor.clock = lambda: EXPIRES
                if failure == "budget":
                    self.accounting.reserve.side_effect = lambda _: None
                if failure == "transport":
                    self.transport.side_effect = OSError("private failure")
                if failure == "accounting":
                    self.accounting.complete.side_effect = OSError("private failure")
                result = self.advisor.answer_question(
                    "x" * 501 if failure == "oversize" else "A smell",
                    CASE,
                    resident_key("C-1"),
                    base,
                )
                self.assertIn("Summary by rules", result.label)
                self.assertEqual(result.answer, base.answer)
                if failure in ("expired", "budget", "oversize"):
                    self.token.assert_not_called()
                    self.transport.assert_not_called()

    def test_question_expiry_after_response_rejects_generated_text(self) -> None:
        self.advisor.clock = Mock(side_effect=[EXPIRES - 1, EXPIRES - 1, EXPIRES])
        self.transport.side_effect = None
        self.transport.return_value = question_reply()
        base = chat.answer("repair", {})
        result = self.advisor.answer_question("A smell", CASE, resident_key("C-1"), base)
        self.assertIn("AI unavailable", result.label)
        self.assertEqual(result.answer, base.answer)
