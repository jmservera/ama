"""Epic #104: staff can reject or override AI output, with named audit attribution.

Offline and synthetic. Unaccepted AI output stays unapproved, and nothing ratifies it
except a named person acting on their own record.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

import release_support
from zava_forward.core import ai_tasks
from zava_forward.core.aftercare import AftercareRegister
from zava_forward.core.store import Store

import test_mvp

OWNER = "Aftercare Lead"


class AiTaskOverrideAudit(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name) / "zavaforward.json"
        path.write_text(json.dumps(test_mvp.DATA))
        self.store: Any = Store(
            str(path),
            os.path.join(self.tmp.name, "live.json"),
            os.path.join(self.tmp.name, "audit.jsonl"),
        )
        self.sam, self.pam = test_mvp.DATA["staff"]
        self.store.ai.endpoint = "http://scripted-model.invalid"
        self.store.ai._chat = lambda *a, **k: "- ok [[Stage: Contacting resident]]"
        release_support.install(self.store)

    def record(self, rec_id: str) -> dict[str, Any]:
        return next(r for r in self.store.data["recommendations"] if r["id"] == rec_id)

    def audit_details(self, action: str) -> list[dict[str, Any]]:
        return [e for e in self.store.audit_entries() if e["action"] == action]

    def test_fresh_ai_output_is_unreviewed_and_unattributed(self) -> None:
        out = self.store.ai_run(self.sam, "ZF-1", "summary")
        rec = self.record(out["record_id"])
        self.assertEqual(rec["status"], ai_tasks.NOT_REVIEWED)
        self.assertIsNone(rec["reviewer_action"])
        self.assertIsNone(rec["resolved_by"])
        self.assertFalse(rec["provenance"]["human_reviewed"])
        self.assertEqual(self.audit_details("ai_review_accept"), [])

    def test_reject_and_edit_need_a_reason_and_leave_no_ratification(self) -> None:
        out = self.store.ai_run(self.sam, "ZF-1", "summary")
        for action in ("reject", "edit"):
            with self.assertRaises(ValueError):
                self.store.review_ai(self.sam, out["record_id"], action, "  ")
        with self.assertRaises(ValueError):
            self.store.review_ai(self.sam, out["record_id"], "approve")
        rec = self.record(out["record_id"])
        self.assertEqual(rec["status"], ai_tasks.NOT_REVIEWED)
        self.assertFalse(rec["provenance"]["human_reviewed"])

    def test_reject_records_the_named_reviewer_and_reason(self) -> None:
        out = self.store.ai_run(self.sam, "ZF-1", "summary")
        self.store.review_ai(self.sam, out["record_id"], "reject", "Does not match the file")
        rec = self.record(out["record_id"])
        self.assertEqual(rec["status"], "Rejected")
        self.assertEqual(
            (rec["reviewer_action"], rec["resolved_by"]), ("reject", self.sam["email"])
        )
        self.assertEqual(rec["reviewer_reason"], "Does not match the file")
        self.assertEqual(rec["review_evidence"]["reviewer"], self.sam["email"])
        entries = self.audit_details("ai_review_reject")
        self.assertEqual([e["who"] for e in entries], [self.sam["email"]])
        self.assertIn("Does not match the file", entries[0]["detail"])
        self.assertTrue(self.store.verify_audit())

    def test_edit_override_keeps_ai_text_and_the_person_s_wording(self) -> None:
        out = self.store.ai_run(self.sam, "ZF-1", "summary")
        original = self.record(out["record_id"])["ai_output"]
        self.store.review_ai(self.sam, out["record_id"], "edit", "Too stiff", "My own wording")
        rec = self.record(out["record_id"])
        self.assertEqual(rec["status"], "Edited")
        self.assertEqual(rec["override_text"], "My own wording")
        self.assertEqual(rec["ai_output"], original)
        self.assertEqual(rec["resolved_by"], self.sam["email"])
        self.assertEqual(
            [e["who"] for e in self.audit_details("ai_review_edit")], [self.sam["email"]]
        )

    def test_other_staff_cannot_ratify_or_reject_and_the_record_stays_unreviewed(self) -> None:
        out = self.store.ai_run(self.sam, "ZF-1", "summary")
        for action in ("accept", "reject"):
            with self.assertRaises(PermissionError):
                self.store.review_ai(self.pam, out["record_id"], action, "not mine")
        rec = self.record(out["record_id"])
        self.assertEqual(rec["status"], ai_tasks.NOT_REVIEWED)
        self.assertIsNone(rec["resolved_by"])

    def test_a_decided_record_cannot_be_flipped_to_acceptance(self) -> None:
        out = self.store.ai_run(self.sam, "ZF-1", "summary")
        self.store.review_ai(self.sam, out["record_id"], "reject", "Wrong case")
        with self.assertRaises(ValueError):
            self.store.review_ai(self.sam, out["record_id"], "accept")
        self.assertEqual(self.record(out["record_id"])["status"], "Rejected")
        self.assertEqual(self.audit_details("ai_review_accept"), [])

    def test_priority_suggestion_stays_proposed_until_a_person_rejects_it(self) -> None:
        self.store.ai._chat = lambda *a, **k: json.dumps(
            [dict(case_id="ZF-4", reason="Open safety issue", cites=["Open safety issues: 1"])]
        )
        rec = self.store.ai_priority(self.sam, 1)
        self.assertEqual(rec["status"], "Proposed")
        with self.assertRaises(PermissionError):
            self.store.resolve_priority(self.pam, rec["id"], "reject", "not mine")
        with self.assertRaises(ValueError):
            self.store.resolve_priority(self.sam, rec["id"], "reject", "")
        self.assertEqual(self.store.latest_priority(self.sam)["status"], "Proposed")
        self.store.resolve_priority(self.sam, rec["id"], "reject", "Known already")
        stored = self.record(rec["id"])
        self.assertEqual(stored["status"], "Rejected")
        self.assertEqual(stored["resolved_by"], self.sam["email"])
        self.assertIn(self.sam["email"], [e["who"] for e in self.store.audit_entries()])
        self.assertTrue(self.store.verify_audit())


class ConcernPackOverride(unittest.TestCase):
    def setUp(self) -> None:
        self.reg = AftercareRegister()
        self.cid = str(
            self.reg.raise_concern(
                route="digital",
                raised_by="household",
                home_ref="H1",
                kind="discomfort",
                statement="The living room stays cold in the evening.",
                owner=OWNER,
                next_update="2026-12-01",
            )["id"]
        )

    def test_ai_authored_pack_is_unapproved_and_cannot_self_ratify(self) -> None:
        pack = self.reg.propose_pack(
            self.cid, "Household reports a cold living room in the evening."
        )
        self.assertEqual(pack["source"], "ai")
        self.assertFalse(pack["approved"])
        self.assertIsNone(pack["review"])
        with self.assertRaises(PermissionError):
            self.reg.review_pack(str(pack["id"]), "AI assistant", "accept", "self-approved")
        self.assertFalse(self.reg.packs[str(pack["id"])]["approved"])

    def test_owner_rejection_is_attributed_and_final(self) -> None:
        pid = str(self.reg.propose_pack(self.cid)["id"])
        before = self.reg.view(self.cid)
        done = self.reg.review_pack(pid, f" {OWNER} ", "reject", "Not needed for this concern")
        self.assertEqual(done["review"]["by"], OWNER)
        self.assertEqual(done["review"]["reason"], "Not needed for this concern")
        self.assertEqual((done["approval"], done["approved"]), ("Rejected", False))
        self.assertEqual(self.reg.view(self.cid), before)
        with self.assertRaises(ValueError):
            self.reg.review_pack(pid, OWNER, "accept", "Changed mind")
        self.assertFalse(self.reg.packs[pid]["approved"])


if __name__ == "__main__":
    unittest.main()
