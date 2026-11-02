"""Issue 691: an unhandled handler failure answers 500 and logs a diagnosable, secret-free line."""

import json
import threading
import unittest
import urllib.error
import urllib.request
from collections import Counter
from unittest.mock import patch

from test_auth import ENV, OID_SAM, Base, principal
from zava_forward.api import auth
from zava_forward.api.server import App, _Server, make_handler

SECRET = "tok-SECRET-value"


class ErrorLoggingTests(Base):
    def setUp(self) -> None:
        super().setUp()
        self.app = App(self.store, provider=auth.TrustedProxyProvider(self.store, ENV))
        self.httpd = _Server(("127.0.0.1", 0), make_handler(self.app))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def get(self, path: str, oid: str = OID_SAM) -> tuple[int, bytes]:
        req = urllib.request.Request(self.base + path, headers={"X-MS-CLIENT-PRINCIPAL": principal(oid=oid)})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def test_unhandled_failure_returns_plain_500_and_logs_class_and_path_only(self) -> None:
        def boom(*_a: object, **_k: object) -> None:
            raise RuntimeError(SECRET)

        with patch.object(self.store, "counts", boom), self.assertLogs("zava_forward.api.server", "ERROR") as logs:
            code, body = self.get(f"/api/me?token={SECRET}")
        self.assertEqual(code, 500)
        self.assertIn("error", json.loads(body))
        self.assertNotIn(SECRET, body.decode())
        line = "\n".join(logs.output)
        for part in ("http-error GET /api/me status=500", "exc=RuntimeError", "at=test_error_logging.py:"):
            self.assertIn(part, line)
        self.assertNotIn(SECRET, line)
        self.assertNotIn("Traceback", line)

    def test_client_disconnect_is_logged_without_a_response(self) -> None:
        def gone(*_a: object, **_k: object) -> None:
            raise BrokenPipeError(SECRET)

        with patch.object(self.store, "counts", gone), self.assertLogs("zava_forward.api.server", "WARNING") as logs:
            with self.assertRaises(Exception):
                self.get("/api/me")
        text = "\n".join(logs.output)
        self.assertIn("client-disconnect exc=BrokenPipeError", text)
        self.assertNotIn(SECRET, text)

    def test_optional_provider_gaps_stay_clear_503s_and_denials_stay_403s(self) -> None:
        code, body = self.get("/api/account/photo")
        self.assertEqual(code, 503)
        self.assertIn("photo access is not available", json.loads(body)["error"])
        code, body = self.get("/api/law/alerts")
        data = json.loads(body)
        self.assertEqual((code, data["status"]), (503, "unknown"))
        self.assertIn("safe_route", data)
        self.assertEqual(self.get("/api/chat/regulatory/status")[0], 403)

    def test_concurrent_mixed_burst_has_no_500_or_dropped_connection(self) -> None:
        paths = ["/panels.js", "/api/me", "/api/law/alerts", "/api/account/photo", "/api/cases", "/app", "/vendor/leaflet.js"]
        seen: Counter[tuple[str, object]] = Counter()
        lock = threading.Lock()

        def hit(i: int) -> None:
            path = paths[i % len(paths)]
            try:
                result: object = self.get(path, f"dddddddd-0000-0000-0000-{i:012d}" if i % 2 else OID_SAM)[0]
            except Exception as exc:
                result = type(exc).__name__
            with lock:
                seen[(path, result)] += 1

        threads = [threading.Thread(target=hit, args=(i,)) for i in range(140)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual({r for _, r in seen} - {200, 401, 403, 503}, set(), seen)


if __name__ == "__main__":
    unittest.main()
