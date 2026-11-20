"""App-wide staff workbench fixes from the UX review: labelled fields, check rows, page identity,
links and numbers, copy defects and the programme queue request.

The shipped scripts run in Node against a small DOM, with constructed synthetic values only. This is
not browser, assistive-technology or participant evidence.
"""

from __future__ import annotations

import functools
import http.server
import json
import subprocess
import threading
import unittest
from pathlib import Path
from typing import Any

from test_wcag_workbench_baseline_151 import extract_function, run_node_json

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None  # type: ignore[assignment]

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

DOM = r"""
class Text {
  constructor(data) {this.nodeType = 3; this.data = data;}
  get textContent() {return this.data;}
}
class Element {
  constructor(tag) {
    this.nodeType = 1; this.tagName = tag.toUpperCase(); this.attrs = {}; this.children = [];
    this.listeners = {}; this.checked = false; this.parentElement = null; this.dataset = {};
    const classes = name => [this.attrs.class, name].filter(Boolean).join(" ");
    this.classList = {add: name => this.setAttribute("class", classes(name)),
      toggle() {}, remove() {}};
    this.style = {setProperty() {}};
  }
  get id() {return this.attrs.id || "";}
  get value() {
    if (this.chosen !== undefined) return this.chosen;
    const first = this.tagName === "SELECT" && this.all().find(el => el.tagName === "OPTION");
    return first ? (first.attrs.value ?? first.textContent) : "";
  }
  set value(next) {this.chosen = next;}
  get hidden() {return "hidden" in this.attrs;}
  set hidden(on) {if (on) this.setAttribute("hidden", ""); else this.removeAttribute("hidden");}
  set className(value) {this.setAttribute("class", value);}
  get className() {return this.attrs.class || "";}
  get textContent() {return this.children.map(kid => kid.textContent).join("");}
  set textContent(value) {this.children = value === "" ? [] : [new Text(String(value))];}
  append(...kids) {
    kids.flat().forEach(kid => {this.children.push(kid); kid.parentElement = this;});
  }
  replaceChildren(...kids) {this.children = []; this.append(...kids);}
  insertBefore(kid, before) {
    const at = this.children.indexOf(before);
    this.children.splice(at < 0 ? this.children.length : at, 0, kid); kid.parentElement = this;
  }
  setAttribute(name, value) {this.attrs[name] = String(value);}
  getAttribute(name) {return name in this.attrs ? this.attrs[name] : null;}
  hasAttribute(name) {return name in this.attrs;}
  removeAttribute(name) {delete this.attrs[name];}
  all() {
    return this.children.filter(kid => kid.nodeType === 1).flatMap(kid => [kid, ...kid.all()]);
  }
  querySelector(tag) {return this.all().find(el => el.tagName === tag.toUpperCase()) || null;}
  addEventListener(type, fn) {(this.listeners[type] ||= []).push(fn);}
  async fire(type) {
    const event = {type, currentTarget: this, target: this, preventDefault() {}};
    for (const fn of this.listeners[type] || []) await fn(event);
  }
  focus() {document.activeElement = this;}
  contains(other) {return other === this || this.all().includes(other);}
  closest() {return null;}
}
const document = {
  activeElement: null, title: "",
  createElement: tag => new Element(tag), createElementNS: (ns, tag) => new Element(tag),
  createTextNode: text => new Text(text), addEventListener() {}, removeEventListener() {},
  querySelectorAll: () => [], getElementById: () => null,
};
document.body = new Element("body");
const byTag = (root, tag) => root.all().filter(el => el.tagName === tag.toUpperCase());
const byId = (root, id) => root.all().find(el => el.attrs.id === id);
const button = (root, name) => byTag(root, "button").find(el => el.textContent === name);
const labelFor = (root, control) =>
  byTag(root, "label").find(el => el.attrs.for === control.attrs.id);
const wrap = nodes => {
  const holder = new Element("main");
  holder.append(...[nodes].flat().filter(Boolean));
  return holder;
};
"""

ENABLED_STATUS = """{enabled: true, flag_on: true, dpia_recorded: true, consultation_recorded: true,
  notice_approved: true, requested: true, requested_by: "Pam",
  requested_role: "Retrofit Programme Manager", activated: true, activated_by: "Sam",
  activated_role: "Programme Support Officer", activated_at: "2026-11-19T09:00:00Z",
  acknowledged: true, activities: ["Case work", "Site visit"], notice: "Synthetic staff notice."}"""


