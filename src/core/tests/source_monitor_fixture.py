"""Wholly synthetic local sources and simulated owner decisions; not law or real approval."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core import lawstore, rulecards
from zava_forward.core.source_monitor import EXERCISE_OWNER, SourceMonitor

DAY = "2026-10-16"
EFFECTIVE = "2026-10-18"
RAW = b"# Synthetic exercise\nThis is constructed text, not law.\n"
SOURCE = "synthetic-monitor"
CARD = "synthetic-review-card"
PID = SOURCE + "@v1#0001"
IMPACT = dict(
    requirements=["EXERCISE-REQ"],
    journeys=["Exercise handover"],
    tests=["synthetic-regression"],
    communications=["Exercise staff briefing"],
)


class MonitorFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "law.sqlite"
        self.blobs = Path(self.tmp.name) / "blobs"
        self.law: Any = lawstore.LawStore(self.path, self.blobs)
        self.addCleanup(lambda: self.law.close())
        self.add_source()
        self.card(activate=True, effective="2026-01-01")
        self.monitor = SourceMonitor(self.law)
        self.configure()

    def add_source(self, source_id: str = SOURCE, **overrides: Any) -> None:
        source = dict(
            status="guidance",
            effective="2026-01-01",
            retrieved="2026-01-01",
            reviewed="2026-01-01",
            review_status="reviewed",
            completeness="full",
        )
        source.update(overrides)
        with self.law.transaction():
            self.law.sql.run(
                "INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)",
                (
                    source_id,
                    "SYNTHETIC: constructed test source, not law",
                    "https://example.test",
                    "exercise",
                    "exercise",
                    EXERCISE_OWNER,
                    "High",
                    "weekly",
                    "synthetic.md",
                ),
            )
            blob = self.law._write_blob(source_id, 1, lawstore.sha256(RAW), RAW)
            self.law.sql.run(
                "INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    source_id,
                    1,
                    source["status"],
                    source["effective"],
                    source["retrieved"],
                    source["reviewed"],
                    source["review_status"],
                    lawstore.sha256(RAW),
                    blob,
                    "ok",
                    source["completeness"],
                    "SYNTHETIC reviewed fixture, no legal approval",
                ),
            )
            self.law.sql.run(
                "INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)",
                (
                    source_id + "@v1#0001",
                    source_id,
                    1,
                    1,
                    "SYNTHETIC fixture",
                    RAW.decode(),
                    lawstore.sha256(RAW),
                ),
            )
        self.law.rebuild_index()

    def card(
        self,
        card_id: str = CARD,
        *,
        activate: bool = False,
        effective: str = EFFECTIVE,
        **overrides: Any,
    ) -> int:
        fields = dict(
            title="SYNTHETIC decision safeguard",
            trigger="Constructed significant decision",
            applicability="Exercise only",
            provisions=[PID],
            clock="No clock",
            safe_default="Ask the named human owner",
            escalation_role="Exercise Legal owner",
            approver=EXERCISE_OWNER,
            effective=effective,
            check=dict(kind="automated-decision-safeguard"),
        )
        fields.update(overrides)
        version: int = self.law.rules.propose(
            card_id, "Synthetic exercise author", rulecards.AUTHOR, today=DAY, **fields
        )
        self.law.rules.approve(card_id, version, EXERCISE_OWNER, rulecards.OWNER, DAY)
        if activate:
            self.law.rules.activate(card_id, version, EXERCISE_OWNER, rulecards.OWNER, DAY)
        return version

    def configure(self, **overrides: Any) -> int:
        fields: dict[str, Any] = dict(
            cadence_days=7,
            likelihood="High",
            rationale="Exercise weekly pending-commencement map",
            impact=IMPACT,
            actor=EXERCISE_OWNER,
            role=rulecards.OWNER,
        )
        fields.update(overrides)
        return int(self.monitor.configure(SOURCE, **fields))

    def observe(self, **overrides: Any) -> str:
        fields: dict[str, Any] = dict(
            today=DAY,
            content=RAW + b"Discovery addition, not law.\n",
            metadata=dict(effective=EFFECTIVE, complete=True),
            provenance="Local exercise publication fixture",
            method="scraping",
        )
        fields.update(overrides)
        cid = self.monitor.observe(SOURCE, **fields)
        assert cid is not None
        return str(cid)

    def approve(self, cid: str, **overrides: Any) -> int:
        fields: dict[str, Any] = dict(
            actor=EXERCISE_OWNER,
            role=rulecards.OWNER,
            today=DAY,
            provenance_review="SIMULATED provenance review of the local fixture",
            completeness_review="SIMULATED completeness review of the local fixture",
            interpretation="SIMULATED human interpretation, not law",
            notification="Draft exercise staff briefing; nothing sent",
            rollback="Restore the captured prior active exercise cards",
            targets={CARD: 2},
            effective=EFFECTIVE,
            cases=[
                dict(
                    test_id="synthetic-regression",
                    card_id=CARD,
                    facts=dict(automated_decisions=[]),
                    expected=["not applicable"],
                )
            ],
        )
        fields.update(overrides)
        return int(self.monitor.approve(cid, **fields))

    def ready(self) -> str:
        cid = self.observe()
        self.card()
        self.approve(cid)
        self.monitor.regress(cid, today=DAY)
        return cid

    def activate(self, cid: str, **overrides: Any) -> None:
        fields = dict(actor=EXERCISE_OWNER, role=rulecards.OWNER, today=EFFECTIVE)
        fields.update(overrides)
        self.monitor.activate(cid, **fields)

    def rollback(self, cid: str, **overrides: Any) -> None:
        fields = dict(
            actor=EXERCISE_OWNER,
            role=rulecards.OWNER,
            today=EFFECTIVE,
            reason="SIMULATED exercise reversal",
        )
        fields.update(overrides)
        self.monitor.rollback(cid, **fields)
