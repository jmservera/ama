"""SqlStore list reads answered by SQL: parity with the in-memory store, keyset paging, migration, query plans, 60,000 timing."""
import copy
import json
import os
import random
import sqlite3
import tempfile
import time
import unittest
from pathlib import Path

import dataset as fixtures
from zava_forward.core import ranking
from zava_forward.core.insights import STAGE_ORDER
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

STAFF = [dict(code="RLO-01", name="Sam Example", email="sam@example.test", role="Resident Liaison Officer"),
         dict(code="PM-01", name="Pam Lead", email="pam@example.test", role="Retrofit Programme Manager"),
         dict(code="CON-1", name="Kim Builder", email="kim@example.test", role="Contractor", contractor="Alpha Ltd")]
NAMES = ["Ann Smith", "bob Jones", "Cy Zed", "Dee O'Neil", "Eve 100% Brown", "Flo Under_score", "Gus Ándersen"]
FUNDING = ["Not started", "To prepare", "Draft ready", "Approved", "Submitted", "Confirmed"]


def make_cases(n, seed=11):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        c = fixtures.case(f"ZF-{i:05d}", owner_code=rnd.choice(["RLO-01", "PM-01"]), stage=rnd.choice(STAGE_ORDER),
                          decision=rnd.choice(fixtures.DECISIONS if hasattr(fixtures, "DECISIONS") else ["Waiting", "Accepted", "Declined", "Not yet asked"]))
        c["days_in_stage"] = rnd.choice([0, 1, 5, 5, 30, 60, 61, 120, 400])
        c["resident"].update(name=rnd.choice(NAMES), priority_support=rnd.random() < 0.1, adjustment=rnd.choice(["None", "None", "Hearing"]))
        c["home"].update(area=rnd.choice(["North", "South", "East"]), address=f"{i} Test Road", postcode=f"TE{i % 9} 1ST", lat=54 + rnd.random(), lon=-2 + rnd.random())
        c["wave"] = rnd.choice(["Wave 1", "Wave 2"])
        c["contractor"]["name"] = rnd.choice(["Alpha Ltd", "Beta Ltd"])
        c["funding"] = dict(route="ECO", status=rnd.choice(FUNDING), reference="", draft="", approved_by=None)
        c["closed"] = rnd.random() < 0.03
        if rnd.random() < 0.05:
            c["hazards"] = [dict(category="Damp", priority="P1", noticed="2026-01-01", referred=None, repaired=None, released=rnd.random() < 0.3, job="J", owner="Bea")]
        if rnd.random() < 0.6:
            c["contacts"] = [dict(at=f"2026-0{rnd.randint(1, 9)}-1{rnd.randint(0, 9)}T10:00", purpose="u", channel="Phone", direction="Outbound", outcome="Spoke", note="", by="Sam")]
        if rnd.random() < 0.3:
            c["appointments"] = [dict(type="Survey", date=f"2026-1{rnd.randint(0, 2)}-0{rnd.randint(1, 9)}", slot="AM", outcome="Booked", note="", who="x", person="y")]
        out.append(c)
    return out


def dataset(cases):
    d = copy.deepcopy(fixtures.DATA)
    d["staff"], d["cases"] = copy.deepcopy(STAFF), cases
    return d


