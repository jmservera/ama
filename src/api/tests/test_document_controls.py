from dataset import change_metadata
import base64
import copy
import json
import os
import tempfile
import unittest
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import test_mvp
import test_ui_support as ui_support
from zava_forward.core import (
    ai_tasks,
    assistants,
    chat_case_answers,
    data_protection,
    forms,
    home_case,
    projection,
)
from zava_forward.core.doc_controls import (
    DEFENDER_TAG,
    DefenderForStorageScanner,
    DocumentUnavailable,
    LocalSignatureScanner,
    EICAR_SIGNATURE,
    TEST_MARKER,
    open_scanner,
)
from zava_forward.core.documents import AzureBlobDocumentStore
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from test_documents import FakeBlob

SAM, PAM = test_mvp.DATA["staff"]
FIXTURES = json.loads(
    (
        Path(__file__).resolve().parents[3] / "src/core/evals/document_control_fixtures.json"
    ).read_text()
)
AS_OF = date.fromisoformat(FIXTURES["as_of"])


def payload(kind, scan_class):
    magic = b"\x89PNG\r\n\x1a\n" if kind == "Photo" else b"%PDF-1.4 "
    if scan_class == "test-marker":
        return magic + TEST_MARKER
    if scan_class == "type-mismatch":
        return b"plain text pretending to be a file"
    return magic + b"synthetic body"


class DefenderBlob(FakeBlob):
    """FakeBlob that also answers the blob index tag read."""

    def __init__(self, result=None):
        super().__init__()
        self.result = result

    def __call__(self, method, url, headers, body, timeout=20):
        if "comp=tags" in url:
            if self.result is None:
                return 200, {}, b"<Tags><TagSet></TagSet></Tags>"
            return (
                200,
                {},
                f"<Tags><TagSet><Tag><Key>{DEFENDER_TAG}</Key><Value>{self.result}</Value></Tag></TagSet></Tags>".encode(),
            )
        return super().__call__(method, url, headers, body, timeout)


