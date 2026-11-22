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


def get(page, path):
    return page.evaluate("async (u) => (await fetch(u, {credentials: 'same-origin'})).json()", path)


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app")
    pg.wait_for_timeout(4000)
    st = get(pg, "/api/stats")
    res["kpis_hazards"] = st["kpis"]["hazards"]
    res["kpis_open"] = st["kpis"]["open"]
    lst = get(pg, "/api/cases?view=all&flag=hazard&sort=urgent&limit=200")
    res["list_total"] = lst["total"]
    list_ids = {x["id"] for x in lst["items"]}
    mp = get(pg, "/api/map")
    res["map_mode"] = mp.get("mode")
    res["map_hazard_items"] = sum(1 for x in mp.get("items", []) if x.get("kind") == "hazard")
    map_ids = {x["id"] for x in mp.get("items", []) if x.get("kind") == "hazard"}
    res["in_map_not_list"] = sorted(map_ids - list_ids)
    res["in_list_not_map"] = sorted(list_ids - map_ids)
    for cid in res["in_map_not_list"]:
        d = get(pg, "/api/cases/" + cid)
        res["detail_" + cid] = {
            "hazards": [{k: h.get(k) for k in ("category", "released", "standalone_safeguarding", "item_kind")} for h in d.get("hazards", [])],
            "safeguarding_keys": [k for k in d if "safeguard" in k],
            "closed": d.get("closed"), "stage": d.get("stage"),
        }
    pg.screenshot(path=f"{OUT}/screens/overview-2254.png")
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-safety-count-result.json", "w").write(s)
    print(s[:3000])
    b.close()
