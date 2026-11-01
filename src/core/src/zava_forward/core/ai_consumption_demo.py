"""Credential-free walk-through of the AI consumption ledger on constructed data.

Nothing here is a price, bill, owner approval or paid call; every figure is
synthetic and labelled so.
"""

from __future__ import annotations

import json
import sqlite3
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .ai_consumption import (
    CallContext,
    Consumption,
    DispatchHeld,
    reference,
    timestamp,
)

START = "2026-10-31T00:00:00Z"
END = "2026-11-01T00:00:00Z"
NOW = "2026-10-31T12:00:00Z"
MODEL = "demo-model"
LABEL = "synthetic constructed demo; not a price, invoice, approval or paid call"


class DemoPort:
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


def context(configuration: str, attempt: str) -> CallContext:
    return CallContext(
        root=reference("demo-root"),
        attempt=reference(attempt),
        capability="assessment",
        case_type="retrofit-case",
        configuration=configuration,
        prompt=reference("demo-template-v1"),
    )


def reserve(ledger: Consumption, ctx: CallContext) -> tuple[str | None, str | None]:
    try:
        return ledger.reserve(ctx, MODEL, 1000, 100), None
    except DispatchHeld as error:
        return None, str(error)


def run() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as folder:
        ledger = Consumption(DemoPort(Path(folder) / "demo.sqlite"))
        config = reference("demo-config-v1")
        out: dict[str, Any] = {"evidence_label": LABEL}

        out["without_price_or_authority"] = {
            "dispatch_held": reserve(ledger, context(config, "first"))[1],
            "path": "workflow-only",
        }

        price = ledger.price(
            source="https://prices.azure.com/api/retail/prices",
            source_hash=reference("demo-price-response"),
            retrieved=START,
            version="demo-v1",
            model=MODEL,
            currency="USD",
            start=START,
            end=END,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=True,
        )
        ledger.authorize(
            authority="demo-authority",
            owner="demo-alert-owner",
            evidence="demo-no-paid-spend",
            price=price,
            capability="assessment",
            configuration=config,
            start=START,
            end=END,
            max_calls=2,
            max_depth=2,
            budgets=[dict(id=reference("period"), calls=100, tokens=100000, amount="100")],
        )

        tickets: list[str] = []
        stop = None
        for attempt in ("first", "sibling", "loop"):
            ticket, stop = reserve(ledger, context(config, attempt))
            if ticket is None:
                break
            tickets.append(ticket)
        out["looping_request"] = {
            "model_calls_allowed": len(tickets),
            "stopped_with": stop,
            "path": "workflow-only",
        }

        tokens = dict(prompt_tokens=100, completion_tokens=20, total_tokens=120, cached_tokens=10)
        for ticket in tickets:
            ledger.complete(ticket, tokens, MODEL, "returned")
        ledger.output(reference("demo-root"), "demo-output", eligible=True)
        ledger.review("demo-output", "accept")

        def report() -> dict[str, Any]:
            return ledger.report(start=START, end=END, as_of=END)

        out["report_without_billing"] = report()
        ledger.billing(
            source="demo-bill",
            allocation="demo-exact-allocation",
            budget=reference("period"),
            start=START,
            end=END,
            currency="USD",
            billed="0.000270",
            tolerance="0.01",
            complete=True,
            synthetic=True,
        )
        out["report_with_synthetic_billing"] = report()
        return out


def main() -> None:
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
