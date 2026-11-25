"""Live observation of the Home sensors chart and map card gauges (issue 2193).
Credentials are read at runtime and never printed."""
import json, os, sys
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u); page.click("input[type=submit]"); page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p); page.click("input[type=submit]"); page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back"); page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")



import json as _j, time
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    ids = ["ZF-2025-0331", "ZF-2025-0150", "ZF-2025-0032", "ZF-2025-0389", "ZF-2025-0340"]
    rows = []
    for rnd in range(6):
        for cid in ids:
            t = time.time()
            r = c.request.get(f"{H}/api/cases/{cid}/sensors", timeout=60000)
            rows.append({"round": rnd, "case": cid, "status": r.status, "seconds": round(time.time() - t, 2)})
        time.sleep(5)
    b.close()
from collections import Counter
print(Counter(x["status"] for x in rows), max(x["seconds"] for x in rows))
__import__("pathlib").Path(OUT + "/sensor-loop-before.json").write_text(_j.dumps(rows, indent=1))
