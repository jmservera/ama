"""Quality decisions: every field is labelled and refusals show inside the record.

The shipped ops.js runs in a small Node DOM, as test_case_journey does. These are source
and behaviour checks only; the rendered layout is checked by the browser runs.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

DOM = r"""
const assert = require("node:assert/strict");
class Node {
  constructor(tag = "#text", text = "") {
    this.tagName = tag.toUpperCase(); this.nodeType = 1; this.attrs = {}; this.dataset = {};
    this.children = []; this.events = {}; this._text = text; this.checked = false;
    this.disabled = false; this.hidden = false; this.className = "";
  }
  append(...kids) {
    kids.forEach(k => {
      assert.ok(k && k.nodeType, "append takes nodes, as the real DOM does");
      this.children.push(k); k.parentElement = this;
    });
  }
  replaceChildren(...kids) {this.children = []; this.append(...kids);}
  setAttribute(name, value) {
    this.attrs[name] = String(value);
    if (name.startsWith("data-")) this.dataset[name.slice(5).replace(/-([a-z])/g,
      (_, c) => c.toUpperCase())] = String(value);
    if (name === "hidden") this.hidden = true;
  }
  getAttribute(name) {return this.attrs[name] ?? null;}
  hasAttribute(name) {return name in this.attrs;}
  removeAttribute(name) {
    delete this.attrs[name];
    if (name === "data-case-dirty") delete this.dataset.caseDirty;
  }
  get id() {return this.attrs.id;}
  get name() {return this.attrs.name;}
  get type() {return this.attrs.type || (this.tagName === "TEXTAREA" ? "textarea" : "text");}
  get value() {return this._value ?? "";}
  set value(value) {this._value = value;}
  get textContent() {return this._text + this.children.map(k => k.textContent ?? k).join("");}
  set textContent(value) {this._text = value; this.children = [];}
  all() {return this.children.filter(k => k.nodeType).flatMap(k => [k, ...k.all()]);}
  matches(selector) {
    if (selector.startsWith("#")) return this.id === selector.slice(1);
    if (selector.startsWith("[")) {
      const [, name, value] = selector.match(/^\[([^=\]]+)(?:="([^"]*)")?\]/);
      return this.hasAttribute(name) && (value === undefined || this.getAttribute(name) === value);
    }
    return this.tagName === selector.toUpperCase();
  }
  querySelectorAll(selector) {
    return this.all().filter(k => selector.split(",").some(s => k.matches(s.trim())));
  }
  closest(selector) {
    if (selector.split(",").some(s => this.matches(s.trim()))) return this;
    return this.parentElement?.closest(selector) || null;
  }
  addEventListener(name, fn) {this.events[name] = fn;}
  focus() {document.activeElement = this;}
}
const app = new Node("main");
const document = {activeElement: null, createElement: tag => new Node(tag),
  createTextNode: text => new Node("#text", text),
  getElementById: id => app.all().find(node => node.attrs.id === id) ?? null};
const window = {confirm: () => true};
let caseSession = null, me, session, lists, calls, refreshErrors;
const fmtDate = value => value;
let outcome = () => Promise.resolve({});
const api = async path => path === "/api/checklists" ? lists : {};
const post = (id, name, body) => {calls.push({id, name, body}); return outcome();};
let refresh = async fn => {
  try {await fn(); return true;} catch (error) {refreshErrors.push(error); return false;}
};
const all = (root, tag) => root.all().filter(node => node.tagName === tag.toUpperCase());
const byId = id => document.getElementById(id);
const labelOf = control =>
  all(app, "label").find(l => l.attrs.for === control.attrs.id)?.textContent;
const cards = panel => all(panel, "li").filter(li => li.className.includes("decision-item"));
const errorsIn = root => all(root, "p").filter(p => p.className.includes("field-error"));
const submit = form => form.events.submit({preventDefault() {}});
const settle = () => new Promise(resolve => setTimeout(resolve, 0));
const record = (state, over = {}) => Object.assign({
  measure: `Measure ${state}`, state, source: "Provider submission",
  submitted_by: "Northern Facade Systems Ltd", checklist_version: "QC-LOFT v1",
  evidence_version: 1, aftercare: [], defect: null,
  items: [{label: "Depth measured and photo taken", evidence: "Photo reference SYN-PH-1"}]}, over);
const defect = {description: "No commissioning sheet", reason: "Flow record is missing",
  owner: "Northern Facade Systems Ltd"};
