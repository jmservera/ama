"""Newest-created order of priority recommendations across SQL reloads (#1292), synthetic data."""

import copy
import json
import os
import sys
import tempfile
import threading
import time
import types
import unittest
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from sqlguard import require_task_owned_loopback
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

SECOND = "2026-11-08T10:00:00"
EARLIER = "2026-11-08T09:00:00"


class PriorityFixture(unittest.TestCase):
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


class JsonPriorityOrder(PriorityFixture):
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


class SqliteFixture(PriorityFixture):
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

    def old_writer_insert(self, store: Any, rid: str, created: str = SECOND) -> None:
        """A pre-fix binary: the row gets the column default 0 and the shared seq moves on."""
        seq = int(store.db.execute("SELECT value FROM meta WHERE key='seq'").fetchone()[0]) + 1
        store.db.execute(
            "INSERT INTO recommendations (id, rowversion, seq, user, body, created_ord) "
            "VALUES (?,1,?,?,?,0)",
            (rid, seq, self.sam["email"], self.body(rid, created)),
        )
        store.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(seq),))

    def ordinals(self, store: Any) -> list[str]:
        rows = store.db.execute("SELECT id, created_ord FROM recommendations").fetchall()
        return [r[0] for r in sorted(rows, key=lambda r: int(r[1]))]

    def batches(self, store: Any) -> list[dict[str, Any]]:
        row = store.db.execute("SELECT value FROM meta WHERE key='rec_order_backfills'").fetchone()
        return list(json.loads(row[0])) if row else []


class SqlitePriorityOrder(SqliteFixture, JsonPriorityOrder):
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

    def test_old_writer_insert_after_startup_is_repaired_before_a_later_new_write(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.store.save()
        running = self.open_store()
        self.old_writer_insert(running, "mmm000000002")
        self.assertEqual(self.latest(running), "mmm000000002")
        self.add(running, "aaa000000003", self.sam)
        running.save()
        restarted = self.open_store()
        self.assertEqual(self.latest(restarted), "aaa000000003")
        order = self.ordinals(restarted)
        self.assertLess(order.index("zzz000000001"), order.index("mmm000000002"))
        self.assertLess(order.index("mmm000000002"), order.index("aaa000000003"))
        self.assertEqual(len(self.batches(restarted)), 1)

    def test_old_writer_insert_between_two_new_writes_keeps_commit_order(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.store.save()
        self.old_writer_insert(self.store, "mmm000000002")
        self.add(self.store, "aaa000000003", self.sam)
        self.store.save()
        for store in (self.store, self.open_store()):
            self.assertEqual(self.latest(store), "aaa000000003")
        order = self.ordinals(self.store)
        self.assertEqual(order[-2:], ["mmm000000002", "aaa000000003"])

    def test_zero_ordinal_read_fails_closed_when_repair_is_blocked(self) -> None:
        self.add(self.store, "zzz000000001", self.sam)
        self.store.save()
        running = self.open_store()
        self.old_writer_insert(running, "mmm000000002")
        with patch.object(
            running, "_backfill_zero_ordinals", side_effect=RuntimeError("repair blocked")
        ):
            with self.assertRaises(RuntimeError):
                self.latest(running)
        self.assertEqual(self.latest(running), "mmm000000002")

    def test_audited_same_second_creations_keep_order_after_edit_of_the_older(self) -> None:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.resolve_priority(self.sam, first, "accept", "SYN review of the older proposal")
        rows = self.store.db.execute("SELECT id, seq, user, body FROM recommendations").fetchall()
        same_second = []
        for rid, seq, user, body in rows:
            rec = json.loads(body)
            rec["created"] = SECOND
            same_second.append((rid, seq, user, json.dumps(rec)))
        self.assertGreater(
            max(r[1] for r in same_second if r[0] == first),
            max(r[1] for r in same_second if r[0] == second),
        )
        self.make_legacy(self.store, same_second)
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), second)
        self.assertEqual(self.latest(self.open_store()), second)
        batch = self.batches(reopened)[0]
        self.assertEqual(batch["ambiguous_total"], 0)
        self.assertEqual(batch["audited"], len(same_second))

    def test_ambiguous_group_is_recorded_with_ids_when_audit_evidence_is_absent(self) -> None:
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, self.body("mmm000000002", SECOND)),
                ("aaa000000003", 4, user, self.body("aaa000000003", EARLIER)),
            ],
        )
        batch = self.batches(self.open_store())[0]
        self.assertEqual(batch["ambiguous_total"], 2)
        self.assertEqual(sorted(batch["ambiguous_ids"]), ["mmm000000002", "zzz000000001"])
        self.assertEqual(batch["audited"], 0)

    def test_rollback_batch_is_recorded_without_erasing_earlier_metadata(self) -> None:
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, self.body("mmm000000002", SECOND)),
            ],
        )
        reopened = self.open_store()
        legacy = reopened.db.execute(
            "SELECT value FROM meta WHERE key='rec_order_legacy'"
        ).fetchone()[0]
        first = self.batches(reopened)
        self.assertEqual(len(first), 1)
        self.old_writer_insert(reopened, "bbb000000004")
        self.old_writer_insert(reopened, "aaa000000005")
        after = self.open_store()
        self.assertEqual(
            after.db.execute("SELECT value FROM meta WHERE key='rec_order_legacy'").fetchone()[0],
            legacy,
        )
        batches = self.batches(after)
        self.assertEqual(len(batches), 2)
        self.assertEqual(batches[0], first[0])
        self.assertEqual(batches[1]["rows"], 2)
        self.assertEqual(batches[1]["ambiguous_total"], 2)
        self.assertEqual(self.latest(after), "aaa000000005")


