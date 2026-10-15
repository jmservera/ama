import json
import tempfile
import unittest
import urllib.parse
from pathlib import Path

import dataset
from zava_forward.core import ledger
from zava_forward.orchestrator import digest_blob
from zava_forward.core.store import Store

URL = "https://acct.blob.core.windows.net"


class FakeImmutableContainer:
    """In-memory Blob REST stand-in for a locked container: a name can be written once, never replaced or deleted."""

    def __init__(self):
        self.blobs, self.calls = {}, []

    def __call__(self, method, url, headers, body, timeout=20):
        self.calls.append((method, url, dict(headers)))
        if "oauth2/token" in url or "msi/token" in url:
            return 200, {}, json.dumps(dict(access_token="tok", expires_on="9999999999")).encode()
        u = urllib.parse.urlparse(url)
        name = u.path.split("/", 2)[2] if u.path.count("/") >= 2 else ""
        if method == "PUT":
            if name in self.blobs:
                return 409, {}, b""
            self.blobs[name] = body
            return 201, {}, b""
        if method == "DELETE":
            return 409, {}, b""
        if method == "GET" and "comp=list" in u.query:
            xml = "<EnumerationResults><Blobs>" + "".join(f"<Blob><Name>{n}</Name></Blob>" for n in sorted(self.blobs)) + "</Blobs><NextMarker/></EnumerationResults>"
            return 200, {}, xml.encode()
        if method == "GET":
            return (200, {}, self.blobs[name]) if name in self.blobs else (404, {}, b"")
        return 405, {}, b""


class BlobDigestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(dataset.DATA))
        self.store = Store(str(p))
        self.sam = dataset.DATA["staff"][0]
        for i in range(3):
            self.store.log_call(self.sam, "ZF-1", f"Call {i}", "")
        self.container = FakeImmutableContainer()
        self.blob = digest_blob.BlobDigestStore(URL, "ledger-digests", transport=self.container, env={})
        self.out = []

    def tearDown(self):
        self.tmp.cleanup()

    def run_job(self, *argv):
        return digest_blob.main(list(argv), store=self.store, blob=self.blob, out=self.out.append)

    def test_publish_uploads_create_only_and_is_idempotent(self):
        self.assertEqual(self.run_job("--publish"), 0)
        self.assertEqual(list(self.container.blobs), ["digest-0000000003.json"])
        put = next(c for c in self.container.calls if c[0] == "PUT")
        self.assertEqual(put[2]["If-None-Match"], "*")
        self.assertEqual(digest_blob.publish(self.store, self.blob), [])

    def test_clean_ledger_verifies_against_container(self):
        self.run_job("--publish")
        self.store.log_call(self.sam, "ZF-1", "Call 3", "")
        self.assertEqual(self.run_job(), 0)
        self.assertTrue(digest_blob.verify(self.store, self.blob)["intact"])

    def test_success_prints_heartbeat_marker(self):
        self.assertEqual(self.run_job("--publish"), 0)
        self.assertTrue(any(digest_blob.OK_MARKER in line for line in self.out))

    def test_truncation_after_publish_alerts(self):
        self.run_job("--publish")
        lines = Path(self.store.audit_path).read_text().splitlines()
        Path(self.store.audit_path).write_text("\n".join(lines[:-1]) + "\n")
        self.out.clear()
        self.assertEqual(self.run_job(), 1)
        self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))

    def test_local_digest_deletion_cannot_hide_a_rewrite(self):
        self.run_job("--publish")
        lines = [json.loads(x) for x in Path(self.store.audit_path).read_text().splitlines()]
        lines[1]["detail"] = "rewritten"
        lines[1]["hash"] = ledger.entry_hash(lines[1])
        Path(self.store.audit_path).write_text("\n".join(json.dumps(x) for x in lines) + "\n")
        for f in Path(self.store.digest_dir).glob("*.json"):
            f.unlink()
        self.assertEqual(self.run_job(), 1)

    def test_broken_chain_is_not_anchored(self):
        lines = Path(self.store.audit_path).read_text().splitlines()
        e = json.loads(lines[1])
        e["detail"] = "changed"
        lines[1] = json.dumps(e)
        Path(self.store.audit_path).write_text("\n".join(lines) + "\n")
        self.assertEqual(self.run_job("--publish"), 1)
        self.assertEqual(self.container.blobs, {})

    def test_empty_container_and_unreachable_container_alert(self):
        self.assertEqual(self.run_job(), 1)
        self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
        self.out.clear()
        self.blob.transport = lambda *a, **k: (500, {}, b"")
        self.assertEqual(self.run_job(), 1)
        self.assertTrue(any("unavailable" in line for line in self.out))

    def test_sealed_year_digest_mismatch(self):
        e1 = ledger.make_entry("a", "x", "c", "d", ledger.GENESIS, "2024-05-01T00:00:00")
        e2 = ledger.make_entry("a", "y", "c", "d", e1["hash"], "2025-05-01T00:00:00")
        for d in ledger.year_digests([e1, e2]):
            self.blob.put_digest(f"year-{d['year']}.json", d)
        self.store.audit_entries = lambda: iter([e1, e2])
        self.assertTrue(digest_blob.verify(self.store, self.blob)["intact"])
        forged = ledger.make_entry("a", "z", "c", "d", ledger.GENESIS, "2024-05-01T00:00:00")
        self.store.audit_entries = lambda: iter([forged, e2])
        self.assertFalse(digest_blob.verify(self.store, self.blob)["intact"])

    def test_not_configured(self):
        self.assertIsNone(digest_blob.open_digest_store({}))
        self.assertEqual(digest_blob.main([], store=self.store, env={}, out=self.out.append), 2)


if __name__ == "__main__":
    unittest.main()
