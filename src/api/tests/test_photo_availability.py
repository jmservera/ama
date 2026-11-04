"""Issue 954: the photo service flag is re-evaluated without a reload and 503/403 stay quiet."""

import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const src = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const head = src.slice(src.indexOf("let photoUrl"), src.indexOf("const STARTUP_RETRY_DELAYS"));
const decl = head.split("\n").filter(l => /^(let photo|const PHOTO_)/.test(l)).join("\n");
const fns = head.slice(head.indexOf("async function loadPhoto"));

const els = {};
const el = id => (els[id] ??= {hidden: false, textContent: "", removeAttribute() {}});
let calls = [], listener = null, now = 1_000_000;
const responses = {};
const respond = path => {
  const r = responses[path].shift() ?? responses[path].at(-1);
  return {
    status: r.status, ok: r.status < 400,
    json: async () => r.body ?? {}, blob: async () => "blob",
  };
};
const context = vm.createContext({
  document: {
    getElementById: el, visibilityState: "visible",
    addEventListener: (name, fn) => { if (name === "visibilitychange") listener = fn; },
  },
  URL: {createObjectURL: () => "blob:x", revokeObjectURL() {}},
  Date: {now: () => now},
  fetch: async path => { calls.push(path); return respond(path); },
  fetchReadRetrying: async path => { calls.push(path); return respond(path); },
});
vm.runInContext(
  'let me = null; let microsoftSignIn = true;\n' + decl + "\n" + fns +
  "\nfunction setMe(v) { me = v; }\nfunction getMe() { return me; }", context);
const flush = () => new Promise(r => setImmediate(r));
const photoCalls = () => calls.filter(c => c === "/api/account/photo").length;
const run = code => vm.runInContext(code, context);

(async () => {
  const account = {name: "A B"};
  run("setMe")({account, services: {photo: false}});

  // Flag false: no photo request at all, so the console stays quiet.
  await run("loadPhoto")(account);
  assert.equal(photoCalls(), 0);

  // Availability changes: a return to the tab re-evaluates /api/me and loads the photo.
  responses["/api/me"] = [{status: 200, body: {services: {photo: true}}}];
  responses["/api/account/photo"] = [{status: 200}];
  listener(); await flush(); await flush();
  assert.equal(run("getMe")().services.photo, true);
  assert.equal(photoCalls(), 1);
  assert.equal(el("account-photo").hidden, false);
  assert.equal(el("photo-status").textContent, "Microsoft profile photo");

  // A predictable 503 flips the flag off without a thrown error and is not retried.
  vm.runInContext("photoUrl = null;", context);
  run("getMe")().services.photo = true;
  responses["/api/account/photo"] = [{status: 503}];
  await run("loadPhoto")(account);
  assert.equal(run("getMe")().services.photo, false);
  assert.match(el("photo-status").textContent, /not available/);
  const before = photoCalls();

  // Within the re-check interval nothing is fetched; afterwards the next check can recover.
  listener(); await flush();
  assert.equal(photoCalls(), before);
  now += 61000;
  responses["/api/me"] = [{status: 200, body: {services: {photo: true}}}];
  responses["/api/account/photo"] = [{status: 200}];
  listener(); await flush(); await flush();
  assert.equal(photoCalls(), before + 1);
  assert.equal(run("getMe")().services.photo, true);

  // A failed /api/me re-check is silent and keeps the current state.
  vm.runInContext("photoUrl = null;", context);
  now += 61000;
  responses["/api/me"] = [{status: 500}];
  listener(); await flush();
  assert.equal(run("getMe")().services.photo, true);
  console.log("ok");
})().catch(e => { console.error(e); process.exit(1); });
"""


class PhotoAvailability(unittest.TestCase):
    def test_flag_refreshes_without_reload_and_predictable_denials_are_quiet(self) -> None:
        result = subprocess.run(
            ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=60
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
