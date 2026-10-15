import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import test_mvp
from zavaforward_mvp import ledger, loadcheck, recovery
from zavaforward_mvp.sqlstore import SqlStore


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
            p.write_text(json.dumps(test_mvp.DATA))
            s = SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))
            with s.dblock:
                s.db.execute("BEGIN IMMEDIATE")
                s._append_audit([("a", "x", "ZF-1", "d", at(2025)), ("a", "x", "ZF-1", "d", at(2025))])
                s.db.execute("COMMIT")
            s.log_call(test_mvp.DATA["staff"][0], "ZF-1", "Call", "")
            files = s.write_year_digests()
            self.assertEqual([os.path.basename(f) for f in files], ["year-2025.json"])
            self.assertEqual(s.write_year_digests(), files)
            rep = s.verify_ledger_by_year()
            self.assertTrue(rep["intact"] and rep["years"]["2025"]["sealed"])
            s.db.execute("DROP TRIGGER audit_no_delete")
            s.db.execute("DELETE FROM audit WHERE seq=2")
            self.assertFalse(s.verify_ledger_by_year()["intact"])


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        self.data = str(p)
        self.db = os.path.join(self.tmp.name, "pw.sqlite")
        self.store = SqlStore(self.data, self.db)
        self.sam = test_mvp.DATA["staff"][0]

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

    def test_reason_required(self):
        with self.assertRaises(ValueError):
            recovery.erase_resident(self.store, self.sam, "ZF-1", " ")


class LoadCheckTests(unittest.TestCase):
    def test_grow_clones_to_requested_synthetic_homes_and_run_reports_classes(self):
        src = loadcheck.grow(json.loads(json.dumps(test_mvp.DATA)), 40)
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
