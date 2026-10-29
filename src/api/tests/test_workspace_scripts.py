"""Exercise the actual workspace loader and route guard with Node's VM."""

import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class WorkspaceScripts(unittest.TestCase):
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
  const requests = [], delays = [], removed = [], views = [];
  let context;
  const document = {
    createElement: () => ({remove() {removed.push(this);}}),
    head: {append(script) {
      requests.push(script.src);
      const outcome = outcomes.shift() || "error";
      if (outcome === "timeout") return;
      queueMicrotask(() => {
        if (outcome === "ready") {
          if (script.src === "/vendor/leaflet.js") context.L = {};
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
    querySelectorAll: () => []
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
    qualityPanel() {}, financePanel() {}, assistantCasePanel() {}, chatCasePanel() {},
    timeView() {}, roleScreensView() {},
    overviewView: async () => views.push("overview"),
    listView: async () => views.push("list"),
    show: () => views.push("error"), h: () => ({})
  });
  vm.runInContext(loader, context);
  return {context, requests, delays, removed, views,
    run: expression => vm.runInContext(expression, context)};
}

(async () => {
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
