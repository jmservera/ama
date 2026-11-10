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
from zava_forward.core.store import Store

from zava_forward.importer import exceptions as ex
from zava_forward.importer.exceptions import (
    RefusalLedger,
    feed_inputs,
    route,
    submit_file,
    transfer,
)
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
        self.assertTrue(must(result.refusal).ref.startswith("source:"))
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


class IdentityTests(Base):
    """C2: unknown content gets an honest opaque identity; a digest is never borrowed."""

    def oversized(self, path: Path) -> ex.Refusal:
        with (
            mock.patch.object(ex, "MAX_SOURCE_BYTES", 10),
            mock.patch("zava_forward.importer.mapping.MAX_SOURCE_BYTES", 10),
        ):
            return must(submit_file(self.store, self.ledger, path, "Pat").refusal)

    def test_same_basename_in_different_directories_stays_distinct(self) -> None:
        first = self.source("big.xlsx")
        other = self.tmp / "other"
        other.mkdir()
        second = other / "big.xlsx"
        second.write_bytes(first.read_bytes())
        a, b = self.oversized(first), self.oversized(second)
        self.assertNotEqual(a.ref, b.ref)
        self.assertEqual((a.source_sha256, b.source_sha256), ("", ""))
        self.assertEqual(len(self.ledger.all()), 2)
        queue = queue_for()
        route(queue, self.store, self.ledger, STEWARD)
        items = queue.queue(STEWARD)
        self.assertEqual(len(items), 2)
        self.assertEqual({i["original_source"]["source_sha256"] for i in items}, {None})
        self.assertEqual(len({i["ref"] for i in items}), 2)

    def test_replaced_oversized_file_is_a_new_refusal(self) -> None:
        path = self.source("big.xlsx")
        first = self.oversized(path)
        path.write_bytes(b"replacement content that is longer than before")
        second = self.oversized(path)
        self.assertNotEqual(first.ref, second.ref)
        self.assertEqual(len(self.ledger.all()), 2)

    def test_unchanged_oversized_file_resubmitted_is_one_row(self) -> None:
        path = self.source("big.xlsx")
        self.assertEqual(self.oversized(path), self.oversized(path))
        self.assertEqual(len(self.ledger.all()), 1)

    def test_hashless_identity_is_opaque_not_the_basename(self) -> None:
        ref = self.oversized(self.source("big.xlsx")).ref
        self.assertTrue(ref.startswith("source:"))
        self.assertNotIn("big.xlsx", ref)
        self.assertNotIn(str(self.tmp), ref)

    def test_unreadable_attempts_are_not_merged_by_name(self) -> None:
        a = must(submit_file(self.store, self.ledger, self.tmp / "gone.xlsx", "Pat").refusal)
        sub = self.tmp / "sub"
        sub.mkdir()
        b = must(submit_file(self.store, self.ledger, sub / "gone.xlsx", "Pat").refusal)
        self.assertNotEqual(a.ref, b.ref)
        self.assertEqual((a.source_sha256, b.source_sha256), ("", ""))

    def replacing_scan(self, path: Path, replacement: bytes):  # type: ignore[no-untyped-def]
        def scan(*_args: object, **_kwargs: object) -> tuple[str, str]:
            path.write_bytes(replacement)
            return "infected", "scan: infected"

        return mock.patch(
            "zava_forward.importer.mapping.LocalSignatureScanner.scan", side_effect=scan
        )

    def test_replacement_after_preview_failure_never_lends_its_digest(self) -> None:
        path = self.source("bad.xlsx", raw=b"original bytes")
        original = hashlib.sha256(b"original bytes").hexdigest()
        replacement = b"different replacement bytes"
        with self.replacing_scan(path, replacement):
            refusal = must(submit_file(self.store, self.ledger, path, "Pat").refusal)
        self.assertEqual(refusal.source_sha256, original)
        self.assertNotEqual(refusal.source_sha256, hashlib.sha256(replacement).hexdigest())

    def test_change_during_read_is_hashless_and_never_claims_replacement(self) -> None:
        path = self.source("bad.xlsx", raw=b"original bytes")
        real_open = Path.open

        def open_then_replace(self_path: Path, *args: object, **kwargs: object):  # type: ignore[no-untyped-def]
            handle = real_open(self_path, *args, **kwargs)  # type: ignore[call-overload]
            with open(self_path, "wb") as replaced:
                replaced.write(b"a replacement that is much longer than the original")
            return handle

        with mock.patch.object(Path, "open", open_then_replace):
            refusal = must(submit_file(self.store, self.ledger, path, "Pat").refusal)
        self.assertEqual(refusal.source_sha256, "")
        self.assertTrue(refusal.ref.startswith("source:"))
        self.assertIn("changed while it was being read", refusal.reason)

    def test_file_that_grows_past_the_limit_while_read_is_refused_hashless(self) -> None:
        path = self.source("grow.xlsx", raw=b"12345")
        with (
            mock.patch.object(ex, "MAX_SOURCE_BYTES", 8),
            mock.patch("zava_forward.importer.mapping.MAX_SOURCE_BYTES", 8),
            mock.patch.object(Path, "stat") as stat,
        ):
            stat.return_value = mock.Mock(st_size=5, st_mtime_ns=1, st_ino=1, st_dev=1)
            path.write_bytes(b"123456789012")
            refusal = must(submit_file(self.store, self.ledger, path, "Pat").refusal)
        self.assertEqual(refusal.source_sha256, "")
        self.assertIn("larger than the import limit", refusal.reason)


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


