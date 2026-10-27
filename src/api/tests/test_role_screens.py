"""Specialist hosts describe navigation, never extend server authority."""

import json
import subprocess
import unittest
from pathlib import Path

from zava_forward.api.workbench import navigation

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class RoleScreens(unittest.TestCase):
    def test_closed_queue_retains_projected_safety_without_work(self) -> None:
        result = subprocess.run(
            [
                "node",
                "-e",
                r"""
const fs = require("node:fs");
const vm = require("node:vm");
const app = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
let rendered;
const context = vm.createContext({
  isManager: () => true,
  api: async () => ({total: 2, items: [
    {id: "CLOSED-SAFETY", resident: "Safety resident", address: "1 Test Street",
      town: "Test", postcode: "TE1 1ST", stage: "Completed", hazard: true},
    {id: "CLOSED-ORDINARY", resident: "Ordinary resident", address: "2 Test Street",
      town: "Test", postcode: "TE1 1ST", stage: "Completed", hazard: false}
  ]}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat().filter(
    kid => kid !== false && kid !== null && kid !== undefined)}),
  show: (...nodes) => {rendered = nodes;}
});
vm.runInContext(app.slice(app.indexOf("async function closedView("),
  app.indexOf("async function contractorListView(")), context);
vm.runInContext("closedView()", context).then(() => {
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
        safety, ordinary = json.loads(result.stdout)
        self.assertIn("Safety issue open", json.dumps(safety))
        self.assertIn("flag danger", json.dumps(safety))
        self.assertNotIn("Safety issue open", json.dumps(ordinary))
        for node, case_id, name in (
            (safety, "CLOSED-SAFETY", "Safety resident"),
            (ordinary, "CLOSED-ORDINARY", "Ordinary resident"),
        ):
            with self.subTest(case_id=case_id):
                self.assertEqual(node["attrs"]["href"], f"#/case/{case_id}")
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
      resident_update_due_at: "2026-10-27T10:00:00Z", authority: "External service"},
    {owner: "Second follow-up owner", elapsed_hours: null, aware_at: "Unknown",
      response_due_at: "Unknown", resident_update_due_at: "Unknown",
      authority: "External service"}
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
