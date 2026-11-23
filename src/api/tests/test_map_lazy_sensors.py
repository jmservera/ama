"""Execute the shipped map with delayed synthetic summary reads and a small Leaflet double."""

from __future__ import annotations

import os
import unittest
from typing import Any

from test_app_wide_ux import WEB, run, shipped, shipped_line

APP = (WEB / "app.js").read_text()
MAP_SOURCE = APP.split("const MAP_SIGNALS = ", 1)[1].split("\nasync function coordinatorView()", 1)[
    0
]

SUPPORT = r"""
if (document.body.listeners) {
  const prototype = document.body.constructor.prototype;
  const append = prototype.append;
  const remove = prototype.remove;
  prototype.append = function(...kids) {
    append.call(this, ...kids.flat().map(kid =>
      typeof kid === "string" ? document.createTextNode(kid) : kid));
  };
  prototype.remove = function() {if (this.parentElement) remove.call(this);};
}
let disposeMapPanel = null;
const routeController = new AbortController();
const me = {map: null}, ovState = {}, listState = {};
const AsyncAction = {feedback: () => ({finish() {}})};
const Fields = {checkRow: ({control, label}) => ({
  block: h("label", {}, control, label)
})};
const svg = (tag, attrs, ...kids) => h(tag, attrs, ...kids);
const MAP_AUTO_RETRY_DELAYS = [];
const calls = [], pending = [], visibleMarkers = [];
const latest = {state: "fresh", label: "Recent reading", alert: false,
  temperature_c: 19.2, humidity_pct: 52, source: "Synthetic", age_seconds: 120};
const points = ["ZF-A", "ZF-B"].map((id, i) => ({
  id, name: "Synthetic home " + i, lat: 54.9, lon: -1.6, kind: "normal",
  stage: "Survey", sensor: {state: "not-loaded"}
}));
async function api(url, body, signal) {
  calls.push(url);
  if (url.startsWith("/api/map?")) {
    const bulk = url.includes("sensors=1");
    const items = points.map((point, i) => ({...point,
      sensor: bulk ? {...latest, state: i ? "fresh" : "stale", alert: !i}
        : {state: "not-loaded"}}));
    return {mode: "points", total: items.length, shown: items.length, items};
  }
  return new Promise((resolve, reject) => pending.push({url, signal, resolve, reject}));
}
const map = {
  setView() {return this;}, getZoom() {return 14;},
  getBounds() {return {getSouth: () => 50, getWest: () => -5,
    getNorth: () => 60, getEast: () => 2};},
  on() {}, invalidateSize() {}, remove() {}
};
const L = {
  map: () => map,
  layerGroup: () => ({addTo() {return this;},
    clearLayers() {visibleMarkers.length = 0;}}),
  divIcon: value => value,
  marker: () => {
    const node = document.createElement("button"), listeners = {};
    return {on(name, action) {listeners[name] = action; return this;},
      addTo() {visibleMarkers.push(this); return this;},
      getElement: () => node,
      fire(name, event) {listeners[name](event);}
    };
  }
};
const tick = () => new Promise(resolve => setTimeout(resolve, 0));
const findClass = name => document.body.querySelectorAll("." + name)[0];
const text = () => findClass("map-sensor-box").textContent;
async function setup() {
  const panel = mapPanel();
  document.body.append(panel.box);
  await panel.draw(false);
  return panel;
}
"""

SOURCE = (
    shipped("h")
    + shipped("ownedNotice")
    + 'const SUPPORT_OWNER = "Owner: application support.";\n'
    + shipped_line("qs")
    + SUPPORT
    + "const MAP_SIGNALS = "
    + MAP_SOURCE
)


def execute(body: str) -> Any:
    result = run(body, SOURCE)
    if os.environ.get("ZF_BROWSER_TESTS") == "1":
        from playwright.sync_api import sync_playwright

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.set_content("<!doctype html><html lang='en'><body></body></html>")
                actual = page.evaluate(f"async () => {{ {SOURCE}\n{body} }}")
                if actual != result:
                    raise AssertionError(f"Browser result differs: {actual!r} != {result!r}")
            finally:
                browser.close()
    return result


