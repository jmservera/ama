import json, os
from collections import Counter
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
    res["url_after_login"] = pg.url.split("#")[0].replace(H, "")
    me = c.request.get(H + "/api/me")
    res["me_status"] = me.status
    res["role"] = me.json().get("user", {}).get("role") if me.ok else None
    items = []
    for _ in range(4):
        mr = c.request.get(H + "/api/map", timeout=90000)
        res["map_status"] = mr.status
        if mr.ok and "items" in mr.json():
            items = mr.json()["items"]
            break
        pg.wait_for_timeout(5000)
    res["map_total"] = len(items)
    res["sensor_states"] = dict(Counter((i.get("sensor") or {}).get("state") for i in items))
    pg.goto(H + "/app#/overview")
    pg.wait_for_timeout(8000)
    pg.screenshot(path=f"{OUT}/screens/employee-map.png")
    res["markers_in_dom"] = pg.locator(".leaflet-marker-icon, .leaflet-interactive").count()
    s = json.dumps(res, indent=1)
    assert u not in s and p not in s
    open(OUT + "/probe-staff-map-result.json", "w").write(s)
    print(s)
    b.close()
