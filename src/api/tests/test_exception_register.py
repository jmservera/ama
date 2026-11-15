"""Exception register: scoped to named staff, read-only, honest about what it cannot see (#135)."""

import copy
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from dataset import DATA
from zava_forward.core import continuity, exception_register, import_refusals, projection
from zava_forward.core.exception_register import staff_from_env
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
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
        self.assertTrue(item["unresolved_eligibility"])
        self.assertFalse(item["recovery_policy"]["automatic_replay"])
        self.assertFalse(item["recovery_policy"]["automatic_release"])
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

    def test_one_view_adds_one_ledger_entry_and_leaves_the_data_unchanged(self) -> None:
        data = json.dumps(self.store.data, sort_keys=True, default=str)
        ledger = list(self.store.audit_entries())
        self.store.exception_register(self.steward, STAFF)
        after = list(self.store.audit_entries())
        views = [e for e in after if e["action"] == "viewed_exception_register"]
        self.assertEqual(len(after), len(ledger) + 1)
        self.assertEqual(len(views), 1)
        self.assertEqual(json.dumps(self.store.data, sort_keys=True, default=str), data)

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

    def _key(self, user: dict[str, str], kind: str) -> str:
        view = self.store.exception_register(user, STAFF)
        return str(next(i["recovery_key"] for i in view["items"] if i["kind"] == kind))

    def test_recovery_is_audited_and_changes_nothing_else(self) -> None:
        key = self._key(self.steward, "source_conflict")
        data = json.dumps(self.store.data, sort_keys=True, default=str)
        done = self.store.request_exception_recovery(
            self.steward, STAFF, key, "resolve_by_owner", "Checked both sources with the owner."
        )
        self.assertEqual(done["status"], "closed")
        self.assertFalse(done["recovery"]["replayed"] or done["recovery"]["released"])
        self.assertTrue(done["unresolved_eligibility"])
        self.assertEqual(done["original_source"]["case_id"], self.reg_case["id"])
        self.assertEqual(json.dumps(self.store.data, sort_keys=True, default=str), data)
        entry = [
            e for e in self.store.audit_entries() if e["action"] == "exception_recovery_requested"
        ]
        self.assertEqual((len(entry), entry[0]["case"]), (1, key))
        again = self.store.exception_register(self.steward, STAFF)["items"][0]
        self.assertEqual(
            (again["status"], again["recovery"]["by"]), ("closed", self.steward["email"])
        )
        with self.assertRaises(ValueError):
            self.store.request_exception_recovery(self.steward, STAFF, key, "hold", "Again.")

    def test_recovery_refuses_scope_owner_action_and_missing_reason(self) -> None:
        conflict = self._key(self.steward, "source_conflict")
        failed = self._key(self.operator, "failed_ai_run")
        steward2 = {
            "human0@example.test": ("data_steward",),
            "human2@example.test": ("data_steward",),
        }
        other = dict(self.steward, email="human2@example.test")
        for who, key, action in (
            (self.operator, conflict, "hold"),
            (self.steward, failed, "hold"),
            (other, conflict, "resolve_by_owner"),
        ):
            with self.assertRaises(PermissionError):
                self.store.request_exception_recovery(who, steward2 | STAFF, key, action, "Why.")
        with self.assertRaises(ValueError):
            self.store.request_exception_recovery(self.steward, STAFF, conflict, "replay", "Why.")
        with self.assertRaises(ValueError):
            self.store.request_exception_recovery(self.steward, STAFF, conflict, "hold", " ")
        with self.assertRaises(PermissionError):
            self.store.request_exception_recovery(self.pm, STAFF, conflict, "hold", "Why.")
        done = [
            e for e in self.store.audit_entries() if e["action"] == "exception_recovery_requested"
        ]
        self.assertEqual(done, [])
        self.assertTrue(any(e["action"] == "denied" for e in self.store.audit_entries()))

    def test_failed_run_rerun_is_a_request_not_a_replay(self) -> None:
        key = self._key(self.operator, "failed_ai_run")
        done = self.store.request_exception_recovery(
            self.operator, STAFF, key, "request_rerun", "Model timed out."
        )
        self.assertEqual(done["status"], "rerun_requested")
        self.assertFalse(done["recovery"]["automatic_replay"])
        rec = next(r for r in self.store.data["recommendations"] if r["id"] == "R-AI")
        self.assertEqual(rec["source"], "template")

    def test_conflict_and_failures_expose_resolution_owner_category_correlation_and_context(
        self,
    ) -> None:
        self.reg_case["hazards"] = [{"response_due_at": "2020-01-01T00:00:00Z"}]
        rec = next(r for r in self.store.data["recommendations"] if r["id"] == "R-AI")
        rec["correlation_id"] = "CORR-AI-77"
        self.store.data["import_batches"] = [
            {
                "batch_id": "B-77",
                "status": "rejected",
                "error": "schema mismatch",
                "correlation_id": "CORR-B77",
            }
        ]
        steward_view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(steward_view["access"]["viewer_roles"], ["data_steward"])
        self.assertIn("source_conflict", steward_view["access"]["allowed_kinds"])
        self.assertIn("failed_import", steward_view["access"]["allowed_kinds"])
        conflict = next(i for i in steward_view["items"] if i["kind"] == "source_conflict")
        self.assertEqual(conflict["resolution_owner"], "human0@example.test")
        self.assertEqual(
            [(v["value"], v["source"], v["date"], v["version"]) for v in conflict["values"]],
            [("D", "S-A", "2026-01-01", "1"), ("C", "S-B", "2026-01-01", "2")],
        )
        self.assertEqual(conflict["correlation_id"], f"stock:{self.reg_case['id']}:SQ-1")
        self.assertEqual(conflict["recovery_context"]["correlation_id"], conflict["correlation_id"])
        batch_item = next(i for i in steward_view["items"] if i["kind"] == "failed_import")
        self.assertEqual(batch_item["failure_category"], "failed_import")
        self.assertEqual(batch_item["correlation_id"], "CORR-B77")
        self.assertEqual(batch_item["eligibility"], "Unknown")
        op_view = self.store.exception_register(self.operator, STAFF)
        self.assertEqual(op_view["access"]["viewer_roles"], ["digital_operator"])
        ai_item = next(i for i in op_view["items"] if i["kind"] == "failed_ai_run")
        self.assertEqual(ai_item["failure_category"], "failed_ai_run")
        self.assertEqual(ai_item["correlation_id"], "CORR-AI-77")
        stranded = next(i for i in op_view["items"] if i["kind"] == "stranded_task")
        self.assertEqual(stranded["failure_category"], "stranded_task")
        self.assertEqual(stranded["correlation_id"], f"case:{self.reg_case['id']}/hazards/0")
        self.assertFalse(stranded["recovery_context"]["automatic_replay"])
        self.assertFalse(stranded["recovery_context"]["automatic_release"])

    def test_continuity_suspension_and_actual_hold_surface_honest_outage_banner_with_next_steps(
        self,
    ) -> None:
        for r in self.store.data["recommendations"]:
            r.setdefault("user", "human0@example.test")
        pm = self.people["Retrofit Programme Manager"]
        suspended = self.store.suspend(
            pm,
            {
                "scope": continuity.ALL,
                "reason": "Provider quota exhausted",
                "incident_owner": "Pam Lead",
                "containment": "Manual workflow active",
                "comms_owner": "Comms Lead",
                "comms_audience": "Retrofit staff",
            },
        )
        comp_key = f"ai-tasks ({continuity.ALL})"
        for who, staff, expected_state in (
            (self.operator, STAFF, "ok"),
            (pm, {}, "roles_not_named"),
        ):
            view = self.store.exception_register(who, staff)
            self.assertEqual(view["state"], expected_state)
            self.assertEqual(view["banner"]["state"], "outage")
            self.assertTrue(len(view["banner"]["next_steps"]) >= 2)
            self.assertIn(comp_key, view["banner"]["components"])
            self.assertIn("Pam Lead", view["banner"]["components"][comp_key]["note"])
            self.assertFalse(
                any("service state is Unknown" in s for s in view["sources"]),
                view["sources"],
            )
        # Constructed-only restart where actual_hold remains True keeps the banner in outage.
        susp_doc = next(
            s for s in self.store.data["continuity"]["suspensions"] if s["id"] == suspended["id"]
        )
        susp_doc["status"] = "Restarted"
        susp_doc["actual_hold"] = True
        still_held = self.store.exception_register(self.operator, STAFF)
        self.assertEqual(still_held["banner"]["state"], "outage")


