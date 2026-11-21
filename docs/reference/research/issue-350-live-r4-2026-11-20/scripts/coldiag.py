import collections
from playwright.sync_api import sync_playwright
H = open("<session-dir>/H").read().strip()
with sync_playwright() as pw:
    c = pw.chromium.launch().new_context(storage_state="<session-dir>/state-staff.json")
    g = lambda p: c.request.get(H + p).json()
    items, off = [], 0
    while True:
        pg = g(f"/api/cases?view=all&limit=100&offset={off}"); items += pg["items"]; off += 100
        if off >= pg["total"]: break
    from urllib.parse import quote
    for field, param in (("stage", "stage"), ("owner_code", "owner"), ("area", "area"), ("wave", "wave")):
        vals = collections.Counter(i.get(field) for i in items if i.get(field) is not None)
        bad = 0
        for v, n in vals.items():
            sql = g(f"/api/cases?view=all&{param}={quote(str(v))}&limit=1")["total"]
            if sql != n: bad += 1
        print(field, "values", len(vals), "values where SQL-column count != body count:", bad)
