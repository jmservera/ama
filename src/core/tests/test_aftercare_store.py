"""Runtime aftercare adapter over the Store and SqlStore document mechanism (issue 133).

Synthetic records only. JSON Store and SQLite always run; the owned SQL Server variants run when
ZF_RESIDENT_MSSQL=1 and the task-owned loopback admission passes (SQLite is not a substitute).
"""

import copy
import json
import os
import tempfile
import threading
import unittest
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

from dataset import DATA
from sqlguard import require_task_owned_loopback
from zava_forward.core import aftercare_intake as ai
from zava_forward.core.aftercare_store import DocumentStateStore, UnconfirmedWriteError
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.synthetic import sensor_scenarios as ss

NOW = datetime(2026, 11, 9, 12, 0, tzinfo=UTC)
LIAISON = {"name": "Synthetic Liaison", "role": "Resident Liaison Officer"}
MANAGER = {"name": "Synthetic Manager", "role": "Retrofit Programme Manager"}


def _first_home(scenario: dict[str, object]) -> str:
    rows = scenario["rows"]
    assert isinstance(rows, (list, tuple))
    return str(rows[0]["home_id"])


HOMES = [_first_home(s) for s in ss.retrofit_exercise_scenarios()]


def body(
    request_id: str, statement: str = "The living room stays cold in the evening."
) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "raised_by": "household",
        "home_ref": HOMES[0],
        "kind": "discomfort",
        "statement": statement,
        "channel": "phone",
        "next_update": "2026-11-20",
    }


# Type checkers see the mixin as a TestCase; at runtime it stays a plain mixin so only concrete
# subclasses are collected.
if TYPE_CHECKING:

    class _Base(unittest.TestCase): ...

else:

    class _Base: ...


