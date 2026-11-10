"""Newest-created order of priority recommendations across SQL reloads (#1292), synthetic data."""

import copy
import hashlib
import json
import os
import sqlite3
import stat
import sys
import tempfile
import threading
import time
import types
import unittest
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from sqlguard import require_task_owned_loopback, write_manifest
from zava_forward.core import continuity, ledger
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

    def native_ddl(self) -> str:
        """The current table with the ordinal column, for fixtures that rebuild it by hand."""
        return (
            "CREATE TABLE recommendations (id TEXT PRIMARY KEY, "
            "rowversion INTEGER NOT NULL DEFAULT 1, seq INTEGER NOT NULL, user TEXT NOT NULL, "
            "body TEXT NOT NULL, created_ord BIGINT NOT NULL DEFAULT 0)"
        )

    def lift_audit_guard(self, store: Any, trigger: str) -> None:
        """Privileged fixture step: remove the append-only guard so the audit can be rewritten."""
        store.db.execute(f"DROP TRIGGER {trigger}")

    def make_legacy(self, store: Any, rows: list[tuple[Any, ...]]) -> None:
        """Replace the table by the pre-fix schema holding (id, seq, user, body[, rowversion])."""
        store.db.execute("DROP TABLE recommendations")
        store.db.execute(self.legacy_ddl())
        for rid, seq, user, body, *version in rows:
            store.db.execute(
                "INSERT INTO recommendations (id, rowversion, seq, user, body) VALUES (?,?,?,?,?)",
                (rid, version[0] if version else 1, seq, user, body),
            )

    def body(self, rid: str, created: str) -> str:
        return json.dumps(dict(self.template, id=rid, created=created))

    def old_writer_insert(
        self,
        store: Any,
        rid: str,
        created: str = SECOND,
        user: dict[str, Any] | None = None,
    ) -> None:
        """A pre-fix binary: one atomic commit of a row with the column default 0 and a seq bump."""
        owner = (user or self.sam)["email"]
        store.db.execute("BEGIN IMMEDIATE")
        seq = int(store.db.execute("SELECT value FROM meta WHERE key='seq'").fetchone()[0]) + 1
        store.db.execute(
            "INSERT INTO recommendations (id, rowversion, seq, user, body, created_ord) "
            "VALUES (?,1,?,?,?,0)",
            (rid, seq, owner, json.dumps(dict(self.template, id=rid, user=owner, created=created))),
        )
        store.db.execute("UPDATE meta SET value=? WHERE key='seq'", (str(seq),))
        store.db.execute("COMMIT")

    def ordinals(self, store: Any) -> list[str]:
        rows = store.db.execute("SELECT id, created_ord FROM recommendations").fetchall()
        return [r[0] for r in sorted(rows, key=lambda r: int(r[1]))]

    def meta(self, store: Any, key: str) -> str | None:
        row = store.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return None if row is None else str(row[0])

    def batches(self, store: Any) -> list[dict[str, Any]]:
        count = int(self.meta(store, "rec_order_batches") or 0)
        return [
            json.loads(str(self.meta(store, f"rec_order_batch:{n}"))) for n in range(1, count + 1)
        ]

    def unresolved(self, store: Any) -> list[str]:
        rows = store.db.execute("SELECT key FROM meta WHERE key LIKE 'rec_unres:%'").fetchall()
        return sorted(str(r[0]).split(":", 1)[1] for r in rows)


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
        rows = self.store.db.execute(
            "SELECT id, seq, user, body, rowversion FROM recommendations"
        ).fetchall()
        same_second = []
        for rid, seq, user, body, version in rows:
            rec = json.loads(body)
            rec["created"] = SECOND
            same_second.append((rid, seq, user, json.dumps(rec), version))
        self.assertGreater(
            max(r[1] for r in same_second if r[0] == first),
            max(r[1] for r in same_second if r[0] == second),
        )
        self.make_legacy(self.store, same_second)
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), second)
        self.assertEqual(self.latest(self.open_store()), second)
        batch = self.batches(reopened)[0]
        self.assertEqual(batch["audited"], len(same_second))
        self.assertEqual(batch["ambiguous_ids"], [second])
        self.assertFalse(reopened.latest_priority(self.sam)["order_confirmed"])

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
        self.assertEqual(batch["ambiguous_total"], 1)
        self.assertEqual(batch["ambiguous_ids"], ["mmm000000002"])
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
        self.assertEqual(batches[1]["ambiguous_total"], 1)
        self.assertEqual(self.latest(after), "aaa000000005")
        self.assertEqual(after.latest_priority(self.sam)["order_confirmed"], False)

    def test_provable_creation_order_survives_a_backward_clock_step(self) -> None:
        clock = {"now": "2026-11-08T10:00:00"}

        class Clock(datetime):
            @classmethod
            def now(cls, tz: Any = None) -> Any:
                return cls.fromisoformat(clock["now"])

        with patch("zava_forward.core.store.datetime", Clock):
            first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
            clock["now"] = "2026-11-08T09:59:59"
            second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        rows = self.store.db.execute(
            "SELECT id, seq, user, body, rowversion FROM recommendations"
        ).fetchall()
        self.make_legacy(self.store, [tuple(r) for r in rows])
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), second)
        view = reopened.latest_priority(self.sam)
        self.assertNotIn("order_confirmed", view)
        order = self.ordinals(reopened)
        self.assertLess(order.index(first), order.index(second))
        batch = self.batches(reopened)[0]
        self.assertEqual(batch["ambiguous_total"], 0)
        self.assertGreaterEqual(batch["timestamp_inversions"], 1)

    def test_unresolved_newest_is_marked_in_the_view_and_other_employees_are_not(self) -> None:
        sam, pam = self.sam["email"], self.pam["email"]
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, sam, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 9, sam, self.body("mmm000000002", SECOND), 2),
                (
                    "ppp000000003",
                    4,
                    pam,
                    json.dumps(dict(self.template, id="ppp000000003", created=SECOND, user=pam)),
                ),
                (
                    "ttt000000004",
                    5,
                    sam,
                    json.dumps(
                        dict(self.template, id="ttt000000004", created=SECOND, kind="ai_task")
                    ),
                ),
            ],
        )
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), ["mmm000000002"])
        view = reopened.latest_priority(self.sam)
        self.assertEqual((view["order_confirmed"], view["actionable"]), (False, False))
        self.assertIn("data owner", view["order_note"])
        other = reopened.latest_priority(self.pam)
        self.assertNotIn("order_confirmed", other)
        self.assertEqual(other["id"], "ppp000000003")

    def test_failed_publication_is_neither_persisted_nor_flushed_later(self) -> None:
        store, other = self.store, self.open_store()
        before = len(list(store.audit_entries()))
        with patch.object(continuity, "validate_sql", side_effect=RuntimeError("injected")):
            with self.assertRaises(RuntimeError):
                store.ai_priority(self.sam, mode="workflow-only")
        self.assertEqual(len(list(store.audit_entries())), before + 1)
        newer = other.ai_priority(self.sam, mode="workflow-only")["id"]
        store.save()
        self.assertEqual(self.latest(store), newer)
        self.assertEqual(self.latest(self.open_store()), newer)
        ends = [
            e
            for e in store.audit_entries()
            if e["detail"].startswith("priority_recommendation ")
            and not e["detail"].startswith("priority_recommendation n=")
        ]
        self.assertEqual(len(ends), 2)
        count = store.db.execute("SELECT COUNT(*) FROM recommendations").fetchone()[0]
        self.assertEqual(int(count), 2)


class Barrier:
    """Wraps a store connection and runs one action after the k-th statement once armed."""

    def __init__(self, real: Any) -> None:
        self.real = real
        self.count = 0
        self.limit = 0
        self.action: Any = None

    def arm(self, limit: int, action: Any) -> None:
        self.count, self.limit, self.action = 0, limit, action

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        result = self.real.execute(*args, **kwargs)
        if self.action is not None:
            self.count += 1
            if self.count == self.limit:
                action, self.action = self.action, None
                action()
        return result

    def __getattr__(self, name: str) -> Any:
        return getattr(self.real, name)


