"""Versioned home case: links, shared building separation and retained versions."""

import tempfile
import unittest
from copy import deepcopy
from typing import Any

from building_fixture import fixture, open_store
from zava_forward.core import home_case
from zava_forward.core.store import ConflictError


def meta(version: int, **extra: Any) -> dict[str, Any]:
    return {
        "expected_version": version,
        "source": "SYN-CASE-REVIEW",
        "source_version": "1",
        "reason": "Check links before ordering",
        **extra,
    }


def seed() -> dict[str, Any]:
    data = fixture()
    data["schemes"] = [{"id": "SCH-1", "name": "Fictional scheme", "source": "SYN-SCHEME"}]
    return data


class HomeCaseTests(unittest.TestCase):
    def each_store(self) -> Any:
        for sql in (False, True):
            with tempfile.TemporaryDirectory() as folder:
                store = open_store(folder, sql, seed())
                try:
                    yield store
                finally:
                    if sql:
                        store.db.close()

    def test_version_starts_unrecorded_and_links_are_explicit(self) -> None:
        for store in self.each_store():
            sam = store.data["staff"][0]
            view = store.home_case_view(sam, "ZF-2")
            self.assertEqual(view["version"], 0)
            self.assertEqual(view["scheme"], {"status": "Unknown"})
            self.assertEqual(view["links"]["building_id"], "SYN-B1")
            self.assertEqual(view["links"]["work_packages"], [])
            self.assertFalse(view["changed_since_version"])
            self.assertIn("does not transfer", view["notice"])

    def test_recorded_versions_are_retained_and_conflicts_refused(self) -> None:
        for store in self.each_store():
            pam = store.data["staff"][1]
            first = store.home_case_record_version(pam, "ZF-2", meta(0, scheme_id="SCH-1"))
            self.assertEqual(first["version"], 1)
            self.assertEqual(first["links"]["scheme_id"], "SCH-1")
            self.assertEqual(first["building_record_version"], 1)
            with self.assertRaises(ConflictError):
                store.home_case_record_version(pam, "ZF-2", meta(0))
            store.cases["ZF-2"]["documents"].append(
                {"id": "NEW-DOC", "name": "Survey", "kind": "Survey"}
            )
            self.assertTrue(store.home_case_view(pam, "ZF-2")["changed_since_version"])
            second = store.home_case_record_version(pam, "ZF-2", meta(1))
            self.assertEqual(second["version"], 2)
            view = store.home_case_view(pam, "ZF-2")
            self.assertEqual([v["version"] for v in view["versions"]], [2, 1])
            self.assertNotIn("NEW-DOC", view["versions"][1]["links"]["document_ids"])
            self.assertIn("NEW-DOC", view["versions"][0]["links"]["document_ids"])
            self.assertFalse(view["changed_since_version"])
            self.assertEqual(view["scheme"]["name"], "Fictional scheme")

    def test_versions_survive_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            store = open_store(folder, True, seed())
            pam = store.data["staff"][1]
            store.home_case_record_version(pam, "ZF-2", meta(0, scheme_id="SCH-1"))
            store.db.close()
            reopened = open_store(folder, True)
            try:
                view = reopened.home_case_view(pam, "ZF-2")
                self.assertEqual(view["version"], 1)
                self.assertEqual(view["scheme"]["id"], "SCH-1")
            finally:
                reopened.db.close()

    def test_unknown_scheme_closed_case_and_missing_source_are_refused(self) -> None:
        for store in self.each_store():
            pam = store.data["staff"][1]
            before = deepcopy(store.cases["ZF-2"])
            with self.assertRaises(ValueError):
                store.home_case_record_version(pam, "ZF-2", meta(0, scheme_id="SCH-NOPE"))
            with self.assertRaises(ValueError):
                store.home_case_record_version(pam, "ZF-2", {"expected_version": 0})
            with self.assertRaises(ValueError):
                store.home_case_record_version(pam, "ZF-2", meta("0"))  # type: ignore[arg-type]
            self.assertEqual(store.cases["ZF-2"], before)
            store.cases["ZF-2"]["closed"] = True
            with self.assertRaises(ValueError):
                store.home_case_record_version(pam, "ZF-2", meta(0))

    def test_shared_building_id_never_transfers_evidence_between_homes(self) -> None:
        for store in self.each_store():
            pam = store.data["staff"][1]
            one = store.home_case_view(pam, "ZF-2")
            two = store.home_case_view(pam, "ZF-3")
            self.assertEqual(one["links"]["building_id"], two["links"]["building_id"])
            self.assertIn("SIBLING-EVIDENCE", two["links"]["document_ids"])
            self.assertNotIn("SIBLING-EVIDENCE", one["links"]["document_ids"])
            self.assertEqual(two["links"]["quality_measures"], ["Loft insulation"])
            self.assertEqual(one["links"]["quality_measures"], [])
            store.home_case_record_version(pam, "ZF-3", meta(0))
            self.assertEqual(store.home_case_view(pam, "ZF-2")["version"], 0)
            building = two["building"]
            self.assertNotIn("homes", building)
            for key in ("documents", "quality", "decision", "cost_allocation"):
                self.assertNotIn(key, building)
            self.assertEqual(building["costs"][0]["amount_gbp"], "12000.00")
            self.assertEqual(two["home"]["cost_allocation"][0]["amount_gbp"], "6000.00")

    def test_roles_and_finance_restriction(self) -> None:
        for store in self.each_store():
            sam = store.data["staff"][0]
            view = store.home_case_view(sam, "ZF-2")
            self.assertTrue(view["home"]["cost_allocation_restricted"])
            self.assertIsNone(view["home"]["cost_allocation"])
            self.assertTrue(view["building"]["costs_restricted"])
            contractor = {"email": "c@example.test", "code": "C-1", "role": "Contractor"}
            with self.assertRaises(PermissionError):
                store.home_case_view(contractor, "ZF-2")
            with self.assertRaises(PermissionError):
                store.home_case_record_version(contractor, "ZF-2", meta(0))
            with self.assertRaises(KeyError):
                store.home_case_view(sam, "ZF-NOPE")

    def test_scheme_registry_validation(self) -> None:
        self.assertEqual(home_case.schemes({}), {})
        with self.assertRaises(ValueError):
            home_case.schemes({"schemes": [{"id": "S", "name": "n"}]})


if __name__ == "__main__":
    unittest.main()
