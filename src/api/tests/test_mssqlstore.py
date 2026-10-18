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
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError

ON = os.environ.get("ZF_TEST_MSSQL") == "1"
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


if __name__ == "__main__":
    unittest.main()