const sixStates = () => [
  record("Superseded", {superseded_by: 1, prior_acceptance: {accepted_by: "Quinn Inspector"}}),
  record("Submitted"),
  record("Returned", {defect}),
  record("Fixed, awaiting reinspection",
    {defect: {...defect, remediation_evidence: "Duct isolator fitted"}}),
  record("Accepted", {accepted_by: "Quinn Inspector"}),
  record("Handed over", {accepted_by: "Quinn Inspector",
    handover: {by: "Quinn Inspector", note: "Guarantee pack"},
    aftercare: [{at: "2026-11-20", by: "Sam Example", note: "Shown the display"}]}),
];
const caseWith = (quality, closed = false) =>
  ({closed, measures: "Loft insulation, Solar panels", quality});
const render = async (c, role = "Quality Inspector") => {
  me = {user: {role}};
  calls = []; refreshErrors = []; outcome = () => Promise.resolve({});
  lists = {General: {version: "QC-GEN v1",
    items: ["Work matches the agreed scope", "Area left clean and safe"]}};
  session = {pendingFields: new Map()};
  caseSession = session;
  app.children = [];
  const panel = qualityPanel(c, "SYN", refresh, [], session);
  app.append(panel);
  await settle();
  return panel;
};
"""


def shipped_helpers() -> str:
    source = (WEB / "app.js").read_text()
    shipped_h = re.search(r"^function h\(.*?^\}\n", source, re.S | re.M)
    assert shipped_h is not None, "app.js no longer defines h()"
    draft_keys = source.split("function caseFieldEntries", 1)[1]
    draft_keys = draft_keys.split('app.addEventListener("input"', 1)[0]
    return shipped_h.group(0) + "function caseFieldEntries" + draft_keys


def run(body: str) -> None:
    ending = (
        'console.log("PASS");\n})().catch(error => {console.error(error); process.exitCode = 1;});'
    )
    script = (
        DOM
        + shipped_helpers()
        + (WEB / "fields.js").read_text()
        + (WEB / "ops.js").read_text()
        + "\n(async () => {\n"
        + body
        + "\n"
        + ending
        + "\n"
    )
    result = subprocess.run(["node", "-"], input=script, text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "PASS" in result.stdout, result.stdout


class QualityDecisions(unittest.TestCase):
    def test_every_control_has_a_visible_label_and_no_hidden_name_only(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const tags = ["INPUT", "SELECT", "TEXTAREA"];
const controls = panel.all().filter(node => tags.includes(node.tagName));
assert.ok(controls.length >= 12, controls.length);
for (const control of controls) {
  const label = labelOf(control);
  assert.ok(control.attrs.id, "a control has no id");
  assert.ok(label && label.trim().length > 0, `no visible label for ${control.attrs.id}`);
  assert.equal(control.attrs["aria-label"], undefined, control.attrs.id);
}
""")

    def test_accept_and_return_are_separate_fieldsets_with_their_own_fields(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const sets = all(cards(panel)[1], "fieldset");
assert.deepEqual(sets.map(set => all(set, "legend")[0].textContent),
  ["Accept this work", "Return with a defect"]);
const accept = all(sets[0], "input"), back = all(sets[1], "input");
assert.equal(accept.length, 1);
assert.equal(labelOf(accept[0]), "Note (optional)");
assert.equal(back.length, 3);
assert.deepEqual(back.map(labelOf), ["Why you are returning it (required)",
  "What the defect is (required)", "Who will put it right (required)"]);
assert.equal(new Set([...accept, ...back].map(field => field.name)).size, 4);
assert.equal(accept[0].name, "quality-note-1");
assert.deepEqual(all(sets[0], "button").map(b => b.className), [""]);
assert.deepEqual(all(sets[1], "button").map(b => b.className), ["alt"]);
""")

    def test_return_with_empty_boxes_sends_nothing_and_focuses_the_first(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const form = all(cards(panel)[1], "form")[1];
const [reason, what, who] = all(form, "input");
await submit(form);
assert.equal(calls.length, 0);
const errors = errorsIn(form);
assert.deepEqual(errors.map(error => error.textContent), ["Say why you are returning it.",
  "Say what the defect is.", "Say who will put it right."]);
assert.ok(errors.every((error, n) =>
  !error.hidden && error.parentElement === [reason, what, who][n].parentElement));
assert.equal(document.activeElement, reason);
assert.equal(reason.attrs["aria-invalid"], "true");
reason.value = "Flow temperature record is missing"; reason.events.input();
await submit(form);
assert.equal(calls.length, 0);
assert.equal(reason.attrs["aria-invalid"], undefined);
assert.equal(document.activeElement, what);
what.value = "No commissioning sheet"; who.value = "Northern Facade Systems Ltd";
await submit(form);
assert.deepEqual(calls.map(call => [call.name, call.body]), [["quality-return", {
  index: 1, reason: "Flow temperature record is missing",
  defect: "No commissioning sheet", owner: "Northern Facade Systems Ltd"}]]);
""")

    def test_refused_accept_shows_the_servers_reasons_inside_the_record(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const reason = "Resident scope is unknown. Owner: Resident Liaison Officer. "
  + "Next action: bind the work to its measure and current scope.";
outcome = () => Promise.reject(
  Object.assign(new Error("Not ready yet."), {status: 409, reasons: [reason]}));
await submit(all(cards(panel)[1], "form")[0]);
const feedback = byId("quality-feedback-1");
assert.equal(feedback.textContent, reason);
assert.equal(document.activeElement, feedback);
assert.ok(!panel.textContent.includes("follow the advice above"));
assert.equal(refreshErrors.length, 1);
outcome = () => Promise.reject(
  Object.assign(new Error("Someone independent must accept this work."), {status: 403}));
await submit(all(cards(panel)[1], "form")[0]);
assert.match(feedback.textContent,
  /^Someone independent must accept this work\. Owner: .+\. Next action: /);
""")

    def test_fixed_work_never_submits_on_enter_and_each_button_sends_its_own_result(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const forms = all(cards(panel)[3], "form");
assert.equal(forms.length, 1);
assert.deepEqual(all(forms[0], "button").map(b => b.attrs.type), ["button", "button"]);
let prevented = false;
await forms[0].events.submit({preventDefault() {prevented = true;}});
assert.ok(prevented);
assert.equal(calls.length, 0);
const [accept, notRight] = all(forms[0], "button");
all(forms[0], "input")[0].value = "Fan still rattles";
await accept.events.click();
await notRight.events.click();
assert.deepEqual(calls.map(call => call.body), [
  {index: 3, result: "pass", note: "Fan still rattles"},
  {index: 3, result: "fail", note: "Fan still rattles"}]);
assert.match(all(forms[0], "p").at(-1).textContent,
  /returns to Northern Facade Systems Ltd with the same defect\.$/);
""")

    def test_names_ids_and_buttons_that_other_checks_rely_on_stay(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
assert.equal(panel.attrs.id, "quality");
const named = name => all(panel, "input").filter(field => field.name === name);
assert.equal(named("quality-note-1").length, 1);
assert.equal(named("quality-fixer-2").length, 1);
assert.equal(named("quality-note-2").length, 1);
const told = byId("told-4");
assert.equal(told.attrs.type, "checkbox");
assert.ok(labelOf(told).startsWith("The resident has been told"));
sixStates().forEach((_, n) => {
  const feedback = byId(`quality-feedback-${n}`);
  assert.equal(feedback.attrs.tabindex, "-1");
  assert.equal(feedback.attrs["aria-live"], "polite");
});
for (const id of ["q-measure", "q-by", "q-revision", "q-src", "q-i0", "q-i1"]) {
  assert.ok(byId(id), id);
}
const save = panel.querySelectorAll("[data-quality-save]");
assert.deepEqual(save.map(button => button.textContent), ["Save evidence"]);
assert.ok(!save[0].className.includes("alt"));
const returned = await render(caseWith([record("Returned", {defect})], true));
assert.equal(returned.querySelectorAll("button")[0].textContent,
  "Record that it has been put right");
""")

    def test_evidence_form_is_one_labelled_fieldset_with_a_primary_save(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const form = all(panel, "form").at(-1);
const sets = all(form, "fieldset");
assert.equal(all(sets[0], "legend")[0].textContent, "Record the evidence for a measure");
assert.deepEqual(["q-measure", "q-revision", "q-by", "q-src"].map(id => labelOf(byId(id))), [
  "Which measure (required)", "Scope revision (required)",
  "Who did the work or sent the evidence (required)",
  "Where the evidence came from (required)"]);
assert.equal(byId("q-revision-hint").textContent, "Find this number in the decision for this "
  + "measure on the Resident tab. Without it the work cannot be accepted.");
assert.equal(all(sets[1], "legend")[0].textContent,
  "Checklist QC-GEN v1: say what was seen for every check");
assert.equal(labelOf(byId("q-i0")), "Work matches the agreed scope");
assert.equal(byId("q-i0").attrs["data-label"], "Work matches the agreed scope");
""")

    def test_a_viewer_who_cannot_check_sees_owner_and_next_action_and_no_controls(self) -> None:
        run(r"""
const waiting = [record("Submitted"), record("Fixed, awaiting reinspection", {defect})];
const panel = await render(caseWith(waiting, true), "Resident Liaison Officer");
assert.equal(cards(panel).length, 2);
const sentence = "A Quality Inspector or a manager checks this work. Owner: a Quality "
  + "Inspector or a manager. Next action: ask one of them to check this work.";
for (const card of cards(panel)) {
  assert.ok(card.textContent.includes(sentence));
  for (const tag of ["form", "button", "input", "select", "textarea"]) {
    assert.equal(all(card, tag).length, 0, tag);
  }
}
""")

    def test_superseded_record_is_read_only_and_links_to_the_current_one(self) -> None:
        run(r"""
const panel = await render(caseWith(sixStates()));
const card = cards(panel)[0];
for (const tag of ["form", "button", "input", "select", "textarea"]) {
  assert.equal(all(card, tag).length, 0, tag);
}
assert.ok(card.textContent.includes("Historical record only. Use evidence record 2 for "
  + "current decisions. Previously accepted by Quinn Inspector."));
const link = all(card, "a")[0];
assert.equal(link.attrs.href, "#quality-record-1");
await link.events.click({preventDefault() {}});
assert.equal(document.activeElement, byId("quality-record-1"));
""")

    def test_success_shows_the_recorded_line_and_moves_focus_to_the_record(self) -> None:
        run(r"""
const c = caseWith(sixStates());
refresh = async fn => {
  await fn();
  c.quality[1] = record("Accepted", {accepted_by: "Quinn Inspector"});
  app.children = [];
  app.append(qualityPanel(c, "SYN", refresh, [], session));
  return true;
};
const panel = await render(c);
all(cards(panel)[1], "input")[0].value = "Checked all five items";
await submit(all(cards(panel)[1], "form")[0]);
assert.deepEqual(calls[0].body, {index: 1, result: "pass", note: "Checked all five items"});
const line = byId("quality-result");
assert.ok(!line.hidden);
assert.equal(line.textContent, "Recorded: Measure Submitted was accepted. "
  + "Next action: record the handover once the resident has been told.");
const heading = byId("quality-record-1");
assert.equal(document.activeElement, heading);
assert.equal(heading.attrs["aria-describedby"], "quality-result");
assert.equal(byId("quality-record-2").attrs["aria-describedby"], undefined);
""")

    def test_typed_text_survives_a_refresh_in_its_own_box_only(self) -> None:
        run(r"""
const c = caseWith(sixStates());
await render(c);
const keys = () => caseFieldEntries(app).map(entry => entry.key);
assert.equal(new Set(keys()).size, keys().length);
const type = (id, text) => {byId(id).value = text; byId(id).dataset.caseDirty = "true";};
type("quality-return-reason-1", "Flow temperature record is missing");
type("quality-fixer-2", "Northern Facade Systems Ltd");
type("quality-handover-note-4", "Guarantee pack");
const before = keys();
rememberCaseFields(session);
app.children = [];
app.append(qualityPanel(c, "SYN", refresh, [], session));
await settle();
restoreCaseFields([...session.pendingFields.values()]);
assert.deepEqual(keys(), before);
const filled = caseFieldEntries(app).filter(({field}) => field.value !== "")
  .map(({field}) => [field.attrs.id, field.value]);
assert.deepEqual(filled, [["quality-return-reason-1", "Flow temperature record is missing"],
  ["quality-fixer-2", "Northern Facade Systems Ltd"],
  ["quality-handover-note-4", "Guarantee pack"]]);
""")


class QualityLayout(unittest.TestCase):
    def test_decision_layout_is_desktop_first_and_keeps_the_launcher_clear(self) -> None:
        css = (WEB / "style.css").read_text()
        block = css.split("/* ux-batch:quality-decisions */", 1)[1].split("/* ux-batch:", 1)[0]
        columns = "grid-template-columns:minmax(16rem,1fr) minmax(20rem,2fr)"
        self.assertIn(f".decision-grid{{display:grid;{columns}", block)
        stacked = "@media(max-width:1199px){.decision-grid{grid-template-columns:minmax(0,1fr)}}"
        self.assertIn(stacked, block)
        rules = re.sub(r"\.decision-[a-z-]+\{[^}]*\}", "", block).replace("minmax", "")
        self.assertNotIn("min-width", rules)
        narrow = re.search(r"@media\(max-width:600px\)\{(.*)\}", block)
        self.assertIsNotNone(narrow)
        assert narrow is not None
        self.assertIn(".decision-actions button{width:100%}", narrow.group(1))
        self.assertIn(
            ".case-sections>.case-tab-panel{padding-bottom:calc(var(--sp-5) * 4)}", narrow.group(1)
        )


if __name__ == "__main__":
    unittest.main()
