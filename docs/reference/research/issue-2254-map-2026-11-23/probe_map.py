import json, os, re
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT + "/screens", exist_ok=True)
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


def get(page, path):
    return page.evaluate("async (u) => (await fetch(u, {credentials: 'same-origin'})).json()", path)


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/overview")
    pg.wait_for_timeout(8000)
    pg.locator("text=Map of open cases").scroll_into_view_if_needed()
    try:
        pg.wait_for_selector(".leaflet-marker-icon", timeout=60000)
    except Exception:
        pass
    pg.wait_for_timeout(3000)
    res["role"] = get(pg, "/api/me")["user"]["role"]
    res["tile"] = pg.locator("button.tile.danger").first.inner_text()
    body = pg.locator("body").inner_text()
    res["map_info"] = re.findall(r"[^\n]*(?:homes|records) in this[^\n]*", body)[:2]
    res["markers_total"] = pg.locator(".map-marker").count()
    res["markers_safety_title"] = pg.locator(".leaflet-marker-icon[title*='Safety issue open']").count()
    res["clusters"] = pg.locator(".map-cluster").count()
    res["cluster_titles"] = [t.get_attribute("title") for t in pg.locator(".leaflet-marker-icon[title*='Zoom in']").all()][:40]
    pg.screenshot(path=f"{OUT}/screens/01-overview-map.png")
    m = get(pg, "/api/map")
    res["api_map_keys"] = list(m.keys())[:12]
    items = m.get("items") or []
    res["api_map_mode"] = m.get("mode")
    res["api_map_total"] = m.get("total")
    res["api_map_item_hazards"] = sum(1 for i in items if i.get("kind") == "hazard") if m.get("mode") == "points" else sum(i.get("hazards", 0) for i in items)
    res["api_cases_hazard_total"] = get(pg, "/api/cases?view=all&flag=hazard&sort=urgent&limit=200")["total"]
    res["api_kpi_hazards"] = get(pg, "/api/stats")["kpis"]["hazards"]
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-map-result.json", "w").write(s)
    print(s)
    b.close()
