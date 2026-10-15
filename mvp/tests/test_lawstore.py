"""Law store: versioning, immutability, completeness, gaps, rebuildable index, read-only viewer."""
import json
import os
import shutil
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import test_mvp
from zavaforward_mvp import lawstore
from zava_forward.core.projection import STAFF_ROLES
from zavaforward_mvp.server import App, make_handler
from zava_forward.core.sqlstore import SqlStore

REG = Path(__file__).resolve().parents[2] / "docs" / "reference" / "regulatory"


class LawBase(unittest.TestCase):
    def make(self):
        return lawstore.LawStore(str(Path(self.tmp.name) / "law.sqlite"), Path(self.tmp.name) / "blobs")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.reg = Path(self.tmp.name) / "reg"
        shutil.copytree(REG, self.reg)
        self.law = self.make()
        self.report = self.law.seed(self.reg, today="2026-10-15")

    def tearDown(self):
        self.law.close()
        self.tmp.cleanup()


class FakeContainer:
    """Stands in for an azure.storage.blob ContainerClient; only the calls AzureBlobSnapshots makes."""

    def __init__(self):
        self.items = {}

    def upload_blob(self, name, data, overwrite=False):
        from azure.core.exceptions import ResourceExistsError
        if name in self.items and not overwrite:
            raise ResourceExistsError("exists")
        self.items[name] = data

    def download_blob(self, name):
        data = self.items[name]
        return type("D", (), {"readall": lambda self: data})()


class FakeBlobs:
    def __init__(self, items):
        self.items = items

    def get(self, rel):
        return self.items[rel]


class BlobInterfaceTests(unittest.TestCase):
    def check(self, store):
        store.put("a/v1.md", b"one")
        store.put("a/v1.md", b"one")
        with self.assertRaises(FileExistsError):
            store.put("a/v1.md", b"two")
        self.assertEqual(store.get("a/v1.md"), b"one")

    def test_local_snapshots_are_write_once(self):
        with tempfile.TemporaryDirectory() as d:
            self.check(lawstore.LocalSnapshots(d))

    def test_azure_snapshots_never_overwrite(self):
        try:
            import azure.core.exceptions  # noqa: F401
        except ImportError:
            self.skipTest("azure-core not installed")
        container = FakeContainer()
        self.check(lawstore.AzureBlobSnapshots(container))
        self.assertEqual(container.items, {"a/v1.md": b"one"})

    def test_store_seeds_through_the_azure_interface(self):
        try:
            import azure.core.exceptions  # noqa: F401
        except ImportError:
            self.skipTest("azure-core not installed")
        with tempfile.TemporaryDirectory() as d:
            law = lawstore.LawStore(str(Path(d) / "l.sqlite"), blobs=lawstore.AzureBlobSnapshots(FakeContainer()))
            law.seed(REG, today="2026-10-15")
            s = law.sources()["sources"][0]
            self.assertTrue(law.verify_snapshot(s["id"], s["version"]))
            law.close()


