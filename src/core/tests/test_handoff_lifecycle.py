"""Synthetic state, authority and durable-accountability contract for issue 83."""

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tests.dataset import DATA

from zava_forward.core import projection
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.workflows import handoff_view


class JsonHandoffLifecycle(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                dict(
                    code="RLO-02",
                    name="Rae Other",
                    email="rae@example.test",
                    role="Resident Liaison Officer",
                ),
                dict(
                    code="RC-01",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
            ]
        )
        data["cases"][0]["stage"] = "Install booked"
        data["cases"][1].update(stage="Completed", closed=True)
        self.sam, self.pam, self.rae, self.rex = data["staff"]
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()

    def open_store(self) -> Store:
        if self.sql:
            store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.path))

    def offer(self) -> None:
        self.store.offer_handoff(
            self.sam,
            "ZF-1",
            self.rae["email"],
            "PRIVATE-NOTE",
            metadata=dict(
                urgency="Urgent",
                due_at="2026-10-15T10:00:00+01:00",
                next_action="PRIVATE-ACTION",
                resident_update_to=self.sam["email"],
                resident_update_due_at="2026-10-16T12:00:00Z",
            ),
        )

    def test_receipt_escalation_acceptance_and_completion(self) -> None:
        self.offer()
        self.store.receive_handoff(self.rae, "ZF-1")
        self.store.escalate_handoff(self.sam, "ZF-1", self.pam["email"], "Chase acceptance")
        for user in (self.sam, self.rae, self.pam):
            row = self.store.pending_handoffs(user)[0]
            self.assertEqual(row["status"], "Escalated")
            self.assertEqual(row["accountable_owner_code"], self.sam["code"])
            self.assertEqual(row["chase_owner_code"], self.sam["code"])
            self.assertEqual(row["destination"], self.rae["role"])
            self.assertIsNone(row["confirmed_receiver"])
            self.assertEqual(row["due_at"], "2026-10-15T09:00+00:00")
            self.assertEqual(row["resident_update_owner"], self.sam["name"])
        self.store.accept_handoff(self.rae, "ZF-1")
        self.store.complete_handoff(self.rae, "ZF-1", "Evidence reviewed")
        detail = self.open_store().detail("ZF-1")
        self.assertEqual(detail["owner_code"], self.rae["code"])
        self.assertEqual(detail["handoff"]["status"], "Completed")
        self.assertEqual(detail["handoff"]["confirmed_receiver"], self.rae["name"])
        self.assertEqual(detail["handoff"]["chase_owner"], self.rae["name"])
        events = detail["handoff_history"]
        self.assertEqual(
            [e["status"] for e in events],
            ["Sent", "Received", "Escalated", "Accepted", "Completed"],
        )
        self.assertEqual([e["version"] for e in events], [1, 2, 3, 4, 5])
        self.assertEqual(events[0]["accountable_owner_code"], self.sam["code"])
        self.assertTrue(self.store.verify_audit())
        self.assertEqual(self.store.pending_handoffs(self.pam), [])

    def test_invalid_actors_and_replays_do_not_change_evidence(self) -> None:
        self.offer()
        before = self.store.detail("ZF-1")
        audit = list(self.store.audit_entries())
        actions = [
            lambda: self.store.receive_handoff(self.sam, "ZF-1"),
            lambda: self.store.accept_handoff(self.pam, "ZF-1"),
            lambda: self.store.decline_handoff(self.sam, "ZF-1", "No"),
            lambda: self.store.withdraw_handoff(self.rae, "ZF-1"),
            lambda: self.store.escalate_handoff(self.rae, "ZF-1", self.pam["email"], "No"),
            lambda: self.store.escalate_handoff(self.sam, "ZF-1", self.rex["email"], "No"),
            lambda: self.store.complete_handoff(self.rae, "ZF-1", "Too soon"),
            lambda: self.store.offer_handoff(self.sam, "ZF-1", self.pam["email"]),
        ]
        for action in actions:
            with self.subTest(action=action), self.assertRaises((ValueError, PermissionError)):
                action()
            self.assertEqual(self.store.detail("ZF-1"), before)
            self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.receive_handoff(self.rae, "ZF-1")
        with self.assertRaises(ValueError):
            self.store.receive_handoff(self.rae, "ZF-1")
        self.store.escalate_handoff(self.pam, "ZF-1", self.pam["email"], "Manager chase")
        with self.assertRaises(ValueError):
            self.store.escalate_handoff(self.sam, "ZF-1", self.pam["email"], "Duplicate")
        with self.assertRaises(ValueError):
            self.store.receive_handoff(self.rae, "ZF-1")
        self.store.accept_handoff(self.rae, "ZF-1")
        with self.assertRaises(PermissionError):
            self.store.complete_handoff(self.sam, "ZF-1", "Wrong owner")
        with self.assertRaises(ValueError):
            self.store.complete_handoff(self.rae, "ZF-1", "")
        self.store.complete_handoff(self.rae, "ZF-1", "Done")
        with self.assertRaises(ValueError):
            self.store.complete_handoff(self.rae, "ZF-1", "Replay")

    def test_rejected_or_withdrawn_after_receipt_and_escalation(self) -> None:
        for state in ("Received", "Escalated"):
            for action in ("decline", "withdraw"):
                with self.subTest(state=state, action=action):
                    self.offer()
                    self.store.receive_handoff(self.rae, "ZF-1")
                    if state == "Escalated":
                        self.store.escalate_handoff(self.sam, "ZF-1", self.pam["email"], "Chase")
                    if action == "decline":
                        self.store.decline_handoff(self.rae, "ZF-1", "No capacity")
                    else:
                        self.store.withdraw_handoff(self.sam, "ZF-1")
                    detail = self.store.detail("ZF-1")
                    self.assertEqual(detail["owner_code"], self.sam["code"])
                    self.assertEqual(
                        detail["handoff"]["status"],
                        "Rejected" if action == "decline" else "Withdrawn",
                    )
                    self.assertEqual(detail["resident_update"]["owner"], self.sam["name"])
                    # Replacement offers cannot replace pending resident-update commitments.
                    self.store.offer_handoff(self.sam, "ZF-1", self.rex["email"])
                    row = self.store.pending_handoffs(self.sam)[0]
                    self.assertEqual(row["resident_update_owner"], self.sam["name"])
                    self.store.withdraw_handoff(self.sam, "ZF-1")
                    with self.assertRaises(ValueError):
                        self.store.offer_handoff(
                            self.sam,
                            "ZF-1",
                            self.rae["email"],
                            metadata={"resident_update_to": self.rex["email"]},
                        )

    def test_return_and_reopen_provenance_has_no_assignment_bypass(self) -> None:
        metadata = dict(
            source="Synthetic report 83",
            next_action="Arrange review",
            receiving_owner=self.rae["email"],
        )
        self.store.return_case(self.sam, "ZF-1", "Funding check", "Changed", metadata)
        self.store.reopen_case(self.pam, "ZF-2", "Fault", metadata)
        for cid in ("ZF-1", "ZF-2"):
            detail = self.open_store().detail(cid)
            rec = detail["returns"][-1]
            self.assertEqual(rec["version"], 1)
            self.assertEqual(rec["source"], metadata["source"])
            self.assertEqual(rec["next_action"], metadata["next_action"])
            self.assertEqual(rec["receiving_owner"]["code"], detail["owner_code"])
            self.assertEqual(detail["owner_code"], self.sam["code"])
            self.assertEqual(
                rec["initiating_authority"]["email"],
                self.sam["email"] if cid == "ZF-1" else self.pam["email"],
            )
        self.store.hand_over(self.sam, "ZF-1", self.rae["email"])
        self.assertEqual(self.store.detail("ZF-1")["owner_code"], self.sam["code"])
        self.store.accept_handoff(self.rae, "ZF-1")
        self.assertEqual(self.store.detail("ZF-1")["owner_code"], self.rae["code"])

    def test_incomplete_metadata_is_refused_before_mutation(self) -> None:
        before = self.store.detail("ZF-1")
        for metadata in ({}, {"source": "Report"}, {"next_action": "Review"}):
            with self.assertRaises(ValueError):
                self.store.return_case(self.sam, "ZF-1", "Funding check", "Changed", metadata)
            self.assertEqual(self.store.detail("ZF-1"), before)
        with self.assertRaises(ValueError):
            self.store.return_case(self.sam, "ZF-1", "Funding check", "Missing provenance")
        self.assertEqual(self.store.detail("ZF-1"), before)

    def test_input_validation_and_unknowns(self) -> None:
        invalid_recipients: tuple[object, ...] = (None, 5, [], "missing")
        for recipient in invalid_recipients:
            with self.assertRaises(ValueError):
                self.store.offer_handoff(self.sam, "ZF-1", recipient)
        for value in ("2026-10-15", "2026-10-15T12:00", "invalid", 3):
            with self.assertRaises(ValueError):
                self.store.offer_handoff(
                    self.sam, "ZF-1", self.rae["email"], metadata={"due_at": value}
                )
        for metadata in ({"urgency": "Emergency"}, {"resident_update_to": "missing"}):
            with self.assertRaises(ValueError):
                self.store.offer_handoff(self.sam, "ZF-1", self.rae["email"], metadata=metadata)
        self.store.offer_handoff(self.sam, "ZF-1", self.rae["email"])
        h = self.store.detail("ZF-1")["handoff"]
        for field in ("urgency", "due_at", "next_action", "resident_update_owner"):
            self.assertIsNone(h[field])
        self.assertIsNone(self.store.pending_handoffs(self.sam)[0]["confirmed_receiver"])
        self.assertEqual(self.store.pending_handoffs(self.rex), [])

    def test_projection_and_legacy_labels(self) -> None:
        self.offer()
        row = self.store.pending_handoffs(self.rex)
        self.assertEqual(row, [])
        self.store.withdraw_handoff(self.sam, "ZF-1")
        self.store.offer_handoff(
            self.sam,
            "ZF-1",
            self.rex["email"],
            "PRIVATE-NOTE",
            metadata={"next_action": "PRIVATE-ACTION"},
        )
        held = json.dumps(self.store.pending_handoffs(self.rex))
        self.assertNotIn("PRIVATE", held)
        self.assertIn(projection.NOTE_HELD, held)
        c = dict(owner="Sam", owner_code="S", handoff=dict(state="Offered", to_name="Rae"))
        h = handoff_view(c)
        self.assertEqual(h["status"], "Sent")
        self.assertIsNone(h["destination"])
        self.assertNotIn("status", c["handoff"])

    def test_nonstaff_cannot_mutate_or_read_handoffs(self) -> None:
        self.offer()
        for role in ("Contractor", "Unknown"):
            user = self.rae | {"role": role}
            for method in (
                lambda user=user: self.store.receive_handoff(user, "ZF-1"),
                lambda user=user: self.store.accept_handoff(user, "ZF-1"),
                lambda user=user: self.store.pending_handoffs(user),
                lambda user=user: self.store.hand_over(user, "ZF-1", self.rex["email"]),
                lambda user=user: self.store.return_case(user, "ZF-1", "Funding check", "No"),
            ):
                with self.assertRaises(PermissionError):
                    method()


class SqlHandoffLifecycle(JsonHandoffLifecycle):
    sql = True
