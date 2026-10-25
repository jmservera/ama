"""The SQL store behaviour suites again, against a real SQL Server or Azure SQL.

Skipped unless ZF_TEST_MSSQL=1 and the ZF_SQL_* settings point at a database that may be wiped
(the CI job uses a throwaway SQL Server container; never point this at the pilot database).
"""
import importlib
import json
import os
import re
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import building_fixture
import test_buildings as buildingapi
import test_chatthreads as chattests
import test_handoff_api as handofftests
import test_hazard_referral as hazardtests
import test_mvp
import test_sqlreads as reads
import test_sqlqueues as queuetests
import test_sqlstore as base
import test_stock_reconciliation as stocktests
import test_finance_signoffs as financetests
import test_timecapture as timetests
import test_quality_procurement as procurementtests
import test_procurement_api as procurementapi
from zava_forward.core.chatthreads import MSSQL_DDL as CHAT_DDL
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError

ON = os.environ.get("ZF_TEST_MSSQL") == "1"
CHAT_MEMORY_DDL = next(d for d in CHAT_DDL if d.startswith("CREATE TABLE chat_memory ("))
TABLES = ("chat_memory_control", "chat_memory", "chat_message", "chat_thread", "time_entry", "time_request", "time_enabled", "notice_ack", "assistant_events", "assistant_attempts", "assistant_tasks", "assistant_allowance", "audit_head", "audit", "recommendations", "cases", "staff", "meta")


def wipe():
    from zava_forward.core.mssqlstore import _Conn, connection_string
    c = _Conn(connection_string())
    try:
        c.execute("IF OBJECT_ID(N'audit_append_only', N'TR') IS NOT NULL DROP TRIGGER audit_append_only")
        for t in TABLES:
            c.execute(f"IF OBJECT_ID(N'{t}', N'U') IS NOT NULL DROP TABLE {t}")
    finally:
        c.close()


