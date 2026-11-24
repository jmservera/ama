"""Live probe for #2303: GET /api/ai/report and the Asset and board view. Usage: python3 probe_ai_report.py <label>.

Sign-in values are read from the owner's home files at run time and never printed or stored.
Writes <label>.json and <label>.png beside this file; the JSON keeps status, timing and key names only.
"""
import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
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


def get(page, path):
    t0 = time.monotonic()
    try:
        r = page.request.get(H + path, timeout=int(os.environ.get("UI_WAIT_MS", "240000")), headers={"X-ZF-CSRF": "1"})
    except Exception as e:
        return {"path": path, "status": type(e).__name__, "seconds": round(time.monotonic() - t0, 2)}, None
    row = {"path": path, "status": r.status, "seconds": round(time.monotonic() - t0, 2)}
    try:
        j = r.json()
        row["keys"] = sorted(j)[:20] if isinstance(j, dict) else type(j).__name__
        row["has_consumption"] = isinstance(j, dict) and bool(j.get("consumption"))
        row["error"] = (j.get("error") or "")[:80] if isinstance(j, dict) else None
        return row, j
    except Exception:
        return row, None


res = {"label": label, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "calls": []}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(3000)
    for _ in range(0 if os.environ.get("SKIP_API") else 1):
        row, _j = get(pg, "/api/ai/report")
        res["calls"].append(row)
    _row, cases = get(pg, "/api/cases?view=all&limit=1&offset=0")
    items = (cases or {}).get("items") or []
    cid = items[0].get("id") if items else None
    res["case_found"] = bool(cid)
    seen = {}
    t_nav = time.monotonic()
    pg.on("response", lambda r: seen.__setitem__(r.url.split("?")[0].replace(H, ""), [r.status, round(time.monotonic() - t_nav, 1)]) if "/api/" in r.url else None)
    pg.on("requestfailed", lambda r: seen.__setitem__("FAILED " + r.url.split("?")[0].replace(H, ""), round(time.monotonic() - t_nav, 1)) if "/api/" in r.url else None)
    pg2 = pg.context.new_page()
    pg2.on("response", pg.listeners if False else (lambda r: seen.__setitem__(r.url.split("?")[0].replace(H, ""), [r.status, round(time.monotonic() - t_nav, 1)]) if "/api/" in r.url else None))
    pg = pg2
    t_nav = time.monotonic()
    pg.on("request", lambda r: seen.setdefault("started " + r.url.split("?")[0].replace(H, ""), round(time.monotonic() - t_nav, 1)) if "/api/" in r.url else None)
    msgs = []
    pg.on("console", lambda m: msgs.append(m.type + ": " + m.text[:160]) if m.type in ("error", "warning") else None)
    pg.on("pageerror", lambda e: msgs.append("pageerror: " + str(e)[:160]))
    res["console"] = msgs
    pg.goto(f"{H}/app#/screens?screen=asset-board" + (f"&case={cid}" if cid else ""))
    deadline = time.monotonic() + int(os.environ.get("UI_WAIT_MS", "240000")) / 1000
    while time.monotonic() < deadline:
        txt = pg.inner_text("body")
        if "Loaded" in txt or "AI report could not be loaded" in txt:
            break
        pg.wait_for_timeout(2000)
    body = pg.inner_text("body")
    res["ui_report_response_status"] = seen
    res["ui_heading_present"] = "Asset and board view" in body
    res["ui_report_loaded"] = "Loaded" in body
    res["ui_report_unavailable"] = "AI report could not be loaded" in body
    res["ui_lines"] = [ln.strip()[:160] for ln in body.splitlines() if "AI " in ln and ("quality" in ln or "report" in ln)][:8]
    res["ui_unknown_ai_count"] = body.count("could not be loaded")
    try:
        pg.get_by_text("AI cohort quality floor").first.scroll_into_view_if_needed(timeout=5000)
    except Exception:
        pass
    pg.screenshot(path=os.path.join(OUT, f"{label}.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, f"{label}.json"), "w"), indent=1)
print(json.dumps(res))
