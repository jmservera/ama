"""Variations and escalations reach a named owner and never act as a contract instruction (#132)."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

from dataset import supplied_appointment_fixture
from zava_forward.core import job_pack, projection

from test_procurement_api import ProcurementApiFixture

OWNER = "Pam Lead"
ROLE = "Retrofit Programme Manager"


ROUTE = "/api/workorders/WO-0001/"
WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"


class FieldworkVariationOwnerGuard(ProcurementApiFixture):
    def setUp(self) -> None:
        super().setUp()
        self.assertEqual(self.call(f"/api/packages/{self.pid}/capacity", self.capacity())[0], 200)
        self.assertEqual(self.call("/api/workorders", self.issue("ZF-3"))[0], 200)
        supplied_appointment_fixture(self.store, self.manager, "WO-0001", "2099-01-01")
        self.assertEqual(
            self.call(ROUTE + "appointment", dict(outcome="Booked", date="2099-01-01"))[0], 200
        )

    def view(self, actor: str = "sam") -> dict[str, Any]:
        code, out = self.call(ROUTE + "field-intake", actor=actor)
        self.assertEqual(code, 200, out)
        result: dict[str, Any] = out
        return result

    def restart(self) -> None:
        self.store.save()
        if self.sql:
            self.store.db.close()
        self.store = self.reopen_store()
        self.app.store = self.store

    def raise_it(self, actor: str = "sam", **over: Any) -> tuple[int, Any]:
        body: dict[str, Any] = dict(
            kind="variation",
            summary="Extra 20m2 of loft found",
            named_owner=OWNER,
            owner_role=ROLE,
        )
        body.update(over)
        return self.call(ROUTE + "field-escalate", body, actor)

    def test_routes_to_named_owner_with_non_instruction_stamp_and_audit(self) -> None:
        code, out = self.raise_it()
        self.assertEqual(code, 200, out)
        item = out["escalation"]
        self.assertEqual(item["owner"], dict(name=OWNER, role=ROLE))
        self.assertIs(item["acts_as_contract_instruction"], False)
        self.assertIs(item["contract_instruction"], False)
        self.assertIn("not a contract instruction", item["contract_notice"])
        self.restart()
        view = self.view()
        self.assertEqual(view["escalations"][0]["owner"]["name"], OWNER)
        self.assertIs(view["boundaries"]["acts_as_contract_instruction"], False)
        self.assertIs(view["escalation"]["acts_as_contract_instruction"], False)
        self.assertTrue(self.store.verify_audit())
        if self.sql:
            rows = self.store.db.execute(
                "SELECT detail FROM audit WHERE action = 'field_escalation_raised'"
            ).fetchall()
            self.assertEqual(len(rows), 1)
            self.assertIn("acts_as_contract_instruction=False", rows[0][0])

    def test_owner_is_required_and_must_be_a_matching_staff_member(self) -> None:
        for over in (
            dict(named_owner=""),
            dict(named_owner=None),
            dict(owner_role="Contractor"),
            dict(named_owner="Nobody Real"),
            dict(owner_role="Building Safety Liaison"),
            dict(kind="order"),
        ):
            code, out = self.raise_it(**over)
            self.assertEqual(code, 400, (over, out))
        self.assertEqual(self.view()["escalations"], [])

    def test_non_string_kind_or_summary_and_closed_or_withdrawn_are_refused(self) -> None:
        for over in (dict(kind=["variation"]), dict(summary=123), dict(summary=None)):
            code, out = self.raise_it(**over)
            self.assertEqual(code, 400, (over, out))
        self.store.cases["ZF-3"]["closed"] = True
        self.assertEqual(self.raise_it()[0], 400)
        self.store.cases["ZF-3"]["closed"] = False
        self.store._work_order("WO-0001")["state"] = "Withdrawn"
        self.assertEqual(self.raise_it()[0], 400)
        self.store._work_order("WO-0001")["state"] = "Appointed"
        self.assertEqual(self.raise_it()[0], 200)

    def test_free_text_is_redacted_without_a_recorded_need_and_notice_survives(self) -> None:
        text = "Extra 20m2 of loft found"
        self.assertEqual(self.raise_it()[0], 200)
        self.assertEqual(self.view("sam")["escalations"][0]["summary"], text)
        self.assertEqual(self.view("quil")["escalations"][0]["summary"], projection.NOTE_HELD)
        self.assertEqual(self.view("pam")["escalations"][0]["summary"], text)
        code, quil = self.call("/api/cases/ZF-3", actor="quil")
        self.assertEqual(code, 200, quil)
        item = quil["field_escalations"][0]
        self.assertEqual(item["summary"], projection.NOTE_HELD)
        self.assertEqual(item["contract_notice"], job_pack.NON_INSTRUCTION_NOTICE)
        self.assertIs(item["acts_as_contract_instruction"], False)
        self.assertNotIn(text, json.dumps(quil))
        _, sam = self.call("/api/cases/ZF-3", actor="sam")
        self.assertEqual(sam["field_escalations"][0]["summary"], text)

    def test_instruction_or_binding_claims_are_rejected(self) -> None:
        for over in (
            dict(acts_as_contract_instruction=True),
            dict(contract_instruction=True),
            dict(binding=True),
            dict(approved=True),
            dict(issue_variation="yes"),
        ):
            code, out = self.raise_it(**over)
            self.assertEqual(code, 400, (over, out))
            self.assertIn("cannot be a contract instruction", out["error"])
        self.assertEqual(self.view()["escalations"], [])

    def test_contractor_cannot_raise_and_core_stamp(self) -> None:
        self.assertEqual(self.raise_it("kim")[0], 403)
        item = job_pack.escalation("variation", "x", "Kim", "WO-1", OWNER, ROLE)
        self.assertIs(item["acts_as_contract_instruction"], False)
        for claim in (True, 1, "yes", 0.5):
            with self.assertRaises(ValueError):
                job_pack.reject_instruction_claim(dict(binding=claim))
        job_pack.reject_instruction_claim(dict(binding=False, approved=None, instruct=""))
        with self.assertRaises(ValueError):
            job_pack.reject_instruction_claim(dict(binding=0))


class JsonFieldworkVariationOwnerGuard(FieldworkVariationOwnerGuard):
    sql = False


SCREEN = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/staff-intake.js", "utf8");
const data = JSON.parse(fs.readFileSync(0, "utf8"));
const flat = (kids) => kids.flat(Infinity).filter((k) => k !== false && k != null);
const h = (tag, attrs, ...kids) => {
  const node = {tag, attrs: attrs || {}, kids: flat(kids)};
  node.setAttribute = (key, value) => { node.attrs[key] = value; };
  return node;
};
const text = (n) => typeof n === "object"
  ? [JSON.stringify(n.attrs), ...n.kids.map(text)].join(" ") : String(n);
const find = (n, tag, out = []) => {
  if (typeof n === "object") {
    if (n.tag === tag) out.push(n);
    n.kids.forEach((k) => find(k, tag, out));
  }
  return out;
};
let screen;
const calls = [];
class Form {
  constructor(f) { this.f = f; }
  get(k) { return this.f.values[k]; }
}
const context = vm.createContext({
  h, FormData: Form, routeController: {}, roleScreensView: async () => {},
  api: async (...a) => { calls.push(a); return {}; },
  screenStamp: String, screenPanel: (t, ...k) => h("section", {}, t, ...k),
  screenFields: (rows) => h("dl", {}, rows),
  screenTable: (t, head, rows) => h("table", {}, t, head, rows),
  registerRoleScreen: (s) => { screen = s; },
});
vm.runInContext(src, context);
(async () => {
  const mk = (e) => screen.render({id: "ZF-3"},
    {details: [{id: "WO-0001", data: {...data, escalations: [e]}}]});
  const item = data.escalations[0];
  const good = text(mk(item));
  const forged = text(mk({...item, contract_instruction: undefined}));
  const forged2 = text(mk({...item, acts_as_contract_instruction: true}));
  const label = "Raise a variation or concern";
  const form = find(mk(item), "form").find((f) => f.attrs["aria-label"] === label);
  const names = ["select", "textarea", "input"].flatMap((t) => find(form, t))
    .map((n) => n.attrs.name);
  form.values = {kind: "variation", summary: "S", named_owner: "Pam Lead",
    owner_role: "Retrofit Programme Manager"};
  form.querySelector = () => ({disabled: false});
  await form.attrs.onsubmit({preventDefault() {}});
  console.log(JSON.stringify({good, forged, forged2, names, calls}));
})();
"""


