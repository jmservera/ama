"""Issue 691: an unhandled handler failure answers 500 and logs a diagnosable, secret-free line."""

import http.client
import json
import threading
import unittest
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from unittest.mock import patch

from test_auth import ENV, OID_SAM, Base, principal
from zava_forward.api import auth
from zava_forward.api.server import App, _Server, make_handler

SECRET = "tok-SECRET-value"


class ErrorLoggingTests(Base):
    def setUp(self) -> None:
        super().setUp()  # type: ignore[no-untyped-call]
        self.app = App(  # type: ignore[no-untyped-call]
            self.store,
            provider=auth.TrustedProxyProvider(self.store, ENV),  # type: ignore[no-untyped-call]
        )
        self.httpd = _Server(("127.0.0.1", 0), make_handler(self.app))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()  # type: ignore[no-untyped-call]

    def get(self, path: str, oid: str = OID_SAM) -> tuple[int, bytes]:
        req = urllib.request.Request(
            self.base + path,
            headers={"X-MS-CLIENT-PRINCIPAL": principal(oid=oid)},  # type: ignore[no-untyped-call]
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def test_unhandled_failure_returns_plain_500_and_logs_class_and_path_only(self) -> None:
        def boom(*_a: object, **_k: object) -> None:
            raise RuntimeError(SECRET)

        with (
            patch.object(self.store, "counts", boom),
            self.assertLogs("zava_forward.api.server", "ERROR") as logs,
        ):
            code, body = self.get(f"/api/me?token={SECRET}")
        self.assertEqual(code, 500)
        self.assertIn("error", json.loads(body))
        self.assertNotIn(SECRET, body.decode())
        line = "\n".join(logs.output)
        for part in (
            "http-error GET /api/me status=500",
            "exc=RuntimeError",
            "at=test_error_logging.py:",
        ):
            self.assertIn(part, line)
        self.assertNotIn(SECRET, line)
        self.assertNotIn("Traceback", line)

    def test_failure_between_send_response_and_end_headers_still_yields_plain_500(self) -> None:
        from http.server import BaseHTTPRequestHandler

        real, calls = BaseHTTPRequestHandler.send_header, []

        def broken(self: BaseHTTPRequestHandler, *a: Any, **k: Any) -> None:
            calls.append(a)
            if len(calls) == 1:
                raise RuntimeError(SECRET)
            real(self, *a, **k)

        with (
            patch.object(self.store, "counts", lambda *a, **k: None),
            patch("zava_forward.api.server.SECURITY", {"X-Test": "1"}),
            patch.object(BaseHTTPRequestHandler, "send_header", broken),
            self.assertLogs("zava_forward.api.server", "ERROR") as logs,
        ):
            code, body = self.get("/api/me")
        self.assertEqual(code, 500)
        self.assertIn("response_started=False", "\n".join(logs.output))

    def test_backend_connection_error_before_response_returns_500_and_is_logged(self) -> None:
        def reset(*_a: object, **_k: object) -> None:
            raise ConnectionResetError(SECRET)

        with (
            patch.object(self.store, "counts", reset),
            self.assertLogs("zava_forward.api.server", "ERROR") as logs,
        ):
            code, body = self.get("/api/me")
        self.assertEqual(code, 500)
        self.assertNotIn(SECRET, body.decode())
        text = "\n".join(logs.output)
        self.assertIn("exc=ConnectionResetError", text)
        self.assertIn("response_started=False", text)
        self.assertNotIn(SECRET, text)

    def test_socket_write_error_after_response_started_stays_silent(self) -> None:
        from http.server import BaseHTTPRequestHandler

        def gone(self: BaseHTTPRequestHandler) -> None:
            raise BrokenPipeError(SECRET)

        with (
            patch.object(self.store, "counts", lambda *a, **k: None),
            patch.object(BaseHTTPRequestHandler, "end_headers", gone),
            self.assertLogs("zava_forward.api.server", "WARNING") as logs,
        ):
            with self.assertRaises((OSError, http.client.HTTPException)):
                self.get("/api/me")
        text = "\n".join(logs.output)
        self.assertIn("client-disconnect exc=BrokenPipeError", text)
        self.assertNotIn("status=500", text)
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
        paths = [
            "/panels.js",
            "/api/me",
            "/api/law/alerts",
            "/api/account/photo",
            "/api/cases",
            "/app",
            "/vendor/leaflet.js",
        ]
        seen: Counter[tuple[str, object]] = Counter()
        lock = threading.Lock()

        def hit(i: int) -> None:
            path = paths[i % len(paths)]
            try:
                result: object = self.get(
                    path, f"dddddddd-0000-0000-0000-{i:012d}" if i % 2 else OID_SAM
                )[0]
            except Exception as exc:
                result = type(exc).__name__
            with lock:
                seen[(path, result)] += 1

        with ThreadPoolExecutor(max_workers=16) as pool:
            list(pool.map(hit, range(140)))
        self.assertEqual({r for _, r in seen} - {200, 401, 403, 503}, set(), seen)


if __name__ == "__main__":
    unittest.main()
