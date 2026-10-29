"""Execute the shared widget and employee adapter's focus lifecycle with Node."""

import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

HARNESS = r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
function harness() {
  const listeners = new Set(), elements = new Map(), pending = [];
  let context;
  const document = {
    activeElement: null,
    addEventListener(type, fn) { assert.equal(type, "focusin"); listeners.add(fn); },
    removeEventListener(type, fn) { assert.equal(type, "focusin"); listeners.delete(fn); },
    getElementById(id) { return elements.get(id); },
    createElement(tag) {
      return {tag, children: [], attrs: {}, dataset: {}, hidden: false, value: "",
        setAttribute(name, value) {
          this.attrs[name] = value;
          if (name === "id") { this.id = value; elements.set(value, this); }
        },
        append(...nodes) { this.children.push(...nodes); },
        replaceChildren(...nodes) { this.children = nodes; },
        addEventListener(type, fn) { this["on" + type] = fn; },
        contains(target) {
          return target === this || this.children.some(child => child.contains(target));
        },
        focus() {
          document.activeElement = this;
          for (const fn of listeners) fn({target: this});
        },
        remove() { this.removed = true; }
      };
    },
    createElementNS(namespace, tag) { return this.createElement(tag); }
  };
  document.body = document.createElement("body");
  const launcher = document.createElement("button");
  launcher.setAttribute("id", "employee-chat-launcher");
  context = vm.createContext({document, window: {}, AbortController,
    setTimeout, clearTimeout, location: {hash: ""}, me: {user: {role: "Coordinator"}},
    workspaceStatus: {}, app: document.createElement("main"),
    h(tag, attrs, text) {
      const el = document.createElement(tag);
      for (const [key, value] of Object.entries(attrs)) el.setAttribute(key, value);
      el.textContent = text;
      return el;
    },
    api(path) {
      return new Promise((resolve, reject) => pending.push({path, resolve, reject}));
    }
  });
  vm.runInContext(fs.readFileSync(process.argv[1] + "/chat-widget.js", "utf8"), context);
  vm.runInContext(fs.readFileSync(process.argv[1] + "/chat.js", "utf8"), context);
  const employee = vm.runInContext("employeeChat", context);
  function resolve(path, value) {
    const index = pending.findIndex(item => item.path === path);
    assert.ok(index >= 0, "Missing pending " + path);
    pending.splice(index, 1)[0].resolve(value);
  }
  function reject(path, error) {
    const index = pending.findIndex(item => item.path === path);
    assert.ok(index >= 0, "Missing pending " + path);
    pending.splice(index, 1)[0].reject(error);
  }
  function nodes() {
    const root = document.getElementById("employee-chat");
    const find = (el, tag) => el.tag === tag ? el
      : el.children.map(child => find(child, tag)).find(Boolean);
    return {root, input: find(root, "textarea"), heading: find(root, "h2"),
      select: find(root, "select"), form: find(root, "form"),
      log: root.children.find(el => el.attrs.role === "log"),
      error: document.getElementById("employee-chat-error")};
  }
  return {context, document, listeners, launcher, employee, nodes, resolve, reject};
}
const turn = () => new Promise(resolve => setImmediate(resolve));
async function admit(h) {
  h.resolve("/api/chat/skills", {skills: []});
  h.resolve("/api/chat/status", {warning: "Synthetic only.", retention: "Local."});
  await turn();
}
"""


class ChatWidgetFocusTests(unittest.TestCase):
    def run_node(self, script: str) -> None:
        result = subprocess.run(
            ["node", "-e", HARNESS + script, str(WEB)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_external_focus_hides_without_redirect_or_disposal(self) -> None:
        self.run_node(
            r"""