class SqliteLegacyEdges(SqliteFixture):
    """SQLite only: trigger removal and a large table; SQL Server equivalents are pending."""

    def fresh(self, name: str) -> Any:
        store = SqlStore(str(self.path), str(self.path.with_name(name + ".sqlite")))
        self.addCleanup(store.db.close)
        return store

    def test_old_writer_commit_between_any_two_reload_statements_is_never_served(self) -> None:
        for statement in range(1, 14):
            for victim in (self.sam, self.pam):
                name = f"b{statement}{victim['email'][:3]}"
                with self.subTest(statement=statement, victim=victim["email"]):
                    store, writer = self.fresh(name), self.fresh(name)
                    self.add(store, "aaa000000001", self.sam)
                    self.add(store, "bbb000000002", self.pam)
                    store.save()
                    watcher = self.fresh(name)
                    self.assertEqual(self.latest(watcher), "aaa000000001")
                    self.add(store, "ccc000000003", self.sam)
                    store.save()
                    barrier = Barrier(watcher.db)
                    watcher.db = barrier
                    fired: list[bool] = []

                    def inject(
                        writer: Any = writer,
                        victim: dict[str, Any] = victim,
                        fired: list[bool] = fired,
                    ) -> None:
                        fired.append(True)
                        self.old_writer_insert(writer, "mmm000000009", user=victim)

                    barrier.arm(statement, inject)
                    self.assertIn(self.latest(watcher), ("ccc000000003", "mmm000000009"))
                    if not fired:
                        inject()
                    barrier.action = None
                    mine, theirs = (
                        ("mmm000000009", "bbb000000002")
                        if victim is self.sam
                        else ("ccc000000003", "mmm000000009")
                    )
                    self.assertEqual(self.latest(watcher), mine)
                    self.assertEqual(self.latest(watcher, self.pam), theirs)
                    self.assertNotIn(0, watcher._rec_ord.values())
                    self.add(watcher, "ddd000000004", self.sam)
                    watcher.save()
                    for reader in (watcher, self.fresh(name)):
                        self.assertEqual(self.latest(reader), "ddd000000004")
                        self.assertEqual(self.latest(reader, self.pam), theirs)
                    order = self.ordinals(watcher)
                    self.assertLess(order.index("mmm000000009"), order.index("ddd000000004"))

    def test_rolled_back_queue_transaction_does_not_publish_repaired_cache(self) -> None:
        self.add(self.store, "aaa000000001", self.sam)
        self.store.save()
        watcher = self.open_store()
        self.assertEqual(self.latest(watcher), "aaa000000001")
        self.old_writer_insert(self.store, "mmm000000002")
        with patch.object(
            watcher, "_refresh_queue_membership", side_effect=RuntimeError("injected")
        ):
            with self.assertRaises(RuntimeError):
                watcher._queue_candidates("new")
        self.old_writer_insert(self.store, "ccc000000003")
        self.assertEqual(self.latest(watcher), "ccc000000003")
        self.assertEqual(self.latest(self.open_store()), "ccc000000003")
        self.assertNotIn(0, watcher._rec_ord.values())

    def test_creation_event_that_contradicts_commit_order_is_not_proof(self) -> None:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.ai_priority(self.sam, mode="workflow-only")
        rows = []
        for rid, seq, user, body, version in self.store.db.execute(
            "SELECT id, seq, user, body, rowversion FROM recommendations"
        ).fetchall():
            rec = dict(json.loads(body), created=SECOND)
            late = seq + 50 if rid == first else seq
            rows.append((rid, late, user, json.dumps(rec), version))
        self.make_legacy(self.store, rows)
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [first])
        self.assertFalse(reopened.latest_priority(self.sam)["actionable"])

    def rechain(self, store: Any) -> None:
        """A privileged rewrite: reverse the creation events, then rechain consistently."""
        entries = store.db.execute(
            "SELECT who, action, case_id, detail, at FROM audit ORDER BY seq"
        ).fetchall()
        ends = [i for i, e in enumerate(entries) if e[1] == "ai_run_end"]
        values = [entries[i] for i in ends][::-1]
        for index, value in zip(ends, values, strict=True):
            entries[index] = value
        self.lift_audit_guard(store, "audit_no_delete")
        store.db.execute("DELETE FROM audit")
        head, count = ledger.GENESIS, 0
        for who, action, case_id, detail, at in entries:
            made = ledger.make_entry(who, action, case_id, detail, head, at)
            store.db.execute(
                "INSERT INTO audit (at, who, action, case_id, detail, prev, hash) "
                "VALUES (?,?,?,?,?,?,?)",
                (made["at"], who, action, case_id, detail, head, made["hash"]),
            )
            head, count = made["hash"], count + 1
        store.db.execute("UPDATE audit_head SET count=?, hash=? WHERE id=1", (count, head))

    def test_self_consistent_rechain_conflicting_with_a_retained_digest_is_not_trusted(
        self,
    ) -> None:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.write_digest()
        self.rechain(self.store)
        rows = [
            (rid, seq, user, json.dumps(dict(json.loads(body), created=SECOND)), version)
            for rid, seq, user, body, version in self.store.db.execute(
                "SELECT id, seq, user, body, rowversion FROM recommendations"
            ).fetchall()
        ]
        self.make_legacy(self.store, rows)
        reopened = self.open_store()
        batch = self.batches(reopened)[0]
        self.assertFalse(batch["audit_chain"])
        self.assertIn("digest", batch["audit_reason"])
        self.assertEqual(batch["audited"], 0)
        self.assertEqual(self.unresolved(reopened), [self.latest(reopened)])
        self.assertIn(self.latest(reopened), {first, second})

    def test_database_backfilled_by_the_earlier_candidate_is_reviewed_not_rewritten(self) -> None:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.resolve_priority(self.sam, first, "accept", "SYN review of the older proposal")
        rows = [
            (rid, seq, user, json.dumps(dict(json.loads(body), created=SECOND)), version)
            for rid, seq, user, body, version in self.store.db.execute(
                "SELECT id, seq, user, body, rowversion FROM recommendations"
            ).fetchall()
        ]
        self.make_legacy(self.store, rows)
        db = self.store.db
        db.execute("DROP TABLE recommendations")
        db.execute(self.native_ddl())
        db.execute("CREATE INDEX ix_recs_created_ord ON recommendations (created_ord)")
        heuristic = sorted(rows, key=lambda r: (r[3] and json.loads(r[3])["created"], r[1], r[0]))
        for ordinal, (rid, seq, user, body, version) in enumerate(heuristic, 1):
            db.execute(
                "INSERT INTO recommendations (id, rowversion, seq, user, body, created_ord) "
                "VALUES (?,?,?,?,?,?)",
                (rid, version, seq, user, body, ordinal),
            )
        legacy = json.dumps(dict(rows=len(rows), same_second_groups=1, order="created,seq,id"))
        db.execute("INSERT INTO meta (key, value) VALUES ('rec_order_legacy', ?)", (legacy,))
        db.execute("DELETE FROM meta WHERE key='rec_order_review'")
        before = self.ordinals(self.store)
        self.assertLess(before.index(second), before.index(first))
        reopened = self.open_store()
        self.assertEqual(self.ordinals(reopened), before)
        self.assertEqual(self.meta(reopened, "rec_order_legacy"), legacy)
        self.assertEqual(self.batches(reopened)[0]["source"], "review")
        self.assertEqual(self.unresolved(reopened), [first])
        self.assertFalse(reopened.latest_priority(self.sam)["order_confirmed"])
        self.assertEqual(len(self.batches(self.open_store())), 1)

    def test_repeated_singleton_repairs_do_not_rescan_the_audit_or_rewrite_history(self) -> None:
        pad = [("system", "synthetic_note", "-", f"SYN {n}", SECOND) for n in range(6000)]
        self.store.db.execute("BEGIN IMMEDIATE")
        self.store._append_audit(pad)
        self.store.db.execute("COMMIT")
        total = len(list(self.store.audit_entries()))
        verified: list[int] = []
        real = ledger.verify_entries

        def counting(entries: Any, *args: Any, **kwargs: Any) -> Any:
            verified.append(len(list(entries)))
            return real(entries, *args, **kwargs)

        running = self.open_store()
        with patch.object(ledger, "verify_entries", side_effect=counting):
            for n in range(5):
                self.old_writer_insert(running, f"r{n:011d}")
                running._audit_immediate(
                    ("system", "synthetic_note", "-", f"SYN extra {n}", SECOND)
                )
                self.assertEqual(self.latest(running), f"r{n:011d}")
        self.assertLessEqual(sum(verified), total + 50, verified)
        self.assertEqual(len(self.batches(running)), 5)
        self.assertIsNone(self.meta(running, "rec_order_backfills"))

    def test_broken_audit_chain_is_not_trusted(self) -> None:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.ai_priority(self.sam, mode="workflow-only")
        self.store.resolve_priority(self.sam, first, "accept", "SYN review of the older proposal")
        rows = []
        for rid, seq, user, body, version in self.store.db.execute(
            "SELECT id, seq, user, body, rowversion FROM recommendations"
        ).fetchall():
            rows.append(
                (rid, seq, user, json.dumps(dict(json.loads(body), created=SECOND)), version)
            )
        self.make_legacy(self.store, rows)
        self.lift_audit_guard(self.store, "audit_no_update")
        self.store.db.execute("UPDATE audit SET who='tampered' WHERE seq=1")
        batch = self.batches(self.open_store())[0]
        self.assertFalse(batch["audit_chain"])
        self.assertEqual(batch["audited"], 0)
        self.assertGreater(batch["ambiguous_total"], 0)
        self.assertEqual(batch["ambiguous_ids"], [first])
        view = self.store.latest_priority(self.sam)
        reopened = self.open_store()
        self.assertEqual(reopened.latest_priority(self.sam)["order_confirmed"], False)
        self.assertEqual(view["id"], reopened.latest_priority(self.sam)["id"])

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
        self.store.db.execute("BEGIN IMMEDIATE")
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
        ords = [
            int(r[0])
            for r in final.db.execute("SELECT created_ord FROM recommendations").fetchall()
        ]
        self.assertEqual(sorted(ords), list(range(1, size + 1)))


