"""Live probes for #2202: raw /api/map snapshot and resident consent checkbox. Sign-in values are read at run time, never printed."""
import json, re, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
API = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
RES = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
home = Path.home()
u = (home / ".ama-test-user-id").read_text().strip()
p = (home / ".ama-test-user").read_text().strip()
EMAIL, PASSWORD = (home / ".ama-resident-test-user").read_text().splitlines()[:2]
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900})
    pg = c.new_page()
    pg.goto(API + "/sign-in")
    for _ in range(4):
        try:
            if pg.locator("input[name=loginfmt]").is_visible(timeout=3000):
                pg.fill("input[name=loginfmt]", u); pg.click("input[type=submit]"); pg.wait_for_timeout(1500)
            if pg.locator("input[name=passwd]").is_visible(timeout=3000):
                pg.fill("input[name=passwd]", p); pg.click("input[type=submit]"); pg.wait_for_timeout(2000)
            if pg.locator("#idBtn_Back").is_visible(timeout=2000):
                pg.click("#idBtn_Back"); pg.wait_for_timeout(2000)
        except Exception:
            pass
    pg.wait_for_load_state("networkidle")
    t0 = time.time()
    pg.goto(API + "/app#/overview")
    try:
        pg.wait_for_selector(".leaflet-marker-icon", timeout=90000)
    except Exception:
        pass
    pg.wait_for_timeout(4000)
    pg.screenshot(path=str(OUT / "screens/staff-map.png"))
    r = c.request.get(API + "/api/map", timeout=90000)
    res["map_status"] = r.status
    if r.ok:
        (OUT / "map-snapshot.json").write_text(json.dumps(r.json()))
    # map card gauge: click a marker and read the popup/card text
    try:
        pg.locator(".leaflet-marker-icon").first.click(timeout=5000, force=True)
        pg.wait_for_timeout(2000)
        res["card_text"] = re.sub(r"\s+", " ", pg.inner_text("main"))[:1500]
        res["gauge_elements"] = pg.evaluate("document.querySelectorAll('[role=meter],meter,progress,[class*=gauge]').length")
        pg.screenshot(path=str(OUT / "screens/staff-map-card.png"))
    except Exception as e:
        res["card_error"] = str(e)[:200]
    # resident consent checkbox
    rp = c.new_page()
    for _ in range(8):
        try:
            if rp.request.get(RES + "/demo/session", timeout=60000).status == 200:
                break
        except Exception:
            time.sleep(5)
    rp.goto(RES + "/", wait_until="networkidle", timeout=90000)
    rp.fill("input[type=email], input[name=email], #email", EMAIL)
    rp.fill("input[type=password]", PASSWORD)
    with rp.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        rp.keyboard.press("Enter")
    res["resident_login"] = ri.value.status
    rp.wait_for_selector("#account:not([hidden])", timeout=90000)
    rp.click("#chat-launcher"); rp.wait_for_timeout(800)
    cb = rp.locator("#assistant-consent")
    res["consent_visible"] = cb.is_visible()
    res["consent_checked_before"] = cb.is_checked()
    cb.check()
    res["consent_checked_after"] = cb.is_checked()
    res["consent_label"] = rp.evaluate("(document.querySelector('label[for=assistant-consent]')||{}).innerText||null")
    rp.screenshot(path=str(OUT / "screens/resident-consent.png"))
    b.close()
(OUT / "probe-live-result.json").write_text(json.dumps(res, indent=1))
print({k: (v if k not in ("card_text",) else "...") for k, v in res.items()})
