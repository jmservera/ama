"""Shared loopback fixture for resident demo page tests: fake reader, clock, client and base case.

The password is an unmistakable fake test constant; nothing here touches SQL, Azure or a real
credential.
"""

import http.client
import json
import threading
import unittest
from datetime import UTC, datetime, timedelta
from http.server import ThreadingHTTPServer
from typing import Any

from zava_forward.core import resident_showcase as rs

from zava_forward.api.resident_demo import app as demo

FAKE_PASSWORD = "FAKE-TEST-FIXTURE-ONLY-not-a-real-demo-password"
NOW = datetime(2026, 10, 25, 12, 0, tzinfo=UTC)
HOST = "demo.test.invalid"
KEY = b"fake-session-key-for-tests-only!"


def make_row(case_id: str, email: str, **kw: Any) -> rs.ShowcaseRow:
    base: dict[str, Any] = dict(
        case_id=case_id,
        email=email,
        email_count=1,
        provenance="owner-approved test fixture",
        valid_from=NOW - timedelta(days=1),
        valid_to=NOW + timedelta(days=1),
        revoked=False,
        address=f"{case_id} Test Street",
        town="Testtown",
        postcode="TE1 1ST",
        stage="Survey",
        closed=False,
        measures=(f"Measure for {case_id}",),
    )
    base.update(kw)
    return rs.ShowcaseRow(**base)


class FakeReader:
    def __init__(self, rows: list[rs.ShowcaseRow]):
        self.rows = {r.case_id: r for r in rows}
        self.fail = False

    def list_rows(self) -> list[rs.ShowcaseRow]:
        return list(self.rows.values())

    def fetch_case(self, case_id: str) -> rs.ShowcaseRow | None:
        if self.fail:
            raise RuntimeError("database detail that must never reach a resident")
        return self.rows.get(case_id)


class Clock:
    def __init__(self) -> None:
        self.now = NOW.timestamp()

    def __call__(self) -> float:
        return self.now


class Client:
    """Minimal cookie-aware client. Secure __Host- cookies are kept by hand, as a browser would."""

    def __init__(self, port: int, host: str = HOST):
        self.port, self.host, self.cookies = port, host, {}  # type: int, str, dict[str, str]
        self.session_id: str | None = None

    def call(
        self,
        method: str,
        path: str,
        body: Any = None,
    ) -> tuple[int, dict[str, Any], http.client.HTTPResponse]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        sent = {"Host": self.host}
        if self.cookies:
            sent["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        if self.session_id is not None and path.split("?")[0] in (
            "/demo/view",
            "/demo/assistant",
            "/demo/agenda",
            "/demo/logout",
        ):
            sent[demo.SESSION_HEADER] = self.session_id
        if method == "POST":
            sent["Content-Type"] = "application/json"
            sent["Origin"] = f"http://{self.host}"
            if demo.CSRF_COOKIE in self.cookies:
                sent[demo.CSRF_HEADER] = self.cookies[demo.CSRF_COOKIE]
        data = json.dumps(body).encode() if body is not None else None
        conn.request(method, path, body=data, headers=sent)
        response = conn.getresponse()
        text = response.read()
        for line in response.headers.get_all("Set-Cookie") or []:
            name, _, rest = line.partition("=")
            value = rest.split(";")[0]
            if "Max-Age=0" in line:
                self.cookies.pop(name, None)
            else:
                self.cookies[name] = value
        conn.close()
        try:
            payload = json.loads(text)
        except ValueError:
            payload = {}
        if path in ("/demo/session", "/demo/login") and response.status == 200:
            self.session_id = payload.get("session_id")
        return response.status, payload, response

    def prime(self) -> None:
        self.call("GET", "/demo/session")

    def login(self, email: str, password: str = FAKE_PASSWORD) -> int:
        self.prime()
        return self.call("POST", "/demo/login", dict(email=email, password=password))[0]


class DemoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = Clock()
        self.reader = FakeReader(
            [
                make_row("C-1", "one@example.com"),
                make_row("C-2", "two@example.com"),
                make_row("C-X", "other@example.org"),
            ]
        )
        self.start_app(self.reader)

    def start_app(self, reader: FakeReader, key: bytes = KEY, client_address: str = "peer") -> None:
        identity = rs.build_identity_map(reader.list_rows(), NOW)
        self.codec = rs.SessionCodec(key, NOW + timedelta(hours=6), self.clock)
        self.limiter = rs.LoginLimiter(clock=self.clock)
        self.app = demo.ResidentDemo(
            reader,
            identity,
            rs.PasswordVerifier(rs.make_verifier(FAKE_PASSWORD, n=2**14)),
            self.codec,
            self.limiter,
            (HOST,),
            NOW + timedelta(hours=6),
            "127.0.0.1",
            0,
            self.clock,
            client_address,
        )
        self.server: ThreadingHTTPServer = demo.serve(self.app)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.stop)

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def client(self) -> Client:
        return Client(self.app.port)
