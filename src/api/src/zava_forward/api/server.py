"""HTTP server: sign-in, JSON API and static front end. Binds to loopback."""
import base64
import binascii
import json
import os
import secrets
import sys
import threading
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from zava_forward.core import profile

from zava_forward.core import projection, quality

from zava_forward.core import lawstore
from zava_forward.api import auth
from zava_forward.api.workbench import navigation
from zava_forward.agents.chat import ChatModel
from zava_forward.agents.dispatch import AgentWorker
from zava_forward.core.assistants import Assistants
from zava_forward.core.chat_isolation import ChatForbidden, ChatIsolation
from zava_forward.core.chat_privacy import ChatNotApproved
from zava_forward.core.chat_panel import ChatPanel
from zava_forward.core.chatthreads import ChatNotFound
from zava_forward.core.documents import DocumentStoreError
from zava_forward.core.factory import open_store
from zava_forward.api.timecapture import TimeCapture
from zava_forward.core.store import MANAGER_ROLES, ConflictError, GateError

WEB = Path(__file__).resolve().parent / "web"
TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png"}
OSM_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
OSM_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
SECURITY = {"X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin", "Cache-Control": "no-store", "Strict-Transport-Security": "max-age=31536000"}


def tile_config(env=None):
    """Map tile provider from ZF_TILE_URL. Production never falls back to the public OSM servers."""
    env = os.environ if env is None else env
    url = (env.get("ZF_TILE_URL") or "").strip()
    if not url:
        if env.get("ZF_ENV") == "production":
            return dict(url=None, attribution="", host=None)
        return dict(url=OSM_URL, attribution=OSM_ATTRIBUTION, host="https://tile.openstreetmap.org")
    parts = urlparse(url.replace("{s}", "a").replace("{z}", "0").replace("{x}", "0").replace("{y}", "0"))
    if parts.scheme != "https" or not parts.netloc:
        sys.exit("ZF_TILE_URL must be an https URL such as https://tiles.example.org/{z}/{x}/{y}.png")
    return dict(url=url, attribution=env.get("ZF_TILE_ATTRIBUTION", ""), host=f"https://{parts.netloc}")


class App:
    def __init__(self, store, password=None, timecap=None, provider=None, law=None):
        self.store = store
        self.time = timecap or TimeCapture(store)
        self.tiles = tile_config()
        self.csp = "default-src 'self'; img-src 'self' data: blob:" + (f" {self.tiles['host']}" if self.tiles["host"] else "") + "; frame-ancestors 'none'"
        self.provider = provider or auth.make_provider(store, password or secrets.token_urlsafe(9))
        # The provider call is agents code; the API composes it in process until the queue transport (#144) replaces it.
        self.assistants = Assistants(store, provider=AgentWorker(lambda *args: store.ai.evidence(*args)).provider_call)
        self.chat = ChatIsolation(store)
        self.panel = ChatPanel(self.chat, ChatModel(AgentWorker(lambda *args: store.ai.evidence(*args))))
        self.law = law
        self.law_lock = threading.Lock()


def get_kind(path):
    if path.startswith("/api/buildings/"):
        return "building"
    if path.startswith("/api/chat"):
        return "chat"
    if path.startswith("/api/law"):
        return "law"
    if path.startswith("/api/assistants"):
        return "assistants"
    if path == "/api/account/photo":
        return "me"
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
    if path.startswith("/api/time/"):
        return "time"
    return {"/api/ranking/policy": "ranking", "/api/ranking/snapshot": "ranking", "/api/ai/priority": "ai_priority", "/api/facets": "facets", "/api/stats": "stats",
            "/api/map": "map", "/api/visits": "visits", "/api/funding": "funding", "/api/briefing": "briefing",
            "/api/audit-check": "audit", "/api/handoffs": "handoffs", "/api/packages": "packages",
            "/api/workorders": "workorders", "/api/checklists": "checklists", "/api/ai/report": "ai_report", "/api/finance": "finance_queue", "/api/governance": "governance", "/api/continuity": "continuity", "/api/continuity/export": "continuity_export", "/api/retention": "retention"}.get(path, "unknown")


