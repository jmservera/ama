"""Issue 159: conversational assistant keyboard operability, focus management and live regions.

Exercises shipped `chat-widget.js` and `chat.js` against synthetic `SqlStore` / `ChatPanel`
payloads in Node `vm` and in headless Chromium via Playwright + CDP Accessibility Tree
inspection. Synthetic fixtures only (ADR 0005); no external network or assistive-technology
conformance claim.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar
from unittest.mock import patch

from zava_forward.core.chat_panel import chat_skills
from zava_forward.core.chat_privacy import WARNING as CHAT_WARNING
from zava_forward.core.sqlstore import SqlStore

import role_matrix_fixture
import test_assistants
from zava_forward.api.server import App, make_handler

if TYPE_CHECKING:
    from playwright.sync_api import Page, Route

API_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = API_DIR / "src" / "zava_forward" / "api" / "web"
ROLE = "Retrofit Coordinator"
LOCAL_PASSWORD = "zf-a11y-159-synthetic"
APPROVED_CHAT_ENV = {
    "CHAT_DPIA_REF": "SYNTH-DPIA-1",
    "CHAT_LAWFUL_BASIS_REF": "SYNTH-LB-1",
    "CHAT_NOTICE_REF": "SYNTH-NOTICE-1",
    "ZF_SIM_STORE": "",
    "ZF_SIM_KEY_FILE": "",
}


def _envelope(text: str | None, outcome: str = "returned") -> dict[str, Any]:
    return {
        "outcome": outcome,
        "text": text,
        "usage": {"prompt_tokens": 24, "completion_tokens": 12, "total_tokens": 36},
        "source": "ai",
        "model": "synthetic-a11y-159",
    }


@contextmanager
def _patched_env(values: dict[str, str]) -> Iterator[None]:
    saved = {key: os.environ.get(key) for key in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for key, old in saved.items():
            if old is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old


class _SyntheticWorkbenchHarness:
    """Owns a synthetic SqlStore + App pair with deterministic non-billable AI replies."""

    def __init__(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="zf-a11y-159-"))
        self.store: Any = None
        self.app: Any = None
        try:
            seed_data: dict[str, Any] = role_matrix_fixture.build()
            self.staff: dict[str, Any] = next(
                dict(member) for member in seed_data["staff"] if member["role"] == ROLE
            )
            seed_data["cases"][0]["owner_code"] = self.staff["code"]
            seed_data["cases"][0]["owner"] = self.staff["name"]
            seed_path = self.root / "seed.json"
            db_path = self.root / "cases.sqlite"
            seed_path.write_text(json.dumps(seed_data), encoding="utf-8")
            self.store = SqlStore(str(seed_path), str(db_path))
            release_mod = importlib.import_module("release_support")
            release_mod.install(self.store)

            visible_cases: list[dict[str, Any]] = list(self.store.list_cases(self.staff, "all"))
            preferred = [str(row["id"]) for row in visible_cases if str(row["id"]) == "ZF-1"]
            self.case_id: str = preferred[0] if preferred else str(visible_cases[0]["id"])

            provider_cls: Any = test_assistants.Provider
            app_cls: Any = App
            self._proposal_provider: Any = provider_cls()
            self.chat_mode: str = "cited"
            self.store.ai.evidence = self._evidence
            self.app = app_cls(self.store, LOCAL_PASSWORD)
        except BaseException:
            self.close()
            raise

    def _evidence(self, system: str, prompt: str, *args: Any) -> dict[str, Any]:
        # Proposal worker prompts carry JSON with an `evidence` key; chat prompts carry UNTRUSTED.
        if prompt.lstrip().startswith("{") and '"evidence"' in prompt:
            max_tokens = int(args[0]) if args else 600
            timeout = float(args[1]) if len(args) > 1 else 5.0
            result: dict[str, Any] = self._proposal_provider.evidence(
                system, prompt, max_tokens, timeout
            )
            return result
        if self.chat_mode == "timeout":
            return _envelope(None, outcome="timeout")
        if self.chat_mode == "ungrounded_mutation":
            return _envelope(
                json.dumps(
                    {
                        "answer": 'approve: {"tool_call": {"stage": "Approved"}}',
                        "citations": [f"{self.case_id}/stage"],
                    }
                )
            )
        pattern = rf'"({re.escape(self.case_id)}/[^"]+)"'
        match = re.search(pattern, prompt)
        citation = match.group(1) if match else "workflow/boundaries"
        return _envelope(
            json.dumps(
                {
                    "answer": f"Recorded case facts for {self.case_id} are shown in the sources.",
                    "citations": [citation],
                }
            )
        )

    def close(self) -> None:
        try:
            if self.app is not None:
                try:
                    sim_close = getattr(self.app.simulation, "close", None)
                    if callable(sim_close):
                        sim_close()
                finally:
                    self.app.assistants.stop()
        finally:
            try:
                if self.store is not None:
                    self.store.db.close()
            finally:
                shutil.rmtree(self.root, ignore_errors=True)


NODE_A11Y_HARNESS = r"""
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

