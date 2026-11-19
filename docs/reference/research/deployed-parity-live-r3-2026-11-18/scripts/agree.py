"""GET-only agreement check: stats, stage chart, map, list and CSV counts; no secrets printed."""
import csv, io, json
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    g = lambda p: c.request.get(H + p, max_redirects=0)
    st = g("/api/stats").json()
    print("kpis open", st["kpis"]["open"], "completed", st["kpis"]["completed"], "stage sum", sum(s.get("n", s.get("count", 0)) if isinstance(s, dict) else 0 for s in st["stages"]))
    m = g("/api/map").json()
    items = m.get("items") or []
    print("map keys", sorted(m)[:8], "items", len(items))
    lst = g("/api/cases?view=all&limit=1").json()
    cs = list(csv.DictReader(io.StringIO(g("/api/cases.csv?view=all").text())))
    print("list all total", lst["total"], "csv all rows", len(cs))
    mine = g("/api/cases?view=mine&limit=1").json()
    cm = list(csv.DictReader(io.StringIO(g("/api/cases.csv").text())))
    print("list mine total", mine["total"], "csv default rows", len(cm))
    cl = list(csv.DictReader(io.StringIO(g("/api/cases.csv?view=closed").text())))
    print("closed csv rows", len(cl), "completed kpi", st["kpis"]["completed"])
