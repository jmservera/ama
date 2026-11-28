"""Focused WCAG 2.2 AA verification for housing and resident screens (#232, #151).

Covers #/role/housing_officer, #/role/contact_centre, and #/role/resident_engagement routing,
polite aria-live status announcements, jump-link focus targets, table-scroll regions, row headers,
whitespace-free actForm label/id bindings, plain-language state cues in role-screens.js and
panels.js, ensure_ascii=False Unicode rendering, read-only boundaries, and server-side RBAC and
safeguarding redaction without mutating sys.modules.
"""

from __future__ import annotations

import ast
import copy
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from zava_forward.core import projection, taskqueues
from zava_forward.core.store import Store

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

NODE_WCAG_232_HARNESS = r"""
const fs = require("node:fs");
const vm = require("node:vm");

const webDir = process.argv[1];
const payload = JSON.parse(process.argv[2]);
const appSource = fs.readFileSync(webDir + "/app.js", "utf8");
const roleSource = fs.readFileSync(webDir + "/role-screens.js", "utf8");
const opsSource = fs.readFileSync(webDir + "/ops.js", "utf8");
const panelsSource = fs.readFileSync(webDir + "/panels.js", "utf8");

const h = (tag, attrs, ...kids) => {
  const safeAttrs = attrs ? { ...attrs } : {};
  return {
    tag,
    id: safeAttrs.id || "",
    attrs: safeAttrs,
    dataset: {},
    disabled: false,
    textContent: "",
    setAttribute(k, v) { this.attrs[k] = String(v); },
    removeAttribute(k) { delete this.attrs[k]; },
    focus() {},
    kids: kids
      .flat(Infinity)
      .filter((kid) => kid !== false && kid !== null && kid !== undefined),
  };
};

async function verifyRouter() {
  const navLinks = [
    { href: "#/", attrs: {} },
    { href: "#/screens", attrs: {} },
  ].map((entry) => ({
    href: entry.href,
    attrs: entry.attrs,
    getAttribute(name) { return name === "href" ? this.href : this.attrs[name] ?? null; },
    setAttribute(name, value) { this.attrs[name] = String(value); },
    removeAttribute(name) { delete this.attrs[name]; },
  }));
  const routed = [];
  const mainFocusLog = [];
  const elements = new Map();
  const getEl = (id) => {
    if (!elements.has(id)) {
      elements.set(id, {
        id,
        addEventListener() {},
        replaceChildren() {},
        focus() { if (id === "app") mainFocusLog.push(context.location.hash); },
        querySelector: () => null,
        setAttribute() {},
        removeAttribute() {},
        contains: () => false,
        textContent: "",
        hidden: false,
        open: false,
      });
    }
    return elements.get(id);
  };
  const context = vm.createContext({
    URLSearchParams,
    Intl,
    AbortController,
    clearTimeout,
    setTimeout,
    location: { hash: "#/" },
    history: { replaceState() {} },
    window: { confirm: () => true, addEventListener() {} },
    document: {
      body: { dataset: {} },
      createTextNode: (t) => ({ nodeType: 3, textContent: String(t) }),
      createElement: (tag) => ({
        tag,
        nodeType: 1,
        async: false,
        style: {},
        append() {},
        setAttribute() {},
        addEventListener() {},
        set src(_value) { if (this.onload) this.onload(); },
      }),
      getElementById: getEl,
      querySelector: (sel) => (sel === ".skip-link" ? { addEventListener() {} } : null),
      querySelectorAll: (sel) => (sel === "#nav a" ? navLinks : []),
      addEventListener() {},
      head: {
        append(...scripts) {
          for (const script of scripts) {
            if (script && typeof script.onload === "function") script.onload();
          }
        },
      },
    },
    h,
  });
  vm.runInContext(
    appSource.replace("bootstrapWorkspace().catch(startupFailed);", ""),
    context
  );
  vm.runInContext(
    `
    me = {
      user: { role: "Resident Liaison Officer" },
      navigation: [
        { href: "#/", scope: "Assigned cases" },
        { href: "#/screens", scope: "Role screens" },
      ],
      services: { cases: true },
    };
    globalThis.AsyncAction = { handler() {}, run() {}, feedback() {} };
    globalThis.chatCasePanel = function () {};
    employeeChat = { install() {}, reset() {} };
    `,
    context
  );

  const destinationChecks = {
    housingBare: vm.runInContext('isRoleScreensDestination("#/role/housing_officer")', context),
    housingQuery: vm.runInContext(
      'isRoleScreensDestination("#/role/housing_officer?case=C-1&page=2")',
      context
    ),
    contactBare: vm.runInContext('isRoleScreensDestination("#/role/contact_centre")', context),
    contactQuery: vm.runInContext(
      'isRoleScreensDestination("#/role/contact_centre?case=C-1&page=2")',
      context
    ),
    engagementBare: vm.runInContext(
      'isRoleScreensDestination("#/role/resident_engagement")',
      context
    ),
    engagementQuery: vm.runInContext(
      'isRoleScreensDestination("#/role/resident_engagement?case=C-1")',
      context
    ),
    programmeBare: vm.runInContext(
      'isRoleScreensDestination("#/role/programme_manager")',
      context
    ),
    programmeQuery: vm.runInContext(
      'isRoleScreensDestination("#/role/programme_manager?case=C-1&page=1")',
      context
    ),
    coordinatorBare: vm.runInContext(
      'isRoleScreensDestination("#/role/retrofit_coordinator")',
      context
    ),
    coordinatorQuery: vm.runInContext(
      'isRoleScreensDestination("#/role/retrofit_coordinator?case=C-1")',
      context
    ),
    unknownRole: vm.runInContext('isRoleScreensDestination("#/role/unknown")', context),
    protoRole: vm.runInContext('isRoleScreensDestination("#/role/toString")', context),
  };

  const staffScripts = {
    housing: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/housing_officer?case=C-1", false)', context)
    ),
    contact: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/contact_centre?case=C-1", false)', context)
    ),
    engagement: Array.from(
      vm.runInContext(
        'missingWorkspaceScripts("#/role/resident_engagement?case=C-1", false)',
        context
      )
    ),
  };
  vm.runInContext('me.user.role = "Contractor";', context);
  const contractorScripts = {
    housing: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/housing_officer?case=C-1", false)', context)
    ),
    contact: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/contact_centre?case=C-1", false)', context)
    ),
    engagement: Array.from(
      vm.runInContext(
        'missingWorkspaceScripts("#/role/resident_engagement?case=C-1", false)',
        context
      )
    ),
  };

  vm.runInContext(
    `
    me.user.role = "Resident Liaison Officer";
    roleScreensView = async function () {
      routed.push(location.hash);
      show(h("h1", {}, "Screen"));
    };
    `,
    Object.assign(context, { routed })
  );

  const navStates = {};
  for (const hash of [
    "#/role/housing_officer",
    "#/role/housing_officer?case=C-1",
    "#/role/contact_centre",
    "#/role/contact_centre?case=C-1",
    "#/role/resident_engagement",
    "#/role/resident_engagement?case=C-1",
  ]) {
    context.location.hash = hash;
    await vm.runInContext("route()", context);
    navStates[hash] = {
      screensCurrent: navLinks[1].attrs["aria-current"] || null,
      homeCurrent: navLinks[0].attrs["aria-current"] || null,
    };
  }
  return { destinationChecks, staffScripts, contractorScripts, routed, navStates, mainFocusLog };
}

async function runHostScenario(opts) {
  const shownSnapshots = [];
  const statusHistory = [];
  let clickListener = null;
  const focusEvents = [];
  const lookupCounts = {};
  const targets = new Map();
  let currentStatus = "";
  const workspaceStatus = {
    get textContent() { return currentStatus; },
    set textContent(val) {
      currentStatus = String(val);
      statusHistory.push(currentStatus);
    },
  };
  const routeController = new AbortController();
  const context = vm.createContext({
    URLSearchParams,
    Intl,
    AbortController,
    Date,
    location: { hash: opts.hash },
    routeController,
    me: { user: { role: opts.role } },
    workspaceStatus,
    document: {
      addEventListener(type, fn) {
        if (type === "click") clickListener = fn;
      },
      getElementById(id) {
        lookupCounts[id] = (lookupCounts[id] || 0) + 1;
        return targets.get(id) || null;
      },
    },
    api: async (url) => {
      if (opts.abortDuringLoad) routeController.abort();
      if (url.startsWith("/api/cases?")) {
        return { items: opts.queueItems, total: opts.queueTotal ?? opts.queueItems.length };
      }
      if (url.startsWith("/api/resident/choice-queue?")) {
        return opts.choiceQueue;
      }
      if (url.startsWith("/api/cases/")) {
        if (opts.mismatchCaseId) return { id: opts.mismatchCaseId };
        const requested = decodeURIComponent(url.slice("/api/cases/".length));
        if (opts.caseRecord && requested === opts.caseRecord.id) return opts.caseRecord;
        throw new Error("unavailable");
      }
      return {};
    },
    h,
    show: (...nodes) => {
      shownSnapshots.push(nodes);
    },
  });
  vm.runInContext(
    roleSource +
      "\n;globalThis.__screens = roleScreens;" +
      "globalThis.__roleHashScreens = ROLE_HASH_SCREENS;" +
      "globalThis.__programmeOverviewSections = programmeOverviewSections;",
    context
  );
  const registeredScreenIds = Array.from(context.__screens.keys());
  const roleHashScreens = Object.assign({}, context.__roleHashScreens);
  const programmeOverviewSectionIds = Array.from(
    context.__programmeOverviewSections,
    ([sectionId]) => sectionId
  );
  if (opts.clearScreens) {
    vm.runInContext("roleScreens.clear();", context);
  }
  let abortedError = false;
  try {
    await vm.runInContext("roleScreensView()", context);
  } catch (err) {
    if (opts.abortDuringLoad) abortedError = true;
    else throw err;
  }

  const finalShown = shownSnapshots.length ? shownSnapshots[shownSnapshots.length - 1] : [];
  const registerHeadings = (node) => {
    if (!node || typeof node !== "object") return;
    if (node.attrs && node.attrs.id) {
      targets.set(node.attrs.id, {
        id: node.attrs.id,
        tag: node.tag,
        tabindex: node.attrs.tabindex,
        focus() { focusEvents.push({ action: "focus", id: node.attrs.id }); },
        scrollIntoView(scrollOpts) {
          focusEvents.push({
            action: "scroll",
            id: node.attrs.id,
            block: scrollOpts && scrollOpts.block,
          });
        },
      });
    }
    for (const kid of node.kids || []) registerHeadings(kid);
  };
  finalShown.forEach(registerHeadings);

  const jumpTests = [];
  const triggerJumpLinks = (node) => {
    if (!node || typeof node !== "object") return;
    if (node.tag === "a" && node.attrs && node.attrs["data-jump"]) {
      const targetId = node.attrs["data-jump"];
      const beforeLookups = lookupCounts[targetId] || 0;
      let prevented = false;
      clickListener({
        target: {
          closest: (sel) =>
            sel === "a[data-jump]"
              ? { getAttribute: (attr) => node.attrs[attr] ?? null }
              : null,
        },
        preventDefault() { prevented = true; },
      });
      jumpTests.push({
        target: targetId,
        prevented,
        lookupsForClick: (lookupCounts[targetId] || 0) - beforeLookups,
      });
    }
    for (const kid of node.kids || []) triggerJumpLinks(kid);
  };
  if (clickListener && opts.exerciseJumps) {
    finalShown.forEach(triggerJumpLinks);
  }

  let truncatedTable = null;
  if (opts.checkTruncation) {
    truncatedTable = vm.runInContext(
      `screenTable("Truncated measure rows", ["Col A"], ` +
        `Array.from({ length: 55 }, (_, i) => ["Row " + i]), 50, undefined, true)`,
      context
    );
  }

  return {
    shownSnapshots,
    finalShown,
    workspaceStatus: workspaceStatus.textContent,
    statusHistory,
    focusEvents,
    jumpTests,
    abortedError,
    truncatedTable,
    registeredScreenIds,
    roleHashScreens,
    programmeOverviewSectionIds,
  };
}

function runResidentPanels() {
  const context = vm.createContext({
    URLSearchParams,
    Intl,
    Date,
    caseSession: { historyBarrier: false, rawFormStates: new Map() },
    me: {
      user: { role: "Retrofit Programme Manager" },
      staff: [
        { email: "sam@example.test", name: "Sam Liaison", role: "Resident Liaison Officer" },
        { email: "rex@example.test", name: "Rex Coordinator", role: "Retrofit Coordinator" },
      ],
    },
    document: {
      activeElement: null,
      getElementById: () => null,
      querySelector: () => null,
    },
    AsyncAction: {
      handler(_control, fn) { return fn; },
      feedback() {},
    },
    api: async () => ({}),
    toast() {},
    stamp: (v) => v || "Unknown",
    h,
  });
  vm.runInContext(opsSource + "\n" + panelsSource, context);
  context.__cases = payload.panelCases;
  const contractor = vm.runInContext(
    'residentPanel(__cases.contractor, "C-CON", async () => {})',
    context
  );
  const staffFull = vm.runInContext(
    'residentPanel(__cases.staffFull, "C-FULL", async () => {})',
    context
  );
  const staffEmpty = vm.runInContext(
    'residentPanel(__cases.staffEmpty, "C-EMPTY", async () => {})',
    context
  );
  const duplicateForm = vm.runInContext(
    'actForm("Record resident note!", [["note", "First"], ["note", "Second"]], async () => {})',
    context
  );
  return { contractor, staffFull, staffEmpty, duplicateForm };
}

(async () => {
  const router = await verifyRouter();
  const contactUnselected = await runHostScenario({
    hash: "#/role/contact_centre",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    checkTruncation: true,
  });
  const contactSelected = await runHostScenario({
    hash: "#/role/contact_centre?case=C-1",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    exerciseJumps: true,
  });
  const housingSelected = await runHostScenario({
    hash: "#/role/housing_officer?case=C-1",
    role: "Retrofit Coordinator",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    exerciseJumps: true,
  });
  const engagementSelected = await runHostScenario({
    hash: "#/role/resident_engagement?case=C-1",
    role: "Resident Liaison Officer",
    caseRecord: payload.choiceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    exerciseJumps: true,
  });
  const unicodeSelected = await runHostScenario({
    hash: "#/role/resident_engagement?case=C-UNICODE",
    role: "Resident Liaison Officer",
    caseRecord: payload.unicodeCase,
    queueItems: [{ id: "C-UNICODE", address: "Flat 3B, Tŷ Nant", status: "Active", hazard: false }],
    choiceQueue: payload.choiceQueue,
  });
  const deniedRoutes = {};
  for (const role of [
    "Contractor",
    "Quality Inspector",
    "Building Safety Liaison",
    "Grants and Evidence Officer",
  ]) {
    deniedRoutes[role] = {};
    for (const hash of [
      "#/role/housing_officer",
      "#/role/contact_centre",
      "#/role/resident_engagement",
    ]) {
      const res = await runHostScenario({
        hash,
        role,
        caseRecord: payload.serviceFull,
        queueItems: payload.queueItems,
        choiceQueue: payload.choiceQueue,
      });
      deniedRoutes[role][hash] = {
        status: res.workspaceStatus,
        finalShown: res.finalShown,
      };
    }
  }
  const protoDenied = await runHostScenario({
    hash: "#/role/toString",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
  });
  const invalidPage = await runHostScenario({
    hash: "#/role/contact_centre?page=abc",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
  });
  const chooserInstalled = await runHostScenario({
    hash: "#/screens",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
  });
  const chooserEmpty = await runHostScenario({
    hash: "#/screens",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    clearScreens: true,
  });
  const mismatchCase = await runHostScenario({
    hash: "#/role/contact_centre?case=C-1",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    mismatchCaseId: "C-OTHER",
  });
  const abortedLoad = await runHostScenario({
    hash: "#/role/contact_centre?case=C-1",
    role: "Resident Liaison Officer",
    caseRecord: payload.serviceFull,
    queueItems: payload.queueItems,
    choiceQueue: payload.choiceQueue,
    abortDuringLoad: true,
  });
  const panels = runResidentPanels();

  console.log(
    JSON.stringify({
      router,
      contactUnselected,
      contactSelected,
      housingSelected,
      engagementSelected,
      unicodeSelected,
      deniedRoutes,
      protoDenied,
      invalidPage,
      chooserInstalled,
      chooserEmpty,
      mismatchCase,
      abortedLoad,
      panels,
    })
  );
})().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
"""


