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
from properwarm_mvp.timecapture import ACTIVITIES, TimeCapture, TimeCaptureOff

SAM = test_mvp.DATA["staff"][0]


class TimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "time.sqlite")

    def tearDown(self):
        self.tmp.cleanup()

    def tc(self, **env):
        return TimeCapture(self.db, env)

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
        t = self.tc(PW_TIME_CAPTURE="on", DPIA_APPROVED="DPIA-2026-007")
        t.record(SAM, "PW-1", 15, ACTIVITIES[0])
        for bad in (0, 601, "x", None):
            with self.assertRaises(ValueError):
                t.record(SAM, "PW-1", bad, ACTIVITIES[0])
        with self.assertRaises(ValueError):
            t.record(SAM, "PW-1", 5, "Watching the screen")
        self.assertEqual(len(t.mine(SAM)), 1)
        self.assertEqual(t.db.execute("SELECT dpia_ref FROM time_entry").fetchone()[0], "DPIA-2026-007")

    def test_staff_see_only_their_own_entries(self):
        t = self.tc(PW_TIME_CAPTURE="on", DPIA_APPROVED="D1")
        t.record(SAM, "PW-1", 5, ACTIVITIES[0])
        t.record(dict(code="X-9"), "PW-1", 7, ACTIVITIES[0])
        self.assertEqual([e["minutes"] for e in t.mine(SAM)], [5])

    def test_report_suppresses_small_groups_and_lists_no_person(self):
        t = self.tc(PW_TIME_CAPTURE="on", DPIA_APPROVED="D1")
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
        for env, expect in (({}, 403), (dict(PW_TIME_CAPTURE="on", DPIA_APPROVED="D1"), 200)):
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(Store(str(p)), "pw-test", TimeCapture(self.db, env))))
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            try:
                req = urllib.request.Request(base + "/api/login", json.dumps(dict(email=SAM["email"], password="pw-test")).encode())
                ck = urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0]
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