class Contract(_Base):
    """Shared behaviour; each subclass supplies open_store()."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        self.path.write_text(json.dumps(copy.deepcopy(DATA)))
        self.store = self.open_store()

    def open_store(self) -> Any:
        raise NotImplementedError

    def service(self, store: Any = None) -> ai.AftercareService:
        return ai.AftercareService(
            DocumentStateStore(store or self.store), homes=HOMES, now=lambda: NOW
        )

    def count(self, store: Any = None) -> int:
        return int(self.service(store).concerns(MANAGER)["count"])

    def test_first_read_is_empty_and_namespace_is_explicit(self) -> None:
        self.assertIsNone(DocumentStateStore(self.store).read())
        self.assertEqual(self.count(), 0)

    def test_restart_keeps_receipt_register_and_request_index_together(self) -> None:
        receipt, replay = self.service().record_concern(LIAISON, body("req-0000001"))
        self.assertFalse(replay)
        reopened = self.open_store()
        doc = json.loads(DocumentStateStore(reopened).read() or "{}")
        self.assertEqual(set(doc["requests"]), {"req-0000001"})
        self.assertIn(receipt["concern_id"], doc["receipts"])
        self.assertIn("register", doc)
        again, replay = self.service(reopened).record_concern(LIAISON, body("req-0000001"))
        self.assertTrue(replay)
        self.assertEqual(again["receipt_id"], receipt["receipt_id"])
        self.assertEqual(self.count(reopened), 1)

    def test_same_id_same_payload_replays_without_a_second_write(self) -> None:
        svc = self.service()
        svc.record_concern(LIAISON, body("req-0000002"))
        before = DocumentStateStore(self.store).read()
        with patch.object(self.store, "save", side_effect=AssertionError("replay wrote")):
            _, replay = svc.record_concern(LIAISON, body("req-0000002"))
        self.assertTrue(replay)
        self.assertEqual(DocumentStateStore(self.store).read(), before)

    def test_changed_payload_with_same_id_conflicts_and_keeps_the_original(self) -> None:
        svc = self.service()
        svc.record_concern(LIAISON, body("req-0000003"))
        with self.assertRaises(ai.ConflictError):
            svc.record_concern(LIAISON, body("req-0000003", "A different statement."))
        self.assertEqual(self.count(), 1)

    def test_precommit_failure_reports_nothing_saved_and_leaves_state(self) -> None:
        svc = self.service()
        svc.record_concern(LIAISON, body("req-0000004"))
        before = DocumentStateStore(self.store).read()
        with patch.object(self.store, "save", side_effect=OSError("disk full")):
            with self.assertRaises(ai.PersistenceError) as raised:
                svc.record_concern(LIAISON, body("req-0000005"))
        self.assertNotIsInstance(raised.exception, UnconfirmedWriteError)
        self.assertIn("Nothing was saved", str(raised.exception))
        self.assertEqual(DocumentStateStore(self.store).read(), before)
        self.assertEqual(self.count(self.open_store()), 1)
        receipt, replay = svc.record_concern(LIAISON, body("req-0000005"))
        self.assertFalse(replay)
        self.assertEqual(self.count(), 2)
        self.assertTrue(receipt["receipt_id"])

    def test_committed_then_error_is_unconfirmed_and_same_id_reconciles(self) -> None:
        svc = self.service()
        real = self.store.save

        def save_then_fail() -> None:
            real()
            raise OSError("late failure after commit")

        with patch.object(self.store, "save", side_effect=save_then_fail):
            with self.assertRaises(UnconfirmedWriteError) as raised:
                svc.record_concern(LIAISON, body("req-0000006"))
        self.assertIsInstance(raised.exception.__cause__, OSError)
        self.assertIn("same request reference", str(raised.exception))
        self.assertNotIn("Nothing was saved", str(raised.exception))
        self.assertEqual(self.count(self.open_store()), 1)
        _, replay = svc.record_concern(LIAISON, body("req-0000006"))
        self.assertTrue(replay)
        self.assertEqual(self.count(), 1)

    def test_mutator_runs_once_and_is_not_rerun_after_an_error(self) -> None:
        calls: list[str | None] = []
        adapter = DocumentStateStore(self.store)

        def mutator(text: str | None) -> tuple[str, int]:
            calls.append(text)
            return json.dumps({"n": len(calls)}), 1

        with patch.object(self.store, "save", side_effect=OSError("x")):
            with self.assertRaises(ai.PersistenceError):
                adapter.update(mutator)
        self.assertEqual(len(calls), 1)

    def test_mutator_error_propagates_unchanged(self) -> None:
        def mutator(text: str | None) -> tuple[str, int]:
            raise ValueError("refused")

        with self.assertRaises(ValueError):
            DocumentStateStore(self.store).update(mutator)
        self.assertIsNone(DocumentStateStore(self.store).read())

    def test_unreadable_persisted_value_is_unconfirmed_not_not_saved(self) -> None:
        adapter = DocumentStateStore(self.store)
        real = self.store.save

        def save_then_fail() -> None:
            real()
            raise OSError("late")

        with (
            patch.object(self.store, "save", side_effect=save_then_fail),
            patch.object(DocumentStateStore, "_persisted", side_effect=RuntimeError("reload down")),
        ):
            with self.assertRaises(UnconfirmedWriteError) as raised:
                adapter.update(lambda text: (json.dumps({"v": 1}), None))
        self.assertIsInstance(raised.exception.__cause__, RuntimeError)
        self.assertIn("OSError", " ".join(getattr(raised.exception, "__notes__", [])))

    def seed(self, count: int) -> None:
        """Store `count` valid concerns by cloning the first one, as a restart would find them."""
        self.service().record_concern(LIAISON, body("req-0000001"))
        adapter = DocumentStateStore(self.store)
        doc = json.loads(adapter.read() or "{}")
        concern, receipt = doc["register"]["concerns"]["AC-001"], doc["receipts"]["AC-001"]
        request = doc["requests"]["req-0000001"]
        for n in range(2, count + 1):
            cid, rid = f"AC-{n:03d}", f"req-{n:07d}"
            doc["register"]["concerns"][cid] = {**copy.deepcopy(concern), "id": cid}
            doc["receipts"][cid] = {
                **copy.deepcopy(receipt),
                "concern_id": cid,
                "receipt_id": f"RC-{cid}",
                "request_id": rid,
            }
            doc["requests"][rid] = {**request, "concern_id": cid}
        adapter.update(lambda _: (json.dumps(doc, sort_keys=True), None))

    def assert_listed(self, store: Any, count: int) -> None:
        ids = list(ai._register(self.service(store)._load()).concerns)
        self.assertEqual(ids, [f"AC-{n:03d}" for n in range(1, count + 1)])

    def test_register_at_1000_reads_after_restart(self) -> None:
        self.seed(1000)
        reopened = self.open_store()
        self.assert_listed(reopened, 1000)
        self.assertEqual(self.count(reopened), 1000)

    def test_writes_across_999_1000_1001_survive_restart_and_replay(self) -> None:
        self.seed(999)
        self.assert_listed(self.open_store(), 999)
        for n in (1000, 1001):
            receipt, replay = self.service().record_concern(LIAISON, body(f"req-{n:07d}"))
            self.assertFalse(replay)
            self.assertEqual(receipt["concern_id"], f"AC-{n:03d}")
            reopened = self.open_store()
            self.assert_listed(reopened, n)
            again, replay = self.service(reopened).record_concern(LIAISON, body(f"req-{n:07d}"))
            self.assertTrue(replay)
            self.assertEqual(again["receipt_id"], receipt["receipt_id"])
        self.assertEqual(self.count(self.open_store()), 1001)


class JsonStoreAdapter(Contract, unittest.TestCase):
    def open_store(self) -> Any:
        return Store(str(self.path))

    def test_failed_save_recovery_cannot_restore_over_another_threads_committed_write(self) -> None:
        a_read, release = threading.Event(), threading.Event()
        real_persisted = DocumentStateStore._persisted
        real_save = self.store.save
        outcome: dict[str, Any] = {}

        def paused(adapter: DocumentStateStore) -> str | None:
            value = real_persisted(adapter)
            if threading.current_thread().name == "A":
                a_read.set()
                self.assertTrue(release.wait(10))
            return value

        def save(*_: Any) -> None:
            if threading.current_thread().name == "A":
                raise OSError("A disk full")
            real_save()

        def run(name: str, request_id: str, text: str) -> None:
            try:
                outcome[name] = self.service().record_concern(LIAISON, body(request_id, text))
            except Exception as error:
                outcome[name] = error

        a = threading.Thread(target=run, name="A", args=("A", "req-00000a01", "A statement."))
        b = threading.Thread(target=run, name="B", args=("B", "req-00000b01", "B statement."))
        with (
            patch.object(DocumentStateStore, "_persisted", paused),
            patch.object(self.store, "save", save),
        ):
            a.start()
            self.assertTrue(a_read.wait(10))
            held_elsewhere = not self.store.lock.acquire(blocking=False)
            if not held_elsewhere:
                self.store.lock.release()
            b.start()
            b.join(1)
            release.set()
            a.join(10)
            b.join(10)
        self.assertTrue(held_elsewhere, "recovery must keep the store lock until it has restored")
        self.assertIsInstance(outcome["A"], ai.PersistenceError)
        self.assertNotIsInstance(outcome["A"], UnconfirmedWriteError)
        self.assertIn("Nothing was saved", str(outcome["A"]))
        receipt, replay = outcome["B"]
        self.assertFalse(replay)

        def requests(store: Any) -> set[str]:
            return set(json.loads(DocumentStateStore(store).read() or "{}")["requests"])

        self.assertEqual(requests(self.store), {"req-00000b01"})
        self.assertEqual(requests(self.open_store()), {"req-00000b01"})
        self.service().record_concern(LIAISON, body("req-00000c01", "C statement."))
        self.assertEqual(requests(self.open_store()), {"req-00000b01", "req-00000c01"})
        again, replayed = self.service().record_concern(
            LIAISON, body("req-00000b01", "B statement.")
        )
        self.assertTrue(replayed)
        self.assertEqual(again["receipt_id"], receipt["receipt_id"])
        self.service().record_concern(LIAISON, body("req-00000a01", "A statement."))
        self.assertEqual(self.count(self.open_store()), 3)


class SqliteAdapter(Contract, unittest.TestCase):
    def open_store(self) -> Any:
        store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(store.db.close)
        return store

    def test_lock_exit_failure_after_commit_is_unconfirmed(self) -> None:
        svc = self.service()
        with patch.object(self.store, "_finish", side_effect=RuntimeError("finish failed")):
            with self.assertRaises(UnconfirmedWriteError):
                svc.record_concern(LIAISON, body("req-0000007"))
        _, replay = svc.record_concern(LIAISON, body("req-0000007"))
        self.assertTrue(replay)
        self.assertEqual(self.count(self.open_store()), 1)

    def test_two_writers_keep_both_receipts(self) -> None:
        other = self.open_store()
        self.service().record_concern(LIAISON, body("req-0000008"))
        self.service(other).record_concern(
            LIAISON, body("req-0000009", "Damp patch by the window.")
        )
        self.assertEqual(self.count(self.open_store()), 2)

    def test_interleaved_writer_is_a_conflict_and_never_overwritten(self) -> None:
        other = self.open_store()
        winner = self.service(other)
        adapter = DocumentStateStore(self.store)
        real_update = adapter.update
        fired: list[bool] = []

        def racing(mutator: Any) -> Any:
            def wrapped(text: str | None) -> Any:
                if not fired:
                    fired.append(True)
                    winner.record_concern(LIAISON, body("req-0000010", "Winner statement."))
                return mutator(text)

            return real_update(wrapped)

        loser = ai.AftercareService(adapter, homes=HOMES, now=lambda: NOW)
        with patch.object(adapter, "update", side_effect=racing):
            with self.assertRaises(ai.ConflictError):
                loser.record_concern(LIAISON, body("req-0000011", "Loser statement."))
        reopened = self.open_store()
        self.assertEqual(self.count(reopened), 1)
        loser.record_concern(LIAISON, body("req-0000011", "Loser statement."))
        self.assertEqual(self.count(self.open_store()), 2)

    def test_only_the_aftercare_document_is_added_to_the_meta_documents(self) -> None:
        self.service().record_concern(LIAISON, body("req-0000012"))
        keys = {r[0] for r in self.store.db.execute("SELECT key FROM meta").fetchall()}
        self.assertIn("aftercare", keys)
        self.assertNotIn("aftercare_requests", keys)


@unittest.skipUnless(os.environ.get("ZF_RESIDENT_MSSQL") == "1", "opt-in owned loopback SQL Server")
class MssqlAdapter(SqliteAdapter):
    """The same contract on the task-owned disposable SQL Server, one database per test."""

    def setUp(self) -> None:
        require_task_owned_loopback(os.environ)
        from zava_forward.core.mssqlstore import _Conn, connection_string

        database = "zf_aftercare133_" + uuid.uuid4().hex
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

    def open_store(self) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store


if __name__ == "__main__":
    unittest.main()
