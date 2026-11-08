"""Retained ranking snapshot publication (Refs #79)."""

import contextlib
import errno
import json
import multiprocessing
import os
import stat
import tempfile
import threading
import unittest
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import case
from zava_forward.core import ranking
from zava_forward.core import ranking_publication as rp

AS_OF = "2026-10-09"


def snap():
    a, b = case("ZF-A"), case("ZF-B")
    b["days_in_stage"] = 50
    return ranking.snapshot([a, b], ranking.POLICY_V1, AS_OF)


DEADLINE = 20


class CommitGate:
    """Holds registered threads just before the real publication syscall.

    The wrapper only waits, then runs the real os.link (or the earlier os.replace), so every
    filesystem result is real. Unregistered threads pass straight through.
    """

    def __init__(self, *names: str) -> None:
        self.arrived = {n: threading.Event() for n in names}
        self.go = {n: threading.Event() for n in names}
        self.done = {n: threading.Event() for n in names}
        self.results: dict[str, Any] = {}
        self.threads: list[threading.Thread] = []

    def wrap(self, real: Any) -> Any:
        def call(src: Any, dst: Any, *args: Any, **kw: Any) -> Any:
            name = threading.current_thread().name
            if name not in self.arrived:
                return real(src, dst, *args, **kw)
            self.arrived[name].set()
            if not self.go[name].wait(DEADLINE):
                raise RuntimeError(f"gate deadline for {name}")
            try:
                return real(src, dst, *args, **kw)
            finally:
                self.done[name].set()

        return call

    def start(self, name: str, fn: Any) -> None:
        def work() -> None:
            try:
                self.results[name] = fn()
            except BaseException as e:  # recorded, then asserted on by the test
                self.results[name] = e

        thread = threading.Thread(target=work, name=name)
        self.threads.append(thread)
        thread.start()

    def release(self, name: str) -> None:
        self.go[name].set()
        self.done[name].wait(DEADLINE)

    def join(self) -> None:
        for name in self.go:
            self.go[name].set()
        for thread in self.threads:
            thread.join(DEADLINE)


@contextlib.contextmanager
def gated(*names: str) -> Iterator[CommitGate]:
    gate = CommitGate(*names)
    with (
        patch.object(os, "link", gate.wrap(os.link)),
        patch.object(os, "replace", gate.wrap(os.replace)),
    ):
        try:
            yield gate
        finally:
            gate.join()