def served_store(root: Path) -> Store:
    seed = root / "seed.json"
    if not seed.exists():
        seed.write_text(json.dumps({"cases": [], "staff": []}))
    return Store(str(seed), str(root / "state" / "live.json"), str(root / "state" / "audit.jsonl"))


class TransferTests(Base):
    def test_refusals_reach_the_served_store_once_and_survive_restart(self) -> None:
        bad = self.source("bad.xlsx", raw=b"not a workbook")
        before = self.snapshot(bad)
        self.assertIsNotNone(submit_file(self.store, self.ledger, bad, "Pat").refusal)
        served = served_store(self.tmp)
        self.assertEqual(
            transfer(self.ledger, served), {"added": 1, "already_present": 0, "total": 1}
        )
        self.assertEqual(
            transfer(self.ledger, served), {"added": 0, "already_present": 1, "total": 1}
        )
        view = served_store(self.tmp).exception_register(
            {"email": STEWARD, "role": "Retrofit Programme Manager"}, {STEWARD: ("data_steward",)}
        )
        (item,) = [i for i in view["items"] if i["kind"] == "failed_import"]
        self.assertEqual(item["ref"], f"file:{before[0]}")
        self.assertEqual(item["original_source"]["source_sha256"], before[0])
        self.assertEqual(item["eligibility"], "Unknown")
        self.assertEqual(self.snapshot(bad), before)
        self.assertEqual(len(self.ledger.all()), 1)

    def test_hashless_refusals_stay_distinct_in_the_served_store(self) -> None:
        for folder in ("a", "b"):
            (self.tmp / folder).mkdir()
            big = self.tmp / folder / "big.xlsx"
            big.write_bytes(b"x" * 10)
            with mock.patch("zava_forward.importer.exceptions.MAX_SOURCE_BYTES", 5):
                submit_file(self.store, self.ledger, big, "Pat")
        served = served_store(self.tmp)
        self.assertEqual(transfer(self.ledger, served)["added"], 2)
        view = served.exception_register(
            {"email": STEWARD, "role": "Retrofit Programme Manager"}, {STEWARD: ("data_steward",)}
        )
        items = [i for i in view["items"] if i["kind"] == "failed_import"]
        self.assertEqual(len({i["ref"] for i in items}), 2)
        self.assertTrue(all(i["original_source"]["source_sha256"] is None for i in items))


