"""Issue #104 criterion 5: no billable capability beyond the exercise without bounds, alert."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from test_ai_consumption import CONFIG, END, MODEL, START, Port
from zava_forward.core.ai_consumption import (
    SCHEMA,
    CallContext,
    Consumption,
    DispatchHeld,
    reference,
)

OWNER = "approving-owner-fixture"


class NonExerciseBounds(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.port = Port(Path(temp.name) / "bounds.sqlite")
        self.ledger = Consumption(self.port)
        self.billable = self.price(synthetic=False)

    def price(self, **changes: Any) -> str:
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
        return str(self.ledger.price(**fields))

    def authorize(self, limits: dict[str, Any] | None = None, **changes: Any) -> str:
        budget = dict(id=reference("period"), calls=2, tokens=5000, amount="1")
        budget.update(limits or {})
        fields: dict[str, Any] = dict(
            authority="beyond-exercise-authority",
            owner=OWNER,
            evidence="owner-approved-fixture",
            price=self.billable,
            capability="assessment",
            configuration=CONFIG,
            start=START,
            end=END,
            max_calls=2,
            max_depth=1,
            budgets=[budget],
            alert="alert-rule-ai-limits",
            alert_owner="alert-owner-fixture",
        )
        fields.update(changes)
        return str(self.ledger.authorize(**fields))

    def context(self, attempt: str) -> CallContext:
        return CallContext(
            root=reference("root"),
            attempt=reference(attempt),
            capability="assessment",
            case_type="retrofit-case",
            configuration=CONFIG,
            prompt=reference("template-v1"),
        )

    def records(self, kind: str) -> list[dict[str, Any]]:
        with self.port.transaction() as db:
            return [r for r in self.ledger._read(db) if r["kind"] == kind]

    def test_unbounded_or_unowned_authority_is_refused(self) -> None:
        cases: list[dict[str, Any]] = [
            dict(limits=dict(calls=0)),
            dict(limits=dict(tokens=0)),
            dict(limits=dict(amount="0")),
            dict(owner="   "),
            dict(alert=None),
            dict(alert="  "),
            dict(alert_owner=None),
            dict(alert_owner=""),
        ]
        for changes in cases:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.authorize(**changes)
        self.assertEqual(self.records("authority"), [])

    def test_legacy_billable_authority_without_alert_is_held_with_zero_reservations(self) -> None:
        with self.port.transaction() as db:
            body = dict(
                id=reference("legacy"),
                owner=reference(OWNER),
                evidence=reference("legacy-evidence"),
                price=self.billable,
                capability="assessment",
                configuration=CONFIG,
                start=float(self.port.clock - 60),
                end=float(self.port.clock + 60),
                budgets=[dict(id=reference("p"), calls=2, tokens=5000, amount="1")],
                max_calls=2,
                max_depth=1,
            )
            self.port.event(db, "ai-consumption", schema=SCHEMA, kind="authority", **body)
        with self.assertRaises(DispatchHeld) as held:
            self.ledger.reserve(self.context("legacy"), MODEL, 100, 10, live=True)
        self.assertEqual(str(held.exception), "alert-unowned")
        self.assertEqual(self.records("reserved"), [])
        self.assertEqual(self.records("alert")[-1]["reason"], "alert-unowned")

    def test_bounded_owned_authority_admits_then_denies_when_exhausted(self) -> None:
        self.authorize(limits=dict(calls=1))
        self.ledger.reserve(self.context("first"), MODEL, 100, 10, live=True)
        with self.assertRaises(DispatchHeld) as held:
            self.ledger.reserve(self.context("second"), MODEL, 100, 10, live=True)
        self.assertEqual(str(held.exception), "call-budget-limit")
        self.assertEqual(len(self.records("reserved")), 1)
        alert = self.records("alert")[-1]
        self.assertEqual(alert["owner"], reference("alert-owner-fixture"))

    def test_token_and_money_exhaustion_deny(self) -> None:
        for limits, reason in (
            (dict(tokens=100), "token-budget-limit"),
            (dict(amount="0.000001"), "money-budget-limit"),
        ):
            with self.subTest(reason=reason):
                fresh = NonExerciseBounds()
                fresh.setUp()
                self.addCleanup(fresh.doCleanups)
                fresh.authorize(limits=limits)
                with self.assertRaises(DispatchHeld) as held:
                    fresh.ledger.reserve(fresh.context("only"), MODEL, 100, 10, live=True)
                self.assertEqual(str(held.exception), reason)
                self.assertEqual(fresh.records("reserved"), [])

    def test_exercise_authority_on_synthetic_price_needs_no_alert(self) -> None:
        self.authorize(
            price=self.price(synthetic=True, version="synthetic-v1"), alert=None, alert_owner=None
        )
        self.assertEqual(len(self.records("authority")), 1)
        self.assertNotIn("alert", self.records("authority")[0])


if __name__ == "__main__":
    unittest.main()