class FlakyDb:
    """Delegates to a real connection; fails the next BEGIN once armed, recording statements."""

    def __init__(self, db: Any) -> None:
        self.real, self.armed = db, False
        self.seen: list[str] = []

    def execute(self, sql: str, *args: Any) -> Any:
        self.seen.append(sql.split()[0].upper())
        if self.armed and sql.startswith("BEGIN"):
            self.armed = False
            raise sqlite3.OperationalError("injected: cannot start a transaction")
        return self.real.execute(sql, *args)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.real, name)


class SqliteC3Corrections(SqliteFixture):
    """Correction C3 scenarios; SQLite only, SQL Server equivalents are pending."""

    def two_audited(self, created: tuple[str, str] = (SECOND, SECOND)) -> tuple[str, str]:
        first = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.rows = [
            (rid, seq, user, json.dumps(dict(json.loads(body), created=stamp)), version)
            for (rid, seq, user, body, version), stamp in zip(
                self.store.db.execute(
                    "SELECT id, seq, user, body, rowversion FROM recommendations "
                    "WHERE id <> ? ORDER BY seq",
                    (self.template["id"],),
                ).fetchall(),
                created,
                strict=True,
            )
        ]
        return first, second

    def flagged_latest(self, store: Any) -> bool:
        view = store.latest_priority(self.sam)
        return bool(view.get("order_confirmed") is False and not view["actionable"])

    def test_unaudited_row_beside_audited_rows_leaves_the_newest_unconfirmed(self) -> None:
        first, second = self.two_audited()
        extra = ("uuu000000009", 99, self.sam["email"], self.body("uuu000000009", EARLIER))
        self.make_legacy(self.store, [*self.rows, extra])
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [self.latest(reopened)])
        self.assertTrue(self.flagged_latest(reopened))
        self.assertIn(self.latest(reopened), {first, second})

    def test_unaudited_rows_with_different_timestamps_are_not_confirmed_newest(self) -> None:
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                ("aaa000000001", 2, user, self.body("aaa000000001", EARLIER)),
                ("zzz000000002", 3, user, self.body("zzz000000002", SECOND)),
            ],
        )
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), "zzz000000002")
        self.assertEqual(self.unresolved(reopened), ["zzz000000002"])
        self.assertTrue(self.flagged_latest(reopened))

    def test_audited_clock_step_with_agreeing_insert_order_stays_confirmed(self) -> None:
        self.two_audited((SECOND, EARLIER))
        self.make_legacy(self.store, self.rows)
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [])
        self.assertNotIn("order_confirmed", reopened.latest_priority(self.sam))

    def test_tied_transaction_sequence_is_not_proof_of_joint_commit(self) -> None:
        self.two_audited()
        tied = [(rid, 50, user, body, version) for rid, _, user, body, version in self.rows]
        self.make_legacy(self.store, tied)
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [self.latest(reopened)])

    def test_orphan_creation_event_for_a_later_inserted_row_is_not_proof(self) -> None:
        self.two_audited()
        self.store._audit_immediate(
            ("system", "ai_run_end", "-", "priority_recommendation orph00000009 n=5", SECOND)
        )
        top = max(seq for _, seq, *_ in self.rows)
        orphan = ("orph00000009", top, self.sam["email"], self.body("orph00000009", SECOND))
        self.make_legacy(self.store, [*self.rows, orphan])
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), "orph00000009")
        self.assertEqual(self.unresolved(reopened), ["orph00000009"])

    def c1_database(self) -> None:
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, self.body("mmm000000002", SECOND)),
            ],
        )
        self.open_store()
        self.store.db.execute("DELETE FROM meta WHERE key='rec_order_review'")
        self.store.db.execute("DELETE FROM meta WHERE key LIKE 'rec_unres:%'")
        self.store.db.execute("DELETE FROM meta WHERE key='rec_unres_index'")

    def test_prior_batch_database_is_reviewed_once_even_with_batch_metadata_and_a_zero_row(
        self,
    ) -> None:
        self.c1_database()
        before = self.ordinals(self.store)
        self.assertGreaterEqual(len(self.batches(self.store)), 1)
        self.old_writer_insert(self.store, "ccc000000003")
        reopened = self.open_store()
        self.assertEqual(self.ordinals(reopened)[:2], before)
        self.assertEqual(self.latest(reopened), "ccc000000003")
        self.assertEqual(self.unresolved(reopened), ["ccc000000003", "mmm000000002"])
        self.assertEqual([b["source"] for b in self.batches(reopened)].count("review"), 1)
        sources = len(self.batches(self.open_store()))
        self.assertEqual(sources, len(self.batches(reopened)))

    def test_prior_candidate_audit_inversion_across_timestamps_is_reviewed(self) -> None:
        first, second = self.two_audited((SECOND, EARLIER))
        self.make_legacy(self.store, self.rows)
        db = self.store.db
        db.execute("DROP TABLE recommendations")
        db.execute(self.native_ddl())
        heuristic = sorted(self.rows, key=lambda r: json.loads(r[3])["created"])
        for ordinal, (rid, seq, user, body, version) in enumerate(heuristic, 1):
            db.execute(
                "INSERT INTO recommendations VALUES (?,?,?,?,?,?)",
                (rid, version, seq, user, body, ordinal),
            )
        legacy = json.dumps(dict(rows=2, same_second_groups=0, order="created,seq,id"))
        db.execute("INSERT INTO meta (key, value) VALUES ('rec_order_legacy', ?)", (legacy,))
        db.execute("DELETE FROM meta WHERE key='rec_order_review'")
        before = self.ordinals(self.store)
        self.assertEqual(before, [second, first])
        reopened = self.open_store()
        self.assertEqual(self.ordinals(reopened), before)
        self.assertEqual(self.unresolved(reopened), [first])

    def unresolved_latest(self) -> Any:
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, self.body("mmm000000002", SECOND)),
            ],
        )
        return self.open_store()

    def test_server_refuses_accept_and_edit_of_an_unresolved_record_but_allows_reject(self) -> None:
        reopened = self.unresolved_latest()
        view = reopened.latest_priority(self.sam)
        self.assertEqual(view["id"], "mmm000000002")
        self.assertEqual(
            (view["order_confirmed"], view["actionable"], view["relied_on"]), (False, False, False)
        )
        self.assertIn("data owner", view["order_note"])
        items = [dict(case_id=i["case_id"], reason="SYN") for i in view["items"]]
        with self.assertRaises(PermissionError):
            reopened.resolve_priority(self.sam, "mmm000000002", "accept")
        with self.assertRaises(PermissionError):
            reopened.resolve_priority(self.sam, "mmm000000002", "edit", "SYN why", items)
        self.assertEqual(reopened.latest_priority(self.sam)["status"], "Proposed")
        done = reopened.resolve_priority(self.sam, "mmm000000002", "reject", "SYN not wanted")
        self.assertEqual(done["status"], "Rejected")
        self.assertFalse(done["relied_on"])

    def test_already_accepted_unresolved_record_is_not_relied_on(self) -> None:
        user = self.sam["email"]
        accepted = json.dumps(
            dict(self.template, id="mmm000000002", created=SECOND, status="Accepted")
        )
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, accepted),
            ],
        )
        view = self.open_store().latest_priority(self.sam)
        self.assertEqual(view["status"], "Accepted")
        self.assertFalse(view["relied_on"])
        self.assertFalse(view["order_confirmed"])

    def test_priority_panel_renders_the_order_explanation_accessibly(self) -> None:
        web = Path(__file__).parents[2] / "api/src/zava_forward/api/web/app.js"
        text = web.read_text(encoding="utf-8")
        at = text.index("order_note")
        self.assertIn('role: "status"', text[at - 120 : at + 120])

    def test_new_conflicting_digest_with_the_same_head_is_not_served_from_the_cache(self) -> None:
        self.two_audited()
        self.make_legacy(self.store, self.rows)
        store = self.open_store()
        self.assertTrue(store._audit_evidence()["ok"])
        count = int(store.db.execute("SELECT count FROM audit_head WHERE id=1").fetchone()[0])
        ledger.write_digest(store.digest_dir, ledger.make_digest(count, "f" * 64))
        evidence = store._audit_evidence()
        self.assertFalse(evidence["ok"])
        self.assertIn("digest", evidence["reason"])

    def test_appending_to_a_sealed_year_is_not_served_incrementally(self) -> None:
        self.two_audited()
        store = self.open_store()
        year = SECOND[:4]
        entries = list(store.audit_entries())
        ledger.write_year_digest(store.digest_dir, ledger.make_year_digest(year, entries))
        self.assertTrue(store._audit_evidence()["ok"])
        store._audit_immediate(("system", "synthetic_note", "-", "SYN late", SECOND))
        evidence = store._audit_evidence()
        self.assertFalse(evidence["ok"])
        self.assertIn("sealed year", evidence["reason"])

    def test_failed_begin_quarantines_unsaved_records_and_events_without_a_rollback(self) -> None:
        store = self.open_store()
        flaky = FlakyDb(store.db)
        store.db = flaky
        self.add(store, "bbb000000007", self.sam)
        store.local.pending.append(
            (
                self.sam["email"],
                "ai_run_end",
                "-",
                "priority_recommendation bbb000000007 n=5",
                SECOND,
            )
        )
        flaky.armed = True
        with self.assertRaises(sqlite3.OperationalError):
            store.save()
        self.assertNotIn("ROLLBACK", flaky.seen)
        self.assertNotIn("bbb000000007", {r["id"] for r in store.data["recommendations"]})
        self.assertFalse([p for p in store.local.pending if "bbb000000007" in p[3]])
        store.save()
        store._audit_immediate(("system", "synthetic_note", "-", "SYN flush", SECOND))
        store.db = flaky.real
        ids = {r[0] for r in store.db.execute("SELECT id FROM recommendations").fetchall()}
        self.assertNotIn("bbb000000007", ids)
        details = [e["detail"] for e in store.audit_entries()]
        self.assertFalse([d for d in details if "bbb000000007" in d])

    def test_repeated_ambiguous_batches_write_only_their_own_flags(self) -> None:
        store = self.unresolved_latest()
        writes: list[str] = []
        real = store._meta_set

        def counting(key: str, value: str) -> Any:
            writes.append(key)
            return real(key, value)

        store._meta_set = counting
        for n in range(4):
            self.old_writer_insert(store, f"r{n:011d}")
            self.assertEqual(self.latest(store), f"r{n:011d}")
        flags = [k for k in writes if k.startswith("rec_unres:")]
        self.assertEqual(len(flags), 4)
        self.assertEqual(len(set(flags)), 4)
        self.assertNotIn("rec_order_unresolved", writes)
        self.assertIsNone(self.meta(store, "rec_order_unresolved"))
        self.assertTrue(store.rec_order_unresolved("r00000000003"))

    def test_earlier_single_list_index_is_adopted_once_and_left_untouched(self) -> None:
        store = self.open_store()
        store.db.execute(
            "INSERT INTO meta (key, value) VALUES ('rec_order_unresolved', ?)",
            (json.dumps(["old000000001", "old000000002"]),),
        )
        store.db.execute("DELETE FROM meta WHERE key='rec_unres_index'")
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), ["old000000001", "old000000002"])
        self.assertEqual(
            json.loads(str(self.meta(reopened, "rec_order_unresolved"))),
            ["old000000001", "old000000002"],
        )
        self.assertEqual(self.meta(reopened, "rec_unres_index"), "1")


