"""The Home sensors case tab: tab list, states, wording, alert label and the narrow tab row.

The shipped scripts run in a Node mini DOM. Payloads come from the server's own sensor_view and
sensor_badges code over hand-made reading rows, so field names and states are the real contract.
These tests check structure and wording on constructed data. They are not accessibility or
usability evidence.
"""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest import mock

from zava_forward.core import sensor_map, sensor_review_draft, sensor_view

from zava_forward.api import sensor_badges

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
OPS = (WEB / "ops.js").read_text()
HOME = "ZF-Q"
NOW = datetime(2026, 11, 20, 13, 31, 46, tzinfo=UTC)
LAST = NOW - timedelta(minutes=6)
ANCHOR = NOW - timedelta(days=9)
QI = "Quality Inspector"
FORBIDDEN = (
    "manual-sensor-review",
    "Durable SQL",
    "decision_rule",
    "dew_point_c",
    "mould_risk_index",
    "quality_record_anchor",
)
NOT_LINKED = "Current staff role has changed or been revoked."
NOT_CONNECTED = "Durable SQL is required; use the ordinary case/manual route."
SERVICE_DOWN = "Sensor readings unavailable; continue the ordinary quality check manually."
DRAFTS_DOWN = "Sensor review drafts unavailable; use the manual route: manual-sensor-review."
OWNER_NEXT = r"Owner: [^.]+\. Next action: "

Row = tuple[str, ...]


def _row(n: int, when: datetime, temp: object, hum: object, **extra: Any) -> Row:
    live = bool(extra.get("live"))
    return (
        f"SYN-R-{n:04d}",
        extra.get("sensor", "SYN-S-01"),
        when.strftime(sensor_view.STAMP),
        str(temp),
        str(hum),
        "live-simulator" if live else "synthetic",
        "live-sim-reading-v1" if live else "reading-v1",
        HOME,
        "SYNTHETIC",
    )


def _recent(age_minutes: int) -> list[Row]:
    return [
        _row(i, NOW - timedelta(minutes=age_minutes + (11 - i) * 30), 17 + i / 10, 61 + i)
        for i in range(12)
    ]


def _context() -> list[Row]:
    before = [_row(100 + i, ANCHOR - timedelta(minutes=90 * (i + 1)), 16.5, 64) for i in range(4)]
    after = [_row(200 + i, ANCHOR + timedelta(minutes=90 * (i + 1)), 18.0, 58) for i in range(4)]
    return before + after


def _rows(kind: str) -> list[Row]:
    if kind == "stale":
        return _recent(180) + _context()
    if kind == "offline-24h":
        return _recent(3 * 24 * 60) + _context()
    if kind == "conflict":
        return _recent(6) + _context() + [_row(99, LAST, 21.4, 70)]
    if kind == "conflict-stale":
        return _recent(180) + _context() + [_row(99, NOW - timedelta(minutes=180), 21.4, 70)]
    if kind == "fault":
        return _recent(6)[:-1] + [_row(11, LAST, 17.1, "")] + _context()
    if kind == "out-of-range":
        return _recent(6)[:-1] + [_row(11, LAST, 75.0, 72)] + _context()
    if kind == "mixed":
        rows = [
            _row(
                i,
                NOW - timedelta(minutes=6 + (11 - i) * 30),
                17 + i / 10,
                61 + i,
                live=i % 2 == 0,
                sensor="SYN-S-02" if i % 3 == 0 else "SYN-S-01",
            )
            for i in range(12)
        ]
        return rows + _context()
    if kind == "no-readings":
        return []
    if kind == "no-anchor":
        return _recent(6)
    return _recent(6) + _context()


def payload(kind: str) -> dict[str, Any]:
    """The /sensors response for one state, built by the server's read model and badge code."""
    db = sqlite3.connect(":memory:")
    db.execute(
        "CREATE TABLE sensor_reading (reading_id, sensor_id, observed_at, temperature_c,"
        " humidity_pct, scenario, schema_version, home_id, source_type)"
    )
    db.executemany("INSERT INTO sensor_reading VALUES (?,?,?,?,?,?,?,?,?)", _rows(kind))
    if kind == "unavailable":
        consent = mock.patch.object(sensor_view, "consent", side_effect=RuntimeError("no table"))
    else:
        verdict = "declined" if kind == "withheld" else "granted"
        consent = mock.patch.object(sensor_view, "consent", return_value=verdict)
    reference = None if kind == "no-anchor" else ANCHOR
    with consent:
        view: dict[str, Any] = sensor_view.view(db, HOME, reference, NOW.timestamp())
    annotated: dict[str, Any] = sensor_badges.annotate(view)
    return annotated


