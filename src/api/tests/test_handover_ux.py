"""The case handover card: the shipped app.js runs in a mini DOM; the held-back text is pinned."""

from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

from zava_forward.core import projection, taskqueues

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
APP = (WEB / "app.js").read_text()

# The words a person reads, written once. Anything the card says about who owns a step is here.
COPY = {
    "open_sender": (
        "You cannot offer this case yet. An offer to Miguel Garcia is waiting for an answer. "
        "Owner: Miguel Garcia to answer, or you to withdraw it. "
        "Next action: withdraw the offer first, then offer the case to someone else."
    ),
    "open_other": (
        "You cannot offer this case. Only Helen Marsden or a manager can offer or withdraw it. "
        "Owner: Helen Marsden. Next action: ask Helen Marsden or a manager."
    ),
    "accepted": (
        "You cannot offer this case yet. Miguel Garcia accepted it and the handover is not "
        "marked complete. Owner: Miguel Garcia. "
        "Next action: ask Miguel Garcia to record that the handover is complete."
    ),
    "accepted_by_you": (
        "You cannot offer this case yet. You accepted it and the handover is not marked "
        "complete. Owner: you."
    ),
    "closed": (
        "This case is closed, so it cannot be offered. Owner: a manager. "
        "Next action: ask a manager to reopen it."
    ),
    "not_owner": (
        "Only the case owner, Helen Marsden, or a manager can offer this case. "
        "Owner: Helen Marsden. Next action: ask Helen Marsden or a manager to offer it."
    ),
    "held": (
        "Held back for your role. Owner: Helen Marsden. "
        "Next action: ask Helen Marsden what they want you to do."
    ),
    "held_detail": (
        "Held back for your role. Owner: Helen Marsden. "
        "Next action: ask Helen Marsden for this detail."
    ),
    "stays": (
        "The case stays with Helen Marsden until Miguel accepts. "
        "You can withdraw the offer before then."
    ),
    "sent": "Offer sent to Miguel Garcia. The case stays with you until Miguel accepts.",
    "sent_elsewhere": (
        "Offer sent to Cassandra Dunn. The case stays with Helen Marsden until they accept."
    ),
    "withdrawn": "Offer withdrawn. The case stays with Helen Marsden.",
    "accepted_message": (
        "You are now the owner of this case. Helen Marsden is no longer the owner."
    ),
    "if_you_accept": (
        "If you accept, you become the owner of this case and Helen Marsden stops being the owner."
    ),
    "accept_hint": "Where the handover was agreed. For example: Programme meeting 14 Oct.",
    "no_update_owner": (
        "No one named yet. Next action: ask the case lead to name one. "
        "No message is sent automatically."
    ),
    "chase": (
        "Aadi Kapoor: chase Miguel Garcia, or withdraw the offer and offer the case to someone else"
    ),
}

# A small DOM in the style of test_case_journey, with the few extras this card needs.
DOM = r"""
process.env.TZ = "UTC";
const assert = require("node:assert/strict");
class Node {
  constructor(tag = "#text", text = "") {
    this.tagName = tag.toUpperCase(); this.nodeType = 1; this.attrs = {};
    this.dataset = {}; this.children = []; this.events = {}; this._text = text;
    this.writes = 0; this.checked = false; this.disabled = false;
    this.classList = {add() {}, toggle() {}};
  }
  append(...kids) {
    kids.flat().forEach(k => {this.children.push(k); if (k.nodeType) k.parentElement = this;});
  }
  setAttribute(name, value) {
    this.attrs[name] = String(value);
    if (name.startsWith("data-")) this.dataset[name.slice(5).replace(/-([a-z])/g,
      (_, c) => c.toUpperCase())] = String(value);
    if (["disabled", "hidden", "checked"].includes(name)) this[name] = true;
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
  get value() {return this._value ?? (this.tagName === "TEXTAREA" ? this.textContent : "");}
  set value(value) {this._value = value;}
  get textContent() {return this._text + this.children.map(k => k.textContent ?? k).join("");}
  set textContent(value) {this.writes++; this._text = value; this.children = [];}
  all() {return this.children.filter(k => k.nodeType).flatMap(k => [k, ...k.all()]);}
  matches(selector) {
    if (selector.startsWith("#")) return this.id === selector.slice(1);
    if (selector.startsWith(".")) return (this.className || "").split(" ")
      .includes(selector.slice(1).split("[")[0]) && (!selector.includes("[")
        || this.matches(selector.slice(selector.indexOf("["))));
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
  closest(selector) {
    if (selector.split(",").some(s => this.matches(s.trim()))) return this;
    return this.parentElement?.closest(selector) || null;
  }
  addEventListener(name, fn) {this.events[name] = fn;}
  focus() {document.activeElement = this;}
}
Node.prototype.replaceChildren = function (...kids) {
  this.children.forEach(kid => {if (kid.nodeType) kid.parentElement = null;});
  this.children = [];
  this._text = "";
  this.append(...kids);
};
Object.defineProperty(Node.prototype, "isConnected", {get() {
  let node = this;
  while (node.parentElement) node = node.parentElement;
  return node === app;
}});
const document = {
  createElement: tag => new Node(tag),
  createTextNode: text => new Node("#text", text),
};
const app = new Node("main");
const window = {addEventListener() {}};
const hasUnsavedChanges = () => false;
let caseSession = null;
"""

