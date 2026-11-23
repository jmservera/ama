"""Live probe for #2303: GET /api/ai/report and the Asset and board view on the demo."""
import json, os
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


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    res["role"] = c.request.get(H + "/api/me").json()["user"]["role"]
    r = c.request.get(H + "/api/ai/report", timeout=120000)
    res["ai_report_status"] = r.status
    if r.ok:
        d = r.json()
        res["keys"] = sorted(d)[:20]
        res["has_consumption"] = bool(d.get("consumption"))
    pg.goto(H + "/app#/asset-board")
    pg.wait_for_timeout(10000)
    txt = pg.locator("main").inner_text() if pg.locator("main").count() else pg.inner_text("body")
    res["screen_excerpt"] = txt[:700]
    res["shows_could_not_be_loaded"] = "could not be loaded" in txt
    res["ai_report_loaded_text"] = "Loaded" in txt
    pg.screenshot(path=f"{OUT}/screens/asset-board-live.png", full_page=True)
    b.close()
json.dump(res, open(f"{OUT}/probe-result.json", "w"), indent=2)
print(json.dumps(res, indent=1)[:2500])
