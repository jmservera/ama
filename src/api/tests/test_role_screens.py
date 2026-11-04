"""Specialist hosts describe navigation, never extend server authority."""

import json
import re
import subprocess
import unittest
from pathlib import Path

from zava_forward.api.workbench import navigation

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
DESIGN_SYSTEM = Path(__file__).resolve().parents[3] / "docs/reference/research/ux/design-system.md"


def inventory_classes() -> set[str]:
    """Class names the #150 component inventory documents, read from the design system."""
    text = DESIGN_SYSTEM.read_text()
    section = text.split("## Component inventory", 1)[1].split("### AI suggestion", 1)[0]
    return set(re.findall(r"`\.([A-Za-z0-9_-]+)", section))


class RoleScreens(unittest.TestCase):
    def test_closed_queue_retains_projected_safety_without_work(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const fs = require("node:fs");
const vm = require("node:vm");
const app = fs.readFileSync(process.argv[1] + "/progress.js", "utf8");
let rendered;
const context = vm.createContext({
  isManager: () => true,
  URLSearchParams, Intl, navigator: {language: "en-GB"},
  routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  location: {hash: "#/closed"},
  api: async () => ({total: 2, page: 1, pages: 1,
    facets: {statuses: ["Completed"], teams: []}, unknown_closure_dates: 2, items: [
    {id: "CLOSED-SAFETY", resident: "Safety resident", address: "1 Test Street",
      town: "Test", postcode: "TE1 1ST", status: "Completed", hazard: true},
    {id: "CLOSED-ORDINARY", resident: "Ordinary resident", address: "2 Test Street",
      town: "Test", postcode: "TE1 1ST", status: "Completed", hazard: false}
  ]}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat().filter(
    kid => kid !== false && kid !== null && kid !== undefined)}),
  show: (...nodes) => {rendered = nodes;}
});
vm.runInContext(app, context);
vm.runInContext("ProgressViews.closed()", context).then(() => {
  const links = [];
  function visit(node) {
    if (!node || typeof node !== "object") return;
    if (node.tag === "tr" && node.kids[0]?.attrs?.scope === "row") links.push(node);
    for (const child of node.kids || []) visit(child);
  }
  rendered.forEach(visit);
  console.log(JSON.stringify(links));
}).catch(error => {console.error(error); process.exitCode = 1;});
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        safety, ordinary = json.loads(result.stdout)
        self.assertIn("Safety issue open", json.dumps(safety))
        self.assertIn("flag danger", json.dumps(safety))
        self.assertNotIn("Safety issue open", json.dumps(ordinary))
        for node, case_id, name in (
            (safety, "CLOSED-SAFETY", "Safety resident"),
            (ordinary, "CLOSED-ORDINARY", "Ordinary resident"),
        ):
            with self.subTest(case_id=case_id):
                self.assertIn(f"#/case/{case_id}", json.dumps(node))
                self.assertIn(name, json.dumps(node))
                self.assertIn("Completed", json.dumps(node))
                self.assertNotIn("work-context", json.dumps(node))
                self.assertNotIn("safety-clock", json.dumps(node))

    def test_queue_renders_projected_safety_and_optional_work(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const fs = require("node:fs");
const vm = require("node:vm");
const app = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const work = {
  owner: "Task owner", reason: "Recorded reason", next_action: "Chase the response",
  source: "Recorded source", evidence: "SYN-EVIDENCE", version: 3,
  recorded_at: "2026-10-26T08:00:00Z", as_of: "2026-10-27",
  handoff: {destination: "Repairs", proposed_receiver: "Proposed receiver",
    confirmed_receiver: "Unknown", chase_owner: "Chase owner",
    resident_update_owner: "Update owner"},
  hazard_clocks: [
    {owner: "Safety follow-up owner", elapsed_hours: 24,
      aware_at: "2026-10-26T09:00:00Z", response_due_at: "2026-10-27T09:00:00Z",
      resident_update_due_at: "2026-10-27T10:00:00Z", authority: "External service",
      owner_named: true, owner_status: "Named follow-up owner recorded.",
      response_state: "Open", resident_update_state: "Open"},
    {owner: "Second follow-up owner", elapsed_hours: null, aware_at: "Unknown",
      response_due_at: "Unknown", resident_update_due_at: "Unknown",
      authority: "External service", owner_named: false,
      owner_status: "No named follow-up owner is recorded. Ask Task owner to record one.",
      response_state: "Unknown", resident_update_state: "Unknown"}
  ]
};
const rows = [
  {id: "SAFETY", address: "Safety home", status: "Generic status owner", hazard: true, work},
  {id: "ORDINARY", address: "Ordinary home", hazard: false,
    work: {...work, hazard_clocks: []}},
  {id: "CONTRACTOR", address: "Contractor home", stage: "Survey booked"},
  {id: "NULL-WORK", address: "No work supplied", hazard: true, work: null}
];
let rendered;
const context = vm.createContext({
  URLSearchParams, Intl, AbortController,
  location: {hash: "#/screens?screen=synthetic&page=2"},
  me: {user: {role: "Synthetic role"}},
  routeController: new AbortController(), workspaceStatus: {},
  api: async () => ({items: rows, total: 60}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat().filter(
    kid => kid !== false && kid !== null && kid !== undefined)}),
  show: (...nodes) => {rendered = nodes;}
});
vm.runInContext(app.slice(app.indexOf("function workSummary("),
  app.indexOf("function workSteps(")) + "\n" + host, context);