class LazyMapSensors(unittest.TestCase):
    def test_initial_map_and_pan_do_not_request_sensor_details(self) -> None:
        result = execute("""
          const panel = await setup();
          await panel.draw(false);
          return {calls, hidden: findClass("map-home-card").hidden};
        """)
        self.assertEqual(len(result["calls"]), 2)
        self.assertTrue(all(url.startswith("/api/map?") for url in result["calls"]))
        self.assertTrue(all("sensors=1" not in url for url in result["calls"]))
        self.assertTrue(result["hidden"])

    def test_selection_loads_one_home_and_redraw_does_not_refetch(self) -> None:
        result = execute("""
          const panel = await setup();
          visibleMarkers[0].fire("click");
          const loading = text();
          await panel.draw(false);
          const count = pending.length;
          pending[0].resolve(latest);
          await tick();
          return {count, url: pending[0].url, loading, text: text(),
            busy: findClass("map-sensor-box").getAttribute("aria-busy")};
        """)
        self.assertEqual(result["count"], 1)
        self.assertEqual(result["url"], "/api/cases/ZF-A/sensor-summary")
        self.assertIn("Loading sensor readings", result["loading"])
        self.assertIn("19.2", result["text"])
        self.assertIn("52%", result["text"])
        self.assertIsNone(result["busy"])

    def test_keyboard_selection_ignores_late_results_for_previous_home(self) -> None:
        result = execute("""
          await setup();
          visibleMarkers[0].fire("click");
          visibleMarkers[1].fire("keydown", {
            originalEvent: {key: "Enter", preventDefault() {}}
          });
          pending[1].resolve({...latest, temperature_c: 21.7});
          await tick();
          pending[0].resolve(latest);
          await tick();
          return {aborted: pending[0].signal.aborted, text: text(),
            urls: pending.map(read => read.url)};
        """)
        self.assertTrue(result["aborted"])
        self.assertEqual(
            result["urls"], ["/api/cases/ZF-A/sensor-summary", "/api/cases/ZF-B/sensor-summary"]
        )
        self.assertIn("21.7", result["text"])
        self.assertNotIn("19.2", result["text"])

    def test_close_reopen_same_home_and_route_cleanup_guard_pending_reads(self) -> None:
        result = execute("""
          await setup();
          visibleMarkers[0].fire("click");
          findClass("map-home-close").listeners
            ? await findClass("map-home-close").fire("click")
            : findClass("map-home-close").click();
          const closed = findClass("map-home-card").hidden;
          visibleMarkers[0].fire("click");
          pending[0].resolve(latest);
          await tick();
          const stillLoading = text().includes("Loading sensor readings");
          const sensorBox = findClass("map-sensor-box");
          const beforeDispose = text();
          routeController.abort();
          pending[1].resolve(latest);
          await tick();
          return {closed, stillLoading, firstAborted: pending[0].signal.aborted,
            secondAborted: pending[1].signal.aborted,
            unchanged: sensorBox.textContent === beforeDispose};
        """)
        self.assertTrue(all(result.values()), result)

    def test_unavailable_and_malformed_reads_show_retry_and_clear_old_values(self) -> None:
        result = execute("""
          await setup();
          visibleMarkers[0].fire("click");
          pending[0].resolve(latest);
          await tick();
          visibleMarkers[1].fire("click");
          const loading = text();
          pending[1].reject(new Error("network unavailable"));
          await tick();
          const failure = text();
          visibleMarkers[1].fire("click");
          pending[2].resolve({});
          await tick();
          return {loading, failure, malformed: text()};
        """)
        self.assertNotIn("19.2", result["loading"])
        for key in ("failure", "malformed"):
            self.assertIn("unavailable", result[key])
            self.assertIn("Owner: application support.", result[key])
            self.assertIn("retry", result[key])
            self.assertNotIn("19.2", result[key])

    def test_bulk_filter_is_explicit_and_unchecking_restores_lazy_reads(self) -> None:
        result = execute("""
          await setup();
          visibleMarkers[0].fire("click");
          const input = document.body.querySelector("input");
          async function toggle(checked) {
            input.checked = checked;
            if (input.fire) await input.fire("change");
            else input.dispatchEvent(new Event("change"));
            await tick();
          }
          await toggle(true);
          const filtered = visibleMarkers.length;
          const cancelled = pending[0].signal.aborted;
          pending[0].resolve({...latest, temperature_c: 26.4});
          await tick();
          const bulkText = text();
          const bulkDetails = pending.length;
          await toggle(false);
          visibleMarkers[1].fire("click");
          return {calls, filtered, cancelled, bulkText, bulkDetails,
            details: pending.map(read => read.url)};
        """)
        self.assertEqual(result["filtered"], 1)
        self.assertTrue(result["cancelled"])
        self.assertEqual(result["bulkDetails"], 1)
        self.assertIn("out of date", result["bulkText"])
        self.assertNotIn("26.4", result["bulkText"])
        maps = [url for url in result["calls"] if url.startswith("/api/map?")]
        self.assertNotIn("sensors=1", maps[0])
        self.assertIn("sensors=1", maps[1])
        self.assertNotIn("sensors=1", maps[2])
        self.assertEqual(
            result["details"], ["/api/cases/ZF-A/sensor-summary", "/api/cases/ZF-B/sensor-summary"]
        )


if __name__ == "__main__":
    unittest.main()
