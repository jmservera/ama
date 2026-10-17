"""Explicit single-record change sources on synthetic JSON and SQLite stores."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store


def supplied(store: Any, cid: str = "ZF-1", **overrides: Any) -> dict[str, Any]:
    return dict(
        source="SYN supplied register",
        source_version="source revision 7",
        reason="Synthetic recorded change",
        handoff_version=len(store.cases[cid].get("handoff_history", [])),
        **overrides,
    )


class JsonChangeProvenance(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        self.path.write_text(json.dumps(copy.deepcopy(DATA)))
        self.store = self.open_store()
        self.sam, self.pam = DATA["staff"]

    def open_store(self) -> Any:
        store: Any = (
            SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            if self.sql
            else Store(str(self.path))
        )
        if self.sql:
            self.addCleanup(store.db.close)
        return store

    def upload(self, metadata: object) -> Any:
        return self.store.add_document(
            self.sam, "ZF-1", "supplied.txt", "Other", b"synthetic source", metadata=metadata
        )

    def offer(self) -> None:
        self.store.offer_handoff(self.sam, "ZF-1", self.pam["email"], metadata=supplied(self.store))

    def test_missing_or_invalid_metadata_refuses_without_case_or_success_audit(self) -> None:
        for field in ("source", "source_version", "reason"):
            for value in (None, "", " ", 7, "x" * 501):
                with self.subTest(field=field, value=str(value)[:8]):
                    meta = supplied(self.store)
                    meta[field] = value
                    before = copy.deepcopy(self.store.cases)
                    with self.assertRaises(ValueError):
                        self.upload(meta)
                    self.assertEqual(self.store.cases, before)
                    self.assertFalse(
                        any(e["action"] == "upload_document" for e in self.store.audit_entries())
                    )
                    self.assertEqual(
                        list(self.store.audit_entries())[-1]["action"], "upload_document_rejected"
                    )
        with self.assertRaises(ValueError):
            self.store.add_document(self.sam, "ZF-1", "legacy.txt", "Other", b"no metadata")

    def test_upload_exact_provenance_reference_history_audit_and_reopen(self) -> None:
        meta = supplied(self.store)
        doc = self.upload(meta)
        current = self.open_store()
        saved = current.cases["ZF-1"]["documents"][-1]
        event = current.cases["ZF-1"]["document_history"][-1]
        for field in ("source", "source_version", "reason"):
            self.assertEqual(saved[field], meta[field])
            self.assertEqual(event[field], meta[field])
        self.assertEqual(event["actor"]["email"], self.sam["email"])
        self.assertEqual(event["version"], 1)
        self.assertTrue(event["at"].endswith("+00:00"))
        self.assertEqual(event["changes"]["documents"]["old"], [])
        reference = {key: doc[key] for key in ("id", "name", "kind", "content_sha256", "version")}
        self.assertEqual(event["changes"]["documents"]["new"], [reference])
        audit = next(e for e in current.audit_entries() if e["action"] == "upload_document")
        self.assertEqual(json.loads(audit["detail"]), event)
        self.assertTrue(current.verify_audit())
        doc["source"] = "Caller mutation is not a recorded edit"
        self.assertEqual(self.store.cases["ZF-1"]["documents"][0]["source"], meta["source"])
        self.upload(meta)
        events = self.open_store().cases["ZF-1"]["document_history"]
        self.assertEqual([row["version"] for row in events], [1, 2])
        self.assertEqual(events[1]["changes"]["documents"]["old"], [reference])
        self.assertEqual(len(events[1]["changes"]["documents"]["new"]), 2)

    def test_offer_and_accept_require_supplied_metadata_and_exact_ownership_events(self) -> None:
        before = copy.deepcopy(self.store.cases)
        with self.assertRaises(ValueError):
            self.store.offer_handoff(self.sam, "ZF-1", self.pam["email"])
        self.assertEqual(self.store.cases, before)
        self.offer()
        with self.assertRaises(ValueError):
            self.store.accept_handoff(self.pam, "ZF-1")
        with self.assertRaises(PermissionError):
            self.store.accept_handoff(self.sam, "ZF-1", metadata=supplied(self.store))
        stale = supplied(self.store)
        stale["handoff_version"] = 0
        with self.assertRaises(ConflictError):
            self.store.accept_handoff(self.pam, "ZF-1", metadata=stale)
        self.store.accept_handoff(self.pam, "ZF-1", metadata=supplied(self.store))
        reopened = self.open_store()
        events = reopened.cases["ZF-1"]["handoff_history"]
        for event in events:
            for field in ("source", "source_version", "reason"):
                self.assertEqual(event[field], supplied(self.store)[field])
        change = events[-1]["changes"]["ownership"]
        self.assertEqual(change["old"]["owner_code"], self.sam["code"])
        self.assertEqual(change["new"]["owner_code"], self.pam["code"])
        self.assertEqual(
            change["new"],
            dict(
                owner=self.pam["name"],
                owner_code=self.pam["code"],
                owner_role=self.pam["role"],
                waiting_on=self.pam["name"],
            ),
        )
        self.assertEqual(events[-1]["actor"]["email"], self.pam["email"])
        audit = next(e for e in reopened.audit_entries() if e["action"] == "handoff_accepted")
        self.assertEqual(json.loads(audit["detail"]), events[-1])
        self.assertEqual([e["version"] for e in events], [1, 2])
        self.assertTrue(reopened.verify_audit())

    def test_handoff_metadata_rejects_forged_or_missing_fields_without_owner_changes(self) -> None:
        self.offer()
        before = copy.deepcopy(self.store.cases)
        for field in ("source", "source_version", "reason", "handoff_version"):
            meta = supplied(self.store)
            meta.pop(field)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.store.accept_handoff(self.pam, "ZF-1", metadata=meta)
            self.assertEqual(self.store.cases, before)
        for field in ("actor", "at", "version", "changes"):
            meta = supplied(self.store)
            meta[field] = {"forged": "not caller owned"}
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.store.accept_handoff(self.pam, "ZF-1", metadata=meta)
            self.assertEqual(self.store.cases, before)
        self.assertFalse(any(e["action"] == "handoff_accepted" for e in self.store.audit_entries()))

    def test_source_notes_redacted_without_changing_legacy_records(self) -> None:
        from zava_forward.core import projection

        self.upload(supplied(self.store))
        self.offer()
        case = self.store.detail("ZF-1")
        projection.hold_notes(case)
        self.assertNotIn("SYN supplied register", json.dumps(case))
        self.assertNotIn("source revision 7", json.dumps(case))
        self.assertNotIn("Synthetic recorded change", json.dumps(case))
        before = copy.deepcopy(self.store.cases["ZF-1"]["documents"][0])
        with self.assertRaises(ValueError):
            self.upload({})
        self.assertEqual(self.store.cases["ZF-1"]["documents"][0], before)


class SqlChangeProvenance(JsonChangeProvenance):
    sql = True

    def test_save_failure_has_no_case_history_or_ghost_success_after_reopen(self) -> None:
        for action in ("upload", "offer", "accept"):
            with self.subTest(action=action):
                if action == "accept":
                    self.offer()
                before = copy.deepcopy(self.store.cases)
                successes = [
                    e for e in self.store.audit_entries() if not e["action"].endswith("_rejected")
                ]
                with patch.object(
                    self.store, "_append_audit", side_effect=RuntimeError("synthetic rollback")
                ):
                    with self.assertRaises(RuntimeError):
                        if action == "upload":
                            self.upload(supplied(self.store))
                        elif action == "offer":
                            self.offer()
                        else:
                            self.store.accept_handoff(
                                self.pam, "ZF-1", metadata=supplied(self.store)
                            )
                reopened = self.open_store()
                self.assertEqual(reopened.cases, before)
                self.assertEqual(
                    [e for e in reopened.audit_entries() if not e["action"].endswith("_rejected")],
                    successes,
                )
                self.store = reopened

    def test_current_actor_revocation_at_commit_refuses_without_success_or_changes(self) -> None:
        original = self.store.save
        before = copy.deepcopy(self.store.cases)

        def revoke_then_save() -> None:
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(dict(self.sam, role="Contractor")), self.sam["email"]),
            )
            original()

        with patch.object(self.store, "save", side_effect=revoke_then_save):
            with self.assertRaises(PermissionError):
                self.upload(supplied(self.store))
        reopened = self.open_store()
        self.assertEqual(reopened.cases, before)
        self.assertFalse(any(e["action"] == "upload_document" for e in reopened.audit_entries()))
        self.assertEqual(list(reopened.audit_entries())[-1]["action"], "upload_document_rejected")
        self.assertEqual(reopened.docstore.list_ids("ZF-1"), [])
        self.assertTrue(reopened.verify_audit())

    def test_concurrent_owner_change_rolls_back_acceptance_and_lost_ack_keeps_document(
        self,
    ) -> None:
        self.offer()
        other = self.open_store()
        original = self.store.save

        def competing_save() -> None:
            with other.lock:
                other._case("ZF-1")["reason"] = "Synthetic concurrent case revision"
                other.save()
            original()

        with patch.object(self.store, "save", side_effect=competing_save):
            with self.assertRaises(ConflictError):
                self.store.accept_handoff(self.pam, "ZF-1", metadata=supplied(self.store))
        reopened = self.open_store()
        self.assertEqual(reopened.cases["ZF-1"]["owner_code"], self.sam["code"])
        self.assertEqual(len(reopened.cases["ZF-1"]["handoff_history"]), 1)
        self.assertFalse(any(e["action"] == "handoff_accepted" for e in reopened.audit_entries()))
        self.store = reopened
        original = self.store.save

        def committed_without_ack() -> None:
            original()
            raise RuntimeError("Synthetic lost commit acknowledgement")

        with patch.object(self.store, "save", side_effect=committed_without_ack):
            with self.assertRaises(RuntimeError):
                self.upload(supplied(self.store))
        reopened = self.open_store()
        doc = reopened.cases["ZF-1"]["documents"][-1]
        self.assertEqual(reopened.get_document("ZF-1", doc["id"], self.sam)[2], b"synthetic source")
        self.assertEqual(len(reopened.cases["ZF-1"]["document_history"]), 1)
        self.assertTrue(reopened.verify_audit())
