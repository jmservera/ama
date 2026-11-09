"""E1 regressions for issue 1288 (original C7 independent findings F1-F6). Synthetic data, SQLite
or a disposable SQL Server, controlled fake transports and providers, never a live model call.

F1 physical send bound and unfenced providers; F2 direct control writes during a live dispatch gate;
F3 a manual request and the serviced proactive Quality slot; F4 bounded legacy adoption;
F5 coalescing under continuing readings; F6 an unavailable current capture is unknown, not
missing."""

import copy
import json
import os
import threading
import time
import unittest
from unittest.mock import patch

from zava_forward.core import ai_consumption, sensor_view
from zava_forward.core import assistants as ai_gate
from zava_forward.core.assistants import review_flag

import test_assistants as ta
import test_quality_sensors as qs
import test_quality_sensors_c7 as c7


class GateBase(c7.Base):
    def live_row(self, home, seconds=600):
        with self.service.transaction() as db:
            db.execute(
                "INSERT INTO assistant_dispatch_gate (home_id,task_id,fence,expires_at)"
                " VALUES (?,?,1,?)",
                (home, "t-" + home, self.service.now(db) + seconds),
            )

    def clear_rows(self):
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_dispatch_gate")

    def direct(self, sql, *args):
        with self.service.transaction() as db:
            db.execute(sql, args)

    def control_body(self, sensor=qs.DEFAULT):
        with self.service.transaction() as db:
            return db.execute(
                "SELECT body FROM sensor_consumer_control WHERE sensor_id=?", (sensor,)
            ).fetchone()[0]


class DirectControlWrites(GateBase):
    """F2: a direct write cannot commit while a dispatch for the home is authorised."""

    def withdraw_sql(self):
        return (
            "UPDATE sensor_consumer_control SET body=REPLACE(body,'\"granted\"','\"declined\"')"
            " WHERE sensor_id=?",
            qs.DEFAULT,
        )

    def test_direct_update_delete_and_insert_are_rejected_for_a_home_with_a_live_gate(self):
        self.put(3)
        self.live_row("ZF-1")
        body = self.control_body()
        new = json.dumps(dict(json.loads(body), sensor_id="SENS-NEW"))
        for sql, args in (
            (self.withdraw_sql()[0], (qs.DEFAULT,)),
            ("DELETE FROM sensor_consumer_control WHERE sensor_id=?", (qs.DEFAULT,)),
            (
                "INSERT INTO sensor_consumer_control (sensor_id, body) VALUES (?,?)",
                ("SENS-NEW", new),
            ),
        ):
            with self.assertRaises(Exception):  # noqa: B017 - sqlite3 and pyodbc raise different types
                self.direct(sql, *args)
            self.assertEqual(self.consent_now(), "granted")
            self.assertEqual(self.control_body(), body)

    def test_direct_write_for_another_home_or_after_the_gate_ends_commits(self):
        self.put(3)
        self.live_row("ZF-2")
        self.direct(*self.withdraw_sql())
        self.assertNotEqual(self.consent_now(), "granted")
        self.set_consent("granted")
        self.clear_rows()
        self.live_row("ZF-1", seconds=-5)
        self.direct(*self.withdraw_sql())
        self.assertNotEqual(self.consent_now(), "granted")

    def test_a_direct_withdrawal_is_rejected_while_a_non_transmitting_carrier_is_held(self):
        self.ready()
        calls = []
        real_evidence = self.provider.evidence
        self.provider.evidence = lambda *a: calls.append(a) or real_evidence(*a)
        self.service.scan()
        (tid,) = self.quality_task()
        seen = []
        real = self.service._dispatch_gate

        def factory(task):
            gate = real(task)

            def authorised():
                valid = gate()
                try:
                    self.direct(*self.withdraw_sql())
                    seen.append("committed")
                except Exception:  # noqa: BLE001 - the guard rejection is the assertion
                    seen.append("rejected")
                return valid

            authorised.release = gate.release
            return authorised

        with patch.object(self.service, "_dispatch_gate", side_effect=factory):
            self.service.execute(tid)
        self.assertEqual(seen, ["rejected"])
        self.assertEqual(len(calls), 1)
        self.assertEqual(self.consent_now(), "granted")
        self.direct(*self.withdraw_sql())
        self.assertNotEqual(self.consent_now(), "granted")

    def test_a_withdrawing_writer_that_is_open_orders_before_a_gate_request(self):
        self.put(4)
        self.add_live(10)
        self.quality_ready()
        self.service.scan()
        (tid,) = self.quality_task()
        with self.service.transaction() as db:
            task = self.service._row(db, tid)
        writer = self.service.store.assistant_connection()
        outcome = []
        try:
            writer.execute("BEGIN IMMEDIATE")
            sql, arg = self.withdraw_sql()
            writer.execute(sql, (arg,))

            def request():
                gate = ai_gate.DispatchGate(self.service, task)
                try:
                    gate()
                    outcome.append("granted")
                except ai_consumption.DispatchWithdrawn:
                    outcome.append("withdrawn")
                finally:
                    gate.release()

            thread = threading.Thread(target=request)
            thread.start()
            thread.join(1.0)
            writer.execute("COMMIT")
        finally:
            writer.close()
        thread.join(30)
        self.assertEqual(outcome, ["withdrawn"])
        self.assertEqual(self.gate_rows(), [])

    def test_configure_changes_only_changed_controls_and_old_triggers_are_upgraded(self):
        self.put(3)
        self.controls["SENS-SYN-2"] = ("ZF-2", "granted")
        self.configure()
        self.live_row("ZF-1")
        self.set_consent("declined", home="ZF-2", sensor="SENS-SYN-2")
        self.assertEqual(self.consent_now(), "granted")
        self.clear_rows()


