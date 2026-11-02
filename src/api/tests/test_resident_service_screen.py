"""Resident service issue screen shows access needs, owners and commitment with no controls."""

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
  routeController: new AbortController(), me: {user: {role: "Resident Liaison Officer"}},
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('resident-service-issues');", context);
const c = JSON.parse(process.argv[2]);
const s = context.__s;
console.log(JSON.stringify({roles: s.roles, tree: s.render(c), empty: s.render({id: "C-2"}),
  summary: s.summary([[{id: "C-1"}, c], [{id: "C-9"}, null]])}));
"""

CASE = {
    "id": "C-1",
    "resident_update": {
        "status": "Outstanding",
        "purpose": "Explain damp query",
        "owner_identity": {"name": "Owner One"},
        "due_at": "2026-12-01T10:00:00+00:00",
        "safe_contact_ref": "SC-77",
    },
    "service_requests": [
        {
            "id": "SR-1",
            "route": "Complaint",
            "summary": "Mould not treated",
            "desired_outcome": "Treatment visit",
            "status": "Resolved",
            "service_owner": "Service Person",
            "redress_owner": "Redress Person",
            "accessibility": ["Phone only", "Large print"],
            "representative_ref": "REP-3",
            "next_update": "2026-12-05",
            "history": [{"status": "In progress", "by": "Service Person", "note": "Visit booked"}],
        },
        {"id": "SR-2", "route": "Repair", "status": "Closed"},
    ],
}

CONTROLS = ("button", "form", "input", "select", "textarea")


def run() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(CASE)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def tags(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        found.append(node.get("tag", ""))
        for kid in node.get("kids", []):
            found += tags(kid)
    return found


class ResidentServiceScreen(unittest.TestCase):
    def test_issue_owners_needs_and_commitment_are_visible(self) -> None:
        out = run()
        text = json.dumps(out["tree"])
        self.assertIn("Resident Liaison Officer", json.dumps(out["roles"]))
        self.assertNotIn("Resident Simulator", json.dumps(out["roles"]))
        for expected in (
            "Mould not treated",
            "Wanted: Treatment visit",
            "Resolved. The owner says it is dealt with. It is not closed",
            "Service: Service Person. Redress: Redress Person",
            "Phone only, Large print",
            "REP-3",
            "Visit booked",
            "Explain damp query",
            "Owner One",
            "SC-77",
            "A commitment is not a message",
            "shown on the resident choice screen, not here",
            "Not an independent review",
        ):
            self.assertIn(expected, text)

    def test_summary_lists_open_issues_only_and_marks_unavailable_homes(self) -> None:
        text = json.dumps(run()["summary"])
        self.assertIn("SR-1 Complaint: Resolved", text)
        self.assertNotIn("SR-2", text)
        self.assertIn("Unavailable", text)
        self.assertIn("not a portfolio total", text)

    def test_empty_case_is_unknown_not_clear(self) -> None:
        text = json.dumps(run()["empty"])
        self.assertIn("does not establish that the resident has none", text)
        self.assertIn("No update commitment is recorded", text)

    def test_screen_offers_no_controls(self) -> None:
        found = tags(run()["tree"])
        for control in CONTROLS:
            self.assertNotIn(control, found)


if __name__ == "__main__":
    unittest.main()
