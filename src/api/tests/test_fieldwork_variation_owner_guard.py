"""Variations and escalations reach a named owner and never act as a contract instruction (#132)."""

import unittest
from typing import Any

from dataset import supplied_appointment_fixture
from zava_forward.core import job_pack

from test_procurement_api import ProcurementApiFixture

OWNER = "Pam Lead"
ROLE = "Retrofit Programme Manager"


ROUTE = "/api/workorders/WO-0001/"


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
        self.assertIn("not a contract instruction", item["note"])
        self.restart()
        view = self.view()
        self.assertEqual(view["escalations"][0]["owner"]["name"], OWNER)
        self.assertIs(view["boundaries"]["acts_as_contract_instruction"], False)
        self.assertIs(view["escalation"]["acts_as_contract_instruction"], False)
        self.assertTrue(self.store.verify_audit())
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
        with self.assertRaises(ValueError):
            job_pack.reject_instruction_claim(dict(binding=True))


if __name__ == "__main__":
    unittest.main()
