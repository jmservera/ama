"""WCAG 2.2 conformance for Housing Officer and Resident Engagement screens (#232, #151).

Verifies #/role/housing_officer and #/role/resident_engagement route wiring, keyboard jump
navigation (role="navigation", aria-label, "Go to ..." links, 1-to-1 section landmarks, and
tabindex="-1" heading focus targets), and explicit plain-language textual state cues across all
badges, choice/readiness indicators, pause/withdrawal states, update commitments, redress/history
rows, and safe-route indicators without sys.modules mutations.
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

NODE_HARNESS = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const webDir = process.argv[1];
const payload = JSON.parse(process.argv[2]);
const appSource = fs.readFileSync(webDir + "/app.js", "utf8");
const roleSource = fs.readFileSync(webDir + "/role-screens.js", "utf8");

const h = (tag, attrs, ...kids) => ({
  tag,
  attrs: attrs || {},
  kids: kids.flat(Infinity).filter((kid) => kid !== false && kid !== null && kid !== undefined),
});

function checkRouter() {
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
  const elements = new Map();
  const getEl = (id) => {
    if (!elements.has(id)) {
      elements.set(id, {
        id,
        addEventListener() {},
        replaceChildren() {},
        focus() {},
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
        set src(_value) {
          if (this.onload) this.onload();
        },
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
  const missingBeforeLoad = {
    housingStaff: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/housing_officer?case=C-1", false)', context)
    ),
    engagementStaff: Array.from(
      vm.runInContext(
        'missingWorkspaceScripts("#/role/resident_engagement?case=C-1", false)',
        context
      )
    ),
  };
  vm.runInContext('me.user.role = "Contractor";', context);
  const missingContractor = {
    housingContractor: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/housing_officer", false)', context)
    ),
    engagementContractor: Array.from(
      vm.runInContext('missingWorkspaceScripts("#/role/resident_engagement", false)', context)
    ),
  };
  vm.runInContext(
    `
    me.user.role = "Resident Liaison Officer";
    roleScreensView = async function () { routed.push(location.hash); };
    `,
    Object.assign(context, { routed })
  );
  return (async () => {
    const navStates = {};
    for (const hash of [
      "#/role/housing_officer",
      "#/role/housing_officer?case=C-1",
      "#/role/resident_engagement",
      "#/role/resident_engagement?case=C-1",
    ]) {
      context.location.hash = hash;
      await vm.runInContext("route()", context);
      navStates[hash] = {
        screensCurrent: navLinks[1].attrs["aria-current"] || null,
        homeCurrent: navLinks[0].attrs["aria-current"] || null,
        status: vm.runInContext("workspaceStatus.textContent", context),
      };
    }
    return { missingBeforeLoad, missingContractor, routed, navStates };
  })();
}

async function runHost(hash, caseRecord, queueItems, choiceQueue) {
  const shown = [];
  let clickListener = null;
  const focusEvents = [];
  const targets = new Map();
  const context = vm.createContext({
    URLSearchParams,
    Intl,
    AbortController,
    Date,
    location: { hash },
    routeController: new AbortController(),
    me: { user: { role: "Resident Liaison Officer" } },
    workspaceStatus: { textContent: "" },
    document: {
      addEventListener(type, fn) {
        if (type === "click") clickListener = fn;
      },
      getElementById(id) {
        return targets.get(id) || null;
      },
    },
    api: async (url) => {
      if (url.startsWith("/api/cases?")) {
        return { items: queueItems, total: queueItems.length };
      }
      if (url.startsWith("/api/resident/choice-queue?")) {
        return choiceQueue;
      }
      if (url.startsWith("/api/cases/")) {
        const requested = decodeURIComponent(url.slice("/api/cases/".length));
        if (caseRecord && requested === caseRecord.id) return caseRecord;
        if (requested === "C-FAIL") throw new Error("unavailable");
        return caseRecord || { id: requested };
      }
      return {};
    },
    h,
    show: (...nodes) => {
      shown.length = 0;
      shown.push(...nodes);
    },
  });
  vm.runInContext(roleSource + "\n;globalThis.__screens = roleScreens;", context);
  await vm.runInContext("roleScreensView()", context);

  const registerHeadings = (node) => {
    if (!node || typeof node !== "object") return;
    if (node.attrs && node.attrs.id) {
      targets.set(node.attrs.id, {
        id: node.attrs.id,
        tag: node.tag,
        tabindex: node.attrs.tabindex,
        focus() { focusEvents.push({ action: "focus", id: node.attrs.id }); },
        scrollIntoView(opts) {
          focusEvents.push({ action: "scroll", id: node.attrs.id, block: opts && opts.block });
        },
      });
    }
    for (const kid of node.kids || []) registerHeadings(kid);
  };
  shown.forEach(registerHeadings);

  const jumpTests = [];
  const collectJumpLinks = (node) => {
    if (!node || typeof node !== "object") return;
    if (node.tag === "a" && node.attrs && node.attrs["data-jump"]) {
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
      jumpTests.push({ target: node.attrs["data-jump"], prevented });
    }
    for (const kid of node.kids || []) collectJumpLinks(kid);
  };
  if (clickListener) {
    shown.forEach(collectJumpLinks);
    let missingPrevented = false;
    clickListener({
      target: {
        closest: (sel) =>
          sel === "a[data-jump]"
            ? { getAttribute: () => "non-existent-heading" }
            : null,
      },
      preventDefault() { missingPrevented = true; },
    });
    jumpTests.push({ target: "non-existent-heading", prevented: missingPrevented });
  }

  return {
    shown,
    workspaceStatus: context.workspaceStatus.textContent,
    focusEvents,
    jumpTests,
    choiceEmpty: context.__screens.get("resident-choice").render({ id: "C-EMPTY" }),
    serviceNoRedress: context.__screens
      .get("resident-service-issues")
      .render({ id: "C-NOREDRESS", service_requests: [] }),
    serviceWithRedressAndHistory: context.__screens
      .get("resident-service-issues")
      .render(payload.serviceFull),
    protoCase: {
      choice: context.__screens.get("resident-choice").render(payload.protoCase),
      service: context.__screens.get("resident-service-issues").render(payload.protoCase),
    },
  };
}

(async () => {
  const router = await checkRouter();
  const housingUnselected = await runHost(
    "#/role/housing_officer",
    payload.serviceFull,
    payload.queueItems,
    payload.choiceQueue
  );
  const housingSelected = await runHost(
    "#/role/housing_officer?case=C-1",
    payload.serviceFull,
    payload.queueItems,
    payload.choiceQueue
  );
  const engagementUnselected = await runHost(
    "#/role/resident_engagement",
    payload.choiceFull,
    payload.queueItems,
    payload.choiceQueue
  );
  const engagementSelected = await runHost(
    "#/role/resident_engagement?case=C-1",
    payload.choiceFull,
    payload.queueItems,
    payload.choiceQueue
  );
  console.log(
    JSON.stringify({
      router,
      housingUnselected,
      housingSelected,
      engagementUnselected,
      engagementSelected,
    })
  );
})().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
"""

