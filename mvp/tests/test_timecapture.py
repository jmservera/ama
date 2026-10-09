import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from properwarm_mvp.server import App, make_handler
from properwarm_mvp.store import Store
from properwarm_mvp.timecapture import ACTIVITIES, NoticeNotAcknowledged, TimeCapture, TimeCaptureOff

SAM = test_mvp.DATA["staff"][0]


class TimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "time.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def tc(self, **env):
        return TimeCapture(self.db, env)

    def on(self, *users, dpia="DPIA-2026-007"):
        """Capture fully enabled (flag, DPIA, consultation) with the given users having acknowledged the notice."""
        t = self.tc(PW_TIME_CAPTURE="on", DPIA_APPROVED=dpia, PW_TIME_CONSULTATION="CONS-2026-02")
        for u in users:
            t.acknowledge(u)
        return t

    def test_off_by_default_and_nothing_is_written(self):
        t = self.tc()
        self.assertFalse(t.status()["enabled"])
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "PW-1", 10, ACTIVITIES[0])
        with self.assertRaises(TimeCaptureOff):
            t.mine(SAM)
        self.assertFalse(os.path.exists(self.db))

    def test_flag_alone_is_refused_without_dpia(self):
        t = self.tc(PW_TIME_CAPTURE="on")
        st = t.status()
        self.assertTrue(st["flag_on"] and not st["enabled"])
        self.assertIn("DPIA", st["reason"])
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "PW-1", 10, ACTIVITIES[0])
        self.assertFalse(os.path.exists(self.db))

    def test_dpia_alone_does_not_switch_it_on(self):
        t = self.tc(DPIA_APPROVED="DPIA-2026-007")
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "PW-1", 10, ACTIVITIES[0])

    def test_records_with_flag_and_dpia_reference_and_validates(self):
        t = self.on(SAM)
        t.record(SAM, "PW-1", 15, ACTIVITIES[0])
        for bad in (0, 601, "x", None):
            with self.assertRaises(ValueError):
                t.record(SAM, "PW-1", bad, ACTIVITIES[0])
        with self.assertRaises(ValueError):
            t.record(SAM, "PW-1", 5, "Watching the screen")
        self.assertEqual(len(t.mine(SAM)), 1)
        self.assertEqual(t.db.execute("SELECT dpia_ref FROM time_entry").fetchone()[0], "DPIA-2026-007")

    def test_staff_see_only_their_own_entries(self):
        x = dict(code="X-9")
        t = self.on(SAM, x, dpia="D1")
        t.record(SAM, "PW-1", 5, ACTIVITIES[0])
        t.record(x, "PW-1", 7, ACTIVITIES[0])
        self.assertEqual([e["minutes"] for e in t.mine(SAM)], [5])

    def test_dpia_and_flag_without_consultation_is_refused(self):
        t = self.tc(PW_TIME_CAPTURE="on", DPIA_APPROVED="D1")
        st = t.status()
        self.assertFalse(st["enabled"])
        self.assertIn("consultation", st["reason"])
        with self.assertRaises(TimeCaptureOff):
            t.acknowledge(SAM)
        with self.assertRaises(TimeCaptureOff):
            t.record(SAM, "PW-1", 10, ACTIVITIES[0])
        self.assertFalse(os.path.exists(self.db))

    def test_notice_must_be_acknowledged_before_recording_or_listing(self):
        t = self.on()
        st = t.status(SAM)
        self.assertTrue(st["enabled"] and not st["acknowledged"])
        self.assertIn("not to rate you", st["notice"])
        with self.assertRaises(NoticeNotAcknowledged):
            t.record(SAM, "PW-1", 10, ACTIVITIES[0])
        with self.assertRaises(NoticeNotAcknowledged):
            t.mine(SAM)
        t.acknowledge(SAM)
        t.acknowledge(SAM)
        self.assertTrue(t.status(SAM)["acknowledged"])
        t.record(SAM, "PW-1", 10, ACTIVITIES[0])
        row = t.db.execute("SELECT dpia_ref, consultation_ref FROM time_entry").fetchone()
        self.assertEqual(row, ("DPIA-2026-007", "CONS-2026-02"))
        self.assertEqual(t.db.execute("SELECT COUNT(*) FROM notice_ack").fetchone()[0], 1)

    def test_acknowledgement_is_per_person_and_per_notice_version(self):
        from properwarm_mvp import timecapture
        t = self.on(SAM)
        with self.assertRaises(NoticeNotAcknowledged):
            t.record(dict(code="OTHER"), "PW-1", 5, ACTIVITIES[0])
        old = timecapture.NOTICE_VERSION
        try:
            timecapture.NOTICE_VERSION = "draft-2"
            with self.assertRaises(NoticeNotAcknowledged):
                t.record(SAM, "PW-1", 5, ACTIVITIES[0])
        finally:
            timecapture.NOTICE_VERSION = old

    def test_existing_database_without_consultation_column_is_migrated(self):
        import sqlite3
        db = sqlite3.connect(self.db)
        db.execute("CREATE TABLE time_entry (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, user_code TEXT NOT NULL, "
                   "case_id TEXT NOT NULL, minutes INTEGER NOT NULL, activity TEXT NOT NULL, dpia_ref TEXT NOT NULL)")
        db.commit()
        db.close()
        t = self.on(SAM)
        t.record(SAM, "PW-1", 10, ACTIVITIES[0])
        self.assertEqual(len(t.mine(SAM)), 1)

    def test_acknowledgement_is_audited_through_the_api(self):
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(test_mvp.DATA))
        store = Store(str(p))
        env = dict(PW_TIME_CAPTURE="on", DPIA_APPROVED="D1", PW_TIME_CONSULTATION="C1")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "pw-test", TimeCapture(self.db, env))))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            ck = urllib.request.urlopen(urllib.request.Request(base + "/api/login", json.dumps(dict(email=SAM["email"], password="pw-test")).encode())).headers["Set-Cookie"].split(";")[0]
            urllib.request.urlopen(urllib.request.Request(base + "/api/time/acknowledge", b"{}", headers={"Cookie": ck}))
            self.assertIn("time_notice_acknowledged", [e["action"] for e in store.audit_entries()])
            self.assertTrue(store.verify_audit())
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_report_suppresses_small_groups_and_lists_no_person(self):
        t = self.on(*[dict(code=f"U{i}") for i in range(5)], dpia="D1")
        for i in range(5):
            t.record(dict(code=f"U{i}"), "PW-1", 10, ACTIVITIES[0])
        for i in range(2):
            t.record(dict(code=f"U{i}"), "PW-1", 10, ACTIVITIES[1])
        rep = t.report()
        self.assertEqual([r["activity"] for r in rep["by_activity"]], [ACTIVITIES[0]])
        self.assertEqual(rep["by_activity"][0]["minutes"], 50)
        self.assertEqual(rep["suppressed_activities"], 1)
        self.assertNotIn("U0", json.dumps(rep))

    def test_api_disabled_then_enabled(self):
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(test_mvp.DATA))
        for env, expect in (({}, 403), (dict(PW_TIME_CAPTURE="on", DPIA_APPROVED="D1", PW_TIME_CONSULTATION="C1"), 200)):
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(Store(str(p)), "pw-test", TimeCapture(self.db, env))))
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            try:
                req = urllib.request.Request(base + "/api/login", json.dumps(dict(email=SAM["email"], password="pw-test")).encode())
                ck = urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0]
                if expect == 200:
                    req = urllib.request.Request(base + "/api/time", json.dumps(dict(case_id="PW-1", minutes=10, activity=ACTIVITIES[0])).encode(), headers={"Cookie": ck})
                    with self.assertRaises(urllib.error.HTTPError) as cm:
                        urllib.request.urlopen(req)
                    self.assertEqual(cm.exception.code, 403)
                    req = urllib.request.Request(base + "/api/time/acknowledge", b"{}", headers={"Cookie": ck})
                    self.assertTrue(json.load(urllib.request.urlopen(req))["acknowledged"])
                req = urllib.request.Request(base + "/api/time", json.dumps(dict(case_id="PW-1", minutes=10, activity=ACTIVITIES[0])).encode(), headers={"Cookie": ck})
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
