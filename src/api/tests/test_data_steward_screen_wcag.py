"""Steward and operator state indicators are written and keyboard reachable (#229, WCAG 2.2)."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const data = JSON.parse(process.argv[2]);
const h = (tag, attrs, ...kids) => ({tag, attrs: attrs || {}, addEventListener() {},
  kids: kids.flat(Infinity).filter(kid => kid !== false && kid !== null && kid !== undefined)});
const controller = new AbortController();
const context = vm.createContext({URLSearchParams, Intl, AbortController, Date,
  location: {hash: "#/screens?screen=data-operator&exceptions=1"}, routeController: controller,
  me: {user: {role: "Retrofit Programme Manager"}}, api: async () => data, h});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
context.__s.overview(controller.signal, [], null).then(out => console.log(JSON.stringify(out)));
"""

CLICK_SCRIPT = (
    SCRIPT.replace(
        "location:", "document: {getElementById: (id) => targets[id] || null}, location:"
    )
    .replace("const controller", "const calls = []; const targets = {};\nconst controller")
    .replace(
        "context.__s.overview(controller.signal, [], null)"
        ".then(out => console.log(JSON.stringify(out)));",
        """const find = (n, f, o = []) => {
  if (n && typeof n === "object") {
    if (f(n)) o.push(n);
    (n.kids || []).forEach(k => find(k, f, o));
  }
  return o;
};
context.__s.overview(controller.signal, [], null).then(out => {
  const hs = find(out, n => n.tag === "h3" && n.attrs.id);
  hs.forEach(n => { targets[n.attrs.id] = {focus: () => calls.push(["focus", n.attrs.id]),
    scrollIntoView: (o) => calls.push(["scroll", n.attrs.id, o.block])}; });
  const bs = find(out, n => n.tag === "button" && n.attrs["data-jump-target"]);
  bs.forEach(b => b.attrs.onclick());
  const missing = bs[0].attrs.onclick; delete targets["exception-state"]; missing();
  console.log(JSON.stringify(calls));
});""",
    )
)

BASE: dict[str, Any] = {
    "state": "ok",
    "items": [
        {
            "id": "EX-001",
            "kind": "failed_import",
            "status": "open",
            "owner": "Sam",
            "owner_role": "data_steward",
            "summary": "Batch refused.",
            "original_source": {"status": "Quarantined", "batch_id": "B-1"},
        }
    ],
    "unrouted": [],
    "sources": [],
    "banner": {"state": "unknown", "text": "Unknown."},
    "access": {"roles": {}, "scope": {}},
    "note": "Synthetic.",
}

INDICATORS: dict[str, Any] = {
    "lineage": {"state": "stale", "as_of": "2026-11-01"},
    "sensor_feed": {"state": "degraded"},
    "ai_tasks": [{"task": "summary", "enabled": False}, {"task": "triage", "enabled": True}],
}


def render(contract: dict[str, Any]) -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(contract)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    tree: dict[str, Any] = json.loads(result.stdout)
    return tree


def walk(node: Any) -> list[dict[str, Any]]:
    if not isinstance(node, dict):
        return []
    found = [node]
    for kid in node.get("kids", []):
        found += walk(kid)
    return found


def text(node: Any) -> str:
    if isinstance(node, str):
        return node
    return " ".join(text(kid) for kid in node.get("kids", []))


def glance(tree: dict[str, Any]) -> str:
    nodes = walk(tree)
    index = next(i for i, n in enumerate(nodes) if text(n) == "State at a glance")
    return " ".join(text(n) for n in nodes[index + 1 :] if n.get("tag") == "dl")[:2000]