def factory(data, db, *a, **k):
    from zava_forward.core.mssqlstore import MssqlStore
    return MssqlStore(data, state_dir=os.path.dirname(db))


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlBuildings(unittest.TestCase):
    """Constructed building conformance, using real independent SQL sessions."""

    def setUp(self):
        wipe()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def make_store(self, data=None):
        def owned_factory(*args, **kwargs):
            store = factory(*args, **kwargs)
            self.addCleanup(self.close_store, store)
            return store

        with patch.object(building_fixture, "SqlStore", owned_factory):
            return building_fixture.open_store(self.tmp.name, True, data)

    @staticmethod
    def close_store(store):
        if store.db.raw is not None:
            store.db.close()
            store.db.raw = None

    def test_record_and_home_allocations_reopen_without_seed(self):
        data = building_fixture.fixture()
        data["buildings"][0]["dependencies"] = [
            dict(building_fixture.hold(), id="DEP-1", status="Resolved")
        ]
        store = self.make_store(data)
        building = deepcopy(store.data["buildings"])
        homes = deepcopy(store.cases)
        store.save()
        self.close_store(store)
        reopened = None
        try:
            Path(self.tmp.name, "synthetic.json").unlink()
            reopened = factory("nonexistent-constructed-seed.json", store.db_path)
            self.assertEqual(reopened.data["buildings"], building)
            self.assertEqual(reopened.cases, homes)
            view = reopened.building_view(reopened.staff["pam@example.test"], "SYN-B1")
            self.assertEqual(view["costs"][0]["amount_gbp"], "12000.00")
            for home in homes.values():
                self.assertEqual(home["cost_allocation"][0]["amount_gbp"], "6000.00")
            for key in ("cost_allocation", "documents", "quality", "technical", "decision"):
                self.assertNotIn(key, json.dumps(view))
        finally:
            if reopened is not None:
                reopened.db.close()

    def test_independent_hold_visibility_and_stale_document_conflict(self):
        first = self.make_store(building_fixture.fixture())
        second = self.make_store()
        self.assertIsNot(first.db.raw, second.db.raw)
        first.data["buildings"][0]["holds"].append(building_fixture.hold())
        first.save()
        view = second.building_view(second.staff["pam@example.test"], "SYN-B1")
        self.assertEqual(view["holds"], [building_fixture.hold()])
        self.assertIn("Building SYN-B1", " ".join(second.detail("ZF-2")["gate"]))
        with first.lock:
            second.data["buildings"][0]["version"] = 2
            second.data["buildings"][0]["name"] = "Committed winning building"
            second.save()
            winner = deepcopy(second.data["buildings"])
            first.data["buildings"][0]["version"] = 3
            first.data["buildings"][0]["holds"] = []
            with self.assertRaises(ConflictError):
                first.save()
        self.assertEqual(first.data["buildings"], winner)
        third = self.make_store()
        self.assertIsNot(third.db.raw, second.db.raw)
        self.assertEqual(third.data["buildings"], winner)
        self.assertEqual(third.data["buildings"][0]["holds"], [building_fixture.hold()])

    def test_hold_scopes_refuse_matching_work_but_keep_orthogonal_controls_usable(self):
        from dataset import supplied_appointment_fixture

        writer = self.make_store(building_fixture.fixture())
        manager = writer.staff["pam@example.test"]
        bindings = [dict(measure="Loft insulation", context_revision=1)]
        wid = writer.issue_work_order(
            manager, "PKG-SHARED", "ZF-2", resident_bindings=bindings
        )
        writer.data["buildings"][0]["holds"].append(building_fixture.hold())
        writer.save()
        store = self.make_store()
        self.assertIsNot(writer.db.raw, store.db.raw)
        cases = deepcopy(store.cases)
        orders = deepcopy(store.data["procurement"]["work_orders"])
        for operation, args, kwargs in (
            (store.advance, (manager, "ZF-2"), {}),
            (store.issue_work_order, (manager, "PKG-SHARED", "ZF-2"),
             dict(resident_bindings=bindings)),
            (store.reissue_work_order, (manager, wid, "Changed scope", "Synthetic change"),
             dict(resident_bindings=bindings)),
        ):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(GateError) as caught:
                    operation(*args, **kwargs)
                self.assertIn("Building SYN-B1", str(caught.exception))
                self.assertIn("Competent review pending", str(caught.exception))
                self.assertEqual(store.cases, cases)
                self.assertEqual(store.data["procurement"]["work_orders"], orders)
        other = store.issue_work_order(
            manager, "PKG-OTHER", "ZF-2", resident_bindings=bindings
        )
        store.reissue_work_order(
            manager, other, "Changed other scope", "Synthetic change",
            resident_bindings=bindings,
        )
        sibling = store.issue_work_order(
            manager, "PKG-SHARED", "ZF-3", resident_bindings=bindings
        )
        supplied_appointment_fixture(store, manager, sibling)
        store.record_wo_appointment(manager, sibling, "Booked", "2099-01-01")
        store.advance(manager, "ZF-3")
        reopened = self.make_store()
        self.assertEqual(reopened.detail("ZF-3")["stage"], "Install booked")
        self.assertEqual(reopened.cases["ZF-2"]["stage"], cases["ZF-2"]["stage"])
        self.assertEqual(reopened.data["buildings"][0]["holds"], [building_fixture.hold()])
        self.assertTrue(reopened.verify_audit())

    def test_clear_building_does_not_supply_independent_home_approvals(self):
        for missing, reason in (
            ("resident", "Resident decision or authority needs confirmation"),
            ("funding", "Funding has not been confirmed"),
            ("technical", "Technical stage:"),
        ):
            with self.subTest(missing=missing):
                wipe()
                data = building_fixture.fixture()
                home = data["cases"][0]
                if missing == "resident":
                    home["decision"]["status"] = "Waiting"
                    home["measure_decisions"] = {}
                elif missing == "funding":
                    home["funding_ok"] = False
                else:
                    home["technical"] = {"signoffs": {}, "design_version": 1}
                store = self.make_store(data)
                before = deepcopy(store.cases)
                view = store.building_view(data["staff"][1], "SYN-B1")
                self.assertEqual(view["holds"], [])
                self.assertEqual(view["dependencies"], [])
                with self.assertRaises(GateError) as caught:
                    store.advance(data["staff"][1], "ZF-2")
                self.assertIn(reason, str(caught.exception))
                self.assertNotIn("Building SYN-B1", str(caught.exception))
                reopened = self.make_store()
                self.assertEqual(reopened.cases, before)
                self.assertEqual(reopened.cases["ZF-3"]["quality"][0]["state"], "Accepted")
                self.close_store(reopened)
                self.close_store(store)

    def test_clear_building_does_not_supply_sibling_qa_or_handover(self):
        data = building_fixture.fixture()
        data["cases"][1]["closed"] = True
        data["cases"][0]["quality"] = [
            dict(data["cases"][1]["quality"][0], state="Submitted", accepted_by=None)
        ]
        store = self.make_store(data)
        before = deepcopy(store.cases)
        view = store.building_view(data["staff"][1], "SYN-B1")
        self.assertEqual([home["closed"] for home in view["homes"]], [False, True])
        with self.assertRaisesRegex(
            ValueError, "This work is 'Submitted'. It cannot go to 'Handed over' from there"
        ):
            store.hand_over_quality(data["staff"][1], "ZF-2", 0, "Synthetic handover", True)
        self.assertEqual(self.make_store().cases, before)


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlBuildingHttp(buildingapi.BuildingHttpTests):
    """Replay existing HTTP projections and gates on the disposable SQL database."""

    def setUp(self):
        wipe()

        def owned_factory(*args, **kwargs):
            store = factory(*args, **kwargs)
            self.addCleanup(MssqlBuildings.close_store, store)
            return store

        try:
            with patch.object(building_fixture, "SqlStore", owned_factory):
                super().setUp()
        finally:
            self.addCleanup(self.close_http)

    def close_http(self):
        server = getattr(self, "server", None)
        thread = getattr(self, "thread", None)
        if server is not None:
            if thread is not None and thread.is_alive():
                server.shutdown()
                thread.join()
            server.server_close()
        if hasattr(self, "tmp"):
            self.tmp.cleanup()

    def tearDown(self):
        # Registered cleanups cover both partial setup and normal completion.
        pass


