"""Data steward and operator screen shows both sources and offers no replay."""

import json
import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const side = (value, id, version) => ({value, source_id: id, date: "2026-01-01", version,
  validation_state: "Unvalidated"});
const c = {id: "C-1",
  stock_reconciliation: [{id: "SQ-1", field: "epc", query_owner: {name: "Query Owner"},
    left: side("D", "S-A", "1"), right: side("C", "S-B", "2")},
    {id: "SQ-2", field: "age", query_owner: {name: "Query Owner"},
    left: side("1", "S-A", "1"), right: side("2", "S-B", "2")}],
  stock_reconciliation_events: [{id: "SQE-1", query_id: "SQ-1", status: "Withdrawn",
    at: "2026-10-01T10:00:00Z", recorded_by: {name: "Named Person"}, reason: "Duplicate"}],
  work: {owner: "Task owner", reason: "Returned for evidence", next_action: "Resend pack",
    as_of: "2026-10-27", handoff: {destination: "Repairs", proposed_receiver: "R",
      confirmed_receiver: "Unknown", chase_owner: "Chase owner"},
    blockers: [{step: "Survey", reason: "Missing reference", owner: "Owner A",
      next_action: "Supply it", source: "SYN", version: 3}]}};
const ret = {at: "2026-10-02T09:00:00Z", reopened: false, from_stage: "Install booked",
  to_stage: "Survey", reason: "Return reason X", source: "SRC-R", source_version: "4",
  next_action: "Rework survey", receiving_owner: {name: "Receiver Y"}};
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  api: async () => ({}),
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('data-operator');", context);
const s = context.__s;
const noHandoff = {...c, returns: [ret], work: {...c.work, handoff: undefined}};
const noReturn = {...c, returns: [], work: {...c.work, reason: "Handoff reason Z"}};
const reopen = {...c, returns: [{...ret, reopened: true, reason: "Reopen reason"}]};
const adv = {...ret, event_type: "advance", reason: "Forward reason",
  receiving_owner: {name: "Forward Owner"}};
const forwardOnly = {...c, returns: [adv]};
const mixed = {...c, returns: [adv, ret]};
console.log(JSON.stringify({forwardOnly: s.render(forwardOnly), mixed: s.render(mixed),
  roles: s.roles, tree: s.render(c), empty: s.render({id: "C-2"}),
  noHandoff: s.render(noHandoff), noReturn: s.render(noReturn), reopen: s.render(reopen)}));
"""


def run() -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=30
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


class DataOperatorScreen(unittest.TestCase):
    def test_both_values_provenance_and_preserved_eligibility(self) -> None:
        out = run()
        text = json.dumps(out["tree"])
        self.assertEqual(out["roles"], ["Retrofit Programme Manager", "Programme Support Officer"])
        for phrase in ("D; source S-A v1", "C; source S-B v2", "Query Owner", "Unresolved"):
            self.assertIn(phrase, text)
        self.assertIn("Eligibility", text)
        self.assertIn("Not selected. No latest-wins or silent correction", text)

    def test_exceptions_events_and_audit_caveat(self) -> None:
        text = json.dumps(run()["tree"])
        for phrase in ("Returned for evidence", "Missing reference", "Chase owner", "Named Person"):
            self.assertIn(phrase, text)
        self.assertIn("not an operational audit trail", text)
        self.assertIn("Recovery context", text)

    def test_no_controls_and_unknown_when_empty(self) -> None:
        out = run()
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(out["tree"]))
        empty = json.dumps(out["empty"])
        self.assertIn("No return or reopen is recorded", empty)
        self.assertIn("No handoff is recorded", empty)
        self.assertIn("No records supplied", empty)

    def test_return_without_handoff_and_handoff_without_return(self) -> None:
        out = run()
        returned = json.dumps(out["noHandoff"])
        for phrase in (
            "Return reason X",
            "Receiver Y",
            "SRC-R v4",
            "Rework survey",
            "Returned",
            "No handoff is recorded",
        ):
            self.assertIn(phrase, returned)
        self.assertNotIn("No return or reopen is recorded", returned)
        handed = json.dumps(out["noReturn"])
        for phrase in ("Repairs", "Chase owner", "No return or reopen is recorded"):
            self.assertIn(phrase, handed)
        self.assertNotIn("Returned to", handed)
        self.assertIn("Reopened", json.dumps(out["reopen"]))

    def test_advance_events_are_not_returns(self) -> None:
        out = run()
        forward = json.dumps(out["forwardOnly"])
        self.assertIn("No return or reopen is recorded", forward)
        self.assertNotIn("Forward Owner", forward)
        mixed = json.dumps(out["mixed"])
        self.assertIn("Receiver Y", mixed)
        self.assertNotIn("Forward Owner", mixed)
        self.assertNotIn("Recorded returns and reopens", forward)


if __name__ == "__main__":
    unittest.main()