# The case, the viewer and the server, in the smallest form the card reads.
WORLD = r"""
const COPY = __COPY__;
const HELD = __HELD__;
const staff = [
  {code: "RLO-01", name: "Helen Marsden", email: "helen@example.test",
    role: "Resident Liaison Officer"},
  {code: "RC-01", name: "Miguel Garcia", email: "miguel@example.test",
    role: "Retrofit Coordinator"},
  {code: "PM-01", name: "Aadi Kapoor", email: "aadi@example.test",
    role: "Retrofit Programme Manager"},
  {code: "BSL-01", name: "Cassandra Dunn", email: "cassandra@example.test",
    role: "Building Safety Liaison"},
  {code: "CON-01", name: "Carl Contractor", email: "carl@example.test", role: "Contractor"},
];
let me, c, card, failNext = null, serverState = () => {};
const requests = [], failures = [];
const viewer = code => {me = {user: {...staff.find(s => s.code === code)}, staff};};
const suggestion = (code, reasons) => {
  const s = staff.find(item => item.code === code);
  return {email: s.email, name: s.name, role: s.role, reasons};
};
const base = () => ({
  id: "ZF-5", closed: false, owner: "Helen Marsden", owner_code: "RLO-01", resident_update: null,
  handoff_history: [],
  suggestions: [
    suggestion("RC-01", ["Can pick up anything when needed", "0 open cases (team average 1)"]),
    suggestion("PM-01", ["Can pick up anything when needed"]),
    suggestion("BSL-01", ["0 open cases (team average 1)"]),
  ],
});
const offered = (state = "Offered", extra = {}) => ({
  state, from_code: "RLO-01", from_name: "Helen Marsden", to_code: "RC-01",
  to_name: "Miguel Garcia", to_role: "Retrofit Coordinator", offered_by: "Helen Marsden",
  offered_at: new Date(Date.now() - 3 * 864e5).toISOString(),
  note: "Covering while I am on leave", answer_note: "", due_at: null, urgency: "Routine",
  next_action: "Agree an access date with the resident", resident_update_owner: null,
  resident_update_due_at: null, status: "Sent", accountable_owner: "Helen Marsden",
  chase_owner: "Helen Marsden", ...extra,
});
const post = async (id, action, body) => {
  requests.push({id, action, body});
  if (failNext) {const error = failNext; failNext = null; throw error;}
  serverState(action, body);
};
const api = async path => {throw new Error(`api() must not be used here: ${path}`);};
const refresh = async (fn, submitted = []) => {
  try {await fn();} catch (error) {failures.push(error.message); return false;}
  mount();
  return true;
};
function mount() {
  card = handoffPanel(c, "ZF-5", refresh);
  app.replaceChildren(card);
  return card;
}
const textOf = node => node.textContent;
const buttonTexts = root => root.querySelectorAll("button").map(textOf);
const buttonIn = (root, name) => {
  const found = root.querySelectorAll("button").filter(node => node.textContent === name);
  assert.equal(found.length, 1, `${name} in ${JSON.stringify(buttonTexts(root))}`);
  return found[0];
};
const clickOn = node => node.events.click({preventDefault() {}});
const submitForm = form => form.events.submit({preventDefault() {}});
const labelledIn = (root, label) => {
  const named = root.querySelectorAll("label").filter(node => node.textContent === label);
  assert.equal(named.length, 1, `label ${label}`);
  const controls = root.querySelectorAll("input, select, textarea");
  const control = controls.find(node => node.id === named[0].attrs.for);
  assert.ok(control, `a control for ${label}`);
  return control;
};
const typeInto = (control, value) => {
  control.value = value;
  control.dataset.caseDirty = "true";
  if (control.events.input) control.events.input();
};
const shownErrors = root => root.querySelectorAll(".field-error")
  .filter(node => !node.hidden).map(textOf);
const fieldsOf = root => Object.fromEntries(root.querySelectorAll("dt").map(dt => {
  const row = dt.parentElement.children;
  return [dt.textContent, row[row.indexOf(dt) + 1].textContent];
}));
const session = () => ({id: "ZF-5", pendingFields: new Map()});
const asOwner = () => {viewer("RLO-01"); c = base(); caseSession = session();};
const asManager = () => {viewer("PM-01"); c = base(); caseSession = session();};
const asReceiver = () => {viewer("RC-01"); c = base(); caseSession = session();};
const fillRecord = (root, values) => {
  typeInto(labelledIn(root, "Source reference (required)"), values[0]);
  typeInto(labelledIn(root, "Source version (required)"), values[1]);
  typeInto(labelledIn(root, "Reason (required)"), values[2]);
};
const resultOf = root => root.querySelector(".handoff-result").querySelector("p").textContent;
"""


