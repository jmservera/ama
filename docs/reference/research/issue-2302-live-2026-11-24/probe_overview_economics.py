"""Capture the Overview AI consumption economics card on the live demo for #2302.

Sign-in values are read from the owner's home files at run time and never printed or stored.
Writes overview-economics.json (API payload and rendered text) and overview-economics.png beside this file.
"""
import json
import os

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


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 1000})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/overview")
    pg.wait_for_selector("#ai-economics-heading", timeout=60000)
    r = pg.request.get(H + "/api/stats", headers={"X-ZF-CSRF": "1"})
    res["stats_status"] = r.status
    res["ai_consumption_economics"] = r.json().get("ai_consumption_economics")
    card = pg.locator("section[aria-labelledby=ai-economics-heading]")
    card.scroll_into_view_if_needed()
    res["card_text"] = card.inner_text()
    card.screenshot(path=os.path.join(OUT, "overview-economics.png"))
    b.close()
json.dump(res, open(os.path.join(OUT, "overview-economics.json"), "w"), indent=1)
print(res["stats_status"], res["card_text"])