class StoreTests(LawBase):
    def test_every_snapshot_is_loaded_with_full_records(self):
        register = json.loads(lawstore.REGISTER.read_text())
        self.assertEqual(self.report["missing_files"], [])
        self.assertEqual(len(self.report["added"]), len(register["sources"]))
        for s in self.law.sources()["sources"]:
            self.assertTrue(s["official_url"].startswith("https://"), s["id"])
            self.assertIn(s["status"], lawstore.STATUSES)
            self.assertIn(s["completeness"], lawstore.COMPLETENESS)
            self.assertEqual(len(s["content_hash"]), 64)
            self.assertTrue(s["retrieved"] and s["authority_type"] and s["owner"])
            self.assertIn("reviewed", s)
            self.assertTrue(self.law.verify_snapshot(s["id"], s["version"]))

    def test_reseed_is_idempotent_and_newer_retrieval_is_a_new_version(self):
        again = self.law.seed(self.reg)
        self.assertEqual(again["added"], [])
        f = self.reg / "social-housing-regulation" / "awaabs-law-phase-1-guidance-2025.md"
        old = self.law.source("awaabs-law-phase-1-guidance-2025")["versions"][0]
        f.write_text(f.read_text() + "\n\n## Later addition\n\nNew text.\n")
        self.assertEqual(self.law.seed(self.reg)["added"], ["awaabs-law-phase-1-guidance-2025@v2"])
        d = self.law.source("awaabs-law-phase-1-guidance-2025")
        self.assertEqual([v["version"] for v in d["versions"]], [2, 1])
        self.assertEqual(d["versions"][1]["content_hash"], old["content_hash"])
        self.assertTrue(self.law.verify_snapshot("awaabs-law-phase-1-guidance-2025", 1))
        self.assertTrue(self.law.provision("awaabs-law-phase-1-guidance-2025@v1#0001"))

    def test_existing_rows_cannot_be_changed_or_deleted(self):
        for sql in ("UPDATE reg_version SET status='in_force'", "DELETE FROM reg_version", "UPDATE reg_provision SET text='x'",
                    "DELETE FROM reg_source", "UPDATE reg_gap SET reason='x'"):
            with self.assertRaises(self.law.sql.dberror, msg=sql):
                try:
                    self.law.sql.run(sql)
                finally:
                    self.law.sql.rollback()

    def test_snapshot_files_are_never_overwritten(self):
        v = self.law.source("pas-2035-bsi-overview")["versions"][0]
        with self.assertRaises(FileExistsError):
            self.law._write_blob("pas-2035-bsi-overview", 1, v["content_hash"], b"x")

    def test_partial_sources_say_so(self):
        for sid in ("pas-2035-bsi-overview", "awaabs-law-phase-2-hazards-guidance-2026"):
            v = self.law.source(sid)["versions"][0]
            self.assertEqual(v["completeness"], "partial")
            self.assertTrue(any("in part" in c for c in v["caveats"]))
        hit = self.law.search("PAS 2035 retrofit")
        self.assertTrue(any(lawstore.PARTIAL in c for c in hit["caveats"]))

    def test_missing_sources_are_gaps_returned_as_no_source_held(self):
        topics = {g["id"] for g in self.law.gaps()}
        self.assertEqual(topics, {"gap-leasehold", "gap-complaints-handling", "gap-trustmark", "gap-pas-2035-licensed"})
        for q, gap in (("leasehold service charge", "gap-leasehold"), ("complaint handling", "gap-complaints-handling"),
                       ("TrustMark registration", "gap-trustmark"), ("licensed PAS 2035", "gap-pas-2035-licensed")):
            r = self.law.search(q)
            self.assertIn(gap, [g["id"] for g in r["no_source_held"]])
            self.assertEqual(r["no_source_held"][0]["answer"], lawstore.NO_SOURCE)
        self.assertEqual(self.law.search("zzzqqq")["answer"], lawstore.NO_SOURCE)

    def test_unreviewed_and_historical_are_labelled(self):
        h = self.law.source("uk-gdpr-adopted-text")["versions"][0]
        self.assertTrue(any("Historical" in c for c in h["caveats"]))
        self.assertTrue(any(lawstore.NOT_REVIEWED == c for c in h["caveats"]))

    def test_snapshot_tampering_is_detected(self):
        v = self.law.source("pas-2035-bsi-overview")["versions"][0]
        self.assertTrue(self.law.verify_snapshot("pas-2035-bsi-overview", 1))
        self.law.blobs = FakeBlobs({v["blob_path"]: b"changed"})
        self.assertFalse(self.law.verify_snapshot("pas-2035-bsi-overview", 1))

    def test_index_rebuilds_from_sql_alone(self):
        before = self.law.search("hazard timeframe")["results"]
        self.assertTrue(before)
        self.law.sql.run("DELETE FROM reg_index")
        self.law.sql.commit()
        self.assertEqual(self.law.search("hazard timeframe")["results"], [])
        self.assertGreater(self.law.rebuild_index(), 0)
        self.assertEqual([r["id"] for r in self.law.search("hazard timeframe")["results"]], [r["id"] for r in before])

    def test_ledger_ddl_maps_every_append_only_table(self):
        for t in lawstore.APPEND_ONLY:
            self.assertTrue(any(d.startswith(f"CREATE TABLE {t} ") for d in lawstore.MSSQL_DDL), t)

    def test_split_provisions_keeps_heading_path(self):
        out = lawstore.split_provisions("---\ntitle: x\n---\n\n## A\n\ntext a\n\n### B\n\ntext b\n")
        self.assertEqual(out, [("A", "text a"), ("A > B", "text b")])


