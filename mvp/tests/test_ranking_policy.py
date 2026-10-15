"""Ranking policy files and snapshots (PR-006, FR-012, ADR 0002 decision 4)."""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import test_mvp
from zava_forward.core import ranking
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from test_ranking_scale import STAFF, hazard, varied

AS_OF = "2026-10-09"
POLICY_FILE = Path(ranking.POLICY_DIR) / "ranking-v1.json"
RLO, PM = STAFF[0], STAFF[1]


def golden_cases():
    a, b, c, d, e = (test_mvp.case(f"ZF-{x}") for x in "ABCDE")
    b["days_in_stage"] = 50
    c["hazards"] = [hazard()]
    d["resident"]["priority_support"] = True
    e.update(stage="Survey booked", days_in_stage=50)
    return [a, b, c, d, e]


class PolicyFileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)

    def test_shipped_policy_loads_with_owner_and_status_unchanged(self):
        p = ranking.load_policy(POLICY_FILE)
        self.assertEqual((p["policy_id"], p["version"], p["owner"]), ("zava-forward-home-ranking", "1.0.0", "to be named"))
        self.assertTrue(p["status"].startswith("Draft rule order, not yet signed off"))
        self.assertEqual(p["content_hash"], ranking.policy_hash(p))
        self.assertIn("1.0.0", ranking.POLICIES)

    def test_tampered_policy_is_refused(self):
        p = json.loads(POLICY_FILE.read_text())
        p["rules"][0], p["rules"][1] = p["rules"][1], p["rules"][0]
        (self.dir / "ranking-v1.json").write_text(json.dumps(p))
        with self.assertRaises(ranking.PolicyError):
            ranking.load_policy(self.dir / "ranking-v1.json")
        with self.assertRaises(ranking.PolicyError):
            ranking.load_registry(str(self.dir))

    def test_policy_missing_a_field_is_refused(self):
        p = json.loads(POLICY_FILE.read_text())
        del p["effective_date"]
        (self.dir / "x.json").write_text(json.dumps(p))
        with self.assertRaises(ranking.PolicyError):
            ranking.load_policy(self.dir / "x.json")

    def test_old_version_stays_loadable_and_reruns_identically(self):
        shutil.copy(POLICY_FILE, self.dir / "ranking-v1.json")
        v2 = json.loads(POLICY_FILE.read_text())
        v2.update(version="2.0.0", effective_date="2026-12-01")
        v2["rules"] = [r for r in v2["rules"] if r["code"] != "support"]
        v2["content_hash"] = ranking.policy_hash(v2)
        (self.dir / "ranking-v2.json").write_text(json.dumps(v2))
        reg = ranking.load_registry(str(self.dir))
        self.assertEqual(sorted(reg), ["1.0.0", "2.0.0"])
        self.assertEqual(ranking.latest(reg)["version"], "2.0.0")
        cases = golden_cases()
        old = ranking.snapshot(cases, reg["1.0.0"], AS_OF)
        self.assertEqual(ranking.canonical(old), ranking.canonical(ranking.snapshot(cases, ranking.POLICY_V1, AS_OF)))
        new = ranking.snapshot(cases, reg["2.0.0"], AS_OF)
        self.assertNotEqual([e["id"] for e in old["entries"]], [e["id"] for e in new["entries"]])
        self.assertEqual(new["policy_version"], "2.0.0")


class SnapshotTests(unittest.TestCase):
    def test_golden_snapshot_order_and_byte_identical_rerun(self):
        cases = golden_cases()
        snap = ranking.snapshot(cases, ranking.POLICY_V1, AS_OF)
        self.assertEqual([e["id"] for e in snap["entries"]], ["ZF-C", "ZF-D", "ZF-B", "ZF-E", "ZF-A"])
        self.assertEqual([e["deciding_rule"] for e in snap["entries"]], [None, "safety_open", "support", "stage_order", "waiting_days"])
        self.assertEqual((snap["policy_version"], snap["policy_hash"], snap["as_of"]),
                         ("1.0.0", ranking.POLICY_V1["content_hash"], AS_OF))
        self.assertEqual(snap["entries"][0]["reason_codes"][0], "safety_open")
        first = ranking.canonical(snap)
        for _ in range(3):
            shuffled = copy.deepcopy(cases[::-1])
            self.assertEqual(ranking.canonical(ranking.snapshot(shuffled, ranking.POLICY_V1, AS_OF)), first)

    def test_ranking_module_has_no_clock(self):
        src = Path(ranking.__file__).read_text()
        self.assertNotIn("datetime", src)
        self.assertNotIn("import time", src)


class StoreSnapshotBase:
    def make(self, tmp, cases):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = self.make(Path(self.tmp.name), varied(60, seed=5))

    def test_snapshot_matches_ranking_and_is_manager_only(self):
        with self.assertRaises(PermissionError):
            self.store.ranking_snapshot(RLO)
        snap = self.store.ranking_snapshot(PM)
        want = [e["id"] for e in ranking.rank([c for c in self.store.cases.values() if not c["closed"]])]
        self.assertEqual([e["id"] for e in snap["entries"]], want)
        self.assertEqual(snap["as_of"], self.store.as_of)
        with self.assertRaises(ValueError):
            self.store.ranking_snapshot(PM, "9.9.9")

    def test_snapshot_unchanged_after_ai_priority_call(self):
        before = ranking.canonical(self.store.ranking_snapshot(PM))
        files = {p.name: p.read_bytes() for p in Path(self.tmp.name).glob("ranking-snapshot-*.json")}
        self.assertEqual(len(files), 1)
        self.store.ai_priority(RLO, 5)
        self.assertEqual(ranking.canonical(self.store.ranking_snapshot(PM)), before)
        self.assertEqual({p.name: p.read_bytes() for p in Path(self.tmp.name).glob("ranking-snapshot-*.json")}, files)

    def test_list_header_carries_policy_hash_and_as_of(self):
        d = self.store.page_cases(PM, "all", limit=10)
        self.assertEqual((d["policy_version"], d["policy_hash"], d["as_of"]),
                         ("1.0.0", ranking.CURRENT["content_hash"], self.store.as_of))


class JsonStoreSnapshotTests(StoreSnapshotBase, unittest.TestCase):
    def make(self, tmp, cases):
        (tmp / "zavaforward.json").write_text(json.dumps(dict(staff=STAFF, cases=cases)))
        return Store(str(tmp / "zavaforward.json"))


class SqlStoreSnapshotTests(StoreSnapshotBase, unittest.TestCase):
    def make(self, tmp, cases):
        (tmp / "zavaforward.json").write_text(json.dumps(dict(staff=STAFF, cases=cases)))
        return SqlStore(str(tmp / "zavaforward.json"), str(tmp / "pw.sqlite"))

    def test_json_and_sql_snapshots_agree(self):
        other = Path(self.tmp.name) / "j"
        other.mkdir()
        cases = [json.loads(json.dumps(c)) for c in self.store.cases.values()]
        js = JsonStoreSnapshotTests.make(self, other, cases)
        js.as_of = self.store.as_of
        self.assertEqual(ranking.canonical(js.ranking_snapshot(PM)), ranking.canonical(self.store.ranking_snapshot(PM)))


if __name__ == "__main__":
    unittest.main()