GOVERNANCE_ACTIONS = {"protocol-freeze": "protocol_freeze", "protocol-approve": "protocol_approve", "benefits-record": "benefits_record",
                      "benefits-approve": "benefits_approve", "release": "release_record", "breach": "breach_record", "restart": "breach_restart"}
CONTINUITY_ACTIONS = {"restart-propose": "restart_propose", "restart-decide": "restart_decide", "change": "change_record",
                      "change-reverse": "change_reverse"}
QUALITY_ACTIONS = {
    "quality-submit": lambda s, u, cid, b: s.submit_quality(u, cid, b.get("measure"), b.get("submitted_by"), b.get("source"), b.get("items"), b.get("context_revision")),
    "quality-accept": lambda s, u, cid, b: s.accept_quality(u, cid, b.get("index"), b.get("note", "")),
    "quality-return": lambda s, u, cid, b: s.return_quality(u, cid, b.get("index"), b.get("reason"), b.get("defect"), b.get("owner")),
    "quality-fix": lambda s, u, cid, b: s.record_fix(u, cid, b.get("index"), b.get("fixed_by"), b.get("note", "")),
    "quality-reinspect": lambda s, u, cid, b: s.reinspect_quality(u, cid, b.get("index"), b.get("result"), b.get("note", "")),
    "quality-handover": lambda s, u, cid, b: s.hand_over_quality(u, cid, b.get("index"), b.get("note"), b.get("resident_told")),
    "quality-aftercare": lambda s, u, cid, b: s.add_aftercare(u, cid, b.get("index"), b.get("note")),
}
WO_ACTIONS = {
    "reissue": lambda s, u, wid, b: s.reissue_work_order(u, wid, b.get("scope"), b.get("reason"), b.get("resident_bindings")),
    "appointment": lambda s, u, wid, b: s.record_wo_appointment(u, wid, b.get("outcome"), b.get("date", "")),
    "complete": lambda s, u, wid, b: s.complete_work_order(u, wid, b.get("note", "")),
    "correct": lambda s, u, wid, b: s.correct_work_order(u, wid, b.get("reason"), b.get("scope", ""), b.get("resident_bindings")),
    "withdraw": lambda s, u, wid, b: s.withdraw_work_order(u, wid, b.get("reason")),
}


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
        server_version = "ZavaForward"

        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="application/json", extra=None):
            raw = body if isinstance(body, bytes) else body.encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(raw)))
            for k, v in {**SECURITY, "Content-Security-Policy": app.csp, **(extra or {})}.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(raw)

        def _json(self, code, obj, extra=None):
            self._send(code, json.dumps(obj), extra=extra)

        def _cookie(self):
            m = SimpleCookie(self.headers.get("Cookie", "")).get("zf_session")
            return m.value if m else None

        def _user(self):
            return app.provider.authenticate(self.headers)

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
                if url.path == "/sign-in":
                    target = "/.auth/login/aad?post_login_redirect_uri=%2Fapp" if app.provider.name == "trusted-proxy" else "/app"
                    if app.provider.name == "trusted-proxy":
                        switch = parse_qs(url.query, keep_blank_values=True).get("switch") == ["1"]
                        if switch:
                            target += "&prompt=select_account"
                            print("auth flow: account-picker-started", flush=True)
                        else:
                            print("auth flow: sign-in-started", flush=True)
                    return self._send(302, "", extra={"Location": target})
                name = "welcome.html" if url.path in ("/", "") else "index.html" if url.path == "/app" else url.path.lstrip("/")
                f = (WEB / name).resolve()
                if WEB in f.parents and f.is_file():
                    if app.provider.name == "trusted-proxy" and url.path not in ("/", "/welcome.html", "/style.css", "/zava-logo.png") and not self._user():
                        if self.headers.get("X-MS-CLIENT-PRINCIPAL"):
                            return self._send(403, '<h1>Account not authorised</h1><p>Your account needs a provisioned workbench role.</p><a href="/.auth/logout?post_logout_redirect_uri=%2F">Sign out</a>', "text/html; charset=utf-8")
                        return self._send(302, "", extra={"Location": "/sign-in"})
                    raw = f.read_bytes()
                    if name == "index.html":
                        if app.provider.name == "trusted-proxy":
                            print("auth flow: workbench-entered", flush=True)
                        raw = raw.replace(b"__AUTH_PROVIDER__", app.provider.name.encode())
                    return self._send(200, raw, TYPES.get(f.suffix, "application/octet-stream"))
                return self._send(404, "Not found", "text/plain")
            u = self._user()
            if not u:
                return self._json(401, {"error": "Please sign in."})
            q = parse_qs(url.query)
            s = app.store
            if not projection.allowed(u, get_kind(url.path)):
                return self._json(403, {"error": "Your role does not include this."})
            if url.path.startswith("/api/chat"):
                return self._chat(u, url.path, None)
            if url.path.startswith("/api/buildings/"):
                try:
                    parts = url.path.strip("/").split("/")
                    if len(parts) != 3:
                        return self._json(404, {"error": "Building not found."})
                    return self._json(200, s.building_view(u, unquote(parts[2])))
                except KeyError:
                    return self._json(404, {"error": "Building not found; shared context is unknown."})
                except ValueError as e:
                    return self._json(400, {"error": str(e)})
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
            if url.path.startswith("/api/law"):
                if app.law is None:
                    return self._json(503, {"error": "The law store is not loaded."})
                parts = [unquote(x) for x in url.path.strip("/").split("/")]
                try:
                    with app.law_lock:
                        if parts == ["api", "law", "sources"]:
                            return self._json(200, app.law.sources())
                        if len(parts) == 4 and parts[:3] == ["api", "law", "sources"]:
                            return self._json(200, app.law.source(parts[3]))
                        if len(parts) == 4 and parts[:3] == ["api", "law", "provisions"]:
                            return self._json(200, app.law.provision(parts[3]))
                        if parts == ["api", "law", "search"]:
                            return self._json(200, app.law.search(q.get("q", [""])[0][:200]))
                except KeyError:
                    pass
                return self._json(404, {"error": "Not found."})
            if url.path.startswith("/api/assistants"):
                try:
                    if url.path == "/api/assistants":
                        return self._json(200, app.assistants.registry(u))
                    if url.path == "/api/assistants/proposals":
                        return self._json(200, app.assistants.listing(u, q.get("case_id", [None])[0], q.get("after", [""])[0]))
                    parts = url.path.strip("/").split("/")
                    if len(parts) == 4 and parts[:3] == ["api", "assistants", "proposals"]:
                        return self._json(200, app.assistants.detail(u, parts[3], num(q, "history_offset", 0, 0, 1000000)))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
                except KeyError:
                    return self._json(404, {"error": "Proposal not found."})
                except ValueError as e:
                    return self._json(400, {"error": str(e)})
                except Exception:
                    return self._json(503, {"error": "Assistant service unavailable; continue ordinary case work manually."})
                return self._json(404, {"error": "Not found."})
            if url.path == "/api/me":
                out = projection.me_payload(u, s.counts(u), list(s.staff.values()))
                out["account"] = app.provider.account(self.headers, u)
                out["map"] = dict(tiles=app.tiles["url"], attribution=app.tiles["attribution"])
                out["navigation"] = navigation(u)
                return self._json(200, out)
            if url.path == "/api/account/photo":
                try:
                    token = self.headers.get("X-MS-TOKEN-AAD-ACCESS-TOKEN") if app.provider.name == "trusted-proxy" else None
                    raw, kind = profile.own_photo(token)
                    return self._send(200, raw, kind)
                except profile.PhotoError as error:
                    return self._json(error.status, {"error": str(error)})
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
                try:
                    after = q.get("after", [""])[0][:100] or None
                    return self._json(200, s.page_cases(u, view, text, filt(q), sort, limit, offset, after))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
            if url.path == "/api/ranking/policy":
                return self._json(200, s.ranking_policy())
            if url.path == "/api/ranking/snapshot":
                try:
                    return self._json(200, s.ranking_snapshot(u, q.get("policy", [""])[0] or None))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
                except ValueError as e:
                    return self._json(400, {"error": str(e)})
            if url.path == "/api/ai/priority":
                return self._json(200, {"recommendation": s.latest_priority(u)})
            if url.path == "/api/time/status":
                return self._json(200, app.time.status(u))
            if url.path in ("/api/time/mine", "/api/time/report"):
                try:
                    if url.path.endswith("report"):
                        if u["role"] not in MANAGER_ROLES:
                            raise PermissionError("Only a manager can see the time report.")
                        return self._json(200, app.time.report())
                    return self._json(200, app.time.mine(u))
                except PermissionError as e:
                    return self._json(403, {"error": str(e), "enabled": app.time.status()["enabled"]})
            if url.path in ("/api/continuity", "/api/continuity/export"):
                try:
                    if url.path == "/api/continuity":
                        return self._json(200, s.continuity_view(u))
                    return self._json(200, s.continuity_export(u, app.assistants.export()))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
            if url.path == "/api/retention":
                try:
                    return self._json(200, s.retention_due(u))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
            if url.path == "/api/governance":
                try:
                    return self._json(200, s.governance_view(u))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
            if url.path == "/api/finance":
                try:
                    return self._json(200, s.finance_queue(u))
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
            if url.path == "/api/handoffs":
                return self._json(200, s.pending_handoffs(u))
            if url.path == "/api/packages":
                return self._json(200, s.list_packages(u))
            if url.path == "/api/workorders":
                return self._json(200, s.list_work_orders(u, q.get("case", [None])[0]))
            if url.path == "/api/checklists":
                return self._json(200, quality.CHECKLISTS)
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
                return self._json(200, s.briefing(u, q.get("mode", [None])[0]))
            if url.path == "/api/ai/report":
                if u["role"] not in MANAGER_ROLES:
                    return self._json(403, {"error": "Only a manager can see the AI evaluation report."})
                from zava_forward.core import ai_registry

                from zava_forward.agents import ai_eval
                return self._json(200, {"evaluation": ai_eval.run_eval(), "live": s.ai_live_report(), "registry": ai_registry.registry()})
            if url.path.startswith("/api/docs/"):
                try:
                    _, _, _, cid, did = url.path.split("/")
                    name, mime, raw = s.get_document(cid, did, u)
                except (KeyError, ValueError):
                    return self._json(404, {"error": "File not found."})
                except PermissionError as e:
                    return self._json(403, {"error": str(e)})
                except DocumentStoreError:
                    return self._json(502, {"error": "The document store is not available. Try again shortly."})
                safe = "".join(ch for ch in name if ch.isalnum() or ch in " ._-")
                return self._send(200, raw, mime, {"Content-Disposition": f'attachment; filename="{safe}"'})
            if url.path.startswith("/api/cases/"):
                d = s.detail(url.path.rsplit("/", 1)[1], u)
                return self._json(200, d) if d else self._json(404, {"error": "Case not found."})
            if url.path == "/api/audit-check":
                return self._json(200, s.verify_ledger())
            return self._json(404, {"error": "Not found."})

        def _chat(self, user, path, body):
            """Chat and memory. The owner is always the signed-in user; no request field names an owner."""
            c, s, parts = app.chat, app.store, path.strip("/").split("/")[2:]
            post = body is not None
            if post and not isinstance(body, dict):
                return self._json(400, {"error": "Chat request must be an object."})
            try:
                if not post and parts == ["threads"]:
                    return self._json(200, s.chat_list_threads(c.current_user(user)))
                if not post and len(parts) == 2 and parts[0] == "threads":
                    return self._json(200, s.chat_resume(c.current_user(user), parts[1]))
                if not post and parts == ["memory"]:
                    return self._json(200, c.privacy.list_memory(c.current_user(user)))
                if not post and parts == ["memory", "status"]:
                    return self._json(200, c.privacy.memory_status(c.current_user(user), (parse_qs(urlparse(self.path).query).get("task") or [""])[0]))
                if post and parts == ["threads"]:
                    u = c.current_user(user)
                    if body.get("case_id") and s.detail(body["case_id"], u) is None:
                        raise ChatNotFound("case")
                    return self._json(200, {"id": c.privacy.start_thread(u, body.get("case_id", ""), body.get("task", ""))})
                if post and len(parts) == 3 and parts[0] == "threads":
                    u, tid = c.current_user(user), parts[1]
                    if parts[2] == "messages":
                        return self._json(200, c.turn(u, tid, body.get("content")))
                    if parts[2] == "ask":
                        return self._json(200, app.panel.ask(u, tid, body.get("content")))
                    if parts[2] == "proposals":
                        # Proposal-only: the existing assistants path queues it for the independent review.
                        t = s.chat_resume(u, tid)
                        if not t["case_id"]:
                            raise ValueError("Open the panel from a case to request a proposal.")
                        p = app.assistants.invoke(u, str(body.get("capability") or ""), t["case_id"])
                        s.chat_add_message(u, tid, "assistant", "Proposal requested. It needs a separate source check and role review before anything changes.", evidence=[p["id"]] if isinstance(p, dict) and p.get("id") else ())
                        return self._json(202, p)
                    if parts[2] == "archive":
                        return self._json(200, s.chat_archive(u, tid))
                    if parts[2] == "delete":
                        s.chat_delete(u, tid)
                        return self._json(200, {"ok": True})
                if post and parts == ["memory"]:
                    return self._json(200, {"id": c.privacy.add_memory(c.current_user(user), body.get("content", ""), task=str(body.get("task") or ""))})
                if post and parts == ["memory", "opt-in"]:
                    c.privacy.opt_in(c.current_user(user), body.get("acknowledged"))
                    return self._json(200, {"ok": True})
                if post and parts == ["memory", "opt-out"]:
                    return self._json(200, {"deleted": c.privacy.opt_out(c.current_user(user))})
                if post and len(parts) == 3 and parts[0] == "memory" and parts[2] in ("edit", "delete"):
                    u = c.current_user(user)
                    if parts[2] == "edit":
                        c.privacy.edit_memory(u, parts[1], body.get("content", ""))
                    else:
                        c.privacy.delete_memory(u, parts[1])
                    return self._json(200, {"ok": True})
                if post and parts == ["memory", "global"]:
                    c.privacy.set_global(c.current_user(user), body.get("enabled") is True)
                    return self._json(200, {"ok": True})
                if post and parts == ["memory", "task"]:
                    c.privacy.set_task(c.current_user(user), str(body.get("task") or ""), body.get("enabled") is True)
                    return self._json(200, {"ok": True})
                if post and parts == ["memory", "erase"]:
                    return self._json(200, {"erased": c.erase_memory(user)})
                if post and parts == ["breakglass"]:
                    return self._json(200, c.break_glass(user, body.get("target"), body.get("purpose"), body.get("minutes", 15)))
            except (ChatNotFound, LookupError):
                return self._json(404, {"error": "Not found."})
            except (ChatForbidden, ChatNotApproved, PermissionError) as e:
                return self._json(403, {"error": str(e)})
            except (ValueError, TypeError) as e:
                return self._json(400, {"error": str(e)})
            except ConflictError:
                return self._json(409, {"error": "Someone else changed this at the same moment. Reload and try again."})
            return self._json(404, {"error": "Not found."})

        def _procurement(self, s, u, parts, body):
            """Package, capacity and work-order writes. Returns the refreshed list the screen shows."""
            kind, rest = parts[1], parts[2:]
            if kind == "packages" and not rest:
                s.create_package(u, body.get("name"), body.get("period_from"), body.get("period_to"), body.get("scope"), body.get("contract_ref"))
            elif kind == "packages" and len(rest) == 2 and rest[1] == "rescope":
                s.rescope_package(u, rest[0], body.get("scope"), body.get("reason"))
            elif kind == "packages" and len(rest) == 2 and rest[1] == "capacity":
                s.set_capacity(u, rest[0], body.get("contractor"), body.get("offered"), body.get("committed"), body.get("evidence", ""))
            elif kind == "workorders" and not rest:
                s.issue_work_order(u, body.get("package"), body.get("case_id"), body.get("scope", ""), body.get("resident_bindings"))
            elif kind == "workorders" and len(rest) == 2 and rest[1] in WO_ACTIONS:
                WO_ACTIONS[rest[1]](s, u, rest[0], body)
            else:
                raise KeyError("route")
            return dict(packages=s.list_packages(u), work_orders=s.list_work_orders(u))

        def do_POST(self):
            url = urlparse(self.path)
            try:
                body = self._body()
                if not isinstance(body, dict):
                    raise ValueError("Request must be an object.")
            except ValueError:
                return self._json(400, {"error": "Could not read that."})
            if url.path == "/api/login":
                if not hasattr(app.provider, "login"):
                    return self._json(404, {"error": "Sign-in is handled by your organisation's single sign-on."})
                tok = app.provider.login(body.get("email"), body.get("password"))
                if not tok:
                    return self._json(401, {"error": "Email or password not recognised."})
                ck = f"zf_session={tok}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800" + ("; Secure" if os.environ.get("ZF_SECURE_COOKIE") else "")
                return self._json(200, {"ok": True}, {"Set-Cookie": ck})
            u = self._user()
            if not u:
                return self._json(401, {"error": "Please sign in."})
            if app.provider.name == "trusted-proxy" and self.headers.get("X-ZF-CSRF") != "1":
                return self._json(403, {"error": "Missing request header."})
            if url.path == "/api/logout":
                if app.provider.name == "trusted-proxy":
                    if body.get("switchAccount") is True:
                        print("auth flow: account-switch-requested", flush=True)
                    else:
                        print("auth flow: sign-out-requested", flush=True)
                return self._json(200, app.provider.logout_response(switch=body.get("switchAccount") is True), {"Set-Cookie": "zf_session=; Max-Age=0; Path=/"})
            s = app.store
            if not projection.allowed(u, "post", "POST"):
                return self._json(403, {"error": "Your role does not include this."})
            if url.path.startswith("/api/chat"):
                return self._chat(u, url.path, body)
            parts = url.path.strip("/").split("/")
            try:
                if len(parts) == 4 and parts[:2] == ["api", "assistants"] and parts[3] == "invoke":
                    return self._json(202, app.assistants.invoke(u, parts[2], body.get("case_id")))
                if url.path == "/api/assistants/releases":
                    return self._json(201, app.assistants.record_release(u, body))
                if len(parts) == 5 and parts[:3] == ["api", "assistants", "releases"] and parts[4] in ("suspend", "revoke"):
                    return self._json(200, app.assistants.change_release(
                        u, parts[3], "suspended" if parts[4] == "suspend" else "revoked", body.get("reason")))
                if len(parts) == 5 and parts[:3] == ["api", "assistants", "proposals"] and parts[4] == "review":
                    return self._json(200, app.assistants.review(
                        u, parts[3], body.get("action"), body.get("revision"), body.get("note", ""),
                        body.get("output"), body.get("source_verified", False)))
                if url.path == "/api/time/acknowledge":
                    ver = app.time.acknowledge(u)
                    s.audit(u["email"], "time_notice_acknowledged", "-", f"notice {ver}")
                    return self._json(200, app.time.status(u))
                if url.path == "/api/time/request-enable":
                    if u["role"] not in MANAGER_ROLES:
                        raise PermissionError("Only a manager can request the enabling action.")
                    refs = app.time.request_enable(u)
                    s.audit(u["email"], "time_capture_enable_requested", "-", f"as {u['role']}; DPIA {refs['dpia_ref']}; consultation {refs['consultation_ref']}; notice {refs['notice_ref']}")
                    return self._json(200, app.time.status(u))
                if url.path == "/api/time/enable":
                    if u["role"] not in MANAGER_ROLES:
                        raise PermissionError("Only a manager can take the enabling action.")
                    refs = app.time.activate(u)
                    s.audit(u["email"], "time_capture_enabled", "-", f"requested by {refs['requested_by']} ({refs['requested_role']}), enabled as {u['role']}; DPIA {refs['dpia_ref']}; consultation {refs['consultation_ref']}; notice {refs['notice_ref']}")
                    return self._json(200, app.time.status(u))
                if url.path == "/api/time":
                    s._case(body.get("case_id"))
                    app.time.record(u, body.get("case_id"), body.get("minutes"), body.get("activity"))
                    return self._json(200, {"ok": True})
                if url.path == "/api/ledger/digest":
                    if u["role"] not in MANAGER_ROLES:
                        raise PermissionError("Only a manager can write a ledger digest.")
                    return self._json(200, {"written": os.path.basename(s.write_digest()), "report": s.verify_ledger()})
                if parts[:2] == ["api", "continuity"] and len(parts) == 3 and parts[2] == "suspend":
                    return self._json(200, s.suspend(u, body, app.assistants.affected(body.get("scope"))))
                if parts[:2] == ["api", "continuity"] and len(parts) == 3 and parts[2] in CONTINUITY_ACTIONS:
                    return self._json(200, getattr(s, CONTINUITY_ACTIONS[parts[2]])(u, body))
                if parts[:2] == ["api", "governance"] and len(parts) == 3 and parts[2] in GOVERNANCE_ACTIONS:
                    return self._json(200, getattr(s, GOVERNANCE_ACTIONS[parts[2]])(u, body))
                if url.path == "/api/import-check":
                    return self._json(200, s.import_check(body.get("text", "")))
                if url.path == "/api/ai/priority":
                    return self._json(200, s.ai_priority(u, body.get("n", 5), body.get("mode")))
                if len(parts) == 5 and parts[:3] == ["api", "ai", "review"]:
                    return self._json(200, s.review_ai(u, parts[3], parts[4], body.get("reason", ""), body.get("text")))
                if parts[:2] == ["api", "packages"] or parts[:2] == ["api", "workorders"]:
                    return self._json(200, self._procurement(s, u, parts, body))
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
                        s.return_case(u, cid, body.get("to_stage"), body.get("reason"), metadata=body)
                    elif act == "reopen":
                        s.reopen_case(u, cid, body.get("reason"), metadata=body)
                    elif act == "offer-handoff":
                        s.offer_handoff(u, cid, body.get("to"), body.get("note", ""), metadata=body)
                    elif act == "receive-handoff":
                        s.receive_handoff(u, cid)
                    elif act == "escalate-handoff":
                        s.escalate_handoff(u, cid, body.get("to"), body.get("reason"))
                    elif act == "complete-handoff":
                        s.complete_handoff(u, cid, body.get("note"))
                    elif act == "accept-handoff":
                        s.accept_handoff(u, cid)
                    elif act == "decline-handoff":
                        s.decline_handoff(u, cid, body.get("reason"))
                    elif act == "withdraw-handoff":
                        s.withdraw_handoff(u, cid)
                    elif act == "hazard-raise":
                        s.raise_hazard(u, cid, body.get("category"), body.get("priority"), body.get("note", ""), metadata=body)
                    elif act == "hazard-refer":
                        s.refer_hazard(u, cid, body.get("index"), body.get("to"), body.get("job"), metadata=body)
                    elif act == "hazard-receive":
                        s.receive_hazard(u, cid, body.get("index"), body.get("evidence"))
                    elif act == "hazard-accept":
                        s.accept_hazard(u, cid, body.get("index"), body.get("evidence"))
                    elif act == "hazard-times":
                        s.observe_hazard_times(u, cid, body.get("index"), body)
                    elif act == "hazard-repaired":
                        s.record_repair(u, cid, body.get("index"), body.get("evidence"))
                    elif act == "hazard-release":
                        s.release_hazard(u, cid, body.get("index"), body.get("note", ""), body.get("evidence"))
                    elif act in QUALITY_ACTIONS:
                        QUALITY_ACTIONS[act](s, u, cid, body)
                    elif act == "advance":
                        s.advance(u, cid)
                    elif act == "stock-reconciliation":
                        s.stock_reconcile(u, cid, body)
                    elif act == "stock-query-event":
                        s.stock_query_event(u, cid, body)
                    elif act == "ai":
                        s._case(cid)
                        return self._json(200, s.ai_run(u, cid, body.get("task"), body.get("mode")))
                    elif act == "upload":
                        try:
                            raw = base64.b64decode(body.get("data", ""), validate=True)
                        except (binascii.Error, ValueError):
                            raise ValueError("Could not read that file.")
                        s.add_document(u, cid, body.get("name"), body.get("kind"), raw)
                    elif act == "rescan-doc":
                        return self._json(200, s.rescan_document(u, cid, body.get("id")))
                    elif act == "legal-hold":
                        s.place_legal_hold(u, cid, body.get("reference"))
                    elif act == "legal-hold-release":
                        s.release_legal_hold(u, cid)
                    elif act == "retention-approve":
                        s.approve_retention_deletion(u, cid, body.get("id"))
                    elif act == "read-doc":
                        return self._json(200, s.read_document(u, cid, body.get("id"), body.get("mode")))
                    elif act in ("finance", "grant", "technical", "resident"):
                        getattr(s, {"finance": "finance_action", "grant": "grant_action", "technical": "technical_action",
                                    "resident": "resident_action"}[act])(u, cid, body)
                    elif act == "funding-draft":
                        return self._json(200, dict(s.detail(cid, u), ai=s.funding_draft(u, cid, body.get("mode"))))
                    elif act == "funding":
                        s.funding_step(u, cid, body.get("action"), body.get("text", ""))
                    elif act == "draft":
                        s._case(cid)
                        return self._json(200, s.draft(cid, body.get("kind", "update")))
                    else:
                        return self._json(404, {"error": "Not found."})
                    return self._json(200, s.detail(cid, u))
            except DocumentStoreError:
                return self._json(502, {"error": "The document store is not available. Try again shortly."})
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
            except Exception:
                if url.path.startswith("/api/assistants"):
                    return self._json(503, {"error": "Assistant service unavailable; continue ordinary case work manually."})
                raise
            return self._json(404, {"error": "Not found."})

    return H


def main() -> None:
    password = os.environ.get("ZF_PASSWORD") or secrets.token_urlsafe(9)
    try:
        store = open_store()
    except FileNotFoundError:
        sys.exit("No data file. Run build_mvp_dataset.py first (see src/api/README.md).")
    law = lawstore.LawStore.from_env()
    app = App(store, password, law=law)
    host, port = os.environ.get("ZF_BIND", "127.0.0.1"), int(os.environ.get("PORT", "8088"))
    print(f"Zava Forward is running at http://{host}:{port}")
    if app.provider.name == "password" and not os.environ.get("ZF_PASSWORD"):
        print(f"Sign in with any staff email and the password {password}")
    app.assistants.start()
    try:
        ThreadingHTTPServer((host, port), make_handler(app)).serve_forever()
    finally:
        app.assistants.stop()


if __name__ == "__main__":
    main()
