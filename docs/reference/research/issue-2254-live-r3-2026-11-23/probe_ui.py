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
    page.wait_for_timeout(6000)


def get(page, path):
    return page.evaluate("async (u) => (await fetch(u, {credentials: 'same-origin'})).json()", path)


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/overview")
    pg.wait_for_timeout(6000)
    res["role"] = get(pg, "/api/me")["user"]["role"]
    res["overview_tile_text"] = pg.locator("button.tile.danger").first.inner_text()
    pg.screenshot(path=f"{OUT}/screens/01-overview-tile.png")
    pg.goto(H + "/app#/all")
    pg.wait_for_timeout(3000)
    sel = pg.get_by_label("Show only").first
    sel.select_option(label="Safety issue open")
    pg.wait_for_timeout(3000)
    res["list_count_text"] = __import__("re").findall(r"(?m)^\d+ cases?\b[^\n]*", pg.locator("body").inner_text())[:2]
    res["show_only_in_status"] = __import__("re").findall(r"Show only: [^.]*\.", pg.locator("body").inner_text(), flags=0)[:1]
    res["api_total"] = get(pg, "/api/cases?view=all&flag=hazard&sort=urgent&limit=200")["total"]
    res["api_kpi"] = get(pg, "/api/stats")["kpis"]["hazards"]
    pg.screenshot(path=f"{OUT}/screens/02-all-cases-safety-filter.png")
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-ui-result.json", "w").write(s)
    print(s)
    b.close()
