"""Timed GET of case detail for #2303 (the Asset and board screen loads it before /api/ai/report). Sign-in read at run time, never printed."""
import os, sys, time, json
from playwright.sync_api import sync_playwright
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_ai_report.py")).read().split("def get(")[0].replace("label = sys.argv[1]", "label = 'x'"))
out = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context().new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(2000)
    r = pg.request.get(H + "/api/cases?view=all&limit=4&offset=0", headers={"X-ZF-CSRF": "1"}, timeout=60000)
    ids = [i["id"] for i in r.json().get("items", [])]
    for cid in ids:
        t0 = time.monotonic()
        try:
            rr = pg.request.get(f"{H}/api/cases/{cid}", headers={"X-ZF-CSRF": "1"}, timeout=150000)
            out.append({"case": cid, "status": rr.status, "seconds": round(time.monotonic() - t0, 1)})
        except Exception as e:
            out.append({"case": cid, "status": type(e).__name__, "seconds": round(time.monotonic() - t0, 1)})
    b.close()
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "case-detail-r0000061.json"), "w"), indent=1)
print(json.dumps(out))