def drafts(kind: str) -> dict[str, Any]:
    if kind == "withheld":
        note = sensor_review_draft.WITHHELD_NOTE
        return {"state": "consent-withheld", "case_id": HOME, "drafts": [], "note": note}
    if kind == "none":
        return {"state": "ok", "case_id": HOME, "drafts": []}
    if kind == "integrity":
        return {"state": "ok", "case_id": HOME, "drafts": [{"state": "INTEGRITY_MISMATCH"}]}
    draft = {
        "state": sensor_review_draft.STATE,
        "label": sensor_review_draft.LABEL,
        "task_key": "SYN-TASK-1",
        "candidate": {
            "summary": "Humidity stayed high for four days.",
            "rule_id": "SYN-RULE-7",
            "policy_version": "1",
            "analysis_version": "3",
        },
        "lineage": {"window_start": "2026-11-11T08:00:00Z", "window_end": "2026-11-20T08:00:00Z"},
        "approval_note": sensor_review_draft.APPROVAL_NOTE,
        "created_by": {"name": "Quality Inspector Example", "role": QI},
        "created_at": "2026-11-20T09:15:00Z",
        "digest_prefix": "a1b2c3d4e5f6",
    }
    return {"state": "ok", "case_id": HOME, "drafts": [draft]}


def reply(body: Any, status: int = 200) -> dict[str, Any]:
    return {"status": status, "body": body}


# A minimal DOM: only what h(), sensorPanel() and CaseWorkspace.enhance() touch.
DOM = r"""
const assert = require("node:assert/strict");
class Node {
  constructor(tag = "#text", text = "") {
    this.tagName = tag.toUpperCase(); this.nodeType = 1; this.attrs = {}; this.dataset = {};
    this.children = []; this.events = {}; this._text = text; this.writes = 0; this.className = "";
    this.observers = [];
  }
  append(...kids) {
    kids.flat().forEach(k => {this.children.push(k); if (k.nodeType) k.parentElement = this;});
  }
  replaceChildren(...kids) {this.children = []; this.append(...kids);}
  setAttribute(name, value) {
    this.attrs[name] = String(value);
    if (name.startsWith("data-")) {
      this.dataset[name.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = String(value);
    }
    this.observers.forEach(observer => queueMicrotask(observer.callback));
  }
  getAttribute(name) {return this.attrs[name] ?? null;}
  hasAttribute(name) {return name in this.attrs;}
  removeAttribute(name) {delete this.attrs[name];}
  get id() {return this.attrs.id;}
  get textContent() {return this._text + this.children.map(k => k.textContent ?? k).join("");}
  set textContent(value) {this.writes++; this._text = value; this.children = [];}
  all() {return this.children.filter(k => k.nodeType).flatMap(k => [k, ...k.all()]);}
  matches(selector) {
    if (selector.startsWith("#")) return this.id === selector.slice(1);
    if (selector.startsWith(".")) return this.className.split(" ").includes(selector.slice(1));
    if (selector.startsWith("[")) {
      const [, name, value] = selector.match(/^\[([^=\]]+)(?:="([^"]*)")?\]/);
      return this.hasAttribute(name) && (value === undefined || this.getAttribute(name) === value);
    }
    return this.tagName === selector.toUpperCase();
  }
  querySelectorAll(selector) {
    return this.all().filter(k => selector.split(",").some(s => k.matches(s.trim())));
  }
  querySelector(selector) {return this.querySelectorAll(selector)[0];}
  addEventListener(name, fn) {this.events[name] = fn;}
  focus() {document.activeElement = this;}
  scrollIntoView() {}
}
const document = {createElement: tag => new Node(tag),
  createElementNS: (ns, tag) => new Node(tag),
  createTextNode: text => new Node("#text", text),
  getElementById: () => ({scrollIntoView() {document.scrolled = true;}})};
class MutationObserver {
  constructor(callback) {this.callback = callback; MutationObserver.all.push(this);}
  observe(node) {node.observers.push(this);}
  disconnect() {}
}
MutationObserver.all = [];
"""

