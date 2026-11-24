"""Timed GET /api/assistants/forecast probe for #2304. Usage: python3 probe_forecast.py <label> [count].

Sign-in values are read from the owner's home files at run time and never printed or stored.
Writes <label>.json beside this file with status and elapsed seconds only.
"""
import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
count = int(sys.argv[2]) if len(sys.argv) > 2 else 6
gap = float(sys.argv[3]) if len(sys.argv) > 3 else 0
others_first = len(sys.argv) > 4 and sys.argv[4] == "others-first"
OTHERS = ("/api/assistants", "/api/briefing", "/api/ai/report", "/api/retention")
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()


def login(page):
    page.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if page.locator("input[name=loginfmt]").is_visible(timeout=3000):
                page.fill("input[name=loginfmt]", u)
                page.click("input[type=submit]")
                page.wait_for_timeout(1500)
            if page.locator("input[name=passwd]").is_visible(timeout=3000):
                page.fill("input[name=passwd]", p)
                page.click("input[type=submit]")
                page.wait_for_timeout(2000)
            if page.locator("#idBtn_Back").is_visible(timeout=2000):
                page.click("#idBtn_Back")
                page.wait_for_timeout(2000)
        except Exception:
            pass
    page.wait_for_load_state("networkidle")


def timed(page, path):
    t0 = time.monotonic()
    try:
        r = page.request.get(H + path, timeout=240000, headers={"X-ZF-CSRF": "1"})
        status, body = r.status, r.text()
    except Exception as e:
        status, body = type(e).__name__, ""
    row = {"path": path, "status": status, "seconds": round(time.monotonic() - t0, 2)}
    try:
        j = json.loads(body)
        row["state"] = j.get("state")
        row["error"] = (j.get("error") or "")[:80] or None
    except Exception:
        pass
    return row


res = {"label": label, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "calls": []}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(3000)
    res["calls"].append(timed(pg, "/api/stats"))
    if others_first:
        for pth in OTHERS:
            res["calls"].append(timed(pg, pth))
    for _ in range(count):
        res["calls"].append(timed(pg, "/api/assistants/forecast"))
        time.sleep(gap)
    if not others_first:
        for pth in OTHERS:
            res["calls"].append(timed(pg, pth))
    pg.screenshot(path=os.path.join(OUT, f"{label}.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, f"{label}.json"), "w"), indent=1)
print(json.dumps(res["calls"]))
