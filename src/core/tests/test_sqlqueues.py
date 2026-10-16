"""Durable queue flags, transactional dependencies, migration and dialect contracts."""

import json
import re
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from building_fixture import fixture, hold
from test_sqlreads import STAFF, dataset, queue_cases
from zava_forward.core import ranking, taskqueues
from zava_forward.core.mssqlstore import TABLES, MssqlStore, _Conn, _indexes
from zava_forward.core.sqlstore import QUEUE_COLS, SqlStore

AS_OF = "2026-10-16"


class SqlQueueMembership(unittest.TestCase):
    """Also inherited by the existing opt-in SQL Server harness."""

    def make_store(self, seed: Path) -> Any:
        return SqlStore(str(seed), str(seed.with_suffix(".sqlite")))

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.seed = Path(self.tmp.name) / "synthetic.json"
        data = dataset(queue_cases(80))
        data["as_of"] = AS_OF
        self.seed.write_text(json.dumps(data))
        self.store = self.make_store(self.seed)
        self.addCleanup(self.store.db.close)

    def assert_flags(self, store: Any) -> None:
        with store.lock:
            rows = store.db.execute(f"SELECT id, {', '.join(QUEUE_COLS)} FROM cases").fetchall()
            for cid, *flags in rows:
                queues = store.work_context(store.cases[cid], None)["queues"]
                self.assertEqual(flags, [int(col[6:] in queues) for col in QUEUE_COLS], cid)

    def test_seed_and_every_case_write_maintain_physical_flags(self) -> None:
        self.assert_flags(self.store)
        with patch.object(self.store, "_work_context", wraps=self.store._work_context) as evaluator:
            with self.store.lock:
                case = self.store._case("ZF-00001")
                case.update(
                    stage_since=AS_OF,
                    documents=[dict(kind="EPC", at="2026-01-01")],
                    resident_update=dict(due_at="2026-10-15T12:00Z"),
                    handoff=dict(state="Offered"),
                )
                self.store.save()
            self.assertEqual(evaluator.call_count, 1)
        self.assertEqual(
            self.store.db.execute(
                "SELECT queue_new, queue_stale, queue_overdue, queue_unowned FROM cases WHERE id=?",
                ("ZF-00001",),
            ).fetchone(),
            (1, 1, 1, 1),
        )
        self.assert_flags(self.store)
        with self.store.lock:
            self.store._case("ZF-00001")["closed"] = True
            self.store.save()
        self.assertEqual(
            self.store.db.execute(
                f"SELECT {', '.join(QUEUE_COLS)} FROM cases WHERE id=?", ("ZF-00001",)
            ).fetchone(),
            (0,) * len(QUEUE_COLS),
        )
        self.assert_flags(self.store)

    def test_cold_and_hot_lookup_never_evaluate_nonreturned_cases(self) -> None:
        self.store.page_cases(STAFF[1], "all", filters={"queue": "new"}, limit=3)
        with self.store.lock:
            self.store._case("ZF-00001")["stage_since"] = AS_OF
            self.store.save()
        for queue, _, _ in taskqueues.DEFINITIONS:
            with patch.object(
                self.store, "_work_context", wraps=self.store._work_context
            ) as evaluator:
                for _ in range(2):
                    page = self.store.page_cases(STAFF[1], "all", filters={"queue": queue}, limit=3)
                self.assertEqual(evaluator.call_count, 2 * len(page["items"]), queue)

    def test_failed_case_evaluation_rolls_back_body_flags_generation_and_sequence(self) -> None:
        before = self.store.db.execute("SELECT * FROM cases ORDER BY id").fetchall()
        meta = self.store.db.execute("SELECT key, value FROM meta ORDER BY key").fetchall()
        with patch.object(self.store, "_work_context", side_effect=ValueError("synthetic failure")):
            with self.assertRaisesRegex(ValueError, "synthetic failure"), self.store.lock:
                self.store._case("ZF-00001")["stage_since"] = AS_OF
                self.store.save()
        self.assertEqual(
            before, self.store.db.execute("SELECT * FROM cases ORDER BY id").fetchall()
        )
        self.assertEqual(
            meta, self.store.db.execute("SELECT key, value FROM meta ORDER BY key").fetchall()
        )
        self.assert_flags(self.store)

    def test_refresh_only_generations_invalidate_other_process_hot_ids(self) -> None:
        other = self.make_store(self.seed)
        self.addCleanup(other.db.close)
        expected = self.store.list_cases(STAFF[1], "all", filters={"queue": "new"})
        original = dict(ranking.CURRENT)
        for changed in ("snapshot", "day", "policy", "definition"):
            with self.subTest(changed=changed):
                patches: Any
                if changed == "snapshot":
                    other.as_of = "2026-11-30"
                    patches = patch.object(other, "as_of", "2026-11-30")
                elif changed == "day":
                    patches = patch("zava_forward.core.controls.today", return_value="2032-01-01")
                elif changed == "policy":
                    patches = patch.dict(
                        ranking.CURRENT, dict(original, status="Approved", owner="Synthetic owner")
                    )
                else:
                    patches = patch.object(taskqueues, "VERSION", "synthetic-next-definition")
                with patches:
                    other.list_cases(STAFF[1], "all", filters={"queue": "new"})
                other.as_of = AS_OF
                self.assertEqual(
                    self.store.list_cases(STAFF[1], "all", filters={"queue": "new"}),
                    expected,
                )
                self.assert_flags(self.store)

    def test_refresh_failure_does_not_certify_partial_backfill(self) -> None:
        self.store.db.execute("UPDATE cases SET queue_new=0")
        self.store.db.execute("UPDATE meta SET value='' WHERE key='queue_context'")
        generation = self.store.db.execute(
            "SELECT value FROM meta WHERE key='queue_generation'"
        ).fetchone()
        with patch.object(self.store, "_work_context", side_effect=ValueError("backfill failure")):
            with self.assertRaisesRegex(ValueError, "backfill failure"):
                self.store._ensure_queue_membership()
        self.assertEqual(
            self.store.db.execute("SELECT value FROM meta WHERE key='queue_context'").fetchone(),
            ("",),
        )
        self.assertEqual(
            self.store.db.execute("SELECT value FROM meta WHERE key='queue_generation'").fetchone(),
            generation,
        )
        reopened = self.make_store(self.seed)
        self.addCleanup(reopened.db.close)
        self.assert_flags(reopened)

    def test_shared_write_uses_authoritative_state_not_stale_process_documents(self) -> None:
        # A second fixture has linked homes, scoped holds and procurement package IDs.
        data = fixture()
        data["as_of"] = AS_OF
        linked = Path(self.tmp.name) / "linked.json"
        linked.write_text(json.dumps(data))
        writer = self.make_store(linked)
        reader = self.make_store(linked)
        self.addCleanup(writer.db.close)
        self.addCleanup(reader.db.close)
        with reader.lock:
            reader._case("ZF-3")["stage_since"] = AS_OF
            with writer.lock:
                writer.data["buildings"][0]["holds"].append(hold())
                writer.save()
            reader.save()
        self.assert_flags(reader)
        self.assertEqual(
            reader.db.execute("SELECT queue_blocked FROM cases WHERE id=?", ("ZF-2",)).fetchone(),
            (1,),
        )
        # Removing a linked home makes the explicit building home scope invalid.
        with writer.lock:
            writer._case("ZF-2").pop("building_id")
            writer.save()
        with reader.lock:
            pass
        self.assert_flags(reader)
        self.assertEqual(
            reader.db.execute("SELECT queue_blocked FROM cases WHERE id=?", ("ZF-3",)).fetchone(),
            (1,),
        )

    def test_write_between_initial_sync_and_lookup_keeps_ranks_and_context_consistent(self) -> None:
        other = self.make_store(self.seed)
        self.addCleanup(other.db.close)
        lookup = self.store._queue_candidates

        def interleaved(queue: str) -> Any:
            with other.lock:
                case = other._case("ZF-00001")
                case.update(stage_since=AS_OF, days_in_stage=999)
                other.save()
            return lookup(queue)

        with patch.object(self.store, "_queue_candidates", new=interleaved):
            page = self.store.page_cases(STAFF[1], "all", filters={"queue": "new"}, limit=80)
        expected = other.page_cases(STAFF[1], "all", filters={"queue": "new"}, limit=80)
        self.assertEqual(page, expected)