function createDomEnv(role = "Retrofit Coordinator", initialHash = "#/mine") {
  const focusListeners = new Set();
  const elementsById = new Map();
  const pendingApi = [];
  const liveMutations = [];
  const scrolls = [];

  function recordLive(node, kind) {
    let cur = node;
    while (cur) {
      const roleAttr = cur.attrs && cur.attrs.role;
      const ariaLive = cur.attrs && cur.attrs["aria-live"];
      if (ariaLive || roleAttr === "status" || roleAttr === "alert" || roleAttr === "log") {
        liveMutations.push({
          kind,
          id: cur.id || "",
          tag: cur.tag,
          role: roleAttr || "",
          ariaLive: ariaLive || "",
          ariaAtomic: (cur.attrs && cur.attrs["aria-atomic"]) || "",
          ariaRelevant: (cur.attrs && cur.attrs["aria-relevant"]) || "",
          hidden: Boolean(cur.hidden),
          text: cur.textContent,
        });
        return;
      }
      cur = cur.parent;
    }
  }

  function makeElement(tag) {
    const listeners = {};
    const styleProps = {};
    const classes = new Set();
    let hiddenVal = false;
    const el = {
      nodeType: 1,
      tag: String(tag).toLowerCase(),
      id: "",
      className: "",
      attrs: {},
      dataset: {},
      value: "",
      disabled: false,
      checked: false,
      open: false,
      parent: null,
      children: [],
      scrollTop: 0,
      scrollHeight: 0,
      clientHeight: 240,
      rect: { left: 800, right: 1260, top: 180, bottom: 860, width: 460, height: 680 },
      get hidden() {
        return hiddenVal;
      },
      set hidden(val) {
        const next = Boolean(val);
        const changed = hiddenVal !== next;
        hiddenVal = next;
        if (changed) recordLive(this, next ? "hide" : "reveal");
      },
      get textContent() {
        return this.children
          .map((child) => (typeof child === "string" ? child : child.textContent))
          .join("");
      },
      set textContent(val) {
        for (const child of this.children) {
          if (child && typeof child === "object") child.parent = null;
        }
        this.children = val === null || val === undefined || val === "" ? [] : [String(val)];
        recordLive(this, "text");
      },
      classList: {
        add(...names) {
          for (const n of names) classes.add(n);
        },
        toggle(name, force) {
          const on = force === undefined ? !classes.has(name) : Boolean(force);
          if (on) classes.add(name);
          else classes.delete(name);
          return on;
        },
        contains(name) {
          return classes.has(name);
        },
      },
      style: {
        paddingBottom: "",
        paddingRight: "",
        setProperty(name, val) {
          styleProps[name] = String(val);
        },
        getPropertyValue(name) {
          return styleProps[name] || "";
        },
      },
      setAttribute(name, val) {
        const str = String(val);
        this.attrs[name] = str;
        if (name === "id") {
          this.id = str;
          elementsById.set(str, this);
        }
        if (name === "class") this.className = str;
        if (name === "disabled") this.disabled = true;
        if (name === "value") this.value = str;
      },
      getAttribute(name) {
        return Object.prototype.hasOwnProperty.call(this.attrs, name) ? this.attrs[name] : null;
      },
      removeAttribute(name) {
        delete this.attrs[name];
        if (name === "disabled") this.disabled = false;
      },
      append(...nodes) {
        for (const raw of nodes) {
          if (raw === null || raw === undefined) continue;
          const item = typeof raw === "object" && raw.nodeType ? raw : String(raw);
          if (typeof item === "object") item.parent = this;
          this.children.push(item);
        }
        if (this.tag === "select" && !this.value) {
          const opt = this.children.find((c) => typeof c === "object" && c.tag === "option");
          if (opt) this.value = opt.getAttribute("value") || "";
        }
        recordLive(this, "append");
      },
      before(node) {
        if (!this.parent) return;
        this.parent.insertBefore(node, this);
      },
      insertBefore(node, refNode) {
        if (typeof node === "object") node.parent = this;
        const idx = this.children.indexOf(refNode);
        this.children.splice(idx < 0 ? this.children.length : idx, 0, node);
        recordLive(this, "insert");
      },
      replaceChildren(...nodes) {
        for (const child of this.children) {
          if (child && typeof child === "object") child.parent = null;
        }
        this.children = [];
        if (nodes.length) this.append(...nodes);
      },
      addEventListener(type, fn) {
        listeners[type] = listeners[type] || [];
        listeners[type].push(fn);
      },
      removeEventListener(type, fn) {
        listeners[type] = (listeners[type] || []).filter((item) => item !== fn);
      },
      dispatchEvent(type, init = {}) {
        let prevented = false;
        const event = Object.assign(
          {
            type,
            target: init.target || this,
            key: "",
            shiftKey: false,
            isComposing: false,
            keyCode: 0,
            preventDefault() {
              prevented = true;
            },
          },
          init
        );
        let cur = this;
        while (cur) {
          if (type === "click" && typeof cur.onclick === "function") cur.onclick(event);
          if (type === "submit" && typeof cur.onsubmit === "function") cur.onsubmit(event);
          for (const fn of cur._listeners(type)) fn(event);
          cur = init.bubbles === false ? null : cur.parent;
        }
        return { prevented, event };
      },
      _listeners(type) {
        return listeners[type] || [];
      },
      requestSubmit() {
        this._lastSubmit = this.onsubmit ? this.onsubmit({ preventDefault() {} }) : undefined;
        return this._lastSubmit;
      },
      contains(target) {
        if (!target || typeof target !== "object") return false;
        if (target === this) return true;
        return this.children.some(
          (child) => typeof child === "object" && child.contains && child.contains(target)
        );
      },
      getBoundingClientRect() {
        return this.rect;
      },
      focus() {
        if (this.hidden || this.disabled) return;
        document.activeElement = this;
        for (const fn of [...focusListeners]) fn({ target: this });
      },
      remove() {
        this.removed = true;
        if (this.parent) {
          this.parent.children = this.parent.children.filter((c) => c !== this);
          this.parent = null;
        }
        if (this.id && elementsById.get(this.id) === this) elementsById.delete(this.id);
      },
    };
    return el;
  }

  const document = {
    activeElement: null,
    body: null,
    createElement(tag) {
      return makeElement(tag);
    },
    createElementNS(_ns, tag) {
      return makeElement(tag);
    },
    createTextNode(text) {
      return String(text);
    },
    getElementById(id) {
      return elementsById.get(id) || null;
    },
    addEventListener(type, fn) {
      if (type === "focusin") focusListeners.add(fn);
    },
    removeEventListener(type, fn) {
      if (type === "focusin") focusListeners.delete(fn);
    },
  };
  document.body = makeElement("body");
  const appMain = makeElement("main");
  appMain.setAttribute("id", "app");
  appMain.setAttribute("tabindex", "-1");
  const workspaceStatus = makeElement("p");
  workspaceStatus.setAttribute("id", "workspace-status");
  workspaceStatus.setAttribute("role", "status");
  workspaceStatus.setAttribute("aria-live", "polite");
  const launcher = makeElement("button");
  launcher.setAttribute("id", "employee-chat-launcher");
  document.body.append(workspaceStatus, appMain);

  const windowObj = {
    scrollBy(opts) {
      scrolls.push(opts);
    },
  };

  function h(tag, attrs, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === "class") el.setAttribute("class", v);
      else if (k === "checked") el.checked = Boolean(v);
      else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
      else if (v !== false && v !== null && v !== undefined) {
        el.setAttribute(k, v === true ? "" : v);
      }
    }
    for (const kid of kids.flat(Infinity)) {
      if (kid === null || kid === undefined || kid === false) continue;
      el.append(typeof kid === "object" && kid.nodeType ? kid : String(kid));
    }
    return el;
  }

  const locationObj = { hash: initialHash };
  const meObj = {
    user: { name: "Sam Example", email: "sam@example.test", role },
    services: { law_alerts: false },
  };

  const context = vm.createContext({
    window: windowObj,
    document,
    location: locationObj,
    AbortController,
    Intl,
    Date,
    setTimeout,
    clearTimeout,
    me: meObj,
    app: appMain,
    workspaceStatus,
    h,
    caseFieldUnchanged: () => true,
    retryWorkspaceScript: async () => {},
    api(path, body) {
      return new Promise((resolve, reject) => {
        pendingApi.push({ path, body, resolve, reject });
      });
    },
  });

  const webDir = process.argv[1];
  vm.runInContext(fs.readFileSync(webDir + "/chat-widget.js", "utf8"), context);
  vm.runInContext(fs.readFileSync(webDir + "/chat.js", "utf8"), context);

  function findAll(root, pred, acc = []) {
    if (!root || typeof root !== "object") return acc;
    if (pred(root)) acc.push(root);
    for (const child of root.children || []) findAll(child, pred, acc);
    return acc;
  }

  function resolveApi(path, payload) {
    const idx = pendingApi.findIndex((item) => item.path === path);
    assert.ok(
      idx >= 0,
      `Expected pending API call ${path}, saw: ${pendingApi.map((p) => p.path).join(", ")}`
    );
    const entry = pendingApi.splice(idx, 1)[0];
    entry.resolve(payload);
    return entry.body;
  }

  function rejectApi(path, status, message) {
    const idx = pendingApi.findIndex((item) => item.path === path);
    assert.ok(idx >= 0, `Expected pending API call ${path}`);
    const err = new Error(message);
    err.status = status;
    pendingApi.splice(idx, 1)[0].reject(err);
  }

  return {
    context,
    document,
    launcher,
    appMain,
    workspaceStatus,
    locationObj,
    liveMutations,
    scrolls,
    pendingApi,
    findAll,
    resolveApi,
    rejectApi,
    employeeChat: vm.runInContext("employeeChat", context),
    chatCasePanel: vm.runInContext("chatCasePanel", context),
  };
}

