"""Resident topic adapter joined to the consumption ledger. Constructed evidence only:
no credentials, no network, no paid call, no resident text."""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from unittest.mock import Mock

from zava_forward.core.ai_consumption import Consumption, reference, timestamp
from zava_forward.core.resident_assistant import AssistantUnavailable, CaseProgress, Topic

from zava_forward.api.resident_demo.aoai import AzureAdvisor, resident_key
from zava_forward.api.resident_demo.assistant import EXPIRES, AzureTopicProvider
from zava_forward.api.resident_demo.ledger_meter import (
    ADVISOR_CAPABILITIES,
    CAPABILITY,
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
            if isinstance(self.response, Exception):
                raise self.response
            return self.response

        return AzureAdvisor(
            ENDPOINT,
            self.accounting,
            lambda: "FAKE-TOKEN",
            transport=transport,
            clock=lambda: EXPIRES - 10,
            meters={k: m for k, m in meters.items() if k in kinds} if metered else None,
        )

    def records(self, kind: str) -> list[dict[str, Any]]:
        with self.port.transaction() as db:
            rows: list[dict[str, Any]] = self.ledger._read(db)
        return [r for r in rows if r["kind"] == kind]

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

    def test_each_request_kind_needs_a_prompt_version(self) -> None:
        with self.assertRaises(ValueError):
            advisor_meters(
                self.ledger, model=MODEL, configuration=CONFIG, prompts={"guidance": PROMPT}
            )


if __name__ == "__main__":
    unittest.main()