RUNTIME = r"""
const routeController = new AbortController();
const app = new Node("main"), aiMode = {workflow: false}, history = {pushState() {}};
let location = {hash: "#/case/ZF-Q?tab=sensors"}, displayedHash;
const CASE = {id: "ZF-Q", hazards: [], work: {}};
let requests = [];
globalThis.fetch = async (path) => {
  requests.push(path);
  const key = Object.keys(RESPONSES).find(suffix => path.endsWith(suffix));
  if (!key) return {ok: false, status: 404, json: async () => ({error: "Not stubbed."})};
  if (RESPONSES[key].network) throw new TypeError("Failed to fetch");
  const {status, body} = RESPONSES[key];
  return {ok: status < 400, status, json: async () => body};
};
const settle = async () => {
  for (let i = 0; i < 8; i++) await new Promise(resolve => setImmediate(resolve));
};
const observe = (panel) => ({
  status: panel.querySelector(".status-line").textContent,
  order: panel.children.map(node => node.hasAttribute("data-sensor-badges") ? "status"
    : node.hasAttribute("data-sensor-advisory") ? "advice" : "details"),
  firstHoldsStatus: panel.children[0].querySelectorAll(".status-line").length === 1,
  advice: (panel.querySelector("[data-sensor-advisory]") || {}).textContent,
  text: panel.textContent,
  attrs: panel.all().flatMap(node => Object.values(node.attrs)).join(" "),
  headings: panel.querySelectorAll("h3,h4").map(node => node.textContent),
  tables: panel.querySelectorAll("table").length,
  alerts: panel.querySelectorAll(".sensor-alert")
    .map(item => item.querySelectorAll("dt").map(node => node.textContent)),
  alertCount: panel.getAttribute("data-sensor-alerts"),
  busy: panel.hasAttribute("aria-busy"),
  requests,
});
"""

PANEL_JS = """
const panel = sensorPanel("ZF-Q");
await settle();
console.log(JSON.stringify(observe(panel)));
"""

POINTER_JS = """
const calls = [];
const line = sensorPointer({controller: {select: (...args) => calls.push(args)}});
const button = line.querySelector("button");
button.events.click();
sensorPointer({}).querySelector("button").events.click();
console.log(JSON.stringify({text: line.textContent, kind: button.className, calls,
  scrolled: Boolean(document.scrolled), nested: line.querySelectorAll("#sensors").length}));
"""

TABS_JS = """
const definitions = DATA.tabs.map(([id, label]) => ({id, label,
  panel: h("section", {id: `case-panel-${id}`}, h("h2", {}, label),
    id === "sensors" && DATA.live ? sensorPanel("ZF-Q") : null)}));
const ui = CaseWorkspace.enhance(CASE, definitions, null, h("section", {}), h("div", {}));
const buttons = ui.tabs.querySelectorAll("button");
const sensors = buttons[DATA.tabs.findIndex(([id]) => id === "sensors")];
const before = sensors.textContent;
await settle();
MutationObserver.all.forEach(observer => { observer.callback(); observer.callback(); });
await settle();
const rows = ui.tabs.children.filter(child => child.nodeType);
console.log(JSON.stringify({labels: buttons.map(button => button.textContent), before,
  after: sensors.textContent, writes: sensors.writes, rows: rows.map(row => row.className),
  inRow: rows[0].children.length, role: ui.tabs.getAttribute("role")}));
"""

AI_LABEL_JS = """
const definitions = ["overview", "ai"].map(id => ({id, label: id,
  panel: h("section", {}, h("h2", {}, id))}));
const assistant = h("section", {});
const ui = CaseWorkspace.enhance(CASE, definitions, null, assistant, h("div", {}));
assistant.setAttribute("data-waiting", "0");
assistant.setAttribute("data-assistance", "AI assistance unavailable. Work continues manually.");
ui.counts();
console.log(JSON.stringify({label: ui.tabs.querySelectorAll("button")[1].textContent}));
"""

MODEL_JS = """
const stale = (age) => sensorModel(
  {badges: [{kind: "freshness", state: "stale"}], age_seconds: age}).alerts;
console.log(JSON.stringify({at: stale(DATA.offline), over: stale(DATA.offline + 1),
  fresh: SENSOR_FRESH_SECONDS, offline: SENSOR_OFFLINE_SECONDS,
  words: sensorState("stale").words}));
"""

SHAPE_JS = """
const tables = (view) => sensorBody(view, sensorModel(view))
  .flatMap(node => node.querySelectorAll ? node.querySelectorAll("table") : []);
const heads = (table) => table.querySelectorAll("th")
  .filter(cell => cell.attrs.scope === "col").map(cell => cell.textContent);
const first = tables(DATA.fresh)[0], body = first.querySelector("tbody");
console.log(JSON.stringify({one: heads(first), wide: heads(tables(DATA.mixed)[0]),
  caption: first.querySelector("caption").textContent,
  rowHeader: body.querySelector("th").attrs.scope, time: body.querySelector("time").attrs.datetime,
  firstCell: body.querySelector("th").textContent, region: first.parentElement.attrs.role,
  name: first.parentElement.attrs["aria-label"]}));
"""

COPY_JS = """
const states = Object.fromEntries(Object.keys(SENSOR_COPY).map(key => [key, sensorState(key)]));
const alerts = Object.entries(SENSOR_COPY).filter(([, entry]) => entry.alert)
  .map(([key, entry]) => [key, entry.alert.message]);
console.log(JSON.stringify({keys: Object.keys(SENSOR_COPY), states, alerts}));
"""


