import json
import os
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import dataset
from zava_forward.core import ledger
from zava_forward.core.mssqlstore import MssqlStore
from zava_forward.core.sqlstore import LedgerRelianceError, SqlStore
from zava_forward.core.store import ConflictError


def seed(tmp):
    p = Path(tmp) / "zavaforward.json"
    p.write_text(json.dumps(dataset.DATA))
    return str(p), os.path.join(tmp, "pw.sqlite")


class SqlImproveTests(dataset.ImproveTests):
    """The whole store behaviour suite again, against the SQL store."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        data, db = seed(self.tmp.name)
        self.store = SqlStore(data, db)
        self.sam, self.pam = dataset.DATA["staff"]


class SqlStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.data, self.db = seed(self.tmp.name)
        self.sam, self.pam = dataset.DATA["staff"]

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
        from zava_forward.core.store import GateError
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

    def _drop_audit_triggers(self, store):
        if isinstance(store, MssqlStore):
            store.db.execute("IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only")
        else:
            store.db.execute("DROP TRIGGER IF EXISTS audit_no_update")
            store.db.execute("DROP TRIGGER IF EXISTS audit_no_delete")

    def _seed_multi_year_sql(self, store):
        rows = [
            ("sam", "log_contact", "ZF-1", "y2024-1", "2024-03-10T09:00:00"),
            ("sam", "log_contact", "ZF-1", "y2024-2", "2024-11-20T14:30:00"),
            ("sam", "log_contact", "ZF-1", "y2025-1", "2025-02-15T11:00:00"),
            ("sam", "log_contact", "ZF-1", "y2025-2", "2025-09-05T16:45:00"),
            ("sam", "log_contact", "ZF-1", "y2026-1", "2026-01-12T08:15:00"),
            ("sam", "log_contact", "ZF-1", "y2026-2", "2026-06-01T10:00:00"),
        ]
        with store.dblock:
            store.db.execute("BEGIN IMMEDIATE")
            store._append_audit(rows)
            store.db.execute("COMMIT")

    def test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years(self):
        s = SqlStore(self.data, self.db)
        self.addCleanup(s.db.close)
        self._seed_multi_year_sql(s)
        rep = s.require_verified_ledger_for_reliance(current_year=2026)
        self.assertTrue(rep["reliance_allowed"])
        self.assertTrue(rep["audit_head_matches"])
        self.assertEqual(rep["entries"], 6)
        self.assertEqual(rep["sealed_years"], ["2024", "2025"])
        self.assertTrue(rep["years"]["2024"]["sealed"] and rep["years"]["2025"]["sealed"])
        self.assertFalse(rep["years"]["2026"]["sealed"])
        self.assertEqual(rep["problems"], [])

        # Tamper a sealed 2025 row after dropping the backend append-only trigger
        self._drop_audit_triggers(s)
        s.db.execute("UPDATE audit SET detail=? WHERE at=?", ("tampered-2025", "2025-02-15T11:00:00"))
        tampered = s.verify_ledger_before_reliance(current_year=2026)
        self.assertFalse(tampered["reliance_allowed"])
        with self.assertRaises(LedgerRelianceError):
            s.require_verified_ledger_for_reliance(current_year=2026)

        # Reuse s (2024 and 2025 are sealed in s.digest_dir and triggers are dropped): drop 2024 rows and rebuild chain + audit_head
        s.db.execute("DELETE FROM audit")
        prev = ledger.GENESIS
        kept = [
            ("2025-02-15T11:00:00", "sam", "log_contact", "ZF-1", "y2025-1"),
            ("2025-09-05T16:45:00", "sam", "log_contact", "ZF-1", "y2025-2"),
            ("2026-01-12T08:15:00", "sam", "log_contact", "ZF-1", "y2026-1"),
        ]
        for at, who, action, cid, detail in kept:
            entry = ledger.make_entry(who, action, cid, detail, prev, at)
            s.db.execute(
                "INSERT INTO audit (at, who, action, case_id, detail, prev, hash) VALUES (?,?,?,?,?,?,?)",
                (at, who, action, cid, detail, prev, entry["hash"]),
            )
            prev = entry["hash"]
        s.db.execute("UPDATE audit_head SET count=?, hash=? WHERE id=1", (len(kept), prev))
        self.assertTrue(s.verify_audit())
        dropped = s.verify_ledger_before_reliance(current_year=2026)
        self.assertFalse(dropped["reliance_allowed"])
        self.assertEqual(dropped["missing_years"], ["2024"])
        self.assertIn("missing_audit_year", {p["code"] for p in dropped["problems"]})

    def test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head(self):
        s = SqlStore(self.data, self.db)
        self.addCleanup(s.db.close)
        self._seed_multi_year_sql(s)
        s.require_verified_ledger_for_reliance(current_year=2026)
        self._drop_audit_triggers(s)
        # Delete the unsealed tail 2026 entry without updating audit_head
        s.db.execute("DELETE FROM audit WHERE at=?", ("2026-06-01T10:00:00",))
        mismatch = s.verify_ledger_before_reliance(current_year=2026)
        self.assertFalse(mismatch["reliance_allowed"])
        self.assertFalse(mismatch["audit_head_matches"])
        self.assertIn("audit_head_mismatch", {p["code"] for p in mismatch["problems"]})

        s.db.execute("DELETE FROM audit_head WHERE id=1")
        missing = s.verify_ledger_before_reliance(current_year=2026)
        self.assertFalse(missing["reliance_allowed"])
        self.assertIn("audit_head_missing", {p["code"] for p in missing["problems"]})

    def _verify_mssqlstore_factory_hook(self, base_sql_cls):
        tsql_drop = "IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only"

        class _MssqlSqlGuard:
            def __init__(self, raw, stats):
                self._raw = raw
                self._stats = stats

            def execute(self, sql, *args):
                if sql.strip() == tsql_drop:
                    self._stats["dropped_triggers"] += 1
                    self._raw.execute("DROP TRIGGER IF EXISTS audit_no_update")
                    return self._raw.execute("DROP TRIGGER IF EXISTS audit_no_delete")
                if "audit_no_update" in sql or "audit_no_delete" in sql:
                    raise AssertionError(f"SQLite trigger DDL issued against MssqlStore: {sql}")
                norm = " ".join(sql.split()).upper()
                if norm.startswith("INSERT INTO AUDIT"):
                    if norm.startswith("INSERT INTO AUDIT VALUES"):
                        raise AssertionError(f"Columnless INSERT INTO audit targets IDENTITY seq: {sql}")
                    m = re.match(r"^INSERT INTO AUDIT\s*\(([^)]*)\)", norm)
                    if m and "SEQ" in {c.strip().strip('[]"') for c in m.group(1).split(",")}:
                        raise AssertionError(f"Explicit seq column in INSERT INTO audit violates IDENTITY: {sql}")
                return self._raw.execute(sql, *args)

            def __getattr__(self, name):
                return getattr(self._raw, name)

        class _SimulatedMssqlStore(MssqlStore):
            _priority_correction_rows = base_sql_cls._priority_correction_rows
            dberror = base_sql_cls.dberror
            _open = base_sql_cls._open
            _epoch_sql = base_sql_cls._epoch_sql
            _add_column_default = base_sql_cls._add_column_default
            assistant_connection = base_sql_cls.assistant_connection
            _create_schema = base_sql_cls._create_schema
            _has_rec_order = base_sql_cls._has_rec_order
            _create_rec_order_index = base_sql_cls._create_rec_order_index
            _rec_order_indexes_present = base_sql_cls._rec_order_indexes_present
            _create_indexes = base_sql_cls._create_indexes
            _columns = base_sql_cls._columns
            _meta_set = base_sql_cls._meta_set
            _insert_ignore = base_sql_cls._insert_ignore
            _contains = staticmethod(base_sql_cls._contains)
            _limit = staticmethod(base_sql_cls._limit)

            def __init__(self, data_path, backing_db, state_dir, stats):
                base_sql_cls.__init__(
                    self,
                    data_path,
                    backing_db,
                    digest_dir=os.path.join(state_dir, "digests"),
                )
                self.db = _MssqlSqlGuard(self.db, stats)

        overridden_on_mssql = {
            "test_ledger_is_append_only_and_detects_tampering",
            "test_list_filters_use_indexes",
        }
        expected_trigger_drops = {
            "test_pre_reliance_multi_year_verification_passes_and_blocks_tampering_and_dropped_years": 1,
            "test_pre_reliance_detects_sql_audit_head_mismatch_and_missing_head": 1,
        }
        inherited_methods = sorted(
            name
            for name in dir(SqlStoreTests)
            if name.startswith("test_") and name not in overridden_on_mssql
        )
        self.assertEqual(len(inherited_methods), 10)

        with tempfile.TemporaryDirectory() as server_dir:
            for idx, method_name in enumerate(inherited_methods):
                backing_db = os.path.join(server_dir, f"mssql-sim-{idx}.sqlite")
                stats = {"dropped_triggers": 0}
                case = SqlStoreTests(method_name)
                case._running_factory_hook = True

                def factory(data, db, *_a, _backing=backing_db, _stats=stats, _case=case, **_k):
                    store = _SimulatedMssqlStore(data, _backing, state_dir=os.path.dirname(db), stats=_stats)
                    _case.addCleanup(store.db.close)
                    return store

                with patch.dict(globals(), {"SqlStore": factory}):
                    case.setUp()
                    try:
                        getattr(case, method_name)()
                        self.assertFalse(os.path.exists(case.db), method_name)
                        self.assertEqual(
                            stats["dropped_triggers"],
                            expected_trigger_drops.get(method_name, 0),
                            method_name,
                        )
                    finally:
                        case.doCleanups()
                        case.tearDown()

    def test_pre_reliance_scrubs_driver_secrets_and_is_inherited_by_mssqlstore(self):
        from zava_forward.core.sqlstore import SqlStore as BaseSqlStore

        self.assertTrue(issubclass(MssqlStore, BaseSqlStore))
        mssql_db = os.path.join(self.tmp.name, "mssql-double.sqlite")
        base = BaseSqlStore(self.data, mssql_db)
        self.addCleanup(base.db.close)
        self._seed_multi_year_sql(base)
        ms = MssqlStore.__new__(MssqlStore)
        ms.db = base.db
        ms.dblock = base.dblock
        ms.digest_dir = base.digest_dir
        ms.lock = base.lock
        ok = ms.require_verified_ledger_for_reliance(current_year=2026)
        self.assertTrue(ok["reliance_allowed"])
        self.assertEqual(ok["sealed_years"], ["2024", "2025"])

        sentinel = "Server=tcp:secret-sql.database.windows.net;Password=SUPER_SECRET_PASSWORD_99;"

        class FakeDriverError(Exception):
            pass

        with (
            patch.object(MssqlStore, "dberror", property(lambda inst: FakeDriverError)),
            patch.object(ms, "db") as fake_db,
        ):
            fake_db.execute.side_effect = FakeDriverError(sentinel)
            failed = ms.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(failed["reliance_allowed"])
            self.assertIn("audit_unreadable", {p["code"] for p in failed["problems"]})
            self.assertNotIn(sentinel, json.dumps(failed))
            with self.assertRaises(LedgerRelianceError) as cm:
                ms.require_verified_ledger_for_reliance(current_year=2026)
            self.assertNotIn(sentinel, str(cm.exception))
            self.assertIsNone(cm.exception.__cause__)

        if not getattr(self, "_running_factory_hook", False):
            self._verify_mssqlstore_factory_hook(BaseSqlStore)


if __name__ == "__main__":
    unittest.main()
