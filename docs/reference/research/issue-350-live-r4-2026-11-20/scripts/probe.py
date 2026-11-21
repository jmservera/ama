"""GET-only staff probe: statuses and counts only, no personal data or secrets printed."""
import csv, io, json
from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
def brief(r):
    try:
        j = r.json()
    except Exception:
        return f"{r.status} non-json len={len(r.body())}"
    if isinstance(j, dict):
        return f"{r.status} keys={sorted(j)[:10]}" + (f" error={str(j.get('error'))[:90]}" if "error" in j else "")
    return f"{r.status} list={len(j)}"
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    g = lambda p: c.request.get(H + p, max_redirects=0)
    for p in ["/api/me", "/api/stats", "/api/map", "/api/assistants", "/api/governance", "/api/continuity", "/api/time/status",
              "/api/law", "/api/law/sources", "/api/law/alerts", "/api/account/photo", "/api/ledger/verify", "/api/ledger/digest",
              "/api/retention", "/api/sensors", "/api/staff", "/api/visits", "/api/funding", "/api/finance", "/api/handoffs"]:
        print(p, brief(g(p)))
    st = g("/api/stats").json(); me = g("/api/me").json()
    print("role", me.get("role"), "kpis", st["kpis"])
    all_ = g("/api/cases?view=all&limit=1").json()["total"]
    mine = g("/api/cases?view=mine&limit=1").json()["total"]
    cm = list(csv.DictReader(io.StringIO(g("/api/cases.csv").text())))
    cmm = list(csv.DictReader(io.StringIO(g("/api/cases.csv?view=mine").text())))
    ca = list(csv.DictReader(io.StringIO(g("/api/cases.csv?view=all").text())))
    cl = list(csv.DictReader(io.StringIO(g("/api/cases.csv?view=closed").text())))
    print("list all", all_, "csv all", len(ca), "| list mine", mine, "csv default", len(cm), "csv mine", len(cmm), "| closed csv", len(cl))
    m = g("/api/map").json(); print("map total", m.get("total"), "shown", m.get("shown"), "mode", m.get("mode"))
    for p in ["/app", "/cases.html", "/healthz"]:
        print(p, g(p).status)