def helpers() -> str:
    """h(), api() and fmtDate() exactly as app.js ships them, with the read retry passed through."""
    source = (WEB / "app.js").read_text()
    return (
        "function h"
        + source.split("function h", 1)[1].split("async function api", 1)[0]
        + "let caseSession = null;\n"
        + "const fetchReadRetrying = (path, options) => fetch(path, options);\n"
        + "async function api"
        + source.split("async function api", 1)[1].split("const ago", 1)[0]
    )


def run_node(
    body: str,
    *,
    role: str = QI,
    responses: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    ops: str = OPS,
) -> Any:
    script = (
        DOM
        + helpers()
        + f"const me = {{user: {{role: {json.dumps(role)}}}}};\n"
        + f"let RESPONSES = {json.dumps(responses or {})};\n"
        + f"const DATA = {json.dumps(data or {})};\n"
        + RUNTIME
        + ops
        + (WEB / "case-workspace.js").read_text()
        + "\n(async () => {\n"
        + body
        + "\n})().catch(error => {console.error(error); process.exitCode = 1;});\n"
    )
    result = subprocess.run(
        ["node", "-"], input=script, text=True, capture_output=True, timeout=120
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout.strip().splitlines()[-1])


def tab_definitions() -> list[list[str]]:
    """Tab ids and labels in the order app.js lists them."""
    app = (WEB / "app.js").read_text()
    block = app.split("const definitions = [", 1)[1].split("].map(([tab, label, nodes])", 1)[0]
    found = re.findall(r'^    \["(\w+)", (?:"([^"]*)"|`([^`]*)`)', block, re.M)
    return [
        [tab, (quoted or templated).replace("${c.work.blockers.length}", "0")]
        for tab, quoted, templated in found
    ]


def scenario(
    sensors: dict[str, Any], draft: dict[str, Any] | None = None, **extra: Any
) -> dict[str, Any]:
    responses = {"/sensors": sensors}
    if draft is not None:
        responses["/sensor-drafts"] = draft
    return {"responses": responses, **extra}


def injected_values() -> dict[str, Any]:
    """A withheld reply that wrongly carries readings: the screen must still show none of them."""
    row = {
        "reading_id": "SYN-R-0777",
        "sensor_id": "SYN-S-01",
        "observed_at": "2026-11-20T13:25:46Z",
        "temperature_c": "23.7",
        "humidity_pct": "88",
        "provenance_class": "synthetic-modelled-indoor",
    }
    return dict(payload("withheld"), latest=row, readings=[row])


# One entry per state a person can reach. The matrix runs once for the whole class.
SCENARIOS: dict[str, dict[str, Any]] = {
    "fresh": scenario(reply(payload("fresh")), reply(drafts("one"))),
    "stale": scenario(reply(payload("stale")), reply(drafts("none"))),
    "offline-24h": scenario(reply(payload("offline-24h")), reply(drafts("none"))),
    "conflict": scenario(reply(payload("conflict")), reply({"state": "disabled"})),
    "conflict-stale": scenario(reply(payload("conflict-stale")), reply(drafts("none"))),
    "fault": scenario(reply(payload("fault")), reply(drafts("integrity"))),
    "out-of-range": scenario(reply(payload("out-of-range")), reply(drafts("none"))),
    "mixed": scenario(reply(payload("mixed")), reply(drafts("none"))),
    "no-anchor": scenario(reply(payload("no-anchor")), reply(drafts("none"))),
    "no-readings": scenario(reply(payload("no-readings")), reply(drafts("none"))),
    "withheld": scenario(reply(payload("withheld")), reply(drafts("withheld"))),
    "withheld-with-values": scenario(reply(injected_values()), reply(drafts("withheld"))),
    "unavailable": scenario(reply(payload("unavailable"))),
    "drafts-down": scenario(reply(payload("fresh")), reply({"error": DRAFTS_DOWN}, 503)),
    "not-linked": scenario(reply({"error": NOT_LINKED}, 403), reply(drafts("one"))),
    "other-refusal": scenario(reply({"error": "Case is outside your current scope."}, 403)),
    "service-down": scenario(reply({"error": SERVICE_DOWN}, 503), reply(drafts("one"))),
    "not-connected": scenario(reply({"error": NOT_CONNECTED}, 400)),
    "network": scenario({"network": True}),
    "restricted": scenario(
        reply(payload("fresh")), reply(drafts("one")), role="Resident Liaison Officer"
    ),
}


