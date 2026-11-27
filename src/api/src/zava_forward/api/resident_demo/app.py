"""Synthetic resident showcase server (issue 462): fake-email sign-in over a read-only SQL view.

Separate from the staff server and from the loopback-only #444 preview, which it never imports.
Identity comes only from a signed, expiring session cookie that was issued after a password check;
no header, query or path value chooses who is viewing. Every protected request re-reads the case
row through the allowlist view and re-checks admission, so revocation and expiry apply at once.
"""

import json
import re
import secrets
import socket
import sqlite3
import sys
import threading
import time
from collections.abc import Callable, Mapping
from dataclasses import replace
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlsplit

from zava_forward.core import resident_journey_design as rjd
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

from zava_forward.api.listener import NonBlockingAcceptMixin
from zava_forward.api.static_assets import StaticAssets

from . import chat
from . import sensor_consent as sc
from .agenda import MANUAL, ZONE, Agenda, AgendaConflict
from .agenda import NOTICE as AGENDA_NOTICE
from .aoai import resident_key
from .chat_log import ChatLog
from .sensor_consent import ConsentPort

WEB = Path(__file__).parent / "web"
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/demo.css": ("demo.css", "text/css; charset=utf-8"),
    "/demo.js": ("demo.js", "text/javascript; charset=utf-8"),
    "/assistant.js": ("assistant.js", "text/javascript; charset=utf-8"),
}
SHARED_ASSETS = {
    "/chat-widget.js": ("chat-widget.js", "text/javascript; charset=utf-8"),
    "/chat-widget.css": ("chat-widget.css", "text/css; charset=utf-8"),
}
SHARED_WEB = Path(__file__).parent.parent / "web"
SESSION_COOKIE = "__Host-zfdemo"
CSRF_COOKIE = "__Host-zfdemo-csrf"
CSRF_HEADER = "X-CSRF-Token"
SESSION_HEADER = "X-Resident-Session"
MAX_BODY = 2048
# Decision (#1054): keep 8. One replica serves a short demonstration; the cap bounds load and sheds
# the rest with Retry-After; the page retries a shed view once.
MAX_CONCURRENT = 8
SOCKET_TIMEOUT = 10
HEADERS = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Strict-Transport-Security": "max-age=31536000",
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
BUSY = (
    "The showcase is busy because several people are viewing it at once. "
    "Nothing is wrong with your case. Try again in a few seconds."
)
MIN_RETRY_AFTER_SECONDS = 1
MAX_RETRY_AFTER_SECONDS = 10
RETRY_AFTER_SECONDS = 3


def clamp_retry_after(seconds: object) -> int:
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise ValueError("retry_after_seconds must be an integer")
    return max(MIN_RETRY_AFTER_SECONDS, min(MAX_RETRY_AFTER_SECONDS, seconds))


class Reader(Protocol):
    def list_rows(self) -> list[rs.ShowcaseRow]: ...

    def fetch_case(self, case_id: str) -> rs.ShowcaseRow | None: ...