def shipped(name: str) -> str:
    """The top-level function or arrow function `name` from app.js, cut by matching braces."""
    source = (WEB / "app.js").read_text()
    for prefix in (f"async function {name}(", f"function {name}(", f"const {name} = "):
        start = source.find(prefix)
        if start >= 0:
            break
    else:
        raise AssertionError(f"app.js no longer defines {name}")
    depth, index = 0, source.index("{", start)
    for end in range(index, len(source)):
        depth += source[end] == "{"
        depth -= source[end] == "}"
        if depth == 0:
            return source[start : end + 1] + (";\n" if prefix.startswith("const") else "\n")
    raise AssertionError(f"unbalanced braces in {name}")


def shipped_line(name: str) -> str:
    """The one-line top-level declaration `const name = ...;` from app.js."""
    for line in (WEB / "app.js").read_text().splitlines():
        if line.startswith(f"const {name} = "):
            return line + "\n"
    raise AssertionError(f"app.js no longer declares {name}")


def run(body: str, *sources: str) -> Any:
    """Run `body` (an async function body that returns JSON) after the DOM and the given sources."""
    script = (
        DOM
        + "\n".join(sources)
        + f"\n(async () => {{ const out = await (async () => {{ {body} }})();\n"
        + "console.log(JSON.stringify(out)); })()\n"
        + ".catch(error => { console.error(error); process.exit(1); });"
    )
    result = subprocess.run(["node", "-"], input=script, text=True, capture_output=True, timeout=60)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


H = shipped("h")
FIELDS = (WEB / "fields.js").read_text()
TIME = (WEB / "timecapture.js").read_text()
OPS = (WEB / "ops.js").read_text()
WIDGET = (WEB / "chat-widget.js").read_text()
INTAKE = (WEB / "staff-intake.js").read_text()

TIME_STUBS = (
    H
    + FIELDS
    + TIME
    + """
const calls = [];
let shown = [];
const me = {user: {role: "Resident Liaison Officer"}};
const isManager = () => false;
const show = (...nodes) => {shown = nodes.flat();};
const api = async (path, body) => {
  calls.push([path, body === undefined ? "GET" : "POST", body]);
  if (path === "/api/time/status") return STATUS;
  if (path === "/api/time/mine") return [];
  return {};
};
"""
).replace("STATUS", ENABLED_STATUS)


