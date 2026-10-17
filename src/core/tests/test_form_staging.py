"""Source-linked collection mechanics over fictional data, never approval evidence."""

import copy
import hashlib
import json
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import patch

import dataset
from dataset import change_metadata
from zava_forward.core import forms
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, Store


def schema() -> dict[str, Any]:
    return dict(
        id="SYN-TECH",
        version=1,
        form_type="technical",
        template=dict(id="SYN-TEMPLATE", version="1", evidence_ref="SYN-NOT-APPROVED"),
        reviewer="pam@example.test",
        funding=dict(status="Not applicable", scheme_id=None, route=None, evidence_ref=None),
        rule_refs=[dict(id="SYN-RULE", version="1", evidence_ref="SYN-RULE-SOURCE")],
        fields=[
            dict(
                id="epc",
                section_id="home",
                type="enum",
                unit=None,
                options=list("ABCDEFG"),
                required=True,
                required_when=[],
                source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
                evidence_required=["certificate"],
                calculation_ref=None,
                category="value",
            ),
            dict(
                id="area",
                section_id="home",
                type="number",
                unit="m2",
                options=[],
                required=False,
                required_when=[dict(field_id="epc", equals="D")],
                source_authority=[dict(kind="EPC", rank=1, evidence_ref="SYN-POLICY")],
                evidence_required=["survey"],
                calculation_ref=dict(id="SYN-CALC", version="1", evidence_ref="SYN-FORMULA"),
                category="value",
            ),
        ],
    )


def batch(doc_id: str, raw: str = "D", start: int = 4) -> dict[str, Any]:
    return dict(
        schema_id="SYN-TECH",
        schema_version=1,
        document_id=doc_id,
        processing=dict(
            kind="text",
            parser="SYN-importer",
            parser_version="test-1",
            model_version=None,
            route_evidence=None,
            error_record=None,
        ),
        candidates=[dict(field_id="epc", raw_value=raw, locator=dict(start=start, end=start + 1))],
    )


