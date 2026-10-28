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
    document, AbortController, clearTimeout,
    setTimeout: (callback, delay) => {
      delays.push(delay);
      return setTimeout(callback, delay === 5000 ? 5 : 0);
    },
    me: {user: {role: "Retrofit Programme Manager"}, navigation: []},
    workspaceStatus: {textContent: ""},
    location: {hash: "#/overview"}, displayedHash: "#/overview",
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

  h = harness(["ready"]);
  const signedOut = h.run("route()");
  h.context.me = null;
  h.context.routeController.abort();
  await signedOut;
  assert.deepEqual(h.views, [], "signed-out route must not render");
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