class HomeSensorsTab(unittest.TestCase):
    matrix: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = {
            name: run_node(PANEL_JS, role=item.get("role", QI), responses=item["responses"])
            for name, item in SCENARIOS.items()
        }

    def text(self, name: str) -> str:
        return str(self.matrix[name]["text"])

    def test_the_status_line_comes_first_and_the_advice_sentence_sits_under_it(self) -> None:
        advice = "Readings are advice for a person to check. They do not change the case."
        for name, seen in self.matrix.items():
            with self.subTest(state=name):
                self.assertEqual(seen["order"], ["status", "advice", "details"])
                self.assertTrue(seen["firstHoldsStatus"])
                self.assertEqual(seen["advice"], advice)

    def test_ten_tabs_with_home_sensors_between_quality_and_ai(self) -> None:
        tabs = tab_definitions()
        self.assertEqual([tab for tab, _ in tabs], [
            "overview", "blockers", "survey", "funding", "resident",
            "contractor", "quality", "sensors", "ai", "history",
        ])  # fmt: skip
        labels = dict(tabs)
        self.assertEqual(
            [labels[i] for i in ("quality", "sensors", "ai", "history")],
            ["Quality and handover", "Home sensors", "AI assistance", "History"],
        )
        shown = run_node(TABS_JS, data={"tabs": tabs})
        self.assertEqual(len(shown["labels"]), 10)
        self.assertEqual(
            shown["labels"][6:],
            ["Quality and handover", "Home sensors", "AI assistance (loading)", "History"],
        )

    def test_quality_tab_points_to_home_sensors_and_no_longer_holds_the_readings(self) -> None:
        app = (WEB / "app.js").read_text()
        block = app.split("const definitions = [", 1)[1].split("].map(([tab, label, nodes])", 1)[0]
        quality = re.search(r'^    \["quality".*$', block, re.M)
        sensors = re.search(r'^    \["sensors".*$', block, re.M)
        assert quality and sensors
        self.assertIn("sensorPointer(session)", quality.group(0))
        self.assertNotIn("sensorPanel(", quality.group(0))
        self.assertIn("sensorPanel(id)", sensors.group(0))
        seen = run_node(POINTER_JS)
        self.assertEqual(
            seen["text"],
            "Home sensor readings and alerts are on the Home sensors tab. Open Home sensors",
        )
        self.assertEqual(seen["kind"], "alt")
        self.assertEqual(seen["calls"], [["sensors", True, True]])
        self.assertTrue(seen["scrolled"])
        self.assertEqual(seen["nested"], 0)

    def test_a_role_that_may_not_read_makes_no_request_and_is_told_why(self) -> None:
        seen = self.matrix["restricted"]
        self.assertEqual(seen["requests"], [])
        self.assertEqual(seen["status"], "Sensor readings are not shown for your role")
        self.assertIn(
            "Your role does not include indoor readings. Owner: a Quality Inspector or a Retrofit"
            " Programme Manager. Next action: ask one of them for the readings you need.",
            seen["text"],
        )
        self.assertEqual((seen["tables"], seen["alertCount"], seen["busy"]), (0, None, False))

    def test_a_revoked_role_reply_shows_the_not_linked_copy_and_asks_for_no_drafts(self) -> None:
        seen = self.matrix["not-linked"]
        self.assertEqual(seen["requests"], ["/api/cases/ZF-Q/sensors"])
        self.assertEqual(seen["status"], "Your staff account is not linked to your role")
        self.assertIn(
            "Your staff account is not linked to your role, so home readings are hidden. Owner:"
            " your team manager. Next action: ask them to check that your account is on the staff"
            " list with your role, then refresh this page. Until then, use the ordinary quality"
            " check.",
            seen["text"],
        )
        self.assertEqual((seen["tables"], seen["alerts"], seen["alertCount"]), (0, [], None))
        self.assertNotIn("Latest reading", seen["headings"])
        self.assertNotIn(NOT_LINKED, seen["text"])

    def test_other_failures_use_the_matching_copy(self) -> None:
        down = self.matrix["service-down"]
        self.assertEqual(down["requests"], ["/api/cases/ZF-Q/sensors"])
        self.assertEqual(down["status"], "Home sensors are unavailable right now")
        self.assertIn(
            "Owner: application support. Next action: refresh this page. If it keeps happening,"
            " tell application support. Use the ordinary quality check meanwhile.",
            down["text"],
        )
        for name in ("network", "other-refusal"):
            self.assertEqual(self.matrix[name]["status"], down["status"], name)
        connected = self.matrix["not-connected"]
        self.assertEqual(connected["status"], "Sensor readings are not connected in this setup")
        self.assertIn(
            "Owner: application support. Next action: use the ordinary quality check. Tell"
            " application support if you expected readings here.",
            connected["text"],
        )

    def test_consent_withheld_shows_no_number_and_no_table(self) -> None:
        for name in ("withheld", "withheld-with-values"):
            seen = self.matrix[name]
            self.assertEqual(
                seen["status"], "Readings withheld: monitoring consent is not granted", name
            )
            self.assertEqual(seen["tables"], 0, name)
            self.assertNotIn("Latest reading", seen["headings"], name)
            self.assertFalse(re.search(r"\d+(\.\d+)?\s*(degC|%RH)", seen["text"]), name)
            for value in ("23.7", "88", "SYN-R-0777"):
                self.assertNotIn(value, seen["text"], name)
        self.assertIn("Owner: the resident's consent owner.", self.text("withheld"))
        self.assertEqual(
            self.matrix["withheld"]["requests"],
            ["/api/cases/ZF-Q/sensors", "/api/cases/ZF-Q/sensor-drafts"],
        )

    def test_conflicting_readings_show_no_single_latest_value_and_one_alert(self) -> None:
        seen = self.matrix["conflict"]
        self.assertEqual(seen["status"], "Readings disagree")
        self.assertNotIn("Latest reading", seen["headings"])
        self.assertIn("Readings that disagree", seen["headings"])
        self.assertEqual(seen["alerts"], [["What we see", "Owner", "Next action"]])
        self.assertEqual(seen["alertCount"], "1")
        self.assertIn("Do not choose between them.", seen["text"])
        self.assertIn("Do not choose between conflicting readings.", seen["text"])
        both = self.matrix["conflict-stale"]
        self.assertEqual((both["alertCount"], len(both["alerts"])), ("2", 2))
        self.assertEqual(both["status"], "Readings disagree")

    def test_alerts_follow_the_badge_states_and_the_server_next_action_leads(self) -> None:
        fresh = self.matrix["fresh"]
        self.assertEqual(fresh["status"], "Recent reading (within 15 minutes)")
        self.assertEqual((fresh["alerts"], fresh["alertCount"]), ([], None))
        self.assertIn("No sensor alerts for this home.", fresh["text"])
        self.assertIn("Latest reading", fresh["headings"])
        stale = self.matrix["stale"]
        self.assertEqual(stale["status"], "Reading out of date (older than 15 minutes)")
        self.assertIn(
            "The latest reading is older than 15 minutes. Last reading 3 hours ago.", stale["text"]
        )
        self.assertIn(", out of date", stale["text"])
        old = self.matrix["offline-24h"]
        self.assertEqual(old["status"], "Sensor may be offline (no reading for over 24 hours)")
        self.assertIn("Sensor may be offline", old["headings"], "the alert hedges too")
        self.assertIn("No reading for over 24 hours. Last reading 3 days ago.", old["text"])
        self.assertEqual(old["alertCount"], "1")
        for name, wanted in (("fault", "Sensor fault"), ("out-of-range", "Reading out of range")):
            self.assertEqual(self.matrix[name]["status"], wanted, name)
            self.assertIn("Do not use this reading. See the alert above.", self.text(name), name)
        for name in ("no-readings", "withheld", "unavailable"):
            seen = self.matrix[name]
            self.assertEqual((seen["alerts"], seen["alertCount"]), ([], None), name)
        self.assertEqual(self.matrix["no-readings"]["status"], "No sensor readings recorded")
        self.assertNotIn("sensor-drafts", " ".join(self.matrix["unavailable"]["requests"]))

    def test_the_offline_rule_switches_one_second_after_the_server_value(self) -> None:
        seen = run_node(MODEL_JS, data={"offline": sensor_map.OFFLINE_SECONDS})
        self.assertEqual((seen["at"], seen["over"]), (["stale"], ["offline-24h"]))
        self.assertEqual(seen["fresh"], sensor_view.FRESH_SECONDS)
        self.assertEqual(seen["offline"], sensor_map.OFFLINE_SECONDS)
        self.assertIn(f"older than {sensor_view.FRESH_SECONDS // 60} minutes", seen["words"])
        self.assertIn(f"{sensor_map.OFFLINE_SECONDS // 3600} hours", sensor_map.LABELS["offline"])

    def test_tables_show_local_times_without_ids_and_widen_only_when_needed(self) -> None:
        fresh = self.matrix["fresh"]
        self.assertEqual(fresh["tables"], 3)
        self.assertEqual(
            fresh["headings"],
            [
                "Alerts for this home",
                "Latest reading",
                "Temperature and humidity over time",
                "Recent readings (up to 12)",
                "Around the first quality evidence record",
                "Before",
                "From then on",
                "Sensor review draft",
            ],
        )
        shown = fresh["text"].split("Reference numbers")[0]
        self.assertNotRegex(shown, r"SYN-R-\d{4}")
        self.assertNotRegex(shown, r"\d{4}-\d\d-\d\dT")
        shape = run_node(SHAPE_JS, data={"fresh": payload("fresh"), "mixed": payload("mixed")})
        self.assertEqual(
            shape["one"], ["Observed (UK time)", "Temperature (degC)", "Relative humidity (%RH)"]
        )
        self.assertEqual(shape["wide"][3:], ["Sensor", "Source"])
        self.assertEqual((shape["rowHeader"], shape["region"]), ("row", "region"))
        self.assertEqual(shape["caption"], "Recent readings, newest first")
        self.assertEqual(shape["name"], "Recent readings, newest first table")
        self.assertEqual(shape["time"], "2026-11-20T13:25:46Z")
        self.assertEqual(shape["firstCell"], "20 Nov, 13:25")

    def test_the_dual_axis_chart_has_a_text_alternative_and_respects_every_state(self) -> None:
        for name in ("fresh", "stale"):
            with self.subTest(state=name):
                text = self.text(name)
                self.assertIn("Temperature (degC)", text)
                self.assertIn("Relative humidity (%RH)", text)
                self.assertIn("different scales", text)
                self.assertIn("dashed line, squares, right axis", text)
                self.assertIn("The same readings are in the Recent readings table below.", text)
        self.assertNotIn("Out of date: these are the last readings", self.text("fresh"))
        self.assertIn("Out of date: these are the last readings", self.text("stale"))
        for name in (
            "no-readings",
            "withheld",
            "withheld-with-values",
            "unavailable",
            "not-linked",
            "service-down",
            "not-connected",
            "network",
            "restricted",
        ):
            with self.subTest(state=name):
                self.assertNotIn(
                    "Temperature and humidity over time", self.matrix[name]["headings"]
                )

    def test_no_internal_identifier_reaches_the_screen_in_any_state(self) -> None:
        banned = re.compile(r"(?i)\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b")
        fancy = re.compile("[\u2014\u2013\u2018\u2019\u201c\u201d\u2026]")
        for name, seen in self.matrix.items():
            everything = seen["text"] + " " + seen["attrs"]
            for word in FORBIDDEN:
                self.assertNotIn(word, everything, f"{name}: {word}")
            self.assertIsNone(fancy.search(everything), name)
            self.assertIsNone(banned.search(seen["text"]), name)
            self.assertFalse(seen["busy"], name)
        self.assertIn(
            "Dew point and mould risk are not kept for this home and are not estimated.",
            self.text("fresh"),
        )
        self.assertIn("Sensor review drafts are unavailable right now.", self.text("drafts-down"))

    def test_draft_section_and_about_details_are_plain(self) -> None:
        for wanted in (
            "Sensor review draft",
            sensor_review_draft.LABEL,
            "Not reviewed by a person yet.",
            "Rule and version details",
            "About these readings",
            "Reference numbers",
        ):
            self.assertIn(wanted, self.text("fresh"))
        self.assertIn(
            "No review draft exists for this home yet. Owner: a Quality Inspector. Next action:"
            " use the ordinary quality check.",
            self.text("stale"),
        )
        self.assertIn(
            "A saved draft failed its integrity check and is withheld. Owner: application support.",
            self.text("fault"),
        )
        self.assertNotIn("Sensor review draft", self.text("conflict"))