CHOICE_FULL: dict[str, Any] = {
    "id": "C-1",
    "address": "14 Oak Lane",
    "town": "Northwich",
    "resident_update": {
        "status": "Proposed",
        "purpose": "Confirm loft survey window",
        "owner_identity": {"name": "Sam Example"},
        "due_at": "2026-12-01T10:00:00+00:00",
        "basis": "Resident callback request",
        "safe_contact_ref": "SC-77",
        "version": 2,
    },
    "measure_decisions": [
        {
            "measure": "Loft insulation",
            "status": "Paused",
            "readiness": "Needs human review",
            "context": {"scope": "S-9", "revision": 2, "design_version": 3},
            "review": {"status": "Needs human review", "decision_version": 2},
            "versions": [
                {
                    "version": 2,
                    "status": "Paused",
                    "answered_by": "The resident",
                    "at": "2026-11-10T09:00:00+00:00",
                    "scope": "S-9",
                    "context_revision": 2,
                    "design_version": 3,
                    "note": "Wait until spring",
                }
            ],
        },
        {
            "measure": "Heat pump",
            "status": "Accepted",
            "readiness": "Resident decision current",
            "context": {"scope": "S-9", "revision": 2, "design_version": 3},
            "versions": [],
        },
        {
            "measure": "Solar PV",
            "status": "Not recorded",
            "readiness": "",
            "versions": [],
        },
    ],
    "service_requests": [
        {
            "id": "SR-1",
            "route": "Accessibility support",
            "status": "Open",
            "accessibility": ["Large print", "Telephone before visit"],
            "next_update": "2026-12-03",
        }
    ],
}