def _publish_in_process(archive: str, published_on: str, barrier: Any, out: Any) -> None:
    barrier.wait(DEADLINE)
    try:
        out.put(rp.publish(snap(), archive, published_on))
    except BaseException as e:  # reported to the parent, which fails the test
        out.put(repr(e))


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name) / "archive"

    def test_publish_is_dated_idempotent_and_verifies(self):
        first = rp.publish(snap(), self.dir, "2026-10-10")
        self.assertTrue(first["written"])
        again = rp.publish(snap(), self.dir, "2026-10-11")
        self.assertFalse(again["written"])
        self.assertEqual((again["path"], again["published_on"]), (first["path"], "2026-10-10"))
        self.assertEqual(len(list(self.dir.iterdir())), 1)
        self.assertEqual(rp.verify(self.dir), dict(count=1, problems=[], latest="2026-10-10"))

    def test_edited_record_is_reported_and_not_overwritten(self):
        path = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        rec = json.loads(path.read_text())
        rec["snapshot"]["entries"].reverse()
        path.write_text(json.dumps(rec))
        want = [f"{path.name}: content does not match its snapshot hash."]
        self.assertEqual(rp.verify(self.dir)["problems"], want)
        damaged = path.read_bytes()
        with self.assertRaises(rp.PublicationError):
            rp.publish(snap(), self.dir, "2026-10-12")
        self.assertEqual(path.read_bytes(), damaged)

    def test_unknown_policy_hash_and_unreadable_files_are_reported(self):
        s = snap()
        s["policy_hash"] = "0" * 64
        s["snapshot_hash"] = rp.snapshot_hash(s)
        rp.publish(s, self.dir, "2026-10-10")
        (self.dir / "ranking-bad.json").write_text("{")
        probs = rp.verify(self.dir)["problems"]
        self.assertEqual(len(probs), 2)
        self.assertTrue(any("policy registry" in p for p in probs))
        self.assertTrue(any("unreadable" in p for p in probs))

    def test_refuses_tampered_snapshot_and_bad_date(self):
        s = snap()
        s["total"] = 99
        with self.assertRaises(rp.PublicationError):
            rp.publish(s, self.dir, "2026-10-10")
        with self.assertRaises(rp.PublicationError):
            rp.publish(snap(), self.dir, "10/10/2026")
        self.assertFalse(self.dir.exists())

    def test_overdue_reports_missing_and_stale_publication(self):
        self.assertTrue(rp.overdue(self.dir, "2026-10-10"))
        rp.publish(snap(), self.dir, "2026-10-10")
        self.assertFalse(rp.overdue(self.dir, "2026-10-10"))
        self.assertTrue(rp.overdue(self.dir, "2026-10-11"))

    def test_malformed_archived_publication_date_is_a_problem_and_not_latest(self):
        good = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        s2 = snap()
        s2["as_of"] = "2026-10-08"
        s2["snapshot_hash"] = rp.snapshot_hash(s2)
        bad = Path(rp.publish(s2, self.dir, "2026-10-11")["path"])
        odd = ("2026-10-11\n", "\u0662\u0660\u0662\u0666-\u0661\u0660-\u0661\u0661")
        for value in ("2026-11-31", "20261011", "", None, 20261011, ["2026-10-11"], *odd):
            with self.subTest(value=value):
                rec = json.loads(bad.read_text())
                rec["published_on"] = value
                bad.write_text(json.dumps(rec))
                res = rp.verify(self.dir)
                self.assertEqual(
                    res["problems"], [f"{bad.name}: publication date is not a valid calendar date."]
                )
                self.assertEqual((res["count"], res["latest"]), (2, "2026-10-10"))
        self.assertTrue(good.exists())

    def test_only_malformed_dates_leave_no_trusted_latest(self):
        path = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        rec = json.loads(path.read_text())
        rec["published_on"] = "2026-11-31"
        path.write_text(json.dumps(rec))
        self.assertIsNone(rp.verify(self.dir)["latest"])
        self.assertTrue(rp.overdue(self.dir, "2026-10-10"))

    def test_publish_refuses_impossible_calendar_date_before_writing(self):
        odd = ("2026-10-10\n", "\u0662\u0660\u0662\u0666-\u0661\u0660-\u0661\u0660")
        for value in ("2026-11-31", "2026-02-29", "2026-13-01", "0000-01-01", *odd):
            with self.subTest(value=value), self.assertRaises(rp.PublicationError):
                rp.publish(snap(), self.dir, value)
        self.assertFalse(self.dir.exists())

    def test_schedule_states_what_is_not_decided(self):
        self.assertEqual(rp.SCHEDULE["owner"], "to be named")
        self.assertIn("not set", rp.SCHEDULE["retention"])

    def test_module_has_no_clock_and_no_delete(self):
        src = Path(rp.__file__).read_text()
        for word in ("datetime", "import time", "os.remove", "rmtree"):
            self.assertNotIn(word, src)
        self.assertEqual(src.count("os.unlink("), 1)
        self.assertIn("os.unlink(stage)", src)

    def test_unusable_record_at_final_name_is_refused_and_untouched(self):
        path = Path(rp.publish(snap(), self.dir, "2026-10-10")["path"])
        good = path.read_text()
        other = snap()
        other["total"] = 99
        other["snapshot_hash"] = rp.snapshot_hash(other)
        bad_date = json.loads(good)
        bad_date["published_on"] = "2026-11-31"
        cases = {
            "garbage": "{",
            "truncated": good[:25],
            "empty": "",
            "not a mapping": "[]",
            "different snapshot": rp._canonical({"published_on": "2026-10-10", "snapshot": other}),
            "bad date": json.dumps(bad_date),
        }
        for label, text in cases.items():
            with self.subTest(label):
                path.write_text(text)
                with self.assertRaises(rp.PublicationError):
                    rp.publish(snap(), self.dir, "2026-10-12")
                self.assertEqual(path.read_text(), text)
        self.assertEqual(len(list(self.dir.iterdir())), 1)

    def test_publish_syncs_file_then_removes_stage_then_syncs_directory(self):
        real_sync, real_unlink, events = os.fsync, os.unlink, []

        def syncing(fd):
            events.append("sync-dir" if stat.S_ISDIR(os.fstat(fd).st_mode) else "sync-file")
            return real_sync(fd)

        def unlinking(path, *args, **kwargs):
            events.append("unlink-stage")
            return real_unlink(path, *args, **kwargs)

        with patch.object(os, "fsync", syncing), patch.object(os, "unlink", unlinking):
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual(events[:2], ["sync-file", "unlink-stage"])
        self.assertGreaterEqual(events[2:].count("sync-dir"), 2)
        self.assertEqual(set(events[2:]), {"sync-dir"})
        self.assertEqual([p.name for p in self.dir.iterdir()], [rp._name(snap())])

    def test_an_already_archived_record_is_returned_only_after_the_directory_sync(self):
        rp.publish(snap(), self.dir, "2026-10-10")
        kinds = []
        real_sync = os.fsync

        def syncing(fd):
            kinds.append(stat.S_ISDIR(os.fstat(fd).st_mode))
            return real_sync(fd)

        with patch.object(os, "fsync", syncing):
            res = rp.publish(snap(), self.dir, "2026-10-11")
        self.assertEqual((res["written"], res["published_on"]), (False, "2026-10-10"))
        self.assertIn(True, kinds)

    def test_directory_sync_failure_after_commit_is_raised_and_the_record_is_kept(self):
        real_sync = os.fsync

        def syncing(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.EIO, "directory sync failed")
            return real_sync(fd)

        with patch.object(os, "fsync", syncing), self.assertRaises(OSError) as ctx:
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual(ctx.exception.errno, errno.EIO)
        self.assertEqual([p.name for p in self.dir.iterdir()], [rp._name(snap())])
        with patch.object(os, "fsync", syncing), self.assertRaises(OSError):
            rp.publish(snap(), self.dir, "2026-10-11")
        self.assertEqual(rp.publish(snap(), self.dir, "2026-10-12")["published_on"], "2026-10-10")


