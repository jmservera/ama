"""Held draft export of a working review; synthetic data, no Finance authority."""

import unittest
from typing import Any

import test_form_review
from zava_forward.core import form_export, forms


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

    def test_export_carries_ordered_detached_review_history(self) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            with self.subTest(store=type(store).__name__):
                empty = self.export(store, draft)
                self.assertEqual(empty["history"], [])
                draft = self.review(store, draft, epc)
                draft = self.review(store, draft, epc, "epc", "correct", "C")
                draft = self.review(store, draft, epc, "epc", "reject")
                draft = self.review(store, draft, area, "area")
                saved = self.export(store, draft)
                with store.lock:
                    stored = store._case("ZF-1")["form_reviews"][0]["history"]
                    self.assertEqual(saved["history"], stored)
                self.assertEqual(
                    [(e["field_id"], e["decision"]) for e in saved["history"]],
                    [("epc", "accept"), ("epc", "correct"), ("epc", "reject"), ("area", "accept")],
                )
                self.assertIsNotNone(saved["history"][2]["prior"]["evidence"])
                saved["history"][0]["reason"] = "changed"
                with store.lock:
                    self.assertNotEqual(
                        store._case("ZF-1")["form_reviews"][0]["history"][0]["reason"], "changed"
                    )
                saved = self.export(store, draft)
                self.assertEqual(saved, self.export(store, draft))
                newer = self.review(store, draft, area, "area")
                again = self.export(store, newer)
                self.assertNotEqual(again["content_sha256"], saved["content_sha256"])
                self.assertEqual(len(saved["history"]), 4)
                self.assertEqual(
                    form_export.export_freshness(store, self.actor, "ZF-1", saved)["status"],
                    "Stale",
                )

    def test_history_is_integrity_covered_and_legacy_copy_is_invalid(self) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            draft = self.review(store, self.review(store, draft, epc), area, "area")
            saved = self.export(store, draft)
            legacy = {k: v for k, v in saved.items() if k != "history"}
            legacy["content_sha256"] = form_export._digest(
                {k: legacy[k] for k in form_export.BODY_KEYS if k != "history"}
            )
            reordered = dict(saved, history=list(reversed(saved["history"])))
            removed = dict(saved, history=saved["history"][:1])
            for name, bad in (("legacy", legacy), ("reordered", reordered), ("removed", removed)):
                with self.subTest(store=type(store).__name__, case=name):
                    out = form_export.export_freshness(store, self.actor, "ZF-1", bad)
                    self.assertEqual(out["status"], "Invalid")
                    self.assertIn("Create a new held export", out["action"])
            ok = form_export.export_freshness(store, self.actor, "ZF-1", saved)
            self.assertEqual(ok["status"], "Current")

    def test_unknown_draft_is_refused_and_fresh_export_has_no_stale_fields(self) -> None:
        store = self.stores[0]
        draft, epc, _area = self.prepare(store)
        draft = self.review(store, draft, epc)
        self.assertEqual(self.export(store, draft)["stale_fields"], [])
        with self.assertRaises(KeyError):
            form_export.draft_export(store, self.actor, "ZF-1", "missing")

    def test_saved_export_goes_stale_only_for_dependent_fields(self) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            draft = self.review(store, draft, epc)
            saved = self.export(store, draft)
            with self.subTest(store=type(store).__name__):
                fresh = form_export.export_freshness(store, self.actor, "ZF-1", saved)
                self.assertEqual(fresh["status"], "Current")
                self.assertEqual(fresh["stale_fields"], [])
                self.assertFalse(fresh["reviewed"])
                with store.lock:
                    case = store._case("ZF-1")
                    doc = next(d for d in case["documents"] if d["id"] == epc["source"]["id"])
                    doc["version"] += 1
                    store.save()
                stale = form_export.export_freshness(store, self.actor, "ZF-1", saved)
                self.assertEqual(stale["status"], "Stale")
                self.assertEqual(stale["stale_fields"], ["epc"])
                self.assertIn("area", stale["unaffected_fields"])

    def test_input_and_schema_changes_stale_saved_export(self) -> None:
        store = self.stores[0]
        draft, epc, area = self.prepare(store)
        draft = self.review(store, draft, epc)
        saved = self.export(store, draft)
        draft = self.review(store, dict(draft, input_version=2), area, "area", "correct", 12)
        changed = form_export.export_freshness(store, self.actor, "ZF-1", saved)
        self.assertEqual(changed["status"], "Stale")
        self.assertEqual(changed["stale_fields"], ["area"])
        self.assertEqual(changed["reasons"], ["Reviewed field inputs changed after this export."])
        saved = self.export(store, draft)
        forms.register_schema(store, self.actor, test_form_review.rule_successor())
        newer = form_export.export_freshness(store, self.actor, "ZF-1", saved)
        self.assertEqual(newer["status"], "Stale")
        self.assertEqual(newer["stale_fields"], ["area", "epc"])

    def test_edited_or_incomplete_saved_export_is_invalid_not_trusted(self) -> None:
        store = self.stores[0]
        draft, epc, _area = self.prepare(store)
        saved = self.export(store, self.review(store, draft, epc))
        edited = dict(saved, content_sha256="0" * 64)
        for bad in (edited, {k: v for k, v in saved.items() if k != "fields"}, {}):
            out = form_export.export_freshness(store, self.actor, "ZF-1", bad)
            self.assertEqual(out["status"], "Invalid")
            self.assertEqual(out["stale_fields"], [])
        tampered = dict(saved, fields=[])
        self.assertEqual(
            form_export.export_freshness(store, self.actor, "ZF-1", tampered)["status"], "Invalid"
        )

    def test_missing_or_other_case_draft_is_unavailable_not_keyerror(self) -> None:
        store = self.stores[0]
        draft, epc, _area = self.prepare(store)
        saved = self.export(store, self.review(store, draft, epc))
        other = dict(saved, draft_id="FR-missing")
        body = {key: other[key] for key in form_export.BODY_KEYS}
        other["content_sha256"] = form_export._digest(body)
        for case_id, candidate in (("ZF-1", other), ("ZF-404", saved)):
            with self.subTest(case_id=case_id):
                out = form_export.export_freshness(store, self.actor, case_id, candidate)
                self.assertEqual(out["status"], "Unavailable")
                self.assertEqual(out["stale_fields"], [])
                self.assertIs(out["reviewed"], False)


if __name__ == "__main__":
    unittest.main()
