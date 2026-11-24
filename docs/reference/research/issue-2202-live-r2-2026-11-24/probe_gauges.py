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
    me = c.request.get(H + "/api/me")
    print("me", me.status)
    cases = c.request.get(H + "/api/cases")
    print("cases", cases.status)
    data = cases.json() if cases.ok else []
    items = data if isinstance(data, list) else data.get("cases", data.get("items", []))
    ids = [x.get("id") or x.get("case_id") for x in items]
    print("n", len(ids))
    summary = []
    for cid in ids:
        r = c.request.get(f"{H}/api/cases/{cid}/sensors")
        if not r.ok:
            summary.append((cid, r.status)); continue
        j = r.json()
        summary.append((cid, r.status, j.get("kind"), len(j.get("readings") or []), (j.get("latest") or {}).get("observed_at"), j.get("alerts") if "alerts" in j else None))
    from collections import Counter
    print("sensor status counts", dict(Counter((x[1], x[2] if len(x) > 2 else None) for x in summary)))
    live = [x[0] for x in summary if len(x) > 3 and x[3] >= 2]
    print("homes with chart data", live)
    cid = live[0]
    pg.goto(f"{H}/app#/case/{cid}")
    pg.wait_for_timeout(2500)
    pg.get_by_role("tab", name="Home sensors").click()
    pg.wait_for_selector("[data-sensor-chart]", timeout=90000)
    fig = pg.locator("[data-sensor-chart]")
    fig.scroll_into_view_if_needed()
    pg.screenshot(path=OUT + "/live-home-sensors-chart.png")
    probe = pg.evaluate("""() => {
      const f = document.querySelector('[data-sensor-chart]');
      const svg = f.querySelector('svg');
      const cs = (sel) => getComputedStyle(f.querySelector(sel));
      const axes = [...svg.querySelectorAll('.sensor-chart-axis')].map(t => t.textContent);
      const ticks = [...svg.querySelectorAll('.sensor-chart-tick')].map(t => [t.getAttribute('text-anchor'), t.textContent]);
      return {
        axes, leftTicks: ticks.filter(t => t[0] === 'end').map(t => t[1]),
        rightTicks: ticks.filter(t => t[0] === 'start').map(t => t[1]),
        tempDash: cs('polyline.temp').strokeDasharray, humidDash: cs('polyline.humid').strokeDasharray,
        circles: svg.querySelectorAll('circle.temp').length, squares: svg.querySelectorAll('rect.humid').length,
        role: svg.getAttribute('role'), describedby: svg.getAttribute('aria-describedby'),
        summary: document.getElementById('sensor-chart-summary')?.textContent.slice(0, 400),
        key: [...f.querySelectorAll('.sensor-chart-key li')].map(l => l.textContent.trim()),
        tableRows: [...document.querySelectorAll('#case-panel-sensors table')].map(t => [t.querySelector('caption')?.textContent, t.querySelectorAll('tbody tr').length]),
        animations: document.getAnimations().filter(a => a.playState === 'running').length,
        overflowX: document.documentElement.scrollWidth > innerWidth,
        old: f.classList.contains('out-of-date'),
        reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
      };
    }""")
    print(json.dumps(probe, indent=1))
    json.dump(probe, open(OUT + "/live-chart-probe.json", "w"), indent=1)
    api = c.request.get(f"{H}/api/cases/{cid}/sensors").json()
    rd = api.get("readings") or []
    print("api keys", list(api)[:8])
    if rd: print("api readings", len(rd), "temp", min(r["temperature_c"] for r in rd), max(r["temperature_c"] for r in rd),
          "rh", min(r["humidity_pct"] for r in rd), max(r["humidity_pct"] for r in rd))
    pg.screenshot(path=OUT + "/live-home-sensors-tab-full.png", full_page=False)
    # map card on the overview
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
    withr = pg.locator('.map-marker[title*="relative humidity"]')
    n = withr.count()
    print("markers", pg.locator(".map-marker").count(), "with readings in label", n)
    shown = None
    if n:
        withr.first.focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(1000)
        if pg.locator(".map-home-card").is_visible() and pg.locator(".map-home-card meter").count():
            shown = 0
    print("marker with gauges", shown)
    if shown is not None:
        card = pg.locator(".map-home-card")
        card.scroll_into_view_if_needed()
        card.screenshot(path=OUT + "/live-map-card-top.png")
        print("card scroll", card.evaluate("el => [el.clientHeight, el.scrollHeight]"))
        card.evaluate("el => { el.scrollTop = el.scrollHeight; }"); pg.wait_for_timeout(500)
        card.screenshot(path=OUT + "/live-map-card-gauges.png")
        gp = card.evaluate("""(el) => ({
          title: el.querySelector('#map-home-title').textContent,
          latest: el.querySelector('.map-sensor-list').innerText,
          meters: [...el.querySelectorAll('meter')].map(m => ({label: m.getAttribute('aria-label'), value: m.value, min: m.min, max: m.max, text: m.textContent})),
          labels: [...el.querySelectorAll('.map-gauge label')].map(l => l.textContent),
          old: !!el.querySelector('.map-gauges.out-of-date'),
          oldNote: el.querySelector('.map-gauges p')?.textContent,
          animations: document.getAnimations().filter(a => a.playState === 'running').length,
        })""")
        print(json.dumps(gp, indent=1))
        json.dump(gp, open(OUT + "/live-map-card-probe.json", "w"), indent=1)
    pg.screenshot(path=OUT + "/live-map.png")
    b.close()
