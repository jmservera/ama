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



with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = c.new_page()
    msgs = []
    pg.on("console", lambda m: msgs.append((m.type, m.text[:200])))
    pg.on("pageerror", lambda e: msgs.append(("pageerror", str(e)[:300])))
    login(pg)
    cid = "ZF-2025-0331"
    pg.goto(f"{H}/app#/case/{cid}")
    pg.wait_for_timeout(3000)
    pg.get_by_role("tab", name="Home sensors").click()
    pg.wait_for_timeout(6000)
    t = pg.evaluate("() => { const p=document.querySelector('[role=tabpanel]:not([hidden])')||document.querySelector('main'); return p.innerText.slice(0,1200) }")
    print(t)
    print(msgs[:10])
    pg.screenshot(path=OUT + "/diag-sensors-tab.png")
    b.close()
