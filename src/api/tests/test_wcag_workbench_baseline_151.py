"""WCAG 2.2 workbench baseline (#151) and map/chart/table accessible equivalents (#119)."""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
WEB = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web"
DOC_PATH = ROOT / "docs" / "reference" / "research" / "ux" / "wcag-conformance-baseline.md"

MOCK_DOM_PRELUDE = r"""
function makeNode(tag, attrs = {}, ...rawKids) {
  const attributes = new Map();
  const node = {
    tag,
    value: "",
    inert: false,
    disabled: false,
    open: false,
    isConnected: true,
    children: [],
    classList: {
      _set: new Set(),
      add(...names) { names.forEach(n => this._set.add(n)); syncClass(); },
      remove(...names) { names.forEach(n => this._set.delete(n)); syncClass(); },
      contains(name) { return this._set.has(name); },
    },
    setAttribute(k, v) {
      const str = String(v);
      attributes.set(k, str);
      if (k === "class") {
        node.classList._set = new Set(str.split(/\s+/).filter(Boolean));
      }
      if (k === "value") node.value = str;
    },
    getAttribute(k) {
      return attributes.has(k) ? attributes.get(k) : null;
    },
    hasAttribute(k) {
      return attributes.has(k);
    },
    removeAttribute(k) {
      attributes.delete(k);
      if (k === "class") node.classList._set.clear();
    },
    append(...items) {
      for (const item of items.flat()) {
        if (item === false || item === null || item === undefined) continue;
        node.children.push(typeof item === "object" ? item : String(item));
      }
    },
    prepend(...items) {
      const valid = items.flat().filter(x => x !== false && x !== null && x !== undefined)
        .map(x => typeof x === "object" ? x : String(x));
      node.children.unshift(...valid);
    },
    insertBefore(item, ref) {
      const idx = node.children.indexOf(ref);
      if (idx >= 0) node.children.splice(idx, 0, item);
      else node.children.push(item);
    },
    replaceChildren(...items) {
      node.children = [];
      node.append(...items);
    },
    after(sibling) {
      node._after = node._after || [];
      node._after.push(sibling);
    },
    remove() {},
    focus() {},
    addEventListener() {},
    removeEventListener() {},
    contains() { return false; },
    showModal() { node.open = true; },
    close() { node.open = false; },
    querySelector(sel) {
      return node.querySelectorAll(sel)[0] || null;
    },
    querySelectorAll(sel) {
      const found = [];
      function matches(el) {
        if (!el || typeof el !== "object") return false;
        if (sel.startsWith(".")) return el.classList.contains(sel.slice(1));
        if (sel.startsWith("#")) return el.getAttribute("id") === sel.slice(1);
        const attrMatch = sel.match(/^\[([\w-]+)(?:=([^\]]+))?\]$/);
        if (attrMatch) {
          if (!el.hasAttribute(attrMatch[1])) return false;
          const expected = attrMatch[2]?.replace(/^"|"$/g, "");
          return expected === undefined || el.getAttribute(attrMatch[1]) === expected;
        }
        return el.tag === sel;
      }
      function walk(cur) {
        if (!cur || typeof cur !== "object") return;
        for (const child of cur.children || []) {
          if (matches(child)) found.push(child);
          walk(child);
        }
      }
      walk(node);
      return found;
    },
    get textContent() {
      return node.children.map(c => typeof c === "string" ? c : c.textContent).join("");
    },
    set textContent(val) {
      node.children = val === "" || val === null || val === undefined ? [] : [String(val)];
    },
    toJSON() {
      return {
        tag: node.tag,
        attrs: Object.fromEntries(attributes.entries()),
        hidden: node.hidden,
        children: node.children,
      };
    },
  };
  function syncClass() {
    attributes.set("class", [...node.classList._set].join(" "));
  }
  Object.defineProperty(node, "hidden", {
    get() { return attributes.has("hidden"); },
    set(flag) {
      if (flag) attributes.set("hidden", "");
      else attributes.delete("hidden");
    },
    enumerable: true,
  });
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === false || v === null || v === undefined) continue;
    if (k.startsWith("on") && typeof v === "function") {
      node[k] = v;
    } else if (k === "hidden" || k === "selected" || k === "disabled" || k === "open") {
      if (v) node.setAttribute(k, "");
    } else {
      node.setAttribute(k, v);
    }
  }
  node.append(...rawKids);
  return node;
}
"""


