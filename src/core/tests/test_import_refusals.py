"""Durable refused-import projection: failed saves, audit truth, idempotent retry (#135 C4)."""

import copy
import importlib
import json
import os
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core import import_refusals, sqlstore
from zava_forward.core import store as store_module
from zava_forward.core.sqlstore import CommittedReloadError
from zava_forward.core.store import ConflictError

ACTION = "recorded_import_refusals"


def refusal(n: int = 1) -> dict[str, str]:
    return {
        "source_name": f"synthetic-{n}.xlsx",
        "source_sha256": f"{n:064x}",
        "reason": "Refused: the file is not a valid .xlsx workbook.",
        "at": "2026-11-10T01:02:03Z",
    }


class Projection(unittest.TestCase):
    backend = "json"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        self.path.write_text(json.dumps(copy.deepcopy(DATA)))
        self.prepare()
        self.store = self.reopen()

    def prepare(self) -> None:
        return None

    def reopen(self) -> Any:
        if self.backend == "sqlite":
            store: Any = vars(sqlstore)["SqlStore"](
                str(self.path), str(self.path.with_suffix(".sqlite"))
            )
            self.addCleanup(store.db.close)
            return store
        return vars(store_module)["Store"](
            str(self.path),
            str(Path(self.tmp.name) / "live.json"),
            str(Path(self.tmp.name) / "audit.jsonl"),
        )

    def events(self, store: Any = None) -> list[dict[str, str]]:
        return [e for e in (store or self.store).audit_entries() if e["action"] == ACTION]

    def stored(self, store: Any = None) -> list[dict[str, str]]:
        return import_refusals.load((store or self.store).data) or []

    def break_the_write(self) -> Any:
        """Make the document write fail before commit, the way each store can."""
        if self.backend == "json":
            return patch.object(self.store, "save", side_effect=OSError("injected save failure"))
        return patch.object(
            self.store, "_append_audit", side_effect=sqlite3.OperationalError("injected")
        )

    def test_failed_save_leaves_nothing_and_retry_persists_once(self) -> None:
        self.store.save()
        with self.break_the_write(), self.assertRaises((OSError, sqlite3.Error)):
            self.store.record_import_refusals([refusal()])
        self.assertIsNone(self.store.data.get(import_refusals.KEY))
        self.assertEqual(self.events(), [])
        self.assertEqual(self.stored(self.reopen()), [])
        self.assertEqual(self.store.record_import_refusals([refusal()])["added"], 1)
        reopened = self.reopen()
        self.assertEqual(self.stored(reopened), [refusal()])
        self.assertEqual(len(self.events(reopened)), 1)

    def test_failed_save_restores_the_previous_document(self) -> None:
        self.store.record_import_refusals([refusal(1)])
        with self.break_the_write(), self.assertRaises((OSError, sqlite3.Error)):
            self.store.record_import_refusals([refusal(2)])
        self.assertEqual(self.stored(), [refusal(1)])
        self.assertEqual(len(self.events()), 1)
        self.assertEqual(self.store.record_import_refusals([refusal(2)])["added"], 1)
        self.assertEqual(len(self.stored(self.reopen())), 2)

    def test_repeat_and_batch_limit(self) -> None:
        self.assertEqual(self.store.record_import_refusals([refusal(), refusal()])["added"], 1)
        again = self.store.record_import_refusals([refusal()])
        self.assertEqual((again["added"], again["already_present"]), (0, 1))
        self.assertEqual(len(self.events()), 1)
        many = [refusal(n) for n in range(2, import_refusals.MAX_REFUSALS + 1)]
        self.assertEqual(self.store.record_import_refusals(many)["total"], 500)
        with self.assertRaisesRegex(ValueError, "nothing was recorded"):
            self.store.record_import_refusals([refusal(501)])
        self.assertEqual(len(self.stored(self.reopen())), 500)


class JsonProjection(Projection):
    def test_audit_failure_after_a_durable_save_is_partial_not_nothing(self) -> None:
        with (
            patch.object(self.store, "audit", side_effect=OSError("injected audit failure")),
            self.assertRaises(import_refusals.PartiallyRecordedError),
        ):
            self.store.record_import_refusals([refusal()])
        self.assertEqual(self.stored(self.reopen()), [refusal()])
        self.assertEqual(self.events(), [])
        self.assertEqual(self.store.record_import_refusals([refusal()])["already_present"], 1)


