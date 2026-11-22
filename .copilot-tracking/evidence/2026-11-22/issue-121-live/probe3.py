"""Read-only: count uploaded (non-generated) documents on the live demo cases. Reads credentials at runtime; retains counts only."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe2.py")).read().split("out = {}")[0]
exec(src)
from playwright.sync_api import sync_playwright
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(); page = c.new_page()
    page.goto(APP + "/api/me", wait_until="domcontentloaded"); login(page)
    r = c.request.get(APP + "/api/cases"); res["cases_status"] = r.status
    j = r.json(); rows = j if isinstance(j, list) else j.get("cases", j.get("items", []))
    res["case_rows"] = len(rows); up = 0; checked = 0
    for row in rows[:40]:
        cid = row.get("id") if isinstance(row, dict) else None
        if not cid: continue
        d = c.request.get(APP + "/api/cases/" + cid)
        if d.status != 200: continue
        checked += 1
        docs = d.json().get("documents", []) or d.json().get("docs", [])
        up += sum(1 for x in docs if x.get("generated") is False)
    res.update(checked=checked, uploaded_docs=up)
    b.close()
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe3.json"), "w"), indent=1); print(res)
