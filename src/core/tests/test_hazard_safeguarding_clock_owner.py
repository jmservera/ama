"""Staff-ordering invariance and SQL Server email-order parity tests for Issue #76."""

from __future__ import annotations

import copy
import itertools
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import test_sqlreads
from zava_forward.core import taskqueues
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

AS_OF = "2026-10-15T12:00:00Z"

STAFF_INSERTION_ORDER: list[dict[str, Any]] = [
    {
        "code": "RLO-01",
        "name": "Sam Example",
        "email": "sam@example.test",
        "role": "Resident Liaison Officer",
    },
    {
        "code": "PM-01",
        "name": "Pam Lead",
        "email": "pam@example.test",
        "role": "Retrofit Programme Manager",
    },
    {
        "code": "CON-1",
        "name": "Kim Builder",
        "email": "kim@example.test",
        "role": "Contractor",
        "contractor": "Alpha Ltd",
    },
]

STAFF_EMAIL_PK_ORDER: list[dict[str, Any]] = sorted(
    STAFF_INSERTION_ORDER,
    key=lambda m: str(m["email"]),
)


class StaffOrderInvarianceTests(unittest.TestCase):
    def test_match_staff_checks_code_then_email_then_name_across_staff_orders(self) -> None:
        for roster in (STAFF_INSERTION_ORDER, STAFF_EMAIL_PK_ORDER):
            by_code = taskqueues._match_staff(
                code=" PM-01 ",
                email="sam@example.test",
                name="Sam Example",
                staff=roster,
            )
            assert by_code is not None
            self.assertEqual(by_code["code"], "PM-01")
            self.assertEqual(by_code["name"], "Pam Lead")

            by_email = taskqueues._match_staff(
                code=None,
                email=" PAM@EXAMPLE.TEST ",
                name="Sam Example",
                staff=roster,
            )
            assert by_email is not None
            self.assertEqual(by_email["code"], "PM-01")
            self.assertEqual(by_email["name"], "Pam Lead")

            by_name = taskqueues._match_staff(
                code="UNLISTED-99",
                email="unlisted@example.test",
                name=" Sam Example ",
                staff=roster,
            )
            assert by_name is not None
            self.assertEqual(by_name["code"], "RLO-01")

    def test_project_safety_clock_and_owner_is_identical_for_all_staff_permutations(self) -> None:
        case_mixed_owner: dict[str, Any] = {
            "id": "ZF-00007",
            "owner": "Sam Example",
            "owner_code": "PM-01",
        }
        allocated_hazard: dict[str, Any] = {
            "category": "Damp",
            "priority": "P1",
            "noticed": "2026-10-15T06:00:00Z",
            "owner": "Bea",
        }
        unallocated_safeguarding: dict[str, Any] = {
            "id": "SG-ORDER-1",
            "priority": "Urgent",
            "raised_at": "2026-10-15T06:00:00Z",
        }

        baseline_allocated = taskqueues.project_safety_clock_and_owner(
            allocated_hazard,
            case=case_mixed_owner,
            as_of=AS_OF,
            staff=STAFF_INSERTION_ORDER,
        )
        email_order_allocated = taskqueues.project_safety_clock_and_owner(
            allocated_hazard,
            case=case_mixed_owner,
            as_of=AS_OF,
            staff=STAFF_EMAIL_PK_ORDER,
        )
        self.assertEqual(baseline_allocated, email_order_allocated)
        self.assertEqual(baseline_allocated["named_owner"], "Bea")
        self.assertEqual(baseline_allocated["escalation_owner"], "Pam Lead")
        self.assertEqual(baseline_allocated["escalation_owner_role"], "Retrofit Programme Manager")
        self.assertEqual(baseline_allocated["escalation_owner_id"], "PM-01")

        baseline_unallocated = taskqueues.project_safety_clock_and_owner(
            unallocated_safeguarding,
            case=case_mixed_owner,
            as_of=AS_OF,
            staff=STAFF_INSERTION_ORDER,
            default_kind="safeguarding",
        )
        self.assertTrue(baseline_unallocated["unassigned"])
        self.assertEqual(baseline_unallocated["named_owner"], "Pam Lead")
        self.assertEqual(baseline_unallocated["escalation_owner"], "Pam Lead")
        self.assertEqual(baseline_unallocated["owner_id"], "PM-01")

        for perm in itertools.permutations(STAFF_INSERTION_ORDER):
            roster = list(perm)
            self.assertEqual(
                taskqueues.project_safety_clock_and_owner(
                    allocated_hazard,
                    case=case_mixed_owner,
                    as_of=AS_OF,
                    staff=roster,
                ),
                baseline_allocated,
            )
            self.assertEqual(
                taskqueues.project_safety_clock_and_owner(
                    unallocated_safeguarding,
                    case=case_mixed_owner,
                    as_of=AS_OF,
                    staff=roster,
                    default_kind="safeguarding",
                ),
                baseline_unallocated,
            )

    def test_role_fallback_is_deterministic_when_multiple_staff_share_target_role(self) -> None:
        bsl_a: dict[str, Any] = {
            "code": "BS-01",
            "name": "Alex Liaison",
            "email": "z-alex@example.test",
            "role": "Building Safety Liaison",
        }
        bsl_b: dict[str, Any] = {
            "code": "BS-02",
            "name": "Blair Liaison",
            "email": "a-blair@example.test",
            "role": "Building Safety Liaison",
        }
        unowned_hazard: dict[str, Any] = {
            "category": "Fire safety",
            "priority": "Emergency",
            "aware_at": "2026-10-15T08:00:00Z",
        }
        forward = taskqueues.project_safety_clock_and_owner(
            unowned_hazard,
            case={"id": "ZF-UNOWNED"},
            as_of=AS_OF,
            staff=[bsl_a, bsl_b],
        )
        reverse = taskqueues.project_safety_clock_and_owner(
            unowned_hazard,
            case={"id": "ZF-UNOWNED"},
            as_of=AS_OF,
            staff=[bsl_b, bsl_a],
        )
        self.assertEqual(forward, reverse)
        self.assertEqual(forward["named_owner"], "Alex Liaison")
        self.assertEqual(forward["escalation_owner"], "Alex Liaison")
        self.assertEqual(forward["owner_id"], "BS-01")

    def test_store_and_email_seeded_sqlstore_match_on_mixed_owner_code_dataset(self) -> None:
        reads_mod: Any = test_sqlreads
        store_cls: Any = Store
        sql_store_cls: Any = SqlStore

        cases: list[dict[str, Any]] = reads_mod.make_cases(120, seed=11)
        json_data: dict[str, Any] = reads_mod.dataset(copy.deepcopy(cases))
        sql_data: dict[str, Any] = copy.deepcopy(json_data)
        sql_data["staff"] = copy.deepcopy(STAFF_EMAIL_PK_ORDER)

        with tempfile.TemporaryDirectory() as tmp:
            json_seed = Path(tmp) / "json_seed.json"
            sql_seed = Path(tmp) / "sql_seed.json"
            sql_db = Path(tmp) / "parity.sqlite"
            json_seed.write_text(json.dumps(json_data))
            sql_seed.write_text(json.dumps(sql_data))

            jstore: Any = store_cls(str(json_seed))
            sstore: Any = sql_store_cls(str(sql_seed), str(sql_db))
            try:
                self.assertEqual(
                    [m["email"] for m in jstore.data["staff"]],
                    ["sam@example.test", "pam@example.test", "kim@example.test"],
                )
                self.assertEqual(
                    [m["email"] for m in sstore.data["staff"]],
                    ["kim@example.test", "pam@example.test", "sam@example.test"],
                )
                for user in STAFF_INSERTION_ORDER[:2]:
                    self.assertEqual(jstore.counts(user), sstore.counts(user))
                    for view in ("all", "mine"):
                        for flt in (
                            None,
                            {"flag": "hazard"},
                            {"queue": "blocked"},
                            {"queue": "overdue"},
                        ):
                            self.assertEqual(
                                jstore.page_cases(user, view, "", flt, "urgent"),
                                sstore.page_cases(user, view, "", flt, "urgent"),
                            )
                hazard_case_ids = [c["id"] for c in cases if c.get("hazards")]
                self.assertGreater(len(hazard_case_ids), 0)
                pm_user = STAFF_INSERTION_ORDER[1]
                for cid in hazard_case_ids:
                    self.assertEqual(jstore.detail(cid, pm_user), sstore.detail(cid, pm_user))
            finally:
                sstore.db.close()


if __name__ == "__main__":
    unittest.main()