class TimeCaptureFields(unittest.TestCase):
    def test_case_reference_minutes_and_activity_each_have_a_visible_label_and_hint(self) -> None:
        out = run(
            """
await timeView();
const page = wrap(shown);
return ["time-case", "time-minutes", "time-activity"].map(id => {
  const control = byId(page, id);
  const label = labelFor(page, control);
  const hint = byId(page, `${id}-hint`);
  return {tag: control.tagName, label: label ? label.textContent : null,
    ariaLabel: control.getAttribute("aria-label"), hint: hint ? hint.textContent : null,
    describedBy: control.getAttribute("aria-describedby"),
    row: control.parentElement.parentElement.className};
});
""",
            TIME_STUBS,
        )
        self.assertEqual(
            [(row["tag"], row["label"]) for row in out],
            [
                ("INPUT", "Case reference (required)"),
                ("INPUT", "Minutes (required)"),
                ("SELECT", "Activity"),
            ],
        )
        self.assertEqual(
            [row["hint"] for row in out],
            [
                "Copy it from the case page, for example ZF-1.",
                "A whole number from 1 to 600.",
                None,
            ],
        )
        for row in out:
            self.assertIsNone(row["ariaLabel"], "the visible label now names the control")
            self.assertEqual(row["row"], "field-row")
        self.assertEqual(
            [row["describedBy"] for row in out][:2], ["time-case-hint", "time-minutes-hint"]
        )

    def test_empty_case_reference_or_minutes_fail_in_place_and_send_nothing(self) -> None:
        out = run(
            """
await timeView();
const page = wrap(shown);
const save = button(page, "Save");
const caseRef = byId(page, "time-case"), minutes = byId(page, "time-minutes");
const posted = () => calls.filter(call => call[1] === "POST").length;
const state = control => {
  const error = byId(page, control.id + "-error");
  return {invalid: control.getAttribute("aria-invalid"), error: error.textContent,
    described: control.getAttribute("aria-describedby"), shown: !error.hidden};
};
const result = {};

caseRef.value = ""; minutes.value = "15";
await save.fire("click");
result.noCase = {posted: posted(), focus: document.activeElement.id, ...state(caseRef),
  other: state(minutes)};

caseRef.value = "ZF-1"; minutes.value = "";
await save.fire("click");
result.noMinutes = {posted: posted(), focus: document.activeElement.id, ...state(minutes),
  other: state(caseRef)};

minutes.value = "abc";
await save.fire("click");
result.words = {posted: posted(), focus: document.activeElement.id};

caseRef.value = ""; minutes.value = "";
await save.fire("click");
result.both = {posted: posted(), focus: document.activeElement.id,
  caseShown: state(caseRef).shown, minutesShown: state(minutes).shown};

caseRef.value = "ZF-1"; minutes.value = "15";
await caseRef.fire("input");
result.typing = state(caseRef);
return result;
""",
            TIME_STUBS,
        )
        no_case, no_minutes = out["noCase"], out["noMinutes"]
        self.assertEqual((no_case["posted"], no_case["focus"]), (0, "time-case"))
        self.assertEqual(no_case["invalid"], "true")
        self.assertEqual(
            no_case["error"],
            "Enter the case reference, for example ZF-1. Owner: you. "
            "Next action: type it, then choose Save again.",
        )
        self.assertEqual(no_case["described"], "time-case-hint time-case-error")
        self.assertFalse(no_case["other"]["shown"])
        self.assertIsNone(no_case["other"]["invalid"])
        self.assertEqual((no_minutes["posted"], no_minutes["focus"]), (0, "time-minutes"))
        self.assertEqual(
            no_minutes["error"],
            "Enter the minutes as a whole number from 1 to 600. Owner: you. "
            "Next action: type it, then choose Save again.",
        )
        self.assertFalse(no_minutes["other"]["shown"], "the earlier problem is cleared")
        self.assertEqual(out["words"], {"posted": 0, "focus": "time-minutes"})
        self.assertEqual(out["both"]["focus"], "time-case")
        self.assertTrue(out["both"]["caseShown"] and out["both"]["minutesShown"])
        self.assertFalse(out["typing"]["shown"], "typing clears the message")
        self.assertIsNone(out["typing"]["invalid"])

    def test_a_complete_entry_goes_to_the_server_which_keeps_its_own_range_rules(self) -> None:
        out = run(
            """
await timeView();
const page = wrap(shown);
byId(page, "time-case").value = "ZF-1";
byId(page, "time-minutes").value = "0";
byId(page, "time-activity").value = "Site visit";
await button(page, "Save").fire("click");
return calls.filter(call => call[1] === "POST");
""",
            TIME_STUBS,
        )
        self.assertEqual(
            out,
            [["/api/time", "POST", {"case_id": "ZF-1", "minutes": "0", "activity": "Site visit"}]],
        )