def node_text(node: object) -> str:
    if node is None or isinstance(node, bool):
        return ""
    if not isinstance(node, dict):
        return str(node)
    return " ".join(part for kid in node.get("kids", []) if (part := node_text(kid))).strip()


def walk_nodes(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, list):
        for item in node:
            found.extend(walk_nodes(item))
        return found
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found.extend(walk_nodes(kid))
    return found


def build_payload() -> dict[str, Any]:
    queue_items = [
        {
            "id": "C-1",
            "address": "14 Oak Lane",
            "town": "Leeds",
            "status": "Active",
            "hazard": True,
        },
        {
            "id": "C-2",
            "address": "22 Birch Walk",
            "town": "Leeds",
            "status": "Survey booked",
            "hazard": False,
        },
    ]
    choice_queue = {
        "total": 2,
        "items": [
            {
                "id": "C-1",
                "address": "14 Oak Lane",
                "town": "Leeds",
                "measure_decisions": [
                    {"measure": "Loft insulation", "status": "Accepted"},
                    {"measure": "Heat pump", "status": "Paused"},
                ],
                "resident_update": {
                    "status": "Outstanding",
                    "purpose": "Confirm loft access slot",
                    "owner_identity": {"name": "Sam Liaison"},
                    "due_at": "2026-11-20T10:00:00Z",
                },
            },
            {
                "id": "C-2",
                "address": "22 Birch Walk",
                "town": "Leeds",
                "measure_decisions": [{"measure": "Windows", "status": "Waiting"}],
                "resident_update": None,
            },
        ],
    }
    choice_full: dict[str, Any] = {
        "id": "C-1",
        "measure_decisions": [
            {
                "measure": "Loft insulation",
                "status": "Accepted",
                "readiness": "Resident decision current",
                "context": {"scope": "S1", "revision": 2, "design_version": 1},
                "versions": [
                    {
                        "version": 1,
                        "status": "Accepted",
                        "scope": "S1",
                        "context_revision": 2,
                        "design_version": 1,
                        "answered_by": "Resident",
                        "recorded_by": "Sam Liaison",
                        "at": "2026-11-10T09:00:00Z",
                        "note": "Agreed after survey walkthrough",
                    }
                ],
            },
            {
                "measure": "Heat pump",
                "status": "Paused",
                "readiness": "Needs human review",
                "context": None,
                "versions": [
                    {
                        "version": 2,
                        "status": "Paused",
                        "scope": "S2",
                        "context_revision": 1,
                        "design_version": 1,
                        "answered_by": "Representative",
                        "recorded_by": "Sam Liaison",
                        "at": "2026-11-11T14:00:00Z",
                        "note": "Waiting on medical room layout",
                    }
                ],
            },
        ],
        "resident_update": {
            "status": "Outstanding",
            "purpose": "Confirm loft access slot",
            "owner_identity": {"name": "Sam Liaison"},
            "due_at": "2026-11-20T10:00:00Z",
            "basis": "Resident telephone request",
            "safe_contact_ref": "SAFE-REF-9",
            "at": "2026-11-11T15:00:00Z",
            "opened_at": "2026-11-10T09:30:00Z",
            "version": 2,
        },
    }
    service_full: dict[str, Any] = {
        "id": "C-1",
        "resident_update": choice_full["resident_update"],
        "service_requests": [
            {
                "id": "SR-1",
                "route": "Complaint",
                "status": "Open",
                "version": 2,
                "summary": "Scaffolding blocking mobility scooter path",
                "desired_outcome": "Clear ramp access before Friday",
                "service_owner": "Neighbourhood Housing",
                "redress_owner": "Complaints Team",
                "accessibility": ["Large print", "Step-free visits"],
                "representative_ref": "REP-12",
                "next_update": "2026-11-18",
                "status_owner": {"name": "Rex Coordinator"},
                "status_at": "2026-11-12T10:00:00Z",
                "opened_at": "2026-11-11T08:00:00Z",
                "remedy": {
                    "status": "In progress",
                    "version": 1,
                    "owner": {"name": "Sam Liaison"},
                    "at": "2026-11-12T11:00:00Z",
                    "opened_at": "2026-11-11T08:30:00Z",
                },
                "history": [
                    {
                        "kind": "Response owner reassigned",
                        "responsibility": "service",
                        "at": "2026-11-12T10:00:00Z",
                        "actor": {"name": "Pam Manager"},
                        "changes": {
                            "old": {"name": "Sam Liaison"},
                            "new": {"name": "Rex Coordinator"},
                        },
                        "note": "Coordinating scaffold adjustment",
                    }
                ],
            },
            {
                "id": "SR-2",
                "route": "Service request",
                "status": "Closed",
                "version": 1,
                "summary": "Heating timer explanation",
                "desired_outcome": "Written operating card",
                "service_owner": "Resident Engagement",
                "redress_owner": "None",
                "accessibility": ["Plain English"],
                "representative_ref": None,
                "next_update": "None",
                "status_owner": {"name": "Sam Liaison"},
                "status_at": "2026-11-13T12:00:00Z",
                "opened_at": "2026-11-10T09:00:00Z",
                "remedy": {
                    "status": "Closed",
                    "version": 2,
                    "owner": {"name": "Sam Liaison"},
                    "at": "2026-11-13T12:00:00Z",
                    "opened_at": "2026-11-10T09:00:00Z",
                },
                "history": [],
            },
        ],
    }
    unicode_case = {
        "id": "C-UNICODE",
        "measure_decisions": [
            {
                "measure": "Solar PV (Tŷ Nant)",
                "status": "Declined",
                "readiness": "Needs human review",
                "context": {"scope": "S-Ü1", "revision": 1, "design_version": 1},
                "versions": [
                    {
                        "version": 1,
                        "status": "Declined",
                        "scope": "S-Ü1",
                        "context_revision": 1,
                        "design_version": 1,
                        "answered_by": "Siân O'Connor",
                        "recorded_by": "Zoë Müller",
                        "at": "2026-11-14T10:00:00Z",
                        "note": "Prefers façade conservation review first",
                    }
                ],
            }
        ],
        "resident_update": {
            "status": "Proposed",
            "purpose": "Follow up with Siân O'Connor",
            "owner_identity": {"name": "Zoë Müller"},
            "due_at": "2026-11-22T09:00:00Z",
            "basis": "Home visit",
            "safe_contact_ref": "",
            "at": "2026-11-14T10:05:00Z",
            "opened_at": "2026-11-14T10:00:00Z",
            "version": 1,
        },
    }
    panel_cases = {
        "contractor": {
            "resident_readiness": [
                {"measure": "Loft insulation", "flag": "Proceed"},
                {"measure": "Heat pump", "flag": "Hold"},
                {"measure": "Windows", "flag": ""},
            ]
        },
        "staffFull": {
            "can_record_resident": True,
            "measure_decisions": [
                choice_full["measure_decisions"][0],
                {
                    "measure": "Windows",
                    "status": "Waiting",
                    "readiness": "",
                    "context": None,
                    "versions": [],
                },
            ],
            "resident_update": {
                **choice_full["resident_update"],
                "purpose": "SYN browser update",
            },
            "service_requests": [
                service_full["service_requests"][0],
                {
                    **service_full["service_requests"][1],
                    "remedy": {
                        "status": "Open",
                        "version": 0,
                        "owner": {"name": "Rex Coordinator"},
                        "at": "2026-11-13T12:00:00Z",
                        "opened_at": "2026-11-10T09:00:00Z",
                    },
                },
            ],
        },
        "staffEmpty": {
            "can_record_resident": False,
            "measure_decisions": [],
            "resident_update": None,
            "service_requests": [],
        },
    }
    return {
        "queueItems": queue_items,
        "choiceQueue": choice_queue,
        "choiceFull": choice_full,
        "serviceFull": service_full,
        "unicodeCase": unicode_case,
        "panelCases": panel_cases,
    }


