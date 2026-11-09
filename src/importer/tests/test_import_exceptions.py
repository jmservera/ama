import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from zava_forward.core.exception_queue import ExceptionQueue

from zava_forward.importer import exceptions as ex
from zava_forward.importer.exceptions import RefusalLedger, feed_inputs, route, submit_file
from zava_forward.importer.quarantine import ImportError_, QuarantineStore
from zava_forward.importer.xlsx import write_workbook

STEWARD = "synthetic.steward@example.test"
GOOD = [
    ["Ref", "Property Address", "Post code", "Stage", "Owner"],
    ["ZF-1", "1 Synthetic Row", "AB1 2CD", "Survey", "Sam"],
]
NO_REF = [["Property Address", "Post code", "Stage"], ["9 Secret Row", "AB1 2CD", "Survey"]]
DUPES = [GOOD[0], GOOD[1], ["ZF-1", "7 Dupe Row", "AB1 2CE", "Design", "Alex"]]
HOSTILE_HEADER = [
    ["Ref", "Ref", "Post code SECRET-HEADER", "Stage"],
    ["ZF-1", "ZF-2", "AB1 2CD", "Survey"],
]


def must[T](value: T | None) -> T:
    assert value is not None
    return value


def queue_for(owner: str | None = STEWARD) -> ExceptionQueue:
    return ExceptionQueue({owner: ["data_steward"]} if owner else {})


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.db = self.tmp / "import.db"
        self.open()
        self.addCleanup(self.conn.close)

    def open(self) -> None:
        fresh = not self.db.exists()
        self.conn = sqlite3.connect(self.db)
        self.store, self.ledger = QuarantineStore(self.conn), RefusalLedger(self.conn)
        if fresh:
            self.store.create_schema()
            self.ledger.create_schema()

    def source(
        self, name: str, rows: list[list[str]] | None = None, raw: bytes | None = None
    ) -> Path:
        path = self.tmp / name
        path.write_bytes(raw if raw is not None else write_workbook({"Cases": rows or GOOD}))
        return path

    def snapshot(self, path: Path) -> tuple[str, int, int]:
        st = path.stat()
        return hashlib.sha256(path.read_bytes()).hexdigest(), st.st_size, st.st_mtime_ns


class ProducerTests(Base):
    def test_refused_file_is_durable_and_source_unchanged(self) -> None:
        path = self.source("bad.xlsx", raw=b"not a workbook")
        before = self.snapshot(path)
        result = submit_file(self.store, self.ledger, path, "Pat Importer")
        self.assertIsNone(result.batch)
        self.assertEqual(self.snapshot(path), before)
        self.assertEqual(must(result.refusal).source_sha256, before[0])
        self.assertEqual(must(result.refusal).data_label, "synthetic-demo")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM import_batches").fetchone()[0], 0)

    def test_clean_file_stages_and_records_no_refusal(self) -> None:
        result = submit_file(self.store, self.ledger, self.source("ok.xlsx"), "Pat Importer")
        self.assertEqual(must(result.batch).status, "staged")
        self.assertEqual(self.ledger.all(), [])

    def test_repeat_refusal_is_one_row_and_keeps_first_reason(self) -> None:
        path = self.source("bad.xlsx", raw=b"not a workbook")
        first = must(submit_file(self.store, self.ledger, path, "Pat").refusal)
        again = must(submit_file(self.store, self.ledger, path, "Someone Else").refusal)
        self.assertEqual(first, again)
        self.assertEqual(len(self.ledger.all()), 1)

    def test_same_content_under_two_names_is_one_ref_like_the_feed(self) -> None:
        a = must(
            submit_file(self.store, self.ledger, self.source("a.xlsx", raw=b"junk"), "Pat").refusal
        )
        b = must(
            submit_file(self.store, self.ledger, self.source("b.xlsx", raw=b"junk"), "Pat").refusal
        )
        self.assertEqual(a.ref, b.ref)
        self.assertEqual(len(self.ledger.all()), 1)

    def test_blocking_mapping_is_refused_without_row_or_header_text(self) -> None:
        for name, rows in (
            ("noref.xlsx", NO_REF),
            ("dupes.xlsx", DUPES),
            ("hdr.xlsx", HOSTILE_HEADER),
        ):
            result = submit_file(self.store, self.ledger, self.source(name, rows), "Pat")
            self.assertIsNone(result.batch, name)
            for secret in ("Secret Row", "Dupe Row", "SECRET-HEADER", "ZF-1", "ZF-2"):
                self.assertNotIn(secret, must(result.refusal).reason, name)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM import_batches").fetchone()[0], 0)
        reasons = " ".join(r.reason for r in self.ledger.all())
        self.assertIn("required column missing: reference", reasons)
        self.assertIn("duplicate key values", reasons)

    def test_oversized_file_is_refused_and_not_hashed(self) -> None:
        path = self.source("big.xlsx")
        with (
            mock.patch.object(ex, "MAX_SOURCE_BYTES", 10),
            mock.patch("zava_forward.importer.mapping.MAX_SOURCE_BYTES", 10),
        ):
            result = submit_file(self.store, self.ledger, path, "Pat")
        self.assertEqual(must(result.refusal).source_sha256, "")
        self.assertEqual(must(result.refusal).ref, "file:big.xlsx")
        self.assertIn("larger than the import limit", must(result.refusal).reason)

    def test_missing_file_is_a_refusal_not_a_crash(self) -> None:
        result = submit_file(self.store, self.ledger, self.tmp / "gone.xlsx", "Pat")
        self.assertIn("could not be read", must(result.refusal).reason)

    def test_blank_stager_is_an_error_not_a_refusal(self) -> None:
        with self.assertRaises(ImportError_):
            submit_file(self.store, self.ledger, self.source("x.xlsx", raw=b"x"), " ")
        self.assertEqual(self.ledger.all(), [])

    def test_insert_race_returns_the_existing_row(self) -> None:
        winner = RefusalLedger(sqlite3.connect(self.db))
        real_get = self.ledger._get
        calls: list[str] = []

        def racing_get(ref: str):  # type: ignore[no-untyped-def]
            calls.append(ref)
            if len(calls) == 1:
                winner.record("race.xlsx", "d" * 64, "case-list", "Refused: first.", "Pat")
                return None
            return real_get(ref)

        with mock.patch.object(self.ledger, "_get", racing_get):
            got = self.ledger.record("race.xlsx", "d" * 64, "case-list", "Refused: second.", "Sam")
        self.assertEqual(got.reason, "Refused: first.")
        self.assertEqual(len(self.ledger.all()), 1)