class Fence(GateBase):
    """F1 (E2): a carrier not declared to send no bytes never receives captured readings."""

    def test_a_provider_that_cannot_be_fenced_is_never_given_captured_readings(self):
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        called = []

        def bare(system, prompt, tokens, timeout):
            called.append(prompt)
            return self.provider.evidence(system, prompt, tokens, timeout)

        self.service.provider = bare
        self.assertTrue(self.service.execute(tid))
        self.assertEqual(called, [])
        task = self.service.detail(self.pm, tid)
        self.assertNotEqual(task["state"], "ready")
        self.assertIn("manual", (task.get("reason") or "").lower())


class ManualAndProactive(GateBase):
    """F3: a person's request for another exact capture never rewrites the serviced Quality slot."""

    def serviced(self):
        self.ready()
        self.service.scan()
        (a,) = self.quality_task()
        self.assertTrue(self.service.execute(a))
        return a

    def test_a_pending_manual_request_does_not_allow_a_second_autonomous_call(self):
        a = self.serviced()
        self.add_live(5)
        b = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.assertNotEqual(a, b)
        self.add_live(4)
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(self.quality_task(), sorted([a, b]))
        self.assertEqual((self.provider.calls, self.used_calls()), (1, 1))

    def test_a_scan_between_the_manual_request_and_a_later_reading_does_not_adopt_the_manual_task(
        self,
    ):
        a = self.serviced()
        self.add_live(5)
        b = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(self.quality_task(), sorted([a, b]))
        self.add_live(4)
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(self.quality_task(), sorted([a, b]))
        self.assertEqual((self.provider.calls, self.used_calls()), (1, 1))

    def test_a_completed_manual_request_after_a_restart_does_not_allow_another_call(self):
        a = self.serviced()
        self.add_live(5)
        b = self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"]
        self.assertTrue(self.service.execute(b))
        self.add_live(4)
        restarted = self.other()
        restarted.scan_cursor = ""
        restarted.scan()
        self.assertEqual(self.quality_task(), sorted([a, b]))
        self.assertEqual((self.provider.calls, self.used_calls()), (2, 2))


class Adoption(GateBase):
    """F4: legacy history is searched within a bound; an incomplete search is not no history."""

    def legacy(self, newer):
        self.ready()
        cap = "assessment-preparation"
        self.service.scan()
        (first,) = self.assessments()
        self.assertTrue(self.service.execute(first))
        with self.service.transaction() as db:
            body = json.loads(
                db.execute("SELECT body FROM assistant_tasks WHERE id=?", (first,)).fetchone()[0]
            )
            body["dispatch"] = dict(body.get("dispatch") or {}, trigger="requested")
            for i in range(newer):
                db.execute(
                    "INSERT INTO assistant_tasks (id,capability,case_id,signature,body,state,fence,"
                    "owner,lease_until,attempts,not_before,revision,dispatched)"
                    " VALUES (?,?,?,?,?,'ready',1,'',0,1,0,?,?)",
                    (
                        f"old{i:03d}",
                        cap,
                        "ZF-1",
                        f"s{i}",
                        json.dumps(body),
                        100 + i,
                        time.time() + 10 + i,
                    ),
                )
            db.execute("DELETE FROM assistant_schedule")
        return first

    def assessments(self):
        with self.service.transaction() as db:
            rows = db.execute(
                "SELECT id FROM assistant_tasks WHERE capability='assessment-preparation'"
                " AND case_id='ZF-1' AND id NOT LIKE 'old%' ORDER BY id"
            ).fetchall()
        return [r[0] for r in rows]

    def test_more_than_one_page_of_newer_manual_tasks_does_not_hide_the_serviced_task(self):
        self.legacy(8)
        self.complete_documents("1")
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self.assessments()), 2)
        self.service.scan_cursor = ""
        self.service.scan()
        self.assertEqual(len(self.assessments()), 2)

    def test_an_exhausted_search_bound_is_explicit_blocks_autonomous_work_and_is_resolved_later(
        self,
    ):
        self.legacy(8)
        self.complete_documents("1")
        with patch.object(type(self.service), "ADOPT_PAGES", 1):
            self.service.scan_cursor = ""
            report = self.service.scan()
            self.assertIn("assessment-preparation:ZF-1", report["incomplete_history"])
            self.assertEqual(len(self.assessments()), 1)
            restarted = self.other()
            restarted.scan_cursor = ""
            restarted.scan()
            # The durable cursor lets the next scan resume and reach the serviced task.
            self.assertEqual(len(self.assessments()), 2)

    def complete_documents(self, version):
        c7.Upgrade.complete_documents(self, version)