class CountingCursor:
    def __init__(self, probe: "CountingDb", cursor: Any, counted: bool) -> None:
        self.probe, self.cursor, self.counted = probe, cursor, counted

    def fetchall(self) -> Any:
        rows = self.cursor.fetchall()
        if self.counted:
            self.probe.rows += len(rows)
        return rows

    def fetchone(self) -> Any:
        row = self.cursor.fetchone()
        if self.counted and row is not None:
            self.probe.rows += 1
        return row

    def __getattr__(self, name: str) -> Any:
        return getattr(self.cursor, name)


class CountingDb:
    """Counts statements and recommendation rows read through a real connection."""

    def __init__(self, db: Any) -> None:
        self.real, self.rows, self.statements = db, 0, 0

    def execute(self, sql: str, *args: Any) -> Any:
        self.statements += 1
        counted = "FROM recommendations" in sql and "created_ord = 0" not in sql
        return CountingCursor(self, self.real.execute(sql, *args), counted)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.real, name)


class SqliteC4Corrections(SqliteFixture):
    """Correction C4 scenarios; SQLite and fakes only, SQL Server equivalents are pending."""

    rows: list[tuple[Any, ...]]
    two_audited: Any = SqliteC3Corrections.two_audited

    def ordinal_db(self, rows: list[tuple[Any, ...]], **meta: str) -> None:
        """A database with ordinals assigned by an earlier candidate: (id, seq, body, version)."""
        db = self.store.db
        db.execute("DROP TABLE recommendations")
        db.execute(self.native_ddl())
        for ordinal, (rid, seq, body, version) in enumerate(rows, 1):
            db.execute(
                "INSERT INTO recommendations VALUES (?,?,?,?,?,?)",
                (rid, version, seq, self.sam["email"], body, ordinal),
            )
        for key in ("rec_order_review", "rec_order_legacy", "rec_order_batches", "rec_unres_index"):
            db.execute("DELETE FROM meta WHERE key=?", (key,))
        db.execute("DELETE FROM meta WHERE key LIKE 'rec_order_batch:%' OR key LIKE 'rec_unres:%'")
        for key, value in meta.items():
            db.execute("DELETE FROM meta WHERE key=?", (key,))
            db.execute("INSERT INTO meta (key, value) VALUES (?, ?)", (key, value))

    def test_orphan_event_then_later_insert_and_edit_does_not_confirm_the_newest(self) -> None:
        first, second = self.two_audited((EARLIER, SECOND))
        top = max(seq for _, seq, *_ in self.rows)
        rows = [
            (rid, top + 1 if rid == first else seq, user, body, 2 if rid == first else version)
            for rid, seq, user, body, version in self.rows
        ]
        self.make_legacy(self.store, rows)
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), second)
        self.assertEqual(self.unresolved(reopened), [second])
        self.assertFalse(reopened.latest_priority(self.sam)["actionable"])

    def test_tied_sequence_with_different_timestamps_is_not_confirmed(self) -> None:
        first, second = self.two_audited((EARLIER, SECOND))
        self.make_legacy(
            self.store,
            [(rid, 50, user, body, version) for rid, _, user, body, version in self.rows],
        )
        reopened = self.open_store()
        self.assertEqual(self.latest(reopened), second)
        self.assertEqual(self.unresolved(reopened), [second])

    def test_agreeing_audit_and_distinct_unedited_sequence_confirm_in_order(self) -> None:
        self.two_audited((EARLIER, SECOND))
        self.make_legacy(self.store, self.rows)
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [])
        self.assertTrue(reopened.latest_priority(self.sam)["actionable"])

    def test_c1_shaped_rollback_history_is_reviewed_without_rewriting_ordinals(self) -> None:
        rows = [
            (f"c1r00000000{n}", n + 1, self.body(f"c1r00000000{n}", SECOND), 1) for n in (1, 2, 3)
        ]
        backfills = json.dumps(
            [dict(at=SECOND, rows=2, first_ord=2, last_ord=3, audited=0, heuristic=2)]
        )
        self.ordinal_db(rows, rec_order_backfills=backfills)
        reopened = self.open_store()
        self.assertEqual(self.ordinals(reopened), [r[0] for r in rows])
        self.assertEqual(self.unresolved(reopened), ["c1r000000003"])
        self.assertTrue(self.flagged_latest(reopened))
        self.assertEqual([b["source"] for b in self.batches(reopened)], ["review"])

    def flagged_latest(self, store: Any) -> bool:
        view = store.latest_priority(self.sam)
        return bool(view.get("order_confirmed") is False and not view["actionable"])

    def test_malformed_c1_history_is_treated_as_wholly_suspect(self) -> None:
        for bad in ("not json", json.dumps([dict(first_ord="x")]), json.dumps({"a": 1})):
            with self.subTest(bad=bad):
                rows = [
                    (f"c1m0000000{n}", n + 1, self.body(f"c1m0000000{n}", SECOND), 1)
                    for n in (10, 11)
                ]
                self.ordinal_db(rows, rec_order_backfills=bad)
                reopened = self.open_store()
                self.assertEqual(self.unresolved(reopened), ["c1m000000011"])

    def legacy_pair(self, status: str) -> Any:
        user = self.sam["email"]
        newest = json.dumps(dict(self.template, id="mmm000000002", created=SECOND, status=status))
        self.make_legacy(
            self.store,
            [
                ("zzz000000001", 2, user, self.body("zzz000000001", SECOND)),
                ("mmm000000002", 3, user, newest),
            ],
        )
        return self.open_store()

    def exported(self, store: Any, limited: bool) -> dict[str, Any]:
        ids = [r["id"] for r in store.data["recommendations"]]
        with patch("zava_forward.core.projection.can_see_reason", return_value=not limited):
            bundle = store.continuity_export(self.pam)
        self.assertEqual(bundle["audience"]["scope"], "limited" if limited else "full")
        return dict(zip(ids, bundle["ai_records"], strict=True))

    def test_continuity_exports_apply_the_unresolved_projection(self) -> None:
        for status in ("Proposed", "Accepted", "Edited"):
            for limited in (False, True):
                with self.subTest(status=status, limited=limited):
                    self.setUp()
                    record = self.exported(self.legacy_pair(status), limited)["mmm000000002"]
                    self.assertIs(record["actionable"], False)
                    self.assertIs(record["relied_on"], False)
                    self.assertIs(record["order_confirmed"], False)

    def test_continuity_export_leaves_confirmed_and_other_records_unchanged(self) -> None:
        self.two_audited((EARLIER, SECOND))
        self.make_legacy(self.store, self.rows)
        records = self.exported(self.open_store(), False)
        self.assertNotIn("order_confirmed", records[self.rows[1][0]])
        self.assertTrue(records[self.rows[1][0]]["actionable"])

    def test_singleton_rollback_write_after_native_records_stays_confirmed(self) -> None:
        native = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.old_writer_insert(self.store, "bbb000000002")
        self.store._audit_immediate(
            ("system", "ai_run_end", "-", "priority_recommendation bbb000000002 n=5", SECOND)
        )
        reopened = self.open_store()
        self.assertEqual(self.ordinals(reopened)[-2:], [native, "bbb000000002"])
        self.assertEqual(self.latest(reopened), "bbb000000002")
        self.assertEqual(self.unresolved(reopened), [])
        done = reopened.resolve_priority(self.sam, "bbb000000002", "accept")
        self.assertEqual(done["status"], "Accepted")

    def test_two_rollback_writes_in_one_batch_stay_unresolved_and_other_user_is_clear(self) -> None:
        self.old_writer_insert(self.store, "bbb000000002")
        self.old_writer_insert(self.store, "ccc000000003")
        self.old_writer_insert(self.store, "ppp000000004", user=self.pam)
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), ["ccc000000003"])
        self.assertEqual(self.latest(reopened, self.pam), "ppp000000004")

    def test_post_commit_reload_exhaustion_is_a_committed_outcome(self) -> None:
        from zava_forward.core import sqlstore as sqlmod

        other = self.open_store()
        self.add(other, "ooo000000001", self.pam)
        other.save()
        self.add(self.store, "bbb000000005", self.sam)

        def exhausted() -> None:
            raise RuntimeError("Reload could not settle against concurrent writers; retry.")

        with patch.object(self.store, "_sync", exhausted):
            with self.assertRaises(sqlmod.CommittedReloadError) as caught:
                self.store.save()
        self.assertTrue(caught.exception.committed)
        self.assertIn("saved", str(caught.exception))
        ids = [r[0] for r in self.store.db.execute("SELECT id FROM recommendations").fetchall()]
        self.assertEqual(ids.count("bbb000000005"), 1)
        self.assertEqual(self.latest(self.store), "bbb000000005")

    def test_post_commit_reload_oserror_or_valueerror_is_a_committed_outcome(self) -> None:
        from zava_forward.core import sqlstore as sqlmod

        for n, error in enumerate((OSError("disk"), ValueError("row"))):
            with self.subTest(error=type(error).__name__):
                other = self.open_store()
                self.add(other, f"ooo00000010{n}", self.pam)
                other.save()
                rid = f"bbb00000010{n}"
                self.add(self.store, rid, self.sam)

                def failing(error: BaseException = error) -> None:
                    raise error

                with patch.object(self.store, "_sync", failing):
                    with self.assertRaises(sqlmod.CommittedReloadError) as caught:
                        self.store.save()
                self.assertTrue(caught.exception.committed)
                self.assertIs(caught.exception.__cause__, error)
                ids = [r[0] for r in self.store.db.execute("SELECT id FROM recommendations")]
                self.assertEqual(ids.count(rid), 1)
                self.store.save()
                ids = [r[0] for r in self.store.db.execute("SELECT id FROM recommendations")]
                self.assertEqual(ids.count(rid), 1)

    def test_server_reports_a_committed_priority_outcome(self) -> None:
        server = (Path(__file__).parents[2] / "api/src/zava_forward/api/server.py").read_text()
        at = server.rindex('if url.path == "/api/ai/priority":')
        self.assertIn("CommittedReloadError", server[at - 400 : at + 700])

    def pending_task(self, store: Any) -> None:
        self.add(store, "tsk000000001", self.sam, kind="ai_task")
        self.add(store, "bbb000000007", self.sam)
        mine = self.sam["email"]
        store.local.pending.extend(
            [
                (mine, "synthetic_note", "-", "SYN unrelated tsk000000001x", SECOND),
                (mine, "ai_record", "-", "plan tsk000000001 mode=x source=y verified=True", SECOND),
                (mine, "ai_run_end", "-", "priority_recommendation bbb000000007 n=5", SECOND),
            ]
        )

    def assert_quarantined(self, store: Any) -> None:
        self.assertEqual([p[3] for p in store.local.pending], ["SYN unrelated tsk000000001x"])
        store.save()
        ids = {r[0] for r in store.db.execute("SELECT id FROM recommendations").fetchall()}
        self.assertFalse(ids & {"tsk000000001", "bbb000000007"})
        details = [e["detail"] for e in store.audit_entries()]
        self.assertFalse([d for d in details if "plan tsk000000001" in d or "bbb000000007" in d])
        self.assertIn("SYN unrelated tsk000000001x", details)

    def test_failed_begin_quarantines_the_ai_task_creation_event_too(self) -> None:
        store = self.open_store()
        flaky = FlakyDb(store.db)
        store.db = flaky
        self.pending_task(store)
        flaky.armed = True
        with self.assertRaises(sqlite3.OperationalError):
            store.save()
        self.assert_quarantined(store)

    def test_failure_after_begin_quarantines_the_ai_task_creation_event_too(self) -> None:
        store = self.open_store()
        self.pending_task(store)
        with patch.object(store, "_validate_safety_clear", side_effect=RuntimeError("injected")):
            with self.assertRaises(RuntimeError):
                store.save()
        self.assert_quarantined(store)

    def test_repeated_singleton_repairs_read_a_bounded_number_of_history_rows(self) -> None:
        history = [(f"h{n:011d}", n + 1, self.body(f"h{n:011d}", SECOND), 1) for n in range(60)]
        self.ordinal_db(history, rec_order_review="3")
        store = self.open_store()
        probe = CountingDb(store.db)
        store.db = probe
        reads = []
        for n in range(4):
            self.old_writer_insert(store, f"s{n:011d}")
            before = probe.rows
            store._repair_zero_ordinals()
            reads.append(probe.rows - before)
        self.assertLessEqual(max(reads), 8, reads)
        self.assertEqual(self.unresolved(store), [])

    def test_many_singleton_batches_are_reviewed_with_bounded_statements(self) -> None:
        rows = [
            (f"b{n:011d}", n + 1, self.body(f"b{n:011d}", f"2026-11-08T09:{n % 60:02d}:00"), 1)
            for n in range(1500)
        ]
        self.ordinal_db(rows)
        batches = {
            f"rec_order_batch:{n}": json.dumps(dict(first_ord=n, last_ord=n, source="repair"))
            for n in range(1, 1501)
        }
        for key, value in batches.items():
            self.store.db.execute("INSERT INTO meta (key, value) VALUES (?, ?)", (key, value))
        self.store.db.execute("INSERT INTO meta (key, value) VALUES ('rec_order_batches', '1500')")
        probe = CountingDb(self.store.db)
        self.store.db = probe
        self.store.db.execute("BEGIN IMMEDIATE")
        self.store._review_priority_order()
        self.store.db.execute("COMMIT")
        self.assertLess(probe.statements, 60)
        self.assertEqual(self.unresolved(self.store), ["b00000001499"])

    def digest_for(self, store: Any) -> Path:
        count, head = store.ledger_head()
        return Path(ledger.write_digest(store.digest_dir, ledger.make_digest(count, head)))

    def test_digest_readability_and_content_changes_invalidate_the_cache(self) -> None:
        self.two_audited()
        store = self.open_store()
        path = self.digest_for(store)
        self.assertTrue(store._audit_evidence()["ok"])
        path.chmod(0)
        try:
            self.assertFalse(store._audit_evidence()["ok"])
        finally:
            path.chmod(0o600)
        self.assertTrue(store._audit_evidence()["ok"])
        stamp = path.stat().st_mtime_ns
        original = path.read_text()
        changed = json.loads(original)
        changed["head"] = "f" * len(changed["head"])
        path.write_text(json.dumps(changed, sort_keys=True))
        os.utime(path, ns=(stamp, stamp))
        self.assertEqual(len(original), len(path.read_text()))
        self.assertFalse(store._audit_evidence()["ok"])

    def test_malformed_independent_digests_are_unusable_evidence(self) -> None:
        self.two_audited()
        store = self.open_store()
        count, head = store.ledger_head()
        good = dict(algorithm="sha256", chain="main", count=count, head=head)
        bad = [
            {},
            [],
            "text",
            dict(good, count="1"),
            dict(good, count=True),
            dict(good, count=0),
            dict(good, count=-3),
            dict(good, head=""),
            dict(good, head=7),
            dict(good, algorithm="md5"),
        ]
        for n, content in enumerate(bad):
            with self.subTest(content=content):
                folder = Path(self.tmp.name) / f"digests{n}"
                folder.mkdir()
                (folder / "digest-0000000001.json").write_text(json.dumps(content))
                store.digest_dir = str(folder)
                store._audit_ev = None
                evidence = store._audit_evidence()
                self.assertFalse(evidence["ok"])
                self.assertIn("digest", evidence["reason"])

    def test_malformed_digest_does_not_stop_startup_and_leaves_order_unresolved(self) -> None:
        self.two_audited()
        self.make_legacy(self.store, self.rows)
        Path(self.store.digest_dir).mkdir(parents=True, exist_ok=True)
        (Path(self.store.digest_dir) / "digest-0000000001.json").write_text("[]")
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [self.latest(reopened)])

    def test_priority_panel_keeps_the_order_note_for_every_status(self) -> None:
        web = Path(__file__).parents[2] / "api/src/zava_forward/api/web/app.js"
        text = web.read_text(encoding="utf-8")
        shared = text.index("rec?.order_note")
        self.assertLess(shared, text.index('if (rec.status === "Proposed")'))
        load = text.index('api("/api/ai/priority").then')
        self.assertIn("order_note", text[load : load + 400])


