import json, os, sys
from collections import Counter
from playwright.sync_api import sync_playwright
H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip(); p = open(home + "/.ama-test-user").read().strip()
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
    b = pw.chromium.launch(); c = b.new_context(viewport={"width": 1440, "height": 900}); pg = c.new_page()
    login(pg)
    me = c.request.get(H + "/api/me").json()["user"]
    res["role"] = me["role"]; res["app_roles"] = me["app_roles"]
    for _ in range(4):
        mr = c.request.get(H + "/api/map", timeout=90000)
        if mr.ok and "items" in mr.json():
            break
        pg.wait_for_timeout(5000)
    res["map_http"] = mr.status
    items = mr.json()["items"]
    res["map_total"] = len(items)
    res["map_sensor_states"] = dict(Counter((i.get("sensor") or {}).get("state") for i in items))
    fresh = [(i["id"], i["sensor"]["age_seconds"]) for i in items if (i.get("sensor") or {}).get("state") == "fresh"]
    res["fresh_homes"] = len(fresh); res["fresh_max_age_seconds"] = max(a for _, a in fresh)
    res["stale_or_offline_homes"] = [i["id"] for i in items if (i.get("sensor") or {}).get("state") in ("stale", "offline")]
    for cid in ("ZF-2025-0031", "ZF-2025-0148", "ZF-2025-0331"):
        r = c.request.get(f"{H}/api/cases/{cid}/sensors"); j = r.json()
        res["sensors_" + cid] = {"http": r.status, "state": j.get("state"), "freshness": j.get("freshness"), "readings": len(j.get("readings") or []), "age_seconds": j.get("age_seconds")}
    pr = c.request.get(H + "/api/progress"); res["progress_http"] = pr.status
    if pr.ok:
        d = pr.json(); res["progress_keys"] = list(d)[:12]; res["progress_days"] = len(d.get("daily", []))
    seen = []
    pg.on("response", lambda r: seen.append((r.status, r.url.split("/api/")[-1][:60])) if "/sensors" in r.url else None)
    for cid, tag in (("ZF-2025-0031", "granted"), ("ZF-2025-0148", "declined")):
        pg.goto(f"{H}/app#/case/{cid}?tab=sensors"); pg.wait_for_function("() => { const s = document.querySelector('#sensors .status-line'); return s && !/Loading/.test(s.textContent); }", timeout=60000); pg.wait_for_timeout(1000)
        t = pg.locator("#sensors").inner_text() if pg.locator("#sensors").count() else ""
        res["tab_" + tag] = t[:900]
        pg.screenshot(path=f"{OUT}/screens/home-sensors-{tag}.png")
    res["browser_sensor_responses"] = seen
    pg.goto(H + "/app#/progress"); pg.wait_for_timeout(3500)
    res["progress_charts"] = pg.locator("svg.chart, .progress-chart").count()
    res["progress_headings"] = [h for h in pg.locator("h2").all_inner_texts()][:10]
    pg.screenshot(path=f"{OUT}/screens/progress-charts.png", full_page=False)
    pg.goto(H + "/app#/overview"); pg.wait_for_timeout(6000)
    cb = pg.locator("#map-sensor-alerts")
    res["map_filter_present"] = cb.count()
    if cb.count():
        cb.check(); pg.wait_for_timeout(1500)
        res["map_filter_text"] = [x for x in pg.locator("body").inner_text().split("\n") if "stale or offline" in x][:2]
    pg.screenshot(path=f"{OUT}/screens/map-filter.png")
    for name in ("forecast", "rai-metrics"):
        try:
            r = c.request.get(f"{H}/api/assistants/{name}", timeout=90000)
            res[name] = {"http": r.status, "body": (json.dumps(r.json())[:900] if r.ok else None)}
        except Exception:
            res[name] = {"http": None, "body": "request timed out or failed"}
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-result.json", "w").write(s); print(s[:5000])
    b.close()