class AlertLabel(unittest.TestCase):
    def label(self, kind: str) -> dict[str, Any]:
        responses = {"/sensors": reply(payload(kind)), "/sensor-drafts": reply(drafts("none"))}
        data = {"tabs": tab_definitions(), "live": True}
        seen: dict[str, Any] = run_node(TABS_JS, responses=responses, data=data)
        return seen

    def test_label_counts_alerts_once_after_the_reply_and_never_says_loading(self) -> None:
        none = self.label("fresh")
        self.assertEqual(
            (none["before"], none["after"], none["writes"]), ("Home sensors",) * 2 + (0,)
        )
        one = self.label("stale")
        self.assertEqual(
            (one["before"], one["after"], one["writes"]),
            ("Home sensors", "Home sensors (1 alert)", 1),
        )
        self.assertEqual(self.label("conflict")["after"], "Home sensors (1 alert)")
        two = self.label("conflict-stale")
        self.assertEqual((two["after"], two["writes"]), ("Home sensors (2 alerts)", 1))
        for kind in ("fresh", "stale", "conflict-stale", "withheld", "no-readings", "unavailable"):
            self.assertNotIn("loading", self.label(kind)["after"].lower(), kind)

    def test_states_that_are_not_alerts_leave_the_label_alone(self) -> None:
        for kind in ("withheld", "no-readings", "unavailable"):
            seen = self.label(kind)
            self.assertEqual((seen["after"], seen["writes"]), ("Home sensors", 0), kind)

    def test_ai_label_is_shortened_when_the_count_is_unavailable(self) -> None:
        seen = run_node(AI_LABEL_JS)
        self.assertEqual(seen["label"], "AI assistance (count unavailable)")