class LegacyMetadata(SqliteFixture):
    """Earlier-candidate database: ordinals marked heuristic only by rec_order_legacy (#1292 E1)."""

    FIRST, LATEST = "zzz000000001", "mmm000000002"
    RESET = (
        "DELETE FROM meta WHERE key LIKE 'rec_order_batch%' OR key LIKE 'rec_unres%' "
        "OR key IN ('rec_order_review', 'rec_order_unresolved', 'rec_order_backfills')"
    )
    MALFORMED = {
        "invalid json": "{not json",
        "empty text": "",
        "empty object": "{}",
        "list": "[]",
        "null": "null",
        "bare number": "2",
        "missing rows": json.dumps(dict(same_second_groups=1)),
        "negative rows": json.dumps(dict(rows=-2)),
        "zero rows": json.dumps(dict(rows=0)),
        "string rows": json.dumps(dict(rows="2")),
        "bool rows": json.dumps(dict(rows=True)),
        "float rows": json.dumps(dict(rows=2.0)),
    }

    def earlier_candidate(self, legacy: str | None) -> Any:
        """Two same-second proposals with positive ordinals; only the legacy row marks them."""
        user = self.sam["email"]
        self.make_legacy(
            self.store,
            [
                (self.FIRST, 2, user, self.body(self.FIRST, SECOND)),
                (self.LATEST, 3, user, self.body(self.LATEST, SECOND)),
            ],
        )
        backfilled = self.open_store()
        self.assertEqual(self.ordinals(backfilled), [self.FIRST, self.LATEST])
        backfilled.db.execute(self.RESET)
        backfilled.db.execute("DELETE FROM meta WHERE key='rec_order_legacy'")
        if legacy is not None:
            backfilled.db.execute(
                "INSERT INTO meta (key, value) VALUES ('rec_order_legacy', ?)", (legacy,)
            )
        return backfilled

    def test_malformed_legacy_row_fails_conservative_without_guessing_the_latest(self) -> None:
        for name, legacy in self.MALFORMED.items():
            with self.subTest(name):
                self.setUp()
                self.earlier_candidate(legacy)
                reopened = self.open_store()
                self.assertEqual(self.ordinals(reopened), [self.FIRST, self.LATEST], name)
                self.assertEqual(self.unresolved(reopened), [self.LATEST], name)
                self.assertEqual(self.meta(reopened, "rec_order_legacy"), legacy, name)
                self.assertEqual(self.batches(reopened)[0]["source"], "review", name)
                view = reopened.latest_priority(self.sam)
                self.assertEqual(view["id"], self.LATEST)
                flags = (view["order_confirmed"], view["actionable"], view["relied_on"])
                self.assertEqual(flags, (False, False, False), name)
                items = [dict(case_id=i["case_id"], reason="SYN") for i in view["items"]]
                with self.assertRaises(PermissionError):
                    reopened.resolve_priority(self.sam, self.LATEST, "accept")
                with self.assertRaises(PermissionError):
                    reopened.resolve_priority(self.sam, self.LATEST, "edit", "SYN why", items)
                self.assertEqual(self.ordinals(self.open_store()), [self.FIRST, self.LATEST], name)

    def test_valid_legacy_row_bounds_the_suspect_range(self) -> None:
        for rows, flagged in ((2, [self.LATEST]), (1, [])):
            with self.subTest(rows=rows):
                self.setUp()
                legacy = dict(rows=rows, same_second_groups=1, order="created,seq,id")
                self.earlier_candidate(json.dumps(legacy))
                reopened = self.open_store()
                self.assertEqual(self.unresolved(reopened), flagged)
                self.assertEqual(self.ordinals(reopened), [self.FIRST, self.LATEST])

    def test_absent_legacy_row_is_the_insert_time_case_and_flags_nothing(self) -> None:
        self.earlier_candidate(None)
        reopened = self.open_store()
        self.assertEqual(self.unresolved(reopened), [])
        self.assertIsNone(self.meta(reopened, "rec_order_legacy"))
        self.assertEqual(self.ordinals(reopened), [self.FIRST, self.LATEST])


