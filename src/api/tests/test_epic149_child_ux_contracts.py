"""Epic #149 child UX surfaces are wired and intact; automated wiring only, never human sign-off."""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
API = ROOT / "src" / "api" / "src" / "zava_forward" / "api"
UX_DOCS = ROOT / "docs" / "reference" / "research" / "ux"
STYLESHEETS: dict[str, Path] = {
    "staff": API / "web" / "style.css",
    "chat": API / "web" / "chat-widget.css",
    "resident-demo": API / "resident_demo" / "web" / "demo.css",
    "resident-preview": API / "resident_preview" / "web" / "resident.css",
}
ROOT_TOKEN_SHEETS = ("staff", "resident-demo", "resident-preview")
TOKEN_GROUPS: dict[str, str] = {
    "colour": "--brand",
    "type": "--font",
    "spacing": "--sp-1",
    "focus": "--focus",
    "motion": "--motion",
}
NON_COLOUR_CUES: tuple[str, ...] = (
    ".flag.danger:before",
    ".status-line.danger:before",
    ".status-line.ok:before",
    ".blocked .blocked-title:before",
)
RESIDENT_COPY_BANNED = re.compile(r"\b(gates?|provenance|traces?|snapshots?|envelopes?)\b", re.I)
PENDING_HUMAN_EVIDENCE: dict[str, str] = {"#155": "assistive technology", "#215": "comprehension"}


def read(path: Path) -> str:
    return path.read_text()


def root_block(css: str) -> str:
    match = re.search(r":root\{(.*?)\n\}", css, re.S)
    return match.group(1) if match else ""


class DesignSystemTokens(unittest.TestCase):
    def test_every_child_surface_defines_and_uses_tokens(self) -> None:
        for name in ROOT_TOKEN_SHEETS:
            css: str = read(STYLESHEETS[name])
            block: str = root_block(css) or css
            for group, token in TOKEN_GROUPS.items():
                if name != "staff" and group in ("type", "spacing"):
                    continue
                self.assertIn(token + ":", block, f"{name} {group}")
                self.assertIn(f"var({token})", css, f"{name} {group}")

    def test_staff_tokens_are_documented(self) -> None:
        doc: str = read(UX_DOCS / "design-system.md")
        block: str = root_block(read(STYLESHEETS["staff"]))
        names: list[str] = re.findall(r"(--[\w-]+):", block)
        self.assertTrue(names)
        for token in names:
            if re.match(r"--sp-\d", token):
                continue
            self.assertIn(f"`{token}`", doc, token)


class NonColourStatusSignals(unittest.TestCase):
    def test_status_cues_use_glyphs_not_colour_alone(self) -> None:
        css: str = read(STYLESHEETS["staff"])
        for selector in NON_COLOUR_CUES:
            self.assertIn(selector, css, selector)
        self.assertRegex(css, r'\.status-line\.ok:before\{content:"\\2713')
        self.assertRegex(css, r'\.flag\.danger:before[^{]*\{content:"\\26A0')

    def test_resident_pages_announce_status_politely(self) -> None:
        for sub in ("resident_demo", "resident_preview"):
            html: str = read(API / sub / "web" / "index.html")
            self.assertIn('role="status"', html, sub)
            self.assertIn('aria-live="polite"', html, sub)


class ReducedMotion(unittest.TestCase):
    def test_each_stylesheet_has_reduced_motion_hook(self) -> None:
        for name, path in STYLESHEETS.items():
            self.assertIn("prefers-reduced-motion:reduce", read(path), name)

    def test_motion_token_zeroed_for_reduced_motion(self) -> None:
        for name in ROOT_TOKEN_SHEETS:
            css: str = read(STYLESHEETS[name])
            self.assertIn("prefers-reduced-motion:reduce){:root{--motion:0s}}", css, name)

    def test_animations_are_disabled_under_reduced_motion(self) -> None:
        self.assertIn(".async-spinner{animation:none", read(STYLESHEETS["staff"]))
        self.assertIn("animation:none", read(STYLESHEETS["chat"]))
        self.assertIn("animation:none", read(STYLESHEETS["resident-demo"]))


