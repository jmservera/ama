"""Exception register: scoped to named staff, read-only, honest about what it cannot see (#135)."""

import json
import os
import unittest
from typing import Any
from unittest import mock

from zava_forward.core import exception_register
from zava_forward.core.exception_register import staff_from_env
from zava_forward.core.workflows import MANAGER_ROLES

from role_matrix_fixture import ROLES, MatrixServer, SqlStoreCase

STAFF = {
    "human0@example.test": ("data_steward",),
    "human1@example.test": ("digital_operator",),
}


def side(value: str, source: str, version: str) -> dict[str, str]:
    return {"value": value, "source_id": source, "date": "2026-01-01", "version": version}


class Register(SqlStoreCase):
    reg_case: dict[str, Any]

    def setUp(self) -> None:
        super().setUp()
        self.reg_case = next(iter(self.store.cases.values()))
        self.reg_case["closed"] = False
        self.reg_case["stock_reconciliation"] = [
            {
                "id": "SQ-1",
                "field": "epc",
                "left": side("D", "S-A", "1"),
                "right": side("C", "S-B", "2"),
            }
        ]
        self.store.data["recommendations"].append(
            {
                "id": "R-AI",
                "kind": "ai_task",
                "task": "summary",
                "mode": "ai",
                "source": "template",
                "fallback_reason": "model timeout",
                "status": "Not reviewed",
                "created": "2026-11-01",
            }
        )
        self.steward = self.people["Retrofit Programme Manager"]
        self.steward = dict(self.steward, email="human0@example.test")
        self.operator = dict(self.steward, email="human1@example.test", name="Operator")

    def test_steward_sees_only_conflict_with_both_values_and_owner(self) -> None:
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(view["state"], "ok")
        kinds = {i["kind"] for i in view["items"]}
        self.assertEqual(kinds, {"source_conflict"})
        item = view["items"][0]
        self.assertEqual({v["value"] for v in item["values"]}, {"D", "C"})
        self.assertEqual(item["owner"], "human0@example.test")
        self.assertEqual(item["eligibility"], "Unknown")
        self.assertEqual(item["original_source"]["case_id"], self.reg_case["id"])

    def test_operator_sees_failed_ai_run_not_conflicts(self) -> None:
        view = self.store.exception_register(self.operator, STAFF)
        kinds = {i["kind"] for i in view["items"]}
        self.assertIn("failed_ai_run", kinds)
        self.assertNotIn("source_conflict", kinds)

    def test_unreadable_case_record_is_reported_not_hidden(self) -> None:
        self.reg_case["handoff"] = {"state": "Offered"}
        view = self.store.exception_register(self.operator, STAFF)
        self.assertTrue(
            any(self.reg_case["id"] in u and "could not be read" in u for u in view["unrouted"])
        )

    def test_reading_changes_nothing(self) -> None:
        before = json.dumps(self.store.data["recommendations"], sort_keys=True) + json.dumps(
            self.reg_case.get("stock_reconciliation"), sort_keys=True
        )
        self.store.exception_register(self.steward, STAFF)
        self.store.exception_register(self.steward, STAFF)
        after = json.dumps(self.store.data["recommendations"], sort_keys=True) + json.dumps(
            self.reg_case.get("stock_reconciliation"), sort_keys=True
        )
        self.assertEqual(before, after)

    def test_unnamed_staff_are_refused_and_the_refusal_is_audited(self) -> None:
        stranger = dict(self.steward, email="other@example.test")
        with self.assertRaises(PermissionError):
            self.store.exception_register(stranger, STAFF)
        self.assertTrue(any(e["action"] == "denied" for e in self.store.audit_entries()))

    def test_view_is_audited(self) -> None:
        self.store.exception_register(self.steward, STAFF)
        self.assertTrue(
            any(e["action"] == "viewed_exception_register" for e in self.store.audit_entries())
        )

    def test_banner_is_unknown_and_unconnected_sources_are_stated(self) -> None:
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(view["banner"]["state"], "unknown")
        self.assertIn("Do not assume it is healthy", view["banner"]["text"])
        self.assertTrue(any("Failed imports are not connected" in s for s in view["sources"]))

    def test_no_named_roles_gives_empty_queue_for_managers_only(self) -> None:
        view = self.store.exception_register(self.pm, {})
        self.assertEqual((view["state"], view["items"]), ("roles_not_named", []))
        with self.assertRaises(PermissionError):
            self.store.exception_register(self.people["Resident Liaison Officer"], {})

    def test_malformed_stock_query_is_reported_and_other_cases_still_route(self) -> None:
        self.reg_case["stock_reconciliation"].append({"id": "SQ-BAD"})
        view = self.store.exception_register(self.steward, STAFF)
        self.assertTrue(
            any(
                self.reg_case["id"] in u and "stock query could not be read" in u
                for u in view["unrouted"]
            )
        )
        other = next(
            c for c in self.store.cases.values() if c is not self.reg_case and not c.get("closed")
        )
        other["stock_reconciliation"] = [
            {
                "id": "SQ-2",
                "field": "tenure",
                "left": side("A", "S-A", "1"),
                "right": side("B", "S-B", "2"),
            }
        ]
        view = self.store.exception_register(self.steward, STAFF)
        self.assertTrue(any(i["original_source"]["case_id"] == other["id"] for i in view["items"]))

    def test_malformed_recommendation_does_not_break_the_operator_view(self) -> None:
        self.store.data["recommendations"].append(None)
        view = self.store.exception_register(self.operator, STAFF)
        self.assertIn("failed_ai_run", {i["kind"] for i in view["items"]})
        self.assertTrue(any("could not be read" in u for u in view["unrouted"]))

    def test_access_roles_show_only_the_callers_own_entry(self) -> None:
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(view["access"]["roles"], {"human0@example.test": ["data_steward"]})

    def test_empty_staff_paths_are_audited(self) -> None:
        self.store.exception_register(self.pm, {})
        with self.assertRaises(PermissionError):
            self.store.exception_register(self.people["Resident Liaison Officer"], {})
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertIn("viewed_exception_register", actions)
        self.assertIn("denied", actions)

    def test_missing_role_holder_is_reported_not_defaulted(self) -> None:
        view = self.store.exception_register(
            self.steward, {"human0@example.test": ("data_steward",)}
        )
        self.assertTrue(any("No named digital operator" in u for u in view["unrouted"]))