class MssqlBeginRecovery(unittest.TestCase):
    """The SQL Server adapter must not leave a transaction open when BEGIN fails part way."""

    class Error(Exception):
        pass

    def adapter(self, rollback_fails: bool = False) -> Any:
        from zava_forward.core import mssqlstore

        outer = self
        state = types.SimpleNamespace(open=0, log=[], timeout=True)

        class Cursor:
            rowcount = 0

            def execute(self, sql: str, args: Any = ()) -> None:
                state.log.append(sql.split()[0] + " " + sql.split()[1])
                if sql.startswith("BEGIN TRAN"):
                    state.open += 1
                    if state.timeout:
                        raise outer.Error("could not take the write lock")
                elif "ROLLBACK TRAN" in sql:
                    if rollback_fails:
                        raise outer.Error("rollback failed")
                    state.open = 0
                elif sql.startswith("COMMIT"):
                    state.open = max(0, state.open - 1)

        class Raw:
            def cursor(self) -> Cursor:
                return Cursor()

            def close(self) -> None:
                state.open = 0
                state.log.append("CLOSE")

        conn = mssqlstore._Conn.__new__(mssqlstore._Conn)
        fake_driver = types.ModuleType("fake_mssql_python")
        vars(fake_driver)["Error"] = self.Error
        conn.driver = fake_driver
        conn.conn_str, conn.raw, conn.in_tran, conn.attrs = "", Raw(), False, {}
        conn.state = state  # type: ignore[attr-defined]
        return conn

    def test_failed_begin_batch_leaves_no_open_transaction(self) -> None:
        conn = self.adapter()
        with self.assertRaisesRegex(self.Error, "write lock"):
            conn.execute("BEGIN IMMEDIATE")
        self.assertEqual((conn.state.open, conn.in_tran), (0, False))
        conn.state.timeout = False
        conn.execute("BEGIN IMMEDIATE")
        self.assertEqual((conn.state.open, conn.in_tran), (1, True))
        conn.execute("COMMIT")
        self.assertEqual(conn.state.open, 0)

    def test_failed_rollback_discards_the_connection_and_keeps_the_original_error(self) -> None:
        conn = self.adapter(rollback_fails=True)
        with self.assertRaisesRegex(self.Error, "write lock"):
            conn.execute("BEGIN IMMEDIATE")
        self.assertEqual((conn.state.open, conn.in_tran), (0, False))
        self.assertIn("CLOSE", conn.state.log)
        self.assertIsNone(conn.raw)


