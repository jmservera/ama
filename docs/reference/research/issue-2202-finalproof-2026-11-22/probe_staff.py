"""Staff proofs for #2202 deploy proof: items 1, 4, 5, 6. Sign-in values are read at run time, never printed."""
import json, os, re, time
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


def txt(pg, sel="main", n=3000):
    return re.sub(r"\s+", " ", pg.inner_text(sel))[:n]


res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    login(pg)
    # 6 and 4: map with readings, tile and markers
    t0 = time.time()
    pg.goto(H + "/app#/overview")
    try:
        pg.wait_for_selector(".leaflet-marker-icon", timeout=90000)
        res["map_markers_secs"] = round(time.time() - t0, 1)
    except Exception:
        res["map_markers_secs"] = None
    pg.wait_for_timeout(5000)
    body = txt(pg, "main", 6000)
    res["overview_text"] = body[:1500]
    res["tile_safety"] = re.findall(r"(\d+)\s*Safety issues? open", body) or re.findall(r"Safety issues? open\s*(\d+)", body)
    titles = pg.evaluate("[...document.querySelectorAll('.leaflet-marker-icon')].map(e=>e.title)")
    res["markers"] = len(titles)
    res["safety_markers"] = sum("afety" in t for t in titles)
    pg.screenshot(path=f"{OUT}/screens/staff-overview-map.png")
    mr = c.request.get(H + "/api/map", timeout=90000)
    items = mr.json().get("items", []) if mr.ok else []
    res["map_status"] = mr.status
    res["map_items"] = len(items)
    from collections import Counter
    res["sensor_states"] = dict(Counter((i.get("sensor") or {}).get("state") for i in items))
    res["map_hazard_items"] = sum(1 for i in items if i.get("hazard") or i.get("flags", {}).get("hazard") if isinstance(i, dict))
    # 4: list
    api = c.request.get(H + "/api/cases?view=all&flag=hazard&sort=urgent", timeout=90000)
    res["api_hazard_total"] = api.json().get("total") if api.ok else api.status
    pg.goto(H + "/app#/all"); pg.wait_for_timeout(7000)
    pg.get_by_label("Show only").select_option(label="Safety issue open")
    pg.wait_for_timeout(5000)
    t = txt(pg, "main", 400000)
    res["list_heading"] = re.findall(r"All open cases (\d+) cases?", t)
    # 1: clocks
    res["clock_unknown"] = len(re.findall(r"elapsed time unknown; no response target window recorded", t))
    res["clock_with_elapsed"] = len(re.findall(r"Hazard clock: \d+ hours elapsed", t))
    res["service_response_due"] = len(re.findall(r"service response due", t))
    res["named_owners"] = len(re.findall(r"Accountable owner: [A-Z][a-z]+ [A-Z][a-z]+", t))
    m = re.search(r"Hazard clock: \d+ hours elapsed.{0,300}", t)
    res["clock_sample"] = m.group(0) if m else None
    pg.screenshot(path=f"{OUT}/screens/staff-safety-list.png")
    # 5: handoff waiting
    pg.goto(H + "/app#/handoff-waiting"); pg.wait_for_timeout(8000)
    res["handoff_text"] = txt(pg, "main", 2500)
    res["handoff_rows"] = pg.locator("main tbody tr").count()
    pg.screenshot(path=f"{OUT}/screens/staff-handoff-waiting.png")
    pg.goto(H + "/app#/case/ZF-2025-0030"); pg.wait_for_timeout(6000)
    ct = txt(pg, "main", 400000)
    m = re.search(r".{0,80}Offered to .{0,150}", ct)
    res["case_0030_offer"] = m.group(0) if m else None
    s = json.dumps(res, indent=1, default=str)
    assert u not in s and p not in s
    open(OUT + "/probe-staff-result.json", "w").write(s)
    print(s)
    b.close()
