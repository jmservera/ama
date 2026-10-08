"""HTTP server: sign-in, JSON API and static front end. Binds to loopback."""
import hashlib
import base64
import binascii
import hmac
import json
import os
import secrets
import sys
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import projection
from .factory import open_store
from .store import MANAGER_ROLES, ConflictError, GateError

WEB = Path(__file__).resolve().parents[1] / "web"
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png"}
SECURITY = {"Content-Security-Policy": "default-src 'self'; img-src 'self' data: https://tile.openstreetmap.org; frame-ancestors 'none'",
            "X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin", "Cache-Control": "no-store", "Strict-Transport-Security": "max-age=31536000"}


def pw_hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)


class App:
    def __init__(self, store, password):
        self.store = store
        self.salt = secrets.token_bytes(16)
        self.pw = pw_hash(password, self.salt)
        self.sessions = {}

    def login(self, email, password):
        u = self.store.staff.get((email or "").strip().lower())
        ok = hmac.compare_digest(pw_hash(password or "", self.salt), self.pw)
        if not u or not ok:
            return None
        token = secrets.token_urlsafe(32)
        self.sessions[token] = u
        return token


def get_kind(path):
    if path == "/api/me":
        return "me"
    if path == "/api/cases":
        return "cases"
    if path == "/api/cases.csv":
        return "cases.csv"
    if path.startswith("/api/cases/"):
        return "case"
    if path.startswith("/api/docs/"):
        return "doc"
    return {"/api/ranking/policy": "ranking", "/api/ai/priority": "ai_priority", "/api/facets": "facets", "/api/stats": "stats",
            "/api/map": "map", "/api/visits": "visits", "/api/funding": "funding", "/api/briefing": "briefing",
            "/api/audit-check": "audit", "/api/handoffs": "handoffs"}.get(path, "unknown")


def filt(q):
    return {k: q[k][0] for k in ("stage", "area", "wave", "owner", "contractor", "flag") if q.get(k) and q[k][0]}


def num(q, key, default, lo, hi):
    if not q.get(key) or q[key][0] == "":
        return default
    try:
        v = int(q[key][0])
    except ValueError:
        raise ValueError(f"{key} must be a whole number.")
    return max(lo, min(hi, v))


def bbox(q):
    raw = q.get("bbox", [""])[0]
    if not raw:
        return None
    try:
        s, w, n, e = (float(x) for x in raw.split(","))
    except ValueError:
        raise ValueError("bbox must be south,west,north,east.")
    return (min(s, n), min(w, e), max(s, n), max(w, e))


