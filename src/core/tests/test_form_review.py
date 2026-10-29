"""Synthetic working-review evidence; no Finance or Board approvals."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset
from dataset import change_metadata
from test_form_staging import batch, schema
from zava_forward.core import form_review, forms
from zava_forward.core.doc_controls import DocumentUnavailable
from zava_forward.core.documents import DocumentStoreError
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store


class FormReview(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.stores: list[Any] = []
        for kind in ("json", "sql"):
            folder = Path(self.tmp.name) / kind
            folder.mkdir()
            seed = folder / "synthetic.json"
            seed.write_text(json.dumps(copy.deepcopy(dataset.DATA)))
            store: Any = (
                Store(str(seed))
                if kind == "json"
                else SqlStore(str(seed), str(folder / "synthetic.sqlite"))
            )
            if kind == "sql":
                self.addCleanup(store.db.close)
            self.stores.append(store)
        self.actor = dict(dataset.DATA["staff"][1])

    def reopen(self, store: Any) -> Any:
        if type(store) is Store:
            return Store(store.live_path)
        result = SqlStore("nonexistent-seed-not-read", store.db_path)
        self.addCleanup(result.db.close)
        return result

    def prepare(self, store: Any, definition: Any = None) -> tuple[Any, Any, Any]:
        forms.register_schema(store, self.actor, definition or schema())
        batches = []
        for field, raw in (("epc", "D"), ("area", "12")):
            doc = store.add_document(
                self.actor,
                "ZF-1",
                "synthetic.txt",
                "EPC",
                raw.encode(),
                metadata=change_metadata(store, "ZF-1"),
            )
            request = batch(doc["id"])
            request["candidates"] = [
                dict(field_id=field, raw_value=raw, locator=dict(start=0, end=len(raw)))
            ]
            batches.append(forms.stage_candidates(store, self.actor, "ZF-1", request))
        draft = form_review.action(
            store,
            self.actor,
            "ZF-1",
            dict(action="open", schema_id="SYN-TECH", schema_version=1),
        )
        return draft, batches[0], batches[1]

    def review(
        self,
        store: Any,
        draft: Any,
        staged: Any,
        field: str = "epc",
        decision: str = "accept",
        value: Any = None,
    ) -> Any:
        return form_review.action(
            store,
            self.actor,
            "ZF-1",
            dict(
                action="review",
                draft_id=draft["draft_id"],
                expected_version=draft["input_version"],
                field_id=field,
                decision=decision,
                batch_id=staged["id"] if decision != "reject" else None,
                candidate_id=staged["candidates"][0]["id"] if decision != "reject" else None,
                value=value,
                reason="SYN explicit reviewer note",
            ),
        )

    def prepare_shared_source(self, store: Any) -> tuple[Any, Any, Any]:
        draft, epc, other = self.prepare(store)
        request = batch(epc["source"]["id"])
        request["candidates"] = [dict(field_id="area", raw_value="D", locator=dict(start=0, end=1))]
        area = forms.stage_candidates(store, self.actor, "ZF-1", request)
        draft = self.review(store, draft, epc)
        draft = self.review(store, draft, area, "area", "correct", 12)
        return draft, epc, other

    def prepare_alternatives(self, store: Any) -> tuple[Any, list[Any]]:
        forms.register_schema(store, self.actor, schema())
        doc = store.add_document(
            self.actor,
            "ZF-1",
            "synthetic.txt",
            "EPC",
            b"DE",
            metadata=change_metadata(store, "ZF-1"),
        )
        staged = [
            forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"], raw, start))
            for start, raw in enumerate("DE")
        ]
        draft = form_review.action(
            store,
            self.actor,
            "ZF-1",
            dict(action="open", schema_id="SYN-TECH", schema_version=1),
        )
        return draft, staged

    def test_missing_bytes_block_stale_rejected_and_replaced_retained_history(self) -> None:
        for store in self.stores:
            draft, epc, _ = self.prepare(store)
            draft = self.review(store, draft, epc)
            draft = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(
                    action="diagnose",
                    draft_id=draft["draft_id"],
                    expected_version=draft["input_version"],
                ),
            )
            replacement = store.add_document(
                self.actor,
                "ZF-1",
                "replacement.txt",
                "EPC",
                b"E",
                metadata=change_metadata(store, "ZF-1"),
            )
            staged = forms.stage_candidates(
                store, self.actor, "ZF-1", batch(replacement["id"], "E", 0)
            )
            for state in ("rejected", "replaced", "stale-schema"):
                with self.subTest(store=type(store).__name__, state=state):
                    if state == "rejected":
                        draft = self.review(store, draft, epc, decision="reject")
                    elif state == "replaced":
                        draft = self.review(store, draft, staged)
                    else:
                        forms.register_schema(store, self.actor, dict(schema(), version=2))
                    before = copy.deepcopy(store._case("ZF-1"))
                    audit = list(store.audit_entries())
                    store.docstore.delete("ZF-1", epc["source"]["id"])
                    with (
                        patch.object(
                            store, "ensure_scanned", side_effect=AssertionError("No scan")
                        ),
                        patch.object(store.docstore, "put", side_effect=AssertionError("No put")),
                        patch.object(
                            store.docstore, "delete", side_effect=AssertionError("No delete")
                        ),
                    ):
                        with self.assertRaises(DocumentUnavailable):
                            form_review.view(store, self.actor, "ZF-1")
                        with self.assertRaises(DocumentUnavailable):
                            self.review(store, draft, staged, decision="reject")
                        with self.assertRaises(DocumentUnavailable):
                            form_review.action(
                                store,
                                self.actor,
                                "ZF-1",
                                dict(
                                    action="diagnose",
                                    draft_id=draft["draft_id"],
                                    expected_version=draft["input_version"],
                                ),
                            )
                    self.assertEqual(self.reopen(store)._case("ZF-1"), before)
                    self.assertEqual(list(store.audit_entries()), audit)
                    store.docstore.put("ZF-1", epc["source"]["id"], b"D", "text/plain")
                    restored = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
                    self.assertEqual(restored["history"], draft["history"])
                    self.assertEqual(
                        restored["recorded_diagnostics"], before["form_reviews"][0]["diagnostics"]
                    )

    def test_missing_snapshot_only_sources_block_each_retained_snapshot_surface(self) -> None:
        for store in self.stores:
            draft, epc, _ = self.prepare(store)
            draft = self.review(store, draft, epc)
            empty_fields = {
                fid: dict(value=None, state="Unknown", evidence=None) for fid in draft["fields"]
            }
            for surface in ("fields", "history", "prior", "attachments"):
                with self.subTest(store=type(store).__name__, surface=surface):
                    snapshot = dict(
                        draft, fields=copy.deepcopy(empty_fields), history=[], attachments=[]
                    )
                    if surface == "prior":
                        snapshot["history"] = [
                            dict(
                                draft["history"][0],
                                prior=copy.deepcopy(draft["fields"]["epc"]),
                                new=dict(value=None, state="Rejected", evidence=None),
                            )
                        ]
                    else:
                        snapshot[surface] = copy.deepcopy(draft[surface])
                    with store.lock:
                        saved = store._case("ZF-1")["form_reviews"][0]
                        saved["fields"] = copy.deepcopy(empty_fields)
                        saved["history"] = []
                        saved["diagnostics"] = [snapshot]
                        store.save()
                    before = copy.deepcopy(store._case("ZF-1"))
                    store.docstore.delete("ZF-1", epc["source"]["id"])
                    with self.assertRaises(DocumentUnavailable):
                        form_review.view(store, self.actor, "ZF-1")
                    self.assertEqual(self.reopen(store)._case("ZF-1"), before)
                    store.docstore.put("ZF-1", epc["source"]["id"], b"D", "text/plain")
                    report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
                    self.assertEqual(report["recorded_diagnostics"], [snapshot])

    def test_retained_history_snapshots_and_stale_schema_reuse_one_read_per_report(self) -> None:
        for store in self.stores:
            draft, epc, _ = self.prepare_shared_source(store)
            draft = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(
                    action="diagnose",
                    draft_id=draft["draft_id"],
                    expected_version=draft["input_version"],
                ),
            )
            forms.register_schema(store, self.actor, dict(schema(), version=2))
            with store.lock:
                doc = next(
                    d for d in store._case("ZF-1")["documents"] if d["id"] == epc["source"]["id"]
                )
                doc["version"] += 1
                store.save()
            for operation in ("view", "diagnose"):
                with self.subTest(store=type(store).__name__, operation=operation):
                    with patch.object(store.docstore, "get", wraps=store.docstore.get) as read:
                        if operation == "view":
                            with patch.object(store, "save", side_effect=AssertionError("No save")):
                                report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
                        else:
                            report = form_review.action(
                                store,
                                self.actor,
                                "ZF-1",
                                dict(
                                    action="diagnose",
                                    draft_id=draft["draft_id"],
                                    expected_version=draft["input_version"],
                                ),
                            )
                            draft = report
                    read.assert_called_once_with("ZF-1", epc["source"]["id"])
                    self.assertEqual(report["stale_fields"], ["area", "epc"])
                    self.assertEqual(report["history"], draft["history"])
            store.docstore.delete("ZF-1", epc["source"]["id"])
            with self.assertRaises(DocumentUnavailable):
                form_review.view(store, self.actor, "ZF-1")

    def test_retained_source_storage_outage_is_not_missing_or_stale(self) -> None:
        for store in self.stores:
            draft, epc, _ = self.prepare(store)
            draft = self.review(store, draft, epc)
            forms.register_schema(store, self.actor, dict(schema(), version=2))
            before = copy.deepcopy(store._case("ZF-1"))
            error = DocumentStoreError("SYN storage service unavailable")
            with patch.object(store.docstore, "get", side_effect=error):
                with self.assertRaises(DocumentStoreError) as raised:
                    form_review.view(store, self.actor, "ZF-1")
                self.assertIs(raised.exception, error)
                with self.assertRaises(DocumentStoreError):
                    self.review(store, draft, epc, decision="reject")
            self.assertEqual(self.reopen(store)._case("ZF-1"), before)

    def test_conflicts_exclude_unreviewable_alternatives_without_removing_staging(self) -> None:
        for store in self.stores:
            draft, staged = self.prepare_alternatives(store)
            self.assertTrue(any(i["status"] == "Conflict" for i in draft["issues"]))
            original = copy.deepcopy(store._case("ZF-1"))
            did = staged[0]["source"]["id"]
            for changed in (
                "version",
                "hash",
                "kind",
                "bytes",
                "missing",
                "pending",
                "deleted",
                "generated",
                "policy",
                "case",
            ):
                with self.subTest(store=type(store).__name__, changed=changed):
                    with store.lock:
                        case = store._case("ZF-1")
                        case["documents"] = copy.deepcopy(original["documents"])
                        case["form_staging"] = copy.deepcopy(original["form_staging"])
                        doc = next(d for d in case["documents"] if d["id"] == did)
                        if changed == "version":
                            doc["version"] += 1
                        elif changed == "hash":
                            doc["content_sha256"] = "0" * 64
                        elif changed in ("kind", "policy"):
                            doc["kind"] = "Survey"
                            if changed == "policy":
                                for row in case["form_staging"]:
                                    row["source"]["kind"] = "Survey"
                        elif changed == "pending":
                            doc["scan"]["status"] = "pending"
                        elif changed == "deleted":
                            case["documents"].remove(doc)
                        elif changed == "generated":
                            doc["generated"] = True
                        elif changed == "case":
                            for row in case["form_staging"]:
                                row["case_id"] = "ZF-2"
                        store.save()
                    if changed == "missing":
                        store.docstore.delete("ZF-1", did)
                    elif changed == "bytes":
                        store.docstore.put("ZF-1", did, b"EF", "text/plain")
                    before = copy.deepcopy(store._case("ZF-1")["form_staging"])
                    with patch.object(
                        store, "ensure_scanned", side_effect=AssertionError("No scan")
                    ):
                        report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
                        self.assertFalse(any(i["status"] == "Conflict" for i in report["issues"]))
                        report = form_review.action(
                            store,
                            self.actor,
                            "ZF-1",
                            dict(
                                action="diagnose",
                                draft_id=report["draft_id"],
                                expected_version=report["input_version"],
                            ),
                        )
                        self.assertFalse(any(i["status"] == "Conflict" for i in report["issues"]))
                        for row in staged:
                            with self.assertRaises((ValueError, PermissionError)):
                                self.review(store, report, row)
                    reopened = self.reopen(store)
                    self.assertEqual(reopened._case("ZF-1")["form_staging"], before)
                    self.assertEqual(
                        reopened._case("ZF-1")["form_reviews"][0]["diagnostics"][-1], report
                    )
                    self.assertEqual(report["history"], [])
                    store.docstore.put("ZF-1", did, b"DE", "text/plain")

    def test_conflict_policy_is_field_specific_with_shared_freshness_and_byte_reads(self) -> None:
        for store in self.stores:
            _, staged = self.prepare_alternatives(store)
            did = staged[0]["source"]["id"]
            with store.lock:
                case = store._case("ZF-1")
                doc = next(d for d in case["documents"] if d["id"] == did)
                doc["kind"] = "Survey"
                draft = case["form_reviews"][0]
                draft["schema"]["fields"][0]["source_authority"].append(
                    dict(kind="Survey", rank=2, evidence_ref="SYN-POLICY")
                )
                for row in case["form_staging"]:
                    row["source"]["kind"] = "Survey"
                    row["candidates"].append(dict(row["candidates"][0], field_id="area"))
                store.save()
            with patch.object(store.docstore, "get", wraps=store.docstore.get) as read:
                report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
            self.assertEqual(
                [i["field_id"] for i in report["issues"] if i["status"] == "Conflict"], ["epc"]
            )
            read.assert_called_once_with("ZF-1", did)
            report = self.review(store, report, staged[0])
            with patch.object(store.docstore, "get", wraps=store.docstore.get) as read:
                form_review.view(store, self.actor, "ZF-1")
            read.assert_called_once_with("ZF-1", did)

    def test_alternative_storage_outages_propagate_and_later_reports_recheck(self) -> None:
        for store in self.stores:
            draft, staged = self.prepare_alternatives(store)
            did = staged[0]["source"]["id"]
            before = copy.deepcopy(store._case("ZF-1"))
            audit = list(store.audit_entries())
            error = DocumentStoreError("SYN storage outage")
            with patch.object(store.docstore, "get", side_effect=error):
                with self.assertRaises(DocumentStoreError) as raised:
                    form_review.view(store, self.actor, "ZF-1")
                self.assertIs(raised.exception, error)
                with self.assertRaises(DocumentStoreError):
                    form_review.action(
                        store,
                        self.actor,
                        "ZF-1",
                        dict(
                            action="diagnose",
                            draft_id=draft["draft_id"],
                            expected_version=draft["input_version"],
                        ),
                    )
            self.assertEqual(self.reopen(store)._case("ZF-1"), before)
            self.assertEqual(list(store.audit_entries()), audit)
            with patch.object(store.docstore, "get", wraps=store.docstore.get) as read:
                report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
            self.assertTrue(any(i["status"] == "Conflict" for i in report["issues"]))
            read.assert_called_once_with("ZF-1", did)
            store.docstore.delete("ZF-1", did)
            with patch.object(store.docstore, "get", wraps=store.docstore.get) as read:
                report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
            read.assert_called_once_with("ZF-1", did)
            self.assertFalse(any(i["status"] == "Conflict" for i in report["issues"]))
            store.docstore.put("ZF-1", did, b"DE", "text/plain")
            report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
            self.assertTrue(any(i["status"] == "Conflict" for i in report["issues"]))

    def test_shared_source_read_once_per_report_and_rechecked_on_later_reports(self) -> None:
        for store in self.stores:
            draft, epc, _ = self.prepare_shared_source(store)
            for operation in ("view", "diagnose"):
                with self.subTest(store=type(store).__name__, operation=operation):
                    with patch.object(store.docstore, "get", wraps=store.docstore.get) as read:
                        for changed in (False, True):
                            if changed:
                                read.return_value = b"SYN changed bytes without metadata changes"
                            if operation == "view":
                                report = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
                            else:
                                report = form_review.action(
                                    store,
                                    self.actor,
                                    "ZF-1",
                                    dict(
                                        action="diagnose",
                                        draft_id=draft["draft_id"],
                                        expected_version=draft["input_version"],
                                    ),
                                )
                                draft = report
                            self.assertEqual(read.call_count, 2 if changed else 1)
                            read.assert_called_with("ZF-1", epc["source"]["id"])
                            self.assertEqual(
                                report["stale_fields"], ["area", "epc"] if changed else []
                            )
                            self.assertEqual(
                                report["fields"]["epc"]["effective_state"],
                                "Stale" if changed else "Accepted",
                            )
                            self.assertEqual(
                                report["fields"]["area"]["effective_state"],
                                "Stale" if changed else "Corrected",
                            )

    def test_report_freshness_separates_exact_source_identity(self) -> None:
        for store in self.stores:
            _, epc, other = self.prepare_shared_source(store)
            for key, value in (
                ("id", other["source"]["id"]),
                ("version", epc["source"]["version"] + 1),
                ("content_sha256", "0" * 64),
                ("kind", "Survey"),
            ):
                with self.subTest(store=type(store).__name__, key=key), store.lock:
                    case = store._case("ZF-1")
                    draft = copy.deepcopy(case["form_reviews"][0])
                    draft["fields"]["area"]["evidence"]["source"][key] = value
                    with patch.object(
                        form_review, "_current", wraps=form_review._current
                    ) as current:
                        report = form_review._report(store, case, draft)
                    self.assertEqual(current.call_count, 2)
                    self.assertEqual(report["stale_fields"], ["area"])
                    self.assertEqual(report["fields"]["epc"]["effective_state"], "Accepted")

    def test_isolated_accept_correct_reject_history_and_held_inputs_survive_reopen(self) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            before = copy.deepcopy(store._case("ZF-1"))
            draft = self.review(store, draft, area, "area", "correct", 12)
            sibling = copy.deepcopy(draft["fields"]["area"])
            draft = self.review(store, draft, epc)
            draft = self.review(store, draft, epc, decision="correct", value="C")
            draft = self.review(store, draft, epc, decision="reject")
            self.assertEqual(draft["fields"]["area"], sibling)
            self.assertEqual(
                [h["new"]["value"] for h in draft["history"] if h["field_id"] == "epc"],
                ["D", "C", None],
            )
            self.assertEqual(draft["history"][-1]["prior"]["value"], "C")
            self.assertTrue(all(h["reviewer"] == self.actor["email"] for h in draft["history"]))
            self.assertFalse(draft["reviewed_ready"])
            self.assertEqual(draft["approved_rule_validation"], "Not evaluated")
            after = copy.deepcopy(store._case("ZF-1"))
            after.pop("form_reviews")
            after.pop("finance_decision_holds")
            expected = copy.deepcopy(before)
            expected.pop("form_reviews")
            expected.pop("finance_decision_holds")
            self.assertEqual(after, expected)
            for key in ("form_reviews", "finance_decision_holds", "form_staging"):
                self.assertNotIn(key, store.detail("ZF-1", self.actor))
            result = form_review.view(self.reopen(store), self.actor, "ZF-1")
            holds = result["decision_holds"]
            self.assertEqual(
                [h["decision_id"] for h in holds], ["template-rules", "OD-12", "OD-15"]
            )
            self.assertTrue(all(h["status"] == "Held" for h in holds))
            self.assertTrue(all(h["approved_input"] is None for h in holds))
            self.assertTrue(all(h["approval_evidence"] is None for h in holds))
            self.assertEqual(result["drafts"][0]["history"], draft["history"])
            self.assertEqual(result["drafts"][0]["acceleration"]["approved_envelope"], None)
            self.assertEqual(
                result["drafts"][0]["acceleration"]["breach_assessment"], "Not evaluated"
            )
            self.assertTrue(store.verify_audit())
            self.assertNotIn("SYN explicit reviewer note", json.dumps(list(store.audit_entries())))

    def test_manifest_binds_exact_fields_sources_versions_and_history_without_finance_writes(
        self,
    ) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            draft = self.review(store, draft, epc)
            draft = self.review(store, draft, area, "area", "correct", 12)
            before = copy.deepcopy(store._case("ZF-1"))
            report = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(
                    action="diagnose",
                    draft_id=draft["draft_id"],
                    expected_version=draft["input_version"],
                ),
            )
            self.assertEqual(report["template"], schema()["template"])
            self.assertEqual(report["rule_refs"], schema()["rule_refs"])
            self.assertEqual(
                {fid: f["value"] for fid, f in report["fields"].items()},
                {"epc": "D", "area": 12},
            )
            self.assertEqual(report["fields"]["epc"]["evidence"]["locator"], {"start": 0, "end": 1})
            self.assertEqual(report["fields"]["epc"]["evidence"]["source"], epc["source"])
            self.assertEqual(report["fields"]["area"]["evidence"]["raw_value"], "12")
            self.assertEqual(
                {a["id"]: a["content_sha256"] for a in report["attachments"]},
                {b["source"]["id"]: b["source"]["content_sha256"] for b in (epc, area)},
            )
            saved = form_review.view(self.reopen(store), self.actor, "ZF-1")["drafts"][0]
            self.assertEqual(saved["recorded_diagnostics"], [report])
            self.assertEqual(report["history"], draft["history"])
            self.assertFalse(report["reviewed_ready"])
            self.assertIn("Not a reviewed", report["notice"])
            after = copy.deepcopy(store._case("ZF-1"))
            before.pop("form_reviews")
            after.pop("form_reviews")
            self.assertEqual(after, before)

    def test_source_and_schema_freshness_exact_draft_sets_preserve_unrelated_decisions(
        self,
    ) -> None:
        for store in self.stores:
            draft, epc, area = self.prepare(store)
            draft = self.review(store, draft, epc)
            draft = self.review(store, draft, area, "area", "correct", 12)
            history = copy.deepcopy(draft["history"])
            with store.lock:
                case = store._case("ZF-1")
                next(d for d in case["documents"] if d["id"] == epc["source"]["id"])["version"] += 1
                store.save()
            result = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
            self.assertEqual(result["stale_fields"], ["epc"])
            self.assertEqual(result["fields"]["area"]["effective_state"], "Corrected")
            self.assertEqual(result["history"], history)
            with self.assertRaises(ValueError):
                self.review(store, result, epc)
            forms.register_schema(store, self.actor, dict(schema(), version=2))
            result = form_review.view(self.reopen(store), self.actor, "ZF-1")["drafts"][0]
            self.assertEqual(result["stale_fields"], ["area", "epc"])
            self.assertEqual(result["history"], history)
            self.assertFalse(result["reviewed_ready"])

    def test_types_use_no_implicit_conversion_and_type_aware_equality(self) -> None:
        examples = (
            ("string", "D", True),
            ("string", 1, False),
            ("integer", 1, True),
            ("integer", True, False),
            ("integer", "1", False),
            ("number", 1.5, True),
            ("number", 1, True),
            ("number", True, False),
            ("number", float("inf"), False),
            ("number", float("nan"), False),
            ("boolean", True, True),
            ("boolean", "true", False),
            ("date", "2024-02-29", True),
            ("date", "2026-02-29", False),
            ("date", "2026-1-01", False),
            ("enum", 1, True),
            ("enum", True, False),
        )
        for kind, value, valid in examples:
            with self.subTest(kind=kind, value=value):
                self.assertEqual(form_review._valid(value, dict(type=kind, options=[1])), valid)
        self.assertFalse(form_review._equal(True, 1))
        for store in self.stores:
            draft, _, area = self.prepare(store)
            draft = self.review(store, draft, area, "area")
            self.assertEqual(draft["fields"]["area"]["value"], "12")
            self.assertTrue(any(i["status"] == "Fail" for i in draft["issues"]))
            draft = self.review(store, draft, area, "area", "correct", 12)
            self.assertFalse(any(i["status"] == "Fail" for i in draft["issues"]))
            with self.assertRaises(ValueError):
                self.review(store, draft, area, "area", "correct", float("nan"))

    def test_conditions_or_unknown_conflict_and_unreviewed_values_not_used(self) -> None:
        for store in self.stores:
            definition = schema()
            definition["fields"][1]["required_when"].append(dict(field_id="epc", equals="C"))
            draft, epc, area = self.prepare(store, definition)
            self.assertTrue(
                any(i["reason"] == "Conditional requirement is unknown." for i in draft["issues"])
            )
            doc_id = epc["source"]["id"]
            request = batch(doc_id)
            request["candidates"] = [
                dict(field_id="epc", raw_value="D", locator=dict(start=0, end=1)),
            ]
            forms.stage_candidates(store, self.actor, "ZF-1", request)
            # A second permitted source supplies a conflicting alternative.
            doc = store.add_document(
                self.actor,
                "ZF-1",
                "synthetic.txt",
                "EPC",
                b"E",
                metadata=change_metadata(store, "ZF-1"),
            )
            forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"], "E", 0))
            result = form_review.view(store, self.actor, "ZF-1")["drafts"][0]
            self.assertTrue(any(i["status"] == "Conflict" for i in result["issues"]))
            draft = self.review(store, result, epc, decision="correct", value="C")
            self.assertTrue(
                any(
                    i["field_id"] == "area"
                    and i["reason"] == "Required confirmed input is missing."
                    for i in draft["issues"]
                )
            )
            draft = self.review(store, draft, epc, decision="correct", value=True)
            self.assertTrue(any(i["status"] == "Fail" for i in draft["issues"]))
            self.assertTrue(
                any(i["reason"] == "Conditional requirement is unknown." for i in draft["issues"])
            )
            self.assertFalse(draft["reviewed_ready"])

    def test_pending_missing_infected_or_deleted_evidence_never_scans_or_discloses_history(
        self,
    ) -> None:
        for store in self.stores:
            draft, epc, _ = self.prepare(store)
            draft = self.review(store, draft, epc)
            before_history = copy.deepcopy(draft["history"])
            for status in ("pending", "missing", "infected"):
                with store.lock:
                    doc = next(
                        d
                        for d in store._case("ZF-1")["documents"]
                        if d["id"] == epc["source"]["id"]
                    )
                    if status == "missing":
                        doc.pop("scan", None)
                    else:
                        doc["scan"] = dict(status=status)
                    store.save()
                with patch.object(store, "ensure_scanned", side_effect=AssertionError("No scan")):
                    with self.assertRaises(DocumentUnavailable):
                        form_review.view(store, self.actor, "ZF-1")
                    with self.assertRaises(DocumentUnavailable):
                        self.review(store, draft, epc, decision="reject")
                self.assertEqual(store._case("ZF-1")["form_reviews"][0]["history"], before_history)
            with store.lock:
                store._case("ZF-1")["documents"] = [
                    d for d in store._case("ZF-1")["documents"] if d["id"] != epc["source"]["id"]
                ]
                store.save()
            with self.assertRaises(DocumentUnavailable):
                form_review.view(self.reopen(store), self.actor, "ZF-1")
            self.assertEqual(store._case("ZF-1")["form_reviews"][0]["history"], before_history)

    def test_foreign_candidate_role_forgery_human_only_and_version_rejected(self) -> None:
        for store in self.stores:
            definition = schema()
            extra = dict(copy.deepcopy(definition["fields"][0]), id="sign", category="signature")
            definition["fields"].append(extra)
            draft, epc, _ = self.prepare(store, definition)
            for actor in (dataset.DATA["staff"][0], dict(self.actor, name="Forged")):
                with self.assertRaises(PermissionError):
                    form_review.view(store, actor, "ZF-1")
                with self.assertRaises(PermissionError):
                    form_review.action(
                        store,
                        actor,
                        "ZF-1",
                        dict(action="open", schema_id="SYN-TECH", schema_version=1),
                    )
            with self.assertRaises(PermissionError):
                self.review(store, draft, epc, field="sign")
            with self.assertRaises(ValueError):
                self.review(store, draft, epc, field="area")
            with self.assertRaises(KeyError):
                form_review.action(
                    store,
                    self.actor,
                    "ZF-2",
                    dict(action="diagnose", draft_id=draft["draft_id"], expected_version=1),
                )
            with self.assertRaises(ValueError):
                form_review.action(
                    store,
                    self.actor,
                    "ZF-1",
                    dict(action="open", schema_id="SYN-TECH", schema_version=1, approved=True),
                )
            self.review(store, draft, epc)
            with self.assertRaises(ConflictError):
                self.review(store, draft, epc)

    def test_failed_save_and_audit_leave_no_review_or_hold_success(self) -> None:
        for store in self.stores:
            forms.register_schema(store, self.actor, schema())
            for method in ("save", "audit"):
                with patch.object(store, method, side_effect=OSError("Synthetic failure")):
                    with self.assertRaises(OSError):
                        form_review.action(
                            store,
                            self.actor,
                            "ZF-1",
                            dict(action="open", schema_id="SYN-TECH", schema_version=1),
                        )
                reopened = self.reopen(store)
                self.assertEqual(form_review.view(reopened, self.actor, "ZF-1")["drafts"], [])
                self.assertEqual(
                    form_review.view(reopened, self.actor, "ZF-1")["decision_holds"], []
                )
                self.assertTrue(reopened.verify_audit())
        # A failed final write must not leave a review in existing history.
        for store in self.stores:
            doc = store.add_document(
                self.actor,
                "ZF-1",
                "synthetic.txt",
                "EPC",
                b"D",
                metadata=change_metadata(store, "ZF-1"),
            )
            staged = forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"], "D", 0))
            draft = form_review.action(
                store,
                self.actor,
                "ZF-1",
                dict(action="open", schema_id="SYN-TECH", schema_version=1),
            )
            method = "_append_audit" if hasattr(store, "db") else "save"
            with patch.object(store, method, side_effect=OSError("Synthetic final write failure")):
                with self.assertRaises(OSError):
                    self.review(store, draft, staged)
            result = form_review.view(self.reopen(store), self.actor, "ZF-1")
            self.assertEqual(result["drafts"][0]["history"], [])
            self.assertEqual(len(result["decision_holds"]), 3)
            self.assertTrue(store.verify_audit())

    def test_sql_independent_writer_conflict_and_transactional_actor_recheck(self) -> None:
        store = self.stores[1]
        draft, epc, _ = self.prepare(store)
        other = self.reopen(store)
        original = store.save

        def race() -> None:
            self.review(other, draft, epc, decision="correct", value="C")
            original()

        with patch.object(store, "save", side_effect=race):
            with self.assertRaises(ConflictError):
                self.review(store, draft, epc)
        current = form_review.view(self.reopen(store), self.actor, "ZF-1")["drafts"][0]
        self.assertEqual(current["fields"]["epc"]["value"], "C")
        self.assertEqual(len(current["history"]), 1)
        self.assertTrue(store.verify_audit())

        def revoke() -> None:
            store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (
                    json.dumps(dict(self.actor, role="Programme Support Officer")),
                    self.actor["email"],
                ),
            )
            original()

        with patch.object(store, "save", side_effect=revoke):
            with self.assertRaises(PermissionError):
                self.review(store, current, epc, decision="reject")
        self.assertEqual(store._case("ZF-1")["form_reviews"][0]["fields"]["epc"]["value"], "C")


if __name__ == "__main__":
    unittest.main()
