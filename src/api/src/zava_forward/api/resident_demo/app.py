"""Synthetic resident showcase server (issue 462): fake-email sign-in over a read-only SQL view.

Separate from the staff server and from the loopback-only #444 preview, which it never imports.
Identity comes only from a signed, expiring session cookie that was issued after a password check;
no header, query or path value chooses who is viewing. Every protected request re-reads the case
row through the allowlist view and re-checks admission, so revocation and expiry apply at once.
"""

import json
import socket
import sys
import threading
import time
from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlsplit

from zava_forward.core import resident_showcase as rs

WEB = Path(__file__).parent / "web"
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/demo.css": ("demo.css", "text/css; charset=utf-8"),
    "/demo.js": ("demo.js", "text/javascript; charset=utf-8"),
}
SESSION_COOKIE = "__Host-zfdemo"
CSRF_COOKIE = "__Host-zfdemo-csrf"
CSRF_HEADER = "X-CSRF-Token"
MAX_BODY = 2048
MAX_CONCURRENT = 8
SOCKET_TIMEOUT = 10
HEADERS = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Content-Security-Policy": (
        "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; "
        "connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    ),
}
GENERIC_DENIAL = "We could not sign you in with those details."
UNAVAILABLE = "The showcase is not available right now."


class Reader(Protocol):
    def list_rows(self) -> list[rs.ShowcaseRow]: ...

    def fetch_case(self, case_id: str) -> rs.ShowcaseRow | None: ...


class _Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], handler: Any):
        self.address_family = socket.AF_INET6 if ":" in address[0] else socket.AF_INET
        super().__init__(address, handler)


class ResidentDemo:
    """Everything the handler needs. Holds no password, no staff store and no row cache."""

    def __init__(
        self,
        reader: Reader,
        identity: rs.IdentityMap,
        verifier: rs.PasswordVerifier,
        codec: rs.SessionCodec,
        limiter: rs.LoginLimiter,
        allowed_hosts: tuple[str, ...],
        expires_at: datetime,
        host: str = "127.0.0.1",
        port: int = 8089,
        clock: Callable[[], float] = time.time,
        client_address: str = "peer",
    ):
        self.client_address = client_address
        self.reader, self.identity, self.verifier = reader, identity, verifier
        self.codec, self.limiter, self.allowed_hosts = codec, limiter, allowed_hosts
        self.expires_at = min(expires_at, rs.AUTHORITY_END)
        self.host, self.port, self.clock = host, port, clock
        self.slots = threading.BoundedSemaphore(MAX_CONCURRENT)
        self.by_handle = {codec.handle(case): case for case in identity.cases.values()}

    @property
    def ready(self) -> bool:
        return bool(self.identity.cases) and not self.expired

    @property
    def expired(self) -> bool:
        return bool(datetime.fromtimestamp(self.clock(), UTC) >= self.expires_at)

    def now(self) -> datetime:
        return datetime.fromtimestamp(self.clock(), UTC)

    def host_allowed(self, header: str | None) -> bool:
        if not header or len(header) > 255:
            return False
        name = header.rpartition(":")[0] if header.count(":") == 1 else header
        if name.startswith("[") and name.endswith("]"):
            name = name[1:-1]
        return name.lower() in self.allowed_hosts

    def login(self, email: Any, password: Any) -> str | None:
        """Return a session token, or None. Re-reads the case, so a revoked row cannot sign in."""
        case_id = rs.verify_login(self.verifier, self.identity, email, password)
        if case_id is None:
            return None
        row = self.reader.fetch_case(case_id)
        if row is None:
            return None
        try:
            rs.authorise(row, self.now(), case_id, self.identity.email_for(case_id))
        except rs.ShowcaseDenied:
            return None
        token: str = self.codec.issue(case_id)[0]
        return token

    def view_for(self, token: str | None) -> dict[str, Any] | None:
        found = self.codec.verify(token)
        case_id = self.by_handle.get(found[0]) if found else None
        if case_id is None:
            return None
        row = self.reader.fetch_case(case_id)
        if row is None:
            return None
        try:
            rs.authorise(row, self.now(), case_id, self.identity.email_for(case_id))
        except rs.ShowcaseDenied:
            return None
        view: dict[str, Any] = rs.showcase_view(row)
        return view