vm.runInContext(`registerRoleScreen({id: "synthetic", title: "Synthetic queue",
  roles: ["Synthetic role"]}); roleScreensView()`, context).then(() => {
  const links = [];
  function visit(node) {
    if (!node || typeof node !== "object") return;
    if (node.tag === "a" && node.attrs.class === "item") links.push(node);
    for (const child of node.kids || []) visit(child);
  }
  rendered.forEach(visit);
  console.log(JSON.stringify(links));
}).catch(error => {console.error(error); process.exitCode = 1;});
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        links = json.loads(result.stdout)
        self.assertEqual(len(links), 4)

        def text(node: object) -> str:
            if isinstance(node, dict):
                return " ".join(text(child) for child in node["kids"])
            return str(node)

        safety, ordinary, contractor, no_work = map(text, links)
        for phrase in (
            "Safety issue open",
            "Current owner: Task owner",
            "Reason: Recorded reason",
            "Next action: Chase the response",
            "Source: Recorded source",
            "evidence: SYN-EVIDENCE; version: 3",
            "recorded: 2026-10-26T08:00:00Z; recorded as of: 2026-10-27",
            "Destination: Repairs",
            "chase owner: Chase owner",
            "resident-update owner: Update owner",
            "24 elapsed hours",
            "awareness: 2026-10-26T09:00:00Z",
            "named follow-up owner: Safety follow-up owner",
            "service response due: 2026-10-27T09:00:00Z",
            "resident update due: 2026-10-27T10:00:00Z",
            "Safety clock in this recorded view: Unknown",
            "awareness: Unknown",
            "named follow-up owner: Second follow-up owner",
            "service response due: Unknown",
            "resident update due: Unknown",
            "External service owns timing.",
            "No named follow-up owner is recorded. Ask Task owner to record one.",
            "Service response: Open; resident update: Open.",
            "Service response: Unknown; resident update: Unknown.",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, safety)
        self.assertEqual(safety.count("Safety clock in this recorded view:"), 2)
        self.assertEqual(links[0]["attrs"]["href"], "#/screens?screen=synthetic&case=SAFETY&page=2")
        self.assertIn("Current owner: Task owner", ordinary)
        self.assertNotIn("Safety issue open", ordinary)
        self.assertNotIn("Safety clock", ordinary)
        self.assertIn("Contractor home", contractor)
        self.assertNotIn("Current owner:", contractor)
        self.assertNotIn("Safety issue open", contractor)
        self.assertIn("Safety issue open", no_work)
        self.assertNotIn("Current owner:", no_work)
        self.assertNotIn("Safety clock", no_work)
        marker = next(
            kid
            for kid in links[0]["kids"][0]["kids"]
            if isinstance(kid, dict) and kid["attrs"].get("class") == "flag danger"
        )
        self.assertEqual(text(marker), "Safety issue open")

    def test_resident_choice_states_choice_precedence_after_choice_panels(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const context = vm.createContext({
  URLSearchParams, Intl, AbortController,
  me: {user: {role: "Resident Liaison Officer"}}, workspaceStatus: {},
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat().filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host, context);
const homes = [
  {id: "HOME-STOPPED", measure_decisions: [{measure: "Loft insulation", status: "Withdrawn",
    versions: [{version: 1, status: "Withdrawn", scope: "S1", context_revision: 1,
      design_version: 1, answered_by: "Resident", at: "2026-10-26T08:00:00Z", note: "No"}]}]},
  {id: "HOME-OPEN", measure_decisions: [{measure: "Windows", status: "Agreed",
    versions: [{version: 1, status: "Agreed", scope: "S1", context_revision: 1,
      design_version: 1, answered_by: "Resident", at: "2026-10-26T08:00:00Z"}]}]},
  {id: "HOME-EMPTY"}
];
function text(node) {
  if (!node || typeof node !== "object") return String(node);
  return (node.kids || []).map(text).join(" ");
}
const screen = vm.runInContext(`roleScreens.get("resident-choice")`, context);
console.log(JSON.stringify(homes.map(home => {
  const panels = screen.render(home).kids;
  return panels.map(panel => ({
    tag: panel.tag, title: text(panel.kids[0]), text: text(panel),
    paragraphs: panel.kids.slice(1).filter(kid => kid.tag === "p").map(text)
  }));
})));
""",
                str(WEB),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        homes = json.loads(result.stdout)
        self.assertEqual(len(homes), 3)
        for home in homes:
            titles = [panel["title"] for panel in home]
            for earlier in ("Choice for each measure", "Paused or withdrawn by the resident"):
                self.assertLess(
                    titles.index(earlier), titles.index("Choice comes before offered capacity")
                )
            index = titles.index("Choice comes before offered capacity")
            panel = home[index]
            self.assertEqual(panel["tag"], "section")
            self.assertEqual(len(panel["paragraphs"]), 1)
            self.assertIn(
                "takes precedence over any offered contractor slot", panel["paragraphs"][0]
            )
            self.assertIn("not a booking and not a promise to the resident", panel["paragraphs"][0])
            before = " ".join(p["text"] for p in home[:index]).lower()
            for word in ("capacity", "utilisation", "headroom"):
                self.assertNotIn(word, before)

    def test_staff_and_contractor_navigation_retains_scoped_screen_link(self) -> None:
        for role in ("Resident Liaison Officer", "Retrofit Programme Manager", "Contractor"):
            links = navigation({"role": role})
            self.assertEqual(links[-1]["href"], "#/screens")
            self.assertTrue(links[-1]["scope"])
        self.assertEqual(navigation({"role": "Asset Executive"}), [])

    def test_host_reads_existing_scoped_endpoints_without_post(self) -> None:
        source = (WEB / "role-screens.js").read_text()
        self.assertIn("/api/cases?view=all&limit=20&offset=", source)
        self.assertIn("encodeURIComponent(caseId)", source)
        self.assertNotIn('"POST"', source)
        self.assertNotIn("innerHTML", source)

    def test_route_supports_contractor_screens_before_contractor_case_dispatch(self) -> None:
        source = (WEB / "app.js").read_text()
        self.assertLess(
            source.index("return await roleScreensView()"),
            source.index("return await (m ? contractorCaseView"),
        )
        self.assertIn('src="/role-screens.js"', (WEB / "index.html").read_text())

    def test_host_requires_explicit_selection_and_retains_abort_boundary(self) -> None:
        source = (WEB / "role-screens.js").read_text()
        self.assertIn("No home selected", source)
        self.assertIn("signal.throwIfAborted()", source)
        self.assertIn('"aria-current"', source)
        self.assertIn("Reset screen view", source)

    def test_screens_use_only_documented_design_system_classes_and_no_simulator(self) -> None:
        source = (WEB / "role-screens.js").read_text()
        used = {
            name for literal in re.findall(r'class: "([^"]*)"', source) for name in literal.split()
        }
        documented = inventory_classes()
        self.assertTrue({"card", "screen-record", "table-scroll", "empty"} <= documented)
        self.assertTrue(used, "no class literals found; the check would pass vacuously")
        self.assertEqual(used - documented, set())
        for word in ("Simulate", "simulator", "switch role", "fluent-"):
            self.assertNotIn(word.lower(), source.lower())