class CopyTable(unittest.TestCase):
    """Every state a person can see has client wording, keyed by the server's badge states."""

    @staticmethod
    def entries(ops: str = OPS) -> dict[str, Any]:
        seen: dict[str, Any] = run_node(COPY_JS, ops=ops)
        return seen

    @staticmethod
    def needed() -> set[str]:
        badge_states = set(sensor_badges._FRESHNESS) | set(sensor_badges._HEALTH)
        for kind in ("fresh", "conflict", "fault", "out-of-range", "no-readings", "withheld"):
            badge_states |= {badge["state"] for badge in payload(kind)["badges"]}
        only_here = {"loading", "restricted", "not-connected", "not-linked", "service-down"}
        return badge_states | {"uncalibrated", "offline-24h"} | only_here

    def missing(self, ops: str) -> list[str]:
        return sorted(self.needed() - set(self.entries(ops)["keys"]))

    def test_every_badge_state_and_screen_state_has_an_entry(self) -> None:
        self.assertEqual(self.missing(OPS), [])
        for state in ("conflict", "stale", "offline"):
            mutated = OPS.replace(f"\n  {state}: {{", f"\n  {state}_removed: {{", 1)
            self.assertNotEqual(mutated, OPS, state)
            self.assertEqual(self.missing(mutated), [state], state)

    def test_every_alert_and_stop_names_an_owner_then_a_next_action(self) -> None:
        seen = self.entries()
        self.assertEqual(
            sorted(key for key, _ in seen["alerts"]),
            ["conflict", "fault", "offline-24h", "out_of_range", "stale"],
        )
        for key, message in seen["alerts"]:
            self.assertRegex(message, OWNER_NEXT, key)
        stops = ("restricted", "not-connected", "not-linked", "service-down", "withheld")
        for key in (*stops, "unavailable"):
            self.assertRegex(seen["states"][key]["notice"], OWNER_NEXT, key)

    def test_status_words_match_the_map_labels_so_one_home_reads_the_same(self) -> None:
        words = {key: state["words"] for key, state in self.entries()["states"].items()}
        labels = sensor_map.LABELS
        self.assertEqual(words["fresh"], labels["fresh"])
        self.assertEqual(words["stale"], labels["stale"])
        # The server's map label states the 24 hour case as fact; this tab hedges it like its alert.
        self.assertEqual(
            words["offline-24h"],
            labels["offline"].replace("Sensor offline", "Sensor may be offline"),
        )
        self.assertNotEqual(words["offline-24h"], labels["offline"])
        self.assertEqual(words["offline"], labels["no-readings"])
        self.assertEqual(words["withheld"], labels["consent-withheld"])
        self.assertEqual(words["unavailable"], labels["unavailable"])
        self.assertEqual(words["unknown"], labels["future-dated"])
        self.assertEqual(words["restricted"], labels["restricted"])
        self.assertEqual(
            words["not-connected"], labels["not-connected"].replace("deployment", "setup")
        )


