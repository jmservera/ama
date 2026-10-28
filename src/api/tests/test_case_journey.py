"""Case journey semantics execute the shipped JavaScript, not a Python copy."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.insights import STAGE_ORDER

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

DOM = r"""
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
  addEventListener(name, fn) {this.events[name] = fn;}
  focus() {}
  scrollIntoView() {}
}
const document = {createElement: tag => new Node(tag),
  createTextNode: text => new Node("#text", text)};
"""


def shipped_helpers() -> str:
    source = (WEB / "app.js").read_text()
    return (
        "function h"
        + source.split("function h", 1)[1].split("async function api", 1)[0]
        + "function snapshotCaseFields"
        + source.split("function snapshotCaseFields", 1)[1].split("function captureCaseFields", 1)[
            0
        ]
    )


def evaluate(expression: str) -> Any:
    source = (WEB / "case-workspace.js").read_text()
    result = subprocess.run(
        ["node", "-e", source + f"\nconsole.log(JSON.stringify({expression}));"],
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def journey(**overrides: Any) -> list[dict[str, Any]]:
    case = dict(
        stage="Works under way",
        closed=False,
        work={"blockers": []},
        funding={"status": "Confirmed"},
        decision={"status": "Accepted"},
    )
    case.update(overrides)
    return list(evaluate(f"CaseWorkspace.journey({json.dumps(case)})"))


class CaseJourney(unittest.TestCase):
    def test_both_chat_submissions_clear_only_successful_unchanged_raw_questions(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const me = {user: {role: "Retrofit Programme Manager"}};
let finish, fail, requests = [], failure;
const api = async (path, body) => {
  if (path === "/api/assistants") return {assistants: []};
  if (path.endsWith("/status")) return new Promise(() => {});
  requests.push({path, body});
  if (failure === "thread" && path.endsWith("/threads")) throw new Error("Thread failed");
  if (path.endsWith("/threads")) return {id: "SYN-CHAT"};
  return await new Promise((resolve, reject) => {finish = resolve; fail = reject;});
};
"""
            + (WEB / "chat.js").read_text()
            + r"""
(async () => {
  for (const regulatory of [false, true]) {
    for (const change of ["none", "text", "space", "answer-failure", "thread-failure"]) {
      requests = []; failure = change === "thread-failure" ? "thread" : null;
      const panel = chatCasePanel("SYN-526");
      const root = regulatory ? panel.querySelector("#regulatory-chat") : panel;
      const input = root.querySelector(regulatory ? "#regulatory-question" : "#chat-question");
      const form = root.querySelector("form"), button = form.querySelector("button");
      input.value = "  Submitted question  "; input.dataset.caseDirty = "true";
      const event = {preventDefault() {}};
      const pending = form.events.submit(event);
      await new Promise(resolve => setImmediate(resolve));
      if (change !== "thread-failure") {
        assert.equal(button.disabled, true);
        const before = requests.length;
        await form.events.submit(event);
        assert.equal(requests.length, before, "pending duplicate excluded");
        if (change === "text") input.value = "New question";
        if (change === "space") input.value += " ";
        if (change === "answer-failure") fail(new Error("Answer failed"));
        else finish({reply: "Synthetic answer", kind: "answer", citations: []});
      }
      await pending;
      assert.equal(button.disabled, false);
      const unchanged = change === "none";
      assert.equal(input.value, unchanged ? "" : change === "text"
        ? "New question" : change === "space"
        ? "  Submitted question   " : "  Submitted question  ");
      assert.equal(Boolean(input.dataset.caseDirty), !unchanged);
      assert.equal(requests[0].body.case_id, "SYN-526");
      if (change !== "thread-failure") {
        assert.equal(requests[1].body.content, "Submitted question");
      }
    }
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)
        source = (WEB / "app.js").read_text()
        self.assertIn("session.chatPanel ||= chatCasePanel(id)", source)
        self.assertIn('["ai", "AI assistance", [assistantPanel, chatPanel,', source)

    def test_all_proposal_accept_controls_share_readiness_and_own_verification(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + 'const me = {user: {email: "reviewer@example.test"}};\n'
            + (WEB / "assistants.js").read_text()
            + r"""
