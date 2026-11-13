"""Resident topic adapter joined to the consumption ledger. Constructed evidence only:
no credentials, no network, no paid call, no resident text."""

from __future__ import annotations

import json
import logging
import sqlite3
import tempfile
import unittest
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

from zava_forward.core.ai_consumption import Consumption, reference, timestamp
from zava_forward.core.resident_assistant import (
    AssistantUnavailable,
    CaseProgress,
    FakeProvider,
    Topic,
    advise,
)

from zava_forward.api.resident_demo.aoai import AzureAdvisor, configured_advisor, resident_key
from zava_forward.api.resident_demo.assistant import EXPIRES, AzureTopicProvider
from zava_forward.api.resident_demo.ledger_meter import (
    ADVISOR_CAPABILITIES,
    CAPABILITY,
    AdvisorLedger,
    LedgerTopicMeter,
    advisor_meters,
)

START = "2026-10-31T00:00:00Z"
END = "2026-11-01T00:00:00Z"
CONFIG = reference("resident-topic-config-v1")
PROMPT = reference("resident-topic-prompt-v1")
MODEL = "review-required"
COUNTS = {"prompt_tokens": 40, "completion_tokens": 2, "total_tokens": 42}
CACHED = {"prompt_tokens_details": {"cached_tokens": 0}}
ENDPOINT = "https://synthetic-test.openai.azure.com"


class Port:
    sql = True
    mssql = False

    def __init__(self, path: Path) -> None:
        self.path = path
        self.clock: float = float(timestamp("2026-10-31T12:00:00Z"))
        with self.transaction() as db:
            db.execute(
                "CREATE TABLE assistant_events "
                "(id TEXT PRIMARY KEY, task_id TEXT, at REAL, body TEXT)"
            )

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def now(self, db: Any) -> float:
        return self.clock

    def event(self, db: Any, tid: str, **body: Any) -> None:
        db.execute(
            "INSERT INTO assistant_events VALUES (?,?,?,?)",
            (uuid.uuid4().hex, tid, self.clock, json.dumps(body)),
        )


CANARIES = ("SYN-RESIDENT-QUESTION-CANARY", "Ada Example", "07700 900123", "SYN-CASE-CANARY")
QUESTION = "SYN-RESIDENT-QUESTION-CANARY: I am Ada Example, phone 07700 900123. When is my visit?"


def call_join(
    test: unittest.TestCase, records: list[dict[str, Any]], capability: str, **completed: Any
) -> tuple[dict[str, Any], dict[str, Any]]:
    """One reservation joined by id to one completion; context on it, counts on the latter."""
    reserved = [r for r in records if r["kind"] == "reserved"]
    closed = [r for r in records if r["kind"] == "completed"]
    test.assertEqual((len(reserved), len(closed)), (1, 1))
    test.assertEqual(reserved[0]["id"], closed[0]["id"])
    test.assertEqual(reserved[0]["capability"], capability)
    test.assertEqual(reserved[0]["case_type"], "resident-chat")
    test.assertEqual(reserved[0]["configuration"], CONFIG)
    test.assertEqual(reserved[0]["prompt"], PROMPT)
    for key, value in completed.items():
        test.assertEqual(closed[0][key], value, key)
    return reserved[0], closed[0]


def assert_content_free(
    test: unittest.TestCase, records: list[dict[str, Any]], sent: list[bytes], logs: str
) -> None:
    """The canaries really reached the provider, yet no ledger record or log line holds one."""
    test.assertTrue(sent)
    test.assertTrue(any(b"SYN-RESIDENT-QUESTION-CANARY" in payload for payload in sent))
    stored = json.dumps(records)
    for canary in CANARIES:
        test.assertNotIn(canary, stored)
        test.assertNotIn(canary, logs)


def reply(usage: dict[str, Any] | None, model: str = MODEL) -> bytes:
    body: dict[str, Any] = {
        "model": model,
        "choices": [{"message": {"content": "status"}, "finish_reason": "stop"}],
    }
    if usage is not None:
        body["usage"] = usage
    return json.dumps(body).encode()


class ResidentLedgerJoinTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.port = Port(Path(temp.name) / "constructed.sqlite")
        self.ledger = Consumption(self.port)
        self.response: bytes | Exception = reply(dict(COUNTS, **CACHED))
        self.sent = 0

    def authorize(self, budget_calls: int = 10) -> None:
        price = self.ledger.price(
            source="https://prices.azure.com/api/retail/prices",
            source_hash=reference("constructed-price-response"),
            retrieved=START,
            version="constructed-v1",
            model=MODEL,
            currency="USD",
            start=START,
            end=END,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=False,
        )
        self.ledger.authorize(
            authority="constructed-authority",
            owner="constructed-finance-owner",
            evidence="constructed-no-paid-spend",
            price=price,
            capability=CAPABILITY,
            configuration=CONFIG,
            start=START,
            end=END,
            max_calls=5,
            max_depth=1,
            budgets=[dict(id=reference("period"), calls=budget_calls, tokens=10000, amount="10")],
        )

    def provider(self) -> AzureTopicProvider:
        meter = LedgerTopicMeter(self.ledger, model=MODEL, configuration=CONFIG, prompt=PROMPT)

        def transport(url: str, payload: bytes, token: str) -> bytes:
            self.sent += 1
            if isinstance(self.response, Exception):
                raise self.response
            return self.response

        return AzureTopicProvider(
            ENDPOINT,
            MODEL,
            enabled=True,
            token=meter.token(lambda: "FAKE-TOKEN"),
            reserve=meter.reserve,
            record_call=meter.close,
            transport=transport,
            clock=lambda: EXPIRES - 10,
        )

    def kinds(self) -> list[dict[str, Any]]:
        with self.port.transaction() as db:
            records: list[dict[str, Any]] = self.ledger._read(db)
            return records

    def test_admitted_call_is_closed_with_context_counts_and_outcome(self) -> None:
        self.authorize()
        self.assertEqual(self.provider().select(Topic.STATUS), Topic.STATUS)
        reserved = [r for r in self.kinds() if r["kind"] == "reserved"]
        completed = [r for r in self.kinds() if r["kind"] == "completed"]
        self.assertEqual(len(reserved), 1)
        self.assertEqual(reserved[0]["capability"], CAPABILITY)
        self.assertEqual(reserved[0]["configuration"], CONFIG)
        self.assertEqual(reserved[0]["prompt"], PROMPT)
        self.assertEqual(completed[0]["outcome"], "returned")
        self.assertEqual(completed[0]["tokens"]["total_tokens"], 42)
        self.assertFalse(completed[0]["held"])
        self.assertNotIn("status", json.dumps(self.kinds()))

    def test_topic_call_joins_by_id_and_empty_credential_closes_the_reservation(self) -> None:
        self.authorize()
        self.provider().select(Topic.STATUS)
        call_join(
            self,
            self.kinds(),
            CAPABILITY,
            outcome="returned",
            held=False,
            tokens=COUNTS | {"cached_tokens": 0},
        )
        meter = LedgerTopicMeter(self.ledger, model=MODEL, configuration=CONFIG, prompt=PROMPT)
        provider = AzureTopicProvider(
            ENDPOINT,
            MODEL,
            enabled=True,
            token=lambda: "",
            reserve=meter.reserve,
            record_call=meter.close,
            transport=lambda url, payload, token: reply(None),
            clock=lambda: EXPIRES - 10,
        )
        with self.assertRaises(AssistantUnavailable):
            provider.select(Topic.STATUS)
        closed = [r for r in self.kinds() if r["kind"] == "completed"]
        self.assertEqual(sorted(r["outcome"] for r in closed), ["provider-unavailable", "returned"])
        self.assertEqual(len({r["id"] for r in closed}), 2)

    def test_unknown_authority_refuses_before_the_network_and_alerts(self) -> None:
        with self.assertRaises(AssistantUnavailable) as caught:
            self.provider().select(Topic.STATUS)
        self.assertEqual(str(caught.exception), "budget_unavailable")
        self.assertEqual(self.sent, 0)
        alerts = [r for r in self.kinds() if r["kind"] == "alert"]
        self.assertEqual(alerts[0]["reason"], "authority-unknown")
        self.assertEqual(alerts[0]["route"], "workflow-only")

    def test_call_budget_stops_the_next_call_with_an_owned_alert(self) -> None:
        self.authorize(budget_calls=1)
        provider = self.provider()
        provider.select(Topic.STATUS)
        with self.assertRaises(AssistantUnavailable) as caught:
            provider.select(Topic.STATUS)
        self.assertEqual(str(caught.exception), "budget_unavailable")
        self.assertEqual(self.sent, 1)
        alerts = [r for r in self.kinds() if r["kind"] == "alert"]
        self.assertEqual(alerts[0]["reason"], "call-budget-limit")
        self.assertEqual(alerts[0]["owner"], reference("constructed-finance-owner"))

    def test_returned_call_links_an_ineligible_content_free_output(self) -> None:
        self.authorize()
        provider = self.provider()
        self.assertEqual(provider.select(Topic.STATUS), Topic.STATUS)
        outputs = [r for r in self.kinds() if r["kind"] == "output"]
        reserved = [r for r in self.kinds() if r["kind"] == "reserved"]
        self.assertEqual(len(outputs), 1)
        self.assertIs(outputs[0]["eligible"], False)
        self.assertEqual(outputs[0]["root"], reserved[0]["root"])
        self.assertNotIn("status", json.dumps(outputs))

    def test_unexpected_credential_error_closes_the_reservation_without_output(self) -> None:
        self.authorize()
        meter = LedgerTopicMeter(self.ledger, model=MODEL, configuration=CONFIG, prompt=PROMPT)

        def broken() -> str:
            raise RuntimeError("synthetic credential failure")

        provider = AzureTopicProvider(
            ENDPOINT,
            MODEL,
            enabled=True,
            token=meter.token(broken),
            reserve=meter.reserve,
            record_call=meter.close,
            transport=lambda url, payload, token: self.fail("sent"),
            clock=lambda: EXPIRES - 10,
        )
        with self.assertRaises(RuntimeError):
            provider.select(Topic.STATUS)
        records = self.kinds()
        call_join(self, records, CAPABILITY, outcome="provider-unavailable", held=True)
        self.assertEqual([r for r in records if r["kind"] == "output"], [])

    def test_transport_failure_is_closed_as_unknown_liability(self) -> None:
        self.authorize()
        self.response = TimeoutError("synthetic")
        with self.assertRaises(AssistantUnavailable):
            self.provider().select(Topic.STATUS)
        completed = [r for r in self.kinds() if r["kind"] == "completed"]
        self.assertEqual(completed[0]["outcome"], "timeout")
        self.assertTrue(completed[0]["held"])
        self.assertEqual(
            [r["reason"] for r in self.kinds() if r["kind"] == "alert"], ["liability-unknown"]
        )

    def test_missing_usage_is_held_as_unknown_not_estimated(self) -> None:
        self.authorize()
        self.response = reply(None)
        self.provider().select(Topic.STATUS)
        completed = [r for r in self.kinds() if r["kind"] == "completed"]
        self.assertTrue(completed[0]["held"])
        self.assertIsNone(completed[0]["charge"])

    def test_missing_cached_count_is_held_as_unknown_not_assumed(self) -> None:
        self.authorize()
        self.response = reply(COUNTS)
        self.provider().select(Topic.STATUS)
        completed = [r for r in self.kinds() if r["kind"] == "completed"]
        self.assertTrue(completed[0]["held"])
        self.assertIsNone(completed[0]["charge"])

    def test_expiry_after_credential_acquisition_stops_dispatch(self) -> None:
        self.authorize()
        meter = LedgerTopicMeter(self.ledger, model=MODEL, configuration=CONFIG, prompt=PROMPT)

        def credential() -> str:
            self.port.clock = float(timestamp(END))
            return "FAKE-TOKEN"

        provider = AzureTopicProvider(
            ENDPOINT,
            MODEL,
            enabled=True,
            token=meter.token(credential),
            reserve=meter.reserve,
            record_call=meter.close,
            transport=lambda url, payload, token: reply(None),
            clock=lambda: EXPIRES - 10,
        )
        with self.assertRaises(AssistantUnavailable):
            provider.select(Topic.STATUS)
        reasons = [r["reason"] for r in self.kinds() if r["kind"] == "alert"]
        self.assertEqual(reasons, ["authority-expired"])


