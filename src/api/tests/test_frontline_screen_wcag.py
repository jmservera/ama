"""Frontline screens carry state in text, not colour alone (WCAG 1.4.1, Refs #232)."""

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
vm.runInContext(host + "\n;globalThis.__c = roleScreens.get('resident-choice');" +
  "globalThis.__s = roleScreens.get('resident-service-issues');", context);
const c = JSON.parse(process.argv[2]);
console.log(JSON.stringify({choice: context.__c.render(c), service: context.__s.render(c)}));
"""

CASE: dict[str, Any] = {
    "id": "C-1",
    "resident_update": {"status": "Proposed", "purpose": "Explain", "safe_contact_ref": "SC-1"},
    "measure_decisions": [
        {"measure": "Heat pump", "status": "Accepted", "versions": []},
        {"measure": "Solar PV", "status": "Waiting", "versions": []},
        {"measure": "Loft", "status": "Not recorded", "versions": []},
        {"measure": "Cavity", "status": "constructor", "versions": []},
    ],
    "service_requests": [
        {"id": "SR-1", "route": "Repair", "status": "Open", "accessibility": ["Large print"]},
        {"id": "SR-2", "route": "Repair", "status": "Closed", "accessibility": []},
        {"id": "SR-3", "route": "Repair", "status": "toString"},
    ],
}


def render() -> dict[str, str]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(CASE)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return {k: json.dumps(v) for k, v in json.loads(result.stdout).items()}


class FrontlineScreenWcag(unittest.TestCase):
    def test_choice_states_have_text_prefixes(self) -> None:
        text = render()["choice"]
        for expected in (
            "Confirmed: Accepted",
            "Waiting for resident: Waiting",
            "Waiting for resident: Not recorded",
            "Action needed: Proposed",
            "Confirmed: Large print",
            "Waiting for resident: Unknown",
        ):
            self.assertIn(expected, text)

    def test_unlisted_or_inherited_state_names_default_to_action_needed(self) -> None:
        out = render()
        self.assertIn("Action needed: constructor", out["choice"])
        self.assertIn("Action needed: toString. Meaning not recorded.", out["service"])

    def test_service_states_have_text_prefixes(self) -> None:
        text = render()["service"]
        self.assertIn("Action needed: Open. Opened and waiting", text)
        self.assertIn("Confirmed: Closed. Closed with an outcome", text)


if __name__ == "__main__":
    unittest.main()
