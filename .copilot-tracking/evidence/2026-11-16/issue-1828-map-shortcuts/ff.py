import sys
from pathlib import Path
from checks.design_system_browser_check import main
from checks import map_fullscreen_browser_check as m
from playwright.sync_api import sync_playwright, expect
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
def run(base):
    with sync_playwright() as pw:
        b = pw.chromium.launch(); ctx = b.new_context(viewport={"width":1280,"height":900})
        page = ctx.new_page()
        page.goto(base + "/app")
        page.locator("#email").fill("sam@example.test"); page.locator("#pw").fill("synthetic-check")
        page.get_by_role("button", name="Sign in", exact=True).click()
        page.get_by_role("heading", name="My cases today").wait_for()
        page.get_by_role("link", name="Overview", exact=True).click()
        page.locator(".map-cluster").first.wait_for()
        page.locator("#mapArea").select_option(label="Point examples")
        expect(page.locator(".map-marker")).to_have_count(3)
        page.wait_for_timeout(1000)
        for i in range(N):
            try:
                m.check_shortcuts_after_pending_resize(page); print("RUN", i, "PASS")
            except AssertionError as e:
                print("RUN", i, "FAIL", e)
            page.wait_for_timeout(600)
        if len(sys.argv) > 2:
            page.evaluate("document.querySelector('#leaflet').addEventListener('keydown', e => { if (e.ctrlKey) setTimeout(() => fetch('/api/map?zoom=15&area=Point%20examples'), 100); })")
            try:
                m.check_browser_shortcuts(page, "mutant"); print("MUTANT PASS (bad)")
            except AssertionError as e:
                print("MUTANT FAIL (good)", e)
        b.close()
main(run)
