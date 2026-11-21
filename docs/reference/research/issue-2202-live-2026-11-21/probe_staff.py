import json, os
from collections import Counter
from playwright.sync_api import sync_playwright

H = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
home = os.path.expanduser("~")
u = open(home + "/.ama-test-user-id").read().strip()
p = open(home + "/.ama-test-user").read().strip()
HOOK = """
(() => { let real; Object.defineProperty(window, 'L', { configurable: true,
  set(v) { real = v; if (v && v.Map && v.Map.addInitHook) v.Map.addInitHook(function () { window.__map = this; }); },
  get() { return real; } }); })();
"""


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
    c.add_init_script(HOOK)
    pg = c.new_page()
    login(pg)
    me = c.request.get(H + "/api/me").json()["user"]
    res["role"] = me["role"]
    for _ in range(4):
        mr = c.request.get(H + "/api/map", timeout=90000)
        if mr.ok and "items" in mr.json():
            break
        pg.wait_for_timeout(5000)
    items = mr.json()["items"]
    res["map_total"] = len(items)
    res["map_sensor_states"] = dict(Counter((i.get("sensor") or {}).get("state") for i in items))
    fresh = [i for i in items if (i.get("sensor") or {}).get("state") == "fresh"]
    res["fresh_homes"] = len(fresh)
    res["fresh_max_age_seconds"] = max(i["sensor"]["age_seconds"] for i in fresh) if fresh else None
    res["share_with_readings_pct"] = round(100 * len([i for i in items if (i.get("sensor") or {}).get("state") in ("fresh", "stale", "offline")]) / len(items), 1)
    page_js = c.request.get(H + "/static/app.js").text() if c.request.get(H + "/static/app.js").ok else ""
    res["app_js_has_map_gauge"] = "map-gauge" in page_js or None
    # home tab chart
    cid = "ZF-2025-0031"
    pg.goto(f"{H}/app#/case/{cid}?tab=sensors")
    pg.wait_for_function("() => { const s = document.querySelector('#sensors .status-line'); return s && !/Loading/.test(s.textContent); }", timeout=90000)
    pg.wait_for_timeout(1500)
    sens = pg.locator("#sensors")
    res["tab_svg_count"] = sens.locator("svg").count()
    res["tab_chart_text"] = [t for t in sens.inner_text().split("\n") if t.strip()][:30]
    res["tab_axis_labels"] = sens.locator("svg text").all_inner_texts()[:40]
    res["tab_paths"] = sens.locator("svg path, svg polyline").count()
    sens.scroll_into_view_if_needed()
    pg.screenshot(path=f"{OUT}/screens/home-sensor-chart.png", full_page=True)
    # map gauges on a home card
    pg.goto(H + "/app#/overview")
    pg.wait_for_function("() => window.__map", timeout=60000)
    pg.wait_for_timeout(4000)
    target = fresh[0] if fresh else None
    if target:
        res["gauge_home"] = target["id"]
        pg.evaluate("([la, lo]) => window.__map.setView([la, lo], 18, {animate:false})", [target["lat"], target["lon"]])
        pg.wait_for_timeout(5000)
        mk = pg.locator(".leaflet-marker-icon")
        res["markers_visible"] = mk.count()
        if mk.count():
            mk.first.focus()
            pg.keyboard.press("Enter")
            pg.wait_for_timeout(1500)
        card = pg.locator(".map-home-card")
        res["card_visible"] = card.is_visible()
        if card.is_visible():
            res["card_text"] = card.inner_text()[:500]
            res["meters"] = pg.locator(".map-home-card meter").evaluate_all("els => els.map(e => [e.id, e.value, e.min, e.max])")
        pg.screenshot(path=f"{OUT}/screens/map-gauges.png")
    # employee chat routing
    chat = {}
    for q in ("Which documents are missing for this home?", "Is there a damp and mould hazard to chase?"):
        try:
            r = c.request.post(H + "/api/chat/unstored-ask", data=json.dumps({"content": q, "skill": "auto", "case_id": cid}),
                               headers={"Content-Type": "application/json"}, timeout=120000)
            j = r.json() if r.ok else {}
            chat[q] = {"http": r.status, "routing": j.get("routing"), "label": j.get("label")}
        except Exception as e:
            chat[q] = {"error": type(e).__name__}
    res["employee_chat"] = chat
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-staff-result.json", "w").write(s)
    print(s[:6000])
    b.close()
