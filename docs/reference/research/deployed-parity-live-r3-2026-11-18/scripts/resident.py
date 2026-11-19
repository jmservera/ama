"""Resident demo: anonymous status, sign in with owner file (never printed), screenshot and heading only."""
import os, re, sys
from playwright.sync_api import sync_playwright
base = "https://" + sys.argv[1]
l = open(os.path.expanduser("~/.ama-resident-test-user")).read().splitlines()
with sync_playwright() as pw:
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    pg.goto(base + "/"); print("anon landed", re.sub(r"\?.*", "", pg.url)); pg.screenshot(path="../screens/resident-anon.png")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", l[0].strip()); pg.click("input[type=submit]"); pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", l[1].strip()); pg.click("input[type=submit]"); pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000): pg.click("#idBtn_Back"); pg.wait_for_timeout(2000)
        except Exception: pass
    pg.wait_for_load_state("networkidle")
    print("final", re.sub(r"\?.*", "", pg.url), "|", pg.title())
    h = pg.locator("h1").first
    print("h1:", h.inner_text()[:100] if h.count() else "-")
    pg.screenshot(path="../screens/resident-after-login.png")
    r = c.request.get(base + "/api/cases", max_redirects=0); print("resident /api/cases", r.status)
