"""Exception register: scoped to named staff, read-only, honest about what it cannot see (#135)."""

import json
import unittest
from unittest import mock

from zava_forward.core import exception_register
from zava_forward.core.exception_register import staff_from_env

from test_assistants import Base

STAFF = {
    "human0@example.test": ("data_steward",),
    "human1@example.test": ("digital_operator",),
}


def side(value, source, version):
    return {"value": value, "source_id": source, "date": "2026-01-01", "version": version}


class Register(Base):
    def setUp(self):
        super().setUp()
        self.case = next(iter(self.store.cases.values()))
        self.case["closed"] = False
        self.case["stock_reconciliation"] = [
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

    def test_steward_sees_only_conflict_with_both_values_and_owner(self):
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(view["state"], "ok")
        kinds = {i["kind"] for i in view["items"]}
        self.assertEqual(kinds, {"source_conflict"})
        item = view["items"][0]
        self.assertEqual({v["value"] for v in item["values"]}, {"D", "C"})
        self.assertEqual(item["owner"], "human0@example.test")
        self.assertEqual(item["eligibility"], "Unknown")
        self.assertEqual(item["original_source"]["case_id"], self.case["id"])

    def test_operator_sees_failed_ai_run_not_conflicts(self):
        view = self.store.exception_register(self.operator, STAFF)
        kinds = {i["kind"] for i in view["items"]}
        self.assertIn("failed_ai_run", kinds)
        self.assertNotIn("source_conflict", kinds)

    def test_unreadable_case_record_is_reported_not_hidden(self):
        self.case["handoff"] = {"state": "Offered"}
        view = self.store.exception_register(self.operator, STAFF)
        self.assertTrue(
            any(self.case["id"] in u and "could not be read" in u for u in view["unrouted"])
        )

    def test_reading_changes_nothing(self):
        before = json.dumps(self.store.data["recommendations"], sort_keys=True) + json.dumps(
            self.case.get("stock_reconciliation"), sort_keys=True
        )
        self.store.exception_register(self.steward, STAFF)
        self.store.exception_register(self.steward, STAFF)
        after = json.dumps(self.store.data["recommendations"], sort_keys=True) + json.dumps(
            self.case.get("stock_reconciliation"), sort_keys=True
        )
        self.assertEqual(before, after)

    def test_unnamed_staff_are_refused_and_the_refusal_is_audited(self):
        stranger = dict(self.steward, email="other@example.test")
        with self.assertRaises(PermissionError):
            self.store.exception_register(stranger, STAFF)
        self.assertTrue(any(e["action"] == "denied" for e in self.store.audit_entries()))

    def test_view_is_audited(self):
        self.store.exception_register(self.steward, STAFF)
        self.assertTrue(
            any(e["action"] == "viewed_exception_register" for e in self.store.audit_entries())
        )

    def test_banner_is_unknown_and_unconnected_sources_are_stated(self):
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(view["banner"]["state"], "unknown")
        self.assertIn("Do not assume it is healthy", view["banner"]["text"])
        self.assertTrue(any("Failed imports are not connected" in s for s in view["sources"]))

    def test_no_named_roles_gives_empty_queue_for_managers_only(self):
        view = self.store.exception_register(self.pm, {})
        self.assertEqual((view["state"], view["items"]), ("roles_not_named", []))
        with self.assertRaises(PermissionError):
            self.store.exception_register(self.people["Resident Liaison Officer"], {})

    def test_missing_role_holder_is_reported_not_defaulted(self):
        view = self.store.exception_register(
            self.steward, {"human0@example.test": ("data_steward",)}
        )
        self.assertTrue(any("No named digital operator" in u for u in view["unrouted"]))


class Config(unittest.TestCase):
    def test_parses_valid_staff(self):
        env = {exception_register.STAFF_ENV: json.dumps({"A@x.test": ["data_steward"]})}
        self.assertEqual(staff_from_env(env), {"a@x.test": ("data_steward",)})

    def test_bad_input_names_nobody(self):
        for raw in ("", "{", "[]", json.dumps({"a": ["admin"]}), json.dumps({"a": []})):
            self.assertEqual(staff_from_env({exception_register.STAFF_ENV: raw}), {}, raw)


class Endpoint(unittest.TestCase):
    def test_route_is_registered_in_server(self):
        from pathlib import Path

        import zava_forward.api.server as server

        text = Path(server.__file__).read_text()
        self.assertIn('"/api/exceptions"', text)
        self.assertIn("exception_register.staff_from_env", text)


if __name__ == "__main__":
    with mock.patch.dict("os.environ", {}):
        unittest.main()
