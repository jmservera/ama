import base64
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

from properwarm import server


def principal(role):
    return base64.b64encode(json.dumps({"userId": f"u-{role}", "claims": [{"typ": "roles", "val": role}]}).encode()).decode()


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server.STORE.__init__()
        server.STORE.add_case("C-001")
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def call(self, path, body=None, role=None, key="k"):
        req = urllib.request.Request(self.base + path, data=json.dumps(body).encode() if body is not None else None)
        if role:
            req.add_header("X-MS-CLIENT-PRINCIPAL", principal(role))
        req.add_header("Idempotency-Key", key)
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            return e.code, json.load(e)

    def test_health_reports_audit_valid(self):
        self.assertEqual(self.call("/healthz")[1]["audit_valid"], True)

    def test_unauthenticated_is_401(self):
        self.assertEqual(self.call("/cases/C-001/transitions", {"to_stage": "assessment"})[0], 401)

    def test_agent_cannot_transition_over_http(self):
        code, body = self.call("/cases/C-001/transitions", {"to_stage": "assessment", "expected_version": 1}, "agent")
        self.assertEqual((code, body["error"]), (403, "forbidden_role"))

    def test_human_transition_and_agent_proposal(self):
        code, body = self.call("/cases/C-001/transitions", {"to_stage": "assessment", "expected_version": 1}, "coordinator", "http-1")
        self.assertEqual((code, body["stage"]), (200, "assessment"))
        code, body = self.call("/proposals", {"task": "extract", "case_id": "C-001", "summary": "s", "citations": ["d1"]}, "agent")
        self.assertEqual((code, body["status"]), (201, "pending"))


if __name__ == "__main__":
    unittest.main()