const baseline = {id: "SYN", revision: 1, case_id: "SYN-526", state: "ready",
  capability: "assessment-preparation", provenance: [],
  output: {summary: "Synthetic", findings: [], unknowns: []},
  verification: {by: me.user.email}};
for (const override of [{}, {stale: true}, {state: "queued"}, {state: "accepted"},
  {state: "failed"}, {actionable: false}, {release_denial: {reason: "Denied"}},
  {epoch_current: false}, {verification: null},
  {verification: {by: "other@example.test"}}]) {
  const card = assistantProposal({...baseline, ...override}, () => {});
  const buttons = card.querySelectorAll("button");
  const ready = Object.keys(override).length === 0;
  for (const label of ["Accept", "Edit", "Save edited proposal"]) {
    assert.equal(buttons.find(button => button.textContent === label).disabled, !ready, label);
  }
  const editor = card.querySelectorAll("textarea")
    .find(field => field.attrs["aria-label"] === "Edited evidence proposal JSON");
  assert.equal(editor.disabled, false, "edited JSON stays copyable");
  assert.equal(buttons.find(button => button.textContent === "Reject").disabled, false);
}
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_count_live_text_is_atomic_and_only_mutates_for_changed_counts(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const app = new Node("main"), aiMode = {workflow: false};
const location = {hash: "#/case/SYN?tab=overview"};
const history = {pushState() {}};
const MutationObserver = class {observe() {} disconnect() {}};
const definitions = ["overview", "ai"].map(id => ({
  id, label: id, panel: h("section", {}, h("h2", {}, id))
}));
const assistant = h("section", {}), drafts = h("div", {});
"""
            + (WEB / "case-workspace.js").read_text()
            + r"""
const workspace = CaseWorkspace.enhance({id: "SYN", hazards: [], work: {}},
  definitions, null, assistant, drafts);
const summary = workspace.top[0], count = summary.querySelector("[data-case-ai-count]");
assert.equal(count.attrs.role, "status");
assert.equal(count.attrs["aria-live"], "polite");
assert.equal(count.attrs["aria-atomic"], "true");
assert.equal(count.querySelectorAll("button").length, 0);
assert.match(count.textContent, /loading/);
const writes = count.writes;
workspace.counts(); workspace.counts();
assert.equal(count.writes, writes, "unchanged loading is not reannounced");
assistant.setAttribute("data-waiting", "2");
assistant.setAttribute("data-assistance", "Assistance available.");
workspace.counts();
assert.equal(count.textContent, "2 AI suggestions waiting for review.");
assert.equal(count.writes, writes + 1);
workspace.counts();
assistant.setAttribute("data-assistance", "Assistance available. Proactive checks off.");
workspace.counts();
assert.equal(count.writes, writes + 1, "availability belongs to the panel, not count live text");
assistant.setAttribute("data-assistance", "AI assistance unavailable. Work continues manually.");
workspace.counts();
assert.equal(count.textContent, "AI review count unavailable.");
assert.equal(count.writes, writes + 2);
workspace.counts();
assert.equal(count.writes, writes + 2);
assert.equal(definitions[1].panel.hidden, true, "summary does not require the AI tab");
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_all_stages_mapped_once_in_shipped_module(self) -> None:
        stages = evaluate("CaseWorkspace.steps.flatMap(step => step.stages)")
        self.assertEqual(len(stages), len(set(stages)))
        self.assertEqual(set(stages), set(STAGE_ORDER))
        for stage in STAGE_ORDER:
            with self.subTest(stage=stage):
                current = [step for step in journey(stage=stage) if step["current"]]
                self.assertEqual(len(current), 1)

    def test_fixed_slide_order_and_evidence_exceptions(self) -> None:
        states = journey(funding={"status": "Submitted"}, decision={"status": "Asked"})
        self.assertEqual(
            [step["name"] for step in states],
            [
                "Survey",
                "Assessment",
                "Funding",
                "Resident agreement",
                "Contractor",
                "Quality and handover",
            ],
        )
        for index in (2, 3):
            self.assertEqual(states[index]["state"], "upcoming")
            self.assertEqual(states[index]["text"], "Earlier step not confirmed")
        self.assertEqual(journey()[2]["state"], "done")
        self.assertEqual(journey()[3]["state"], "done")
        self.assertNotEqual(
            journey(stage="Waiting for resident decision", funding={"status": "Draft ready"})[2][
                "state"
            ],
            "done",
        )

    def test_blocker_mapping_current_and_unknown(self) -> None:
        for label, index in (
            ("Final checks: funding", 2),
            ("Final checks: resident decision", 3),
            ("Final checks: technical review", 1),
            ("Stock review", 1),
            ("Safety review", 4),
            ("Shared building review", 4),
            ("Unknown blocker", 4),
        ):
            with self.subTest(label=label):
                states = journey(work={"blockers": [{"step": label, "reason": "Check evidence"}]})
                self.assertEqual(states[index]["state"], "blocked")
                self.assertIn("Check evidence", states[index]["text"])
                self.assertEqual(sum(bool(step["current"]) for step in states), 1)
                self.assertTrue(states[4]["current"])
                self.assertNotEqual(states[0]["state"], "blocked")

    def test_closed_overrides_blockers_unknown_stage_does_not_invent_step(self) -> None:
        states = journey(
            closed=True, work={"blockers": [{"step": "Safety review", "reason": "Check"}]}
        )
        self.assertTrue(all(step["state"] == "done" for step in states))
        self.assertFalse(any(step["current"] for step in states))
        self.assertFalse(any(step["current"] for step in journey(stage="Unknown")))

    def test_summary_empty_values_handoff_and_overdue(self) -> None:
        empty = evaluate("CaseWorkspace.summary({work: {}})")
        self.assertEqual(empty["owner"], "Unknown")
        self.assertEqual(empty["blockers"], "No recorded blockers.")
        self.assertEqual(empty["step"], "Step unknown")
        case = {
            "owner": "Sam",
            "owner_role": "Officer",
            "handoff": {"state": "Received", "proposed_receiver": "Pam"},
            "work": {
                "next_action": "Check the evidence.",
                "blockers": [
                    {"reason": "Missing source.", "owner": "Unknown", "next_action": "Ask Sam."}
                ],
                "overdue": [{"task": "Call"}],
            },
        }
        summary = evaluate(f"CaseWorkspace.summary({json.dumps(case)})")
        self.assertIn("Offered to Pam, not yet confirmed", summary["owner"])
        self.assertIn("Owner: Unknown. Next action: Ask Sam.", summary["blockers"])
        self.assertEqual(summary["overdue"], 1)

    def test_reviewable_count_states(self) -> None:
        for state, output, stale, expected in (
            ("ready", {}, False, True),
            ("ready", {}, True, False),
            ("queued", None, False, False),
            ("running", None, False, False),
            ("failed", None, False, False),
            ("accepted", {}, False, False),
            ("rejected", {}, False, False),
        ):
            proposal: dict[str, Any] = {"state": state, "output": output, "stale": stale}
            self.assertEqual(evaluate(f"CaseWorkspace.waiting({json.dumps(proposal)})"), expected)

    def test_summary_jump_targets_record_actions(self) -> None:
        for case, expected in (
            ({"stage": "Contacting resident", "work": {}}, "resident"),
            ({"stage": "Final checks before ordering", "can_advance": True}, "overview"),
            ({"work": {"source": "case:ZF-1/handoff"}}, "quality"),
            ({"work": {"blockers": [{"current_stop": True}]}}, "blockers"),
        ):
            self.assertEqual(evaluate(f"CaseWorkspace.nextTab({json.dumps(case)})"), expected)

    def test_panels_mounted_once_and_tab_only_navigation_precedes_guard(self) -> None:
        app = (WEB / "app.js").read_text()
        case = app.split("async function caseView(id) {", 1)[1].split(
            "async function buildingView", 1
        )[0]
        for panel in (
            "workSteps",
            "safetyPanel",
            "regulatoryAlertsPanel",
            "returnPanel",
            "stockPanel",
            "technicalPanel",
            "documentsPanel",
            "fundingPanel",
            "financePanel",
            "grantPanel",
            "residentPanel",
            "affectedChallengePanel",
            "qualityPanel",
            "handoffPanel",
            "assistantCasePanel",
            "chatCasePanel",
        ):
            self.assertEqual(case.count(panel + "("), 1, panel)
        route = app.split("async function route() {", 1)[1]
        self.assertLess(route.index("controller.select"), route.index("window.confirm"))
        self.assertIn('draftBox: h("div", { id: "resident-draft-output" })', app)
        self.assertIn('data-case-dirty="true"', app)

    def test_refresh_clears_only_explicit_submission_after_success(self) -> None:
        app = (WEB / "app.js").read_text()
        case = app.split("async function caseView(id) {", 1)[1]
        refresh = case.split("  const refresh = ", 1)[1].split("  const outcome = ", 1)[0]
        snapshot = (
            "function snapshotCaseFields"
            + app.split("function snapshotCaseFields", 1)[1].split("function captureCaseFields", 1)[
                0
            ]
        )
        script = (
            """
let briefingBox = {}, renders = 0, errors = 0;
const id = "SYN-526";
const session = {}, caseSession = session;
const msg = {replaceChildren() { errors++; }};
const h = () => ({});
const caseView = async () => { renders++; };
const submitted = {dataset: {caseDirty: "true"}};
const unrelated = {dataset: {caseDirty: "true"}};
const refresh = """
            + refresh
            + snapshot
            + """
(async () => {
  await refresh(async () => { throw new Error("Synthetic refusal"); }, [submitted]);
  const failed = submitted.dataset.caseDirty === "true"
    && unrelated.dataset.caseDirty === "true" && errors === 1 && renders === 0;
  await refresh(async () => {}, [submitted]);
  const cleared = !submitted.dataset.caseDirty;
  submitted.dataset.caseDirty = "true"; submitted.value = "Dispatched";
  const sent = snapshotCaseFields([submitted]);
  submitted.value = "Later edit before refresh";
  await refresh(async () => {}, sent);
  const delayed = submitted.dataset.caseDirty === "true";
  const file = {dataset: {caseDirty: "true"}, value: "same-name.txt", files: [{}]};
  const fileSent = snapshotCaseFields([file]);
  file.files = [{}];
  await refresh(async () => {}, fileSent);
  const replacedFile = file.dataset.caseDirty === "true";
  submitted.dataset.caseDirty = "true"; submitted.value = "Sent";
  await refresh(async () => { submitted.value = "Typed while saving"; }, [submitted]);
  console.log(JSON.stringify({failed, cleared, delayed, replacedFile,
    pending: submitted.dataset.caseDirty,
    unrelated: unrelated.dataset.caseDirty, renders}));
})();
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True, check=True)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "failed": True,
                "cleared": True,
                "delayed": True,
                "replacedFile": True,
                "pending": "true",
                "unrelated": "true",
                "renders": 4,
            },
        )

    def test_live_field_identity_wins_over_stale_recovery_in_either_dom_order(self) -> None:
        app = (WEB / "app.js").read_text()
        entries = (
            "function caseFieldEntries"
            + app.split("function caseFieldEntries", 1)[1].split("function snapshotCaseFields", 1)[
                0
            ]
        )
        script = (
            """
const live = {id: "q-i0", dataset: {caseFieldKey: "measure:version:item"},
  closest: () => null};
const recovery = {preservedCaseField: {key: "measure:version:item"},
  closest: () => null};
const app = {querySelectorAll: () => [live, recovery]};
"""
            + entries
            + """
const first = caseFieldEntries();
app.querySelectorAll = () => [recovery, live];
const second = caseFieldEntries();
console.log(JSON.stringify([first.length, first[0].field === live,
  second.length, second[0].field === live]));
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(result.stdout), [1, True, 1, True])

    def test_shared_dirty_guard_reconciles_pending_and_unload(self) -> None:
        source = (WEB / "app.js").read_text()
        guard = source.split("function hasUnsavedChanges()", 1)[1].split(
            "async function route()", 1
        )[0]
        remember = source.split("function rememberCaseFields(session)", 1)[1].split(
            "function restoreCaseFields", 1
        )[0]
        unload = (
            source.split('window.addEventListener("beforeunload",', 1)[1].split("\n});", 1)[0]
            + "\n};\n"
        )
        script = (
            """
const assert = require("node:assert/strict");
let live = [], captured = [], domDirty = false;
let caseSession = {pendingFields: new Map([["pending", {key: "pending", value: "Only cache"}]])};
const document = {querySelector: () => domDirty};
const caseFieldEntries = () => live;
const captureCaseFields = () => captured;
function rememberCaseFields(session)"""
            + remember
            + "function hasUnsavedChanges()"
            + guard
            + "const unload = "
            + unload
            + """
assert.equal(hasUnsavedChanges(), true);
const event = {preventDefault() {this.prevented = true;}};
unload(event);
assert.equal(event.prevented, true);
assert.equal(event.returnValue, "");
live = [{key: "pending", field: {dataset: {}}}];
assert.equal(hasUnsavedChanges(), false, "clean live counterpart retires cached snapshot");
live = []; captured = [{key: "new", value: "Latest"}];
assert.equal(hasUnsavedChanges(), true);
assert.equal(caseSession.pendingFields.get("new").value, "Latest");
caseSession = null; domDirty = true;
assert.equal(hasUnsavedChanges(), true, "ordinary form dirtiness still warns");
domDirty = false;
assert.equal(hasUnsavedChanges(), false);
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_review_dispatch_preserves_newer_values_and_completes_only_once(self) -> None:
        source = (WEB / "app.js").read_text()
        notes = (
            "function aiNotes"
            + source.split("function aiNotes", 1)[1].split("function aiBox", 1)[0]
        )
        snapshots = (
            "function snapshotCaseFields"
            + source.split("function snapshotCaseFields", 1)[1].split(
                "function captureCaseFields", 1
            )[0]
        )
        script = (
            r"""
const assert = require("node:assert/strict");
class Node {
  constructor(tag, attrs, kids) {
    this.tag = tag; this.attrs = attrs || {}; this.kids = kids.flat().filter(Boolean);
    this.dataset = {}; this.value = ""; this.hidden = false;
    this.disabled = Boolean(this.attrs.disabled);
    if (tag === "textarea") this.value = kids.join("");
  }
  all() { return this.kids.filter(k => k instanceof Node)
    .flatMap(k => [k, ...k.all()]); }
  querySelectorAll(tag) { return this.all().filter(k => k.tag === tag); }
  querySelector(tag) { return this.querySelectorAll(tag)[0]; }
  setAttribute(name, value) { this.attrs[name] = value; }
  removeAttribute(name) {
    delete this.attrs[name];
    if (name === "data-case-dirty") delete this.dataset.caseDirty;
  }
  addEventListener() {}
  focus() {}
  prepend(node) { this.kids.unshift(node); }
}
const h = (tag, attrs, ...kids) => new Node(tag, attrs, kids);
const app = {dispatchEvent() {}};
let finish, fail, requests = [], done = [];
const api = async (path, body) => {
  requests.push({path, body});
  await new Promise((resolve, reject) => { finish = resolve; fail = reject; });
};
"""
            + snapshots
            + notes
            + r"""
(async () => {
  for (const change of ["none", "text", "reason", "both", "failure"]) {
    requests = []; done = [];
    const record = {record_id: "SYN-REVIEW", approval: "Not reviewed", text: "Original"};
    const meta = aiNotes(record, (action, text) => done.push({action, text}));
    const editing = meta.querySelector("textarea"), reason = meta.querySelector("input");
    const box = meta.querySelector("fieldset"), buttons = box.querySelectorAll("button");
    editing.value = "Submitted replacement"; reason.value = "Submitted reason";
    editing.dataset.caseDirty = reason.dataset.caseDirty = "true";
    const pending = buttons[1].attrs.onclick();
    assert.equal(buttons.every(button => button.disabled), true);
    await buttons[1].attrs.onclick();
    assert.equal(requests.length, 1, "duplicate dispatch must not issue another review");
    if (["text", "both", "failure"].includes(change)) editing.value = "Newer replacement";
    if (["reason", "both", "failure"].includes(change)) reason.value = "Newer reason";
    if (change === "failure") fail(new Error("Synthetic refusal")); else finish();
    await pending;
    assert.equal(requests[0].body.text, "Submitted replacement");
    assert.equal(requests[0].body.reason, "Submitted reason");
    if (change === "failure") {
      assert.equal(record.approval, "Not reviewed");
      assert.equal(editing.dataset.caseDirty, "true");
      assert.equal(reason.dataset.caseDirty, "true");
      assert.equal(buttons.some(button => button.disabled), false);
      assert.equal(done.length, 0);
      continue;
    }
    assert.equal(record.approval, "Edited");
    assert.deepEqual(done, [{action: "edit", text: "Submitted replacement"}]);
    assert.equal(box.hidden, change === "none");
    assert.equal(Boolean(editing.dataset.caseDirty), ["text", "both"].includes(change));
    assert.equal(Boolean(reason.dataset.caseDirty), ["reason", "both"].includes(change));
    if (change !== "none") {
      assert.equal(editing.readOnly, true);
      assert.equal(reason.readOnly, true);
      assert.match(box.querySelector("legend").textContent, /reviewed record SYN-REVIEW/);
    }
    await buttons[2].attrs.onclick();
    assert.equal(requests.length, 1, "completed review cannot submit again");
    assert.equal(buttons.every(button => button.disabled), true);
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_journey_links_keep_non_tab_query_values_when_resynchronized(self) -> None:
        source = (WEB / "case-workspace.js").read_text()
        sync = (
            "function syncLinks()"
            + source.split("function syncLinks()", 1)[1].split("function select(", 1)[0]
        )
        script = (
            """
const assert = require("node:assert/strict");
const c = {id: "ZF /1"};
const location = {hash: "#/case/ZF%20%2F1?tab=resident&challenge-target-history=2"
  + "&challenge-record-history=3&filter=a%26b&filter=second"};
const links = ["survey", "funding", "resident", "contractor", "quality"].map(tab => ({
  dataset: {caseTab: tab}, setAttribute(name, value) {this[name] = value;}
}));
const nav = {querySelectorAll: () => links};
"""
            + sync
            + """
for (const page of [2, 4]) {
  location.hash = location.hash.replace("challenge-target-history=2",
    "challenge-target-history=" + page);
  syncLinks();
  for (const link of links) {
    const [path, query] = link.href.split("?");
    const params = new URLSearchParams(query);
    assert.equal(path, "#/case/ZF%20%2F1");
    assert.equal(params.get("tab"), link.dataset.caseTab);
    assert.equal(params.get("challenge-target-history"), String(page));
    assert.equal(params.get("challenge-record-history"), "3");
    assert.deepEqual(params.getAll("filter"), ["a&b", "second"]);
  }
}
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
