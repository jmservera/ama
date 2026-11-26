import json
import os
import shutil
import tempfile
import unittest
import urllib.parse
from pathlib import Path

import dataset
from zava_forward.core import ledger
from zava_forward.core.synthetic import loadcheck
from zava_forward.core import recovery
from zava_forward.core import assistant_release as rel
from zava_forward.core.documents import AzureBlobDocumentStore, DocumentStoreError
from zava_forward.core.sqlstore import LedgerRelianceError, SqlStore
from zava_forward.core.store import Store


def at(year):
    return f"{year}-06-01T10:00:00"


def chain(years):
    prev, out = ledger.GENESIS, []
    for i, y in enumerate(years):
        e = ledger.make_entry("sam", "x", "ZF-1", f"n{i}", prev, at(y))
        out.append(e)
        prev = e["hash"]
    return out


class YearLedgerTests(unittest.TestCase):
    def test_each_year_verifies_alone_and_with_sealed_digests(self):
        es = chain([2024, 2024, 2025, 2025, 2025, 2026])
        sealed = ledger.year_digests(es, before=2026)
        self.assertEqual([d["year"] for d in sealed], ["2024", "2025"])
        rep = ledger.verify_years(es, sealed)
        self.assertTrue(rep["intact"])
        self.assertEqual({y: v["entries"] for y, v in rep["years"].items()}, {"2024": 2, "2025": 3, "2026": 1})
        self.assertTrue(rep["years"]["2025"]["sealed"] and not rep["years"]["2026"]["sealed"])

    def test_edit_in_one_year_is_reported_for_that_year_only_and_digest_catches_rewrite(self):
        es = chain([2024, 2024, 2025, 2025])
        sealed = ledger.year_digests(es, before=2026)
        bad = [dict(e) for e in es]
        bad[0]["detail"] = "changed"
        rep = ledger.verify_years(bad, sealed)
        self.assertFalse(rep["intact"])
        self.assertFalse(rep["years"]["2024"]["intact"])
        self.assertTrue(rep["years"]["2025"]["intact"])
        # rewrite 2025 as a self-consistent shorter chain: only the sealed digest exposes it
        short = es[:3]
        self.assertTrue(ledger.verify_entries(short)["intact"])
        rep = ledger.verify_years(short, sealed)
        self.assertFalse(rep["intact"])
        self.assertIn("year differs from its sealed digest", rep["years"]["2025"]["problems"])

    def test_dropping_a_sealed_year_is_reported(self):
        es = chain([2024, 2025, 2025])
        sealed = ledger.year_digests(es, before=2026)
        rep = ledger.verify_years(es[1:], sealed)
        self.assertFalse(rep["intact"])
        self.assertEqual(rep["missing_years"], ["2024"])

    def test_sql_store_seals_past_years_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(dataset.DATA))
            s = SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))
            with s.dblock:
                s.db.execute("BEGIN IMMEDIATE")
                s._append_audit([("a", "x", "ZF-1", "d", at(2025)), ("a", "x", "ZF-1", "d", at(2025))])
                s.db.execute("COMMIT")
            s.log_call(dataset.DATA["staff"][0], "ZF-1", "Call", "")
            files = s.write_year_digests()
            self.assertEqual([os.path.basename(f) for f in files], ["year-2025.json"])
            self.assertEqual(s.write_year_digests(), files)
            rep = s.verify_ledger_by_year()
            self.assertTrue(rep["intact"] and rep["years"]["2025"]["sealed"])
            s.db.execute("DROP TRIGGER audit_no_delete")
            s.db.execute("DELETE FROM audit WHERE seq=2")
            self.assertFalse(s.verify_ledger_by_year()["intact"])


    def test_corrupt_or_malformed_digests_fail_closed_and_sealed_years_are_listed(self):
        es = chain([2024, 2025])
        sealed = ledger.year_digests(es, before=2026)
        rep = ledger.verify_years(es, sealed)
        self.assertEqual(rep["sealed_years"], ["2024", "2025"])
        for bad in ({"unreadable": "year-2024.json"}, {"year": "2024"}, None):
            rep = ledger.verify_years(es, [bad, sealed[1]])
            self.assertFalse(rep["intact"])
            self.assertEqual(len(rep["bad_digests"]), 1)
        rep = ledger.verify_years(es, [sealed[0], dict(sealed[0], head="0" * 64)])
        self.assertFalse(rep["intact"])

    def test_unreadable_digest_file_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "year-2024.json").write_text("{not json")
            got = ledger.read_year_digests(tmp)
            self.assertEqual(got, [{"unreadable": "year-2024.json"}])
            self.assertFalse(ledger.verify_years(chain([2024]), got)["intact"])

    def test_non_object_digest_file_is_unreadable_and_fails_closed(self):
        for text in ("null", "[]", "[1, 2]", "7", '"x"', "true"):
            with self.subTest(text=text), tempfile.TemporaryDirectory() as tmp:
                Path(tmp, "year-2024.json").write_text(text)
                got = ledger.read_year_digests(tmp)
                self.assertEqual(got, [{"unreadable": "year-2024.json"}])
                rep = ledger.verify_years(chain([2024]), got)
                self.assertFalse(rep["intact"])
                self.assertEqual(rep["bad_digests"], ["year-2024.json"])

    def _seed_file_store(self, tmp, entries):
        data_path = Path(tmp) / "zavaforward.json"
        data_path.write_text(json.dumps(dataset.DATA))
        audit_path = Path(tmp) / "audit.jsonl"
        audit_path.write_text("".join(json.dumps(e) + "\n" for e in entries))
        return Store(str(data_path))

    def test_file_store_pre_reliance_seals_past_years_and_passes_across_2024_2025_2026(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = self._seed_file_store(tmp, chain([2024, 2024, 2025, 2025, 2025, 2026]))
            rep = s.verify_ledger_before_reliance(current_year=2026)
            self.assertTrue(rep["reliance_allowed"])
            self.assertTrue(rep["intact"])
            self.assertEqual(rep["current_year"], "2026")
            self.assertEqual(rep["entries"], 6)
            self.assertEqual(rep["sealed_years"], ["2024", "2025"])
            self.assertEqual(rep["sealed_digest_files"], ["year-2024.json", "year-2025.json"])
            self.assertTrue(rep["years"]["2024"]["sealed"] and rep["years"]["2025"]["sealed"])
            self.assertFalse(rep["years"]["2026"]["sealed"])
            self.assertEqual(rep["problems"], [])
            # Idempotent re-verification and default current_year path
            again = s.require_verified_ledger_for_reliance()
            self.assertTrue(again["reliance_allowed"])
            # Next-year rollover seals 2026 too
            rolled = s.require_verified_ledger_for_reliance(current_year=2027)
            self.assertEqual(rolled["sealed_years"], ["2024", "2025", "2026"])
            self.assertTrue(rolled["years"]["2026"]["sealed"])

    def test_unsealed_single_year_run_writes_no_digest_and_report_carries_no_entry_content(self):
        prev, entries = ledger.GENESIS, []
        for i in range(40):
            e = ledger.make_entry("alice-private-actor", "private-action", "ZF-PRIVATE", f"n{i}", prev, at(2026))
            entries.append(e)
            prev = e["hash"]
        with tempfile.TemporaryDirectory() as tmp:
            s = self._seed_file_store(tmp, entries)
            rep = s.verify_ledger_before_reliance(current_year=2026, seal_past_years=False)
            self.assertTrue(rep["reliance_allowed"])
            self.assertEqual(rep["entries"], 40)
            self.assertEqual(rep["sealed_digest_files"], [])
            self.assertEqual(list(Path(s.digest_dir).glob("year-*.json")) if Path(s.digest_dir).is_dir() else [], [])
            text = json.dumps(rep)
            for private in ("alice-private-actor", "private-action", "ZF-PRIVATE"):
                self.assertNotIn(private, text)

    def test_pre_reliance_refuses_to_seal_tampered_chain_and_blocks_reliance(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = chain([2024, 2025, 2026])
            bad[0] = dict(bad[0], detail="tampered-before-seal")
            s = self._seed_file_store(tmp, bad)
            rep = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(rep["reliance_allowed"])
            self.assertIn("chain_tampered", {p["code"] for p in rep["problems"]})
            self.assertFalse(os.path.exists(s.digest_dir))
            with self.assertRaises(LedgerRelianceError) as cm:
                s.require_verified_ledger_for_reliance(current_year=2026)
            self.assertFalse(cm.exception.report["reliance_allowed"])
            self.assertIn("chain_tampered", {p["code"] for p in cm.exception.problems})
            self.assertNotIn(tmp, json.dumps(rep))
            self.assertNotIn(tmp, str(cm.exception))

    def test_pre_reliance_blocks_corrupt_swapped_or_root_mismatched_digests_and_unsealed_past_years(self):
        entries = chain([2024, 2025, 2026])
        with self.subTest("unsealed_past_years_blocked_when_seal_disabled"), tempfile.TemporaryDirectory() as tmp:
            s = self._seed_file_store(tmp, entries)
            blocked = s.verify_ledger_before_reliance(current_year=2026, seal_past_years=False)
            self.assertFalse(blocked["reliance_allowed"])
            self.assertEqual(
                [(p["code"], p.get("year")) for p in blocked["problems"]],
                [("unsealed_past_year", "2024"), ("unsealed_past_year", "2025")],
            )
            allowed = s.verify_ledger_before_reliance(
                current_year=2026, require_sealed_past_years=False, seal_past_years=False
            )
            self.assertTrue(allowed["reliance_allowed"])

        with self.subTest("corrupt_and_swapped_year_digests"), tempfile.TemporaryDirectory() as tmp:
            s = self._seed_file_store(tmp, entries)
            s.require_verified_ledger_for_reliance(current_year=2026)
            y2024 = Path(s.digest_dir) / "year-2024.json"
            y2025 = Path(s.digest_dir) / "year-2025.json"
            y2024.write_text(y2025.read_text())
            swapped = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(swapped["reliance_allowed"])
            self.assertIn(
                ("corrupt_year_digest", "2024"),
                {(p["code"], p.get("year")) for p in swapped["problems"]},
            )
            self.assertTrue(any("mismatched" in p["reason"] for p in swapped["problems"]))
            y2024.write_text("{corrupt")
            corrupt = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(corrupt["reliance_allowed"])
            self.assertIn("corrupt_year_digest", {p["code"] for p in corrupt["problems"]})

        with self.subTest("tampered_root_digest_and_dropped_sealed_year"), tempfile.TemporaryDirectory() as tmp:
            s = self._seed_file_store(tmp, entries)
            s.write_digest()
            s.require_verified_ledger_for_reliance(current_year=2026)
            root_file = Path(s.digest_dir) / "digest-0000000003.json"
            payload = json.loads(root_file.read_text())
            payload["head"] = "0" * 64
            root_file.write_text(json.dumps(payload))
            rep = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(rep["reliance_allowed"])
            self.assertIn("root_digest_mismatch", {p["code"] for p in rep["problems"]})
            root_file.unlink()
            # Rewrite audit.jsonl dropping 2024 as a fresh chain over 2025 and 2026
            rewritten = chain([2025, 2026])
            Path(s.audit_path).write_text("".join(json.dumps(e) + "\n" for e in rewritten))
            dropped = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(dropped["reliance_allowed"])
            self.assertEqual(dropped["missing_years"], ["2024"])
            self.assertIn("missing_audit_year", {p["code"] for p in dropped["problems"]})

    def test_pre_reliance_blocks_corrupt_audit_file_non_dir_digests_and_malformed_entry_years(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = self._seed_file_store(tmp, chain([2024, 2025, 2026]))
            Path(s.digest_dir).write_text("not-a-directory")
            rep = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(rep["reliance_allowed"])
            self.assertIn("digest_store_unreadable", {p["code"] for p in rep["problems"]})
            Path(s.digest_dir).unlink()
            bad_year = ledger.make_entry("sam", "x", "ZF-1", "n0", ledger.GENESIS, "20X4-06-01T10:00:00")
            Path(s.audit_path).write_text(json.dumps(bad_year) + "\n")
            rep_year = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(rep_year["reliance_allowed"])
            self.assertIn("audit_entry_malformed", {p["code"] for p in rep_year["problems"]})
            Path(s.audit_path).write_text("{corrupt-audit-jsonl\n")
            rep_corrupt = s.verify_ledger_before_reliance(current_year=2026)
            self.assertFalse(rep_corrupt["reliance_allowed"])
            self.assertIn("audit_unreadable", {p["code"] for p in rep_corrupt["problems"]})


class FakeRegisterBlob:
    def __init__(self):
        self.blobs, self.fail_put, self.fail_list = {}, False, False

    def __call__(self, method, url, headers, body):
        u = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(u.query)
        if method == "PUT":
            if self.fail_put:
                return 500, {}, b""
            if "If-None-Match" in headers and u.path in self.blobs:
                return 409, {}, b""
            self.blobs[u.path] = body
            return 201, {}, b""
        if method == "GET" and q.get("comp") == ["list"]:
            if self.fail_list:
                return 503, {}, b""
            pre = "/" + q["prefix"][0]
            names = "".join(f"<Blob><Name>{k[len('/case-docs/'):]}</Name></Blob>" for k in sorted(self.blobs) if k.startswith("/case-docs" + pre))
            return 200, {}, f"<EnumerationResults><Blobs>{names}</Blobs><NextMarker /></EnumerationResults>".encode()
        if method == "GET":
            return (200, {}, self.blobs[u.path]) if u.path in self.blobs else (404, {}, b"")
        return 405, {}, b""


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(dataset.DATA))
        self.data = str(p)
        self.db = os.path.join(self.tmp.name, "pw.sqlite")
        self.store = SqlStore(self.data, self.db)
        self.sam = dataset.DATA["staff"][0]

    def tearDown(self):
        self.tmp.cleanup()

    def test_erasure_survives_restore_of_an_older_backup(self):
        self.store.log_call(self.sam, "ZF-1", "Spoke to resident", "phone note")
        bak = recovery.backup(self.store, os.path.join(self.tmp.name, "backup.sqlite"))
        recovery.erase_resident(self.store, self.sam, "ZF-1", "Erasure request ER-DEMO-1 (synthetic)")
        self.assertEqual(self.store.cases["ZF-1"]["resident"]["name"], recovery.REDACTED)
        self.store.db.close()
        shutil.copy(bak, self.db)
        for suffix in ("-wal", "-shm"):
            if os.path.exists(self.db + suffix):
                os.remove(self.db + suffix)
        restored = SqlStore(self.data, self.db)
        self.assertEqual(restored.cases["ZF-1"]["resident"]["name"], "Pat Test")
        self.assertEqual(recovery.reapply_deletions(restored), ["ZF-1"])
        r = restored.cases["ZF-1"]
        self.assertEqual((r["resident"]["name"], r["resident"]["phone"], r["contacts"][0]["note"]), (recovery.REDACTED,) * 3)
        self.assertEqual(recovery.reapply_deletions(restored), [])
        self.assertIn("ZF-1", " ".join(e["case"] for e in restored.audit_entries() if e["action"] == "erasure_reapplied"))
        self.assertTrue(restored.verify_ledger()["intact"])
        self.assertNotIn("Pat Test", json.dumps(recovery.read_register(restored)))

    def test_register_is_in_the_document_backend_not_a_local_register_file(self):
        recovery.erase_resident(self.store, self.sam, "ZF-1", "ER-1")
        self.assertEqual([e["case"] for e in recovery.read_register(self.store)], ["ZF-1"])
        found = [f for _, _, fs in os.walk(self.tmp.name) for f in fs]
        self.assertFalse([f for f in found if f.endswith(".jsonl")])

    def test_register_survives_on_blob_backend_and_blocks_erasure_when_unwritable(self):
        blob = FakeRegisterBlob()
        self.store.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        recovery.erase_resident(self.store, self.sam, "ZF-1", "ER-1")
        self.assertTrue(any(k.startswith("/case-docs/_erasures/") for k in blob.blobs))
        self.assertEqual(self.store.cases["ZF-1"]["resident"]["name"], recovery.REDACTED)
        self.assertEqual([e["reason"] for e in recovery.read_register(self.store)], ["ER-1"])
        blob.fail_put = True
        before = self.store.cases["ZF-2"]["resident"]["name"] if "ZF-2" in self.store.cases else None
        with self.assertRaises(DocumentStoreError):
            recovery.erase_resident(self.store, self.sam, "ZF-1", "ER-2")
        self.assertEqual(len(blob.blobs), 1)
        if before:
            self.assertEqual(self.store.cases["ZF-2"]["resident"]["name"], before)

    def test_unreadable_register_is_an_error_not_an_empty_register(self):
        blob = FakeRegisterBlob()
        blob.fail_list = True
        self.store.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        with self.assertRaises(DocumentStoreError):
            recovery.reapply_deletions(self.store)

    def test_entry_is_written_before_redaction_so_a_crash_cannot_lose_it(self):
        def boom():
            raise RuntimeError("crash after redaction")
        self.store.save = boom
        with self.assertRaises(RuntimeError):
            recovery.erase_resident(self.store, self.sam, "ZF-1", "ER-CRASH")
        self.assertEqual([e["reason"] for e in recovery.read_register(self.store)], ["ER-CRASH"])

    def test_register_entry_precedes_redaction_and_unknown_case_writes_nothing(self):
        seen = []
        real = recovery._redact
        recovery._redact = lambda c: (seen.append(len(recovery.read_register(self.store))), real(c))[1]
        try:
            recovery.erase_resident(self.store, self.sam, "ZF-1", "ER-1")
        finally:
            recovery._redact = real
        self.assertEqual(seen, [1])
        with self.assertRaises(KeyError):
            recovery.erase_resident(self.store, self.sam, "ZF-NOPE", "ER-2")
        self.assertEqual(len(recovery.read_register(self.store)), 1)

    def test_reason_required(self):
        with self.assertRaises(ValueError):
            recovery.erase_resident(self.store, self.sam, "ZF-1", " ")

    def _release_db(self):
        db = self.store.assistant_connection()
        for ddl in rel.SQLITE_DDL:
            db.execute(ddl)
        db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES ('r1','t','active','{}',1)")
        db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES ('r2','t','active','{}',1)")
        db.execute("CREATE TABLE IF NOT EXISTS assistant_events (id TEXT PRIMARY KEY, task_id TEXT, at REAL, body TEXT)")
        return db

    def test_restore_does_not_resurrect_suspended_or_revoked_release(self):
        db = self._release_db()
        self.assertTrue(recovery.record_release_change(self.store, db, "r1", "suspended"))
        self.assertTrue(recovery.record_release_change(self.store, db, "r2", "suspended"))
        rel.change(db, 1.0, None, "r1", "suspended", "incident", system=True)
        rel.change(db, 1.0, None, "r2", "suspended", "incident", system=True)
        self.assertTrue(recovery.record_release_change(self.store, db, "r2", "revoked"))
        rel.change(db, 2.0, None, "r2", "revoked", "withdrawn", system=True)
        # a restore returns both rows to the earlier active state
        db.execute("UPDATE assistant_releases SET status='active'")
        self.assertEqual(recovery.reapply_release_changes(db, 3.0, self.store), ["r1", "r2"])
        got = dict(db.execute("SELECT id,status FROM assistant_releases").fetchall())
        self.assertEqual(got, {"r1": "suspended", "r2": "revoked"})
        self.assertEqual(recovery.reapply_release_changes(db, 4.0, self.store), [])
        self.assertNotIn("incident", json.dumps(recovery.read_release_register(self.store)))

    def test_restore_does_not_resurrect_spent_allowance(self):
        from zava_forward.core import assistants
        db = self._release_db()
        db.execute(next(d for d in assistants.SQLITE_DDL if "assistant_allowance" in d))
        db.execute("INSERT INTO assistant_allowance VALUES ('p1', 10, 1000, 9e9, 2, 200)")
        db.execute("INSERT INTO assistant_allowance VALUES ('p2', 10, 1000, 9e9, 10, 1000)")
        self.assertEqual(recovery.close_allowance_after_restore(db), 1)
        rows = db.execute("SELECT id,calls,tokens,used_calls,reserved_tokens FROM assistant_allowance ORDER BY id").fetchall()
        self.assertEqual([tuple(r) for r in rows], [("p1", 10, 1000, 10, 1000), ("p2", 10, 1000, 10, 1000)])
        self.assertEqual(recovery.close_allowance_after_restore(db), 0)

    def test_reconcile_after_restore_runs_every_step_once_and_fails_closed(self):
        from zava_forward.core import assistants
        db = self._release_db()
        db.execute(next(d for d in assistants.SQLITE_DDL if "assistant_allowance" in d))
        db.execute("INSERT INTO assistant_allowance VALUES ('p1', 10, 1000, 9e9, 2, 200)")
        self.assertTrue(recovery.record_release_change(self.store, db, "r1", "suspended"))
        rel.change(db, 1.0, None, "r1", "suspended", "incident", system=True)
        db.execute("UPDATE assistant_releases SET status='active'")
        got = recovery.reconcile_after_restore(self.store, db, 2.0)
        self.assertEqual(got, dict(erasures=[], releases=["r1"], allowance_pools=1))
        self.assertEqual(recovery.reconcile_after_restore(self.store, db, 3.0), dict(erasures=[], releases=[], allowance_pools=0))
        db.execute("UPDATE assistant_allowance SET used_calls=0, reserved_tokens=0")
        self.store.docstore.list_ids = lambda case: (_ for _ in ()).throw(DocumentStoreError("down"))
        with self.assertRaises(DocumentStoreError):
            recovery.reconcile_after_restore(self.store, db, 4.0)
        self.assertEqual(db.execute("SELECT used_calls FROM assistant_allowance").fetchone()[0], 0)

    def test_release_register_writes_nothing_for_unchanged_unknown_or_invalid_change(self):
        db = self._release_db()
        self.assertFalse(recovery.record_release_change(self.store, db, "nope", "suspended"))
        self.assertFalse(recovery.record_release_change(self.store, db, "r1", "active"))
        rel.change(db, 1.0, None, "r1", "revoked", "withdrawn", system=True)
        self.assertFalse(recovery.record_release_change(self.store, db, "r1", "suspended"))
        self.assertEqual(recovery.read_release_register(self.store), [])

    def test_unwritable_release_register_blocks_the_change(self):
        db = self._release_db()
        blob = FakeRegisterBlob()
        blob.fail_put = True
        self.store.docstore = AzureBlobDocumentStore("https://acct.blob.core.windows.net", "case-docs", sas="s=1", transport=blob)
        with self.assertRaises(DocumentStoreError):
            recovery.record_release_change(self.store, db, "r1", "suspended")
        self.assertEqual(blob.blobs, {})


class LoadCheckTests(unittest.TestCase):
    def test_grow_clones_to_requested_synthetic_homes_and_run_reports_classes(self):
        src = loadcheck.grow(json.loads(json.dumps(dataset.DATA)), 40)
        self.assertEqual(len({c["id"] for c in src["cases"]}), 40)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "d.json"
            p.write_text(json.dumps(src))
            s = SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))
            rep = loadcheck.run(s, src["staff"][1], seconds=1)
        self.assertEqual(rep["errors"], 0)
        self.assertTrue(all(c["n"] > 0 for c in rep["classes"].values()))


if __name__ == "__main__":
    unittest.main()
