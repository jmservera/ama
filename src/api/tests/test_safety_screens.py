"""Building safety and hazard triage screens show referral states and offer no controls."""

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
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Building Safety Liaison"}},
  api: async () => ({}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__r = roleScreens;", context);
(async () => {
  const c = {id: "C-1", hazards: JSON.parse(process.argv[2])};
  const out = {};
  for (const id of ["safety-lead", "hazard-triage"]) {
    const s = context.__r.get(id);
    out[id] = {roles: s.roles, tree: await s.render(c), empty: await s.render({id: "C-2"}),
      summary: s.summary([[{id: "C-1"}, c], [{id: "C-9"}, null], [{id: "C-3"}, {id: "C-3"}],
        [{id: "C-4", hazard: true}, {id: "C-4", hazards: []}],
        [{id: "C-5", hazard: false}, {id: "C-5", hazards: []}]])};
  }
  console.log(JSON.stringify(out));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""
VIEW_SCRIPT = (
    SCRIPT.split("(async () => {")[0].replace(
        "api: async () => ({}),",
        """location: {hash: "#/screens?screen=safety-lead"}, shown: [],
  show: (...n) => context.shown.push(n), workspaceStatus: () => null,
  api: async (u) => u.startsWith("/api/cases?") ? {items: [{id: "C-1"}], total: 1}
    : {id: "C-1", hazards: [{category: "Damp", priority: "Urgent", source: "Call"}]},""",
    )
    + """
(async () => {
  await context.roleScreensView();
  console.log(JSON.stringify(context.shown));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""
)

SENDER = {"name": "Rex Coordinator", "role": "Retrofit Coordinator"}
SAFE = {"name": "Bea Safe", "role": "Building Safety Liaison"}


def hazard(**kw: object) -> dict[str, object]:
    base: dict[str, object] = {
        "category": "Damp and mould",
        "priority": "Urgent",
        "aware_at": "2026-10-30T09:00:00+00:00",
        "source": "Resident phone call",
        "destination": SAFE,
        "sender": SENDER,
        "owner": "Rex Coordinator",
        "state": "Sent",
        "sent_at": "2026-10-30T10:00:00+00:00",
        "received_at": None,
        "accepted_at": None,
        "hold": {"scope": "Home", "case_id": "C-1", "status": "Active", "decision": None},
    }
    base.update(kw)
    return base


def run(hazards: list[dict[str, object]]) -> dict[str, dict[str, Any]]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(hazards)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, dict[str, Any]] = json.loads(result.stdout)
    return parsed


def tags(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        found.append(node.get("tag", ""))
        for kid in node.get("kids", []):
            found += tags(kid)
    return found


def find_all(node: object, tag: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if node.get("tag") == tag:
            found.append(node)
        for kid in node.get("kids", []):
            found += find_all(kid, tag)
    return found


class SafetyScreens(unittest.TestCase):
    def test_rendered_tables_are_labelled_focusable_and_aligned(self) -> None:
        for screen in run([hazard()]).values():
            for view in (screen["tree"], screen["summary"]):
                regions = [r for r in find_all(view, "div") if r["attrs"].get("role") == "region"]
                self.assertTrue(regions)
                for region in regions:
                    self.assertTrue(region["attrs"]["aria-label"])
                    self.assertEqual(region["attrs"]["tabindex"], 0)
                    (table,) = find_all(region, "table")
                    (caption,) = find_all(table, "caption")
                    self.assertEqual(caption["kids"], [region["attrs"]["aria-label"]])
                    heads = find_all(table, "th")
                    self.assertTrue(all(t["attrs"] == {"scope": "col"} for t in heads))
                    for row in find_all(find_all(table, "tbody")[0], "tr"):
                        self.assertEqual(len(find_all(row, "td")), len(heads))

    def test_cross_home_summary_is_not_truncated_beyond_fifty(self) -> None:
        released = hazard(hold={"scope": "Home", "case_id": "C-1", "status": "Released"})
        items = [released] * 50 + [hazard(source="Late active hazard")]
        for screen in run(items).values():
            text = json.dumps(screen["summary"])
            self.assertIn("C-1 H-51", text)
            self.assertIn("Late active hazard", text)
            self.assertNotIn("Showing the first", text)

    def test_roles_are_scoped(self) -> None:
        out = run([])
        self.assertEqual(
            out["safety-lead"]["roles"],
            ["Building Safety Liaison", "Retrofit Programme Manager", "Programme Support Officer"],
        )
        self.assertNotIn("Building Safety Liaison", out["hazard-triage"]["roles"])
        self.assertIn("Retrofit Coordinator", out["hazard-triage"]["roles"])

    def test_pending_receipt_has_owned_follow_up_and_distinct_states(self) -> None:
        out = run([hazard()])
        for screen in out.values():
            text = json.dumps(screen["tree"])
            self.assertIn("Resident phone call", text)
            self.assertIn("Aware at", text)
            self.assertIn("Bea Safe, Building Safety Liaison", text)
            self.assertIn(
                "Pending receipt. Follow-up owner: Rex Coordinator, Retrofit Coordinator", text
            )
            self.assertIn("Not recorded", text)
            for column in ("Sent", "Received", "Accepted"):
                self.assertIn(column, text)

    def test_received_is_not_accepted(self) -> None:
        text = json.dumps(
            run(
                [
                    hazard(
                        received_at="2026-10-30T11:00:00+00:00",
                        state="Received",
                        follow_up=SENDER,
                    )
                ]
            )["safety-lead"]["tree"]
        )
        self.assertIn("Pending acceptance. Follow-up owner: Rex Coordinator", text)
        self.assertNotIn("owns the accepted scope", text)

    def test_legacy_referral_without_send_time_is_not_reported_unsent(self) -> None:
        text = json.dumps(run([hazard(sent_at=None, referred="2026-10-01")])["safety-lead"]["tree"])
        self.assertIn("Legacy referral with no recorded send time", text)
        self.assertNotIn("No referral sent", text)

    def test_legacy_owner_only_referral_keeps_recorded_owner_as_unverified(self) -> None:
        legacy = hazard(sent_at=None, referred="2026-10-01", owner="Pat Owner")
        text = json.dumps(run([legacy])["safety-lead"]["tree"])
        self.assertIn("Recorded owner (unverified): Pat Owner", text)
        self.assertIn("Retrofit Coordinator to confirm ownership", text)

    def test_every_record_is_reachable_beyond_fifty(self) -> None:
        released = hazard(hold={"scope": "Home", "case_id": "C-1", "status": "Released"})
        items = [released] * 50 + [hazard(source="Late active hazard")]
        for screen in run(items).values():
            text = json.dumps(screen["tree"])
            self.assertIn("Late active hazard", text)
            self.assertIn("H-51", text)
            self.assertNotIn("Showing the first", text)

    def test_release_shows_decision_evidence_and_released_stays_visible(self) -> None:
        released = hazard(
            state="Retrofit hold released",
            received_at="2026-10-30T11:00:00+00:00",
            accepted_at="2026-10-30T12:00:00+00:00",
            accepted_by=SAFE,
            hold={
                "scope": "Home",
                "case_id": "C-1",
                "status": "Released",
                "decision": {
                    "at": "2026-10-31T09:00:00+00:00",
                    "actor": SAFE,
                    "reason": "Repair verified",
                    "evidence": "External job J-9 sign-off",
                },
            },
        )
        legacy = hazard(
            state="Legacy",
            hold={"scope": "Home", "case_id": "C-1", "status": "Released", "decision": None},
        )
        text = json.dumps(run([released, legacy])["safety-lead"]["tree"])
        self.assertIn("Decided by Bea Safe", text)
        self.assertIn("External job J-9 sign-off", text)
        self.assertIn("H-2", text)
        self.assertIn("No authoritative decision evidence is recorded", text)

    def test_cross_home_summary_lists_every_hazard_and_unavailable_homes(self) -> None:
        released = hazard(source="Released source", hold={"status": "Released"})
        out = run([hazard(), released])
        for screen in out.values():
            text = json.dumps(screen["summary"])
            self.assertIn("across this page of homes", text)
            self.assertIn("not a portfolio total", text)
            self.assertIn("C-1 H-1", text)
            self.assertIn("C-1 H-2", text)
            self.assertIn("Resident phone call", text)
            self.assertIn("Pending receipt. Follow-up owner: Rex Coordinator", text)
            self.assertIn("Unavailable. Open the home to check.", text)
            self.assertIn("does not establish that no hazard exists", text)
            self.assertIn("Unknown. Hazard list not supplied", text)
            self.assertIn("C-3", text)
            self.assertIn("Mismatch. The list flags a hazard", text)
            self.assertIn("C-4", text)
            self.assertNotIn("C-5", text)
            for part in (
                "Aware at",
                "2026",
                "Destination",
                "Bea Safe",
                "Sent",
                "Received",
                "Accepted",
                "Recorded",
                "Not recorded",
                "Pause status",
                "Active",
            ):
                self.assertIn(part, text)
            self.assertIn("Released. Release decision evidence: open the home", text)
            for control in ("button", "form", "input", "select", "textarea"):
                self.assertNotIn(control, tags(screen["summary"]))

    def test_view_summarises_when_no_home_selected(self) -> None:
        result = subprocess.run(
            ["node", "-e", VIEW_SCRIPT, str(WEB)], capture_output=True, text=True, check=True
        )
        text = result.stdout
        self.assertIn("Hazard referrals across this page of homes", text)
        self.assertIn("C-1 H-1", text)

    def test_no_controls_and_boundary_text(self) -> None:
        out = run([hazard()])
        for screen in out.values():
            text = json.dumps(screen["tree"]).lower()
            for control in ("button", "form", "input", "select", "textarea"):
                self.assertNotIn(control, tags(screen["tree"]))
            self.assertIn(
                "does not classify hazards, set clocks, close hazards or authorise work", text
            )
            self.assertIn("including released ones", text)
            self.assertIn("No records supplied", json.dumps(screen["empty"]))


if __name__ == "__main__":
    unittest.main()
