"""Probe the resident Sensors chart: screenshot plus text size and marker metrics.

Usage: probe_chart.py BASE_URL OUT_PNG [signin]  (signin reads ~/.ama-resident-test-user at runtime)
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright



def measure(page, out):
    page.get_by_text("Sensors", exact=True).first.click()
    page.wait_for_selector(".sensor-chart svg", timeout=30000)
    page.wait_for_timeout(1000)
    chart = page.locator(".sensor-chart").first
    chart.scroll_into_view_if_needed()
    chart.screenshot(path=out)
    return chart.evaluate(
        """(f) => {
        const s = f.querySelector('svg'); const k = s.getBoundingClientRect().width / s.viewBox.baseVal.width;
        const t = [...s.querySelectorAll('text')].map(n => ({text: n.textContent, px: parseFloat(getComputedStyle(n).fontSize) * k, box: n.getBoundingClientRect().toJSON()}));
        const boxes = t.map(x => x.box);
        let overlap = 0;
        for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
          const a = boxes[i], c = boxes[j];
          if (a.left < c.right && c.left < a.right && a.top < c.bottom && c.top < a.bottom) overlap++;
        }
        const pts = [...s.querySelectorAll('circle.sensor-point')].map(c => c.getBoundingClientRect());
        let touching = 0;
        for (let i = 1; i < pts.length; i++) if (pts[i].left < pts[i-1].right) touching++;
        return {scale: k, body_px: parseFloat(getComputedStyle(f.querySelector('figcaption')).fontSize),
          text: t.map(x => [x.text, Math.round(x.px * 10) / 10]), text_overlaps: overlap,
          circles: pts.length, touching_circles: touching};
      }"""
    )


if __name__ == "__main__":
    base, out = sys.argv[1], sys.argv[2]
    signin = len(sys.argv) > 3
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.goto(base + "/", wait_until="networkidle", timeout=90000)
        if signin:
            email, password = (Path.home() / ".ama-resident-test-user").read_text().splitlines()[:2]
            page.fill("input[type=email], input[name=email], #email", email)
            page.fill("input[type=password]", password)
            page.keyboard.press("Enter")
        page.wait_for_selector("#account:not([hidden])", timeout=90000)
        page.wait_for_timeout(3000)
        print(json.dumps(measure(page, out)))
        b.close()
