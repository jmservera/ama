"""The resident sensor chart must render legibly in a real browser (issue 2253)."""

from __future__ import annotations

import functools
import http.server
import json
import threading
import unittest
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None  # type: ignore[assignment]

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/resident_demo/web"

MEASURE = """({history, points}) => {
  const metric = sensorMetrics[0];
  const figure = sensorChart(history, metric, {points});
  document.body.appendChild(figure);
  const svg = figure.querySelector('svg');
  const scale = svg.getBoundingClientRect().width / svg.viewBox.baseVal.width;
  const bodyPx = parseFloat(getComputedStyle(document.body).fontSize);
  const hit = (a, b) =>
    a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
  const texts = [...svg.querySelectorAll('text')];
  const boxes = texts.map(t => t.getBoundingClientRect());
  const textOverlaps = [];
  for (let i = 0; i < boxes.length; i++)
    for (let j = i + 1; j < boxes.length; j++)
      if (hit(boxes[i], boxes[j]))
        textOverlaps.push([texts[i].textContent, texts[j].textContent]);
  const circles = [...svg.querySelectorAll('circle.sensor-point')]
    .map(c => c.getBoundingClientRect());
  let circleTouches = 0;
  for (let i = 1; i < circles.length; i++) if (hit(circles[i - 1], circles[i])) circleTouches++;
  const circleOnText = circles.some(c => boxes.some(b => hit(c, b)));
  return {
    labels: texts.map(t => t.textContent),
    maxLabelRatio: Math.max(
      ...texts.map(t => parseFloat(getComputedStyle(t).fontSize) * scale)) / bodyPx,
    textOverlaps, circleCount: circles.length, circleTouches, circleOnText,
    squares: svg.querySelectorAll('rect.sensor-forecast-point').length,
    circleRadiusPx: circles[0].width / 2,
  };
}"""


def history(count: int, step_minutes: int) -> list[dict[str, object]]:
    from datetime import UTC, datetime, timedelta

    start = datetime(2026, 11, 22, tzinfo=UTC)
    return [
        {
            "observed_at": (start + timedelta(minutes=i * step_minutes)).isoformat(),
            "temperature_c": 6 + (i % 5) * 0.4,
            "temperature_status": "ok",
            "humidity_pct": 50,
            "humidity_status": "ok",
        }
        for i in range(count)
    ]


def forecast_points(hist: list[dict[str, object]]) -> list[dict[str, object]]:
    from datetime import datetime, timedelta

    last = datetime.fromisoformat(str(hist[-1]["observed_at"]))
    return [
        {
            "forecast_at": (last + timedelta(hours=h)).isoformat(),
            "temperature_c": 7,
            "humidity_pct": 50,
        }
        for h in (4, 8, 12, 16, 20, 24)
    ]


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        return


def harness() -> str:
    js = (WEB / "demo.js").read_text(encoding="utf-8")
    helpers = js[js.index("  function el(") : js.index("  function card(")]
    chart = js[js.index("  var sensorMetrics") : js.index("  function renderConsent(")]
    return (
        '<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
        '<link rel="stylesheet" href="/demo.css"></head><body><main></main>'
        f"<script>{helpers}{chart}</script></body></html>"
    )


@unittest.skipIf(sync_playwright is None, "playwright is not installed")
class ResidentSensorChartBrowserTests(unittest.TestCase):
    def test_chart_labels_body_sized_not_overlapping_with_circle_markers(self) -> None:
        page_html = harness()

        class Serving(Handler):
            def do_GET(self) -> None:
                if self.path == "/harness.html":
                    body = page_html.encode()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                super().do_GET()

        handler = functools.partial(Serving, directory=str(WEB))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch()
                except Exception as exc:  # pragma: no cover
                    self.skipTest(f"chromium is not available: {exc}")
                try:
                    cases = {"dense": (288, 5), "short": (6, 30)}
                    for name, (count, step) in cases.items():
                        with self.subTest(name):
                            hist = history(count, step)
                            page = browser.new_page(viewport={"width": 1440, "height": 900})
                            page.goto(f"http://127.0.0.1:{server.server_port}/harness.html")
                            result = page.evaluate(
                                MEASURE,
                                json.loads(
                                    json.dumps({"history": hist, "points": forecast_points(hist)})
                                ),
                            )
                            page.close()
                            self.assertIn("Latest stored", result["labels"])
                            # Tick and marker labels are close to body text, not the 26 px blow-up.
                            self.assertLessEqual(result["maxLabelRatio"], 1.25, result)
                            self.assertGreaterEqual(result["maxLabelRatio"], 0.75, result)
                            self.assertEqual(result["textOverlaps"], [], result)
                            self.assertGreaterEqual(result["circleCount"], 3, result)
                            self.assertEqual(result["circleTouches"], 0, result)
                            self.assertFalse(result["circleOnText"], result)
                            self.assertEqual(result["squares"], 6, result)
                            self.assertGreaterEqual(result["circleRadiusPx"], 2.5, result)
                finally:
                    browser.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