class DataStewardScreenWcag(unittest.TestCase):
    def test_supplied_states_are_written_out(self) -> None:
        page = glance(render({**BASE, "indicators": INDICATORS}))
        for phrase in (
            "State: Stale",
            "State: Quarantined (1 item listed below)",
            "State: Degraded",
            "AI task: summary State: Disabled",
            "AI task: triage State: Enabled",
        ):
            self.assertIn(phrase, page)

    def test_missing_states_read_unknown_not_healthy(self) -> None:
        page = glance(render(BASE))
        self.assertIn("Lineage freshness State: Unknown", page)
        self.assertIn("Sensor feed health State: Unknown", page)
        self.assertIn("State: Unknown. No task settings were returned", page)
        self.assertNotIn("Fresh", page)
        self.assertNotIn("Healthy", page)
        self.assertNotIn("Enabled", page)

    def test_unrecognised_state_value_is_unknown(self) -> None:
        bad = {"lineage": {"state": "green"}, "sensor_feed": {"state": 3}}
        page = glance(render({**BASE, "indicators": bad}))
        self.assertIn("Lineage freshness State: Unknown", page)
        self.assertIn("Sensor feed health State: Unknown", page)

    def test_inherited_object_keys_are_unknown(self) -> None:
        bad = {"lineage": {"state": "constructor"}, "sensor_feed": {"state": "toString"}}
        page = glance(render({**BASE, "indicators": bad}))
        self.assertIn("Lineage freshness State: Unknown", page)
        self.assertIn("Sensor feed health State: Unknown", page)

    def test_section_jump_buttons_target_focusable_headings(self) -> None:
        nodes = walk(render(BASE))
        navs = [n for n in nodes if n.get("tag") == "nav"]
        self.assertEqual(len(navs), 1)
        self.assertEqual(navs[0]["attrs"]["aria-label"], "Data stewardship sections")
        buttons = [n for n in walk(navs[0]) if n.get("tag") == "button"]
        self.assertEqual(len(buttons), 4)
        headings = {
            n["attrs"].get("id"): n["attrs"].get("tabindex") for n in nodes if n.get("tag") == "h3"
        }
        for button in buttons:
            self.assertEqual(button["attrs"]["type"], "button")
            self.assertEqual(headings.get(button["attrs"]["data-jump-target"]), "-1")

    def test_jump_handlers_focus_then_scroll_to_start(self) -> None:
        result = subprocess.run(
            ["node", "-e", CLICK_SCRIPT, str(WEB), json.dumps(BASE)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = json.loads(result.stdout)
        ids = ["exception-state", "exception-sources", "exception-items", "exception-conflicts"]
        expected = [step for i in ids for step in (["focus", i], ["scroll", i, "start"])]
        self.assertEqual(calls, expected)

    def test_empty_or_blocked_register_is_never_pass(self) -> None:
        for contract, label in (
            ({**BASE, "items": []}, "Needs review"),
            ({**BASE, "items": [], "state": "roles_not_named"}, "Action needed"),
            ({**BASE, "unrouted": ["R-1"]}, "Action needed"),
            ({**BASE, "items": [{}]}, "Action needed"),
        ):
            page = glance(render(contract))
            self.assertNotIn("State: Pass", page)
            self.assertIn(f"Suppressed records State: {label}", page)
        self.assertIn("Open exceptions State: Attention", glance(render(BASE)))

    def test_no_quarantine_is_not_an_all_clear(self) -> None:
        page = glance(render({**BASE, "items": []}))
        self.assertIn("None returned, which is not an all clear", page)

    def test_indicators_are_read_only_and_add_no_status_or_invalid_markup(self) -> None:
        tree = render({**BASE, "indicators": INDICATORS})
        nodes = walk(tree)
        self.assertFalse([n for n in nodes if n.get("tag") in ("input", "select")])
        self.assertFalse([n for n in nodes if "aria-invalid" in n["attrs"]])
        statuses = [n for n in nodes if n["attrs"].get("role") == "status"]
        plain = [n for n in walk(render(BASE)) if n["attrs"].get("role") == "status"]
        self.assertEqual(len(statuses), len(plain))

    def test_tables_stay_keyboard_reachable_and_named(self) -> None:
        tree = render({**BASE, "indicators": INDICATORS})
        regions = [n for n in walk(tree) if n["attrs"].get("role") == "region"]
        self.assertTrue(regions)
        for region in regions:
            self.assertEqual(region["attrs"].get("tabindex"), 0)
            self.assertTrue(region["attrs"].get("aria-label"))
        self.assertTrue(all(n["kids"] for n in walk(tree) if n.get("tag") == "caption"))


OPERATOR_WCAG_SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");

let clickHandler = null;
let caseMap = {};
let registerPayload = null;
let registerMode = "ok";
const focusCalls = [];
const targets = {};
const locationState = {hash: "#/screens?screen=data-operator&case=C-1"};
const h = (tag, attrs, ...kids) => ({
  tag,
  attrs: attrs || {},
  addEventListener() {},
  kids: kids.flat(Infinity).filter(k => k !== false && k !== null && k !== undefined)
});
const documentStub = {
  addEventListener(type, fn) { if (type === "click") clickHandler = fn; },
  getElementById(id) { return Object.hasOwn(targets, id) ? targets[id] : null; }
};
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  document: documentStub,
  location: locationState,
  routeController: new AbortController(),
  me: {user: {role: "Retrofit Programme Manager"}},
  screenHref: (screenId, caseId) =>
    `#/screens?screen=${screenId}${caseId ? `&case=${caseId}` : ""}`,
  screenScopeQuery: () => new URLSearchParams((locationState.hash.split("?")[1]) || ""),
  api: async (path) => {
    if (path === "/api/exceptions") {
      if (registerMode === "fail") {
        const err = new Error("synthetic outage");
        err.status = 503;
        throw err;
      }
      return registerPayload;
    }
    return caseMap[path] || {id: "C-1"};
  },
  h
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
const s = context.__s;

const find = (node, pred, out = []) => {
  if (node && typeof node === "object") {
    if (pred(node)) out.push(node);
    (node.kids || []).forEach(kid => find(kid, pred, out));
  }
  return out;
};
const registerSections = (tree) => {
  Object.keys(targets).forEach(k => delete targets[k]);
  find(tree, n => n.tag === "section" && n.attrs.id).forEach(sec => {
    targets[sec.attrs.id] = {focus: () => focusCalls.push(sec.attrs.id)};
  });
};
const clickLink = (link) => {
  let prevented = false;
  const isJump = Object.hasOwn(link.attrs, "data-jump");
  clickHandler({
    target: {
      closest: (sel) => (sel === "a[data-jump]" && isJump ? {
        getAttribute: (name) => link.attrs[name]
      } : null)
    },
    preventDefault: () => { prevented = true; }
  });
  return prevented;
};

const side = (value, sourceId, version, validationState) => ({
  value, source_id: sourceId, version, date: "2026-10-01", validation_state: validationState
});
const homeCase = {
  id: "C-1",
  stock_reconciliation: [
    {id: "SQ-1", field: "epc", query_owner: {name: "Steward One"},
      left: side("D", "S-A", "1", "Unvalidated"), right: side("C", "S-B", "2", "Validated")},
    {id: "SQ-2", field: "wall_type", query_owner: {name: "Steward Two"},
      left: side("Solid", "S-A", "1", "Unverified"), right: side("Cavity", "S-B", "2", "Disputed")},
    {id: "SQ-3", field: "loft", query_owner: {name: "Steward Three"},
      left: side("100mm", "S-A", "1", "Quarantined"), right: side("270mm", "S-B", "2", "Stale")}
  ],
  stock_reconciliation_events: [
    {id: "SQE-1", query_id: "SQ-2", status: "Withdrawn", at: "2026-10-05T10:00:00Z",
      recorded_by: {name: "Steward Two"}, reason: "Superseded batch", evidence: "EV-1"},
    {id: "SQE-2", query_id: "SQ-3", status: "Reconciled", at: "2026-10-06T11:00:00Z",
      recorded_by: {name: "Steward Three"}, reason: "Survey verified", evidence: "EV-2"}
  ],
  returns: [
    {at: "2026-10-02T09:00:00Z", reopened: false, from_stage: "Install", to_stage: "Survey",
      reason: "Missing roof photo", source: "SRC-1", source_version: "2",
      next_action: "Re-book survey", receiving_owner: {name: "Coordinator A"}},
    {at: "2026-10-03T09:00:00Z", reopened: true, from_stage: "Handover", to_stage: "Quality",
      reason: "Ventilation check", source: "SRC-2", source_version: "3",
      next_action: "Inspect fan", receiving_owner: {name: "Coordinator B"}}
  ],
  work: {
    owner: "Operator A",
    reason: "Awaiting handoff confirmation",
    next_action: "Chase repairs team",
    as_of: "2026-10-27",
    handoff: {
      destination: "Repairs",
      proposed_receiver: "Repairs Lead",
      confirmed_receiver: "Unknown",
      chase_owner: "Operator A",
      state: "Offered"
    },
    blockers: [
      {step: "Survey", current_stop: true, reason: "Missing reference", owner: "Owner A",
        next_action: "Supply ref", source: "SYN", version: 1},
      {step: "Design", current_stop: false, reason: "Pending calc", owner: "Owner B",
        next_action: "Attach calc", source: "SYN", version: 2},
      {step: "Scaffold", status: "open", current_stop: true, reason: "Permit needed",
        owner: "Owner D", next_action: "Obtain permit", source: "SYN", version: 4},
      {step: "Meter", status: "blocked", current_stop: true, reason: "DNO fuse",
        owner: "Owner E", next_action: "Book DNO", source: "SYN", version: 5},
      {step: "EPC", status: "resolved", current_stop: false, reason: "Lodged",
        owner: "Owner F", next_action: "None", source: "SYN", version: 6},
      {step: "Grant", reason: "Legacy fixture", owner: "Owner C",
        next_action: "Check grant", source: "SYN", version: 3}
    ]
  }
};

const handoffVariants = ["Received", "Escalated", "Declined", "Completed"].map((state, idx) =>
  s.render({
    ...homeCase,
    id: `C-H${idx}`,
    work: {...homeCase.work, handoff: {...homeCase.work.handoff, state}}
  })
);

const registerStatesPayload = {
  state: "ok",
  items: [
    {id: "EX-001", kind: "source_conflict", status: "held", eligibility: "suppressed",
      owner: "Sam", owner_role: "data_steward", summary: "Conflict", runbook: "Check both",
      values: [{value: "D", source: "S-A", version: "1", date: "2026-10-01"},
        {value: "C", source: "S-B", version: "2", date: "2026-10-01"}]},
    {id: "EX-002", kind: "failed_import", status: "rerun_requested", eligibility: "not_assessed",
      owner: "Pat", owner_role: "digital_operator", summary: "Import stopped",
      runbook: "Inspect batch"},
    {id: "EX-003", kind: "stranded_task", status: "closed", eligibility: "unknown",
      owner: "Alex", owner_role: "data_steward", summary: "Closed item", runbook: "None"}
  ],
  unrouted: [],
  sources: [],
  banner: {state: "unknown", text: "Unknown."},
  access: {roles: {}, scope: {}},
  note: "Synthetic."
};

const poisonValues = [
  "green", "red", "Pass", "Healthy", "Clear", "false",
  "constructor", "toString", "__proto__", 7, null
];
const poisonedHome = poisonValues.map((bad, idx) => s.render({
  id: `C-BAD-${idx}`,
  stock_reconciliation: [{
    id: "SQ-B", field: "epc", query_owner: "Owner",
    left: side("D", "S-A", "1", bad), right: null
  }],
  stock_reconciliation_events: [{
    id: "SQE-B", query_id: "SQ-B", status: bad, at: "2026-10-01T00:00:00Z",
    recorded_by: "Recorder", reason: "Recorded", evidence: "EV-B"
  }],
  returns: [
    {at: "2026-10-02T09:00:00Z", reopened: bad, from_stage: "Install", to_stage: "Survey",
      reason: "Malformed flag", source: "SRC-1", source_version: "1",
      next_action: "Check", receiving_owner: "Owner"},
    {at: "2026-10-03T09:00:00Z", reason: "Missing stages and flag",
      source: "SRC-2", source_version: "1", next_action: "Check", receiving_owner: "Owner"},
    {at: "2026-10-04T09:00:00Z", reopened: true, event_type: "return",
      from_stage: "Install", to_stage: "Survey", reason: "Contradictory kind",
      source: "SRC-3", source_version: "1", next_action: "Check", receiving_owner: "Owner"}
  ],
  work: {
    owner: "Owner", reason: "Reason", next_action: "Next", as_of: "2026-10-27",
    handoff: {destination: "Repairs", proposed_receiver: "R", confirmed_receiver: "Unknown",
      chase_owner: "C", state: bad},
    blockers: [
      {step: "S1", status: bad, reason: "R1", owner: "O1",
        next_action: "N1", source: "SRC", version: 1},
      {step: "S2", current_stop: bad, reason: "R2", owner: "O2",
        next_action: "N2", source: "SRC", version: 1},
      {step: "S3", status: "open", current_stop: bad, reason: "R3", owner: "O3",
        next_action: "N3", source: "SRC", version: 1},
      {step: "S4", status: "resolved", current_stop: true, reason: "R4", owner: "O4",
        next_action: "N4", source: "SRC", version: 1}
    ]
  }
}));
const poisonedRegisters = [];

(async () => {
  caseMap = {"/api/cases/C-1": homeCase};
  registerPayload = registerStatesPayload;
  registerMode = "ok";

  const homeTree = s.render(homeCase);
  const emptyHomeTree = s.render({id: "C-EMPTY"});
  const summaryTree = s.summary([[{id: "C-1"}, homeCase], [{id: "C-9"}, null]]);

  registerSections(homeTree);
  const homeLinks = find(homeTree, n => n.tag === "a" && Object.hasOwn(n.attrs, "data-jump"));
  const homePrevented = homeLinks.map(clickLink);
  const hashAfterHome = locationState.hash;
  const homeFocusCalls = focusCalls.splice(0);

  locationState.hash = "#/screens?screen=data-operator";
  const overviewDefault = await s.overview(new AbortController().signal, [{id: "C-1"}], null);
  const overviewEntryOnly = await s.overview(new AbortController().signal, [], null);
  registerSections(overviewDefault);
  const isJumpLink = n => n.tag === "a" && Object.hasOwn(n.attrs, "data-jump");
  const overviewLinks = find(overviewDefault, isJumpLink);
  const overviewPrevented = overviewLinks.map(clickLink);
  const plainRegisterLink = find(overviewDefault, n => n.tag === "a" && !isJumpLink(n))[0];
  const plainLinkPrevented = clickLink(plainRegisterLink);
  const overviewFocusCalls = focusCalls.splice(0);

  locationState.hash = "#/screens?screen=data-operator&exceptions=1";
  const overviewExceptions = await s.overview(new AbortController().signal, [{id: "C-1"}], null);
  registerSections(overviewExceptions);
  const exLinks = find(overviewExceptions, isJumpLink);
  const exPrevented = exLinks.map(clickLink);
  const exFocusCalls = focusCalls.splice(0);

  registerMode = "fail";
  const overviewExceptionsUnavailable = await s.overview(
    new AbortController().signal, [{id: "C-1"}], null
  );

  registerMode = "ok";
  for (const bad of poisonValues) {
    const scope = {};
    if (typeof bad === "string") Object.defineProperty(scope, bad, {
      value: "digital_operator", enumerable: true, configurable: true
    });
    registerPayload = {
      ...registerStatesPayload,
      state: typeof bad === "string" ? bad : "unknown_state",
      banner: {state: typeof bad === "string" ? bad : "unknown_state", text: "Synthetic."},
      access: {roles: {}, scope},
      items: [
        {
          id: "EX-901", kind: "source_conflict", status: bad, eligibility: bad,
          owner: "Sam", owner_role: "data_steward", summary: "Item", runbook: "Guide",
          values: [{value: "D", source: "S-A", version: "1", date: "2026-10-01"},
            {value: "C", source: "S-B", version: "2", date: "2026-10-01"}]
        },
        {
          id: "EX-902", kind: typeof bad === "string" ? bad : "unknown_kind",
          status: bad, eligibility: bad, owner: "Pat", owner_role: "digital_operator",
          summary: "Second", runbook: "Guide"
        }
      ]
    };
    poisonedRegisters.push(await s.overview(new AbortController().signal, [], null));
  }

  console.log(JSON.stringify({
    homeTree,
    emptyHomeTree,
    summaryTree,
    handoffVariants,
    overviewDefault,
    overviewEntryOnly,
    overviewExceptions,
    overviewExceptionsUnavailable,
    poisonedHome,
    poisonedRegisters,
    clicks: {
      homePrevented,
      hashAfterHome,
      homeFocusCalls,
      overviewPrevented,
      plainLinkPrevented,
      overviewFocusCalls,
      exPrevented,
      exFocusCalls
    }
  }));
})();
"""


def run_operator_wcag() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", OPERATOR_WCAG_SCRIPT, str(WEB)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


class DataOperatorHomeAndOverviewWcag(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = run_operator_wcag()

    def test_home_view_jump_nav_links_target_focusable_sections(self) -> None:
        for key in ("homeTree", "emptyHomeTree"):
            tree = self.out[key]
            self.assertEqual(tree["kids"][0]["tag"], "nav")
            nav = tree["kids"][0]
            self.assertEqual(nav["attrs"].get("aria-label"), "Data steward and operator sections")
            links = [n for n in walk(nav) if n.get("tag") == "a"]
            expected_ids = [
                "operator-boundary",
                "operator-conflicts",
                "operator-eligibility",
                "operator-returns",
                "operator-handoff",
                "operator-events",
            ]
            self.assertEqual([link["attrs"].get("data-jump") for link in links], expected_ids)
            for link in links:
                target_id = link["attrs"]["data-jump"]
                self.assertEqual(link["attrs"].get("href"), f"#{target_id}")
                self.assertEqual(link["attrs"].get("class"), "btn alt")
                self.assertTrue(text(link).startswith("Go to "))
            sections = [n for n in walk(tree) if n.get("tag") == "section"]
            self.assertEqual([s["attrs"].get("id") for s in sections], expected_ids)
            for sec in sections:
                self.assertEqual(sec["attrs"].get("class"), "card screen-record")
                self.assertEqual(sec["attrs"].get("tabindex"), "-1")
                self.assertNotIn("aria-labelledby", sec["attrs"])
                self.assertNotIn("aria-label", sec["attrs"])
                self.assertEqual(sec["kids"][0]["tag"], "h2")
            neg_tabs = [n["tag"] for n in walk(tree) if str(n["attrs"].get("tabindex")) == "-1"]
            self.assertEqual(neg_tabs, ["section"] * 6)

    def test_delegated_jump_link_click_focuses_section_without_hash_change(self) -> None:
        clicks = self.out["clicks"]
        self.assertEqual(clicks["homePrevented"], [True] * 6)
        self.assertEqual(clicks["hashAfterHome"], "#/screens?screen=data-operator&case=C-1")
        self.assertEqual(
            clicks["homeFocusCalls"],
            [
                "operator-boundary",
                "operator-conflicts",
                "operator-eligibility",
                "operator-returns",
                "operator-handoff",
                "operator-events",
            ],
        )
        self.assertEqual(clicks["overviewPrevented"], [True, True])
        self.assertFalse(clicks["plainLinkPrevented"])
        self.assertEqual(
            clicks["overviewFocusCalls"], ["operator-register-entry", "operator-page-queue"]
        )
        self.assertEqual(clicks["exPrevented"], [True, True])
        self.assertEqual(clicks["exFocusCalls"], ["operator-register", "operator-page-queue"])

    def test_overview_jump_nav_targets_matching_register_and_page_queue_in_dom_order(
        self,
    ) -> None:
        default_tree = self.out["overviewDefault"]
        self.assertEqual(default_tree["kids"][0]["tag"], "nav")
        self.assertEqual(
            default_tree["kids"][0]["attrs"].get("aria-label"),
            "Data steward overview sections",
        )
        default_sections = [
            n["attrs"].get("id") for n in walk(default_tree) if n["tag"] == "section"
        ]
        self.assertEqual(default_sections, ["operator-register-entry", "operator-page-queue"])

        for key in ("overviewExceptions", "overviewExceptionsUnavailable"):
            ex_tree = self.out[key]
            self.assertEqual(ex_tree["kids"][0]["tag"], "nav")
            links = [
                n["attrs"].get("data-jump") for n in walk(ex_tree["kids"][0]) if n["tag"] == "a"
            ]
            self.assertEqual(links, ["operator-register", "operator-page-queue"])
            ex_sections = [n for n in walk(ex_tree) if n["tag"] == "section"]
            self.assertEqual(
                [s["attrs"].get("id") for s in ex_sections],
                ["operator-register", "operator-page-queue"],
            )
            self.assertTrue(all(s["attrs"].get("tabindex") == "-1" for s in ex_sections))

        entry_only = self.out["overviewEntryOnly"]
        self.assertEqual([n for n in walk(entry_only) if n["tag"] == "nav"], [])
        self.assertEqual(len([n for n in walk(entry_only) if n["tag"] == "a"]), 1)
        summary_tags = {n["tag"] for n in walk(self.out["summaryTree"])}
        self.assertFalse(summary_tags & {"a", "button", "nav"})

    def test_home_conflict_source_return_handoff_and_event_states_are_written_out(self) -> None:
        home_text = text(self.out["homeTree"])
        for phrase in (
            "Every state is written in words with a State or Source state label",
            "Source state: Unvalidated (needs steward check)",
            "Source state: Validated on record (not a winning source)",
            "Source state: Unverified (needs steward check)",
            "Source state: Disputed (action needed; sources disagree)",
            "Source state: Quarantined (not cleared for use)",
            "Source state: Stale (needs refresh check)",
            "State: Unresolved (action needed; both source values kept)",
            "State: Withdrawn (recorded disposition; not a winning source)",
            "State: Reconciled on record",
            "State: Unknown. Unresolved on this screen; not confirmed or cleared.",
            "State: Preserved unchanged in the table above",
            "State: Not selected. No latest-wins or silent correction is applied.",
            "State: Returned (action needed)",
            "State: Reopened (action needed)",
            "State: Offered, awaiting acceptance (action needed)",
            "State: Active stop on current stage (action needed)",
            "State: Active stop on current stage (open prerequisite; action needed)",
            "State: Active stop on current stage (blocked; action needed)",
            "State: Resolved on record (does not stop current stage)",
            "State: Open prerequisite (does not stop current stage; action needed)",
            "State: Open prerequisite (action needed)",
            "State: Action needed. Next action: Chase repairs team.",
            "State: Unknown. No interface run record is supplied to this screen.",
        ):
            self.assertIn(phrase, home_text)

        empty_text = text(self.out["emptyHomeTree"])
        self.assertIn("State: Unknown (none supplied)", empty_text)
        self.assertIn("State: Unknown. No recovery context is recorded.", empty_text)

        variants_text = " ".join(text(t) for t in self.out["handoffVariants"])
        for phrase in (
            "State: Received, awaiting acceptance (ownership unchanged; action needed)",
            "State: Escalated (unaccepted handoff; action needed)",
            "State: Declined by receiver (action needed)",
            "State: Completed on record",
        ):
            self.assertIn(phrase, variants_text)

        summary_text = text(self.out["summaryTree"])
        self.assertIn("State: Unavailable (action needed; not clear)", summary_text)
        self.assertIn("Source state: Unknown (Unavailable)", summary_text)

        ex_text = text(self.out["overviewExceptions"])
        for phrase in (
            "State: Loaded (ok; not an all clear)",
            "State: Paused for human review (held; action needed)",
            "State: Re-run requested (human action needed; not replayed)",
            "State: Closed on record",
            "State: Suppressed. No winning source is selected.",
            "State: Not assessed",
        ):
            self.assertIn(phrase, ex_text)

    def test_home_and_register_states_fail_closed_on_missing_colour_or_prototype_keys(
        self,
    ) -> None:
        leaked = r"\b(green|red|Pass|Healthy|Clear|false|constructor|toString|__proto__)\b"
        for bad_tree in self.out["poisonedHome"]:
            rendered = text(bad_tree)
            self.assertIn("Source state: Unknown", rendered)
            self.assertIn("State: Unknown (handoff not confirmed)", rendered)
            self.assertGreaterEqual(rendered.count("State: Unknown"), 9)
            self.assertNotIn("State: Returned", rendered)
            self.assertNotIn("State: Reopened", rendered)
            self.assertNotIn("function Object", rendered)
            self.assertNotIn("[native code]", rendered)
            self.assertNotRegex(rendered, leaked)
        for bad_reg in self.out["poisonedRegisters"]:
            rendered = text(bad_reg)
            self.assertIn("Service state Unknown. Synthetic.", rendered)
            self.assertIn("Register state State: Unknown", rendered)
            self.assertIn("State: Unknown. No winning source is selected.", rendered)
            self.assertNotIn("function Object", rendered)
            self.assertNotIn("[native code]", rendered)
            self.assertNotRegex(rendered, leaked)

    def test_home_and_summary_tables_are_keyboard_focusable_named_and_scoped(self) -> None:
        for key in ("homeTree", "summaryTree", "overviewExceptions"):
            nodes = walk(self.out[key])
            regions = [n for n in nodes if n["attrs"].get("role") == "region"]
            labels = [r["attrs"].get("aria-label") for r in regions]
            self.assertTrue(labels, key)
            self.assertEqual(len(labels), len(set(labels)), key)
            for region in regions:
                self.assertEqual(region["attrs"].get("tabindex"), 0, key)
            tables = [n for n in nodes if n.get("tag") == "table"]
            self.assertEqual(len(tables), len(regions), key)
            for table in tables:
                self.assertEqual(table["kids"][0]["tag"], "caption", key)
                self.assertTrue(text(table["kids"][0]).strip(), key)
                thead = next(k for k in table["kids"] if k.get("tag") == "thead")
                col_ths = [n for n in walk(thead) if n.get("tag") == "th"]
                self.assertTrue(col_ths, key)
                self.assertTrue(all(th["attrs"].get("scope") == "col" for th in col_ths), key)
                tbody = next(k for k in table["kids"] if k.get("tag") == "tbody")
                rows = [k for k in tbody["kids"] if k.get("tag") == "tr"]
                self.assertTrue(rows, key)
                for row in rows:
                    cells = row["kids"]
                    self.assertEqual(cells[0]["tag"], "th", key)
                    self.assertEqual(cells[0]["attrs"].get("scope"), "row", key)
                    self.assertTrue(all(c["tag"] == "td" for c in cells[1:]), key)
            if key in ("homeTree", "summaryTree"):
                for node in nodes:
                    self.assertNotIn(
                        node.get("tag"), ("button", "form", "input", "select", "textarea")
                    )
                    self.assertNotIn("onclick", node["attrs"])
                    self.assertNotIn("aria-invalid", node["attrs"])

    def test_rebase_preserves_housing_resident_helpers_alongside_steward_screen(self) -> None:
        role_source = (WEB / "role-screens.js").read_text(encoding="utf-8")
        style_source = (WEB / "style.css").read_text(encoding="utf-8")
        for token in (
            "const stateCue =",
            "const screenRecordTable =",
            "const ROLE_HASH_SCREENS =",
            "const residentJumpNav =",
            'id: "resident-service-issues"',
            'id: "resident-choice"',
            'id: "data-operator"',
            'screenRecordTable("Exception items returned for you"',
            'screenRecordTable("Source conflicts by home with both values"',
            'screenRecordTable("Source conflicts with both values and source details"',
        ):
            self.assertIn(token, role_source)
        for rule in (
            ".screen-record h2",
            '[tabindex="-1"] { scroll-margin-top: var(--sp-4); }',
            '[tabindex="-1"]:where(:not(#app)):focus',
        ):
            self.assertIn(rule, style_source)


if __name__ == "__main__":
    unittest.main()
