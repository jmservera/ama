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
    report: dict[str, object] | None, left_date: str = "2020-01-01", queue: str = "ok"
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

    def test_missing_evidence_class_is_unknown_and_hides_cost(self) -> None:
        consumption = {
            "quality_status": "Pass",
            "quality_qualified_cost": "1.20",
            "currency": "GBP",
            "coverage": "complete",
        }
        tree = run({"consumption": consumption})["tree"]
        self.assertNotIn("1.20", json.dumps(tree))
        nodes = walk(tree)
        index = next(
            i
            for i, n in enumerate(nodes)
            if n.get("tag") == "dt" and n["kids"] == ["Evidence class"]
        )
        after = [n for n in nodes[index + 1 :] if n.get("tag") == "dd"][0]
        self.assertEqual(after["kids"], ["Unknown"])

    def test_ai_unavailable_is_stated_and_cost_stays_unknown(self) -> None:
        down = json.dumps(run(None)["tree"])
        self.assertIn("Unavailable. The AI report could not be loaded", down)
        self.assertIn("Nothing on this view needs AI", down)
        self.assertIn("S-A v1", down)
        up = json.dumps(run({"consumption": {"quality_status": "Fail"}})["tree"])
        self.assertIn('"Loaded"', up)
        self.assertNotIn("could not be loaded", up)
        empty = json.dumps(run({})["tree"])
        self.assertNotIn('"Loaded"', empty)
        self.assertIn("could not be loaded", empty)

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

    def test_phase_gate_table_is_unknown_with_owners_and_no_approval(self) -> None:
        tree = run({})["tree"]
        text = json.dumps(tree)
        self.assertIn("Phase checks and benefits", text)
        self.assertIn("Pause or exit choice for the next tranche", text)
        self.assertIn("Board or delegated owner", text)
        self.assertIn("does not pass a check", text)
        table = next(
            n
            for n in walk(tree)
            if n.get("tag") == "table" and "Phase checks and benefits" in json.dumps(n)
        )
        rows = [n for n in walk(table) if n.get("tag") == "tr"][1:]
        self.assertEqual(len(rows), 6)
        for row in rows:
            cells = [json.dumps(k) for k in row["kids"]]
            self.assertIn("Unknown", cells[1])
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))

    def test_structure_uses_shared_components_and_text_states(self) -> None:
        reports: list[dict[str, object] | None] = [
            None,
            {},
            {"consumption": {"quality_status": "Fail"}},
        ]
        for report in reports:
            tree = run(report)["tree"]
            nodes = walk(tree)
            sections = [n for n in nodes if n.get("tag") == "section"]
            self.assertTrue(sections)
            for section in sections:
                self.assertEqual(section["attrs"]["class"], "card screen-record")
                self.assertEqual(section["kids"][0]["tag"], "h2")
            self.assertNotIn("h1", tags(tree))
            self.assertNotIn("h3", tags(tree))
            tables = [n for n in nodes if n.get("tag") == "table"]
            self.assertGreaterEqual(len(tables), 4)
            for table in tables:
                self.assertEqual(table["kids"][0]["tag"], "caption")
                head = next(n for n in walk(table) if n.get("tag") == "thead")
                for th in (n for n in walk(head) if n.get("tag") == "th"):
                    self.assertEqual(th["attrs"]["scope"], "col")
            blocked = [n for n in nodes if n.get("attrs", {}).get("class") == "blocked"]
            self.assertTrue(blocked)
            for item in blocked:
                self.assertIn("Cannot confirm readiness", json.dumps(item))
            for node in nodes:
                attrs = node.get("attrs", {})
                self.assertNotIn("onclick", attrs)
                self.assertNotIn("role-switch", json.dumps(attrs))

    def test_screen_source_has_no_role_simulator(self) -> None:
        source = (WEB / "role-screens.js").read_text(encoding="utf-8")
        start = source.index('id: "asset-board"')
        block = source[start : source.index("registerRoleScreen", start)]
        for banned in ("simulat", "impersonat", "switchRole", "viewAs", "role-switch"):
            self.assertNotIn(banned, block.lower() if banned.islower() else block)
        self.assertNotIn("me.user.role =", block)

    def test_queue_failure_is_unknown_not_empty(self) -> None:
        text = json.dumps(run({}, queue="fail")["tree"])
        self.assertIn("The cross-home queue could not be loaded.", text)
        self.assertIn("Cannot confirm readiness", text)

    def test_usage_panel_shows_counts_alerts_and_unknown_not_zero(self) -> None:
        report: dict[str, object] = {
            "consumption": {
                "calls": 12,
                "retries": 0,
                "failures": 2,
                "unknown_liabilities": 1,
                "accepted_proposals": 3,
                "tokens_per_proposal": {"measured": 4, "missing": 1, "mean": "7777"},
                "token_cost": "555",
                "owned_alerts": [
                    {"owner": "Finance owner", "reason": "token-budget-limit", "route": "finance"}
                ],
                "other_tca_components": {"review_time": "Unknown", "licences": "2.50"},
                "currency": "GBP",
                "reconciliation": "unreconciled",
                "total_cost_of_ai": "Unknown",
            }
        }
        tree = run(report)["tree"]
        text = json.dumps(tree)
        self.assertIn("Ledger-wide AI usage, alerts and cost components", text)
        self.assertIn("Finance owner", text)
        self.assertIn("token-budget-limit", text)
        self.assertIn("2.50 GBP", text)
        self.assertIn("OD-51 is open", text)
        self.assertIn("Total Cost of AI", text)
        self.assertNotIn("7777", text)
        self.assertNotIn("555", text)
        cells = [n["kids"][0] for n in walk(tree) if n.get("tag") in ("dt", "dd")]
        pairs = dict(zip(cells[0::2], cells[1::2], strict=False))
        self.assertEqual(pairs["Proposals with at least one call"], "5")
        self.assertEqual(pairs["Human-accepted proposals"], "3")
        self.assertEqual(pairs["Metered calls in the period (all capabilities)"], "12")
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))

    def test_capability_table_shows_counts_and_unknown_cost(self) -> None:
        rows = {
            "assessment": {
                "calls": 4,
                "proposals": 3,
                "accepted_proposals": 2,
                "total_tokens": 900,
                "tokens_per_accepted_proposal": "450",
            },
            "drafting": {"calls": 1},
        }
        tree = run({"consumption": {"by_capability": rows}})["tree"]
        text = json.dumps(tree)
        self.assertIn("Metered usage by AI capability", text)
        self.assertIn("assessment", text)
        self.assertIn("drafting", text)
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))

    def test_capability_rows_show_values_and_unknown_for_gaps(self) -> None:
        rows = {
            "assessment": {
                "calls": 4,
                "proposals": 3,
                "proposals_with_known_tokens": 2,
                "accepted_proposals": 2,
                "total_tokens": 900,
                "tokens_per_accepted_proposal": "450",
            },
            "drafting": {"calls": 1},
        }
        tree = run({"consumption": {"by_capability": rows}})["tree"]
        body = [n for n in walk(tree) if n.get("tag") == "tr"][-2:]
        first = [json.dumps(k) for k in body[0]["kids"]]
        sparse = [json.dumps(k) for k in body[1]["kids"]]
        self.assertTrue(
            first[1].find("4") >= 0
            and first[3].find("2") >= 0
            and first[5].find("900") >= 0
            and first[6].find("450") >= 0
        )
        self.assertEqual(sum("Unknown" in c for c in sparse), 5)

    def test_capability_breakdown_missing_or_wrong_shape_is_unknown(self) -> None:
        for value in ({}, {"by_capability": [{"capability": "x"}]}, {"by_capability": None}):
            text = json.dumps(run({"consumption": value})["tree"])
            self.assertIn("per-capability breakdown could not be read", text)

    def test_usage_panel_missing_figures_are_unknown_not_zero(self) -> None:
        text = json.dumps(run({"consumption": {"quality_status": "Fail"}})["tree"])
        cells = [
            n["kids"][0]
            for n in walk(run({"consumption": {}})["tree"])
            if n.get("tag") in ("dt", "dd")
        ]
        pairs = dict(zip(cells[0::2], cells[1::2], strict=False))
        for label in (
            "Metered calls in the period (all capabilities)",
            "Human-accepted proposals",
            "Proposals with at least one call",
        ):
            self.assertEqual(pairs[label], "Unknown")
        self.assertIn("Alerts could not be read", text)
        down = json.dumps(run(None)["tree"])
        self.assertIn("Unknown is not zero", down)


if __name__ == "__main__":
    unittest.main()
