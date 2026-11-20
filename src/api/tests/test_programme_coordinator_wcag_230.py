"""WCAG 2.2 AA conformance tests for programme manager and coordinator screens (#230, #151).

Exercises #/role/programme_manager, #/role/retrofit_coordinator, programme-queue
(role-screens.js), and Coordinator flow #/coordinator (app.js, style.css) inside isolated
Node vm DOM contexts with zero sys.modules mutation.
Engineering checks only; human assistive-technology and lived-experience
validation remain in #151 and #155.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
CSS = (WEB / "style.css").read_text(encoding="utf-8")

DOM_HARNESS = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const webDir = process.argv[1];
const payload = JSON.parse(process.argv[2]);

function makeDoc(initialHash) {
  const byId = new Map();
  const docListeners = new Map();
  const winListeners = new Map();
  let focusedEl = null;
  const scrolled = [];

  class NodeItem {
    constructor(tag, text = "") {
      this.nodeType = tag === "#text" ? 3 : 1;
      this.tagName = tag.toUpperCase();
      this.text = text;
      this.attrs = {};
      this.dataset = {};
      this.children = [];
      this.parentElement = null;
      this.listeners = new Map();
      this.focusCount = 0;
      this.hidden = false;
      this.open = false;
      this.inert = false;
      this.disabled = false;
      this.isConnected = true;
      this._value = "";
    }
    get value() {
      if (this.tagName === "SELECT" && !this._value) {
        const first = this.querySelector("option");
        return first ? (first.attrs.value ?? first.textContent) : "";
      }
      return this._value;
    }
    set value(v) {
      this._value = String(v ?? "");
    }
    get className() { return this.attrs.class || ""; }
    set className(v) {
      if (v) this.attrs.class = String(v);
      else delete this.attrs.class;
    }
    get id() { return this.attrs.id || ""; }
    set id(v) { this.setAttribute("id", v); }
    get textContent() {
      if (this.nodeType === 3) return this.text;
      return this.children.map((c) => c.textContent).join("");
    }
    set textContent(v) {
      this.children = [new NodeItem("#text", String(v ?? ""))];
    }
    setAttribute(k, v) {
      const s = String(v);
      this.attrs[k] = s;
      if (k === "id" && s) byId.set(s, this);
      if (k === "value") this._value = s;
      if (k.startsWith("data-")) {
        const camel = k.slice(5).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
        this.dataset[camel] = s;
      }
    }
    getAttribute(k) {
      return Object.hasOwn(this.attrs, k) ? this.attrs[k] : null;
    }
    removeAttribute(k) {
      if (k === "id" && this.attrs.id) byId.delete(this.attrs.id);
      delete this.attrs[k];
    }
    append(...kids) {
      for (const kid of kids.flat()) {
        if (kid === null || kid === undefined || kid === false) continue;
        const node = kid instanceof NodeItem ? kid : new NodeItem("#text", String(kid));
        if (node.parentElement) {
          const idx = node.parentElement.children.indexOf(node);
          if (idx >= 0) node.parentElement.children.splice(idx, 1);
        }
        node.parentElement = this;
        this.children.push(node);
        indexSubtree(node);
      }
    }
    replaceChildren(...kids) {
      this.children = [];
      this.append(...kids);
    }
    insertBefore(node, refNode) {
      const idx = refNode ? this.children.indexOf(refNode) : -1;
      if (node.parentElement) {
        const oldIdx = node.parentElement.children.indexOf(node);
        if (oldIdx >= 0) node.parentElement.children.splice(oldIdx, 1);
      }
      node.parentElement = this;
      if (idx >= 0) this.children.splice(idx, 0, node);
      else this.children.push(node);
      indexSubtree(node);
      return node;
    }
    remove() {
      if (!this.parentElement) return;
      const idx = this.parentElement.children.indexOf(this);
      if (idx >= 0) this.parentElement.children.splice(idx, 1);
      this.parentElement = null;
    }
    contains(other) {
      let cur = other;
      while (cur) {
        if (cur === this) return true;
        cur = cur.parentElement;
      }
      return false;
    }
    classList() {
      return (this.attrs.class || "").split(/\s+/).filter(Boolean);
    }
    matches(selector) {
      if (this.nodeType !== 1) return false;
      const s = selector.trim();
      if (s === "a[data-jump]") {
        return this.tagName === "A" && Object.hasOwn(this.attrs, "data-jump");
      }
      if (s === ".skip-link") return this.classList().includes("skip-link");
      if (s === "#nav a") return this.tagName === "A" && this.parentElement?.id === "nav";
      if (s === "#account > summary") {
        return this.tagName === "SUMMARY" && this.parentElement?.id === "account";
      }
      if (s.startsWith(".")) return this.classList().includes(s.slice(1));
      if (s.startsWith("#")) return this.id === s.slice(1);
      return this.tagName === s.toUpperCase();
    }
    closest(selector) {
      let cur = this;
      while (cur) {
        if (cur.nodeType === 1 && cur.matches(selector)) return cur;
        cur = cur.parentElement;
      }
      return null;
    }
    querySelectorAll(selector) {
      const parts = selector.split(",").map((p) => p.trim()).filter(Boolean);
      const out = [];
      const visit = (n) => {
        for (const c of n.children) {
          if (c.nodeType === 1 && parts.some((p) => c.matches(p))) out.push(c);
          visit(c);
        }
      };
      visit(this);
      return out;
    }
    querySelector(selector) {
      return this.querySelectorAll(selector)[0] || null;
    }
    addEventListener(type, fn) {
      if (!this.listeners.has(type)) this.listeners.set(type, []);
      this.listeners.get(type).push(fn);
    }
    fire(type, extra = {}) {
      let prevented = false;
      const event = {
        type,
        target: this,
        get defaultPrevented() { return prevented; },
        preventDefault() { prevented = true; },
        stopPropagation() {},
        ...extra,
      };
      if (typeof this[`on${type}`] === "function") this[`on${type}`](event);
      for (const fn of this.listeners.get(type) || []) fn(event);
      return prevented;
    }
    focus() {
      this.focusCount += 1;
      focusedEl = this;
    }
    scrollIntoView(opts) {
      scrolled.push({ id: this.id, opts: opts || null });
    }
    toJSON() {
      if (this.nodeType === 3) return this.text;
      return {
        tag: this.tagName.toLowerCase(),
        attrs: this.attrs,
        focusCount: this.focusCount,
        kids: this.children.map((c) => c.toJSON()),
      };
    }
  }

  function indexSubtree(node) {
    if (node.nodeType === 1 && node.attrs.id) byId.set(node.attrs.id, node);
    for (const c of node.children || []) indexSubtree(c);
  }

  const root = new NodeItem("body");
  const skip = new NodeItem("a");
  skip.className = "skip-link";
  skip.setAttribute("href", "#app");
  const nav = new NodeItem("nav");
  nav.setAttribute("id", "nav");
  for (const [href, label] of [
    ["#/", "My work"],
    ["#/coordinator", "Coordinator flow"],
    ["#/screens", "Specialist screens"],
  ]) {
    const link = new NodeItem("a");
    link.setAttribute("href", href);
    link.textContent = label;
    nav.append(link);
  }
  const account = new NodeItem("details");
  account.setAttribute("id", "account");
  account.append(new NodeItem("summary"));
  for (const id of [
    "who", "account-photo", "account-initials", "account-name", "account-short",
    "account-email", "switch-account", "signout", "account-error", "photo-status",
    "workspace-status", "app"
  ]) {
    const el = new NodeItem("div");
    el.setAttribute("id", id);
    root.append(el);
  }
  root.append(skip, nav, account);

  const document = {
    body: root,
    head: new NodeItem("head"),
    documentElement: root,
    get activeElement() { return focusedEl || root; },
    createElement: (tag) => new NodeItem(tag),
    createElementNS: (_ns, tag) => new NodeItem(tag),
    createTextNode: (text) => new NodeItem("#text", text),
    getElementById: (id) => (id ? root.querySelector(`#${id}`) : null),
    querySelector: (sel) => root.querySelector(sel),
    querySelectorAll: (sel) => root.querySelectorAll(sel),
    addEventListener: (type, fn) => {
      if (!docListeners.has(type)) docListeners.set(type, []);
      docListeners.get(type).push(fn);
    },
    dispatchEvent: () => true,
    fireClick(target) {
      let prevented = false;
      const event = {
        target,
        get defaultPrevented() { return prevented; },
        preventDefault() { prevented = true; },
      };
      for (const fn of docListeners.get("click") || []) fn(event);
      return prevented;
    },
  };
  const location = { hash: initialHash || "#/", href: "/app" };
  const windowObj = {
    location,
    confirm: () => true,
    addEventListener: (type, fn) => {
      if (!winListeners.has(type)) winListeners.set(type, []);
      winListeners.get(type).push(fn);
    },
  };
  return { document, location, window: windowObj, scrolled };
}

function makeLeafletStub() {
  return {
    map() {
      const m = {
        setView() { return m; },
        getZoom() { return 9; },
        setZoom() {},
        panBy() {},
        invalidateSize() {},
        fitBounds() {},
        on() {},
        remove() {},
        getBounds() {
          return {
            getSouth: () => 54.5,
            getWest: () => -2.0,
            getNorth: () => 55.2,
            getEast: () => -1.2,
          };
        },
      };
      return m;
    },
    tileLayer() {
      return { addTo() { return this; }, on() {} };
    },
    layerGroup() {
      return { addTo() { return this; }, clearLayers() {} };
    },
    divIcon(opts) { return opts; },
    marker(_coords, opts) {
      return {
        on() {},
        addTo() { return this; },
        getElement: () => opts?.icon?.html || null,
      };
    },
  };
}

(async () => {
  const { document, location, window: win, scrolled } = makeDoc(payload.hash || "#/");
  const apiCalls = [];
  const context = vm.createContext({
    document,
    location,
    window: win,
    L: makeLeafletStub(),
    fetch: async () => ({
      ok: false,
      status: 401,
      headers: { get: () => "application/json" },
      json: async () => ({ error: "unauthenticated" }),
    }),
    history: { replaceState() {} },
    URL: { createObjectURL: () => "blob:test", revokeObjectURL() {} },
    URLSearchParams,
    Intl,
    AbortController,
    Event: class { constructor(t) { this.type = t; } },
    Date,
    setTimeout,
    clearTimeout,
    AsyncAction: { handler: (fn) => fn, run: (fn) => fn(), feedback: () => ({ finish() {} }) },
    chatCasePanel: () => null,
    employeeChat: { reset() {}, install() {} },
    console,
  });

  const scripts = payload.scripts || ["fields.js", "app.js", "role-screens.js"];
  for (const name of scripts) {
    const src = fs.readFileSync(`${webDir}/${name}`, "utf8");
    vm.runInContext(src, context, { filename: name });
  }
  await new Promise((resolve) => setTimeout(resolve, 0));

  context.api = async (path) => {
    apiCalls.push(path);
    if (path.startsWith("/api/coordinator")) {
      if (payload.coordinatorFail) throw new Error("Coordinator report down");
      return payload.coordinator;
    }
    if (path.startsWith("/api/facets")) return payload.facets;
    if (path.startsWith("/api/workorders")) return payload.orders || [];
    if (path.startsWith("/api/cases?")) {
      return { items: payload.cases || [], total: (payload.cases || []).length };
    }
    if (path.startsWith("/api/cases/")) return payload.caseDetail;
    return {};
  };
  vm.runInContext("api = globalThis.api;", context);
  vm.runInContext(`me = ${JSON.stringify(payload.me)};`, context);

  const missingBeforeLoad = payload.checkMissingBeforeLoad
    ? (() => {
        const saved = vm.runInContext("roleScreensView", context);
        vm.runInContext("roleScreensView = undefined;", context);
        const out = vm.runInContext(
          `missingWorkspaceScripts(${JSON.stringify(payload.hash)}, false)`,
          context
        );
        context.__savedRoleScreensView = saved;
        vm.runInContext("roleScreensView = globalThis.__savedRoleScreensView;", context);
        return out;
      })()
    : null;
  const missingAfterLoad = vm.runInContext(
    `missingWorkspaceScripts(${JSON.stringify(payload.hash)}, false)`,
    context
  );

  if (payload.mode === "route") {
    await vm.runInContext("route()", context);
  } else if (payload.mode === "coordinator") {
    await vm.runInContext("coordinatorView()", context);
  }

  const jumpClicks = [];
  if (payload.exerciseJumps) {
    const beforeHash = location.hash;
    for (const link of document.getElementById("app").querySelectorAll("a[data-jump]")) {
      const prevented = document.fireClick(link);
      jumpClicks.push({
        label: link.textContent,
        jump: link.getAttribute("data-jump"),
        jumpTarget: link.getAttribute("data-jump-target"),
        prevented,
        focusedId: document.activeElement?.id || null,
        focusedTabindex: document.activeElement?.getAttribute?.("tabindex") || null,
        hashUnchanged: location.hash === beforeHash,
      });
    }
  }

  let filterValidation = null;
  if (payload.exerciseFilterValidation) {
    const form = document.getElementById("app").querySelector("form");
    const viewSel = document.getElementById("co-view");
    const groupSel = document.getElementById("co-group_by");
    const errEl = document.getElementById("co-filter-error");
    viewSel.value = "";
    groupSel.value = "area";
    form.fire("submit");
    const missingView = {
      errorText: errEl.textContent,
      focusedId: document.activeElement?.id || null,
    };
    viewSel.value = "all";
    viewSel.fire("change");
    const afterViewChange = errEl.textContent;
    groupSel.value = "";
    form.fire("submit");
    const missingGroup = {
      errorText: errEl.textContent,
      focusedId: document.activeElement?.id || null,
    };
    groupSel.value = "building";
    groupSel.fire("change");
    const afterGroupChange = errEl.textContent;
    filterValidation = { missingView, afterViewChange, missingGroup, afterGroupChange };
  }

  const navCurrent = document.getElementById("nav").querySelectorAll("a")
    .filter((a) => a.getAttribute("aria-current") === "page")
    .map((a) => a.getAttribute("href"));

  process.stdout.write(JSON.stringify({
    app: document.getElementById("app").toJSON(),
    workspaceStatus: document.getElementById("workspace-status").textContent,
    navCurrent,
    apiCalls,
    missingBeforeLoad,
    missingAfterLoad,
    jumpClicks,
    scrolled,
    filterValidation,
  }));
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
"""