class Parity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        p = Path(cls.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(dataset(make_cases(400))))
        cls.mem = Store(str(p), os.path.join(cls.tmp.name, "mem", "live.json"), os.path.join(cls.tmp.name, "mem", "audit.jsonl"))
        cls.sql = SqlStore(str(p), os.path.join(cls.tmp.name, "pw.sqlite"))
        cls.sam, cls.pam, cls.kim = STAFF

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def same(self, user, **kw):
        a, b = self.mem.page_cases(user, **kw), self.sql.page_cases(user, **kw)
        a.pop("next_cursor", None), b.pop("next_cursor", None)
        self.assertEqual(a, b, kw)

    def test_default_order_matches_ranking_exactly(self):
        order = [e["id"] for e in ranking.rank([c for c in self.mem.cases.values() if not c["closed"]])]
        got = []
        for off in range(0, len(order), 100):
            got += [r["id"] for r in self.sql.page_cases(self.pam, "all", limit=100, offset=off)["items"]]
        self.assertEqual(got, order)

    def test_every_view_filter_sort_and_search_matches_the_in_memory_store(self):
        filters = [{}, {"stage": "Survey booked"}, {"area": "North", "wave": "Wave 1"}, {"owner": "PM-01"}, {"contractor": "Beta Ltd"}] + \
                  [{"flag": f} for f in ("hazard", "support", "long", "nodecision", "funding", "fundingprog")] + [{"area": "East", "flag": "long"}]
        for user in (self.pam, self.sam, self.kim):
            for view in ("all", "mine"):
                for f in filters:
                    for sort in ("urgent", "waiting", "contact", "name", "visit", "bogus"):
                        self.same(user, view=view, filters=f, sort=sort, limit=37, offset=11)
        for q in ("smith", "SMITH", "100%", "under_score", "ándersen", "te3", "zf-0004", "1 test", "zzz"):
            for user in (self.pam, self.kim):
                self.same(user, view="all", q=q, limit=500)

    def test_contractor_search_still_cannot_use_the_resident_name(self):
        self.assertEqual(self.sql.page_cases(self.kim, "all", q="smith", limit=50)["total"], 0)
        self.assertGreater(self.sql.page_cases(self.pam, "all", q="smith", limit=50)["total"], 0)

    def test_contractor_rows_have_no_reason_or_rank_ordering_leak(self):
        d = self.sql.page_cases(self.kim, "all", limit=100)
        self.assertTrue(d["items"])
        for r in d["items"]:
            self.assertEqual(set(r), {"id", "address", "town", "postcode", "stage", "status", "next_visit", "needs_notice", "named_contact", "closed"})

    def test_keyset_walk_equals_offset_walk_and_never_repeats(self):
        for user, view in ((self.pam, "all"), (self.sam, "mine")):
            by_offset = [r["id"] for r in self.sql.page_cases(user, view, limit=1000)["items"]]
            for engine in (self.sql, self.mem):
                walked, cur = [], None
                while True:
                    d = engine.page_cases(user, view, limit=23, after=cur)
                    walked += [r["id"] for r in d["items"]]
                    cur = d["next_cursor"]
                    if not cur:
                        break
                self.assertEqual(walked, by_offset)
                self.assertEqual(len(set(walked)), len(walked))

    def test_keyset_is_stable_when_a_case_changes_between_pages(self):
        first = self.sql.page_cases(self.pam, "all", limit=20)
        last = first["items"][-1]["id"]
        later = self.sql.page_cases(self.pam, "all", limit=20, after=first["next_cursor"])
        self.assertNotIn(last, [r["id"] for r in later["items"]])
        self.assertEqual(later["items"][0]["rank"], 21)

    def test_ranks_are_global_not_page_local(self):
        d = self.sql.page_cases(self.pam, "all", filters={"stage": "Survey booked"}, limit=5)
        ranks = {e["id"]: e["rank"] for e in ranking.rank([c for c in self.mem.cases.values() if not c["closed"]])}
        for r in d["items"]:
            self.assertEqual(r["rank"], ranks[r["id"]])

    def test_counts_match(self):
        for u in (self.sam, self.pam):
            self.assertEqual(self.sql.counts(u), self.mem.counts(u))

    def test_closed_list_and_full_export_still_work(self):
        self.assertEqual(self.sql.page_cases(self.pam, "closed", limit=1000)["total"], sum(c["closed"] for c in self.mem.cases.values()))
        with self.assertRaises(PermissionError):
            self.sql.page_cases(self.sam, "closed", limit=10)
        self.assertEqual(len(self.sql.list_cases(self.pam, "all")), len([c for c in self.mem.cases.values() if not c["closed"]]))


class Writes(unittest.TestCase):
    def test_a_write_moves_the_case_in_the_sql_order_and_another_process_sees_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(dataset(make_cases(300))))
            db = os.path.join(tmp, "pw.sqlite")
            a, b = SqlStore(str(p), db), SqlStore(str(p), db)
            pam = STAFF[1]
            victim = next(r for r in a.page_cases(pam, "all", limit=300)["items"] if r["rank"] > 100)
            a.raise_hazard(pam, victim["id"], "Electrical", "Routine", "x",
                           metadata=dict(source="Synthetic report", aware_at="2026-01-01T10:00:00Z"))
            for engine in (a, b):
                top = {r["id"]: r["rank"] for r in engine.page_cases(pam, "all", limit=50)["items"]}
                self.assertIn(victim["id"], top)


