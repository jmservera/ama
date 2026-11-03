"""Held draft export of a working review; synthetic data, no Finance authority."""

import unittest
from typing import Any

import test_form_review
from zava_forward.core import form_export


class FormExport(unittest.TestCase):
    def setUp(self) -> None:
        self.base = test_form_review.FormReview()
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.stores = self.base.stores
        self.actor = self.base.actor
        self.prepare = self.base.prepare
        self.review = self.base.review

    def export(self, store: Any, draft: Any) -> Any:
        return form_export.draft_export(store, self.actor, "ZF-1", draft["draft_id"])

    def test_export_is_held_and_links_evidence_without_authority(self) -> None:
        for store in self.stores:
            draft, epc, _area = self.prepare(store)
            draft = self.review(store, draft, epc)
            before = store.audit_log[:] if hasattr(store, "audit_log") else None
            out = self.export(store, draft)
            with self.subTest(store=type(store).__name__):
                self.assertEqual(out["status"], "Held")
                self.assertIs(out["reviewed"], False)
                self.assertEqual(out["submission"], "Not submitted")
                self.assertEqual(out["eligibility"], "Not assessed")
                row = next(f for f in out["fields"] if f["field_id"] == "epc")
                self.assertEqual(row["state"], "Accepted")
                self.assertEqual(
                    row["source_id"], draft["history"][-1]["new"]["evidence"]["source"]["id"]
                )
                self.assertIsNotNone(row["document_hash"])
                self.assertIsNotNone(row["locator"])
                self.assertEqual(out["input_version"], draft["input_version"])
                self.assertEqual(out["schema_digest"], draft["schema_digest"])
                self.assertTrue(out["attachments"])
                self.assertIn("not submit", out["notice"])
                self.assertIn("Unknown", {i["status"] for i in out["open_issues"]})
                for key in ("reviewed_ready", "approved", "award", "payment"):
                    self.assertNotIn(key, out)
                if before is not None:
                    self.assertEqual(store.audit_log, before)

    def test_export_digest_is_deterministic_and_tracks_changes(self) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            first = self.export(store, draft)
            self.assertEqual(first["content_sha256"], self.export(store, draft)["content_sha256"])
            self.assertEqual(draft["input_version"], first["input_version"])
            changed = self.review(store, draft, epc)
            second = self.export(store, changed)
            self.assertNotEqual(first["content_sha256"], second["content_sha256"])

    def test_unknown_draft_is_refused_and_fresh_export_has_no_stale_fields(self) -> None:
        store = self.stores[0]
        draft, epc, _area = self.prepare(store)
        draft = self.review(store, draft, epc)
        self.assertEqual(self.export(store, draft)["stale_fields"], [])
        with self.assertRaises(KeyError):
            form_export.draft_export(store, self.actor, "ZF-1", "missing")


if __name__ == "__main__":
    unittest.main()
