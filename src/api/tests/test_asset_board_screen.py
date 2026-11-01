"""Asset and board reader screen shows unknowns and offers no approval."""

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
const side = (value, id, date) => ({value, source_id: id, date, version: "1",
  validation_state: "Unvalidated"});
const owner = {name: "Query Owner", role: "Retrofit Programme Manager"};
const c = {id: "C-1", stock_reconciliation: [
  {id: "SQ-1", field: "epc", query_owner: owner,
    left: side("D", "S-A", process.argv[3] || "2020-01-01"), right: side("C", "S-B", "2026-01-01")}
], stock_reconciliation_events: []};
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
  api: async (path) => path.startsWith("/api/ai/report")
    ? JSON.parse(process.argv[2])
    : path.startsWith("/api/asset/stock-queue")
      ? (process.argv[4] === "fail" ? Promise.reject(new Error("x")) : {items: [
        {id: "C-9", address: "1 Test Rd", town: "Testville", open_queries: 2,
          fields: ["epc", "built"],
          oldest_source_date: "2020-01-01", owners: ["Query Owner"]},
        {id: "C-8", address: "2 Test Rd", town: "Testville", open_queries: 1, fields: ["type"],
          oldest_source_date: "2021-01-01", owners: []}]})
      : {total: 7, items: []},
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('asset-board');", context);
(async () => {
  const s = context.__s;
  const extra = await s.load(c);
  console.log(JSON.stringify({roles: s.roles, tree: await s.render(c, extra),
    empty: await s.render({id: "C-2"}, extra)}));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""


def run(
    report: dict[str, object], left_date: str = "2020-01-01", queue: str = "ok"
) -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(report), left_date, queue],
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


def walk(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


class AssetBoardScreen(unittest.TestCase):
    def test_unknowns_owner_age_and_no_controls(self) -> None:
        out = run(
            {
                "consumption": {
                    "quality_status": "Unknown",
                    "token_cost": "123",
                    "tokens_per_proposal": {"mean": "9999"},
                }
            }
        )
        text = json.dumps(out["tree"])
        self.assertEqual(out["roles"], ["Retrofit Programme Manager", "Programme Support Officer"])
        self.assertIn("Query Owner", text)
        self.assertIn("days old", text)
        self.assertIn("Unresolved", text)
        self.assertIn("Eligibility", text)
        self.assertIn("no investment approval", text.lower())
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(out["tree"]))
        self.assertIn("Cases permitted to your role", text)
        self.assertIn("Portfolio scope", text)
        self.assertNotIn("9999", text)
        self.assertNotIn("123", text)

    def test_accepted_iso_forms_show_age(self) -> None:
        for accepted in ("20200101", "2020-W01-3", "2020W013", "2020-W01"):
            with self.subTest(accepted=accepted):
                text = json.dumps(run({}, accepted)["tree"])
                self.assertIn("S-A v1, ", text)
                self.assertRegex(text, r"S-A v1, \d+ days old")

    def test_cost_unknown_without_pass_and_shown_with_evidence_class(self) -> None:
        unknown = json.dumps(
            run({"consumption": {"quality_status": "Fail", "quality_qualified_cost": "1.20"}})[
                "tree"
            ]
        )
        self.assertNotIn("1.20", unknown)
        self.assertIn("Overall AI cost per accepted outcome", unknown)
        shown = json.dumps(
            run(
                {
                    "consumption": {
                        "quality_status": "Pass",
                        "quality_qualified_cost": "1.20",
                        "currency": "GBP",
                        "evidence_label": "synthetic",
                        "coverage": "complete",
                        "denominator": "accepted outputs",
                        "period": {"start": "P1", "end": "P2", "as_of": "A1"},
                    }
                }
            )["tree"]
        )
        self.assertIn("1.20 GBP", shown)
        self.assertIn("synthetic", shown)
        self.assertIn("component only", shown)
        self.assertIn("Ledger-wide", shown)
        self.assertIn("P1 to P2, as of A1", shown)
        self.assertIn("accepted outputs", shown)
        self.assertIn("S-A v1", shown)

    def test_missing_report_and_no_conflicts_stay_unknown(self) -> None:
        out = run({})
        text = json.dumps(out["empty"])
        self.assertIn("Unassigned", text)
        self.assertIn("No records supplied", text)
        self.assertIn("Unknown", text)

    def test_cross_home_queue_is_read_only_text_and_keyboard_reachable(self) -> None:
        tree = run({})["tree"]
        text = json.dumps(tree)
        self.assertIn("Stock conflict queue across homes", text)
        self.assertIn("C-9, 1 Test Rd, Testville", text)
        self.assertIn("epc, built", text)
        self.assertIn("It is not an investment priority", text)
        self.assertIn("Unassigned", text)
        self.assertLess(text.index("C-9, 1 Test Rd"), text.index("C-8, 2 Test Rd"))
        regions = [n for n in walk(tree) if n.get("attrs", {}).get("role") == "region"]
        self.assertTrue(regions)
        for region in regions:
            self.assertEqual(region["attrs"]["tabindex"], 0)
            self.assertTrue(region["attrs"]["aria-label"])
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))

    def test_queue_failure_is_unknown_not_empty(self) -> None:
        text = json.dumps(run({}, queue="fail")["tree"])
        self.assertIn("The cross-home queue could not be loaded.", text)
        self.assertIn("Cannot confirm readiness", text)


if __name__ == "__main__":
    unittest.main()