class StaffIntakeEscalationScreen(unittest.TestCase):
    def test_raise_form_posts_and_non_instruction_status_fails_closed(self) -> None:
        item = job_pack.escalation("variation", "Loft", "Sam", "WO-0001", OWNER, ROLE)
        payload = dict(
            pack=dict(
                scope="s",
                scope_version=1,
                design_version="d",
                access="a",
                named_contact="n",
                state="Appointed",
                ready=False,
                not_ready_reason="x",
                measures=[],
                checklists={},
            ),
            receipts=[],
            recovery=[],
            escalation=dict(
                owner="o", role="r", contact="c", acts_as_contract_instruction=False, note="n"
            ),
            escalation_options=dict(
                kinds=list(job_pack.ESCALATION_KINDS),
                owner_roles=list(job_pack.ESCALATION_OWNER_ROLES),
            ),
            escalations=[item],
            boundaries=dict(acceptance="a", consent="c"),
        )
        done = subprocess.run(
            ["node", "-e", SCREEN, str(WEB)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=True,
        )
        out = json.loads(done.stdout)
        self.assertIn("No - not a contract instruction", out["good"])
        for bad in ("forged", "forged2"):
            self.assertNotIn("No - not a contract instruction", out[bad])
            self.assertIn("Unknown - check with the contract manager", out[bad])
        self.assertEqual(sorted(out["names"]), ["kind", "named_owner", "owner_role", "summary"])
        self.assertEqual(
            out["calls"],
            [
                [
                    "/api/workorders/WO-0001/field-escalate",
                    dict(
                        kind="variation",
                        summary="S",
                        named_owner="Pam Lead",
                        owner_role="Retrofit Programme Manager",
                    ),
                ]
            ],
        )

    def test_screen_source_stays_safe(self) -> None:
        src = (WEB / "staff-intake.js").read_text()
        self.assertNotIn("innerHTML", src)
        self.assertNotIn("aria-invalid", src)
        self.assertIn("field-escalate", src)


if __name__ == "__main__":
    unittest.main()