class CapacityWorkOrderRow(unittest.TestCase):
    STUBS = (
        H
        + FIELDS
        + OPS
        + """
let shown = [];
const me = {user: {role: "Retrofit Programme Manager"}};
const isManager = () => true;
const show = (...nodes) => {shown = nodes.flat();};
const routeController = new AbortController();
const fmtDate = value => String(value);
const mutationNeedsHistory = () => false;
const order = {id: "WO-0001", version: 1, state: "Issued", contractor: "Test Ltd",
  address: "1 Test Street", issued_by: "Pam", scope: "Loft", appointments: [],
  appointment_control: {current_binding: null, status: "Not started", missing: [], date: null}};
const api = async path =>
  path.startsWith("/api/packages") ? {items: [], total: 0} : {items: [order], total: 1};
const actionsOf = page => byTag(page, "li")
  .find(li => li.textContent.startsWith("WO-0001, version 1"))
  .all().find(el => el.className === "work-order-actions");
"""
    )

    def test_note_outcome_and_bindings_have_visible_labels_with_hints(self) -> None:
        out = run(
            """
await capacityView();
const actions = actionsOf(wrap(shown));
return byTag(actions, "label").map(label => {
  const control = byId(actions, label.attrs.for);
  const hint = byId(actions, `${label.attrs.for}-hint`);
  return {text: label.textContent, tag: control.tagName,
    ariaLabel: control.getAttribute("aria-label"), hint: hint ? hint.textContent : null,
    described: control.getAttribute("aria-describedby")};
});
""",
            self.STUBS,
        )
        self.assertEqual(
            [(row["text"], row["tag"]) for row in out],
            [
                ("Note, date or reason for WO-0001", "INPUT"),
                ("Affected measures and scope revisions for WO-0001", "INPUT"),
                ("Appointment outcome for WO-0001", "SELECT"),
            ],
        )
        self.assertEqual(
            [row["hint"] for row in out],
            [
                "The buttons use it like this: Record appointment takes the date when the "
                "outcome is Booked; Record completion takes a note; New version takes the "
                "new scope; Withdraw takes the reason.",
                "Only for New version. Write Measure|revision pairs separated by semicolons, "
                "for example Loft insulation|2; Cavity wall insulation|1.",
                None,
            ],
        )
        for row in out:
            self.assertIsNone(row["ariaLabel"], row["text"])
        self.assertEqual(
            [row["described"] for row in out],
            ["order-note-WO-0001-hint", "order-bindings-WO-0001-hint", None],
        )

    def test_the_row_has_one_primary_button_and_keeps_every_button_name(self) -> None:
        out = run(
            """
await capacityView();
return byTag(actionsOf(wrap(shown)), "button").map(b => [b.textContent, b.className]);
""",
            self.STUBS,
        )
        self.assertEqual(
            out,
            [
                ["Record appointment (date for Booked)", ""],
                ["New version", "alt"],
                ["Record completion", "alt"],
                ["Withdraw (add the reason)", "alt"],
            ],
        )

    def test_new_package_fields_sit_in_field_blocks_for_the_width_rule(self) -> None:
        out = run(
            """
await capacityView();
const card = byTag(wrap(shown), "section").find(s => s.children[0].textContent === "New package");
const labels = byTag(card, "label");
return {count: labels.length, inField: labels.every(l => l.parentElement.className === "field"),
  perControl: labels.map(l => byId(card, l.attrs.for).parentElement === l.parentElement)};
""",
            self.STUBS,
        )
        self.assertEqual(out["count"], 6)
        self.assertTrue(out["inField"])
        self.assertTrue(all(out["perControl"]))


class ChatComposerLabels(unittest.TestCase):
    STUBS = "const window = {};\n" + WIDGET

    def composer(self, options: str) -> Any:
        return run(
            f"""
const ui = window.ChatWidget.create({{id: "employee-chat", title: "Employee assistant",
  questionLabel: "Your work question", skillLabel: "Agent skill", {options} resizable: true}});
const [entry, tools] = ui.form.children;
const names = el => el.children.map(
  kid => kid.tagName.toLowerCase() + (kid.attrs.for ? ":" + kid.attrs.for : ""));
const labels = byTag(ui.form, "label");
return {{entry: names(entry), tools: names(tools), labels: labels.map(
  l => [l.textContent, l.attrs.for, byId(ui.form, l.attrs.for).getAttribute("aria-label")])}};
""",
            self.STUBS,
        )

    def test_employee_composer_has_both_labels_above_the_controls_and_equal_aria_labels(
        self,
    ) -> None:
        out = self.composer("visibleLabels: true,")
        self.assertEqual(
            out["entry"][:4], ["div", "label:employee-chat-question", "textarea", "small"]
        )
        self.assertEqual(out["tools"][:2], ["label:employee-chat-skill", "select"])
        self.assertEqual(
            out["labels"],
            [
                ["Your work question", "employee-chat-question", "Your work question"],
                ["Agent skill", "employee-chat-skill", "Agent skill"],
            ],
        )

    def test_other_chat_surfaces_stay_as_they_are_until_they_ask_for_labels(self) -> None:
        out = self.composer("")
        self.assertEqual(out["labels"], [])
        self.assertEqual(out["entry"][:3], ["div", "textarea", "small"])

    def test_the_employee_chat_asks_for_the_labels(self) -> None:
        chat = (WEB / "chat.js").read_text()
        self.assertIn(
            'questionLabel: "Your work question", skillLabel: "Agent skill", visibleLabels: true,',
            chat,
        )


