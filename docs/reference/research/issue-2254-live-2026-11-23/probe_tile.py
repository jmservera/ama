"""Staff safety tile / map / list probe for #2254. Usage: python3 probe_tile.py before|after.

Sign-in values are read from the owner's home files at run time and never printed or stored.
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
label = sys.argv[1]
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
    page.wait_for_timeout(3000)


def get(c, path):
    r = c.request.get(H + path)
    return r.json() if r.ok else {"status": r.status}


res = {"label": label}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    pg.goto(H + "/app#/overview")
    pg.wait_for_timeout(10000)
    pg.screenshot(path=f"{OUT}/screens/overview-{label}.png")
    res["tile_texts"] = [t.replace("\n", " ") for t in pg.locator("button.tile").all_inner_texts()]
    res["map_markers_titled_safety"] = pg.locator("[aria-label*='Safety issue open'], [title*='Safety issue open']").count()
    res["stats_kpis"] = get(c, "/api/stats").get("kpis")
    m = get(c, "/api/map?flag=hazard&zoom=20")
    res["map_flag_hazard_mode"] = m.get("mode")
    res["map_hazard_points"] = sorted(i["id"] for i in m.get("items", []) if i.get("kind") == "hazard")
    listed, off = [], 0
    while True:
        d = get(c, f"/api/cases?view=all&flag=hazard&sort=urgent&limit=100&offset={off}")
        listed += [i["id"] for i in d.get("items", [])]
        res["list_total"] = d.get("total")
        off += 100
        if off >= (d.get("total") or 0):
            break
    res["list_ids"] = sorted(listed)
    res["map_not_in_list"] = sorted(set(res["map_hazard_points"]) - set(listed))
    res["list_not_in_map"] = sorted(set(listed) - set(res["map_hazard_points"]))
    for cid in res["map_not_in_list"] + res["list_not_in_map"]:
        d = get(c, f"/api/cases/{cid}")
        res.setdefault("divergent_case_hazards", {})[cid] = [
            {k: h.get(k) for k in ("category", "released", "status", "standalone_safeguarding")}
            for h in d.get("hazards", [])
        ]
        res.setdefault("divergent_case_flags", {})[cid] = {k: d.get(k) for k in ("stage", "closed", "owner_code")}
    try:
        pg.goto(H + "/app#/all")
        pg.wait_for_timeout(12000)
        pg.get_by_label("Show only").select_option(label="Safety issue open", timeout=60000)
        pg.wait_for_timeout(6000)
        res["list_heading_text"] = [t for t in pg.inner_text("main").split("\n") if "cases" in t and any(ch.isdigit() for ch in t)][:4]
        pg.screenshot(path=f"{OUT}/screens/list-safety-{label}.png")
    except Exception as e:
        res["ui_list_error"] = type(e).__name__
    s = json.dumps(res, indent=1)
    open(f"{OUT}/probe-{label}.json", "w").write(s)
    print(s[:3500])
    b.close()
