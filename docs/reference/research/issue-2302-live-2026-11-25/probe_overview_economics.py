"""Live probe for #2302: the Overview management view's AI consumption economics card.

Sign-in values are read from the owner's home files at run time and never printed or stored.
Writes overview-economics.json and overview-economics.png beside this file.
"""
import json
import os
import re

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context(viewport={"width": 1440, "height": 1000}).new_page()
    pg.goto(H + "/sign-in")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", u)
                pg.click("input[type=submit]")
                pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", p)
                pg.click("input[type=submit]")
                pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000):
                pg.click("#idBtn_Back")
                pg.wait_for_timeout(2000)
        except Exception:
            pass
    stats = {}
    pg.on("response", lambda r: stats.update(status=r.status) if r.url.split("?")[0].endswith("/api/stats") else None)
    pg.goto(H + "/app#/overview")
    res = {"status": None}
    try:
        pg.wait_for_selector("#ai-economics-heading", timeout=180000)
        card = pg.locator("section[aria-labelledby=ai-economics-heading]")
        card.scroll_into_view_if_needed()
        text = card.inner_text()
        res["card_text"] = re.sub(r"\n+", " | ", text)
        res["dt_dd"] = card.evaluate("e => [...e.querySelectorAll('dt')].map(t => [t.textContent, t.nextElementSibling.textContent])")
        pg.screenshot(path=OUT + "/overview-economics.png", full_page=False)
    except Exception as e:
        res["error"] = type(e).__name__
        pg.screenshot(path=OUT + "/overview-economics-failed.png")
    res["stats_status"] = stats.get("status")
    json.dump(res, open(OUT + "/overview-economics.json", "w"), indent=1)
    b.close()