INTAKE_STUBS = """
let screen;
const registerRoleScreen = s => { screen = s; };
const screenStamp = String;
const screenPanel = (title, ...kids) => h("section", {}, title, ...kids);
const screenFields = rows => h("dl", {}, rows);
const screenTable = (title, head, rows) => h("table", {}, title, head, rows);
const FormData = class {};
const routeController = {};
const roleScreensView = async () => {};
const api = async () => ({});
const checklist = {version: "C1", items: ["Depth checked"]};
const ORDER = {
  pack: {scope: "Loft", scope_version: 1, design_version: "D1", access: "Key safe",
    named_contact: "Ann", state: "Committed", ready: true, measures: ["Loft insulation"],
    checklists: {"Loft insulation": checklist}, pack_digest: "digest"},
  receipts: [], recovery: [], escalations: [], escalation_options: {},
  escalation: {owner: "Pam", role: "Retrofit Programme Manager", contact: "pam@example.test",
    contract_instruction: false, note: "Advice only."},
  boundaries: {acceptance: "Not acceptance.", consent: "Not consent."},
};
const RECEIPT = {record: "R1", capture_ref: "SYN-1", measure: "Loft insulation",
  checklist_version: "C1", confirmed_by: "Wren", recorded_by: "Sam", mode: "online",
  captured_at: "2026-11-19T09:00:00Z", status: "Submitted", quality_state: "Submitted",
  acknowledgement: null, accepted: false, corrections: [],
  review: {state: "Waiting", you_may_review: false, blocker: "Not yet."},
  original_notes: {"Depth checked": "Ok"}};
const render = (...receipts) => wrap(screen.render({id: "ZF-3"},
  {details: [{id: "WO-0001", data: {...ORDER, receipts}}]}));
"""


class StaffIntakeFields(unittest.TestCase):
    def test_each_hint_is_linked_to_its_control_and_uses_the_field_hint_style(self) -> None:
        out = run(
            """
const page = render();
const fields = byTag(page, "div").filter(el => el.className === "field");
const withHint = fields.filter(f => f.children.some(kid => kid.className === "field-hint"));
return {hintClasses: byTag(page, "p").map(p => p.className).filter(name => /hint/.test(name)),
  linked: withHint.map(f => {
    const [label, hint, control] = f.children;
    return [label.tagName, hint.tagName, hint.textContent,
      control.attrs["aria-describedby"] === hint.attrs.id, label.attrs.for === control.attrs.id];
  })};
""",
            H,
            FIELDS,
            INTAKE_STUBS,
            INTAKE,
        )
        self.assertEqual(out["hintClasses"], ["field-hint", "field-hint"])
        self.assertEqual(
            sorted(row[2] for row in out["linked"]),
            [
                "A named staff member who will decide this, not a role.",
                "The person who did the work, not you.",
            ],
        )
        for row in out["linked"]:
            self.assertEqual(row[:2], ["LABEL", "P"])
            self.assertTrue(all(row[3:]), row)


class CheckRows(unittest.TestCase):
    def test_intake_checkboxes_keep_their_label_beside_the_box(self) -> None:
        out = run(
            """
const page = render(RECEIPT);
return byTag(page, "input").filter(el => el.attrs.type === "checkbox").map(box => {
  const row = box.parentElement;
  const next = row.children[row.children.indexOf(box) + 1];
  return [box.id, row.className, next.tagName, next.attrs.for, next.textContent];
});
""",
            H,
            FIELDS,
            INTAKE_STUBS,
            INTAKE,
        )
        self.assertEqual(
            out,
            [
                [
                    "intake-confirmed",
                    "check",
                    "LABEL",
                    "intake-confirmed",
                    "The worker confirms these notes are their own",
                ],
                [
                    "intake-offline",
                    "check",
                    "LABEL",
                    "intake-offline",
                    "These were written down offline earlier",
                ],
                [
                    "fix-ok-R1",
                    "check",
                    "LABEL",
                    "fix-ok-R1",
                    "The worker confirms this correction is their own",
                ],
            ],
        )

    def test_overview_sensor_filter_is_a_check_row_that_keeps_its_hint_link(self) -> None:
        app_js = (WEB / "app.js").read_text()
        map_slice = extract_function(app_js, "const OV_TILES =", "async function coordinatorView(")
        out = run_node_json(
            r"""
const h = makeNode, svg = makeNode;
let disposeMapPanel = null;
const routeController = new AbortController();
const listState = {};
const me = { map: null };
const qs = (o) => new URLSearchParams(o).toString();
const document = {
  body: makeNode("body"), activeElement: null, getElementById: () => makeNode("div") };
const AsyncAction = { feedback: () => ({ finish() {} }) };
const api = async () => ({ mode: "clusters", total: 0, mapped: 0, unmapped: 0, items: [] });
const bounds = { getSouth: () => 53, getWest: () => -2, getNorth: () => 54, getEast: () => -1 };
const L = {
  map: () => ({ setView() { return this; }, on() {}, getBounds: () => bounds, getZoom: () => 10,
    fitBounds() {}, invalidateSize() {}, remove() {} }),
  tileLayer: () => ({ on() { return this; }, addTo() { return this; } }),
  layerGroup: () => ({ addTo() { return this; }, clearLayers() {} }),
  divIcon: (opts) => opts,
  marker: () => ({ on() { return this; }, addTo() { return this; },
    getElement: () => makeNode("button") }),
};
"""
            + (WEB / "fields.js").read_text()
            + map_slice
            + r"""
const filter = mapPanel().box.querySelector(".map-sensor-filter");
const row = filter.querySelector(".check");
const input = filter.querySelector("#map-sensor-alerts");
const part = (kid) => kid.tag + (kid.getAttribute("for") ? ":" + kid.getAttribute("for") : "")
  + (kid.getAttribute("id") ? "#" + kid.getAttribute("id") : "");
console.log(JSON.stringify({
  parts: row.children.map(part), label: row.children[1].textContent,
  hint: row.children[2].textContent, described: input.getAttribute("aria-describedby"),
  type: input.getAttribute("type"),
}));
"""
        )
        self.assertEqual(
            out["parts"],
            ["input#map-sensor-alerts", "label:map-sensor-alerts", "p#map-sensor-alerts-hint"],
        )
        self.assertEqual(out["label"], "Show only homes with stale or offline sensors")
        self.assertEqual(
            out["hint"], "Applies to individual homes. Zoom in until homes are shown one by one."
        )
        self.assertEqual((out["type"], out["described"]), ("checkbox", "map-sensor-alerts-hint"))


