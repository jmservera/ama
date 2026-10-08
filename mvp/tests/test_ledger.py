import json
import os
import tempfile
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
import threading
from pathlib import Path

import test_mvp
from properwarm_mvp import ledger
from properwarm_mvp.factory import open_store
from properwarm_mvp.server import App, make_handler
from properwarm_mvp.sqlstore import SqlStore
from properwarm_mvp.store import Store


class LedgerCases:
    def make(self):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.sam, self.pam = test_mvp.DATA["staff"]
        self.store = self.make()
        for i in range(3):
            self.store.log_call(self.sam, "PW-1", f"Call {i}", "")

    def tearDown(self):
        self.tmp.cleanup()

    def test_chain_verifies_and_head_counts(self):
        rep = self.store.verify_ledger()
        self.assertTrue(rep["intact"])
        self.assertEqual((rep["entries"], rep["head"]), self.store.ledger_head())

    def test_digest_matches_then_catches_truncation_and_rewrite(self):
        self.store.write_digest()
        self.store.log_call(self.sam, "PW-1", "Call 3", "")
        rep = self.store.verify_ledger()
        self.assertTrue(rep["intact"])
        self.assertEqual(rep["digests_checked"], 1)
        self.tamper_truncate()
        rep = self.store.verify_ledger()
        self.assertFalse(rep["intact"])
        self.assertTrue(rep["digest_mismatches"])

    def test_digest_files_are_not_overwritten(self):
        a = self.store.write_digest()
        b = self.store.write_digest()
        self.assertEqual(a, b)
        self.assertEqual(len(os.listdir(self.store.digest_dir)), 1)


class JsonLedgerTests(LedgerCases, unittest.TestCase):
    def make(self):
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(test_mvp.DATA))
        return Store(str(p))

    def tamper_truncate(self):
        lines = Path(self.store.audit_path).read_text().splitlines()
        # drop the newest entry and rewrite the tail so the shortened chain is itself valid
        Path(self.store.audit_path).write_text("\n".join(lines[:-2]) + "\n")

    def test_edited_line_breaks_chain(self):
        lines = Path(self.store.audit_path).read_text().splitlines()
        e = json.loads(lines[1])
        e["detail"] = "changed"
        lines[1] = json.dumps(e)
        Path(self.store.audit_path).write_text("\n".join(lines) + "\n")
        rep = self.store.verify_ledger()
        self.assertFalse(rep["intact"])
        self.assertEqual(rep["problem"]["entry"], 2)


class SqlLedgerTests(LedgerCases, unittest.TestCase):
    def make(self):
        p = Path(self.tmp.name) / "properwarm.json"
        p.write_text(json.dumps(test_mvp.DATA))
        return SqlStore(str(p), os.path.join(self.tmp.name, "pw.sqlite"))

    def tamper_truncate(self):
        import sqlite3
        raw = sqlite3.connect(self.store.db_path)
        raw.execute("DROP TRIGGER audit_no_delete")
        raw.execute("DELETE FROM audit WHERE seq > 2")
        raw.commit()


class LedgerToolTests(unittest.TestCase):
    def test_entries_hash_independent_of_store(self):
        e1 = ledger.make_entry("a", "x", "c", "d", ledger.GENESIS, "2026-01-01T00:00:00")
        e2 = ledger.make_entry("a", "y", "c", "d", e1["hash"], "2026-01-01T00:00:01")
        self.assertTrue(ledger.verify_entries([e1, e2])["intact"])
        self.assertFalse(ledger.verify_entries([e2, e1])["intact"])

    def test_cli_and_endpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "properwarm.json"
            p.write_text(json.dumps(test_mvp.DATA))
            env = dict(PW_DATA=str(p), PW_STATE=tmp, PW_STORE="sqlite")
            store = open_store(env)
            self.assertIsInstance(store, SqlStore)
            store.log_call(test_mvp.DATA["staff"][0], "PW-1", "Call", "")
            old = dict(os.environ)
            os.environ.update(env)
            try:
                self.assertEqual(ledger.main([]), 0)
                self.assertEqual(ledger.main(["--digest"]), 0)
            finally:
                os.environ.clear()
                os.environ.update(old)
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(store, "pw-test")))
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            base = f"http://127.0.0.1:{httpd.server_address[1]}"
            def call(path, email, body=None):
                op = urllib.request.build_opener()
                req = urllib.request.Request(base + "/api/login", json.dumps(dict(email=email, password="pw-test")).encode())
                ck = op.open(req).headers["Set-Cookie"].split(";")[0]
                req = urllib.request.Request(base + path, json.dumps(body).encode() if body is not None else None, headers={"Cookie": ck})
                try:
                    with op.open(req) as r:
                        return r.status, json.loads(r.read())
                except urllib.error.HTTPError as e:
                    return e.code, json.loads(e.read())
            try:
                code, rep = call("/api/audit-check", "sam@example.test")
                self.assertTrue(code == 200 and rep["intact"] and rep["entries"] == 1)
                self.assertEqual(call("/api/ledger/digest", "sam@example.test", {})[0], 403)
                code, out = call("/api/ledger/digest", "pam@example.test", {})
                self.assertEqual(code, 200)
                self.assertTrue(out["report"]["intact"])
            finally:
                httpd.shutdown()
                httpd.server_close()
