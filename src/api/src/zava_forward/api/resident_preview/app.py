"""Loopback-only, read-only synthetic resident preview server.

Separate from the staff server on purpose: it imports no staff routes, reads no cookie, header,
query or path to choose who is viewing, and answers only from the resident boundary in core.
"""

import json
import socket
import threading
from collections.abc import Mapping
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from zava_forward.core import resident_preview as rp

WEB = Path(__file__).parent / "web"
ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/resident.css": ("resident.css", "text/css; charset=utf-8"),
    "/resident.js": ("resident.js", "text/javascript; charset=utf-8"),
}
UNAVAILABLE_PATHS = (
    "/resident/messages",
    "/resident/uploads",
    "/resident/downloads",
    "/resident/appointments/respond",
    "/resident/consent",
    "/resident/ai",
)
HEADERS = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Content-Security-Policy": (
        "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; "
        "connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    ),
}


class _Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address: tuple[str, int], handler: Any):
        self.address_family = socket.AF_INET6 if ":" in address[0] else socket.AF_INET
        super().__init__(address, handler)


class ResidentPreview:
    """Holds the private store, the fixture path and the one subject chosen at start-up."""

    def __init__(self, store: Any, fixture: Path, subject: str, host: str, port: int):
        self.store, self.fixture, self.subject = store, fixture, subject
        self.host, self.port = host, port
        self.lock = threading.Lock()

    def host_allowed(self, header: str | None) -> bool:
        if not header:
            return False
        name, _, port = header.rpartition(":")
        if name.startswith("[") and name.endswith("]"):
            name = name[1:-1]
        names = ("127.0.0.1", "localhost", "::1")
        return name in names and port == str(self.port)

    def view(self) -> dict[str, Any]:
        grant = rp.resolve_grant(self.fixture, self.subject)
        with self.lock:
            view: dict[str, Any] = rp.resident_view(self.store, grant)
        return view

    def about(self) -> dict[str, Any]:
        info = rp.fixture_summary(self.fixture)
        return dict(banner=rp.BANNER, fixture=info.get("id"), limitations=info.get("limitations"))


def make_handler(app: ResidentPreview) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "ZavaResidentPreview"

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send(self, status: int, body: bytes, ctype: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            for key, value in HEADERS.items():
                self.send_header(key, value)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _json(self, status: int, payload: Mapping[str, Any]) -> None:
            self._send(status, json.dumps(payload).encode(), "application/json; charset=utf-8")

        def _route(self) -> None:
            if not app.host_allowed(self.headers.get("Host")):
                self._json(403, dict(error="This preview answers only on its loopback address."))
                return
            path = self.path.split("?", 1)[0].split("#", 1)[0]
            if path in UNAVAILABLE_PATHS:
                message = "This feature is not available in the synthetic preview."
                self._json(403, dict(error=message, banner=rp.BANNER))
                return
            if self.command not in ("GET", "HEAD"):
                known = path in ASSETS or path in ("/healthz", "/resident/view", "/resident/about")
                self._json(405 if known else 404, dict(error="This preview is read-only."))
                return
            if path in ASSETS:
                name, ctype = ASSETS[path]
                self._send(200, (WEB / name).read_bytes(), ctype)
            elif path == "/healthz":
                self._json(200, dict(status="ok", synthetic=True, banner=rp.BANNER))
            elif path == "/resident/about":
                self._json(200, app.about())
            elif path == "/resident/view":
                try:
                    self._json(200, app.view())
                except rp.GrantDenied as error:
                    self._json(403, dict(error=str(error), banner=rp.BANNER))
            else:
                self._json(404, dict(error="Not found."))

        do_GET = do_HEAD = do_POST = do_PUT = do_PATCH = do_DELETE = do_OPTIONS = _route

    return Handler


def serve(app: ResidentPreview) -> _Server:
    server = _Server((app.host, app.port), make_handler(app))
    app.port = server.server_address[1]
    return server
