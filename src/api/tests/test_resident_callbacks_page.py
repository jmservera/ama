"""Run the shipped resident page script with Node and prove it promises only what is connected.

Refs #1053: with no callback agenda the signed-in page must not invite callback booking.
The script is executed unchanged against a small fake DOM; the view comes from the real demo.
"""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Any

from resident_demo_fixture import DemoTestCase

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/resident_demo/web"
CHAT_WIDGET = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web/chat-widget.js"

HARNESS = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const view = JSON.parse(process.argv[2]);
const mode = JSON.parse(process.argv[4] || "{}");
class Node_ {
  constructor(tag) {
    this.tag = tag; this.children = []; this.attrs = {}; this.className = ""; this.hidden = false;
    this.open = false; this.disabled = false; this.checked = false; this.value = "";
    this.style = {setProperty() {}}; this.dataset = {}; this._text = ""; this.listeners = {};
    this.scrollTop = 0; this.scrollHeight = 0; this.clientHeight = 0;
    this.namespaceURI = "http://www.w3.org/1999/xhtml";
    this.classList = {add() {}, remove() {}, toggle() {}, contains: () => false};
  }
  get textContent() { return this._text + this.children.map(c => c.textContent).join(""); }
  set textContent(v) { this.children = []; this._text = String(v); }
  appendChild(c) { this.children.push(c); return c; }
  append(...cs) { cs.forEach(c => this.children.push(c)); }
  insertBefore(c, ref) {
    const idx = this.children.indexOf(ref);
    if (idx >= 0) this.children.splice(idx, 0, c); else this.children.push(c);
    return c;
  }
  replaceChildren(...cs) { this.children = cs; }
  setAttribute(k, v) {
    this.attrs[k] = String(v);
    if (k === "id") this.id = String(v);
    if (k === "class") this.className = String(v);
    if (k === "disabled") this.disabled = true;
  }
  getAttribute(k) { return this.attrs[k] ?? null; }
  removeAttribute(k) { delete this.attrs[k]; }
  addEventListener(t, f) { (this.listeners[t] ||= []).push(f); }
  fire(t, e) { (this.listeners[t] || []).forEach(f => f(e || {preventDefault() {}})); }
  focus() {}
  contains() { return false; }
  getBoundingClientRect() { return {top: 0, bottom: 0, left: 0, right: 0, width: 0, height: 0}; }
  getClientRects() { return [{width: 1, height: 1}]; }
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
ids.lede.textContent = process.argv[3];
const body = new Node_("body");
const document = {
  body,
  activeElement: null,
  getElementById: id => ids[id] || body.find(n => n.id === id)[0] || (ids[id] = new Node_("x")),
  createElement: tag => new Node_(tag),
  createElementNS: (ns, tag) => { const n = new Node_(tag); n.namespaceURI = ns; return n; },
  createTextNode: t => { const n = new Node_("#text"); n.textContent = t; return n; },
  addEventListener() {}
};
let mounts = 0;
const window = {
  innerWidth: 1280,
  innerHeight: 800,
  addEventListener() {},
  mountResidentAssistant: () => ({setSession() {}}),
  mountResidentAppointments: () => { mounts += 1; return {dispose() {}, searchFromChat() {}}; }
};
const reply = (status, payload) => Promise.resolve({ok: status < 400, status,
  json: () => Promise.resolve(payload), headers: {get: () => null}});
const sessionBody = mode.session || {signed_in: true, session_id: "s", csrf: "c"};
const fetchStub = path => {
  if (path === "/demo/session") return reply(200, sessionBody);
  if (path === "/demo/assistant") return reply(200, mode.assistantReply || {
    answer: "Not connected.", label: "Summary by rules", sources: ["Callbacks"], action: null
  });
  return reply(200, view);
};
const context = vm.createContext({document, window, fetch: fetchStub, setTimeout, clearTimeout,
  BroadcastChannel: class { addEventListener() {} postMessage() {} }, Number, Promise, Object,
  String, Boolean, Math, console});
if (mode.realAssistant) {
  vm.runInContext(fs.readFileSync(mode.chatWidgetPath, "utf8"), context);
  vm.runInContext(fs.readFileSync(mode.assistantPath, "utf8"), context);
}
vm.runInContext(fs.readFileSync(process.argv[1], "utf8"), context);
(async () => {
  for (let i = 0; i < 20; i++) await new Promise(r => setImmediate(r));
  if (mode.realAssistant && mode.askChat) {
    const consent = body.find(n => n.id === "assistant-consent")[0];
    const form = body.find(n => /\bchat-widget-composer\b/.test(n.className))[0];
    const q = body.find(n => n.id === "resident-chat-question")[0];
    if (consent && form && q) {
      consent.checked = true;
      q.value = mode.askChat;
      form.fire("submit", {preventDefault() {}});
      for (let i = 0; i < 20; i++) await new Promise(r => setImmediate(r));
    }
  }
  const content = ids.content;
  const unavailSec = content.find(n => n.id === "sec-unavailable")[0];
  const unavailItems = unavailSec ? unavailSec.find(n => n.tag === "li").map(li => {
    const btn = li.find(n => n.tag === "button")[0];
    const why = li.find(n => n.className === "why")[0];
    return {
      button: btn ? btn.textContent : "",
      disabled: btn ? Boolean(btn.disabled) : false,
      ariaDisabled: btn ? btn.attrs["aria-disabled"] || "" : "",
      why: why ? why.textContent : ""
    };
  }) : [];
  const manualBtn = body.find(
    n => n.tag === "button" && n.textContent === "Use the manual callback form"
  )[0];
  const chatNotice = body.find(n => n.id === "assistant-notice")[0];
  const offNote = body.find(n => n.id === "assistant-callbacks-note")[0];
  const chatSearchBtns = body.find(
    n => n.tag === "button" && n.textContent === "Find callback times in the manual form"
  ).length;
  console.log(JSON.stringify({
    lede: ids.lede.textContent,
    mounts,
    callbackSections: content.find(n => /\bcallbacks\b/.test(n.className)).length,
    bookingLinks: content.find(
      n => n.tag === "a" && /Book a synthetic callback/.test(n.textContent)).length,
    unavailItems,
    manualBtnHidden: manualBtn ? Boolean(manualBtn.hidden) : null,
    chatNotice: chatNotice ? chatNotice.textContent : null,
    offNoteHidden: offNote ? Boolean(offNote.hidden) : null,
    offNoteText: offNote ? offNote.textContent : null,
    chatSearchBtns,
    bodyText: body.textContent,
    text: content.textContent
  }));
  process.exit(0);
})();
"""


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class CallbacksPageTests(DemoTestCase):
    def render(
        self,
        callbacks_available: bool,
        *,
        mode: dict[str, Any] | None = None,
        mutate_view: Any = None,
    ) -> dict[str, Any]:
        c = self.client()
        self.assertEqual(c.login("one@example.com"), 200)
        status, view, _ = c.call("GET", "/demo/view")
        self.assertEqual(status, 200)
        self.assertFalse(view["agenda_available"])
        self.assertFalse(view["callbacks_available"])
        view["agenda_available"] = callbacks_available
        view["callbacks_available"] = callbacks_available
        if mutate_view is not None:
            mutate_view(view)
        html = (WEB / "index.html").read_text(encoding="utf-8")
        match = re.search(r'<p id="lede"[^>]*>(.*?)</p>', html, re.S)
        self.assertIsNotNone(match)
        assert match is not None
        lede = match.group(1).strip()
        opts = dict(mode or {})
        if opts.get("realAssistant"):
            opts["chatWidgetPath"] = str(CHAT_WIDGET)
            opts["assistantPath"] = str(WEB / "assistant.js")
        done = subprocess.run(
            [
                "node",
                "-e",
                HARNESS,
                str(WEB / "demo.js"),
                json.dumps(view),
                lede,
                json.dumps(opts),
            ],
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
        self.assertNotIn("You can try", page["lede"])
        self.assertIn("not connected in this showcase environment", page["lede"])
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
        self.assertGreaterEqual(page["bookingLinks"], 1)
        self.assertNotIn("is not connected", page["text"])

    def test_unconfigured_agenda_lists_disabled_synthetic_callbacks_and_guards_assistant(
        self,
    ) -> None:
        page = self.render(
            False,
            mode={
                "realAssistant": True,
                "session": {
                    "signed_in": True,
                    "session_id": "s",
                    "csrf": "c",
                    "agenda_available": False,
                    "callbacks_available": False,
                },
                "askChat": "Can I book a callback?",
                "assistantReply": {
                    "answer": "Callback booking is not connected.",
                    "label": "Summary by rules",
                    "sources": ["Callbacks"],
                    "action": "appointments",
                },
            },
        )
        synthetic_items = [
            item for item in page["unavailItems"] if item["button"] == "Synthetic callbacks"
        ]
        self.assertEqual(len(synthetic_items), 1)
        self.assertTrue(synthetic_items[0]["disabled"])
        self.assertEqual(synthetic_items[0]["ariaDisabled"], "true")
        self.assertIn("not connected in this showcase", synthetic_items[0]["why"])
        self.assertIs(page["manualBtnHidden"], True)
        self.assertIs(page["offNoteHidden"], False)
        self.assertIn("not connected in this showcase", page["offNoteText"] or "")
        self.assertNotIn("Callback booking needs", page["chatNotice"] or "")
        self.assertEqual(page["chatSearchBtns"], 0)

    def test_connected_agenda_enables_assistant_manual_callback_button_even_when_signed_out(
        self,
    ) -> None:
        signed_in = self.render(
            True,
            mode={
                "realAssistant": True,
                "session": {
                    "signed_in": True,
                    "session_id": "s",
                    "csrf": "c",
                    "agenda_available": True,
                    "callbacks_available": True,
                },
            },
        )
        self.assertIs(signed_in["manualBtnHidden"], False)
        self.assertIs(signed_in["offNoteHidden"], True)
        self.assertEqual(signed_in["offNoteText"], "")
        self.assertIn(
            "Callback booking needs your separate confirmation.",
            signed_in["chatNotice"] or "",
        )
        self.assertNotIn("is not connected", signed_in["text"])
        self.assertNotIn("is not connected", signed_in["bodyText"])
        self.assertEqual(
            [item for item in signed_in["unavailItems"] if item["button"] == "Synthetic callbacks"],
            [],
        )

        signed_out = self.render(
            True,
            mode={
                "realAssistant": True,
                "session": {
                    "signed_in": False,
                    "session_id": None,
                    "csrf": "c",
                    "agenda_available": True,
                    "callbacks_available": True,
                },
            },
        )
        self.assertIs(signed_out["manualBtnHidden"], False)
        self.assertIs(signed_out["offNoteHidden"], True)
        self.assertNotIn("is not connected", signed_out["bodyText"])

    def test_callbacks_available_fallback_supports_payload_without_agenda_available(
        self,
    ) -> None:
        def drop_agenda_available(v: dict[str, Any]) -> None:
            v.pop("agenda_available", None)

        connected = self.render(True, mutate_view=drop_agenda_available)
        self.assertEqual(connected["mounts"], 1)
        self.assertGreaterEqual(connected["bookingLinks"], 1)
        self.assertIn("synthetic callback booking", connected["lede"])

        disconnected = self.render(False, mutate_view=drop_agenda_available)
        self.assertEqual(disconnected["mounts"], 0)
        self.assertEqual(disconnected["bookingLinks"], 0)
        self.assertNotIn("You can try", disconnected["lede"])


if __name__ == "__main__":
    unittest.main()
