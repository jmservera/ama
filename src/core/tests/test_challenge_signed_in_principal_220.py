"""Issue #220 criterion 5: a staff-recorded write by a signed-in Entra-shaped principal.

The live demo refused every staff-recorded route write because the whole principal was compared
with the roster row. Immutable keys (email, code, oid) decide identity; display and tenant
claims must not. These tests prove the write then succeeds without lowering priority, inferring
refusal or touching a hazard clock, and that a different person is still refused.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset as _dataset
from zava_forward.core import identity
from zava_forward.core.store import Store as _Store

DATA: dict[str, Any] = _dataset.DATA
STORE_CLS: Any = _Store

TID = "11111111-1111-4111-8111-111111111111"
OID = "22222222-2222-4222-8222-222222222222"
PAYLOAD: dict[str, Any] = {
    "action": "nomination_record",
    "case_id": "ZF-1",
    "kind": "Self-referral",
    "reported_subject_ref": "SYN-NOM-SUBJ-220",
    "account": "SYN household asked for retrofit consideration.",
    "source": "SYN-NOM-SRC-220",
    "channel": "Phone",
    "owner": "sam@example.test",
    "acknowledgement_ref": "SYN-NOM-ACK-220",
    "next_update": "2099-01-20",
    "non_digital_route": "SYN Phone Sam.",
    "hazard_concern": False,
}


class SignedInPrincipalStaffRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seed = Path(tmp.name) / "seed.json"
        seed.write_text(json.dumps(copy.deepcopy(DATA)))
        self.store = STORE_CLS(str(seed))
        self.sam = self.store.staff["sam@example.test"]
        self.sam.update(tid=TID, oid=OID)

    def principal(self, oid: str = OID) -> dict[str, Any]:
        raw = identity.principal(
            tid=TID,
            oid=oid,
            name="Directory Display Name",
            email="sam@example.test",
            role=self.sam["role"],
            roles=(),
        )
        bound = identity.bind(self.store, raw)
        assert bound is not None
        return bound

    def test_extra_claims_do_not_block_and_nothing_adverse_is_inferred(self) -> None:
        principal = self.principal()
        self.assertNotEqual(principal, self.store.staff["sam@example.test"])
        self.store._ranks = None
        ranking = copy.deepcopy(self.store._ranking())
        case = self.store._case("ZF-1")
        protected = {
            k: copy.deepcopy(case.get(k)) for k in ("stage", "hazards", "closed", "score", "urgent")
        }

        self.store.resident_action(principal, "ZF-1", dict(PAYLOAD))

        after = self.store._case("ZF-1")
        self.assertEqual(len(after["nomination_records"]), 1)
        self.assertEqual({k: after.get(k) for k in protected}, protected)
        self.store._ranks = None
        self.assertEqual(self.store._ranking(), ranking)

    def test_different_code_is_still_refused_before_any_write(self) -> None:
        impostor = self.principal("33333333-3333-4333-8333-333333333333")
        with self.assertRaises((PermissionError, ValueError)):
            self.store.resident_action(impostor, "ZF-1", dict(PAYLOAD))
        self.assertFalse(self.store._case("ZF-1").get("nomination_records"))
    def test_roster_row_without_oid_still_admits_the_matching_principal(self) -> None:
        raw = identity.principal(
            tid=TID, oid=OID, name="Directory Display Name", email="sam@example.test",
            role=self.sam["role"], roles=(),
        )
        row = self.store.staff.pop("sam@example.test")
        row.pop("oid", None)
        row.pop("tid", None)
        row.update(code=raw["code"], email=raw["email"])
        self.store.staff[raw["email"]] = row
        principal = identity.bind(self.store, raw)
        assert principal is not None and not principal.get("bound")
        payload = dict(PAYLOAD, owner=raw["email"])
        self.store.resident_action(principal, "ZF-1", payload)
        self.assertEqual(len(self.store._case("ZF-1")["nomination_records"]), 1)

        other = identity.principal(
            tid=TID,
            oid="33333333-3333-4333-8333-333333333333",
            name="Other",
            role=row["role"],
            roles=(),
        )
        with self.assertRaises((PermissionError, ValueError)):
            self.store.resident_action(other, "ZF-1", dict(payload, next_update="2099-01-21"))
        self.assertEqual(len(self.store._case("ZF-1")["nomination_records"]), 1)


if __name__ == "__main__":
    unittest.main()