ON = os.environ.get("ZF_TEST_MSSQL") == "1"
TABLES = ("reg_index", "reg_gap", "reg_provision", "reg_version", "reg_source")


def wipe_mssql():
    from zava_forward.core.mssqlstore import _Conn, connection_string
    c = _Conn(connection_string())
    for t in TABLES:
        c.execute(f"IF OBJECT_ID(N'{t}_append_only', N'TR') IS NOT NULL DROP TRIGGER {t}_append_only")
        c.execute(f"IF OBJECT_ID(N'{t}', N'U') IS NOT NULL DROP TABLE {t}")


@unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")
class MssqlStoreTests(StoreTests):
    """The same behaviour suite against SQL Server or Azure SQL, snapshots in the local test double."""

    def make(self):
        wipe_mssql()
        return lawstore.LawStore(db=lawstore.MssqlDb(), blobs=lawstore.LocalSnapshots(Path(self.tmp.name) / "blobs"))

    test_ledger_ddl_maps_every_append_only_table = None


class ViewerTests(LawBase):
    def setUp(self):
        super().setUp()
        self.user = {"email": "pm@example.org", "name": "PM", "role": "Retrofit Programme Manager", "code": "PM"}
        test = self
        tmp = tempfile.TemporaryDirectory()
        self.tmp2 = tmp
        data = Path(tmp.name) / "zavaforward.json"
        data.write_text(json.dumps(test_mvp.DATA))

        class Identity:
            name = "password"

            def authenticate(self, headers):
                return test.user
        self.app = App(SqlStore(str(data), str(Path(tmp.name) / "pw.sqlite")), provider=Identity(), law=self.law)
        self.http = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.http.server_port}"

    def tearDown(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
        self.tmp2.cleanup()
        super().tearDown()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.url + path) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            return e.code, json.load(e)

    def test_viewer_api_works_without_ai(self):
        self.assertIn(self.user["role"], STAFF_ROLES)
        status, body = self.get("/api/law/sources")
        self.assertEqual(status, 200)
        self.assertEqual(len(body["gaps"]), 4)
        sid = body["sources"][0]["id"]
        status, src = self.get(f"/api/law/sources/{sid}")
        self.assertEqual(status, 200)
        status, p = self.get(f"/api/law/provisions/{src['provisions'][0]['id'].replace('#', '%23')}")
        self.assertEqual(status, 200)
        self.assertIn("caveats", p)
        self.assertEqual(self.get("/api/law/search?q=leasehold")[1]["no_source_held"][0]["id"], "gap-leasehold")
        self.assertEqual(self.get("/api/law/sources/nope")[0], 404)

    def test_viewer_is_read_only_and_role_gated(self):
        req = urllib.request.Request(self.url + "/api/law/sources", data=b"{}", method="POST", headers={"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(req)
        self.user = dict(self.user, role="Contractor")
        self.assertEqual(self.get("/api/law/sources")[0], 403)
        self.user = self.user and dict(self.user, role="Retrofit Programme Manager")
        self.app.law = None
        self.assertEqual(self.get("/api/law/sources")[0], 503)


if __name__ == "__main__":
    unittest.main()
