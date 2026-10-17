
from dataset import change_metadata
import json
import os
import tempfile
import unittest
import urllib.parse
from pathlib import Path

import dataset
from zava_forward.core.documents import (AzureBlobDocumentStore, DocumentStoreError, LocalDocumentStore, open_document_store)
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

SAM, PAM = dataset.DATA["staff"]
CONTRACTOR = dict(code="C-1", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Test Ltd")


class FakeBlob:
    """In-memory stand-in for Blob REST plus the identity endpoint. Records every call."""

    def __init__(self, token_status=200, put_status=201):
        self.blobs, self.calls, self.token_status, self.put_status = {}, [], token_status, put_status

    def __call__(self, method, url, headers, body, timeout=20):
        self.calls.append((method, url, dict(headers), body))
        if "oauth2/token" in url or "msi/token" in url:
            if self.token_status != 200:
                return self.token_status, {}, b""
            return 200, {}, json.dumps(dict(access_token="tok-1", expires_on="9999999999")).encode()
        path = urllib.parse.urlparse(url).path
        if method == "PUT":
            if self.put_status not in (200, 201):
                return self.put_status, {}, b""
            self.blobs[path] = body
            return 201, {}, b""
        if method == "GET":
            return (200, {}, self.blobs[path]) if path in self.blobs else (404, {}, b"")
        if method == "DELETE":
            return (202, {}, b"") if self.blobs.pop(path, None) is not None else (404, {}, b"")
        return 405, {}, b""


class BlobStoreTests(unittest.TestCase):
    URL = "https://acct.blob.core.windows.net"

    def test_managed_identity_put_get_delete_and_token_cached(self):
        t = FakeBlob()
        s = AzureBlobDocumentStore(self.URL, "case-docs", transport=t, env={"IDENTITY_ENDPOINT": "http://127.0.0.1:42356/msi/token", "IDENTITY_HEADER": "h"})
        s.put("ZF-1", "abc", b"data", "application/pdf")
        self.assertEqual(s.get("ZF-1", "abc"), b"data")
        s.delete("ZF-1", "abc")
        with self.assertRaises(KeyError):
            s.get("ZF-1", "abc")
        token_calls = [c for c in t.calls if "msi/token" in c[1]]
        self.assertEqual(len(token_calls), 1)
        self.assertEqual(token_calls[0][2]["X-IDENTITY-HEADER"], "h")
        self.assertIn("resource=https%3A%2F%2Fstorage.azure.com%2F", token_calls[0][1])
        put = next(c for c in t.calls if c[0] == "PUT")
        self.assertEqual(put[1], f"{self.URL}/case-docs/ZF-1/abc")
        self.assertEqual(put[2]["Authorization"], "Bearer tok-1")
        self.assertEqual(put[2]["x-ms-blob-type"], "BlockBlob")
        self.assertEqual(put[2]["If-None-Match"], "*")

    def test_imds_fallback_with_client_id(self):
        t = FakeBlob()
        s = AzureBlobDocumentStore(self.URL, "case-docs", client_id="cid", transport=t, env={})
        s.put("ZF-1", "abc", b"x", "text/plain")
        tok = t.calls[0]
        self.assertTrue(tok[1].startswith("http://169.254.169.254/metadata/identity/oauth2/token"))
        self.assertIn("client_id=cid", tok[1])
        self.assertEqual(tok[2]["Metadata"], "true")

    def test_sas_token_is_used_and_no_identity_call_made(self):
        t = FakeBlob()
        s = AzureBlobDocumentStore(self.URL, "case-docs", sas="?sv=1&sig=abc", transport=t)
        s.put("ZF-1", "abc", b"x", "text/plain")
        self.assertEqual(len(t.calls), 1)
        self.assertTrue(t.calls[0][1].endswith("/case-docs/ZF-1/abc?sv=1&sig=abc"))
        self.assertNotIn("Authorization", t.calls[0][2])

    def test_failures_become_document_store_errors(self):
        with self.assertRaises(DocumentStoreError):
            AzureBlobDocumentStore(self.URL, "case-docs", transport=FakeBlob(token_status=403), env={}).put("ZF-1", "a", b"x", "text/plain")
        with self.assertRaises(DocumentStoreError):
            AzureBlobDocumentStore(self.URL, "case-docs", sas="s=1", transport=FakeBlob(put_status=500)).put("ZF-1", "a", b"x", "text/plain")

    def test_config_is_validated_and_ids_cannot_escape(self):
        for url, cont in (("http://x.example", "c-1"), ("", "c-1"), (self.URL, "Bad_Name")):
            with self.assertRaises(ValueError):
                AzureBlobDocumentStore(url, cont)
        s = AzureBlobDocumentStore(self.URL, "case-docs", sas="s=1", transport=FakeBlob())
        for bad in (("..", "a"), ("ZF-1", "../x"), ("ZF-1/x", "a")):
            with self.assertRaises(KeyError):
                s.put(*bad, b"x", "text/plain")

    def test_factory_selects_implementation(self):
        self.assertIsInstance(open_document_store("/x", {}), LocalDocumentStore)
        env = dict(ZF_DOC_STORE="azure-blob", ZF_BLOB_ACCOUNT_URL=self.URL, ZF_BLOB_CONTAINER="case-docs", ZF_BLOB_SAS="s=1")
        self.assertIsInstance(open_document_store("/x", env), AzureBlobDocumentStore)
        with self.assertRaises(ValueError):
            open_document_store("/x", {"ZF_DOC_STORE": "ftp"})


class LocalStoreTests(unittest.TestCase):
    def test_round_trip_and_traversal_refused(self):
        with tempfile.TemporaryDirectory() as d:
            s = LocalDocumentStore(d)
            s.put("ZF-1", "a1", b"hi", "text/plain")
            self.assertEqual(s.get("ZF-1", "a1"), b"hi")
            with self.assertRaises(KeyError):
                s.get("ZF-1", "missing")
            with self.assertRaises(KeyError):
                s.get("..", "a1")


class StoreDocumentTests(unittest.TestCase):
    def make(self, sql):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(dataset.DATA))
        st = SqlStore(str(p), os.path.join(self.tmp.name, "pw.sqlite")) if sql else Store(str(p))
        self.blob = FakeBlob()
        st.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=self.blob)
        return st

    def actions(self, st):
        return [e["action"] for e in st.audit_entries()]

    def run_all(self, sql):
        st = self.make(sql)
        doc = st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF-1", metadata=change_metadata(st, "ZF-1"))
        self.assertEqual(st.get_document("ZF-1", doc["id"], SAM), ("epc.pdf", "application/pdf", b"%PDF-1"))
        self.assertEqual(len(self.blob.blobs), 1)
        self.assertEqual(self.actions(st), ["upload_document", "download_document"])
        self.assertTrue(st.verify_audit())
        with self.assertRaises(PermissionError):
            st.get_document("ZF-1", doc["id"], CONTRACTOR)
        with self.assertRaises(PermissionError):
            st.add_document(CONTRACTOR, "ZF-1", "a.pdf", "EPC", b"x", metadata=change_metadata(st, "ZF-1"))
        with self.assertRaises(ValueError):
            st.add_document(SAM, "ZF-1", "a.exe", "EPC", b"x", metadata=change_metadata(st, "ZF-1"))
        with self.assertRaises(ValueError):
            st.add_document(SAM, "ZF-1", "a.pdf", "EPC", b"x" * (5 * 1024 * 1024 + 1), metadata=change_metadata(st, "ZF-1"))
        with self.assertRaises(ValueError):
            st.add_document(SAM, "ZF-1", "a.pdf", "EPC", b"", metadata=change_metadata(st, "ZF-1"))
        self.assertEqual(len(st.detail("ZF-1")["documents"]), 1)

    def test_json_store_with_blob(self):
        self.run_all(False)

    def test_sql_store_with_blob(self):
        self.run_all(True)

    def test_storage_outage_writes_no_metadata_and_is_audited(self):
        st = self.make(False)
        self.blob.put_status = 500
        with self.assertRaises(DocumentStoreError):
            st.add_document(SAM, "ZF-1", "epc.pdf", "EPC", b"%PDF", metadata=change_metadata(st, "ZF-1"))
        self.assertEqual(st.detail("ZF-1")["documents"], [])
        self.assertEqual(self.actions(st), ["upload_document_failed", "upload_document_rejected"])


if __name__ == "__main__":
    unittest.main()
