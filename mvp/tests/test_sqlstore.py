import json
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

import test_mvp
from zavaforward_mvp.sqlstore import SqlStore
from zavaforward_mvp.store import ConflictError


def seed(tmp):
    p = Path(tmp) / "zavaforward.json"
    p.write_text(json.dumps(test_mvp.DATA))
    return str(p), os.path.join(tmp, "pw.sqlite")


class SqlImproveTests(test_mvp.ImproveTests):
    """The whole store behaviour suite again, against the SQL store."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        data, db = seed(self.tmp.name)
        self.store = SqlStore(data, db)
        self.sam, self.pam = test_mvp.DATA["staff"]


class SqlStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data, self.db = seed(self.tmp.name)
        self.sam, self.pam = test_mvp.DATA["staff"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_state_survives_restart(self):
        a = SqlStore(self.data, self.db)
        a.log_call(self.sam, "ZF-1", "Contacted", "ok")
        a.set_decision(self.sam, "ZF-1", "Accepted")
        b = SqlStore(self.data, self.db)
        self.assertEqual(b.detail("ZF-1")["decision"]["status"], "Accepted")
        self.assertEqual(b.detail("ZF-1")["contacts"][0]["outcome"], "Contacted")
        self.assertTrue(b.verify_audit())
        self.assertEqual(b.ledger_head()[0], 2)

    def test_initial_seed_retains_procurement_and_date_without_reseeding_restart(self):
        data = json.loads(Path(self.data).read_text())
        data["as_of"] = "2026-10-13"
        data["procurement"] = {"packages": [{"id": "PKG-SYNTHETIC"}], "work_orders": []}
        Path(self.data).write_text(json.dumps(data))
        with patch.dict(os.environ, {"ZF_AS_OF": ""}):
            first = SqlStore(self.data, self.db)
            self.addCleanup(first.db.close)
            self.assertEqual(first.as_of, "2026-10-13")
            self.assertEqual(first.data["procurement"], data["procurement"])
            data["as_of"] = "2030-01-01"
            data["procurement"] = {"packages": [], "work_orders": []}
            Path(self.data).write_text(json.dumps(data))
            reopened = SqlStore(self.data, self.db)
            self.addCleanup(reopened.db.close)
            self.assertEqual(reopened.as_of, "2026-10-13")
            self.assertEqual(reopened.data["procurement"], first.data["procurement"])

    def test_second_process_sees_changes_without_restart(self):
        a, b = SqlStore(self.data, self.db), SqlStore(self.data, self.db)
        a.log_call(self.sam, "ZF-1", "Voicemail left", "")
        self.assertEqual(b.detail("ZF-1")["contacts"][0]["outcome"], "Voicemail left")
        b.log_call(self.sam, "ZF-1", "Contacted", "")
        self.assertEqual([c["outcome"] for c in a.detail("ZF-1")["contacts"]], ["Contacted", "Voicemail left"])
        self.assertTrue(a.verify_audit() and b.verify_audit())
        self.assertEqual(a.ledger_head(), b.ledger_head())

    def test_stale_write_is_refused_not_overwritten(self):
        a, b = SqlStore(self.data, self.db), SqlStore(self.data, self.db)
        with b.lock:
            c = b._case("ZF-1")
            c["contacts"].append(dict(at="x", purpose="Update", channel="Phone", direction="Outbound",
                                      outcome="Stale", note="", by="b"))
            b.audit("b", "log_contact", "ZF-1", "Stale")
            a.log_call(self.sam, "ZF-1", "Winner", "")
            with self.assertRaises(ConflictError):
                b.save()
        outcomes = [c["outcome"] for c in b.detail("ZF-1")["contacts"]]
        self.assertEqual(outcomes, ["Winner"])
        self.assertEqual(a.ledger_head()[0], 1)
        self.assertTrue(a.verify_audit())

    def test_gate_error_leaves_no_partial_change(self):
        s = SqlStore(self.data, self.db)
        from zavaforward_mvp.store import GateError
        with self.assertRaises(GateError):
            s.advance(self.sam, "ZF-2")
        self.assertEqual(SqlStore(self.data, self.db).detail("ZF-2")["stage"], "Final checks before ordering")

    def test_recommendation_persists_across_instances(self):
        a = SqlStore(self.data, self.db)
        rec = a.ai_priority(self.sam, 2)
        b = SqlStore(self.data, self.db)
        self.assertEqual(b.latest_priority(self.sam)["id"], rec["id"])
        b.resolve_priority(self.sam, rec["id"], "accept")
        self.assertEqual(a.latest_priority(self.sam)["status"], "Accepted")

    def test_ledger_is_append_only_and_detects_tampering(self):
        s = SqlStore(self.data, self.db)
        s.log_call(self.sam, "ZF-1", "Contacted", "")
        s.log_call(self.sam, "ZF-1", "Contacted again", "")
        raw = sqlite3.connect(self.db)
        with self.assertRaises(sqlite3.DatabaseError):
            raw.execute("UPDATE audit SET detail='x' WHERE seq=1")
        with self.assertRaises(sqlite3.DatabaseError):
            raw.execute("DELETE FROM audit WHERE seq=1")
        raw.execute("DROP TRIGGER audit_no_update")
        raw.execute("UPDATE audit SET detail='rewritten' WHERE seq=1")
        raw.commit()
        self.assertFalse(s.verify_audit())

    def test_list_filters_use_indexes(self):
        s = SqlStore(self.data, self.db)
        plan = " ".join(s.explain("SELECT id FROM cases WHERE closed=0 AND stage=? AND area=? ORDER BY id LIMIT 50", ("Contacting resident", "Test")))
        self.assertIn("ix_cases_filter", plan)
        plan = " ".join(s.explain("SELECT id FROM cases WHERE closed=0 AND owner_code=? AND id>? ORDER BY id LIMIT 50", ("RLO-01", "ZF-1")))
        self.assertIn("USING INDEX", plan.upper().replace("COVERING ", ""))
        self.assertEqual(s.query_case_ids(owner_code="PM-01"), ["ZF-5"])
        self.assertEqual(s.query_case_ids(after="ZF-3", limit=1), ["ZF-4"])

    def test_health_checks_database(self):
        self.assertTrue(SqlStore(self.data, self.db).ready())


if __name__ == "__main__":
    unittest.main()
