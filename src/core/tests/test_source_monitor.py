"""Offline monitoring contract; all source text and approval evidence are synthetic."""

from __future__ import annotations

import copy
import json
import sqlite3
import threading
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from source_monitor_fixture import CARD, DAY, EFFECTIVE, IMPACT, RAW, SOURCE, MonitorFixture
from zava_forward.core import lawstore, rule_engine, rulecards
from zava_forward.core.source_monitor import (
    EXERCISE_OWNER,
    LABEL,
    MSSQL_DDL,
    TABLES,
    SourceMonitor,
)


class SourceMonitorTests(MonitorFixture):
    def test_detection_is_idempotent_unverified_and_does_not_change_law_or_cards(self) -> None:
        before = self.law.rules.history(CARD)
        sources, search = self.law.sources(), self.law.search("constructed")
        cid = self.observe()
        self.assertEqual(self.observe(), cid)
        changes = self.monitor.changes()
        self.assertEqual(len(changes), 1)
        change = changes[0]
        self.assertEqual(change["id"], cid)
        self.assertFalse(change["verified"])
        self.assertEqual(change["owner"], EXERCISE_OWNER)
        self.assertEqual(change["method"], "scraping")
        self.assertEqual(change["categories"], ["content", "metadata"])
        self.assertIn("+Discovery addition, not law.", change["difference"]["content_diff"])
        self.assertFalse(change["difference"]["truncated"])
        self.assertEqual(change["affected"]["journeys"], IMPACT["journeys"])
        self.assertEqual(change["affected"]["communications"], IMPACT["communications"])
        self.assertEqual(change["affected"]["cards"][CARD], before)
        review = self.law.rules.reviews(CARD)[0]
        self.assertEqual(review["affected"]["candidate_id"], cid)
        self.assertEqual(review["source_version"], 1)
        self.assertEqual(self.law.rules.history(CARD), before)
        self.assertEqual(self.law.sources(), sources)
        self.assertEqual(self.law.search("constructed"), search)
        self.assertEqual(
            self.law.blobs.get(change["candidate_blob"]), RAW + b"Discovery addition, not law.\n"
        )

    def test_unchanged_metadata_only_and_failed_retrieval_are_distinct(self) -> None:
        self.assertIsNone(
            self.monitor.observe(
                SOURCE,
                today=DAY,
                content=RAW,
                metadata={},
                provenance="Exercise unchanged fixture",
            )
        )
        meta = self.observe(content=RAW)
        failed = self.observe(content=None, metadata={}, error="Exercise retrieval failed")
        changes = {c["id"]: c for c in self.monitor.changes()}
        self.assertEqual(changes[meta]["categories"], ["metadata"])
        self.assertEqual(changes[failed]["categories"], ["retrieval_failure"])
        self.assertIsNone(changes[failed]["candidate_blob"])
        with self.assertRaisesRegex(rulecards.RuleError, "missing or corrupt"):
            self.monitor._fresh(changes[failed])

    def test_exact_source_matching_and_explicit_unmapped_impact(self) -> None:
        self.add_source(SOURCE + "-other")
        self.card("unrelated", provisions=[SOURCE + "-other@v1#0001"])
        cid = self.observe()
        self.assertEqual(list(self.monitor._change(cid)["affected"]["cards"]), [CARD])
        self.assertEqual(len(self.law.rules.reviews()), 1)
        self.monitor.configure(
            SOURCE + "-other",
            cadence_days=30,
            likelihood="Low",
            rationale="Exercise only",
            impact={k: [] for k in IMPACT},
            actor=EXERCISE_OWNER,
            role=rulecards.OWNER,
        )
        other = self.monitor.observe(
            SOURCE + "-other",
            today=DAY,
            content=RAW + b"x",
            metadata={},
            provenance="Local fixture",
        )
        assert other is not None
        self.assertTrue(self.monitor._change(other)["affected"]["unmapped"])

    def test_cadence_is_per_source_and_configuration_is_validated(self) -> None:
        self.assertTrue(self.monitor.due(SOURCE, DAY))
        self.observe()
        self.assertFalse(self.monitor.due(SOURCE, "2026-10-22"))
        self.assertTrue(self.monitor.due(SOURCE, "2026-10-23"))
        revision = self.configure()
        self.assertEqual(revision, self.configure())
        self.configure(cadence_days=1, likelihood="Medium")
        self.assertTrue(self.monitor.due(SOURCE, "2026-10-17"))
        fields: dict[str, Any]
        for fields in (
            dict(cadence_days=0),
            dict(cadence_days=True),
            dict(cadence_days=367),
            dict(likelihood="high"),
            dict(impact={}),
            dict(rationale=""),
            dict(actor="agent"),
            dict(role=rulecards.AUTHOR),
        ):
            with self.subTest(fields=fields), self.assertRaises(rulecards.RuleError):
                self.configure(**fields)
        with self.assertRaisesRegex(rulecards.RuleError, "clock"):
            self.monitor.due(SOURCE, "2026-10-15")

    def test_failed_retrieval_without_success_is_due_next_day(self) -> None:
        for cadence in (30, 366):
            with self.subTest(cadence=cadence):
                self.configure(cadence_days=cadence)
                self.observe(content=None, metadata={}, error="Synthetic retrieval failure")
                self.assertTrue(self.monitor.due(SOURCE, "2026-10-17"))

    def test_failures_preserve_success_cadence_and_successful_retry_resets_it(self) -> None:
        self.configure(cadence_days=30)
        self.monitor.observe(
            SOURCE, today=DAY, content=RAW, metadata={}, provenance="Synthetic unchanged fixture"
        )
        self.observe(today="2026-10-17", content=None, metadata={}, error="Synthetic early failure")
        self.assertFalse(self.monitor.due(SOURCE, "2026-11-14"))
        self.assertTrue(self.monitor.due(SOURCE, "2026-11-15"))
        self.observe(
            today="2026-11-15", content=None, metadata={}, error="Synthetic due-day failure"
        )
        self.assertTrue(self.monitor.due(SOURCE, "2026-11-16"))
        self.observe(
            today="2026-11-16", content=None, metadata={}, error="Synthetic repeated failure"
        )
        self.assertTrue(self.monitor.due(SOURCE, "2026-11-17"))
        self.observe(today="2026-11-17")
        self.assertFalse(self.monitor.due(SOURCE, "2026-11-18"))
        self.assertFalse(self.monitor.due(SOURCE, "2026-12-16"))
        self.assertTrue(self.monitor.due(SOURCE, "2026-12-17"))

    def test_clock_cannot_precede_latest_failed_attempt(self) -> None:
        self.observe(content=None, metadata={}, error="Synthetic retrieval failure")
        with self.assertRaisesRegex(rulecards.RuleError, "clock"):
            self.monitor.due(SOURCE, "2026-10-15")
        self.observe()
        self.observe(today="2026-10-17", content=None, metadata={}, error="Synthetic later failure")
        with self.assertRaisesRegex(rulecards.RuleError, "clock"):
            self.monitor.due(SOURCE, DAY)
        with self.assertRaisesRegex(rulecards.RuleError, "clock"):
            self.observe()

    def test_approval_needs_owner_provenance_complete_impact_and_card_approval(self) -> None:
        cid = self.observe()
        self.card()
        fields: dict[str, Any]
        for fields in (
            dict(actor="agent"),
            dict(role=rulecards.AUTHOR),
            dict(provenance_review=""),
            dict(completeness_review=""),
            dict(interpretation=""),
            dict(notification=""),
            dict(rollback=""),
            dict(targets={}),
            dict(targets={CARD: 999}),
            dict(effective="2026-10-17"),
        ):
            with self.subTest(fields=fields), self.assertRaises(rulecards.RuleError):
                self.approve(cid, **fields)
        self.assertEqual(self.monitor.events(cid), [])
        self.approve(cid)
        self.assertTrue(self.monitor.events(cid)[0]["verified"])
        review = self.law.rules.reviews(CARD)[0]
        self.assertEqual(review["status"], "assessed")
        self.assertEqual(review["assessment"]["actor"], EXERCISE_OWNER)
        self.assertTrue(review["assessment"]["simulated"])

    def test_failed_partial_and_unknown_inventory_cannot_approve(self) -> None:
        self.card()
        fields: dict[str, Any]
        for fields in (
            dict(metadata=dict(complete=False)),
            dict(content=None, metadata={}, error="Retrieval failure"),
        ):
            with self.subTest(fields=fields):
                cid = self.observe(**fields)
                with self.assertRaises(rulecards.RuleError):
                    self.approve(cid)
        self.configure(impact=dict(IMPACT, journeys=[]))
        cid = self.observe()
        with self.assertRaisesRegex(rulecards.RuleError, "inventory"):
            self.approve(cid)

    def test_approval_binds_every_target_and_required_regression_id(self) -> None:
        cid = self.observe()
        self.card()
        valid = dict(
            test_id="synthetic-regression",
            card_id=CARD,
            facts=dict(automated_decisions=[]),
            expected=["not applicable"],
        )
        for cases in (
            [],
            [dict(valid, test_id="wrong")],
            [valid, valid],
            [dict(valid, card_id="wrong")],
            [dict(valid, expected=[])],
            [dict(valid, expected=["compliant"])],
            [dict(valid, command="echo")],
        ):
            with self.subTest(cases=cases), self.assertRaises(rulecards.RuleError):
                self.approve(cid, cases=cases)
        self.approve(cid, cases=[valid])
        valid["expected"] = ["clear"]
        result = self.monitor.regress(cid, today=DAY)
        self.assertTrue(result["passed"])
        self.assertEqual(result["results"][0]["expected"], ["not applicable"])

    def test_regression_requires_approval_and_latest_failure_blocks_activation(self) -> None:
        cid = self.observe()
        self.card()
        with self.assertRaisesRegex(rulecards.RuleError, "approval"):
            self.monitor.regress(cid, today=DAY)
        self.approve(cid)
        with self.assertRaisesRegex(rulecards.RuleError, "regression"):
            self.activate(cid)
        self.assertTrue(self.monitor.regress(cid, today=DAY)["passed"])
        with patch.object(rule_engine, "evaluate", return_value=[dict(result="unknown")]):
            self.assertFalse(self.monitor.regress(cid, today=DAY)["passed"])
        with self.assertRaisesRegex(rulecards.RuleError, "regression"):
            self.activate(cid)
        self.assertEqual(self.law.rules.is_active(CARD, EFFECTIVE), 1)
        self.assertEqual(
            [e["passed"] for e in self.monitor.events(cid) if e["action"] == "regression"],
            [True, False],
        )

    def test_activation_needs_effective_date_owner_and_runtime_eligibility(self) -> None:
        cid = self.ready()
        source = self.law.sources()
        search = self.law.search("constructed")
        before = self.law.rules.history(CARD)
        for fields in (dict(today="2026-10-17"), dict(actor="agent"), dict(role=rulecards.AUTHOR)):
            with self.subTest(fields=fields), self.assertRaises(rulecards.RuleError):
                self.activate(cid, **fields)
            self.assertEqual(self.law.rules.history(CARD), before)
        self.activate(cid)
        self.assertEqual(self.law.rules.is_active(CARD, EFFECTIVE), 2)
        db = sqlite3.connect(":memory:")
        self.addCleanup(db.close)
        db.execute("CREATE TABLE cases (id TEXT PRIMARY KEY, rowversion INT, body TEXT)")
        db.execute(
            "INSERT INTO cases VALUES (?,?,?)",
            (
                "synthetic-case",
                1,
                json.dumps(
                    dict(home_id="synthetic-home", automated_decisions=[], stage="Handover")
                ),
            ),
        )
        store = SimpleNamespace(db=db, lock=threading.RLock())
        output = rule_engine.RuleEngine(self.law).run(
            store, "synthetic-case", now=datetime(2026, 10, 18, 12, tzinfo=UTC)
        )
        check = next(c for c in output["checks"] if c["card_id"] == CARD)
        self.assertEqual(check["result"], "not applicable")
        self.rollback(cid)
        self.assertEqual(self.law.sources(), source)
        self.assertEqual(self.law.search("constructed"), search)

    def test_existing_activate_and_release_cannot_bypass_monitoring(self) -> None:
        self.observe()
        self.card()
        self.card()
        for version in (2, 3):
            with self.assertRaisesRegex(rulecards.RuleError, "monitored"):
                self.law.rules.activate(CARD, version, EXERCISE_OWNER, rulecards.OWNER, EFFECTIVE)
        self.law.rules.hold(CARD, 1, EXERCISE_OWNER, rulecards.OWNER, "Human hold", DAY)
        with self.assertRaisesRegex(rulecards.RuleError, "monitored"):
            self.law.rules.release(CARD, 1, EXERCISE_OWNER, rulecards.OWNER, DAY)

    def test_new_card_joins_review_and_overlapping_source_release_is_fail_closed(self) -> None:
        cid = self.observe()
        self.card("new-joiner")
        with self.assertRaisesRegex(rulecards.RuleError, "monitored"):
            self.law.rules.activate("new-joiner", 1, EXERCISE_OWNER, rulecards.OWNER, EFFECTIVE)
        refreshed = self.observe()
        self.assertNotEqual(refreshed, cid)
        self.assertIn("new-joiner", self.monitor._change(refreshed)["affected"]["cards"])
        self.add_source("second-rule-source")
        self.monitor.configure(
            "second-rule-source",
            cadence_days=7,
            likelihood="High",
            rationale="Exercise overlap",
            impact=IMPACT,
            actor=EXERCISE_OWNER,
            role=rulecards.OWNER,
        )
        from source_monitor_fixture import PID

        self.card(provisions=[PID, "second-rule-source@v1#0001"])
        second = self.monitor.observe(
            "second-rule-source",
            today=DAY,
            content=RAW + b"overlap",
            metadata=dict(complete=True),
            provenance="Exercise second source",
        )
        self.assertIsNotNone(second)
        cases = [
            dict(
                test_id=tid,
                card_id=card,
                facts=dict(automated_decisions=[]),
                expected=["not applicable"],
            )
            for tid, card in (("synthetic-regression", CARD), ("new-joiner-test", "new-joiner"))
        ]
        self.approve(refreshed, targets={CARD: 2, "new-joiner": 1}, cases=cases)
        self.monitor.regress(refreshed, today=DAY)
        before = self.law.rules.history(CARD)
        with self.assertRaisesRegex(rulecards.RuleError, "overlapping changed sources"):
            self.activate(refreshed)
        self.assertEqual(self.law.rules.history(CARD), before)

    def test_owner_hold_cannot_be_superseded_by_monitor_activation(self) -> None:
        cid = self.ready()
        self.law.rules.hold(CARD, 1, EXERCISE_OWNER, rulecards.OWNER, "Human hold", DAY)
        self.approve(cid)
        self.monitor.regress(cid, today=DAY)
        with self.assertRaisesRegex(rulecards.RuleError, "hold"):
            self.activate(cid)
        self.assertEqual(self.law.rules.state(CARD, 1), "held")

    def test_no_change_owner_review_regresses_before_releasing_hold_and_can_restore_it(
        self,
    ) -> None:
        self.law.rules.hold(CARD, 1, EXERCISE_OWNER, rulecards.OWNER, "Source doubt", DAY)
        cid = self.observe()
        self.approve(cid, targets={CARD: 1})
        self.assertEqual(self.law.rules.reviews(CARD)[0]["assessment"]["outcome"], "no_change")
        with self.assertRaisesRegex(rulecards.RuleError, "regression"):
            self.activate(cid)
        self.monitor.regress(cid, today=DAY)
        self.activate(cid)
        self.assertEqual(self.law.rules.is_active(CARD, EFFECTIVE), 1)
        self.rollback(cid)
        self.assertEqual(self.law.rules.state(CARD, 1), "held")

    def test_independent_connection_detection_is_serialized_and_deduplicated(self) -> None:
        other: Any = lawstore.LawStore(self.path, self.blobs)
        self.addCleanup(other.close)
        second = SourceMonitor(other)
        barrier = threading.Barrier(2)
        results: list[str | None] = []
        errors: list[Exception] = []

        def observe(monitor: SourceMonitor) -> None:
            try:
                barrier.wait(timeout=5)
                results.append(
                    monitor.observe(
                        SOURCE,
                        today=DAY,
                        content=RAW + b"Shared fixture change",
                        metadata=dict(complete=True),
                        provenance="Concurrent local fixture",
                    )
                )
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=observe, args=(monitor,)) for monitor in (self.monitor, second)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)
            self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])
        self.assertEqual(len(self.monitor.changes()), 1)

    def test_changes_in_configuration_card_or_engine_invalidate_regression(self) -> None:
        cid = self.ready()
        with patch.object(rule_engine, "ENGINE_VERSION", 999):
            with self.assertRaisesRegex(rulecards.RuleError, "evaluator"):
                self.activate(cid)
        self.card()
        with self.assertRaisesRegex(rulecards.RuleError, "lifecycle"):
            self.activate(cid)
        self.configure(cadence_days=1)
        with self.assertRaisesRegex(rulecards.RuleError, "configuration"):
            self.activate(cid)
        newer = self.observe()
        self.assertNotEqual(cid, newer)

    def test_material_observation_invalidates_after_reversion_but_duplicates_do_not(self) -> None:
        cid = self.ready()
        self.observe()
        self.monitor.regress(cid, today=DAY)
        self.observe(content=RAW + b"different new change")
        self.observe()
        with self.assertRaisesRegex(rulecards.RuleError, "intervening"):
            self.activate(cid)
        self.approve(cid)
        self.monitor.regress(cid, today=DAY)
        self.activate(cid)

    def test_stale_baseline_and_corrupt_snapshot_block_release(self) -> None:
        cid = self.ready()
        blob = self.monitor._change(cid)["candidate_blob"]
        with patch.object(self.law.blobs, "get", return_value=b"corrupt"):
            with self.assertRaisesRegex(rulecards.RuleError, "corrupt"):
                self.activate(cid)
        self.assertTrue(self.law.blobs.get(blob))
        with self.law.transaction():
            row = self.law.source(SOURCE)["versions"][0]
            self.law.sql.run(
                "INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    SOURCE,
                    2,
                    row["status"],
                    row["effective"],
                    DAY,
                    DAY,
                    "reviewed",
                    row["content_hash"],
                    row["blob_path"],
                    "ok",
                    "full",
                    "Synthetic fixture",
                ),
            )
        with self.assertRaisesRegex(rulecards.RuleError, "baseline"):
            self.activate(cid)

    def test_runtime_citation_gate_rejects_missing_partial_unreviewed_and_historical(self) -> None:
        variants: tuple[dict[str, Any], ...] = (
            dict(provisions=["candidate-only@v2#0001"]),
            dict(completeness="partial"),
            dict(review_status="not_reviewed"),
            dict(status="historical"),
            dict(status="consultation"),
        )
        for index, variant in enumerate(variants):
            sid = f"eligibility-{index}"
            self.add_source(sid, **{k: v for k, v in variant.items() if k != "provisions"})
            card = dict(
                provisions=variant.get("provisions", [sid + "@v1#0001"]),
                check=dict(kind="automated-decision-safeguard"),
                effective=DAY,
                retirement=None,
            )
            with (
                self.subTest(variant=variant),
                self.assertRaisesRegex(rulecards.RuleError, "citations"),
            ):
                self.monitor._eligible(card, DAY)

    def test_rollback_restores_prior_version_and_is_owner_only_not_repeatable(self) -> None:
        cid = self.ready()
        self.activate(cid)
        with self.assertRaises(rulecards.RuleError):
            self.rollback(cid, actor="agent")
        with self.assertRaises(rulecards.RuleError):
            self.rollback(cid, reason="")
        self.rollback(cid)
        self.assertEqual(self.law.rules.is_active(CARD, EFFECTIVE), 1)
        self.assertEqual([c["state"] for c in self.law.rules.history(CARD)], ["active", "retired"])
        with self.assertRaisesRegex(rulecards.RuleError, "rollback"):
            self.rollback(cid)
        for event in self.monitor.events(cid):
            self.assertTrue(event["simulated"])
            self.assertEqual(event["label"], LABEL)

    def test_rollback_rejects_intervening_human_hold_or_retirement_or_new_version(self) -> None:
        cid = self.ready()
        self.activate(cid)
        self.law.rules.hold(CARD, 2, EXERCISE_OWNER, rulecards.OWNER, "Human stop", EFFECTIVE)
        with self.assertRaisesRegex(rulecards.RuleError, "intervening"):
            self.rollback(cid)
        self.law.rules.retire(CARD, 2, EXERCISE_OWNER, rulecards.OWNER, EFFECTIVE)
        with self.assertRaises(rulecards.RuleError):
            self.rollback(cid)
        self.card()
        with self.assertRaises(rulecards.RuleError):
            self.rollback(cid)

    def test_rollback_without_prior_active_card_retires_only_new_release(self) -> None:
        self.law.rules.retire(CARD, 1, EXERCISE_OWNER, rulecards.OWNER, DAY)
        cid = self.ready()
        self.activate(cid)
        self.rollback(cid)
        self.assertIsNone(self.law.rules.is_active(CARD, EFFECTIVE))

    def test_expired_prior_version_cannot_be_restored(self) -> None:
        self.card(activate=True, effective="2026-01-01", retirement="2026-10-19")
        cid = self.observe()
        self.card()
        self.approve(cid, targets={CARD: 3})
        self.monitor.regress(cid, today=DAY)
        self.activate(cid)
        before = self.law.rules.history(CARD)
        with self.assertRaisesRegex(rulecards.RuleError, "executable"):
            self.rollback(cid, today="2026-10-19")
        self.assertEqual(self.law.rules.history(CARD), before)

    def test_multi_card_activation_and_rollback_are_atomic(self) -> None:
        self.card("second", activate=True, effective="2026-01-01")
        cid = self.observe()
        self.card()
        self.card("second")
        cases = [
            dict(
                test_id=tid,
                card_id=card,
                facts=dict(automated_decisions=[]),
                expected=["not applicable"],
            )
            for tid, card in (("synthetic-regression", CARD), ("second-test", "second"))
        ]
        self.approve(cid, targets={CARD: 2, "second": 2}, cases=cases)
        self.monitor.regress(cid, today=DAY)
        original = self.law.rules._event

        def fail_second(card: str, *args: Any, **kwargs: Any) -> None:
            if card == "second":
                raise RuntimeError("injected second-card failure")
            original(card, *args, **kwargs)

        before = self.law.rules.history(CARD)
        with patch.object(self.law.rules, "_event", side_effect=fail_second):
            with self.assertRaises(RuntimeError):
                self.activate(cid)
        self.assertEqual(self.law.rules.history(CARD), before)
        self.activate(cid)
        before = self.law.rules.history(CARD)
        with patch.object(self.law.rules, "_event", side_effect=fail_second):
            with self.assertRaises(RuntimeError):
                self.rollback(cid)
        self.assertEqual(self.law.rules.history(CARD), before)
        self.rollback(cid)
        self.assertEqual(self.law.rules.is_active("second", EFFECTIVE), 1)

    def test_restart_and_independent_connection_staleness(self) -> None:
        cid = self.ready()
        other: Any = lawstore.LawStore(self.path, self.blobs)
        self.addCleanup(other.close)
        monitor = SourceMonitor(other)
        self.assertEqual(monitor.events(cid), self.monitor.events(cid))
        other.rules.hold(CARD, 1, EXERCISE_OWNER, rulecards.OWNER, "Other owner session", DAY)
        before = self.law.rules.history(CARD)
        with self.assertRaisesRegex(rulecards.RuleError, "lifecycle"):
            self.activate(cid)
        self.assertEqual(self.law.rules.history(CARD), before)
        self.assertEqual(monitor.changes()[0]["label"], LABEL)

    def test_append_only_and_sqlserver_ddl_contract(self) -> None:
        self.ready()
        for table in TABLES:
            with self.subTest(table=table), self.assertRaises(sqlite3.DatabaseError):
                self.law.sql.run(f"DELETE FROM {table}")
            self.law.sql.rollback()

        class Contract:
            dialect = "mssql"
            ledger = True
            statements: list[str] = []

            def run(self, sql: str, args: tuple[Any, ...] = ()) -> None:
                self.statements.append(sql)

            def all(self, sql: str, args: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
                return [dict(ledger_type_desc="APPEND_ONLY_LEDGER_TABLE")]

        db = Contract()
        from contextlib import nullcontext

        fake = SimpleNamespace(sql=db, rules=SimpleNamespace(transaction=nullcontext))
        SourceMonitor(fake)
        for ddl in MSSQL_DDL:
            self.assertTrue(any(ddl in sql and "LEDGER = ON" in sql for sql in db.statements))
        for forbidden in ("INSERT OR REPLACE", "INSERT OR IGNORE", "AUTOINCREMENT", "PRAGMA"):
            self.assertFalse(any(forbidden in sql for sql in db.statements))

    def test_input_and_date_errors_leave_no_approval_or_observation(self) -> None:
        for fields in (
            dict(today="2026-2-3"),
            dict(metadata=dict(complete="yes")),
            dict(metadata=dict(status="law")),
            dict(method="unknown"),
            dict(content=None),
            dict(provenance=""),
            dict(metadata=dict(effective="bad")),
            dict(metadata=dict(unrecognised=True)),
        ):
            with self.subTest(fields=fields), self.assertRaises(rulecards.RuleError):
                self.observe(**fields)
        self.assertEqual(self.monitor.changes(), [])
        cid = self.ready()
        with self.assertRaisesRegex(rulecards.RuleError, "precede"):
            self.monitor.regress(cid, today="2026-10-15")
        before = copy.deepcopy(self.monitor.events(cid))
        with self.assertRaisesRegex(rulecards.RuleError, "precede"):
            self.activate(cid, today="2026-10-17")
        self.assertEqual(self.monitor.events(cid), before)