def shipped() -> str:
    helpers = "function h" + APP.split("function h", 1)[1].split("async function api", 1)[0]
    fields = (
        "function caseFieldEntries"
        + APP.split("function caseFieldEntries", 1)[1].split("function captureCaseFields", 1)[0]
    )
    handover = (
        "const recordedMissing"
        + APP.split("const recordedMissing", 1)[1].split("function hazardState", 1)[0]
    )
    manager = re.search(r"^const isManager = .*;$", APP, re.M)
    assert manager is not None
    return "\n".join([helpers, fields, manager.group(0), (WEB / "fields.js").read_text(), handover])


def run(body: str) -> None:
    world = WORLD.replace("__COPY__", json.dumps(COPY)).replace(
        "__HELD__", json.dumps(projection.NOTE_HELD)
    )
    script = "\n".join(
        [
            DOM,
            shipped(),
            world,
            "(async () => {",
            body,
            "console.log('PASS');",
            "})().catch(error => {console.error(error.stack || error); process.exitCode = 1;});",
        ]
    )
    result = subprocess.run(["node", "-"], input=script, text=True, capture_output=True, timeout=60)
    assert result.returncode == 0, result.stderr
    assert "PASS" in result.stdout, result.stdout


class OfferButtons(unittest.TestCase):
    def test_each_suggestion_has_one_named_button_that_opens_its_own_form(self) -> None:
        run(
            r"""
asManager();
mount();
const offers = buttonTexts(card).filter(name => name.startsWith("Offer this case to "));
assert.deepEqual(offers, ["Offer this case to Miguel Garcia", "Offer this case to Aadi Kapoor",
  "Offer this case to Cassandra Dunn"]);
assert.ok(!buttonTexts(card).some(name => /^Offer to /.test(name)), "old buttons are gone");
const names = card.querySelectorAll("strong");
assert.deepEqual(names.map(textOf), ["Miguel Garcia, Retrofit Coordinator",
  "Aadi Kapoor, Retrofit Programme Manager", "Cassandra Dunn, Building Safety Liaison"]);
assert.ok(names.every(node => node.closest("li")), "each name is an li strong");
assert.ok(card.querySelectorAll("h3").map(textOf).includes("Who could take this on"));

clickOn(buttonIn(card, "Offer this case to Miguel Garcia"));
const boxes = card.querySelectorAll(".handoff-offer");
assert.deepEqual(boxes.map(node => node.hidden), [false, true, true]);
const heading = boxes[0].querySelector("h4");
assert.equal(heading.textContent, "Offer this case to Miguel Garcia");
assert.equal(document.activeElement, heading);
assert.equal(buttonIn(boxes[0], "Send offer to Miguel Garcia").attrs.type, "submit");
buttonIn(boxes[0], "Cancel");
for (const label of ["What do you want Miguel to do? (optional)", "How urgent (optional)",
  "Due date (optional)", "Note for Miguel (optional)", "Source reference (required)",
  "Source version (required)", "Reason (required)"]) {
  labelledIn(boxes[0], label);
}
assert.ok(boxes[0].textContent.includes(COPY.stays));
assert.ok(boxes[0].textContent.includes("A date you choose. It is not an agreed deadline."));
"""
        )

    def test_sending_with_empty_required_fields_posts_nothing_and_names_each_field(self) -> None:
        run(
            r"""
asOwner();
mount();
clickOn(buttonIn(card, "Offer this case to Aadi Kapoor"));
const box = card.querySelectorAll(".handoff-offer")[1];
await submitForm(box.querySelector("form"));
assert.equal(requests.length, 0);
const messages = shownErrors(box);
assert.equal(messages.length, 3);
for (const message of messages) {
  assert.match(message,
    /Owner: you\. Next action: .*, then choose Send offer to Aadi Kapoor again\.$/);
}
for (const label of ["Source reference (required)", "Source version (required)",
  "Reason (required)"]) {
  const control = labelledIn(box, label);
  assert.equal(control.attrs["aria-invalid"], "true");
  const beside = control.parentElement.querySelectorAll(".field-error");
  assert.ok(beside.some(node => !node.hidden && node.textContent), `${label}: message beside`);
  assert.ok(control.attrs["aria-describedby"].includes(`${control.id}-error`));
}
const source = labelledIn(box, "Source reference (required)");
assert.equal(document.activeElement, source);
typeInto(source, "Capacity check on 14 Oct");
assert.equal(source.attrs["aria-invalid"], undefined);
"""
        )

    def test_a_valid_send_posts_the_offer_action_and_confirms_in_the_card(self) -> None:
        run(
            r"""
asOwner();
c.handoff_history = [{}, {}];
serverState = () => {c.handoff = offered();};
mount();
clickOn(buttonIn(card, "Offer this case to Miguel Garcia"));
const box = card.querySelectorAll(".handoff-offer")[0];
typeInto(labelledIn(box, "What do you want Miguel to do? (optional)"), "Agree an access date");
labelledIn(box, "How urgent (optional)").value = "Urgent";
labelledIn(box, "Due date (optional)").value = "2026-11-27T09:00";
typeInto(labelledIn(box, "Note for Miguel (optional)"), "Covering from Monday");
fillRecord(box, ["Capacity check on 14 Oct", "1", "I am on leave from Monday"]);
await submitForm(box.querySelector("form"));

assert.deepEqual(requests, [{id: "ZF-5", action: "offer-handoff", body: {
  source: "Capacity check on 14 Oct", source_version: "1", reason: "I am on leave from Monday",
  handoff_version: 2, to: "miguel@example.test", note: "Covering from Monday",
  next_action: "Agree an access date", urgency: "Urgent",
  due_at: new Date("2026-11-27T09:00").toISOString()}}]);
assert.deepEqual(failures, []);
const after = app.children[0];
const status = after.querySelector(".status-line");
assert.equal(status.textContent, "Offered to Miguel Garcia, waiting for an answer");
assert.equal(document.activeElement, status);
assert.equal(resultOf(after), COPY.sent);
assert.deepEqual(buttonTexts(after.querySelector(".handoff-result")),
  ["Withdraw the offer to Miguel Garcia"]);
const withdraws = buttonTexts(after).filter(name => name.startsWith("Withdraw the offer to"));
assert.equal(withdraws.length, 1);
assert.ok(!buttonTexts(after).some(name => name.startsWith("Offer this case to ")));
"""
        )

    def test_the_form_for_someone_not_listed_preselects_nobody_and_keeps_its_button(self) -> None:
        run(
            r"""
asManager();
serverState = () => {c.handoff = offered();};
mount();
const more = card.querySelectorAll("details").find(
  node => node.querySelector("summary").textContent === "Offer to someone who is not listed");
assert.ok(more && !more.hasAttribute("open"), "a closed disclosure");
const choice = labelledIn(more, "Offer to (required)");
const options = choice.children.filter(node => node.tagName === "OPTION");
assert.equal(options[0].textContent, "Choose a colleague");
assert.ok(options[0].disabled && options[0].hasAttribute("selected"));
assert.equal(options[0].attrs.value, "");
assert.equal(choice.value, "");
assert.ok(!options.some(node => /Carl Contractor|^Helen Marsden/.test(node.textContent)));

await submitForm(more.querySelector("form"));
assert.equal(requests.length, 0);
assert.equal(shownErrors(more)[0], "Choose a colleague. Owner: you. Next action: "
  + "choose who should take the case, then choose Offer the case again.");
assert.equal(document.activeElement, choice);
choice.value = "cassandra@example.test";
if (choice.events.input) choice.events.input();
fillRecord(more, ["Capacity check", "1", "On leave"]);
await submitForm(more.querySelector("form"));
assert.equal(requests.length, 1);
assert.equal(requests[0].action, "offer-handoff");
assert.equal(requests[0].body.to, "cassandra@example.test");
assert.equal(resultOf(app.children[0]), COPY.sent_elsewhere);
buttonIn(more, "Offer the case");
"""
        )

    def test_cancel_and_escape_close_the_form_and_return_to_the_persons_button(self) -> None:
        run(
            r"""
asOwner();
mount();
const miguel = buttonIn(card, "Offer this case to Miguel Garcia");
const aadi = buttonIn(card, "Offer this case to Aadi Kapoor");
const boxes = card.querySelectorAll(".handoff-offer");
clickOn(miguel);
clickOn(aadi);
assert.deepEqual(boxes.map(node => node.hidden), [true, false, true], "an untouched form closes");
typeInto(labelledIn(boxes[1], "Reason (required)"), "On leave");
const cassandra = buttonIn(card, "Offer this case to Cassandra Dunn");
clickOn(cassandra);
assert.deepEqual(boxes.map(node => node.hidden), [true, false, false], "a typed-in form stays");
caseSession.pendingFields.set("ho-offer-1-reason:0", {});
clickOn(buttonIn(boxes[1], "Cancel"));
assert.equal(boxes[1].hidden, true);
assert.equal(boxes[1].children.length, 0);
assert.equal(document.activeElement, aadi);
assert.equal(caseSession.pendingFields.size, 0, "discarded typing is not kept");
boxes[2].events.keydown({key: "Escape"});
assert.equal(boxes[2].hidden, true);
assert.equal(document.activeElement, cassandra);
"""
        )

    def test_typing_kept_across_a_reload_reopens_that_persons_form(self) -> None:
        run(
            r"""
asOwner();
const key = "ho-offer-1-reason:0";
caseSession.pendingFields.set(key, {key, value: "On leave", checked: false});
mount();
const boxes = card.querySelectorAll(".handoff-offer");
assert.deepEqual(boxes.map(node => node.hidden), [true, false, true]);
labelledIn(boxes[1], "Reason (required)");
c.handoff = offered();
mount();
assert.equal(card.querySelectorAll(".handoff-offer").length, 0, "no form while an offer is open");
"""
        )

    def test_a_refusal_shows_inside_the_form_and_keeps_what_was_typed(self) -> None:
        run(
            r"""
asOwner();
mount();
clickOn(buttonIn(card, "Offer this case to Miguel Garcia"));
const box = card.querySelectorAll(".handoff-offer")[0];
fillRecord(box, ["Capacity check", "1", "On leave"]);
const refusal = "The handoff changed. Reload and check the current offer.";
failNext = Object.assign(new Error(refusal), {status: 409});
await submitForm(box.querySelector("form"));
const status = box.querySelector("#ho-offer-0-status");
assert.equal(status.textContent, refusal);
assert.equal(document.activeElement, status);
assert.equal(labelledIn(box, "Reason (required)").value, "On leave");
assert.equal(buttonIn(box, "Send offer to Miguel Garcia").disabled, false);
"""
        )


