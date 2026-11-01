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
      const el = {tag, children: [], attrs: {}, dataset: {}, hidden: false, value: "",
        scrollTop: 0, scrollHeight: 0, clientHeight: 0,
        setAttribute(name, value) {
          this.attrs[name] = value;
          if (name === "id") { this.id = value; elements.set(value, this); }
        },
        append(...nodes) { this.children.push(...nodes); },
        insertBefore(node, before) {
          const at = this.children.indexOf(before);
          this.children.splice(at < 0 ? this.children.length : at, 0, node);
        },
        classes: new Set(),
        classList: {add(name) { this.owner.classes.add(name); }, toggle() {}},
        style: {setProperty() {}},
        getBoundingClientRect() { return {top: 0, bottom: 0, height: 0}; },
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
      el.classList.owner = el;
      return el;
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
  const pendingPaths = () => pending.map(item => item.path);
  return {context, document, listeners, launcher, employee, nodes, resolve, reject, pendingPaths};
}
const turn = () => new Promise(resolve => setImmediate(resolve));
async function admit(h) {
  h.resolve("/api/chat/skills", {skills: []});
  h.resolve("/api/chat/status", {warning: "Synthetic only.",
    retention: "Local.", storage_approved: true});
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

    def test_delayed_reply_preserves_current_follow_intent_across_layout_changes(self) -> None:
        self.run_node(
            r"""
for (const mode of ["follow", "older-before", "older-after", "log-before",
    "sources-before", "sources-after", "return-bottom"]) {
  const h = harness();
  let scheduled = null;
  h.context.setTimeout = (fn, delay) => { scheduled = {fn, delay}; return scheduled; };
  h.context.clearTimeout = timer => { if (timer === scheduled) scheduled = null; };
  const ui = h.context.window.ChatWidget.create({
    id: "unit", title: "Unit chat", launcher: h.launcher,
    questionLabel: "Question", skillLabel: "Skill"
  });
  const loading = ui.root.children.find(el => el.attrs.class === "chat-widget-loading");
  let position = 0;
  Object.defineProperties(ui.log, {
    clientHeight: {get() {
      return 300 - (loading.hidden ? 0 : 24)
        - Math.ceil((ui.status.textContent || "").length / 24) * 24
        - (ui.error.hidden ? 0 : 48);
    }},
    scrollTop: {
      get() { return Math.min(position, this.scrollHeight - this.clientHeight); },
      set(value) { position = Math.max(0, Math.min(value, this.scrollHeight - this.clientHeight)); }
    }
  });
  const append = ui.log.append;
  ui.log.append = function (...items) {
    append.apply(this, items);
    this.scrollHeight += 300;
  };
  ui.open();
  ui.input.focus();
  ui.message("assistant", "Existing overflowing history");
  ui.message("assistant", "More history");
  const sources = ui.log.children[0].children.find(el => el.tag === "details").children[0];
  const atBottom = () => assert.equal(ui.log.scrollTop,
    ui.log.scrollHeight - ui.log.clientHeight, `${mode}: bottom-follow lost`);
  const setStatus = text => ui.setStatus ? ui.setStatus(text) : (ui.status.textContent = text);
  atBottom();
  ui.busy(true);
  setStatus("Getting your advice...");
  ui.message("user", "Delayed question");
  atBottom();
  assert.equal(loading.hidden, true, "No loading row before the scheduled delay");
  assert.equal(scheduled.delay, 200);
  let chosen = ui.input;
  function readHistory() {
    if (mode.startsWith("older") || mode === "return-bottom") ui.log.scrollTop = 40;
    if (mode === "log-before") chosen = ui.log;
    if (mode.startsWith("sources")) chosen = sources;
    chosen.focus();
  }
  if (mode.endsWith("before") || mode === "return-bottom") readHistory();
  let before = ui.log.scrollTop;
  scheduled.fn();
  assert.equal(loading.hidden, false);
  if (mode === "follow" || mode.endsWith("after")) atBottom();
  else assert.equal(ui.log.scrollTop, before, `${mode}: loading moved history reader`);
  if (mode.endsWith("after")) readHistory();
  if (mode === "return-bottom") ui.log.scrollTop = ui.log.scrollHeight;
  before = ui.log.scrollTop;
  const follow = mode === "follow" || mode === "return-bottom";
  setStatus("");
  ui.message("assistant", "Long reply ".repeat(100));
  setStatus("Answer added. Check the sources before relying on it.");
  if (follow) atBottom();
  else assert.equal(ui.log.scrollTop, before, `${mode}: reply/status moved history reader`);
  ui.busy(false);
  assert.equal(loading.hidden, true);
  assert.equal(scheduled, null, "Completion cancels the loading timer");
  if (follow) atBottom();
  else assert.equal(ui.log.scrollTop, before, `${mode}: loading removal moved history reader`);
  ui.fail("Controlled failure");
  ui.clearError();
  if (follow) atBottom();
  else assert.equal(ui.log.scrollTop, before, `${mode}: error layout moved history reader`);
  assert.equal(h.document.activeElement, chosen);
  ui.busy(true);
  ui.dispose();
  assert.equal(scheduled, null, "Disposal cancels the loading timer");
}
"""
        )

    def test_append_follows_only_bottom_readers_without_history_focus(self) -> None:
        self.run_node(
            r"""
const h = harness();
const ui = h.context.window.ChatWidget.create({
  id: "unit", title: "Unit chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill"
});
ui.open();
ui.log.scrollHeight = 1000;
ui.log.clientHeight = 200;
const append = ui.log.append;
ui.log.append = function (...items) {
  append.apply(this, items);
  this.scrollHeight += 300;
};
ui.input.focus();
ui.log.scrollTop = 100;
ui.message("assistant", "Older-history reader");
assert.equal(ui.log.scrollTop, 100, "Reply must not jump an older-history reader");
ui.log.scrollTop = ui.log.scrollHeight - ui.log.clientHeight - 0.5;
ui.message("assistant", "Bottom reader");
assert.equal(ui.log.scrollTop, ui.log.scrollHeight, "Follow with pixel rounding tolerance");
assert.equal(h.document.activeElement, ui.input);
const sources = ui.log.children[0].children.find(el => el.tag === "details").children[0];
for (const focused of [ui.log, sources]) {
  focused.focus();
  for (const atBottom of [false, true]) {
    ui.log.scrollTop = atBottom ? ui.log.scrollHeight - ui.log.clientHeight : 50;
    const before = ui.log.scrollTop;
    ui.message("assistant", "Do not move focused history");
    assert.equal(ui.log.scrollTop, before);
    assert.equal(h.document.activeElement, focused);
  }
}
ui.dispose();
"""
        )

    def test_reinstall_preserves_widget_toggle_and_launcher_state(self) -> None:
        self.run_node(
            r"""
(async () => {
  const h = harness();
  h.employee.install();
  assert.equal(h.launcher.attrs["aria-expanded"], "false");
  const opening = h.launcher.onclick();
  await admit(h);
  await opening;
  const ui = h.nodes(), toggle = h.launcher.onclick, icon = h.launcher.children[0];
  ui.input.value = "Retained draft";
  for (const hidden of [false, true]) {
    if (ui.root.hidden !== hidden) h.launcher.onclick();
    for (let count = 0; count < 2; count++) h.employee.install();
    assert.equal(h.launcher.onclick, toggle, "Install must not replace widget-owned toggle");
    assert.equal(h.launcher.children[0], icon, "Install must not redecorate live launcher");
    assert.equal(h.launcher.attrs["aria-expanded"], String(!hidden));
    h.launcher.onclick();
    assert.equal(ui.root.hidden, !hidden, "Launcher must toggle after refresh");
    assert.equal(h.launcher.attrs["aria-expanded"], String(hidden));
    assert.equal(h.nodes().root, ui.root, "Refresh must retain conversation identity");
    assert.equal(ui.input.value, "Retained draft");
  }
  h.launcher.hidden = true;
  h.employee.install();
  assert.equal(h.launcher.hidden, true, "Install must keep a docked launcher hidden");
  h.employee.reset();
})().catch(error => { console.error(error); process.exitCode = 1; });
"""
        )

    def test_unapproved_storage_uses_unstored_route_and_stays_open(self) -> None:
        self.run_node(
            r"""
(async () => {
  const h = harness();
  h.employee.install();
  const opening = h.launcher.onclick();
  h.resolve("/api/chat/skills", {skills: []});
  h.resolve("/api/chat/status", {warning: "Synthetic only.",
    retention: "Unknown", storage_approved: false});
  await turn();
  await opening;
  const ui = h.nodes();
  assert.equal(ui.root.hidden, false);
  assert.ok(ui.root.classes.has("chat-widget-resizable"),
    "Employee chat uses the resizable resident layout");
  const width = h.document.getElementById("employee-chat-width");
  const height = h.document.getElementById("employee-chat-height");
  assert.ok(Number(width.attrs.value) >= 35, "At least the resident default width");
  assert.ok(Number(height.attrs.value) >= 70, "At least the resident default height");
  ui.input.value = "Question";
  const submitted = ui.form.onsubmit({preventDefault() {}});
  await turn();
  assert.equal(h.pendingPaths().includes("/api/chat/threads"), false,
    "No stored thread is requested");
  h.resolve("/api/chat/unstored-ask", {reply: "Rules reply", skill: "general", kind: "fallback",
    label: "Workflow-only", workflow_only: true, citations: []});
  await submitted;
  assert.equal(ui.root.hidden, false, "Chat stays open");
  assert.equal(ui.log.children.length, 2);
  assert.equal(ui.input.value, "");
  h.employee.reset();
})().catch(error => { console.error(error); process.exitCode = 1; });
"""
        )

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

    def test_resizable_employee_panel_stays_open_on_outside_focus(self) -> None:
        self.run_node(
            r"""
const h = harness();
const ui = h.context.window.ChatWidget.create({
  id: "unit", title: "Unit chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill", resizable: true, stayOpen: true
});
ui.open();
const external = h.document.createElement("textarea");
external.focus();
assert.equal(ui.root.hidden, false, "Employee panel must stay open when the page is used");
ui.dispose();
"""
        )

    def test_employee_panel_scrolls_obscured_outside_focus_clear(self) -> None:
        self.run_node(
            r"""
const h = harness();
const calls = [];
h.context.window.scrollBy = arg => calls.push(arg);
const ui = h.context.window.ChatWidget.create({
  id: "unit", title: "Unit chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill", resizable: true, stayOpen: true
});
ui.open();
ui.root.getBoundingClientRect = () => ({top: 300, bottom: 700, left: 0, right: 400});
const external = h.document.createElement("textarea");
external.getBoundingClientRect = () => ({top: 400, bottom: 440, left: 10, right: 200});
external.focus();
assert.equal(calls.length, 1, "Obscured control must be scrolled clear of the panel");
assert.ok(calls[0].top >= 156, "Control must end above the panel");
assert.equal(ui.root.hidden, false);
ui.dispose();
"""
        )

    def test_resident_resizable_panel_still_closes_on_outside_focus(self) -> None:
        self.run_node(
            r"""
const h = harness();
const ui = h.context.window.ChatWidget.create({
  id: "unit", title: "Unit chat", launcher: h.launcher,
  questionLabel: "Question", skillLabel: "Skill", resizable: true
});
ui.open();
assert.equal(h.document.getElementById("unit-width").attrs.value, "35");
assert.equal(h.document.getElementById("unit-height").attrs.value, "70");
assert.equal(ui.root.classes.has("chat-widget-roomy"), false);
const external = h.document.createElement("textarea");
external.focus();
assert.equal(ui.root.hidden, true, "Resident panel closes when focus moves to the page");
ui.dispose();
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