class Config(unittest.TestCase):
    def test_parses_valid_staff(self) -> None:
        env = {exception_register.STAFF_ENV: json.dumps({"A@x.test": ["data_steward"]})}
        self.assertEqual(staff_from_env(env), {"a@x.test": ("data_steward",)})

    def test_bad_input_names_nobody(self) -> None:
        for raw in ("", "{", "[]", json.dumps({"a": ["admin"]}), json.dumps({"a": []})):
            self.assertEqual(staff_from_env({exception_register.STAFF_ENV: raw}), {}, raw)


DIGEST = "a" * 64
REFUSAL = {
    "source_name": "synthetic-cases.xlsx",
    "source_sha256": DIGEST,
    "reason": "Refused: the file is not a valid .xlsx workbook.",
    "at": "2026-11-10T01:02:03Z",
}
HASHLESS = {
    "source_name": "big.xlsx (unverified source source:0123456789abcdef01234567)",
    "source_sha256": "",
    "reason": "Refused: the file is larger than the import limit.",
    "at": "2026-11-10T01:05:00Z",
}


class ImportRefusalRegister(unittest.TestCase):
    """One refused file reaches the existing register, survives a restart and transfers once."""

    kind = "sqlite"

    def open(self) -> Any:
        seed, state = str(self.root / "seed.json"), self.root / "state"
        if self.kind == "sqlite":
            store = SqlStore(seed, str(self.root / "cases.sqlite"))
            self.addCleanup(store.db.close)
            return store
        return Store(seed, str(state / "live.json"), str(state / "audit.jsonl"))

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="refusal-register-"))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        data: dict[str, Any] = copy.deepcopy(DATA)
        self.people = {}
        for i, role in enumerate(projection.STAFF_ROLES):
            self.people[role] = dict(
                code=f"ROLE-{i}", name=f"Human {i}", email=f"human{i}@example.test", role=role
            )
        data["staff"] = list(self.people.values())
        (self.root / "seed.json").write_text(json.dumps(data))
        self.pm = self.people["Retrofit Programme Manager"]
        self.steward = dict(self.pm, email="human0@example.test")
        self.operator = dict(self.pm, email="human1@example.test")
        self.store = self.open()

    def failed_imports(self, view: dict[str, Any]) -> list[dict[str, Any]]:
        return [i for i in view["items"] if i["kind"] == "failed_import"]

    def test_nothing_transferred_stays_not_connected(self) -> None:
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(self.failed_imports(view), [])
        self.assertTrue(any("not connected" in s for s in view["sources"]))

    def test_refused_file_survives_restart_with_identity_reason_time_and_unknown_eligibility(
        self,
    ) -> None:
        self.assertEqual(
            self.store.record_import_refusals([REFUSAL, HASHLESS]),
            {"added": 2, "already_present": 0, "total": 2},
        )
        self.store = self.open()
        view = self.store.exception_register(self.steward, STAFF)
        by_ref = {i["ref"]: i for i in self.failed_imports(view)}
        known = by_ref[f"file:{DIGEST}"]
        self.assertEqual(known["original_source"]["source_sha256"], DIGEST)
        self.assertEqual(known["original_source"]["at"], REFUSAL["at"])
        self.assertIn(REFUSAL["reason"], known["error"])
        self.assertIn("2026-11-10T01:02:03Z", known["error"])
        self.assertEqual(known["eligibility"], "Unknown")
        self.assertEqual(known["owner"], "human0@example.test")
        self.assertIsNone(
            by_ref[f"file:{HASHLESS['source_name']}"]["original_source"]["source_sha256"]
        )
        self.assertTrue(any("2 refused import file(s)" in s for s in view["sources"]))
        self.assertFalse(
            any(s.startswith("Failed imports are not connected") for s in view["sources"])
        )

    def test_repeat_transfer_changes_nothing_and_reading_writes_only_audits(self) -> None:
        self.store.record_import_refusals([REFUSAL])
        before = copy.deepcopy(self.store.data[import_refusals.KEY])
        again = self.store.record_import_refusals([dict(REFUSAL, reason="Different later reason.")])
        self.assertEqual(again, {"added": 0, "already_present": 1, "total": 1})
        first = self.store.exception_register(self.steward, STAFF)
        second = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(self.store.data[import_refusals.KEY], before)
        self.assertEqual(len(self.failed_imports(first)), 1)
        self.assertEqual(
            self.failed_imports(first)[0]["ref"], self.failed_imports(second)[0]["ref"]
        )
        actions = [e["action"] for e in self.store.audit_entries()]
        self.assertEqual(actions.count("recorded_import_refusals"), 1)
        self.assertEqual(actions.count("viewed_exception_register"), 2)

    def test_scope_operator_and_unnamed_manager_do_not_see_it(self) -> None:
        self.store.record_import_refusals([REFUSAL])
        self.assertEqual(
            self.failed_imports(self.store.exception_register(self.operator, STAFF)), []
        )
        view = self.store.exception_register(self.pm, {})
        self.assertEqual((view["state"], view["items"]), ("roles_not_named", []))
        with self.assertRaises(PermissionError):
            self.store.exception_register(dict(self.pm, email="human9@example.test"), STAFF)

    def test_source_text_separates_stored_from_shown_per_scope(self) -> None:
        self.store.record_import_refusals([REFUSAL])
        both = {
            self.steward["email"]: ("data_steward",),
            self.operator["email"]: ("digital_operator",),
        }
        operator_only = {self.operator["email"]: ("digital_operator",)}
        cases = [
            (self.steward, both, "1 are shown"),
            (self.operator, both, "0 are shown"),
            (self.operator, operator_only, "0 are shown"),
            (self.pm, {}, "0 are shown"),
        ]
        for who, staff, shown in cases:
            source = self.store.exception_register(who, staff)["sources"][0]
            self.assertIn("1 refused import file(s) are stored here", source)
            self.assertIn(shown, source)
            self.assertNotIn("not connected", source.split("Rejected")[0])
        self.assertNotIn("1 refused import file(s) are shown", source)

    def test_no_named_steward_reports_the_count_unrouted(self) -> None:
        self.store.record_import_refusals([REFUSAL])
        view = self.store.exception_register(
            self.operator, {self.operator["email"]: ("digital_operator",)}
        )
        self.assertEqual(self.failed_imports(view), [])
        self.assertTrue(
            any("1 refused import file(s) are not routed" in u for u in view["unrouted"])
        )

    def test_damaged_projection_is_not_shown_as_connected(self) -> None:
        self.store.data[import_refusals.KEY] = {"refusals": "damaged"}
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(self.failed_imports(view), [])
        self.assertTrue(any("could not be read" in u for u in view["unrouted"]))
        self.assertTrue(any("not connected" in s for s in view["sources"]))

    def test_invalid_refusals_are_refused_and_record_nothing(self) -> None:
        for bad in (
            dict(REFUSAL, source_sha256="XYZ"),
            dict(REFUSAL, reason=""),
            dict(REFUSAL, at="x" * 40),
        ):
            with self.assertRaises(ValueError):
                self.store.record_import_refusals([REFUSAL, bad])
        self.assertNotIn(import_refusals.KEY, self.store.data)

    def test_rejected_import_batches_survive_restart_for_sql_and_json_without_mutating_data(
        self,
    ) -> None:
        self.store.data.setdefault(import_refusals.KEY, {"refusals": []})["rejected_batches"] = [
            {
                "batch_id": "BATCH-404",
                "status": "rejected",
                "error": "Missing UPRN header",
                "correlation_id": "CORR-BATCH-404",
            }
        ]
        self.store.save()
        self.store = self.open()
        before = copy.deepcopy(self.store.data[import_refusals.KEY])
        view = self.store.exception_register(self.steward, STAFF)
        self.assertEqual(self.store.data[import_refusals.KEY], before)
        items = self.failed_imports(view)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["ref"], "batch:BATCH-404")
        self.assertEqual(items[0]["failure_category"], "failed_import")
        self.assertEqual(items[0]["correlation_id"], "CORR-BATCH-404")
        self.assertEqual(items[0]["eligibility"], "Unknown")
        self.assertEqual(
            self.failed_imports(self.store.exception_register(self.operator, STAFF)), []
        )
        self.assertTrue(any("1 rejected import batch(es)" in s for s in view["sources"]))


