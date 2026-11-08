"""C7 regressions for issue 1288: physical-send ordering, per-home consent coordination, schedule
upgrade and bounded coalescing. Synthetic data, SQLite, a loopback transport that counts request
bytes and a local MOCK provider. None of this is a live model call or SQL Server acceptance."""

import os
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import release_support
from zava_forward.core import sensor_view
from zava_forward.core.ai import Ai

import test_assistants as ta
import test_quality_sensors as qs


class Meter:
    """Stands in for the financial meter; `before` runs where the former final check sat."""

    def __init__(self, before=None):
        self.before = before

    def reserve(self, *args, **kwargs):
        return "rid"

    def dispatch_check(self, rid):
        if self.before:
            self.before()

    def complete(self, *args, **kwargs):
        return None


class Sink:
    """Loopback server that records every request body it receives."""

    def __init__(self):
        sink = self
        self.bodies = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                size = int(self.headers.get("Content-Length", 0))
                sink.bodies.append(self.rfile.read(size))
                out = b'{"model":"test-model","choices":[{"message":{"content":"{}"}}],"usage":{}}'
                self.send_response(200)
                self.send_header("Content-Length", str(len(out)))
                self.end_headers()
                self.wfile.write(out)

            def log_message(self, *args):
                return None

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    @property
    def endpoint(self):
        return f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(5)


class Base(qs.Seed, ta.ApiTests):
    def ready(self, **kw):
        self.mock(**kw)
        self.put(4)
        self.add_live(10)
        self.quality_ready()

    def real_transport(self, before=None):
        """A real Ai client whose only network is a loopback sink."""
        sink = Sink()
        self.addCleanup(sink.close)
        ai = Ai()
        ai.endpoint, ai.token, ai.expires = sink.endpoint, "t", time.time() + 3600
        ai.consumption = Meter(before)
        self.store.ai = ai
        # A constructed record only admits the loopback fixture; it grants no real authority.
        release_support.install(self.store, cls="actual")
        return sink

    def withdraw_in_thread(self, controls=None):
        errors = []

        def run():
            try:
                if controls is None:
                    self.set_consent("declined")
                else:
                    self.controls.update(controls)
                    self.configure()
            except Exception as error:  # noqa: BLE001 - asserted by the caller
                errors.append(error)

        thread = threading.Thread(target=run)
        thread.start()
        return thread, errors

    def consent_now(self):
        with self.service.transaction() as db:
            return sensor_view.consent(db, "ZF-1", {qs.DEFAULT}, self.service.mssql)

    def used_calls(self):
        with self.service.transaction() as db:
            return db.execute("SELECT SUM(used_calls) FROM assistant_allowance").fetchone()[0] or 0

    def pending(self, service=None):
        service = service or self.service
        return [t for t in self.quality_task() if service.detail(self.pm, t)["state"] == "pending"]

    def gate_task(self):
        self.service.scan()
        (tid,) = self.quality_task()
        with self.service.transaction() as db:
            return self.service._row(db, tid)

    def gate_rows(self):
        with self.service.transaction() as db:
            return db.execute(
                "SELECT home_id,fence FROM assistant_dispatch_gate ORDER BY home_id,fence"
            ).fetchall()