class SqlQueueMigration(unittest.TestCase):
    def test_old_schema_backfills_shared_context_and_reopens_without_seed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "synthetic.json"
            data = fixture()
            data["as_of"] = AS_OF
            data["buildings"][0]["holds"].append(hold())
            seed.write_text(json.dumps(data))
            store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
            before = store.db.execute("SELECT id, body, rowversion, seq FROM cases").fetchall()
            head = store.ledger_head()
            for col in QUEUE_COLS:
                store.db.execute(f"DROP INDEX ix_cases_{col}")
                store.db.execute(f"ALTER TABLE cases DROP COLUMN {col}")
            store.db.execute("DELETE FROM meta WHERE key IN ('as_of','queue_context')")
            store.db.close()
            seed.unlink()
            with patch.dict("os.environ", {"ZF_AS_OF": AS_OF}):
                upgraded = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
            self.addCleanup(upgraded.db.close)
            self.assertEqual(
                before,
                upgraded.db.execute("SELECT id, body, rowversion, seq FROM cases").fetchall(),
            )
            self.assertEqual(head, upgraded.ledger_head())
            self.assertEqual(upgraded.as_of, AS_OF)
            for cid, *flags in upgraded.db.execute(
                f"SELECT id, {', '.join(QUEUE_COLS)} FROM cases"
            ).fetchall():
                queues = upgraded.work_context(upgraded.cases[cid], None)["queues"]
                self.assertEqual(flags, [int(col[6:] in queues) for col in QUEUE_COLS], cid)
            self.assertEqual(
                upgraded.db.execute("SELECT queue_blocked FROM cases WHERE id='ZF-2'").fetchone(),
                (1,),
            )

    def test_every_queue_lookup_uses_its_covering_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "synthetic.json"
            data = dataset(queue_cases(100))
            data["as_of"] = AS_OF
            seed.write_text(json.dumps(data))
            store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            for col in QUEUE_COLS:
                plan = " ".join(store.explain(f"SELECT id FROM cases WHERE {col}=1"))
                self.assertIn(f"ix_cases_{col}", plan)
                self.assertIn("SEARCH", plan)


