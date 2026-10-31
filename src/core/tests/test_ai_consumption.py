"""Constructed ledger evidence only: no credentials, private data or paid calls."""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
import uuid
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from unittest.mock import patch

from zava_forward.core.ai_consumption import (
    COMPONENTS,
    QUALITY,
    CallContext,
    Consumption,
    DispatchHeld,
    amount,
    reference,
    timestamp,
    usage,
)

START = "2026-10-31T00:00:00Z"
END = "2026-11-01T00:00:00Z"
NOW = "2026-10-31T12:00:00Z"
CONFIG = reference("constructed-config-v1")
MODEL = "test-model"


class Port:
    sql = True
    mssql = False

    def __init__(self, path: Path) -> None:
        self.path = path
        self.clock = timestamp(NOW)
        with self.transaction() as db:
            db.execute(
                "CREATE TABLE assistant_events "
                "(id TEXT PRIMARY KEY, task_id TEXT, at REAL, body TEXT)"
            )
            for action in ("UPDATE", "DELETE"):
                db.execute(
                    f"CREATE TRIGGER immutable_{action} BEFORE {action} ON assistant_events "
                    "BEGIN SELECT RAISE(ABORT, 'append-only'); END"
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


class ConsumptionTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.port = Port(Path(temp.name) / "constructed.sqlite")
        self.ledger = Consumption(self.port)
        self.price_id = self.add_price()

    def add_price(self, **changes: Any) -> str:
        fields: dict[str, Any] = dict(
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
            synthetic=True,
        )
        fields.update(changes)
        return self.ledger.price(**fields)

    def authorize(self, **changes: Any) -> str:
        fields: dict[str, Any] = dict(
            authority="constructed-authority",
            owner="constructed-finance-owner",
            evidence="constructed-no-paid-spend",
            price=self.price_id,
            capability="assessment",
            configuration=CONFIG,
            start=START,
            end=END,
            max_calls=2,
            max_depth=2,
            budgets=[
                dict(id=reference("period"), calls=100, tokens=100000, amount="100"),
                dict(id=reference("task"), calls=100, tokens=100000, amount="100"),
            ],
        )
        fields.update(changes)
        return self.ledger.authorize(**fields)

    def context(self, attempt: str = "first", **changes: Any) -> CallContext:
        fields: dict[str, Any] = dict(
            root=reference("root"),
            attempt=reference(attempt),
            capability="assessment",
            case_type="retrofit-case",
            configuration=CONFIG,
            prompt=reference("template-v1"),
        )
        fields.update(changes)
        return CallContext(**fields)

    def complete(self, rid: str, **changes: Any) -> None:
        tokens = dict(prompt_tokens=100, completion_tokens=20, total_tokens=120, cached_tokens=10)
        tokens.update(changes)
        self.ledger.complete(rid, tokens, MODEL, "returned")

    def report(self, **fields: Any) -> dict[str, Any]:
        return self.ledger.report(start=START, end=END, as_of=END, **fields)

    def records(self) -> list[dict[str, Any]]:
        with self.port.transaction() as db:
            return self.ledger._read(db)

    def accepted(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.complete(ticket)
        self.ledger.output(reference("root"), "output-one", eligible=True)
        self.ledger.review("output-one", "accept")

    def bill(self, **changes: Any) -> str:
        fields: dict[str, Any] = dict(
            source="constructed-bill",
            allocation="constructed-exact-allocation",
            budget=reference("period"),
            start=START,
            end=END,
            currency="USD",
            billed="0.000135",
            tolerance="0.01",
            complete=True,
            synthetic=True,
        )
        fields.update(changes)
        return self.ledger.billing(**fields)

    def test_usage_absent_cached_zero_and_invalid_are_distinct(self) -> None:
        base = dict(prompt_tokens=10, completion_tokens=2, total_tokens=12)
        absent = usage(base)
        zero = usage(base | {"cached_tokens": 0})
        cached = usage(base | {"prompt_tokens_details": {"cached_tokens": 3}})
        assert absent is not None and zero is not None and cached is not None
        self.assertIsNone(absent["cached_tokens"])
        self.assertEqual(zero["cached_tokens"], 0)
        self.assertEqual(cached["cached_tokens"], 3)
        for fields in (
            {"cached_tokens": 11},
            {"cached_tokens": True},
            {"total_tokens": 13},
            {"prompt_tokens": True},
            {"completion_tokens": -1},
        ):
            with self.subTest(fields=fields):
                self.assertIsNone(usage(base | fields))

    def test_loop_fanout_exact_calls_depth_and_owned_workflow_stop(self) -> None:
        self.authorize()
        calls = 0
        for attempt in ("first", "sibling", "loop"):
            try:
                rid = self.ledger.reserve(self.context(attempt), MODEL, 1000, 100)
            except DispatchHeld as error:
                self.assertEqual(str(error), "request-call-limit")
                break
            calls += 1
            self.complete(rid)
        self.assertEqual(calls, 2)
        with self.assertRaisesRegex(DispatchHeld, "request-depth-limit"):
            self.ledger.reserve(self.context("deep", root=reference("other"), depth=3), MODEL, 1, 1)
        alerts = [r for r in self.records() if r["kind"] == "alert"]
        self.assertEqual(alerts[-1]["route"], "workflow-only")
        self.assertEqual(alerts[-1]["owner"], reference("constructed-finance-owner"))

    def test_independent_budgets_and_concurrent_last_slot(self) -> None:
        self.authorize(
            budgets=[
                dict(id=reference("period"), calls=1, tokens=100000, amount="100"),
                dict(id=reference("task"), calls=10, tokens=100000, amount="100"),
            ]
        )

        def reserve(i: int) -> bool:
            try:
                self.ledger.reserve(self.context(str(i), root=reference(str(i))), MODEL, 1000, 100)
                return True
            except DispatchHeld:
                return False

        with ThreadPoolExecutor(max_workers=4) as pool:
            self.assertEqual(sum(pool.map(reserve, range(4))), 1)
        self.assertEqual(len([r for r in self.records() if r["kind"] == "reserved"]), 1)

    def test_duplicate_attempt_and_completion_never_reauthorise(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        with self.assertRaisesRegex(DispatchHeld, "duplicate-attempt"):
            self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.complete(ticket)
        self.complete(ticket, cached_tokens=0)
        self.assertEqual(len([r for r in self.records() if r["kind"] == "completed"]), 1)

    def test_restart_immutable_authority_and_budget_no_reset(self) -> None:
        aid = self.authorize()
        self.assertEqual(aid, self.authorize())
        for changes in (
            {"max_calls": 3},
            {"end": "2027-01-01T00:00:00Z"},
            {"authority": "replacement"},
            {
                "authority": "replacement",
                "budgets": [dict(id=reference("period"), calls=101, tokens=100000, amount="100")],
            },
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.authorize(**changes)

    def test_expiry_unknown_price_and_image_liability_stop(self) -> None:
        self.authorize()
        with self.assertRaisesRegex(DispatchHeld, "price-unknown"):
            self.ledger.reserve(self.context("live-synthetic"), MODEL, 1000, 100, live=True)
        for model, bound, reason in (
            ("other-model", 1000, "price-unknown"),
            (MODEL, None, "liability-unknown"),
        ):
            with self.subTest(reason=reason), self.assertRaisesRegex(DispatchHeld, reason):
                self.ledger.reserve(self.context(reason), model, bound, 100)
        self.port.clock = timestamp(END)
        with self.assertRaisesRegex(DispatchHeld, "authority-expired"):
            self.ledger.reserve(self.context(), MODEL, 1000, 100)

    def test_token_and_money_limits_exact_boundary(self) -> None:
        self.authorize(
            budgets=[dict(id=reference("period"), calls=10, tokens=1100, amount="0.0012")]
        )
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.complete(ticket)
        with self.assertRaisesRegex(DispatchHeld, "token-budget-limit"):
            self.ledger.reserve(self.context("next", root=reference("next")), MODEL, 1000, 100)
        self.assertEqual(len([r for r in self.records() if r["kind"] == "authority"]), 1)

    def test_pre_network_expiry_future_price_and_visible_denial_alert(self) -> None:
        self.authorize(price=self.add_price(retrieved="2026-10-31T13:00:00Z"))
        with self.assertRaisesRegex(DispatchHeld, "price-unknown"):
            self.ledger.reserve(self.context(), MODEL, 1, 1)
        result = self.report()
        self.assertEqual(result["calls"], 0)
        self.assertEqual(result["owned_alerts"][0]["reason"], "price-unknown")
        self.port.clock = timestamp("2026-10-31T14:00:00Z")
        ticket = self.ledger.reserve(self.context(), MODEL, 1, 1)
        self.port.clock = timestamp(END)
        with self.assertRaisesRegex(DispatchHeld, "authority-expired"):
            self.ledger.dispatch_check(ticket)

    def test_shared_budget_rejects_cross_currency_authority(self) -> None:
        self.authorize()
        with self.assertRaisesRegex(ValueError, "currencies"):
            self.authorize(
                authority="other-currency",
                configuration=reference("other-config"),
                price=self.add_price(currency="GBP"),
            )

    def test_exact_budget_comparison_and_thirty_decimal_charge(self) -> None:
        budget = "10000000000000000000000000000000"
        budgets = [dict(id=reference("period"), calls=100, tokens=10**12, amount=budget)]
        self.authorize(
            price=self.add_price(input_rate=budget, output_rate="0", cached_rate="0"),
            budgets=budgets,
        )
        ticket = self.ledger.reserve(self.context(), MODEL, 1000000, 0)
        self.ledger.complete(
            ticket,
            dict(prompt_tokens=1000000, completion_tokens=0, total_tokens=1000000, cached_tokens=0),
            MODEL,
            "returned",
        )
        tiny_price = self.add_price(
            input_rate="0.000000000000000000000001", output_rate="0", cached_rate="0"
        )
        tiny_config = reference("tiny-config")
        self.authorize(
            authority="tiny-authority", price=tiny_price, configuration=tiny_config, budgets=budgets
        )
        with self.assertRaisesRegex(DispatchHeld, "money-budget-limit"):
            self.ledger.reserve(
                self.context("tiny", root=reference("tiny"), configuration=tiny_config), MODEL, 1, 0
            )
        self.authorize(
            authority="independent-tiny",
            price=tiny_price,
            configuration=reference("fresh-config"),
            budgets=[dict(id=reference("fresh-budget"), calls=1, tokens=2, amount="1")],
        )
        ticket = self.ledger.reserve(
            self.context("fresh", root=reference("fresh"), configuration=reference("fresh-config")),
            MODEL,
            1,
            0,
        )
        self.ledger.complete(
            ticket,
            dict(prompt_tokens=1, completion_tokens=0, total_tokens=1, cached_tokens=0),
            MODEL,
            "returned",
        )
        completed = next(
            r for r in self.records() if r["kind"] == "completed" and r["id"] == ticket
        )
        self.assertEqual(completed["charge"], "0.000000000000000000000000000001")
        self.assertTrue(self.report()["projected_token_charge"].endswith("000000000001"))

    def test_unknown_and_overrun_liabilities_are_sticky_across_restart(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.complete(ticket, cached_tokens=None)
        restarted = Consumption(self.port)
        with self.assertRaisesRegex(DispatchHeld, "liability-unknown"):
            restarted.reserve(self.context("retry", retry=1), MODEL, 1000, 100)
        self.assertEqual(self.report()["unknown_liabilities"], 1)

    def test_timeout_late_completion_preserves_hold_and_no_refund(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.ledger.complete(ticket, None, None, "timeout")
        self.complete(ticket)
        self.assertTrue(next(r for r in self.records() if r["kind"] == "completed")["held"])
        with self.assertRaisesRegex(DispatchHeld, "liability-unknown"):
            self.ledger.reserve(self.context("after-timeout"), MODEL, 1000, 100)

    def test_stale_reservation_cannot_dispatch_or_clear_its_hold(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.port.clock += 40
        with self.assertRaisesRegex(DispatchHeld, "liability-unknown"):
            self.ledger.dispatch_check(ticket)
        self.complete(ticket)
        self.assertTrue(next(r for r in self.records() if r["kind"] == "completed")["held"])
        with self.assertRaisesRegex(DispatchHeld, "liability-unknown"):
            self.ledger.reserve(self.context("late-retry"), MODEL, 1000, 100)

    def test_known_overrun_records_actual_charge_and_alert(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 100, 20)
        self.complete(ticket, prompt_tokens=200, total_tokens=220)
        completed = next(r for r in self.records() if r["kind"] == "completed")
        self.assertEqual(completed["charge"], "0.000235")
        self.assertTrue(
            any(r["kind"] == "alert" and r["reason"] == "liability-overrun" for r in self.records())
        )

    def test_metadata_canaries_and_historical_output_not_exported(self) -> None:
        self.accepted()
        with self.port.transaction() as db:
            self.port.event(db, "old-task", kind="completed", output="PRIVATE-CASE-CANARY")
        body = json.dumps(self.report())
        self.assertNotIn("PRIVATE-CASE-CANARY", body)
        for context in (
            self.context(capability="PRIVATE CASE CONTENT"),
            self.context(configuration="not-a-hash"),
            self.context(depth=True),
        ):
            with self.assertRaises(ValueError):
                self.ledger.reserve(context, MODEL, 1000, 100)
        with self.port.transaction() as db, self.assertRaises(sqlite3.IntegrityError):
            db.execute("DELETE FROM assistant_events")

    def test_scan_overflow_never_truncates_budgets(self) -> None:
        with patch("zava_forward.core.ai_consumption.MAX_EVENTS", 0):
            with self.assertRaisesRegex(DispatchHeld, "meter-capacity-reached"):
                self.ledger.reserve(self.context(), MODEL, 1000, 100)

    def test_decimal_validation_and_unreconciled_zero_denominator(self) -> None:
        invalid: list[Any] = ["NaN", "-1", "Infinity", "1e3", 0.1, "0." + "1" * 25]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                amount(value)
        self.authorize()
        rid = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.complete(rid)
        self.ledger.output(reference("root"), "fallback", eligible=False)
        self.ledger.review("fallback", "accept")
        self.bill()
        result = self.report()
        self.assertEqual(result["accepted_proposals"], 0)
        self.assertEqual(result["cost_per_accepted_proposal"], "Unknown")
        self.assertEqual(result["quality_status"], "Unknown")

    def test_billing_is_financial_source_not_projection(self) -> None:
        self.accepted()
        self.assertEqual(self.report()["token_cost"], "Unknown")
        self.bill(billed="0.000200", synthetic=False)
        result = self.report()
        self.assertEqual(result["token_cost"], "0.000200")
        self.assertEqual(result["projected_token_charge"], "0.000135")
        self.assertEqual(result["cost_per_accepted_proposal"], "0.000200")
        self.assertEqual(result["reconciliation"], "variance-alert")
        self.assertEqual(result["evidence_label"], "synthetic")

    def test_duplicate_overlap_partial_currency_billing_fail_closed(self) -> None:
        self.accepted()
        self.bill(complete=False, currency="GBP")
        self.assertEqual(self.report()["token_cost"], "Unknown")
        with self.assertRaisesRegex(ValueError, "Duplicate/overlapping"):
            self.bill(source="second")

    def test_retries_count_all_attempts_and_accept_once(self) -> None:
        self.authorize()
        for i in range(2):
            ticket = self.ledger.reserve(self.context(str(i), retry=i), MODEL, 1000, 100)
            self.complete(ticket)
        self.ledger.output(reference("root"), "one", eligible=True)
        self.ledger.output(reference("root"), "one", eligible=True)
        self.ledger.review("one", "edit-accept")
        self.ledger.review("one", "edit-accept")
        result = self.report()
        self.assertEqual(result["calls"], 2)
        self.assertEqual(result["retries"], 1)
        self.assertEqual(result["accepted_proposals"], 1)
        self.assertEqual(result["projected_token_charge"], "0.000270")

    def test_unjoined_and_failed_review_are_not_accepted(self) -> None:
        self.authorize()
        ticket = self.ledger.reserve(self.context(), MODEL, 1000, 100)
        self.complete(ticket)
        with self.assertRaises(ValueError):
            self.ledger.review("lost-output", "accept")
        self.bill()
        result = self.report()
        self.assertEqual(result["unjoined_outputs"], 1)
        self.assertEqual(result["token_cost"], "Unknown")
        self.assertEqual(result["accepted_proposals"], 0)

    def test_quality_regression_fails_even_when_cheaper_and_capacity_not_cash(self) -> None:
        self.accepted()
        self.bill()
        metrics = {k: dict(count=0, denominator=10, floor="0.1", baseline="0") for k in QUALITY}
        metrics["critical_misses"]["count"] = 1
        result = self.report(
            quality=dict(approved=True, cohort=self.report()["cohort"], metrics=metrics),
            components={k: "1" for k in COMPONENTS},
            capacity_hours="4",
        )
        self.assertEqual(result["quality_status"], "Failure")
        self.assertEqual(result["quality_qualified_cost"], "Unknown")
        self.assertEqual(result["total_cost_of_ai"], "5.000135")
        self.assertEqual(result["capacity_hours"], "4")
        self.assertEqual(result["cash_value"], "Unknown")

    def test_unapproved_or_mismatched_quality_never_qualifies_cost(self) -> None:
        self.accepted()
        self.bill()
        metrics = {k: dict(count=0, denominator=10, floor="0", baseline="0") for k in QUALITY}
        self.assertEqual(
            self.report(
                quality=dict(approved=False, cohort=self.report()["cohort"], metrics=metrics)
            )["quality_status"],
            "Unknown",
        )
        with self.assertRaises(ValueError):
            self.report(quality=dict(approved=True, cohort=reference("other"), metrics=metrics))

    def test_exclusive_call_period_and_late_review(self) -> None:
        self.accepted()
        self.port.clock = timestamp(END)
        self.ledger.output(reference("other"), "late-output", eligible=True)
        self.assertEqual(self.report()["calls"], 1)
        self.assertEqual(self.report()["accepted_proposals"], 1)
        with self.assertRaises(ValueError):
            self.ledger.report(start=START, end=END, as_of=NOW)


if __name__ == "__main__":
    unittest.main()