class WhenOfferingIsNotPossible(unittest.TestCase):
    def test_an_open_offer_swaps_the_offer_buttons_for_a_notice_and_a_withdraw_button(
        self,
    ) -> None:
        run(
            r"""
for (const who of ["RLO-01", "PM-01"]) {
  viewer(who); c = base(); c.handoff = offered(); requests.length = 0;
  caseSession = session();
  serverState = () => {c.handoff = offered("Withdrawn");};
  mount();
  assert.ok(!buttonTexts(card).some(name => name.startsWith("Offer this case to ")), who);
  assert.equal(card.querySelector(".notice").textContent, COPY.open_sender);
  assert.deepEqual(card.querySelectorAll(".flag").map(textOf), ["Offer waiting for an answer"]);
  const summaries = card.querySelectorAll("summary").map(textOf);
  assert.ok(!summaries.includes("Offer to someone who is not listed"));
  await clickOn(buttonIn(card, "Withdraw the offer to Miguel Garcia"));
  assert.deepEqual(requests.map(request => request.action), ["withdraw-handoff"]);
  const after = app.children[0];
  assert.equal(after.querySelector(".status-line").textContent,
    "Last offer to Miguel Garcia: withdrawn");
  assert.equal(resultOf(after), COPY.withdrawn);
  const again = buttonTexts(after).filter(name => name.startsWith("Offer this case to "));
  assert.equal(again.length, 3, "the candidates can be offered again");
}
"""
        )

    def test_every_other_situation_explains_itself_and_offers_nothing(self) -> None:
        run(
            r"""
const accepted = () => {
  c.handoff = offered("Accepted"); c.owner = "Miguel Garcia"; c.owner_code = "RC-01";
};
const situations = [
  ["offer open, another viewer", "BSL-01", () => {c.handoff = offered();}, COPY.open_other],
  ["accepted, not complete", "PM-01", accepted, COPY.accepted],
  ["case closed", "PM-01", () => {c.closed = true;}, COPY.closed],
  ["viewer is not the owner or a manager", "BSL-01", () => {}, COPY.not_owner],
];
for (const [name, who, setup, notice] of situations) {
  viewer(who); c = base(); setup();
  caseSession = session();
  mount();
  assert.ok(card.querySelector(".notice").textContent.startsWith(notice), name);
  assert.deepEqual(buttonTexts(card), [], `${name}: no action for this viewer`);
  assert.equal(card.querySelectorAll("form").length, 0, name);
  assert.equal(card.querySelectorAll("strong").length, 3, `${name}: the people stay listed`);
}
// A closed case points at the tab where a manager reopens it.
viewer("PM-01"); c = base(); c.closed = true;
let chosen = null, prevented = false;
caseSession = session();
caseSession.controller = {select: (...args) => {chosen = args;}};
mount();
const link = card.querySelectorAll("a").find(node => node.textContent === "Go to the Overview tab");
assert.equal(link.attrs.href, "#/case/ZF-5?tab=overview");
link.events.click({preventDefault() {prevented = true;}});
assert.ok(prevented);
assert.deepEqual(chosen, ["overview", true, true]);
// The accepting owner has the one action that unblocks it.
viewer("RC-01"); c = base(); accepted();
caseSession = session();
mount();
assert.ok(card.querySelector(".notice").textContent.startsWith(COPY.accepted_by_you));
assert.deepEqual(buttonTexts(card), ["Complete handoff"]);
labelledIn(card, "Completed action (required)");
await submitForm(card.querySelector("form"));
assert.equal(requests.length, 0);
assert.match(shownErrors(card)[0], /^Enter the completed action\. Owner: you\. Next action: /);
"""
        )