class PhysicalSend(Base):
    def test_withdrawal_during_preparation_is_not_delayed_and_nothing_is_sent(self):
        entered, proceed = threading.Event(), threading.Event()

        def before():
            entered.set()
            proceed.wait(20)

        self.put(4)
        self.add_live(10)
        self.quality_ready()
        sink = self.real_transport(before)
        self.service.scan()
        (tid,) = self.quality_task()
        worker = threading.Thread(target=self.service.execute, args=(tid,))
        worker.start()
        try:
            self.assertTrue(entered.wait(20))
            thread, errors = self.withdraw_in_thread()
            thread.join(5)
            self.assertFalse(thread.is_alive(), "withdrawal waited for request preparation")
        finally:
            proceed.set()
            worker.join(30)
        thread.join(30)
        self.assertEqual(errors, [])
        self.assertEqual(sink.bodies, [])
        self.assertEqual(self.consent_now(), "declined")
        self.assertEqual(self.gate_rows(), [])

    def test_authorised_send_holds_a_withdrawal_until_the_call_ends(self):
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        sink = self.real_transport()
        self.service.scan()
        (tid,) = self.quality_task()
        seen = []
        real = self.service._dispatch_gate

        def factory(task):
            gate = real(task)

            def authorised():
                valid = gate()
                thread, errors = self.withdraw_in_thread()
                thread.join(1.0)
                seen.append((thread.is_alive(), errors))
                self.thread = thread
                return valid

            authorised.release = gate.release
            return authorised

        with patch.object(self.service, "_dispatch_gate", side_effect=factory):
            self.service.execute(tid)
        self.thread.join(30)
        self.assertEqual(seen, [(True, [])])
        self.assertEqual(len(sink.bodies), 1)
        self.assertEqual(self.consent_now(), "declined")

    def test_a_stall_after_authorisation_past_the_database_expiry_sends_nothing(self):
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        sink = self.real_transport()
        self.service.scan()
        (tid,) = self.quality_task()
        real_gate, outcome, offset = self.service._dispatch_gate, [], [0.0]
        real_clock = time.monotonic

        def factory(task):
            gate = real_gate(task)

            def stalled():
                valid = gate()
                with self.service.transaction() as db:
                    db.execute("UPDATE assistant_dispatch_gate SET expires_at=expires_at-1000")
                offset[0] += 1000
                thread, errors = self.withdraw_in_thread()
                thread.join(10)
                outcome.append((thread.is_alive(), errors))
                return valid

            stalled.release = gate.release
            return stalled

        with (
            patch.object(self.service, "_dispatch_gate", side_effect=factory),
            patch.object(time, "monotonic", side_effect=lambda: real_clock() + offset[0]),
        ):
            self.service.execute(tid)
        self.assertEqual(outcome, [(False, [])])
        self.assertEqual(sink.bodies, [])
        self.assertEqual(self.consent_now(), "declined")

    def test_each_attempt_has_its_own_fence_and_never_releases_another(self):
        self.ready()
        task = self.gate_task()
        first, second = (
            self.service._dispatch_gate(dict(task, fence=1)),
            self.service._dispatch_gate(dict(task, fence=2)),
        )
        first()
        second()
        self.assertEqual(self.gate_rows(), [("ZF-1", 1), ("ZF-1", 2)])
        thread, errors = self.withdraw_in_thread()
        first.release()
        self.assertEqual(self.gate_rows(), [("ZF-1", 2)])
        thread.join(1.0)
        self.assertTrue(thread.is_alive())
        second.release()
        thread.join(30)
        self.assertEqual((thread.is_alive(), errors), (False, []))
        self.assertEqual(self.consent_now(), "declined")

    def test_a_dispatch_for_a_foreign_provider_runs_the_gate_before_the_call(self):
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        rows = []
        real = self.provider.evidence

        def evidence(*args):
            rows.append(self.gate_rows())
            return real(*args)

        self.provider.evidence = evidence
        self.assertTrue(self.service.execute(tid))
        self.assertEqual(rows, [[("ZF-1", 1)]])
        self.assertEqual(self.gate_rows(), [])


class PerHome(Base):
    def live_row(self, home):
        with self.service.transaction() as db:
            db.execute(
                "INSERT INTO assistant_dispatch_gate (home_id,task_id,fence,expires_at)"
                " VALUES (?,?,1,?)",
                (home, "t-" + home, self.service.now(db) + 600),
            )

    def clear_rows(self):
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_dispatch_gate")

    def test_an_unrelated_homes_dispatch_does_not_block_a_withdrawal(self):
        self.put(3)
        self.live_row("ZF-2")
        thread, errors = self.withdraw_in_thread()
        thread.join(5)
        self.assertEqual((thread.is_alive(), errors), (False, []))
        self.assertEqual(self.consent_now(), "declined")

    def test_a_same_home_dispatch_blocks_until_it_ends(self):
        self.put(3)
        self.live_row("ZF-1")
        thread, errors = self.withdraw_in_thread()
        thread.join(1.0)
        self.assertTrue(thread.is_alive())
        self.clear_rows()
        thread.join(30)
        self.assertEqual((thread.is_alive(), errors), (False, []))

    def test_moving_a_sensor_waits_for_the_old_home_and_a_batch_only_for_changed_homes(self):
        self.put(3)
        self.controls["SENS-SYN-2"] = ("ZF-2", "granted")
        self.configure()
        self.live_row("ZF-1")
        unrelated, errors = self.withdraw_in_thread({"SENS-SYN-2": ("ZF-2", "declined")})
        unrelated.join(5)
        self.assertEqual((unrelated.is_alive(), errors), (False, []))
        moved, errors = self.withdraw_in_thread({qs.DEFAULT: ("ZF-2", "granted")})
        moved.join(1.0)
        self.assertTrue(moved.is_alive())
        self.clear_rows()
        moved.join(30)
        self.assertEqual((moved.is_alive(), errors), (False, []))