def run_dom(payload: dict[str, Any]) -> dict[str, Any]:
    proc = subprocess.run(
        ["node", "-e", DOM_HARNESS, str(WEB), json.dumps(payload)],
        check=True,
        capture_output=True,
        text=True,
    )
    result: dict[str, Any] = json.loads(proc.stdout)
    return result


def walk(node: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(node, dict):
        out.append(node)
        for kid in node.get("kids", []):
            out.extend(walk(kid))
    return out


def text(node: Any) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        return "".join(text(k) for k in node.get("kids", []))
    return ""


def base_me(role: str) -> dict[str, Any]:
    return {
        "user": {"name": "Pam Test", "email": "pam@example.test", "role": role},
        "navigation": [{"href": "#/screens", "scope": "Specialist screens"}],
        "staff": [{"code": "RC", "name": "Pam Test"}],
        "work_queues": {"definitions": [{"id": "blocked", "label": "Blocked work"}]},
        "map": {"tiles": "", "attribution": ""},
    }


def sample_cases() -> list[dict[str, Any]]:
    return [
        {
            "id": "C-1",
            "name": "Pat Test",
            "address": "1 Test Street",
            "stage": "Design",
            "work": {
                "owner": "Retrofit Coordinator",
                "next_action": "Review returned survey",
                "queues": ["returned"],
                "resident_update_owner": "Resident Liaison Officer",
                "returned": {"reason": "Missing survey", "sender": "Technical Lead"},
                "hazard_clocks": [],
            },
        },
        {
            "id": "C-2",
            "name": "Sam Example",
            "address": "2 Example Road",
            "stage": "Survey",
            "work": {
                "owner": "Programme Support Officer",
                "next_action": "Confirm receiver",
                "queues": ["unowned"],
                "resident_update_owner": "Resident Liaison Officer",
                "handoff": {
                    "state": "Offered",
                    "sender": "Retrofit Coordinator",
                    "proposed_receiver": "Contractor Lead",
                    "chase_owner": "Programme Support Officer",
                },
                "hazard_clocks": [],
            },
        },
        {
            "id": "C-3",
            "name": "Alex Demo",
            "address": "3 Demo Lane",
            "stage": "Handover",
            "work": {
                "owner": "Retrofit Programme Manager",
                "next_action": "Check closure notes",
                "queues": [],
                "resident_update_owner": "Resident Liaison Officer",
                "hazard_clocks": [],
            },
        },
    ]


def blocked_case_detail() -> dict[str, Any]:
    return {
        "id": "C-1",
        "name": "Pat Test",
        "address": "1 Test Street",
        "stage": "Design",
        "hazards": [{"status": "Open"}],
        "consent": None,
        "survey": None,
        "design": None,
        "measures": "Loft",
        "documents": [],
        "funding_evidence": [],
        "work": {
            "blockers": [
                {
                    "step": "Technical review",
                    "reason": "Survey missing.",
                    "owner": "Retrofit Coordinator",
                    "next_action": "Complete survey",
                }
            ],
            "owner": "Retrofit Coordinator",
            "next_action": "Review returned survey",
        },
    }


def unblocked_case_detail() -> dict[str, Any]:
    bound = {"measure": "Loft", "context_revision": 2}
    return {
        "id": "C-1",
        "name": "Pat Test",
        "address": "1 Test Street",
        "stage": "Handover",
        "hazards": [],
        "technical": {},
        "measures": "Loft",
        "measure_decisions": [{"measure": "Loft", "context": {"revision": 2}}],
        "quality": [{"state": "Accepted", "measure": "Loft", "resident_binding": bound}],
        "funding_ok": True,
        "finance": {"budget": {"status": "Approved"}},
        "work": {
            "blockers": [],
            "owner": "Retrofit Coordinator",
            "next_action": "Confirm records",
        },
    }


def sample_coordinator_payload() -> dict[str, Any]:
    return {
        "as_of": "2026-11-15T08:00:00Z",
        "current_as_of": "2026-11-15",
        "period_start": None,
        "audit_integrity": "Intact",
        "approval_status": "Read-only summary",
        "cohort": {"selected_cases": 4, "baseline_cases": 5, "excluded_by_filters": 1},
        "counts": {"stopped": 1},
        "priority": {"version": "v1", "status": "Draft", "approved": False, "count": None},
        "coverage": {
            "stage_history_partial": 2,
            "stage_history_unknown": 1,
            "missing_geocode": 1,
        },
        "definitions": {"selected_cases": "Current open cases matching filters."},
        "heatmap": [
            {
                "group": "Leeds",
                "stage": "Design",
                "count": 3,
                "denominator": 4,
                "stopped": 1,
                "missing_geocode": 0,
                "unknown_history": 0,
            },
            {
                "group": "Leeds",
                "stage": "Survey",
                "count": 0,
                "denominator": 4,
                "stopped": 0,
                "missing_geocode": 1,
                "unknown_history": 1,
            },
            {
                "group": "York",
                "stage": "Handover",
                "count": None,
                "denominator": 4,
                "stopped": None,
                "missing_geocode": 0,
                "unknown_history": 1,
            },
        ],
        "funnel": [
            {
                "stage": "Design",
                "current": 3,
                "entries": 3,
                "exits": 1,
                "returns": 1,
                "reopens": 0,
                "stopped": 1,
                "denominator": 4,
            }
        ],
        "selection": {"metric": "current", "metric_stage": "", "group": ""},
        "records": {
            "total": 3,
            "offset": 0,
            "limit": 25,
            "items": [
                {
                    "id": "C-1",
                    "stage": "Design",
                    "address": "1 Test Street",
                    "postcode": "LS1 1AA",
                    "geocode": "Mapped",
                    "stopped": True,
                },
                {
                    "id": "C-2",
                    "stage": "Survey",
                    "address": "2 Example Road",
                    "postcode": "LS1 2BB",
                    "geocode": "Unknown",
                    "stopped": False,
                },
                {
                    "id": "C-3",
                    "stage": "Handover",
                    "address": "3 Demo Lane",
                    "postcode": "YO1 3CC",
                    "geocode": "Mapped",
                    "stopped": None,
                },
            ],
        },
        "map": {
            "total": 3,
            "mapped": 2,
            "missing_geocode": 1,
            "in_view": 2,
            "shown": 1,
            "mode": "clusters",
            "bounds": [54.6, -1.9, 55.0, -1.3],
            "items": [{"lat": 54.8, "lon": -1.6, "count": 2, "hazards": 1}],
        },
    }


def sample_facets() -> dict[str, Any]:
    return {
        "stages": ["Survey", "Design", "Handover"],
        "areas": ["Leeds", "York"],
        "waves": ["Wave 1"],
        "contractors": ["North Works"],
    }


class ProgrammeCoordinatorWcag230Tests(unittest.TestCase):
    def test_role_hash_route_aliases_script_loading_and_rbac(self) -> None:
        for route_hash in (
            "#/role/programme_manager",
            "#/role/retrofit_coordinator?case=C-1&scope=all",
        ):
            for role in (
                "Retrofit Programme Manager",
                "Programme Support Officer",
                "Retrofit Coordinator",
            ):
                out = run_dom(
                    {
                        "mode": "route",
                        "hash": route_hash,
                        "me": base_me(role),
                        "cases": sample_cases(),
                        "caseDetail": blocked_case_detail(),
                        "coordinator": sample_coordinator_payload(),
                        "orders": [],
                        "checkMissingBeforeLoad": True,
                    }
                )
                self.assertEqual(out["missingBeforeLoad"], ["/role-screens.js"])
                self.assertEqual(out["missingAfterLoad"], [])
                self.assertEqual(out["navCurrent"], ["#/screens"])
                headings = [text(n) for n in walk(out["app"]) if n["tag"] == "h1"]
                self.assertEqual(headings, ["Programme queue and connected home view"])
                if "case=C-1" in route_hash:
                    evidence = next(
                        n for n in walk(out["app"]) if n["attrs"].get("class") == "screen-evidence"
                    )
                    self.assertEqual(evidence["attrs"].get("aria-label"), "Evidence for C-1")
                    write_tags = {
                        n["tag"]
                        for n in walk(evidence)
                        if n["tag"] in {"form", "button", "input", "select", "textarea"}
                    }
                    self.assertEqual(write_tags, set())

        for denied_role in ("Contractor", "Resident Liaison Officer"):
            denied = run_dom(
                {
                    "mode": "route",
                    "hash": "#/role/programme_manager?case=C-1",
                    "me": base_me(denied_role),
                    "cases": sample_cases(),
                    "caseDetail": blocked_case_detail(),
                    "coordinator": sample_coordinator_payload(),
                    "checkMissingBeforeLoad": True,
                }
            )
            self.assertEqual(denied["missingBeforeLoad"], ["/role-screens.js"])
            h1s = [text(n) for n in walk(denied["app"]) if n["tag"] == "h1"]
            self.assertEqual(h1s, ["Screen unavailable"])
            alerts = [text(n) for n in walk(denied["app"]) if n["attrs"].get("role") == "alert"]
            self.assertTrue(
                alerts
                and alerts[0].startswith("This screen is not installed for your signed-in role."),
                alerts,
            )
            self.assertEqual(denied["apiCalls"], [])

    def test_programme_queue_row_headers_scope_descriptions_jump_targets_and_state_cues(
        self,
    ) -> None:
        bound = {"measure": "Loft", "context_revision": 2}
        out = run_dom(
            {
                "mode": "route",
                "hash": "#/role/programme_manager?case=C-1&scope=all",
                "me": base_me("Retrofit Programme Manager"),
                "cases": sample_cases(),
                "caseDetail": unblocked_case_detail(),
                "coordinator": sample_coordinator_payload(),
                "orders": [
                    {
                        "id": "WO-1",
                        "state": "Appointed",
                        "appointment_control": {"status": "Committed", "missing": []},
                        "versions": [{"resident_bindings": [bound]}],
                    }
                ],
                "exerciseJumps": True,
            }
        )
        app = out["app"]
        scope_select = next(n for n in walk(app) if n["attrs"].get("id") == "programme-scope")
        self.assertEqual(
            scope_select["attrs"].get("aria-describedby"),
            "programme-page-status programme-filter-status",
        )

        # All 8 jump links (4 overview + 4 connected) share data-jump & data-jump-target.
        self.assertEqual(len(out["jumpClicks"]), 8)
        for click in out["jumpClicks"]:
            self.assertTrue(click["prevented"], click)
            self.assertTrue(click["hashUnchanged"], click)
            self.assertEqual(click["jump"], click["jumpTarget"], click)
            self.assertEqual(click["focusedId"], click["jump"], click)
            self.assertEqual(click["focusedTabindex"], "-1", click)

        # All 3 programme-queue tables expose <th scope="col"> and <th scope="row">.
        tables = [n for n in walk(app) if n["tag"] == "table"]
        self.assertEqual(len(tables), 3)
        for table in tables:
            thead = next(n for n in walk(table) if n["tag"] == "thead")
            self.assertTrue(
                all(th["attrs"].get("scope") == "col" for th in walk(thead) if th["tag"] == "th")
            )
            tbody = next(n for n in walk(table) if n["tag"] == "tbody")
            trs = [n for n in tbody["kids"] if isinstance(n, dict) and n["tag"] == "tr"]
            self.assertTrue(trs)
            for tr in trs:
                first_cell = next(c for c in tr["kids"] if isinstance(c, dict))
                self.assertEqual(first_cell["tag"], "th")
                self.assertEqual(first_cell["attrs"].get("scope"), "row")
                # First-column record label remains plain text inside <th scope="row">.
                self.assertTrue(all(isinstance(k, str) for k in first_cell["kids"]))

        # Fluent 2 non-colour cues in queue, funnel, unblocked warning, and step states.
        cues = {
            (n["attrs"].get("data-state-cue"), n["attrs"].get("class"), text(n))
            for n in walk(app)
            if "data-state-cue" in n["attrs"]
        }
        self.assertIn(("returned", "flag danger", "State: Returned. Missing survey"), cues)
        self.assertIn(("handoff", "flag", "State: Not returned. Handoff state: Offered."), cues)
        self.assertIn(("not-returned", "flag", "State: Not returned"), cues)
        self.assertIn(
            (
                "warning",
                "status-line wait",
                "State: Warning. No blocker is recorded, which does not confirm readiness.",
            ),
            cues,
        )
        self.assertIn(("warning", "flag", "No recorded blocker"), cues)

        stage_history_p = next(
            n for n in walk(app) if n["attrs"].get("data-state-cue") == "stage-history"
        )
        self.assertEqual(stage_history_p["attrs"].get("class"), "status-line wait")
        self.assertIsNone(stage_history_p["attrs"].get("role"))

        evidence = next(n for n in walk(app) if n["attrs"].get("class") == "screen-evidence")
        ok_badges = [n for n in walk(evidence) if "ok" in (n["attrs"].get("class") or "").split()]
        self.assertEqual(ok_badges, [])
        for cue_attr, _, cue_text in cues:
            self.assertNotIn(cue_attr, {"pass", "ready", "confirmed"})
            self.assertFalse(
                cue_text.startswith(("Pass", "Ready", "State: Pass", "State: Ready")),
                cue_text,
            )

        # Blocked case & failed coordinator report fallback cues.
        down_out = run_dom(
            {
                "mode": "route",
                "hash": "#/role/retrofit_coordinator?case=C-1",
                "me": base_me("Retrofit Coordinator"),
                "cases": sample_cases(),
                "caseDetail": blocked_case_detail(),
                "coordinatorFail": True,
                "orders": [],
            }
        )
        down_cues = [
            (
                n["attrs"].get("data-state-cue"),
                n["attrs"].get("class"),
                n["attrs"].get("role"),
                text(n),
            )
            for n in walk(down_out["app"])
            if "data-state-cue" in n["attrs"]
        ]
        self.assertIn(
            (
                "unknown",
                "empty",
                None,
                "State: Unknown. Lifecycle and funnel counts are Unknown. No record was supplied.",
            ),
            down_cues,
        )
        self.assertTrue(
            any(
                cue == "action-needed" and cls == "flag danger" and txt.startswith("Blocked")
                for cue, cls, _role, txt in down_cues
            ),
            down_cues,
        )

    def test_coordinator_view_jump_navigation_landmarks_and_focus_delegation(self) -> None:
        out = run_dom(
            {
                "mode": "coordinator",
                "hash": "#/coordinator?view=all",
                "me": base_me("Retrofit Coordinator"),
                "coordinator": sample_coordinator_payload(),
                "facets": sample_facets(),
                "exerciseJumps": True,
            }
        )
        app = out["app"]
        jump_nav = next(
            n
            for n in walk(app)
            if n["tag"] == "nav" and n["attrs"].get("aria-label") == "Jump to a coordinator section"
        )
        self.assertEqual(jump_nav["attrs"].get("class"), "screen-links")

        expected_targets = [
            "coordinator-filters-heading",
            "coordinator-summary-heading",
            "coordinator-heatmap-heading",
            "coordinator-funnel-heading",
            "coordinator-selection-heading",
            "map-title",
            "coordinator-records-heading",
        ]
        self.assertEqual([c["jump"] for c in out["jumpClicks"]], expected_targets)
        for click in out["jumpClicks"]:
            self.assertTrue(click["prevented"], click)
            self.assertTrue(click["hashUnchanged"], click)
            self.assertEqual(click["jump"], click["jumpTarget"], click)
            self.assertEqual(click["focusedId"], click["jump"], click)
            self.assertEqual(click["focusedTabindex"], "-1", click)
        self.assertEqual(
            [entry["id"] for entry in out["scrolled"]],
            expected_targets,
        )

        # Verify single clean landmark naming and zero duplicate nested table regions (PC-002).
        form = next(n for n in walk(app) if n["tag"] == "form")
        self.assertEqual(form["attrs"].get("aria-labelledby"), "coordinator-filters-heading")

        summary = next(
            n for n in walk(app) if "coordinator-summary" in (n["attrs"].get("class") or "")
        )
        self.assertEqual(summary["attrs"].get("aria-labelledby"), "coordinator-summary-heading")
        self.assertNotIn("aria-label", summary["attrs"])

        map_panel = next(n for n in walk(app) if "map-panel" in (n["attrs"].get("class") or ""))
        self.assertEqual(map_panel["attrs"].get("aria-labelledby"), "map-title")

        table_sections = [
            n
            for n in walk(app)
            if n["tag"] == "section"
            and any(
                isinstance(k, dict) and k["attrs"].get("class") == "table-scroll" for k in n["kids"]
            )
        ]
        self.assertEqual(len(table_sections), 3)
        for sec in table_sections:
            self.assertNotIn("aria-labelledby", sec["attrs"])
            self.assertNotIn("aria-label", sec["attrs"])

        scroll_regions = [n for n in walk(app) if n["attrs"].get("class") == "table-scroll"]
        self.assertEqual(
            [r["attrs"].get("aria-label") for r in scroll_regions],
            [
                "Heatmap of current cases",
                "Lifecycle funnel: current and observed cases",
                "Selected records",
            ],
        )
        self.assertEqual(scroll_regions[2]["attrs"].get("id"), "coordinator-records")

    def test_coordinator_view_filter_descriptions_error_recovery_and_tristate_cues(
        self,
    ) -> None:
        out = run_dom(
            {
                "mode": "coordinator",
                "hash": "#/coordinator?view=all",
                "me": base_me("Retrofit Programme Manager"),
                "coordinator": sample_coordinator_payload(),
                "facets": sample_facets(),
                "exerciseFilterValidation": True,
            }
        )
        app = out["app"]
        by_id = {n["attrs"]["id"]: n for n in walk(app) if "id" in n["attrs"]}
        self.assertEqual(by_id["co-filter-error"]["attrs"].get("role"), "alert")
        self.assertEqual(by_id["co-view"]["attrs"].get("aria-describedby"), "co-filter-error")
        self.assertEqual(by_id["co-group_by"]["attrs"].get("aria-describedby"), "co-filter-error")
        self.assertEqual(by_id["co-as_of"]["attrs"].get("aria-describedby"), "co-cutoff-note")
        self.assertEqual(by_id["co-start"]["attrs"].get("aria-describedby"), "co-cutoff-note")

        fv = out["filterValidation"]
        self.assertEqual(
            fv["missingView"],
            {
                "errorText": "Choose the case scope and heatmap grouping.",
                "focusedId": "co-view",
            },
        )
        self.assertEqual(fv["afterViewChange"], "")
        self.assertEqual(
            fv["missingGroup"],
            {
                "errorText": "Choose the case scope and heatmap grouping.",
                "focusedId": "co-group_by",
            },
        )
        self.assertEqual(fv["afterGroupChange"], "")

        # Tri-state heatmap cells: >0 ("present"), 0 ("zero"), null ("unknown").
        heat_cells = [
            n
            for n in walk(app)
            if n["tag"] == "td" and "heat-count" in (n["attrs"].get("class") or "").split()
        ]
        self.assertEqual(len(heat_cells), 3)

        self.assertEqual(heat_cells[0]["attrs"].get("class"), "heat-count heat-present")
        self.assertEqual(heat_cells[0]["attrs"].get("data-state-cue"), "present")
        self.assertIn("Present", text(heat_cells[0]))
        heat_link_0 = next(n for n in walk(heat_cells[0]) if n["tag"] == "a")
        self.assertEqual(
            heat_link_0["attrs"].get("aria-label"),
            "3 current cases (present) in Leeds, Design",
        )

        self.assertEqual(heat_cells[1]["attrs"].get("class"), "heat-count")
        self.assertEqual(heat_cells[1]["attrs"].get("data-state-cue"), "zero")
        self.assertIn("None", text(heat_cells[1]))
        heat_link_1 = next(n for n in walk(heat_cells[1]) if n["tag"] == "a")
        self.assertEqual(
            heat_link_1["attrs"].get("aria-label"),
            "0 current cases (none recorded) in Leeds, Survey",
        )

        self.assertEqual(heat_cells[2]["attrs"].get("class"), "heat-count")
        self.assertEqual(heat_cells[2]["attrs"].get("data-state-cue"), "unknown")
        self.assertIn("Unknown", text(heat_cells[2]))
        heat_link_2 = next(n for n in walk(heat_cells[2]) if n["tag"] == "a")
        self.assertEqual(
            heat_link_2["attrs"].get("aria-label"),
            "Unknown current cases (unknown count) in York, Handover",
        )

        # Tri-state Selected records stop cells: true, false, and null ("unknown").
        records_region = by_id["coordinator-records"]
        stop_badges = [
            (n["attrs"].get("data-state-cue"), n["attrs"].get("class"), text(n))
            for n in walk(records_region)
            if n["tag"] == "span" and "data-state-cue" in n["attrs"]
        ]
        self.assertEqual(
            stop_badges,
            [
                ("stopped", "flag danger", "Action needed: Cannot move on"),
                ("no-stop", "flag", "State: No current stop recorded"),
                ("unknown", "flag", "State: Unknown (stop state not supplied)"),
            ],
        )

    def test_css_focus_ring_and_heatmap_non_colour_contracts(self) -> None:
        self.assertRegex(
            CSS,
            r'\.coordinator\s+h2\[tabindex="-1"\]:focus-visible,\s*\.screen-record\s+h2\[tabindex="-1"\]:focus-visible\s*\{[^}]*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)',
        )
        self.assertRegex(
            CSS,
            r"\.coordinator\s+\.heat-present\s*\{[^}]*box-shadow:\s*inset\s+3px\s+0\s+0\s+var\(--brand\)",
        )


if __name__ == "__main__":
    unittest.main()
