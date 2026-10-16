"""Rule cards: lifecycle, role separation, version retention, holds, exercise labelling, source changes."""
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from zava_forward.core import rulecards as rc

OWNER = "Named compliance owner (unassigned)"


class RuleCardTests(unittest.TestCase):
    def setUp(self):
        self.s = rc.RuleCardStore(sqlite3.connect(":memory:"))
        self.s.seed()
        self.cid = "hazard-awareness-clock"

    def activate(self, v=1):
        self.s.approve(self.cid, v, OWNER, rc.OWNER, "2026-10-16")
        self.s.activate(self.cid, v, OWNER, rc.OWNER, "2026-10-16")

    def test_seed_cards_are_labelled_exercise_drafts(self):
        for cid in ("hazard-awareness-clock", "automated-decision-safeguard"):
            h = self.s.history(cid)[0]
            self.assertEqual(h["state"], "draft")
            self.assertIn("EXERCISE CARD", h["label"])
            self.assertIsNone(self.s.is_active(cid, "2027-01-01"))
        self.assertEqual(self.s.seed(), [])

    def test_only_owner_approved_card_is_active(self):
        with self.assertRaises(rc.RuleError):
            self.s.activate(self.cid, 1, OWNER, rc.OWNER)
        with self.assertRaises(rc.RuleError):
            self.s.approve(self.cid, 1, "Someone else", rc.OWNER)
        self.activate()
        self.assertEqual(self.s.is_active(self.cid, "2026-10-20"), 1)
        h = self.s.history(self.cid)[0]
        self.assertEqual((h["approved_by"], h["approved_on"]), (OWNER, "2026-10-16"))
        self.assertTrue(h["events"][1]["simulated"])

    def test_author_cannot_approve_own_card(self):
        v = self.s.propose("c", "Pat", rc.AUTHOR, **{k: v for k, v in dict(
            title="t", trigger="x", applicability="a", provisions=["p"], clock="c", safe_default="s",
            escalation_role="e", approver="Pat", effective="2026-01-01").items()})
        with self.assertRaises(rc.RuleError):
            self.s.approve("c", v, "Pat", rc.OWNER)
        with self.assertRaises(rc.RuleError):
            self.s.approve("c", v, "Pat", rc.AUTHOR)
        with self.assertRaises(rc.RuleError):
            self.s.approve("c", v, " pat ", rc.OWNER)
        with self.assertRaises(rc.RuleError):
            self.s.propose("c", "Lee", rc.OWNER, title="t")

    def test_unlabelled_cards_are_refused(self):
        with self.assertRaises(rc.RuleError):
            self.s.propose("c", "Pat", rc.AUTHOR, exercise=False, title="t", trigger="x", applicability="a",
                           provisions=["p"], clock="c", safe_default="s", escalation_role="e",
                           approver="Lee", effective="2026-01-01")

    def test_hold_by_owner_only_and_stops_firing(self):
        self.activate()
        with self.assertRaises(rc.RuleError):
            self.s.hold(self.cid, 1, "Exercise author (synthetic)", rc.AUTHOR, "no")
        self.s.hold(self.cid, 1, OWNER, rc.OWNER, "source doubt")
        self.assertEqual(self.s.state(self.cid, 1), "held")
        self.assertIsNone(self.s.is_active(self.cid, "2026-10-20"))
        self.s.release(self.cid, 1, OWNER, rc.OWNER)
        self.assertEqual(self.s.is_active(self.cid, "2026-10-20"), 1)

    def test_versions_preserved_and_append_only(self):
        self.activate()
        v2 = self.s.propose(self.cid, "Exercise author (synthetic)", rc.AUTHOR, exercise=True, title="Hazard awareness clock v2",
                            trigger="t", applicability="a", provisions=["awaabs-law-regulations-2025"], clock="c",
                            safe_default="s", escalation_role="e", approver=OWNER, effective="2026-11-01")
        self.assertEqual(self.s.is_active(self.cid, "2026-10-20"), 1)
        self.s.approve(self.cid, v2, OWNER, rc.OWNER)
        self.s.activate(self.cid, v2, OWNER, rc.OWNER, "2026-11-01")
        h = self.s.history(self.cid)
        self.assertEqual([x["state"] for x in h], ["retired", "active"])
        self.assertEqual(h[0]["title"], "Hazard awareness clock")
        with self.assertRaises(sqlite3.DatabaseError):
            self.s.db.execute("UPDATE rule_card_version SET title='x'")
        with self.assertRaises(sqlite3.DatabaseError):
            self.s.db.execute("DELETE FROM rule_card_event")

    def test_effective_and_retirement_dates(self):
        self.activate()
        self.assertIsNone(self.s.is_active(self.cid, "2025-01-01"))

    def fields(self, **kw):
        fields = dict(rc.SEED_CARDS[0])
        fields.pop("card_id")
        fields.update(kw)
        return fields

    def test_invalid_fields_are_atomic(self):
        before = self.s.history(self.cid)
        for kw in (dict(effective="2026-1-01"), dict(effective="2026-02-30"),
                   dict(retirement="2025-10-27"), dict(provisions="citation"),
                   dict(provisions=[None]), dict(approver=" "), dict(title=123), dict(title="t" * 201)):
            with self.subTest(kw=kw), self.assertRaises(rc.RuleError):
                self.s.propose(self.cid, "Pat", rc.AUTHOR, **self.fields(**kw))
            self.assertEqual(before, self.s.history(self.cid))
        self.activate()
        with self.assertRaises(rc.RuleError):
            self.s.hold(self.cid, 1, OWNER, rc.OWNER, "")
        self.assertEqual(self.s.state(self.cid, 1), "active")

    def test_supersession_failure_rolls_back_and_connection_recovers(self):
        self.activate()
        v = self.s.propose(self.cid, "Pat", rc.AUTHOR, **self.fields())
        self.s.approve(self.cid, v, OWNER, rc.OWNER)
        before = self.s.history(self.cid)
        original = self.s._event

        def fail(cid, version, state, *args, **kw):
            if state == "active":
                raise RuntimeError("injected activation failure")
            return original(cid, version, state, *args, **kw)

        with patch.object(self.s, "_event", side_effect=fail), self.assertRaises(RuntimeError):
            self.s.activate(self.cid, v, OWNER, rc.OWNER)
        self.assertEqual(self.s.history(self.cid), before)
        self.s.activate(self.cid, v, OWNER, rc.OWNER)
        self.assertEqual([r["state"] for r in self.s.history(self.cid)], ["retired", "active"])

    def test_persisted_legacy_history_and_initialization_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "rules.sqlite")
            original = rc.RuleCardStore(sqlite3.connect(path))
            original.seed()
            original.approve(self.cid, 1, OWNER, rc.OWNER, "2026-10-16")
            original.source_changed("awaabs-law-regulations-2025", 2)
            history, reviews = original.history(self.cid), original.reviews()
            original.db.close()
            reopened = rc.RuleCardStore(sqlite3.connect(path))
            reopened.seed()
            self.assertEqual(reopened.history(self.cid), history)
            self.assertEqual(reopened.reviews(), reviews)
            self.assertEqual(reopened.propose(self.cid, "Pat", rc.AUTHOR, **self.fields()), 2)
            with self.assertRaises(sqlite3.DatabaseError):
                reopened.db.execute("DELETE FROM rule_card_version")
            reopened.db.rollback()
            reopened.db.close()

    def test_independent_and_shared_connection_writers_serialize_versions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "rules.sqlite")
            stores = [rc.RuleCardStore(sqlite3.connect(path, check_same_thread=False)) for _ in range(2)]
            errors = []
            barrier = threading.Barrier(4)

            def write(store):
                try:
                    barrier.wait(timeout=5)
                    store.propose("concurrent", "Pat", rc.AUTHOR, **self.fields())
                except Exception as exc:
                    errors.append(exc)

            threads = [threading.Thread(target=write, args=(stores[i % 2],)) for i in range(4)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=10)
                self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual([r["version"] for r in stores[0].history("concurrent")], [1, 2, 3, 4])
            for store in stores:
                store.db.close()

    def test_driver_integrity_error_is_translated_and_rolled_back(self):
        class DriverIntegrityError(Exception):
            pass

        with patch.object(type(self.s.sql), "integrity_error", DriverIntegrityError):
            with patch.object(self.s.sql, "run", side_effect=DriverIntegrityError("conflict")):
                with self.assertRaisesRegex(rc.RuleError, "conflicting"):
                    self.s.propose("c", "Pat", rc.AUTHOR, **self.fields())
        self.assertEqual(self.s.history("c"), [])
        self.assertEqual(self.s.propose("c", "Pat", rc.AUTHOR, **self.fields()), 1)

    def test_sqlserver_adapter_initializes_append_only_portable_tables(self):
        from zava_forward.core import lawstore

        class ContractDb(lawstore.MssqlDb):
            def __init__(self):
                self.lock = threading.RLock()
                self.ledger = True
                self.db = None
                self.statements = []

            def begin(self):
                self.statements.append("begin")

            def run(self, sql, args=()):
                self.statements.append(sql)

            def all(self, sql, args=()):
                return [{"ledger_type_desc": "APPEND_ONLY_LEDGER_TABLE"}]

            def commit(self):
                self.statements.append("commit")

            def rollback(self):
                self.statements.append("rollback")

        db = ContractDb()
        rc.RuleCardStore(db)
        self.assertEqual(db.statements[0], "begin")
        self.assertEqual(db.statements[-1], "commit")
        for table in rc.APPEND_ONLY:
            self.assertTrue(any(f"CREATE TABLE {table} " in s and rc.LEDGER_SUFFIX in s for s in db.statements))

    def test_source_change_never_overwrites_approved_card(self):
        self.activate()
        before = self.s.history(self.cid)
        self.assertEqual(self.s.source_changed("awaabs-law-regulations-2025", 2), [self.cid])
        self.assertEqual(self.s.history(self.cid), before)
        self.assertEqual(self.s.is_active(self.cid, "2026-10-20"), 1)
        self.assertEqual(self.s.reviews(self.cid)[0]["status"], "open")

    def test_review_item_lists_affected_requirements_rules_tests_and_versions(self):
        self.activate()
        self.s.source_changed("awaabs-law-regulations-2025", 2, "2026-11-01", source_effective="2026-11-30")
        r = self.s.reviews(self.cid)[0]
        self.assertEqual(r["affected"]["rules"], [self.cid])
        self.assertEqual(r["affected"]["active_version"], 1)
        self.assertIn("CON-001", r["affected"]["requirements"])
        self.assertTrue(r["affected"]["tests"])
        self.assertEqual((r["source_version"], r["prior_version"], r["source_effective"]), (2, 1, "2026-11-30"))
        with self.assertRaises(sqlite3.DatabaseError):
            self.s.db.execute("UPDATE rule_card_review SET status='x'")

    def assess(self, rid=1, actor=OWNER, role=rc.OWNER, **kw):
        a = dict(interpretation="Owner reading (exercise)", outcome="new_version_required", tests=["t1"], effective="2026-11-30",
                 notification="Notify Repairs", rollback="Retain v1")
        a.update(kw)
        self.s.assess_review(rid, actor, role, "2026-11-02", **a)

    def test_assessment_needs_named_owner_and_complete_record(self):
        self.activate()
        self.s.source_changed("awaabs-law-regulations-2025", 2, "2026-11-01")
        for actor, role in (("Agent", rc.OWNER), (OWNER, rc.AUTHOR), ("Exercise author (synthetic)", rc.AUTHOR)):
            with self.assertRaises(rc.RuleError):
                self.assess(actor=actor, role=role)
        with self.assertRaises(rc.RuleError):
            self.assess(rollback="")
        self.assertEqual(self.s.reviews()[0]["status"], "open")
        self.assess(hold="pending new version")
        r = self.s.reviews()[0]
        self.assertEqual((r["status"], r["assessment"]["actor"]), ("assessed", OWNER))
        self.assertEqual(self.s.state(self.cid, 1), "held")
        self.assertIsNone(self.s.is_active(self.cid, "2026-11-03"))
        with self.assertRaises(rc.RuleError):
            self.assess()

    def test_assessment_never_activates_a_rule(self):
        self.s.source_changed("awaabs-law-regulations-2025", 2, "2026-11-01")
        self.assess(outcome="no_change")
        self.assertIsNone(self.s.is_active(self.cid, "2026-11-03"))
        self.assertEqual(self.s.state(self.cid, 1), "draft")
        for role in ("agent", rc.AUTHOR):
            with self.assertRaises(rc.RuleError):
                self.s.activate(self.cid, 1, "Agent", role)


if __name__ == "__main__":
    unittest.main()