class FormStaging(unittest.TestCase):
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

    def setup_source(self, store: Any, data: bytes = b"EPC D\nEPC E") -> dict[str, Any]:
        forms.register_schema(store, self.actor, schema())
        doc: dict[str, Any] = store.add_document(
            self.actor,
            "ZF-1",
            "synthetic.txt",
            "EPC",
            data,
            metadata=change_metadata(store, "ZF-1"),
        )
        return doc

    def reopen(self, store: Any) -> Any:
        if type(store) is Store:
            return Store(store.live_path)
        result = SqlStore("nonexistent-seed-is-not-read", store.db_path)
        self.addCleanup(result.db.close)
        return result

    def test_schema_contract_immutable_versions_no_approval_or_authority_inference(self) -> None:
        for store in self.stores:
            request = schema()
            result = forms.register_schema(store, self.actor, request)
            self.assertEqual(result["definition"], request)
            self.assertEqual(result["approval"], "Unapproved")
            self.assertIsNone(result["approval_evidence"])
            self.assertEqual(result["recorded_by"], self.actor["email"])
            self.assertEqual(len(result["digest"]), 64)
            result["definition"]["fields"].clear()
            self.assertEqual(
                len(forms.list_schemas(store, self.actor)[0]["definition"]["fields"]), 2
            )
            with self.assertRaises(ValueError):
                forms.register_schema(store, self.actor, schema())
            second = dict(schema(), version=2)
            forms.register_schema(store, self.actor, second)
            self.assertEqual(
                [
                    r["definition"]["version"]
                    for r in forms.list_schemas(self.reopen(store), self.actor)
                ],
                [1, 2],
            )

    def test_schema_rejects_bad_types_conditions_and_server_owned_overrides(self) -> None:
        for store in self.stores:
            for mutation in (
                {"approved": True},
                {"recorded_by": "forged"},
                {"version": True},
                {"version": 2},
                {"reviewer": "missing@example.test"},
            ):
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    forms.register_schema(store, self.actor, dict(schema(), **mutation))
            for key, value in (
                ("type", "object"),
                ("required", "yes"),
                ("unit", 12),
                ("required_when", [dict(field_id="missing", equals=True)]),
                ("source_authority", [dict(kind="EPC", rank=1, approved=True)]),
                ("options", [float("nan")]),
            ):
                bad = schema()
                bad["fields"][0][key] = value
                with self.subTest(key=key), self.assertRaises(ValueError):
                    forms.register_schema(store, self.actor, bad)
            self.assertEqual(forms.list_schemas(store, self.actor), [])

    def test_funding_unknown_and_not_applicable_are_distinct_unapproved_policy(self) -> None:
        for store in self.stores:
            funding = dict(
                schema(),
                form_type="funding",
                funding=dict(status="Unknown", scheme_id=None, route=None, evidence_ref=None),
            )
            result = forms.register_schema(store, self.actor, funding)
            self.assertEqual(result["definition"]["funding"]["status"], "Unknown")
            self.assertEqual(result["approval"], "Unapproved")
            with self.assertRaises(ValueError):
                forms.register_schema(
                    store, self.actor, dict(schema(), version=2, form_type="funding")
                )

    def test_staging_preserves_exact_sources_alternatives_and_controlled_state(self) -> None:
        for store in self.stores:
            doc = self.setup_source(store)
            before = copy.deepcopy(store._case("ZF-1"))
            request = batch(doc["id"])
            request["candidates"].append(
                dict(field_id="epc", raw_value="E", locator=dict(start=10, end=11))
            )
            saved = forms.stage_candidates(store, self.actor, "ZF-1", request)
            self.assertEqual(saved["status"], "Staged candidates only")
            self.assertEqual(saved["schema_version"], 1)
            self.assertEqual(
                saved["source"]["content_sha256"], hashlib.sha256(b"EPC D\nEPC E").hexdigest()
            )
            self.assertEqual(saved["source"]["version"], doc["version"])
            self.assertEqual(saved["processing"]["assertion_status"], "Supplied, unverified")
            self.assertEqual(saved["verification"]["verifier"], "form-source-locator-1")
            self.assertEqual(saved["verification"]["status"], "Exact source match")
            self.assertEqual([c["raw_value"] for c in saved["candidates"]], ["D", "E"])
            self.assertTrue(all(c["review_state"] == "Not reviewed" for c in saved["candidates"]))
            self.assertEqual(saved["source"]["authority"], "Not established")
            after = copy.deepcopy(store._case("ZF-1"))
            after.pop("form_staging")
            self.assertEqual(after, before)
            self.assertNotIn("form_staging", store.detail("ZF-1", self.actor))
            saved["candidates"].clear()
            retained = forms.list_candidates(self.reopen(store), self.actor, "ZF-1")
            self.assertEqual(len(retained[0]["candidates"]), 2)
            audit = json.dumps(list(store.audit_entries()))
            self.assertNotIn("raw_value", audit)
            self.assertTrue(store.verify_audit())

    def test_rescanned_sources_retain_full_batch_after_reads_and_sql_reopen(self) -> None:
        store = self.stores[1]
        forms.register_schema(store, self.actor, schema())
        for status in ("pending", "missing"):
            with self.subTest(scan=status):
                doc = store.add_document(
                    self.actor,
                    "ZF-1",
                    "synthetic.txt",
                    "EPC",
                    b"EPC D\nEPC E",
                    metadata=change_metadata(store, "ZF-1"),
                )
                with store.lock:
                    source = next(
                        d for d in store._case("ZF-1")["documents"] if d["id"] == doc["id"]
                    )
                    if status == "missing":
                        source.pop("scan")
                    else:
                        source["scan"]["status"] = status
                    store.save()
                result = forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
                self.assertEqual(result["candidates"][0]["raw_value"], "D")
                self.assertEqual(result["candidates"][0]["locator"], dict(start=4, end=5))
                self.assertEqual(
                    result["processing"],
                    dict(batch(doc["id"])["processing"], assertion_status="Supplied, unverified"),
                )
                for current in (store, self.reopen(store)):
                    for _ in range(2):
                        rows = forms.list_candidates(current, self.actor, "ZF-1")
                        self.assertEqual(next(r for r in rows if r["id"] == result["id"]), result)
                        self.assertNotIn("form_staging", current.detail("ZF-1", self.actor))
                    self.assertTrue(current.verify_audit())

    def test_rescan_final_save_failure_and_conflict_do_not_commit_batch_or_success_audit(
        self,
    ) -> None:
        store = self.stores[1]
        forms.register_schema(store, self.actor, schema())
        for failure in ("save", "conflict"):
            with self.subTest(failure=failure):
                doc = store.add_document(
                    self.actor,
                    "ZF-1",
                    "synthetic.txt",
                    "EPC",
                    b"EPC D",
                    metadata=change_metadata(store, "ZF-1"),
                )
                with store.lock:
                    source = next(
                        d for d in store._case("ZF-1")["documents"] if d["id"] == doc["id"]
                    )
                    source["scan"]["status"] = "pending"
                    store.save()
                original = store.save
                calls = 0

                def save(failure: str = failure, original: Callable[[], None] = original) -> None:
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        if failure == "save":
                            raise OSError("synthetic post-scan save failure")
                        other = self.reopen(store)
                        other.add_document(
                            self.actor,
                            "ZF-1",
                            "other.txt",
                            "EPC",
                            b"other",
                            metadata=change_metadata(other, "ZF-1"),
                        )
                    original()

                with patch.object(store, "save", side_effect=save):
                    with self.assertRaises(OSError if failure == "save" else ConflictError):
                        forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
                self.assertEqual(calls, 2)
                for current in (store, self.reopen(store)):
                    self.assertEqual(forms.list_candidates(current, self.actor, "ZF-1"), [])
                    self.assertNotIn(
                        "form_candidates_staged", json.dumps(list(current.audit_entries()))
                    )
                    self.assertTrue(current.verify_audit())

    def test_unicode_spans_and_quoted_multiline_csv_are_reproducible(self) -> None:
        for store in self.stores:
            doc = self.setup_source(store, "é EPC D\n".encode())
            saved = forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"], start=6))
            self.assertEqual(saved["candidates"][0]["locator"], dict(start=6, end=7))
            csv_doc = store.add_document(
                self.actor,
                "ZF-1",
                "synthetic.csv",
                "EPC",
                b'field,value\r\nepc,"D\nE"\r\n',
                metadata=change_metadata(store, "ZF-1"),
            )
            request = batch(csv_doc["id"])
            request["processing"]["kind"] = "csv"
            request["candidates"] = [
                dict(field_id="epc", raw_value="D\nE", locator=dict(row=2, column=2))
            ]
            saved = forms.stage_candidates(store, self.actor, "ZF-1", request)
            self.assertEqual(saved["candidates"][0]["raw_value"], "D\nE")

    def test_invalid_candidates_hash_or_foreign_source_never_partially_write(self) -> None:
        for store in self.stores:
            doc = self.setup_source(store)
            mutations = (
                {"schema_version": True},
                {"schema_version": 5},
                {"approved": True},
                {"source_authority": "forged"},
                {"processing": dict(batch(doc["id"])["processing"], verified=True)},
                {"candidates": [dict(field_id="epc", raw_value="E", locator=dict(start=4, end=5))]},
                {
                    "candidates": [
                        dict(field_id="epc", raw_value="D", locator=dict(start=-1, end=0))
                    ]
                },
                {
                    "candidates": [
                        dict(field_id="epc", raw_value="D", locator=dict(start=4, end=999))
                    ]
                },
                {
                    "candidates": [
                        dict(field_id="epc", raw_value="D", locator=dict(start=True, end=5))
                    ]
                },
                {
                    "candidates": [
                        dict(field_id="unknown", raw_value="D", locator=dict(start=4, end=5))
                    ]
                },
            )
            for mutation in mutations:
                with self.subTest(mutation=mutation), self.assertRaises((ValueError, KeyError)):
                    forms.stage_candidates(
                        store, self.actor, "ZF-1", dict(batch(doc["id"]), **mutation)
                    )
            with self.assertRaises(KeyError):
                forms.stage_candidates(store, self.actor, "ZF-2", batch(doc["id"]))
            mixed = batch(doc["id"])
            mixed["candidates"].append(
                dict(field_id="epc", raw_value="x", locator=dict(start=4, end=5))
            )
            with self.assertRaises(ValueError):
                forms.stage_candidates(store, self.actor, "ZF-1", mixed)
            store.docstore.put("ZF-1", doc["id"], b"EPC X", "text/plain")
            with self.assertRaises(ValueError):
                forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
            self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])

    def test_human_only_categories_never_prefilled(self) -> None:
        for store in self.stores:
            request = schema()
            request["fields"][0]["category"] = "declaration"
            forms.register_schema(store, self.actor, request)
            doc = store.add_document(
                self.actor,
                "ZF-1",
                "synthetic.txt",
                "EPC",
                b"EPC D",
                metadata=change_metadata(store, "ZF-1"),
            )
            with self.assertRaises(PermissionError):
                forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
            self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])

    def test_unreadable_unsupported_scan_is_owned_manual_recovery_not_values(self) -> None:
        for store in self.stores:
            self.setup_source(store)
            for name, raw in (("scan.pdf", b"%PDF-SYN-SCAN"), ("bad.txt", b"\xff")):
                doc = store.add_document(
                    self.actor, "ZF-1", name, "EPC", raw, metadata=change_metadata(store, "ZF-1")
                )
                result = forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
                self.assertEqual(result["status"], "Manual recovery required")
                self.assertEqual(result["candidates"], [])
                self.assertEqual(result["recovery"]["owner"], self.actor["email"])
                self.assertIn("manual", result["recovery"]["next_action"].lower())

    def test_ocr_lineage_is_import_assertion_not_route_approval_or_pixel_proof(self) -> None:
        for store in self.stores:
            self.setup_source(store)
            doc = store.add_document(
                self.actor,
                "ZF-1",
                "scan.pdf",
                "EPC",
                b"%PDF-SYN-SCAN",
                metadata=change_metadata(store, "ZF-1"),
            )
            request = batch(doc["id"])
            request["processing"].update(
                kind="ocr",
                parser="SYN-OCR",
                parser_version="2",
                model_version="SYN-model-7",
                route_evidence="SYN-UNAPPROVED-ROUTE",
                error_record="SYN-OCR-ERROR-LOG",
            )
            request["candidates"][0]["locator"] = dict(page=1, region="synthetic top left")
            result = forms.stage_candidates(store, self.actor, "ZF-1", request)
            self.assertEqual(result["processing"]["model_version"], "SYN-model-7")
            self.assertEqual(result["processing"]["error_record"], "SYN-OCR-ERROR-LOG")
            self.assertEqual(result["verification"]["status"], "Unverified OCR import")
            self.assertEqual(result["processing"]["assertion_status"], "Supplied, unverified")
            self.assertEqual(result["candidates"][0]["raw_value"], "D")

    def test_current_identity_rights_and_scan_rechecked_on_reads_and_writes(self) -> None:
        for store in self.stores:
            doc = self.setup_source(store)
            forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
            for actor in (
                dataset.DATA["staff"][0],
                dict(self.actor, role="Contractor"),
                dict(self.actor, role="Unknown"),
                dict(self.actor, name="Forged"),
            ):
                with self.assertRaises(PermissionError):
                    forms.list_candidates(store, actor, "ZF-1")
                with self.assertRaises(PermissionError):
                    forms.stage_candidates(store, actor, "ZF-1", batch(doc["id"]))
            with patch.dict("os.environ", {"ZF_REASON_ROLES": "Building Safety Liaison"}):
                with self.assertRaises(PermissionError):
                    forms.list_candidates(store, self.actor, "ZF-1")
            with store.lock:
                store._case("ZF-1")["documents"][0]["scan"]["status"] = "pending"
                store.save()
            self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])

    def test_failed_save_registry_and_candidate_are_not_locally_or_durably_replayed(self) -> None:
        for store in self.stores:
            with patch.object(store, "save", side_effect=OSError("synthetic disk failure")):
                with self.assertRaises(OSError):
                    forms.register_schema(store, self.actor, schema())
            self.assertEqual(forms.list_schemas(store, self.actor), [])
            doc = self.setup_source(store)
            with patch.object(store, "save", side_effect=OSError("synthetic disk failure")):
                with self.assertRaises(OSError):
                    forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
            self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])
            store.add_document(
                self.actor,
                "ZF-1",
                "unrelated.txt",
                "EPC",
                b"unrelated",
                metadata=change_metadata(store, "ZF-1"),
            )
            reopened = self.reopen(store)
            self.assertEqual(forms.list_candidates(reopened, self.actor, "ZF-1"), [])
            self.assertEqual(len(forms.list_schemas(reopened, self.actor)), 1)
            self.assertNotIn("form_candidates_staged", json.dumps(list(reopened.audit_entries())))

    def test_sql_transaction_fault_and_cross_process_conflict_restore_state(self) -> None:
        store = self.stores[1]
        with patch.object(store, "_append_audit", side_effect=OSError("synthetic audit failure")):
            with self.assertRaises(OSError):
                forms.register_schema(store, self.actor, schema())
        self.assertEqual(forms.list_schemas(store, self.actor), [])
        self.assertEqual(forms.list_schemas(self.reopen(store), self.actor), [])
        doc = self.setup_source(store)
        with patch.object(store, "_append_audit", side_effect=OSError("synthetic audit failure")):
            with self.assertRaises(OSError):
                forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
        self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])
        other = self.reopen(store)
        original = store.save

        def race() -> None:
            forms.register_schema(other, self.actor, dict(schema(), version=2))
            original()

        with patch.object(store, "save", side_effect=race):
            with self.assertRaises(ConflictError):
                forms.register_schema(store, self.actor, dict(schema(), version=2))
        self.assertEqual(len(forms.list_schemas(self.reopen(store), self.actor)), 2)
        forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
        self.assertEqual(len(forms.list_candidates(self.reopen(store), self.actor, "ZF-1")), 1)

    def test_sql_role_revocation_is_read_from_database_not_stale_staff_cache(self) -> None:
        store = self.stores[1]
        doc = self.setup_source(store)
        forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
        revoked = dict(self.actor, role="Programme Support Officer")
        store.db.execute(
            "UPDATE staff SET body=? WHERE email=?",
            (json.dumps(revoked), self.actor["email"]),
        )
        with self.assertRaises(PermissionError):
            forms.list_candidates(store, self.actor, "ZF-1")
        with self.assertRaises(PermissionError):
            forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))

    def test_json_audit_failure_restores_snapshot_without_replay(self) -> None:
        store = self.stores[0]
        with patch.object(store, "audit", side_effect=OSError("synthetic ledger failure")):
            with self.assertRaises(OSError):
                forms.register_schema(store, self.actor, schema())
        self.assertEqual(forms.list_schemas(self.reopen(store), self.actor), [])
        doc = self.setup_source(store)
        with patch.object(store, "audit", side_effect=OSError("synthetic ledger failure")):
            with self.assertRaises(OSError):
                forms.stage_candidates(store, self.actor, "ZF-1", batch(doc["id"]))
        self.assertEqual(forms.list_candidates(self.reopen(store), self.actor, "ZF-1"), [])
        forms.register_schema(store, self.actor, dict(schema(), version=2))
        self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])
        self.assertNotIn("form_candidates_staged", json.dumps(list(store.audit_entries())))

    def test_source_policy_missing_source_and_malformed_csv_safe_recovery(self) -> None:
        for store in self.stores:
            self.setup_source(store)
            restricted = store.add_document(
                self.actor,
                "ZF-1",
                "synthetic.txt",
                "Funding evidence",
                b"EPC D",
                metadata=change_metadata(store, "ZF-1"),
            )
            with self.assertRaises(PermissionError):
                forms.stage_candidates(store, self.actor, "ZF-1", batch(restricted["id"]))
            malformed = store.add_document(
                self.actor,
                "ZF-1",
                "bad.csv",
                "EPC",
                b'field,"unterminated',
                metadata=change_metadata(store, "ZF-1"),
            )
            request = batch(malformed["id"])
            request["processing"]["kind"] = "csv"
            result = forms.stage_candidates(store, self.actor, "ZF-1", request)
            self.assertEqual(result["status"], "Manual recovery required")
            self.assertEqual(result["candidates"], [])
            with store.lock:
                store._case("ZF-1")["documents"].clear()
                store.save()
            self.assertEqual(forms.list_candidates(store, self.actor, "ZF-1"), [])


if __name__ == "__main__":
    unittest.main()
