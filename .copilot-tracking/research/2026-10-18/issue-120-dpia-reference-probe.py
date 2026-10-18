"""Failing-first probe using installed source, synthetic fixtures and loopback HTTP."""

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from zava_forward.api.server import App, make_handler
from zava_forward.api.timecapture import ACTIVITIES, TimeCapture, TimeCaptureOff
from zava_forward.core.store import Store

ENV = {
    "ZF_TIME_CAPTURE": "on",
    "DPIA_APPROVED": " yes ",
    "ZF_TIME_CONSULTATION": "C1",
    "ZF_TIME_NOTICE_APPROVED": "N1",
}
MGR = {"code": "MGR", "email": "manager@example.test", "role": "Retrofit Programme Manager"}
MGR2 = {"code": "SUP", "email": "support@example.test", "role": "Programme Support Officer"}
SAM = test_mvp.DATA["staff"][0]


class ReferenceProbe(unittest.TestCase):
    def test_real_timecapture(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unused" / "time.sqlite"
            capture = TimeCapture(env=dict(ENV), db_path=str(path))
            denied = []
            for name, action in (
                ("request", lambda: capture.request_enable(MGR)),
                ("activate", lambda: capture.activate(MGR2)),
                ("acknowledge", lambda: capture.acknowledge(SAM)),
                ("record", lambda: capture.record(SAM, "ZF-1", 10, ACTIVITIES[0])),
            ):
                try:
                    action()
                except TimeCaptureOff:
                    denied.append(name)
            status = capture.status(SAM)
            print(json.dumps({"probe": "direct", "denied": denied, "status": status,
                              "local_store_created": path.exists()}, sort_keys=True))
            self.assertEqual(denied, ["request", "activate", "acknowledge", "record"])
            self.assertFalse(status["dpia_recorded"])
            self.assertFalse(status["enabled"])
            self.assertFalse(path.exists())

    def test_existing_http(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "synthetic.json"
            data = json.loads(json.dumps(test_mvp.DATA))
            manager = next(u for u in data["staff"] if u["role"] == MGR["role"])
            support = dict(manager, **MGR2, name="Synthetic Support")
            data["staff"].append(support)
            path.write_text(json.dumps(data))
            store = Store(str(path))
            db = Path(tmp) / "unused" / "time.sqlite"
            capture = TimeCapture(env=dict(ENV), db_path=str(db))
            httpd = ThreadingHTTPServer(("127.0.0.1", 0),
                                        make_handler(App(store, "zf-test", capture)))
            worker = threading.Thread(target=httpd.serve_forever, daemon=True)
            worker.start()
            try:
                base = f"http://127.0.0.1:{httpd.server_address[1]}"

                def login(user):
                    body = json.dumps({"email": user["email"], "password": "zf-test"}).encode()
                    with urllib.request.urlopen(urllib.request.Request(base + "/api/login", body)) as response:
                        return response.headers["Set-Cookie"].split(";")[0]

                cookies = [login(user) for user in (manager, support, SAM)]
                outcomes = []
                for cookie, route, body in (
                    (cookies[0], "/api/time/request-enable", {}),
                    (cookies[1], "/api/time/enable", {}),
                    (cookies[2], "/api/time/acknowledge", {}),
                    (cookies[2], "/api/time", {"case_id": "ZF-1", "minutes": 10,
                                              "activity": ACTIVITIES[0]}),
                ):
                    request = urllib.request.Request(base + route, json.dumps(body).encode(),
                                                     headers={"Cookie": cookie})
                    try:
                        with urllib.request.urlopen(request) as response:
                            outcomes.append(response.status)
                    except urllib.error.HTTPError as error:
                        outcomes.append(error.code)
                        error.close()
                actions = [entry["action"] for entry in store.audit_entries()]
                print(json.dumps({"probe": "http", "statuses": outcomes, "audit_actions": actions,
                                  "local_store_created": db.exists()}, sort_keys=True))
                self.assertEqual(outcomes, [403, 403, 403, 403])
                self.assertFalse(db.exists())
                self.assertNotIn("time_capture_enabled", actions)
            finally:
                httpd.shutdown()
                httpd.server_close()
                worker.join()


if __name__ == "__main__":
    unittest.main(verbosity=2)