CASE = CaseProgress("Your survey is being arranged.", "Your officer will contact you.")


def advisor_reply(usage: dict[str, Any] | None, model: str = MODEL) -> bytes:
    body: dict[str, Any] = {
        "model": model,
        "choices": [
            {"finish_reason": "stop", "message": {"content": json.dumps({"guidance": ["contact"]})}}
        ],
    }
    if usage is not None:
        body["usage"] = usage
    return json.dumps(body).encode()


class ResidentAdvisorLedgerJoinTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.port = Port(Path(temp.name) / "constructed.sqlite")
        self.ledger = Consumption(self.port)
        self.response: bytes | Exception = advisor_reply(dict(COUNTS, **CACHED))
        self.sent = 0
        self.payloads: list[bytes] = []
        self.accounting = Mock()
        self.accounting.reserve.return_value = "ticket"

    def authorize(self, capability: str) -> None:
        price = self.ledger.price(
            source="https://prices.azure.com/api/retail/prices",
            source_hash=reference("constructed-price-response"),
            retrieved=START,
            version="constructed-v1",
            model=MODEL,
            currency="USD",
            start=START,
            end=END,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=False,
        )
        self.ledger.authorize(
            authority="constructed-" + capability,
            owner="constructed-finance-owner",
            evidence="constructed-no-paid-spend",
            price=price,
            capability=capability,
            configuration=CONFIG,
            start=START,
            end=END,
            max_calls=5,
            max_depth=1,
            budgets=[dict(id=reference(capability), calls=10, tokens=100000, amount="100")],
        )

    def credential(self) -> str:
        return "FAKE-TOKEN"

    def advisor(
        self, metered: bool = True, kinds: tuple[str, ...] = ("guidance", "question")
    ) -> AzureAdvisor:
        meters = advisor_meters(
            self.ledger,
            model=MODEL,
            configuration=CONFIG,
            prompts={kind: PROMPT for kind in ADVISOR_CAPABILITIES},
        )

        def transport(url: str, payload: bytes, token: str) -> bytes:
            self.sent += 1
            self.payloads.append(payload)
            if isinstance(self.response, Exception):
                raise self.response
            return self.response

        return AzureAdvisor(
            ENDPOINT,
            self.accounting,
            self.credential,
            transport=transport,
            clock=lambda: EXPIRES - 10,
            meters={k: m for k, m in meters.items() if k in kinds} if metered else None,
        )

    def everything(self) -> list[dict[str, Any]]:
        with self.port.transaction() as db:
            rows: list[dict[str, Any]] = self.ledger._read(db)
        return rows

    def records(self, kind: str) -> list[dict[str, Any]]:
        return [r for r in self.everything() if r["kind"] == kind]

    def ask(self) -> Any:
        base = advise(Topic.STATUS, CASE, FakeProvider())
        return self.advisor().answer_question(QUESTION, CASE, resident_key("C-1"), base)

    def test_admitted_guidance_call_is_closed_with_its_own_capability(self) -> None:
        self.authorize("resident-guidance")
        advice = self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertEqual(advice.label, "AI suggestion, not approved")
        reserved, completed = self.records("reserved"), self.records("completed")
        self.assertEqual(reserved[0]["capability"], "resident-guidance")
        self.assertEqual(reserved[0]["prompt"], PROMPT)
        self.assertEqual(completed[0]["outcome"], "returned")
        self.assertEqual(completed[0]["tokens"]["total_tokens"], 42)
        self.assertFalse(completed[0]["held"])
        self.assertNotIn("survey", json.dumps(self.records("reserved") + completed))

    def test_unauthorised_capability_stops_before_the_network_with_rules_fallback(self) -> None:
        self.authorize("resident-question")
        advice = self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertTrue(advice.label.startswith("Summary by rules - AI unavailable"))
        self.assertEqual(self.sent, 0)
        alert = self.records("alert")[0]
        self.assertEqual(alert["reason"], "authority-unknown")
        self.assertEqual(alert["route"], "workflow-only")

    def test_kind_without_a_meter_is_refused_not_sent_unmetered(self) -> None:
        self.authorize("resident-guidance")
        advice = self.advisor(kinds=("question",)).answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertTrue(advice.label.startswith("Summary by rules - AI unavailable"))
        self.assertEqual(self.sent, 0)
        self.assertEqual(self.records("reserved"), [])

    def test_transport_failure_is_held_as_unknown_liability(self) -> None:
        self.authorize("resident-guidance")
        self.response = TimeoutError("synthetic")
        advice = self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertTrue(advice.label.startswith("Summary by rules - AI unavailable"))
        completed = self.records("completed")
        self.assertEqual(completed[0]["outcome"], "timeout")
        self.assertTrue(completed[0]["held"])
        self.assertEqual([r["reason"] for r in self.records("alert")], ["liability-unknown"])

    def test_missing_usage_is_held_not_estimated(self) -> None:
        self.authorize("resident-guidance")
        self.response = advisor_reply(None)
        self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        completed = self.records("completed")
        self.assertTrue(completed[0]["held"])
        self.assertIsNone(completed[0]["charge"])

    def test_without_meters_the_advisor_behaves_as_before(self) -> None:
        advice = self.advisor(metered=False).answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertEqual(advice.label, "AI suggestion, not approved")
        self.assertEqual(self.records("reserved"), [])

    def test_question_call_joins_the_ledger_and_stays_content_free(self) -> None:
        self.authorize("resident-question")
        self.response = json.dumps(
            {
                "model": MODEL,
                "usage": dict(COUNTS, **CACHED),
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "content": json.dumps({"answer": "Soon.", "sources": ["case"]})
                        },
                    }
                ],
            }
        ).encode()
        with self.assertLogs("zava_forward.api.resident_demo.aoai", level="INFO") as logs:
            advice = self.ask()
        self.assertEqual(advice.label, "AI-generated")
        everything = self.everything()
        _, closed = call_join(
            self,
            everything,
            "resident-question",
            outcome="returned",
            held=False,
            tokens=COUNTS | {"cached_tokens": 0},
        )
        assert_content_free(self, everything, self.payloads, "\n".join(logs.output))

    def test_guidance_call_joins_by_id_with_counts(self) -> None:
        self.authorize("resident-guidance")
        self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        call_join(
            self,
            self.everything(),
            "resident-guidance",
            outcome="returned",
            held=False,
            tokens=COUNTS | {"cached_tokens": 0},
        )

    def test_failed_question_call_stays_joined_and_content_free(self) -> None:
        self.authorize("resident-question")
        self.response = TimeoutError("synthetic")
        with self.assertLogs("zava_forward.api.resident_demo.aoai", level="INFO") as logs:
            logging.getLogger("zava_forward.api.resident_demo.aoai").info("started")
            advice = self.ask()
        self.assertTrue(advice.label.startswith("Summary by rules - AI unavailable"))
        everything = self.everything()
        call_join(self, everything, "resident-question", outcome="timeout", held=True)
        self.assertEqual(
            [r["reason"] for r in everything if r["kind"] == "alert"], ["liability-unknown"]
        )
        assert_content_free(self, everything, self.payloads, "\n".join(logs.output))

    def test_credential_failure_after_admission_closes_the_reservation(self) -> None:
        self.authorize("resident-guidance")
        with patch.object(self, "credential", return_value=""):
            advice = self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertTrue(advice.label.startswith("Summary by rules - AI unavailable"))
        self.assertEqual(self.sent, 0)
        call_join(
            self, self.everything(), "resident-guidance", outcome="provider-unavailable", held=True
        )

    def test_configured_advisor_joins_only_when_the_caller_supplies_meters(self) -> None:
        self.authorize("resident-guidance")
        env = {
            "ZF_DEMO_ASSISTANT_ENABLED": "true",
            "ZF_DEMO_ASSISTANT_ENDPOINT": ENDPOINT,
            "ZF_SQL_CLIENT_ID": "synthetic-client",
        }
        meters = advisor_meters(
            self.ledger,
            model=MODEL,
            configuration=CONFIG,
            prompts={kind: PROMPT for kind in ADVISOR_CAPABILITIES},
        )
        with patch("zava_forward.api.resident_demo.aoai.ManagedIdentityCredential") as identity:
            identity.return_value.get_token.return_value.token = "FAKE-TOKEN"
            unmetered = configured_advisor(env, Mock())
            metered = configured_advisor(env, Mock(), meters=meters)
        assert unmetered is not None and metered is not None
        self.assertIsNone(unmetered.meters)
        for advisor in (unmetered, metered):
            advisor.accounting = self.accounting
            advisor.clock = lambda: EXPIRES - 10
            advisor.transport = lambda url, payload, token: advisor_reply(dict(COUNTS, **CACHED))
            advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
            if advisor is unmetered:
                self.assertEqual(self.records("reserved"), [])
        call_join(self, self.everything(), "resident-guidance", outcome="returned", held=False)

    def test_returned_advisor_call_links_an_ineligible_output(self) -> None:
        self.authorize("resident-guidance")
        self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        outputs = self.records("output")
        self.assertEqual(len(outputs), 1)
        self.assertIs(outputs[0]["eligible"], False)
        self.assertEqual(outputs[0]["root"], self.records("reserved")[0]["root"])
        self.assertNotIn("Ada Example", json.dumps(self.everything()))

    def test_unexpected_credential_error_closes_the_reservation(self) -> None:
        self.authorize("resident-guidance")
        with patch.object(self, "credential", side_effect=RuntimeError("synthetic")):
            with self.assertRaises(RuntimeError):
                self.advisor().answer(Topic.STATUS, CASE, resident_key("C-1"))
        self.assertEqual(self.sent, 0)
        call_join(
            self, self.everything(), "resident-guidance", outcome="provider-unavailable", held=True
        )
        self.assertEqual(self.records("output"), [])

    def test_configured_advisor_builds_meters_from_a_supplied_ledger(self) -> None:
        self.authorize("resident-guidance")
        env = {
            "ZF_DEMO_ASSISTANT_ENABLED": "true",
            "ZF_DEMO_ASSISTANT_ENDPOINT": ENDPOINT,
            "ZF_SQL_CLIENT_ID": "synthetic-client",
        }
        ledger = AdvisorLedger(
            self.ledger, MODEL, CONFIG, {kind: PROMPT for kind in ADVISOR_CAPABILITIES}
        )
        with patch("zava_forward.api.resident_demo.aoai.ManagedIdentityCredential") as identity:
            identity.return_value.get_token.return_value.token = "FAKE-TOKEN"
            advisor = configured_advisor(env, Mock(), ledger=ledger)
            with self.assertRaises(ValueError):
                configured_advisor(env, Mock(), ledger=ledger, meters={})
        assert advisor is not None
        self.assertEqual(set(advisor.meters or {}), set(ADVISOR_CAPABILITIES))
        advisor.accounting = self.accounting
        advisor.clock = lambda: EXPIRES - 10
        advisor.transport = lambda url, payload, token: advisor_reply(dict(COUNTS, **CACHED))
        advisor.answer(Topic.STATUS, CASE, resident_key("C-1"))
        call_join(self, self.everything(), "resident-guidance", outcome="returned", held=False)

    def test_each_request_kind_needs_a_prompt_version(self) -> None:
        with self.assertRaises(ValueError):
            advisor_meters(
                self.ledger, model=MODEL, configuration=CONFIG, prompts={"guidance": PROMPT}
            )


if __name__ == "__main__":
    unittest.main()
