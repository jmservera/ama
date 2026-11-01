"""Finance and grants reader screens compare invoice lines, show conflicts and offer no actions."""

import json
import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const data = JSON.parse(process.argv[2]);
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Grants and Evidence Officer"}},
  api: async (path) => {
    if (path === "/api/finance") return data.queue;
    if (path.startsWith("/api/ai/report")) throw new Error("403");
    if (path.endsWith("/form-review")) {
      if (data.review === null) throw new Error("403");
      return data.review;
    }
    return {};
  },
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens;", context);
(async () => {
  const out = {};
  for (const id of ["finance-invoices", "finance-funding"]) {
    const s = context.__s.get(id);
    const extra = await s.load(data.case);
    out[id] = {roles: s.roles, tree: await s.render(data.case, extra)};
  }
  console.log(JSON.stringify(out));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""

CASE: dict[str, object] = {
    "id": "C-1",
    "finance": {
        "budget": {"amount": 8750, "status": "Proposed"},
        "commitments": [
            {
                "id": "COM-1",
                "measure": "Loft insulation",
                "quantity": 1,
                "amount": 1700,
                "status": "Approved",
            }
        ],
        "invoices": [
            {
                "id": "INV-1",
                "kind": "Invoice",
                "ref": "R1",
                "supplier": "Test Ltd",
                "work_order": "WO-1",
                "status": "Exception, with Finance",
                "commitment": "COM-1",
                "payment_status": "Not payable yet",
                "disposition": None,
                "hold": None,
                "lines": [
                    {"measure": "Cavity wall", "quantity": 2, "amount": 1950, "milestone_ref": ""}
                ],
                "exceptions": [{"line": 0, "message": "Quantity 2 is above the 1 authorised."}],
            },
            {
                "id": "INV-2",
                "kind": "Invoice",
                "ref": "R2",
                "supplier": "Test Ltd",
                "work_order": "WO-2",
                "status": "Received",
                "commitment": None,
                "payment_status": "Awaiting payment run",
                "disposition": None,
                "hold": None,
                "lines": [
                    {
                        "measure": "Loft insulation",
                        "quantity": 1,
                        "amount": 100,
                        "milestone_ref": "M-1",
                    }
                ],
                "exceptions": [],
            },
        ],
    },
    "funding": {"route": "Grant route", "status": "To prepare", "reference": None},
    "grants": [
        {
            "id": "GR-1",
            "scheme": "Test scheme",
            "state": "Opportunity",
            "pending": None,
            "history": [],
        }
    ],
}
REVIEW: dict[str, object] = {
    "drafts": [
        {
            "draft_id": "FD-1",
            "schema_id": "S1",
            "schema_version": 1,
            "template": {"id": "T1"},
            "funding": {"route": "Grant route"},
            "rule_refs": [],
            "stale_fields": ["f2"],
            "reviewed_ready": False,
            "approved_rule_validation": "Not evaluated",
            "unit_currency_verification": "Not evaluated",
            "notice": "Unapproved working notes only.",
            "fields": {
                "f1": {"state": "Unknown", "value": None, "evidence": None},
                "f2": {
                    "state": "Accepted",
                    "effective_state": "Stale",
                    "value": 5,
                    "evidence": {"source": {"id": "DOC-1", "version": 2, "kind": "Survey"}},
                },
            },
            "issues": [
                {
                    "field_id": "f1",
                    "status": "Conflict",
                    "reason": "Unreviewed source alternatives.",
                }
            ],
        }
    ],
    "decision_holds": [],
}
QUEUE = [
    {
        "case_id": "C-1",
        "invoice": "INV-1",
        "supplier": "Test Ltd",
        "ref": "R1",
        "status": "Exception, with Finance",
        "exceptions": 1,
        "on_hold": False,
        "total": 1950,
    }
]
CONTROLS = ("button", "form", "input", "select", "textarea")


def run(
    case: dict[str, object] = CASE, review: object = REVIEW, queue: object = QUEUE
) -> dict[str, dict[str, object]]:
    payload = json.dumps({"case": case, "review": review, "queue": queue})
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), payload], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, dict[str, object]] = json.loads(result.stdout)
    return parsed


def tags(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        found.append(node.get("tag", ""))
        for kid in node.get("kids", []):
            found += tags(kid)
    return found


class FinanceGrantsScreens(unittest.TestCase):
    def test_roles_exclude_other_staff_and_no_controls(self) -> None:
        out = run()
        for screen in out.values():
            self.assertIn("Grants and Evidence Officer", screen["roles"])  # type: ignore[arg-type]
            self.assertNotIn("Contractor", screen["roles"])  # type: ignore[arg-type]
            for control in CONTROLS:
                self.assertNotIn(control, tags(screen["tree"]))

    def test_invoice_lines_compare_scope_quantity_budget_milestone(self) -> None:
        text = json.dumps(run()["finance-invoices"]["tree"])
        for expected in (
            "Not in scope (authorised: Loft insulation)",
            "Above authorised (2 of 1)",
            "Quantity 2 is above the 1 authorised.",
            "Proposed",
            "Unknown. No accepted milestone evidence.",
            "INV-1",
            "COM-1",
            "Not checked yet. Exceptions are unknown.",
            "Unknown. Not matched.",
            "Invoices waiting for Finance",
            "never makes or releases a payment",
        ):
            self.assertIn(expected, text)

    def test_ai_economics_unknown_without_report_or_billing(self) -> None:
        text = json.dumps(run()["finance-invoices"]["tree"])
        self.assertIn("Usage reconciled to billing", text)
        self.assertIn("Total Cost of AI components", text)
        self.assertIn("Booked-value status", text)
        self.assertIn("Overall AI cost per accepted outcome", text)
        self.assertIn("Unknown. No finance-defensible value", text)

    def test_queue_unreadable_stays_unknown(self) -> None:
        text = json.dumps(run(queue=None)["finance-invoices"]["tree"])
        self.assertIn("could not be read for your role", text)

    def test_funding_draft_shows_conflicts_and_evidence_without_submission(self) -> None:
        text = json.dumps(run()["finance-funding"]["tree"])
        for expected in (
            "Conflicting source candidates",
            "Unreviewed source alternatives.",
            "Nothing here picks a winning source",
            "DOC-1 v2 (Survey)",
            "Stale",
            "Not ready. No reviewed export exists.",
            "never infers them",
            "Eligibility",
            "Test scheme",
        ):
            self.assertIn(expected, text)
        self.assertNotIn("Submitted", text)

    def test_missing_records_are_unknown_not_empty_success(self) -> None:
        bare: dict[str, object] = {"id": "C-2"}
        out = run(bare, review=None)
        funding = json.dumps(out["finance-funding"]["tree"])
        self.assertIn("could not be read for your role", funding)
        self.assertIn("No grant recorded", funding)
        invoices = json.dumps(out["finance-invoices"]["tree"])
        self.assertIn("does not establish that nothing is owed", invoices)
        empty = json.dumps(
            run(bare, review={"drafts": [], "decision_holds": []})["finance-funding"]
        )
        self.assertIn("No field draft recorded", empty)


if __name__ == "__main__":
    unittest.main()