class LoopbackGuard(unittest.TestCase):
    PASSWORD = "SYN-one-time-secret"
    CONTAINER = "ab" * 32

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manifest = str(Path(self.tmp.name) / "task-sql.json")
        write_manifest(self.manifest, "127.0.0.1", "14331", self.PASSWORD, self.CONTAINER)

    def inspect(self, **change: Any) -> Any:
        info: dict[str, Any] = dict(
            Id=self.CONTAINER,
            Created=datetime.now().astimezone().isoformat(),
            State=dict(Running=True),
            Config=dict(
                Labels={"zf.task": "1292-sql-disposable"},
                Env=[f"MSSQL_SA_PASSWORD={self.PASSWORD}"],
            ),
            NetworkSettings=dict(Ports={"1433/tcp": [dict(HostIp="127.0.0.1", HostPort="14331")]}),
        )
        info.update(change)
        return lambda _container: info

    def env(self, **override: str) -> dict[str, str]:
        base = dict(
            ZF_SQL_SERVER="127.0.0.1",
            ZF_SQL_PORT="14331",
            ZF_SQL_AUTH="password",
            ZF_SQL_PASSWORD=self.PASSWORD,
            ZF_SQL_TASK_MANIFEST=self.manifest,
        )
        base.update(override)
        return base

    def refuse(self, case_type: type, env: dict[str, str]) -> None:
        constructed: list[str] = []

        def forbidden(*_args: Any, **_kwargs: Any) -> Any:
            constructed.append("connection")
            raise AssertionError("connection attempted before the admission check")

        fake = types.SimpleNamespace(_Conn=forbidden, connection_string=lambda *_a, **_k: "x")
        case = case_type("setUp")
        with (
            patch.dict(os.environ, env),
            patch.dict(sys.modules, {"zava_forward.core.mssqlstore": fake}),
        ):
            with self.assertRaises(RuntimeError):
                case.setUp()
        self.assertEqual(constructed, [])

    def test_task_owned_sql_fixtures_refuse_unadmitted_destinations_before_any_connection(
        self,
    ) -> None:
        import test_resident_decisions

        other = Path(self.tmp.name) / "other.json"
        write_manifest(str(other), "127.0.0.1", "14332", self.PASSWORD, self.CONTAINER)
        loose = Path(self.tmp.name) / "loose.json"
        write_manifest(str(loose), "127.0.0.1", "14331", self.PASSWORD, self.CONTAINER)
        loose.chmod(0o666)
        stale = Path(self.tmp.name) / "stale.json"
        write_manifest(
            str(stale),
            "127.0.0.1",
            "14331",
            self.PASSWORD,
            self.CONTAINER,
            created=time.time() - 90000,
        )
        cases = [
            self.env(ZF_SQL_SERVER="example.database.windows.net"),
            self.env(ZF_SQL_SERVER="10.1.2.3"),
            self.env(ZF_SQL_SERVER=""),
            self.env(ZF_SQL_AUTH="msi"),
            self.env(ZF_SQL_TASK_MANIFEST=""),
            self.env(ZF_SQL_TASK_MANIFEST=str(Path(self.tmp.name) / "missing.json")),
            self.env(ZF_SQL_TASK_MANIFEST=str(other)),
            self.env(ZF_SQL_PASSWORD="a-shared-server-password"),
            self.env(ZF_SQL_TASK_MANIFEST=str(loose)),
            self.env(ZF_SQL_TASK_MANIFEST=str(stale)),
            self.env(ZF_SQL_PORT="1433"),
        ]
        for case_type in (MssqlPriorityOrder, test_resident_decisions.MssqlResidentControls):
            for env in cases:
                with self.subTest(
                    case=case_type.__name__, server=env["ZF_SQL_SERVER"], port=env["ZF_SQL_PORT"]
                ):
                    self.refuse(case_type, env)

    def test_symlinked_manifest_is_refused(self) -> None:
        link = Path(self.tmp.name) / "link.json"
        link.symlink_to(self.manifest)
        with self.assertRaises(RuntimeError):
            require_task_owned_loopback(self.env(ZF_SQL_TASK_MANIFEST=str(link)), self.inspect())

    def bound(self, host_ip: str, port: str = "14331") -> Any:
        return self.inspect(
            NetworkSettings=dict(Ports={"1433/tcp": [dict(HostIp=host_ip, HostPort=port)]})
        )

    def test_admitted_loopback_endpoint_is_accepted_only_for_its_own_published_address(
        self,
    ) -> None:
        for host in ("127.0.0.1", "127.0.0.2", "::1"):
            path = self.manifest + host
            write_manifest(path, host, "14331", self.PASSWORD, self.CONTAINER)
            env = self.env(ZF_SQL_SERVER=f"[{host}]" if ":" in host else host)
            env["ZF_SQL_TASK_MANIFEST"] = path
            require_task_owned_loopback(env, self.bound(host))

    def test_connecting_host_must_equal_the_address_the_container_publishes(self) -> None:
        for host, published in (
            ("127.0.0.2", "127.0.0.1"),
            ("127.0.0.1", "::1"),
            ("::1", "127.0.0.1"),
            ("localhost", "127.0.0.1"),
        ):
            with self.subTest(host=host, published=published):
                path = self.manifest + host
                write_manifest(path, host, "14331", self.PASSWORD, self.CONTAINER)
                env = self.env(ZF_SQL_SERVER=host, ZF_SQL_TASK_MANIFEST=path)
                with self.assertRaises(RuntimeError):
                    require_task_owned_loopback(env, self.bound(published))

    def test_remote_docker_engines_are_refused_before_any_inspection(self) -> None:
        def forbidden(_container: str) -> Any:
            raise AssertionError("inspected before the engine was proven local")

        for extra in (
            dict(DOCKER_HOST="tcp://10.1.2.3:2375"),
            dict(DOCKER_HOST="ssh://someone@host"),
            dict(DOCKER_HOST="unix:///var/run/docker.sock", DOCKER_TLS_VERIFY="1"),
            dict(DOCKER_CONTEXT="remote"),
        ):
            with self.subTest(extra=extra):
                with self.assertRaises(RuntimeError):
                    require_task_owned_loopback(self.env(**extra), forbidden)
        require_task_owned_loopback(
            self.env(DOCKER_HOST="unix:///var/run/docker.sock", DOCKER_CONTEXT="default"),
            self.inspect(),
        )

    def test_caller_written_manifest_without_matching_container_evidence_is_refused(self) -> None:
        def missing(_container: str) -> Any:
            raise OSError("no such container")

        bad = [
            missing,
            self.inspect(Id="cd" * 32),
            self.inspect(State=dict(Running=False)),
            self.inspect(Config=dict(Labels={}, Env=[f"MSSQL_SA_PASSWORD={self.PASSWORD}"])),
            self.inspect(
                Config=dict(Labels={"zf.task": "other"}, Env=[f"MSSQL_SA_PASSWORD={self.PASSWORD}"])
            ),
            self.inspect(
                NetworkSettings=dict(Ports={"1433/tcp": [dict(HostIp="0.0.0.0", HostPort="14331")]})
            ),
            self.inspect(
                NetworkSettings=dict(Ports={"1433/tcp": [dict(HostIp="127.0.0.1", HostPort="9")]})
            ),
            self.inspect(
                Config=dict(
                    Labels={"zf.task": "1292-sql-disposable"}, Env=["MSSQL_SA_PASSWORD=other"]
                )
            ),
            self.inspect(Created="2020-01-01T00:00:00+00:00"),
        ]
        for inspector in bad:
            with self.subTest(inspector=getattr(inspector, "__name__", "info")):
                with self.assertRaises(RuntimeError):
                    require_task_owned_loopback(self.env(), inspector)
        require_task_owned_loopback(self.env(), self.inspect())

    def test_manifest_is_private_and_stores_only_a_password_digest(self) -> None:
        text = Path(self.manifest).read_text()
        self.assertNotIn(self.PASSWORD, text)
        self.assertIn(hashlib.sha256(self.PASSWORD.encode()).hexdigest(), text)
        self.assertEqual(stat.S_IMODE(os.stat(self.manifest).st_mode) & 0o077, 0)