class CliTests(unittest.TestCase):
    def run_cli(  # type: ignore[no-untyped-def]
        self,
        *args: str,
        staff: dict[str, list[str]] | None = None,
        extra: dict[str, str] | None = None,
    ):
        env = {k: v for k, v in os.environ.items() if k != "ZF_EXCEPTION_STAFF"}
        env.update(extra or {})
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

    def assert_clean_failure(self, result) -> None:  # type: ignore[no-untyped-def]
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)
        self.assertIn("Cannot", result.stderr)

    def test_stage_connection_failure_exits_2_without_traceback(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        bad = tmp / "bad.xlsx"
        bad.write_bytes(b"not a workbook")
        result = self.run_cli(
            "stage", str(bad), "--db", str(tmp / "no-such-dir" / "x.db"), "--staged-by", "Pat"
        )
        self.assert_clean_failure(result)

    def test_stage_write_failure_exits_2_not_recorded_refusal(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        bad, db = tmp / "bad.xlsx", tmp / "import.db"
        bad.write_bytes(b"not a workbook")
        conn = sqlite3.connect(db)
        QuarantineStore(conn).create_schema()
        RefusalLedger(conn).create_schema()
        conn.execute(
            "CREATE TRIGGER block BEFORE INSERT ON import_refusals "
            "BEGIN SELECT RAISE(ABORT, 'blocked'); END"
        )
        conn.commit()
        conn.close()
        result = self.run_cli("stage", str(bad), "--db", str(db), "--staged-by", "Pat")
        self.assert_clean_failure(result)
        check = sqlite3.connect(db)
        self.addCleanup(check.close)
        self.assertEqual(check.execute("SELECT COUNT(*) FROM import_refusals").fetchone()[0], 0)

    def test_viewer_on_a_non_database_exits_2_without_traceback(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        db = tmp / "junk.db"
        db.write_bytes(b"this is not a sqlite database" * 20)
        before = hashlib.sha256(db.read_bytes()).hexdigest()
        result = self.run_cli("exceptions", str(db), staff={STEWARD: ["data_steward"]})
        self.assert_clean_failure(result)
        self.assertEqual(hashlib.sha256(db.read_bytes()).hexdigest(), before)

    def test_close_failure_after_error_still_exits_2_once(self) -> None:
        import contextlib
        import io
        import runpy

        class Conn:
            def execute(self, *_a: object) -> None:
                raise sqlite3.OperationalError("boom")

            def close(self) -> None:
                raise sqlite3.ProgrammingError("close failed")

        out, err = io.StringIO(), io.StringIO()
        argv = ["x", "stage", __file__, "--db", "unused.db", "--staged-by", "Pat"]
        with (
            mock.patch.object(sys, "argv", argv),
            mock.patch.object(sqlite3, "connect", return_value=Conn()),
            contextlib.redirect_stdout(out),
            contextlib.redirect_stderr(err),
            self.assertRaises(SystemExit) as raised,
        ):
            runpy.run_module("zava_forward.importer", run_name="__main__")
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue().count("Cannot"), 1)

    def test_missing_database_is_an_error(self) -> None:
        self.assertEqual(self.run_cli("exceptions", "/nonexistent/x.db").returncode, 2)
        self.assertEqual(self.run_cli("transfer", "/nonexistent/x.db").returncode, 2)

    def test_transfer_command_is_idempotent_and_reports_a_refused_store(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        bad, db = tmp / "bad.xlsx", tmp / "import.db"
        bad.write_bytes(b"not a workbook")
        self.assertEqual(
            self.run_cli("stage", str(bad), "--db", str(db), "--staged-by", "Pat").returncode, 1
        )
        served_store(tmp)
        env = {
            "ZF_STORE": "json",
            "ZF_DATA": str(tmp / "seed.json"),
            "ZF_STATE": str(tmp / "state"),
        }
        first = self.run_cli("transfer", str(db), extra=env)
        again = self.run_cli("transfer", str(db), extra=env)
        self.assertEqual((first.returncode, again.returncode), (0, 0), first.stderr + again.stderr)
        self.assertIn("added=1", first.stdout)
        self.assertIn("added=0 already_present=1", again.stdout)
        broken = self.run_cli("transfer", str(db), extra={**env, "ZF_STORE": "nonsense"})
        self.assertEqual(broken.returncode, 2)
        self.assertEqual(broken.stdout, "")
        self.assertIn("Nothing was recorded", broken.stderr)


if __name__ == "__main__":
    unittest.main()
