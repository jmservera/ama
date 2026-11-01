"""Package queue and contractor job pack screens are read-only and keep review separate."""

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
const input = JSON.parse(process.argv[2]);
const calls = [];
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  api: async (path) => {
    calls.push(path);
    return path.startsWith("/api/packages") ? input.packages : input.orders;
  },
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
const lookup = `;globalThis.__s = roleScreens.get(${JSON.stringify(input.id)});`;
vm.runInContext(host + "\n" + lookup, context);
(async () => {
  const s = context.__s;
  const extra = await s.load(input.c);
  console.log(JSON.stringify({roles: s.roles, calls, tree: await s.render(input.c, extra),
    empty: await s.render(input.c, {})}));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""

PACKAGE = {
    "id": "PKG-1",
    "name": "North wave",
    "period_from": "2026-04-01",
    "period_to": "2026-09-30",
    "contract_ref": "CALL-OFF-7",
    "contract_version": "2",
    "scope": "Loft insulation",
    "scope_version": 3,
    "consultation_status": "unknown",
    "capacity": [
        {
            "contractor": "Test Ltd",
            "offered": 40,
            "committed": 25,
            "in_use": 5,
            "headroom": 20,
            "evidence_status": "Unknown - not confirmed: missing",
        }
    ],
}
ORDER = {
    "id": "WO-1",
    "version": 2,
    "scope_version": 3,
    "package": "PKG-1",
    "contractor": "Test Ltd",
    "state": "Issued",
    "measures": "Loft insulation",
    "scope": "Loft insulation 270mm",
}
CONTROLS = ("button", "form", "input", "select", "textarea", "a")


def run(screen: str, **extra: object) -> dict[str, Any]:
    payload = {
        "id": screen,
        "c": {"id": "C-1", "needs_notice": True, "named_contact": "Named Contact"},
        "packages": [PACKAGE],
        "orders": [ORDER],
    } | extra
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(payload)],
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


def row_texts(node: object) -> list[str]:
    rows: list[str] = []
    if isinstance(node, dict):
        if node.get("tag") == "tr":
            rows.append(" | ".join(cells(node)))
        for kid in node.get("kids", []):
            rows += row_texts(kid)
    return rows


def cells(node: object) -> list[str]:
    if isinstance(node, str):
        return [node]
    if not isinstance(node, dict):
        return []
    if node.get("tag") in ("td", "th"):
        return ["".join(flat(node))]
    return [c for kid in node.get("kids", []) for c in cells(kid)]


def flat(node: object) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, dict):
        return [t for kid in node.get("kids", []) for t in flat(kid)]
    return []


class PackageQueue(unittest.TestCase):
    def test_fields_draft_readiness_and_no_controls(self) -> None:
        out = run("procurement-packages")
        text = json.dumps(out["tree"])
        self.assertEqual(out["roles"], ["Retrofit Programme Manager", "Programme Support Officer"])
        self.assertIn("/api/workorders?case=C-1", out["calls"])
        for expected in (
            "2026-04-01 to 2026-09-30",
            "Loft insulation (v3)",
            "CALL-OFF-7 v2",
            "Offered",
            "Committed",
            "WO-1 v2",
            "Draft readiness only",
            "Unmet or Unknown",
            "Contracts manager, independent",
            "Unassigned",
        ):
            self.assertIn(expected, text)
        self.assertNotIn("Ready for release", text)
        for control in CONTROLS:
            self.assertNotIn(control, tags(out["tree"]))

    def test_submission_is_separate_from_review_and_empty_is_unknown(self) -> None:
        out = run("procurement-packages", packages=[], orders=[])
        text = json.dumps(out["empty"])
        self.assertIn("not acceptance", text)
        self.assertIn("Separate step", text)
        self.assertIn("No records supplied", text)
        self.assertNotIn("Met on record", text)

    def prereq(self, orders: list[dict[str, Any]]) -> str:
        out = run("procurement-packages", orders=orders)
        return json.dumps(out["tree"])

    def test_work_order_validity_governs_resident_scope_prerequisite(self) -> None:
        met = [r for r in row_texts(json.loads(self.prereq([ORDER]))) if "with resident scope" in r]
        self.assertEqual(len(met), 1, met)
        self.assertIn("| Met on record |", met[0] + " |")
        withdrawn = self.prereq([ORDER | {"state": "Withdrawn"}])
        self.assertIn("Every work order for this home is withdrawn", withdrawn)
        self.assertIn("WO-1 v2", withdrawn)
        self.assertIn("older package scope", self.prereq([ORDER | {"scope_version": 2}]))
        unknown = self.prereq([{k: v for k, v in ORDER.items() if k != "scope_version"}])
        self.assertIn("scope version not supplied", unknown)

    def test_capacity_evidence_status_shown_with_recorded_counts(self) -> None:
        text = self.prereq([ORDER])
        self.assertIn("Recorded committed", text)
        self.assertIn("Unknown - not confirmed: missing", text)


class ContractorJobPack(unittest.TestCase):
    def test_contractor_view_has_checklist_and_no_reason_or_controls(self) -> None:
        out = run(
            "contractor-job-pack", c={"id": "C-1", "needs_notice": True, "named_contact": "NC"}
        )
        text = json.dumps(out["tree"])
        self.assertEqual(out["roles"], ["Contractor"])
        self.assertIn("WO-1 v2", text)
        self.assertIn("Needs notice", text)
        self.assertIn("reason for any notice is not shared", text)
        self.assertIn("Not assessed on this screen", text)
        self.assertNotIn("Not supplied", text)
        self.assertIn("Completion photographs", text)
        self.assertIn("not a provider portal", text)
        self.assertIn("Submission and review are separate", text)
        self.assertIn("acknowledgement is not acceptance", text.lower())
        self.assertIn("Done by someone other than you", text)
        self.assertNotIn("vulnerab", text.lower())
        for control in CONTROLS:
            self.assertNotIn(control, tags(out["tree"]))

    def test_appointment_outcome_derived_from_records(self) -> None:
        order = ORDER | {"appointments": [{"outcome": "Attended"}]}
        out = run("contractor-job-pack", orders=[order])
        self.assertIn("Recorded on a work order", json.dumps(out["tree"]))

    def test_no_notice_and_no_orders(self) -> None:
        out = run("contractor-job-pack", c={"id": "C-1", "needs_notice": False}, orders=[])
        text = json.dumps(out["tree"])
        self.assertIn("No extra notice needed", text)
        self.assertIn("No records supplied", text)
        self.assertIn("Unknown", text)


if __name__ == "__main__":
    unittest.main()