class _Server(NonBlockingAcceptMixin, ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 128

    def __init__(self, address: tuple[str, int], handler: Any):
        self.address_family = socket.AF_INET6 if ":" in address[0] else socket.AF_INET
        super().__init__(address, handler)


CALLBACKS_OFF = (
    "Synthetic callback booking is not connected in this showcase, so I cannot find "
    "or book callback times. Nobody will call you."
)


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
        chat_log: ChatLog | None = None,
        sensor_consent: ConsentPort | None = None,
        retry_after_seconds: int = RETRY_AFTER_SECONDS,
        representative_grants: tuple[rs.RepresentativeShowcaseGrant, ...] = (),
    ):
        self.client_address = client_address
        self.reader, self.identity, self.verifier = reader, identity, verifier
        self.codec, self.limiter, self.allowed_hosts = codec, limiter, allowed_hosts
        self.expires_at = min(expires_at, rs.AUTHORITY_END)
        self.host, self.port, self.clock = host, port, clock
        self.retry_after_seconds = clamp_retry_after(retry_after_seconds)
        self.slots = threading.BoundedSemaphore(MAX_CONCURRENT)
        self.by_handle = {codec.handle(case): case for case in identity.cases.values()}
        self._rep_by_email: dict[str, str] = {}
        self.rep_by_handle: dict[str, rs.RepresentativeShowcaseGrant] = {}
        self.rep_sessions = rjd.RepresentativeSessionStore()
        for grant in representative_grants:
            self.register_representative_grant(grant)
        self.assistant_provider = (
            assistant_provider if assistant_provider is not None else FakeProvider()
        )
        self.assistant_advisor = assistant_advisor
        self.agenda = agenda
        self.chat_log = chat_log
        self.sensor_consent = sensor_consent

    def register_representative_grant(self, grant: rs.RepresentativeShowcaseGrant) -> None:
        """Admit or update a task-limited representative grant under its disjoint session handle."""
        email = rs.admit_representative_grant(grant)
        if email in self.identity.cases:
            raise rs.ShowcaseConfigError("Representative showcase email collides with a resident.")
        handle = self.codec.handle(grant.principal_subject)
        if handle in self.by_handle:
            raise rs.ShowcaseConfigError("Representative showcase handle collides with a resident.")
        self._rep_by_email[email] = handle
        self.rep_by_handle[handle] = grant

    @property
    def ready(self) -> bool:
        return bool(self.identity.cases or self.rep_by_handle) and not self.expired

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

    def _is_representative_token(self, token: str | None) -> bool:
        found = self.codec.verify(token)
        return found is not None and found[0] in self.rep_by_handle

    def _sync_rep_session(
        self,
        session_id: str,
        grant: rs.RepresentativeShowcaseGrant,
        row: rs.ShowcaseRow | None,
    ) -> tuple[rjd.AuthorityEvaluation, dict[str, Any]]:
        now_utc = self.now()
        stamp = rjd.format_iso_utc(now_utc)
        if row is None:
            exp_dt = rjd.parse_iso_utc(grant.expires_at) if grant.expires_at is not None else None
            exp_iso = rjd.format_iso_utc(exp_dt) if exp_dt is not None else None
            clean_ref = rjd.valid_representative_ref(grant.representative_ref) or ""
            ev = rjd.AuthorityEvaluation(
                state="held",
                active=False,
                reason="missing_authority",
                representative_ref=clean_ref,
                expires_at=exp_iso,
            )
            view = rjd.held_or_expired_view(
                representative_ref=clean_ref,
                state="held",
                reason="missing_authority",
                expires_at=exp_iso,
            )
            view["banner"] = rs.BANNER
        else:
            ev = rs.representative_grant_evaluation(grant, row, now_utc)
            view = rs.representative_showcase_view(grant, row, now_utc)
            if ev.active:
                view["callbacks_available"] = self.agenda is not None and "Communicate" in ev.tasks
        prior = self.rep_sessions.get(session_id)
        resolved_exp = (
            ev.expires_at
            if ev.expires_at is not None
            else (prior.expires_at if prior is not None else None)
        )
        tracked = rjd.RepresentativeSession(
            session_id=session_id,
            case_id=grant.case_id,
            representative_ref=ev.representative_ref,
            state=ev.state,
            reason=ev.reason,
            expires_at=resolved_exp,
            journey_stages=tuple(view["journey_stages"]),
            permitted_actions=tuple(view["permitted_actions"]),
            updated_at=stamp,
        )
        self.rep_sessions.record_session(tracked)
        if view.get("expires_at") is None and resolved_exp is not None:
            view["expires_at"] = resolved_exp
            if isinstance(view.get("renewal_route"), Mapping):
                route = dict(view["renewal_route"])
                route["recorded_expires_at"] = resolved_exp
                view["renewal_route"] = route
        view["session"] = tracked.snapshot()
        return ev, view

    def _live_grant_for_handle(
        self,
        handle: str,
    ) -> rs.RepresentativeShowcaseGrant | None:
        grant_loader = getattr(self.reader, "list_representative_grants", None)
        if callable(grant_loader):
            for candidate in grant_loader():
                if (
                    isinstance(candidate, rs.RepresentativeShowcaseGrant)
                    and self.codec.handle(candidate.principal_subject) == handle
                ):
                    return candidate
            cached = self.rep_by_handle.get(handle)
            if cached is not None:
                return replace(cached, status="Missing")
        return self.rep_by_handle.get(handle)

    def representative_state_for(
        self, token: str | None
    ) -> (
        tuple[
            rs.RepresentativeShowcaseGrant,
            rs.ShowcaseRow | None,
            rjd.AuthorityEvaluation,
            dict[str, Any],
        ]
        | None
    ):
        found = self.codec.verify(token)
        if found is None:
            return None
        grant = self._live_grant_for_handle(found[0])
        if grant is None:
            return None
        row = self.reader.fetch_case(grant.case_id)
        ev, view = self._sync_rep_session(found[1], grant, row)
        return grant, row, ev, view

    def representative_active(self, token: str | None) -> bool:
        state = self.representative_state_for(token)
        return state is not None and state[2].active

    def login(self, email: Any, password: Any) -> str | None:
        """Return a session token, or None. Re-reads the case, so a revoked row cannot sign in."""
        password_ok = self.verifier.verify(password if isinstance(password, str) else "")
        case_id = self.identity.case_for(email) if isinstance(email, str) else None
        if password_ok and case_id is not None:
            row = self.reader.fetch_case(case_id)
            if row is None:
                return None
            try:
                rs.authorise(row, self.now(), case_id, self.identity.email_for(case_id))
            except rs.ShowcaseDenied:
                return None
            token: str = self.codec.issue(case_id)[0]
            return token
        canonical = rs.canonical_email(email) if isinstance(email, str) else None
        rep_handle = self._rep_by_email.get(canonical) if canonical else None
        if password_ok and rep_handle is not None:
            grant = self.rep_by_handle.get(rep_handle)
            if grant is None:
                return None
            row = self.reader.fetch_case(grant.case_id)
            if row is None:
                return None
            ev = rs.representative_grant_evaluation(grant, row, self.now())
            if not ev.active:
                return None
            rep_token, session_id = self.codec.issue(grant.principal_subject)
            self._sync_rep_session(session_id, grant, row)
            return str(rep_token)
        return None

    def view_for(self, token: str | None) -> dict[str, Any] | None:
        row = self.row_for(token)
        if row is None:
            return None
        view: dict[str, Any] = rs.showcase_view(row, self.now())
        view["account"] = {"email": self.identity.email_for(row.case_id)}
        view["agenda_available"] = self.agenda is not None
        view["callbacks_available"] = view["agenda_available"]
        view["sensor_consent"] = sc.card(self.sensor_consent, row.sensor_home_id)
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
    assets = StaticAssets(
        {
            **{url: (WEB / name, ctype) for url, (name, ctype) in ASSETS.items()},
            **{url: (SHARED_WEB / name, ctype) for url, (name, ctype) in SHARED_ASSETS.items()},
        }
    )

    class Handler(BaseHTTPRequestHandler):
        server_version = "ZavaResidentDemo"
        sys_version = ""
        timeout = SOCKET_TIMEOUT

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send(
            self,
            status: int,
            body: bytes,
            ctype: str,
            cookies: tuple[str, ...] = (),
            extra: Mapping[str, str] | None = None,
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            if status != 304:
                self.send_header("Content-Length", str(len(body)))
            for key, value in {**HEADERS, **(extra or {})}.items():
                self.send_header(key, value)
            for cookie in cookies:
                self.send_header("Set-Cookie", cookie)
            self.end_headers()
            if self.command != "HEAD" and status != 304:
                self.wfile.write(body)

        def _json(
            self, status: int, payload: Mapping[str, Any], cookies: tuple[str, ...] = ()
        ) -> None:
            body = json.dumps(payload).encode()
            self._send(status, body, "application/json; charset=utf-8", cookies)

        def _same_origin(self) -> bool:
            origin = self.headers.get("Origin")
            if not origin:
                return False
            try:
                netloc = urlsplit(origin).netloc
            except ValueError:
                return False
            if netloc != self.headers.get("Host"):
                return False
            return self.headers.get("Sec-Fetch-Site", "same-origin") == "same-origin"

        def _csrf_ok(self) -> bool:
            sent = _cookies(self.headers.get("Cookie")).get(CSRF_COOKIE)
            return bool(app.codec.csrf_ok(sent, self.headers.get(CSRF_HEADER)))

        def _session_bound(self) -> bool:
            signed = app.codec.verify(_cookies(self.headers.get("Cookie")).get(SESSION_COOKIE))
            if signed is None:
                self._json(401, dict(error="Please sign in again."))
                return False
            values = self.headers.get_all(SESSION_HEADER) or []
            if (
                len(values) != 1
                or re.fullmatch(r"[0-9a-f]{16}", values[0]) is None
                or not secrets.compare_digest(values[0], signed[1])
            ):
                self._json(
                    409,
                    dict(
                        error="Your sign-in changed. Please sign in again.",
                        session_changed=True,
                    ),
                )
                return False
            return True

        def _body(self) -> dict[str, Any] | None:
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            length = self.headers.get("Content-Length", "")
            if (
                ctype != "application/json"
                or not (length.isascii() and length.isdigit())
                or len(length) > len(str(MAX_BODY))
                or int(length) > MAX_BODY
            ):
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
                wait = app.retry_after_seconds
                self._send(
                    503,
                    json.dumps(dict(error=BUSY, retry_after_seconds=wait)).encode(),
                    "application/json; charset=utf-8",
                    extra={"Retry-After": str(wait)},
                )
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
            asset = assets.get(path)
            if self.command in ("GET", "HEAD") and asset is not None:
                status = 304 if asset.not_modified(self.headers.get("If-None-Match")) else 200
                self._send(
                    status,
                    b"" if status == 304 else asset.body,
                    asset.content_type,
                    extra=asset.headers(urlsplit(self.path).query),
                )
            elif self.command in ("GET", "HEAD") and path == "/demo/session":
                token, cookie = self._csrf_cookie()
                raw_session = _cookies(self.headers.get("Cookie")).get(SESSION_COOKIE)
                signed = app.codec.verify(raw_session)
                rep_state = (
                    app.representative_state_for(raw_session) if signed is not None else None
                )
                if rep_state is not None and signed is not None:
                    _, _, ev, rep_view = rep_state
                    payload: dict[str, Any] = dict(
                        csrf=token,
                        authenticated=True,
                        active=ev.active,
                        signed_in=ev.active,
                        session_id=signed[1],
                        banner=rs.BANNER,
                        principal_kind="representative",
                        viewer_kind="representative",
                        state=ev.state,
                        expires_at=rep_view["expires_at"],
                        journey_stages=rep_view["journey_stages"],
                        permitted_actions=rep_view["permitted_actions"],
                        authority_scope=rep_view["authority_scope"],
                    )
                    if not ev.active:
                        payload["reason"] = ev.reason
                        payload["notice"] = rep_view["notice"]
                        payload["renewal_route"] = rep_view["renewal_route"]
                    self._json(200, payload, (cookie,))
                else:
                    signed_in = signed is not None and signed[0] in app.by_handle
                    agenda_available = app.agenda is not None
                    self._json(
                        200,
                        dict(
                            csrf=token,
                            signed_in=signed_in,
                            session_id=signed[1] if signed_in and signed else None,
                            banner=rs.BANNER,
                            agenda_available=agenda_available,
                            callbacks_available=agenda_available,
                        ),
                        (cookie,),
                    )
            elif self.command in ("GET", "HEAD") and path == "/demo/view":
                if not self._session_bound():
                    return
                raw_session = _cookies(self.headers.get("Cookie")).get(SESSION_COOKIE)
                rep_state = app.representative_state_for(raw_session)
                if rep_state is not None:
                    _, _, ev, rep_view = rep_state
                    self._json(200 if ev.active else 403, rep_view)
                else:
                    view = app.view_for(raw_session)
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
            elif self.command == "POST" and path == "/demo/sensor-consent":
                self._sensor_consent()
            elif path in ASSETS or path in ("/demo/session", "/demo/view", "/demo/login"):
                self._json(405, dict(error="That is not allowed here."))
            elif path in (
                "/demo/logout",
                "/demo/assistant",
                "/demo/agenda",
                "/demo/sensor-consent",
            ):
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
            signed = app.codec.verify(token)
            if signed is None:
                self._json(401, dict(error=GENERIC_DENIAL))
                return
            self._json(
                200,
                dict(signed_in=True, csrf=csrf, session_id=signed[1]),
                (session, csrf_cookie),
            )

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
            if not self._session_bound():
                return
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

            rep_state = app.representative_state_for(session)
            signed = app.codec.verify(session)
            if rep_state is not None:
                grant, rep_row, ev, rep_view = rep_state
                if not ev.active or rep_row is None:
                    blocked = rjd.RepresentativeAccessBlockedError(
                        state=ev.state,
                        reason=ev.reason,
                        expires_at=rep_view["expires_at"],
                        renewal_route=rep_view["renewal_route"],
                    )
                    self._json(403, blocked.to_payload())
                    return
                topic_key = topic.value if isinstance(topic, Topic) else str(topic)
                if topic_key not in rjd.allowed_assistant_topics(ev.tasks):
                    denied = rjd.RepresentativeScopeDeniedError(
                        action=f"assistant:{topic_key}",
                        expires_at=rep_view["expires_at"],
                        permitted_actions=rep_view["permitted_actions"],
                    )
                    self._json(403, denied.to_payload())
                    return
                view = rep_view
                docs = grant.documents
                principal_id: str | None = grant.principal_subject
                callbacks_permitted = "Communicate" in ev.tasks
            else:
                row = app.row_for(session)
                if row is None:
                    self._json(401, dict(error="Please sign in again."))
                    return
                view = rs.showcase_view(row, app.now())
                docs = row.documents
                principal_id = app.by_handle.get(signed[0]) if signed else None
                callbacks_permitted = True

            if principal_id is None:
                self._json(401, dict(error="Please sign in again."))
                return
            try:
                case = CaseProgress(
                    view.get("progress", ""),
                    view.get("next_step", ""),
                    view.get("closed", ""),
                    docs,
                )
                if (
                    "question" in body
                    and topic is not Topic.DOCUMENTS
                    and (isinstance(topic, Topic) or topic in ("home", "repair"))
                ):
                    base = (
                        advise(topic, case, FakeProvider())
                        if isinstance(topic, Topic)
                        else chat.answer(
                            topic, view, value, callbacks_available=app.agenda is not None
                        )
                    )
                    advice = (
                        app.assistant_advisor.answer_question(
                            value.strip(), case, resident_key(principal_id), base
                        )
                        if app.assistant_advisor is not None
                        else replace(base, label="Summary by rules - AI is not enabled")
                    )
                else:
                    advice = (
                        (
                            app.assistant_advisor.answer(topic, case, resident_key(principal_id))
                            if app.assistant_advisor is not None
                            else advise(topic, case, app.assistant_provider)
                        )
                        if isinstance(topic, Topic)
                        else chat.answer(
                            topic,
                            view,
                            value if "question" in body else "",
                            callbacks_available=app.agenda is not None,
                        )
                    )
                    if (
                        "question" in body
                        and topic is Topic.DOCUMENTS
                        and app.assistant_advisor is None
                        and not app.assistant_provider.ai
                    ):
                        advice = replace(advice, label="Summary by rules - AI is not enabled")
                advice = chat.with_pause_note(advice, topic, view)
                callbacks = (
                    topic == "appointments" and app.agenda is not None and callbacks_permitted
                )
                if topic == "appointments" and not callbacks:
                    advice = replace(
                        advice,
                        answer=CALLBACKS_OFF + " " + MANUAL,
                        sources=("Showcase limit: synthetic callback booking is not connected",),
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
            if rep_state is not None:
                after = app.representative_state_for(session)
                if after is None:
                    self._json(401, dict(error="Please sign in again."))
                    return
                _, _, after_ev, after_view = after
                if not after_ev.active:
                    blocked = rjd.RepresentativeAccessBlockedError(
                        state=after_ev.state,
                        reason=after_ev.reason,
                        expires_at=after_view["expires_at"],
                        renewal_route=after_view["renewal_route"],
                    )
                    self._json(403, blocked.to_payload())
                    return
            elif app.view_for(session) is None:
                self._json(401, dict(error="Please sign in again."))
                return
            if app.chat_log is not None and signed is not None:
                try:
                    app.chat_log.record(
                        app.now(),
                        signed[1],
                        chat.outcome(value, topic) if "question" in body else str(topic),
                        app.assistant_advisor is not None or app.assistant_provider.ai,
                        value if "question" in body else "",
                    )
                except (sqlite3.Error, OSError, ValueError):
                    print("chat learning record unavailable", file=sys.stderr)
            self._json(
                200,
                dict(
                    answer=advice.answer,
                    sources=advice.sources,
                    label=advice.label,
                    routing=chat.routing(topic),
                    notice=advice.notice,
                    help=advice.help,
                    action="appointments" if callbacks else None,
                    callback_search=(
                        {
                            "earliest": app.now().astimezone(ZONE).date().isoformat(),
                            "period": (
                                "morning"
                                if "morning" in chat.words(value)
                                else "afternoon"
                                if "afternoon" in chat.words(value)
                                else "any"
                            ),
                        }
                        if callbacks
                        else None
                    ),
                ),
            )

        def _sensor_consent(self) -> None:
            if not (self._same_origin() and self._csrf_ok()):
                self._json(403, dict(error="Please reload the page and try again."))
                return
            body = self._body()
            if body is None or set(body) != {"granted"} or type(body["granted"]) is not bool:
                self._json(400, dict(error="Tick or untick the sensor consent box."))
                return
            if not self._session_bound():
                return
            session = _cookies(self.headers.get("Cookie")).get(SESSION_COOKIE)
            row = None if app.representative_state_for(session) else app.row_for(session)
            if row is None or not row.sensor_home_id:
                self._json(403, dict(error="Only the resident can change this choice."))
                return
            if app.sensor_consent is None:
                self._json(503, dict(error=sc.ERROR_TEXT))
                return
            try:
                sc.apply(app.sensor_consent, row.sensor_home_id, row.case_id, body["granted"])
            except Exception as error:
                code = error.args[0] if error.args and isinstance(error.args[0], str) else ""
                print(
                    f"sensor consent write failed: {type(error).__name__} {code[:40]}",
                    file=sys.stderr,
                )
                self._json(503, dict(error=sc.ERROR_TEXT))
                return
            self._json(200, dict(sensor_consent=sc.card(app.sensor_consent, row.sensor_home_id)))

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
            if not self._session_bound():
                return
            session = _cookies(self.headers.get("Cookie")).get(SESSION_COOKIE)
            rep_state = app.representative_state_for(session)
            if rep_state is not None:
                grant, _, ev, rep_view = rep_state
                if not ev.active:
                    blocked = rjd.RepresentativeAccessBlockedError(
                        state=ev.state,
                        reason=ev.reason,
                        expires_at=rep_view["expires_at"],
                        renewal_route=rep_view["renewal_route"],
                    )
                    self._json(403, blocked.to_payload())
                    return
                if "request_scoped_callback" not in rep_view["permitted_actions"]:
                    denied = rjd.RepresentativeScopeDeniedError(
                        action="request_scoped_callback",
                        expires_at=rep_view["expires_at"],
                        permitted_actions=rep_view["permitted_actions"],
                    )
                    self._json(403, denied.to_payload())
                    return
                owner = resident_key(grant.principal_subject)

                def authorised() -> bool:
                    return app.representative_active(session) and not app.expired
            else:
                if app.view_for(session) is None:
                    self._json(401, dict(error="Please sign in again."))
                    return
                signed = app.codec.verify(session)
                case_id = app.by_handle.get(signed[0]) if signed else None
                if case_id is None:
                    self._json(401, dict(error="Please sign in again."))
                    return
                owner = resident_key(case_id)

                def authorised() -> bool:
                    return app.view_for(session) is not None and not app.expired

            if app.agenda is None:
                self._json(503, dict(error="The local callback agenda is not connected. " + MANUAL))
                return

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
                if rep_state is not None:
                    after = app.representative_state_for(session)
                    if after is not None and not after[2].active:
                        blocked = rjd.RepresentativeAccessBlockedError(
                            state=after[2].state,
                            reason=after[2].reason,
                            expires_at=after[3]["expires_at"],
                            renewal_route=after[3]["renewal_route"],
                        )
                        self._json(403, blocked.to_payload())
                        return
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
            if not self._session_bound():
                return
            app.codec.revoke(_cookies(self.headers.get("Cookie")).get(SESSION_COOKIE))
            # A delayed response must not delete another tab's replacement login cookies.
            self._json(200, dict(signed_in=False))

        do_GET = do_HEAD = do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = _route

    return Handler


def serve(app: ResidentDemo) -> _Server:
    server = _Server((app.host, app.port), make_handler(app))
    app.port = server.server_address[1]
    return server
