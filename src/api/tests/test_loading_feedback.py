"""Execute the shared async helper's lifecycle with a controlled clock."""

import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class LoadingFeedback(unittest.TestCase):
    def test_actual_helper_timing_duplicates_errors_and_state_ownership(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
let now = 0, clock = [], observer;
class Node {
  constructor(tag = "BUTTON") {
    this.tagName = tag; this.attrs = {}; this.children = [];
    this.isConnected = true; this.textContent = "Save"; this._disabled = false;
    this.classList = {add: value => {this.error = value;}};
  }
  get disabled() {return this._disabled;}
  set disabled(value) {this._disabled = value; observer?.notify(this);}
  setAttribute(name, value) {this.attrs[name] = value;}
  getAttribute(name) {return this.attrs[name] ?? null;}
  removeAttribute(name) {delete this.attrs[name];}
  append(node) {this.children.push(node); node.parentElement = this;}
  prepend(node) {this.children.unshift(node);}
  after(node) {this.children.push(node); node.parentElement = this.parentElement;}
  remove() {this.isConnected = false;}
  querySelector(selector) {return this.children.find(n => selector.startsWith("button")
    ? n.tagName === "BUTTON" : n.className === "async-spinner");}
}
class Observer {
  constructor(callback) {this.callback = callback; this.records = []; observer = this;}
  observe(node) {this.node = node;}
  notify(node) {if (node === this.node) this.records.push({});}
  takeRecords() {return this.records;}
  disconnect() {observer = null;}
}
const context = vm.createContext({
  document: {createElement: tag => new Node(tag), getElementById: () => null},
  MutationObserver: Observer,
  setTimeout: (callback, delay) => {
    const t = {at: now + delay, callback}; clock.push(t); return t;
  },
  clearTimeout: timer => {clock = clock.filter(t => t !== timer);}
});
vm.runInContext(fs.readFileSync(process.argv[1] + "/async-action.js", "utf8"), context);
const helper = vm.runInContext("AsyncAction", context);
function tick(ms) {
  now += ms;
  for (const timer of [...clock]) if (timer.at <= now) {
    clock = clock.filter(t => t !== timer); timer.callback();
  }
}
(async () => {
  const control = new Node();
  let release, calls = 0;
  const task = () => {calls++; return new Promise(resolve => {release = resolve;});};
  const first = helper.run(control, task, "Saving");
  assert.equal(control.disabled, true);
  assert.equal(control.getAttribute("aria-busy"), "true");
  const status = control.children[0];
  assert.equal(status.textContent, "Saving: working...");
  assert.equal(status.attrs["aria-live"], "polite");
  assert.equal(status.children.length, 0);
  tick(199);
  assert.equal(status.children.length, 0, "spinner must not appear before 200ms");
  tick(1);
  assert.equal(status.children.length, 1, "spinner appears at 200ms");
  assert.equal(helper.run(control, task), first);
  assert.equal(calls, 1);
  release("saved");
  assert.equal(await first, "saved");
  assert.equal(control.disabled, false);
  assert.equal(control.getAttribute("aria-busy"), null);
  assert.equal(clock.length, 0);
  assert.equal(status.isConnected, false);
  await helper.run(control, () => Promise.reject(new Error("Synthetic failure")), "Saving");
  assert.equal(control.disabled, false);
  assert.match(control.children.at(-1).textContent, /Synthetic failure.*Try again/);
  await helper.run(control, async () => {await Promise.resolve(); control.disabled = true;});
  assert.equal(control.disabled, true, "never override action-owned permanent refusal");
  const guarded = new Node();
  const guardedAction = helper.run(guarded, () => {
    guarded.setAttribute("aria-disabled", "true");
    return new Promise(resolve => {release = resolve;});
  });
  assert.equal(guarded.disabled, false,
    "preserve focusable action-owned aria-disabled controls");
  assert.equal(guarded.getAttribute("aria-busy"), "true");
  release(); await guardedAction;
  assert.equal(guarded.disabled, false);
  assert.equal(guarded.getAttribute("aria-disabled"), "true");
  const quick = new Node();
  await helper.run(quick, async () => 1);
  tick(200);
  assert.equal(quick.children[0].children.length, 0, "completed timer is cancelled");
  const parent = new Node("DIV"), form = new Node("FORM"), submit = new Node();
  parent.append(form); form.append(submit);
  const formAction = helper.run(form,
    () => new Promise(resolve => {release = resolve;}), "Submitting");
  const formStatus = form.children.find(node => node.className === "async-feedback");
  assert.equal(form.getAttribute("aria-busy"), "true");
  assert.equal(formStatus.parentElement, parent,
    "form status stays outside the busy form");
  assert.equal(submit.disabled, true);
  release(); await formAction;
  assert.equal(submit.disabled, false);
  for (const before of [null, "false"]) {
    const managed = new Node();
    if (before !== null) managed.setAttribute("aria-busy", before);
    const managedAction = helper.run(managed, async () => {
      managed.disabled = true;
      managed.setAttribute("aria-busy", "true");
      try {await new Promise(resolve => {release = resolve;});}
      finally {
        managed.disabled = false;
        managed.removeAttribute("aria-busy");
      }
      throw new Error("Recoverable handler failure");
    }, "Recording");
    assert.equal(managed.getAttribute("aria-busy"), "true");
    release(); await managedAction;
    assert.equal(managed.disabled, false);
    assert.equal(managed.getAttribute("aria-busy"), before,
      "restore the pre-handler state, not the handler's temporary busy value");
    assert.match(managed.children.at(-1).textContent, /Recoverable handler failure/);
    let retried = false;
    await helper.run(managed, async () => {retried = true;});
    assert.equal(retried, true);
    assert.equal(managed.getAttribute("aria-busy"), before);
    assert.equal(managed.children.filter(node =>
      node.className === "async-feedback" && node.isConnected).length, 0,
      "successful retry must remove the earlier error");
  }
  const connected = node => node.children.filter(child =>
    child.className === "async-feedback" && child.isConnected);
  for (const useRegion of [false, true]) {
    const retry = new Node(), region = useRegion ? new Node("DIV") : null;
    const host = region || retry;
    const inline = new Node("P"); inline.textContent = "Handler-owned error";
    host.append(inline);
    await helper.run(retry, () => Promise.reject(new Error("First failure")), "Save", region);
    assert.equal(connected(host).length, 1);
    let settle;
    const attempt = helper.run(retry,
      () => new Promise(resolve => {settle = resolve;}), "Retry", region);
    assert.equal(connected(host).length, 1, "replace only previous helper feedback");
    assert.equal(connected(host)[0].textContent, "Retry: working...");
    assert.equal(helper.run(retry, () => {throw new Error("Duplicate ran");}), attempt);
    assert.equal(connected(host).length, 1, "overlap keeps original pending status");
    settle(); await attempt;
    assert.equal(connected(host).length, 0, "reject then succeed leaves no stale error");
    await helper.run(retry, () => Promise.reject(new Error("Latest failure")), "Save", region);
    assert.equal(connected(host).length, 1, "succeed then fail has one current error");
    assert.match(connected(host)[0].textContent, /Latest failure/);
    await helper.run(retry, () => {throw new Error("Synchronous failure");}, "Save", region);
    assert.equal(connected(host).length, 1);
    assert.match(connected(host)[0].textContent, /Synchronous failure/);
    assert.equal(helper.run(retry, () => 42, "Save", region), 42);
    assert.equal(connected(host).length, 0, "sync success clears previous sync error");
    await helper.run(retry, () => Promise.reject(new Error("Before abort")), "Save", region);
    await helper.run(retry, () => Promise.reject(
      Object.assign(new Error("Cancelled"), {name: "AbortError"})), "Save", region);
    assert.equal(connected(host).length, 0, "abort clears only its replaced attempt");
    assert.equal(inline.isConnected, true);
    assert.equal(inline.textContent, "Handler-owned error");
  }
  for (const controls of [[new Node(), new Node()], [null, null]]) {
    const region = new Node("DIV");
    let rejectFirst, finishSecond;
    const first = helper.run(controls[0],
      () => new Promise((_resolve, reject) => {rejectFirst = reject;}), "First", region);
    const second = helper.run(controls[1],
      () => new Promise(resolve => {finishSecond = resolve;}), "Second", region);
    assert.equal(connected(region).length, 2, "independent attempts have independent notices");
    finishSecond(); await second;
    assert.equal(connected(region).length, 1, "later success cannot remove pending first");
    assert.equal(connected(region)[0].textContent, "First: working...");
    rejectFirst(new Error("First failed")); await first;
    assert.equal(connected(region).length, 1);
    assert.match(connected(region)[0].textContent, /First failed/);
    await helper.run(controls[1], async () => {}, "Third", region);
    assert.equal(connected(region).length, 1, "other success cannot clear first error");
  }
  tick(200);
  assert.equal(clock.length, 0, "settled/replaced attempts leave no spinner timers");
  console.log("PASS actual helper");
})().catch(error => {console.error(error); process.exitCode = 1;});
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS actual helper", result.stdout)


class ChecklistLoading(unittest.TestCase):
    def test_empty_measures_replace_the_loading_status(self) -> None:
        source = (WEB / "ops.js").read_text(encoding="utf-8")
        branch = source.split('api("/api/checklists")', 1)[1].split(".catch", 1)[0]
        self.assertIn("if (measures.length) paint();", branch)
        self.assertIn("no measures to check yet", branch)


class BriefingFeedbackGuidance(unittest.TestCase):
    def test_briefing_says_how_to_correct_and_give_feedback(self) -> None:
        source = (WEB / "app.js").read_text(encoding="utf-8")
        self.assertIn("data-briefing-feedback", source)
        self.assertIn("If review controls are shown, choose Edit this draft", source)
        self.assertIn("is unavailable, or the review is already recorded", source)
        self.assertIn(
            "may reuse the cached draft for an unverified briefing with unchanged records", source
        )
        self.assertIn(
            "Use rules and templates, without AI, or continue with ordinary case work", source
        )
        self.assertIn("kept in the audit log as feedback", source)
