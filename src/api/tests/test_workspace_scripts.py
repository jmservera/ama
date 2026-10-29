"""Exercise the actual workspace loader and route guard with Node's VM."""

import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class WorkspaceScripts(unittest.TestCase):
    def test_law_helper_failure_renders_native_reload_before_reads(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(process.argv[1] + "/law.js", "utf8");
for (const state of ["absent", "null", "empty", "handler-only", "run-only",
  "bad-handler", "bad-run"]) {
  let reloads = 0, reads = 0, helperBindings = 0;
  const element = tag => ({tag, attrs: {}, children: [], listeners: {},
    setAttribute(name, value) {this.attrs[name] = value;},
    addEventListener(name, callback) {this.listeners[name] = callback;},
    replaceChildren(...children) {this.children = children;},
    focus() {this.focused = true;}});
  const out = element("div"), status = element("p"), form = element("form");
  const controls = [element("input"), element("button"), element("button")];
  form.querySelectorAll = () => controls;
  const nodes = {"law-out": out, "law-status": status, "law-form": form,
    "law-q": controls[0], "law-all": controls[2]};
  const context = vm.createContext({
    document: {getElementById: id => nodes[id], createElement: element},
    location: {reload() {reloads++;}},
    fetch() {reads++; throw new Error("No read before helper readiness");}
  });
  const handler = () => {helperBindings++; throw new Error("Unready helper called");};
  if (state !== "absent") context.AsyncAction = state === "null" ? null
    : state === "empty" ? {}
    : state === "handler-only" ? {handler}
    : state === "run-only" ? {run: handler}
    : state === "bad-handler" ? {handler: true, run: handler}
    : {handler, run: true};
  assert.doesNotThrow(() => vm.runInContext(source, context), state);
  assert.equal(reads, 0, state);
  assert.equal(helperBindings, 0, state);
  assert.match(status.textContent, /Required law viewer file did not load: \/async-action.js/,
    state);
  assert.ok(out.focused, state);
  const reload = out.children.find(node => node.tag === "button");
  assert.ok(reload, state);
  assert.equal(reload.type, "button", state);
  assert.equal(reload.textContent, "Reload law viewer", state);
  assert.equal(typeof reload.listeners.click, "function", state);
  reload.listeners.click();
  assert.equal(reloads, 1, state);
  assert.ok(controls.every(control => control.disabled), state);
  let prevented = false;
  form.listeners.submit({preventDefault() {prevented = true;}});
  assert.ok(prevented, state);
}
console.log("PASS law helper failure and native reload");
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS law helper failure", result.stdout)

    def test_terminal_startup_renders_native_reload_with_unready_helper(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const factory = source.slice(source.indexOf("function h("),
  source.indexOf("function mutationNeedsHistory"));
const failure = source.slice(source.indexOf("function startupFailed("),
  source.indexOf("bootstrapWorkspace().catch"));
for (const state of ["absent", "null", "empty", "non-callable", "ready"]) {
  const elements = [], events = [], views = [];
  let reloads = 0, wraps = 0;
  const document = {
    createElement(tag) {
      const element = {tag, attrs: {}, children: [], listeners: {},
        setAttribute(name, value) {this.attrs[name] = value;},
        addEventListener(name, callback) {this.listeners[name] = callback;},
        append(child) {this.children.push(child);}};
      elements.push(element);
      return element;
    },
    createTextNode: text => ({nodeType: 3, textContent: text}),
    dispatchEvent: event => events.push(event.type)
  };
  const context = vm.createContext({document, Event, workspaceStatus: {textContent: ""},
    location: {reload() {reloads++;}}, show: (...nodes) => views.push(nodes)});
  if (state !== "absent") context.AsyncAction = state === "null" ? null
    : state === "empty" ? {}
    : state === "non-callable" ? {handler: true}
    : {handler: callback => {wraps++; return callback;}};
  vm.runInContext(factory + failure, context);
  vm.runInContext(`startupFailed({message: "Synthetic helper unavailable",
    reloadWorkspace: true})`, context);
  assert.equal(views.length, 1, state);
  const [heading, alert, reload] = views[0];
  const text = node => node.children.map(child => child.textContent).join("");
  assert.equal(text(heading), "Workspace unavailable", state);
  assert.equal(alert.attrs.role, "alert", state);
  assert.match(text(alert), /Synthetic helper unavailable/, state);
  assert.equal(context.workspaceStatus.textContent,
    "Workspace unavailable: Synthetic helper unavailable", state);
  assert.deepEqual(events, ["workspace-ready"], state);
  assert.equal(reload.tag, "button", state);
  assert.equal(reload.attrs.type, "button", state);
  assert.equal(text(reload), "Reload workspace", state);
  assert.equal(typeof reload.listeners.click, "function", state);
  reload.listeners.click();
  assert.equal(reloads, 1, state);
  assert.equal(wraps, state === "ready" ? 1 : 0, state);
}
console.log("PASS actual terminal renderer and native reload");
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS actual terminal renderer", result.stdout)

    def test_retry_contracts_and_route_isolation(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const loader = source.slice(source.indexOf("const workspaceScriptLoads"),
  source.indexOf("const defaultListState"));
const message = path => `Required workspace files did not load: ${path}. Reload this page`
  + " to try again. If this continues, ask application support to check these files.";

function harness(outcomes = []) {
  const requests = [], delays = [], removed = [], views = [], listeners = [];
  let context;
  const document = {
    createElement: () => ({remove() {removed.push(this);}}),
    head: {append(script) {
      requests.push(script.src);
      const outcome = outcomes.shift() || "error";
      if (outcome === "timeout") return;
      queueMicrotask(() => {
        if (outcome === "unready") context.AsyncAction = {};
        if (outcome === "null") context.AsyncAction = null;
        if (outcome.startsWith("partial-")) {
          context.AsyncAction = {handler: task => task, run() {}, feedback() {}};
          context.AsyncAction[outcome.slice(8)] = true;
        }
        if (outcome === "ready") {
          if (script.src === "/async-action.js") {
            context.AsyncAction = {handler: task => task, run() {}, feedback() {}};
          }
          else if (script.src === "/vendor/leaflet.js") context.L = {};
          else if (script.src === "/role-screens.js") {
            context.roleScreensView = async () => views.push("screens");
          }
          else context.qualityPanel = () => {};
        }
        const handler = outcome === "error" ? script.onerror : script.onload;
        if (handler) handler();
      });
    }},
    querySelector: () => null,
    querySelectorAll: () => [],
    getElementById: id => ({addEventListener: (event, handler) =>
      listeners.push({id, event, handler})})
  };
  context = vm.createContext({
    document, AbortController, URLSearchParams, clearTimeout,
    setTimeout: (callback, delay) => {
      delays.push(delay);
      return setTimeout(callback, delay === 5000 ? 5 : 0);
    },
    me: {user: {role: "Retrofit Programme Manager"}, navigation: []},
    workspaceStatus: {textContent: ""},
    location: {hash: "#/overview"}, displayedHash: "#/overview",
    caseSession: null, fundingAi: {},
    rememberCaseFields: session => Array.from(session.pendingFields.values()),
    window: {confirm: () => false},
    history: {replaceState: (_state, _title, hash) => {context.location.hash = hash;}},
    routeController: new AbortController(), searchTimer: 0,
    coordinatorOrigin: null, queueOrigin: "mine",
    AsyncAction: {handler: task => task, run() {}, feedback() {}},
    qualityPanel() {}, financePanel() {}, assistantCasePanel() {}, chatCasePanel() {},
    timeView() {}, roleScreensView() {},
    overviewView: async () => views.push("overview"),
    listView: async () => views.push("list"),
    show: () => views.push("error"), h: () => ({})
  });
  vm.runInContext(loader, context);
  return {context, requests, delays, removed, views, listeners,
    run: expression => vm.runInContext(expression, context)};
}

(async () => {
  for (const hash of ["#/overview", "#/case/ZF-1", "#/screens"]) {
    let bootstrap = harness(["ready"]);
    bootstrap.context.me = null;
    for (const global of ["qualityPanel", "financePanel", "assistantCasePanel",
      "chatCasePanel", "timeView", "roleScreensView"]) delete bootstrap.context[global];
    assert.deepEqual(Array.from(bootstrap.run(
      `missingWorkspaceScripts("${hash}", ${hash.includes("/case/")})`)), []);
    delete bootstrap.context.AsyncAction;
    assert.deepEqual(Array.from(bootstrap.run(
      `missingWorkspaceScripts("${hash}", ${hash.includes("/case/")})`)),
      ["/async-action.js"], "pre-session deep links only require the helper");
    await bootstrap.run('requireWorkspaceScripts("", false)');
    assert.deepEqual(bootstrap.requests, ["/async-action.js"]);
    assert.equal(bootstrap.run("typeof AsyncAction"), "object");
    for (const outcomes of [["error", "error"], ["load"], ["timeout"], ["unready"]]) {
      bootstrap = harness([...outcomes]);
      bootstrap.context.me = null;
      delete bootstrap.context.AsyncAction;
      await assert.rejects(bootstrap.run('requireWorkspaceScripts("", false)'),
        error => error.message === message("/async-action.js") && error.reloadWorkspace);
      await assert.rejects(bootstrap.run('requireWorkspaceScripts("", false)'));
      assert.equal(bootstrap.requests.length, outcomes.length,
        "null session still checks readiness and retains terminal retry budget");
    }
  }
  for (const outcomes of [["ready"], ["error", "ready"], ["error", "error"],
    ["load"], ["timeout"], ["unready"], ["null"],
    ["partial-handler"], ["partial-run"], ["partial-feedback"]]) {
    const bootstrap = harness([...outcomes]);
    bootstrap.context.me = null;
    if (outcomes.includes("unready")) bootstrap.context.AsyncAction = {};
    else delete bootstrap.context.AsyncAction;
    bootstrap.context.start = async () => bootstrap.views.push("start");
    bootstrap.context.signOut = async switchAccount => bootstrap.views.push(switchAccount);
    bootstrap.run(source.slice(source.indexOf("async function bootstrapWorkspace"),
      source.indexOf('document.querySelector(".skip-link")')));
    const started = bootstrap.run("bootstrapWorkspace()");
    assert.equal(bootstrap.listeners.length, 0, "no listeners before helper readiness");
    assert.deepEqual(bootstrap.views, [], "no API start before helper readiness");
    if (outcomes.includes("ready")) {
      await started;
      assert.deepEqual(bootstrap.views, ["start"]);
      assert.deepEqual(bootstrap.listeners.map(({id}) => id), ["signout", "switch-account"]);
      await bootstrap.listeners[0].handler();
      await bootstrap.listeners[1].handler();
      assert.deepEqual(bootstrap.views, ["start", false, true]);
    } else {
      await assert.rejects(started, error => error.reloadWorkspace);
      assert.equal(bootstrap.listeners.length, 0);
      assert.deepEqual(bootstrap.views, [], "terminal bootstrap must not start the workspace");
    }
  }
  let h = harness(["ready"]);
  await h.run('requireWorkspaceScripts("#/overview", false)');
  assert.deepEqual(h.requests, ["/vendor/leaflet.js"]);
  assert.deepEqual(h.delays, [250, 5000]);
  assert.equal(h.removed.length, 1);
  assert.equal(h.removed[0].onload, null);
  assert.equal(h.removed[0].onerror, null);
  await h.run('requireWorkspaceScripts("#/overview", false)');
  assert.equal(h.requests.length, 1, "healthy dependencies must not reload");

  h = harness(["error", "ready"]);
  await h.run('requireWorkspaceScripts("#/overview", false)');
  assert.equal(h.requests.length, 2);
  assert.deepEqual(h.delays, [250, 5000, 500, 5000]);
  assert.equal(h.removed.length, 2);

  h = harness(["error", "error", "ready"]);
  await assert.rejects(h.run('requireWorkspaceScripts("#/overview", false)'),
    error => error.message === message("/vendor/leaflet.js") && error.reloadWorkspace);
  await assert.rejects(h.run('requireWorkspaceScripts("#/overview", false)'));
  assert.equal(h.requests.length, 2, "exhaustion must survive route revisits");

  for (const outcome of ["timeout", "load"]) {
    h = harness([outcome, "ready"]);
    await assert.rejects(h.run('requireWorkspaceScripts("#/overview", false)'),
      error => error.message === message("/vendor/leaflet.js") && error.reloadWorkspace);
    assert.equal(h.requests.length, 1, "no reinjection after uncertain execution");
    assert.equal(h.removed.length, 1);
    await assert.rejects(h.run('requireWorkspaceScripts("#/overview", false)'));
    assert.equal(h.requests.length, 1, "terminal attempt remains cached");
  }

  h = harness(["ready"]);
  await Promise.all([h.run('requireWorkspaceScripts("#/overview", false)'),
    h.run('requireWorkspaceScripts("#/coordinator", false)')]);
  assert.equal(h.requests.length, 1, "concurrent routes share recovery");

  h = harness(["ready"]);
  h.context.L = {};
  delete h.context.qualityPanel;
  await h.run('requireWorkspaceScripts("#/capacity", false)');
  assert.deepEqual(h.requests, ["/ops.js"]);

  const cases = [
    ["#/case/ZF-1", true, "Retrofit Programme Manager",
      ["/ops.js", "/panels.js", "/assistants.js", "/chat.js"]],
    ["#/capacity", false, "Retrofit Programme Manager", ["/ops.js"]],
    ["#/finance", false, "Retrofit Programme Manager", ["/panels.js"]],
    ["#/assistants", false, "Retrofit Programme Manager", ["/assistants.js"]],
    ["#/time", false, "Retrofit Programme Manager", ["/timecapture.js"]],
    ["#/screens?screen=example", false, "Retrofit Programme Manager", ["/role-screens.js"]],
    ["#/overview", false, "Retrofit Programme Manager", ["/vendor/leaflet.js"]],
    ["#/coordinator?area=example", false, "Retrofit Programme Manager", ["/vendor/leaflet.js"]],
    ["#/", false, "Contractor", ["/ops.js"]],
    ["#/case/ZF-1", true, "Contractor", []],
    ["#/screens", false, "Contractor", ["/role-screens.js"]],
    ["#/", false, "Retrofit Programme Manager", []]
  ];
  for (const [hash, caseRoute, role, expected] of cases) {
    h = harness();
    for (const global of ["qualityPanel", "financePanel", "assistantCasePanel",
      "chatCasePanel", "timeView", "roleScreensView"]) delete h.context[global];
    h.context.me.user.role = role;
    assert.deepEqual(Array.from(h.run(
      `missingWorkspaceScripts(${JSON.stringify(hash)}, ${caseRoute})`)), expected);
  }

  h = harness(["ready"]);
  const old = h.run("route()");
  h.context.location.hash = "#/";
  await h.run("route()");
  await old;
  assert.deepEqual(h.views, ["list"], "obsolete route must not render");

  h = harness(["error", "error"]);
  const failure = h.run("route()");
  h.context.location.hash = "#/";
  await h.run("route()");
  await failure;
  assert.deepEqual(h.views, ["list"], "obsolete error must not render");

  for (const hash of ["#/overview", "#/screens"]) {
    for (const outcome of ["ready", "error", "timeout", "load"]) {
      for (const replacement of [null, {user: {role: "Contractor"}, navigation: []}]) {
        h = harness([outcome, outcome]);
        h.context.location.hash = hash;
        delete h.context.roleScreensView;
        const staleSession = h.run("route()");
        h.context.me = replacement;
        h.context.workspaceStatus.textContent = replacement ? "New session" : "";
        assert.equal(h.context.routeController.signal.aborted, false);
        await staleSession;
        assert.deepEqual(h.views, [], "ended or replaced session must not dispatch");
        assert.equal(h.context.workspaceStatus.textContent, replacement ? "New session" : "",
          "stale session must not restore status or render an error");
        assert.equal(h.context.routeController.signal.aborted, false,
          "session isolation must not depend on an artificial route abort");
      }
    }
  }
  h = harness();
  h.context.me = null;
  await h.run("route()");
  assert.deepEqual(h.views, [], "no-session route entry must be harmless");

  h = harness();
  const selected = [];
  h.context.caseSession = {id: "ZF-1", pendingFields: new Map([["draft", {value: "Unsent"}]]),
    controller: {select: value => selected.push(value)}};
  h.context.displayedHash = "#/case/ZF-1?challenge-target-history=2&tab=ai";
  h.context.location.hash = "#/case/ZF-1?challenge-target-history=2&tab=survey";
  await h.run("route()");
  assert.deepEqual(selected, ["survey"], "pending-only drafts must allow retained tab changes");
  assert.equal(h.context.caseSession.pendingFields.size, 1);
  h.context.location.hash = "#/";
  await h.run("route()");
  assert.equal(h.context.location.hash, h.context.displayedHash,
    "pending-only drafts must warn and restore the previous URL on cancellation");
  assert.deepEqual(h.views, [], "cancelled navigation must not redraw");
  assert.equal(h.run("hasUnsavedChanges()"), true);
  h.context.caseSession.pendingFields.clear();
  assert.equal(h.run("hasUnsavedChanges()"), false, "clean cache must not warn");
  console.log("PASS recovery, bounds, timeout, readiness, route predicates and isolation");
})().catch(error => {console.error(error); process.exitCode = 1;});
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS recovery", result.stdout)


if __name__ == "__main__":
    unittest.main()
