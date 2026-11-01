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
const context = vm.createContext({
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
  const form = find(overview, "form")[0];
  const select = find(form, "select")[0];
  select.value = "returned";
  form.attrs.onsubmit({preventDefault() {}});
  const queueRows = () => find(overview, "tbody")[0].kids.length;
  const filteredRows = queueRows();
  const buttons = find(form, "button");
  const reset = buttons.find(b => b.attrs.type === "button");
  reset.attrs.onclick();
  const resetRows = queueRows();
  const gates = (c, orders) => s.render(c, {orders});
  const done = [{id: "WO-1", state: "Appointed", appointment_control: {status: "Committed", missing: []}}];
  console.log(JSON.stringify({roles: s.roles, before, filteredRows, resetRows, defaultRows: 2,
    blocked: gates({id: "C-9", work: {blockers: [
      {step: "Final checks: funding", reason: "Funding has not been confirmed.", owner: "Owen", next_action: "Check funding"},
      {step: "Final checks: resident decision", reason: "No decision.", owner: "Rae", next_action: "Ask resident"}]},
      technical: null, quality: [{state: "Returned", measure: "Loft"}]}),
    clear: gates({id: "C-8", work: {blockers: []}, technical: {},
      measures: "Loft", quality: [{state: "Accepted", measure: "Loft"}], funding_ok: true, finance: {budget: {status: "Approved"}}}, done),
    legacyOnly: gates({id: "C-4", work: {blockers: []}, technical: {}, appointments: [{outcome: "Booked", date: "2026-11-02"}],
      measures: "Loft", quality: [{state: "Accepted", measure: "Loft"}], finance: {budget: {status: "Approved"}}}, []),
    held: gates({id: "C-3", work: {blockers: []}, technical: {}, funding_ok: true, measures: "Loft",
      quality: [{state: "Accepted", measure: "Loft"}], finance: {budget: {status: "Approved"}, invoices: [
        {id: "INV-1", hold: {name: "Fin Officer", reason: "Query"}, exceptions: []},
        {id: "INV-2", hold: null, disposition: null, exceptions: [{}]},
        {id: "INV-3", hold: null, disposition: "Accept for payment", exceptions: [{}]}]}}, done),
    proposed: gates({id: "C-2", work: {blockers: []}, technical: {}, funding_ok: true, measures: "Loft",
      quality: [{state: "Accepted", measure: "Loft"}], finance: {budget: {status: "Proposed"}}}, done),
    submitted: gates({id: "C-7", work: {blockers: []}, measures: "Loft", quality: [{state: "Submitted", measure: "Loft"}]}),
    fixed: gates({id: "C-6", work: {blockers: []}, measures: "Loft", quality: [{state: "Fixed, awaiting reinspection", measure: "Loft"}]}),
    partial: gates({id: "C-5", work: {blockers: []}, measures: "Loft, Heat pump",
      quality: [{state: "Accepted", measure: "Loft"}, {state: "Superseded", measure: "Heat pump"}]})}));
})().catch(e => {console.error(e); process.exitCode = 1;});
"""  # noqa: E501


def run(role: str = "Retrofit Programme Manager", coordinator: str = "up") -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), role, coordinator],
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

    def test_delivery_and_finance_use_current_orders_holds_and_budget_status(self) -> None:
        out = run()
        for key in ("legacyOnly",):
            node = json.dumps(out[key])
            self.assertIn("No active work order is recorded", node[node.index('"Delivery"') :])
        held = json.dumps(out["held"])
        finance = held[held.index('"Finance"') :]
        self.assertIn("INV-1 is on payment hold", finance)
        self.assertIn("Fin Officer", finance)
        self.assertIn("INV-2 has 1 unresolved match exception", finance)
        self.assertNotIn("INV-3", finance)
        proposed = json.dumps(out["proposed"])
        self.assertIn("Proposed, not Approved", proposed[proposed.index('"Finance"') :])

    def test_funnel_unknown_when_coordinator_unavailable(self) -> None:
        self.assertIn("Unknown", str(run(coordinator="down")["before"]))

    def test_missing_gates_are_blocked_in_text_and_no_role_switcher(self) -> None:
        out = run()
        blocked = json.dumps(out["blocked"])
        for gate in ("Technical", "Resident", "Delivery", "Quality", "Finance"):
            self.assertIn(gate, blocked)
        self.assertIn("Blocked: evidence missing", blocked)
        self.assertIn("Funding has not been confirmed.", blocked)
        self.assertIn("5 of 5 gates are blocked", blocked)
        clear = json.dumps(out["clear"])
        self.assertIn("No recorded blocker", clear)
        self.assertIn("not a pass", clear)
        self.assertNotIn("Blocked", clear)
        for node in (out["blocked"], out["clear"]):
            for control in ("button", "form", "input", "select", "textarea"):
                self.assertNotIn(control, tags(node))


if __name__ == "__main__":
    unittest.main()
