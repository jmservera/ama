"""Live observation of the Home sensors chart and map card gauges (issue 2193).
Credentials are read at runtime and never printed."""
import json, os, sys
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


with sync_playwright() as pw:
    b = pw.chromium.launch()
    c = b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    pg = c.new_page()
    login(pg)
    pg.goto(f"{H}/app")
    pg.get_by_role("link", name="Overview", exact=True).click()
    pg.wait_for_selector("#leaflet", timeout=90000)
    pg.wait_for_timeout(5000)
    for _ in range(8):
        if pg.locator(".map-marker").count():
            break
        cl = pg.locator(".map-cluster").first
        if not cl.count():
            break
        cl.click(); pg.wait_for_timeout(2500)
    print("markers", pg.locator(".map-marker").count())
    tried = 0; shown = False
    for i in range(min(60, pg.locator(".map-marker").count())):
        m = pg.locator(".map-marker").nth(i)
        try:
            m.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(1500)
        except Exception:
            continue
        tried += 1
        if pg.locator(".map-home-card").is_visible() and pg.locator(".map-home-card meter").count():
            shown = True; break
    print("markers tried", tried, "gauge card shown", shown)
    if shown:
        card = pg.locator(".map-home-card")
        card.scroll_into_view_if_needed()
        card.screenshot(path=OUT + "/live-map-card-top.png")
        card.evaluate("el => { el.scrollTop = el.scrollHeight; }"); pg.wait_for_timeout(500)
        card.screenshot(path=OUT + "/live-map-card-gauges.png")
        gp = card.evaluate("""(el) => ({
          title: el.querySelector('#map-home-title').textContent,
          latest: el.querySelector('.map-sensor-list').innerText,
          meters: [...el.querySelectorAll('meter')].map(m => ({label: m.getAttribute('aria-label'), value: m.value, min: m.min, max: m.max, text: m.textContent})),
          labels: [...el.querySelectorAll('.map-gauge label')].map(l => l.textContent),
          old: !!el.querySelector('.map-gauges.out-of-date'),
          animations: document.getAnimations().filter(a => a.playState === 'running').length,
        })""")
        print(json.dumps(gp, indent=1))
        json.dump(gp, open(OUT + "/live-map-card-probe.json", "w"), indent=1)
    pg.screenshot(path=OUT + "/live-map.png")
    b.close()
