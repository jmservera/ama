"""WCAG 2.2 keyboard jump nav, landmarks, and non-colour textual state cues (#228, #151).

Exercises role-screens.js, app.js, and ops.js inside isolated Node vm DOM contexts.
Engineering checks only; human assistive-technology and usability validation remain in #151/#155.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

TOP_LEVEL_DECL = re.compile(
    r"^(?:async\s+)?(?:const|let|var|function\*?|class)\s+([A-Za-z_$][\w$]*)",
    re.MULTILINE,
)

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
      this.isConnected = true;
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
    after(...nodes) {
      if (!this.parentElement) return;
      const idx = this.parentElement.children.indexOf(this);
      if (idx < 0) return;
      const built = nodes.flat().filter((n) => n !== null && n !== undefined && n !== false)
        .map((n) => (n instanceof NodeItem ? n : new NodeItem("#text", String(n))));
      for (const b of built) {
        b.parentElement = this.parentElement;
        indexSubtree(b);
      }
      this.parentElement.children.splice(idx + 1, 0, ...built);
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
    matches(selector) {
      if (this.nodeType !== 1) return false;
      const s = selector.trim();
      if (s === "a[data-jump]") {
        return this.tagName === "A" && Object.hasOwn(this.attrs, "data-jump");
      }
      if (s === ".skip-link") return this.classList().includes("skip-link");
      if (s === "#nav a") {
        return this.tagName === "A" && this.parentElement?.id === "nav";
      }
      if (s === "#account > summary") {
        return this.tagName === "SUMMARY" && this.parentElement?.id === "account";
      }
      if (s.startsWith(".")) return this.classList().includes(s.slice(1));
      if (s.startsWith("#")) return this.id === s.slice(1);
      return this.tagName === s.toUpperCase();
    }
    classList() {
      return (this.attrs.class || "").split(/\s+/).filter(Boolean);
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
    dispatchEvent() { return true; }
    focus() {
      this.focusCount += 1;
      focusedEl = this;
    }
    scrollIntoView() {}
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
  for (const [href, label] of [["#/", "My work"], ["#/screens", "Specialist screens"]]) {
    const link = new NodeItem("a");
    link.setAttribute("href", href);
    link.textContent = label;
    nav.append(link);
  }
  const account = new NodeItem("details");
  account.setAttribute("id", "account");
  const summary = new NodeItem("summary");
  account.append(summary);
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
  return { document, location, window: windowObj, byId };
}

(async () => {
  const { document, location, window: win } = makeDoc(payload.hash || "#/");
  if (payload.removeAccount) document.getElementById("account")?.remove();
  const apiCalls = [];
  const context = vm.createContext({
    document,
    location,
    window: win,
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

  const scripts = payload.scripts || ["app.js", "role-screens.js"];
  for (const name of scripts) {
    let src = fs.readFileSync(`${webDir}/${name}`, "utf8");
    if (name === "role-screens.js" && !scripts.includes("app.js")) {
      context.routeController = new AbortController();
      context.workspaceStatus = document.getElementById("workspace-status");
      context.me = payload.me;
      context.show = (...nodes) => document.getElementById("app").replaceChildren(...nodes);
      context.workSummary = () => "";
      context.h = (tag, attrs, ...kids) => {
        const el = document.createElement(tag);
        for (const [k, v] of Object.entries(attrs || {})) {
          if (k === "class") el.className = v;
          else if (v !== false && v !== null && v !== undefined) {
            el.setAttribute(k, v === true ? "" : v);
          }
        }
        el.append(...kids);
        return el;
      };
    }
    vm.runInContext(src, context, { filename: name });
  }
  await new Promise((resolve) => setTimeout(resolve, 0));

  const mockApi = async (path) => {
    apiCalls.push(path);
    if (path.startsWith("/api/packages")) return payload.packages || [];
    if (path.startsWith("/api/workorders")) return payload.orders || [];
    if (path.startsWith("/api/cases?")) {
      return { items: payload.cases || [], total: (payload.cases || []).length };
    }
    if (path.startsWith("/api/cases/")) return payload.caseDetail;
    return {};
  };
  context.api = mockApi;
  if (scripts.includes("app.js")) {
    vm.runInContext("api = globalThis.api;", context);
    vm.runInContext(`me = ${JSON.stringify(payload.me)};`, context);
  } else {
    context.me = payload.me;
  }

  let missingScripts = null;
  if (payload.mode === "route") {
    missingScripts = vm.runInContext(
      `missingWorkspaceScripts(${JSON.stringify(payload.hash)}, false)`,
      context
    );
    await vm.runInContext("route()", context);
  } else if (payload.mode === "roleScreenRender") {
    const screenObj = vm.runInContext(
      `roleScreens.get(${JSON.stringify(payload.screenId)})`,
      context
    );
    const extra = await screenObj.load(payload.caseDetail);
    const rendered = await screenObj.render(payload.caseDetail, extra);
    document.getElementById("app").replaceChildren(rendered);
    missingScripts = { ownsStageMap: Boolean(screenObj.ownsStageMap) };
  } else if (payload.mode === "contractorList") {
    await vm.runInContext("contractorListView()", context);
  } else if (payload.mode === "contractorCase") {
    await vm.runInContext(`contractorCaseView(${JSON.stringify(payload.caseDetail.id)})`, context);
  } else if (payload.mode === "jumpClick") {
    const appEl = document.getElementById("app");
    const heading = document.createElement("h2");
    heading.setAttribute("id", "jump-target-heading");
    heading.setAttribute("tabindex", "-1");
    heading.textContent = "Target section";
    const link = document.createElement("a");
    link.setAttribute("href", "#jump-target-heading");
    link.setAttribute("data-jump", "jump-target-heading");
    const inner = document.createElement("span");
    inner.textContent = "Go to Target section";
    link.append(inner);
    if (!payload.missingTarget) appEl.append(heading);
    appEl.append(link);
    const prevented = document.fireClick(payload.clickInner ? inner : link);
    console.log(JSON.stringify({ prevented, focusCount: heading.focusCount }));
    return;
  }

  const jumpClicks = [];
  if (payload.exerciseJumps) {
    for (const link of document.getElementById("app").querySelectorAll("a[data-jump]")) {
      const targetId = link.getAttribute("data-jump");
      const target = document.getElementById(targetId);
      const before = target ? target.focusCount : 0;
      const prevented = document.fireClick(link);
      jumpClicks.push({
        href: link.getAttribute("href"),
        targetId,
        text: link.textContent,
        prevented,
        focusedDelta: target ? target.focusCount - before : 0,
      });
    }
  }

  const navCurrent = document.getElementById("nav").querySelectorAll("a")
    .filter((a) => a.getAttribute("aria-current") === "page")
    .map((a) => a.getAttribute("href"));

  console.log(JSON.stringify({
    app: document.getElementById("app").toJSON(),
    workspaceStatus: document.getElementById("workspace-status").textContent,
    navCurrent,
    apiCalls,
    meta: missingScripts,
    jumpClicks,
  }));
})().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
"""

