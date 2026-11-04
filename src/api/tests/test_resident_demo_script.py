"""Behavioural checks of the resident demo script, run in Node against a minimal fake DOM."""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/resident_demo/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const scenario = process.argv[2];
const log = {focus: [], timers: []};
class El {
  constructor(id) {
    this.id = id; this.textContent = ""; this.hidden = false; this.disabled = false;
    this.value = ""; this.attrs = {}; this.listeners = {}; this.open = false;
  }
  setAttribute(k, v) { this.attrs[k] = String(v); }
  removeAttribute(k) { delete this.attrs[k]; }
  getAttribute(k) { return this.attrs[k] ?? null; }
  addEventListener(t, f) { (this.listeners[t] ||= []).push(f); }
  fire(t, e) { (this.listeners[t] || []).forEach(f => f(e || {})); }
  focus() { log.focus.push(this.id); }
  contains() { return false; }
  querySelector() { return new El("q"); }
  appendChild(c) { return c; }
}
const els = {};
const get = id => els[id] ||= new El(id);
get("lede").textContent = "Signed in text";
const docListeners = {};
const timers = [];
let pending = [];
const document = {
  getElementById: get,
  createElement: () => new El("new"),
  body: new El("body"),
  addEventListener: (t, f) => (docListeners[t] ||= []).push(f),
};
const respond = (status, body) => ({ok: status < 400, status, json: async () => body});
const fetchStub = (path) => new Promise((resolve, reject) => pending.push({path, resolve, reject}));
const context = {
  document, window: {mountResidentAssistant: () => ({setSession() {}})},
  BroadcastChannel: class { addEventListener() {} postMessage() {} },
  fetch: fetchStub,
  setTimeout: (f, ms) => { timers.push({f, ms, live: true}); return timers.length - 1; },
  clearTimeout: i => { if (timers[i]) timers[i].live = false; },
  Intl,
};
vm.createContext(context);
vm.runInContext(fs.readFileSync(process.argv[1] + "/demo.js", "utf8"), context);
const tick = () => new Promise(r => setImmediate(r));
const out = () => ({
  status: get("status").textContent, timers: timers.map(t => ({ms: t.ms, live: t.live})),
  focus: [...log.focus], signinError: get("signin-error").textContent,
  signinErrorHidden: get("signin-error").hidden, email: {...get("email").attrs},
  password: {...get("password").attrs}, lede: get("lede").textContent,
  errorText: get("error-text").textContent, signinHidden: get("signin").hidden,
  busy: get("main").attrs["aria-busy"] ?? null, statusClass: get("status").className,
  emailValue: get("email").value, passwordValue: get("password").value,
});
(async () => {
  if (scenario === "slow") {
    const early = out();
    timers[0].f();
    const slow = out();
    pending[0].resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    console.log(JSON.stringify({early, slow, after: out()}));
  } else if (scenario === "fast") {
    pending[0].resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    const done = out();
    if (timers[0].live) timers[0].f();
    console.log(JSON.stringify({done, afterTimer: out()}));
  } else if (scenario === "validation") {
    pending[0].resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    const submit = () => get("signin-form").fire("submit", {preventDefault() {}});
    submit();
    const both = out();
    log.focus.length = 0;
    get("email").value = "a@example.com";
    get("email").fire("input");
    submit();
    const passwordOnly = out();
    get("password").fire("input");
    const cleared = out();
    console.log(JSON.stringify({both, passwordOnly, cleared}));
  } else if (scenario === "loading" || scenario === "badlogin") {
    pending[0].resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    get("email").value = "a@example.com";
    get("password").value = "secret";
    get("signin-form").fire("submit", {preventDefault() {}});
    const loading = out();
    const slowTimer = timers.filter(t => t.live && t.ms === 4000).at(-1);
    slowTimer.f();
    const slow = out();
    pending.at(-1).resolve(respond(401, {error: "Email or password not recognised."}));
    await tick();
    await tick();
    console.log(JSON.stringify({loading, slow, after: out()}));
  } else if (scenario === "signout") {
    pending[0].resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    get("signout").fire("click");
    pending.at(-1).reject(new Error("offline"));
    await tick();
    console.log(JSON.stringify({failed: out()}));
  }
})().catch(e => { console.error(e); process.exitCode = 1; });
"""


def run(scenario: str) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), scenario],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


@unittest.skipIf(shutil.which("node") is None, "node is not installed")
class ResidentDemoScriptTests(unittest.TestCase):
    def test_slow_start_message_appears_after_four_seconds_and_clears(self) -> None:
        got = run("slow")
        self.assertEqual(got["early"]["status"], "Loading\u2026")
        self.assertEqual(got["early"]["timers"], [{"ms": 4000, "live": True}])
        self.assertIn("can take up to 30 seconds", got["slow"]["status"])
        self.assertFalse(got["after"]["timers"][0]["live"])

    def test_fast_start_cancels_the_slow_message(self) -> None:
        got = run("fast")
        self.assertFalse(got["done"]["timers"][0]["live"])
        self.assertNotIn("waking up", got["afterTimer"]["status"])

    def test_empty_sign_in_names_fields_links_error_and_focuses_first_invalid(self) -> None:
        got = run("validation")
        both = got["both"]
        self.assertEqual(both["signinError"], "Enter your email address and the password.")
        linked = {"aria-invalid": "true", "aria-describedby": "signin-error"}
        self.assertEqual(both["email"], linked)
        self.assertEqual(both["password"]["aria-describedby"], "signin-error")
        self.assertEqual(both["focus"][-1], "email")
        only = got["passwordOnly"]
        self.assertEqual(only["signinError"], "Enter the password.")
        self.assertEqual(only["email"], {})
        self.assertEqual(only["password"]["aria-invalid"], "true")
        self.assertEqual(only["focus"], ["password"])
        self.assertEqual(got["cleared"]["password"], {})

    def test_sign_in_shows_only_the_loading_state_then_restores_form(self) -> None:
        got = run("loading")
        loading = got["loading"]
        self.assertTrue(loading["signinHidden"])
        self.assertEqual(loading["busy"], "true")
        self.assertIn("loading-card", loading["statusClass"])
        self.assertIn("Signing you in", loading["status"])
        self.assertIn("can take up to 30 seconds", got["slow"]["status"])
        after = got["after"]
        self.assertFalse(after["signinHidden"])
        self.assertIsNone(after["busy"])
        self.assertEqual(after["emailValue"], "a@example.com")
        self.assertEqual(after["passwordValue"], "")
        self.assertEqual(after["signinError"], "Email or password not recognised.")
        self.assertEqual(after["focus"][-1], "signin-error")

    def test_failed_sign_out_keeps_the_30_minute_fact_in_short_copy(self) -> None:
        text = run("signout")["failed"]["errorText"]
        self.assertTrue(text.startswith("We could not confirm that you signed out."))
        self.assertIn("within 30 minutes", text)
        self.assertNotIn("Your session may still be active", text)


if __name__ == "__main__":
    unittest.main()