class Upgrade(Base):
    C5_SCHEDULE = (
        "CREATE TABLE assistant_schedule (capability TEXT NOT NULL, case_id TEXT NOT NULL,"
        " scope TEXT NOT NULL, signature TEXT NOT NULL, task_id TEXT NOT NULL, at REAL NOT NULL,"
        " PRIMARY KEY (capability, case_id))"
    )

    def downgrade(self):
        """Rebuild the C5 shape, with the retained rows, from the current one."""
        with self.service.transaction() as db:
            saved = db.execute(
                "SELECT capability,case_id,scope,signature,task_id,at FROM assistant_schedule"
            ).fetchall()
            db.execute("DROP TABLE assistant_schedule")
            db.execute(self.C5_SCHEDULE)
            for row in saved:
                db.execute("INSERT INTO assistant_schedule VALUES (?,?,?,?,?,?)", row)
            columns = [r[1] for r in db.execute("PRAGMA table_info(assistant_tasks)")]
            if "dispatched" in columns:
                db.execute("DROP INDEX IF EXISTS ix_assistant_dispatched")
                db.execute("ALTER TABLE assistant_tasks DROP COLUMN dispatched")
        return saved

    def columns(self, table):
        with self.service.transaction() as db:
            return [r[1] for r in db.execute(f"PRAGMA table_info({table})")]

    def test_actual_c5_tables_are_upgraded_in_place_idempotently_and_keep_their_rows(self):
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        saved = self.downgrade()
        self.assertTrue(saved)
        self.assertNotIn("replaced", self.columns("assistant_schedule"))
        restarted = self.other()
        self.assertTrue(restarted.sql, restarted.schema_error)
        restarted.migrate()
        self.assertIn("replaced", self.columns("assistant_schedule"))
        self.assertIn("dispatched", self.columns("assistant_tasks"))
        with restarted.transaction() as db:
            kept = db.execute(
                "SELECT capability,case_id,scope,signature,task_id,at FROM assistant_schedule"
            ).fetchall()
        self.assertEqual(sorted(kept), sorted(saved))
        self.assertTrue(restarted.execute(tid))
        restarted.scan_cursor = ""
        restarted.scan()
        self.assertEqual(self.quality_task(), [tid])
        self.assertEqual(restarted.invoke(self.pm, "quality-evidence", "ZF-1")["id"], tid)

    def complete_documents(self, version):
        with self.store.lock:
            case = self.store._case("ZF-1")
            case["documents"] = [
                dict(
                    id="SURVEY-1",
                    kind="Survey",
                    name="s",
                    summary="s",
                    content_sha256="a" + version,
                    version=1,
                ),
                dict(
                    id="DESIGN-1",
                    kind="Design",
                    name="d",
                    summary="d",
                    content_sha256="b" + version,
                    version=1,
                ),
            ]
            case["technical"] = dict(case.get("technical") or {}, design_version="v1")
            self.store.save()

    def test_a_legacy_gap_free_assessment_change_is_detected_after_upgrade(self):
        self.ready()
        cap = "assessment-preparation"
        self.service.scan()
        (first,) = [t for t in self.tasks(cap)]
        self.assertTrue(self.service.execute(first))
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_schedule")
        self.complete_documents("1")
        self.service.scan_cursor = ""
        self.service.scan()
        after_a = self.tasks(cap)
        self.assertEqual(len(after_a), 2)
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(self.tasks(cap), after_a)
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_schedule")
        self.complete_documents("2")
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self.tasks(cap)), 3)

    def tasks(self, cap):
        with self.service.transaction() as db:
            rows = db.execute(
                "SELECT id FROM assistant_tasks WHERE capability=? AND case_id='ZF-1' ORDER BY id",
                (cap,),
            ).fetchall()
        return [r[0] for r in rows]

    def test_legacy_adoption_reads_a_bounded_number_of_task_bodies(self):
        self.ready()
        self.service.scan()
        (first,) = self.quality_task()
        self.assertTrue(self.service.execute(first))
        with self.service.transaction() as db:
            body = db.execute("SELECT body FROM assistant_tasks WHERE id=?", (first,)).fetchone()[0]
            for i in range(40):
                db.execute(
                    "INSERT INTO assistant_tasks (id,capability,case_id,signature,body,state,fence,"
                    "owner,lease_until,attempts,not_before,revision)"
                    " VALUES (?,?,?,?,?,'ready',1,'',0,1,0,?)",
                    (f"old{i:03d}", "quality-evidence", "ZF-1", f"s{i}", body, 100 + i),
                )
            db.execute("DELETE FROM assistant_schedule")
        fetched, real = [], self.store.assistant_connection

        class Cursor:
            def __init__(self, cursor, sql):
                self.cursor, self.sql = cursor, sql

            def fetchall(self):
                rows = self.cursor.fetchall()
                fetched.append((self.sql, len(rows)))
                return rows

            def __getattr__(self, name):
                return getattr(self.cursor, name)

        class Recording:
            def __init__(self, db):
                self.db = db

            def execute(self, sql, *args):
                return Cursor(self.db.execute(sql, *args), sql)

            def __getattr__(self, name):
                return getattr(self.db, name)

        with patch.object(
            self.store, "assistant_connection", side_effect=lambda: Recording(real())
        ):
            self.service.scan_cursor = ""
            self.service.scan()
        history = [n for sql, n in fetched if "FROM assistant_tasks" in sql and "attempts" in sql]
        self.assertTrue(history)
        self.assertLessEqual(max(history), 5)