class StatusAndHistory(unittest.TestCase):
    def test_the_focused_status_and_its_confirmation_stay_in_view_while_content_above_loads(
        self,
    ) -> None:
        run(
            r"""
asOwner();
c.handoff = offered("Withdrawn");
caseSession.handoffResult = {text: COPY.withdrawn};
const scrolled = [], observers = [];
Node.prototype.scrollIntoView = function (options) {scrolled.push([this, options]);};
globalThis.ResizeObserver = class {
  constructor(callback) {
    this.callback = callback; this.watched = []; this.stopped = false; observers.push(this);
  }
  observe(node) {this.watched.push(node);}
  disconnect() {this.stopped = true;}
};
const panel = new Node("section");
panel.className = "case-tab-panel";
const heading = h("h2", {}, "Quality and handover"), above = h("section", {}, "Quality checks");
card = handoffPanel(c, "ZF-5", refresh);
panel.append(heading, above, card);
app.replaceChildren(panel);
await Promise.resolve();
const status = card.querySelector(".status-line");
const confirmation = card.querySelector(".handoff-result");
assert.equal(document.activeElement, status);
assert.deepEqual(observers[0].watched, [heading, above], "only what is above can push it down");
scrolled.length = 0;
observers[0].callback();
assert.deepEqual(scrolled, [[status, {block: "nearest"}], [confirmation, {block: "nearest"}]]);
status.events.blur();
assert.equal(observers[0].stopped, true, "it stops once the person moves on");
"""
        )

    def test_a_handoff_recorded_without_names_never_prints_undefined(self) -> None:
        run(
            r"""
asManager();
c.handoff = {state: "Offered", to_code: "RC-01", note: "Constructed handoff note"};
mount();
assert.equal(card.querySelector(".status-line").textContent,
  "Offered to a colleague, waiting for an answer");
for (const word of ["undefined", "null", "NaN"]) assert.ok(!card.textContent.includes(word), word);
const rows = fieldsOf(card.querySelector("dl"));
assert.equal(rows["Case stays with"], "Helen Marsden until the offer is accepted");
"""
        )

    def test_the_status_is_a_list_with_the_spec_labels_and_no_raw_times_or_record_paths(
        self,
    ) -> None:
        run(
            r"""
asManager();
c.handoff = offered();
c.work = {source: "case:ZF-5/handoff", recorded_at: "2026-11-20T13:21:01.115035+00:00"};
c.handoff_history = [{event_type: "handoff_offered", version: 1, at: "2026-10-13T09:00:00+00:00",
  actor: {name: "Helen Marsden"}, source: "Capacity check on 14 Oct", source_version: "1",
  reason: "I am on leave from Monday", from_name: "Helen Marsden", to_name: "Miguel Garcia",
  state: "Offered"}];
mount();
const list = card.querySelector("dl");
assert.deepEqual(list.querySelectorAll("dt").map(textOf), ["Case stays with",
  "Who must act next", "Offered by", "What they are asked to do", "How urgent", "Due",
  "Note from Helen Marsden", "Chase owner", "Resident update owner"]);
const rows = fieldsOf(list);
assert.equal(rows["Case stays with"], "Helen Marsden until the offer is accepted");
assert.equal(rows["Who must act next"], "Miguel Garcia: accept or decline");
assert.match(rows["Offered by"],
  /^Helen Marsden, \d{1,2} \w{3} \d{4}, \d\d:\d\d \(waiting 3 days\)$/);
assert.equal(rows["What they are asked to do"], "Agree an access date with the resident");
assert.equal(rows["How urgent"], "Routine");
assert.equal(rows["Due"], "Not set");
assert.equal(rows["Note from Helen Marsden"], "Covering while I am on leave");
assert.equal(rows["Resident update owner"], COPY.no_update_owner);
assert.equal(card.querySelector("h2").textContent, "Hand this case to a colleague");
assert.equal(card.querySelector(".status-line").textContent,
  "Offered to Miguel Garcia, waiting for an answer");
const everything = card.textContent;
assert.doesNotMatch(everything, /\d{4}-\d\d-\d\dT/);
assert.doesNotMatch(everything, /case:/);
assert.ok(!everything.includes(";"), "no semicolon runs");

const history = card.querySelector(".tl");
assert.deepEqual(card.querySelectorAll("h3").map(textOf).slice(-1), ["History of this handover"]);
const entry = history.querySelector("li");
assert.equal(entry.children[0].textContent,
  "13 Oct 2026, 09:00: Helen Marsden offered the case to Miguel Garcia.");
const record = entry.querySelector("details");
assert.ok(!record.hasAttribute("open"));
assert.deepEqual(Object.entries(fieldsOf(record)), [["Source", "Capacity check on 14 Oct"],
  ["Source version", "1"], ["Reason", "I am on leave from Monday"], ["Change number", "1"],
  ["Recorded by", "Helen Marsden"]]);

const lines = [
  ["Received", {}, "Miguel Garcia has seen the offer, not accepted yet"],
  ["Accepted", {}, "Accepted by Miguel Garcia. The handover is not complete yet."],
  ["Declined", {}, "Last offer: declined by Miguel Garcia"],
  ["Escalated", {escalation_owner: "Aadi Kapoor", answer_note: "No answer after three days"},
    "Escalated to Aadi Kapoor"],
];
for (const [state, extra, line] of lines) {
  c.handoff = offered(state, extra);
  mount();
  assert.equal(card.querySelector(".status-line").textContent, line);
}
assert.equal(fieldsOf(card.querySelector("dl"))["Who must act next"], COPY.chase);
"""
        )