SAMPLE_PACKAGE: dict[str, Any] = {
    "id": "PKG-1",
    "name": "North wave",
    "period_from": "2026-04-01",
    "period_to": "2026-09-30",
    "contract_ref": "CALL-OFF-7",
    "contract_version": "2",
    "scope": "Loft insulation",
    "scope_version": 3,
    "leaseholder_consultation_status": "unknown",
    "capacity": [
        {
            "contractor": "Test Ltd",
            "offered": 40,
            "committed": 25,
            "in_use": 5,
            "headroom": 15,
            "evidence_status": "Evidenced: signed call-off schedule",
            "insurance_expiry": "2099-12-31",
            "certification_expiry": "2020-01-01",
        },
        {
            "contractor": "Peak Works",
            "offered": 10,
            "committed": 12,
            "in_use": 10,
            "headroom": -2,
            "evidence_status": "Awaiting signed schedule",
        },
    ],
}

SAMPLE_ORDER: dict[str, Any] = {
    "id": "WO-1",
    "version": 2,
    "scope_version": 3,
    "package": "PKG-1",
    "contractor": "Test Ltd",
    "state": "Issued",
    "address": "10 North Street",
    "postcode": "ZN1 2AB",
    "measures": "Loft insulation",
    "scope": "Loft insulation 270mm",
    "needs_notice": True,
    "named_contact": "Alex Liaison",
    "appointment_control": {"status": "Offer", "missing": []},
    "appointments": [],
}

MANAGER_SESSION: dict[str, Any] = {
    "user": {"name": "Pam Manager", "role": "Retrofit Programme Manager"},
    "navigation": [
        {"href": "#/", "label": "My work", "scope": "My work"},
        {"href": "#/screens", "label": "Specialist screens", "scope": "Specialist screens"},
    ],
}

