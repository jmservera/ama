"""Finance and grants reader screens compare invoice lines, show conflicts and offer no actions."""

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
                "exceptions": [
                    {
                        "line": 0,
                        "code": "quantity",
                        "message": "Quantity 2 is above the 1 authorised.",
                    },
                    {"line": 0, "code": "no_budget", "message": "No approved budget."},
                    {"line": 0, "code": "future_code", "message": "Something new."},
                ],
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


def walk(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


def node_text(node: object) -> str:
    if isinstance(node, dict):
        return "".join(node_text(k) for k in node.get("kids", []))
    return node if isinstance(node, str) else ""


def explanation_rows(tree: object, invoice: str) -> list[list[str]]:
    caption = f"Exception explanations for {invoice}"
    for table in (n for n in walk(tree) if n["tag"] == "table"):
        if node_text(table["kids"][0]) == caption:
            body = [n for n in walk(table) if n["tag"] == "tr"][1:]
            return [[node_text(c) for c in row["kids"]] for row in body]
    return []


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
            "Unknown. No milestone reference supplied.",
            "line total",
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

    def test_economics_section_on_both_screens_is_unknown_without_inputs(self) -> None:
        out = run()
        for screen_id in ("finance-invoices", "finance-funding"):
            text = json.dumps(out[screen_id]["tree"])
            for expected in (
                "Usage reconciled to billing",
                "Total Cost of AI component: Platform and hosting",
                "Total Cost of AI component: People and process change",
                "Booked-value status",
                "spend avoided or capital freed",
                "nothing here depends on AI",
                "could not be read for your role. Cost and value stay Unknown",
            ):
                self.assertIn(expected, text)
            self.assertNotIn("GBP", text)

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

    def test_unchecked_queue_row_and_unreadable_review_stay_unknown(self) -> None:
        unchecked = [{**QUEUE[0], "status": "Received", "exceptions": 0}]
        text = json.dumps(run(queue=unchecked)["finance-invoices"]["tree"])
        self.assertIn("Unknown. Not checked yet", text)
        self.assertNotIn("0 exceptions", text)
        funding = json.dumps(run(review=None)["finance-funding"]["tree"])
        self.assertIn("Unknown. The field review could not be read.", funding)
        self.assertNotIn("None recorded", funding)
        self.assertNotIn("No reviewed export exists", funding)

    def test_nonconforming_review_and_invalid_quantity_stay_unknown(self) -> None:
        funding = json.dumps(run(review={})["finance-funding"]["tree"])
        self.assertIn("Unknown. The field review could not be read.", funding)
        self.assertNotIn("No reviewed export exists", funding)
        case = json.loads(json.dumps(CASE))
        for line in case["finance"]["invoices"][0]["lines"]:
            line["quantity"] = None
        text = json.dumps(run(case)["finance-invoices"]["tree"])
        self.assertIn("Unknown. Quantity not supplied or invalid.", text)
        self.assertNotIn("Within authorised", text)

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

    def test_exception_explanations_name_decider_and_never_decide_payment(self) -> None:
        rows = explanation_rows(run()["finance-invoices"]["tree"], "INV-1")
        self.assertEqual(len(rows), 3)
        by_message = {row[0]: row for row in rows}
        quantity = by_message["Quantity 2 is above the 1 authorised."]
        no_budget = by_message["No approved budget."]
        unknown = by_message["Something new."]
        self.assertEqual(no_budget[1], "Whole invoice")
        for row in (quantity, unknown):
            self.assertEqual(row[1], "Line 1")
        for row in (quantity, no_budget, unknown):
            self.assertIn("Payment is made outside this system.", row[4])
        self.assertEqual(quantity[2], "This line is above the quantity the commitment authorises.")
        self.assertTrue(quantity[4].startswith("Finance approver (Retrofit Programme Manager"))
        self.assertIn("It stays Unknown.", no_budget[3])
        self.assertTrue(no_budget[4].startswith("Finance approver"))
        self.assertTrue(unknown[2].startswith("Unknown."))
        self.assertEqual(unknown[3], "Unknown")
        self.assertTrue(unknown[4].startswith("Unknown."))
        self.assertNotIn("Finance approver", unknown[4])
        tree = json.dumps(run()["finance-invoices"]["tree"])
        inv2 = tree[tree.index("INV-2: Invoice") :]
        self.assertIn("Exception explanations are Unknown. The invoice is not checked yet.", inv2)

    def test_invoice_level_exception_is_grouped_across_lines(self) -> None:
        case = json.loads(json.dumps(CASE))
        inv = case["finance"]["invoices"][0]
        inv["lines"].append(
            {"measure": "Loft insulation", "quantity": 1, "amount": 100, "milestone_ref": ""}
        )
        inv["exceptions"] = [
            {"line": 0, "code": "no_budget", "message": "No approved budget."},
            {"line": 1, "code": "no_budget", "message": "No approved budget."},
            {"line": 0, "code": "duplicate", "message": "Same reference."},
            {"line": 1, "code": "duplicate", "message": "Same reference."},
            {"line": 1, "code": "quantity", "message": "Too many."},
        ]
        rows = explanation_rows(run(case)["finance-invoices"]["tree"], "INV-1")
        self.assertEqual([row[1] for row in rows], ["Whole invoice", "Whole invoice", "Line 2"])

    def test_mixed_whole_invoice_and_numbered_lines_show_both(self) -> None:
        case = json.loads(json.dumps(CASE))
        inv = case["finance"]["invoices"][0]
        inv["exceptions"] = [
            {"line": None, "code": "no_milestone", "message": "Milestone."},
            {"line": 0, "code": "no_milestone", "message": "Milestone."},
        ]
        rows = explanation_rows(run(case)["finance-invoices"]["tree"], "INV-1")
        self.assertEqual(rows[0][1], "Whole invoice and line 1")

    def test_invoice_with_no_lines_is_not_checked(self) -> None:
        case = json.loads(json.dumps(CASE))
        inv = case["finance"]["invoices"][0]
        inv["lines"] = []
        inv["exceptions"] = []
        text = json.dumps(run(case)["finance-invoices"]["tree"])
        self.assertIn("The invoice has no lines, so it is not checked.", text)
        self.assertNotIn("No exception found by the match", text)

    def test_decider_names_match_core_finance_approvers(self) -> None:
        from zava_forward.core.controls import FINANCE_APPROVERS

        source = (WEB / "role-screens.js").read_text(encoding="utf-8")
        decider = next(
            line for line in source.splitlines() if line.startswith("const financeDecider")
        )
        for role in FINANCE_APPROVERS:
            self.assertIn(role, decider)

    def test_finance_decision_shows_plain_label_without_panels_loaded(self) -> None:
        case = json.loads(json.dumps(CASE))
        case["finance"]["invoices"][0]["disposition"] = "Keep on hold"
        case["finance"]["invoices"][0]["disposition_by"] = "Finance Lead"
        text = json.dumps(run(case)["finance-invoices"]["tree"])
        self.assertIn("Keep payment paused, recorded by Finance Lead", text)
        self.assertNotIn("Keep on hold", text)

    def test_clean_match_is_not_a_payment_decision(self) -> None:
        case = json.loads(json.dumps(CASE))
        case["finance"]["invoices"][0]["exceptions"] = []
        tree = run(case)["finance-invoices"]["tree"]
        self.assertEqual(explanation_rows(tree, "INV-1"), [])
        text = json.dumps(tree)
        self.assertNotIn("Exception explanations for INV-1", text)
        self.assertIn("No exception found by the match. This is not a payment decision", text)
        self.assertIn("does not confirm milestone acceptance", text)

    def test_tables_are_keyboard_reachable_and_labelled(self) -> None:
        for screen in run().values():
            nodes = walk(screen["tree"])
            regions = [n for n in nodes if (n["attrs"] or {}).get("role") == "region"]
            self.assertTrue(regions)
            for region in regions:
                self.assertEqual(region["attrs"]["tabindex"], 0)
                self.assertTrue(region["attrs"]["aria-label"])
            for node in nodes:
                tabindex = (node["attrs"] or {}).get("tabindex")
                if tabindex is not None:
                    self.assertLessEqual(int(str(tabindex)), 0, node)
                attrs = node["attrs"] or {}
                self.assertNotIn(node["tag"], ("button", "input", "select", "textarea", "a"))
                self.assertNotEqual(attrs.get("role"), "button", node)
                self.assertNotIn("onclick", attrs, node)
            for table in (n for n in nodes if n["tag"] == "table"):
                self.assertEqual(table["kids"][0]["tag"], "caption")


if __name__ == "__main__":
    unittest.main()