SHELL_STUBS = """
const app = new Element("main");
let me = null;
let renderedContext = null;
const location = {hash: "#/"};
"""


def title_stubs() -> str:
    return H + shipped_line("SITE_TITLE") + shipped("pageTitle") + shipped("show") + SHELL_STUBS


LOGIN_JS = """
let disposeMapPanel = null;
const workspaceReady = () => {};
const aiMode = {workflow: true};
let caseSession = null;
const fundingAi = {};
const workspaceStatus = new Element("p");
const clearPhoto = () => {};
let microsoftSignIn = false;
const api = async () => ({});
const start = async () => {};
const elements = {};
document.getElementById = id => (elements[id] ||= new Element("div"));
"""


def login_stubs() -> str:
    return title_stubs() + shipped_line("SIGN_IN_TITLE") + shipped("login") + LOGIN_JS


API_JS = """
let me = null;
let signedInBefore = false;
const routeController = new AbortController();
const pendingMutations = new Set();
const mutationKey = () => "key";
const GENERIC_READ_ERROR = "read", GENERIC_CHANGE_ERROR = "change";
const messages = [];
const login = message => messages.push(message);
const fetchReadRetrying = async () => ({status: 401, ok: false, json: async () => ({})});
const attempt = async () => {
  try { await api("/api/cases"); } catch (error) { return [error.status, error.message]; }
};
"""


def api_stubs() -> str:
    return H + shipped("api") + API_JS


LIST_JS = """
me = {user: {role: "Resident Liaison Officer", code: "RLO"}, staff: [],
  work_queues: {version: "work-queues-1", default: {view: "mine", sort: "urgent"},
    definitions: [], status: "Status.", clock: "Clock."}};
let coordinatorOrigin = null, queueOrigin = "mine", briefingBox = null, resetFocus = false;
let searchTimer = 0;
const routeController = new AbortController();
const listState = {q: "", sort: "urgent", stage: "", area: "", wave: "", owner: "",
  queue: "", flag: ""};
const facets = {sorts: {urgent: "Most urgent first"}, stages: [], areas: [], waves: []};
const api = async path => path === "/api/facets"
  ? facets : {items: [], total: 0, next_cursor: null, policy_version: "p"};
const section = title => h("section", {}, h("h2", {}, title));
const aiBox = () => section("Today's briefing");
const pendingHandoffs = () => section("Handoffs waiting for you");
const priorityPanel = () => section("Priority suggestions");
const FLAGS = [];
const AsyncAction = {handler: fn => fn};
const workspaceStatus = new Element("p");
const queueEmptyExplanation = () => ({text: "No cases."});
const qs = () => "";
const shown = [];
const show = (...nodes) => shown.push(...nodes.flat());
"""