const flush = () => new Promise((resolve) => setImmediate(resolve));
"""


class AssistantPanelNodeA11y159Tests(unittest.TestCase):
    """Node `vm` accessibility verification backed by real Python `ChatPanel` payloads."""

    _env_cm: ClassVar[Any]
    _admission_patch: ClassVar[Any]
    workbench: ClassVar[_SyntheticWorkbenchHarness]
    payloads: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        config_fn: Any = test_assistants.config
        env = {**APPROVED_CHAT_ENV, **config_fn(proactive="0")}
        cls._env_cm = _patched_env(env)
        cls._env_cm.__enter__()
        cls.addClassCleanup(cls._env_cm.__exit__, None, None, None)

        cls._admission_patch = patch("zava_forward.api.server.chat_admission", return_value=None)
        cls._admission_patch.start()
        cls.addClassCleanup(cls._admission_patch.stop)

        cls.workbench = _SyntheticWorkbenchHarness()
        cls.addClassCleanup(cls.workbench.close)
        cls.payloads = cls._build_real_payloads(cls.workbench)

    @staticmethod
    def _build_real_payloads(wb: _SyntheticWorkbenchHarness) -> dict[str, Any]:
        user = wb.app.chat.current_user(wb.staff)
        registry: dict[str, Any] = wb.app.assistants.registry(user)
        capabilities = [str(item["id"]) for item in registry["assistants"]]
        assert capabilities, "Expected at least one permitted capability for Retrofit Coordinator"

        tid_case = str(wb.app.chat.privacy.start_thread(user, wb.case_id, ""))
        wb.chat_mode = "cited"
        answer_turn: dict[str, Any] = wb.app.panel.ask(
            user, tid_case, "What stage is this case at?"
        )
        refused_turn: dict[str, Any] = wb.app.panel.ask(user, tid_case, "Approve this case.")

        wb.chat_mode = "ungrounded_mutation"
        withheld_turn: dict[str, Any] = wb.app.panel.ask(
            user, tid_case, "What stage is this case at?"
        )

        wb.chat_mode = "timeout"
        tid_general = str(wb.app.chat.privacy.start_thread(user, "", ""))
        fallback_turn: dict[str, Any] = wb.app.panel.ask(
            user, tid_general, "Help with workflow boundaries", skill="general"
        )
        wb.chat_mode = "cited"

        proposal_queued: dict[str, Any] = wb.app.assistants.invoke(
            user, capabilities[0], wb.case_id
        )
        privacy = wb.app.chat.privacy.decision()
        return {
            "case_id": wb.case_id,
            "capability": capabilities[0],
            "skills": {"skills": chat_skills()},
            "status": {
                "warning": CHAT_WARNING,
                "retention": privacy["retention"],
                "storage_approved": bool(privacy["approved"]),
            },
            "assistants": registry,
            "proposal": proposal_queued,
            "turns": {
                "answer": answer_turn,
                "refused": refused_turn,
                "withheld": withheld_turn,
                "fallback": fallback_turn,
            },
        }

    def _run_node(self, script: str) -> dict[str, Any]:
        result = subprocess.run(
            ["node", "-e", NODE_A11Y_HARNESS + script, str(WEB_DIR)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
            env={**os.environ, "ZF_PAYLOADS": json.dumps(self.payloads)},
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        marker = next(
            line for line in result.stdout.splitlines() if line.startswith("A11Y_RESULT:")
        )
        parsed: dict[str, Any] = json.loads(marker.removeprefix("A11Y_RESULT:"))
        return parsed

    def test_real_backend_payload_shapes_cover_answer_refused_withheld_and_fallback(self) -> None:
        turns = self.payloads["turns"]
        self.assertEqual(turns["answer"]["kind"], "answer")
        self.assertTrue(turns["answer"]["citations"])
        self.assertTrue(
            all(
                str(c["id"]).startswith(f"{self.payloads['case_id']}/")
                for c in turns["answer"]["citations"]
            )
        )
        self.assertEqual((turns["refused"]["kind"], turns["refused"]["citations"]), ("refused", []))
        self.assertIs(turns["refused"]["workflow_only"], True)
        self.assertEqual(turns["withheld"]["kind"], "withheld")
        self.assertEqual(turns["fallback"]["kind"], "fallback")
        self.assertIs(turns["fallback"]["workflow_only"], True)

    def test_widget_keyboard_focus_and_live_region_lifecycle_with_real_payloads(self) -> None:
        summary = self._run_node(
            r"""