SERVICE_FULL: dict[str, Any] = {
    "id": "C-1",
    "address": "14 Oak Lane",
    "town": "Northwich",
    "resident_update": {
        "status": "Outstanding",
        "purpose": "Follow up damp inspection",
        "owner_identity": {"name": "Sam Example"},
        "due_at": "2026-12-02T11:00:00+00:00",
        "safe_contact_ref": "",
    },
    "service_requests": [
        {
            "id": "SR-10",
            "route": "Complaint",
            "summary": "Ventilation fan noisy",
            "desired_outcome": "Quiet replacement unit",
            "status": "Resolved",
            "service_owner": "Alex Service",
            "redress_owner": "Pat Redress",
            "accessibility": ["BSL interpreter"],
            "representative_ref": "REP-9",
            "next_update": "2026-12-04T09:00:00+00:00",
            "history": [
                {
                    "status": "In progress",
                    "by": "Alex Service",
                    "at": "2026-11-12T14:00:00+00:00",
                    "note": "Engineer booked",
                }
            ],
        }
    ],
    "redress_route": {
        "commitments": ["No detriment to repairs or programme place."],
        "routes": [{"route": "Formal complaint", "who": "Resident", "how": "Named redress owner"}],
        "reviewable_decisions": [{"measure": "Loft insulation", "version": 2, "status": "Paused"}],
        "formal_requests": [
            {
                "id": "SR-10",
                "route": "Complaint",
                "status": "Open",
                "formal_route_status": "Unconfigured",
                "next_update": "2026-12-04T09:00:00+00:00",
                "review_measure": "Loft insulation",
                "review_decision_version": 2,
            },
            {
                "id": "SR-11",
                "route": "Independent review",
                "status": "Closed",
                "formal_route_status": "Acknowledged",
                "next_update": "2026-12-05T09:00:00+00:00",
                "review_measure": "Heat pump",
                "review_decision_version": 1,
            },
        ],
        "send_note": "Nothing reaches the formal route unless marked Acknowledged.",
    },
}

PROTO_CASE: dict[str, Any] = {
    "id": "C-PROTO",
    "resident_update": {"status": "constructor", "purpose": "Check", "safe_contact_ref": ""},
    "measure_decisions": [
        {"measure": "Wall insulation", "status": "toString", "readiness": "constructor"}
    ],
    "service_requests": [
        {
            "id": "SR-P",
            "route": "Repair",
            "status": "constructor",
            "history": [{"status": "toString", "by": "Staff", "note": "Check"}],
        }
    ],
    "redress_route": {
        "commitments": [],
        "routes": [],
        "reviewable_decisions": [{"measure": "Wall", "version": 1, "status": "constructor"}],
        "formal_requests": [
            {
                "id": "SR-P",
                "route": "Complaint",
                "status": "toString",
                "formal_route_status": "constructor",
            }
        ],
        "send_note": "Note.",
    },
}

