"""Programme queue screen shows returned work, separate responsibilities and blocked gates."""

import json
import subprocess
import unittest
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const role = process.argv[2];
const returned = {id: "C-1", address: "1 Test Street", work: {owner: "Owen Owner", queues: [],
  returned: {reason: "Missing survey", sender: "Quinn Sender"}, handoff: null}};
const pending = {id: "C-2", address: "2 Test Street", work: {owner: "Owen Owner", queues: ["unowned"],
  resident_update_owner: "Una Updater", returned: null, handoff: {state: "Offered", sender: "Sam Sender", proposed_receiver: "Rae Receiver",
  chase_owner: "Sam Sender", resident_update_owner: "Una Updater"}}};
const plain = {id: "C-3", address: "3 Test Street", work: {owner: "Owen Owner", queues: [], returned: null, handoff: null}};
const hist = [];
const loc = {hash: process.argv[4] ? "#/screens?screen=programme-queue&scope=" + process.argv[4] : "#/screens?screen=programme-queue"};
const context = vm.createContext({
  location: loc, history: {replaceState: (a, b, url) => { hist.push(url); loc.hash = url; }},
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role}},
  api: async (path) => path.startsWith("/api/coordinator")
    ? (!path.includes("view=all") ? Promise.reject(new Error("scope")) : process.argv[3] === "down" ? Promise.reject(new Error("down"))
      : {as_of: "2026-10-01", audit_integrity: "Intact",
        funnel: [{stage: "Funding check", entries: 3, exits: 2, returns: 1, reopens: 0, denominator: 9}]})
    : {total: 3, items: [returned, pending, plain]},
  h: (tag, attrs, ...kids) => {
    const node = {tag, attrs, kids: kids.flat(Infinity).filter(
      kid => kid !== false && kid !== null && kid !== undefined)};
    Object.defineProperty(node, "replaceChildren", {value: (...k) => { node.kids = k; }});
    Object.defineProperty(node, "textContent", {set: (v) => { node.kids = [v]; }});
    return node;
  }
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('programme-queue');", context);
(async () => {
  const s = context.__s;
  const overview = await s.overview(new AbortController().signal);
  const find = (n, tag, out = []) => { if (n && typeof n === "object") { if (n.tag === tag) out.push(n); (n.kids || []).forEach(k => find(k, tag, out)); } return out; };
  const before = JSON.stringify(overview);
  const initialScope = find(overview, "select")[0].value;
  const form = find(overview, "form")[0];
  const select = find(form, "select")[0];
  select.value = "returned";
  form.attrs.onsubmit({preventDefault() {}});
  const queueRows = () => find(overview, "tbody")[0].kids.length;
  const filteredRows = queueRows();
  const keptHash = loc.hash;
  const buttons = find(form, "button");
  const reset = buttons.find(b => b.attrs.type === "button");
  reset.attrs.onclick();
  const resetRows = queueRows();
  const gates = (c, orders) => s.render(c, {orders});
  const bound = {measure: "Loft", context_revision: 2};
  const done = [{id: "WO-1", state: "Appointed", appointment_control: {status: "Committed", missing: []},
    versions: [{resident_bindings: [bound]}]}];
  const stale = [{id: "WO-2", state: "Appointed", appointment_control: {status: "Committed", missing: []},
    versions: [{resident_bindings: [{measure: "Loft", context_revision: 1}]}]}];
  const decisions = [{measure: "Loft", context: {revision: 2}}];
  const accepted = {state: "Accepted", measure: "Loft", resident_binding: bound};
  console.log(JSON.stringify({initialScope, keptHash, resetHash: loc.hash, roles: s.roles, before, filteredRows, resetRows, defaultRows: 2,
    blocked: gates({id: "C-9", work: {blockers: [
      {step: "Final checks: funding", reason: "Funding has not been confirmed.", owner: "Owen", next_action: "Check funding"},
      {step: "Technical review", reason: "Survey missing.", owner: "Unknown", responsible_role: "Retrofit Coordinator", next_action: "Complete survey"},
      {step: "Stock review", reason: "Stock unchecked.", owner: "Unknown", responsible_role: "Quality Inspector", next_action: "Check stock"},
      {step: "Final checks: resident decision", reason: "No decision.", owner: "Rae", next_action: "Ask resident"}]},
      technical: null, quality: [{state: "Returned", measure: "Loft", defect: {reason: "Gaps in insulation", owner: "Ivy Installer"}}]}),
    clear: gates({id: "C-8", work: {blockers: []}, technical: {},
      measures: "Loft", measure_decisions: decisions, quality: [accepted], funding_ok: true, finance: {budget: {status: "Approved"}}}, done),
    legacyOnly: gates({id: "C-4", work: {blockers: []}, technical: {}, appointments: [{outcome: "Booked", date: "2026-11-02"}],
      measures: "Loft", quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}], finance: {budget: {status: "Approved"}}}, []),
    held: gates({id: "C-3", work: {blockers: []}, technical: {}, funding_ok: true, measures: "Loft",
      quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}], finance: {budget: {status: "Approved"}, invoices: [
        {id: "INV-1", hold: {name: "Fin Officer", reason: "Query"}, exceptions: []},
        {id: "INV-2", hold: null, disposition: null, exceptions: [{}]},
        {id: "INV-3", hold: null, disposition: "Accept for payment", exceptions: [{}]},
        {id: "INV-4", hold: null, disposition: "Keep on hold", disposition_by: "Fiona Finance", exceptions: []}]}}, done),
    proposed: gates({id: "C-2", work: {blockers: []}, technical: {}, funding_ok: true, measures: "Loft",
      quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}], finance: {budget: {status: "Proposed"}}}, done),
    unmatched: gates({id: "C-10", work: {blockers: []}, technical: {}, measures: "Loft",
      quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}], finance: {budget: {status: "Approved"}, invoices: [
        {id: "INV-9", status: "Received", hold: null, disposition: null, exceptions: []}]}}, done),
    withheld: gates({id: "C-11", work: {blockers: []}, technical: {}, funding_ok: true, measures: "Loft",
      quality: [{state: "Accepted", measure: "Loft", resident_binding: bound}]}, done),
    staleQuality: gates({id: "C-12", work: {blockers: []}, technical: {}, measures: "Loft", measure_decisions: [{measure: "Loft", context: {revision: 3}}],
      quality: [accepted], finance: {budget: {status: "Approved"}}}, done),
    unboundQuality: gates({id: "C-13", work: {blockers: []}, technical: {}, measures: "Loft", measure_decisions: decisions,
      quality: [{state: "Handed over", measure: "Loft"}], finance: {budget: {status: "Approved"}}}, done),
    staleOrder: gates({id: "C-14", work: {blockers: []}, technical: {}, measures: "Loft", measure_decisions: decisions,
      quality: [accepted], finance: {budget: {status: "Approved"}}}, stale),
    completedOrder: gates({id: "C-15", work: {blockers: []}, technical: {}, measures: "Loft", measure_decisions: decisions,
      quality: [accepted], finance: {budget: {status: "Approved"}}}, stale.map((w) => ({...w, state: "Completed"}))),
    overCommit: gates({id: "C-16", work: {blockers: []}, technical: {}, funding_ok: true, measures: "Loft",
      quality: [accepted], finance: {budget: {status: "Approved", amount: 100}, commitments: [{id: "COM-1", amount: 100}], invoices: [
        {id: "INV-A", status: "Matched", commitment: "COM-1", disposition: "Accept for payment", exceptions: [], lines: [{amount: 60}]},
        {id: "INV-B", status: "Matched", commitment: "COM-1", disposition: null, exceptions: [], lines: [{amount: 60}]}]}}, done),
    submitted: gates({id: "C-7", work: {blockers: []}, measures: "Loft", quality: [{state: "Submitted", measure: "Loft"}]}),
    fixed: gates({id: "C-6", work: {blockers: []}, measures: "Loft", quality: [{state: "Fixed, awaiting reinspection", measure: "Loft"}]}),
    partial: gates({id: "C-5", work: {blockers: []}, measures: "Loft, Heat pump",
      quality: [{state: "Accepted", measure: "Loft"}, {state: "Superseded", measure: "Heat pump"}]})}));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""  # noqa: E501


