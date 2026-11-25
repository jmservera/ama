"""Issue 691: an unhandled handler failure answers 500 and logs a diagnosable, secret-free line."""

import http.client
import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from unittest.mock import patch

from zava_forward.core.mssqlstore import LOCK_FAILED

from test_auth import ENV, OID_SAM, Base, principal
from zava_forward.api import auth
from zava_forward.api.server import App, _Server, make_handler

SECRET = "tok-SECRET-value"
CHAT_APPROVED = {
    "CHAT_DPIA_REF": "SYNTH-DPIA-1",
    "CHAT_LAWFUL_BASIS_REF": "SYNTH-LB-1",
    "CHAT_NOTICE_REF": "SYNTH-NOTICE-1",
}


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

    def test_busy_sql_write_lock_answers_503_with_retry_after_and_names_the_cause(self) -> None:
        busy = type("ProgrammingError", (Exception,), {"__module__": "mssql_python.exceptions"})(
            f"[SQL Server]{LOCK_FAILED} {SECRET}"
        )

        def audit_fails(*_a: object, **_k: object) -> None:
            raise busy

        req = urllib.request.Request(
            self.base + "/api/retention",
            headers={
                "X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.ProgrammeManager",))  # type: ignore[no-untyped-call]
            },
        )
        with (
            patch.object(self.store, "retention_due", audit_fails),
            self.assertLogs("zava_forward.api.server", "WARNING") as logs,
        ):
            try:
                urllib.request.urlopen(req, timeout=20)
                self.fail("expected an HTTP error")
            except urllib.error.HTTPError as e:
                code, body, retry = e.code, e.read(), e.headers.get("Retry-After")
        self.assertEqual((code, retry), (503, "5"))
        self.assertNotIn(SECRET, body.decode())
        line = "\n".join(logs.output)
        for part in (
            "http-error GET /api/retention status=503",
            "cause=sql-write-lock-busy",
            "exc=ProgrammingError",
        ):
            self.assertIn(part, line)
        self.assertNotIn(SECRET, line)

    def test_retention_listing_answers_200_unrecorded_while_lock_busy(self) -> None:
        busy = self.busy_error()
        real_audit = self.store.audit
        calls: list[int] = []

        def audit_busy_once(*a: Any, **k: Any) -> Any:
            calls.append(1)
            if len(calls) == 1:
                raise busy
            return real_audit(*a, **k)

        def retention() -> tuple[int, bytes, str | None]:
            req = urllib.request.Request(
                self.base + "/api/retention",
                headers={
                    "X-MS-CLIENT-PRINCIPAL": principal(roles=("ZavaForward.ProgrammeManager",))  # type: ignore[no-untyped-call]
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    return r.status, r.read(), None
            except urllib.error.HTTPError as e:
                return e.code, e.read(), e.headers.get("Retry-After")

        with patch.object(self.store, "audit", audit_busy_once):
            first = retention()
            second = retention()
        self.assertEqual(first[0], 200)
        self.assertIs(json.loads(first[1])["recorded"], False)
        self.assertNotIn(SECRET, first[1].decode())
        self.assertEqual(second[0], 200)
        self.assertNotIn("recorded", json.loads(second[1]))
        self.assertEqual(len(calls), 2)

    def post(self, path: str, body: dict[str, Any]) -> tuple[int, bytes, str | None]:
        req = urllib.request.Request(
            self.base + path,
            data=json.dumps(body).encode(),
            headers={
                "X-MS-CLIENT-PRINCIPAL": principal(oid=OID_SAM),  # type: ignore[no-untyped-call]
                "X-ZF-CSRF": "1",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read(), None
        except urllib.error.HTTPError as e:
            return e.code, e.read(), e.headers.get("Retry-After")

    def busy_error(self) -> Exception:
        error: Exception = type(
            "ProgrammingError", (Exception,), {"__module__": "mssql_python.exceptions"}
        )(f"[SQL Server]{LOCK_FAILED} {SECRET}")
        return error

    def test_assistants_registry_busy_lock_503_retry_after_and_other_failures_logged(self) -> None:
        def listing(error: Exception) -> tuple[int, bytes, str | None, str]:
            def fails(*_a: object, **_k: object) -> None:
                raise error

            req = urllib.request.Request(
                self.base + "/api/assistants",
                headers={"X-MS-CLIENT-PRINCIPAL": principal(oid=OID_SAM)},  # type: ignore[no-untyped-call]
            )
            with (
                patch.object(self.app.assistants, "registry", fails),
                self.assertLogs("zava_forward.api.server", "WARNING") as logs,
            ):
                try:
                    urllib.request.urlopen(req, timeout=20)
                    self.fail("expected an HTTP error")
                except urllib.error.HTTPError as e:
                    return e.code, e.read(), e.headers.get("Retry-After"), "\n".join(logs.output)

        code, body, retry, line = listing(self.busy_error())
        self.assertEqual((code, retry), (503, "5"))
        self.assertIn("cause=sql-write-lock-busy", line)
        self.assertNotIn(SECRET, body.decode() + line)
        code, body, retry, line = listing(RuntimeError(SECRET))
        self.assertEqual((code, retry), (503, None))
        self.assertIn("Assistant service unavailable", body.decode())
        self.assertIn("http-error GET /api/assistants status=503 exc=RuntimeError", line)
        self.assertNotIn(SECRET, body.decode() + line)

    def test_busy_sql_write_lock_on_chat_thread_create_answers_503_with_retry_after(self) -> None:
        busy = self.busy_error()

        def create_fails(*_a: object, **_k: object) -> None:
            raise busy

        with (
            patch.dict(os.environ, CHAT_APPROVED),
            patch.object(self.store, "chat_create_thread", create_fails),
            self.assertLogs("zava_forward.api.server", "WARNING") as logs,
        ):
            code, body, retry = self.post("/api/chat/threads", {})
        self.assertEqual((code, retry), (503, "5"))
        self.assertNotIn(SECRET, body.decode())
        line = "\n".join(logs.output)
        for part in (
            "http-error POST /api/chat/threads status=503",
            "cause=sql-write-lock-busy",
        ):
            self.assertIn(part, line)
        self.assertNotIn(SECRET, line)

    def test_non_lock_driver_error_on_chat_thread_create_still_answers_500(self) -> None:
        other = type("ProgrammingError", (Exception,), {"__module__": "mssql_python.exceptions"})(
            f"Invalid object name {SECRET}"
        )

        def create_fails(*_a: object, **_k: object) -> None:
            raise other

        with (
            patch.dict(os.environ, CHAT_APPROVED),
            patch.object(self.store, "chat_create_thread", create_fails),
            self.assertLogs("zava_forward.api.server", "ERROR") as logs,
        ):
            code, body, retry = self.post("/api/chat/threads", {})
        self.assertEqual((code, retry), (500, None))
        self.assertNotIn(SECRET, body.decode())
        line = "\n".join(logs.output)
        self.assertIn("http-error POST /api/chat/threads status=500", line)
        self.assertNotIn(SECRET, line)

    def test_busy_sql_write_lock_on_other_post_still_answers_500(self) -> None:
        busy = self.busy_error()

        def add_fails(*_a: object, **_k: object) -> None:
            raise busy

        with (
            patch.dict(os.environ, CHAT_APPROVED),
            patch.object(self.store, "chat_resume", add_fails),
            self.assertLogs("zava_forward.api.server", "ERROR") as logs,
        ):
            code, _, retry = self.post("/api/chat/threads/CT-x/ask", {"content": "hello"})
        self.assertEqual((code, retry), (500, None))
        self.assertIn("status=500", "\n".join(logs.output))

    def test_other_driver_error_on_retention_still_answers_500(self) -> None:
        other = type("ProgrammingError", (Exception,), {"__module__": "mssql_python.exceptions"})(
            "Invalid object name"
        )

        def boom(*_a: object, **_k: object) -> None:
            raise other

        with (
            patch.object(self.store, "retention_due", boom),
            self.assertLogs("zava_forward.api.server", "ERROR") as logs,
        ):
            code, _ = self.get("/api/retention")
        self.assertEqual(code, 500)
        self.assertIn("status=500", "\n".join(logs.output))

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

    def test_client_disconnect_during_request_read_logs_warning_not_error(self) -> None:
        from http.server import BaseHTTPRequestHandler

        def gone(self: BaseHTTPRequestHandler) -> bool:
            raise ConnectionResetError(SECRET)

        with (
            patch.object(BaseHTTPRequestHandler, "parse_request", gone),
            self.assertLogs("zava_forward.api.server", "WARNING") as logs,
        ):
            with self.assertRaises((OSError, http.client.HTTPException)):
                self.get("/api/me")
        self.assertEqual([r.levelname for r in logs.records], ["WARNING"])
        text = "\n".join(logs.output)
        self.assertIn("client-disconnect exc=ConnectionResetError phase=request-read", text)
        self.assertNotIn("status=500", text)
        self.assertNotIn(SECRET, text)

    def test_client_reset_during_post_body_read_logs_warning_not_error(self) -> None:
        import socket
        import struct
        import time

        with self.assertLogs("zava_forward.api.server", "WARNING") as logs:
            sock = socket.create_connection(("127.0.0.1", self.httpd.server_address[1]), timeout=5)
            hdr = principal(oid=OID_SAM)  # type: ignore[no-untyped-call]
            lines = ["POST /api/bulk-edits/preview HTTP/1.1", "Host: x", "Content-Length: 500"]
            head = "\r\n".join([*lines, f"X-MS-CLIENT-PRINCIPAL: {hdr}", "", ""])
            sock.sendall(head.encode() + b"{")
            time.sleep(0.2)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
            sock.close()
            deadline = time.monotonic() + 5
            while not logs.records and time.monotonic() < deadline:
                time.sleep(0.05)
        self.assertEqual([r.levelname for r in logs.records], ["WARNING"])
        text = "\n".join(logs.output)
        self.assertIn("client-disconnect exc=ConnectionResetError phase=request-read", text)
        self.assertNotIn("status=500", text)

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
