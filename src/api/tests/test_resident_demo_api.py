"""HTTP boundary of the synthetic resident showcase, over a real loopback socket.

The reader is an in-memory fake that serves constructed rows. The password is an unmistakable
fake test constant; nothing here touches SQL, Azure or a real credential.
"""

import base64
import http.client
import json
import threading
import unittest
from dataclasses import replace
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

    def call(
        self,
        method: str,
        path: str,
        body: Any = None,
        headers: dict[str, str] | None = None,
        csrf: bool = True,
        origin: bool = True,
        raw: bytes | None = None,
    ) -> tuple[int, dict[str, Any], http.client.HTTPResponse]:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        sent = {"Host": self.host}
        if self.cookies:
            sent["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        if method == "POST":
            sent["Content-Type"] = "application/json"
            if origin:
                sent["Origin"] = f"http://{self.host}"
            if csrf and demo.CSRF_COOKIE in self.cookies:
                sent[demo.CSRF_HEADER] = self.cookies[demo.CSRF_COOKIE]
        sent.update(headers or {})
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
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


class SignInTests(DemoTestCase):
    def test_login_shows_only_own_allowlisted_view(self) -> None:
        c = self.client()
        self.assertEqual(c.login("one@example.com"), 200)
        status, view, _ = c.call("GET", "/demo/view")
        self.assertEqual(status, 200)
        self.assertEqual(view["home"]["address"], "C-1 Test Street")
        self.assertEqual(view["measures"], ["Measure for C-1"])
        self.assertTrue(view["read_only"])
        self.assertEqual(
            set(view),
            {
                "banner",
                "viewer",
                "read_only",
                "home",
                "measures",
                "progress",
                "next_step",
                "unavailable",
                "help",
            },
        )
        text = json.dumps(view)
        for hidden in ("one@example.com", "two@example.com", "case_id", "C-2", "provenance"):
            self.assertNotIn(hidden, text)

    def test_email_is_canonicalised_at_login(self) -> None:
        self.assertEqual(self.client().login("  ONE@Example.COM "), 200)

    def test_wrong_password_unknown_email_and_other_domain_get_the_same_401(self) -> None:
        outcomes = set()
        for email, password in (
            ("one@example.com", "wrong"),
            ("nobody@example.com", FAKE_PASSWORD),
            ("other@example.org", FAKE_PASSWORD),
            ("", ""),
        ):
            c = self.client()
            c.prime()
            status, body, _ = c.call("POST", "/demo/login", dict(email=email, password=password))
            outcomes.add((status, body["error"]))
            self.assertNotIn(demo.SESSION_COOKIE, c.cookies)
        self.assertEqual(outcomes, {(401, demo.GENERIC_DENIAL)})

    def test_malformed_bodies_are_refused_without_a_session(self) -> None:
        for raw in (b"not json", b"[]", b'{"email": 5, "password": ["x"]}', b""):
            c = self.client()
            c.prime()
            status, _, _ = c.call("POST", "/demo/login", raw=raw)
            self.assertIn(status, (401,))
            self.assertNotIn(demo.SESSION_COOKIE, c.cookies)

    def test_login_requires_csrf_and_same_origin(self) -> None:
        c = self.client()
        c.prime()
        creds = dict(email="one@example.com", password=FAKE_PASSWORD)
        self.assertEqual(c.call("POST", "/demo/login", creds, csrf=False)[0], 403)
        self.assertEqual(c.call("POST", "/demo/login", creds, origin=False)[0], 403)
        bad = {"Origin": "http://evil.test.invalid"}
        self.assertEqual(c.call("POST", "/demo/login", creds, headers=bad)[0], 403)
        cross = {"Sec-Fetch-Site": "cross-site"}
        self.assertEqual(c.call("POST", "/demo/login", creds, headers=cross)[0], 403)
        forged = {demo.CSRF_HEADER: "forged.token"}
        self.assertEqual(c.call("POST", "/demo/login", creds, headers=forged)[0], 403)
        other = self.client()
        other.prime()
        mismatch = {demo.CSRF_HEADER: other.cookies[demo.CSRF_COOKIE]}
        self.assertEqual(c.call("POST", "/demo/login", creds, headers=mismatch)[0], 403)
        self.assertEqual(c.call("POST", "/demo/login", creds)[0], 200)

    def test_cookies_are_host_prefixed_secure_samesite_and_session_is_httponly(self) -> None:
        c = self.client()
        c.prime()
        _, _, response = c.call(
            "POST", "/demo/login", dict(email="one@example.com", password=FAKE_PASSWORD)
        )
        cookies = response.headers.get_all("Set-Cookie") or []
        self.assertEqual(len(cookies), 2)
        for line in cookies:
            self.assertTrue(line.startswith("__Host-"))
            for flag in ("Secure", "SameSite=Strict", "Path=/"):
                self.assertIn(flag, line)
            self.assertNotIn("Domain", line)
        session = next(x for x in cookies if x.startswith(demo.SESSION_COOKIE + "="))
        self.assertIn("HttpOnly", session)

    def test_content_type_and_body_size_are_enforced(self) -> None:
        c = self.client()
        c.prime()
        creds = dict(email="one@example.com", password=FAKE_PASSWORD)
        self.assertEqual(
            c.call("POST", "/demo/login", creds, headers={"Content-Type": "text/plain"})[0], 401
        )
        big = b'{"email": "' + b"a" * 5000 + b'"}'
        self.assertEqual(c.call("POST", "/demo/login", raw=big)[0], 401)
        self.assertNotIn(demo.SESSION_COOKIE, c.cookies)


class SessionTests(DemoTestCase):
    def test_no_cookie_and_forged_cookies_are_401(self) -> None:
        c = self.client()
        self.assertEqual(c.call("GET", "/demo/view")[0], 401)
        good = self.client()
        good.login("one@example.com")
        token = good.cookies[demo.SESSION_COOKIE]
        forgeries = (
            "x",
            token[:-3] + "AAA",
            token.replace("v1", "v2", 1),
            ".".join(token.split(".")[:4]),
            "v1.a.b.c.d",
            "A" * 400,
        )
        for forged in forgeries:
            f = self.client()
            f.cookies[demo.SESSION_COOKIE] = forged
            self.assertEqual(f.call("GET", "/demo/view")[0], 401, forged[:20])

    def test_other_residents_handle_in_a_forged_token_is_rejected(self) -> None:
        one = self.client()
        one.login("one@example.com")
        parts = one.cookies[demo.SESSION_COOKIE].split(".")
        parts[1] = self.codec.handle("C-2")
        swapped = self.client()
        swapped.cookies[demo.SESSION_COOKIE] = ".".join(parts)
        self.assertEqual(swapped.call("GET", "/demo/view")[0], 401)

    def test_each_resident_sees_only_their_own_case(self) -> None:
        one, two = self.client(), self.client()
        one.login("one@example.com")
        two.login("two@example.com")
        self.assertEqual(one.call("GET", "/demo/view")[1]["home"]["address"], "C-1 Test Street")
        self.assertEqual(two.call("GET", "/demo/view")[1]["home"]["address"], "C-2 Test Street")

    def test_case_ids_and_identity_are_never_in_urls_or_query_choose_nothing(self) -> None:
        one = self.client()
        one.login("one@example.com")
        for path in ("/demo/view?case=C-2", "/demo/view?email=two@example.com", "/demo/view/C-2"):
            status, body, _ = one.call("GET", path)
            if "/C-2" in path:
                self.assertEqual(status, 404)
            else:
                self.assertEqual(body["home"]["address"], "C-1 Test Street")
        spoofed = one.call(
            "GET", "/demo/view", headers={"X-Case-Id": "C-2", "X-Forwarded-User": "two"}
        )
        self.assertEqual(spoofed[1]["home"]["address"], "C-1 Test Street")

    def test_session_expires_after_thirty_minutes(self) -> None:
        c = self.client()
        c.login("one@example.com")
        self.clock.now += rs.SESSION_SECONDS - 1
        self.assertEqual(c.call("GET", "/demo/view")[0], 200)
        self.clock.now += 2
        self.assertEqual(c.call("GET", "/demo/view")[0], 401)

    def test_logout_revokes_and_replay_fails(self) -> None:
        c = self.client()
        c.login("one@example.com")
        token = c.cookies[demo.SESSION_COOKIE]
        status, _, response = c.call("POST", "/demo/logout", {})
        self.assertEqual(status, 200)
        self.assertNotIn(demo.SESSION_COOKIE, c.cookies)
        replay = self.client()
        replay.cookies[demo.SESSION_COOKIE] = token
        self.assertEqual(replay.call("GET", "/demo/view")[0], 401)

    def test_logout_needs_csrf(self) -> None:
        c = self.client()
        c.login("one@example.com")
        self.assertEqual(c.call("POST", "/demo/logout", {}, csrf=False)[0], 403)
        self.assertEqual(c.call("GET", "/demo/view")[0], 200)

    def test_restart_invalidates_every_session(self) -> None:
        c = self.client()
        c.login("one@example.com")
        token = c.cookies[demo.SESSION_COOKIE]
        self.stop()
        self.start_app(self.reader)
        again = self.client()
        again.cookies[demo.SESSION_COOKIE] = token
        self.assertEqual(again.call("GET", "/demo/view")[0], 401)

    def test_changed_database_email_denies_old_and_new_email_and_live_sessions(self) -> None:
        live = self.client()
        self.assertEqual(live.login("one@example.com"), 200)
        self.assertEqual(live.call("GET", "/demo/view")[0], 200)
        self.reader.rows["C-1"] = replace(self.reader.rows["C-1"], email="renamed@example.com")
        self.assertEqual(live.call("GET", "/demo/view")[0], 401)
        for email in ("one@example.com", "renamed@example.com"):
            self.assertEqual(self.client().login(email), 401, email)
        self.reader.rows["C-1"] = make_row("C-1", "one@example.com")
        self.assertEqual(self.client().login("one@example.com"), 200)

    def test_revoked_or_expired_case_is_denied_on_the_next_request(self) -> None:
        for change in (
            dict(revoked=True),
            dict(valid_to=NOW),
            dict(email_count=2),
            dict(provenance=" "),
        ):
            self.reader.rows["C-1"] = make_row("C-1", "one@example.com")
            c = self.client()
            self.assertEqual(c.login("one@example.com"), 200)
            self.reader.rows["C-1"] = replace(make_row("C-1", "one@example.com"), **change)
            self.assertEqual(c.call("GET", "/demo/view")[0], 401, change)
            self.assertEqual(self.client().login("one@example.com"), 401, change)
        self.reader.rows.pop("C-1")
        self.assertEqual(self.client().login("one@example.com"), 401)

    def test_database_errors_are_503_with_no_detail(self) -> None:
        c = self.client()
        c.login("one@example.com")
        self.reader.fail = True
        status, body, response = c.call("GET", "/demo/view")
        self.assertEqual(status, 503)
        self.assertEqual(body, dict(error=demo.UNAVAILABLE))
        self.assertEqual(self.client().login("one@example.com"), 503)

    def test_showcase_ends_at_expiry(self) -> None:
        c = self.client()
        c.login("one@example.com")
        self.clock.now = (NOW + timedelta(hours=6)).timestamp()
        self.assertEqual(c.call("GET", "/demo/view")[0], 503)
        self.assertEqual(c.call("GET", "/demo/session")[0], 503)
        self.assertEqual(c.call("GET", "/healthz")[0], 503)


class AbuseAndHardeningTests(DemoTestCase):
    def test_limiter_blocks_after_five_failures_and_recovers(self) -> None:
        c = self.client()
        c.prime()
        bad = dict(email="one@example.com", password="wrong")
        for _ in range(5):
            self.assertEqual(c.call("POST", "/demo/login", bad)[0], 401)
        self.assertEqual(c.call("POST", "/demo/login", bad)[0], 429)
        good = dict(email="one@example.com", password=FAKE_PASSWORD)
        self.assertEqual(c.call("POST", "/demo/login", good)[0], 429)
        self.clock.now += 700
        self.assertEqual(c.call("POST", "/demo/login", good)[0], 200)

    def test_spoofed_forwarded_headers_cannot_change_the_limiter_key(self) -> None:
        c = self.client()
        c.prime()
        bad = dict(email="one@example.com", password="wrong")
        for i in range(5):
            spoof = {"X-Forwarded-For": f"10.0.0.{i}", "Forwarded": f"for=10.0.0.{i}"}
            self.assertEqual(c.call("POST", "/demo/login", bad, headers=spoof)[0], 401)
        spoof = {"X-Forwarded-For": "203.0.113.99"}
        self.assertEqual(c.call("POST", "/demo/login", bad, headers=spoof)[0], 429)

    def ingress_login(self, forwarded: list[str], password: str = "wrong") -> int:
        c = self.client()
        c.prime()
        conn = http.client.HTTPConnection("127.0.0.1", self.app.port, timeout=10)
        conn.putrequest("POST", "/demo/login", skip_host=True, skip_accept_encoding=True)
        for name, value in (
            ("Host", HOST),
            ("Content-Type", "application/json"),
            ("Origin", f"http://{HOST}"),
            ("Cookie", "; ".join(f"{k}={v}" for k, v in c.cookies.items())),
            (demo.CSRF_HEADER, c.cookies[demo.CSRF_COOKIE]),
        ):
            conn.putheader(name, value)
        for line in forwarded:
            conn.putheader("X-Forwarded-For", line)
        body = json.dumps(dict(email="one@example.com", password=password)).encode()
        conn.putheader("Content-Length", str(len(body)))
        conn.endheaders(body)
        status = conn.getresponse().status
        conn.close()
        return status

    def test_ingress_mode_limits_each_trusted_client_separately(self) -> None:
        self.start_app(self.reader, client_address="ingress-rightmost")
        for i in range(5):
            prefix = f"198.51.100.{i}"
            self.assertEqual(self.ingress_login([f"{prefix}, 203.0.113.5"]), 401)
        self.assertEqual(self.ingress_login(["198.51.100.99", "203.0.113.5"]), 429)
        self.assertEqual(self.ingress_login(["203.0.113.5"], FAKE_PASSWORD), 429)
        self.assertEqual(self.ingress_login(["203.0.113.6"], FAKE_PASSWORD), 200)

    def test_ingress_mode_bad_header_uses_the_shared_peer_bucket(self) -> None:
        self.start_app(self.reader, client_address="ingress-rightmost")
        for _ in range(5):
            self.assertEqual(self.ingress_login(["not-an-ip"]), 401)
        self.assertEqual(self.ingress_login([]), 429)
        self.assertEqual(self.ingress_login(["203.0.113.7"], FAKE_PASSWORD), 200)

    def test_overall_cap_still_blocks_every_source_and_is_a_documented_residual(self) -> None:
        self.start_app(self.reader, client_address="ingress-rightmost")
        for i in range(60):
            self.assertEqual(self.ingress_login([f"203.0.113.{i + 10}"]), 401)
        self.assertEqual(self.ingress_login(["203.0.113.250"], FAKE_PASSWORD), 429)

    def test_host_header_must_be_allowlisted(self) -> None:
        for host in ("evil.test.invalid", "", "demo.test.invalid.evil", "127.0.0.1"):
            c = Client(self.app.port, host)
            for path in ("/", "/demo/session", "/demo/view", "/healthz"):
                self.assertEqual(c.call("GET", path)[0], 403, (host, path))
        port = f"{HOST}:{self.app.port}"
        self.assertEqual(Client(self.app.port, port).call("GET", "/demo/session")[0], 200)

    def test_security_headers_and_no_store_on_every_response(self) -> None:
        c = self.client()
        for path in ("/", "/demo.js", "/demo.css", "/demo/session", "/demo/view", "/nope"):
            _, _, response = c.call("GET", path)
            for key, value in demo.HEADERS.items():
                self.assertEqual(response.headers.get(key), value, (path, key))

    def test_assets_are_scriptless_inline_free_and_synthetic_labelled(self) -> None:
        c = self.client()
        _, _, page = c.call("GET", "/")
        html = page.headers
        self.assertIn("script-src 'self'", html["Content-Security-Policy"])
        text = (demo.WEB / "index.html").read_text()
        self.assertNotIn("onclick", text)
        self.assertNotIn("<script>", text)
        self.assertIn("Synthetic showcase", text)
        self.assertIn('autocomplete="username"', text)
        self.assertIn('autocomplete="current-password"', text)

    def test_unknown_methods_and_paths(self) -> None:
        c = self.client()
        self.assertEqual(c.call("GET", "/nope")[0], 404)
        self.assertEqual(c.call("PUT", "/demo/view", {})[0], 405)
        self.assertEqual(c.call("DELETE", "/demo/login")[0], 405)
        self.assertEqual(c.call("POST", "/demo/view", {})[0], 405)
        self.assertEqual(c.call("GET", "/resident/consent")[0], 404)

    def test_error_bodies_never_echo_input(self) -> None:
        c = self.client()
        c.prime()
        marker = "marker-should-not-echo@example.com"
        _, body, _ = c.call("POST", "/demo/login", dict(email=marker, password="x"))
        self.assertNotIn(marker, json.dumps(body))

    def test_healthz_is_ready_only_with_admitted_residents(self) -> None:
        self.assertEqual(self.client().call("GET", "/healthz")[1]["ready"], True)
        self.stop()
        self.start_app(FakeReader([make_row("C-X", "other@example.org")]))
        status, body, _ = self.client().call("GET", "/healthz")
        self.assertEqual((status, body["ready"]), (503, False))
        self.assertEqual(self.client().login("other@example.org"), 401)

    def test_concurrency_cap_returns_503_not_a_hang(self) -> None:
        held = [self.app.slots.acquire(blocking=False) for _ in range(demo.MAX_CONCURRENT)]
        self.assertTrue(all(held))
        try:
            self.assertEqual(self.client().call("GET", "/healthz")[0], 503)
        finally:
            for _ in held:
                self.app.slots.release()
        self.assertEqual(self.client().call("GET", "/healthz")[0], 200)


class BoundaryTests(unittest.TestCase):
    def test_app_does_not_import_the_loopback_preview_or_staff_surfaces(self) -> None:
        import inspect

        source = inspect.getsource(demo)
        for forbidden in (
            "resident_preview",
            "safe_start",
            "resolve_grant",
            "open_store",
            "MssqlStore",
            "zava_forward.api.server",
            "ZF_STORE",
        ):
            self.assertNotIn(forbidden, source)

    def test_main_refuses_without_configuration_and_with_mixed_staff_settings(self) -> None:
        import contextlib
        import io
        import os
        from unittest import mock

        from zava_forward.api.resident_demo import __main__ as entry

        for env in ({}, {"ZF_STORE": "mssql", "ZF_DEMO_EXPIRES_AT": "2026-11-01T00:00:00Z"}):
            err = io.StringIO()
            with mock.patch.dict(os.environ, env, clear=True), contextlib.redirect_stderr(err):
                self.assertEqual(entry.main(), 2)
            self.assertIn("Refusing to start", err.getvalue())
            self.assertNotIn("Traceback", err.getvalue())

    def test_main_refuses_expired_window_without_echoing_values(self) -> None:
        import contextlib
        import io
        import os
        from unittest import mock

        from zava_forward.api.resident_demo import __main__ as entry

        env = {
            "ZF_DEMO_EXPIRES_AT": "2020-01-01T00:00:00Z",
            "ZF_DEMO_ALLOWED_HOSTS": HOST,
            "ZF_DEMO_PASSWORD_VERIFIER": rs.make_verifier(FAKE_PASSWORD, n=2**14),
            "ZF_DEMO_SESSION_KEY": base64.urlsafe_b64encode(KEY).decode(),
            "ZF_SQL_SERVER": "db.invalid",
            "ZF_SQL_DATABASE": "d",
        }
        err = io.StringIO()
        with mock.patch.dict(os.environ, env, clear=True), contextlib.redirect_stderr(err):
            self.assertEqual(entry.main(), 2)
        self.assertNotIn(FAKE_PASSWORD, err.getvalue())
        self.assertNotIn(env["ZF_DEMO_PASSWORD_VERIFIER"], err.getvalue())


if __name__ == "__main__":
    unittest.main()