CONTRACTOR_SESSION: dict[str, Any] = {
    "user": {"name": "Kim Contractor", "role": "Contractor"},
    "navigation": [
        {"href": "#/", "label": "Your jobs", "scope": "Your jobs"},
        {"href": "#/screens", "label": "Specialist screens", "scope": "Specialist screens"},
    ],
}


def run_dom(payload: dict[str, Any]) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", DOM_HARNESS, str(WEB), json.dumps(payload)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def walk_elements(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found.extend(walk_elements(kid))
    return found


def node_text(node: Any) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, dict):
        return "".join(node_text(k) for k in node.get("kids", []))
    return ""


class ProcurementContractorScreenWcagTests(unittest.TestCase):
    def test_procurement_and_contractor_role_screens_jump_nav_and_landmark_bijection(self) -> None:
        scenarios: tuple[
            tuple[str, dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]], ...
        ] = (
            (
                "procurement-packages",
                MANAGER_SESSION,
                [SAMPLE_PACKAGE, SAMPLE_PACKAGE | {"id": "PKG 2/b"}],
                [SAMPLE_ORDER],
            ),
            ("procurement-packages", MANAGER_SESSION, [], []),
            ("contractor-job-pack", CONTRACTOR_SESSION, [], [SAMPLE_ORDER]),
        )
        for screen_id, session, packages, orders in scenarios:
            with self.subTest(screen=screen_id, packages=len(packages)):
                out = run_dom(
                    {
                        "mode": "roleScreenRender",
                        "scripts": ["role-screens.js"],
                        "screenId": screen_id,
                        "me": session,
                        "caseDetail": {
                            "id": "C-1",
                            "needs_notice": True,
                            "named_contact": "Alex Liaison",
                        },
                        "packages": packages,
                        "orders": orders,
                        "exerciseJumps": True,
                    }
                )
                self.assertFalse(bool(out["meta"].get("ownsStageMap")))
                elements = walk_elements(out["app"])
                navs = [el for el in elements if el["tag"] == "nav"]
                self.assertEqual(len(navs), 1)
                nav = navs[0]
                self.assertEqual(nav["attrs"].get("role"), "navigation")
                self.assertEqual(nav["attrs"].get("aria-label"), "Sections of this view")
                links = [el for el in walk_elements(nav) if el["tag"] == "a"]
                sections = [
                    el
                    for el in elements
                    if el["tag"] == "section"
                    and "screen-record" in el["attrs"].get("class", "").split()
                ]
                self.assertEqual(len(links), len(sections))
                for link, section in zip(links, sections, strict=True):
                    label = node_text(link)
                    self.assertTrue(label.startswith("Go to "), label)
                    self.assertNotIn("aria-label", link["attrs"])
                    heading_id = f"{section['attrs']['id']}-heading"
                    self.assertEqual(section["attrs"].get("aria-labelledby"), heading_id)
                    self.assertEqual(link["attrs"].get("href"), f"#{heading_id}")
                    self.assertEqual(link["attrs"].get("data-jump"), heading_id)
                    self.assertEqual(link["attrs"].get("data-jump-target"), heading_id)
                    headings = [
                        k for k in section["kids"] if isinstance(k, dict) and k.get("tag") == "h2"
                    ]
                    self.assertEqual(len(headings), 1)
                    self.assertEqual(headings[0]["attrs"].get("id"), heading_id)
                    self.assertEqual(headings[0]["attrs"].get("tabindex"), "-1")
                self.assertEqual(len(out["jumpClicks"]), len(sections))
                for click in out["jumpClicks"]:
                    self.assertTrue(click["prevented"], click)
                    self.assertEqual(click["focusedDelta"], 1, click)

    def test_role_hash_aliases_and_nav_active_mapping(self) -> None:
        safety_session = {
            "user": {"name": "Sam Safety", "role": "Building Safety Liaison"},
            "navigation": [{"href": "#/screens", "scope": "Specialist screens"}],
            "services": {"cases": True},
        }
        repairs_session = {
            "user": {"name": "Robin Coord", "role": "Retrofit Coordinator"},
            "navigation": [{"href": "#/screens", "scope": "Specialist screens"}],
            "services": {"cases": True},
        }
        aliases = (
            ("#/role/procurement?case=C-1", MANAGER_SESSION, "Package queue"),
            ("#/role/contractor?case=C-1", CONTRACTOR_SESSION, "Job pack and evidence checklist"),
            (
                "#/role/building_safety_lead?case=C-1",
                safety_session,
                "Building safety referral queue",
            ),
            ("#/role/repairs?case=C-1", repairs_session, "Repairs and hazard triage"),
        )
        for route_hash, session, expected_h1 in aliases:
            with self.subTest(route_hash=route_hash):
                out = run_dom(
                    {
                        "mode": "route",
                        "scripts": ["app.js", "role-screens.js"],
                        "hash": route_hash,
                        "me": session,
                        "cases": [{"id": "C-1", "address": "10 North Street", "status": "Open"}],
                        "caseDetail": {
                            "id": "C-1",
                            "needs_notice": False,
                            "named_contact": "Alex Liaison",
                        },
                        "packages": [SAMPLE_PACKAGE],
                        "orders": [SAMPLE_ORDER],
                    }
                )
                self.assertEqual(out["meta"], [])
                self.assertEqual(out["navCurrent"], ["#/screens"])
                elements = walk_elements(out["app"])
                h1_texts = [node_text(el) for el in elements if el["tag"] == "h1"]
                self.assertEqual(h1_texts, [expected_h1])
                all_sections = [el for el in elements if el["tag"] == "section"]
                shell_sections = [
                    el
                    for el in all_sections
                    if "screen-record" not in el["attrs"].get("class", "").split()
                ]
                self.assertEqual(len(shell_sections), 2)
                self.assertEqual(
                    shell_sections[0]["attrs"].get("aria-labelledby"), "screen-queue-heading"
                )
                self.assertEqual(shell_sections[1]["attrs"].get("aria-label"), "Evidence for C-1")

    def test_staff_contractor_list_and_case_views_landmarks_and_jump_links(self) -> None:
        list_out = run_dom(
            {
                "mode": "contractorList",
                "scripts": ["app.js", "ops.js"],
                "me": CONTRACTOR_SESSION,
                "cases": [
                    {
                        "id": "C-1",
                        "address": "10 North Street",
                        "town": "Leeds",
                        "postcode": "ZN1 2AB",
                        "status": "Works scheduled",
                        "needs_notice": True,
                        "named_contact": "Alex Liaison",
                        "stage": "Delivery",
                    }
                ],
                "orders": [SAMPLE_ORDER],
                "exerciseJumps": True,
            }
        )
        app_kids = [k for k in list_out["app"]["kids"] if isinstance(k, dict)]
        top_sections = [k for k in app_kids if k["tag"] == "section"]
        self.assertEqual(
            [s["attrs"].get("id") for s in top_sections],
            ["contractor-assigned-jobs", "contractor-work-orders"],
        )
        for section in top_sections:
            nested = [el for el in walk_elements(section)[1:] if el["tag"] == "section"]
            self.assertEqual(nested, [], "Work-orders landmark must be a sibling, not nested")
        list_nav = next(el for el in walk_elements(list_out["app"]) if el["tag"] == "nav")
        self.assertEqual(list_nav["attrs"].get("role"), "navigation")
        self.assertEqual(list_nav["attrs"].get("aria-label"), "Sections of your jobs")
        self.assertEqual(
            [node_text(a) for a in walk_elements(list_nav) if a["tag"] == "a"],
            ["Go to Assigned jobs", "Go to Your work orders"],
        )
        self.assertEqual([c["focusedDelta"] for c in list_out["jumpClicks"]], [1, 1])

        case_out = run_dom(
            {
                "mode": "contractorCase",
                "scripts": ["app.js"],
                "me": CONTRACTOR_SESSION,
                "caseDetail": {
                    "id": "C-1",
                    "status": "Works scheduled",
                    "needs_notice": True,
                    "named_contact": "Alex Liaison",
                    "measures": "Loft insulation",
                    "stage": "Delivery",
                    "home": {
                        "address": "10 North Street",
                        "town": "Leeds",
                        "postcode": "ZN1 2AB",
                        "type": "Terrace",
                    },
                    "contractor": {"name": "Test Ltd", "contact": "0113 000 0000"},
                    "appointments": [
                        {
                            "date": "2026-06-01",
                            "slot": "Morning",
                            "type": "Install",
                            "outcome": "Booked",
                        }
                    ],
                },
                "exerciseJumps": True,
            }
        )
        case_sections = [el for el in walk_elements(case_out["app"]) if el["tag"] == "section"]
        self.assertEqual(
            [s["attrs"].get("id") for s in case_sections],
            [
                "regulatory-supplier",
                "contractor-before-visit",
                "contractor-job-details",
                "contractor-visits",
            ],
        )
        case_nav = next(el for el in walk_elements(case_out["app"]) if el["tag"] == "nav")
        self.assertEqual(case_nav["attrs"].get("role"), "navigation")
        self.assertEqual(case_nav["attrs"].get("aria-label"), "Sections of this job")
        self.assertEqual(len(case_out["jumpClicks"]), 4)
        self.assertTrue(
            all(c["prevented"] and c["focusedDelta"] == 1 for c in case_out["jumpClicks"])
        )

    def test_delegated_jump_focus_deduplicated_across_script_load_orders(self) -> None:
        orders = (
            ["app.js"],
            ["role-screens.js"],
            ["app.js", "role-screens.js"],
            ["role-screens.js", "app.js"],
        )
        for scripts in orders:
            with self.subTest(scripts=scripts):
                res = run_dom(
                    {
                        "mode": "jumpClick",
                        "scripts": scripts,
                        "me": MANAGER_SESSION,
                        "clickInner": True,
                        "removeAccount": True,
                    }
                )
                self.assertEqual(res, {"prevented": True, "focusCount": 1})
                missing = run_dom(
                    {
                        "mode": "jumpClick",
                        "scripts": scripts,
                        "me": MANAGER_SESSION,
                        "missingTarget": True,
                    }
                )
                self.assertEqual(missing, {"prevented": True, "focusCount": 0})

    def test_non_colour_badges_pair_visual_classes_with_plain_language_state_cues(self) -> None:
        completed_order = SAMPLE_ORDER | {
            "state": "Completed",
            "corrections": [{"reason": "Seal gap", "by": "Pam Manager", "at": "2026-05-01"}],
            "history": [{"to_state": "Completed", "by": "Pam Manager", "at": "2026-05-02"}],
            "appointments": [{"outcome": "Attended", "date": "2026-05-02"}],
        }
        pkg_without_evidence = SAMPLE_PACKAGE | {
            "id": "PKG-2",
            "capacity": [
                {"contractor": "Solo Ltd", "offered": 5, "committed": 5, "in_use": 0, "headroom": 0}
            ],
        }
        proc = run_dom(
            {
                "mode": "roleScreenRender",
                "scripts": ["role-screens.js"],
                "screenId": "procurement-packages",
                "me": MANAGER_SESSION,
                "caseDetail": {"id": "C-1"},
                "packages": [SAMPLE_PACKAGE, pkg_without_evidence],
                "orders": [completed_order],
            }
        )
        badges = [
            (el["attrs"].get("class"), el["attrs"].get("data-state-cue"), node_text(el))
            for el in walk_elements(proc["app"])
            if "data-state-cue" in el.get("attrs", {})
        ]
        badge_texts = [text for _, _, text in badges]
        self.assertIn(
            (
                "status-line wait",
                "Draft readiness only",
                "State: Draft readiness only. This is not a release or approval.",
            ),
            badges,
        )
        for cls, expected_fragment in (
            ("flag", "Offered capacity remaining: 15"),
            ("flag", "Fully committed: 0"),
            ("flag danger", "Over-committed: -2"),
            ("flag", "Evidenced: signed call-off schedule"),
            ("flag danger", "Action needed: Awaiting signed schedule"),
            ("flag danger", "Unknown - not confirmed"),
            ("flag", "Met on record (scope v3)"),
            ("flag danger", "Unmet or Unknown"),
            ("flag danger", "Blocked: letting or renewal held."),
            ("flag", "Completed on record, not accepted: Completed"),
            ("flag danger", "Seal gap (Pam Manager, 2026-05-01)"),
            (
                "flag",
                "Recorded by Pam Manager on 2026-05-02. A recorded completion is not acceptance.",
            ),
            ("flag danger", "Unknown. No independent review record is supplied to this screen."),
            ("flag danger", "Action needed: Unassigned. Contracts manager to name a person."),
            ("flag danger", "Pending review: A contractor acknowledgement is not acceptance"),
            (
                "flag danger",
                "Pending independent review: Separate step by a named reviewer; "
                "not available from this screen",
            ),
        ):
            self.assertTrue(
                any(b_cls == cls and expected_fragment in b_txt for b_cls, _, b_txt in badges),
                f"Missing ({cls!r}, {expected_fragment!r}) in {badges}",
            )
        self.assertFalse(any("Unmet or Unknown: Unmet or Unknown" in t for t in badge_texts))

        jobpack = run_dom(
            {
                "mode": "roleScreenRender",
                "scripts": ["role-screens.js"],
                "screenId": "contractor-job-pack",
                "me": CONTRACTOR_SESSION,
                "caseDetail": {"id": "C-1", "needs_notice": True, "named_contact": "Alex Liaison"},
                "orders": [completed_order],
            }
        )
        jp_text = node_text(jobpack["app"])
        self.assertNotIn("Not supplied", jp_text)
        jp_badges = [
            (el["attrs"].get("class"), el["attrs"].get("data-state-cue"), node_text(el))
            for el in walk_elements(jobpack["app"])
            if "data-state-cue" in el.get("attrs", {})
        ]
        for cls, expected_fragment in (
            ("flag danger", "Visit notice required: Needs notice"),
            ("flag", "Recorded: Recorded on a work order"),
            ("flag danger", "Unknown: Not assessed on this screen"),
            ("flag danger", "Not recorded on this screen"),
            (
                "flag",
                "Completed on record, not accepted: Marked Completed on the work order by staff.",
            ),
            ("flag danger", "Not recorded. An acknowledgement is not acceptance."),
            (
                "flag danger",
                "Unknown. Review data is not available here. Done by someone other than you.",
            ),
        ):
            self.assertTrue(
                any(b_cls == cls and expected_fragment in b_txt for b_cls, _, b_txt in jp_badges),
                f"Missing ({cls!r}, {expected_fragment!r}) in {jp_badges}",
            )

    def test_contractor_views_redact_vulnerability_canaries(self) -> None:
        canary_case = {
            "id": "C-1",
            "address": "10 North Street",
            "town": "Leeds",
            "postcode": "ZN1 2AB",
            "status": "Open",
            "needs_notice": True,
            "named_contact": "Alex Liaison",
            "stage": "Delivery",
            "measures": "Loft insulation",
            "vulnerability_reason": "CANARY-VULN-REASON",
            "vulnerability_notes": "CANARY-VULN-NOTES",
            "household": "CANARY-HOUSEHOLD-DETAIL",
            "home": {
                "address": "10 North Street",
                "town": "Leeds",
                "postcode": "ZN1 2AB",
                "type": "Terrace",
            },
            "contractor": {"name": "Test Ltd", "contact": "0113 000 0000"},
            "appointments": [],
        }
        canary_order = SAMPLE_ORDER | {
            "vulnerability_reason": "CANARY-ORDER-VULN",
            "household": "CANARY-ORDER-HOUSEHOLD",
        }
        views = (
            {
                "mode": "roleScreenRender",
                "scripts": ["role-screens.js"],
                "screenId": "contractor-job-pack",
                "me": CONTRACTOR_SESSION,
                "caseDetail": canary_case,
                "orders": [canary_order],
            },
            {
                "mode": "contractorList",
                "scripts": ["app.js", "ops.js"],
                "me": CONTRACTOR_SESSION,
                "cases": [canary_case],
                "orders": [canary_order],
            },
            {
                "mode": "contractorCase",
                "scripts": ["app.js"],
                "me": CONTRACTOR_SESSION,
                "caseDetail": canary_case,
            },
        )
        for spec in views:
            with self.subTest(mode=spec["mode"]):
                rendered = json.dumps(run_dom(spec)["app"])
                self.assertNotIn("CANARY", rendered)
                self.assertIn("Visit notice required: Needs notice", rendered)

    def test_top_level_identifiers_disjoint_and_no_sys_modules_deletion(self) -> None:
        decls = {
            name: set(TOP_LEVEL_DECL.findall((WEB / name).read_text(encoding="utf-8")))
            for name in ("app.js", "ops.js", "role-screens.js")
        }
        self.assertEqual(decls["app.js"] & decls["role-screens.js"], set())
        self.assertEqual(decls["app.js"] & decls["ops.js"], set())
        self.assertEqual(decls["ops.js"] & decls["role-screens.js"], set())

        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Delete):
                for target in node.targets:
                    self.assertNotIn("modules", ast.dump(target))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in {"pop", "clear", "__delitem__"}:
                    self.assertNotIn("modules", ast.dump(node.func.value))


if __name__ == "__main__":
    unittest.main()
