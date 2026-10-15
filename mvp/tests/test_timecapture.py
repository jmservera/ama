import json
import os
import sqlite3
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from zavaforward_mvp.server import App, make_handler
from zava_forward.core.store import Store
from zavaforward_mvp.timecapture import ACTIVITIES, NoticeNotAcknowledged, SeparationOfDuties, TimeCapture, TimeCaptureOff

SAM = test_mvp.DATA["staff"][0]
MGR = dict(code="MGR", email="manager@example.test", role="Retrofit Programme Manager")
MGR2 = dict(code="MG2", email="support@example.test", role="Programme Support Officer")


def enable(t, requester=MGR, enabler=MGR2):
    t.request_enable(requester)
    return t.activate(enabler)


class TimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "time.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def tc(self, **env):
        return TimeCapture(env=env, db_path=self.db)

    def on(self, *users, dpia="DPIA-2026-007"):
        """Capture fully enabled (flag, DPIA, consultation) with the given users having acknowledged the notice."""
        t = self.tc(ZF_TIME_CAPTURE="on", DPIA_APPROVED=dpia, ZF_TIME_CONSULTATION="CONS-2026-02", ZF_TIME_NOTICE_APPROVED="NOTICE-2026-01")
        enable(t)
        for u in users:
            t.acknowledge(u)
        return t

    def test_off_by_default_and_nothing_is_written(self):
        t = self.tc()
        self.assertFalse(t.status()["enabled"])
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "ZF-1", 10, ACTIVITIES[0])
        with self.assertRaises(TimeCaptureOff):
            t.mine(SAM)
        self.assertFalse(os.path.exists(self.db))

    def test_flag_alone_is_refused_without_dpia(self):
        t = self.tc(ZF_TIME_CAPTURE="on")
        st = t.status()
        self.assertTrue(st["flag_on"] and not st["enabled"])
        self.assertIn("DPIA", st["reason"])
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "ZF-1", 10, ACTIVITIES[0])
        self.assertFalse(os.path.exists(self.db))

    def test_dpia_alone_does_not_switch_it_on(self):
        t = self.tc(DPIA_APPROVED="DPIA-2026-007")
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "ZF-1", 10, ACTIVITIES[0])

    def test_records_with_flag_and_dpia_reference_and_validates(self):
        t = self.on(SAM)
        t.record(SAM, "ZF-1", 15, ACTIVITIES[0])
        for bad in (0, 601, "x", None):
            with self.assertRaises(ValueError):
                t.record(SAM, "ZF-1", bad, ACTIVITIES[0])
        with self.assertRaises(ValueError):
            t.record(SAM, "ZF-1", 5, "Watching the screen")
        self.assertEqual(len(t.mine(SAM)), 1)
        self.assertEqual(sqlite3.connect(self.db).execute("SELECT dpia_ref FROM time_entry").fetchone()[0], "DPIA-2026-007")

    def test_staff_see_only_their_own_entries(self):
        x = dict(code="X-9")
        t = self.on(SAM, x, dpia="D1")
        t.record(SAM, "ZF-1", 5, ACTIVITIES[0])
        t.record(x, "ZF-1", 7, ACTIVITIES[0])
        self.assertEqual([e["minutes"] for e in t.mine(SAM)], [5])

    def test_dpia_and_flag_without_consultation_is_refused(self):
        t = self.tc(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1")
        st = t.status()
        self.assertFalse(st["enabled"])
        self.assertIn("consultation", st["reason"])
        with self.assertRaises(TimeCaptureOff):
            t.acknowledge(SAM)
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "ZF-1", 10, ACTIVITIES[0])
        self.assertFalse(os.path.exists(self.db))

    def test_notice_must_be_acknowledged_before_recording_or_listing(self):
        t = self.on()
        st = t.status(SAM)
        self.assertTrue(st["enabled"] and not st["acknowledged"])
        self.assertIn("not to rate you", st["notice"])
        with self.assertRaises(NoticeNotAcknowledged):
            t.record(SAM, "ZF-1", 10, ACTIVITIES[0])
        with self.assertRaises(NoticeNotAcknowledged):
            t.mine(SAM)
        t.acknowledge(SAM)
        t.acknowledge(SAM)
        self.assertTrue(t.status(SAM)["acknowledged"])
        t.record(SAM, "ZF-1", 10, ACTIVITIES[0])
        row = sqlite3.connect(self.db).execute("SELECT dpia_ref, consultation_ref FROM time_entry").fetchone()
        self.assertEqual(row, ("DPIA-2026-007", "CONS-2026-02"))
        self.assertEqual(sqlite3.connect(self.db).execute("SELECT COUNT(*) FROM notice_ack").fetchone()[0], 1)

    def test_acknowledgement_is_per_person_and_per_notice_version(self):
        from zavaforward_mvp import timecapture
        t = self.on(SAM)
        with self.assertRaises(NoticeNotAcknowledged):
            t.record(dict(code="OTHER"), "ZF-1", 5, ACTIVITIES[0])
        old = timecapture.NOTICE_VERSION
        try:
            timecapture.NOTICE_VERSION = "draft-2"
            with self.assertRaises(NoticeNotAcknowledged):
                t.record(SAM, "ZF-1", 5, ACTIVITIES[0])
        finally:
            timecapture.NOTICE_VERSION = old

    def test_acknowledgement_is_audited_through_the_api(self):
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        store = Store(str(p))
        env = dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1")
        enable(TimeCapture(env=env, db_path=self.db))
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "zf-test", TimeCapture(env=env, db_path=self.db))))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            ck = urllib.request.urlopen(urllib.request.Request(base + "/api/login", json.dumps(dict(email=SAM["email"], password="zf-test")).encode())).headers["Set-Cookie"].split(";")[0]
            urllib.request.urlopen(urllib.request.Request(base + "/api/time/acknowledge", b"{}", headers={"Cookie": ck}))
            self.assertIn("time_notice_acknowledged", [e["action"] for e in store.audit_entries()])
            self.assertTrue(store.verify_audit())
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_notice_approval_and_audited_enabling_are_required(self):
        env = dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1")
        t = self.tc(**env)
        with self.assertRaises(TimeCaptureOff):
            t.request_enable(MGR)
        env["ZF_TIME_NOTICE_APPROVED"] = "N1"
        t = self.tc(**env)
        self.assertIn("enabling request", t.status()["reason"])
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "ZF-1", 5, ACTIVITIES[0])
        enable(t)
        self.assertTrue(t.status()["enabled"])
        env["DPIA_APPROVED"] = "D2"
        self.assertFalse(self.tc(**env).status()["enabled"])

    def test_enabling_is_manager_only_and_audited_through_the_api(self):
        p = Path(self.tmp.name) / "zavaforward.json"
        data = json.loads(json.dumps(test_mvp.DATA))
        first = next(u for u in data["staff"] if u["role"] == "Retrofit Programme Manager")
        data["staff"].append(dict(first, code="SUP", name="Support Officer", email="support-officer@example.test", role="Programme Support Officer"))
        p.write_text(json.dumps(data))
        store = Store(str(p))
        env = dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "zf-test", TimeCapture(env=env, db_path=self.db))))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            mgr = next(u for u in test_mvp.DATA["staff"] if u["role"] == "Retrofit Programme Manager")
            nonmgr = next(u for u in test_mvp.DATA["staff"] if u["role"] not in ("Retrofit Programme Manager", "Programme Support Officer"))

            mgr2 = next(u for u in data["staff"] if u["role"] == "Programme Support Officer")

            def call(user, path):
                ck = urllib.request.urlopen(urllib.request.Request(base + "/api/login", json.dumps(dict(email=user["email"], password="zf-test")).encode())).headers["Set-Cookie"].split(";")[0]
                return urllib.request.urlopen(urllib.request.Request(base + path, b"{}", headers={"Cookie": ck}))

            def refused(user, path):
                with self.assertRaises(urllib.error.HTTPError) as cm:
                    call(user, path)
                self.assertEqual(cm.exception.code, 403)
            audited = lambda: [e["action"] for e in store.audit_entries()]
            refused(nonmgr, "/api/time/request-enable")
            refused(nonmgr, "/api/time/enable")
            refused(mgr, "/api/time/enable")
            self.assertNotIn("time_capture_enabled", audited())
            self.assertFalse(json.load(call(mgr, "/api/time/request-enable"))["enabled"])
            refused(mgr, "/api/time/enable")
            self.assertIn("time_capture_enable_requested", audited())
            self.assertNotIn("time_capture_enabled", audited())
            self.assertTrue(json.load(call(mgr2, "/api/time/enable"))["enabled"])
            entry = [e for e in store.audit_entries() if e["action"] == "time_capture_enabled"][0]
            self.assertIn("notice N1", entry["detail"])
            self.assertIn("requested by", entry["detail"])
            self.assertTrue(store.verify_audit())
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_report_suppresses_small_groups_and_lists_no_person(self):
        t = self.on(*[dict(code=f"U{i}") for i in range(5)], dpia="D1")
        for i in range(5):
            t.record(dict(code=f"U{i}"), "ZF-1", 10, ACTIVITIES[0])
        for i in range(2):
            t.record(dict(code=f"U{i}"), "ZF-1", 10, ACTIVITIES[1])
        rep = t.report()
        self.assertEqual([r["activity"] for r in rep["by_activity"]], [ACTIVITIES[0]])
        self.assertEqual(rep["by_activity"][0]["minutes"], 50)
        self.assertEqual(rep["suppressed_activities"], 1)
        self.assertNotIn("U0", json.dumps(rep))

    def test_api_disabled_then_enabled(self):
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        enable(TimeCapture(env=dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1"), db_path=self.db))
        for env, expect in (({}, 403), (dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1"), 200)):
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(Store(str(p)), "zf-test", TimeCapture(env=env, db_path=self.db))))
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            try:
                req = urllib.request.Request(base + "/api/login", json.dumps(dict(email=SAM["email"], password="zf-test")).encode())
                ck = urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0]
                if expect == 200:
                    req = urllib.request.Request(base + "/api/time", json.dumps(dict(case_id="ZF-1", minutes=10, activity=ACTIVITIES[0])).encode(), headers={"Cookie": ck})
                    with self.assertRaises(urllib.error.HTTPError) as cm:
                        urllib.request.urlopen(req)
                    self.assertEqual(cm.exception.code, 403)
                    req = urllib.request.Request(base + "/api/time/acknowledge", b"{}", headers={"Cookie": ck})
                    self.assertTrue(json.load(urllib.request.urlopen(req))["acknowledged"])
                req = urllib.request.Request(base + "/api/time", json.dumps(dict(case_id="ZF-1", minutes=10, activity=ACTIVITIES[0])).encode(), headers={"Cookie": ck})
                try:
                    code = urllib.request.urlopen(req).status
                except urllib.error.HTTPError as e:
                    code = e.code
                self.assertEqual(code, expect)
                req = urllib.request.Request(base + "/api/time/status", headers={"Cookie": ck})
                self.assertEqual(json.load(urllib.request.urlopen(req))["enabled"], expect == 200)
            finally:
                httpd.shutdown()
                httpd.server_close()

    def test_requester_cannot_enable_and_same_role_cannot_enable(self):
        t = self.tc(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1")
        with self.assertRaises(SeparationOfDuties):
            t.activate(MGR2)
        t.request_enable(MGR)
        for who in (MGR, dict(MGR2, role=MGR["role"]), dict(MGR, email="other@example.test")):
            with self.assertRaises(SeparationOfDuties):
                t.activate(who)
        self.assertFalse(t.status()["enabled"])
        self.assertIn("different role", t.status()["reason"])
        t.activate(MGR2)
        st = t.status()
        self.assertTrue(st["enabled"])
        self.assertEqual((st["requested_role"], st["activated_role"]), (MGR["role"], MGR2["role"]))

    def test_changed_references_need_a_new_request(self):
        env = dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1")
        enable(self.tc(**env))
        env["ZF_TIME_NOTICE_APPROVED"] = "N2"
        t = self.tc(**env)
        with self.assertRaises(SeparationOfDuties):
            t.activate(MGR2)


class SharedStoreTests(unittest.TestCase):
    """The record lives in the shared SQL store, not in a local file."""

    def make_store(self, tmp):
        import test_sqlstore as base
        data, db = base.seed(tmp)
        from zava_forward.core.sqlstore import SqlStore
        return SqlStore(data, db)

    ENV = dict(ZF_TIME_CAPTURE="on", DPIA_APPROVED="D1", ZF_TIME_CONSULTATION="C1", ZF_TIME_NOTICE_APPROVED="N1")

    def test_enabling_entries_and_acknowledgements_use_the_shared_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = self.make_store(tmp)
            t = TimeCapture(store, dict(self.ENV, ZF_STATE=tmp))
            self.assertIn("shared SQL store", t.status()["storage"])
            enable(t)
            t.acknowledge(SAM)
            t.acknowledge(SAM)
            t.record(SAM, "ZF-1", 10, ACTIVITIES[0])
            self.assertFalse(os.path.exists(os.path.join(tmp, "time.sqlite")))
            fresh = TimeCapture(store, dict(self.ENV, ZF_STATE=tmp))
            self.assertTrue(fresh.status(SAM)["acknowledged"])
            self.assertEqual([e["minutes"] for e in fresh.mine(SAM)], [10])
            for table, n in (("time_entry", 1), ("time_request", 1), ("time_enabled", 1), ("notice_ack", 1)):
                self.assertEqual(store.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0], n)
            self.assertEqual(len(fresh.mine(SAM)), 1)


if __name__ == "__main__":
    unittest.main()