class QueueSqlPortability(unittest.TestCase):
    def test_sql_server_fresh_schema_and_indexes_include_all_integer_flags(self) -> None:
        indexes = "\n".join(_indexes())
        for col in QUEUE_COLS:
            self.assertIn(f"{col} INT NOT NULL DEFAULT 0", TABLES["cases"])
            self.assertIn(f"ON cases ({col}, id)", indexes)

    def test_sql_server_migration_adds_integer_flags_and_invalidates_readiness(self) -> None:
        statements: list[str] = []

        class Db:
            def execute(self, sql: str, args: Any = ()) -> Any:
                statements.append(_Conn._rewrite(sql))
                return self

            def fetchall(self) -> list[tuple[str]]:
                return [("id",), ("body",)]

        store: Any = object.__new__(MssqlStore)
        store.db = Db()
        store._migrate_queues()
        for col in QUEUE_COLS:
            self.assertIn(f"ALTER TABLE cases ADD {col} INTEGER NOT NULL DEFAULT 0", statements)
        self.assertTrue(
            any("queue_context" not in sql and "MERGE meta" in sql for sql in statements)
        )
        banned = re.compile(r"INSERT\s+OR|AUTOINCREMENT|PRAGMA", re.I)
        self.assertFalse(any(banned.search(sql) for sql in statements))

    def test_lookup_and_write_refresh_statements_are_portable(self) -> None:
        log: list[str] = []

        class Recorder:
            def __init__(self, db: Any) -> None:
                self.db = db

            def execute(self, sql: str, args: Any = ()) -> Any:
                log.append(_Conn._rewrite(sql))
                return self.db.execute(sql, args)

            def executemany(self, sql: str, rows: Any) -> Any:
                log.append(_Conn._rewrite(sql))
                return self.db.executemany(sql, rows)

        class PortableStore(SqlStore):
            def _meta_set(self, key: str, value: str) -> None:
                self.db.execute("UPDATE meta SET value=? WHERE key=?", (value, key))
                self.db.execute(
                    "INSERT INTO meta (key, value) SELECT ?, ? "
                    "WHERE NOT EXISTS (SELECT 1 FROM meta WHERE key=?)",
                    (key, value, key),
                )

        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "synthetic.json"
            data = dataset(queue_cases(20))
            data["as_of"] = AS_OF
            seed.write_text(json.dumps(data))
            store: Any = PortableStore(str(seed), str(seed.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            store.db = Recorder(store.db)
            with store.lock:
                store._case("ZF-00001")["stage_since"] = AS_OF
                store.save()
            for queue, _, _ in taskqueues.DEFINITIONS:
                store.page_cases(STAFF[1], "all", filters={"queue": queue}, limit=3)
        banned = re.compile(r"INSERT\s+OR|AUTOINCREMENT|PRAGMA|\bLIMIT\b", re.I)
        self.assertFalse([sql for sql in log if banned.search(sql)])
        self.assertTrue(any("UPDATE cases SET queue_new=" in sql for sql in log))
        self.assertTrue(any("WHERE queue_new=1" in sql for sql in log))


if __name__ == "__main__":
    unittest.main()