class SqliteLegacyEdges(SqliteFixture):
    """SQLite only: trigger removal and a large table; SQL Server equivalents are pending."""

    def test_broken_audit_chain_is_not_trusted(self) -> None:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.resolve_priority(self.sam, first, "accept", "SYN review of the older proposal")
        rows = []
        for rid, seq, user, body in self.store.db.execute(
            "SELECT id, seq, user, body FROM recommendations"
        ).fetchall():
            rows.append((rid, seq, user, json.dumps(dict(json.loads(body), created=SECOND))))
        self.make_legacy(self.store, rows)
        self.store.db.execute("DROP TRIGGER audit_no_update")
        self.store.db.execute("UPDATE audit SET who='tampered' WHERE seq=1")
        batch = self.batches(self.open_store())[0]
        self.assertFalse(batch["audit_chain"])
        self.assertEqual(batch["audited"], 0)
        self.assertGreater(batch["ambiguous_total"], 0)
        self.assertIn(second, batch["ambiguous_ids"])

    def test_large_legacy_backfill_is_linear_and_survives_concurrent_openers(self) -> None:
        size = 30000
        user = self.sam["email"]
        self.store.db.execute("DROP TABLE recommendations")
        self.store.db.execute(self.legacy_ddl())
        base = json.loads(self.body("x", SECOND))
        rows = []
        for n in range(size):
            rid = f"{n:012x}"
            day, rest = divmod(n, 86400)
            stamp = (
                f"2026-01-{1 + day:02d}T{rest // 3600:02d}:{rest // 60 % 60:02d}:{rest % 60:02d}"
            )
            rows.append((rid, 2 + n, user, json.dumps(dict(base, id=rid, created=stamp))))
        self.store.db.execute("BEGIN")
        self.store.db.executemany(
            "INSERT INTO recommendations (id, rowversion, seq, user, body) VALUES (?,1,?,?,?)",
            rows,
        )
        self.store.db.execute("COMMIT")
        errors: list[BaseException] = []

        def opener() -> None:
            try:
                self.open_store()
            except BaseException as error:
                errors.append(error)

        started = time.monotonic()
        threads = [threading.Thread(target=opener) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        elapsed = time.monotonic() - started
        self.assertEqual(errors, [])
        self.assertLess(elapsed, 20.0, f"backfill took {elapsed:.1f}s while holding the write lock")
        final = self.open_store()
        self.assertEqual(len(self.batches(final)), 1)
        self.assertEqual(self.batches(final)[0]["rows"], size)
        ords = [int(r[0]) for r in final.db.execute("SELECT created_ord FROM recommendations")]
        self.assertEqual(sorted(ords), list(range(1, size + 1)))


class LoopbackGuard(unittest.TestCase):
    def refuse(self, case_type: type, **env: str) -> None:
        constructed: list[str] = []

        def forbidden(*_args: Any, **_kwargs: Any) -> Any:
            constructed.append("connection")
            raise AssertionError("connection attempted before the loopback check")

        fake = types.SimpleNamespace(_Conn=forbidden, connection_string=lambda *_a, **_k: "x")
        case = case_type("setUp")
        with (
            patch.dict(os.environ, env),
            patch.dict(sys.modules, {"zava_forward.core.mssqlstore": fake}),
        ):
            with self.assertRaises(RuntimeError):
                case.setUp()
        self.assertEqual(constructed, [])

    def test_task_owned_sql_fixtures_refuse_non_loopback_before_any_connection(self) -> None:
        import test_resident_decisions

        for case_type in (MssqlPriorityOrder, test_resident_decisions.MssqlResidentControls):
            for host in ("example.database.windows.net", "10.1.2.3", ""):
                self.refuse(case_type, ZF_SQL_SERVER=host, ZF_SQL_AUTH="password")
            self.refuse(case_type, ZF_SQL_SERVER="127.0.0.1", ZF_SQL_AUTH="msi")

    def test_loopback_with_password_auth_is_accepted(self) -> None:
        for host in ("127.0.0.1", "localhost", "[::1]"):
            require_task_owned_loopback({"ZF_SQL_SERVER": host, "ZF_SQL_AUTH": "password"})


@unittest.skipUnless(os.environ.get("ZF_RESIDENT_MSSQL") == "1", "opt-in owned loopback SQL Server")
class MssqlPriorityOrder(SqlitePriorityOrder):
    def setUp(self) -> None:
        require_task_owned_loopback(os.environ)
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
