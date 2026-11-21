"""Local per-role sign-in matrix (issue 2204): real TrustedProxyProvider and HTTP server,
synthetic fictional data, synthetic principal headers (no credentials involved).
Run from src/api with PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests."""
import json, tempfile, threading, urllib.error, urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from test_auth import ENV, OID_NEW, TENANT, principal
from zava_forward.api import auth
from zava_forward.api.server import App, make_handler
from zava_forward.core import identity
from zava_forward.core.store import Store

PATHS = ["/api/cases", "/api/stats", "/api/finance", "/api/packages", "/api/funding", "/api/workorders",
         "/api/audit-check", "/api/admin/simulator-control"]
CASES = [(role, (zr,)) for zr, role in auth.DEFAULT_ROLE_MAP.items()] + [
    ("Application Administrator (alone)", (auth.ADMIN_ROLE,)),
    ("Application Administrator + Coordinator", (auth.ADMIN_ROLE, "ZavaForward.Coordinator")),
    ("DENIED: Contractor role claim without a roster company binding", ("ZavaForward.Contractor",)),
    ("DENIED: Contractor + admin", (auth.ADMIN_ROLE, "ZavaForward.Contractor")),
    ("DENIED: two staff roles", ("ZavaForward.Coordinator", "ZavaForward.Contractor")),
    ("DENIED: unmapped role claim", ("ZavaForward.Nope",)),
    ("DENIED: no role claim", ()),
]

tmp = tempfile.TemporaryDirectory()
CON_OID = "aaaaaaaa-0000-0000-0000-000000000009"
d = json.loads(json.dumps(test_mvp.DATA)); d["staff"].clear()
d[identity.LEGACY_TENANT_KEY] = TENANT
d["staff"].append(dict(code="CON-1", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Test Ltd", oid=CON_OID))
p = Path(tmp.name) / "zavaforward.json"; p.write_text(json.dumps(d))
store = Store(str(p))
httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, provider=auth.TrustedProxyProvider(store, ENV))))
threading.Thread(target=httpd.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{httpd.server_address[1]}"


def get(path, header):
    req = urllib.request.Request(base + path, headers={"X-MS-CLIENT-PRINCIPAL": header} if header else {})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


out = []
for label, roles in CASES:
    h = principal(roles=roles, oid=CON_OID if label == "Contractor" else OID_NEW)
    code, me = get("/api/me", h)
    row = {"case": label, "app_roles": list(roles), "me_status": code}
    if code == 200:
        nav = me.get("navigation", [])
        row.update(role=me["user"]["role"], app_admin=me["user"].get("app_admin"), view_only=me["user"].get("view_only"),
                   nav_labels=[n["label"] for n in nav],
                   nav_unavailable=[n["label"] for n in nav if n.get("access") == "needs a role with this authority"],
                   statuses={x: get(x, h)[0] for x in PATHS})
    out.append(row)
row = {"case": "anonymous (no principal header)", "me_status": get("/api/me", None)[0]}
out.append(row)
httpd.shutdown()
print(json.dumps(out, indent=1))
