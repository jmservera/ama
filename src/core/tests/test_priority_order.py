"""Newest-created order of priority recommendations across SQL reloads (#1292), synthetic data."""

import copy
import hashlib
import json
import os
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
        return sorted(json.loads(self.meta(store, "rec_order_unresolved") or "[]"))


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
        self.assertEqual(self.unresolved(reopened), ["mmm000000002", "zzz000000001"])
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
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        rows = []
        for rid, seq, user, body, version in self.store.db.execute(
            "SELECT id, seq, user, body, rowversion FROM recommendations"
        ).fetchall():
            rec = dict(json.loads(body), created=SECOND)
            late = seq + 50 if rid == first else seq
            rows.append((rid, late, user, json.dumps(rec), version))
        self.make_legacy(self.store, rows)
        reopened = self.open_store()
        self.assertTrue({first, second} <= set(self.unresolved(reopened)))
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
        store.db.execute("DROP TRIGGER audit_no_delete")
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
        self.assertTrue({first, second} <= set(self.unresolved(reopened)))

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
        db.execute(
            "CREATE TABLE recommendations (id TEXT PRIMARY KEY, "
            "rowversion INTEGER NOT NULL DEFAULT 1, seq INTEGER NOT NULL, user TEXT NOT NULL, "
            "body TEXT NOT NULL, created_ord BIGINT NOT NULL DEFAULT 0)"
        )
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
        before = self.ordinals(self.store)
        self.assertLess(before.index(second), before.index(first))
        reopened = self.open_store()
        self.assertEqual(self.ordinals(reopened), before)
        self.assertEqual(self.meta(reopened, "rec_order_legacy"), legacy)
        self.assertEqual(self.batches(reopened)[0]["source"], "c0-review")
        self.assertTrue({first, second} <= set(self.unresolved(reopened)))
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
        second = self.store.ai_priority(self.sam, mode="workflow-only")["id"]
        self.store.resolve_priority(self.sam, first, "accept", "SYN review of the older proposal")
        rows = []
        for rid, seq, user, body, version in self.store.db.execute(
            "SELECT id, seq, user, body, rowversion FROM recommendations"
        ).fetchall():
            rows.append(
                (rid, seq, user, json.dumps(dict(json.loads(body), created=SECOND)), version)
            )
        self.make_legacy(self.store, rows)
        self.store.db.execute("DROP TRIGGER audit_no_update")
        self.store.db.execute("UPDATE audit SET who='tampered' WHERE seq=1")
        batch = self.batches(self.open_store())[0]
        self.assertFalse(batch["audit_chain"])
        self.assertEqual(batch["audited"], 0)
        self.assertGreater(batch["ambiguous_total"], 0)
        self.assertIn(second, batch["ambiguous_ids"])
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
    PASSWORD = "SYN-one-time-secret"

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manifest = str(Path(self.tmp.name) / "task-sql.json")
        write_manifest(self.manifest, "127.0.0.1", "14331", self.PASSWORD)

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
        write_manifest(str(other), "127.0.0.1", "14332", self.PASSWORD)
        loose = Path(self.tmp.name) / "loose.json"
        write_manifest(str(loose), "127.0.0.1", "14331", self.PASSWORD)
        loose.chmod(0o666)
        stale = Path(self.tmp.name) / "stale.json"
        write_manifest(str(stale), "127.0.0.1", "14331", self.PASSWORD, created=time.time() - 90000)
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
            require_task_owned_loopback(self.env(ZF_SQL_TASK_MANIFEST=str(link)))

    def test_admitted_loopback_endpoint_is_accepted(self) -> None:
        for host in ("127.0.0.1", "localhost", "[::1]"):
            write_manifest(self.manifest + host, host.strip("[]"), "14331", self.PASSWORD)
            require_task_owned_loopback(
                self.env(ZF_SQL_SERVER=host, ZF_SQL_TASK_MANIFEST=self.manifest + host)
            )

    def test_manifest_is_private_and_stores_only_a_password_digest(self) -> None:
        text = Path(self.manifest).read_text()
        self.assertNotIn(self.PASSWORD, text)
        self.assertIn(hashlib.sha256(self.PASSWORD.encode()).hexdigest(), text)
        self.assertEqual(stat.S_IMODE(os.stat(self.manifest).st_mode) & 0o077, 0)


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