def run(
    role: str = "Retrofit Programme Manager", coordinator: str = "up", scope: str = ""
) -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), role, coordinator, scope],
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


class ProgrammeScreen(unittest.TestCase):
    def test_roles_exclude_other_roles(self) -> None:
        roles = list(run()["roles"])  # type: ignore[call-overload]
        self.assertIn("Retrofit Programme Manager", roles)
        self.assertIn("Retrofit Coordinator", roles)
        self.assertNotIn("Resident Liaison Officer", roles)

    def test_queue_shows_return_sender_owner_receiver_and_separate_responsibilities(self) -> None:
        before = str(run()["before"])
        for expected in (
            "Missing survey",
            "Quinn Sender",
            "Owen Owner",
            "Rae Receiver",
            "Una Updater",
            "Chase owner",
            "Resident-update owner",
            "not a confirmed owner",
        ):
            self.assertIn(expected, before)
        self.assertNotIn("3 Test Street", before)
        self.assertIn("Funding check", before)

    def test_filter_and_reset_change_view_only(self) -> None:
        out = run()
        self.assertEqual(out["filteredRows"], 1)
        self.assertEqual(out["resetRows"], 2)
        self.assertIn("no record is changed", str(out["before"]))

    def test_quality_gate_stays_blocked_until_every_measure_is_accepted(self) -> None:
        out = run()
        self.assertIn("Offered", str(out["before"]))
        self.assertNotIn("Not returned. Pending handoff", str(out["before"]))
        for key, text in (
            ("submitted", "Submitted"),
            ("fixed", "Fixed, awaiting reinspection"),
            ("partial", "Heat pump: no quality check recorded"),
        ):
            node = json.dumps(out[key])
            row = node[node.index('"Quality"') :]
            self.assertIn(text, row)
            self.assertIn("Blocked", row)

    def test_applied_scope_persists_in_route_until_reset(self) -> None:
        out = run()
        self.assertIn("scope=returned", str(out["keptHash"]))
        self.assertNotIn("scope=", str(out["resetHash"]))
        self.assertEqual(run(scope="blocked")["initialScope"], "blocked")
        self.assertEqual(run(scope="bogus")["initialScope"], "default")

    def test_stale_resident_scope_blocks_quality_and_delivery(self) -> None:
        out = run()
        for key, gate, text in (
            ("staleQuality", '"Quality"', "not bound to the current resident scope"),
            ("unboundQuality", '"Quality"', "not bound to the current resident scope"),
            ("staleOrder", '"Delivery"', "resident scope bindings are missing or not current"),
        ):
            node = json.dumps(out[key])
            row = node[node.index(gate) :]
            self.assertIn(text, row)
            self.assertIn("Blocked", row)
        self.assertIn("Reissue the work order", json.dumps(out["staleOrder"]))
        completed = json.dumps(out["completedOrder"])
        self.assertIn("Correct the completed work order", completed)
        self.assertNotIn("Reissue the work order", completed)

    def test_finance_projects_match_against_accepted_invoices(self) -> None:
        text = json.dumps(run()["overCommit"])
        self.assertIn("INV-B", text)
        self.assertIn("over the commitment and over the approved budget", text)

    def test_delivery_and_finance_use_current_orders_holds_and_budget_status(self) -> None:
        out = run()
        for key in ("legacyOnly",):
            node = json.dumps(out[key])
            self.assertIn("No active work order is recorded", node[node.index('"Delivery"') :])
        held = json.dumps(out["held"])
        finance = held[held.index('"Finance"') :]
        self.assertIn("INV-1 is on payment pause", finance)
        self.assertIn("Fin Officer", finance)
        self.assertIn("INV-2 has 1 unresolved match exception", finance)
        self.assertNotIn("INV-3", finance)
        proposed = json.dumps(out["proposed"])
        self.assertIn("Proposed, not Approved", proposed[proposed.index('"Finance"') :])
        unmatched = json.dumps(out["unmatched"])
        self.assertIn("not been matched", unmatched[unmatched.index('"Finance"') :])
        withheld = json.dumps(out["withheld"])
        self.assertIn("Blocked: evidence missing", withheld[withheld.index('"Finance"') :])

    def test_blocker_roles_returned_quality_and_kept_hold_are_preserved(self) -> None:
        out = run()
        blocked = json.dumps(out["blocked"])
        self.assertIn("Retrofit Coordinator", blocked)
        self.assertIn("Quality Inspector", blocked)
        self.assertIn("Complete survey", blocked)
        self.assertIn("Check stock", blocked)
        quality = blocked[blocked.index('"Quality"') :]
        self.assertIn("Gaps in insulation", quality)
        self.assertIn("Ivy Installer", quality)
        self.assertIn("fixed and reinspected", quality)
        finance = json.dumps(out["held"])
        finance = finance[finance.index('"Finance"') :]
        self.assertIn("INV-4 has a Finance decision to keep the pause", finance)
        self.assertIn("Fiona Finance", finance)

    def test_funnel_unknown_when_coordinator_unavailable(self) -> None:
        self.assertIn("Unknown", str(run(coordinator="down")["before"]))

    def test_missing_gates_are_blocked_in_text_and_no_role_switcher(self) -> None:
        out = run()
        blocked = json.dumps(out["blocked"])
        for gate in ("Technical", "Resident", "Delivery", "Quality", "Finance"):
            self.assertIn(gate, blocked)
        self.assertIn("Blocked: evidence missing", blocked)
        self.assertIn("Funding has not been confirmed.", blocked)
        self.assertIn("5 of 5 steps are blocked", blocked)
        clear = json.dumps(out["clear"])
        self.assertIn("No recorded blocker", clear)
        self.assertIn("not a pass", clear)
        self.assertNotIn("Blocked", clear)
        for node in (out["blocked"], out["clear"]):
            for control in ("button", "form", "input", "select", "textarea"):
                self.assertNotIn(control, tags(node))


if __name__ == "__main__":
    unittest.main()