def _cookies(header: str | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (header or "")[:2048].split(";"):
        name, sep, value = part.strip().partition("=")
        if sep and name not in out:
            out[name] = value
    return out


def _set_cookie(name: str, value: str, max_age: int, http_only: bool) -> str:
    flags = "; HttpOnly" if http_only else ""
    return f"{name}={value}; Max-Age={max_age}; Path=/; Secure; SameSite=Strict{flags}"


def make_handler(app: ResidentDemo) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "ZavaResidentDemo"
        timeout = SOCKET_TIMEOUT

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send(
            self, status: int, body: bytes, ctype: str, cookies: tuple[str, ...] = ()
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            for key, value in HEADERS.items():
                self.send_header(key, value)
            for cookie in cookies:
                self.send_header("Set-Cookie", cookie)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _json(
            self, status: int, payload: Mapping[str, Any], cookies: tuple[str, ...] = ()
        ) -> None:
            body = json.dumps(payload).encode()
            self._send(status, body, "application/json; charset=utf-8", cookies)

        def _same_origin(self) -> bool:
            origin = self.headers.get("Origin")
            if not origin or urlsplit(origin).netloc != self.headers.get("Host"):
                return False
            return self.headers.get("Sec-Fetch-Site", "same-origin") == "same-origin"

        def _csrf_ok(self) -> bool:
            sent = _cookies(self.headers.get("Cookie")).get(CSRF_COOKIE)
            return bool(app.codec.csrf_ok(sent, self.headers.get(CSRF_HEADER)))

        def _body(self) -> dict[str, Any] | None:
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            length = self.headers.get("Content-Length", "")
            if ctype != "application/json" or not length.isdigit() or int(length) > MAX_BODY:
                return None
            try:
                parsed = json.loads(self.rfile.read(int(length)))
            except (ValueError, OSError):
                return None
            return parsed if isinstance(parsed, dict) else None

        def _csrf_cookie(self) -> tuple[str, str]:
            token = app.codec.new_csrf()
            return token, _set_cookie(CSRF_COOKIE, token, rs.SESSION_SECONDS, False)

        def _route(self) -> None:
            if not app.slots.acquire(blocking=False):
                self._json(503, dict(error=UNAVAILABLE))
                return
            try:
                self._dispatch()
            except (OSError, ValueError):
                pass
            except Exception as error:
                print(f"request failed: {type(error).__name__}", file=sys.stderr)
                self._json(503, dict(error=UNAVAILABLE))
            finally:
                app.slots.release()

        def _dispatch(self) -> None:
            if not app.host_allowed(self.headers.get("Host")):
                self._json(403, dict(error="This showcase does not answer on that address."))
                return
            path = self.path.split("?", 1)[0].split("#", 1)[0]
            if path == "/healthz" and self.command in ("GET", "HEAD"):
                ready = app.ready
                self._json(
                    200 if ready else 503,
                    dict(status="ok" if ready else "not-ready", synthetic=True, ready=ready),
                )
                return
            if app.expired:
                self._json(503, dict(error="This synthetic showcase has ended.", banner=rs.BANNER))
                return
            if self.command in ("GET", "HEAD") and path in ASSETS:
                name, ctype = ASSETS[path]
                self._send(200, (WEB / name).read_bytes(), ctype)
            elif self.command in ("GET", "HEAD") and path == "/demo/session":
                token, cookie = self._csrf_cookie()
                signed = app.codec.verify(_cookies(self.headers.get("Cookie")).get(SESSION_COOKIE))
                signed_in = signed is not None and signed[0] in app.by_handle
                self._json(200, dict(csrf=token, signed_in=signed_in, banner=rs.BANNER), (cookie,))
            elif self.command in ("GET", "HEAD") and path == "/demo/view":
                view = app.view_for(_cookies(self.headers.get("Cookie")).get(SESSION_COOKIE))
                if view is None:
                    self._json(401, dict(error="Please sign in again."))
                else:
                    self._json(200, view)
            elif self.command == "POST" and path == "/demo/login":
                self._login()
            elif self.command == "POST" and path == "/demo/logout":
                self._logout()
            elif path in ASSETS or path in ("/demo/session", "/demo/view", "/demo/login"):
                self._json(405, dict(error="That is not allowed here."))
            elif path == "/demo/logout":
                self._json(405, dict(error="That is not allowed here."))
            else:
                self._json(404, dict(error="Not found."))

        def _login(self) -> None:
            if not (self._same_origin() and self._csrf_ok()):
                self._json(403, dict(error="Please reload the page and try again."))
                return
            source = rs.client_key(
                self.client_address[0],
                self.headers.get_all("X-Forwarded-For") or [],
                app.client_address,
            )
            wait = app.limiter.retry_after(source)
            if wait:
                self._send(
                    429,
                    json.dumps(
                        dict(error="Too many attempts. Please wait and try again.")
                    ).encode(),
                    "application/json; charset=utf-8",
                )
                return
            body = self._body()
            token = app.login(body.get("email"), body.get("password")) if body else None
            if token is None:
                app.limiter.record_failure(source)
                self._json(401, dict(error=GENERIC_DENIAL))
                return
            csrf, csrf_cookie = self._csrf_cookie()
            session = _set_cookie(SESSION_COOKIE, token, rs.SESSION_SECONDS, True)
            self._json(200, dict(signed_in=True, csrf=csrf), (session, csrf_cookie))

        def _logout(self) -> None:
            if not (self._same_origin() and self._csrf_ok()):
                self._json(403, dict(error="Please reload the page and try again."))
                return
            app.codec.revoke(_cookies(self.headers.get("Cookie")).get(SESSION_COOKIE))
            self._json(
                200,
                dict(signed_in=False),
                (_set_cookie(SESSION_COOKIE, "", 0, True), _set_cookie(CSRF_COOKIE, "", 0, False)),
            )

        do_GET = do_HEAD = do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = _route

    return Handler


def serve(app: ResidentDemo) -> _Server:
    server = _Server((app.host, app.port), make_handler(app))
    app.port = server.server_address[1]
    return server