(async () => {
  const payloads = JSON.parse(process.env.ZF_PAYLOADS);
  const env = createDomEnv("Retrofit Coordinator", `#/case/${payloads.case_id}?tab=ai`);
  env.document.body.append(env.launcher);
  env.employeeChat.install();

  assert.equal(env.launcher.getAttribute("aria-label"), "Chat");
  assert.equal(env.launcher.getAttribute("aria-haspopup"), "dialog");
  assert.equal(env.launcher.getAttribute("aria-expanded"), "false");

  const openPromise = env.launcher.onclick();
  const root = env.document.getElementById("employee-chat");
  assert.ok(root, "employee-chat dialog created");
  assert.equal(env.launcher.getAttribute("aria-controls"), "employee-chat");
  assert.equal(env.launcher.getAttribute("aria-expanded"), "true");
  assert.equal(root.getAttribute("role"), "dialog");
  assert.equal(root.getAttribute("aria-labelledby"), "employee-chat-title");
  assert.equal(env.document.activeElement.id, "employee-chat-title");
  assert.equal(env.document.activeElement.getAttribute("tabindex"), "-1");

  env.resolveApi("/api/chat/skills", payloads.skills);
  env.resolveApi("/api/chat/status", payloads.status);
  await flush();
  await openPromise;

  const input = env.document.getElementById("employee-chat-question");
  const select = env.document.getElementById("employee-chat-skill");
  const errorEl = env.document.getElementById("employee-chat-error");
  const logEl = env.findAll(root, (n) => n.getAttribute && n.getAttribute("role") === "log")[0];
  const statusEl = env.findAll(
    root,
    (n) => n.getAttribute && n.getAttribute("role") === "status"
  )[0];
  const formEl = env.findAll(root, (n) => n.tag === "form")[0];
  const buttons = env.findAll(root, (n) => n.tag === "button");
  const sendBtn = buttons.find((b) => b.textContent === "Send");
  const dockBtn = buttons.find((b) => b.textContent === "Dock to right edge");
  const widthSlider = env.document.getElementById("employee-chat-width");
  const heightSlider = env.document.getElementById("employee-chat-height");

  assert.equal(logEl.getAttribute("aria-live"), "polite");
  assert.equal(logEl.getAttribute("aria-relevant"), "additions");
  assert.equal(logEl.getAttribute("tabindex"), "0");
  assert.equal(statusEl.getAttribute("aria-live"), "polite");
  assert.equal(statusEl.getAttribute("aria-atomic"), "true");
  assert.equal(errorEl.getAttribute("role"), "alert");
  assert.equal(errorEl.getAttribute("aria-live"), "polite");
  assert.equal(errorEl.getAttribute("aria-atomic"), "true");
  assert.equal(
    input.getAttribute("aria-describedby"),
    "employee-chat-entry-warning chat-privacy employee-chat-error"
  );

  // Shift+Enter and IME composition must never submit prematurely.
  input.value = "Multi-line draft";
  const shiftEnter = input.dispatchEvent("keydown", { key: "Enter", shiftKey: true });
  const imeComposing = input.dispatchEvent("keydown", { key: "Enter", isComposing: true });
  const ime229 = input.dispatchEvent("keydown", { key: "Enter", keyCode: 229 });
  assert.equal(shiftEnter.prevented, false);
  assert.equal(imeComposing.prevented, false);
  assert.equal(ime229.prevented, false);
  assert.equal(env.pendingApi.length, 0);

  // Blank Enter submits, reveals role="alert", and keeps focus on the question textarea.
  input.value = "   ";
  const blankEnter = input.dispatchEvent("keydown", { key: "Enter" });
  assert.equal(blankEnter.prevented, true);
  assert.equal(errorEl.hidden, false);
  assert.equal(errorEl.textContent, "Type a question first.");
  assert.equal(env.document.activeElement, input);

  // Submitting from Send moves focus back to input before disabling Send (no focus drop to body).
  const expectedStatuses = {
    answer: "Answer added. Check the sources before relying on it.",
    refused: "Request refused. A person must take that action in the workflow.",
    withheld: "Reply withheld. Check the case card for recorded facts.",
    fallback:
      "Workflow-only help added. No assistant answer was given. " +
      "Check the case card for recorded facts.",
  };
  const expectedOutcomes = {
    answer: "Outcome: answer",
    refused: "Outcome: refused",
    withheld: "Outcome: withheld",
    fallback: "Outcome: workflow-only help",
  };

  let threadCreated = false;
  const focusModes = ["send", "log", "sources", "external"];
  const outsideControl = env.document.createElement("button");
  outsideControl.textContent = "Outside case control";
  outsideControl.rect = { left: 900, right: 1120, top: 300, bottom: 340, width: 220, height: 40 };
  env.document.body.append(outsideControl);

  const kinds = ["answer", "refused", "withheld", "fallback"];
  for (let i = 0; i < kinds.length; i += 1) {
    const kind = kinds[i];
    const mode = focusModes[i];
    input.value = `Question for ${kind}`;
    let askTask;
    if (mode === "send") {
      sendBtn.focus();
      askTask = formEl.requestSubmit();
    } else {
      input.focus();
      formEl._lastSubmit = undefined;
      const enterSub = input.dispatchEvent("keydown", { key: "Enter" });
      assert.equal(enterSub.prevented, true);
      askTask = formEl._lastSubmit;
      assert.ok(askTask, "Enter keydown triggered form.requestSubmit()");
    }
    if (mode === "send") {
      assert.equal(env.document.activeElement, input, "busy(true) moved focus off disabled Send");
    }
    assert.equal(sendBtn.disabled, true);
    assert.equal(select.disabled, true);
    assert.equal(formEl.getAttribute("aria-busy"), "true");
    assert.equal(statusEl.textContent, "Asking the assistant.");

    let expectedFocus = input;
    if (mode === "log") {
      logEl.focus();
      expectedFocus = logEl;
    } else if (mode === "sources") {
      const firstSummary = env.findAll(logEl, (n) => n.tag === "summary")[0];
      assert.ok(firstSummary, "prior turn summary present");
      firstSummary.focus();
      expectedFocus = firstSummary;
    } else if (mode === "external") {
      outsideControl.focus();
      expectedFocus = outsideControl;
    }

    if (!threadCreated) {
      const threadBody = env.resolveApi("/api/chat/threads", { id: "thread-159" });
      assert.equal(threadBody.case_id, payloads.case_id);
      threadCreated = true;
      await flush();
    }
    env.resolveApi("/api/chat/threads/thread-159/ask", payloads.turns[kind]);
    await askTask;

    assert.equal(formEl.getAttribute("aria-busy"), "false");
    assert.equal(sendBtn.disabled, false);
    assert.equal(statusEl.textContent, expectedStatuses[kind]);
    assert.equal(env.document.activeElement, expectedFocus, `focus preserved in mode ${mode}`);
    assert.ok(
      logEl.textContent.includes(expectedOutcomes[kind]),
      `log includes ${expectedOutcomes[kind]}`
    );
  }

  // Non-auth 500 error announces polite role="alert" and preserves unsent draft.
  input.focus();
  input.value = "Draft preserved across outage";
  const failedAsk = formEl.requestSubmit();
  await flush();
  env.rejectApi("/api/chat/threads/thread-159/ask", 500, "Synthetic transport outage.");
  await failedAsk;
  assert.equal(errorEl.hidden, false);
  assert.ok(
    errorEl.textContent.includes(
      "Chat unavailable: Synthetic transport outage. Owner: application support. " +
        "Next action: try again or continue with the ordinary workflow."
    )
  );
  assert.equal(input.value, "Draft preserved across outage");
  assert.equal(sendBtn.disabled, false);

  // Width + height sliders update CSS custom properties while undocked; docking disables height.
  widthSlider.value = "48";
  widthSlider.dispatchEvent("input");
  heightSlider.value = "75";
  heightSlider.dispatchEvent("input");
  assert.equal(root.style.getPropertyValue("--chat-width"), "48vw");
  assert.equal(root.style.getPropertyValue("--chat-height"), "75dvh");

  // External focus overlap scrolls vertically when undocked, horizontally when docked (2.4.11).
  env.scrolls.length = 0;
  outsideControl.focus();
  assert.ok(env.scrolls.some((s) => typeof s.top === "number" && s.top > 0));

  dockBtn.dispatchEvent("click");
  assert.equal(dockBtn.getAttribute("aria-pressed"), "true");
  assert.equal(heightSlider.disabled, true);
  assert.equal(env.launcher.hidden, true);

  env.scrolls.length = 0;
  outsideControl.focus();
  assert.ok(env.scrolls.some((s) => typeof s.left === "number" && s.left > 0));

  // Pressing Escape while docked un-hides launcher BEFORE focusing it.
  const esc = input.dispatchEvent("keydown", { key: "Escape" });
  assert.equal(esc.prevented, true);
  assert.equal(root.hidden, true);
  assert.equal(env.launcher.hidden, false);
  assert.equal(env.launcher.getAttribute("aria-expanded"), "false");
  assert.equal(env.document.activeElement, env.launcher);

  console.log(
    "A11Y_RESULT:" +
      JSON.stringify({
        liveCount: env.liveMutations.length,
        articles: logEl.children.length,
        logs: env.liveMutations
          .filter((m) => m.role === "log")
          .map((m) => m.text)
          .filter(Boolean),
        statuses: env.liveMutations
          .filter((m) => m.role === "status")
          .map((m) => m.text)
          .filter(Boolean),
        alerts: env.liveMutations
          .filter((m) => m.role === "alert" && !m.hidden)
          .map((m) => m.text)
          .filter(Boolean),
      })
  );
})().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
"""
        )
        self.assertGreaterEqual(summary["articles"], 9)
        log_joined = "\n".join(summary["logs"])
        for expected_outcome in (
            "Outcome: answer",
            "Outcome: refused",
            "Outcome: withheld",
            "Outcome: workflow-only help",
        ):
            self.assertIn(expected_outcome, log_joined)
        for expected_status in (
            "Loading skills.",
            "Choose a skill or ask a general work question.",
            "Asking the assistant.",
            "Answer added. Check the sources before relying on it.",
            "Request refused. A person must take that action in the workflow.",
            "Reply withheld. Check the case card for recorded facts.",
            (
                "Workflow-only help added. No assistant answer was given. "
                "Check the case card for recorded facts."
            ),
        ):
            self.assertIn(expected_status, summary["statuses"])
        self.assertTrue(any("Type a question first." in item for item in summary["alerts"]))
        self.assertTrue(
            any(
                "Chat unavailable: Synthetic transport outage." in item
                for item in summary["alerts"]
            )
        )

    def test_case_panel_proposal_announcements_and_access_loss_focus_recovery(self) -> None:
        summary = self._run_node(
            r"""
