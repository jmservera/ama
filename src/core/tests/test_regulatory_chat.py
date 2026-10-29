"""Deterministic retrieval, storage and handoff proofs, synthetic-demo only."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from regulatory_fixture import ENV, NOW, PID, QUOTE, Fixture
from zava_forward.core import rule_engine, rulecards
from zava_forward.core.chat_isolation import ChatForbidden
from zava_forward.core.chatthreads import ChatNotFound
from zava_forward.core.regulatory_chat import RegulatoryChat, encode
from zava_forward.core.regulatory_usage import MAX_BYTES, MAX_POSITIONS
from zava_forward.core.store import ConflictError


def raw(bundle: dict[str, Any]) -> dict[str, Any]:
    """Core tests inspect the bounded API bundle without depending on agents."""
    return dict(
        schema="regulatory-chat-v1",
        kind="conflict" if bundle["conflict"] else "answer" if bundle["sources"] else "refused",
        citations=bundle["sources"] + bundle["facts"],
        reply="synthetic-demo",
        **{k: v for k, v in bundle.items() if k != "sources"},
    )


class RegulatoryTests(unittest.TestCase):
    def test_conflict_automatically_routes_exact_pair_once_per_stored_turn(self) -> None:
        for sql in (False, True):
            f, service, tid = self.make(sql)
            f.source(2, text="Different synthetic source, not law.")
            answer = service.ask(f.user, tid, "hazard sources")
            receipt = answer["escalation"]
            self.assertEqual(service.doubt(f.user, tid, answer["turn"]), receipt)
            self.assertEqual(service.doubt(f.user, tid, answer["turn"]), receipt)
            inbox = service.inbox(f.owner)["threads"]
            self.assertEqual(len(inbox), 1)
            stored = json.loads(inbox[0]["messages"][1]["content"])
            self.assertEqual(stored["citations"], answer["citations"])
            self.assertEqual(len(stored["citations"]), 2)
            self.assertEqual(service.usage_status(f.user)["outcomes"]["conflict"], 1)
            reopened = f.open()
            try:
                self.assertEqual(
                    len(reopened.chat_resume(f.user, tid)["messages"]),
                    3,
                )
                self.assertEqual(len(reopened.chat_list_threads(f.owner)), 1)
            finally:
                if sql:
                    reopened.db.close()
            again = service.ask(f.user, tid, "hazard sources")
            self.assertNotEqual(again["turn"], answer["turn"])
            self.assertEqual(len(service.inbox(f.owner)["threads"]), 2)

    def test_automatic_referral_write_and_save_failures_roll_back_complete_pair(self) -> None:
        for sql in (False, True):
            for operation in ("insert_thread", "commit", "_append_audit"):
                if operation == "_append_audit" and not sql:
                    continue
                f, service, tid = self.make(sql)
                f.source(2, text="Different synthetic source, not law.")
                before = service.history(f.user, tid)
                head = f.store.ledger_head()
                target = f.store if operation == "_append_audit" else f.store.chat_repo
                with patch.object(target, operation, side_effect=RuntimeError("injected")):
                    with self.assertRaises(RuntimeError):
                        service.ask(f.user, tid, "hazard sources")
                reopened = f.open()
                try:
                    self.assertEqual(reopened.chat_resume(f.user, tid), before)
                    self.assertEqual(reopened.chat_list_threads(f.owner), [])
                    self.assertEqual(reopened.ledger_head(), head)
                finally:
                    if sql:
                        reopened.db.close()

    def test_transaction_rechecks_sender_owner_and_case_before_conflict_mutation(self) -> None:
        for sql in (False, True):
            for change in ("sender", "owner", "case", "ambiguous-owner", "missing-owner"):
                f, service, tid = self.make(sql)
                f.source(2, text="Different synthetic source, not law.")
                before = service.history(f.user, tid)
                txn = f.store.chat_repo.txn
                detail = f.store.detail

                @contextmanager
                def changed(
                    change: str = change,
                    f: Fixture = f,
                    sql: bool = sql,
                    txn: Any = txn,
                ) -> Iterator[None]:
                    if change == "missing-owner":
                        if sql:
                            f.store.db.execute(
                                "DELETE FROM staff WHERE email=?", (f.owner["email"],)
                            )
                        else:
                            del f.store.staff[f.owner["email"]]
                    elif change in ("sender", "owner", "ambiguous-owner"):
                        person = f.user if change == "sender" else f.owner
                        key = (
                            "duplicate-owner@example.test"
                            if change == "ambiguous-owner"
                            else person["email"]
                        )
                        updated = dict(
                            person,
                            role=person["role"]
                            if change == "ambiguous-owner"
                            else "Quality Inspector",
                            email=key,
                        )
                        if sql:
                            if change == "ambiguous-owner":
                                f.store.db.execute(
                                    "INSERT INTO staff (body,email) VALUES (?,?)",
                                    (json.dumps(updated), key),
                                )
                            else:
                                f.store.db.execute(
                                    "UPDATE staff SET body=? WHERE email=?",
                                    (json.dumps(updated), key),
                                )
                        else:
                            f.store.staff[key] = updated
                    with txn():
                        if change == "case":
                            with patch.object(f.store, "detail", return_value=None):
                                yield
                        else:
                            yield

                with patch.object(f.store.chat_repo, "txn", changed):
                    with self.assertRaises((ChatForbidden, ChatNotFound, ValueError)):
                        service.ask(f.user, tid, "hazard sources")
                self.assertEqual(f.store.chat_repo.messages(tid), before["messages"])
                self.assertEqual(f.store.chat_list_threads(f.owner), [])
                self.assertIsNotNone(detail("ZF-1", f.owner))

    def test_real_sql_commit_attempt_failure_rolls_back_turn_referral_and_audit(self) -> None:
        f, service, tid = self.make(sql=True)
        f.source(2, text="Different synthetic source, not law.")
        before = service.history(f.user, tid)
        head = f.store.ledger_head()
        db = f.store.db
        attempted = []

        class FailCommit:
            def __getattr__(self, name: str) -> Any:
                return getattr(db, name)

            def execute(self, statement: str, *args: Any) -> Any:
                if statement == "COMMIT":
                    attempted.append(statement)
                    raise RuntimeError("Injected before SQL COMMIT takes effect")
                return db.execute(statement, *args)

        with patch.object(f.store, "db", FailCommit()):
            with self.assertRaisesRegex(RuntimeError, "SQL COMMIT"):
                service.ask(f.user, tid, "hazard sources")
        self.assertTrue(attempted)
        reopened = f.open()
        try:
            self.assertEqual(reopened.chat_resume(f.user, tid), before)
            self.assertEqual(reopened.chat_list_threads(f.owner), [])
            self.assertEqual(reopened.ledger_head(), head)
            self.assertTrue(reopened.verify_ledger()["intact"])
        finally:
            reopened.db.close()

    def test_json_automatic_referral_audit_failure_preserves_durable_receipt(self) -> None:
        f, service, tid = self.make()
        f.source(2, text="Different synthetic source, not law.")
        with patch.object(f.store, "audit", side_effect=OSError("injected audit failure")):
            with self.assertRaisesRegex(RuntimeError, "were saved.*audit failed"):
                service.ask(f.user, tid, "hazard sources")
        reopened = f.open()
        history = reopened.chat_resume(f.user, tid)
        self.assertEqual(len(history["messages"]), 3)
        self.assertEqual(len(reopened.chat_list_threads(f.owner)), 1)
        receipt = json.loads(history["messages"][2]["content"])
        self.assertEqual(service.doubt(f.user, tid, 2), receipt)
        status = service.usage_status(f.user)
        self.assertEqual(status["recorded_turns"], 0)
        self.assertEqual(status["coverage"], "recorded_audit_only")
        self.assertIn("not exact turn totals", status["coverage_note"])

    def test_usage_reads_only_bounded_audit_metadata_and_survives_restart(self) -> None:
        for sql in (False, True):
            f, service, tid = self.make(sql)
            service.ask(f.user, tid, "hazard sources")
            service.clock = lambda: NOW + timedelta(days=1)
            service.ask(f.user, tid, "hazard sources")
            service.clock = lambda: NOW
            for who, role in (
                (f.owner["email"], f.user["role"]),
                (f.user["email"], "Quality Inspector"),
            ):
                f.store.audit(who, "chat.regulatory.turn", "ZF-1", json.dumps(dict(role=role)))
            for operation in ("audit_entries",):
                with (
                    patch.object(f.store, operation, side_effect=AssertionError("No full scan")),
                    patch.object(
                        f.store.chat_repo, "messages", side_effect=AssertionError("No content")
                    ),
                ):
                    status = service.usage_status(f.user)
            self.assertEqual(status["recorded_turns"], 1)
            self.assertEqual(status["unmetered_events_in_window"], 0)
            self.assertNotIn("PRIVATE-", json.dumps(status))
            self.assertNotIn(QUOTE, json.dumps(status))
            f.store.audit(
                f.user["email"],
                "chat.regulatory.turn",
                "ZF-1",
                json.dumps(dict(role=f.user["role"])),
            )
            self.assertEqual(service.usage_status(f.user)["unmetered_events_in_window"], 1)
            for _ in range(MAX_POSITIONS + 1):
                f.store.audit(f.owner["email"], "unrelated", "-", "PRIVATE-FOREIGN-DETAIL")
            self.assertEqual(service.usage_status(f.user)["coverage"], "bounded_partial")
            if not sql:
                f.store.audit(f.owner["email"], "unrelated", "-", "x" * (MAX_BYTES + 1))
                self.assertEqual(service.usage_status(f.user)["coverage"], "bounded_partial")
            reopened = f.open()
            try:
                service.store = reopened
                service.iso.store = reopened
                self.assertEqual(service.usage_status(f.user)["coverage"], "bounded_partial")
            finally:
                service.store = f.store
                service.iso.store = f.store
                if sql:
                    reopened.db.close()

    def test_json_usage_snapshot_excludes_append_crossing_byte_limit(self) -> None:
        f, service, tid = self.make()
        service.ask(f.user, tid, "hazard sources")
        expected = service.usage_status(f.user)
        path = Path(f.store.audit_path)
        size = path.stat().st_size
        self.assertLess(size, MAX_BYTES)
        self.assertEqual(expected["recorded_turns"], 1)
        with path.open("rb") as stream:
            reader = MagicMock(wraps=stream)
            reader.__enter__.return_value = reader

            def append_before_read(length: int) -> bytes:
                f.store.audit(f.owner["email"], "unrelated", "-", "x" * (MAX_BYTES + 1))
                self.assertGreater(path.stat().st_size, MAX_BYTES)
                return stream.read(length)

            reader.read.side_effect = append_before_read
            with patch("zava_forward.core.regulatory_chat.open", return_value=reader):
                actual = service.usage_status(f.user)
            reader.read.assert_called_once_with(size)
        self.assertEqual(actual, expected)
        self.assertEqual(service.usage_status(f.user)["coverage"], "bounded_partial")

    def test_sql_turn_and_referral_audit_failure_roll_back_messages_and_ledger(self) -> None:
        f, service, tid = self.make(sql=True)
        before = service.history(f.user, tid)
        head = f.store.ledger_head()
        original = f.store._append_audit

        def failed(entries: Any) -> None:
            original(entries)
            raise RuntimeError("synthetic audit failure after append")

        with patch.object(f.store, "_append_audit", side_effect=failed):
            with self.assertRaises(RuntimeError):
                service.ask(f.user, tid, "hazard sources")
        self.assertEqual(service.history(f.user, tid), before)
        self.assertEqual(f.store.ledger_head(), head)
        answer = service.ask(f.user, tid, "hazard sources")
        before = service.history(f.user, tid)
        head = f.store.ledger_head()
        with patch.object(f.store, "_append_audit", side_effect=failed):
            with self.assertRaises(RuntimeError):
                service.doubt(f.user, tid, answer["turn"])
        self.assertEqual(service.history(f.user, tid), before)
        self.assertEqual(f.store.chat_list_threads(f.owner), [])
        self.assertEqual(f.store.ledger_head(), head)
        self.assertTrue(f.store.verify_ledger()["intact"])

    def test_sql_turn_audit_survives_restart_without_content_and_referral_is_once(self) -> None:
        f, service, tid = self.make(sql=True)
        reply = service.ask(f.user, tid, "hazard sources")
        receipt = service.doubt(f.user, tid, reply["turn"])
        service.doubt(f.user, tid, reply["turn"])
        reopened = f.open()
        try:
            events = list(reopened.audit_entries())
            turns = [e for e in events if e["action"] == "chat.regulatory.turn"]
            referrals = [e for e in events if e["action"] == "chat.regulatory.doubt"]
            self.assertEqual((len(turns), len(referrals)), (1, 1))
            meta = json.loads(turns[0]["detail"])
            self.assertEqual(meta["citations"], [c["id"] for c in reply["citations"]])
            self.assertEqual(len(meta["answer_hash"]), 64)
            self.assertEqual(meta["role"], f.user["role"])
            self.assertEqual(
                json.loads(referrals[0]["detail"])["inbox_thread"], receipt["inbox_thread"]
            )
            self.assertNotIn(QUOTE, json.dumps(events))
            self.assertNotIn("PRIVATE-", json.dumps(events))
            self.assertTrue(reopened.verify_ledger()["intact"])
        finally:
            reopened.db.close()

    def test_retention_status_includes_archived_own_role_only_without_messages(self) -> None:
        f, service, tid = self.make(sql=True)
        service.ask(f.user, tid, "hazard sources")
        f.store.chat_archive(f.user, tid)
        f.store.chat_create_thread(f.owner, case_id="ZF-1")
        f.store.chat_create_thread(f.user, case_id="ZF-1", title="ordinary chat")
        with patch.object(f.store.chat_repo, "messages", side_effect=AssertionError("No content")):
            result = service.privacy_status(f.user)
        self.assertEqual([r["thread_id"] for r in result["chat"]["records"]], [tid])
        self.assertEqual(result["chat"]["status"], "unknown")
        self.assertNotIn(QUOTE, json.dumps(result))

    def make(self, sql: bool = False) -> tuple[Fixture, RegulatoryChat, str]:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        fixture = Fixture(temp.name, sql=sql)
        self.addCleanup(fixture.close)
        service = RegulatoryChat(
            fixture.iso,
            fixture.law,
            raw,
            lambda _: "hazard-awareness-clock",
            lambda _: None,
            env=ENV,
            clock=lambda: NOW,
        )
        tid = service.start(fixture.user, "ZF-1")
        return fixture, service, tid

    def test_grounding_snapshot_minimisation_and_value_hash(self) -> None:
        f, service, tid = self.make()
        first = service.ask(f.user, tid, "hazard sources")
        sources = first["citations"]
        self.assertEqual(sources[0]["id"], PID)
        self.assertEqual(sources[0]["text"], QUOTE)
        serial = json.dumps(first)
        self.assertNotIn("PRIVATE-", serial)
        self.assertNotIn("preferred", serial)
        self.assertTrue(all("effective" in c and c["retrieved"] for c in sources))
        old_id = sources[1]["id"]
        f.store.cases["ZF-1"]["hazards"][0]["category"] = "Mould"
        second = service.ask(f.user, tid, "hazard sources")
        self.assertNotEqual(second["citations"][1]["id"], old_id)
        stored = json.loads(service.history(f.user, tid)["messages"][1]["content"])
        self.assertEqual(stored["citations"], first["citations"])

    def test_admission_matrix_and_no_mutation(self) -> None:
        f, service, tid = self.make()
        for env in ({}, {"ZF_REGULATORY_CHAT": "true"}, ENV | {"ZF_ENV": "production"}):
            service.env = env
            before = copy.deepcopy(f.store.data)
            with self.assertRaises(ChatForbidden):
                service.ask(f.user, tid, "hazard")
            self.assertEqual(before, f.store.data)
        service.env = ENV
        f.store.data["regulatory_chat_exercise"] = "real"
        with self.assertRaises(ChatForbidden):
            service.history(f.user, tid)
        f.store.data["regulatory_chat_exercise"] = "synthetic-demo"
        f.iso.env = ENV | {"CHAT_DPIA_REF": "REAL-UNVERIFIED"}
        with self.assertRaises(ChatForbidden):
            service.ask(f.user, tid, "hazard")

    def test_no_memory_other_home_or_other_role_facts(self) -> None:
        f, service, _ = self.make()
        user = f.store.staff["pam@example.test"]
        user["role"] = "Quality Inspector"
        bundle = service.bundle(user, "ZF-1", "hazard")
        self.assertEqual(bundle["facts"], [])
        self.assertIn("No permitted", bundle["unknown"])
        self.assertNotIn("Emergency", json.dumps(bundle))
        self.assertNotIn("ZF-2", json.dumps(bundle))

    def test_unapproved_held_and_retired_cards_do_not_support_answers(self) -> None:
        for state in ("draft", "held", "retired"):
            f, service, tid = self.make()
            if state == "draft":
                f.card(approve=False)
                # Active v1 must remain usable while draft v2 is edited.
                self.assertTrue(service.bundle(f.user, "ZF-1", "hazard")["sources"])
            else:
                action = getattr(f.law.rules, "hold" if state == "held" else "retire")
                args: dict[str, Any] = {"note": "synthetic hold"} if state == "held" else {}
                action(
                    "synthetic-hazard",
                    1,
                    "exercise-owner@example.test",
                    rulecards.OWNER,
                    today="2026-10-16",
                    **args,
                )
                self.assertEqual(service.ask(f.user, tid, "hazard")["citations"], [])

    def test_source_gates_and_changed_version_conflict(self) -> None:
        for status, effective, reviewed, completeness in (
            ("consultation", "2026-01-01", "reviewed", "full"),
            ("historical", "2026-01-01", "reviewed", "full"),
            ("in_force", "2027-01-01", "reviewed", "full"),
            ("in_force", "2026-01-01", "not_reviewed", "full"),
            ("in_force", "2026-01-01", "reviewed", "partial"),
        ):
            f, service, _ = self.make()
            f.source(
                2, status=status, effective=effective, reviewed=reviewed, completeness=completeness
            )
            f.card(pid="synthetic@v2#0001")
            self.assertEqual(service.bundle(f.user, "ZF-1", "hazard")["sources"], [])
        f, service, tid = self.make()
        f.source(2, text="Synthetic conflicting replacement; not law.")
        result = service.ask(f.user, tid, "hazard")
        self.assertTrue(result["conflict"])
        self.assertEqual([c["id"] for c in result["citations"]], [PID, "synthetic@v2#0001"])
        self.assertEqual(len(f.store.chat_list_threads(f.owner)), 1)

    def test_card_conflict_and_no_rule_alert_suppression(self) -> None:
        f, service, tid = self.make(sql=True)
        engine = rule_engine.RuleEngine(f.law)
        engine.run(f.store, "ZF-1", now=NOW)
        before = f.law.sql.all("SELECT * FROM reg_alert")
        self.assertTrue(before)
        f.card("synthetic-alternative", safe="Different synthetic human route")
        self.assertTrue(service.ask(f.user, tid, "hazard")["conflict"])
        service.law = None
        self.assertEqual(service.ask(f.user, tid, "hazard")["citations"], [])
        self.assertEqual(before, f.law.sql.all("SELECT * FROM reg_alert"))
        self.assertFalse(f.store.cases["ZF-1"]["hazards"][0]["released"])

    def test_isolation_reauthorisation_and_missing_owner(self) -> None:
        f, service, tid = self.make()
        answer = service.ask(f.user, tid, "hazard")
        with self.assertRaises(ChatNotFound):
            service.history(f.owner, tid)
        f.user["role"] = "Quality Inspector"
        with self.assertRaises(ChatForbidden):
            service.history(f.user, tid)
        f.user["role"] = "Resident Liaison Officer"
        with patch.object(f.store, "detail", return_value=None):
            with self.assertRaises(ChatNotFound):
                service.history(f.user, tid)
        del f.store.staff[f.owner["email"]]
        with self.assertRaisesRegex(ValueError, "missing"):
            service.doubt(f.user, tid, answer["turn"])

    def test_atomic_selected_turn_handoff_idempotency_and_restart(self) -> None:
        for sql in (False, True):
            f, service, tid = self.make(sql)
            answer = service.ask(f.user, tid, "hazard sources")
            service.ask(f.user, tid, "another source question")
            receipt = service.doubt(f.user, tid, answer["turn"])
            self.assertEqual(receipt, service.doubt(f.user, tid, answer["turn"]))
            inbox = service.inbox(f.owner)["threads"]
            self.assertEqual(len(inbox), 1)
            self.assertEqual(len(inbox[0]["messages"]), 2)
            self.assertEqual(
                json.loads(inbox[0]["messages"][1]["content"])["citations"], answer["citations"]
            )
            with self.assertRaises(ChatForbidden):
                service.inbox(f.user)
            reopened = f.open()
            try:
                messages = reopened.chat_resume(f.owner, receipt["inbox_thread"])["messages"]
                self.assertEqual(messages, inbox[0]["messages"])
            finally:
                if sql:
                    reopened.db.close()

    def test_handoff_failure_rolls_back_all_partial_writes(self) -> None:
        for sql in (False, True):
            for fail_at in (1, 2, 3):
                f, service, tid = self.make(sql)
                answer = service.ask(f.user, tid, "hazard sources")
                before = service.history(f.user, tid)
                original = f.store.chat_repo.add_message
                calls = 0

                def failing(message: Any, fail: int = fail_at, add: Any = original) -> None:
                    nonlocal calls
                    calls += 1
                    if calls == fail:
                        raise RuntimeError("synthetic injected storage failure")
                    add(message)

                with patch.object(f.store.chat_repo, "add_message", side_effect=failing):
                    with self.assertRaises(RuntimeError):
                        service.doubt(f.user, tid, answer["turn"])
                self.assertEqual(service.history(f.user, tid), before)
                self.assertEqual(f.store.chat_list_threads(f.owner), [])

    def test_size_input_archived_and_forged_turn_fail_closed(self) -> None:
        f, service, tid = self.make()
        for value in ("", "x" * 1001, None):
            with self.assertRaises(ValueError):
                service.ask(f.user, tid, value)
        with self.assertRaises(ValueError):
            encode(dict(reply="x" * 8000))
        with self.assertRaises(ValueError):
            service.doubt(f.user, tid, 999)
        f.store.chat_archive(f.user, tid)
        with self.assertRaises(ConflictError):
            service.ask(f.user, tid, "hazard")

    def test_pair_and_handoff_commit_failures_preserve_reopened_state(self) -> None:
        for sql in (False, True):
            f, service, tid = self.make(sql)
            before = service.history(f.user, tid)
            with patch.object(f.store.chat_repo, "commit", side_effect=RuntimeError("save failed")):
                with self.assertRaises(RuntimeError):
                    service.ask(f.user, tid, "hazard")
            self.assertEqual(service.history(f.user, tid), before)
            reply = service.ask(f.user, tid, "hazard")
            before = service.history(f.user, tid)
            with patch.object(f.store.chat_repo, "commit", side_effect=RuntimeError("save failed")):
                with self.assertRaises(RuntimeError):
                    service.doubt(f.user, tid, reply["turn"])
            reopened = f.open()
            try:
                self.assertEqual(reopened.chat_resume(f.user, tid), before)
                self.assertEqual(reopened.chat_list_threads(f.owner), [])
            finally:
                if sql:
                    reopened.db.close()

    def test_json_post_commit_audit_error_is_not_misreported_as_rollback(self) -> None:
        f, service, tid = self.make()
        reply = service.ask(f.user, tid, "hazard")
        with patch.object(f.store, "audit", side_effect=RuntimeError("audit failed")):
            with self.assertRaises(RuntimeError):
                service.doubt(f.user, tid, reply["turn"])
        self.assertEqual(len(service.inbox(f.owner)["threads"]), 1)
        receipt = service.doubt(f.user, tid, reply["turn"])
        self.assertEqual(receipt["status"], "sent-to-exercise-inbox")
        self.assertEqual(len(service.inbox(f.owner)["threads"]), 1)

    def test_missing_citation_and_draft_only_refuse(self) -> None:
        f, service, tid = self.make()
        f.card(pid="missing@v1#0001")
        self.assertEqual(service.ask(f.user, tid, "hazard")["citations"], [])
        f.law.rules.retire(
            "synthetic-hazard",
            2,
            "exercise-owner@example.test",
            rulecards.OWNER,
            "2026-10-16",
        )
        f.card(approve=False)
        self.assertEqual(service.ask(f.user, tid, "hazard")["citations"], [])


if __name__ == "__main__":
    unittest.main()
