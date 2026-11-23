"""Resident smoke: login and Home sensors chart. Credentials are read at runtime and never printed or saved."""
import json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    for _ in range(8):
        try:
            res["session_status"] = page.request.get(URL + "/demo/session", timeout=60000).status
            if res["session_status"] == 200:
                break
        except Exception:
            time.sleep(5)
    page.goto(URL + "/", wait_until="networkidle", timeout=90000)
    page.fill("input[type=email], input[name=email], #email", EMAIL)
    page.fill("input[type=password]", PASSWORD)
    with page.expect_response(lambda x: x.url.endswith("/demo/login")) as ri:
        page.keyboard.press("Enter")
    res["login_status"] = ri.value.status
    page.wait_for_selector("#account:not([hidden])", timeout=90000)
    page.wait_for_timeout(3000)
    page.get_by_text("Sensors", exact=True).first.click(); page.wait_for_timeout(3000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(OUT / "screens/resident-sensors-tab.png"), full_page=True)
    info = page.evaluate("""() => { const f = document.querySelector('[data-sensor-chart]'); const svgs = [...document.querySelectorAll('svg')].filter(s => s.querySelectorAll('text').length > 3 || s.querySelectorAll('path,polyline').length > 0);
      const m = document.body.innerText.match(/Temperature history[^\\n]*/); return {fig: !!f, svgs: svgs.length, circles: f ? f.querySelectorAll('circle').length : 0, caption: m ? m[0] : null, notice: [...document.querySelectorAll('p')].map(p => p.innerText).filter(t => /history|chart|forecast/i.test(t)).slice(0, 4)} }""")
    chart = page.locator("[data-sensor-chart], figure:has(svg)").first
    if chart.count():
        chart.scroll_into_view_if_needed(); page.wait_for_timeout(500)
    page.screenshot(path=str(OUT / "screens/resident-sensors-chart.png"))
    res["chart"] = info
    s = json.dumps(res, indent=1)
    assert EMAIL not in s and PASSWORD not in s
    (OUT / "probe-resident-result.json").write_text(s)
    print(s)
    b.close()