class Coalescing(Base):
    def test_sustained_churn_is_bounded_without_dispatch_and_recovers_after_a_quiet_interval(self):
        self.ready()
        self.service.scan()
        for minute in (31, 25, 19, 13, 7):
            self.service.scan_cursor = ""
            self.service.scan()
            queued = self.pending()
            self.add_live(minute)
            for tid in queued:
                self.service.execute(tid)
        self.assertEqual((self.provider.calls, self.used_calls()), (0, 0))
        rows = self.quality_task()
        self.assertLessEqual(len(rows), 6)
        reasons = [self.service.detail(self.pm, t).get("reason") or "" for t in rows]
        self.assertTrue(any("paused" in r for r in reasons), reasons)
        restarted = self.other()
        later = patch.object(restarted, "now", side_effect=lambda db=None: time.time() + 400)
        with later:
            restarted.scan_cursor = ""
            restarted.scan()
            self.assertLessEqual(len(self.quality_task()), len(rows) + 1)
            (recovery,) = self.pending(restarted)
            self.assertTrue(restarted.execute(recovery))
        self.assertEqual((self.provider.calls, self.used_calls()), (1, 1))

    def test_a_late_manual_request_does_not_cause_another_autonomous_call_in_the_bucket(self):
        gate = dict(entered=threading.Event(), proceed=threading.Event())
        self.mock(gate=gate)
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        (tid,) = self.quality_task()
        worker = threading.Thread(target=self.service.execute, args=(tid,))
        worker.start()
        try:
            self.assertTrue(gate["entered"].wait(20))
            self.assertEqual(self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], tid)
        finally:
            gate["proceed"].set()
            worker.join(30)
        for minute in (5, 4):
            self.add_live(minute)
            self.service.scan_cursor = ""
            self.service.scan()
        self.assertEqual(self.quality_task(), [tid])
        self.assertEqual((self.provider.calls, self.used_calls()), (1, 1))
        self.assertEqual(
            self.service.detail(self.pm, tid)["review_flag"]["status"], "review-suggested"
        )


class Comparison(Base):
    def flag(self, tid):
        return self.service.detail(self.pm, tid)["review_flag"]

    def proactive(self):
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        return tid

    def test_a_corrected_cited_row_is_reported_changed_even_with_the_same_id(self):
        tid = self.proactive()
        cited = self.flag(tid)["readings"][0]
        with self.service.transaction() as db:
            db.execute(
                "UPDATE sensor_reading SET temperature_c='1.5' WHERE sensor_id=? AND reading_id=?",
                (cited["sensor_id"], cited["reading_id"]),
            )
        flag = self.flag(tid)
        self.assertIs(flag["changed_since_capture"], True)
        self.assertEqual(flag["cited_comparison"]["state"], "changed")
        self.assertEqual(len(flag["cited_comparison"]["changed_ids"]), 1)

    def test_an_extra_uncited_row_is_reported_separately_and_the_cited_rows_match(self):
        tid = self.proactive()
        self.add_live(5)
        flag = self.flag(tid)
        self.assertIs(flag["changed_since_capture"], False)
        self.assertEqual(flag["cited_comparison"]["state"], "match")
        self.assertEqual(flag["newer_reading_count"], 1)

    def test_a_removed_cited_row_is_missing_and_no_current_capture_is_unknown(self):
        tid = self.proactive()
        cited = self.flag(tid)["readings"][0]
        with self.service.transaction() as db:
            db.execute(
                "DELETE FROM sensor_reading WHERE sensor_id=? AND reading_id=?",
                (cited["sensor_id"], cited["reading_id"]),
            )
        flag = self.flag(tid)
        self.assertIs(flag["changed_since_capture"], True)
        self.assertEqual(len(flag["cited_comparison"]["missing_ids"]), 1)

    def test_withheld_current_capture_reports_unknown_not_match(self):
        tid = self.proactive()
        task = self.service.detail(self.pm, tid)
        from zava_forward.core.assistants import review_flag

        flag = review_flag(
            dict(task, snapshot=task["snapshot"]), actionable=True, withheld=False, current=None
        )
        self.assertIsNone(flag["changed_since_capture"])
        self.assertEqual(flag["cited_comparison"]["state"], "unknown")


MSSQL = unittest.skipUnless(
    os.environ.get("ZF_TEST_MSSQL") == "1", "needs disposable SQL Server (ZF_TEST_MSSQL=1)"
)


@MSSQL
class MssqlPerHome(ta.MssqlFixture, PerHome):
    pass


if __name__ == "__main__":
    unittest.main()