class Receiver(unittest.TestCase):
    def test_the_receiver_can_accept_or_decline_through_labelled_required_fields(self) -> None:
        run(
            r"""
asReceiver();
c.handoff = offered();
c.handoff_history = [{}];
serverState = (action) => {
  c.handoff = offered(action === "accept-handoff" ? "Accepted" : "Declined");
};
mount();
assert.ok(card.querySelectorAll("h3").map(textOf).includes("Your answer"));
assert.ok(card.textContent.includes(COPY.if_you_accept));
assert.deepEqual(buttonTexts(card),
  ["Record receipt (not acceptance)", "Accept this case", "Decline this case"]);
assert.deepEqual(card.querySelectorAll("legend").map(textOf),
  ["Accept this case", "Decline this case"]);
for (const label of ["Source reference (required)", "Source version (required)",
  "Reason (required)", "Reason if you cannot take it (required)"]) {
  labelledIn(card, label);
}
assert.ok(card.textContent.includes(COPY.accept_hint));
const [accept, decline] = card.querySelectorAll("form");

await submitForm(accept);
assert.equal(requests.length, 0);
assert.equal(shownErrors(accept).length, 3);
assert.equal(document.activeElement, labelledIn(accept, "Source reference (required)"));

await submitForm(decline);
assert.equal(requests.length, 0);
assert.equal(shownErrors(decline).length, 1);
const reason = labelledIn(decline, "Reason if you cannot take it (required)");
assert.equal(document.activeElement, reason);
assert.equal(reason.attrs["aria-invalid"], "true");

fillRecord(accept, ["Programme meeting 14 Oct", "1", "I have capacity this week"]);
await submitForm(accept);
assert.deepEqual(requests.map(request => [request.action, request.body]), [["accept-handoff",
  {source: "Programme meeting 14 Oct", source_version: "1",
    reason: "I have capacity this week", handoff_version: 1}]]);
assert.equal(resultOf(app.children[0]), COPY.accepted_message);

c.handoff = offered();
mount();
typeInto(labelledIn(card, "Reason if you cannot take it (required)"), "I am full until January");
await submitForm(card.querySelectorAll("form")[1]);
assert.deepEqual(requests[1],
  {id: "ZF-5", action: "decline-handoff", body: {reason: "I am full until January"}});
"""
        )

    def test_held_back_text_gets_an_owner_and_a_next_action_instead_of_the_placeholder(
        self,
    ) -> None:
        run(
            r"""
asReceiver();
c.handoff = offered("Offered", {note: HELD, next_action: HELD});
c.handoff_history = [{event_type: "handoff_offered", version: 1,
  at: "2026-10-13T09:00:00+00:00", actor: {name: "Helen Marsden"}, source: HELD,
  source_version: HELD, reason: HELD, from_name: "Helen Marsden"}];
mount();
const rows = fieldsOf(card.querySelector("dl"));
assert.equal(rows["What they are asked to do"], COPY.held);
assert.equal(rows["Note from Helen Marsden"], COPY.held);
assert.ok(!card.textContent.includes(HELD), "the placeholder never reaches the card");
assert.ok(card.textContent.includes(COPY.held_detail));
"""
        )

    def test_the_held_back_text_matches_both_server_constants(self) -> None:
        match = re.search(r'^const SERVER_HELD = "([^"]*)";$', APP, re.M)
        assert match is not None
        self.assertEqual(match.group(1), projection.NOTE_HELD)
        self.assertEqual(match.group(1), taskqueues.HELD)


if __name__ == "__main__":
    unittest.main()
