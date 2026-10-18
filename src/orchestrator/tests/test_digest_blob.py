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

    def test_unrelated_json_is_not_a_remote_anchor(self):
        self.container.blobs["unrelated.json"] = b"not a digest or even JSON"
        rep = digest_blob.verify(self.store, self.blob)
        self.assertFalse(rep["intact"])
        self.assertEqual((rep["digests"], rep["year_digests"], rep["entries"]), (0, 0, 3))
        self.assertEqual(rep["problems"], [
            dict(check="digests", problem="the container holds no recognized head or year digest anchors to verify against")
        ])
        self.assertEqual(self.run_job(), 1)
        self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
        self.assertFalse(any(digest_blob.OK_MARKER in line for line in self.out))
        self.assertFalse(any(url.endswith("/unrelated.json") for _, url, _ in self.container.calls))

    def test_missing_remote_anchor_cli_alerts_without_success_marker(self):
        self.container.blobs["unrelated.json"] = b"{}"
        self.assertEqual(self.run_job(), 1)
        self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
        self.assertFalse(any(digest_blob.OK_MARKER in line for line in self.out))

    def test_local_digests_do_not_substitute_for_remote_anchors(self):
        self.store.write_digest()
        for unrelated in (False, True):
            with self.subTest(unrelated=unrelated):
                self.container.blobs = {"unrelated.json": b"{}"} if unrelated else {}
                self.out.clear()
                rep = digest_blob.verify(self.store, self.blob)
                self.assertFalse(rep["intact"])
                self.assertEqual((rep["digests"], rep["year_digests"]), (0, 0))
                self.assertEqual(self.run_job(), 1)
                self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
                self.assertFalse(any(digest_blob.OK_MARKER in line for line in self.out))

    def test_valid_head_anchor_ignores_unrelated_blobs(self):
        self.assertEqual(self.run_job("--publish"), 0)
        for unrelated in (False, True):
            with self.subTest(unrelated=unrelated):
                if unrelated:
                    self.container.blobs["unrelated.json"] = b"not JSON"
                self.out.clear()
                rep = digest_blob.verify(self.store, self.blob)
                self.assertTrue(rep["intact"])
                self.assertEqual((rep["digests"], rep["year_digests"]), (1, 0))
                self.assertEqual(self.run_job(), 0)
                self.assertTrue(any(digest_blob.OK_MARKER in line for line in self.out))
                self.assertFalse(any(digest_blob.ALERT_MARKER in line for line in self.out))
                self.assertFalse(any(url.endswith("/unrelated.json") for _, url, _ in self.container.calls))

    def test_valid_sealed_year_anchor_ignores_unrelated_blobs(self):
        e1 = ledger.make_entry("a", "x", "c", "d", ledger.GENESIS, "2024-05-01T00:00:00")
        e2 = ledger.make_entry("a", "y", "c", "d", e1["hash"], "2025-05-01T00:00:00")
        self.store.audit_entries = lambda: iter([e1, e2])
        d = ledger.year_digests([e1, e2], before=2025)[0]
        self.blob.put_digest("year-2024.json", d)
        for unrelated in (False, True):
            with self.subTest(unrelated=unrelated):
                if unrelated:
                    self.container.blobs["unrelated.json"] = b"not JSON"
                self.out.clear()
                rep = digest_blob.verify(self.store, self.blob)
                self.assertTrue(rep["intact"])
                self.assertEqual((rep["digests"], rep["year_digests"]), (0, 1))
                self.assertEqual(self.run_job(), 0)
                self.assertTrue(any(digest_blob.OK_MARKER in line for line in self.out))
                self.assertFalse(any(digest_blob.ALERT_MARKER in line for line in self.out))
                self.assertFalse(any(url.endswith("/unrelated.json") for _, url, _ in self.container.calls))

    def test_empty_ledger_requires_a_remote_anchor_not_local_digests(self):
        Path(self.store.audit_path).write_text("")
        self.store.last_hash = ledger.GENESIS
        self.assertEqual(list(self.store.audit_entries()), [])
        self.store.write_digest()
        for unrelated in (False, True):
            with self.subTest(unrelated=unrelated):
                self.container.blobs = {"unrelated.json": b"{}"} if unrelated else {}
                self.out.clear()
                rep = digest_blob.verify(self.store, self.blob)
                self.assertFalse(rep["intact"])
                self.assertEqual((rep["digests"], rep["year_digests"], rep["entries"]), (0, 0, 0))
                self.assertEqual(rep["problems"][0]["check"], "digests")
                self.assertEqual(self.run_job(), 1)
                self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
                self.assertFalse(any(digest_blob.OK_MARKER in line for line in self.out))

    def test_empty_ledger_remote_anchor_controls(self):
        entries = list(self.store.audit_entries())
        head = ledger.make_digest(len(entries), entries[-1]["hash"])
        year = ledger.year_digests(entries)[0]
        Path(self.store.audit_path).write_text("")
        self.store.last_hash = ledger.GENESIS
        self.assertEqual(list(self.store.audit_entries()), [])
        for name, digest, intact in (
            ("digest-0000000000.json", ledger.make_digest(0, ledger.GENESIS), True),
            ("digest-0000000003.json", head, False),
            (f"year-{year['year']}.json", year, False),
        ):
            with self.subTest(name=name):
                self.container.blobs = {"unrelated.json": b"not JSON"}
                self.blob.put_digest(name, digest)
                self.out.clear()
                self.assertEqual(digest_blob.verify(self.store, self.blob)["intact"], intact)
                self.assertEqual(self.run_job(), 0 if intact else 1)
                self.assertEqual(any(digest_blob.OK_MARKER in line for line in self.out), intact)
                self.assertEqual(any(digest_blob.ALERT_MARKER in line for line in self.out), not intact)

    def test_unrelated_blobs_cannot_hide_anchor_mismatches(self):
        entries = list(self.store.audit_entries())
        head = ledger.make_digest(len(entries), "f" * 64)
        year = {**ledger.year_digests(entries)[0], "head": "f" * 64}
        for name, digest, check in (
            ("digest-0000000003.json", head, "chain"),
            (f"year-{year['year']}.json", year, "years"),
        ):
            with self.subTest(name=name):
                self.container.blobs = {"unrelated.json": b"not JSON"}
                self.blob.put_digest(name, digest)
                self.out.clear()
                rep = digest_blob.verify(self.store, self.blob)
                self.assertFalse(rep["intact"])
                self.assertTrue(any(problem["check"] == check for problem in rep["problems"]))
                self.assertEqual(self.run_job(), 1)
                self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
                self.assertFalse(any(digest_blob.OK_MARKER in line for line in self.out))

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

    def assert_invalid_remote_anchor(self, name, body):
        self.container.blobs = {name: body}
        for with_good_anchor in (False, True):
            with self.subTest(with_good_anchor=with_good_anchor):
                if with_good_anchor:
                    entries = list(self.store.audit_entries())
                    good = ledger.make_digest(1, entries[0]["hash"])
                    self.container.blobs["digest-0000000001.json"] = json.dumps(good).encode()
                snapshot = dict(self.container.blobs)
                rep = digest_blob.verify(self.store, self.blob)
                self.assertFalse(rep["intact"])
                self.assertIn(dict(check="digests", problem="invalid remote digest anchor"), rep["problems"])
                self.out.clear()
                self.assertEqual(self.run_job(), 1)
                self.assertTrue(any(digest_blob.ALERT_MARKER in line for line in self.out))
                self.assertFalse(any(digest_blob.OK_MARKER in line for line in self.out))
                self.assertNotIn(name, "\n".join(self.out))
                self.assertNotIn("PRIVATE_SENTINEL", "\n".join(self.out))
                self.assertEqual(self.container.blobs, snapshot)
                self.assertFalse(any(method in ("PUT", "DELETE") for method, _, _ in self.container.calls))

    def test_malformed_prefixed_anchor_names_fail_closed(self):
        entries = list(self.store.audit_entries())
        head = ledger.make_digest(3, entries[-1]["hash"])
        year = ledger.make_year_digest("2024", entries)
        for name, payload in (
            ("digest-not-a-count.json", {}),
            ("digest-3.json", head),
            ("digest-00000000003.json", head),
            ("digest--000000003.json", head),
            ("digest-0000000002.json", head),
            ("digest-PRIVATE_SENTINEL.json", head),
            ("year-not-a-year.json", year),
            ("year-202.json", year),
            ("year-0000.json", {**year, "year": "0000"}),
            ("year-2025.json", year),
        ):
            with self.subTest(name=name):
                self.assert_invalid_remote_anchor(name, json.dumps(payload).encode())

    def test_malformed_anchor_payloads_fail_closed(self):
        entries = list(self.store.audit_entries())
        head = ledger.make_digest(3, entries[-1]["hash"])
        year = ledger.make_year_digest("2024", entries)
        for name, valid in (("digest-0000000003.json", head), ("year-2024.json", year)):
            bodies = [b"{}", b"null", b"[]", b'"PRIVATE_SENTINEL"', b"not JSON PRIVATE_SENTINEL", b"\xff"]
            bodies += [json.dumps({k: v for k, v in valid.items() if k != field}).encode()
                       for field in valid if field != "at"]
            for field, values in (
                ("count", (True, -1, 1.5, "3", None)),
                ("head", (None, 4, [], "PRIVATE_SENTINEL", "A" * 64)),
                ("chain", ("other", "", None)),
                ("algorithm", ("sha512", "", None)),
            ):
                bodies += [json.dumps({**valid, field: value}).encode() for value in values]
            if name.startswith("year-"):
                bodies += [json.dumps({**valid, field: value}).encode() for field, value in
                           (("year", 2024), ("year", "2025"), ("count", 0),
                            ("first_prev", None), ("first_prev", "PRIVATE_SENTINEL"))]
            else:
                bodies.append(json.dumps({**head, "count": 0, "head": "f" * 64}).encode())
            for index, body in enumerate(bodies):
                with self.subTest(name=name, case=index):
                    self.assert_invalid_remote_anchor(name, body)

    def test_anchor_qualification_preserves_publisher_and_reader_compatibility(self):
        entries = list(self.store.audit_entries())
        head = ledger.make_digest(3, entries[-1]["hash"])
        del head["at"]
        self.container.blobs = {"digest-0000000003.json": json.dumps({**head, "extra": "provenance"}).encode()}
        self.assertEqual(self.run_job(), 0)
        large = ledger.make_digest(10000000000, entries[-1]["hash"])
        self.container.blobs = {"digest-10000000000.json": json.dumps(large).encode()}
        rep = digest_blob.verify(self.store, self.blob)
        self.assertFalse(rep["intact"])
        self.assertEqual(rep["digests"], 1)
        self.assertEqual([p["check"] for p in rep["problems"]], ["chain"])

    def test_invalid_zero_head_is_not_an_anchor(self):
        self.assert_invalid_remote_anchor(
            "digest-0000000000.json", json.dumps(ledger.make_digest(0, "f" * 64)).encode())


if __name__ == "__main__":
    unittest.main()