class HousingResidentWcag232Tests(unittest.TestCase):
    data: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        payload_json = json.dumps(build_payload(), ensure_ascii=False)
        proc = subprocess.run(
            ["node", "-e", NODE_WCAG_232_HARNESS, str(WEB), payload_json],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if proc.returncode != 0:
            raise AssertionError(f"Node WCAG #232 harness failed:\n{proc.stderr}")
        cls.data = json.loads(proc.stdout)

    def test_test_module_does_not_mutate_sys_modules(self) -> None:
        tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr == "modules":
                if isinstance(node.value, ast.Name) and node.value.id == "sys":
                    self.fail("test_housing_resident_wcag_232.py must not touch sys.modules")

    def test_static_shell_css_and_table_guards_hold(self) -> None:
        index_html = (WEB / "index.html").read_text(encoding="utf-8")
        style_css = (WEB / "style.css").read_text(encoding="utf-8")
        self.assertIn('class="skip-link" href="#app"', index_html)
        self.assertIn('<main id="app" tabindex="-1">', index_html)
        self.assertIn('id="workspace-status"', index_html)
        self.assertIn('aria-live="polite"', index_html)
        self.assertIn(":focus-visible", style_css)
        self.assertIn("prefers-reduced-motion:reduce", style_css)
        self.assertIn("forced-colors:active", style_css)
        self.assertIn(".table-scroll", style_css)

        tables = 0
        aria_invalid = 0
        for path in sorted(WEB.glob("*.js")):
            source = path.read_text(encoding="utf-8")
            self.assertNotIn('h("th", {}', source, path.name)
            aria_invalid += source.count('setAttribute("aria-invalid", "true")')
            for match in re.finditer(r'h\("table", \{\},\s*(.{0,60})', source):
                tables += 1
                self.assertIn('h("caption"', match.group(1), path.name)
        self.assertEqual(tables, 18)
        self.assertEqual(aria_invalid, 9)

    def test_contact_centre_housing_and_resident_routes_and_script_isolation(self) -> None:
        router = self.data["router"]
        checks = router["destinationChecks"]
        for key in (
            "housingBare",
            "housingQuery",
            "contactBare",
            "contactQuery",
            "engagementBare",
            "engagementQuery",
            "programmeBare",
            "programmeQuery",
            "coordinatorBare",
            "coordinatorQuery",
        ):
            self.assertTrue(checks[key], key)
        self.assertFalse(checks["unknownRole"])
        self.assertFalse(checks["protoRole"])

        coexistence = self.data["contactUnselected"]
        for screen_id in ("programme-queue", "resident-choice", "resident-service-issues"):
            self.assertIn(screen_id, coexistence["registeredScreenIds"])
        role_hash_screens = coexistence["roleHashScreens"]
        self.assertEqual(role_hash_screens.get("#/role/housing_officer"), "resident-service-issues")
        self.assertEqual(role_hash_screens.get("#/role/contact_centre"), "resident-service-issues")
        self.assertEqual(role_hash_screens.get("#/role/resident_engagement"), "resident-choice")
        self.assertEqual(role_hash_screens.get("#/role/programme_manager"), "programme-queue")
        self.assertEqual(role_hash_screens.get("#/role/retrofit_coordinator"), "programme-queue")
        for overview_id in ("programme-shared-queue", "programme-funnel"):
            self.assertIn(overview_id, coexistence["programmeOverviewSectionIds"])

        for group in (router["staffScripts"], router["contractorScripts"]):
            for route_key, scripts in group.items():
                self.assertIn("/role-screens.js", scripts, route_key)
                self.assertNotIn("/ops.js", scripts, route_key)

        expected_hashes = [
            "#/role/housing_officer",
            "#/role/housing_officer?case=C-1",
            "#/role/contact_centre",
            "#/role/contact_centre?case=C-1",
            "#/role/resident_engagement",
            "#/role/resident_engagement?case=C-1",
        ]
        self.assertEqual(router["routed"], expected_hashes)
        self.assertEqual(router["mainFocusLog"], expected_hashes)
        for route_hash in expected_hashes:
            state = router["navStates"][route_hash]
            self.assertEqual(state["screensCurrent"], "page", route_hash)
            self.assertIsNone(state["homeCurrent"], route_hash)

    def test_default_deny_and_prototype_safety_across_all_three_role_routes(self) -> None:
        for role, by_hash in self.data["deniedRoutes"].items():
            for route_hash, outcome in by_hash.items():
                with self.subTest(role=role, route_hash=route_hash):
                    self.assertEqual(outcome["status"], f"{role}. Screen unavailable.")
                    alerts = [
                        n
                        for n in walk_nodes(outcome["finalShown"])
                        if n.get("attrs", {}).get("role") == "alert"
                    ]
                    self.assertTrue(alerts)
                    self.assertIn("Screen unavailable", node_text(outcome["finalShown"]))

        proto = self.data["protoDenied"]
        self.assertEqual(
            proto["workspaceStatus"],
            "Resident Liaison Officer. Specialist screens. Choose a screen.",
        )

    def test_aria_live_polite_and_workspace_status_lifecycle_announcements(self) -> None:
        unselected = self.data["contactUnselected"]
        self.assertEqual(
            unselected["statusHistory"],
            [
                "Resident Liaison Officer. Resident service issue queue. "
                "Loading recorded evidence.",
                "Resident Liaison Officer. Resident service issue queue. No home selected.",
            ],
        )
        loading_nodes = walk_nodes(unselected["shownSnapshots"][0])
        loading_statuses = [n for n in loading_nodes if n.get("attrs", {}).get("role") == "status"]
        self.assertEqual(len(loading_statuses), 1)
        self.assertEqual(loading_statuses[0]["attrs"].get("aria-live"), "polite")

        trunc_statuses = [
            n
            for n in walk_nodes(unselected["truncatedTable"])
            if n.get("attrs", {}).get("role") == "status"
        ]
        self.assertEqual(len(trunc_statuses), 1)
        self.assertEqual(trunc_statuses[0]["attrs"].get("aria-live"), "polite")
        self.assertIn("Showing the first 50 of 55 records.", node_text(trunc_statuses[0]))

        for scenario_key, expected_final in (
            (
                "contactSelected",
                "Resident Liaison Officer. Resident service issue queue. Selected home C-1.",
            ),
            (
                "housingSelected",
                "Retrofit Coordinator. Resident service issue queue. Selected home C-1.",
            ),
            (
                "engagementSelected",
                "Resident Liaison Officer. Resident choice and update queue. Selected home C-1.",
            ),
        ):
            scenario = self.data[scenario_key]
            self.assertEqual(scenario["workspaceStatus"], expected_final, scenario_key)
            for status_node in (
                n
                for n in walk_nodes(scenario["finalShown"])
                if n.get("attrs", {}).get("role") == "status"
            ):
                self.assertEqual(status_node["attrs"].get("aria-live"), "polite", scenario_key)

        self.assertEqual(
            self.data["invalidPage"]["workspaceStatus"],
            "Resident Liaison Officer. Invalid screen page.",
        )
        self.assertEqual(
            self.data["chooserInstalled"]["workspaceStatus"],
            "Resident Liaison Officer. Specialist screens. Choose a screen.",
        )
        self.assertEqual(
            self.data["chooserEmpty"]["workspaceStatus"],
            "Resident Liaison Officer. Specialist screens. No specialist screens installed.",
        )
        self.assertEqual(
            self.data["mismatchCase"]["workspaceStatus"],
            "Resident Liaison Officer. Resident service issue queue. Record mismatch.",
        )
        self.assertTrue(self.data["abortedLoad"]["abortedError"])
        self.assertEqual(
            self.data["abortedLoad"]["workspaceStatus"],
            "Resident Liaison Officer. Resident service issue queue. Loading recorded evidence.",
        )

    def test_specialist_landmarks_headings_jump_focus_tables_cues_and_read_only_safety(
        self,
    ) -> None:
        forbidden_tags = {"input", "select", "textarea", "button", "form"}
        for key in ("contactSelected", "housingSelected", "engagementSelected", "unicodeSelected"):
            scenario = self.data[key]
            nodes = walk_nodes(scenario["finalShown"])
            with self.subTest(scenario=key):
                headings = [
                    int(n["tag"][1])
                    for n in nodes
                    if n["tag"] in {"h1", "h2", "h3", "h4", "h5", "h6"}
                ]
                self.assertTrue(headings and headings[0] == 1)
                for prev, curr in zip(headings, headings[1:], strict=False):
                    self.assertLessEqual(curr, prev + 1, f"Skipped heading level: {headings}")

                jump_navs = [
                    n
                    for n in nodes
                    if n["tag"] == "nav"
                    and n["attrs"].get("role") == "navigation"
                    and n["attrs"].get("aria-label") == "Sections of this view"
                ]
                self.assertEqual(len(jump_navs), 1)
                jump_links = [n for n in walk_nodes(jump_navs[0]) if n["tag"] == "a"]
                self.assertGreaterEqual(len(jump_links), 3)
                node_by_id = {n["attrs"]["id"]: n for n in nodes if n.get("attrs", {}).get("id")}
                expected_case_id = "C-UNICODE" if key == "unicodeSelected" else "C-1"
                evidence_section = node_by_id.get("screen-evidence")
                self.assertIsNotNone(evidence_section)
                assert evidence_section is not None
                self.assertEqual(
                    evidence_section["attrs"].get("aria-label"),
                    f"Evidence for {expected_case_id}",
                )
                for link in jump_links:
                    self.assertTrue(node_text(link).startswith("Go to "))
                    target_id = link["attrs"]["data-jump"]
                    self.assertEqual(link["attrs"].get("href"), f"#{target_id}")
                    heading = node_by_id.get(target_id)
                    self.assertIsNotNone(heading, target_id)
                    assert heading is not None
                    self.assertEqual(heading["tag"], "h2")
                    self.assertEqual(heading["attrs"].get("tabindex"), -1)

                for node in nodes:
                    self.assertNotIn(node["tag"], forbidden_tags)
                    href = str(node.get("attrs", {}).get("href", ""))
                    self.assertFalse(href.startswith(("mailto:", "tel:")))

                tables = [n for n in nodes if n["tag"] == "table"]
                self.assertGreaterEqual(len(tables), 1)
                regions = [
                    n
                    for n in nodes
                    if n["tag"] == "div" and n["attrs"].get("class") == "table-scroll"
                ]
                self.assertEqual(len(regions), len(tables))
                for region in regions:
                    self.assertEqual(region["attrs"].get("role"), "region")
                    self.assertTrue(region["attrs"].get("aria-label"))
                    self.assertEqual(region["attrs"].get("tabindex"), 0)

                for table in tables:
                    self.assertEqual(table["kids"][0]["tag"], "caption")
                    self.assertTrue(node_text(table["kids"][0]))
                    thead_ths = [n for n in walk_nodes(table["kids"][1]) if n["tag"] == "th"]
                    self.assertTrue(thead_ths)
                    for th in thead_ths:
                        self.assertEqual(th["attrs"].get("scope"), "col")
                    tbody_trs = [kid for kid in table["kids"][2]["kids"] if kid["tag"] == "tr"]
                    for tr in tbody_trs:
                        self.assertEqual(tr["kids"][0]["tag"], "th")
                        self.assertEqual(tr["kids"][0]["attrs"].get("scope"), "row")

        for key in ("contactSelected", "housingSelected", "engagementSelected"):
            scenario = self.data[key]
            self.assertTrue(scenario["jumpTests"])
            for jump in scenario["jumpTests"]:
                self.assertTrue(jump["prevented"])
                self.assertIn(jump["lookupsForClick"], (1, 2))
            self.assertEqual(len(scenario["focusEvents"]), len(scenario["jumpTests"]) * 2)
            for idx, jump in enumerate(scenario["jumpTests"]):
                focus_ev = scenario["focusEvents"][idx * 2]
                scroll_ev = scenario["focusEvents"][idx * 2 + 1]
                self.assertEqual(focus_ev, {"action": "focus", "id": jump["target"]})
                self.assertEqual(
                    scroll_ev,
                    {"action": "scroll", "id": jump["target"], "block": "start"},
                )

        unicode_text = node_text(self.data["unicodeSelected"]["finalShown"])
        self.assertIn("Siân O'Connor", unicode_text)
        self.assertIn("Zoë Müller", unicode_text)
        self.assertIn("Tŷ Nant", unicode_text)
        self.assertIn("Confirmed: Declined", unicode_text)
        self.assertIn("Action needed: Proposed", unicode_text)

    def test_panels_actform_slugs_table_semantics_and_textual_state_cues(self) -> None:
        panels = self.data["panels"]

        contractor_text = node_text(panels["contractor"])
        self.assertIn("Decision for each measure", contractor_text)
        self.assertIn("Confirmed: Proceed", contractor_text)
        self.assertIn("Action needed: Hold", contractor_text)
        self.assertIn("Action needed: Unknown", contractor_text)
        cues = [
            n
            for n in walk_nodes(panels["contractor"])
            if n.get("attrs", {}).get("data-state-cue") == "readiness"
        ]
        self.assertEqual(len(cues), 3)

        dup_inputs = [
            n for n in walk_nodes(panels["duplicateForm"]) if n["tag"] in {"input", "select"}
        ]
        self.assertEqual(
            [n["attrs"]["id"] for n in dup_inputs],
            ["f-record-resident-note-note", "f-record-resident-note-note-2"],
        )

        staff_nodes = walk_nodes(panels["staffFull"])
        controls = [n for n in staff_nodes if n["tag"] in {"input", "select", "textarea"}]
        control_ids = [str(n["attrs"].get("id", "")) for n in controls]
        self.assertTrue(control_ids)
        self.assertEqual(len(control_ids), len(set(control_ids)))
        actform_ids = [cid for cid in control_ids if cid.startswith("f-")]
        self.assertTrue(actform_ids)
        for cid in actform_ids:
            self.assertRegex(cid, r"^f-[a-z0-9-]+$")
        for cid in control_ids:
            self.assertRegex(cid, r"^[A-Za-z0-9_-]+$")

        labels = [n for n in staff_nodes if n["tag"] == "label"]
        self.assertEqual(len(labels), len(controls))
        for label in labels:
            target = str(label["attrs"].get("for", ""))
            self.assertIn(target, control_ids)

        dup_buttons = [n for n in walk_nodes(panels["duplicateForm"]) if n["tag"] == "button"]
        self.assertEqual(len(dup_buttons), 1)
        self.assertEqual(dup_buttons[0]["attrs"].get("type"), "button")

        buttons = [n for n in staff_nodes if n["tag"] == "button"]
        self.assertTrue(buttons)
        for btn in buttons:
            self.assertIn(btn["attrs"].get("type"), {"button", "submit"})

        regions = [
            n
            for n in staff_nodes
            if n["tag"] == "div" and n["attrs"].get("class") == "table-scroll"
        ]
        self.assertEqual(len(regions), 1)
        self.assertEqual(regions[0]["attrs"].get("role"), "region")
        self.assertEqual(regions[0]["attrs"].get("aria-label"), "Resident decisions by measure")
        self.assertEqual(regions[0]["attrs"].get("tabindex"), 0)

        tables = [n for n in walk_nodes(regions[0]) if n["tag"] == "table"]
        self.assertEqual(len(tables), 1)
        table = tables[0]
        self.assertEqual(table["kids"][0]["tag"], "caption")
        self.assertEqual(node_text(table["kids"][0]), "Resident decisions by measure")
        tbody_rows = [kid for kid in table["kids"][2]["kids"] if kid["tag"] == "tr"]
        self.assertEqual(len(tbody_rows), 2)
        for row in tbody_rows:
            self.assertEqual(row["kids"][0]["tag"], "th")
            self.assertEqual(row["kids"][0]["attrs"].get("scope"), "row")

        staff_text = node_text(panels["staffFull"])
        for expected in (
            "Confirmed: Accepted. Confirmed: Resident decision current",
            "Waiting for resident: Waiting. Waiting for resident: Unknown",
            "Waiting for resident: None",
            "Action needed: Outstanding: SYN browser update.",
            "Version 2.",
            "SR-1: Complaint. Action needed: Open.",
            "State: Action needed. Response: Open. Owner: Rex Coordinator.",
            "State: Action needed. Remedy: In progress. Owner: Sam Liaison.",
            "SR-2: Service request. Confirmed: Closed.",
            "State: Confirmed. Response: Closed. Owner: Sam Liaison.",
            "State: Action needed. Remedy: Open. Owner: Rex Coordinator.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, staff_text)

        empty_text = node_text(panels["staffEmpty"])
        self.assertIn("Action needed: No commitment recorded.", empty_text)
        self.assertIn("State: None recorded. No requests recorded.", empty_text)

    def test_server_resident_choice_queue_rbac_and_safeguarding_redaction(self) -> None:
        for role in projection.STAFF_ROLES:
            self.assertTrue(
                projection.allowed({"role": role}, "resident_choice_queue", "GET"),
                role,
            )
        for denied_role in ("Contractor", "Application Administrator", "Unknown Role", ""):
            self.assertFalse(
                projection.allowed({"role": denied_role}, "resident_choice_queue", "GET"),
                denied_role,
            )

        with tempfile.TemporaryDirectory() as tmp:
            raw = copy.deepcopy(dataset.DATA)
            for code, role in (
                ("rc_232", "Retrofit Coordinator"),
                ("qi_232", "Quality Inspector"),
                ("bs_232", "Building Safety Liaison"),
                ("pso_232", "Programme Support Officer"),
            ):
                raw["staff"].append(
                    {
                        "code": code,
                        "name": f"Synthetic {code}",
                        "email": f"{code}@example.test",
                        "role": role,
                    }
                )
            open_case = next(c for c in raw["cases"] if not c["closed"])
            first_id = str(open_case["id"])
            open_case["reason"] = "Safeguarding visit escort required"
            open_case["resident"]["adjustment"] = "Step-free doorway"
            data_path = Path(tmp) / "synthetic_232.json"
            data_path.write_text(json.dumps(raw), encoding="utf-8")

            store: Any = Store(str(data_path))
            users = {person["role"]: person for person in raw["staff"]}

            for allowed_role in Store.RESIDENT_CHOICE_QUEUE_ROLES:
                queue = store.resident_choice_queue(users[allowed_role], limit=10, offset=0)
                self.assertGreater(queue["total"], 0, allowed_role)
                for item in queue["items"]:
                    self.assertEqual(
                        set(item),
                        {"id", "address", "town", "measure_decisions", "resident_update"},
                    )

            for refused_role in ("Quality Inspector", "Building Safety Liaison"):
                with self.assertRaises(PermissionError):
                    store.resident_choice_queue(users[refused_role])
            for non_staff in ("Contractor", "Application Administrator"):
                with self.assertRaises(PermissionError):
                    store.resident_choice_queue({"role": non_staff, "code": "ext"})

            for reason_role in projection.DEFAULT_REASON_ROLES:
                projected = store.detail(first_id, users[reason_role])
                self.assertEqual(
                    projected["reason"],
                    "Safeguarding visit escort required",
                    reason_role,
                )
                self.assertEqual(
                    projected["resident"]["adjustment"],
                    "Step-free doorway",
                    reason_role,
                )

            for redacted_role in (
                "Retrofit Coordinator",
                "Quality Inspector",
                "Programme Support Officer",
            ):
                projected = store.detail(first_id, users[redacted_role])
                self.assertEqual(projected["reason"], projection.NOTE_HELD, redacted_role)
                self.assertEqual(
                    projected["resident"]["adjustment"],
                    projection.REDACTED,
                    redacted_role,
                )

            self.assertTrue(taskqueues.is_safeguarding("Safeguarding referral"))


if __name__ == "__main__":
    unittest.main()