const h = harness();
const ui = h.context.window.ChatWidget.create({
  id: "unit", title: "Unit chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill"
});
ui.open();
ui.input.value = "Retained draft";
ui.select.value = "general";
ui.message("assistant", "Retained reply");
ui.busy(true);
ui.input.focus();
assert.equal(ui.root.hidden, false);
h.launcher.focus();
assert.equal(ui.root.hidden, false);
const external = h.document.createElement("textarea");
external.focus();
assert.equal(ui.root.hidden, true, "External focus must dismiss popup");
assert.equal(h.listeners.size, 1);
assert.equal(h.document.activeElement, external, "Dismissal must not return focus");
assert.equal(h.launcher.attrs["aria-expanded"], "false");
assert.equal(ui.form.attrs["aria-busy"], "true", "Dismissal must retain work");
assert.equal(ui.input.value, "Retained draft");
assert.equal(ui.select.value, "general");
assert.equal(ui.log.children.length, 1);
ui.message("assistant", "Current hidden reply");
assert.equal(h.document.activeElement, external);
ui.open();
assert.equal(ui.log.children.length, 2);
assert.equal(ui.input.value, "Retained draft");
assert.equal(ui.log.attrs["aria-live"], "polite");
assert.equal(ui.status.attrs["aria-live"], "polite");
assert.equal(ui.error.attrs["aria-live"], "polite");
ui.dispose();
assert.equal(h.listeners.size, 0, "Dispose must unregister document listener");
assert.equal(h.launcher.hidden, false, "Adapter owns launcher admission, not disposal");
external.focus();
assert.equal(h.document.activeElement, external);
"""
        )

    def test_setup_and_replies_preserve_deliberately_chosen_focus(self) -> None:
        self.run_node(
            r"""
(async () => {
  for (const stage of ["skills", "status", "thread", "ask"]) {
    for (const outcome of ["success", "error", "403", "404"]) {
      for (const target of ["external", "launcher", "internal"]) {
        const h = harness();
        const opening = h.employee.open();
        const ui = h.nodes();
        assert.equal(h.document.activeElement, ui.heading);
        let task = opening, path;
        if (stage === "skills" || stage === "status") {
          const other = stage === "skills" ? "status" : "skills";
          h.resolve("/api/chat/" + other, other === "skills" ? {skills: []}
            : {warning: "Synthetic only.", retention: "Local."});
          path = "/api/chat/" + stage;
        } else {
          await admit(h);
          await opening;
          assert.equal(h.document.activeElement, ui.heading,
            "Setup must not asynchronously focus the input");
          ui.input.value = "Question";
          ui.input.focus();
          task = ui.form.onsubmit({preventDefault() {}});
          path = "/api/chat/threads";
          if (stage === "ask") {
            h.resolve(path, {id: "unit"});
            await turn();
            path = "/api/chat/threads/unit/ask";
          }
        }
        const chosen = target === "external" ? h.document.createElement("textarea")
          : target === "launcher" ? h.launcher : ui.heading;
        chosen.focus();
        const hidden = ui.root.hidden;
        if (outcome === "success") {
          h.resolve(path, stage === "skills" ? {skills: []}
            : stage === "status" ? {warning: "Synthetic only.", retention: "Local."}
            : stage === "thread" ? {id: "unit"}
            : {reply: "Current answer", citations: [], skill: "general"});
          if (stage === "thread") {
            await turn();
            h.resolve("/api/chat/threads/unit/ask",
              {reply: "Current answer", citations: [], skill: "general"});
          }
        } else {
          const error = new Error("Controlled failure");
          if (outcome !== "error") error.status = Number(outcome);
          h.reject(path, error);
        }
        await task;
        const denied = outcome === "403" || outcome === "404";
        assert.equal(h.document.activeElement,
          denied && target === "internal" ? h.context.app : chosen,
          `${stage}/${outcome}/${target}: asynchronous focus theft`);
        if (!denied) {
          assert.equal(ui.root.hidden, hidden, "Completion must not reopen");
          assert.equal(ui.form.attrs["aria-busy"], "false");
          assert.equal(ui.error.attrs["aria-live"], "polite");
          if (outcome === "error") {
            assert.equal(ui.error.hidden, false);
            assert.match(ui.error.textContent, /Controlled failure/);
          }
          if (stage === "thread" || stage === "ask") {
            assert.equal(ui.input.value, outcome === "success" ? "" : "Question");
            assert.equal(ui.log.children.length, outcome === "success" ? 2 : 1);
          }
          h.employee.reset();
        } else {
          assert.equal(ui.root.removed, true);
        }
        assert.equal(h.listeners.size, 0);
      }
    }
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
"""
        )