class SqlProjection(Projection):
    backend = "sqlite"

    def committed_but_unconfirmed(self) -> None:
        original = self.store.save

        def ack_failure() -> None:
            original()
            raise CommittedReloadError("refresh did not settle")

        with (
            patch.object(self.store, "save", side_effect=ack_failure),
            self.assertRaises(CommittedReloadError),
        ):
            self.store.record_import_refusals([refusal()])

    def test_committed_reload_failure_keeps_the_committed_record_and_audit(self) -> None:
        self.committed_but_unconfirmed()
        reopened = self.reopen()
        self.assertEqual(self.stored(reopened), [refusal()])
        self.assertEqual(len(self.events(reopened)), 1)
        self.assertEqual(self.reopen().record_import_refusals([refusal()])["added"], 0)

    def test_prior_pending_audit_survives_a_failed_write_exactly_once(self) -> None:
        with self.store.lock:
            self.store.audit("SYN", "SYN_prior_pending", "-", "kept")
            with self.break_the_write(), self.assertRaises(sqlite3.Error):
                self.store.record_import_refusals([refusal()])
        actions = [e["action"] for e in self.reopen().audit_entries()]
        self.assertEqual(actions.count("SYN_prior_pending"), 1)
        self.assertNotIn(ACTION, actions)

    def test_conflicting_writer_is_refused_and_leaves_nothing(self) -> None:
        other = self.reopen()
        original = self.store.save

        def compete() -> None:
            other.record_import_refusals([refusal(9)])
            original()

        with (
            patch.object(self.store, "save", side_effect=compete),
            self.assertRaises(ConflictError),
        ):
            self.store.record_import_refusals([refusal(1)])
        self.assertEqual(self.stored(self.reopen()), [refusal(9)])
        self.assertEqual(len(self.events(self.reopen())), 1)
        self.assertEqual(self.store.record_import_refusals([refusal(1)])["added"], 1)

    def trigger_sql(self, action: str) -> str:
        return (
            f"CREATE TRIGGER reject_refusals_{action.lower()} BEFORE {action} ON meta "
            "WHEN NEW.key = 'import_exceptions' "
            "BEGIN SELECT RAISE(ABORT, 'injected projection write failure'); END"
        )

    def test_real_rejected_meta_write_rolls_back_and_retries(self) -> None:
        for action in ("INSERT", "UPDATE"):
            self.store.db.execute(self.trigger_sql(action))
        with self.assertRaises(sqlite3.Error):
            self.store.record_import_refusals([refusal()])
        self.assertIsNone(self.store.data.get(import_refusals.KEY))
        self.assertEqual(self.events(), [])
        for action in ("insert", "update"):
            self.store.db.execute(f"DROP TRIGGER reject_refusals_{action}")
        self.assertEqual(self.store.record_import_refusals([refusal()])["added"], 1)
        reopened = self.reopen()
        self.assertEqual(self.stored(reopened), [refusal()])
        self.assertEqual(len(self.events(reopened)), 1)


@unittest.skipUnless(os.environ.get("ZF_IMPORT135_MSSQL") == "1", "opt-in task-owned loopback SQL")
class MssqlProjection(SqlProjection):
    backend = "mssql"

    def prepare(self) -> None:
        from sqlguard import require_task_owned_loopback
        from zava_forward.core import mssqlstore

        require_task_owned_loopback(os.environ)
        env = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        env.start()
        self.addCleanup(env.stop)
        self.admin: Any = vars(mssqlstore)["_Conn"](vars(mssqlstore)["connection_string"]())
        self.addCleanup(self.admin.close)
        self.database = "zf_import135_" + uuid.uuid4().hex
        self.admin.execute(f"CREATE DATABASE [{self.database}]")
        self.addCleanup(self.drop_database)
        os.environ["ZF_SQL_DATABASE"] = self.database

    def drop_database(self) -> None:
        self.admin.execute(
            f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
        )
        self.admin.execute(f"DROP DATABASE [{self.database}]")

    def reopen(self) -> Any:
        mssql: Any = vars(importlib.import_module("zava_forward.core.mssqlstore"))["MssqlStore"]
        store: Any = mssql(str(self.path), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store

    def trigger_sql(self, action: str) -> str:
        return (
            f"CREATE TRIGGER reject_refusals_{action.lower()} ON meta AFTER {action} AS "
            "IF EXISTS (SELECT 1 FROM inserted WHERE [key] = 'import_exceptions') "
            "THROW 50001, 'injected projection write failure', 1"
        )

    def test_real_rejected_meta_write_rolls_back_and_retries(self) -> None:
        from zava_forward.core.mssqlstore import MssqlStore

        store = self.store
        assert isinstance(store, MssqlStore)
        for action in ("INSERT", "UPDATE"):
            store.db.execute(self.trigger_sql(action))
        with self.assertRaises(store.dberror):
            store.record_import_refusals([refusal()])
        self.assertIsNone(store.data.get(import_refusals.KEY))
        self.assertEqual(self.events(), [])
        for action in ("insert", "update"):
            store.db.execute(f"DROP TRIGGER reject_refusals_{action}")
        self.assertEqual(store.record_import_refusals([refusal()])["added"], 1)
        reopened = self.reopen()
        self.assertEqual(self.stored(reopened), [refusal()])
        self.assertEqual(len(self.events(reopened)), 1)


if __name__ == "__main__":
    unittest.main()
