"""Synthetic exact-scope decisions, authority, release and independent redress."""

import copy
import json
import os
import tempfile
import unittest
import uuid
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from functools import partial
from pathlib import Path
from threading import Barrier
from typing import Any
from unittest.mock import patch

from dataset import DATA, supplied_contract_fixture
from zava_forward.core import ai_tasks, controls, projection
from zava_forward.core.quality import checklist_for
from zava_forward.core.resident_decisions import resident_gate
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError, Store

MEASURES = ("Loft insulation", "Cavity wall")


class JsonResidentDecisions(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["cases"][0]["measures"] = list(MEASURES)
        data["staff"].extend(
            [
                dict(
                    code="RLO-2",
                    name="Rae Reviewer",
                    email="rae@example.test",
                    role="Resident Liaison Officer",
                ),
                dict(
                    code="RC-1",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-1",
                    name="Kim Contractor",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        self.sam, self.pam, self.rae, self.rex, self.kim = data["staff"]
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()
        self.store.technical_action(self.pam, "ZF-1", dict(action="design_submit", note="SYN"))

    def open_store(self) -> Store:
        if self.sql:
            store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.path))

    def action(self, action: str, **body: Any) -> None:
        self.store.resident_action(self.sam, "ZF-1", dict(action=action, **body))

    def scope(self, measure: str = MEASURES[0], design: int = 1) -> None:
        self.action(
            "scope_record", measure=measure, design_version=design, scope="SYN-SCOPE", source="SYN"
        )

    def answer(self, measure: str = MEASURES[0], status: str = "Accepted", **kw: Any) -> None:
        body = dict(
            measure=measure,
            context_revision=1,
            status=status,
            answered_by="The resident",
            source="SYN-SOURCE-CANARY",
            note="SYN-NOTE-CANARY",
        )
        body.update(kw)
        self.action("decision_record", **body)

    def authority(self, **kw: Any) -> None:
        body = dict(
            measure=MEASURES[0],
            context_revision=1,
            representative_ref="SYN-REP-A",
            status="Confirmed",
            tasks=["Works decision", "Receive information"],
            source="SYN-AUTH-CANARY",
            authority_date="2026-01-01",
            review_date="2099-01-01",
            resident_wishes="SYN-WISHES-CANARY",
            safe_contact_ref="SYN-SAFE-CANARY",
        )
        body.update(kw)
        self.action("representative_record", **body)

    def bind(self, *measures: str) -> list[dict[str, Any]]:
        return [dict(measure=m, context_revision=1) for m in measures]

    def unchanged_failure(self, operation: Callable[[], object]) -> None:
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        with self.assertRaises((ValueError, PermissionError, GateError, ConflictError)):
            operation()
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_first_contact_retention_withdrawn_expired_and_purge(self) -> None:
        from datetime import date

        from zava_forward.core.resident_decisions import retention_schedule

        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority(review_date="2026-02-01")
        self.answer(status="Withdrawn")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["contacts"] = [dict(at="2020-02-29T10:00", channel="Phone", outcome="SYN")]
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["service_requests"] = [
                dict(representative_ref="SYN-REP", outcome="SYN-COMPLAINT-OUTCOME")
            ]
            self.store.save()
        with patch("zava_forward.core.controls.today", return_value="2025-02-27"):
            schedule = retention_schedule(self.store.cases["ZF-1"])
            self.assertEqual(schedule["due"], "2025-02-28")
            self.assertFalse(schedule["expired"])
        with patch("zava_forward.core.controls.today", return_value="2025-02-28"):
            schedule = retention_schedule(self.store.cases["ZF-1"])
            self.assertTrue(schedule["expired"])
            rows = self.store.retention_due(self.pam, today=date(2025, 2, 28))["records"]
            self.assertTrue(any(r["doc_id"] == "resident-decisions" for r in rows))
            self.store.approve_retention_deletion(
                self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
            )
        again = self.open_store()
        c = again.cases["ZF-1"]
        for key in ("measure_decisions", "representative_authorities", "resident_safe_contact"):
            self.assertNotIn(key, c)
        self.assertNotIn("first_contact_at", c["resident"])
        self.assertEqual(c["decision"]["status"], "Not recorded")
        self.assertNotIn("SYN-WISHES-CANARY", json.dumps(c))
        self.assertEqual(len(c["contacts"]), 1)
        self.assertEqual(c["service_requests"], [dict(outcome="SYN-COMPLAINT-OUTCOME")])
        self.assertTrue(again.verify_audit())

    def test_returning_resident_general_contact_restarts_after_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        self.scope()
        self.answer()
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["contacts"] = [
                dict(at="2020-02-29T10:00"),
                dict(at="2025-02-28T10:00", note="SYN-OLD-CONTACT"),
            ]
            self.store.save()
        with patch("zava_forward.core.controls.today", return_value="2025-02-28"):
            self.store.approve_retention_deletion(
                self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
            )
            self.store = self.open_store()
            c = self.store.cases["ZF-1"]
            self.assertIsNone(retention_schedule(c)["first_contact"])
            self.assertIsNone(retention_schedule(c)["due"])
            self.assertFalse(retention_schedule(c)["expired"])
            self.assertTrue(resident_gate(c, self.bind(MEASURES[0])))
            self.unchanged_failure(lambda: self.answer())
            with patch("zava_forward.core.store.datetime") as clock:
                clock.now.return_value = datetime(2025, 2, 28, 10)
                self.store.log_call(self.sam, "ZF-1", "SYN-RETURN", "SYN-NEW-CONTACT")
            self.scope()
            self.answer()
            self.store = self.open_store()
            c = self.store.cases["ZF-1"]
            self.assertEqual(retention_schedule(c)["first_contact"], "2025-02-28")
            self.assertEqual(retention_schedule(c)["due"], "2030-02-28")
            self.assertFalse(resident_gate(c, self.bind(MEASURES[0])))
            self.assertEqual(len(c["contacts"]), 3)
            self.assertEqual(len(c["measure_decisions"][MEASURES[0]]), 1)
            self.assertTrue(self.store.verify_audit())

    def test_returning_resident_safe_contact_starts_once_not_at_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        self.scope()
        self.answer(status="Withdrawn")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["contacts"] = [dict(at="2020-02-29T10:00")]
            self.store.save()
        self.store.approve_retention_deletion(
            self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
        )
        with patch.object(controls, "today", return_value="2026-02-28"):
            self.assertIsNone(retention_schedule(self.open_store().cases["ZF-1"])["due"])
            self.scope()
            self.assertIsNone(retention_schedule(self.store.cases["ZF-1"])["due"])
            with patch.object(controls, "now", return_value="2026-02-28T10:00"):
                self.action("safe_contact_record", safe_contact_ref="SYN-NEW-SAFE", source="SYN")
            self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
            self.answer()
            self.store = self.open_store()
            self.assertEqual(retention_schedule(self.store.cases["ZF-1"])["due"], "2031-02-28")
            self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        with (
            patch.object(controls, "today", return_value="2027-03-01"),
            patch.object(controls, "now", return_value="2027-03-01T10:00"),
        ):
            self.action("safe_contact_record", safe_contact_ref="SYN-LATER-SAFE", source="SYN")
            self.answer(status="Withdrawn")
            c = self.open_store().cases["ZF-1"]
            self.assertEqual(retention_schedule(c)["first_contact"], "2026-02-28")
            self.assertEqual(retention_schedule(c)["due"], "2031-02-28")

    def test_renewed_period_expires_and_contact_cannot_reset_before_next_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2016-02-29"
            c["contacts"] = [dict(at="2016-02-29")]
            self.store.save()
        for deletion_day, contact_day, due_day in (
            ("2021-02-28", "2024-02-29", "2029-02-28"),
            ("2029-02-28", "2030-03-01", "2035-03-01"),
        ):
            with patch.object(controls, "today", return_value=deletion_day):
                self.assertTrue(retention_schedule(self.store.cases["ZF-1"])["expired"])
                with patch.object(controls, "now", return_value=deletion_day + "T09:00"):
                    self.action("safe_contact_record", safe_contact_ref="SYN-EXPIRED", source="SYN")
                self.scope()
                with self.assertRaises(GateError):
                    self.store.require_resident_clear(
                        self.store.cases["ZF-1"], self.bind(MEASURES[0])
                    )
                self.assertTrue(retention_schedule(self.store.cases["ZF-1"])["expired"])
                self.store.approve_retention_deletion(
                    self.pam, "ZF-1", "resident-decisions", today=date.fromisoformat(deletion_day)
                )
                self.assertIsNone(retention_schedule(self.open_store().cases["ZF-1"])["due"])
            with (
                patch.object(controls, "today", return_value=contact_day),
                patch("zava_forward.core.store.datetime") as clock,
            ):
                clock.now.return_value = datetime.fromisoformat(contact_day + "T10:00")
                self.store.log_call(self.sam, "ZF-1", "SYN-RETURN", "SYN")
                self.scope()
                self.answer()
                self.store = self.open_store()
                schedule = retention_schedule(self.store.cases["ZF-1"])
                self.assertEqual(schedule["first_contact"], contact_day)
                self.assertEqual(schedule["due"], due_day)
                self.assertFalse(schedule["expired"])
                self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        with patch.object(controls, "today", return_value="2035-03-01"):
            self.assertTrue(retention_schedule(self.store.cases["ZF-1"])["expired"])
            self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))

    def test_legacy_deletion_ignores_old_contacts_and_allows_later_contact(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["resident_retention_deleted_at"] = "2025-02-28"
            c["contacts"] = [
                dict(at="2020-02-29"),
                dict(at="2025-02-28T10:00"),
                dict(at="invalid"),
                dict(at="2099-01-01"),
            ]
            self.store.save()
        with (
            patch.object(controls, "today", return_value="2025-03-01"),
            patch("zava_forward.core.store.datetime") as clock,
        ):
            self.assertIsNone(retention_schedule(self.open_store().cases["ZF-1"])["due"])
            clock.now.return_value = datetime(2025, 3, 1, 10)
            self.store.log_call(self.sam, "ZF-1", "SYN-RETURN", "SYN")
            self.scope()
            self.answer()
            c = self.open_store().cases["ZF-1"]
            self.assertEqual(retention_schedule(c)["first_contact"], "2025-03-01")
            self.assertEqual(retention_schedule(c)["due"], "2030-03-01")
            self.assertFalse(resident_gate(c, self.bind(MEASURES[0])))

    def test_deletion_tombstone_contains_only_boundary_metadata(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["contacts"] = [dict(at="2020-02-29", note="SYN-PERSONAL-CONTACT")]
            self.store.save()
        self.store.approve_retention_deletion(
            self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
        )
        c = self.open_store().cases["ZF-1"]
        tombstone = {
            key: value for key, value in c.items() if key.startswith("resident_retention_")
        }
        self.assertEqual(
            tombstone,
            {
                "resident_retention_deleted_at": "2025-02-28",
                "resident_retention_tombstone": {"contacts_before_deletion": 1},
            },
        )
        self.assertIs(
            type(tombstone["resident_retention_tombstone"]["contacts_before_deletion"]), int
        )
        for personal in (
            "SYN-SAFE-CANARY",
            "SYN-WISHES-CANARY",
            "SYN-AUTH-CANARY",
            "SYN-REP-A",
            "SYN-NOTE-CANARY",
            "SYN-PERSONAL-CONTACT",
            self.sam["name"],
            self.sam["email"],
        ):
            self.assertNotIn(personal, json.dumps(tombstone))
        self.assertNotIn("first_contact_at", c["resident"])
        for key in (
            "resident_scopes",
            "measure_decisions",
            "representative_authorities",
            "resident_safe_contact",
            "resident_contact_history",
            "resident_reviews",
        ):
            self.assertNotIn(key, c)
        self.assertEqual(c["contacts"][0]["note"], "SYN-PERSONAL-CONTACT")
        self.assertTrue(self.store.verify_audit())

    def test_matrix_registered_writer_and_exact_private_fields(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer()
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["adjustment"] = "SYN-VULNERABILITY"
            c["contacts"] = [
                dict(
                    at="2026-10-16",
                    channel="Phone",
                    outcome="SYN-CONTACT-OUTCOME",
                    note="SYN-CONTACT-NOTE",
                    by="Sam Example",
                )
            ]
            self.store.save()
        with patch.dict("os.environ", {"ZF_REASON_ROLES": ""}):
            for role in controls.RESIDENT_VIEW_ROLES:
                text = json.dumps(self.store.detail("ZF-1", dict(self.sam, role=role)))
                for visible in ("SYN-WISHES-CANARY", "SYN-SAFE-CANARY", "SYN-NOTE-CANARY"):
                    self.assertIn(visible, text)
                for held in ("SYN-VULNERABILITY", "SYN-CONTACT-NOTE", "SYN-CONTACT-OUTCOME"):
                    self.assertNotIn(held, text)
        self.assertNotIn(
            "SYN-WISHES-CANARY",
            json.dumps(self.store.detail("ZF-1", dict(self.sam, role="Quality Inspector"))),
        )
        for actor in (self.pam, dict(self.sam, email="agent@example.test")):
            self.unchanged_failure(
                partial(
                    self.store.resident_action,
                    actor,
                    "ZF-1",
                    dict(action="safe_contact_record", safe_contact_ref="FORGED", source="FORGED"),
                )
            )
            self.unchanged_failure(partial(self.store.set_decision, actor, "ZF-1", "Accepted"))
        detail = self.store.detail("ZF-1", self.rex)
        self.assertEqual(detail["resident_safe_contact"], "SYN-SAFE-CANARY")
        self.assertEqual(detail["measure_decisions"][0]["versions"][0]["note"], "SYN-NOTE-CANARY")
        self.assertIn("SYN-WISHES-CANARY", json.dumps(detail))
        flags = self.store.detail("ZF-1", self.kim)["resident_readiness"]
        self.assertEqual(
            flags,
            [dict(measure=MEASURES[0], flag="Proceed"), dict(measure=MEASURES[1], flag="Hold")],
        )

    def test_first_contact_evidence_is_not_decision_date_and_stays_until_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        with patch.object(controls, "today", return_value="2026-10-16"):
            c = copy.deepcopy(self.store.cases["ZF-1"])
            c["decision"]["at"] = "2020-01-01"
            c["contacts"] = [dict(at="invalid"), dict(at="2099-01-01")]
            self.assertIsNone(retention_schedule(c)["due"])
            c["contacts"].append(dict(at="2022-10-17T10:00"))
            self.assertEqual(retention_schedule(c)["due"], "2027-10-17")
            c["resident"]["first_contact_at"] = "2024-01-01"
            self.assertEqual(retention_schedule(c)["due"], "2027-10-17")
            with patch("zava_forward.core.resident_decisions.RESIDENT_RETENTION_YEARS", 2):
                self.assertEqual(retention_schedule(c)["due"], "2024-10-17")
        with (
            patch.object(controls, "today", return_value="2026-10-16"),
            patch.object(controls, "now", return_value="2026-10-16T10:00"),
        ):
            self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.assertEqual(retention_schedule(self.store.cases["ZF-1"])["due"], "2031-10-16")
        self.store.log_call(self.sam, "ZF-1", "SYN", "SYN")
        self.assertEqual(
            self.open_store().cases["ZF-1"]["resident"]["first_contact_at"], "2026-10-16"
        )

    def test_retention_anniversary_holds_disclosure_and_legal_hold_blocks_purge(self) -> None:
        from datetime import date

        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2021-10-16"
            self.store.save()
        disclosure = dict(
            measure=MEASURES[0],
            context_revision=1,
            representative_ref="SYN-REP-A",
            task="Receive information",
        )
        with patch.object(controls, "today", return_value="2026-10-15"):
            self.action("disclosure_check", **disclosure)
            self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        with patch.object(controls, "today", return_value="2026-10-16"):
            for held in (False, True):
                with self.store.lock:
                    self.store._case("ZF-1")["legal_hold"] = dict(active=held)
                    self.store.save()
                self.unchanged_failure(lambda: self.action("disclosure_check", **disclosure))
                self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
            self.unchanged_failure(
                lambda: self.store.approve_retention_deletion(
                    self.pam, "ZF-1", "resident-decisions", today=date(2026, 10, 16)
                )
            )

    def test_unknown_scope_source_and_no_contact_or_legacy_inference(self) -> None:
        self.store.log_call(self.sam, "ZF-1", "Happy to go ahead", "Access agreed")
        self.store.set_decision(self.sam, "ZF-1", "Accepted")
        d = self.store.detail("ZF-1")
        self.assertEqual([m["status"] for m in d["measure_decisions"]], ["Not recorded"] * 2)
        self.assertTrue(resident_gate(self.store.cases["ZF-1"]))
        self.unchanged_failure(lambda: self.answer())
        self.scope()
        self.unchanged_failure(lambda: self.answer(source=""))
        self.unchanged_failure(lambda: self.answer(status=""))
        self.unchanged_failure(lambda: self.answer(context_revision=True))
        self.unchanged_failure(lambda: self.answer(context_revision=2))
        self.answer()
        d = self.store.detail("ZF-1")
        self.assertEqual(
            [m["status"] for m in d["measure_decisions"]], ["Accepted", "Not recorded"]
        )
        a = d["measure_decisions"][0]["versions"][0]
        self.assertEqual(
            (a["case_id"], a["measure"], a["scope"], a["design_version"], a["source"]),
            ("ZF-1", MEASURES[0], "SYN-SCOPE", 1, "SYN-SOURCE-CANARY"),
        )
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.kim, "ZF-1", dict(action="decision_record", measure=MEASURES[0])
            )
        )

    def test_design_change_and_switch_back_never_restore_old_acceptance(self) -> None:
        self.scope()
        self.answer()
        history = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"])
        self.store.technical_action(
            self.pam, "ZF-1", dict(action="design_change", note="SYN-CHANGED")
        )
        self.assertIsNone(self.store.detail("ZF-1")["measure_decisions"][0]["context"])
        self.assertTrue(resident_gate(self.store.cases["ZF-1"]))
        self.unchanged_failure(lambda: self.scope(design=1))
        self.unchanged_failure(lambda: self.scope(design=3))
        self.scope(design=2)
        self.assertEqual(
            self.store.detail("ZF-1")["measure_decisions"][0]["status"], "Not recorded"
        )
        self.scope(design=2)
        self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], history)
        self.answer(context_revision=3)
        self.assertFalse(
            resident_gate(self.store.cases["ZF-1"], [dict(measure=MEASURES[0], context_revision=3)])
        )

    def test_authority_tasks_versions_dates_safe_contact_and_multiple_representatives(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN-CONTACT")
        self.authority(tasks=["Attend", "Communicate"])
        self.unchanged_failure(
            lambda: self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        )
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.authority(representative_ref="SYN-REP-B", tasks=["Attend"])
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        for status in ("Disputed", "Unclear", "Revoked"):
            self.authority(status=status)
            self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
            self.unchanged_failure(
                lambda: self.action(
                    "disclosure_check",
                    measure=MEASURES[0],
                    context_revision=1,
                    representative_ref="SYN-REP-A",
                    task="Receive information",
                )
            )
        self.authority()
        self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        self.authority(review_date="2027-01-01")
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        for today, held in (("2026-12-31", False), ("2027-01-01", True)):
            with patch.object(controls, "today", return_value=today):
                self.assertEqual(
                    bool(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0]))), held
                )
        self.action("safe_contact_record", safe_contact_ref="SYN-NEW-SAFE", source="SYN-CHANGE")
        self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN-RETURN")
        self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.answer()
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        for bad in (
            dict(authority_date="2099-01-01"),
            dict(review_date="2025-01-01"),
            dict(review_date="invalid"),
            dict(tasks=["Approve everything"]),
            dict(source=""),
            dict(resident_wishes=""),
        ):
            self.unchanged_failure(partial(self.authority, **bad))

    def package(self) -> str:
        pid = self.store.create_package(
            self.pam, "SYN", "2026-01-01", "2099-01-01", "SYN-SCOPE", "SYN-CONTRACT", "SYN-1"
        )
        details = supplied_contract_fixture(self.store, pid, self.pam)
        self.store.set_capacity(self.pam, pid, "Test Ltd", 5, 5, "SYN-CAPACITY", details)
        assert isinstance(pid, str)
        return pid

    def test_pause_withdrawal_dependency_isolation_and_evidenced_restart(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        pid = self.package()
        wid_a = self.store.issue_work_order(
            self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
        )
        # Separate packages permit independent work orders on this same home.
        pid_b = self.package()
        wid_b = self.store.issue_work_order(
            self.pam, pid_b, "ZF-1", resident_bindings=self.bind(MEASURES[1])
        )
        sibling = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[1]])
        for status in ("Paused", "Withdrawn"):
            self.answer(status=status)
            self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[1]], sibling)
            for bindings in ([], self.bind(MEASURES[0]), self.bind(*MEASURES)):
                self.assertTrue(resident_gate(self.store.cases["ZF-1"], bindings))
            self.unchanged_failure(
                lambda: self.store.record_wo_appointment(self.pam, wid_a, "Booked", "2098-01-01")
            )
        self.store.record_wo_appointment(self.pam, wid_b, "Booked", "2098-01-01")
        self.store.complete_work_order(self.pam, wid_b)
        self.unchanged_failure(
            lambda: self.store.correct_work_order(
                self.pam, wid_b, "SYN", resident_bindings=self.bind(MEASURES[0])
            )
        )
        self.unchanged_failure(
            lambda: self.store.reissue_work_order(self.pam, wid_a, "Changed", "SYN")
        )
        self.unchanged_failure(lambda: self.answer())
        self.answer(review_ref="SYN-HUMAN-REVIEW")
        self.store.record_wo_appointment(self.pam, wid_a, "Booked", "2098-01-01")
        self.assertEqual(
            self.store.cases["ZF-1"]["resident_reviews"][MEASURES[0]]["status"],
            "Reviewed with supplied acceptance",
        )
        self.assertTrue(self.store.verify_audit())

    def test_resident_acceptance_never_clears_technical_or_hazard_gates(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        with self.store.lock:
            c = self.store._case("ZF-1")
            c.update(stage="Final checks before ordering", funding_ok=True)
            self.store.save()
        self.assertFalse(resident_gate(self.store.cases["ZF-1"]))
        self.assertIn("sign-off", " ".join(self.store.detail("ZF-1")["gate"]))
        self.unchanged_failure(lambda: self.store.advance(self.pam, "ZF-1"))
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["technical"]["signoffs"] = {
                key: dict(status="Signed off", history=[])
                for key in ("assessment", "design", "building", "coordination")
            }
            c["documents"] = [
                dict(id=f"SYN-{kind}", kind=kind, generated=False) for kind in self.store.EVIDENCE
            ]
            self.store.save()
        self.assertEqual(self.store.detail("ZF-1")["gate"], [])
        self.store.technical_action(
            self.pam, "ZF-1", dict(action="signoff_return", type="coordination", reason="SYN")
        )
        technical = copy.deepcopy(self.store.cases["ZF-1"]["technical"])
        self.answer(status="Withdrawn")
        self.answer(review_ref="SYN-HUMAN-REVIEW")
        self.assertEqual(self.store.cases["ZF-1"]["technical"], technical)
        self.unchanged_failure(lambda: self.store.advance(self.pam, "ZF-1"))
        self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Electrical",
            "Emergency",
            metadata=dict(source="SYN", aware_at="2026-01-01T10:00:00Z"),
        )
        hazards = copy.deepcopy(self.store.cases["ZF-1"]["hazards"])
        self.answer(status="Withdrawn")
        self.answer(review_ref="SYN-HUMAN-REVIEW")
        self.assertEqual(self.store.cases["ZF-1"]["hazards"], hazards)
        self.assertEqual(self.store.cases["ZF-1"]["technical"], technical)
        self.assertFalse(resident_gate(self.store.cases["ZF-1"]))
        self.unchanged_failure(lambda: self.store.advance(self.pam, "ZF-1"))
        pid = self.package()
        self.unchanged_failure(
            lambda: self.store.issue_work_order(
                self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[1])
            )
        )

    def test_redress_independence_no_detriment_and_closed_case_access(self) -> None:
        self.scope()
        self.answer(status="Paused")
        before = copy.deepcopy(self.store.cases["ZF-1"])
        base = dict(
            route="Independent review",
            review_measure=MEASURES[0],
            review_decision_version=1,
            review_reference="SYN-REVIEW",
            summary="SYN",
            desired_outcome="Speak to a person",
            next_update="2099-01-01",
            service_owner=self.pam["email"],
            redress_owner=self.rae["email"],
        )
        self.unchanged_failure(
            lambda: self.action("service_open", **dict(base, redress_owner=self.sam["email"]))
        )
        self.action("service_open", **base)
        update = dict(
            action="service_update", id="SR-1", status="Resolved", next_update="2099-01-01"
        )
        self.unchanged_failure(lambda: self.store.resident_action(self.pam, "ZF-1", update))
        self.store.resident_action(self.rae, "ZF-1", update)
        self.unchanged_failure(lambda: self.action("service_close", id="SR-1", note="SYN"))
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN")
        )
        with self.store.lock:
            self.store._case("ZF-1")["closed"] = True
            self.store.save()
        self.action("service_open", **dict(base, route="Complaint"))
        for key in ("measure_decisions", "resident_reviews", "decision", "hazards", "stage"):
            self.assertEqual(self.store.cases["ZF-1"][key], before[key])
        self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Electrical",
            "Emergency",
            metadata=dict(source="SYN", aware_at="2026-01-01T10:00:00Z"),
        )
        self.assertTrue(self.store.cases["ZF-1"]["closed"])

    def commitment(self, **kw: Any) -> None:
        body = dict(
            expected_version=0,
            purpose="SYN update about remedy",
            owner=self.sam["email"],
            due_at="2099-01-01T12:00:00Z",
            basis="SYN human-selected fixture date",
            safe_contact_ref="Unknown",
            status="Outstanding",
        )
        body.update(kw)
        self.action("update_record", **body)

    def request(self, route: str = "Complaint") -> None:
        self.action(
            "service_open",
            route=route,
            summary="SYN issue",
            desired_outcome="SYN remedy requested",
            service_owner=self.sam["email"],
            redress_owner=self.rae["email"],
            next_update="2099-01-01",
        )

    def register_followup_actor(self, actor: dict[str, Any]) -> None:
        if self.sql:
            assert isinstance(self.store, SqlStore)
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(actor), actor["email"])
            )
        else:
            self.store.staff[actor["email"]] = copy.deepcopy(actor)

    def test_response_reassignment_status_clock_follows_responsibility_not_shared_person(
        self,
    ) -> None:
        self.scope()
        self.answer()
        for route in ("Service request", "Complaint", "Independent review"):
            service_owner = self.rae if route == "Service request" else self.sam
            for status in ("Open", "Closed"):
                for responsibility in ("service", "redress"):
                    for legacy in (False, True):
                        with self.subTest(
                            route=route, status=status, responsibility=responsibility, legacy=legacy
                        ):
                            self.store.resident_action(
                                self.pam,
                                "ZF-1",
                                dict(
                                    action="service_open",
                                    route=route,
                                    summary="SYN responsibility clock",
                                    desired_outcome="SYN separate remedy",
                                    service_owner=service_owner["email"],
                                    redress_owner=self.rae["email"],
                                    next_update="2099-01-01",
                                    review_measure=MEASURES[0],
                                    review_decision_version=1,
                                    review_reference="SYN recorded decision",
                                ),
                            )
                            req = self.store.cases["ZF-1"]["service_requests"][-1]
                            request_id = req["id"]
                            if status == "Closed":
                                self.store.resident_action(
                                    self.rae,
                                    "ZF-1",
                                    dict(
                                        action="service_update",
                                        id=request_id,
                                        status="Resolved",
                                        next_update="2099-01-01",
                                    ),
                                )
                                self.store.resident_action(
                                    self.rae,
                                    "ZF-1",
                                    dict(
                                        action="service_close",
                                        id=request_id,
                                        note="SYN response only",
                                    ),
                                )
                            if legacy:
                                with self.store.lock:
                                    req = self.store._case("ZF-1")["service_requests"][-1]
                                    req.pop("status_owner")
                                    req.pop("status_at")
                                    self.store.save()
                            before = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][-1])
                            self.store.resident_action(
                                self.pam,
                                "ZF-1",
                                dict(
                                    action="service_reassign",
                                    id=request_id,
                                    expected_version=before["version"],
                                    responsibility=responsibility,
                                    owner=self.rex["email"],
                                    note="SYN explicit responsibility",
                                ),
                            )
                            current = self.open_store().cases["ZF-1"]["service_requests"][-1]
                            status_key = (
                                "redress"
                                if status == "Closed" or route == "Independent review"
                                else "service"
                            )
                            if responsibility == status_key:
                                self.assertEqual(
                                    current["status_owner"]["email"], self.rex["email"]
                                )
                                self.assertNotEqual(current["status_at"], before.get("status_at"))
                                self.assertEqual(current["status_at"], current["history"][-1]["at"])
                            else:
                                for field in ("status_owner", "status_at"):
                                    self.assertEqual(current.get(field), before.get(field))
                                    self.assertEqual(field in current, field in before)
                            other = "redress" if responsibility == "service" else "service"
                            for suffix in ("_owner", "_owner_email", "_identity"):
                                self.assertEqual(current[other + suffix], before[other + suffix])
                            self.assertEqual(
                                current[responsibility + "_identity"]["email"], self.rex["email"]
                            )
                            self.assertEqual(current["remedy"], before["remedy"])
                            self.assertEqual(current["opened_at"], before["opened_at"])
                            self.assertEqual(current["status"], before["status"])
                            self.assertEqual(current["version"], before["version"] + 1)
                            self.assertEqual(current["history"][:-1], before["history"])
                            self.assertEqual(
                                current["history"][-1]["old_status_owner"],
                                before.get("status_owner"),
                            )
                            self.assertEqual(
                                current["history"][-1]["old_status_at"], before.get("status_at")
                            )
                            self.assertTrue(self.store.verify_audit())

    def test_departed_response_owners_explicit_recovery_keeps_other_clocks(self) -> None:
        self.request()
        original = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][0])
        self.register_followup_actor(dict(self.sam, role="Contractor"))
        for actor in (self.pam, self.rae):
            self.unchanged_failure(
                partial(
                    self.store.resident_action,
                    actor,
                    "ZF-1",
                    dict(
                        action="service_update",
                        id="SR-1",
                        status="Resolved",
                        next_update="2099-01-01",
                    ),
                )
            )
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-1",
                expected_version=1,
                responsibility="service",
                owner=self.rex["email"],
                note="SYN officer departure",
            ),
        )
        recovered = self.open_store().cases["ZF-1"]["service_requests"][0]
        self.assertEqual(recovered["service_identity"]["email"], self.rex["email"])
        self.assertEqual(recovered["status_owner"]["email"], self.rex["email"])
        self.assertNotEqual(recovered["status_at"], original["status_at"])
        self.assertEqual(recovered["remedy"], original["remedy"])
        event = recovered["history"][-1]
        self.assertEqual(event["changes"]["old"], original["service_identity"])
        self.assertEqual(event["changes"]["new"], recovered["service_identity"])
        self.assertEqual(event["actor"]["email"], self.pam["email"])
        self.assertEqual(event["note"], "SYN officer departure")
        self.assertEqual(event["old_status_at"], original["status_at"])
        self.store.resident_action(
            self.rex,
            "ZF-1",
            dict(action="service_update", id="SR-1", status="Resolved", next_update="2099-01-01"),
        )
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response")
        )
        closed = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][0])
        self.register_followup_actor(dict(self.rae, role="Quality Inspector"))
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-1",
                expected_version=closed["version"],
                responsibility="redress",
                owner=self.pam["email"],
                note="SYN reviewer departure",
            ),
        )
        current = self.store.cases["ZF-1"]["service_requests"][0]
        self.assertEqual(current["status"], "Closed")
        self.assertEqual(current["history"][-1]["changes"]["old"], original["redress_identity"])
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reopen",
                id="SR-1",
                expected_version=current["version"],
                note="SYN reopen",
            ),
        )
        self.store.resident_action(
            self.rex,
            "ZF-1",
            dict(action="service_update", id="SR-1", status="Resolved", next_update="2099-01-01"),
        )
        self.store.resident_action(
            self.pam, "ZF-1", dict(action="service_close", id="SR-1", note="SYN second response")
        )
        final = self.open_store().cases["ZF-1"]["service_requests"][0]
        self.assertEqual(final["status_owner"]["email"], self.pam["email"])
        self.assertEqual(final["remedy"], original["remedy"])
        self.assertEqual(final["opened_at"], original["opened_at"])
        self.assertEqual(final["history"][: len(closed["history"])], closed["history"])
        self.assertTrue(self.store.verify_audit())

    def test_response_reassignment_requires_current_manager_version_and_independence(self) -> None:
        self.request()
        body = dict(
            action="service_reassign",
            id="SR-1",
            expected_version=1,
            responsibility="service",
            owner=self.rex["email"],
            note="SYN recovery",
        )
        for actor, changes in (
            (self.sam, {}),
            (self.kim, {}),
            (self.pam, {"expected_version": 0}),
            (self.pam, {"expected_version": True}),
            (self.pam, {"owner": ""}),
            (self.pam, {"owner": "unknown@example.test"}),
            (self.pam, {"owner": self.kim["email"]}),
            (self.pam, {"owner": self.rae["email"]}),
            (self.pam, {"note": ""}),
            (self.pam, {"responsibility": "remedy"}),
        ):
            with self.subTest(actor=actor["code"], changes=changes):
                self.unchanged_failure(
                    partial(self.store.resident_action, actor, "ZF-1", dict(body, **changes))
                )
        self.register_followup_actor(dict(self.pam, role="Contractor"))
        self.unchanged_failure(lambda: self.store.resident_action(self.pam, "ZF-1", body))
        self.register_followup_actor(self.pam)
        self.scope()
        self.answer()
        self.action(
            "service_open",
            route="Independent review",
            summary="SYN review",
            desired_outcome="SYN independent response",
            service_owner=self.rex["email"],
            redress_owner=self.rae["email"],
            next_update="2099-01-01",
            review_measure=MEASURES[0],
            review_decision_version=1,
            review_reference="SYN decision",
        )
        review_body = dict(body, id="SR-2", responsibility="redress")
        for owner in (self.sam["email"], self.rex["email"]):
            self.unchanged_failure(
                partial(
                    self.store.resident_action, self.pam, "ZF-1", dict(review_body, owner=owner)
                )
            )
        self.register_followup_actor(dict(self.rae, role="Contractor"))
        self.store.resident_action(self.pam, "ZF-1", dict(review_body, owner=self.pam["email"]))
        review = self.store.cases["ZF-1"]["service_requests"][1]
        self.assertEqual(review["status_owner"]["email"], self.pam["email"])
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.rex,
                "ZF-1",
                dict(
                    action="service_update", id="SR-2", status="Resolved", next_update="2099-01-01"
                ),
            )
        )
        for action, changes in (
            ("service_update", dict(status="Resolved", next_update="2099-01-01")),
            ("service_close", dict(note="SYN independent outcome")),
            ("service_reopen", dict(expected_version=4, note="SYN independent reopen")),
        ):
            self.store.resident_action(self.pam, "ZF-1", dict(action=action, id="SR-2", **changes))
        self.assertEqual(
            self.store.cases["ZF-1"]["service_requests"][1]["status_owner"]["email"],
            self.pam["email"],
        )
        with self.store.lock:
            req = self.store._case("ZF-1")["service_requests"][0]
            req.pop("service_identity")
            req.pop("status_owner")
            req.pop("status_at")
            self.store.save()
        self.store.resident_action(self.pam, "ZF-1", body)
        event = self.open_store().cases["ZF-1"]["service_requests"][0]["history"][-1]
        self.assertIsNone(event["changes"]["old"])
        self.assertEqual(event["old_owner_email"], self.sam["email"])
        self.assertIsNone(event["old_status_at"])
        self.assertEqual(event["changes"]["new"]["email"], self.rex["email"])

    def test_complete_update_and_explicit_reassignment_preserve_history(self) -> None:
        self.commitment()
        first = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])
        self.commitment(expected_version=1, owner=self.rae["email"], status="Proposed")
        update = self.open_store().detail("ZF-1")["resident_update"]
        self.assertEqual(update["version"], 2)
        self.assertEqual(update["owner_identity"]["email"], self.rae["email"])
        first.pop("history")
        self.assertEqual(update["history"][-1]["old"], first)
        self.assertEqual(update["due_at"], "2099-01-01T12:00:00+00:00")
        self.assertNotIn("sent_at", update)
        self.assertNotIn("completed_at", update)
        self.assertEqual(update["basis"], "SYN human-selected fixture date")
        self.unchanged_failure(lambda: self.commitment(expected_version=1))
        self.unchanged_failure(lambda: self.commitment(expected_version=2))
        self.assertTrue(self.store.verify_audit())

    def test_incomplete_commitments_dates_and_identity_fail_without_mutation(self) -> None:
        for field, value in (
            ("purpose", ""),
            ("basis", ""),
            ("owner", "missing@example.test"),
            ("due_at", "2099-01-01"),
            ("due_at", "2099-02-30T12:00:00Z"),
            ("expected_version", True),
            ("status", "Sent"),
        ):
            with self.subTest(field=field, value=value):
                self.unchanged_failure(partial(self.commitment, **{field: value}))
        self.unchanged_failure(
            lambda: self.store.resident_action(
                dict(self.sam, oid="SYN-forged"), "ZF-1", dict(action="update_record")
            )
        )
        self.unchanged_failure(
            lambda: self.action(
                "service_open",
                route="Complaint",
                service_owner=self.sam["email"],
                redress_owner=self.rae["email"],
                summary="SYN",
                desired_outcome="SYN",
                next_update="2099-02-30",
            )
        )

    def test_response_and_remedy_close_and_reopen_are_independent(self) -> None:
        self.request()
        original = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][0]["remedy"])
        self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response")
        )
        req = self.open_store().cases["ZF-1"]["service_requests"][0]
        self.assertEqual(req["status"], "Closed")
        self.assertEqual(req["remedy"], original)
        self.assertEqual(req["status_owner"]["email"], self.rae["email"])
        self.assertTrue(req["status_at"])
        self.unchanged_failure(
            lambda: self.action(
                "remedy_update", id="SR-1", expected_version=1, status="Resolved", note="SYN"
            )
        )
        for version, status in ((1, "Resolved"), (2, "Closed"), (3, "Open")):
            self.store.resident_action(
                self.rae,
                "ZF-1",
                dict(
                    action="remedy_update",
                    id="SR-1",
                    expected_version=version,
                    status=status,
                    note="SYN remedy",
                ),
            )
            current = self.open_store().cases["ZF-1"]["service_requests"][0]
            self.assertEqual(current["status"], "Closed")
            self.assertEqual(current["remedy"]["opened_at"], original["opened_at"])
            self.assertEqual(current["remedy"]["status"], status)
        remedy = copy.deepcopy(current["remedy"])
        self.action("service_reopen", id="SR-1", expected_version=3, note="SYN response only")
        self.assertEqual(self.store.cases["ZF-1"]["service_requests"][0]["remedy"], remedy)
        self.assertEqual(self.store.cases["ZF-1"]["service_requests"][0]["status"], "Open")

    def test_legacy_confirmation_preserves_unknown_history_and_closed_response(self) -> None:
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident_update"] = dict(owner="Legacy unknown person", due_at=None)
            c["service_requests"] = [
                dict(
                    id="SR-1",
                    route="Complaint",
                    status="Closed",
                    service_owner="Old",
                    service_owner_email="absent@example.test",
                    redress_owner="Old",
                    redress_owner_email="absent@example.test",
                    history=[],
                )
            ]
            self.store.save()
        old = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])
        projected = self.store.detail("ZF-1")
        self.assertIsNone(projected["service_requests"][0]["remedy"]["opened_at"])
        self.assertEqual(projected["service_requests"][0]["remedy"]["status"], "Unknown")
        self.unchanged_failure(
            lambda: self.action(
                "remedy_update", id="SR-1", expected_version=0, status="Resolved", note="SYN"
            )
        )
        self.commitment()
        update = self.store.cases["ZF-1"]["resident_update"]
        self.assertEqual(update["history"][0]["old"], old)
        self.assertIsNone(update["opened_at"])
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="remedy_confirm",
                id="SR-1",
                expected_version=0,
                owner=self.rae["email"],
                basis="SYN new responsibility",
            ),
        )
        req = self.open_store().detail("ZF-1")["service_requests"][0]
        self.assertEqual(req["status"], "Closed")
        self.assertIsNone(req["status_owner"])
        self.assertIsNone(req["status_at"])
        self.assertIsNone(req["remedy"]["opened_at"])
        self.assertEqual(req["remedy"]["history"][0]["old"], None)
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.pam,
                "ZF-1",
                dict(
                    action="remedy_confirm",
                    id="SR-1",
                    expected_version=0,
                    owner=self.rae["email"],
                    basis="SYN",
                ),
            )
        )

    def test_actionable_owner_roles_projection_and_captured_identity(self) -> None:
        self.unchanged_failure(lambda: self.commitment(owner=self.kim["email"]))
        self.unchanged_failure(lambda: self.commitment(owner=self.rex["role"]))
        self.commitment()
        self.request()
        for actor in (self.sam, self.pam, self.rae):
            self.assertIn("resident_update", self.store.detail("ZF-1", actor))
        self.assertNotIn("resident_update", self.store.detail("ZF-1", self.kim))
        self.assertNotIn("service_requests", self.store.detail("ZF-1", self.kim))
        self.assertNotIn("SYN update about remedy", self.store._facts(self.store.cases["ZF-1"]))
        # A current manager may explicitly take responsibility, not impersonate the old owner.
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="remedy_update",
                id="SR-1",
                expected_version=1,
                status="In progress",
                owner=self.sam["email"],
                note="SYN reassign",
            ),
        )
        req = self.store.cases["ZF-1"]["service_requests"][0]
        self.assertEqual(req["remedy"]["owner"]["email"], self.sam["email"])
        self.assertEqual(req["remedy"]["history"][-1]["old"]["owner"]["email"], self.rae["email"])
        self.assertEqual(req["remedy"]["history"][-1]["actor"]["email"], self.pam["email"])

    def test_mixed_closure_clocks_survive_unrelated_transitions_and_restart(self) -> None:
        self.commitment()
        for route in ("Complaint", "Defect", "Charge query"):
            self.request(route)
        self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response only")
        )
        expected = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"])
        commitment = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])

        def retained() -> None:
            case = self.open_store().detail("ZF-1")
            self.assertEqual(case["service_requests"], expected)
            self.assertEqual(case["resident_update"], commitment)
            self.assertEqual(case["service_requests"][0]["status"], "Closed")
            self.assertEqual(case["service_requests"][0]["remedy"]["status"], "Open")

        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        pid = self.package()
        wid = self.store.issue_work_order(
            self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
        )
        self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
        self.store.complete_work_order(self.pam, wid, "SYN physical completion only")
        order = self.store._work_order(wid)
        self.assertEqual(order["completed_by"], self.pam["name"])
        self.assertTrue(order["completed_at"])
        retained()
        for index, measure in enumerate(MEASURES):
            self.store.submit_quality(
                self.sam,
                "ZF-1",
                measure,
                "Synthetic installer",
                "Installer",
                {label: "SYN evidence" for label in checklist_for(measure)["items"]},
                context_revision=1,
            )
            if index == 0:
                self.store.accept_quality(self.pam, "ZF-1", index)
                self.store.hand_over_quality(self.pam, "ZF-1", index, "SYN guarantees", True)
                handed = self.store.cases["ZF-1"]["quality"][0]["handover"]
                self.assertEqual(handed["by"], self.pam["name"])
                self.assertTrue(handed["at"])
            else:
                self.store.return_quality(
                    self.pam, "ZF-1", index, "SYN return", "SYN defect", self.rae["name"]
                )
                defect = copy.deepcopy(self.store.cases["ZF-1"]["quality"][index]["defect"])
                self.assertEqual(defect["owner"], self.rae["name"])
                self.assertTrue(defect["raised_at"])
            retained()
        self.store.finance_action(
            self.pam,
            "ZF-1",
            dict(
                action="invoice_receive",
                supplier="Test Ltd",
                work_order=wid,
                ref="SYN-INV",
                kind="Invoice",
                lines=[dict(measure=MEASURES[0], quantity=1, amount=10, milestone_ref="SYN")],
            ),
        )
        self.store.finance_action(
            self.pam, "ZF-1", dict(action="payment_status", id="INV-1", status="Not payable yet")
        )
        invoice = self.store.cases["ZF-1"]["finance"]["invoices"][0]
        self.assertEqual(invoice["payment_status_owner"]["email"], self.pam["email"])
        self.assertTrue(invoice["payment_status_at"])
        retained()
        with self.store.lock:
            self.store._case("ZF-1").update(stage="Completed", closed=True)
            self.store.save()
        self.store.reopen_case(
            self.pam,
            "ZF-1",
            "SYN reopening",
            metadata=dict(source="SYN", next_action="SYN aftercare"),
        )
        retained()
        self.store.return_case(
            self.sam,
            "ZF-1",
            "Contacting resident",
            "SYN return",
            metadata=dict(source="SYN", next_action="SYN next action"),
        )
        retained()
        self.assertEqual(self.open_store().cases["ZF-1"]["quality"][1]["defect"], defect)
        self.store.resident_action(
            self.rae,
            "ZF-1",
            dict(
                action="remedy_update",
                id="SR-3",
                expected_version=1,
                status="Resolved",
                note="SYN charge query progress",
            ),
        )
        current = self.open_store().cases["ZF-1"]["service_requests"]
        self.assertEqual(current[:2], expected[:2])
        self.assertEqual(current[2]["status"], "Open")
        self.assertEqual(current[2]["remedy"]["status"], "Resolved")

    def test_handoff_cannot_create_partial_commitment_or_clear_existing_one(self) -> None:
        from dataset import change_metadata

        before = copy.deepcopy(self.store.cases["ZF-1"])
        with self.assertRaises(ValueError):
            self.store.offer_handoff(
                self.sam,
                "ZF-1",
                self.rae["email"],
                metadata={
                    **change_metadata(self.store, "ZF-1"),
                    "resident_update_to": self.sam["email"],
                },
            )
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries())[-1]["action"], "handoff_offered_rejected")
        self.commitment()
        expected = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])
        self.store.offer_handoff(
            self.sam,
            "ZF-1",
            self.rae["email"],
            metadata=change_metadata(self.store, "ZF-1"),
        )
        self.store.receive_handoff(self.rae, "ZF-1")
        self.store.decline_handoff(self.rae, "ZF-1", "SYN return to sender")
        self.assertEqual(self.open_store().cases["ZF-1"]["resident_update"], expected)
        denied = self.store.detail("ZF-1", dict(self.rex, role="Quality Inspector"))
        self.assertNotIn("SYN human-selected fixture date", json.dumps(denied))

    def test_json_followup_failure_restores_record_and_ledger(self) -> None:
        if self.sql:
            self.skipTest("JSON file rollback only")
        self.commitment()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        for target in ("save", "audit"):
            with self.subTest(target=target):
                original = getattr(self.store, target)

                def failed(
                    *args: Any,
                    target: str = target,
                    original: Callable[..., Any] = original,
                    **kwargs: Any,
                ) -> None:
                    if target == "audit":
                        original(*args, **kwargs)
                    raise OSError("SYN persistence fault")

                with patch.object(self.store, target, side_effect=failed):
                    with self.assertRaises(OSError):
                        self.commitment(expected_version=1)
                self.assertEqual(self.open_store().cases["ZF-1"], before)
                self.assertEqual(list(self.store.audit_entries()), audit)
                self.assertTrue(self.store.verify_audit())

    def test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        ids = []
        for measure in MEASURES:
            items = {label: "Synthetic evidence" for label in checklist_for(measure)["items"]}
            ids.append(
                self.store.submit_quality(
                    self.sam,
                    "ZF-1",
                    measure,
                    "Synthetic installer",
                    "Installer",
                    items,
                    context_revision=1,
                )
            )
        self.answer(status="Withdrawn")
        self.unchanged_failure(lambda: self.store.accept_quality(self.pam, "ZF-1", ids[0]))
        self.store.accept_quality(self.pam, "ZF-1", ids[1])
        self.store.hand_over_quality(self.pam, "ZF-1", ids[1], "Synthetic handover", True)
        self.unchanged_failure(
            lambda: self.store.submit_quality(
                self.sam,
                "ZF-1",
                MEASURES[1],
                "Synthetic installer",
                "Installer",
                {label: "Synthetic evidence" for label in checklist_for(MEASURES[1])["items"]},
            )
        )

    def test_detached_projection_persistence_audit_and_model_minimisation(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        for actor in (self.sam, self.pam, self.rex, self.kim):
            detail = self.store.detail("ZF-1", actor)
            if actor == self.kim:
                text = json.dumps(detail)
                for sentinel in ("SYN-AUTH-CANARY", "SYN-WISHES-CANARY", "SYN-SOURCE-CANARY"):
                    self.assertNotIn(sentinel, text)
            self.assertEqual(self.store.cases["ZF-1"], before)
        with patch.dict("os.environ", {"ZF_REASON_ROLES": "Retrofit Coordinator"}):
            detail = self.store.detail("ZF-1", self.sam)
            self.assertIn("representative_authorities", detail)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.log_call(self.sam, "ZF-1", "SYN", "SYN")
        again = self.open_store()
        for key in ("representative_authorities", "measure_decisions", "resident_scopes"):
            self.assertEqual(again.cases["ZF-1"][key], before[key])
        self.assertNotIn("SYN-WISHES-CANARY", json.dumps(audit))
        self.assertNotIn("SYN-SOURCE-CANARY", json.dumps(audit))
        source = self.store._facts(self.store.cases["ZF-1"])
        self.assertNotIn("SYN-AUTH-CANARY", source)
        self.assertNotIn("SYN-WISHES-CANARY", source)
        self.assertEqual(
            projection.contractor_detail(before, before).get("measure_decisions"), None
        )

    def test_unchecked_addressed_draft_refused_but_enabled_ai_proposals_survive(self) -> None:
        with self.store.lock:
            self.store._case("ZF-1")["resident"]["representative"] = dict(name="SYN-REP")
            self.store.save()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        self.unchanged_failure(lambda: self.store.draft("ZF-1", "visit"))
        result = dict(source="ai", model="synthetic-adapter", validated=True, verified=True)
        with patch.object(ai_tasks, "run_text_task", return_value=result) as service:
            for task in ("message", "summary"):
                proposal = self.store.ai_run(self.sam, "ZF-1", task)
                self.assertIn("not approved", proposal["label"])
            self.assertEqual(service.call_count, 2)
        self.assertEqual(self.store.cases["ZF-1"], before)


@unittest.skipUnless(
    os.environ.get("ZF_RESIDENT_AZURE_TEST") == "1",
    "Explicit isolated synthetic Azure SQL database required",
)
class AzureResidentDecisions(unittest.TestCase):
    def test_synthetic_sqlstore_persistence_permissions_retention_and_audit(self) -> None:
        from datetime import date

        from zava_forward.core.mssqlstore import MssqlStore
        from zava_forward.core.resident_decisions import retention_schedule

        self.assertTrue(os.environ["ZF_SQL_DATABASE"].startswith("resident86test"))
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "synthetic.json"
            data = copy.deepcopy(DATA)
            data["cases"][0]["contacts"] = [
                dict(
                    at="2021-10-17T10:00",
                    channel="Phone",
                    outcome="SYN",
                    note="SYN",
                    by="Sam Example",
                )
            ]
            coordinator = dict(
                code="RC-86",
                name="Synthetic Coordinator",
                email="rc86@example.test",
                role="Retrofit Coordinator",
            )
            contractor = dict(
                code="CON-86",
                name="Synthetic Contractor",
                email="con86@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
            data["staff"].extend([coordinator, contractor])
            path.write_text(json.dumps(data))
            store = MssqlStore(str(path), state_dir=root)
            self.addCleanup(store.db.close)
            self.assertIsInstance(store, SqlStore)
            self.assertEqual(len(store.cases), len(DATA["cases"]))
            sam, manager = data["staff"][:2]
            store.technical_action(manager, "ZF-1", dict(action="design_submit", note="SYN"))

            def action(name: str, **body: Any) -> None:
                store.resident_action(sam, "ZF-1", dict(action=name, **body))

            action(
                "scope_record",
                measure="Loft insulation",
                design_version=1,
                scope="SYN-SCOPE",
                source="SYN",
            )
            action("safe_contact_record", safe_contact_ref="SYN-SAFE", source="SYN")
            binding = dict(measure="Loft insulation", context_revision=1)
            action(
                "representative_record",
                **binding,
                representative_ref="SYN-REP",
                status="Confirmed",
                tasks=["Works decision", "Receive information"],
                authority_date="2026-01-01",
                review_date="2027-01-01",
                safe_contact_ref="SYN-SAFE",
                source="SYN-AUTH",
                resident_wishes="SYN-WISHES",
            )
            answer = dict(**binding, status="Accepted", answered_by="The resident", source="SYN")
            action("decision_record", **answer)
            self.assertEqual(
                store.detail("ZF-1", contractor)["resident_readiness"],
                [dict(measure="Loft insulation", flag="Proceed")],
            )
            action("decision_record", **dict(answer, status="Withdrawn", note="SYN-WITHDRAWN"))
            self.assertEqual(
                store.detail("ZF-1", contractor)["resident_readiness"],
                [dict(measure="Loft insulation", flag="Hold")],
            )
            before = copy.deepcopy(store.cases["ZF-1"])
            with self.assertRaises(PermissionError):
                store.resident_action(manager, "ZF-1", dict(action="safe_contact_record"))
            self.assertEqual(store.cases["ZF-1"], before)
            self.assertIn("SYN-WISHES", json.dumps(store.detail("ZF-1", coordinator)))
            self.assertNotIn("SYN-WISHES", json.dumps(store.detail("ZF-1", contractor)))
            reopened = MssqlStore(str(path), state_dir=root)
            self.addCleanup(reopened.db.close)
            self.assertEqual(reopened.cases["ZF-1"], before)
            with patch.object(controls, "today", return_value="2026-10-16"):
                self.assertEqual(retention_schedule(reopened.cases["ZF-1"])["due"], "2026-10-17")
                self.assertFalse(retention_schedule(reopened.cases["ZF-1"])["expired"])
            with patch.object(controls, "today", return_value="2026-10-17"):
                self.assertTrue(retention_schedule(reopened.cases["ZF-1"])["expired"])
                with self.assertRaises(ValueError):
                    reopened.resident_action(
                        sam,
                        "ZF-1",
                        dict(
                            action="disclosure_check",
                            **binding,
                            representative_ref="SYN-REP",
                            task="Receive information",
                        ),
                    )
                reopened.approve_retention_deletion(
                    manager, "ZF-1", "resident-decisions", today=date(2026, 10, 17)
                )
            final = MssqlStore(str(path), state_dir=root)
            self.addCleanup(final.db.close)
            for key in ("measure_decisions", "resident_safe_contact", "representative_authorities"):
                self.assertNotIn(key, final.cases["ZF-1"])
            self.assertNotIn("SYN-WISHES", json.dumps(final.cases["ZF-1"]))
            self.assertNotIn("first_contact_at", final.cases["ZF-1"]["resident"])
            self.assertTrue(final.verify_audit())
            mode = final.db.execute(
                "SELECT is_ledger_on FROM sys.databases WHERE name=DB_NAME()"
            ).fetchone()[0]
            print(
                json.dumps(
                    dict(
                        platform="Azure SQL",
                        ledger_mode=bool(mode),
                        current_payload_purged=True,
                        restart_verified=True,
                        audit_intact=True,
                        synthetic_only=True,
                    )
                )
            )


class SqlResidentDecisions(JsonResidentDecisions):
    sql = True
    store: SqlStore

    def test_response_reassignment_rechecks_writer_actor_assignee_and_version(self) -> None:
        self.request()
        body = dict(
            action="service_reassign",
            id="SR-1",
            expected_version=1,
            responsibility="service",
            owner=self.rex["email"],
            note="SYN recovery",
        )
        for subject in (self.pam, self.rex):
            for field, value in (("role", "Contractor"), ("oid", "SYN rebound identity")):
                with self.subTest(subject=subject["code"], field=field):
                    save = self.store.save

                    def change_registry(
                        subject: dict[str, Any] = subject,
                        field: str = field,
                        value: str = value,
                        save: Callable[[], None] = save,
                    ) -> None:
                        other = self.store.assistant_connection()
                        try:
                            other.execute(
                                "UPDATE staff SET body=? WHERE email=?",
                                (json.dumps(dict(subject, **{field: value})), subject["email"]),
                            )
                        finally:
                            other.close()
                        save()

                    with patch.object(self.store, "save", side_effect=change_registry):
                        self.unchanged_failure(
                            lambda: self.store.resident_action(self.pam, "ZF-1", body)
                        )
                    self.register_followup_actor(subject)
        other = self.open_store()
        save = self.store.save

        def competing_owner() -> None:
            other.resident_action(self.pam, "ZF-1", dict(body, owner=self.pam["email"]))
            save()

        with patch.object(self.store, "save", side_effect=competing_owner):
            with self.assertRaises(ConflictError):
                self.store.resident_action(self.pam, "ZF-1", body)
        current = self.open_store()
        self.assertEqual(
            current.cases["ZF-1"]["service_requests"][0]["service_identity"]["email"],
            self.pam["email"],
        )
        self.assertEqual(
            sum(e["action"] == "resident_service_reassign" for e in current.audit_entries()), 1
        )
        self.unchanged_failure(lambda: self.store.resident_action(self.pam, "ZF-1", body))

    def test_response_reassignment_faults_preserve_history_and_exactly_once_outcome(self) -> None:
        from zava_forward.core.resident_decisions import ResidentCommittedError

        self.request()
        body = dict(
            action="service_reassign",
            id="SR-1",
            expected_version=1,
            responsibility="service",
            owner=self.rex["email"],
            note="SYN recovery",
        )
        before = copy.deepcopy(self.store.cases["ZF-1"])
        for persistent in (False, True):
            audit = list(self.store.audit_entries())
            append = self.store._append_audit
            original = OSError("SYN response assignment audit failure")

            class RecoveryFault:
                armed = False
                failures = 0

                def __init__(self, db: Any, persistent: bool) -> None:
                    self.db = db
                    self.persistent = persistent

                def execute(self, sql: str, args: Any = ()) -> Any:
                    if self.armed and sql.startswith("SELECT rowversion, body FROM cases"):
                        if self.persistent or self.failures == 0:
                            self.failures += 1
                            raise OSError("SYN response assignment recovery read")
                    return self.db.execute(sql, args)

                def __getattr__(self, name: str) -> Any:
                    return getattr(self.db, name)

            fault = RecoveryFault(self.store.db, persistent)

            def failed_audit(
                entries: Any,
                append: Callable[..., Any] = append,
                fault: RecoveryFault = fault,
                original: OSError = original,
            ) -> None:
                append(entries)
                fault.armed = True
                raise original

            with self.store.lock:
                self.store.audit(self.pam["email"], "prior_assignment_event", "ZF-2", "SYN")
                prior = list(self.store.local.pending)
                with (
                    patch.object(self.store, "db", fault),
                    patch.object(self.store, "_append_audit", side_effect=failed_audit),
                    self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                    self.assertRaises(OSError) as caught,
                ):
                    self.store.resident_action(self.pam, "ZF-1", body)
                self.assertIs(caught.exception, original)
                self.assertEqual(self.store.local.pending, prior)
                self.assertFalse(self.store.local.touched)
            current = self.open_store()
            self.assertEqual(current.cases["ZF-1"], before)
            self.assertEqual(
                [e["action"] for e in current.audit_entries()],
                [e["action"] for e in audit] + ["prior_assignment_event"],
            )
        other = self.open_store()
        save, sync = self.store.save, self.store._sync
        armed = False

        def committed_save() -> None:
            nonlocal armed
            other.log_call(self.sam, "ZF-2", "SYN", "SYN different writer")
            armed = True
            save()

        def unavailable_sync() -> None:
            if armed:
                raise OSError("SYN response assignment committed sync")
            sync()

        with self.store.lock:
            self.store.audit(self.pam["email"], "committed_assignment_prefix", "ZF-2", "SYN")
            with (
                patch.object(self.store, "save", side_effect=committed_save),
                patch.object(self.store, "_sync", side_effect=unavailable_sync),
                self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                self.assertRaises(ResidentCommittedError) as caught_committed,
            ):
                self.store.resident_action(self.pam, "ZF-1", body)
            self.assertIsInstance(caught_committed.exception.__cause__, OSError)
            self.assertFalse(self.store.local.pending)
        current = self.open_store()
        self.assertEqual(current.cases["ZF-1"]["service_requests"][0]["version"], 2)
        audit = list(current.audit_entries())
        self.store.save()
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(sum(e["action"] == "resident_service_reassign" for e in audit), 1)
        self.assertEqual(sum(e["action"] == "committed_assignment_prefix" for e in audit), 1)
        self.assertTrue(current.verify_audit())

    def test_followup_writer_rechecks_current_actor_assignee_and_legacy_identity(self) -> None:
        assert isinstance(self.store, SqlStore)
        for subject in (self.sam, self.rae):
            for key, value in (("oid", "SYN-rebound"), ("role", "Quality Inspector")):
                with self.subTest(subject=subject["code"], field=key):
                    save = self.store.save

                    def changed(
                        subject: dict[str, Any] = subject,
                        key: str = key,
                        value: str = value,
                        save: Callable[[], None] = save,
                    ) -> None:
                        connection = self.store.assistant_connection()
                        try:
                            connection.execute(
                                "UPDATE staff SET body=? WHERE email=?",
                                (json.dumps(dict(subject, **{key: value})), subject["email"]),
                            )
                        finally:
                            connection.close()
                        save()

                    with patch.object(self.store, "save", side_effect=changed):
                        self.unchanged_failure(lambda: self.commitment(owner=self.rae["email"]))
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(subject), subject["email"]),
                    )
        self.request()
        self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")
        with self.store.lock:
            self.store._case("ZF-1")["service_requests"][0].pop("service_identity")
            self.store.save()
        save = self.store.save

        def rebound() -> None:
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(dict(self.sam, code=self.rae["code"])), self.sam["email"]),
            )
            save()

        with patch.object(self.store, "save", side_effect=rebound):
            self.unchanged_failure(
                lambda: self.store.resident_action(
                    self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN")
                )
            )
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(self.sam), self.sam["email"])
        )
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response")
        )

    def test_concurrent_followup_writers_one_version_one_success_event(self) -> None:
        self.commitment()
        other = self.open_store()
        barrier = Barrier(2)

        def record(store: Store, owner: dict[str, Any]) -> str:
            with store.lock:
                barrier.wait(timeout=20)
                try:
                    store.resident_action(
                        self.sam,
                        "ZF-1",
                        dict(
                            action="update_record",
                            expected_version=1,
                            owner=owner["email"],
                            purpose="SYN concurrent",
                            due_at="2099-01-01T12:00:00Z",
                            basis="SYN",
                            status="Outstanding",
                        ),
                    )
                    return "recorded"
                except ConflictError:
                    return "conflict"

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [
                pool.submit(record, self.store, self.sam),
                pool.submit(record, other, self.rae),
            ]
            self.assertCountEqual([f.result(timeout=40) for f in futures], ["recorded", "conflict"])
        current = self.open_store()
        self.assertEqual(current.cases["ZF-1"]["resident_update"]["version"], 2)
        self.assertEqual(
            sum(e["action"] == "resident_update_record" for e in current.audit_entries()), 2
        )
        self.assertTrue(current.verify_audit())

    def test_followup_audit_insert_and_recovery_faults_never_replay_success(self) -> None:
        assert isinstance(self.store, SqlStore)
        self.commitment()
        for persistent in (False, True):
            with self.subTest(persistent=persistent):
                before = copy.deepcopy(self.store.cases["ZF-1"])
                audit = list(self.store.audit_entries())
                db, append = self.store.db, self.store._append_audit
                original = OSError("SYN after real audit insert")

                class ReadFault:
                    armed = False
                    count = 0

                    def __init__(self, db: Any, persistent: bool) -> None:
                        self.db = db
                        self.persistent = persistent

                    def execute(self, sql: str, args: Any = ()) -> Any:
                        if self.armed and sql.startswith("SELECT rowversion, body FROM cases"):
                            if self.persistent or self.count == 0:
                                self.count += 1
                                raise OSError("SYN recovery read")
                        return self.db.execute(sql, args)

                    def __getattr__(self, name: str) -> Any:
                        return getattr(self.db, name)

                fault = ReadFault(db, persistent)

                def audit_failure(
                    entries: Any,
                    append: Callable[..., Any] = append,
                    fault: ReadFault = fault,
                    original: OSError = original,
                ) -> None:
                    append(entries)
                    fault.armed = True
                    raise original

                with self.store.lock:
                    self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN")
                    prior = list(self.store.local.pending)
                    with (
                        patch.object(self.store, "_append_audit", side_effect=audit_failure),
                        patch.object(self.store, "db", fault),
                        self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                    ):
                        with self.assertRaises(OSError) as caught:
                            self.commitment(expected_version=1)
                    self.assertIs(caught.exception, original)
                    self.assertEqual(self.store.local.pending, prior)
                    self.assertEqual(self.store.local.touched, set())
                    self.assertIsNone(self.store.local.resident_validation)
                current = self.open_store()
                self.assertEqual(current.cases["ZF-1"], before)
                self.assertEqual(
                    [e["action"] for e in current.audit_entries()],
                    [e["action"] for e in audit] + ["prior_event"],
                )
                self.assertTrue(current.verify_audit())
        self.commitment(expected_version=1)

    def test_followup_postcommit_sync_fault_is_truthful_and_not_replayed(self) -> None:
        from zava_forward.core.resident_decisions import ResidentCommittedError

        assert isinstance(self.store, SqlStore)
        self.commitment()
        other = self.open_store()
        save, sync = self.store.save, self.store._sync
        fault = dict(armed=False)

        def interleave() -> None:
            other.log_call(self.sam, "ZF-2", "SYN", "SYN concurrent unrelated write")
            fault["armed"] = True
            save()

        def failed_sync() -> None:
            if fault["armed"]:
                raise OSError("SYN persistent postcommit synchronization")
            sync()

        with self.store.lock:
            self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN")
            with (
                patch.object(self.store, "save", side_effect=interleave),
                patch.object(self.store, "_sync", side_effect=failed_sync),
                self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                self.assertRaises(ResidentCommittedError) as caught,
            ):
                self.commitment(expected_version=1)
            self.assertIn("recorded", str(caught.exception))
            self.assertIsInstance(caught.exception.__cause__, OSError)
            self.assertEqual(self.store.local.pending, [])
        current = self.open_store()
        self.assertEqual(current.cases["ZF-1"]["resident_update"]["version"], 2)
        audit = list(current.audit_entries())
        self.store.save()
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(sum(e["action"] == "resident_update_record" for e in audit), 2)
        self.assertEqual(sum(e["action"] == "prior_event" for e in audit), 1)
        self.assertTrue(current.verify_audit())

    def test_save_clears_scoped_dependencies_inside_outer_lock(self) -> None:
        assert isinstance(self.store, SqlStore)
        self.scope()
        self.answer()
        pid = self.package()
        with self.store.lock:
            self.store.require_stock_clear(self.store.cases["ZF-1"])
            self.store.issue_work_order(
                self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
            )
            self.assertEqual(self.store.local.resident_clear, [])
            self.assertEqual(self.store.local.safety_clear, set())
            self.assertEqual(self.store.local.stock_clear, set())

    def test_stock_race_rechecks_all_dependencies_and_clears_them_after_rollback(self) -> None:
        assert isinstance(self.store, SqlStore)
        self.scope()
        self.answer()
        other = self.open_store()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        with self.store.lock:
            self.store.require_safety_clear(self.store.cases["ZF-1"])
            self.store.require_stock_clear(self.store.cases["ZF-1"])
            self.store.require_resident_clear(self.store.cases["ZF-1"], self.bind(MEASURES[0]))
            other.stock_reconcile(
                self.sam,
                "ZF-1",
                dict(
                    field="epc",
                    query_owner=self.sam["email"],
                    left=dict(
                        value="D",
                        source_id="SYN-REGISTER",
                        date="2026-01-01",
                        version="1",
                        validation_state="Unvalidated",
                    ),
                    right=dict(
                        value="E",
                        source_id="SYN-SURVEY",
                        date="2026-01-01",
                        version="1",
                        validation_state="Disputed",
                    ),
                ),
            )
            self.store._case("ZF-1")["reason"] = "Must not persist"
            self.store.audit(self.pam["email"], "synthetic_refused", "ZF-1", "SYN")
            with self.assertRaises(GateError):
                self.store.save()
            self.assertEqual(self.store.local.resident_clear, [])
            self.assertEqual(self.store.local.safety_clear, set())
            self.assertEqual(self.store.local.stock_clear, set())
            self.store.log_call(self.sam, "ZF-2", "Spoke", "Independent home")
        self.assertEqual(self.store.cases["ZF-1"]["reason"], before["reason"])
        self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], before["measure_decisions"])
        self.assertNotIn("synthetic_refused", [e["action"] for e in self.store.audit_entries()])
        self.assertTrue(self.store.verify_audit())

    def test_competing_pause_and_authority_change_refuse_stale_release_commit(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        pid = self.package()
        other = self.open_store()
        original = self.store.save

        def competing_pause() -> None:
            other.resident_action(
                self.sam,
                "ZF-1",
                dict(
                    action="decision_record",
                    measure=MEASURES[0],
                    context_revision=1,
                    status="Paused",
                    answered_by="The resident",
                    source="SYN",
                    note="SYN",
                ),
            )
            original()

        with patch.object(self.store, "save", side_effect=competing_pause):
            with self.assertRaises((GateError, ConflictError)):
                self.store.issue_work_order(
                    self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
                )
        self.assertEqual(self.store.list_work_orders(self.pam), [])
        self.assertNotIn("workorder_issued", [e["action"] for e in self.store.audit_entries()])
        self.answer(review_ref="SYN-REVIEW")
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")

        def competing_authority() -> None:
            other.resident_action(
                self.sam,
                "ZF-1",
                dict(action="safe_contact_record", safe_contact_ref="SYN-NEW", source="SYN"),
            )
            original()

        with patch.object(self.store, "save", side_effect=competing_authority):
            with self.assertRaises((GateError, ConflictError)):
                self.store.issue_work_order(
                    self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
                )
        self.assertEqual(self.store.list_work_orders(self.pam), [])


@unittest.skipUnless(os.environ.get("ZF_RESIDENT_MSSQL") == "1", "opt-in owned loopback SQL Server")
class MssqlResidentControls(SqlResidentDecisions):
    def setUp(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        self.database = "zf_resident88_" + uuid.uuid4().hex
        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{self.database}]")

        def drop_owned_database() -> None:
            admin.execute(
                f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
            )
            admin.execute(f"DROP DATABASE [{self.database}]")

        self.addCleanup(drop_owned_database)
        os.environ["ZF_SQL_DATABASE"] = self.database
        super().setUp()

    def open_store(self) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store