def list_stubs() -> str:
    return H + shipped("listView") + SHELL_STUBS + LIST_JS


class PageIdentity(unittest.TestCase):
    def test_the_tab_title_follows_the_page_heading(self) -> None:
        out = run(
            """
const titles = [];
for (const heading of ["My cases today", "Overview", "Capacity and work orders"]) {
  show(h("h1", {}, heading), h("p", {}, "Body."));
  titles.push(document.title);
}
show(h("p", {}, "Loading."));
titles.push(document.title);
return titles;
""",
            title_stubs(),
        )
        self.assertEqual(
            out,
            [
                "My cases today | Zava Forward",
                "Overview | Zava Forward",
                "Capacity and work orders | Zava Forward",
                "Zava Forward | Zava North Homes",
            ],
        )

    def test_signed_out_title_card_orientation_and_way_back(self) -> None:
        out = run(
            """
const read = message => {
  login(message);
  const card = app.children[0];
  return {title: document.title, h1: byTag(app, "h1")[0].textContent,
    orientation: card.children[1].textContent,
    links: byTag(card, "a").map(a => [a.attrs.href, a.textContent]),
    alert: byTag(card, "p").find(p => p.attrs.role === "alert").textContent};
};
const plain = read("");
const ended = read("Your session has ended. Sign in again.");
microsoftSignIn = true;
login("");
return {plain, ended, microsoft: document.title};
""",
            login_stubs(),
        )
        orientation = (
            "Zava Forward is the staff workbench for the retrofit programme. "
            "This is a demonstration with synthetic data."
        )
        for state, alert in (("plain", ""), ("ended", "Your session has ended. Sign in again.")):
            card = out[state]
            self.assertEqual(card["title"], "Sign in | Zava Forward")
            self.assertEqual(card["h1"], "Sign in")
            self.assertEqual(card["orientation"], orientation)
            self.assertEqual(card["links"], [["/", "Back to the welcome page"]])
            self.assertEqual(card["alert"], alert)
        self.assertEqual(out["microsoft"], "Sign in | Zava Forward")

    def test_a_first_visit_shows_no_ended_session_but_a_mid_session_401_still_does(self) -> None:
        out = run(
            """
const first = await attempt();
me = {user: {}};
const mid = await attempt();
me = null;
signedInBefore = true;
const second = await attempt();
return {messages, first, mid, second};
""",
            api_stubs(),
        )
        ended = "Your session has ended. Sign in again."
        self.assertEqual(out["messages"], ["", ended, ended])
        for outcome in ("first", "mid", "second"):
            self.assertEqual(out[outcome], [401, ended], "the thrown error is unchanged")

    def test_signing_in_marks_that_a_session_existed(self) -> None:
        start = shipped("start")
        self.assertIn("signedInBefore = true;", start)
        self.assertLess(start.index('api("/api/me")'), start.index("signedInBefore = true;"))

    def test_list_views_put_the_page_heading_before_the_filters_and_panels(self) -> None:
        out = run(
            """
const result = {};
for (const view of ["mine", "all"]) {
  shown.length = 0;
  await listView(view);
  const page = wrap(shown);
  result[view] = {order: page.children.map(el => el.className),
    headings: page.all().filter(el => /^H[1-6]$/.test(el.tagName))
      .map(el => [el.tagName, el.textContent])};
}
return result;
""",
            list_stubs(),
        )
        for view, title in (("mine", "My cases today"), ("all", "All open cases")):
            self.assertEqual(out[view]["order"], ["row between", "layout"])
            self.assertEqual(out[view]["headings"][0], ["H1", title])
        self.assertIn(["H2", "Today's briefing"], out["mine"]["headings"])
        self.assertIn(["H2", "Priority suggestions"], out["mine"]["headings"])

    def test_route_status_names_the_screens_that_had_no_scope(self) -> None:
        source = (WEB / "app.js").read_text()
        for text in (
            '"Spreadsheet check"',
            '"Coordinator flow"',
            '"Shared building context"',
            '"Versioned home case"',
        ):
            self.assertIn(text, source)
        self.assertEqual(source.count('"Case workspace"'), 1)

    def test_the_page_declares_a_theme_colour_and_the_logo_is_decorative(self) -> None:
        html = (WEB / "index.html").read_text()
        self.assertIn('<meta name="theme-color" content="#0b5d6b">', html)
        self.assertIn('<img class="zava-logo" src="/zava-logo.png" alt="">', html)


