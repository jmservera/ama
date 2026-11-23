"""Timed signed-in GET of the forecast and two comparison endpoints; prints no secrets.

Usage: python3 live_probe.py <label> [timeout_seconds]
"""
import json, os, sys, time
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
limit = float(sys.argv[2]) if len(sys.argv) > 2 else 200
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


res = {"label": label, "timeout_seconds": limit}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900})
    pg = c.new_page()
    login(pg)
    me = c.request.get(H + "/api/me")
    try:
        res["role"] = me.json().get("role")
    except Exception:
        res["role"] = None
    for path in ("/api/assistants", "/api/exceptions", "/api/assistants/forecast"):
        t = time.monotonic()
        try:
            r = c.request.get(H + path, timeout=limit * 1000)
            elapsed = round(time.monotonic() - t, 2)
            try:
                body = r.json()
            except Exception:
                body = None
            entry = {"status": r.status, "elapsed_s": elapsed}
            if path.endswith("forecast") and isinstance(body, dict):
                entry["keys"] = list(body)
                entry["state"] = body.get("state")
                entry["max_calls_this_period"] = body.get("max_calls_this_period")
                entry["assistants"] = [
                    {k: a.get(k) for k in ("id", "open_cases_in_scope", "eligible_cases", "new_proposals")}
                    for a in body.get("assistants", [])
                ]
            elif isinstance(body, dict) and "error" in body:
                entry["error"] = str(body["error"])[:200]
            res[path] = entry
        except Exception as exc:
            res[path] = {"status": None, "elapsed_s": round(time.monotonic() - t, 2), "error": type(exc).__name__}
    b.close()
txt = json.dumps(res, indent=1)
assert u not in txt and p not in txt
open(f"{OUT}/live_probe_{label}.json", "w").write(txt)
print(txt)