class Config(unittest.TestCase):
    def test_parses_valid_staff(self) -> None:
        env = {exception_register.STAFF_ENV: json.dumps({"A@x.test": ["data_steward"]})}
        self.assertEqual(staff_from_env(env), {"a@x.test": ("data_steward",)})

    def test_bad_input_names_nobody(self) -> None:
        for raw in ("", "{", "[]", json.dumps({"a": ["admin"]}), json.dumps({"a": []})):
            self.assertEqual(staff_from_env({exception_register.STAFF_ENV: raw}), {}, raw)


class Endpoint(MatrixServer):
    def staff_env(self, mapping: dict[str, list[str]]) -> Any:
        return mock.patch.dict("os.environ", {exception_register.STAFF_ENV: json.dumps(mapping)})

    def test_named_steward_gets_scoped_content_and_others_are_refused_and_audited(self) -> None:
        steward, other = self.session("u1@example.test"), self.session("u2@example.test")
        self.store.cases["ZF-1"]["closed"] = False
        self.store.cases["ZF-1"]["stock_reconciliation"] = [
            {
                "id": "SQ-1",
                "field": "epc",
                "left": side("D", "S-A", "1"),
                "right": side("C", "S-B", "2"),
            }
        ]
        with self.staff_env({"u1@example.test": ["data_steward"]}):
            code, text = self.call(steward, "/api/exceptions")
            self.assertEqual(code, 200)
            body = json.loads(text)
            self.assertEqual({i["kind"] for i in body["items"]}, {"source_conflict"})
            self.assertEqual(body["access"]["roles"], {"u1@example.test": ["data_steward"]})
            self.assertEqual(self.call(other, "/api/exceptions")[0], 403)
        entries = list(self.store.audit_entries())
        self.assertTrue(
            any(e["action"] == "denied" and e["who"] == "u2@example.test" for e in entries)
        )
        self.assertTrue(any(e["action"] == "viewed_exception_register" for e in entries))

    def test_other_staff_emails_are_not_exposed_to_a_named_operator(self) -> None:
        with self.staff_env(
            {"u1@example.test": ["data_steward"], "u2@example.test": ["digital_operator"]}
        ):
            code, text = self.call(self.session("u2@example.test"), "/api/exceptions")
        self.assertEqual(code, 200)
        self.assertNotIn("u1@example.test", text)

    def test_with_nobody_named_only_managers_see_the_empty_state(self) -> None:
        with mock.patch.dict("os.environ", {}, clear=False):
            os.environ.pop(exception_register.STAFF_ENV, None)
            for role in ROLES:
                email = next(s["email"] for s in self.store.data["staff"] if s["role"] == role)
                code, text = self.call(self.session(email), "/api/exceptions")
                if role in MANAGER_ROLES:
                    self.assertEqual(
                        (code, json.loads(text)["state"]), (200, "roles_not_named"), role
                    )
                else:
                    self.assertEqual(code, 403, role)

    def test_unauthenticated_is_refused(self) -> None:
        self.assertIn(self.call("", "/api/exceptions")[0], (401, 403))


if __name__ == "__main__":
    with mock.patch.dict("os.environ", {}):
        unittest.main()