class PlainLanguageLabels(unittest.TestCase):
    def test_resident_copy_avoids_internal_terms(self) -> None:
        for sub, files in (
            ("resident_demo", ("index.html", "demo.js", "assistant.js")),
            ("resident_preview", ("index.html", "resident.js")),
        ):
            for file in files:
                text: str = read(API / sub / "web" / file)
                for number, line in enumerate(text.splitlines(), 1):
                    self.assertIsNone(
                        RESIDENT_COPY_BANNED.search(line), f"{sub}/{file}:{number}: {line.strip()}"
                    )

    def test_content_standard_is_present(self) -> None:
        self.assertIn("plain", read(UX_DOCS / "content-standard.md").lower())


class ApprovalAndConsentBoundaries(unittest.TestCase):
    def test_staff_approvals_are_explicit_controls(self) -> None:
        panels: str = read(API / "web" / "panels.js")
        self.assertIn('go("budget_approve")', panels)
        self.assertIn('go("grant_approve"', panels)
        self.assertRegex(panels, r"Approve (the budget|a commitment|a proposed stage)")

    def test_resident_ai_summary_needs_explicit_optional_consent(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        self.assertIn('consent.type = "checkbox"', js)
        self.assertNotIn("consent.checked = true", js)
        self.assertNotIn("consent.defaultChecked", js)
        self.assertIn("if (!consent.checked)", js)
        self.assertIn('consent.setAttribute("aria-invalid", "true")', js)
        self.assertIn("(optional). This is not consent to works.", js)

    def test_automation_never_claims_decision_or_consent(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        self.assertIn("Neither rules nor AI can make decisions, approve documents", js)
        self.assertIn("give consent", js)
        self.assertIn("does not imply consent or refusal", read(API / "web" / "app.js"))

    def test_resident_sensor_chart_text_and_markers_stay_legible(self) -> None:
        css: str = read(STYLESHEETS["resident-demo"])
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        text_rule = re.search(r"\.sensor-chart text\{[^}]*font:(\d+)px", css)
        self.assertIsNotNone(text_rule, "chart text size must be in SVG user units, not rem")
        self.assertLessEqual(int(text_rule.group(1)), 14)  # type: ignore[union-attr]
        self.assertRegex(css, r"\.sensor-chart svg\{[^}]*max-width:\d+rem")
        self.assertIn("markerGap", js)
        self.assertIn("Circles mark some of the stored readings", js)
        # The forced latest marker replaces a too-close neighbour instead of touching it.
        self.assertIn("svg.removeChild(lastMarker)", js)
        # "Latest stored" flips to the divider's right when 90 units of room are missing.
        self.assertIn("anchorX - 4 - 56 >= 90", js)
        self.assertIn('"text-anchor": roomLeft ? "end" : "start"', js)

    @unittest.skipUnless(shutil.which("node"), "node is required")
    def test_resident_sensor_chart_geometry_with_dense_history(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        helpers = re.search(r"  function el\(tag.*?\n  }\n", js, re.S)
        chart = re.search(r"  var sensorMetrics = \[.*?(?=\n  function renderConsent)", js, re.S)
        assert helpers and chart
        script = (
            "const document = { createElement: t => mk(t), createElementNS: (n, t) => mk(t) };\n"
            "function mk(tag) { return { tag, attrs: {}, children: [], className: '',"
            " setAttribute(k, v) { this.attrs[k] = v; },"
            " appendChild(c) { this.children.push(c); return c; },"
            " removeChild(c) { this.children.splice(this.children.indexOf(c), 1); } }; }\n"
            + helpers.group(0)
            + chart.group(0)
            + """
function run(count, hours) {
const history = [];
for (let i = 0; i < count; i++) {
  const at = new Date(Date.UTC(2026, 10, 22, 0, 0) + i * 300000).toISOString();
  history.push({ observed_at: at, temperature_c: 44 - (i % 3) * 0.1,
    temperature_status: "ok", humidity_pct: 50, humidity_status: "ok" });
}
const last = Date.parse(history[count - 1].observed_at);
const at = h => new Date(last + h * 3600000).toISOString();
const points = hours.map(h => ({ forecast_at: at(h), temperature_c: 44, humidity_pct: 50 }));
const forecast = { points };
const svg = sensorChart(history, sensorMetrics[0], forecast).children[1];
const circles = svg.children.filter(c => c.tag === "circle").map(c => c.attrs);
const label = svg.children.find(c => c.textContent === "Latest stored");
const line = svg.children.find(c => c.tag === "line" && c.attrs.class === "sensor-divider");
return { xs: circles.map(c => c.cx), label: label.attrs, divider: line.attrs.x1,
  squares: svg.children.filter(c => c.tag === "rect").length };
}
function outOfRange() {
const history = [{ observed_at: "2026-11-22T00:00:00Z", temperature_c: 60,
  temperature_status: "ok", humidity_pct: 50, humidity_status: "ok" },
  { observed_at: "2026-11-22T00:05:00Z", temperature_c: -30,
  temperature_status: "ok", humidity_pct: 50, humidity_status: "ok" }];
const forecast = { points: [{ forecast_at: "2026-11-22T06:00:00Z", temperature_c: 99,
  humidity_pct: 50 }] };
const svg = sensorChart(history, sensorMetrics[0], forecast).children[1];
const ys = [];
svg.children.forEach(c => {
  if (c.tag === "circle") ys.push(c.attrs.cy);
  if (c.tag === "rect") ys.push(c.attrs.y + 3.5);
  if (c.tag === "polyline") c.attrs.points.split(" ").forEach(p => ys.push(+p.split(",")[1]));
});
return ys;
}
console.log(JSON.stringify({ dense: run(288, [1, 2, 3]), short: run(4, [6, 12, 24]),
  out: outOfRange() }));
"""
        )
        out = json.loads(
            subprocess.run(
                ["node", "-e", script], capture_output=True, text=True, check=True
            ).stdout
        )
        dense, short = out["dense"], out["short"]
        xs = dense["xs"]
        self.assertGreater(len(xs), 10)
        self.assertTrue(
            all(b - a >= 8.99 for a, b in zip(xs, xs[1:], strict=False)), "circles must not touch"
        )
        self.assertAlmostEqual(xs[-1], dense["divider"], places=6)  # latest reading is drawn
        self.assertEqual(dense["squares"], 3)
        self.assertLessEqual(dense["label"]["x"], dense["divider"] - 4)
        self.assertEqual(dense["label"]["text-anchor"], "end")
        self.assertGreaterEqual(short["label"]["x"], short["divider"] + 4)
        self.assertEqual(short["label"]["text-anchor"], "start")
        # Values outside the fixed axis stay inside the plot area instead of covering the ticks.
        self.assertGreaterEqual(len(out["out"]), 4)
        self.assertTrue(all(10 <= y <= 150 for y in out["out"]), out["out"])

    @unittest.skipUnless(shutil.which("node"), "node is required to execute the chart code")
    def test_resident_sensor_chart_behaviour_in_node(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        helpers = js[js.index("  function el(") : js.index("  function card(")]
        chart = js[js.index("  var sensorMetrics") : js.index("  function renderConsent(")]
        self.assertIn("function sensorChart", chart)
        harness = r"""
const vm = require("vm");
const src = JSON.parse(process.argv[1]);
function node(tag) {
  return { tag, attrs: {}, children: [], textContent: "", className: "",
    setAttribute(k, v) { this.attrs[k] = String(v); },
    appendChild(c) { this.children.push(c); return c; },
    removeChild(c) { this.children.splice(this.children.indexOf(c), 1); return c; },
    insertBefore(c) { this.children.push(c); return c; }, querySelector() { return node("x"); } };
}
const document = { createElement: node, createElementNS: (ns, tag) => node(tag) };
const ctx = vm.createContext({ document, Intl, Date });
const tail = "\nthis.sensorChart = sensorChart; this.metric = sensorMetrics[0];";
vm.runInContext(src.helpers + src.chart + tail, ctx);
function readings(count, stepMin) {
  const t0 = Date.parse("2026-11-20T00:00:00Z");
  return Array.from({ length: count }, (_, i) => ({
    observed_at: new Date(t0 + i * stepMin * 60000).toISOString(),
    temperature_c: 18 + (i % 7), temperature_status: "ok" }));
}
function forecast(history) {
  const last = Date.parse(history[history.length - 1].observed_at);
  return { points: Array.from({ length: 6 }, (_, i) => ({
    forecast_at: new Date(last + (i + 1) * 4 * 3600000).toISOString(), temperature_c: 20 })) };
}
function walk(n, out) { out.push(n); n.children.forEach((c) => walk(c, out)); return out; }
const isDivider = (n) => n.attrs.class === "sensor-divider";
function render(history, fc) {
  const all = walk(ctx.sensorChart(history, ctx.metric, fc), []);
  const label = all.find((n) => n.textContent === "Latest stored");
  return {
    circles: all.filter((n) => n.tag === "circle").map((n) => n.attrs.cx).map(Number),
    squares: all.filter((n) => n.attrs.class === "sensor-forecast-point").length,
    labelAnchor: label ? label.attrs["text-anchor"] : null,
    labelX: label ? Number(label.attrs.x) : null,
    divider: Number(((all.find(isDivider)) || { attrs: {} }).attrs.x1 || 0),
    thinnedNote: all.some((n) => /Circles mark some/.test(n.textContent)),
  };
}
const dense = readings(289, 5);
const wide = readings(25, 60);
const narrow = readings(3, 5);
console.log(JSON.stringify({
  dense: render(dense, forecast(dense)), wide: render(wide, forecast(wide)),
  narrow: render(narrow, forecast(narrow)), plain: render(wide, null) }));
"""
        done = subprocess.run(
            ["node", "-e", harness, json.dumps({"helpers": helpers, "chart": chart})],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        out = json.loads(done.stdout)
        dense = out["dense"]
        self.assertGreater(len(dense["circles"]), 5)
        self.assertLess(len(dense["circles"]), 100, "dense history must be thinned")
        gaps = [b - a for a, b in zip(dense["circles"], dense["circles"][1:], strict=False)]
        self.assertGreaterEqual(min(gaps), 9 - 1e-9, "circles must not merge into one thick stroke")
        self.assertAlmostEqual(dense["circles"][-1], dense["divider"], places=6)
        self.assertTrue(dense["thinnedNote"])
        self.assertEqual(dense["squares"], 6)
        self.assertEqual(dense["labelAnchor"], "end")
        self.assertLess(dense["labelX"], dense["divider"])
        self.assertEqual(out["wide"]["labelAnchor"], "end")
        # Near the left edge the label moves right of the divider, clear of the axis tick labels.
        self.assertEqual(out["narrow"]["labelAnchor"], "start")
        self.assertGreater(out["narrow"]["labelX"], out["narrow"]["divider"])
        self.assertEqual(out["plain"]["labelAnchor"], None)
        self.assertEqual(out["plain"]["squares"], 0)

    @unittest.skipUnless(shutil.which("node"), "node is required to execute the chart code")
    def test_resident_sensor_chart_every_metric_in_node(self) -> None:
        js: str = read(API / "resident_demo" / "web" / "demo.js")
        helpers = js[js.index("  function el(") : js.index("  function card(")]
        chart = js[js.index("  var sensorMetrics") : js.index("  function renderConsent(")]
        harness = r"""
const vm = require("vm");
const src = JSON.parse(process.argv[1]);
function node(tag) {
  return { tag, attrs: {}, children: [], textContent: "", className: "",
    setAttribute(k, v) { this.attrs[k] = String(v); },
    appendChild(c) { this.children.push(c); return c; },
    removeChild(c) { this.children.splice(this.children.indexOf(c), 1); return c; },
    insertBefore(c) { this.children.push(c); return c; }, querySelector() { return node("x"); } };
}
const document = { createElement: node, createElementNS: (ns, tag) => node(tag) };
const ctx = vm.createContext({ document, Intl, Date });
vm.runInContext(src.helpers + src.chart
  + "\nthis.sensorChart = sensorChart; this.metrics = sensorMetrics;", ctx);
function walk(n, out) { out.push(n); n.children.forEach((c) => walk(c, out)); return out; }
const t0 = Date.parse("2026-11-20T00:00:00Z");
const result = ctx.metrics.map((metric) => {
  const history = Array.from({ length: 289 }, (_, i) => ({
    observed_at: new Date(t0 + i * 300000).toISOString(),
    [metric.key]: i === 5 ? metric.max + 50 : metric.min + (metric.max - metric.min) * 0.4,
    [metric.status]: "ok" }));
  const last = t0 + 288 * 300000;
  const forecast = { points: [1, 6, 24].map((h) => ({
    forecast_at: new Date(last + h * 3600000).toISOString(), [metric.key]: metric.min - 40 })) };
  const all = walk(ctx.sensorChart(history, metric, forecast), []);
  const svg = all.find((n) => n.tag === "svg");
  const label = all.find((n) => n.textContent === "Latest stored");
  const ticks = all.filter((n) => n.tag === "text"
    && n.attrs["text-anchor"] === "end" && n.attrs.x === "50");
  const ys = [];
  all.forEach((n) => {
    if (n.tag === "circle") ys.push(Number(n.attrs.cy));
    if (n.tag === "rect") ys.push(Number(n.attrs.y) + 3.5);
    if (n.tag === "polyline") {
      n.attrs.points.split(" ").forEach((p) => ys.push(Number(p.split(",")[1])));
    }
  });
  return { name: metric.name, ticks: ticks.length, ys,
    xs: all.filter((n) => n.tag === "circle").map((n) => Number(n.attrs.cx)),
    labelX: Number(label.attrs.x), anchor: label.attrs["text-anchor"],
    labelY: Number(label.attrs.y), viewBox: svg.attrs.viewBox };
});
console.log(JSON.stringify(result));
"""
        done = subprocess.run(
            ["node", "-e", harness, json.dumps({"helpers": helpers, "chart": chart})],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        results = json.loads(done.stdout)
        self.assertEqual([r["name"] for r in results], ["Temperature", "Humidity"])
        for r in results:
            with self.subTest(metric=r["name"]):
                self.assertEqual(r["ticks"], 3)
                self.assertTrue(all(10 <= y <= 150 for y in r["ys"]), "values stay in the plot")
                gaps = [b - a for a, b in zip(r["xs"], r["xs"][1:], strict=False)]
                self.assertGreaterEqual(min(gaps), 9 - 1e-9)
                # End-anchored label (about 80 units wide) must clear the tick column at x=50.
                self.assertEqual(r["anchor"], "end")
                self.assertGreater(r["labelX"] - 80, 50)
                self.assertLess(r["labelX"], 470)
                self.assertLess(r["labelY"], 180)


class HumanEvidenceNotFabricated(unittest.TestCase):
    def test_no_automated_surface_claims_human_sign_off(self) -> None:
        claim = re.compile(
            r"(AT|assistive technology|comprehension)[^\n]{0,40}(passed|signed off)", re.I
        )
        for path in STYLESHEETS.values():
            self.assertIsNone(claim.search(read(path)), path.name)

    def test_pending_evidence_issues_are_named_open(self) -> None:
        self.assertEqual(set(PENDING_HUMAN_EVIDENCE), {"#155", "#215"})


if __name__ == "__main__":
    unittest.main()