class RoutingTests(Base):
    def refuse(self, name: str = "bad.xlsx", raw: bytes = b"not a workbook") -> None:
        submit_file(self.store, self.ledger, self.source(name, raw=raw), "Pat")

    def test_refusal_becomes_steward_item_with_original_source_and_unknown_eligibility(
        self,
    ) -> None:
        self.refuse()
        queue = queue_for()
        routing = route(queue, self.store, self.ledger, STEWARD)
        (item,) = queue.queue(STEWARD)
        self.assertEqual(item["kind"], "failed_import")
        self.assertEqual(item["owner"], STEWARD)
        self.assertEqual(item["owner_role"], "data_steward")
        self.assertEqual(item["eligibility"], "Unknown")
        self.assertEqual(item["status"], "open")
        self.assertIsNone(item["recovery"])
        stored = self.ledger.all()[0]
        self.assertEqual(item["original_source"]["source_name"], "bad.xlsx")
        self.assertEqual(item["original_source"]["source_sha256"], stored.source_sha256)
        self.assertEqual(item["error"], stored.reason)
        self.assertEqual(item["ref"], stored.ref)
        self.assertIn("synthetic", routing.owner_label)
        self.assertEqual(routing.structures[stored.ref], "case-list")
        self.assertEqual(routing.data_label, "synthetic-demo")

    def test_rejected_batch_keeps_ids_reason_and_no_row_values(self) -> None:
        batch = must(submit_file(self.store, self.ledger, self.source("ok.xlsx"), "Pat").batch)
        self.store.reject(batch.batch_id, "Reviewer Rae", "Wrong stage list for this programme")
        queue = queue_for()
        route(queue, self.store, self.ledger, STEWARD)
        (item,) = queue.queue(STEWARD)
        self.assertEqual(item["ref"], f"batch:{batch.batch_id}")
        self.assertEqual(item["original_source"]["batch_id"], batch.batch_id)
        self.assertEqual(item["original_source"]["version"], 1)
        self.assertEqual(item["original_source"]["source_sha256"], batch.source_sha256)
        self.assertIn("Wrong stage list", item["error"])
        self.assertNotIn("Synthetic Row", json.dumps(item))
        self.assertEqual(self.store.rows(batch.batch_id)[0]["reference"], "ZF-1")

    def test_staged_and_approved_batches_raise_nothing(self) -> None:
        batch = must(submit_file(self.store, self.ledger, self.source("ok.xlsx"), "Pat").batch)
        self.store.approve(batch.batch_id, "Reviewer Rae")
        queue = queue_for()
        self.assertEqual(route(queue, self.store, self.ledger, STEWARD).items, [])
        self.assertEqual(queue.queue(STEWARD), [])

    def test_routing_twice_does_not_duplicate(self) -> None:
        self.refuse()
        queue = queue_for()
        route(queue, self.store, self.ledger, STEWARD)
        route(queue, self.store, self.ledger, STEWARD)
        self.assertEqual(len(queue.queue(STEWARD)), 1)

    def test_restart_rebuilds_the_same_items_from_the_file_database(self) -> None:
        self.refuse("a.xlsx", b"junk-a")
        batch = must(submit_file(self.store, self.ledger, self.source("ok.xlsx"), "Pat").batch)
        self.store.reject(batch.batch_id, "Reviewer Rae", "Not this one")
        first = queue_for()
        route(first, self.store, self.ledger, STEWARD)
        before = first.queue(STEWARD)
        self.conn.close()
        self.open()
        second = queue_for()
        route(second, self.store, self.ledger, STEWARD)
        self.assertEqual(second.queue(STEWARD), before)
        self.assertEqual(len(before), 2)

    def test_unassigned_owner_is_reported_not_hidden_or_invented(self) -> None:
        self.refuse()
        queue = queue_for(None)
        routing = route(queue, self.store, self.ledger, None)
        self.assertEqual(routing.items, [])
        self.assertEqual(routing.owner_label, "Unassigned (Unknown)")
        self.assertIn("1 failed import(s) are recorded", routing.unrouted[0])
        self.assertEqual(len(self.ledger.all()), 1)

    def test_non_steward_owner_is_unassigned(self) -> None:
        self.refuse()
        queue = ExceptionQueue({"op@example.test": ["digital_operator"]})
        routing = route(queue, self.store, self.ledger, "op@example.test")
        self.assertEqual(routing.items, [])
        self.assertEqual(routing.owner_label, "Unassigned (Unknown)")
        self.assertTrue(routing.unrouted)

    def test_role_scope_operator_and_unnamed_cannot_see_the_item(self) -> None:
        self.refuse()
        queue = ExceptionQueue({STEWARD: ["data_steward"], "op@example.test": ["digital_operator"]})
        route(queue, self.store, self.ledger, STEWARD)
        self.assertEqual(queue.queue("op@example.test"), [])
        with self.assertRaises(PermissionError):
            queue.queue("stranger@example.test")

    def test_routing_reads_only(self) -> None:
        self.refuse()
        self.conn.commit()
        changes = self.conn.total_changes
        digest = hashlib.sha256(self.db.read_bytes()).hexdigest()
        route(queue_for(), self.store, self.ledger, STEWARD)
        feed_inputs(self.store, self.ledger)
        self.assertEqual(self.conn.total_changes, changes)
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).hexdigest(), digest)