class ImportRefusalRegisterJson(ImportRefusalRegister):
    kind = "json"


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

    def test_transferred_refusal_is_served_to_the_steward_only(self) -> None:
        self.store.record_import_refusals([REFUSAL])
        with self.staff_env({"u1@example.test": ["data_steward"]}):
            code, text = self.call(self.session("u1@example.test"), "/api/exceptions")
            self.assertEqual(code, 200)
            items = [i for i in json.loads(text)["items"] if i["kind"] == "failed_import"]
            self.assertEqual([i["ref"] for i in items], [f"file:{DIGEST}"])
            self.assertEqual(self.call(self.session("u2@example.test"), "/api/exceptions")[0], 403)

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

    def test_post_recovery_multi_step_audit_trail_parity_and_no_replay_or_overwrite(self) -> None:
        steward_ck = self.session("u1@example.test")
        operator_ck = self.session("u2@example.test")
        self.store.cases["ZF-1"]["closed"] = False
        orig_query = {
            "id": "SQ-9",
            "field": "epc",
            "left": side("D", "S-A", "1"),
            "right": side("C", "S-B", "2"),
        }
        self.store.cases["ZF-1"]["stock_reconciliation"] = [copy.deepcopy(orig_query)]
        self.store.data["recommendations"] = [
            r for r in self.store.data["recommendations"] if r.get("id") != "R-EP-1"
        ] + [
            {
                "id": "R-EP-1",
                "kind": "ai_task",
                "task": "summary",
                "mode": "ai",
                "source": "template",
                "fallback_reason": "timeout",
                "correlation_id": "CORR-EP-1",
                "status": "Not reviewed",
                "created": "2026-11-01",
            }
        ]
        mapping = {"u1@example.test": ["data_steward"], "u2@example.test": ["digital_operator"]}
        with self.staff_env(mapping):
            code, text = self.call(steward_ck, "/api/exceptions")
            self.assertEqual(code, 200)
            conflict = next(
                i
                for i in json.loads(text)["items"]
                if i["recovery_key"] == "source_conflict:stock:ZF-1:SQ-9"
            )
            key = conflict["recovery_key"]
            # Cross-role and invalid input boundaries.
            self.assertEqual(
                self.call(
                    operator_ck,
                    "/api/exceptions/recovery",
                    {"key": key, "action": "hold", "reason": "Wrong role."},
                )[0],
                403,
            )
            self.assertEqual(
                self.call(
                    steward_ck,
                    "/api/exceptions/recovery",
                    {"key": key, "action": "hold", "reason": "   "},
                )[0],
                400,
            )
            self.assertEqual(
                self.call(
                    steward_ck,
                    "/api/exceptions/recovery",
                    {"key": key, "action": "replay_now", "reason": "Not allowed."},
                )[0],
                400,
            )
            # Step 1: hold -> Step 2: resolve_by_owner; POST/GET audit_trail lengths match (2).
            c1, t1 = self.call(
                steward_ck,
                "/api/exceptions/recovery",
                {"key": key, "action": "hold", "reason": "Checking EPC certificate."},
            )
            self.assertEqual(c1, 200)
            held = json.loads(t1)
            self.assertEqual((held["status"], len(held["audit_trail"])), ("held", 1))
            c2, t2 = self.call(
                steward_ck,
                "/api/exceptions/recovery",
                {
                    "key": key,
                    "action": "resolve_by_owner",
                    "reason": "Verified source S-B manually in stock system.",
                },
            )
            self.assertEqual(c2, 200)
            closed_post = json.loads(t2)
            self.assertEqual(
                (closed_post["status"], len(closed_post["audit_trail"])),
                ("closed", 2),
            )
            _, after_text = self.call(steward_ck, "/api/exceptions")
            closed_get = next(
                i for i in json.loads(after_text)["items"] if i["recovery_key"] == key
            )
            self.assertEqual(len(closed_get["audit_trail"]), 2)
            self.assertEqual(
                [e["action"] for e in closed_get["audit_trail"]],
                ["hold", "resolve_by_owner"],
            )
            for entry in closed_get["audit_trail"]:
                self.assertEqual(entry["by"], "u1@example.test")
                self.assertTrue(bool(entry["at"]))
                self.assertFalse(entry["replayed"])
                self.assertFalse(entry["released"])
            # Underlying eligibility and original source record remain untouched.
            self.assertEqual(closed_get["eligibility"], "Unknown")
            self.assertEqual(
                self.store.cases["ZF-1"]["stock_reconciliation"],
                [orig_query],
            )
            # Operator request_rerun records human request without replaying AI task.
            co, to = self.call(
                operator_ck,
                "/api/exceptions/recovery",
                {
                    "key": "failed_ai_run:R-EP-1",
                    "action": "request_rerun",
                    "reason": "Operator verified service health for manual re-run.",
                },
            )
            self.assertEqual(co, 200)
            rerun = json.loads(to)
            self.assertEqual(rerun["status"], "rerun_requested")
            rec = next(r for r in self.store.data["recommendations"] if r["id"] == "R-EP-1")
            self.assertEqual(rec["source"], "template")


if __name__ == "__main__":
    with mock.patch.dict("os.environ", {}):
        unittest.main()
