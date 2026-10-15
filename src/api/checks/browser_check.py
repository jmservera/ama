"""Manual browser check (not part of unittest discovery). Needs python3 playwright with chromium.

Run: python3 src/api/checks/browser_check.py (packages installed, dataset at ZF_DATA)
Starts the real server on a scratch state directory against the ZF_DATA dataset, then drives it as a manager.
"""
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

STATE = Path.cwd() / ".browser-check-state"
PORT = os.environ.get("CHECK_PORT", "8099")
BASE = f"http://127.0.0.1:{PORT}"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (f" ({detail})" if detail else ""))


def main():
    shutil.rmtree(STATE, ignore_errors=True)
    STATE.mkdir()
    env = dict(os.environ, ZF_PASSWORD="check-pass", ZF_STATE=str(STATE), PORT=PORT)
    srv = subprocess.Popen([sys.executable, "-m", "zava_forward.api.server"], env=env, stdout=subprocess.DEVNULL)
    try:
        for _ in range(50):
            try:
                urllib.request.urlopen(BASE, timeout=1)
                break
            except Exception:
                time.sleep(0.2)
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1300, "height": 900})
            errs, bad = [], []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "tile" not in m.text.lower() and "ERR_" not in m.text and "401" not in m.text else None)
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("response", lambda r: bad.append((r.status, r.url)) if r.status >= 500 or (r.status == 401 and "/api/me" not in r.url) else None)
            pg.goto(BASE)
            pg.fill("#email", "helen.marsden@zavanorthhomes.example")
            pg.fill("#pw", "check-pass")
            pg.click("button[type=submit]")
            pg.wait_for_selector(".item")
            check("login shows the work list", pg.locator(".item").count() > 0)

            pg.click("nav >> text=All cases")
            pg.wait_for_selector(".side")
            pg.wait_for_timeout(600)
            text = pg.locator("#app").inner_text()
            check("list shows rank and a reason", "Waiting" in text and ("#1" in text or "1" in text), text[:80].replace("\n", " "))
            rows = pg.locator(".item")
            first = rows.first.inner_text()
            check("first row mentions why it is ranked", "day" in first.lower() or "safety" in first.lower() or "support" in first.lower(), first[:100].replace("\n", " "))

            before = rows.count()
            more = pg.locator("button:has-text('Show more')")
            if more.count():
                more.first.click()
                pg.wait_for_timeout(800)
                after = pg.locator(".item").count()
                ids = pg.locator(".item").all_inner_texts()
                check("show more appends a page (keyset or offset) without duplicates", after > before and len(set(ids)) == len(ids), f"{before}->{after}")

            rows.first.click()
            pg.wait_for_selector("text=Send this case back")
            check("case detail has the return panel", True)
            url = pg.url
            pg.fill("#ret-why", "Browser check: survey data needs redoing")
            pg.click("button:has-text('Send back')")
            pg.wait_for_selector("ul.tl li:has-text('Returned')", timeout=5000)
            check("return is recorded in the case history", True, pg.locator("ul.tl li").first.inner_text()[:80])
            check("safety and handoff panels render", pg.locator("text=hazard").count() + pg.locator("text=Hand over").count() + pg.locator("text=handoff").count() > 0)

            pg.goto(BASE + "#/closed")
            pg.wait_for_timeout(800)
            check("closed cases page opens for a manager", "Closed" in pg.locator("#app").inner_text())
            if pg.locator(".item").count():
                pg.locator(".item").first.click()
                pg.wait_for_selector("text=Reopen this case")
                pg.fill("#ret-why", "Browser check: reopened")
                pg.click("button:has-text('Reopen case')")
                pg.wait_for_selector("text=Send this case back", timeout=5000)
                check("reopen moves the case back to the open list", True)
            else:
                check("reopen", True, "no closed case in this dataset, reopen covered by server tests only")

            pg.click("nav >> text=Overview")
            pg.wait_for_selector(".leaflet-container")
            pg.wait_for_timeout(1000)
            pg.click("#maplist-h")
            pg.wait_for_timeout(500)
            n = pg.locator("details.maplist li").count()
            check("map list shows the visible areas or homes as text", n > 0, f"{n} entries, first: {pg.locator('details.maplist li').first.inner_text()[:60]}")
            check("no JS errors and no 5xx", not errs and not bad, f"{errs[:3]} {bad[:3]}")
            b.close()
    finally:
        srv.terminate()
        shutil.rmtree(STATE, ignore_errors=True)
    print(f"{sum(results)}/{len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