class Coalescing(GateBase):
    """F5: the quiet interval needs unchanged evidence; continuing readings never reopen it."""

    def churn(self):
        self.ready()
        self.service.scan()
        for minute in (31, 25, 19, 13, 7):
            self.service.scan_cursor = ""
            self.service.scan()
            queued = self.pending()
            self.add_live(minute)
            for tid in queued:
                self.service.execute(tid)

    def scan_at(self, seconds, service=None):
        service = service or self.service
        with patch.object(service, "now", side_effect=lambda db=None: time.time() + seconds):
            service.scan_cursor = ""
            service.scan()

    def test_continuing_readings_across_quiet_intervals_create_no_new_work(self):
        self.churn()
        rows = self.quality_task()
        for i, minute in enumerate((6, 5, 4, 3)):
            self.add_live(minute)
            self.scan_at(400 * (i + 1))
            self.assertEqual(self.quality_task(), rows, f"scan {i}")
        self.assertEqual((self.provider.calls, self.used_calls()), (0, 0))

    def test_recovery_follows_one_unchanged_quiet_interval_even_after_a_restart(self):
        self.churn()
        rows = self.quality_task()
        self.add_live(2)
        self.scan_at(400)
        self.assertEqual(self.quality_task(), rows)
        restarted = self.other()
        self.scan_at(800, restarted)
        self.assertEqual(len(self.quality_task()), len(rows) + 1)
        (recovery,) = self.pending(restarted)
        self.assertTrue(restarted.execute(recovery))
        self.assertEqual((self.provider.calls, self.used_calls()), (1, 1))

    def test_continuing_readings_still_reach_a_finite_hard_resume(self):
        self.churn()
        rows = self.quality_task()
        minute = 6
        for i in range(1, 6):
            self.add_live(minute)
            minute -= 1
            self.scan_at(400 * i)
        self.assertEqual(len(self.quality_task()), len(rows) + 1)


class Unknown(GateBase):
    """F6: only a successfully observed current capture may assert a cited reading missing."""

    def proactive(self):
        self.ready()
        self.service.scan()
        (tid,) = self.quality_task()
        self.assertTrue(self.service.execute(tid))
        return tid

    def state_current(self, tid, state):
        with self.service.transaction() as db:
            task = self.service._row(db, tid)
        current = copy.deepcopy(task["snapshot"])
        current["sources"]["sensors"] = dict(
            state=state, readings=[], before=[], after=[], latest=None, citation_keys=[]
        )
        return task, current

    def test_unavailable_and_withheld_current_captures_compare_as_unknown(self):
        tid = self.proactive()
        for state in ("unavailable", "consent-withheld"):
            task, current = self.state_current(tid, state)
            flag = review_flag(task, actionable=True, current=current)
            self.assertIsNone(flag["changed_since_capture"], state)
            self.assertEqual(flag["cited_comparison"]["state"], "unknown")
            self.assertEqual(flag["cited_comparison"]["missing_ids"], [])
            self.assertIsNone(flag["newer_reading_count"])

    def test_a_failing_current_read_reaches_the_employee_view_as_unknown(self):
        tid = self.proactive()
        with patch.object(sensor_view, "_select", side_effect=RuntimeError("synthetic")):
            flag = self.service.detail(self.pm, tid)["review_flag"]
        self.assertIsNone(flag["changed_since_capture"])
        self.assertEqual(flag["cited_comparison"]["missing_ids"], [])
        self.assertIsNone(flag["newer_reading_count"])

    def test_an_authoritative_no_readings_capture_still_reports_missing(self):
        tid = self.proactive()
        task, current = self.state_current(tid, "no-readings")
        flag = review_flag(task, actionable=True, current=current)
        self.assertIs(flag["changed_since_capture"], True)
        self.assertTrue(flag["cited_comparison"]["missing_ids"])


MSSQL = unittest.skipUnless(
    os.environ.get("ZF_TEST_MSSQL") == "1", "needs disposable SQL Server (ZF_TEST_MSSQL=1)"
)


@MSSQL
class MssqlDirectControlWrites(ta.MssqlFixture, DirectControlWrites):
    pass


@MSSQL
class MssqlManualAndProactive(ta.MssqlFixture, ManualAndProactive):
    pass


@MSSQL
class MssqlAdoption(ta.MssqlFixture, Adoption):
    pass


@MSSQL
class MssqlCoalescing(ta.MssqlFixture, Coalescing):
    pass


if __name__ == "__main__":
    unittest.main()