LINKS_PAGE = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<link rel="stylesheet" href="/style.css"></head><body><main id="app">
<p><a id="plain" href="#x">Plain link</a></p>
<p><a id="button" class="btn" href="#x">Button link</a></p>
<table><tbody><tr><th scope="row"><a id="rowhead" href="#x">Row</a></th>
<td id="figure">1,200</td></tr></tbody></table>
<ul class="plainlist"><li><a id="maplist" href="#x">Map</a></li></ul>
<details open><summary>Sources</summary>
<ul><li><a id="source" href="#x">Source</a></li></ul></details>
<section class="screen-evidence">
<p><a id="download" class="btn alt" href="#x">Download</a></p></section>
<nav class="screen-links"><a id="jump" href="#x">Jump to a section</a></nav>
<div class="coordinator leaflet-container"><a id="attribution" href="#x">Leaflet</a></div>
</main></body></html>"""
LINK_MEASURES = """() => {
  const probe = document.createElement('i');
  probe.style.color = 'var(--brand-d)';
  document.body.append(probe);
  const brand = getComputedStyle(probe).color;
  const summary = document.querySelector('details > summary');
  const tall = id => document.getElementById(id).getBoundingClientRect().height;
  const style = id => getComputedStyle(document.getElementById(id));
  const buttonMin = (() => {
    const b = document.createElement('button'); document.body.append(b);
    return parseFloat(getComputedStyle(b).minHeight);
  })();
  return {brand, plain: style('plain').color, button: style('button').color,
    compact: parseFloat(getComputedStyle(summary).minHeight), buttonMin,
    rowhead: tall('rowhead'), maplist: tall('maplist'), source: tall('source'),
    download: tall('download'), jump: tall('jump'), attribution: style('attribution').display,
    figure: style('figure').fontVariantNumeric, mainBottom: style('app').paddingBottom};
}"""


class LinksTargetsAndNumbers(unittest.TestCase):
    """The real style.css in Chromium: link colour, target size and tabular figures."""

    def measures(self) -> dict[str, Any]:
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self) -> None:
                if self.path != "/links.html":
                    return super().do_GET()
                body = LINKS_PAGE.encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args: object) -> None:
                return

        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(Handler, directory=str(WEB))
        )
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as playwright:
                try:
                    browser = playwright.chromium.launch()
                except Exception as error:  # pragma: no cover
                    self.skipTest(f"chromium unavailable: {error}")
                page = browser.new_page(viewport={"width": 1280, "height": 800})
                page.goto(f"http://127.0.0.1:{server.server_address[1]}/links.html")
                measured: dict[str, Any] = page.evaluate(LINK_MEASURES)
                browser.close()
                return measured
        finally:
            server.shutdown()

    @unittest.skipIf(sync_playwright is None, "playwright is not installed")
    def test_links_use_the_brand_token_and_small_targets_reach_the_compact_minimum(self) -> None:
        out = self.measures()
        self.assertEqual(out["plain"], out["brand"])
        self.assertNotEqual(out["button"], out["brand"], "a button link keeps its own colours")
        for name in ("rowhead", "maplist", "source"):
            self.assertGreaterEqual(out[name], out["compact"], name)
        self.assertGreaterEqual(out["download"], out["buttonMin"], "a button link keeps its height")
        self.assertGreaterEqual(out["jump"], out["buttonMin"], "the jump links keep their height")
        self.assertEqual(out["attribution"], "inline", "map attribution is left alone")

    @unittest.skipIf(sync_playwright is None, "playwright is not installed")
    def test_figures_line_up_and_the_page_ends_clear_of_the_chat_launcher(self) -> None:
        out = self.measures()
        self.assertEqual(out["figure"], "tabular-nums")
        self.assertEqual(out["mainBottom"], "80px")

    def test_the_new_rules_use_tokens_and_the_old_shrinking_rule_is_scoped(self) -> None:
        css = (WEB / "style.css").read_text()
        block = css[css.rindex("/* ux-batch:app-wide */") :]
        for raw in ("#", "rgb(", "rgba(", "transition"):
            self.assertNotIn(raw, block)
        self.assertIn("{color:var(--brand-d)}", block)
        self.assertIn(".screen-evidence p>a:only-child:not(.btn){", css)
        self.assertNotIn(".screen-evidence p>a:only-child{", css)


if __name__ == "__main__":
    unittest.main()
