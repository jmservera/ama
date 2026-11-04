"""Run the shipped resident page script with Node and prove it promises only what is connected.

Refs #1053: with no callback agenda the signed-in page must not invite callback booking.
The script is executed unchanged against a small fake DOM; the view comes from the real demo.
"""

import json
import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Any

from test_resident_demo_api import DemoTestCase

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/resident_demo/web"

HARNESS = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const view = JSON.parse(process.argv[2]);
class Node_ {
  constructor(tag) {
    this.tag = tag; this.children = []; this.attrs = {}; this.className = ""; this.hidden = false;
    this.open = false; this.disabled = false; this.style = {}; this.dataset = {}; this._text = "";
    this.classList = {add() {}, remove() {}, toggle() {}, contains: () => false};
  }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(""); }
  set textContent(v) { this.children = []; this._text = String(v); }
  appendChild(c) { this.children.push(c); return c; }
  append(...cs) { cs.forEach(c => this.children.push(c)); }
  insertBefore(c) { this.children.push(c); return c; }
  replaceChildren(...cs) { this.children = cs; }
  setAttribute(k, v) { this.attrs[k] = String(v); if (k === "id") this.id = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener() {}
  focus() {}
  contains() { return false; }
  querySelector() { return new Node_("x"); }
  querySelectorAll() { return []; }
  find(pred, out = []) {
    if (pred(this)) out.push(this);
    this.children.forEach(c => c.find(pred, out));
    return out;
  }
}
const ids = {};
["status", "error", "error-title", "error-text", "content", "signin", "signin-form", "signin-error",
  "signin-button", "account", "account-email", "lede", "email", "password", "main", "retry"]
  .forEach(id => { ids[id] = new Node_("x"); ids[id].id = id; });
ids.lede.textContent = "Your home and works records are read-only.";
const document = {
  getElementById: id => ids[id] || (ids[id] = new Node_("x")),
  createElement: tag => new Node_(tag),
  createElementNS: (ns, tag) => new Node_(tag),
  createTextNode: t => { const n = new Node_("#text"); n.textContent = t; return n; },
  addEventListener() {}
};
let mounts = 0;
const window = {
  mountResidentAssistant: () => ({setSession() {}}),
  mountResidentAppointments: () => { mounts += 1; return {dispose() {}, searchFromChat() {}}; }
};
const reply = (status, body) => Promise.resolve({ok: status < 400, status,
  json: () => Promise.resolve(body), headers: {get: () => null}});
const fetchStub = path => path === "/demo/session"
  ? reply(200, {signed_in: true, session_id: "s", csrf: "c"})
  : reply(200, view);
const context = vm.createContext({document, window, fetch: fetchStub, setTimeout, clearTimeout,
  BroadcastChannel: class { addEventListener() {} postMessage() {} }, Number, Promise, console});
vm.runInContext(fs.readFileSync(process.argv[1], "utf8"), context);
(async () => {
  for (let i = 0; i < 20; i++) await new Promise(r => setImmediate(r));
  const content = ids.content;
  console.log(JSON.stringify({
    lede: ids.lede.textContent,
    mounts,
    callbackSections: content.find(n => /\bcallbacks\b/.test(n.className)).length,
    bookingLinks: content.find(
      n => n.tag === "a" && /Book a synthetic callback/.test(n.textContent)).length,
    text: content.textContent
  }));
  process.exit(0);
})();
"""


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class CallbacksPageTests(DemoTestCase):
    def render(self, callbacks_available: bool) -> dict[str, Any]:
        c = self.client()
        self.assertEqual(c.login("one@example.com"), 200)
        status, view, _ = c.call("GET", "/demo/view")
        self.assertEqual(status, 200)
        self.assertFalse(view["callbacks_available"])
        view["callbacks_available"] = callbacks_available
        done = subprocess.run(
            ["node", "-e", HARNESS, str(WEB / "demo.js"), json.dumps(view)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        out: dict[str, Any] = json.loads(done.stdout)
        return out

    def test_unconfigured_agenda_hides_callback_form_and_lede(self) -> None:
        page = self.render(False)
        self.assertNotIn("callback booking", page["lede"])
        self.assertIn("read-only", page["lede"])
        self.assertEqual(page["mounts"], 0)
        self.assertEqual(page["callbackSections"], 0)
        self.assertEqual(page["bookingLinks"], 0)
        self.assertIn("Synthetic callback booking is not connected", page["text"])
        self.assertNotIn("Use the form above", page["text"])

    def test_connected_agenda_shows_callback_form_and_lede(self) -> None:
        page = self.render(True)
        self.assertIn("synthetic callback booking", page["lede"])
        self.assertEqual(page["mounts"], 1)
        self.assertEqual(page["callbackSections"], 1)
        self.assertNotIn("is not connected", page["text"])


if __name__ == "__main__":
    unittest.main()
