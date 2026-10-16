"""Constructed SQL facts and explicitly simulated approvals, never operational approval."""

from __future__ import annotations

import copy
import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import nullcontext
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

from zava_forward.core import lawstore, rule_engine, rulecards

NOW = datetime(2026, 10, 16, 12, tzinfo=UTC)
OWNER = dict(email="owner@example.test", role="Building Safety Liaison", rule_roles=["rule_owner"])
SPEC = dict(kind="hazard-awareness-clock", hours=48, attention_hours=24)
PID = "synthetic@v1#0001"


class EngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.law_path = str(Path(self.tmp.name) / "law.sqlite")
        self.blobs = Path(self.tmp.name) / "blobs"
        self.law: Any = lawstore.LawStore(self.law_path, self.blobs)
        self.addCleanup(lambda: self.law.close())
        self.source()
        self.engine = rule_engine.RuleEngine(self.law)
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.addCleanup(self.db.close)
        self.db.execute("CREATE TABLE cases (id TEXT PRIMARY KEY, rowversion INT, body TEXT)")
        self.store = SimpleNamespace(db=self.db, lock=threading.RLock())
        self.facts: dict[str, Any] = dict(
            stage="Coordinate and deliver", home_id="SYN-HOME", hazards=[]
        )
        self.facts["hazards"] = [self.hazard()]
        self.write()
        self.version = self.card()

    def source(
        self,
        *,
        version: int = 1,
        status: str = "in_force",
        effective: str = "2026-01-01",
        completeness: str = "full",
        reviewed: str = "reviewed",
    ) -> None:
        with self.law.transaction():
            if version == 1:
                self.law.sql.run(
                    "INSERT INTO reg_source VALUES (?,?,?,?,?,?,?,?,?)",
                    (
                        "synthetic",
                        "Fictional test source",
                        "https://example.test",
                        "exercise",
                        "exercise",
                        "Fictional owner",
                        "High",
                        "daily",
                        "none",
                    ),
                )
            self.law.sql.run(
                "INSERT INTO reg_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    "synthetic",
                    version,
                    status,
                    effective,
                    "2026-01-01",
                    "2026-01-01",
                    reviewed,
                    "a" * 64,
                    "none",
                    "parsed",
                    completeness,
                    None,
                ),
            )
            self.law.sql.run(
                "INSERT INTO reg_provision VALUES (?,?,?,?,?,?,?)",
                (
                    f"synthetic@v{version}#0001",
                    "synthetic",
                    version,
                    1,
                    "Fictional provision",
                    "Constructed test text, not law",
                    "b" * 64,
                ),
            )

    def card(
        self,
        *,
        approve: bool = True,
        effective: str = "2026-01-01",
        check: dict[str, Any] | None = None,
        provisions: list[str] | None = None,
    ) -> int:
        v: int = self.law.rules.propose(
            "synthetic-clock",
            "author@example.test",
            rulecards.AUTHOR,
            today="2026-01-01",
            title="Fictional elapsed clock",
            trigger="Synthetic reported hazard",
            applicability="Constructed test homes",
            provisions=provisions or [PID],
            clock="Fictional 48 elapsed hours, not a statutory duration",
            safe_default="Refer to the human hazard owner now",
            escalation_role="Safety owner",
            approver=OWNER["email"],
            effective=effective,
            check=check or SPEC,
        )
        if approve:
            self.law.rules.approve(
                "synthetic-clock", v, OWNER["email"], rulecards.OWNER, "2026-01-01"
            )
            self.law.rules.activate(
                "synthetic-clock", v, OWNER["email"], rulecards.OWNER, "2026-01-01"
            )
        return v

    def hazard(self, *, hours_ago: int = 25, priority: str = "Emergency") -> dict[str, Any]:
        return dict(
            aware_at=(NOW - timedelta(hours=hours_ago)).isoformat(),
            priority=priority,
            source="SYN-REPORT",
            released=False,
            hold=dict(status="Active"),
        )

    def write(self, case_id: str = "SYN-1") -> None:
        row = self.db.execute("SELECT id FROM cases WHERE id=?", (case_id,)).fetchone()
        if row:
            self.db.execute(
                "UPDATE cases SET rowversion=rowversion+1, body=? WHERE id=?",
                (json.dumps(self.facts), case_id),
            )
        else:
            self.db.execute(
                "INSERT INTO cases VALUES (?,?,?)", (case_id, 1, json.dumps(self.facts))
            )
        self.db.commit()

    def run_engine(
        self, *, now: datetime = NOW, trigger: str = "data_change", case_id: str = "SYN-1"
    ) -> dict[str, Any]:
        return self.engine.run(self.store, case_id, trigger, now=now)

    def checks(self, **kw: Any) -> list[dict[str, Any]]:
        return [c for c in self.run_engine(**kw)["checks"] if c["card_id"] == "synthetic-clock"]

    def alerts(self) -> list[dict[str, Any]]:
        return [a for h in self.engine.alerts(OWNER)["homes"] for a in h["alerts"]]

    def test_five_results_exact_thresholds_and_citations(self) -> None:
        for hours, expected in (
            (0, "clear"),
            (23, "clear"),
            (24, "attention"),
            (47, "attention"),
            (48, "breach risk"),
            (72, "breach risk"),
        ):
            self.facts["hazards"] = [self.hazard(hours_ago=hours)]
            self.write()
            c = self.checks()[0]
            self.assertEqual(c["result"], expected)
            self.assertEqual(c["citations"][0]["id"], PID)
            self.assertEqual(c["citations"][0]["status"], "in_force")
            self.assertEqual(c["card_status"], "active")
            self.assertTrue(c["safe_action"] and c["clock"] and c["decision_owner"])
            self.assertTrue(c["exercise"])
        self.facts["hazards"] = []
        self.write()
        self.assertEqual(self.checks()[0]["result"], "not applicable")
        del self.facts["hazards"]
        self.write()
        self.assertEqual(self.checks()[0]["result"], "unknown")

    def test_missing_invalid_future_evidence_never_clear_and_no_side_effects(self) -> None:
        for field, value in (
            ("aware_at", None),
            ("aware_at", "2026-01-01"),
            ("aware_at", "not a time"),
            ("aware_at", (NOW + timedelta(seconds=1)).isoformat()),
            ("source", ""),
            ("priority", "invented"),
            ("released", None),
            ("hold", None),
            ("hold", {"status": "Released"}),
        ):
            with self.subTest(field=field, value=value):
                self.facts["hazards"] = [self.hazard() | {field: value}]
                self.write()
                before = self.db.execute("SELECT body FROM cases").fetchone()[0]
                self.assertEqual(self.checks()[0]["result"], "unknown")
                self.assertEqual(self.db.execute("SELECT body FROM cases").fetchone()[0], before)
        self.assertFalse(hasattr(self.engine, "send"))

    def test_drafts_seeds_and_prose_only_are_not_executable(self) -> None:
        self.card(approve=False)
        # A new draft must not disable the still-approved prior version.
        self.assertEqual(self.checks()[0]["result"], "attention")
        seed_checks = self.run_engine()["checks"]
        self.assertTrue(
            all(c["result"] == "unknown" for c in seed_checks if c["card_id"] != "synthetic-clock")
        )
        self.assertEqual(len(self.alerts()), 1)
        for cid in ("hazard-awareness-clock", "automated-decision-safeguard"):
            h = self.law.rules.history(cid)[0]
            self.assertIsNone(h["approved_by"])
            self.assertIsNone(h["check"])
        self.law.rules.hold(
            "synthetic-clock", 1, OWNER["email"], rulecards.OWNER, "Synthetic hold", "2026-01-02"
        )
        self.assertEqual(self.checks()[0]["result"], "unknown")

    def test_approval_does_not_make_future_rule_active(self) -> None:
        self.card(effective="2027-01-01")
        self.assertEqual(self.checks()[0]["result"], "unknown")
        self.assertEqual(self.alerts(), [])

    def test_future_consulted_historical_partial_stale_and_missing_sources(self) -> None:
        for kw in (
            dict(status="consultation"),
            dict(status="historical"),
            dict(effective="2027-01-01"),
            dict(completeness="partial"),
            dict(reviewed="not_reviewed"),
        ):
            with self.subTest(kw=kw):
                version = len(self.law.source("synthetic")["versions"]) + 1
                self.source(version=version, **kw)
                self.card(provisions=[f"synthetic@v{version}#0001"])
                result = self.checks()[0]["result"]
                self.assertIn(result, ("unknown", "not applicable"))
                self.assertEqual(self.alerts(), [])
        self.card(provisions=["missing@v1#0001"])
        self.assertEqual(self.checks()[0]["citations"][0]["status"], "missing")
        self.card(provisions=[PID])
        self.assertEqual(self.checks()[0]["result"], "unknown")

    def test_no_duration_guessed_and_specs_are_immutable_validated(self) -> None:
        self.card(check=dict(kind=SPEC["kind"]))
        self.assertEqual(self.checks()[0]["result"], "unknown")
        for value in (
            {},
            dict(kind="eval"),
            SPEC | {"hours": True},
            SPEC | {"hours": 0},
            SPEC | {"attention_hours": 49},
            SPEC | {"aware_at": "forged"},
            SPEC | {"suppress": True},
        ):
            with self.subTest(value=value), self.assertRaises(rulecards.RuleError):
                self.card(check=value if value else {"kind": "invalid"})
        with self.assertRaises(sqlite3.IntegrityError):
            self.law.sql.run("UPDATE rule_card_check SET specification='{}'")
        self.law.sql.rollback()

    def test_replay_across_time_restart_and_three_triggers(self) -> None:
        first = self.run_engine()
        self.assertEqual(first, self.run_engine(now=NOW + timedelta(hours=25)))
        self.law.close()
        self.law = lawstore.LawStore(self.law_path, self.blobs)
        self.engine = rule_engine.RuleEngine(self.law)
        self.assertEqual(first, self.run_engine())
        step = self.run_engine(trigger="step_transition")
        scheduled = self.run_engine(trigger="schedule")
        self.assertNotEqual(step["id"], scheduled["id"])
        self.assertEqual(
            scheduled, self.run_engine(trigger="schedule", now=NOW + timedelta(seconds=1))
        )
        self.assertNotEqual(
            scheduled["id"],
            self.run_engine(trigger="schedule", now=NOW + timedelta(minutes=1))["id"],
        )
        self.write()
        self.assertNotEqual(first["id"], self.run_engine()["id"])

    def test_failed_checkpoint_rolls_back_check_and_alert_and_retry_recovers(self) -> None:
        original = self.law.sql.run

        def fail(sql: str, args: object = ()) -> None:
            if sql.startswith("INSERT INTO reg_checkpoint"):
                raise RuntimeError("injected checkpoint failure")
            original(sql, args)

        with patch.object(self.law.sql, "run", side_effect=fail):
            with self.assertRaisesRegex(RuntimeError, "checkpoint"):
                self.run_engine()
        for table in ("reg_check", "reg_alert", "reg_checkpoint"):
            self.assertEqual(self.law.sql.all(f"SELECT COUNT(*) n FROM {table}")[0]["n"], 0)
        self.run_engine()
        self.assertEqual(len(self.alerts()), 1)

    def test_attention_publication_limit_does_not_suppress_checks_or_breach(self) -> None:
        self.run_engine(trigger="schedule")
        self.run_engine(trigger="schedule", now=NOW + timedelta(minutes=1))
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.law.sql.all("SELECT COUNT(*) n FROM reg_checkpoint")[0]["n"], 2)
        self.run_engine(trigger="schedule", now=NOW + timedelta(hours=23))
        self.assertIn("breach risk", {a["result"] for a in self.alerts()})
        # A longer fixture clock allows the attention window itself to expire.
        self.card(check=SPEC | dict(hours=100, attention_hours=100))
        self.run_engine(trigger="schedule")
        count = self.law.sql.all("SELECT COUNT(*) n FROM reg_alert")[0]["n"]
        self.run_engine(trigger="schedule", now=NOW + timedelta(hours=24))
        self.assertEqual(self.law.sql.all("SELECT COUNT(*) n FROM reg_alert")[0]["n"], count + 1)

    def test_breach_owner_ack_outcome_false_positive_history_no_suppression(self) -> None:
        self.facts["hazards"] = [self.hazard(hours_ago=60)]
        self.write()
        self.run_engine()
        a = self.alerts()[0]
        self.assertTrue(a["requires_acknowledgement"] and a["requires_outcome"])
        with self.assertRaises(PermissionError):
            self.engine.disposition(
                OWNER | dict(email="other@example.test"), a["id"], "acknowledge", "SYN"
            )
        with self.assertRaises(PermissionError):
            self.engine.disposition(OWNER | dict(rule_roles=[]), a["id"], "acknowledge", "SYN")
        with self.assertRaises(ValueError):
            self.engine.disposition(OWNER, a["id"], "outcome", "SYN", now=NOW)
        self.engine.disposition(OWNER, a["id"], "false_positive", "SYN", now=NOW)
        stats = self.engine.alerts(OWNER)["precision"]
        self.assertEqual((stats["classified"], stats["false_positive_rate"]), (1, 1.0))
        self.assertTrue(self.alerts()[0]["requires_acknowledgement"])
        self.engine.disposition(OWNER, a["id"], "acknowledge", "SYN", now=NOW)
        self.engine.disposition(OWNER, a["id"], "acknowledge", "SYN", now=NOW)
        self.engine.disposition(OWNER, a["id"], "outcome", "SYN human investigated", now=NOW)
        self.assertEqual(self.alerts(), [])
        self.write()
        self.run_engine()
        self.assertEqual(self.alerts()[0]["result"], "breach risk")
        self.assertTrue(self.alerts()[0]["requires_acknowledgement"])

    def test_home_group_ranking_and_default_deny_roles(self) -> None:
        self.facts["hazards"] = [
            self.hazard(priority="Routine"),
            self.hazard(priority="Emergency"),
            self.hazard(hours_ago=49, priority="Routine"),
        ]
        self.write()
        self.run_engine()
        homes = self.engine.alerts(OWNER)["homes"]
        self.assertEqual(len(homes), 1)
        alerts = homes[0]["alerts"]
        self.assertEqual([a["item"] for a in alerts], ["hazards/2", "hazards/1", "hazards/0"])
        self.facts["hazards"] = [self.hazard(hours_ago=60)]
        self.write("SYN-2")
        self.run_engine(case_id="SYN-2")
        grouped = self.engine.alerts(OWNER)["homes"]
        self.assertEqual(len(grouped), 1)
        self.assertEqual({a["case_id"] for a in grouped[0]["alerts"]}, {"SYN-1", "SYN-2"})
        for role in ("Contractor", "Mystery"):
            with self.assertRaises(PermissionError):
                self.engine.alerts(OWNER | dict(role=role))
        self.assertEqual(
            self.engine.alerts(dict(role="Quality Inspector", email="other@example.test"))["homes"],
            [],
        )
        self.assertIsNone(
            self.engine.alerts(dict(role="Quality Inspector", email="other@example.test"))[
                "precision"
            ]["false_positive_rate"]
        )

    def test_significant_decision_missing_evidence_pending_and_human_record(self) -> None:
        self.card(check=dict(kind="automated-decision-safeguard"))
        self.assertEqual(self.checks()[0]["result"], "unknown")
        self.facts["automated_decisions"] = [dict(significant=True)]
        self.write()
        self.assertEqual(self.checks()[0]["result"], "unknown")
        self.facts["automated_decisions"][0].update(
            state="pending", decision_owner="Human reviewer", source="SYN-PROPOSAL"
        )
        self.write()
        self.assertEqual(self.checks()[0]["result"], "attention")
        self.facts["automated_decisions"][0].update(
            state="recorded", evidence="SYN-HUMAN", decided_at=NOW.isoformat()
        )
        self.write()
        self.assertEqual(self.checks()[0]["result"], "clear")

    def test_sql_new_statements_are_portable_and_append_only(self) -> None:
        text = Path(rule_engine.__file__).read_text()
        for forbidden in ("INSERT OR REPLACE", "INSERT OR IGNORE", "AUTOINCREMENT", "PRAGMA"):
            self.assertNotIn(forbidden, text)
        self.run_engine()
        self.engine.disposition(OWNER, self.alerts()[0]["id"], "acknowledge", "SYN", now=NOW)
        for table in rule_engine.TABLES:
            with self.assertRaises(sqlite3.IntegrityError):
                self.law.sql.run(f"DELETE FROM {table}")
            self.law.sql.rollback()
        before = copy.deepcopy(self.facts)
        self.run_engine()
        self.assertEqual(before, self.facts)

    def test_latest_snapshot_removes_advisories_but_retains_unresolved_breach(self) -> None:
        self.run_engine()
        self.assertEqual(len(self.alerts()), 1)
        self.facts["hazards"] = []
        self.write()
        self.run_engine()
        self.assertEqual(self.alerts(), [])
        self.facts["hazards"] = [self.hazard(hours_ago=60)]
        self.write()
        self.run_engine()
        self.law.rules.hold(
            "synthetic-clock", 1, OWNER["email"], rulecards.OWNER, "SYN source review", "2026-10-16"
        )
        self.run_engine()
        risk = self.alerts()[0]
        self.assertFalse(risk["active_control"])
        self.assertTrue(risk["requires_outcome"])
        self.assertEqual(self.engine.alerts(OWNER)["coverage_status"], "unknown")

    def test_independent_engine_connections_serialize_duplicate_delivery(self) -> None:
        law: Any = lawstore.LawStore(self.law_path, self.blobs)
        try:
            other = rule_engine.RuleEngine(law)
            barrier = threading.Barrier(2)
            results: list[dict[str, Any]] = []
            errors: list[Exception] = []
            store_lock = threading.RLock()

            def run(engine: rule_engine.RuleEngine) -> None:
                try:
                    barrier.wait(timeout=10)
                    store = SimpleNamespace(db=self.db, lock=store_lock)
                    results.append(engine.run(store, "SYN-1", now=NOW))
                except Exception as exc:
                    errors.append(exc)

            threads = [
                threading.Thread(target=run, args=(engine,)) for engine in (self.engine, other)
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=15)
                self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0], results[1])
            self.assertEqual(len(self.alerts()), 1)
            self.assertEqual(self.law.sql.all("SELECT COUNT(*) n FROM reg_checkpoint")[0]["n"], 1)
        finally:
            law.close()

    def test_release_needs_independent_evidence_and_never_releases_by_clock(self) -> None:
        h = self.hazard()
        h.update(
            released=True,
            released_at=NOW.isoformat(),
            accepted_at=NOW.isoformat(),
            repair_evidence="SYN",
            raised_by_email="reporter@example.test",
            repaired_by_email="repairer@example.test",
        )
        self.facts["hazards"] = [h]
        self.write()
        self.assertEqual(self.checks()[0]["result"], "unknown")
        h["hold"]["decision"] = dict(
            evidence="SYN-INDEPENDENT",
            actor=dict(email="reporter@example.test"),
            at=NOW.isoformat(),
        )
        h["hold"]["status"] = "Released"
        self.write()
        self.assertEqual(self.checks()[0]["result"], "unknown")
        h["hold"]["decision"]["actor"]["email"] = "independent@example.test"
        self.write()
        self.assertEqual(self.checks()[0]["result"], "clear")

    def test_mssql_initialization_uses_explicit_keys_and_append_only_guards(self) -> None:
        for ledger in (False, True):
            statements: list[str] = []
            sql = SimpleNamespace(
                dialect="mssql",
                ledger=ledger,
                run=statements.append,
                all=lambda *_: [{"ledger_type_desc": "APPEND_ONLY_LEDGER_TABLE"}],
            )
            law = SimpleNamespace(sql=sql, rules=SimpleNamespace(transaction=nullcontext))
            rule_engine.RuleEngine(law)
            self.assertEqual(sum("CREATE TABLE" in s for s in statements), 4)
            if ledger:
                self.assertTrue(all("APPEND_ONLY = ON" in s for s in statements))
            else:
                self.assertEqual(sum("INSTEAD OF UPDATE, DELETE" in s for s in statements), 4)


if __name__ == "__main__":
    unittest.main()
