"""Issue 83 / BG-010: unaccepted handoffs stay visible and show who must act and when.

The API cases use the real loopback server with synthetic data. The Node cases run the real
app.js handoff source with stubbed rendering helpers. Neither is human, assistive-technology or
live acceptance, and neither establishes an approved waiting time (OD-09).
"""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from test_handoff_api import HandoffApi as _Api

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
OVERDUE = "2020-01-01T00:00:00Z"

NODE = r"""
const fs = require("node:fs"), vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/app.js", "utf8");
const cut = (a, b) => src.slice(src.indexOf(a), src.indexOf(b));
const el = (tag, attrs, kids) => ({tag, attrs, kids, hidden: false,
  replaceChildren(...n) { this.kids = n; },
  text() { return this.kids.map(k => typeof k === "string" ? k : k.text()).join(" "); }});
const h = (tag, attrs, ...kids) => el(tag, attrs || {}, kids.flat().filter(k => k != null && k !== false));
const base = {case_id: "ZF-1", resident: "Pat Test", address: "1 Test Road", status: "Sent",
  state: "Offered", accountable_owner: "Sam Example", proposed_receiver: "Rae Other",
  destination: "Resident Liaison Officer", to_name: "Rae Other", to_role: "Resident Liaison Officer",
  offered_at: "2026-11-10T09:00:00+00:00", due_at: null, to_code: "RLO-02"};
const rows = {
  fresh: [{...base, due_at: "2999-01-01T00:00:00+00:00"}],
  overdue: [{...base, due_at: "2020-01-01T00:00:00+00:00"}],
  escalated: [{...base, state: "Escalated", status: "Escalated", escalation_owner: "Pam Lead"}],
};
const out = {};
(async () => {
  for (const [name, result] of Object.entries(rows)) {
    const ctx = vm.createContext({h, api: () => Promise.resolve(result),
      me: {user: {code: "RLO-01"}}, encodeURIComponent, Date, Number, Math});
    vm.runInContext(cut("const MANAGER_TARGET", "let briefingBox") + "\nthis.p = pendingHandoffs;", ctx);
    const box = ctx.p();
    await new Promise(r => setTimeout(r, 0));
    out[name] = box.text();
  }
  const wait = cut("const WAITING_READ_ERROR", "async function listView");
  const wr = (over) => ({case_id: "ZF-1", status: "Sent", age_hours: 30, due_at: "2020-01-01T00:00:00+00:00",
    chase_owner: "Sam Example", proposed_receiver: "Rae Other", escalated: false, needs_escalation: true,
    reasons: ["Handoff due time has passed"], approved_limit_hours: null, as_of: "2026-11-11T09:00:00+00:00", ...over});
  for (const [name, row] of Object.entries({wOverdue: wr({}), wEscalated: wr({escalated: true, needs_escalation: false})})) {
    let shown = [];
    const ctx = vm.createContext({h, api: () => Promise.resolve([row]), show: (...n) => { shown = n.flat(); },
      queueHref: () => "#/", encodeURIComponent});
    vm.runInContext(wait + "\nthis.v = handoffWaitingView;", ctx);
    await ctx.v();
    out[name] = shown.map(n => n.text()).join(" ");
  }
  console.log(JSON.stringify(out));
})();
"""  # noqa: E501

FORBIDDEN = ("payload", "endpoint", "json", "null", "undefined", "sla", "bg-010", "od-09 is")


class HandoffEscalationApi(unittest.TestCase):
    setUp: Any = _Api.setUp
    make_store: Any = _Api.make_store
    shutdown: Any = _Api.shutdown
    call: Any = _Api.call
    post: Any = _Api.post

    def test_overdue_unaccepted_handoff_is_projected_and_stays_pinned_until_accepted(self) -> None:
        self.assertEqual(
            self.post("sam", "offer-handoff", dict(to="rae@example.test", due_at=OVERDUE))[0], 200
        )
        for actor in ("sam", "rae", "pam"):
            _, rows = self.call(actor, "/api/handoffs/unaccepted")
            (row,) = rows
            self.assertTrue(row["needs_escalation"])
            self.assertFalse(row["escalated"])
            self.assertEqual(row["reasons"], ["Handoff due time has passed"])
            self.assertEqual(row["proposed_receiver"], "Rae Other")
            self.assertEqual(row["chase_owner"], "Sam Example")
        _, mine = self.call("rae", "/api/handoffs")
        self.assertEqual(mine[0]["destination"], "Resident Liaison Officer")
        self.assertEqual(mine[0]["due_at"][:10], "2020-01-01")

    def test_manual_escalation_keeps_it_visible_and_names_the_target(self) -> None:
        self.post("sam", "offer-handoff", dict(to="rae@example.test", due_at=OVERDUE))
        code, result = self.post(
            "sam", "escalate-handoff", dict(to="pam@example.test", reason="Chase overdue")
        )
        self.assertEqual(code, 200, result)
        _, (row,) = self.call("pam", "/api/handoffs/unaccepted")
        self.assertTrue(row["escalated"])
        self.assertFalse(row["needs_escalation"])
        _, (mine,) = self.call("rae", "/api/handoffs")
        self.assertEqual((mine["state"], mine["escalation_owner"]), ("Escalated", "Pam Lead"))
        self.post("rae", "accept-handoff")
        self.assertEqual(self.call("pam", "/api/handoffs/unaccepted")[1], [])


class HandoffEscalationDom(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        done = subprocess.run(
            ["node", "-e", NODE, str(WEB)], capture_output=True, text=True, timeout=60, check=False
        )
        if done.returncode:
            raise AssertionError(done.stderr)
        cls.out = json.loads(done.stdout)

    def test_unaccepted_handoff_says_action_needed_with_wait_due_and_receiver(self) -> None:
        text = self.out["fresh"]
        for phrase in (
            "State: Action needed.",
            "Waiting",
            "Rae Other (Resident Liaison Officer)",
            "Due: 2999-01-01",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("(overdue)", text)
        self.assertNotIn("Escalation target", text)

    def test_overdue_handoff_names_overdue_and_escalation_target_in_words(self) -> None:
        text = self.out["overdue"]
        self.assertIn("State: Action needed.", text)
        self.assertIn("(overdue)", text)
        self.assertIn(
            "Escalation target: a Retrofit Programme Manager or Programme Support Officer", text
        )

    def test_escalated_handoff_says_escalated_unaccepted_and_names_who(self) -> None:
        text = self.out["escalated"]
        self.assertIn("State: Escalated: unaccepted handoff.", text)
        self.assertIn("Escalated to Pam Lead.", text)

    def test_waiting_table_has_a_text_state_column(self) -> None:
        self.assertIn("State", self.out["wOverdue"])
        self.assertIn("Action needed", self.out["wOverdue"])
        self.assertIn("Needs escalation.", self.out["wOverdue"])
        self.assertIn("Escalated: unaccepted handoff", self.out["wEscalated"])
        self.assertIn("Already escalated.", self.out["wEscalated"])

    def test_new_text_avoids_internal_terms(self) -> None:
        lowered = " ".join(self.out[k] for k in ("fresh", "overdue", "escalated")).lower()
        for term in FORBIDDEN[:5]:
            self.assertNotIn(term, lowered)


if __name__ == "__main__":
    unittest.main()