QUEUE_ITEMS: list[dict[str, Any]] = [
    {"id": "C-1", "address": "14 Oak Lane", "status": "Active", "hazard": True},
    {"id": "C-FAIL", "address": "99 Missing Way", "status": "Active", "hazard": False},
]

CHOICE_QUEUE: dict[str, Any] = {
    "items": [
        CHOICE_FULL,
        {"id": "C-2", "address": "22 Elm Road", "town": "Winsford"},
    ],
    "total": 2,
    "limit": 100,
    "offset": 0,
}


def walk(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict) and "tag" in node:
        found.append(node)
        for kid in node.get("kids", []):
            found.extend(walk(kid))
    elif isinstance(node, list):
        for item in node:
            found.extend(walk(item))
    return found


def text_of(node: Any) -> str:
    if isinstance(node, str):
        return node
    if isinstance(node, (int, float)):
        return str(node)
    if isinstance(node, dict):
        return " ".join(part for part in (text_of(kid) for kid in node.get("kids", [])) if part)
    if isinstance(node, list):
        return " ".join(part for part in (text_of(item) for item in node) if part)
    return ""


class HousingResidentScreenWcagTests(unittest.TestCase):
    data: dict[str, Any] = {}

    @classmethod
    def setUpClass(cls) -> None:
        payload = {
            "choiceFull": CHOICE_FULL,
            "serviceFull": SERVICE_FULL,
            "protoCase": PROTO_CASE,
            "queueItems": QUEUE_ITEMS,
            "choiceQueue": CHOICE_QUEUE,
        }
        result = subprocess.run(
            ["node", "-e", NODE_HARNESS, str(WEB), json.dumps(payload)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(f"Node harness failed:\n{result.stderr}")
        cls.data = json.loads(result.stdout)

    def _assert_record_jump_bijection(self, tree: dict[str, Any]) -> None:
        nodes = walk(tree)
        navs = [n for n in nodes if n["tag"] == "nav"]
        self.assertEqual(len(navs), 1)
        nav = navs[0]
        self.assertEqual(nav["attrs"].get("role"), "navigation")
        self.assertEqual(nav["attrs"].get("aria-label"), "Sections of this view")
        self.assertEqual([n for n in walk(nav) if n["tag"] == "button"], [])

        links = [n for n in walk(nav) if n["tag"] == "a"]
        self.assertGreaterEqual(len(links), 4)
        sections = [n for n in nodes if n["tag"] == "section"]
        self.assertEqual(len(links), len(sections))

        headings_by_id = {
            n["attrs"]["id"]: n for n in nodes if n["tag"] == "h2" and "id" in n["attrs"]
        }
        jump_targets: list[str] = []
        for link in links:
            label = text_of(link)
            self.assertTrue(label.startswith("Go to "), label)
            target_id = link["attrs"]["data-jump"]
            self.assertEqual(link["attrs"]["href"], f"#{target_id}")
            self.assertIn(target_id, headings_by_id)
            self.assertEqual(headings_by_id[target_id]["attrs"].get("tabindex"), -1)
            jump_targets.append(target_id)

        section_heading_ids: list[str] = []
        for section in sections:
            sec_id = section["attrs"].get("id")
            self.assertTrue(sec_id, f"Section missing id: {section}")
            expected_heading_id = f"{sec_id}-heading"
            self.assertEqual(section["attrs"].get("aria-labelledby"), expected_heading_id)
            self.assertIn(expected_heading_id, headings_by_id)
            section_heading_ids.append(expected_heading_id)

        self.assertEqual(jump_targets, section_heading_ids)

    def test_role_routes_load_role_screens_and_select_expected_views(self) -> None:
        router = self.data["router"]
        self.assertEqual(
            router["missingBeforeLoad"]["housingStaff"],
            ["/role-screens.js"],
        )
        self.assertEqual(
            router["missingBeforeLoad"]["engagementStaff"],
            ["/role-screens.js"],
        )
        self.assertNotIn("/ops.js", router["missingContractor"]["housingContractor"])
        self.assertNotIn("/ops.js", router["missingContractor"]["engagementContractor"])
        self.assertEqual(
            router["routed"],
            [
                "#/role/housing_officer",
                "#/role/housing_officer?case=C-1",
                "#/role/resident_engagement",
                "#/role/resident_engagement?case=C-1",
            ],
        )
        for state in router["navStates"].values():
            self.assertEqual(state["screensCurrent"], "page")
            self.assertIsNone(state["homeCurrent"])
            self.assertIn("Role screens", state["status"])

        self.assertIn(
            "Resident service issue queue",
            self.data["housingUnselected"]["workspaceStatus"],
        )
        self.assertIn(
            "Resident service issue queue. Selected home C-1.",
            self.data["housingSelected"]["workspaceStatus"],
        )
        self.assertIn(
            "Resident choice and update queue",
            self.data["engagementUnselected"]["workspaceStatus"],
        )
        self.assertIn(
            "Resident choice and update queue. Selected home C-1.",
            self.data["engagementSelected"]["workspaceStatus"],
        )

    def test_record_views_expose_navigation_landmark_and_one_to_one_section_headings(self) -> None:
        sample = self.data["engagementSelected"]
        self._assert_record_jump_bijection(sample["choiceEmpty"])
        self._assert_record_jump_bijection(sample["serviceNoRedress"])
        self._assert_record_jump_bijection(sample["serviceWithRedressAndHistory"])

        # Also check the rendered record subtree inside full #/role/* selected-home views.
        for key in ("housingSelected", "engagementSelected"):
            shown_nodes = walk(self.data[key]["shown"])
            record_navs = [
                n
                for n in shown_nodes
                if n["tag"] == "nav" and n["attrs"].get("aria-label") == "Sections of this view"
            ]
            self.assertEqual(len(record_navs), 1, key)
            self.assertEqual(record_navs[0]["attrs"].get("role"), "navigation")

    def test_workspace_jump_nav_and_click_activation_focus_target_headings(self) -> None:
        for key in (
            "housingUnselected",
            "housingSelected",
            "engagementUnselected",
            "engagementSelected",
        ):
            bundle = self.data[key]
            nodes = walk(bundle["shown"])
            all_ids = [n["attrs"]["id"] for n in nodes if "id" in n.get("attrs", {})]
            self.assertEqual(len(all_ids), len(set(all_ids)), f"Duplicate DOM IDs in {key}")

            ws_nav = next(
                n
                for n in nodes
                if n["tag"] == "nav" and n["attrs"].get("aria-label") == "Workspace sections"
            )
            self.assertEqual(ws_nav["attrs"].get("role"), "navigation")
            ws_links = [n for n in walk(ws_nav) if n["tag"] == "a"]
            self.assertGreaterEqual(len(ws_links), 2)
            for link in ws_links:
                self.assertTrue(text_of(link).startswith("Go to "))

            # Every jump click prevents default hash navigation and focuses + scrolls real headings.
            self.assertTrue(all(item["prevented"] for item in bundle["jumpTests"]))
            real_targets = [
                item["target"]
                for item in bundle["jumpTests"]
                if item["target"] != "non-existent-heading"
            ]
            focused_ids = [ev["id"] for ev in bundle["focusEvents"] if ev["action"] == "focus"]
            scrolled = [
                (ev["id"], ev["block"]) for ev in bundle["focusEvents"] if ev["action"] == "scroll"
            ]
            self.assertEqual(focused_ids, real_targets, key)
            self.assertEqual(scrolled, [(tid, "start") for tid in real_targets], key)

        css = (WEB / "style.css").read_text(encoding="utf-8")
        self.assertRegex(css, r'\[tabindex="-1"\]:where\(:not\(#app\)\):focus\s*\{\s*outline:')
        self.assertIn("scroll-margin-top: var(--sp-4)", css)

    def test_textual_state_cues_cover_badges_choices_pauses_commitments_and_safe_routes(
        self,
    ) -> None:
        engagement_text = json.dumps(self.data["engagementSelected"]["shown"])
        housing_text = json.dumps(self.data["housingSelected"]["shown"])
        housing_unselected_text = json.dumps(self.data["housingUnselected"]["shown"])
        choice_empty_text = json.dumps(self.data["engagementSelected"]["choiceEmpty"])

        # Queue safety and selected-home scope badges pair visual pills with State: cues.
        for rendered in (engagement_text, housing_text):
            self.assertIn("Safety issue open", rendered)
            self.assertIn("State: Action needed - open safety issue.", rendered)
            self.assertIn("Same home: case C-1", rendered)
            self.assertIn("State: Confirmed - single-home record scope.", rendered)

        # Resident choice, version answer, readiness, pause/withdrawal, and safe-route cues.
        for expected in (
            "Confirmed: Paused",
            "Confirmed: v2 Paused (scope S-9, revision 2, design 3)",
            "Action needed: Needs human review",
            "Confirmed: Accepted",
            "Confirmed: Resident decision current",
            "Waiting for resident: Not recorded",
            "Waiting for resident: Unknown",
            "Action needed: Human review before any restart",
            "Action needed: Proposed",
            "Confirmed: SC-77 (safe route reference only; contact details not shown here)",
            "Waiting for resident: No measure choices recorded",
            "Action needed: No commitment recorded",
        ):
            self.assertIn(expected, engagement_text)
        self.assertIn(
            "State: None recorded. No measure is currently paused or withdrawn",
            choice_empty_text,
        )

        # Service issues, redress formal-route cues, history steps, and missing safe route.
        for expected in (
            "Action needed: Resolved. The owner says it is dealt with.",
            "Confirmed: BSL interpreter",
            "Confirmed: Paused",
            "Action needed: Unconfigured",
            "Confirmed: Acknowledged",
            "Action needed: In progress. The named owner is dealing with it.",
            "Action needed: Outstanding",
            "Action needed: Unknown (safe route not recorded)",
        ):
            self.assertIn(expected, housing_text)

        # Housing officer unselected portfolio summary cues for unavailable and open rows.
        for expected in (
            "Action needed: SR-10 Complaint: Resolved",
            "Action needed: Unavailable. Open the home to check.",
            "Waiting for resident: Unavailable",
            "Action needed: Unavailable",
        ):
            self.assertIn(expected, housing_unselected_text)

        # Object.prototype keys never masquerade as Confirmed/Verified states.
        proto_choice = json.dumps(self.data["engagementSelected"]["protoCase"]["choice"])
        proto_service = json.dumps(self.data["engagementSelected"]["protoCase"]["service"])
        self.assertIn("Action needed: toString", proto_choice)
        self.assertIn("Action needed: constructor", proto_choice)
        self.assertIn("Action needed: constructor", proto_service)
        self.assertIn("Action needed: toString. Meaning not recorded.", proto_service)

    def test_module_contains_no_sys_modules_mutation_hazards(self) -> None:
        source = Path(__file__).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=__file__)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Delete, ast.Assign, ast.AugAssign, ast.AnnAssign)):
                segment = ast.get_source_segment(source, node) or ""
                self.assertIsNone(
                    re.search(r"\bsys\.modules\b", segment),
                    f"Forbidden sys.modules mutation: {segment}",
                )
            if isinstance(node, ast.Call):
                segment = ast.get_source_segment(source, node) or ""
                self.assertIsNone(
                    re.search(r"\bsys\.modules\.(pop|clear|delitem| update|setdefault)\b", segment),
                    f"Forbidden sys.modules call: {segment}",
                )


if __name__ == "__main__":
    unittest.main()
