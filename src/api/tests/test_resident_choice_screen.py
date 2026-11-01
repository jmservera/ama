"""Resident choice screen separates choice, pause, access and commitment and offers no controls."""

import json
import subprocess
import unittest
from collections.abc import Mapping
from pathlib import Path

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
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('resident-choice');", context);
const c = JSON.parse(process.argv[2]);
console.log(JSON.stringify({roles: context.__s.roles, tree: context.__s.render(c)}));
"""

CASE = {
    "id": "C-1",
    "measure_decisions": [
        {
            "measure": "Loft insulation",
            "status": "Paused",
            "readiness": "Needs human review",
            "context": {"scope": "S-9", "revision": 2, "design_version": 3},
            "versions": [
                {"version": 1, "status": "Accepted", "answered_by": "The resident"},
                {
                    "version": 2,
                    "status": "Paused",
                    "answered_by": "The resident",
                    "note": "Not before spring",
                },
            ],
        },
        {
            "measure": "Solar PV",
            "status": "Not recorded",
            "readiness": "Resident decision current",
            "versions": [],
        },
    ],
    "resident_update": {
        "status": "Outstanding",
        "purpose": "Explain damp query",
        "owner_identity": {"name": "Owner One"},
        "due_at": "2026-12-01T10:00:00+00:00",
        "basis": "Resident asked",
        "safe_contact_ref": "SC-77",
        "version": 2,
    },
    "service_requests": [
        {
            "id": "SR-1",
            "route": "Repair",
            "status": "Open",
            "accessibility": ["Phone only"],
            "next_update": "2026-12-02",
        }
    ],
}


def run(case: Mapping[str, object]) -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(case)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, object] = json.loads(result.stdout)
    return parsed


def tags(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        found.append(node.get("tag", ""))
        for kid in node.get("kids", []):
            found += tags(kid)
    return found


class ResidentChoiceScreen(unittest.TestCase):
    def test_choice_pause_commitment_and_access_are_distinct(self) -> None:
        out = run(CASE)
        text = json.dumps(out["tree"])
        self.assertIn("Resident Liaison Officer", json.dumps(out["roles"]))
        self.assertNotIn("Resident Simulator", json.dumps(out["roles"]))
        for expected in (
            "Loft insulation",
            "scope S-9, revision 2, design 3",
            "v2 Paused",
            "Not before spring",
            "Not recorded",
            "Paused or withdrawn by the resident",
            "Human review before any restart",
            "Explain damp query",
            "Owner One",
            "SC-77",
            "Safe route reference",
            "Phone only",
            "Service requests and access needs (separate from choice)",
            "not a contact attempt",
        ):
            self.assertIn(expected, text)

    def test_no_controls_and_no_contact(self) -> None:
        tree = run(CASE)["tree"]
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))
        self.assertIn("No message, call or letter is sent", json.dumps(tree))

    def test_empty_case_stays_unknown(self) -> None:
        text = json.dumps(run({"id": "C-2"})["tree"])
        self.assertIn("No records supplied", text)
        self.assertIn("No measure is currently paused or withdrawn", text)
        self.assertIn("No update commitment is recorded", text)


if __name__ == "__main__":
    unittest.main()