def make_handler(app):
    class H(BaseHTTPRequestHandler):
        server_version = "ProperWarm"

        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="application/json", extra=None):
            raw = body if isinstance(body, bytes) else body.encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            for k, v in {**SECURITY, **(extra or {})}.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(raw)

        def _json(self, code, obj, extra=None):
            self._send(code, json.dumps(obj), extra=extra)

        def _cookie(self):
            m = SimpleCookie(self.headers.get("Cookie", "")).get("pw_session")
            return m.value if m else None

        def _user(self):
            u = app.sessions.get(self._cookie())
            return dict(u) if u else None

        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            if n > 8_000_000:
                raise ValueError("Too large")
            return json.loads(self.rfile.read(n) or b"{}")

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/healthz":
                if not app.store.ready():
                    return self._send(503, "database unavailable", "text/plain")
                return self._send(200, "ok", "text/plain")
            if not url.path.startswith("/api/"):
                name = "index.html" if url.path in ("/", "") else url.path.lstrip("/")
                f = (WEB / name).resolve()
                if WEB in f.parents and f.is_file():
                    return self._send(200, f.read_bytes(), TYPES.get(f.suffix, "application/octet-stream"))
                return self._send(404, "Not found", "text/plain")
            u = self._user()
            if not u:
                return self._json(401, {"error": "Please sign in."})
            q = parse_qs(url.query)
            s = app.store
            if not projection.allowed(u, get_kind(url.path)):
                return self._json(403, {"error": "Your role does not include this."})
            if url.path == "/api/me":
                return self._json(200, projection.me_payload(u, s.counts(u), list(s.staff.values())))
            if url.path in ("/api/cases", "/api/cases.csv"):
                view, text, sort = q.get("view", ["mine"])[0], q.get("q", [""])[0], q.get("sort", ["urgent"])[0]
                if url.path.endswith(".csv"):
                    rows = s.list_cases(u, view, text, filt(q), sort)
                    return self._send(200, s.export_csv(rows), "text/csv; charset=utf-8",
                                      {"Content-Disposition": 'attachment; filename="cases.csv"'})
                try:
                    limit, offset = num(q, "limit", 50, 1, 100), num(q, "offset", 0, 0, 10**9)
                except ValueError as e:
                    return self._json(400, {"error": str(e)})
                return self._json(200, s.page_cases(u, view, text, filt(q), sort, limit, offset))
            if url.path == "/api/ranking/policy":
                return self._json(200, s.ranking_policy())
            if url.path == "/api/ai/priority":
                return self._json(200, {"recommendation": s.latest_priority(u)})
            if url.path == "/api/handoffs":
                return self._json(200, s.pending_handoffs(u))
            if url.path == "/api/facets":
                return self._json(200, s.facets())
            if url.path == "/api/stats":
                return self._json(200, s.stats())
            if url.path == "/api/map":
                try:
                    z = num(q, "zoom", None, 0, 20)
                    return self._json(200, s.map_view(filt(q), bbox(q), z))
                except ValueError as e:
                    return self._json(400, {"error": str(e)})
            if url.path == "/api/visits":
                return self._json(200, s.visits(u, q.get("view", ["mine"])[0]))
            if url.path == "/api/funding":
                return self._json(200, s.funding_list(u))
            if url.path == "/api/briefing":
                return self._json(200, s.briefing(u))
            if url.path.startswith("/api/docs/"):
                try:
                    _, _, _, cid, did = url.path.split("/")
                    name, mime, raw = s.get_document(cid, did)
                except (KeyError, ValueError):
                    return self._json(404, {"error": "File not found."})
                safe = "".join(ch for ch in name if ch.isalnum() or ch in " ._-")
                return self._send(200, raw, mime, {"Content-Disposition": f'attachment; filename="{safe}"'})
            if url.path.startswith("/api/cases/"):
                d = s.detail(url.path.rsplit("/", 1)[1], u)
                return self._json(200, d) if d else self._json(404, {"error": "Case not found."})
            if url.path == "/api/audit-check":
                return self._json(200, s.verify_ledger())
            return self._json(404, {"error": "Not found."})

        def do_POST(self):
            url = urlparse(self.path)
            try:
                body = self._body()
            except ValueError:
                return self._json(400, {"error": "Could not read that."})
            if url.path == "/api/login":
                tok = app.login(body.get("email"), body.get("password"))
                if not tok:
                    return self._json(401, {"error": "Email or password not recognised."})
                ck = f"pw_session={tok}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800" + ("; Secure" if os.environ.get("PW_SECURE_COOKIE") else "")
                return self._json(200, {"ok": True}, {"Set-Cookie": ck})
            u = self._user()
            if not u:
                return self._json(401, {"error": "Please sign in."})
            if url.path == "/api/logout":
                app.sessions.pop(self._cookie(), None)
                return self._json(200, {"ok": True}, {"Set-Cookie": "pw_session=; Max-Age=0; Path=/"})
            s = app.store
            if not projection.allowed(u, "post", "POST"):
                return self._json(403, {"error": "Your role does not include this."})
            parts = url.path.strip("/").split("/")
            try:
                if url.path == "/api/ledger/digest":
                    if u["role"] not in MANAGER_ROLES:
                        raise PermissionError("Only a manager can write a ledger digest.")
                    return self._json(200, {"written": os.path.basename(s.write_digest()), "report": s.verify_ledger()})
                if url.path == "/api/import-check":
                    return self._json(200, s.import_check(body.get("text", "")))
                if url.path == "/api/ai/priority":
                    return self._json(200, s.ai_priority(u, body.get("n", 5)))
                if len(parts) == 5 and parts[:3] == ["api", "ai", "priority"]:
                    return self._json(200, s.resolve_priority(u, parts[3], parts[4], body.get("reason", ""), body.get("items")))
                if len(parts) == 4 and parts[:2] == ["api", "cases"]:
                    cid, act = parts[2], parts[3]
                    if act == "call":
                        s.log_call(u, cid, body.get("outcome"), body.get("note"), body.get("channel", "Phone"))
                    elif act == "decision":
                        s.set_decision(u, cid, body.get("status"), body.get("note", ""))
                    elif act == "handover":
                        s.hand_over(u, cid, body.get("to"), body.get("note", ""))
                    elif act == "return":
                        s.return_case(u, cid, body.get("to_stage"), body.get("reason"))
                    elif act == "reopen":
                        s.reopen_case(u, cid, body.get("reason"))
                    elif act == "offer-handoff":
                        s.offer_handoff(u, cid, body.get("to"), body.get("note", ""))
                    elif act == "accept-handoff":
                        s.accept_handoff(u, cid)
                    elif act == "decline-handoff":
                        s.decline_handoff(u, cid, body.get("reason"))
                    elif act == "withdraw-handoff":
                        s.withdraw_handoff(u, cid)
                    elif act == "hazard-raise":
                        s.raise_hazard(u, cid, body.get("category"), body.get("priority"), body.get("note", ""))
                    elif act == "hazard-refer":
                        s.refer_hazard(u, cid, body.get("index"), body.get("to"), body.get("job"))
                    elif act == "hazard-repaired":
                        s.record_repair(u, cid, body.get("index"))
                    elif act == "hazard-release":
                        s.release_hazard(u, cid, body.get("index"), body.get("note", ""))
                    elif act == "advance":
                        s.advance(u, cid)
                    elif act == "ai":
                        s._case(cid)
                        return self._json(200, s.ai_run(u, cid, body.get("task")))
                    elif act == "upload":
                        try:
                            raw = base64.b64decode(body.get("data", ""), validate=True)
                        except (binascii.Error, ValueError):
                            raise ValueError("Could not read that file.")
                        s.add_document(u, cid, body.get("name"), body.get("kind"), raw)
                    elif act == "read-doc":
                        return self._json(200, s.read_document(u, cid, body.get("id")))
                    elif act == "funding-draft":
                        s.funding_draft(u, cid)
                    elif act == "funding":
                        s.funding_step(u, cid, body.get("action"), body.get("text", ""))
                    elif act == "draft":
                        s._case(cid)
                        return self._json(200, s.draft(cid, body.get("kind", "update")))
                    else:
                        return self._json(404, {"error": "Not found."})
                    return self._json(200, s.detail(cid, u))
            except ConflictError:
                return self._json(409, {"error": "Someone else changed this at the same moment. Reload and try again."})
            except GateError as e:
                return self._json(409, {"error": "Not ready yet.", "reasons": e.reasons})
            except PermissionError as e:
                return self._json(403, {"error": str(e)})
            except KeyError:
                return self._json(404, {"error": "Case not found."})
            except ValueError as e:
                return self._json(400, {"error": str(e)})
            return self._json(404, {"error": "Not found."})

    return H


def main():
    password = os.environ.get("PW_PASSWORD") or secrets.token_urlsafe(9)
    try:
        store = open_store()
    except FileNotFoundError:
        sys.exit("No data file. Run build_mvp_dataset.py first (see mvp/README.md).")
    app = App(store, password)
    host, port = os.environ.get("PW_BIND", "127.0.0.1"), int(os.environ.get("PORT", "8088"))
    print(f"Proper Warm is running at http://{host}:{port}")
    if not os.environ.get("PW_PASSWORD"):
        print(f"Sign in with any staff email and the password {password}")
    ThreadingHTTPServer((host, port), make_handler(app)).serve_forever()


if __name__ == "__main__":
    main()