class Base(unittest.TestCase):
    sql = False

    def make(self, cases=None, *, sql=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(test_mvp.DATA)
        data["cases"] += cases or []
        p = Path(tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(data))
        use_sql = self.sql if sql is None else sql
        return SqlStore(str(p), os.path.join(tmp.name, "pw.sqlite")) if use_sql else Store(str(p))

    def actions(self, st):
        return [e["action"] for e in st.audit_entries()]


class ScanTests(Base):
    def test_clean_upload_is_available_and_scan_is_recorded(self):
        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1.4 ok", metadata=change_metadata(st, "ZF-1")
        )
        self.assertEqual(doc["scan"]["status"], "clean")
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1.4 ok")

    def test_infected_and_mismatched_uploads_are_deleted_and_never_recorded(self):
        st = self.make()
        for name, data in (
            ("a.pdf", b"%PDF-" + TEST_MARKER),
            ("b.pdf", b"not a pdf"),
            ("c.png", b"%PDF-1"),
            ("d.txt", b"a\x00b"),
        ):
            with self.assertRaises(ValueError):
                st.add_document(
                    SAM, "ZF-1", name, "EPC", data, metadata=change_metadata(st, "ZF-1")
                )
        self.assertEqual(st.detail("ZF-1")["documents"], [])
        self.assertEqual(st.docstore.list_ids("ZF-1"), [])
        self.assertEqual(self.actions(st).count("upload_document_rejected"), 4)

    def test_standard_eicar_file_is_refused_and_not_kept(self):
        st = self.make()
        for name in ("eicar.txt", "eicar.pdf"):
            with self.assertRaises(ValueError):
                st.add_document(
                    SAM,
                    "ZF-1",
                    name,
                    "EPC",
                    b"%PDF-1\n" + EICAR_SIGNATURE,
                    metadata=change_metadata(st, "ZF-1"),
                )
        self.assertEqual(st.detail("ZF-1")["documents"], [])
        self.assertEqual(st.docstore.list_ids("ZF-1"), [])
        self.assertEqual(
            LocalSignatureScanner().scan(
                "ZF-1", "d", "a.txt", b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE", "text/plain"
            )[0],
            "clean",
        )

    def test_unscanned_document_is_blocked_while_scan_pending(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob
        )
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        del st._case("ZF-1")["documents"][0]["scan"]
        with self.assertRaises(DocumentUnavailable):
            st.get_document("ZF-1", doc["id"], SAM)
        with self.assertRaises(DocumentUnavailable):
            st.read_document(SAM, "ZF-1", doc["id"])

    def test_pending_defender_scan_blocks_until_clean(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob
        )
        st.scanner = open_scanner(st.docstore, {"ZF_SCANNER": "defender"})
        self.assertIsInstance(st.scanner, DefenderForStorageScanner)
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        self.assertEqual(doc["scan"]["status"], "pending")
        with self.assertRaises(DocumentUnavailable):
            st.get_document("ZF-1", doc["id"], SAM)
        blob.result = "No threats found"
        self.assertEqual(st.rescan_document(SAM, "ZF-1", doc["id"])["status"], "clean")
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1")

    def test_pending_rescans_on_read_and_by_job(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob
        )
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        self.assertEqual(st.rescan_pending()["pending"], 1)
        blob.result = "No threats found"
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1")
        blob.result = None
        st.add_document(
            SAM, "ZF-1", "b.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        blob.result = "Malicious"
        self.assertEqual(st.rescan_pending()["removed"], 1)

    def test_upload_without_a_scanner_is_refused_and_leaves_nothing_available(self):
        st = self.make()
        st.scanner = None
        before = len(st.detail("ZF-1")["documents"])
        with self.assertRaisesRegex(RuntimeError, "remains unavailable"):
            st.add_document(
                SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
            )
        self.assertEqual(len(st.detail("ZF-1")["documents"]), before)
        self.assertEqual(list(st.docstore.list_ids("ZF-1")), [])

    def test_document_without_scan_field_is_scanned_on_first_use(self):
        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        for d in st._case("ZF-1")["documents"]:
            d.pop("scan", None)
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1")
        self.assertEqual(st.detail("ZF-1")["documents"][-1]["scan"]["status"], "clean")

    def test_blob_kept_when_save_fails(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob
        )
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        blob.result = "Malicious"

        def boom():
            raise OSError("save failed")

        st.save = boom
        with self.assertRaises(OSError):
            st.rescan_document(SAM, "ZF-1", doc["id"])
        self.assertEqual(len(blob.blobs), 1)
        self.assertEqual(len(st.detail("ZF-1")["documents"]), 1)

    def test_defender_malicious_result_removes_the_document(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob
        )
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        blob.result = "Malicious"
        with self.assertRaises(ValueError):
            st.rescan_document(SAM, "ZF-1", doc["id"])
        self.assertEqual(st.detail("ZF-1")["documents"], [])
        self.assertEqual(blob.blobs, {})

    def test_synthetic_scanner_on_blob_store_warns_but_stays_fail_closed(self):
        blob = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=DefenderBlob()
        )
        with self.assertLogs("zava_forward.core.doc_controls", "WARNING") as logs:
            self.assertIsInstance(open_scanner(blob, {}), LocalSignatureScanner)
        self.assertIn("no malware assurance", logs.output[0])
        with self.assertNoLogs("zava_forward.core.doc_controls", "WARNING"):
            open_scanner(None, {})
            open_scanner(blob, {"ZF_SCANNER": "defender"})

    def test_scanner_config(self):
        self.assertIsInstance(open_scanner(None, {}), LocalSignatureScanner)
        with self.assertRaises(ValueError):
            open_scanner(None, {"ZF_SCANNER": "x"})
        with self.assertRaises(ValueError):
            open_scanner(object(), {"ZF_SCANNER": "defender"})

    def test_synthetic_stock_fixtures_scan_as_labelled(self):
        self.assertEqual(len(FIXTURES["cases"]), 120)
        st = self.make()
        seen = set()
        for fx in FIXTURES["cases"]:
            for u in fx["uploads"]:
                data = payload(u["kind"], u["scan_class"])
                if u["scan_class"] == "clean":
                    st.add_document(
                        SAM,
                        "ZF-1",
                        u["name"],
                        u["kind"],
                        data,
                        metadata=change_metadata(st, "ZF-1"),
                    )
                else:
                    with self.assertRaises(ValueError):
                        st.add_document(
                            SAM,
                            "ZF-1",
                            u["name"],
                            u["kind"],
                            data,
                            metadata=change_metadata(st, "ZF-1"),
                        )
                seen.add(u["scan_class"])
        self.assertEqual(seen, {"clean", "test-marker", "type-mismatch"})
        self.assertTrue(all(d["scan"]["status"] == "clean" for d in st.detail("ZF-1")["documents"]))

    def test_quarantine_blocks_download_and_derivative_use_until_clean(self):
        for use_sql in (False, True):
            with self.subTest(sql=use_sql):
                self._check_quarantine_gate(use_sql)

    def _check_quarantine_gate(self, use_sql):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        seed_path = str(Path(tmp.name) / "zavaforward.json")
        db_path = os.path.join(tmp.name, "pw.sqlite")
        Path(seed_path).write_text(json.dumps(copy.deepcopy(test_mvp.DATA)))
        blob = DefenderBlob()
        st = SqlStore(seed_path, db_path) if use_sql else Store(seed_path)
        st.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob
        )
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1.4 ok", metadata=change_metadata(st, "ZF-1")
        )
        with st.lock:
            if hasattr(st, "_touch"):
                st._touch("ZF-1")
            case = st._case("ZF-1")
            case["form_staging"] = [{"batch_id": "B-1", "source": {"id": doc["id"]}}]
            case["documents"][0]["summary"] = "SYN summary"
            st.save()

        states = (
            (None, {"scan": None}),
            (None, {}),
            (
                None,
                {
                    "scan": {
                        "status": "pending",
                        "scanner": "s",
                        "at": "2026-11-15T00:00:00",
                        "detail": "p",
                    }
                },
            ),
            (
                "No threats found",
                {
                    "scan": {
                        "status": "failed",
                        "scanner": "s",
                        "at": "2026-11-15T00:00:00",
                        "detail": "f",
                    }
                },
            ),
            (
                "No threats found",
                {
                    "scan": {
                        "status": "infected",
                        "scanner": "s",
                        "at": "2026-11-15T00:00:00",
                        "detail": "i",
                    }
                },
            ),
            (
                "No threats found",
                {
                    "scan": {
                        "status": "clean",
                        "scanner": "s",
                        "at": "2026-11-15T00:00:00",
                        "detail": "c",
                    },
                    "scan_status": "infected",
                },
            ),
        )
        for tag_result, fields in states:
            with self.subTest(fields=fields):
                blob.result = tag_result
                with st.lock:
                    if hasattr(st, "_touch"):
                        st._touch("ZF-1")
                    raw_doc = st._case("ZF-1")["documents"][0]
                    raw_doc.pop("scan", None)
                    raw_doc.pop("scan_status", None)
                    raw_doc.update(copy.deepcopy(fields))
                    raw_doc["summary"] = "SYN summary"
                    st.save()

                with self.assertRaises(DocumentUnavailable):
                    st.get_document("ZF-1", doc["id"], SAM)
                with self.assertRaises(DocumentUnavailable):
                    st.read_document(SAM, "ZF-1", doc["id"])
                if fields:
                    with self.assertRaises(DocumentUnavailable):
                        ai_tasks.run_document(st, SAM, "ZF-1", raw_doc, b"%PDF-1.4 ok")
                    for mode_env in ({"ZF_DATA_MODE": "synthetic"}, {"ZF_DATA_MODE": "actual"}):
                        hold = data_protection.document_model_hold(
                            raw_doc,
                            mode_env,
                            case_id="ZF-1",
                            doc_id=doc["id"],
                            derivative="synthetic_safe",
                        )
                        self.assertIsNotNone(hold)
                        self.assertIn("has not passed the content scan", hold)

                detail = st.detail("ZF-1", SAM)
                epc_item = next(r for r in detail["checklist"] if r["kind"] == "EPC")
                self.assertFalse(epc_item["present"])
                self.assertEqual(detail["documents"][0]["summary"], projection.NOTE_HELD)
                self.assertEqual(
                    chat_case_answers.case_facts(detail, reason_visible=True)["documents"],
                    "none recorded",
                )
                epc_fresh = next(
                    f
                    for f in st.work_context(st._case("ZF-1"), PAM)["evidence_freshness"]
                    if f["kind"] == "EPC"
                )
                self.assertEqual(epc_fresh["status"], "Unknown")
                self.assertEqual(home_case.links(st.data, st._case("ZF-1"))["document_ids"], [])
                self.assertEqual(home_case.view(st, SAM, "ZF-1")["home"]["documents"], [])
                self.assertEqual(forms.list_candidates(st, PAM, "ZF-1"), [])
                with self.assertRaises(ValueError):
                    st._capacity_source(
                        {
                            "source_case_id": "ZF-1",
                            "document_id": doc["id"],
                            "source_version": str(raw_doc["version"]),
                        }
                    )
                self.assertNotIn(
                    f"Document: {doc['name']}", ai_tasks.source_labels(st._case("ZF-1"), True)
                )
                self.assertEqual(
                    assistants.capture("assessment-preparation", st._case("ZF-1"))["sources"][
                        "documents"
                    ],
                    [],
                )

        with st.lock:
            if hasattr(st, "_touch"):
                st._touch("ZF-1")
            raw_doc = st._case("ZF-1")["documents"][0]
            raw_doc["scan"] = {
                "status": "failed",
                "scanner": "s",
                "at": "2026-11-15T00:00:00",
                "detail": "f",
            }
            raw_doc["scan_status"] = "failed"
            st.save()

        blob.result = "No threats found"
        self.assertEqual(st.rescan_document(SAM, "ZF-1", doc["id"])["status"], "clean")
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1.4 ok")
        clean_detail = st.detail("ZF-1", SAM)
        self.assertTrue(next(r for r in clean_detail["checklist"] if r["kind"] == "EPC")["present"])
        self.assertEqual(clean_detail["documents"][0]["summary"], "SYN summary")
        self.assertEqual(
            chat_case_answers.case_facts(clean_detail, reason_visible=True)["documents"], "EPC"
        )
        self.assertEqual(home_case.links(st.data, st._case("ZF-1"))["document_ids"], [doc["id"]])
        self.assertEqual(len(forms.list_candidates(st, PAM, "ZF-1")), 1)
        self.assertEqual(
            [
                d["id"]
                for d in assistants.capture("assessment-preparation", st._case("ZF-1"))["sources"][
                    "documents"
                ]
            ],
            [doc["id"]],
        )
        if use_sql:
            reopened = SqlStore(seed_path, db_path)
            reopened.docstore = st.docstore
            reopened.scanner = st.scanner
            reopened_doc = reopened._case("ZF-1")["documents"][0]
            self.assertEqual(reopened_doc["scan"]["status"], "clean")
            self.assertEqual(reopened_doc["scan_status"], "clean")
            self.assertEqual(reopened.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1.4 ok")


class RetentionTests(Base):
    def stock(self):
        """Cases built from the 120 synthetic-stock control fixtures, with their uploads."""
        cases = []
        for fx in FIXTURES["cases"]:
            c = test_mvp.case(fx["case_id"])
            c["closed"], c["retention_trigger"] = fx["closed"], fx["retention_trigger"]
            cases.append(c)
        st = self.make(cases)
        for fx in FIXTURES["cases"]:
            for u in fx["uploads"]:
                if u["scan_class"] == "clean":
                    st.add_document(
                        SAM,
                        fx["case_id"],
                        u["name"],
                        u["kind"],
                        payload(u["kind"], "clean"),
                        metadata=change_metadata(st, fx["case_id"]),
                    )
            if fx["legal_hold"]:
                st.place_legal_hold(PAM, fx["case_id"], f"HOLD-{fx['case_id']}")
        return st

    def run_stock(self):
        st = self.stock()
        before = sum(len(c["documents"]) for c in st.cases.values())
        out = st.retention_due(PAM, AS_OF)
        self.assertIn("not an approved retention schedule", out["label"])
        recs = out["records"]
        self.assertGreater(len(recs), 20)
        held = {fx["case_id"] for fx in FIXTURES["cases"] if fx["legal_hold"]}
        for r in recs:
            self.assertEqual(r["status"].startswith("blocked"), r["case_id"] in held)
        self.assertEqual(sum(len(c["documents"]) for c in st.cases.values()), before)
        free = next(r for r in recs if r["case_id"] not in held)
        blocked = next(r for r in recs if r["case_id"] in held)
        with self.assertRaises(PermissionError):
            st.approve_retention_deletion(SAM, free["case_id"], free["doc_id"], AS_OF)
        with self.assertRaises(PermissionError):
            st.approve_retention_deletion(PAM, blocked["case_id"], blocked["doc_id"], AS_OF)
        self.assertEqual(sum(len(c["documents"]) for c in st.cases.values()), before)
        name = next(
            d["name"] for d in st._case(free["case_id"])["documents"] if d["id"] == free["doc_id"]
        )
        st.approve_retention_deletion(PAM, free["case_id"], free["doc_id"], AS_OF)
        self.assertEqual(sum(len(c["documents"]) for c in st.cases.values()), before - 1)
        with self.assertRaises(KeyError):
            st.docstore.get(free["case_id"], free["doc_id"])
        entries = list(st.audit_entries())
        self.assertIn("retention_deleted", self.actions(st))
        self.assertIn("retention_delete_blocked_legal_hold", self.actions(st))
        self.assertNotIn(
            name, json.dumps([e for e in entries if e["action"].startswith("retention_")])
        )
        self.assertTrue(st.verify_audit())
        st.release_legal_hold(PAM, blocked["case_id"])
        st.approve_retention_deletion(PAM, blocked["case_id"], blocked["doc_id"], AS_OF)

    def test_json_store(self):
        self.run_stock()

    def test_retention_refusals_explain_reason_owner_next_action_and_change_nothing(self):
        triggers = {
            "ZF-N1": None,
            "ZF-N2": AS_OF.isoformat(),
            "ZF-N3": (AS_OF - timedelta(days=365 * 6)).isoformat(),
        }
        cases = []
        for cid, trigger in triggers.items():
            c = test_mvp.case(cid)
            c["closed"], c["retention_trigger"] = False, trigger
            cases.append(c)
        st = self.make(cases)
        docs = {
            cid: st.add_document(
                SAM, cid, "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, cid)
            )
            for cid in triggers
        }

        def refuse(cid, exc):
            did = docs[cid]["id"]
            before = (
                len(st.docstore.get(cid, did)),
                len(st.detail(cid)["documents"]),
                len(self.actions(st)),
            )
            with self.assertRaises(exc) as ctx:
                st.approve_retention_deletion(PAM, cid, did, AS_OF)
            self.assertEqual(
                before,
                (
                    len(st.docstore.get(cid, did)),
                    len(st.detail(cid)["documents"]),
                    len(self.actions(st)) - (exc is PermissionError),
                ),
            )
            self.assertTrue(st.verify_audit())
            return str(ctx.exception)

        for text in (refuse("ZF-N1", ValueError), refuse("ZF-N2", ValueError)):
            for phrase in (
                "not due for deletion",
                "nothing was deleted",
                "retention period",
                "recorded retention start date",
                "not an approved schedule",
                "Keep the document",
                "check the case closing date",
            ):
                self.assertIn(phrase, text)
            self.assertNotIn("retention trigger", text)
        self.assertNotIn("retention_delete_blocked_legal_hold", self.actions(st))

        st.place_legal_hold(PAM, "ZF-N3", "HOLD-ZF-N3")
        held = refuse("ZF-N3", PermissionError)
        for phrase in (
            "legal hold is in place",
            "kept for a legal reason",
            "nothing was deleted",
            "Keep the documents",
            "programme manager",
            "Legal delegate's decision",
            "once the hold has ended",
        ):
            self.assertIn(phrase, held)
        self.assertEqual(self.actions(st).count("retention_delete_blocked_legal_hold"), 1)
        self.assertNotIn("retention_deleted", self.actions(st))

        st.release_legal_hold(PAM, "ZF-N3")
        st.approve_retention_deletion(PAM, "ZF-N3", docs["ZF-N3"]["id"], AS_OF)
        self.assertIn("retention_deleted", self.actions(st))
        with self.assertRaises(KeyError):
            st.docstore.get("ZF-N3", docs["ZF-N3"]["id"])

    def test_not_due_documents_are_refused_and_not_listed(self):
        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        self.assertEqual(st.retention_due(PAM, AS_OF)["records"], [])
        with self.assertRaises(ValueError):
            st.approve_retention_deletion(PAM, "ZF-1", doc["id"], AS_OF)
        with self.assertRaises(PermissionError):
            st.retention_due(SAM)
        with self.assertRaises(ValueError):
            st.place_legal_hold(PAM, "ZF-1", "Resident Pat Test, 1 Test Road")

    def test_retention_listing_survives_a_busy_write_lock_unrecorded(self):
        from zava_forward.core.mssqlstore import LOCK_FAILED

        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        st.cases["ZF-1"]["retention_trigger"] = "not-a-date"
        busy = type("ProgrammingError", (Exception,), {"__module__": "mssql_python.exceptions"})(
            f"[SQL Server]{LOCK_FAILED}"
        )
        real = st.audit

        def audit_fails(*_a, **_k):
            raise busy

        st.audit = audit_fails
        try:
            out = st.retention_due(PAM, AS_OF)
            self.assertEqual([r["doc_id"] for r in out["records"]], [doc["id"]])
            self.assertIs(out["recorded"], False)
            st.audit = lambda *a, **k: (_ for _ in ()).throw(ValueError("other"))
            with self.assertRaises(ValueError):
                st.retention_due(PAM, AS_OF)
        finally:
            st.audit = real
        self.assertNotIn("recorded", st.retention_due(PAM, AS_OF))

    def test_unreadable_trigger_date_is_listed_for_review_not_a_failure(self):
        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        st.cases["ZF-1"]["retention_trigger"] = "not-a-date"
        before = len(st.cases["ZF-1"]["documents"])
        rows = st.retention_due(PAM, AS_OF)["records"]
        self.assertEqual(
            [(r["case_id"], r["doc_id"], r["status"], r["due"]) for r in rows],
            [("ZF-1", doc["id"], "needs review: trigger date unreadable", None)],
        )
        self.assertEqual(len(st.cases["ZF-1"]["documents"]), before)

    def test_approving_unreadable_trigger_date_is_refused_with_a_plain_message(self):
        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        st.cases["ZF-1"]["retention_trigger"] = "not-a-date"
        with self.assertRaisesRegex(ValueError, "cannot be read, so nothing was deleted"):
            st.approve_retention_deletion(PAM, "ZF-1", doc["id"], AS_OF)
        self.assertEqual(len(st.cases["ZF-1"]["documents"]), 1)

    def test_legal_hold_wins_over_an_unreadable_trigger_date(self):
        st = self.make()
        doc = st.add_document(
            SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1")
        )
        st.cases["ZF-1"]["retention_trigger"] = "not-a-date"
        st.place_legal_hold(PAM, "ZF-1", "HOLD-1")
        rows = st.retention_due(PAM, AS_OF)["records"]
        self.assertEqual(
            [(r["doc_id"], r["status"]) for r in rows], [(doc["id"], "blocked: legal hold")]
        )
        with self.assertRaises(PermissionError):
            st.approve_retention_deletion(PAM, "ZF-1", doc["id"], AS_OF)
        self.assertEqual(len(st.cases["ZF-1"]["documents"]), 1)
        self.assertIn("retention_delete_blocked_legal_hold", self.actions(st))

    def test_legal_hold_is_per_case(self):
        trigger = (AS_OF - timedelta(days=365 * 8)).isoformat()
        cases = []
        for cid in ("ZF-H1", "ZF-H2"):
            c = test_mvp.case(cid)
            c["closed"], c["retention_trigger"] = False, trigger
            cases.append(c)
        st = self.make(cases)
        docs = {
            cid: st.add_document(
                SAM, cid, "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, cid)
            )
            for cid in ("ZF-H1", "ZF-H2")
        }
        st.place_legal_hold(PAM, "ZF-H1", "HOLD-H1")
        status = {r["case_id"]: r["status"] for r in st.retention_due(PAM, AS_OF)["records"]}
        self.assertEqual(
            status, {"ZF-H1": "blocked: legal hold", "ZF-H2": "awaiting owner approval"}
        )
        st.approve_retention_deletion(PAM, "ZF-H2", docs["ZF-H2"]["id"], AS_OF)
        self.assertEqual(len(st.cases["ZF-H1"]["documents"]), 1)
        self.assertEqual(len(st.cases["ZF-H2"]["documents"]), 0)

    def test_hold_changes_are_manager_only_and_a_repeat_release_is_refused(self):
        st = self.make()
        before = len(self.actions(st))
        with self.assertRaises(PermissionError):
            st.place_legal_hold(SAM, "ZF-1", "HOLD-1")
        with self.assertRaises(ValueError):
            st.release_legal_hold(PAM, "ZF-1")
        self.assertFalse((st.cases["ZF-1"].get("legal_hold") or {}).get("active"))
        self.assertEqual(len(self.actions(st)), before)
        st.place_legal_hold(PAM, "ZF-1", "HOLD-1")
        with self.assertRaises(PermissionError):
            st.release_legal_hold(SAM, "ZF-1")
        self.assertTrue(st.cases["ZF-1"]["legal_hold"]["active"])
        st.release_legal_hold(PAM, "ZF-1")
        with self.assertRaises(ValueError):
            st.release_legal_hold(PAM, "ZF-1")
        self.assertEqual(self.actions(st)[before:], ["legal_hold_placed", "legal_hold_released"])
        self.assertTrue(st.verify_audit())


class SqlRetentionTests(RetentionTests):
    sql = True


class HttpScanGate(ui_support.Base):
    """The scan gate as seen through the HTTP routes, with a Defender-style blob store."""

    def setUp(self):
        self.blob = DefenderBlob()
        self.saved = (self.store.docstore, self.store.scanner)
        self.store.docstore = AzureBlobDocumentStore(
            "https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=self.blob
        )
        self.store.scanner = DefenderForStorageScanner(self.store.docstore)
        self.addCleanup(lambda: setattr(self.store, "docstore", self.saved[0]))
        self.addCleanup(lambda: setattr(self.store, "scanner", self.saved[1]))

    def upload(self, ck, name, data):
        raw = base64.b64encode(data).decode()
        return self.call(ck, "/api/cases/ZF-3/upload", {"name": name, "kind": "EPC", "data": raw})

    def download(self, ck, doc_id):
        req = urllib.request.Request(self.base + f"/api/docs/ZF-3/{doc_id}", headers={"Cookie": ck})
        try:
            with urllib.request.urlopen(req) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code

    def test_pending_upload_is_unavailable_until_the_scanner_reports_clean(self):
        sam = self.login("sam@example.test")
        status, body, _ = self.upload(sam, "epc.pdf", b"%PDF-1")
        self.assertEqual(status, 200)
        doc = body["documents"][-1]
        self.assertEqual(doc["scan"]["status"], "pending")
        self.assertEqual(self.download(sam, doc["id"]), 403)
        self.assertEqual(self.download(sam, doc["id"]), 403)

        self.blob.result = "No threats found"
        status, scan, _ = self.call(sam, "/api/cases/ZF-3/rescan-doc", {"id": doc["id"]})
        self.assertEqual((status, scan["status"]), (200, "clean"))
        self.assertEqual(self.download(sam, doc["id"]), 200)

    def test_malicious_tag_removes_the_upload_and_the_blob(self):
        sam = self.login("sam@example.test")
        before = len(self.store._case("ZF-3")["documents"])
        doc = self.upload(sam, "epc.pdf", b"%PDF-1")[1]["documents"][-1]
        self.blob.result = "Malicious"
        self.assertEqual(self.call(sam, "/api/cases/ZF-3/rescan-doc", {"id": doc["id"]})[0], 400)
        self.assertEqual(self.download(sam, doc["id"]), 404)
        self.assertNotIn(doc["id"], "".join(self.blob.blobs))
        after = len(self.store._case("ZF-3")["documents"])
        self.assertEqual(after, before)


class HttpLocalScanGate(ui_support.Base):
    def test_eicar_upload_is_refused_and_leaves_no_document(self):
        sam = self.login("sam@example.test")
        raw = base64.b64encode(b"%PDF-1.4 " + EICAR_SIGNATURE).decode()
        status, body, _ = self.call(
            sam, "/api/cases/ZF-3/upload", {"name": "epc.pdf", "kind": "EPC", "data": raw}
        )
        self.assertEqual(status, 400)
        self.assertIn("failed the malware scan", body["error"])
        self.assertNotIn("epc.pdf", [d["name"] for d in self.store._case("ZF-3")["documents"]])


if __name__ == "__main__":
    unittest.main()
