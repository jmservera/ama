"""Synthetic resident showcase server (issue 462): fake-email sign-in over a read-only SQL view.

Separate from the staff server and from the loopback-only #444 preview, which it never imports.
Identity comes only from a signed, expiring session cookie that was issued after a password check;
no header, query or path value chooses who is viewing. Every protected request re-reads the case
row through the allowlist view and re-checks admission, so revocation and expiry apply at once.
"""

import json
import socket
import sqlite3
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
from zava_forward.core.resident_assistant import (
    Advisor,
    AssistantUnavailable,
    CaseProgress,
    FakeProvider,
    Provider,
    Topic,
    advise,
)

from . import chat
from .agenda import MANUAL, ZONE, Agenda, AgendaConflict
from .agenda import NOTICE as AGENDA_NOTICE
from .aoai import resident_key

WEB = Path(__file__).parent / "web"
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/demo.css": ("demo.css", "text/css; charset=utf-8"),
    "/demo.js": ("demo.js", "text/javascript; charset=utf-8"),
    "/assistant.js": ("assistant.js", "text/javascript; charset=utf-8"),
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
        assistant_provider: Provider | None = None,
        assistant_advisor: Advisor | None = None,
        agenda: Agenda | None = None,
    ):
        self.client_address = client_address
        self.reader, self.identity, self.verifier = reader, identity, verifier
        self.codec, self.limiter, self.allowed_hosts = codec, limiter, allowed_hosts
        self.expires_at = min(expires_at, rs.AUTHORITY_END)
        self.host, self.port, self.clock = host, port, clock
        self.slots = threading.BoundedSemaphore(MAX_CONCURRENT)
        self.by_handle = {codec.handle(case): case for case in identity.cases.values()}
        self.assistant_provider = (
            assistant_provider if assistant_provider is not None else FakeProvider()
        )
        self.assistant_advisor = assistant_advisor
        self.agenda = agenda

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
        row = self.row_for(token)
        if row is None:
            return None
        view: dict[str, Any] = rs.showcase_view(row)
        view["account"] = {"email": self.identity.email_for(row.case_id)}
        return view

    def row_for(self, token: str | None) -> rs.ShowcaseRow | None:
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
        return row


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
            held = _cookies(self.headers.get("Cookie")).get(CSRF_COOKIE)
            # Reuse a valid token so a second tab does not invalidate the first tab's sign-out.
            token = held if app.codec.csrf_ok(held, held) and held else app.codec.new_csrf()
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
            elif self.command == "POST" and path == "/demo/assistant":
                self._assistant()
            elif self.command == "POST" and path == "/demo/agenda":
                self._agenda()
            elif path in ASSETS or path in ("/demo/session", "/demo/view", "/demo/login"):
                self._json(405, dict(error="That is not allowed here."))
            elif path in ("/demo/logout", "/demo/assistant", "/demo/agenda"):
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

        def _assistant(self) -> None:
            if not (self._same_origin() and self._csrf_ok()):
                self._json(403, dict(error="Please reload the page and try again."))
                return
            session = _cookies(self.headers.get("Cookie")).get(SESSION_COOKIE)
            body = self._body()
            if (
                body is None
                or set(body) not in ({"topic", "use_record"}, {"question", "use_record"})
                or body.get("use_record") is not True
            ):
                self._json(400, dict(error="Agree to use your own record for this question."))
                return
            row = app.row_for(session)
            if row is None:
                self._json(401, dict(error="Please sign in again."))
                return
            view = rs.showcase_view(row)
            value = body.get("topic", body.get("question"))
            if not isinstance(value, str) or not 1 <= len(value.strip()) <= 500:
                self._json(400, dict(error="Choose one of the listed questions."))
                return
            if "question" in body:
                topic = chat.route(value)
            else:
                try:
                    topic = Topic(value)
                except ValueError:
                    if value not in ("home", "consents", "appointments", "regulations", "safety"):
                        self._json(400, dict(error="Choose one of the listed questions."))
                        return
                    topic = value
            try:
                case = CaseProgress(
                    view["progress"], view["next_step"], view.get("closed", ""), row.documents
                )
                signed = app.codec.verify(session)
                case_id = app.by_handle.get(signed[0]) if signed else None
                if case_id is None:
                    self._json(401, dict(error="Please sign in again."))
                    return
                advice = (
                    (
                        app.assistant_advisor.answer(topic, case, resident_key(case_id))
                        if app.assistant_advisor is not None
                        else advise(topic, case, app.assistant_provider)
                    )
                    if isinstance(topic, Topic)
                    else chat.answer(topic, view)
                )
            except AssistantUnavailable:
                print("resident assistant unavailable", file=sys.stderr)
                self._json(
                    503,
                    dict(
                        error="The assistant is unavailable. Try again or ask your housing officer."
                    ),
                )
                return
            if app.view_for(session) is None:
                self._json(401, dict(error="Please sign in again."))
                return
            self._json(
                200,
                dict(
                    answer=advice.answer,
                    sources=advice.sources,
                    label=advice.label,
                    notice=advice.notice,
                    help=advice.help,
                    action="appointments" if topic == "appointments" else None,
                    callback_search=(
                        {
                            "earliest": app.now().astimezone(ZONE).date().isoformat(),
                            "period": (
                                "morning"
                                if "morning" in value.lower().split()
                                else "afternoon"
                                if "afternoon" in value.lower().split()
                                else "any"
                            ),
                        }
                        if topic == "appointments"
                        else None
                    ),
                ),
            )

        def _agenda(self) -> None:
            if not (self._same_origin() and self._csrf_ok()):
                self._json(403, dict(error="Please reload the page and try again."))
                return
            body = self._body()
            if body is None or body.get("use_record") is not True:
                self._json(400, dict(error="Agree to use your own record for callbacks."))
                return
            action = body.get("action")
            keys = {
                "list": {"action", "use_record"},
                "find": {"action", "use_record", "earliest", "period"},
                "book": {"action", "use_record", "proposal", "confirmed"},
                "cancel": {"action", "use_record", "reference", "confirmed"},
            }
            if not isinstance(action, str) or action not in keys or set(body) != keys[action]:
                self._json(400, dict(error="Choose a listed callback action."))
                return
            if action in ("book", "cancel"):
                field = "proposal" if action == "book" else "reference"
                if (
                    body.get("confirmed") is not True
                    or not isinstance(body[field], str)
                    or not 1 <= len(body[field]) <= 100
                ):
                    self._json(400, dict(error="Confirm the specific callback action first."))
                    return
            session = _cookies(self.headers.get("Cookie")).get(SESSION_COOKIE)
            if app.view_for(session) is None:
                self._json(401, dict(error="Please sign in again."))
                return
            signed = app.codec.verify(session)
            case_id = app.by_handle.get(signed[0]) if signed else None
            if case_id is None:
                self._json(401, dict(error="Please sign in again."))
                return
            if app.agenda is None:
                self._json(503, dict(error="The local callback agenda is not connected. " + MANUAL))
                return
            owner = resident_key(case_id)

            def authorised() -> bool:
                return app.view_for(session) is not None and not app.expired

            try:
                result: dict[str, Any] = dict(notice=AGENDA_NOTICE, manual=MANUAL)
                if action == "find":
                    result["proposals"] = app.agenda.find(
                        owner,
                        app.now(),
                        body["earliest"],
                        body["period"],
                        authorised,
                    )
                elif action == "book":
                    result["booking"] = app.agenda.book(
                        owner,
                        body["proposal"],
                        app.now,
                        authorised,
                    )
                elif action == "cancel":
                    app.agenda.cancel(owner, body["reference"], authorised)
                    result["cancelled"] = True
                result["bookings"] = app.agenda.own(owner)
                if not authorised():
                    raise PermissionError
            except AgendaConflict as error:
                self._json(409, dict(error=str(error)))
                return
            except PermissionError:
                self._json(401, dict(error="Please sign in again."))
                return
            except ValueError as error:
                self._json(400, dict(error=str(error)))
                return
            except sqlite3.Error:
                print("resident callback agenda unavailable", file=sys.stderr)
                self._json(
                    503,
                    dict(
                        error="The callback result could not be confirmed. "
                        "Check your callbacks before trying again. " + MANUAL
                    ),
                )
                return
            self._json(200, result)

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
