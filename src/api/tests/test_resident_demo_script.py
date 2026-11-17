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
const respond = (status, body, headers = {}) => ({
  ok: status < 400, status, json: async () => body,
  headers: {get: k => headers[k] ?? null},
});
const respondRaw = (status, headers = {}) => ({
  ok: status < 400, status,
  json: async () => { throw new SyntaxError("Unexpected end of JSON input"); },
  headers: {get: k => headers[k] ?? null},
});
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
  } else if (scenario === "busy") {
    const busy = () => respond(
      503, {error: "The showcase is busy right now. Try again in a few seconds."},
      {"Retry-After": "3"});
    pending[0].resolve(respond(200, {signed_in: true, session_id: "s", csrf: "c"}));
    await tick();
    const first = pending.at(-1);
    first.resolve(busy());
    await tick();
    await tick();
    const waiting = out();
    const retry = timers.filter(t => t.live && t.ms === 3000).length;
    const before = pending.length;
    timers.filter(t => t.live && t.ms === 3000)[0].f();
    await tick();
    const retried = pending.length === before + 1 && pending.at(-1).path === "/demo/view";
    pending.at(-1).resolve(busy());
    await tick();
    await tick();
    console.log(JSON.stringify({waiting, retry, retried, after: out(), fetches: pending.length}));
  } else if (scenario === "expired503") {
    pending[0].resolve(respond(200, {signed_in: true, session_id: "s", csrf: "c"}));
    await tick();
    pending.at(-1).resolve(respond(503, {error: "This synthetic showcase has ended."}));
    await tick();
    await tick();
    const retryTimers = timers.filter(t => t.live && t.ms !== 4000).length;
    console.log(JSON.stringify({retryTimers, after: out(), fetches: pending.length}));
  } else if (scenario === "shedfallback") {
    pending[0].resolve(respond(200, {signed_in: true, session_id: "s", csrf: "c"}));
    await tick();
    const loadingView = out();
    pending.at(-1).resolve(respondRaw(503, {"Retry-After": "1"}));
    await tick();
    await tick();
    const waiting1 = out();
    const wait1Timer = timers.filter(t => t.live && t.ms === 1000);
    wait1Timer[0].f();
    await tick();
    pending.at(-1).resolve(respond(
      503, {error: "The showcase is not available right now."}, {"Retry-After": "1"}));
    await tick();
    await tick();
    const afterGeneric = out();
    get("retry").fire("click");
    pending.at(-1).resolve(respond(200, {signed_in: true, session_id: "s", csrf: "c"}));
    await tick();
    pending.at(-1).resolve(respondRaw(503, {"Retry-After": "99"}));
    await tick();
    await tick();
    const waitingClamped = out();
    const clampedTimer = timers.filter(t => t.live && t.ms === 10000);
    clampedTimer[0].f();
    await tick();
    pending.at(-1).resolve(respondRaw(503, {"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}));
    await tick();
    await tick();
    console.log(JSON.stringify({
      loadingView,
      waiting1,
      wait1Count: wait1Timer.length,
      afterGeneric,
      waitingClamped,
      clampedCount: clampedTimer.length,
      afterEmpty: out(),
    }));
  } else if (scenario === "loginbusy") {
    const busyBody = {
      error: "The showcase is busy right now. Try again in a few seconds.",
      retry_after_seconds: 3,
    };
    pending[0].resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    get("email").value = "a@example.com";
    get("password").value = "secret";
    get("signin-form").fire("submit", {preventDefault() {}});
    const loginSlowTimer = timers.filter(t => t.live && t.ms === 4000).at(-1);
    pending.at(-1).resolve(respond(200, {session_id: "s", csrf: "c"}));
    await tick();
    pending.at(-1).resolve(respond(503, busyBody, {"Retry-After": "3"}));
    await tick();
    await tick();
    const slowStillLive = loginSlowTimer.live;
    loginSlowTimer.f();
    const duringWait = out();
    const buttonDisabledMidWait = get("signin-button").disabled;
    timers.filter(t => t.live && t.ms === 3000)[0].f();
    await tick();
    pending.at(-1).resolve(respond(503, busyBody, {"Retry-After": "3"}));
    await tick();
    await tick();
    const afterSecond503 = out();
    get("retry").fire("click");
    pending.at(-1).resolve(respond(200, {authenticated: false, csrf: "c"}));
    await tick();
    get("email").value = "a@example.com";
    get("password").value = "secret";
    get("signin-form").fire("submit", {preventDefault() {}});
    pending.at(-1).resolve(respond(200, {session_id: "s", csrf: "c"}));
    await tick();
    pending.at(-1).resolve(respond(503, busyBody, {"Retry-After": "3"}));
    await tick();
    await tick();
    timers.filter(t => t.live && t.ms === 3000).at(-1).f();
    await tick();
    pending.at(-1).reject(new Error("offline"));
    await tick();
    await tick();
    console.log(JSON.stringify({
      slowStillLive,
      duringWait,
      buttonDisabledMidWait,
      afterSecond503,
      buttonDisabledAfterReject: get("signin-button").disabled,
      afterReject: out(),
    }));
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

    def test_busy_view_retries_once_after_retry_after_then_shows_the_error(self) -> None:
        got = run("busy")
        self.assertIn("busy", got["waiting"]["status"])
        self.assertEqual(got["retry"], 1)
        self.assertTrue(got["retried"])
        self.assertIn("Try again in a few seconds", got["after"]["errorText"])
        self.assertEqual(got["fetches"], 3)

    def test_expired_503_without_retry_hint_fails_immediately_without_busy_retry(self) -> None:
        got = run("expired503")
        self.assertEqual(got["retryTimers"], 0)
        self.assertEqual(got["fetches"], 2)
        self.assertEqual(got["after"]["errorText"], "This synthetic showcase has ended.")
        self.assertIsNone(got["after"]["busy"])
        self.assertEqual(got["after"]["focus"][-1], "error-title")

    def test_generic_and_non_json_shed_503_clamp_delay_and_add_retry_guidance(self) -> None:
        got = run("shedfallback")
        self.assertEqual(got["loadingView"]["busy"], "true")
        self.assertEqual(got["wait1Count"], 1)
        self.assertEqual(got["waiting1"]["busy"], "true")
        self.assertIn("1 second.", got["waiting1"]["status"])
        self.assertNotIn("1 seconds", got["waiting1"]["status"])
        self.assertIn("try again in a few seconds", got["waiting1"]["status"])
        self.assertEqual(
            got["afterGeneric"]["errorText"],
            "The showcase is not available right now. Please try again in a few seconds.",
        )
        self.assertIsNone(got["afterGeneric"]["busy"])
        self.assertEqual(got["afterGeneric"]["focus"][-1], "error-title")
        self.assertEqual(got["clampedCount"], 1)
        self.assertIn("10 seconds.", got["waitingClamped"]["status"])
        self.assertIn("try again in a few seconds", got["afterEmpty"]["errorText"].lower())
        self.assertIsNone(got["afterEmpty"]["busy"])

    def test_login_shed_view_clears_slow_timer_and_keeps_promise_chain(self) -> None:
        got = run("loginbusy")
        self.assertFalse(got["slowStillLive"])
        self.assertNotIn("Still signing you in", got["duringWait"]["status"])
        self.assertIn("try again in a few seconds", got["duringWait"]["status"])
        self.assertEqual(got["duringWait"]["busy"], "true")
        self.assertTrue(got["buttonDisabledMidWait"])
        self.assertIn("Try again in a few seconds", got["afterSecond503"]["errorText"])
        self.assertIsNone(got["afterSecond503"]["busy"])
        self.assertFalse(got["buttonDisabledAfterReject"])
        self.assertIsNone(got["afterReject"]["busy"])
        self.assertIn("could not reach the showcase", got["afterReject"]["signinError"])


if __name__ == "__main__":
    unittest.main()