class CliTests(unittest.TestCase):
    def run_cli(self, *args: str, staff: dict[str, list[str]] | None = None):  # type: ignore[no-untyped-def]
        env = {k: v for k, v in os.environ.items() if k != "ZF_EXCEPTION_STAFF"}
        if staff is not None:
            env["ZF_EXCEPTION_STAFF"] = json.dumps(staff)
        return subprocess.run(
            [sys.executable, "-m", "zava_forward.importer", *args],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def test_refusal_survives_process_restart_and_view_is_read_only(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        bad, db = tmp / "bad.xlsx", tmp / "import.db"
        bad.write_bytes(b"not a workbook")
        digest = hashlib.sha256(bad.read_bytes()).hexdigest()
        staged = self.run_cli("stage", str(bad), "--db", str(db), "--staged-by", "Pat")
        self.assertEqual(staged.returncode, 1, staged.stderr)
        self.assertEqual(hashlib.sha256(bad.read_bytes()).hexdigest(), digest)
        self.assertEqual(
            self.run_cli("stage", str(bad), "--db", str(db), "--staged-by", "Pat").returncode, 1
        )
        db_before = hashlib.sha256(db.read_bytes()).hexdigest()
        staff = {STEWARD: ["data_steward"]}
        shown = self.run_cli("exceptions", str(db), staff=staff)
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertIn("items=1", shown.stdout)
        self.assertIn(f"sha256={digest}", shown.stdout)
        self.assertIn("eligibility=Unknown", shown.stdout)
        self.assertIn("configured synthetic demo steward", shown.stdout)
        self.assertEqual(hashlib.sha256(db.read_bytes()).hexdigest(), db_before)
        unowned = self.run_cli("exceptions", str(db))
        self.assertIn("UNROUTED", unowned.stdout)
        self.assertIn("items=0", unowned.stdout)
        self.assertEqual(hashlib.sha256(db.read_bytes()).hexdigest(), db_before)

    def test_missing_database_is_an_error(self) -> None:
        self.assertEqual(self.run_cli("exceptions", "/nonexistent/x.db").returncode, 2)


if __name__ == "__main__":
    unittest.main()
