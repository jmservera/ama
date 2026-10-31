"""Case journey semantics execute the shipped JavaScript, not a Python copy."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tomllib
import unittest
import zipfile
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
  remove() {this.parentElement.children = this.parentElement.children.filter(k => k !== this);}
  addEventListener(name, fn) {this.events[name] = fn;}
  focus() {document.activeElement = this;}
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
        + "let caseSession = null;\nfunction caseFieldEntries"
        + source.split("function caseFieldEntries", 1)[1].split("function captureCaseFields", 1)[0]
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
    def test_shared_mutation_lock_survives_reconstruction_and_response_parsing(self) -> None:
        source = (WEB / "app.js").read_text()
        script = (
            DOM
            + shipped_helpers()
            + "async function api"
            + source.split("async function api", 1)[1].split("const fmtDate", 1)[0]
            + r"""
const routeController = new AbortController();
let requests = [], finish;
const fetch = async (path, options) => {
  if (!options.method) return {ok: true, status: 200, json: async () => ({})};
  requests.push([path, JSON.parse(options.body)]);
  return {ok: true, status: 200, json: () => new Promise(resolve => {finish = resolve;})};
};
(async () => {
  const paths = [
    ["/api/cases/SYN/advance", {}],
    ["/api/cases/SYN/receive-handoff", {}],
    ["/api/cases/SYN/withdraw-handoff", {}],
    ["/api/cases/SYN/quality-submit", {measure: "Loft"}],
    ["/api/cases/SYN/quality-return", {index: 0}],
    ["/api/cases/SYN/finance", {action: "commit_raise"}],
    ["/api/cases/SYN/grant", {action: "grant_propose", id: "G1"}],
    ["/api/cases/SYN/technical", {action: "design_submit"}],
    ["/api/cases/SYN/funding", {action: "save_draft"}],
    ["/api/cases/SYN/hazard-raise", {}],
    ["/api/cases/SYN/upload", {}],
    ["/api/packages", {}],
    ["/api/packages/P1/capacity", {}],
    ["/api/workorders", {case_id: "SYN", package: "P1"}],
    ["/api/workorders/W1/appointment", {action: "record_offer"}],
    ["/api/assistants/assessment-preparation/invoke", {case_id: "SYN"}],
    ["/api/assistants/proposals/P1/review", {action: "reject", revision: 1}],
    ["/api/ai/review/R1/edit", {}],
    ["/api/ai/priority/R1/reject", {}],
    ["/api/chat/threads/T1/proposals", {capability: "assessment-preparation"}],
    ["/api/chat/regulatory/threads/T1/doubt", {turn: "TURN1"}],
    ["/api/time", {case_id: "SYN"}],
  ];
  for (const [path, body] of paths) {
    requests = [];
    const first = api(path, body);
    await new Promise(resolve => setImmediate(resolve));
    assert.equal(pendingMutations.size, 1, "lock includes response-body parsing");
    const rebuiltHandler = () => api(path, {...body, note: "Later edit", revision: 99,
      kind: "Changed document kind"});
    await assert.rejects(rebuiltHandler(), e => e.status === 409
      && !mutationNeedsHistory(e) && /still pending/.test(e.message));
    await api("/api/cases/SYN");
    assert.equal(pendingMutations.size, 1, "GET cannot release pending POST");
    assert.equal(requests.length, 1, path + " reconstructed entry dispatches once");
    finish({}); await first;
    assert.equal(pendingMutations.size, 0);
    const retry = rebuiltHandler(); await new Promise(resolve => setImmediate(resolve));
    assert.equal(requests.length, 2, "completed lock is reusable");
    finish({}); await retry;
  }
  assert.notEqual(mutationKey("/case", {action: "record", id: "A"}),
    mutationKey("/case", {action: "record", id: "B"}));
  assert.notEqual(mutationKey("/case", {action: "record", id: "A"}),
    mutationKey("/case", {action: "approve", id: "A"}));
  assert.notEqual(mutationKey("/chat", {turn: "A"}), mutationKey("/chat", {turn: "B"}));
  const a = api("/api/cases/A/advance", {}); await new Promise(r => setImmediate(r));
  const finishA = finish;
  const b = api("/api/cases/B/advance", {}); await new Promise(r => setImmediate(r));
  assert.equal(pendingMutations.size, 2, "unrelated targets proceed independently");
  finish({}); finishA({}); await Promise.all([a, b]);
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_queue_drafts_survive_old_failed_and_changed_revision_listings(self) -> None:
        source = (WEB / "app.js").read_text()
        script = (
            DOM
            + shipped_helpers()
            + "function captureCaseFields"
            + source.split("function captureCaseFields", 1)[1].split(
                'app.addEventListener("input"', 1
            )[0]
            + r"""
Node.prototype.replaceChildren = function(...children) {
  this.children = []; this.append(...children);
};
const app = new Node("main"), me = {user: {email: "reviewer@example.test"}};
const routeController = new AbortController();
const show = (...nodes) => app.replaceChildren(...nodes);
let listing, failListing = false, finishReview, heldRead;
let proposals = [{id: "P1", revision: 1, case_id: "SYN", state: "ready",
  capability: "assessment-preparation", provenance: [],
  output: {summary: "Synthetic", findings: [], unknowns: []},
  verification: {by: me.user.email}}];
const api = async (path, body) => {
  if (body) return new Promise((resolve, reject) => {finishReview = {resolve, reject};});
  if (failListing) throw Object.assign(new Error("Synthetic listing failed"), {status: 503});
  if (heldRead) return new Promise(resolve => {listing = resolve;});
  return {proposals};
};
"""
            + (WEB / "assistants.js").read_text()
            + r"""
(async () => {
  await assistantQueueView();
  let card = app.querySelector("[data-proposal-id]");
  const [reason, editing] = card.querySelectorAll("textarea");
  reason.value = "Supplied reason"; editing.value = '{"summary":"Unsubmitted JSON"}';
  reason.dataset.caseDirty = editing.dataset.caseDirty = "true";
  const reject = card.querySelectorAll("button").find(b => b.textContent === "Reject");
  const sending = reject.events.click();
  heldRead = true;
  const old = assistantQueueView();
  reason.value = "Later reason";
  finishReview.reject(Object.assign(new Error("Unconfirmed"), {status: 503, outcome: "uncertain"}));
  await sending;
  listing({proposals}); await old;
  card = app.querySelector("[data-proposal-id]");
  assert.equal(card.querySelectorAll("textarea")[0].value, "Later reason");
  assert.equal(card.querySelectorAll("textarea")[1].value, '{"summary":"Unsubmitted JSON"}');
  assert.equal(card.querySelector("fieldset").querySelector("button").disabled, true);
  heldRead = false; failListing = true;
  await assistantQueueView();
  assert.equal(app.querySelector("[data-proposal-id]"), card, "failed GET retains original DOM");
  assert.match(app.textContent, /Synthetic listing failed/);
  failListing = false;
  await assistantQueueView();
  card = app.querySelector("[data-proposal-id]");
  assert.equal(card.querySelectorAll("textarea")[0].value, "Later reason");
  assert.equal(card.querySelector("fieldset").querySelector("button").disabled, false);
  proposals = [{...proposals[0], revision: 2}];
  await assistantQueueView();
  assert.equal(app.querySelector("[data-proposal-id]").querySelector("textarea").value, "");
  let copies = app.querySelector('[data-case-recovery="proposal"]').querySelectorAll("textarea");
  assert.deepEqual(copies.map(field => field.value),
    ["Later reason", '{"summary":"Unsubmitted JSON"}']);
  assert.ok(copies.every(field => field.hasAttribute("readonly")));
  proposals = [];
  await assistantQueueView();
  copies = app.querySelector('[data-case-recovery="proposal"]').querySelectorAll("textarea");
  assert.equal(copies.length, 2, "missing proposal retains copy-only recovery");
  app.querySelector('[data-case-recovery="proposal"]').querySelector("button").events.click();
  assert.equal(me.assistantQueueDrafts.pendingFields.size, 0);
  assert.equal(app.querySelector('[data-case-recovery="proposal"]'), undefined);
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_api_preserves_outcome_before_http_status_classification(self) -> None:
        source = (WEB / "app.js").read_text()
        script = (
            'const assert = require("node:assert/strict");\n'
            "const routeController = new AbortController();\nlet response;\n"
            "const fetch = async () => response;\n"
            "let caseSession = {id: 'SYN', pendingSubmissions: new Map()};\n"
            "const app = {querySelector: () => ({dataset: {caseWorkspace: 'SYN'}})};\n"
            + "function mutationNeedsHistory"
            + source.split("function mutationNeedsHistory", 1)[1].split("const fmtDate", 1)[0]
            + "async function recoverCase(id) {"
            + source.split("async function caseView(id) {", 1)[1].split(
                "  const savedFields = ", 1
            )[0]
            + 'return "rendered";}\n'
            + r"""
(async () => {
  for (const status of [409, 503]) {
    for (const outcome of [undefined, "committed", "uncertain"]) {
      response = {status, ok: false, json: async () => ({
        error: "Synthetic refusal", reasons: ["Synthetic reason"], outcome
      })};
      await assert.rejects(api("/api/cases/SYN/quality-submit", {}), error => {
        assert.equal(error.status, status);
        assert.equal(error.outcome, outcome);
        assert.deepEqual(error.reasons, ["Synthetic reason"]);
        assert.equal(mutationNeedsHistory(error), outcome !== undefined);
        return true;
      });
    }
  }
  assert.equal(mutationNeedsHistory(new TypeError("Connection lost")), true);
  let release;
  response = {status: 200, ok: true, json: () => new Promise(resolve => {release = resolve;})};
  const old = recoverCase("SYN");
  await new Promise(resolve => setImmediate(resolve));
  requireCaseHistory(caseSession);
  const barrier = caseSession.historyBarrier;
  caseSession.qualitySaving = "check-history";
  caseSession.assistantRequests = new Map([["quality", "check-history"]]);
  release({});
  assert.equal(await old, undefined, "pre-outcome read cannot repaint");
  assert.equal(caseSession.historyBarrier, barrier);
  assert.equal(caseSession.assistantRequests.size, 1);
  response = {status: 503, ok: false, json: async () => ({error: "Read failed"})};
  await assert.rejects(recoverCase("SYN"));
  assert.equal(caseSession.historyBarrier, barrier, "failed GET cannot unlock");
  response = {status: 200, ok: true, json: async () => ({})};
  assert.equal(await recoverCase("SYN"), "rendered");
  assert.equal(caseSession.historyBarrier, undefined);
  assert.equal(caseSession.assistantRequests.size, 0);
  response = {status: 200, ok: true, json: () => new Promise(resolve => {release = resolve;})};
  const preRecovery = recoverCase("SYN");
  await new Promise(resolve => setImmediate(resolve));
  requireCaseHistory(caseSession);
  response = {status: 200, ok: true, json: async () => ({})};
  assert.equal(await recoverCase("SYN"), "rendered");
  release({});
  assert.equal(await preRecovery, undefined,
    "pre-outcome GET remains stale even after a later recovery clears the barrier");
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_upload_preparation_and_guarded_dispatch_outcomes(self) -> None:
        source = (WEB / "app.js").read_text()
        case = source.split("async function caseView(id)", 1)[1]
        refresh = case.split("  const refresh = ", 1)[1].split("  const outcome = ", 1)[0]
        script = (
            DOM
            + shipped_helpers()
            + r"""
Node.prototype.setCustomValidity = function() {};
Node.prototype.reportValidity = () => true;
Node.prototype.replaceChildren = function(...children) {
  this.children = []; this.append(...children);
};
const app = new Node("main"), workspaceStatus = {}, id = "SYN";
let session, reads = [], requests = 0, refusal, renders = 0;
const msg = new Node("div");
let briefingBox;
const caseView = async () => {renders++;};
class FileReader {
  readAsDataURL() {reads.push(this);}
}
const api = async () => {
  requests++;
  if (refusal) throw refusal;
  return {};
};
const refresh = """
            + refresh
            + "function recordedChangeForm"
            + source.split("function recordedChangeForm", 1)[1].split("window.addEventListener", 1)[
                0
            ]
            + "function documentsPanel"
            + source.split("function documentsPanel", 1)[1].split("const fundingAi", 1)[0]
            + r"""
(async () => {
  for (const outcome of ["prepare", "refusal", "committed", "uncertain", "transport", "success"]) {
    requests = 0; reads = []; renders = 0; refusal = null;
    session = caseSession = {id, pendingFields: new Map(), documentBox: new Node("div")};
    app.children = [];
    const panel = documentsPanel({checklist: [], documents: []}, id, refresh); app.append(panel);
    const form = panel.querySelector("form"), button = form.querySelector("button");
    form.querySelectorAll("input").forEach(field => {
      field.value = "Synthetic input"; field.files = [{name: "synthetic.txt"}];
      field.dataset.caseDirty = "true";
    });
    const submit = () => form.events.submit({preventDefault() {}});
    let saving = submit();
    await submit();
    assert.equal(reads.length, 1, "form excludes concurrent file preparation");
    if (outcome === "prepare") {
      reads[0].onerror(); await saving;
      assert.equal(requests, 0); assert.equal(session.historyBarrier, undefined);
      assert.equal(button.disabled, false);
      saving = submit();
    }
    if (outcome === "refusal") refusal = Object.assign(new Error("Refused"), {status: 409});
    if (["committed", "uncertain"].includes(outcome))
      refusal = Object.assign(new Error("Check history"), {status: 503, outcome});
    if (outcome === "transport") refusal = new TypeError("Connection lost");
    reads.at(-1).result = "data:text/plain;base64,U1lO";
    reads.at(-1).onload(); await saving;
    const blocked = ["committed", "uncertain", "transport"].includes(outcome);
    assert.equal(button.disabled, blocked, outcome);
    assert.equal(Boolean(session.historyBarrier), blocked);
    if (blocked) {
      await submit();
      assert.equal(requests, 1, "uncertain upload cannot dispatch again");
      assert.equal(form.querySelector('[type="file"]').files.length, 1);
    }
    if (outcome === "refusal") {
      assert.equal(button.disabled, false);
      assert.equal(form.querySelector('[type="file"]').files.length, 1);
    }
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_priority_invocation_and_procurement_preserve_history_barriers(self) -> None:
        source = (WEB / "app.js").read_text()
        script = (
            DOM
            + shipped_helpers()
            + r"""
Node.prototype.replaceChildren = function(...children) {
  this.children = []; this.append(...children);
};
const app = new Node("main"), HTMLButtonElement = Node;
const me = {user: {email: "reviewer@example.test", role: "Retrofit Programme Manager"}};
const routeController = new AbortController(), location = {hash: "#/case/SYN"};
const workspaceStatus = {}, aiMode = {};
const modeBody = body => body, isManager = () => true, fmtDate = value => value;
const restoreBoundFields = () => {}, show = (...nodes) => app.replaceChildren(...nodes);
document.querySelectorAll = () => [];
let pathCalls = [], failure, finish, caseLoads = 0, deferProcurement = false, oldReads = [];
const caseView = async () => {caseLoads++;};
const tick = () => new Promise(resolve => setImmediate(resolve));
const recommendation = {id: "SYN", status: "Proposed", items: [], deterministic: []};
const api = async (path, body) => {
  if (body === undefined) {
    if (path === "/api/ai/priority") return {recommendation};
    if (path === "/api/assistants") return {assistants: [{id: "quality-evidence"}]};
    if (path.startsWith("/api/assistants/proposals")) return {proposals: []};
    if (deferProcurement) return new Promise(resolve => oldReads.push(resolve));
    return [];
  }
  pathCalls.push(path);
  await new Promise(resolve => {finish = resolve;});
  if (failure) throw failure;
  return {};
};
"""
            + "function priorityPanel"
            + source.split("function priorityPanel", 1)[1].split("function pendingHandoffs", 1)[0]
            + (WEB / "assistants.js").read_text()
            + (WEB / "ops.js").read_text()
            + r"""
(async () => {
  for (const family of ["priority", "invoke", "procurement"]) {
    for (const outcome of ["committed", "uncertain", "refusal", "transport"]) {
      pathCalls = []; oldReads = [];
      failure = outcome === "transport" ? new TypeError("Connection lost")
        : Object.assign(new Error("Synthetic outcome"), {status: 409,
          ...(outcome === "refusal" ? {} : {outcome})});
      app.children = [];
      caseSession = {pendingFields: new Map()};
      let button;
      if (family === "priority") {
        app.append(priorityPanel()); await tick();
        button = app.querySelectorAll("button").find(b => b.textContent === "Reject");
      } else if (family === "invoke") {
        const panel = assistantCasePanel("SYN", caseSession); panel.isConnected = true;
        app.append(panel); await tick();
        button = app.querySelector("[data-assistant-request]");
      } else {
        await capacityView();
        button = app.querySelectorAll("button").find(b => b.textContent === "Create package");
        app.querySelector("#capacity-field-6").value = "v1";
      }
      let oldView, laterOldView, oldHeading;
      if (family === "procurement") {
        oldHeading = app.children[0];
        deferProcurement = true;
        oldView = capacityView(); laterOldView = capacityView(); await tick();
        deferProcurement = false;
        assert.equal(oldReads.length, 4);
      }
      if (family === "priority") app.querySelector("#pri-why").value = "Keep this reason";
      button.focus();
      const sending = button.events.click(); await tick();
      await button.events.click();
      assert.equal(pathCalls.length, 1, family + " pending");
      finish(); await sending;
      const blocked = outcome !== "refusal";
      const currentButton = family === "priority"
        ? app.querySelectorAll("button").find(b => b.textContent === "Reject") : button;
      assert.equal(currentButton.disabled, blocked, family + "/" + outcome);
      if (family === "priority")
        assert.equal(app.querySelector("#pri-why").value, "Keep this reason");
      if (blocked) {
        await currentButton.events.click();
        assert.equal(pathCalls.length, 1, family + " repeated ambiguous mutation");
      } else {
        const retry = currentButton.events.click(); await tick();
        assert.equal(pathCalls.length, 2, family + " explicit refusal is retryable");
        finish(); await retry;
      }
      if (family === "procurement") {
        oldReads.slice(0, 2).forEach(resolve => resolve([])); await oldView;
        if (blocked) {
          assert.equal(app.children[0], oldHeading, "older procurement GET cannot repaint");
          assert.ok(capacityHistoryBarrier);
          await capacityView();
          assert.equal(capacityHistoryBarrier, null, "fresh resource reads recover procurement");
        }
        const recoveredHeading = app.children[0];
        oldReads.slice(2).forEach(resolve => resolve([])); await laterOldView;
        if (blocked) assert.equal(app.children[0], recoveredHeading,
          "stale procurement read stays stale after recovery");
      }
      if (family === "invoke") {
        const replacement = assistantCasePanel("SYN", caseSession);
        replacement.isConnected = true; app.replaceChildren(replacement); await tick();
        assert.equal(app.querySelector("[data-assistant-request]").disabled, blocked,
          "render-only rebuild must not recover invocation");
      }
    }
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_raw_resident_and_challenge_outcomes_exclude_repeat_posts(self) -> None:
        source = (WEB / "panels.js").read_text()
        app_source = (WEB / "app.js").read_text()
        script = (
            DOM
            + shipped_helpers()
            + "async function api"
            + app_source.split("async function api", 1)[1].split("const fmtDate", 1)[0]
            + r"""
Node.prototype.replaceChildren = function(...children) {
  this.children = []; this.append(...children);
};
Node.prototype.replaceWith = function(node) {
  const parent = this.parentElement, index = parent.children.indexOf(this);
  parent.children[index] = node; node.parentElement = parent;
};
const app = new Node("main"), id = "SYN", targetOptions = {id: "targets"};
document.getElementById = id => app.querySelector("#" + id);
document.querySelectorAll = () => app.querySelectorAll("form")
  .filter(form => form.dataset.challengeCase && form.dataset.unsaved === "true");
const me = {user: {role: "Retrofit Programme Manager"}};
const residentRoles = [me.user.role], routeController = new AbortController();
let requests = 0, outcome, status, finish, reloads = 0;
const refresh = async () => {
  reloads++;
  if (outcome === "reload-failure") {requireCaseHistory(caseSession); return "check-history";}
};
const fetch = async () => {
  requests++;
  await new Promise(resolve => {finish = resolve;});
  return {ok: status === 200, status, json: async () => {
    if (outcome === "malformed") throw new SyntaxError("Malformed response");
    return {outcome, error: "Synthetic outcome"};
  }};
};
"""
            + "function bindCaseMutationForm"
            + source.split("function bindCaseMutationForm", 1)[1].split("function actForm", 1)[0]
            + "function captureChallengeDrafts"
            + source.split("function captureChallengeDrafts", 1)[1].split(
                "function affectedChallengePanel", 1
            )[0]
            + "const residentForm = "
            + source.split("  const residentForm = ", 1)[1].split("  const serviceForm", 1)[0]
            + "const formFor = "
            + source.split("  const formFor = ", 1)[1].split("  const staff", 1)[0]
            + r"""
(async () => {
  for (const challenge of [false, true]) {
    for (status of [200, 409, 503]) {
      for (outcome of ["committed", "uncertain", undefined, "malformed",
        "success", "reload-failure"]) {
        const successful = ["success", "reload-failure"].includes(outcome);
        if (status === 200 && outcome !== "malformed" && !successful) continue;
        if (status !== 200 && successful) continue;
        const reportedStatus = status, reportedOutcome = outcome;
        const expectsHistory = outcome !== undefined && outcome !== "success";
        requests = 0; reloads = 0;
        caseSession = {pendingFields: new Map()};
        const container = challenge
          ? formFor("synthetic", "Record", [["note", "Note"]], body => body)
          : residentForm("synthetic", "Record", [["note", "Note"]], "record");
        const form = container.tagName === "FORM" ? container : container.querySelector("form");
        const input = form.querySelector("input"), button = form.querySelector("button");
        input.value = "Retained supplied evidence"; input.validity = {valid: true};
        const submit = () => form.events.submit({preventDefault() {}});
        const pending = submit();
        const rebuilt = challenge
          ? formFor("synthetic", "Record", [["note", "Note"]], body => body)
          : residentForm("synthetic", "Record", [["note", "Note"]], "record");
        const rebuiltForm = rebuilt.querySelector("form");
        const rebuiltInput = rebuiltForm.querySelector("input");
        rebuiltInput.value = "Later changed evidence"; rebuiltInput.validity = {valid: true};
        rebuiltInput.events.input?.();
        const originalValue = challenge && successful
          ? "Later retained original evidence" : "Retained supplied evidence";
        input.value = originalValue; input.events.input?.();
        rebuiltForm.dataset.unsaved = "true";
        app.replaceChildren(rebuilt);
        const rebuiltSubmit = () => rebuiltForm.events.submit({preventDefault() {}});
        const rebuiltButton = rebuiltForm.querySelector("button");
        assert.equal(rebuiltButton.disabled, true);
        assert.match(rebuiltForm.querySelector("p").textContent, /Recording/);
        assert.equal(requests, 1);
        assert.equal(Boolean(caseSession.historyBarrier), false,
          "pending duplicate is not an uncertain server outcome");
        assert.equal(pendingMutations.size, 1);
        finish(); await pending;
        assert.equal(pendingMutations.size, 0, "including strict JSON parse failure");
        assert.equal(input.value, originalValue);
        assert.equal(rebuiltButton.disabled, expectsHistory);
        assert.equal(Boolean(caseSession.historyBarrier), expectsHistory);
        assert.match(rebuiltForm.querySelector("p").textContent,
          outcome === undefined ? /Synthetic outcome/ : outcome === "success"
            ? challenge ? /Only the submitted values were recorded/ : /Supplied evidence recorded/
            : /Reload and check the history/);
        if (challenge && successful) {
          form.updateMutationState();
          assert.equal(button.disabled, true, "acknowledged retained draft cannot repeat");
          rebuiltForm.updateMutationState();
        }
        if (expectsHistory) {
          await submit(); await rebuiltSubmit(); assert.equal(requests, 1);
          const drafts = challenge ? captureChallengeDrafts(id) : [];
          rebuiltForm.updateMutationState();
          assert.equal(rebuiltButton.disabled, true, "unresolved read cannot unlock");
          delete caseSession.historyBarrier;
          if (challenge) {
            const replacement = formFor("synthetic", "Record", [["note", "Note"]], b => b);
            app.replaceChildren(replacement);
            restoreChallengeDrafts(drafts);
            assert.equal(app.querySelector("form"), rebuiltForm, "whole form is retained");
          } else rebuiltForm.updateMutationState();
          assert.equal(rebuiltButton.disabled, false, "fresh history recovers retained control");
          assert.match(rebuiltForm.querySelector("p").textContent, /Case history reloaded/);
          assert.equal(rebuiltInput.value, "Later changed evidence");
        }
        outcome = undefined; status = 409;
        const retry = rebuiltSubmit(); assert.equal(requests, 2);
        finish(); await retry;
        status = reportedStatus; outcome = reportedOutcome;
        assert.equal(reloads, successful ? 1 : 0);
      }
    }
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_submission_reconciles_semantic_live_recovery_and_cached_values(self) -> None:
        source = (WEB / "app.js").read_text()
        lifecycle = (
            "function captureCaseFields"
            + source.split("function captureCaseFields", 1)[1].split(
                'app.addEventListener("input"', 1
            )[0]
        )
        script = (
            DOM
            + shipped_helpers()
            + lifecycle
            + r"""
const app = new Node("main");
for (const representation of ["original", "live", "recovery", "cache-only", "both"]) {
  for (const type of ["text", "checkbox"]) {
    for (const later of [false, true]) {
      app.children = [];
      caseSession = {pendingFields: new Map()};
      const original = h("input", {id: "original", type,
        "data-case-field-key": "bound:measure:version:item", "data-case-dirty": "true"});
      original.value = type === "checkbox" ? "on" : "Submitted text";
      original.checked = type === "checkbox";
      original.caseBinding = {kind: "checklist", id: "Measure/version"};
      app.append(h("form", {"data-unsaved": "true"}, original));
      const sent = snapshotCaseFields([original]);
      const cached = {key: sent[0].key, value: sent[0].value, checked: sent[0].checked,
        type, label: "Evidence", binding: {kind: "checklist", id: "Measure/version"}};
      caseSession.pendingFields.set(cached.key, cached);
      const unrelated = {...cached, key: "another:version", value: "Unrelated"};
      caseSession.pendingFields.set(unrelated.key, unrelated);
      if (representation !== "original") app.children = [];
      let current = original;
      if (["live", "both"].includes(representation)) {
        current = h("input", {id: "current", type,
          "data-case-field-key": cached.key, "data-case-dirty": "true"});
        current.value = cached.value; current.checked = cached.checked;
        current.caseBinding = original.caseBinding;
        app.append(h("form", {"data-unsaved": "true"}, current));
      }
      if (["recovery", "both"].includes(representation)) {
        const recovery = h("details", {"data-case-recovery": "checklist"});
        const copy = h("textarea", {"data-case-dirty": "true"});
        copy.preservedCaseField = {...cached};
        copy.value = type === "checkbox" ? String(cached.checked) : cached.value;
        recovery.append(h("div", {}, copy)); app.append(recovery);
        if (representation === "recovery") current = copy;
      }
      if (later) {
        if (representation === "cache-only") {
          caseSession.pendingFields.set(cached.key, {...cached,
            value: type === "checkbox" ? "on" : "Submitted text ",
            checked: type === "checkbox" ? false : cached.checked});
        } else if (type === "checkbox") {
          if (current.preservedCaseField) current.preservedCaseField.checked = false;
          else current.checked = false;
        } else current.value += " ";
      }
      reconcileCaseSubmission(sent);
      assert.equal(caseSession.pendingFields.has(unrelated.key), true);
      if (representation !== "cache-only") {
        assert.equal(Boolean(current.dataset.caseDirty), later,
          `${representation}/${type}/${later}`);
        if (later) assert.equal(type === "checkbox"
          ? current.preservedCaseField?.checked ?? current.checked : current.value,
          type === "checkbox" ? false : "Submitted text ");
        else if (!current.preservedCaseField && type === "text") {
          assert.equal(current.value, "");
        }
        if (current.closest("form")) assert.equal(
          Boolean(current.closest("form").dataset.unsaved), later,
          "form-level unsaved markers follow consumed versus later values");
      }
      rememberCaseFields(caseSession);
      assert.equal(caseSession.pendingFields.has(cached.key), later,
        `later draft survives remember/${representation}/${type}/${later}`);
      const replacement = h("section", {});
      restoreBoundFields([cached], replacement, "checklist", caseSession);
      assert.equal(replacement.querySelectorAll("textarea").length, later ? 2 : 1,
        "stale saved array cannot resurrect consumed evidence");
    }
  }
}
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_proposal_validation_pending_refresh_and_success_reload_failure(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const app = new Node("main"), me = {user: {email: "reviewer@example.test"}};
let finish, reject, requests = [], reloadFails = false;
const api = async (path, body) => {
  requests.push(body);
  return await new Promise((resolve, fail) => {finish = resolve; reject = fail;});
};
"""
            + (WEB / "assistants.js").read_text()
            + r"""
(async () => {
  for (const sessionless of [false, true]) {
    for (const outcome of ["success", "refusal", "reload-failure", "uncertain",
      "committed-409", "committed-503", "uncertain-503"]) {
      app.children = []; requests = [];
      caseSession = sessionless ? null : {pendingFields: new Map()};
      const p = {id: `${sessionless}-${outcome}`, revision: 1, case_id: "SYN",
        state: "ready", capability: "assessment-preparation", provenance: [],
        output: {summary: "Synthetic", findings: [], unknowns: []},
        verification: {by: me.user.email}};
      const reload = async () => {if (outcome === "reload-failure")
        throw new Error("Synthetic reload failed");};
      const card = assistantProposal(p, reload); app.append(card);
      const olderRead = new Map(proposalReviewStates);
      const [reason, editing] = card.querySelectorAll("textarea");
      const save = card.querySelectorAll("button")
        .find(button => button.textContent === "Save edited proposal");
      editing.value = "{";
      await save.events.click();
      assert.equal(document.activeElement, reason);
      assert.equal(reason.attrs["aria-invalid"], "true");
      reason.value = "Valid reason";
      await save.events.click();
      assert.equal(document.activeElement, editing);
      assert.equal(editing.attrs["aria-invalid"], "true");
      assert.equal(editing.attrs["aria-describedby"], card.querySelector(".field-error").id);
      assert.equal(reason.attrs["aria-invalid"], undefined);
      assert.equal(requests.length, 0);
      editing.value = JSON.stringify(p.output); editing.events.input();
      assert.equal(editing.attrs["aria-invalid"], undefined);
      reason.dataset.caseDirty = editing.dataset.caseDirty = "true";
      const pending = save.events.click();
      assert.equal(save.disabled, true);
      const replacement = assistantProposal(p, reload); app.children = []; app.append(replacement);
      const next = replacement.querySelectorAll("button")
        .find(button => button.textContent === "Save edited proposal");
      assert.equal(next.disabled, true);
      await next.events.click();
      assert.equal(requests.length, 1, "same-revision rebuilt card cannot resubmit");
      if (outcome === "refusal") reject(Object.assign(new Error("Refused"), {status: 409}));
      else if (outcome === "uncertain") reject(new TypeError("Connection lost"));
      else if (outcome.includes("-")) {
        const [result, status] = outcome.split("-");
        if (result !== "reload") reject(Object.assign(new Error("Check history"),
          {status: Number(status), outcome: result}));
        else finish({});
      }
      else finish({});
      await pending;
      assert.equal(next.disabled, outcome !== "refusal");
      assert.equal(reason.attrs["aria-invalid"], undefined);
      assert.equal(editing.attrs["aria-invalid"], undefined);
      assert.equal(Boolean(reason.dataset.caseDirty),
        outcome !== "success" && outcome !== "reload-failure");
      if (outcome !== "refusal") {
        await next.events.click(); assert.equal(requests.length, 1);
      }
      if (outcome.includes("committed-") || outcome.includes("uncertain")) {
        let rebuilt = assistantProposal(p, reload, olderRead);
        assert.equal(rebuilt.querySelector("fieldset").querySelector("button").disabled, true,
          "pre-outcome listing cannot clear history barrier");
        rebuilt = assistantProposal(p, reload, new Map(proposalReviewStates));
        assert.equal(rebuilt.querySelector("fieldset").querySelector("button").disabled, false,
          "post-outcome authoritative listing can recover same revision");
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

    def test_quality_errors_and_manual_action_pending_siblings(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const app = new Node("main"), HTMLButtonElement = Node;
const me = {user: {role: "Retrofit Programme Manager"}};
const fmtDate = value => value;
let finish, refuse, errors = [], requests = 0;
const api = async () => {
  requests++;
  return await new Promise((resolve, reject) => {finish = resolve; refuse = reject;});
};
const post = (id, name, body) => api(name, body);
const refresh = async fn => {
  try {await fn(); return true;} catch (error) {errors.push(error); return false;}
};
"""
            + (WEB / "ops.js").read_text()
            + (WEB / "panels.js").read_text()
            + r"""
(async () => {
  const c = {closed: true, measures: "Loft insulation", quality: [{
    measure: "Loft insulation", state: "Returned", source: "Installer",
    submitted_by: "Synthetic installer", items: [], aftercare: [], checklist_version: "v1"
  }]};
  const panel = qualityPanel(c, "SYN", refresh); app.append(panel);
  const note = panel.querySelectorAll("input")
    .find(field => field.name === "quality-note-0");
  const button = panel.querySelector("button");
  button.focus();
  await button.events.click();
  assert.equal(document.activeElement, note);
  assert.equal(note.attrs["aria-invalid"], "true");
  assert.equal(note.attrs["aria-describedby"], "quality-feedback-0");
  assert.equal(requests, 0);
  note.value = "Submitted remediation evidence"; note.events.input();
  assert.equal(note.attrs["aria-invalid"], undefined);
  button.focus();
  const pending = button.events.click();
  assert.equal(button.disabled, true);
  note.value = "";  // A later edit must not redirect a server refusal to this field.
  refuse(Object.assign(new Error("Synthetic server refusal"), {status: 409}));
  await pending;
  assert.equal(errors.length, 1);
  assert.equal(note.attrs["aria-invalid"], undefined);
  assert.equal(document.activeElement.attrs.role, "status");
  assert.equal(button.disabled, false);

  for (const outcome of [true, false, "check-history"]) {
    let runs = 0;
    const form = actForm("Synthetic manual action", [["note", "Note"]], async () => {
      runs++; return await new Promise(resolve => {finish = resolve;});
    });
    const submit = form.querySelector("button");
    const saving = submit.events.click();
    assert.equal(submit.disabled, true);
    await submit.events.click();
    assert.equal(runs, 1);
    finish(outcome); await saving;
    assert.equal(submit.disabled, outcome === "check-history");
    assert.equal(submit.attrs["aria-busy"], undefined);
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_file_recovery_and_other_session_are_not_confused_with_submitted_values(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const app = new Node("main");
caseSession = {pendingFields: new Map()};
const original = h("input", {type: "file", "data-case-field-key": "file",
  "data-case-dirty": "true"});
original.files = [{}]; original._value = "same-name.txt";
Object.defineProperty(original, "value", {
  get() {return this._value;},
  set(value) {this._value = value; if (value === "") this.files = [];}
});
app.append(original);
const sent = snapshotCaseFields([original]);
const saved = {key: "file", value: original.value, checked: original.checked,
  type: "file", fileNode: original};
caseSession.pendingFields.set("file", saved);
const recovery = h("details", {"data-case-recovery": "form"});
const copy = h("textarea", {"data-case-dirty": "true"});
copy.preservedCaseField = saved; copy.value = saved.value;
recovery.append(h("div", {}, copy)); app.children = []; app.append(recovery);
reconcileCaseSubmission(sent);
assert.equal(app.querySelectorAll("textarea").length, 0,
  "compare all counterparts before clearing the shared original FileList");
assert.equal(caseSession.pendingFields.size, 0);

const current = h("input", {type: "file", "data-case-field-key": "file",
  "data-case-dirty": "true"});
current.files = [{}]; current.value = "same-name.txt"; app.append(current);
const sameName = snapshotCaseFields([current]);
current.files = [{}];
reconcileCaseSubmission(sameName);
assert.equal(current.dataset.caseDirty, "true", "same name is not the same selected File");

const oldSession = caseSession;
const oldSent = snapshotCaseFields([current]);
caseSession = {pendingFields: new Map([["file", {...saved, value: "Other case"}]])};
const other = h("input", {"data-case-field-key": "file", "data-case-dirty": "true"});
other.value = "Other case"; app.children = []; app.append(other);
reconcileCaseSubmission(oldSent);
assert.equal(other.value, "Other case");
assert.equal(other.dataset.caseDirty, "true");
assert.equal(caseSession.pendingFields.get("file").value, "Other case");
assert.notEqual(caseSession, oldSession);
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_regulatory_answer_releases_form_before_usage_refresh_settles(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const me = {user: {role: "Retrofit Programme Manager"}};
const app = new Node("main");
let answerReady, usageReady, usageFailed, usageRequests;
const api = async path => {
  if (path.endsWith("/status")) return new Promise(() => {});
  if (path.endsWith("/threads")) return {id: "SYN-CHAT"};
  if (path.endsWith("/ask")) return new Promise(resolve => {answerReady = resolve;});
  if (path === "/api/chat/regulatory/usage") {
    usageRequests++;
    return new Promise((resolve, reject) => {usageReady = resolve; usageFailed = reject;});
  }
  throw new Error(`Unexpected request: ${path}`);
};
const tick = () => new Promise(resolve => setImmediate(resolve));
"""
            + (WEB / "chat.js").read_text()
            + r"""
(async () => {
  for (const outcome of ["success", "failure"]) {
    for (const edited of [false, true]) {
      usageRequests = 0;
      const root = regulatoryChatPanel("SYN-208");
      const input = root.querySelector("#regulatory-question");
      const form = root.querySelector("form"), button = form.querySelector("button");
      const status = root.querySelector('[role="status"]');
      const usage = root.querySelector("#regulatory-usage");
      const log = root.querySelector('[aria-label="Cited regulatory turns"]');
      input.value = "Submitted question"; input.dataset.caseDirty = "true";
      let submitted = false;
      const pending = form.events.submit({preventDefault() {}})
        .then(() => {submitted = true;});
      await tick();
      assert.equal(button.disabled, true, "lookup stays disabled while answer is pending");
      if (edited) input.value = "Next question";
      answerReady({reply: "Synthetic answer", kind: "answer", citations: []});
      await tick();
      assert.match(log.textContent, /Submitted question/);
      assert.match(log.textContent, /Synthetic answer/);
      assert.equal(usageRequests, 1, "answer starts the secondary usage read");
      assert.equal(button.disabled, false, "usage must not keep lookup disabled");
      assert.equal(submitted, true, "submit must settle while usage is still pending");
      assert.equal(document.activeElement, input);
      assert.equal(input.value, edited ? "Next question" : "");
      assert.equal(Boolean(input.dataset.caseDirty), edited);
      const answerStatus = status.textContent;
      assert.match(answerStatus, /answer: synthetic-demo turn stored/);
      if (outcome === "failure") usageFailed(new Error("Metering offline"));
      else usageReady({
        role: me.user.role, period: "2026-10-29", recorded_turns: 1,
        outcomes: {answer: 1, refused: 0, conflict: 0}, coverage: "recorded_audit_only"
      });
      await tick();
      await pending;
      assert.match(usage.textContent, outcome === "failure"
        ? /Recorded usage unavailable: Metering offline/ : /1 turns/);
      assert.equal(status.textContent, answerStatus, "usage cannot replace answer success");
      assert.equal(button.disabled, false);
      assert.equal(document.activeElement, input);
      assert.equal(input.value, edited ? "Next question" : "");
      assert.equal(Boolean(input.dataset.caseDirty), edited);
    }
  }
  console.log("PASS");
})().catch(error => {console.error(error); process.exitCode = 1;});
"""
        )
        result = subprocess.run(
            ["node", "--unhandled-rejections=strict", "-e", script],
            text=True,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_both_chat_submissions_clear_only_successful_unchanged_raw_questions(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
Node.prototype.replaceChildren = function(...children) {
  this.children = []; this.append(...children);
};
Node.prototype.insertBefore = function(node, before) {
  const at = this.children.indexOf(before);
  this.children.splice(at < 0 ? this.children.length : at, 0, node);
  if (node.nodeType) node.parentElement = this;
  return node;
};
Node.prototype.contains = function(target) {return target === this || this.all().includes(target);};
document.body = new Node("body");
document.createElementNS = (_, tag) => new Node(tag);
document.getElementById = id => document.body.querySelector("#" + id);
document.addEventListener = document.removeEventListener = () => {};
const window = {}, location = {hash: "#/case/SYN-526"};
document.body.append(h("button", {id: "employee-chat-launcher"}));
const me = {user: {role: "Retrofit Programme Manager"}};
const app = new Node("main");
let finish, fail, requests = [], failure;
const api = async (path, body) => {
  if (path === "/api/assistants") return {assistants: []};
  if (path === "/api/chat/skills") return {skills: []};
  if (path === "/api/chat/status")
    return {warning: "Synthetic privacy warning", retention: "Unknown"};
  if (path.endsWith("/status")) return new Promise(() => {});
  requests.push({path, body});
  if (path === "/api/chat/regulatory/usage") return {
    role: me.user.role, period: "2026-10-29", recorded_turns: 1,
    outcomes: {answer: 1, refused: 0, conflict: 0}, coverage: "recorded_audit_only"
  };
  if (failure === "thread" && path.endsWith("/threads")) throw new Error("Thread failed");
  if (path.endsWith("/threads")) return {id: "SYN-CHAT"};
  return await new Promise((resolve, reject) => {finish = resolve; fail = reject;});
};
"""
            + (WEB / "chat-widget.js").read_text()
            + (WEB / "chat.js").read_text()
            + r"""
(async () => {
  for (const regulatory of [false, true]) {
    for (const change of ["none", "text", "space", "answer-failure", "thread-failure"]) {
      requests = []; failure = change === "thread-failure" ? "thread" : null;
      const panel = chatCasePanel("SYN-526");
      if (!regulatory) await employeeChat.open();
      await new Promise(resolve => setImmediate(resolve));
      const root = regulatory ? panel.querySelector("#regulatory-chat")
        : document.getElementById("employee-chat");
      const input = root.querySelector(regulatory
        ? "#regulatory-question" : "#employee-chat-question");
      const form = root.querySelector("form");
      const button = form.querySelectorAll("button").find(control => control.type === "submit");
      const submit = form.onsubmit || form.events.submit;
      input.value = "  Submitted question  "; input.dataset.caseDirty = "true";
      const event = {preventDefault() {}};
      const pending = submit(event);
      await new Promise(resolve => setImmediate(resolve));
      if (change !== "thread-failure") {
        assert.equal(button.disabled, true);
        const before = requests.length;
        await submit(event);
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
      if (regulatory && !change.endsWith("failure")) {
        assert.equal(requests[2].path, "/api/chat/regulatory/usage");
        assert.match(root.querySelector("#regulatory-usage").textContent, /1 turns/);
      }
      if (!regulatory) employeeChat.reset();
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
            + 'const app = new Node("main");\n'
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
                self.assertEqual(states[index]["blockers"][0]["reason"], "Check evidence")
                self.assertEqual(
                    states[index]["text"], "Current, blocked" if index == 4 else "Blocked"
                )
                self.assertEqual(sum(bool(step["current"]) for step in states), 1)
                self.assertTrue(states[4]["current"])
                self.assertNotEqual(states[0]["state"], "blocked")

    def test_closed_overrides_blockers_unknown_stage_does_not_invent_step(self) -> None:
        states = journey(
            closed=True, work={"blockers": [{"step": "Safety review", "reason": "Check"}]}
        )
        self.assertTrue(all(step["state"] == "done" for step in states))
        self.assertFalse(any(step["current"] for step in states))
        self.assertFalse(any(step["blockers"] for step in states))
        self.assertFalse(any(step["current"] for step in journey(stage="Unknown")))

    def test_journey_icons_are_declared_as_package_data(self) -> None:
        project = WEB.parents[3]
        with (project / "pyproject.toml").open("rb") as stream:
            config = tomllib.load(stream)
        patterns = config["tool"]["setuptools"]["package-data"]["zava_forward.api"]
        for name in ("survey", "assessment", "funding", "resident", "contractor", "quality"):
            with self.subTest(icon=name):
                relative = f"web/journey-icons/{name}.png"
                self.assertTrue((WEB.parent / relative).is_file())
                self.assertTrue(any(Path(relative).match(pattern) for pattern in patterns))

    def test_journey_icons_are_exact_six_step_presentation_assets(self) -> None:
        root = Path(__file__).resolve().parents[3]
        deck = root / "docs/capstone/deck/zava-forward-cowork-v2-draft.pptx"
        icons = evaluate("CaseWorkspace.steps.map(step => step.icon)")
        expected = ["survey", "assessment", "funding", "resident", "contractor", "quality"]
        self.assertEqual(icons, expected)
        with zipfile.ZipFile(deck) as archive:
            for name, number in zip(expected, (11, 6, 12, 13, 14, 15), strict=True):
                icon = (WEB / "journey-icons" / f"{name}.png").read_bytes()
                source = archive.read(f"ppt/media/image{number}.png")
                self.assertEqual(hashlib.sha256(icon).digest(), hashlib.sha256(source).digest())

    def test_blocker_popovers_keep_full_safe_reasons_and_separate_controls(self) -> None:
        script = (
            DOM
            + shipped_helpers()
            + r"""
const app = new Node("main"), aiMode = {workflow: false};
const location = {hash: "#/case/SYN?tab=overview"}, history = {pushState() {}};
const MutationObserver = class {observe() {} disconnect() {}};
const definitions = ["overview", "funding", "ai"].map(id => ({
  id, label: id, panel: h("section", {}, h("h2", {}, id))
}));
const blockers = [
  {step: "Final checks: funding", reason: "Short reason. " + "Long detail. ".repeat(100),
    owner: "Finance", next_action: "Check the evidence."},
  {step: "Final checks: funding", reason: "<script>not executable</script>"}
];
"""
            + (WEB / "case-workspace.js").read_text()
            + r"""
const ui = CaseWorkspace.enhance({id: "SYN", hazards: [], work: {blockers}},
  definitions, null, h("section", {}), h("div", {}));
const root = h("div", {}, ui.top, ui.tabs);
const popups = root.querySelectorAll("[popover]");
assert.equal(popups.length, 2);
assert.equal(new Set(popups.map(node => node.id)).size, 2);
for (const popup of popups) {
  assert.equal(popup.getAttribute("popover"), "auto");
  assert.match(popup.textContent, /Long detail/);
  assert.match(popup.textContent, /Owner not recorded. Ask the case owner./);
  assert.match(popup.textContent, /Ask the case owner to record the next action./);
  assert.equal(popup.querySelectorAll("script").length, 0);
  assert.match(popup.textContent, /<script>not executable<\/script>/);
}
for (const button of root.querySelectorAll("[popovertarget]")) {
  assert.equal(button.tagName, "BUTTON");
  assert.equal(button.closest("a"), null);
}
const summaries = root.querySelectorAll(".case-blocker-summary");
assert.equal(summaries.length, 2);
assert.equal(summaries[0].textContent, "Short reason.");
assert.equal(root.querySelectorAll("img").length, 6);
assert.equal(ui.tabs.getAttribute("role"), "tablist");
console.log("PASS");
"""
        )
        result = subprocess.run(["node", "-e", script], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)

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
const session = {pendingFields: new Map()}, caseSession = session;
const app = {querySelectorAll: () => []};
const caseFieldEntries = () => [];
const msg = {replaceChildren() { errors++; }};
const workspaceStatus = {};
const h = () => ({});
const caseView = async () => { renders++; };
const submitted = {dataset: {caseDirty: "true"},
  removeAttribute() {delete this.dataset.caseDirty;}, closest() {return null;}};
const unrelated = {dataset: {caseDirty: "true"}};
const refresh = """
            + refresh
            + snapshot
            + "function mutationNeedsHistory"
            + app.split("function mutationNeedsHistory", 1)[1].split("async function api", 1)[0]
            + """
(async () => {
  for (const status of [409, 503]) {
    for (const outcome of ["committed", "uncertain"]) {
      let requests = 0;
      const fn = async () => {requests++; throw Object.assign(new Error("Check history"),
        {status, outcome});};
      const result = await refresh(fn, [submitted]);
      if (result !== "check-history") throw new Error("Missing history result");
      await refresh(fn, []);
      submitted.value = "Changed evidence key";
      await refresh(fn, [submitted]);
      if (requests !== 1) throw new Error("Repeated ambiguous mutation");
      if (!session.historyBarrier) throw new Error("Missing case barrier");
      delete session.historyBarrier; session.pendingSubmissions.clear();
    }
  }
  errors = 0;
  await refresh(async () => { throw Object.assign(new Error("Synthetic refusal"),
    {status: 409}); }, [submitted]);
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
    this.dataset = {}; this.value = ""; this.hidden = Boolean(this.attrs.hidden);
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
  closest() {return null;}
  focus() {}
  prepend(node) { this.kids.unshift(node); }
}
const h = (tag, attrs, ...kids) => new Node(tag, attrs, kids);
const app = {dispatchEvent() {}, querySelectorAll: () => []};
const caseSession = null, caseFieldEntries = () => [];
let finish, fail, requests = [], done = [];
const api = async (path, body) => {
  requests.push({path, body});
  await new Promise((resolve, reject) => { finish = resolve; fail = reject; });
};
"""
            + snapshots
            + "function mutationNeedsHistory"
            + source.split("function mutationNeedsHistory", 1)[1].split("async function api", 1)[0]
            + notes
            + r"""
(async () => {
  for (const change of ["none", "text", "reason", "both", "failure",
    "committed", "uncertain", "transport"]) {
    requests = []; done = [];
    const record = {record_id: "SYN-REVIEW", approval: "Not reviewed", text: "Original"};
    const meta = aiNotes(record, (action, text) => done.push({action, text}));
    const editing = meta.querySelectorAll("textarea")
      .find(field => field.attrs.name === "edited-draft");
    const reason = meta.querySelectorAll("textarea")
      .find(field => field.attrs.name === "review-reason");
    const box = meta.querySelector("fieldset"), buttons = box.querySelectorAll("button");
    const editBox = meta.querySelectorAll("div").find(node => node.kids.includes(editing));
    const reasonBox = meta.querySelectorAll("div").find(node => node.kids.includes(reason));
    assert.equal(editBox.hidden, true);
    assert.equal(reasonBox.hidden, true);
    const editButton = buttons.find(button => button.kids.includes("Edit this draft"));
    editButton.attrs.onclick({currentTarget: editButton});
    assert.equal(editBox.hidden, false);
    assert.equal(reasonBox.hidden, false);
    const submit = buttons.find(button => button.textContent === "Save edited draft review");
    editing.value = "Submitted replacement"; reason.value = "Submitted reason";
    editing.dataset.caseDirty = reason.dataset.caseDirty = "true";
    const pending = submit.attrs.onclick();
    assert.equal(buttons.every(button => button.disabled), true);
    await submit.attrs.onclick();
    assert.equal(requests.length, 1, "duplicate dispatch must not issue another review");
    if (["text", "both", "failure"].includes(change)) editing.value = "Newer replacement";
    if (["reason", "both", "failure"].includes(change)) reason.value = "Newer reason";
    if (change === "failure") fail(Object.assign(new Error("Synthetic refusal"),
      {status: 409}));
    else if (["committed", "uncertain", "transport"].includes(change))
      fail(Object.assign(new Error("Check history"),
        change === "transport" ? {} : {status: 503, outcome: change}));
    else finish();
    await pending;
    assert.equal(requests[0].body.text, "Submitted replacement");
    assert.equal(requests[0].body.reason, "Submitted reason");
    if (["failure", "committed", "uncertain", "transport"].includes(change)) {
      assert.equal(record.approval, "Not reviewed");
      assert.equal(editing.dataset.caseDirty, "true");
      assert.equal(reason.dataset.caseDirty, "true");
      assert.equal(buttons.some(button => button.disabled), change !== "failure");
      assert.equal(reason.attrs["aria-invalid"], undefined,
        "server refusal is not invalid Reason");
      assert.equal(editing.attrs["aria-invalid"], undefined);
      assert.equal(done.length, 0);
      if (change !== "failure") {
        await submit.attrs.onclick();
        assert.equal(requests.length, 1, "ambiguous draft review cannot retry");
      }
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
      assert.equal(editBox.hidden, !["text", "both"].includes(change));
      assert.equal(reasonBox.hidden, !["reason", "both"].includes(change));
      assert.match(box.querySelector("legend").textContent, /reviewed record SYN-REVIEW/);
    }
    await buttons.find(button => button.kids.includes("Use this draft")).attrs.onclick();
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
