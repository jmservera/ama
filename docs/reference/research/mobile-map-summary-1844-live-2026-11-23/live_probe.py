"""Live read-only probe of the employee map summary on the demo API app.

Reads sign-in inputs at runtime from the owner's home files; never prints them.
Usage: python3 live_probe.py <out-dir>
"""

import hashlib
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
username = (Path.home() / ".ama-test-user-id").read_text().strip()
raw = (Path.home() / ".ama-test-user").read_text().strip()
head, sep, tail = raw.partition("=")
password = tail.strip() if sep and " " not in head else raw


def sign_in(page):
    page.goto(APP + "/app")
    page.locator("input[type=email]").fill(username)
    page.locator("input[type=submit]").click()
    page.locator("input[type=password]").wait_for()
    page.locator("input[type=password]").fill(password)
    page.locator("input[type=submit]").click()
    page.get_by_role("button", name="No", exact=True).click()
    page.get_by_role("link", name="Overview", exact=True).wait_for()
    return "authenticated_callback"


UNCOVERED_JS = """() => {
  // Live data has hundreds of markers, most clipped by the map pane. Hit-test the two zoom
  // controls and up to five markers whose centre lies inside the map pane.
  const map = document.querySelector('.leafmap');
  const hit = c => {
    c.scrollIntoView({block: 'center', inline: 'center'});
    const b = c.getBoundingClientRect(); let hits = 0;
    for (const fx of [0.2, 0.5, 0.8]) for (const fy of [0.2, 0.5, 0.8]) {
      const t = document.elementFromPoint(b.left + b.width * fx, b.top + b.height * fy);
      if (t && (t === c || c.contains(t))) hits += 1;
    }
    return hits === 9;
  };
  const inPane = c => { const m = map.getBoundingClientRect(), b = c.getBoundingClientRect();
    const x = b.left + b.width / 2 - m.left, y = b.top + b.height / 2 - m.top;
    return x >= 0 && y >= 0 && x <= m.width && y <= m.height; };
  const zoom = [...map.querySelectorAll('.leaflet-control-zoom a')];
  const zoomCovered = zoom.filter(c => !hit(c)).length;
  map.scrollIntoView({block: 'start'});
  const markers = [...map.querySelectorAll('.map-marker')].filter(inPane).slice(0, 5);
  const markersCovered = markers.filter(c => !hit(c)).length;
  const card = document.querySelector('.map-home-card').getBoundingClientRect();
  const m = map.getBoundingClientRect();
  const overlap = !(card.bottom <= m.top || card.top >= m.bottom || card.right <= m.left || card.left >= m.right);
  return {zoom: zoom.length, zoomCovered, markersSampled: markers.length, markersCovered,
    cardOverlapsMap: overlap};
}"""
result = {}
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    ctx.set_default_timeout(15000)
    page = ctx.new_page()
    result["auth"] = sign_in(page)
    if result["auth"] == "authenticated_callback":
        for name, kind, attr in (("app.js", "script", "src"), ("style.css", "link", "href")):
            url = page.evaluate(
                f"() => [...document.querySelectorAll('{kind}[{attr}]')].map(e => e.{attr})"
                f".find(u => u.split('?')[0].endsWith('/{name}'))"
            )
            body = page.request.get(url).body() if url else b""
            result[f"live_{name}_sha256_16"] = hashlib.sha256(body).hexdigest()[:16]
        page.get_by_role("link", name="Overview", exact=True).click()
        page.locator(".map-marker").first.wait_for(state="attached", timeout=60000)
        for w, h in ((1280, 900), (390, 568), (320, 568)):
            page.set_viewport_size({"width": w, "height": h})
            page.wait_for_timeout(500)
            state = {"markers": page.locator(".map-marker").count()}
            if state["markers"]:
                page.locator(".map-marker").first.focus()
                page.locator(".map-marker").first.press("Enter")
                page.wait_for_timeout(500)
                state["card_visible"] = page.locator(".map-home-card").is_visible()
                state["card_position"] = page.evaluate(
                    "() => getComputedStyle(document.querySelector('.map-home-card')).position"
                )
                state["uncovered"] = page.evaluate(UNCOVERED_JS)
                state["overflow"] = page.evaluate(
                    "() => document.documentElement.scrollWidth > window.innerWidth"
                )
                page.screenshot(path=str(out / f"live-{w}x{h}.png"))
                page.keyboard.press("Escape")
            result[f"{w}x{h}"] = state
    browser.close()
(out / "live-probe.json").write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps(result))