class AncestorDurabilityTests(unittest.TestCase):
    """Refs #1258. Mocked syscall order only; not real crash or filesystem durability proof."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.dir = self.root / "a" / "b" / "archive"

    def labelled(self, fault=None, events=None):
        names = {
            "root": self.root,
            "a": self.root / "a",
            "b": self.root / "a" / "b",
            "archive": self.dir,
        }
        real_sync, real_link = os.fsync, os.link
        events = [] if events is None else events

        def label(fd):
            st = os.fstat(fd)
            if not stat.S_ISDIR(st.st_mode):
                return "file"
            for name, path in names.items():
                try:
                    if os.path.samestat(st, os.stat(path)):
                        return name
                except OSError:
                    pass
            return "other"

        def syncing(fd):
            name = label(fd)
            events.append(name)
            if name == fault:
                raise OSError(errno.EIO, "sync failed")
            return real_sync(fd)

        def linking(src, dst, *args, **kwargs):
            events.append("link")
            return real_link(src, dst, *args, **kwargs)

        return events, patch.object(os, "fsync", syncing), patch.object(os, "link", linking)

    def test_new_nested_ancestors_are_synced_after_link_deepest_first(self):
        events, sync, link = self.labelled()
        with sync, link:
            rp.publish(snap(), self.dir, "2026-10-10")
        known = [e for e in events if e != "other"]
        self.assertEqual(known, ["file", "link", "archive", "b", "a", "root"])

    def test_existing_archive_keeps_its_parent_sync_after_the_archive_sync(self):
        self.dir.mkdir(parents=True)
        events, sync, link = self.labelled()
        with sync, link:
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual([e for e in events if e != "other"][:3], ["file", "link", "archive"])

    def test_ancestor_sync_failure_after_link_is_unconfirmed_and_keeps_the_record(self):
        _, sync, link = self.labelled(fault="a")
        with sync, link, self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual(ctx.exception.errno, errno.EIO)
        self.assertIs(ctx.exception.written, True)
        self.assertEqual(ctx.exception.published_on, "2026-10-10")
        self.assertNotIn(str(self.root), str(ctx.exception))
        self.assertEqual([p.name for p in self.dir.iterdir()], [rp._name(snap())])
        self.assertEqual(rp.verify(self.dir)["problems"], [])

    def test_retry_with_all_directories_present_is_not_confirmed_until_ancestors_sync(self):
        rp.publish(snap(), self.dir, "2026-10-10")
        _, sync, link = self.labelled(fault="a")
        with sync, link, self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
            rp.publish(snap(), self.dir, "2026-10-11")
        self.assertIs(ctx.exception.written, False)
        res = rp.publish(snap(), self.dir, "2026-10-12")
        self.assertEqual((res["written"], res["published_on"]), (False, "2026-10-10"))

    def test_partially_created_ancestors_from_an_earlier_run_are_still_synced(self):
        (self.root / "a" / "b").mkdir(parents=True)
        events, sync, link = self.labelled(fault="root")
        with sync, link, self.assertRaises(rp.DurabilityUnconfirmedError):
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertIn("a", events)

    def test_symlinked_parent_syncs_the_directory_that_holds_the_entry(self):
        real = self.root / "real"
        real.mkdir()
        (self.root / "link").symlink_to(real)
        archive = self.root / "link" / "x" / "archive"
        synced = []
        real_sync = os.fsync
        names = {"real": real, "x": real / "x"}

        def syncing(fd):
            st = os.fstat(fd)
            for name, path in names.items():
                if stat.S_ISDIR(st.st_mode) and os.path.samestat(st, os.stat(path)):
                    synced.append(name)
            return real_sync(fd)

        with patch.object(os, "fsync", syncing):
            rp.publish(snap(), archive, "2026-10-10")
        self.assertEqual(synced, ["x", "real"])

    def test_chain_stops_after_a_mount_point_ancestor(self):
        events, sync, link = self.labelled()
        with sync, link, patch.object(os.path, "ismount", lambda p: str(p) == str(self.root / "a")):
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual([e for e in events if e != "other"][-3:], ["archive", "b", "a"])

    def test_non_writable_ancestor_is_still_synced_through_a_read_only_handle(self):
        if os.geteuid() == 0:
            self.skipTest("root bypasses permission bits; see the mocked access test")
        self.dir.mkdir(parents=True)
        events, sync, link = self.labelled()
        os.chmod(self.root / "a", 0o555)
        try:
            with sync, link:
                rp.publish(snap(), self.dir, "2026-10-10")
        finally:
            os.chmod(self.root / "a", 0o755)
        known = [e for e in events if e != "other"]
        self.assertEqual(known, ["file", "link", "archive", "b", "a", "root"])

    def test_failed_ancestor_then_permission_change_retry_stays_unconfirmed(self):
        if os.geteuid() == 0:
            self.skipTest("root bypasses permission bits; see the mocked access test")
        _, sync, link = self.labelled(fault="a")
        with sync, link, self.assertRaises(rp.DurabilityUnconfirmedError):
            rp.publish(snap(), self.dir, "2026-10-10")
        os.chmod(self.root / "a", 0o555)
        try:
            _, sync, link = self.labelled(fault="a")
            with sync, link, self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
                rp.publish(snap(), self.dir, "2026-10-11")
            events, sync, link = self.labelled()
            with sync, link:
                res = rp.publish(snap(), self.dir, "2026-10-12")
        finally:
            os.chmod(self.root / "a", 0o755)
        self.assertIs(ctx.exception.written, False)
        self.assertEqual((res["written"], res["published_on"]), (False, "2026-10-10"))
        self.assertIn("a", events)

    def test_mocked_denied_access_does_not_skip_any_ancestor_sync(self):
        # Mocked os.access stands in for another creator or later permission change.
        for denied in ("a", "b"):
            with self.subTest(denied=denied):
                tmp = tempfile.TemporaryDirectory()
                self.addCleanup(tmp.cleanup)
                self.root = Path(tmp.name).resolve()
                self.dir = self.root / "a" / "b" / "archive"
                path = str(self.root.joinpath(*(["a"] if denied == "a" else ["a", "b"])))
                events, sync, link = self.labelled()
                real = os.access
                with (
                    sync,
                    link,
                    patch.object(
                        os,
                        "access",
                        lambda p, m, *a, path=path, real=real, **k: (
                            False if str(p) == path else real(p, m)
                        ),
                    ),
                ):
                    rp.publish(snap(), self.dir, "2026-10-10")
                known = [e for e in events if e != "other"]
                self.assertEqual(known, ["file", "link", "archive", "b", "a", "root"])

    def test_archive_that_is_itself_a_mount_point_is_not_synced_past_its_filesystem(self):
        events, sync, link = self.labelled(fault="b")
        with sync, link, patch.object(os.path, "ismount", lambda p: str(p) == str(self.dir)):
            res = rp.publish(snap(), self.dir, "2026-10-10")
        self.assertIs(res["written"], True)
        self.assertEqual([e for e in events if e != "other"], ["file", "link", "archive"])

    def test_required_ancestor_open_failure_is_reported_not_skipped(self):
        real_open = os.open

        def opening(path, flags, *a, **k):
            if str(path) == str(self.root / "a"):
                raise OSError(errno.EACCES, "denied")
            return real_open(path, flags, *a, **k)

        with (
            patch.object(os, "open", opening),
            self.assertRaises(rp.DurabilityUnconfirmedError) as ctx,
        ):
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual(ctx.exception.errno, errno.EACCES)
        self.assertEqual(rp.verify(self.dir)["problems"], [])


class ConcurrentWriterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name) / "archive"

    def record(self):
        (path,) = [p for p in self.dir.iterdir() if p.name.endswith(".json")]
        return path, path.read_bytes()

    def test_same_snapshot_different_dates_keep_one_truthful_record(self):
        with gated("A", "B") as gate:
            gate.start("A", lambda: rp.publish(snap(), self.dir, "2026-10-10"))
            self.assertTrue(gate.arrived["A"].wait(DEADLINE))
            gate.start("B", lambda: rp.publish(snap(), self.dir, "2026-10-11"))
            self.assertTrue(gate.arrived["B"].wait(DEADLINE))
            gate.release("A")
            gate.release("B")
            gate.join()
        a, b = gate.results["A"], gate.results["B"]
        path, data = self.record()
        self.assertEqual(json.loads(data)["published_on"], "2026-10-10")
        self.assertEqual((a["written"], a["published_on"]), (True, "2026-10-10"))
        self.assertIsInstance(b, dict)
        self.assertEqual(
            (b["written"], b["published_on"], b["path"]), (False, "2026-10-10", a["path"])
        )
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()), [path.name])
        self.assertEqual(rp.verify(self.dir), dict(count=1, problems=[], latest="2026-10-10"))

    def test_delayed_contender_leaves_a_finished_record_unchanged(self):
        with gated("B") as gate:
            gate.start("B", lambda: rp.publish(snap(), self.dir, "2026-10-11"))
            self.assertTrue(gate.arrived["B"].wait(DEADLINE))
            first = rp.publish(snap(), self.dir, "2026-10-10")
            _, before = self.record()
            gate.release("B")
            gate.join()
        late = gate.results["B"]
        self.assertTrue(first["written"])
        self.assertIsInstance(late, dict)
        self.assertEqual((late["written"], late["published_on"]), (False, "2026-10-10"))
        self.assertEqual(self.record()[1], before)
        self.assertEqual(json.loads(before)["published_on"], "2026-10-10")

    def test_directory_sync_failure_after_link_keeps_the_record_and_reports_it_unconfirmed(self):
        real = os.fsync

        def failing(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(5, "sync failed")
            return real(fd)

        with patch.object(os, "fsync", failing):
            with self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
                rp.publish(snap(), self.dir, "2026-10-10")
        self.assertIsInstance(ctx.exception, OSError)
        self.assertEqual(ctx.exception.published_on, "2026-10-10")
        self.assertIs(ctx.exception.written, True)
        self.assertIs(
            rp.DurabilityUnconfirmedError("p", "2026-10-10", OSError(5, "x")).written, None
        )
        self.assertEqual([p.name for p in self.dir.iterdir()], [Path(ctx.exception.path).name])
        self.assertEqual(oct(Path(ctx.exception.path).stat().st_mode & 0o777), "0o600")
        self.assertEqual(rp.verify(self.dir)["problems"], [])

    def test_stage_cleanup_failure_does_not_mask_the_unconfirmed_directory_sync(self):
        real_fsync, real_unlink = os.fsync, os.unlink

        def failing_fsync(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.EIO, "sync failed")
            return real_fsync(fd)

        def failing_unlink(path, *a, **k):
            if os.path.basename(path).endswith(".tmp"):
                raise PermissionError(errno.EACCES, "read-only")
            return real_unlink(path, *a, **k)

        with patch.object(os, "fsync", failing_fsync), patch.object(os, "unlink", failing_unlink):
            with self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
                rp.publish(snap(), self.dir, "2026-10-10")
        err = ctx.exception
        self.assertEqual(err.errno, errno.EIO)
        self.assertTrue(err.stage_retained.endswith(".tmp"))
        self.assertNotIn("/", err.stage_retained)
        self.assertEqual(rp.verify(self.dir)["problems"], [])
        self.assertTrue((self.dir / err.stage_retained).exists())

    def test_retry_stays_unconfirmed_until_the_sync_succeeds(self):
        real = os.fsync
        failing_sync = True

        def syncing(fd):
            if failing_sync and stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.EIO, "sync failed")
            return real(fd)

        with patch.object(os, "fsync", syncing):
            with self.assertRaises(rp.DurabilityUnconfirmedError):
                rp.publish(snap(), self.dir, "2026-10-10")
            with self.assertRaises(rp.DurabilityUnconfirmedError) as again:
                rp.publish(snap(), self.dir, "2026-10-11")
            self.assertEqual(again.exception.errno, errno.EIO)
            self.assertEqual(again.exception.published_on, "2026-10-10")
            self.assertIs(again.exception.written, False)
            failing_sync = False
            res = rp.publish(snap(), self.dir, "2026-10-12")
        self.assertEqual((res["written"], res["published_on"]), (False, "2026-10-10"))

    def test_publish_race_loser_confirms_durability_before_reporting_it(self):
        real_link, state = os.link, {}
        real_sync = os.fsync

        def failing(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError(errno.EIO, "sync failed")
            return real_sync(fd)

        def racing(src, dst, *a, **k):
            if not state:
                state["raced"] = True
                rp.publish(snap(), self.dir, "2026-10-11")
                state["sync"] = patch.object(os, "fsync", failing)
                state["sync"].start()
            return real_link(src, dst, *a, **k)

        try:
            with patch.object(os, "link", racing):
                with self.assertRaises(rp.DurabilityUnconfirmedError) as ctx:
                    rp.publish(snap(), self.dir, "2026-10-10")
        finally:
            state["sync"].stop()
        self.assertEqual(ctx.exception.published_on, "2026-10-11")
        self.assertIs(ctx.exception.written, False)
        self.assertEqual(rp.verify(self.dir)["problems"], [])

    def test_cleanup_removes_only_the_staging_file_it_owns(self):
        self.dir.mkdir()
        foreign = {
            self.dir / f"{rp._name(snap())}.tmp": b"legacy writer",
            self.dir / ".other-writer.tmp": b"other writer",
            self.dir / "notes.txt": b"unrelated",
        }
        for path, data in foreign.items():
            path.write_bytes(data)
        rp.publish(snap(), self.dir, "2026-10-10")
        rp.publish(snap(), self.dir, "2026-10-11")
        self.assertEqual({p: p.read_bytes() for p in foreign}, foreign)
        self.assertEqual(len(list(self.dir.iterdir())), len(foreign) + 1)

    def test_failed_publication_removes_its_stage_and_keeps_foreign_files(self):
        self.dir.mkdir()
        keep = self.dir / ".other-writer.tmp"
        keep.write_bytes(b"other writer")
        refused = PermissionError("link refused")
        with (
            patch.object(os, "link", side_effect=refused),
            patch.object(os, "replace", side_effect=refused),
            self.assertRaises(PermissionError),
        ):
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual([p.name for p in self.dir.iterdir()], [keep.name])
        self.assertEqual(keep.read_bytes(), b"other writer")

    def test_filesystem_without_hard_links_refuses_and_publishes_nothing(self):
        self.dir.mkdir()
        foreign = {self.dir / ".other-writer.tmp": b"other", self.dir / "notes.txt": b"note"}
        for path, data in foreign.items():
            path.write_bytes(data)
        unsupported = OSError(errno.EPERM, "hard links are not supported")
        with patch.object(os, "link", side_effect=unsupported), self.assertRaises(OSError) as ctx:
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual(ctx.exception.errno, errno.EPERM)
        self.assertEqual({p: p.read_bytes() for p in self.dir.iterdir()}, foreign)
        self.assertEqual(rp.verify(self.dir)["count"], 0)
        self.assertTrue(rp.publish(snap(), self.dir, "2026-10-10")["written"])

    def failing_unlink(self, error: OSError) -> Any:
        real = os.unlink

        def unlink(path: Any, *args: Any, **kwargs: Any) -> None:
            if os.path.basename(path).startswith(".ranking-"):
                raise error
            real(path, *args, **kwargs)

        return patch.object(os, "unlink", side_effect=unlink)

    def test_cleanup_failure_after_commit_keeps_the_committed_outcome(self):
        with self.failing_unlink(OSError(errno.EROFS, "read-only")):
            res = rp.publish(snap(), self.dir, "2026-10-10")
        path, data = self.record()
        (stage,) = [p for p in self.dir.iterdir() if p.name.endswith(".tmp")]
        self.assertEqual(
            res,
            dict(
                path=str(path),
                written=True,
                published_on="2026-10-10",
                stage_retained=stage.name,
            ),
        )
        self.assertEqual(stage.read_bytes(), data)
        self.assertEqual(rp.verify(self.dir), dict(count=1, problems=[], latest="2026-10-10"))
        self.assertEqual(rp.publish(snap(), self.dir, "2026-10-11")["written"], False)

    def test_cleanup_failure_for_the_loser_returns_the_winner_record(self):
        with gated("B") as gate:
            gate.start("B", lambda: rp.publish(snap(), self.dir, "2026-10-11"))
            self.assertTrue(gate.arrived["B"].wait(DEADLINE))
            first = rp.publish(snap(), self.dir, "2026-10-10")
            _, before = self.record()
            with self.failing_unlink(OSError(errno.EROFS, "read-only")):
                gate.release("B")
                gate.join()
        late = gate.results["B"]
        self.assertTrue(first["written"])
        self.assertIsInstance(late, dict)
        self.assertEqual((late["written"], late["published_on"]), (False, "2026-10-10"))
        self.assertTrue(late["stage_retained"].endswith(".tmp"))
        self.assertEqual(self.record()[1], before)

    def test_stage_and_record_stay_owner_only_under_any_umask(self):
        for mask in (0o022, 0o002):
            with self.subTest(umask=oct(mask)):
                old = os.umask(mask)
                try:
                    with (
                        tempfile.TemporaryDirectory() as d,
                        self.failing_unlink(OSError(errno.EROFS, "ro")),
                    ):
                        res = rp.publish(snap(), Path(d), "2026-10-10")
                        modes = {p.name: stat.S_IMODE(p.stat().st_mode) for p in Path(d).iterdir()}
                finally:
                    os.umask(old)
                self.assertEqual(set(modes.values()), {0o600})
                self.assertEqual(len(modes), 2)
                self.assertIn(res["stage_retained"], modes)

    def test_retained_stage_after_link_failure_is_named_on_the_exception(self):
        with (
            patch.object(os, "link", side_effect=OSError(errno.EPERM, "no links")),
            self.failing_unlink(OSError(errno.EROFS, "read-only")),
            self.assertRaises(OSError) as ctx,
        ):
            rp.publish(snap(), self.dir, "2026-10-10")
        (stage,) = [p for p in self.dir.iterdir() if p.name.endswith(".tmp")]
        self.assertEqual(ctx.exception.stage_retained, stage.name)
        self.assertEqual(stat.S_IMODE(stage.stat().st_mode), 0o600)

    def test_cleanup_failure_does_not_mask_the_link_failure(self):
        refused = OSError(errno.EPERM, "hard links are not supported")
        with (
            patch.object(os, "link", side_effect=refused),
            self.failing_unlink(OSError(errno.EROFS, "read-only")),
            self.assertRaises(OSError) as ctx,
        ):
            rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual(ctx.exception.errno, errno.EPERM)
        self.assertEqual(len(ctx.exception.__notes__), 1)
        self.assertEqual(rp.verify(self.dir)["count"], 0)

    def test_stage_already_gone_after_commit_reports_nothing_retained(self):
        real_link, real_unlink = os.link, os.unlink

        def link_then_lose_stage(src: Any, dst: Any) -> None:
            real_link(src, dst)
            real_unlink(src)

        with patch.object(os, "link", side_effect=link_then_lose_stage):
            res = rp.publish(snap(), self.dir, "2026-10-10")
        self.assertEqual((res["written"], res["published_on"]), (True, "2026-10-10"))
        self.assertNotIn("stage_retained", res)
        self.assertEqual([p.name for p in self.dir.iterdir()], [Path(res["path"]).name])

    def test_sequential_bytes_and_name_are_unchanged(self):
        first = rp.publish(snap(), self.dir, "2026-10-10")
        expected = rp._canonical({"published_on": "2026-10-10", "snapshot": snap()})
        path, data = self.record()
        self.assertEqual(data, expected.encode("utf-8"))
        self.assertEqual(path.name, rp._name(snap()))
        self.assertEqual(first["path"], str(path))
        self.assertEqual(rp.publish(snap(), self.dir, "2026-10-12")["published_on"], "2026-10-10")
        self.assertEqual(self.record()[1], data)

    def test_separate_processes_publish_one_truthful_record(self):
        ctx = multiprocessing.get_context("spawn")
        dates = ["2026-10-10", "2026-10-11", "2026-10-12", "2026-10-13"]
        barrier, out = ctx.Barrier(len(dates)), ctx.Queue()
        procs = [
            ctx.Process(target=_publish_in_process, args=(str(self.dir), d, barrier, out))
            for d in dates
        ]
        for proc in procs:
            proc.start()
        results = [out.get(timeout=60) for _ in procs]
        for proc in procs:
            proc.join(60)
            self.assertEqual(proc.exitcode, 0)
        self.assertTrue(all(isinstance(r, dict) for r in results), results)
        self.assertEqual(sum(r["written"] for r in results), 1)
        _, data = self.record()
        self.assertEqual({r["published_on"] for r in results}, {json.loads(data)["published_on"]})
        self.assertEqual(len(list(self.dir.iterdir())), 1)
        self.assertEqual(rp.verify(self.dir)["problems"], [])


if __name__ == "__main__":
    unittest.main()


class SignoffTests(unittest.TestCase):
    def signed(self):
        p = json.loads(json.dumps(ranking.POLICY_V1))
        p["owner"] = "Dana Example"
        p["signoff"] = dict(
            signed_by="Dana Example",
            signed_on="2026-11-05",
            rule_order_hash=ranking.rule_order_hash(p),
        )
        return p

    def test_draft_policy_is_not_signed_and_says_why(self):
        self.assertFalse(ranking.is_signed(ranking.POLICY_V1))
        self.assertEqual(ranking.signoff_problems(ranking.POLICY_V1), ["No named policy owner."])

    def test_named_owner_without_record_is_not_signed(self):
        p = self.signed()
        del p["signoff"]
        self.assertEqual(ranking.signoff_problems(p), ["No recorded sign-off of the rule order."])

    def test_complete_signoff_is_signed(self):
        self.assertTrue(ranking.is_signed(self.signed()))

    def test_signoff_by_someone_else_or_undated_is_refused(self):
        p = self.signed()
        p["signoff"].update(signed_by="Someone Else", signed_on="soon")
        self.assertEqual(len(ranking.signoff_problems(p)), 2)

    def test_changing_rule_order_voids_signoff(self):
        p = self.signed()
        p["rules"] = list(reversed(p["rules"]))
        self.assertEqual(ranking.signoff_problems(p), ["Sign-off does not match this rule order."])
        q = self.signed()
        q["stage_order"] = list(reversed(q["stage_order"]))
        self.assertFalse(ranking.is_signed(q))

    def test_status_reports_unsigned_reasons_without_changing_ranking(self):
        before = ranking.canonical(ranking.rank([case("ZF-A")]))
        self.assertFalse(ranking.is_signed(ranking.CURRENT))
        self.assertEqual(ranking.canonical(ranking.rank([case("ZF-A")])), before)
