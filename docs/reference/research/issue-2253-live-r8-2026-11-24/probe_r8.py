import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent
URL = "https://ca-resident-demo.happyriver-ace49996.uksouth.azurecontainerapps.io"
EMAIL, PASSWORD = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
JS = """() => {
  const svg = [...document.querySelectorAll('svg')].find(s => s.querySelector('.sensor-line, .sensor-point'));
  const r = svg.getBoundingClientRect();
  const scale = r.width / svg.viewBox.baseVal.width;
  const body = parseFloat(getComputedStyle(document.body).fontSize);
  const texts = [...svg.querySelectorAll('text')].map(t => ({t: t.textContent, px: parseFloat(getComputedStyle(t).fontSize), box: t.getBoundingClientRect()}));
  let overlaps = 0;
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i].box, b = texts[j].box;
    if (a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom) overlaps++;
  }
  const circles = [...svg.querySelectorAll('circle.sensor-point')].map(c => ({x: +c.getAttribute('cx'), y: +c.getAttribute('cy'), r: +c.getAttribute('r')}));
  let touching = 0;
  for (let i = 1; i < circles.length; i++) if (Math.hypot(circles[i].x - circles[i-1].x, circles[i].y - circles[i-1].y) < 2 * circles[i].r) touching++;
  const legend = (svg.closest('figure') || document).innerText;
  return {scale, body_px: body, text: texts.map(t => [t.t, +t.px.toFixed(1)]), text_overlaps: overlaps,
    circles: circles.length, touching_circles: touching,
    forecast_squares: svg.querySelectorAll('.sensor-forecast-point').length,
    latest_label: texts.some(t => t.t === 'Latest stored'), legend: legend.slice(0, 400)};
}"""
tag = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    page.goto(URL + "/", wait_until="networkidle", timeout=90000)
    page.fill("input[type=email], input[name=email], #email", EMAIL)
    page.fill("input[type=password]", PASSWORD)
    page.keyboard.press("Enter")
    page.wait_for_selector("#account:not([hidden])", timeout=90000)
    page.wait_for_timeout(4000)
    page.get_by_text("Sensors", exact=True).first.click()
    page.wait_for_timeout(1500)
    page.wait_for_timeout(2000)
    print(page.locator("#sec-sensors").inner_text()[:1500])
    page.locator("#sec-sensors svg").first.scroll_into_view_if_needed(timeout=5000)
    res = page.evaluate(JS)
    page.locator("#sec-sensors figure.sensor-chart").first.screenshot(path=str(OUT / f"live-{tag}.png"))
    res["figcaption"] = page.locator("#sec-sensors figure.sensor-chart").first.locator("figcaption").inner_text()[:500]
    res["forecast_heading"] = page.locator("#sec-sensors .forecast-heading, #sec-sensors .forecast-reason").all_inner_texts()
    (OUT / f"live-{tag}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res))
    b.close()
