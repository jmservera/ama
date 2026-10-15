import copy
import json
import os
import tempfile
import unittest
import urllib.parse
from datetime import date
from pathlib import Path

import test_mvp
from zavaforward_mvp.doc_controls import (DEFENDER_TAG, DefenderForStorageScanner, DocumentUnavailable, LocalSignatureScanner,
                                          TEST_MARKER, open_scanner)
from zavaforward_mvp.documents import AzureBlobDocumentStore
from zavaforward_mvp.sqlstore import SqlStore
from zavaforward_mvp.store import Store
from test_documents import FakeBlob

SAM, PAM = test_mvp.DATA["staff"]
FIXTURES = json.loads((Path(__file__).resolve().parent.parent / "evals" / "document_control_fixtures.json").read_text())
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
            return 200, {}, f"<Tags><TagSet><Tag><Key>{DEFENDER_TAG}</Key><Value>{self.result}</Value></Tag></TagSet></Tags>".encode()
        return super().__call__(method, url, headers, body, timeout)


class Base(unittest.TestCase):
    sql = False

    def make(self, cases=None):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(test_mvp.DATA)
        data["cases"] += cases or []
        p = Path(tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(data))
        return SqlStore(str(p), os.path.join(tmp.name, "pw.sqlite")) if self.sql else Store(str(p))

    def actions(self, st):
        return [e["action"] for e in st.audit_entries()]


class ScanTests(Base):
    def test_clean_upload_is_available_and_scan_is_recorded(self):
        st = self.make()
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1.4 ok")
        self.assertEqual(doc["scan"]["status"], "clean")
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1.4 ok")

    def test_infected_and_mismatched_uploads_are_deleted_and_never_recorded(self):
        st = self.make()
        for name, data in (("a.pdf", b"%PDF-" + TEST_MARKER), ("b.pdf", b"not a pdf"), ("c.png", b"%PDF-1"), ("d.txt", b"a\x00b")):
            with self.assertRaises(ValueError):
                st.add_document(SAM, "ZF-1", name, "EPC", data)
        self.assertEqual(st.detail("ZF-1")["documents"], [])
        self.assertEqual(st.docstore.list_ids("ZF-1"), [])
        self.assertEqual(self.actions(st).count("upload_document_rejected"), 4)

    def test_unscanned_document_is_blocked_while_scan_pending(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
        del st._case("ZF-1")["documents"][0]["scan"]
        with self.assertRaises(DocumentUnavailable):
            st.get_document("ZF-1", doc["id"], SAM)
        with self.assertRaises(DocumentUnavailable):
            st.read_document(SAM, "ZF-1", doc["id"])

    def test_pending_defender_scan_blocks_until_clean(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        st.scanner = open_scanner(st.docstore, {"ZF_SCANNER": "defender"})
        self.assertIsInstance(st.scanner, DefenderForStorageScanner)
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
        self.assertEqual(doc["scan"]["status"], "pending")
        with self.assertRaises(DocumentUnavailable):
            st.get_document("ZF-1", doc["id"], SAM)
        blob.result = "No threats found"
        self.assertEqual(st.rescan_document(SAM, "ZF-1", doc["id"])["status"], "clean")
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1")

    def test_pending_rescans_on_read_and_by_job(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
        self.assertEqual(st.rescan_pending()["pending"], 1)
        blob.result = "No threats found"
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1")
        blob.result = None
        st.add_document(SAM, "ZF-1", "b.pdf", "EPC", b"%PDF-1")
        blob.result = "Malicious"
        self.assertEqual(st.rescan_pending()["removed"], 1)

    def test_document_without_scan_field_is_scanned_on_first_use(self):
        st = self.make()
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
        for d in st._case("ZF-1")["documents"]:
            d.pop("scan", None)
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM)[2], b"%PDF-1")
        self.assertEqual(st.detail("ZF-1")["documents"][-1]["scan"]["status"], "clean")

    def test_blob_kept_when_save_fails(self):
        blob = DefenderBlob()
        st = self.make()
        st.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
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
        st.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        st.scanner = DefenderForStorageScanner(st.docstore)
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
        blob.result = "Malicious"
        with self.assertRaises(ValueError):
            st.rescan_document(SAM, "ZF-1", doc["id"])
        self.assertEqual(st.detail("ZF-1")["documents"], [])
        self.assertEqual(blob.blobs, {})

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
                    st.add_document(SAM, "ZF-1", u["name"], u["kind"], data)
                else:
                    with self.assertRaises(ValueError):
                        st.add_document(SAM, "ZF-1", u["name"], u["kind"], data)
                seen.add(u["scan_class"])
        self.assertEqual(seen, {"clean", "test-marker", "type-mismatch"})
        self.assertTrue(all(d["scan"]["status"] == "clean" for d in st.detail("ZF-1")["documents"]))


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
                    st.add_document(SAM, fx["case_id"], u["name"], u["kind"], payload(u["kind"], "clean"))
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
        name = next(d["name"] for d in st._case(free["case_id"])["documents"] if d["id"] == free["doc_id"])
        st.approve_retention_deletion(PAM, free["case_id"], free["doc_id"], AS_OF)
        self.assertEqual(sum(len(c["documents"]) for c in st.cases.values()), before - 1)
        with self.assertRaises(KeyError):
            st.docstore.get(free["case_id"], free["doc_id"])
        entries = list(st.audit_entries())
        self.assertIn("retention_deleted", self.actions(st))
        self.assertIn("retention_delete_blocked_legal_hold", self.actions(st))
        self.assertNotIn(name, json.dumps([e for e in entries if e["action"].startswith("retention_")]))
        self.assertTrue(st.verify_audit())
        st.release_legal_hold(PAM, blocked["case_id"])
        st.approve_retention_deletion(PAM, blocked["case_id"], blocked["doc_id"], AS_OF)

    def test_json_store(self):
        self.run_stock()

    def test_not_due_documents_are_refused_and_not_listed(self):
        st = self.make()
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1")
        self.assertEqual(st.retention_due(PAM, AS_OF)["records"], [])
        with self.assertRaises(ValueError):
            st.approve_retention_deletion(PAM, "ZF-1", doc["id"], AS_OF)
        with self.assertRaises(PermissionError):
            st.retention_due(SAM)
        with self.assertRaises(ValueError):
            st.place_legal_hold(PAM, "ZF-1", "Resident Pat Test, 1 Test Road")


class SqlRetentionTests(RetentionTests):
    sql = True


if __name__ == "__main__":
    unittest.main()