class TabRow(unittest.TestCase):
    css = (WEB / "style.css").read_text()

    def test_narrow_screens_get_one_scrolling_row_and_wide_screens_keep_wrapping(self) -> None:
        self.assertIn(".case-tabs{display:flex;flex-wrap:wrap;", self.css)
        self.assertIn(".case-tabs-row{display:contents}", self.css)
        narrow = re.search(
            r"@media\(max-width:899px\)\{\.case-tabs\{padding:0\}"
            r"\.case-tabs-row\{([^}]*)\}\.case-tabs \[role=tab\]\{([^}]*)\}\}",
            self.css,
        )
        assert narrow
        for part in ("flex-wrap:nowrap", "overflow-x:auto"):
            self.assertIn(part, narrow.group(1))
        for part in ("flex:none", "overflow-wrap:normal"):
            self.assertIn(part, narrow.group(2))
        wide = self.css.index(".case-tabs-row{display:contents}")
        self.assertLess(wide, self.css.index(narrow.group(0)))

    def test_the_scrolling_row_is_inside_the_tab_list_so_the_list_never_scrolls(self) -> None:
        shown = run_node(TABS_JS, data={"tabs": tab_definitions()})
        self.assertEqual(shown["rows"], ["case-tabs-row"])
        self.assertEqual((shown["inRow"], shown["role"]), (10, "tablist"))


if __name__ == "__main__":
    unittest.main()