class _Recorder:
    """Wraps the SQLite connection and records every statement the shared store logic sends."""

    def __init__(self, db, log):
        self._db, self._log = db, log

    def execute(self, sql, args=()):
        self._log.append(sql)
        return self._db.execute(sql, args)

    def __getattr__(self, name):
        return getattr(self._db, name)


class SharedSqlIsPortableTests(unittest.TestCase):
    """Runs without a server: SQLite-only upsert syntax must live only in the dialect hooks MssqlStore overrides."""

    SQLITE_ONLY = re.compile(r"(?i)\bINSERT\s+OR\s+(REPLACE|IGNORE)\b|\bREPLACE\s+INTO\b")

    def test_save_paths_use_dialect_hooks_for_upserts(self):
        log = []

        class Probe(SqlStore):
            def _meta_set(self, key, value):
                self.db.execute("UPDATE meta SET value=? WHERE key=?", (value, key))
                self.db.execute("INSERT INTO meta (key, value) SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key=?)", (key, value, key))

        with tempfile.TemporaryDirectory() as tmp:
            data, db = base.seed(tmp)
            store = Probe(data, db)
            store.db = _Recorder(store.db, log)
            sam = test_mvp.DATA["staff"][0]
            store.log_call(sam, "ZF-1", "Contacted", "ok")
            store.set_decision(sam, "ZF-1", "Accepted")
            store.data.setdefault("procurement", {"packages": [], "work_orders": []})
            store.data["procurement"]["packages"].append({"id": "PKG-PORTABLE"})
            store.save()
            store.db.close()
        self.assertTrue(log)
        self.assertEqual([q for q in log if self.SQLITE_ONLY.search(q)], [])

    def test_sqlite_only_syntax_confined_to_dialect_hooks(self):
        for name in ("sqlstore", "assistants"):
            src = Path(importlib.import_module(f"zava_forward.core.{name}").__file__).read_text()
            hook = None
            for line in src.splitlines():
                m = re.match(r"\s*def (\w+)", line)
                hook = m.group(1) if m else hook
                if self.SQLITE_ONLY.search(line):
                    self.assertIn(hook, ("_meta_set", "_insert_ignore"), f"{name}: SQLite-only SQL in {hook}: {line.strip()}")


    def test_time_capture_sql_is_portable(self):
        src = Path(importlib.import_module("zava_forward.api.timecapture").__file__).read_text()
        a, b = src.index("SQLITE_DDL = ("), src.index("MSSQL_DDL = (")
        shared = src[:a] + src[b:]
        banned = re.compile(r"(?i)\bINSERT\s+OR\s+(REPLACE|IGNORE)\b|\bREPLACE\s+INTO\b|\bAUTOINCREMENT\b|\bPRAGMA\b|\bINSERT OR\b")
        self.assertEqual([l.strip() for l in shared.splitlines() if banned.search(l) and not l.lstrip().startswith(("*", "#"))], [])


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlStockDecisions(unittest.TestCase):
    """Selected canonical stock/technical cases on the throwaway SQL Server."""

    setUp = stocktests.StockReconciliation.setUp
    tech = stocktests.StockReconciliation.tech
    signed = stocktests.StockReconciliation.signed
    durable_state = staticmethod(stocktests.StockReconciliation.durable_state)

    def stores(self):
        wipe()
        path = Path(self.tmp.name) / "constructed.json"
        path.write_text(json.dumps(self.data))
        store = factory(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(store.db.close)
        return [store]

    def reopen(self, store):
        reopened = factory("unused-constructed-seed.json", store.db_path)
        self.addCleanup(reopened.db.close)
        return reopened

    test_four_human_signoffs_and_only_affected_reassessment = stocktests.StockReconciliation.test_four_human_signoffs_and_only_affected_reassessment
    test_withdraw_unblocks_all_signoffs_without_editing_history = stocktests.StockReconciliation.test_withdraw_unblocks_all_signoffs_without_editing_history
    test_sql_current_actor_denial_for_all_decisions = stocktests.StockReconciliation.test_sql_current_actor_denial_for_all_decisions
    test_sql_authority_rechecked_inside_writer_transaction = stocktests.StockReconciliation.test_sql_authority_rechecked_inside_writer_transaction
    test_sql_failed_decisions_do_not_commit_or_flush_success_audit = stocktests.StockReconciliation.test_sql_failed_decisions_do_not_commit_or_flush_success_audit
    test_sql_case_write_failure_restores_decision = stocktests.StockReconciliation.test_sql_case_write_failure_restores_decision
    test_sql_transactional_audit_failure_restores_decision = stocktests.StockReconciliation.test_sql_transactional_audit_failure_restores_decision
    test_sql_decision_scope_restored_on_every_exit = stocktests.StockReconciliation.test_sql_decision_scope_restored_on_every_exit
    test_sql_early_and_persistent_recovery_reads_cannot_flush_failed_work = stocktests.StockReconciliation.test_sql_early_and_persistent_recovery_reads_cannot_flush_failed_work
    test_sql_transaction_refusal_keeps_original_error_when_reload_fails = stocktests.StockReconciliation.test_sql_transaction_refusal_keeps_original_error_when_reload_fails


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlFinanceSignoffs(financetests.SqlFlows):
    @classmethod
    def setUpClass(cls):
        cls._orig, financetests.SqlStore = financetests.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        financetests.SqlStore = cls._orig

    def setUp(self):
        wipe()
        super().setUp()
        self.addCleanup(self.store.db.close)


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlProcurement(procurementtests.SqlFlows):
    def make(self, data, tmp):
        wipe()
        self.path = Path(tmp) / "synthetic.json"
        import json
        self.path.write_text(json.dumps(data))
        self.db = str(Path(tmp) / "unused.sqlite")
        return factory(str(self.path), self.db)

    def reopen(self):
        return factory("nonexistent-seed-is-not-read", self.db)


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlProcurementApi(procurementapi.ProcurementApi):
    def make_store(self, path):
        wipe()
        return factory(str(path), str(path.with_suffix(".sqlite")))


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlHandoffApi(handofftests.HandoffApi):
    """The return/handoff HTTP contract on the CI-only throwaway SQL Server."""

    def make_store(self, path):
        wipe()
        return factory(str(path), str(path.with_suffix(".sqlite")))

    def reopen_store(self):
        return factory("nonexistent-seed-is-not-read", self.store.db_path)


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlHazardReferral(hazardtests.JsonHazardReferral):
    """Canonical hazard semantics and authority/failure probes on the disposable server."""

    sql = True

    def setUp(self):
        wipe()
        super().setUp()

    def open_store(self):
        store = factory(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(store.db.close)
        return store

    test_authority_changes_rechecked_at_transaction_for_caller_and_destination = hazardtests.SqlHazardReferral.test_authority_changes_rechecked_at_transaction_for_caller_and_destination
    test_failed_writes_preserve_prior_pending_audit_and_original_error = hazardtests.SqlHazardReferral.test_failed_writes_preserve_prior_pending_audit_and_original_error
    test_recovery_read_failure_quarantines_hazard_and_keeps_prior_audit = hazardtests.SqlHazardReferral.test_recovery_read_failure_quarantines_hazard_and_keeps_prior_audit


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlTimeCapture(timetests.SharedStoreTests):
    """Enabling record, entries and acknowledgements in Azure SQL / SQL Server, not a local file."""

    def setUp(self):
        wipe()

    def make_store(self, tmp):
        data, db = base.seed(tmp)
        return factory(data, db)


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlChatThreads(chattests.ChatBehaviour, unittest.TestCase):
    """Chat thread storage in Azure SQL / SQL Server with the same behaviour as the in-memory store."""

    def setUp(self):
        wipe()
        super().setUp()

    def make_store(self, tmp):
        data, db = base.seed(tmp)
        return factory(data, db)


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlImproveTests(base.SqlImproveTests):
    @classmethod
    def setUpClass(cls):
        cls._orig, base.SqlStore = base.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        base.SqlStore = cls._orig

    def setUp(self):
        wipe()
        super().setUp()


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlStoreTests(base.SqlStoreTests):
    @classmethod
    def setUpClass(cls):
        cls._orig, base.SqlStore = base.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        base.SqlStore = cls._orig

    def setUp(self):
        wipe()
        super().setUp()

    def test_ledger_is_append_only_and_detects_tampering(self):
        from zava_forward.core.mssqlstore import _Conn, connection_string
        s = factory(self.data, self.db)
        s.log_call(self.sam, "ZF-1", "Contacted", "")
        s.log_call(self.sam, "ZF-1", "Contacted again", "")
        raw = _Conn(connection_string())
        for sql in ("UPDATE audit SET detail='x' WHERE seq=1", "DELETE FROM audit WHERE seq=1"):
            with self.assertRaises(s.dberror):
                raw.execute(sql)
        raw.execute("DROP TRIGGER audit_append_only")
        raw.execute("UPDATE audit SET detail='rewritten' WHERE seq=1")
        self.assertFalse(s.verify_audit())

    test_list_filters_use_indexes = None


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlParity(reads.Parity):
    """SQL list reads on SQL Server give the same answers as the in-memory store (binary collation, paging, ranks)."""

    @classmethod
    def setUpClass(cls):
        cls._orig, reads.SqlStore = reads.SqlStore, factory
        wipe()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        reads.SqlStore = cls._orig
        super().tearDownClass()


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlQueueMembership(queuetests.SqlQueueMembership):
    """Durable flags and cross-process queue writes on the opt-in real engine."""

    def setUp(self):
        self._last_seed = None
        super().setUp()

    def make_store(self, seed):
        if self._last_seed != str(seed):
            wipe()
            self._last_seed = str(seed)
        return factory(str(seed), str(seed.with_suffix(".sqlite")))


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlWrites(reads.Writes):
    @classmethod
    def setUpClass(cls):
        cls._orig, reads.SqlStore = reads.SqlStore, factory

    @classmethod
    def tearDownClass(cls):
        reads.SqlStore = cls._orig

    def setUp(self):
        wipe()



class _FakeLedgerDb:
    """Answers the ledger probe and records every other statement."""

    def __init__(self, ledger):
        self.ledger, self.log = ledger, []

    def execute(self, sql, args=()):
        self.log.append(" ".join(sql.split()))
        return self

    def fetchone(self):
        return (1,) if self.ledger else (0,)


class LedgerAddColumnStatements(unittest.TestCase):
    """Runs without a server: the exact DDL sequence for ledger and ordinary tables."""

    def store(self, ledger):
        from zava_forward.core.mssqlstore import MssqlStore
        s = MssqlStore.__new__(MssqlStore)
        s.db = _FakeLedgerDb(ledger)
        return s

    def test_ordinary_table_keeps_not_null_default(self):
        s = self.store(False)
        s._add_column_default("cases", "priority_correction", "INTEGER", "0")
        self.assertEqual(s.db.log[-1], "ALTER TABLE cases ADD priority_correction INTEGER NOT NULL DEFAULT 0")
        self.assertEqual(len(s.db.log), 2)

    def test_ledger_table_adds_nullable_backfills_then_constrains(self):
        s = self.store(True)
        s._add_column_default("cases", "decision", "TEXT", "''")
        self.assertEqual(s.db.log[1:], [
            "ALTER TABLE cases ADD decision NVARCHAR(40) COLLATE Latin1_General_100_BIN2 NULL",
            "UPDATE cases SET decision = '' WHERE decision IS NULL",
            "ALTER TABLE cases ADD CONSTRAINT ck_cases_decision_nn CHECK (decision IS NOT NULL)",
            "ALTER TABLE cases ADD CONSTRAINT df_cases_decision DEFAULT '' FOR decision",
        ])

    def test_unmapped_text_column_on_a_ledger_table_is_refused(self):
        with self.assertRaises(SystemExit):
            self.store(True)._add_column_default("cases", "unmapped", "TEXT", "''")

    def test_every_added_case_column_has_a_ledger_type(self):
        from zava_forward.core.mssqlstore import LEDGER_TYPES
        from zava_forward.core.sqlstore import CASE_COLS
        integers = {"closed", "hazard", "support", "days", "priority_correction"}
        for col in CASE_COLS:
            self.assertTrue(col in integers or ("cases", col) in LEDGER_TYPES, col)

    def test_sqlite_statement_is_unchanged(self):
        log = []
        s = SqlStore.__new__(SqlStore)
        s.db = _Recorder(__import__("sqlite3").connect(":memory:"), log)
        s.db.execute("CREATE TABLE cases (id TEXT)")
        s._add_column_default("cases", "support", "INTEGER", "0")
        self.assertEqual(log[-1], "ALTER TABLE cases ADD COLUMN support INTEGER NOT NULL DEFAULT 0")


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlLedgerMigration(unittest.TestCase):
    """Throwaway databases made WITH LEDGER = ON (or off) on the harness server; never Azure SQL."""

    NEW_CASE = ("priority_correction", "queue_new", "queue_priority", "queue_stale", "queue_blocked", "queue_overdue", "queue_unowned")
    OLD_CASE_TAIL = "  decision "
    COLS = "id, rowversion, seq, stage, area, wave, owner_code, closed, hazard, postcode, address, body, support, days, rkey, contractor, search, search_c, surname, last_contact, next_visit"

    def setUp(self):
        import uuid
        if os.environ.get("ZF_SQL_SERVER") not in ("localhost", "127.0.0.1", "sql"):
            raise ValueError("Ledger migration tests require the local disposable SQL service, never Azure SQL.")
        self.name = f"zf_ledger_{uuid.uuid4().hex[:10]}"
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.seed = Path(self.tmp.name) / "synthetic.json"
        data = reads.dataset(reads.queue_cases(12))
        data["as_of"] = "2026-10-16"
        self.seed.write_text(json.dumps(data))
        self.addCleanup(self.drop_database)

    def conn(self, database):
        from zava_forward.core.mssqlstore import _Conn, connection_string
        return _Conn(connection_string({**os.environ, "ZF_SQL_DATABASE": database}))

    def drop_database(self):
        master = self.conn("master")
        try:
            master.execute(f"IF DB_ID(N'{self.name}') IS NOT NULL BEGIN ALTER DATABASE [{self.name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE; DROP DATABASE [{self.name}] END")
        finally:
            master.close()

    def create_database(self, ledger):
        master = self.conn("master")
        try:
            master.execute(f"CREATE DATABASE [{self.name}]" + (" WITH LEDGER = ON" if ledger else ""))
        finally:
            master.close()

    def open_store(self):
        from zava_forward.core.mssqlstore import MssqlStore
        store = MssqlStore(str(self.seed), env={**os.environ, "ZF_SQL_DATABASE": self.name}, state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store

    def column_facts(self, db, table, names):
        marks = ",".join("?" * len(names))
        return db.execute(
            "SELECT c.name, t.name, c.max_length, c.collation_name FROM sys.columns c JOIN sys.types t ON c.user_type_id = t.user_type_id "
            f"WHERE c.object_id = OBJECT_ID(?) AND c.name IN ({marks}) ORDER BY c.name", (table, *names)).fetchall()

    def nullable(self, db, table, names):
        marks = ",".join("?" * len(names))
        return {r[0]: r[1] for r in db.execute(
            f"SELECT name, is_nullable FROM sys.columns WHERE object_id = OBJECT_ID(?) AND name IN ({marks})", (table, *names)).fetchall()}

    def make_previous_schema(self, store):
        """The earlier slice's tables: no later derived, queue or chat memory columns."""
        from zava_forward.core.mssqlstore import TABLES
        from zava_forward.core.sqlstore import CASE_COLS, QUEUE_COLS
        added = [c for c in CASE_COLS if c in ("decision", "fstatus", "priority_correction")] + list(QUEUE_COLS)
        rows = store.db.execute(f"SELECT {self.COLS} FROM cases ORDER BY id").fetchall()
        derived = store.db.execute(f"SELECT id, {', '.join(added)} FROM cases ORDER BY id").fetchall()
        facts = self.column_facts(store.db, "cases", added)
        store.db.close()
        db = self.conn(self.name)
        self.addCleanup(db.close)
        old_cases = TABLES["cases"][:TABLES["cases"].index(self.OLD_CASE_TAIL)].rstrip().rstrip(",") + ")"
        old_chat = (CHAT_MEMORY_DDL.replace("item_class NVARCHAR(40) NOT NULL, ", "").replace("source NVARCHAR(200) NOT NULL, ", "")
                    .replace("updated_at NVARCHAR(40) NOT NULL, ", ""))
        db.execute("DROP TABLE cases")
        db.execute("DROP TABLE chat_memory")
        db.execute(old_cases)
        db.execute(old_chat)
        db.executemany(f"INSERT INTO cases ({self.COLS}) VALUES ({','.join('?' * 21)})", rows)
        return db, added, derived, facts

    def run_previous_schema(self, ledger):
        self.create_database(ledger)
        db, added, derived, facts = self.make_previous_schema(self.open_store())
        self.assertFalse(set(added) & {r[0] for r in db.execute("SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(N'cases')").fetchall()})
        self.assertEqual(self.table_kind(db, "cases"), "UPDATABLE_LEDGER_TABLE" if ledger else "")
        return db, added, derived, facts

    def table_kind(self, db, table):
        row = db.execute("SELECT ledger_type_desc FROM sys.tables WHERE object_id = OBJECT_ID(?)", (table,)).fetchone()
        return "" if row[0] == "NON_LEDGER_TABLE" else row[0]

    def test_previous_schema_migrates_in_a_ledger_database(self):
        db, added, derived, facts = self.run_previous_schema(True)
        transactions = "SELECT COUNT(*) FROM sys.database_ledger_transactions"
        before = db.execute(transactions).fetchone()[0]
        store = self.open_store()
        self.assertGreater(db.execute(transactions).fetchone()[0], before)
        self.assertEqual(self.column_facts(db, "cases", added), facts)
        self.assertEqual(db.execute(f"SELECT id, {', '.join(added)} FROM cases ORDER BY id").fetchall(), derived)
        self.assertEqual(len(store.cases), 12)
        self.assertEqual(self.table_kind(db, "cases"), "UPDATABLE_LEDGER_TABLE")
        self.assertEqual(self.table_kind(db, "audit"), "APPEND_ONLY_LEDGER_TABLE")
        self.assertTrue(store.verify_audit())
        self.assertEqual(db.execute("SELECT COUNT(*) FROM cases WHERE priority_correction IS NULL OR decision IS NULL").fetchone()[0], 0)
        self.assertEqual([r[0] for r in db.execute("SELECT name FROM sys.columns WHERE object_id = OBJECT_ID(N'chat_memory') AND name IN ('item_class','source','updated_at') ORDER BY name").fetchall()],
                         ["item_class", "source", "updated_at"])
        self.assertEqual(db.execute("SELECT COUNT(*) FROM sys.check_constraints WHERE name LIKE N'ck[_]cases[_]%[_]nn'").fetchone()[0], len(added))
        with self.assertRaises(store.dberror):
            db.execute("UPDATE cases SET priority_correction = NULL WHERE id = (SELECT MIN(id) FROM cases)")
        with self.assertRaises(store.dberror):
            db.execute("UPDATE cases SET decision = NULL WHERE id = (SELECT MIN(id) FROM cases)")
        db.execute("INSERT INTO cases (id, seq, stage, area, wave, owner_code, closed, hazard, postcode, address, body) VALUES (N'ZF-DEFAULT', 1, N'', N'', N'', N'', 0, 0, N'', N'', N'{}')")
        self.assertEqual(db.execute("SELECT priority_correction, queue_new, decision, last_contact FROM cases WHERE id = N'ZF-DEFAULT'").fetchone(), (0, 0, "", "0000"))
        settled = db.execute(transactions).fetchone()[0]
        self.open_store()
        self.assertEqual(db.execute(transactions).fetchone()[0], settled)

    def test_failure_after_backfill_leaves_no_partial_schema_and_can_be_retried(self):
        from zava_forward.core.mssqlstore import MssqlStore
        db, added, derived, facts = self.run_previous_schema(True)
        original, calls = MssqlStore._add_column_default, []

        def fail_on_second(store, *args):
            calls.append(args[1])
            if len(calls) == 2:
                raise RuntimeError("injected after the first backfill")
            return original(store, *args)

        with patch.object(MssqlStore, "_add_column_default", fail_on_second), self.assertRaises(RuntimeError):
            self.open_store()
        self.assertEqual(self.column_facts(db, "cases", added), [])
        self.assertEqual(db.execute("SELECT COUNT(*) FROM sys.check_constraints WHERE name LIKE N'ck[_]cases[_]%'").fetchone()[0], 0)
        self.assertEqual(db.execute("SELECT COUNT(*) FROM cases").fetchone()[0], 12)
        self.open_store()
        self.assertEqual(self.column_facts(db, "cases", added), facts)

    def test_populated_chat_memory_failure_rolls_back_and_retries(self):
        from zava_forward.core.chatthreads import MEMORY_ADDED
        from zava_forward.core.mssqlstore import MssqlStore
        db, _, _, _ = self.run_previous_schema(True)
        names = [c for c, _ in MEMORY_ADDED]
        db.execute("INSERT INTO chat_memory (id, owner, owner_role, content, redactions, created_at) VALUES (N'm1', N'o', N'r', N'kept content', N'', N'2026-10-24')")
        original, calls = MssqlStore._add_column_default, []

        def fail_after_first_chat_backfill(store, table, *args):
            if table == "chat_memory":
                calls.append(args[0])
                if len(calls) == 2:
                    raise RuntimeError("injected after the first chat_memory backfill")
            return original(store, table, *args)

        with patch.object(MssqlStore, "_add_column_default", fail_after_first_chat_backfill), self.assertRaises(RuntimeError):
            self.open_store()
        self.assertEqual(calls, names[:2])
        self.assertEqual(self.column_facts(db, "chat_memory", names), [])
        self.assertEqual(db.execute("SELECT COUNT(*) FROM sys.check_constraints WHERE name LIKE N'ck[_]chat[_]memory[_]%'").fetchone()[0], 0)
        self.assertEqual(db.execute("SELECT COUNT(*) FROM sys.default_constraints WHERE name LIKE N'df[_]chat[_]memory[_]%'").fetchone()[0], 0)
        store = self.open_store()
        self.assertEqual(len(self.column_facts(db, "chat_memory", names)), len(names))
        row = db.execute(f"SELECT content, {', '.join(names)} FROM chat_memory WHERE id = N'm1'").fetchone()
        self.assertEqual(row[0], "kept content")
        self.assertEqual(list(row[1:]), [d for _, d in MEMORY_ADDED])
        for col in names:
            with self.assertRaises(store.dberror):
                db.execute(f"UPDATE chat_memory SET {col} = NULL WHERE id = N'm1'")

    def test_previous_schema_still_migrates_in_an_ordinary_database(self):
        db, added, derived, facts = self.run_previous_schema(False)
        self.open_store()
        self.assertEqual([r[:2] for r in self.column_facts(db, "cases", added) if r[0] in ("decision", "fstatus")], [("decision", "text"), ("fstatus", "text")])
        self.assertEqual([r for r in self.column_facts(db, "cases", added) if r[0] not in ("decision", "fstatus")], [r for r in facts if r[0] not in ("decision", "fstatus")])
        self.assertTrue(all(v == 0 for v in self.nullable(db, "cases", added).values()))
        self.assertEqual(db.execute(f"SELECT id, {', '.join(added)} FROM cases ORDER BY id").fetchall(), derived)

    def test_fresh_ledger_database_initialises(self):
        self.create_database(True)
        store = self.open_store()
        self.assertEqual(self.table_kind(store.db, "audit"), "APPEND_ONLY_LEDGER_TABLE")
        self.assertEqual(len(store.cases), 12)

    def merge_roundtrip(self, ledger):
        import copy
        self.create_database(ledger)
        store = self.open_store()
        store.audit("seed", "proof", "-", "existing")
        store.save()
        data = json.loads(self.seed.read_text())
        data["cases"] += [dict(copy.deepcopy(data["cases"][0]), id=f"ZF-SEED-{n}") for n in range(3)]
        merge = Path(self.tmp.name) / "merge.json"
        merge.write_text(json.dumps(data))
        before = (store.db.execute("SELECT id, body, seq FROM cases ORDER BY id").fetchall(),
                  store.db.execute("SELECT seq, prev, hash FROM audit ORDER BY seq").fetchall())
        self.assertEqual(store.merge_seed(merge)["to_insert"], 3)
        self.assertEqual(store.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0], 12)
        with patch.object(SqlStore, "_append_audit", side_effect=RuntimeError("injected")):
            with self.assertRaises(RuntimeError):
                store.merge_seed(merge, apply=True)
        self.assertEqual(store.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0], 12)
        self.assertTrue(store.merge_seed(merge, apply=True, expect_added=3)["applied"])
        self.assertEqual(store.db.execute("SELECT COUNT(*) FROM cases").fetchone()[0], 15)
        after = store.db.execute("SELECT seq, prev, hash FROM audit ORDER BY seq").fetchall()
        self.assertEqual([tuple(r) for r in after[:len(before[1])]], [tuple(r) for r in before[1]])
        self.assertEqual(len(after), len(before[1]) + 1)
        now = [tuple(r) for r in store.db.execute("SELECT id, body, seq FROM cases ORDER BY id").fetchall()]
        for row in before[0]:
            self.assertIn(tuple(row), now)
        self.assertFalse(store.merge_seed(merge, apply=True, expect_added=0)["applied"])
        self.assertEqual(store.db.execute("SELECT COUNT(*) FROM audit").fetchone()[0], len(after))
        self.assertTrue(store.verify_audit())

    def test_seed_merge_on_ledger_database(self):
        self.merge_roundtrip(True)

    def test_seed_merge_on_plain_database(self):
        self.merge_roundtrip(False)


class MssqlLedgerMigrationGuard(unittest.TestCase):
    def test_remote_server_is_refused_before_any_connection_or_cleanup(self):
        case = MssqlLedgerMigration("test_fresh_ledger_database_initialises")
        with patch.dict(os.environ, {"ZF_SQL_SERVER": "example.database.windows.net"}), \
                patch("zava_forward.core.mssqlstore._Conn", side_effect=AssertionError("connected")) as conn, \
                patch.object(MssqlLedgerMigration, "drop_database", side_effect=AssertionError("cleanup")) as drop:
            with self.assertRaises(ValueError):
                case.setUp()
            case.doCleanups()
        conn.assert_not_called()
        drop.assert_not_called()


if __name__ == "__main__":
    unittest.main()