class OwnedMssql(SqliteFixture):
    """Each test owns a UUID-named database on the admitted task-owned loopback SQL Server."""

    def setUp(self) -> None:
        require_task_owned_loopback(os.environ)
        from zava_forward.core.mssqlstore import _Conn, connection_string

        self.database = database = "zf_priority1292_" + uuid.uuid4().hex
        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{database}]")

        def drop_owned_database() -> None:
            admin.execute(f"ALTER DATABASE [{database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE")
            admin.execute(f"DROP DATABASE [{database}]")

        self.addCleanup(drop_owned_database)
        os.environ["ZF_SQL_DATABASE"] = database
        super().setUp()

    def native_ddl(self) -> str:
        from zava_forward.core.mssqlstore import TABLES

        return TABLES["recommendations"]

    def lift_audit_guard(self, store: Any, trigger: str) -> None:
        store.db.execute("DROP TRIGGER audit_append_only")

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


OPT_IN = unittest.skipUnless(
    os.environ.get("ZF_RESIDENT_MSSQL") == "1", "opt-in owned loopback SQL Server"
)


@OPT_IN
class MssqlPriorityOrder(OwnedMssql, SqlitePriorityOrder):
    pass


@OPT_IN
class MssqlLegacyMetadata(OwnedMssql, LegacyMetadata):
    pass


@OPT_IN
class MssqlLegacyEdges(OwnedMssql, SqliteLegacyEdges):
    pass


@OPT_IN
class MssqlC3Corrections(OwnedMssql, SqliteC3Corrections):
    pass


@OPT_IN
class MssqlC4Corrections(OwnedMssql, SqliteC4Corrections):
    pass


@OPT_IN
class MssqlLockTimeoutBegin(unittest.TestCase):
    """A real write-lock timeout on BEGIN leaves no open transaction and a usable connection."""

    def setUp(self) -> None:
        require_task_owned_loopback(os.environ)
        from zava_forward.core.mssqlstore import _Conn, connection_string

        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        self.holder, self.waiter = _Conn(connection_string()), _Conn(connection_string())
        self.addCleanup(self.holder.close)
        self.addCleanup(self.waiter.close)

    @staticmethod
    def depth(conn: Any) -> int:
        return int(conn.execute("SELECT @@TRANCOUNT").fetchone()[0])

    def test_lock_timeout_on_a_second_connection_leaves_zero_open_transactions(self) -> None:
        from zava_forward.core import mssqlstore

        short = mssqlstore.BEGIN.replace("@LockTimeout = 15000", "@LockTimeout = 300")
        self.assertNotEqual(short, mssqlstore.BEGIN)
        self.holder.execute("BEGIN IMMEDIATE")
        self.assertEqual(self.depth(self.holder), 1)
        with patch.object(mssqlstore, "BEGIN", short):
            with self.assertRaisesRegex(self.waiter.driver.Error, "write lock"):
                self.waiter.execute("BEGIN IMMEDIATE")
        self.assertFalse(self.waiter.in_tran)
        self.assertEqual(self.depth(self.waiter), 0)
        self.assertEqual(self.depth(self.holder), 1)
        self.holder.execute("ROLLBACK")
        self.assertEqual(self.depth(self.holder), 0)
        self.waiter.execute("BEGIN IMMEDIATE")
        self.assertEqual((self.depth(self.waiter), self.waiter.in_tran), (1, True))
        self.waiter.execute("COMMIT")
        self.assertEqual(self.depth(self.waiter), 0)
