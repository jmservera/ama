"""Newest-created order of priority recommendations across SQL reloads (#1292), synthetic data."""

import copy
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

SECOND = "2026-11-08T10:00:00"
EARLIER = "2026-11-08T09:00:00"


class JsonPriorityOrder(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        self.path.write_text(json.dumps(data))
        self.sam, self.pam = data["staff"][:2]
        self.store = self.open_store()
        self.template = self.seed(self.store)

    def open_store(self) -> Any:
        return Store(str(self.path))

    def seed(self, store: Any) -> dict[str, Any]:
        """One real workflow-only proposal; later ones are clones with chosen ids and users."""
        made = store.ai_priority(self.sam, mode="workflow-only")
        return copy.deepcopy(
            next(r for r in store.data["recommendations"] if r["id"] == made["id"])
        )

    def add(
        self,
        store: Any,
        rid: str,
        user: dict[str, Any],
        created: str = SECOND,
        kind: str | None = None,
    ) -> None:
        rec = copy.deepcopy(self.template)
        rec.update(id=rid, user=user["email"], created=created)
        if kind:
            rec["kind"] = kind
        store.data["recommendations"].append(rec)

    def latest(self, store: Any, user: dict[str, Any] | None = None) -> str:
        return str(store.latest_priority(user or self.sam)["id"])

    def test_batch_in_one_save_keeps_creation_order_despite_id_order(self) -> None:
        for rid in ("zzz000000001", "mmm000000002", "aaa000000003"):
            self.add(self.store, rid, self.sam)
        self.store.save()
        self.assertEqual(self.latest(self.store), "aaa000000003")
        self.assertEqual(self.latest(self.open_store()), "aaa000000003")

    def test_edit_of_older_proposal_does_not_make_it_newest(self) -> None:
        for rid in ("zzz000000001", "mmm000000002", "aaa000000003"):
            self.add(self.store, rid, self.sam)
            self.store.save()
        self.store.resolve_priority(
            self.sam, "zzz000000001", "accept", "SYN review of an older proposal"
        )
        self.assertEqual(self.latest(self.store), "aaa000000003")
        self.assertEqual(self.latest(self.open_store()), "aaa000000003")

    def test_each_user_gets_own_newest_and_ai_task_is_excluded(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.add(self.store, "yyy000000002", self.pam)
        self.add(self.store, "mmm000000003", self.sam)
        self.add(self.store, "bbb000000004", self.pam)
        self.add(self.store, "aaa000000005", self.sam, kind="ai_task")
        self.store.save()
        for store in (self.store, self.open_store()):
            self.assertEqual(self.latest(store), "mmm000000003")
            self.assertEqual(self.latest(store, self.pam), "bbb000000004")

    def test_decision_boundary_unchanged_by_ordering(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.add(self.store, "aaa000000002", self.sam)
        self.store.save()
        view = self.store.latest_priority(self.sam)
        self.assertEqual(view["status"], "Proposed")
        self.assertIsNone(view.get("resolved_by"))


class SqlitePriorityOrder(JsonPriorityOrder):
    sql = True

    def open_store(self) -> Any:
        store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(store.db.close)
        return store

    def legacy_ddl(self) -> str:
        return (
            "CREATE TABLE recommendations (id TEXT PRIMARY KEY, "
            "rowversion INTEGER NOT NULL DEFAULT 1, "
            "seq INTEGER NOT NULL, user TEXT NOT NULL, body TEXT NOT NULL)"
        )

    def make_legacy(self, store: Any, rows: list[tuple[str, int, str, str]]) -> None:
        """Replace the table by the pre-fix schema holding (id, seq, user, body) rows."""
        store.db.execute("DROP TABLE recommendations")
        store.db.execute(self.legacy_ddl())
        for rid, seq, user, body in rows:
            store.db.execute(
                "INSERT INTO recommendations (id, rowversion, seq, user, body) VALUES (?,1,?,?,?)",
                (rid, seq, user, body),
            )

    def body(self, rid: str, created: str) -> str:
        return json.dumps(dict(self.template, id=rid, created=created))

    def test_edit_of_older_proposal_is_not_newest_after_incremental_reload(self) -> None:
        for rid in ("zzz000000001", "mmm000000002", "aaa000000003"):
            self.add(self.store, rid, self.sam)
            self.store.save()
        watcher = self.open_store()
        self.assertEqual(self.latest(watcher), "aaa000000003")
        self.store.resolve_priority(
            self.sam, "zzz000000001", "accept", "SYN review of an older proposal"
        )
        self.assertEqual(self.latest(watcher), "aaa000000003")

    def test_incremental_reload_mixes_new_and_updated_rows(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.store.save()
        watcher = self.open_store()
        self.assertEqual(self.latest(watcher), "zzz000000001")
        self.add(self.store, "mmm000000002", self.sam)
        self.add(self.store, "aaa000000003", self.sam)
        self.store.save()
        self.store.resolve_priority(
            self.sam, "zzz000000001", "reject", "SYN review of an older proposal"
        )
        self.assertEqual(self.latest(watcher), "aaa000000003")

    def test_interleaved_writer_commit_does_not_displace_the_later_local_proposal(self) -> None:
        other = self.open_store()
        self.add(self.store, "mmm000000002", self.sam)
        self.add(other, "zzz000000001", self.sam)
        other.save()
        self.store.save()
        self.assertEqual(self.latest(self.store), "mmm000000002")
        self.assertEqual(self.latest(other), "mmm000000002")
        self.assertEqual(self.latest(self.open_store()), "mmm000000002")

    def test_fresh_database_has_the_ordinal_column_and_orders_by_it(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.add(self.store, "aaa000000002", self.sam)
        self.store.save()
        rows = self.store.db.execute(
            "SELECT id, created_ord FROM recommendations ORDER BY created_ord"
        ).fetchall()
        ords = [int(r[1]) for r in rows]
        self.assertEqual(ords, sorted(set(ords)))
        self.assertEqual(rows[-1][0], "aaa000000002")
        self.assertNotIn(0, ords)

    def test_legacy_rows_are_backfilled_by_created_then_seq_then_id_and_recorded(self) -> None:
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, self.body("mmm000000002", SECOND)),
                ("aaa000000003", 9, user, self.body("aaa000000003", EARLIER)),
            ],
        )
        reopened = self.open_store()
        ords = dict(reopened.db.execute("SELECT id, created_ord FROM recommendations").fetchall())
        self.assertEqual(
            sorted(ords, key=lambda k: ords[k]), ["aaa000000003", "zzz000000001", "mmm000000002"]
        )
        info = json.loads(
            reopened.db.execute("SELECT value FROM meta WHERE key='rec_order_legacy'").fetchone()[0]
        )
        self.assertEqual((info["rows"], info["same_second_groups"]), (3, 1))
        self.assertEqual(self.latest(reopened), "mmm000000002")
        self.assertEqual(self.latest(self.open_store()), "mmm000000002")
        self.add(reopened, "bbb000000004", self.sam, created=EARLIER)
        reopened.save()
        self.assertEqual(self.latest(reopened), "bbb000000004")
        self.assertEqual(self.latest(self.open_store()), "bbb000000004")

    def test_running_reader_picks_up_a_backfill_done_by_another_process(self) -> None:
        reader = self.open_store()
        seq = int(reader.db.execute("SELECT value FROM meta WHERE key='seq'").fetchone()[0]) + 1
        reader.db.execute(
            "INSERT INTO recommendations (id, rowversion, seq, user, body, created_ord) "
            "VALUES (?,1,?,?,?,0)",
            ("aaa000000009", seq, self.sam["email"], self.body("aaa000000009", SECOND)),
        )
        reader.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(seq),))
        self.open_store()
        self.assertEqual(self.latest(reader), "aaa000000009")


@unittest.skipUnless(os.environ.get("ZF_RESIDENT_MSSQL") == "1", "opt-in owned loopback SQL Server")
class MssqlPriorityOrder(SqlitePriorityOrder):
    def setUp(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        self.database = "zf_priority1292_" + uuid.uuid4().hex
        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{self.database}]")

        def drop_owned_database() -> None:
            admin.execute(
                f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
            )
            admin.execute(f"DROP DATABASE [{self.database}]")

        self.addCleanup(drop_owned_database)
        os.environ["ZF_SQL_DATABASE"] = self.database
        super().setUp()

    def open_store(self) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store

    def legacy_ddl(self) -> str:
        from zava_forward.core.mssqlstore import TABLES

        ddl = TABLES["recommendations"]
        assert "created_ord" in ddl
        return ddl.replace(", created_ord BIGINT NOT NULL DEFAULT 0", "")
