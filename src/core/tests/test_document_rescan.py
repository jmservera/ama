"""Synthetic rescan paging, SQL races and recovery; no scanner activation."""

from __future__ import annotations

import copy
import json
import os
import tempfile
import threading
import unittest
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core import document_rescan
from zava_forward.core.change_provenance import CommittedOutcomeError
from zava_forward.core.doc_controls import (
    DEFENDER_TAG,
    DefenderForStorageScanner,
    DocumentUnavailable,
)
from zava_forward.core.documents import AzureBlobDocumentStore, DocumentStoreError
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store


def seed(path: Path) -> None:
    data = copy.deepcopy(DATA)
    for case in data["cases"]:
        case["documents"] = []
    for index in range(3):
        data["cases"][0]["documents"].append(
            dict(
                id=f"d{index}",
                name="SYN_PRIVATE_NAME.txt",
                mime="text/plain",
                kind="Other",
                generated=False,
                scan={"status": "pending"},
            )
        )
    data["cases"][0]["legal_hold"] = {"active": True, "reference": "SYN-HOLD"}
    path.write_text(json.dumps(data))


class SqliteRescan(unittest.TestCase):
    backend = "sqlite"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        seed(self.path)
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import _Conn, connection_string

            if os.environ.get("ZF_SQL_SERVER") not in ("127.0.0.1", "localhost"):
                raise RuntimeError("Task-owned loopback SQL required.")
            env = patch.dict(os.environ, ZF_SQL_DATABASE="master")
            env.start()
            self.addCleanup(env.stop)
            connection: Any = _Conn
            config: Any = connection_string
            self.admin = connection(config())
            self.database = "zf_rescan117_" + uuid.uuid4().hex
            self.admin.execute(f"CREATE DATABASE [{self.database}]")
            self.addCleanup(self.drop_database)
            os.environ["ZF_SQL_DATABASE"] = self.database
        self.store = self.open_store()
        for index in range(3):
            self.store.docstore.put("ZF-1", f"d{index}", b"SYN body", "text/plain")

    def drop_database(self) -> None:
        self.admin.execute(
            f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
        )
        self.admin.execute(f"DROP DATABASE [{self.database}]")
        self.admin.close()

    def open_store(self) -> Any:
        constructor: Any = SqlStore
        if self.backend == "mssql":
            from zava_forward.core.mssqlstore import MssqlStore

            constructor = MssqlStore
            store = constructor(str(self.path), state_dir=self.tmp.name)
        else:
            store = constructor(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(store.db.close)
        return store

    def actions(self) -> list[str]:
        return [e["action"] for e in self.open_store().audit_entries()]

    def doc(self, index: int = 0) -> dict[str, Any]:
        result: dict[str, Any] = self.open_store().detail("ZF-1")["documents"][index]
        return result

    def test_bounded_pages_persist_and_repeat_skips_clean(self) -> None:
        result = document_rescan.run(self.store, limit=1)
        self.assertEqual(result["clean"], 1)
        self.assertEqual(result["checked"], 1)
        self.assertEqual(result["next_after"], ["ZF-1", "d0"])
        self.assertEqual(self.doc()["scan"]["status"], "clean")
        result = document_rescan.run(self.store, after=tuple(result["next_after"]))
        self.assertEqual(result["clean"], 2)
        self.assertIsNone(result["next_after"])
        self.assertEqual(document_rescan.run(self.store)["checked"], 0)
        self.assertEqual(self.actions(), ["document_rescanned"] * 3)
        self.assertTrue(self.open_store().verify_audit())

    def test_pending_first_does_not_starve_later_documents(self) -> None:
        def scan(cid: str, did: str, *args: Any) -> tuple[str, str]:
            return ("pending", "result unavailable") if did == "d0" else ("clean", "SYN")

        with patch.object(self.store.scanner, "scan", side_effect=scan):
            first = document_rescan.run(self.store, limit=1)
            later = document_rescan.run(self.store, after=tuple(first["next_after"]))
            self.assertEqual(first["pending"], 1)
            self.assertEqual(later["clean"], 2)
            again = document_rescan.run(self.store)
            self.assertEqual(again["pending"], 1)
            self.assertEqual(again["checked"], 1)
        self.assertEqual(self.doc()["scan"]["status"], "pending")

    def test_missing_scan_included_but_generated_and_clean_excluded(self) -> None:
        with self.store.lock:
            docs = self.store._case("ZF-1")["documents"]
            docs[0].pop("scan")
            docs[1]["generated"] = True
            docs[2]["scan"]["status"] = "clean"
            self.store.save()
        result = document_rescan.run(self.store)
        self.assertEqual(result["checked"], 1)
        self.assertEqual(result["clean"], 1)

    def test_exact_maximum_page_size(self) -> None:
        with self.store.lock:
            docs = self.store._case("ZF-1")["documents"]
            for index in range(3, 101):
                docs.append(dict(docs[0], id=f"d{index:03}"))
                self.store.docstore.put("ZF-1", f"d{index:03}", b"SYN body", "text/plain")
            self.store.save()
        first = document_rescan.run(self.store, limit=100)
        self.assertEqual(first["checked"], 100)
        self.assertEqual(first["clean"], 100)
        self.assertIsNotNone(first["next_after"])
        last = document_rescan.run(self.store, after=tuple(first["next_after"]))
        self.assertEqual(last["checked"], 1)
        self.assertIsNone(last["next_after"])

    def test_actual_defender_tag_reader_outage_and_unknown_stay_pending(self) -> None:
        constructor: Any = AzureBlobDocumentStore
        blob = constructor("https://synthetic.invalid", "docs", sas="SYN")
        scanner: Any = DefenderForStorageScanner
        self.store.scanner = scanner(blob)
        for tags in ({}, {DEFENDER_TAG: "Error"}, {DEFENDER_TAG: "Not scanned"}, None):
            with patch.object(
                blob,
                "tags",
                return_value=tags,
                side_effect=DocumentStoreError("SYN PRIVATE outage") if tags is None else None,
            ):
                result = document_rescan.run(self.store, limit=1)
            self.assertEqual(result["pending"], 1)
            self.assertEqual(result["clean"], 0)
            with self.assertRaises(DocumentUnavailable):
                self.store.require_clean(self.doc())
        with patch.object(blob, "tags", return_value={DEFENDER_TAG: "No threats found"}):
            self.assertEqual(document_rescan.run(self.store, limit=1)["clean"], 1)

    def test_bad_verdicts_never_delete_or_release_hold(self) -> None:
        for verdict in ("infected", "mismatch"):
            with self.subTest(verdict=verdict):
                with self.store.lock:
                    self.store._case("ZF-1")["documents"][0]["scan"] = {"status": "pending"}
                    self.store.save()
                before = copy.deepcopy(self.store.detail("ZF-1"))
                with (
                    patch.object(self.store.scanner, "scan", return_value=(verdict, "SYN")),
                    patch.object(self.store.docstore, "delete") as delete,
                ):
                    result = document_rescan.run(self.store, limit=1)
                self.assertEqual(result["blocked"], 1)
                delete.assert_not_called()
                self.assertEqual(self.doc()["scan"]["status"], verdict)
                self.assertEqual(self.store.docstore.get("ZF-1", "d0"), b"SYN body")
                self.assertEqual(self.store.detail("ZF-1")["legal_hold"], before["legal_hold"])
                with self.assertRaises(DocumentUnavailable):
                    self.store.get_document("ZF-1", "d0")
                with self.assertRaises(PermissionError):
                    self.store.release_legal_hold({"email": document_rescan.WORKER}, "ZF-1")
                with self.assertRaises(PermissionError):
                    self.store.approve_retention_deletion(
                        {"email": document_rescan.WORKER}, "ZF-1", "d0"
                    )
        self.assertNotIn("document_quarantined_deleted", self.actions())
        self.assertNotIn("retention_deleted", self.actions())

    def test_unknown_and_storage_outage_are_explicit_failures_and_retryable(self) -> None:
        for failure in (
            patch.object(self.store.scanner, "scan", return_value=("unknown", "SYN PRIVATE")),
            patch.object(self.store.docstore, "get", side_effect=DocumentStoreError("SYN PRIVATE")),
            patch.object(self.store.scanner, "scan", side_effect=OSError("SYN PRIVATE")),
            patch.object(self.store.scanner, "scan", side_effect=RuntimeError("SYN PRIVATE")),
        ):
            with failure, self.assertLogs(document_rescan.__name__, level="ERROR") as logs:
                result = document_rescan.run(self.store, limit=1)
            self.assertEqual(result["failed"], 1)
            self.assertEqual(result["clean"], 0)
            self.assertEqual(self.doc()["scan"]["status"], "pending")
            self.assertNotIn("SYN PRIVATE", " ".join(logs.output))
            self.assertEqual(self.actions(), [])
        with patch.object(self.store.scanner, "scan", return_value=("unknown", "SYN")):
            with self.assertRaises(RuntimeError):
                self.store.rescan_pending()
        self.assertEqual(document_rescan.run(self.store, limit=1)["clean"], 1)

    def test_malformed_results_fail_closed_without_coercion_and_page_continues(self) -> None:
        class PrivateObject:
            def __str__(self) -> str:
                raise AssertionError("SYN_PRIVATE object must not be stringified")

            def __iter__(self) -> Any:
                raise AssertionError("SYN_PRIVATE object must not be iterated")

        malformed = (
            None,
            (),
            ("clean",),
            ("clean", "SYN", "extra"),
            ["clean", "SYN"],
            {"clean": "SYN"},
            "clean",
            PrivateObject(),
            (PrivateObject(), "SYN"),
            ("clean", PrivateObject()),
            ("unknown", "SYN_PRIVATE"),
            ("clean", None),
        )
        for value in malformed:
            with (
                self.subTest(shape=type(value).__name__),
                patch.object(self.store.scanner, "scan", return_value=value),
                patch.object(self.store.docstore, "delete") as delete,
                self.assertLogs(level="ERROR") as logs,
            ):
                result = document_rescan.run(self.store, limit=1)
                self.assertEqual(result["checked"], 1)
                self.assertEqual(result["failed"], 1)
                self.assertEqual(result["clean"], 0)
                self.assertEqual(result["next_after"], ["ZF-1", "d0"])
                delete.assert_not_called()
            self.assertNotIn("SYN_PRIVATE", "\n".join(logs.output))
            self.assertNotIn("Traceback", "\n".join(logs.output))
            self.assertEqual(self.doc()["scan"]["status"], "pending")
            self.assertEqual(self.actions(), [])
            self.assertEqual(self.store.docstore.get("ZF-1", "d0"), b"SYN body")
            self.assertTrue(self.store.detail("ZF-1")["legal_hold"]["active"])
        for failure in (None, TypeError("SYN_PRIVATE_SCANNER_DIAGNOSTIC")):
            with (
                patch.object(
                    self.store.scanner,
                    "scan",
                    side_effect=[failure, ("clean", "SYN")]
                    if failure is not None
                    else [None, ("clean", "SYN")],
                ),
                self.assertLogs(level="ERROR") as logs,
            ):
                result = document_rescan.run(self.store, limit=2)
            self.assertEqual(result["failed"], 1)
            self.assertEqual(result["clean"], 1)
            self.assertEqual(result["checked"], 2)
            self.assertEqual(result["next_after"], ["ZF-1", "d1"])
            self.assertNotIn("SYN_PRIVATE", "\n".join(logs.output))
            with self.store.lock:
                self.store._case("ZF-1")["documents"][1]["scan"] = {"status": "pending"}
                self.store.save()

    def test_json_and_sql_manual_scan_and_upload_reject_malformed_result(self) -> None:
        constructor: Any = Store
        json_store = constructor(str(self.path))
        json_store.docstore.put("ZF-1", "d0", b"SYN body", "text/plain")
        for target in (json_store, self.store):
            before = copy.deepcopy(target.detail("ZF-1"))
            for value in (None, ("clean",), ["clean", "SYN"], ("clean", None)):
                with (
                    patch.object(target.scanner, "scan", return_value=value),
                    patch.object(target.docstore, "delete") as delete,
                ):
                    with self.assertRaises(RuntimeError):
                        target.rescan_document(DATA["staff"][0], "ZF-1", "d0")
                    with self.assertRaises(RuntimeError):
                        target.scan_new_document("ZF-1", "d0", "SYN.txt", b"SYN body", "text/plain")
                    delete.assert_not_called()
                self.assertEqual(target.detail("ZF-1"), before)
                self.assertEqual(list(target.audit_entries()), [])
                self.assertEqual(target.docstore.get("ZF-1", "d0"), b"SYN body")

    def test_concurrent_connections_commit_success_once(self) -> None:
        other = self.open_store()
        barrier = threading.Barrier(2)

        def scan(*args: Any) -> tuple[str, str]:
            barrier.wait(timeout=20)
            return "clean", "SYN"

        with (
            patch.object(self.store.scanner, "scan", side_effect=scan),
            patch.object(other.scanner, "scan", side_effect=scan),
            ThreadPoolExecutor(max_workers=2) as workers,
        ):
            futures = [workers.submit(document_rescan.run, s, limit=1) for s in (self.store, other)]
            results = [f.result(timeout=30) for f in futures]
        self.assertEqual(sum(r["clean"] for r in results), 1)
        self.assertEqual(sum(r["failed"] for r in results), 1)
        self.assertEqual(sum(r["committed"] for r in results), 0)
        self.assertEqual(self.actions(), ["document_rescanned"])
        self.assertEqual(document_rescan.run(other, limit=1)["clean"], 1)

    def test_stale_result_conflicts_preserve_winner_and_prior_audit(self) -> None:
        other = self.open_store()

        def competing_scan(*args: Any) -> tuple[str, str]:
            self.assertEqual(document_rescan.run(other, limit=1)["clean"], 1)
            return "pending", "SYN late result"

        with self.store.lock:
            self.store.audit("system", "SYN_prior", "ZF-1", "SYN prefix")
            with (
                patch.object(self.store.scanner, "scan", side_effect=competing_scan),
                self.assertLogs(document_rescan.__name__, level="ERROR"),
            ):
                result = document_rescan.run(self.store, limit=1)
            self.assertEqual(result["failed"], 1)
            self.assertEqual(result["committed"], 0)
        self.assertEqual(self.actions(), ["document_rescanned", "SYN_prior"])
        self.assertEqual(self.doc()["scan"]["status"], "clean")
        self.assertTrue(self.open_store().verify_audit())

    def test_failed_recovery_retains_original_conflict_and_prior_prefix(self) -> None:
        other = self.open_store()
        discard = self.store._discard
        original = ConflictError("SYN conflict")

        def broken_recovery(pending: Any = ()) -> None:
            discard(pending)
            raise OSError("SYN recovery diagnostic")

        with self.store.lock:
            self.store.audit("system", "SYN_prior", "ZF-1", "SYN prefix")
            self.store._case("ZF-1")
            self.assertEqual(document_rescan.run(other, limit=1)["clean"], 1)
            with (
                patch.object(self.store, "_discard", side_effect=broken_recovery),
                self.assertLogs(document_rescan.__name__, level="ERROR"),
            ):
                with self.assertRaises(ConflictError) as caught:
                    with document_rescan._attempt(self.store):
                        self.store.audit("system", "document_rescanned", "ZF-1", "SYN failed")
                        raise original
                self.assertIs(caught.exception, original)
                self.assertIn("Rescan recovery failed", caught.exception.__notes__[0])
        self.assertEqual(self.actions(), ["document_rescanned", "SYN_prior"])
        self.assertEqual(self.doc()["scan"]["status"], "clean")

    def test_actual_conflict_with_recovery_failure_is_not_own_commit(self) -> None:
        other = self.open_store()
        discard = self.store._discard

        def competing_scan(*args: Any) -> tuple[str, str]:
            self.assertEqual(document_rescan.run(other, limit=1)["clean"], 1)
            return "clean", "SYN stale"

        def broken_recovery(pending: Any = ()) -> None:
            discard(pending)
            raise OSError("SYN_PRIVATE_SQL_RECOVERY_DIAGNOSTIC")

        with self.store.lock:
            self.store.audit("system", "SYN_prior", "ZF-1", "SYN prefix")
            with (
                patch.object(self.store.scanner, "scan", side_effect=competing_scan),
                patch.object(self.store, "_discard", side_effect=broken_recovery),
                self.assertLogs(level="DEBUG") as logs,
            ):
                result = document_rescan.run(self.store, limit=1)
        self.assertEqual(result["failed"], 1)
        self.assertEqual(result["committed"], 0)
        self.assertEqual(self.actions(), ["document_rescanned", "SYN_prior"])
        self.assertEqual(self.doc()["scan"]["status"], "clean")
        self.assertNotIn("SYN_PRIVATE_SQL_RECOVERY_DIAGNOSTIC", "\n".join(logs.output))
        self.assertNotIn("Traceback", "\n".join(logs.output))

    def test_audit_insert_then_failure_does_not_flush_success(self) -> None:
        append = self.store._append_audit

        def broken_append(pending: Any) -> None:
            append(pending)
            raise OSError("SYN SQL outage after INSERT")

        with self.store.lock:
            self.store.audit("system", "SYN_prior", "ZF-1", "SYN prefix")
            with (
                patch.object(self.store, "_append_audit", side_effect=broken_append),
                self.assertLogs(document_rescan.__name__, level="ERROR"),
            ):
                result = document_rescan.run(self.store, limit=1)
            self.assertEqual(result["failed"], 1)
        self.assertEqual(self.actions(), ["SYN_prior"])
        self.assertEqual(self.doc()["scan"]["status"], "pending")
        self.assertEqual(document_rescan.run(self.store, limit=1)["clean"], 1)
        self.assertEqual(self.actions(), ["SYN_prior", "document_rescanned"])

    def test_own_commit_refresh_error_is_not_rejection_or_duplicate(self) -> None:
        other = self.open_store()
        sync = self.store._sync

        def scan(*args: Any) -> tuple[str, str]:
            with other.lock:
                other._case("ZF-2")["reason"] = "SYN concurrent unrelated change"
                other.save()
            return "clean", "SYN"

        def failed_refresh() -> None:
            context = getattr(self.store.local, "document_rescan", None)
            if context and context["committed"]:
                raise OSError("SYN PRIVATE refresh")
            sync()

        with self.store.lock:
            self.store.audit("system", "SYN_prior", "ZF-1", "SYN prefix")
            with (
                patch.object(self.store.scanner, "scan", side_effect=scan),
                patch.object(self.store, "_sync", side_effect=failed_refresh),
                self.assertLogs(document_rescan.__name__, level="ERROR"),
            ):
                result = document_rescan.run(self.store, limit=1)
        self.assertEqual(result["committed"], 1)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(self.actions(), ["SYN_prior", "document_rescanned"])
        self.assertEqual(self.doc()["scan"]["status"], "clean")
        self.assertEqual(document_rescan.run(self.open_store(), after=("ZF-1", "d0"))["clean"], 2)
        self.assertEqual(self.actions().count("document_rescanned"), 3)

    def test_committed_context_preserves_exception_cause(self) -> None:
        with self.store.lock:
            original = OSError("SYN acknowledgement")
            with self.assertRaises(CommittedOutcomeError) as caught:
                with document_rescan._attempt(self.store):
                    document_rescan.mark_committed(self.store)
                    raise original
            self.assertIs(caught.exception.__cause__, original)

    def test_error_immediately_after_commit_cannot_flush_audit_twice(self) -> None:
        with self.store.lock:
            self.store.audit("system", "SYN_prior", "ZF-1", "SYN prefix")
            with (
                patch("zava_forward.core.hazard.mark_committed", side_effect=OSError("SYN ack")),
                self.assertLogs(document_rescan.__name__, level="ERROR"),
            ):
                result = document_rescan.run(self.store, limit=1)
        self.assertEqual(result["committed"], 1)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(self.actions(), ["SYN_prior", "document_rescanned"])
        self.assertEqual(self.doc()["scan"]["status"], "clean")
        self.assertTrue(self.open_store().verify_audit())

    def test_entire_selected_page_skipped_still_advances_cursor(self) -> None:
        lock = self.store.lock
        entries = 0

        class RacingLock:
            def __enter__(inner: Any) -> Any:
                nonlocal entries
                entries += 1
                if entries == 2:
                    other = self.open_store()
                    self.assertEqual(document_rescan.run(other, limit=1)["clean"], 1)
                return lock.__enter__()

            def __exit__(inner: Any, *args: Any) -> Any:
                return lock.__exit__(*args)

        with patch.object(self.store, "lock", RacingLock()):
            result = document_rescan.run(self.store, limit=1)
        self.assertEqual(result["skipped"], 1)
        self.assertEqual(result["checked"], 0)
        self.assertEqual(result["next_after"], ["ZF-1", "d0"])
        self.assertEqual(document_rescan.run(self.store, after=("ZF-1", "d0"))["clean"], 2)

    def test_invalid_bounds_and_cursor_do_not_scan(self) -> None:
        limits: tuple[Any, ...] = (0, -1, 101, True, "1")
        for limit in limits:
            with self.assertRaises(ValueError):
                document_rescan.run(self.store, limit=limit)
        cursors: tuple[Any, ...] = (("", "d0"), ("ZF-1",), ["ZF-1", "d0"], ("ZF-1", None))
        for after in cursors:
            with self.assertRaises(ValueError):
                document_rescan.run(self.store, after=after)
        self.assertEqual(self.actions(), [])


@unittest.skipUnless(
    os.environ.get("ZF_DOCUMENT_RESCAN_MSSQL") == "1", "requires owned loopback SQL Server"
)
class MssqlRescan(SqliteRescan):
    backend = "mssql"


if __name__ == "__main__":
    unittest.main()
