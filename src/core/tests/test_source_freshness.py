"""Read-only cadence labels do not confer source authority or suppress safety checks."""

from __future__ import annotations

import json
import tempfile
import unittest
from typing import Any

from regulatory_fixture import PID, QUOTE, Fixture
from zava_forward.core import rulecards
from zava_forward.core.source_monitor import (
    SourceMonitor,
    card_freshness,
    dated_card,
    source_freshness,
)


class FreshnessTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.f = Fixture(temp.name)
        self.addCleanup(self.f.close)
        self.law = self.f.law
        self.law.blobs.put("none", QUOTE.encode())
        self.card = self.law.rules.history("synthetic-hazard")[0]

    def monitor(self) -> Any:
        monitor = SourceMonitor(self.law)
        monitor.configure(
            "synthetic",
            cadence_days=7,
            likelihood="High",
            rationale="Synthetic weekly fixture",
            impact=dict(requirements=[], journeys=[], tests=[], communications=[]),
            actor="Juan Manuel Servera",
            role=rulecards.OWNER,
        )
        return monitor

    def observe(self, monitor: Any, day: str, *, fail: bool = False) -> None:
        monitor.observe(
            "synthetic",
            today=day,
            content=None if fail else QUOTE.encode(),
            metadata={},
            provenance="Constructed local snapshot, not legal evidence",
            method="local-fixture",
            error="Synthetic retrieval failure" if fail else None,
        )

    def test_missing_monitor_tables_unknown_without_schema_mutation(self) -> None:
        before = self.law.sql.all("SELECT name FROM sqlite_master ORDER BY name")
        result = card_freshness(self.law, self.card, "2026-10-16")
        self.assertEqual(result["status"], "unknown")
        self.assertEqual(before, self.law.sql.all("SELECT name FROM sqlite_master ORDER BY name"))
        self.assertEqual(self.law.rules.history("synthetic-hazard")[0], self.card)

    def test_unconfigured_missing_and_failed_observations_are_unknown(self) -> None:
        SourceMonitor(self.law)
        self.assertEqual(source_freshness(self.law, "synthetic", "2026-10-16")["status"], "unknown")
        monitor = self.monitor()
        self.assertEqual(source_freshness(self.law, "synthetic", "2026-10-16")["status"], "unknown")
        self.observe(monitor, "2026-10-16", fail=True)
        self.assertEqual(source_freshness(self.law, "synthetic", "2026-10-16")["status"], "unknown")

    def test_due_boundary_and_failed_attempt_do_not_refresh_success(self) -> None:
        monitor = self.monitor()
        self.observe(monitor, "2026-10-09")
        self.assertFalse(monitor.due("synthetic", "2026-10-15"))
        self.assertEqual(card_freshness(self.law, self.card, "2026-10-15")["status"], "in_cadence")
        self.observe(monitor, "2026-10-16", fail=True)
        overdue = card_freshness(self.law, self.card, "2026-10-16")
        self.assertTrue(monitor.due("synthetic", "2026-10-16"))
        self.assertEqual(overdue["status"], "out_of_cadence")
        self.assertEqual(overdue["sources"][0]["last_success"], "2026-10-09")
        self.assertEqual(overdue["sources"][0]["due_on"], "2026-10-16")
        self.assertIn("out of monitoring cadence", overdue["label"])
        self.observe(monitor, "2026-10-17")
        self.assertEqual(card_freshness(self.law, self.card, "2026-10-17")["status"], "in_cadence")

    def test_future_failed_attempt_prevents_in_cadence_label(self) -> None:
        monitor = self.monitor()
        self.observe(monitor, "2026-10-15")
        self.observe(monitor, "2026-10-17", fail=True)
        result = source_freshness(self.law, "synthetic", "2026-10-16")
        self.assertEqual(result["status"], "unknown")
        self.assertIn("clock precedes", result["reason"])

    def test_card_reduction_mixed_missing_and_empty_sources(self) -> None:
        monitor = self.monitor()
        self.observe(monitor, "2026-10-09")
        mixed = dict(self.card, provisions=[PID, "missing@v1#0001"])
        self.assertEqual(card_freshness(self.law, mixed, "2026-10-16")["status"], "out_of_cadence")
        self.assertEqual(card_freshness(self.law, mixed, "2026-10-15")["status"], "unknown")
        self.assertEqual(
            card_freshness(self.law, dict(provisions=[]), "2026-10-15")["status"], "unknown"
        )

    def test_labels_do_not_modify_card_state_or_approval(self) -> None:
        monitor = self.monitor()
        self.observe(monitor, "2026-10-09")
        before = json.dumps(self.law.rules.history("synthetic-hazard"), sort_keys=True)
        decorated = dated_card(self.law, self.card, "2026-10-16")
        self.assertEqual(decorated["source_freshness"]["status"], "out_of_cadence")
        self.assertEqual(
            json.dumps(self.law.rules.history("synthetic-hazard"), sort_keys=True), before
        )
        self.assertEqual(self.law.rules.is_active("synthetic-hazard", "2026-10-16"), 1)


if __name__ == "__main__":
    unittest.main()