(async () => {
  const payloads = JSON.parse(process.env.ZF_PAYLOADS);
  const env = createDomEnv("Retrofit Coordinator", `#/case/${payloads.case_id}?tab=ai`);
  env.document.body.append(env.launcher);
  env.employeeChat.install();

  const panel = env.chatCasePanel(payloads.case_id);
  env.appMain.append(panel);
  // Drain regulatory status/usage reads and assistants registry read.
  env.resolveApi("/api/chat/regulatory/status", {
    available: true,
    warning: payloads.status.warning,
  });
  env.resolveApi("/api/assistants", payloads.assistants);
  await flush();
  if (env.pendingApi.some((p) => p.path === "/api/chat/regulatory/usage")) {
    env.resolveApi("/api/chat/regulatory/usage", {
      role: "Retrofit Coordinator",
      period: "2026-11-15",
      recorded_turns: 0,
      outcomes: { answer: 0, refused: 0, conflict: 0 },
      coverage: "complete",
    });
    await flush();
  }

  // Direct child status (#chat-panel > p[role="status"]) disambiguated from #regulatory-chat.
  const directStatuses = panel.children.filter(
    (child) => child && typeof child === "object" && child.getAttribute("role") === "status"
  );
  assert.equal(directStatuses.length, 1);
  const proposalStatus = directStatuses[0];

  const proposalButtons = env.findAll(
    panel,
    (n) => n.tag === "button" && n.textContent.startsWith("Request proposal:")
  );
  assert.ok(proposalButtons.length >= 1, "Proposal request buttons rendered");
  proposalButtons[0].dispatchEvent("click");
  assert.equal(proposalStatus.textContent, "Requesting a proposal for independent review.");
  env.resolveApi("/api/chat/threads", { id: "proposal-thread-1" });
  await flush();
  env.resolveApi(
    `/api/chat/threads/proposal-thread-1/proposals`,
    payloads.proposal
  );
  await flush();
  await flush();
  assert.equal(
    proposalStatus.textContent,
    "Proposal requested. Find it in the proposals panel and the review queue."
  );

  // Open chat button opens case-scoped dialog and focuses heading.
  const openBtn = env.findAll(panel, (n) => n.tag === "button" && n.textContent === "Open chat")[0];
  const openPromise = openBtn.dispatchEvent("click");
  const root = env.document.getElementById("employee-chat");
  assert.equal(env.document.activeElement.id, "employee-chat-title");
  env.resolveApi("/api/chat/skills", payloads.skills);
  env.resolveApi("/api/chat/status", payloads.status);
  await flush();
  await openPromise;
  assert.ok(root.textContent.includes(`Context: case ${payloads.case_id}.`));

  // Access loss (403) while focus is inside #employee-chat disposes dialog and moves focus to #app.
  const input = env.document.getElementById("employee-chat-question");
  const formEl = env.findAll(root, (n) => n.tag === "form")[0];
  input.focus();
  input.value = "Check case after permission revocation";
  const askPromise = formEl.requestSubmit();
  env.resolveApi("/api/chat/threads", { id: "revoked-thread" });
  await flush();
  env.rejectApi("/api/chat/threads/revoked-thread/ask", 403, "Forbidden");
  await askPromise;

  assert.equal(env.document.getElementById("employee-chat"), null);
  assert.equal(
    env.workspaceStatus.textContent,
    "Chat access ended. Reopen from a record you can see, or sign in again."
  );
  assert.equal(env.document.activeElement, env.appMain);

  // Reopen and verify 401 in chat.js deny() follows the identical reset + #app focus contract.
  env.workspaceStatus.textContent = "";
  const reopenPromise = openBtn.dispatchEvent("click");
  const root401 = env.document.getElementById("employee-chat");
  env.resolveApi("/api/chat/skills", payloads.skills);
  env.resolveApi("/api/chat/status", payloads.status);
  await flush();
  await reopenPromise;
  const input401 = env.document.getElementById("employee-chat-question");
  const form401 = env.findAll(root401, (n) => n.tag === "form")[0];
  input401.focus();
  input401.value = "Check case after 401 session expiry";
  const ask401Promise = form401.requestSubmit();
  env.resolveApi("/api/chat/threads", { id: "expired-thread" });
  await flush();
  env.rejectApi("/api/chat/threads/expired-thread/ask", 401, "Unauthorized");
  await ask401Promise;

  assert.equal(env.document.getElementById("employee-chat"), null);
  assert.equal(
    env.workspaceStatus.textContent,
    "Chat access ended. Reopen from a record you can see, or sign in again."
  );
  assert.equal(env.document.activeElement, env.appMain);

  console.log(
    "A11Y_RESULT:" +
      JSON.stringify({
        proposalStatus: proposalStatus.textContent,
        workspaceStatus: env.workspaceStatus.textContent,
        liveStatusTexts: env.liveMutations
          .filter((m) => m.role === "status")
          .map((m) => m.text)
          .filter(Boolean),
      })
  );
})().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
"""
        )
        self.assertEqual(
            summary["proposalStatus"],
            "Proposal requested. Find it in the proposals panel and the review queue.",
        )
        self.assertEqual(
            summary["workspaceStatus"],
            "Chat access ended. Reopen from a record you can see, or sign in again.",
        )
        self.assertIn(
            "Proposal requested. Find it in the proposals panel and the review queue.",
            summary["liveStatusTexts"],
        )
        self.assertIn(
            "Chat access ended. Reopen from a record you can see, or sign in again.",
            summary["liveStatusTexts"],
        )


LIVE_OBSERVER_INIT_SCRIPT = """
(() => {
  window.__a11yLiveEvents = [];
  const pushLive = (el, reason) => {
    if (!el || el.nodeType !== 1) return;
    const liveEl = el.closest('[aria-live], [role="status"], [role="alert"], [role="log"]');
    if (!liveEl) return;
    window.__a11yLiveEvents.push({
      reason,
      id: liveEl.id || "",
      role: liveEl.getAttribute("role") || "",
      ariaLive: liveEl.getAttribute("aria-live") || "",
      ariaAtomic: liveEl.getAttribute("aria-atomic") || "",
      ariaRelevant: liveEl.getAttribute("aria-relevant") || "",
      hidden: Boolean(liveEl.hidden),
      inChatPanelDirect: Boolean(
        liveEl.parentElement && liveEl.parentElement.id === "chat-panel"
      ),
      text: (liveEl.textContent || "").trim(),
    });
  };
  const install = () => {
    if (!document.body || window.__a11yObserverInstalled) return;
    window.__a11yObserverInstalled = true;
    const observer = new MutationObserver((records) => {
      for (const rec of records) {
        if (rec.type === "attributes") {
          pushLive(rec.target, "attributes:" + rec.attributeName);
        } else if (rec.type === "characterData") {
          pushLive(rec.target.parentElement, "characterData");
        } else if (rec.type === "childList") {
          pushLive(rec.target, "childList");
          for (const added of rec.addedNodes) {
            if (added.nodeType === 1) {
              pushLive(added, "addedNode");
              for (const desc of added.querySelectorAll(
                '[aria-live], [role="status"], [role="alert"], [role="log"]'
              )) {
                pushLive(desc, "addedDescendant");
              }
            }
          }
        }
      }
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ["hidden"],
    });
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", install, { once: true });
  } else {
    install();
  }
})();
"""


class AssistantPanelBrowserA11y159Tests(unittest.TestCase):
    """Real headless Chromium keyboard, focus, live-region and CDP AXTree checks."""

    _env_cm: ClassVar[Any]
    _admission_patch: ClassVar[Any]
    wb: ClassVar[_SyntheticWorkbenchHarness]
    httpd: ClassVar[ThreadingHTTPServer]
    base_url: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if importlib.util.find_spec("playwright") is None:
            raise unittest.SkipTest("Playwright is installed by the browser-check step")

        config_fn: Any = test_assistants.config
        env = {**APPROVED_CHAT_ENV, **config_fn(proactive="0")}
        cls._env_cm = _patched_env(env)
        cls._env_cm.__enter__()
        cls.addClassCleanup(cls._env_cm.__exit__, None, None, None)

        cls._admission_patch = patch("zava_forward.api.server.chat_admission", return_value=None)
        cls._admission_patch.start()
        cls.addClassCleanup(cls._admission_patch.stop)

        cls.wb = _SyntheticWorkbenchHarness()
        cls.addClassCleanup(cls.wb.close)

        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(cls.wb.app))
        cls.addClassCleanup(cls.httpd.server_close)
        cls.base_url = f"http://127.0.0.1:{cls.httpd.server_address[1]}"
        server_thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        server_thread.start()
        cls.addClassCleanup(cls.httpd.shutdown)

    @contextmanager
    def _open_authenticated_page(self) -> Iterator[tuple[Page, list[str]]]:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch()
            except PlaywrightError as exc:
                if "Executable doesn't exist" in str(exc):
                    self.skipTest("Chromium executable is installed by the browser-check step")
                raise
            try:
                context = browser.new_context(viewport={"width": 1280, "height": 900})
                context.add_init_script(LIVE_OBSERVER_INIT_SCRIPT)
                page = context.new_page()

                def guard_loopback(route: Route) -> None:
                    url = route.request.url
                    if url.startswith((self.base_url, "data:", "blob:", "about:")):
                        route.continue_()
                    else:
                        route.abort()

                page.route("**/*", guard_loopback)
                errors: list[str] = []
                page.on("pageerror", lambda err: errors.append(f"pageerror: {err}"))
                page.on(
                    "console",
                    lambda msg: (
                        errors.append(f"console.error: {msg.text}")
                        if msg.type == "error"
                        and not msg.text.startswith("Failed to load resource:")
                        else None
                    ),
                )
                page.on(
                    "response",
                    lambda resp: (
                        errors.append(f"chat-http:{resp.status}:{resp.url}")
                        if ("/api/chat/" in resp.url or "/api/assistants" in resp.url)
                        and "/api/chat/regulatory/" not in resp.url
                        and resp.status >= 400
                        else None
                    ),
                )

                page.goto(f"{self.base_url}/app")
                page.locator("#email").fill(str(self.wb.staff["email"]))
                page.locator("#pw").fill(LOCAL_PASSWORD)
                page.locator("#pw").press("Enter")
                page.get_by_role("heading", name="My cases today").wait_for()
                page.locator("#employee-chat-launcher").wait_for(state="visible")
                errors.clear()
                yield page, errors
            finally:
                browser.close()

    @staticmethod
    def _ax_props(node: dict[str, Any]) -> dict[str, Any]:
        props: dict[str, Any] = {}
        for item in node.get("properties", []):
            val = item.get("value", {})
            if isinstance(val, dict) and "value" in val:
                props[str(item["name"])] = val["value"]
        return props

    @staticmethod
    def _dialog_ax_subtree(ax_nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
        by_id = {str(node["nodeId"]): node for node in ax_nodes if "nodeId" in node}
        dialogs = [
            node
            for node in ax_nodes
            if not node.get("ignored")
            and node.get("role", {}).get("value") == "dialog"
            and node.get("name", {}).get("value") == "Employee assistant"
        ]
        if not dialogs:
            return []
        descendants: list[dict[str, Any]] = []
        stack = [str(cid) for cid in dialogs[0].get("childIds", [])]
        seen: set[str] = set()
        while stack:
            nid = stack.pop()
            if nid in seen or nid not in by_id:
                continue
            seen.add(nid)
            current = by_id[nid]
            if not current.get("ignored"):
                descendants.append(current)
            stack.extend(str(cid) for cid in current.get("childIds", []))
        return descendants

    def test_browser_launcher_keyboard_resize_dock_and_escape_focus(self) -> None:
        with self._open_authenticated_page() as (page, errors):
            cdp = page.context.new_cdp_session(page)

            def find_launcher_ax() -> dict[str, Any]:
                nodes: list[dict[str, Any]] = cdp.send("Accessibility.getFullAXTree")["nodes"]
                matches = [
                    n
                    for n in nodes
                    if not n.get("ignored")
                    and n.get("role", {}).get("value") == "button"
                    and n.get("name", {}).get("value") == "Chat"
                ]
                self.assertEqual(len(matches), 1)
                return matches[0]

            launcher = page.locator("#employee-chat-launcher")
            launcher.focus()
            self.assertIs(self._ax_props(find_launcher_ax()).get("expanded"), False)

            focus_style: dict[str, str] = launcher.evaluate(
                """el => {
                  const s = getComputedStyle(el);
                  return {
                    outlineStyle: s.outlineStyle,
                    outlineWidth: s.outlineWidth,
                    boxShadow: s.boxShadow,
                  };
                }"""
            )
            self.assertNotEqual(focus_style["outlineStyle"], "none")
            self.assertEqual(focus_style["outlineWidth"], "3px")
            self.assertNotEqual(focus_style["boxShadow"], "none")

            # Enter opens #employee-chat and lands focus on #employee-chat-title.
            page.keyboard.press("Enter")
            panel = page.locator("#employee-chat")
            panel.wait_for(state="visible")
            page.wait_for_function(
                "() => document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            self.assertEqual(launcher.get_attribute("aria-expanded"), "true")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-title"
            )

            # Escape closes #employee-chat and returns focus to #employee-chat-launcher.
            page.keyboard.press("Escape")
            panel.wait_for(state="hidden")
            self.assertEqual(launcher.get_attribute("aria-expanded"), "false")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-launcher"
            )

            # Space also activates the native launcher button and focuses the dialog heading.
            page.keyboard.press("Space")
            panel.wait_for(state="visible")
            self.assertEqual(launcher.get_attribute("aria-expanded"), "true")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-title"
            )

            # Keyboard Tab to Close chat and activate via Enter -> closes and restores launcher.
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Close chat"
            )
            page.keyboard.press("Enter")
            panel.wait_for(state="hidden")
            self.assertEqual(launcher.get_attribute("aria-expanded"), "false")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-launcher"
            )

            # Reopen via Space, prove backward Shift+Tab exits #employee-chat without trap.
            page.keyboard.press("Space")
            panel.wait_for(state="visible")
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Close chat"
            )
            page.keyboard.press("Shift+Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-launcher"
            )
            page.keyboard.press("Shift+Tab")
            self.assertTrue(
                page.evaluate(
                    "() => document.getElementById('app')?.contains(document.activeElement)"
                )
            )

            # Tab back into #employee-chat: launcher -> Close chat -> About -> Chat size (Enter).
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-launcher"
            )
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Close chat"
            )
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "About this chat"
            )
            page.keyboard.press("Space")
            self.assertTrue(
                page.evaluate(
                    "() => document.querySelector('#employee-chat .chat-widget-intro')?.open"
                )
            )
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Chat size"
            )
            closed_size_subtree = self._dialog_ax_subtree(
                cdp.send("Accessibility.getFullAXTree")["nodes"]
            )
            size_ax_closed = [
                n
                for n in closed_size_subtree
                if n.get("role", {}).get("value") == "DisclosureTriangle"
                and n.get("name", {}).get("value") == "Chat size"
            ]
            self.assertEqual(len(size_ax_closed), 1)
            self.assertIs(self._ax_props(size_ax_closed[0]).get("expanded"), False)
            page.keyboard.press("Enter")
            self.assertTrue(
                page.evaluate(
                    "() => document.querySelector('#employee-chat .chat-widget-size')?.open"
                )
            )

            # Verify CDP AXTree expanded=True on launcher + Chat size, and pressed="false" on Dock.
            self.assertIs(self._ax_props(find_launcher_ax()).get("expanded"), True)
            open_subtree = self._dialog_ax_subtree(cdp.send("Accessibility.getFullAXTree")["nodes"])
            size_ax = [
                n
                for n in open_subtree
                if n.get("role", {}).get("value") == "DisclosureTriangle"
                and n.get("name", {}).get("value") == "Chat size"
            ]
            self.assertEqual(len(size_ax), 1)
            self.assertIs(self._ax_props(size_ax[0]).get("expanded"), True)
            dock_ax_before = [
                n
                for n in open_subtree
                if n.get("role", {}).get("value") == "button"
                and n.get("name", {}).get("value") == "Dock to right edge"
            ]
            self.assertEqual(len(dock_ax_before), 1)
            self.assertEqual(self._ax_props(dock_ax_before[0]).get("pressed"), "false")

            # Tab into Dock -> Width slider (ArrowRight) -> Height slider while undocked.
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Dock to right edge"
            )
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-width"
            )
            page.keyboard.press("ArrowRight")
            self.assertEqual(
                panel.evaluate("el => el.style.getPropertyValue('--chat-width')"), "41vw"
            )

            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-height"
            )
            page.keyboard.press("ArrowRight")
            self.assertEqual(
                panel.evaluate("el => el.style.getPropertyValue('--chat-height')"), "81dvh"
            )

            # Rendered revealBeside vertical scroll clearance while floating undocked.
            float_scroll: dict[str, Any] = page.evaluate(
                """() => {
                  window.scrollTo(0, 0);
                  const panelRect = document
                    .getElementById('employee-chat')
                    .getBoundingClientRect();
                  const spacer = document.createElement('div');
                  spacer.id = 'zf-a11y-vspacer';
                  spacer.style.height = '2400px';
                  const probe = document.createElement('button');
                  probe.id = 'zf-a11y-under-float';
                  probe.type = 'button';
                  probe.textContent = 'Behind floating chat';
                  probe.style.position = 'absolute';
                  probe.style.left = Math.round(panelRect.left + 32) + 'px';
                  probe.style.top = Math.round(panelRect.top + 48) + 'px';
                  document.body.append(spacer, probe);
                  probe.focus({ preventScroll: true });
                  const scrollY = window.scrollY;
                  const afterBox = probe.getBoundingClientRect();
                  const afterPanel = document
                    .getElementById('employee-chat')
                    .getBoundingClientRect();
                  probe.remove();
                  spacer.remove();
                  window.scrollTo(0, 0);
                  return {
                    scrollY,
                    clearedTop: afterBox.bottom <= afterPanel.top,
                  };
                }"""
            )
            self.assertGreater(float_scroll["scrollY"], 0)
            self.assertTrue(float_scroll["clearedTop"])

            # Re-focus height slider, Shift+Tab to Dock to right edge, toggle docked with Space.
            page.locator("#employee-chat-height").focus()
            page.keyboard.press("Shift+Tab")
            page.keyboard.press("Shift+Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Dock to right edge"
            )
            page.keyboard.press("Space")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.getAttribute('aria-pressed')"),
                "true",
            )
            docked_subtree = self._dialog_ax_subtree(
                cdp.send("Accessibility.getFullAXTree")["nodes"]
            )
            dock_ax_after = [
                n
                for n in docked_subtree
                if n.get("role", {}).get("value") == "button"
                and n.get("name", {}).get("value") == "Dock to right edge"
            ]
            self.assertEqual(len(dock_ax_after), 1)
            self.assertEqual(self._ax_props(dock_ax_after[0]).get("pressed"), "true")
            self.assertTrue(page.locator("#employee-chat-height").is_disabled())
            self.assertTrue(launcher.is_hidden())

            # Prove forward Tab from Send exits #employee-chat cleanly without focus trap.
            page.locator('#employee-chat button[type="submit"]').focus()
            page.keyboard.press("Tab")
            self.assertFalse(panel.evaluate("el => el.contains(document.activeElement)"))
            page.keyboard.press("Tab")
            self.assertTrue(
                page.evaluate("() => document.activeElement?.classList.contains('skip-link')")
            )

            # Rendered revealBeside horizontal scroll clearance while docked to right edge.
            dock_scroll: dict[str, Any] = page.evaluate(
                """() => {
                  window.scrollTo(0, 0);
                  const panelRect = document
                    .getElementById('employee-chat')
                    .getBoundingClientRect();
                  const spacer = document.createElement('div');
                  spacer.id = 'zf-a11y-hspacer';
                  spacer.style.width = '2600px';
                  spacer.style.height = '20px';
                  const probe = document.createElement('button');
                  probe.id = 'zf-a11y-under-dock';
                  probe.type = 'button';
                  probe.textContent = 'Behind docked chat';
                  probe.style.position = 'absolute';
                  probe.style.left = Math.round(panelRect.left + 32) + 'px';
                  probe.style.top = '180px';
                  document.body.append(spacer, probe);
                  probe.focus({ preventScroll: true });
                  const scrollX = window.scrollX;
                  const afterBox = probe.getBoundingClientRect();
                  const afterPanel = document
                    .getElementById('employee-chat')
                    .getBoundingClientRect();
                  probe.remove();
                  spacer.remove();
                  window.scrollTo(0, 0);
                  return {
                    scrollX,
                    clearedLeft: afterBox.right <= afterPanel.left,
                  };
                }"""
            )
            self.assertGreater(dock_scroll["scrollX"], 0)
            self.assertTrue(dock_scroll["clearedLeft"])

            # Move focus back inside #employee-chat and press Escape to close and restore launcher.
            page.locator("#employee-chat .chat-widget-size button").focus()
            page.keyboard.press("Escape")
            panel.wait_for(state="hidden")
            self.assertFalse(launcher.is_hidden())
            self.assertEqual(launcher.get_attribute("aria-expanded"), "false")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-launcher"
            )
            self.assertEqual(errors, [])

    def test_browser_case_assistant_axtree_live_announcements_and_keyboard_turns(self) -> None:
        case_id = self.wb.case_id
        with self._open_authenticated_page() as (page, errors):
            page.goto(f"{self.base_url}/app#/case/{case_id}?tab=ai")
            chat_summary = page.locator("#chat-panel > summary")
            chat_summary.wait_for(state="visible")
            chat_summary.focus()
            page.keyboard.press("Enter")
            self.assertTrue(page.evaluate("() => document.getElementById('chat-panel')?.open"))

            # Wait for assistant proposal buttons in #chat-panel, activate via keyboard Enter.
            page.locator("#chat-panel .row button").first.wait_for(state="visible")
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Open chat"
            )
            page.keyboard.press("Tab")
            self.assertTrue(
                str(page.evaluate("() => document.activeElement?.textContent")).startswith(
                    "Request proposal:"
                )
            )
            page.keyboard.press("Enter")
            direct_status = page.locator('#chat-panel > p[role="status"]')
            page.wait_for_function(
                """() => document.querySelector('#chat-panel > p[role="status"]')?.textContent ===
                'Proposal requested. Find it in the proposals panel and the review queue.'"""
            )
            self.assertIn("Proposal requested.", direct_status.inner_text())

            # Shift+Tab back to Open chat and press Enter to launch case-scoped #employee-chat.
            page.keyboard.press("Shift+Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.textContent"), "Open chat"
            )
            page.keyboard.press("Enter")
            panel = page.locator("#employee-chat")
            panel.wait_for(state="visible")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-title"
            )
            page.wait_for_function(
                "() => document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            self.assertIn(
                f"Context: case {case_id}.",
                panel.locator(".chat-widget-intro").text_content() or "",
            )

            # Inspect Chromium's computed Accessibility Tree scoped to Employee assistant dialog.
            cdp = page.context.new_cdp_session(page)
            ax_nodes: list[dict[str, Any]] = cdp.send("Accessibility.getFullAXTree")["nodes"]
            dialog_subtree = self._dialog_ax_subtree(ax_nodes)
            self.assertTrue(dialog_subtree)

            def find_dialog_ax(
                role_name: str, accessible_name: str | None = None
            ) -> list[dict[str, Any]]:
                matched: list[dict[str, Any]] = []
                for node in dialog_subtree:
                    r_val = node.get("role", {}).get("value")
                    n_val = node.get("name", {}).get("value")
                    if r_val == role_name and (accessible_name is None or n_val == accessible_name):
                        matched.append(node)
                return matched

            log_ax = find_dialog_ax("log", "Employee assistant conversation")
            self.assertEqual(len(log_ax), 1)
            log_props = self._ax_props(log_ax[0])
            self.assertEqual(log_props.get("live"), "polite")
            self.assertEqual(log_props.get("relevant"), "additions")

            textbox_ax = find_dialog_ax("textbox", "Your work question")
            self.assertEqual(len(textbox_ax), 1)
            self.assertIn(
                "Do not enter personal or sensitive resident information.",
                str(textbox_ax[0].get("description", {}).get("value", "")),
            )
            self.assertTrue(find_dialog_ax("combobox", "Agent skill"))
            self.assertTrue(find_dialog_ax("button", "Close chat"))
            self.assertTrue(find_dialog_ax("button", "Send"))
            status_ax = [
                n
                for n in find_dialog_ax("status")
                if self._ax_props(n).get("live") == "polite"
                and self._ax_props(n).get("atomic") is True
            ]
            self.assertEqual(len(status_ax), 1)

            # Keyboard Tab order: heading -> Close -> About -> Chat size -> log -> question -> Send.
            for _ in range(4):
                page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.getAttribute('role')"), "log"
            )
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-skill"
            )
            page.keyboard.press("Tab")
            self.assertEqual(page.evaluate("() => document.activeElement?.textContent"), "Send")
            page.keyboard.press("Shift+Tab")
            page.keyboard.press("Shift+Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )

            # Blank Enter reveals #employee-chat-error (role="alert" inside dialog AX subtree).
            page.keyboard.press("Enter")
            error_el = page.locator("#employee-chat-error")
            error_el.wait_for(state="visible")
            self.assertEqual(error_el.inner_text(), "Type a question first.")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )
            alert_subtree = self._dialog_ax_subtree(
                cdp.send("Accessibility.getFullAXTree")["nodes"]
            )
            alert_ax = [n for n in alert_subtree if n.get("role", {}).get("value") == "alert"]
            self.assertEqual(len(alert_ax), 1)
            self.assertEqual(self._ax_props(alert_ax[0]).get("live"), "polite")
            self.assertIs(self._ax_props(alert_ax[0]).get("atomic"), True)

            # Shift+Enter inserts newline without submitting; Enter submits cited case answer.
            question = page.locator("#employee-chat-question")
            page.keyboard.type("Case check:")
            page.keyboard.press("Shift+Enter")
            page.keyboard.type("What stage is this case at?")
            self.assertIn("\n", question.input_value())
            self.assertEqual(panel.locator('[role="log"] article').count(), 0)

            page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.querySelectorAll('#employee-chat [role=\"log\"] article')"
                ".length === 2 && document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )
            log_text = panel.locator('[role="log"]').inner_text()
            self.assertIn("Outcome: answer", log_text)
            self.assertNotIn("Sources (0)", log_text)

            # Shift+Tab into the reply's Sources (N) summary and press Enter to expand cited facts.
            page.keyboard.press("Shift+Tab")
            self.assertTrue(
                str(page.evaluate("() => document.activeElement?.textContent")).startswith(
                    "Sources ("
                )
            )
            page.keyboard.press("Enter")
            self.assertTrue(
                page.evaluate(
                    "() => document.querySelector('#employee-chat [role=\"log\"] details')?.open"
                )
            )
            self.assertIn(case_id, panel.locator('[role="log"] details ul').inner_text())

            # Keyboard skill selection: Tab to question -> Tab to skill -> ArrowDown -> Shift+Tab.
            page.keyboard.press("Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )
            page.keyboard.press("Tab")
            skill_select = page.locator("#employee-chat-skill")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-skill"
            )
            page.keyboard.press("ArrowDown")
            selected_skill = skill_select.input_value()
            self.assertNotEqual(selected_skill, "general")
            page.keyboard.press("Shift+Tab")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )

            # Submit skill-selected question directly via Enter from #employee-chat-question.
            page.keyboard.type("Summarise next steps for this case.")
            page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.querySelectorAll('#employee-chat [role=\"log\"] article')"
                ".length === 4 && document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )
            skill_log_text = panel.locator('[role="log"]').inner_text()
            self.assertIn(f"Skill: {selected_skill}.", skill_log_text)

            # Separate turn: type refusal prompt, Tab to Send, and submit via Enter on Send.
            page.keyboard.type("Approve this case.")
            page.keyboard.press("Tab")
            page.keyboard.press("Tab")
            self.assertEqual(page.evaluate("() => document.activeElement?.textContent"), "Send")
            page.keyboard.press("Enter")
            page.wait_for_function(
                "() => document.querySelectorAll('#employee-chat [role=\"log\"] article')"
                ".length === 6 && document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-question"
            )
            updated_log_text = panel.locator('[role="log"]').inner_text()
            self.assertIn("Outcome: refused", updated_log_text)

            # Non-auth 500 failure announces polite role="alert" and preserves unsent draft.
            def fail_ask_once(route: Route) -> None:
                route.fulfill(
                    status=500,
                    content_type="application/json",
                    body=json.dumps({"error": "Synthetic transport outage."}),
                )

            ask_pattern = f"{self.base_url}/api/chat/threads/*/ask"
            page.route(ask_pattern, fail_ask_once)
            try:
                page.keyboard.type("Unsent question preserved")
                page.keyboard.press("Enter")
                page.wait_for_function(
                    "() => !document.getElementById('employee-chat-error')?.hidden"
                    " && document.querySelector('#employee-chat form')"
                    "?.getAttribute('aria-busy') === 'false'"
                )
                self.assertIn(
                    "Chat unavailable: Synthetic transport outage. Owner: application support.",
                    error_el.inner_text(),
                )
                self.assertEqual(
                    page.locator("#employee-chat-question").input_value(),
                    "Unsent question preserved",
                )
            finally:
                page.unroute(ask_pattern, fail_ask_once)

            # Live-region MutationObserver recorded status, log, alert, and #chat-panel status.
            live_events: list[dict[str, Any]] = page.evaluate("() => window.__a11yLiveEvents")
            status_texts = [e["text"] for e in live_events if e["role"] == "status" and e["text"]]
            alert_texts = [
                e["text"]
                for e in live_events
                if e["role"] == "alert" and not e["hidden"] and e["text"]
            ]
            log_events = [
                e
                for e in live_events
                if e["role"] == "log"
                and e["ariaLive"] == "polite"
                and "Outcome: answer" in e["text"]
            ]
            direct_panel_events = [
                e
                for e in live_events
                if e["inChatPanelDirect"]
                and "Proposal requested. Find it in the proposals panel and the review queue."
                in e["text"]
            ]
            self.assertIn("Asking the assistant.", status_texts)
            self.assertIn("Answer added. Check the sources before relying on it.", status_texts)
            self.assertIn(
                "Request refused. A person must take that action in the workflow.", status_texts
            )
            self.assertTrue(any("Type a question first." in t for t in alert_texts))
            self.assertTrue(
                any("Chat unavailable: Synthetic transport outage." in t for t in alert_texts)
            )
            self.assertTrue(log_events)
            self.assertTrue(direct_panel_events)

            # Escape closes #employee-chat and returns focus to #employee-chat-launcher.
            page.keyboard.press("Escape")
            panel.wait_for(state="hidden")
            self.assertEqual(
                page.evaluate("() => document.activeElement?.id"), "employee-chat-launcher"
            )

            # Reopen via Enter, then trigger 403 access loss: deny() focuses #app and announces.
            page.keyboard.press("Enter")
            panel.wait_for(state="visible")
            page.wait_for_function(
                "() => document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            page.locator("#employee-chat-question").focus()

            def deny_ask_once(route: Route) -> None:
                route.fulfill(
                    status=403,
                    content_type="application/json",
                    body=json.dumps({"error": "Access lost."}),
                )

            page.route(ask_pattern, deny_ask_once)
            try:
                page.keyboard.type("Check access loss")
                page.keyboard.press("Enter")
                page.wait_for_function("() => !document.getElementById('employee-chat')")
                self.assertEqual(page.evaluate("() => document.activeElement?.id"), "app")
                self.assertEqual(
                    page.locator("#workspace-status").inner_text(),
                    "Chat access ended. Reopen from a record you can see, or sign in again.",
                )
            finally:
                page.unroute(ask_pattern, deny_ask_once)

            # Reopen via launcher and verify 401 session expiry triggers sign-in alert.
            launcher = page.locator("#employee-chat-launcher")
            launcher.focus()
            page.keyboard.press("Enter")
            panel.wait_for(state="visible")
            page.wait_for_function(
                "() => document.querySelector('#employee-chat form')"
                "?.getAttribute('aria-busy') === 'false'"
            )
            page.locator("#employee-chat-question").focus()

            def expire_ask_once(route: Route) -> None:
                route.fulfill(
                    status=401,
                    content_type="application/json",
                    body=json.dumps({"error": "Session expired."}),
                )

            page.route(ask_pattern, expire_ask_once)
            try:
                page.keyboard.type("Check 401 session expiry")
                page.keyboard.press("Enter")
                page.wait_for_function("() => !document.getElementById('employee-chat')")
                self.assertEqual(page.evaluate("() => document.activeElement?.id"), "app")
                self.assertIn(
                    "Your session has ended. Sign in again.",
                    page.locator('#app [role="alert"]').inner_text(),
                )
            finally:
                page.unroute(ask_pattern, expire_ask_once)

            # Verify MutationObserver also captured 403 #workspace-status and 401 sign-in alert.
            post_auth_events: list[dict[str, Any]] = page.evaluate("() => window.__a11yLiveEvents")
            self.assertTrue(
                any(
                    e["id"] == "workspace-status"
                    and "Chat access ended. Reopen from a record you can see, or sign in again."
                    in e["text"]
                    for e in post_auth_events
                )
            )
            self.assertTrue(
                any(
                    e["role"] == "alert" and "Your session has ended. Sign in again." in e["text"]
                    for e in post_auth_events
                )
            )

            # Only our intentional 500, 403, and 401 /ask route failures appear in HTTP errors.
            unexpected = [
                err
                for err in errors
                if not (
                    err.startswith(("chat-http:500:", "chat-http:403:", "chat-http:401:"))
                    and err.endswith("/ask")
                )
            ]
            self.assertEqual(unexpected, [])


if __name__ == "__main__":
    unittest.main()