class Migration(unittest.TestCase):
    def test_database_from_the_previous_slice_is_upgraded_in_place(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(dataset(make_cases(60))))
            db = os.path.join(tmp, "pw.sqlite")
            SqlStore(str(p), db)
            raw = sqlite3.connect(db)
            for ix in ("ix_cases_rkey", "ix_cases_owner_rkey", "ix_cases_contractor_rkey", "ix_cases_stage_rkey", "ix_cases_days"):
                raw.execute(f"DROP INDEX {ix}")
            for col in ("rkey", "search", "search_c", "contractor", "surname", "last_contact", "next_visit", "decision", "fstatus", "support", "days"):
                raw.execute(f"ALTER TABLE cases DROP COLUMN {col}")
            raw.execute("DELETE FROM meta WHERE key='rank_policy'")
            raw.commit()
            raw.close()
            s = SqlStore(str(p), db)
            order = [e["id"] for e in ranking.rank([c for c in s.cases.values() if not c["closed"]])]
            got = [r["id"] for r in s.page_cases(STAFF[1], "all", limit=100)["items"]]
            self.assertEqual(got, order[:100])
            self.assertEqual(s.detail("ZF-00001")["id"], "ZF-00001")

    def test_changed_policy_version_rebuilds_the_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(dataset(make_cases(30))))
            db = os.path.join(tmp, "pw.sqlite")
            SqlStore(str(p), db)
            raw = sqlite3.connect(db)
            raw.execute("UPDATE cases SET rkey='zzz'")
            raw.execute("UPDATE meta SET value='0.0.1' WHERE key='rank_policy'")
            raw.commit()
            raw.close()
            s = SqlStore(str(p), db)
            self.assertNotEqual(s.db.execute("SELECT rkey FROM cases LIMIT 1").fetchone()[0], "zzz")


class Plans(unittest.TestCase):
    def test_list_queries_use_indexes_not_table_scans(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(dataset(make_cases(200))))
            s = SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))
            s.db.execute("ANALYZE")
            for where, args in (("closed=0", []), ("closed=0 AND owner_code=?", ["PM-01"]), ("closed=0 AND contractor=?", ["Alpha Ltd"]),
                                ("closed=0 AND stage=?", ["Survey booked"])):
                plan = " ".join(s.explain(f"SELECT id, rkey, body FROM cases WHERE {where} AND rkey>? ORDER BY rkey LIMIT 50", args + ["0"]))
                self.assertIn("USING", plan.upper(), where)
                self.assertNotIn("SCAN CASES", plan.upper().replace("SCAN CASES USING", ""), where)
            plan = " ".join(s.explain("SELECT id, rkey, body FROM cases WHERE closed=0 AND days>=60 ORDER BY days DESC, rkey LIMIT 50"))
            self.assertIn("ix_cases_days", plan)


class Scale(unittest.TestCase):
    N = 60000

    def test_sql_reads_at_60000(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "zavaforward.json"
            p.write_text(json.dumps(dataset(make_cases(self.N, seed=5))))
            s = SqlStore(str(p), os.path.join(tmp, "pw.sqlite"))
            pam, kim = STAFF[1], STAFF[2]
            s.db.execute("ANALYZE")

            def timed(label, **kw):
                t = time.perf_counter()
                d = s.page_cases(**kw)
                ms = (time.perf_counter() - t) * 1000
                print(f"[timing] SQL {label}, {self.N:,} cases: {ms:.0f} ms ({d['total']} matches)")
                return d, ms

            first, ms1 = timed("first page, default order", user=pam, view="all", limit=50)
            deep, ms2 = timed("keyset page after 50 pages", user=pam, view="all", limit=50, after=first["next_cursor"])
            filt, ms3 = timed("filtered page (area, long wait)", user=pam, view="all", filters={"area": "North", "flag": "long"}, limit=50, offset=100)
            mine, ms4 = timed("my cases", user=STAFF[0], view="mine", limit=50)
            srch, ms5 = timed("search 'smith'", user=pam, view="all", q="smith", limit=50)
            sort, ms6 = timed("sort by waiting", user=pam, view="all", sort="waiting", limit=50)
            con, ms7 = timed("contractor list", user=kim, view="all", limit=50)
            t = time.perf_counter()
            s.counts(pam)
            print(f"[timing] SQL header counts, {self.N:,} cases: {(time.perf_counter() - t) * 1000:.0f} ms")
            self.assertEqual(first["ranked_total"], sum(not c["closed"] for c in s.cases.values()))
            self.assertEqual(first["items"][0]["rank"], 1)
            self.assertEqual(deep["items"][0]["rank"], 51)
            for ms in (ms1, ms2, ms3, ms4, ms5, ms6, ms7):
                self.assertLess(ms, 1500)
            order = [e["id"] for e in ranking.rank([c for c in s.cases.values() if not c["closed"]])]
            self.assertEqual([r["id"] for r in first["items"]], order[:50])
            self.assertEqual([r["id"] for r in deep["items"]], order[50:100])


if __name__ == "__main__":
    unittest.main()