def run_node_json(script: str) -> Any:
    result = subprocess.run(
        ["node", "-e", MOCK_DOM_PRELUDE + "\n" + script, str(WEB)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def extract_function(source: str, signature: str, next_anchor: str) -> str:
    start = source.index(signature)
    end = source.index(next_anchor, start)
    return source[start:end]


def resolve_token(css: str, name: str) -> str:
    values = dict(re.findall(r"(--[\w-]+):([^;}\n]+)", css))
    value = values["--" + name]
    while value.startswith("var("):
        value = values[value[4:-1]]
    return "#" + "".join(c * 2 for c in value[1:]) if len(value) == 4 else value


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    def luminance(colour: str) -> float:
        chans = [int(colour[i : i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chans]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    hi, lo = sorted((luminance(hex_a), luminance(hex_b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


class WcagWorkbenchBaseline151(unittest.TestCase):
    def test_bars_svg_and_table_disclosure_parity_and_empty_state(self) -> None:
        app_js = (WEB / "app.js").read_text()
        bars_fn = extract_function(app_js, "function bars(title, data, link)", "const OV_TILES =")
        payload = run_node_json(
            "const h = makeNode, svg = makeNode;\n"
            + bars_fn
            + r"""
const populated = bars("Cases by stage", [
  { label: "Assessment", n: 12 },
  { label: "Design", n: 5 },
]);
const empty = bars("Cases by wave", []);
console.log(JSON.stringify({
  summaryText: populated.querySelector("summary").textContent,
  srOnlyTitle: populated.querySelector(".sr-only").textContent,
  svgRole: populated.querySelector("svg").getAttribute("role"),
  svgLabel: populated.querySelector("svg").getAttribute("aria-label"),
  scrollRole: populated.querySelector(".table-scroll").getAttribute("role"),
  scrollTabindex: populated.querySelector(".table-scroll").getAttribute("tabindex"),
  scrollLabel: populated.querySelector(".table-scroll").getAttribute("aria-label"),
  caption: populated.querySelector("caption").textContent,
  colHeaders: populated
    .querySelector("thead")
    .querySelectorAll("th")
    .map(th => [th.getAttribute("scope"), th.textContent]),
  rows: populated.querySelector("tbody").querySelectorAll("tr").map(tr => ({
    rowHeader: [
      tr.children[0].tag,
      tr.children[0].getAttribute("scope"),
      tr.children[0].textContent,
    ],
    value: [tr.children[1].tag, tr.children[1].textContent],
  })),
  emptyCells: empty
    .querySelector("tbody")
    .querySelectorAll("td")
    .map(td => [td.getAttribute("colspan"), td.textContent]),
}));
"""
        )
        self.assertEqual(payload["svgRole"], "img")
        self.assertEqual(payload["svgLabel"], "Cases by stage")
        self.assertEqual(payload["summaryText"], "Show this chart as a table: Cases by stage")
        self.assertEqual(payload["srOnlyTitle"], ": Cases by stage")
        self.assertEqual(payload["scrollRole"], "region")
        self.assertEqual(payload["scrollTabindex"], "0")
        self.assertEqual(payload["scrollLabel"], "Cases by stage table")
        self.assertEqual(payload["caption"], "Cases by stage")
        self.assertEqual(payload["colHeaders"], [["col", "Group"], ["col", "Cases"]])
        self.assertEqual(
            payload["rows"],
            [
                {"rowHeader": ["th", "row", "Assessment"], "value": ["td", "12"]},
                {"rowHeader": ["th", "row", "Design"], "value": ["td", "5"]},
            ],
        )
        self.assertEqual(payload["emptyCells"], [["2", "No cases recorded."]])

    def test_map_panel_list_equivalent_clusters_points_and_empty_sync(self) -> None:
        app_js = (WEB / "app.js").read_text()
        map_slice = extract_function(app_js, "const OV_TILES =", "async function coordinatorView(")
        payload = run_node_json(
            r"""
const h = makeNode, svg = makeNode;
let disposeMapPanel = null;
const routeController = new AbortController();
const listState = {};
const me = { map: null };
const qs = (o) => new URLSearchParams(o).toString();
const document = {
  body: makeNode("body"),
  activeElement: null,
  getElementById: () => makeNode("div"),
};
const AsyncAction = { feedback: () => ({ finish() {} }) };
let nextMapResponse = { mode: "clusters", total: 0, mapped: 0, unmapped: 0, items: [] };
const api = async () => nextMapResponse;
const L = {
  map: () => ({
    setView() { return this; },
    on() {},
    getBounds: () => ({
      getSouth: () => 53.0,
      getWest: () => -2.0,
      getNorth: () => 54.0,
      getEast: () => -1.0,
    }),
    getZoom: () => 10,
    fitBounds() {},
    invalidateSize() {},
    remove() {},
  }),
  tileLayer: () => ({ on() { return this; }, addTo() { return this; } }),
  layerGroup: () => ({ addTo() { return this; }, clearLayers() {} }),
  divIcon: (opts) => opts,
  marker: () => ({
    on() { return this; },
    addTo() { return this; },
    getElement: () => makeNode("button"),
  }),
};
"""
            + (WEB / "fields.js").read_text()
            + map_slice
            + r"""
(async () => {
  const mp = mapPanel();
  const emptyNote = mp.box.querySelector("[data-maplist-empty]");
  const initialHidden = [emptyNote.hidden, emptyNote.hasAttribute("hidden")];

  nextMapResponse = {
    mode: "clusters", total: 5, mapped: 5, unmapped: 0,
    items: [{ lat: 53.5, lon: -1.5, count: 5, hazards: 2 }],
  };
  await mp.draw(false);
  const clusterSnap = {
    emptyHidden: [emptyNote.hidden, emptyNote.hasAttribute("hidden")],
    items: mp.box.querySelector(".maplist").querySelectorAll("li").map(li => ({
      text: li.textContent,
      ariaLabel: li.children[0].getAttribute("aria-label"),
    })),
  };

  nextMapResponse = {
    mode: "points", total: 2, mapped: 2, unmapped: 0,
    items: [
      { id: "ZF-1", name: "1 Oak Lane", kind: "hazard", lat: 53.5, lon: -1.5, stage: "Works" },
      { id: "ZF-2", name: "2 Oak Lane", kind: "long", lat: 53.6, lon: -1.6, stage: "Design" },
    ],
  };
  await mp.draw(false);
  const pointsSnap = {
    emptyHidden: [emptyNote.hidden, emptyNote.hasAttribute("hidden")],
    items: mp.box.querySelector(".maplist").querySelectorAll("li").map(li => ({
      href: li.children[0].getAttribute("href"),
      text: li.textContent,
    })),
  };

  nextMapResponse = { mode: "points", total: 3, mapped: 0, unmapped: 3, items: [] };
  await mp.draw(false);
  const emptySnap = {
    emptyHidden: [emptyNote.hidden, emptyNote.hasAttribute("hidden")],
    emptyText: emptyNote.textContent,
    items: mp.box.querySelector(".maplist").querySelectorAll("li").map(li => li.textContent),
  };

  console.log(JSON.stringify({
    regionRole: mp.box.querySelector("#leaflet").getAttribute("role"),
    regionTabindex: mp.box.querySelector("#leaflet").getAttribute("tabindex"),
    initialHidden,
    clusterSnap,
    pointsSnap,
    emptySnap,
  }));
})();
"""
        )
        self.assertEqual(payload["regionRole"], "region")
        self.assertEqual(payload["regionTabindex"], "0")
        self.assertEqual(payload["initialHidden"], [True, True])
        self.assertEqual(payload["clusterSnap"]["emptyHidden"], [True, True])
        self.assertEqual(
            payload["clusterSnap"]["items"],
            [
                {
                    "text": "5 homes, 2 with a safety issue open",
                    "ariaLabel": "5 homes, 2 with a safety issue open. Zoom in to this area",
                }
            ],
        )
        self.assertEqual(payload["pointsSnap"]["emptyHidden"], [True, True])
        self.assertEqual(
            payload["pointsSnap"]["items"],
            [
                {"href": "#/case/ZF-1", "text": "1 Oak Lane, Safety issue open"},
                {"href": "#/case/ZF-2", "text": "2 Oak Lane, Waiting 60+ days"},
            ],
        )
        self.assertEqual(payload["emptySnap"]["emptyHidden"], [False, False])
        self.assertEqual(payload["emptySnap"]["items"], [])
        self.assertIn("No mapped homes in this view", payload["emptySnap"]["emptyText"])

    def test_progress_views_meter_labels_and_table_disclosures(self) -> None:
        payload = run_node_json(
            r"""
const fs = require("node:fs");
const vm = require("node:vm");
const progressSrc = fs.readFileSync(process.argv[1] + "/progress.js", "utf8");
let currentRoot = null;
const ctx = vm.createContext({
  h: makeNode,
  URLSearchParams,
  Intl,
  navigator: { language: "en-GB" },
  location: { hash: "#/progress" },
  history: { replaceState() {} },
  displayedHash: "#/progress",
  routeController: new AbortController(),
  me: { user: { role: "Retrofit Programme Manager" } },
  isManager: () => true,
  route: () => {},
  api: async (url) => {
    if (url.startsWith("/api/progress")) {
      return {
        start: "2026-10-01",
        end: "2026-10-07",
        as_of: "2026-10-07",
        time_to_close: { median_days: 14, p90_days: 30, samples: 4 },
        current: {
          open: 10, stalled: 2, overdue: 1,
          journey: [{ label: "Assessment", count: 6 }],
          teams: [{ label: "Retrofit Coordinator", count: 4 }],
        },
        coverage: {
          synthetic_cases: 10,
          excluded_unmarked: 0,
          known_lifecycle: 10,
          unknown_lifecycle: 0,
        },
        daily: [{ date: "2026-10-01", opened: 3, closed: 1, reopened: 2, backlog: 8 }],
        weekly: [{ date: "2026-09-28", opened: 3, closed: 1, reopened: 2 }],
        ai: {
          basis: "Synthetic basis.",
          eligible_records: 0,
          unknown_review_date: 0,
          unreviewed_or_unavailable: 0,
          rules_or_templates: 0,
          outcomes: [],
        },
      };
    }
    return {
      total: 1, page: 1, pages: 1, limit: 25, unknown_closure_dates: 0,
      facets: { statuses: ["Completed"], teams: ["Retrofit Coordinator"] },
      items: [{
        id: "ZF-10", resident: "A Resident", address: "10 High St",
        town: "Leeds", postcode: "LS1 1AA", status: "Completed",
        closed_on: "2026-10-05", team: "Retrofit Coordinator", hazard: false,
      }],
    };
  },
  show: (...nodes) => {
    currentRoot = makeNode("main", {}, ...nodes);
  },
});
vm.runInContext(progressSrc, ctx);
(async () => {
  await vm.runInContext("ProgressViews.dashboard()", ctx);
  const dashRoot = currentRoot;
  await vm.runInContext("ProgressViews.closed()", ctx);
  const closedRoot = currentRoot;
  const charts = dashRoot.querySelectorAll(".progress-chart").map(sec => ({
    title: sec.querySelector("h2").textContent,
    barsHidden: sec.querySelector(".progress-bars").getAttribute("aria-hidden"),
    meters: sec
      .querySelectorAll("meter")
      .map(m => [m.getAttribute("tabindex"), m.getAttribute("aria-label")]),
    summary: sec.querySelector("summary").textContent,
    scrollRole: sec.querySelector(".table-scroll").getAttribute("role"),
    caption: sec.querySelector("caption").textContent,
    rowHeaders: sec
      .querySelector("tbody")
      .querySelectorAll("th")
      .map(th => [th.getAttribute("scope"), th.textContent]),
    emptyCell: sec.querySelector("tbody").querySelectorAll("td").map(td => td.textContent),
  }));
  const closedScroll = closedRoot.querySelector(".table-scroll");
  console.log(JSON.stringify({
    charts,
    closedRegion: [closedScroll.getAttribute("role"), closedScroll.getAttribute("aria-label")],
    closedCaption: closedScroll.querySelector("caption").textContent,
    closedRowScope: closedScroll.querySelector("tbody").querySelector("th").getAttribute("scope"),
  }));
})();
"""
        )
        self.assertEqual(len(payload["charts"]), 6)
        daily = payload["charts"][0]
        self.assertEqual(daily["title"], "Cases opened and closed per day")
        self.assertEqual(daily["barsHidden"], "true")
        self.assertEqual(
            daily["meters"],
            [
                ["-1", "1 Oct 2026, Opened: 3 (highest shown: 3)"],
                ["-1", "1 Oct 2026, Closed: 1 (highest shown: 3)"],
                ["-1", "1 Oct 2026, Reopened: 2 (highest shown: 3)"],
            ],
        )
        self.assertEqual(daily["summary"], "Show cases opened and closed per day as a table")
        self.assertEqual(daily["scrollRole"], "region")
        self.assertEqual(daily["caption"], "Cases opened and closed per day")
        self.assertEqual(daily["rowHeaders"], [["row", "1 Oct 2026"]])
        empty_ai = payload["charts"][5]
        self.assertEqual(empty_ai["title"], "AI briefing review outcomes")
        self.assertEqual(empty_ai["meters"], [])
        self.assertEqual(empty_ai["emptyCell"], ["No recorded data for this view."])
        self.assertEqual(payload["closedRegion"], ["region", "Matching closed cases table"])
        self.assertEqual(payload["closedCaption"], "Matching closed cases")
        self.assertEqual(payload["closedRowScope"], "row")

    def test_fifteen_table_builders_have_scroll_regions_captions_and_row_headers(
        self,
    ) -> None:
        table_sites: list[str] = []
        for path in sorted(WEB.glob("*.js")):
            text = path.read_text()
            self.assertNotRegex(text, r'h\("table",\s*\{\s*"aria-label"', path.name)
            for match in re.finditer(r'h\("table", \{\},', text):
                start = max(0, match.start() - 180)
                prefix = text[start : match.start()]
                after = text[match.start() : match.start() + 360]
                site = f"{path.name}:{text[: match.start()].count(chr(10)) + 1}"
                self.assertIn('class: "table-scroll"', prefix, site)
                self.assertIn('role: "region"', prefix, site)
                self.assertIn("tabindex", prefix, site)
                self.assertIn('"aria-label":', prefix, site)
                self.assertIn('h("caption"', after, site)
                self.assertIn('scope: "col"', after, site)
                table_sites.append(site)
            if 'h("table", {},' in text:
                self.assertIn('scope: "row"', text, path.name)
        self.assertEqual(len(table_sites), 18, table_sites)

        ops_js = (WEB / "ops.js").read_text()
        sensor_fn = extract_function(
            ops_js, "function sensorTable(", "function sensorDraftSection("
        )
        role_js = (WEB / "role-screens.js").read_text()
        screen_fn = extract_function(
            role_js, "function screenTable(", "// Non-colour state meaning:"
        )
        runtime = run_node_json(
            "const h = makeNode;\nconst screenNodeValue = (v) => String(v ?? 'Unknown');\n"
            + sensor_fn
            + "\n"
            + screen_fn
            + r"""
const sensor = sensorTable("Retained readings", [{
  reading_id: "R-1", sensor_id: "S-1", observed_at: "2026-10-01T00:00:00Z",
  temperature_c: 19.2, humidity_pct: 58, provenance_class: "synthetic",
}], "None", { synthetic: "Synthetic fixture" });
const specialist = screenTable("Ready homes", ["Home", "Stage"], [["ZF-1", "Design"]]);
console.log(JSON.stringify({
  sensorScroll: [
    sensor.querySelector(".table-scroll").getAttribute("role"),
    sensor.querySelector("caption").textContent,
    sensor.querySelector("tbody").querySelector("th").getAttribute("scope"),
  ],
  specialistScroll: [
    specialist.querySelector(".table-scroll").getAttribute("role"),
    specialist.querySelector("caption").textContent,
    specialist.querySelector("tbody").querySelector("th").getAttribute("scope"),
  ],
}));
"""
        )
        self.assertEqual(runtime["sensorScroll"], ["region", "Retained readings", "row"])
        self.assertEqual(runtime["specialistScroll"], ["region", "Ready homes", "row"])

    def test_eight_wcag_dimensions_enforced_in_web_assets(self) -> None:
        css = (WEB / "style.css").read_text()
        chat_css = (WEB / "chat-widget.css").read_text()
        case_ws = (WEB / "case-workspace.js").read_text()
        app_js = (WEB / "app.js").read_text()

        # 1. Keyboard + 2. Focus order/visibility
        self.assertIn('class="skip-link" href="#app"', (WEB / "index.html").read_text())
        self.assertIn('class="skip-link" href="#welcome-main"', (WEB / "welcome.html").read_text())
        for key in ("ArrowRight", "ArrowLeft", "Home", "End"):
            self.assertIn(key, case_ws)
        self.assertNotIn("color:#555", css)
        self.assertIn(".focus dt{color:var(--muted)}", css)

        # 5. Contrast (including caution banner foreground on caution-bg)
        self.assertGreaterEqual(
            contrast_ratio(resolve_token(css, "ink"), resolve_token(css, "caution-bg")),
            4.5,
        )

        # 6. Reflow and zoom
        for bp in ("1199px", "1100px", "900px", "899px", "700px", "600px"):
            self.assertIn(f"@media(max-width:{bp})", css)
        self.assertNotRegex(css, r"min-width:\s*(?:3[6-9]\d|[4-9]\d\d|\d{4})px")

        # 7. Target size (24px minimum, >=40px/44px primary & map/chat controls)
        self.assertIn("details>summary{cursor:pointer;min-height:1.5rem", css)
        self.assertIn(
            "input[type=checkbox],input[type=radio]{min-width:1.5rem;min-height:1.5rem",
            css,
        )
        self.assertIn(
            ".leafmap .leaflet-bar a,.leafmap.leaflet-touch .leaflet-bar a{"
            "width:2.5rem;height:2.5rem;min-width:2.5rem;min-height:2.5rem",
            css,
        )
        self.assertIn(".chat-widget summary{cursor:pointer;min-height:2rem", chat_css)
        self.assertIn("min-width:3.5rem;min-height:3.5rem", chat_css)

        # 8. Error identification
        self.assertIn('class: "field-error"', app_js)
        self.assertIn('setAttribute("aria-invalid", "true")', app_js)
        self.assertIn('setAttribute("aria-describedby"', app_js)

    def test_baseline_doc_records_all_eight_dimensions_and_equivalents_inventory(self) -> None:
        doc = DOC_PATH.read_text()
        for heading in (
            "### 1. Keyboard operation",
            "### 2. Focus order and visibility",
            "### 3. Name, role, value, and non-colour cues",
            "### 4. Status messages",
            "### 5. Contrast",
            "### 6. Reflow and zoom",
            "### 7. Target size",
            "### 8. Error identification",
            "## Accessible equivalents for maps, charts, and tables",
        ):
            self.assertIn(heading, doc)
        for item in (
            "Map of open cases",
            "ProgressViews",
            "sensorTable",
            "screenTable",
            "test_wcag_workbench_baseline_151.py",
            "pending owner confirmation",
            "we do not claim conformance",
            "#155",
        ):
            self.assertIn(item, doc)

    def test_counted_guard_measurement_section_matches_source(self) -> None:
        doc = DOC_PATH.read_text()
        section = doc.split("## Counted guard-suite measurement (2026-11-17, #151)")[1].split(
            "\n## "
        )[0]
        assets = [p for p in WEB.glob("*") if p.suffix in {".js", ".html", ".css"}]
        self.assertIn(f"| Served web assets | {len(assets)} ", section)
        self.assertEqual(len(assets), 24)
        invalid = sum(
            p.read_text().count('setAttribute("aria-invalid", "true")') for p in WEB.glob("*.js")
        )
        self.assertIn(f"| `aria-invalid` sites | {invalid} |", section)
        self.assertIn("we do not claim conformance", section)
        self.assertIn("`Not run`", section)


if __name__ == "__main__":
    unittest.main()
