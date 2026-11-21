import csv, io, collections
from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    t = c.request.get(H + "/api/cases.csv?view=mine").text()
    rows = list(csv.reader(io.StringIO(t)))
    print("header", rows[0]); print("raw lines", t.count("\n"), "rows", len(rows)-1)
    idc = rows[0].index("id") if "id" in rows[0] else 0
    ids = collections.Counter(r[idc] for r in rows[1:]); print("distinct ids", len(ids), "max repeat", max(ids.values()))
    js = c.request.get(H + "/api/cases?view=mine&limit=100").json()
    print("list total", js["total"], "items", len(js["items"]))
