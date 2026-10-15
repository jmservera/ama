import copy
import json
import random
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from zava_forward.core import ranking
from zava_forward.core.insights import STAGE_ORDER
from zava_forward.api.server import App, make_handler
from zava_forward.core.store import Store
from test_mvp import case

STAFF = [dict(code="RLO-01", name="Sam Example", email="sam@example.test", role="Resident Liaison Officer"),
         dict(code="PM-01", name="Pam Lead", email="pam@example.test", role="Retrofit Programme Manager")]


def hazard():
    return dict(category="Damp", priority="P1", noticed="2026-01-01", referred=None, repaired=None, released=False,
                job="J1", owner="Bea Safe")


def varied(n, seed=7):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        c = case(f"ZF-{i:05d}", owner_code="RLO-01" if i % 3 else "PM-01", stage=rnd.choice(STAGE_ORDER),
                 hazards=[hazard()] if rnd.random() < 0.02 else ())
        c["days_in_stage"] = rnd.randint(0, 150)
        c["resident"]["priority_support"] = rnd.random() < 0.08
        c["resident"]["name"] = f"Resident {i}"
        c["home"].update(lat=54.0 + rnd.random() * 2, lon=-3.0 + rnd.random() * 2, area=rnd.choice(["North", "South", "East"]))
        out.append(c)
    return out


class RankingTests(unittest.TestCase):
    def test_golden_order_and_policy_version(self):
        a = case("ZF-A")
        b = case("ZF-B")
        b["days_in_stage"] = 50
        c = case("ZF-C", hazards=[hazard()])
        d = case("ZF-D")
        d["resident"]["priority_support"] = True
        e = case("ZF-E", stage="Survey booked")
        e["days_in_stage"] = 50
        out = ranking.rank([a, b, c, d, e])
        self.assertEqual([x["id"] for x in out], ["ZF-C", "ZF-D", "ZF-B", "ZF-E", "ZF-A"])
        self.assertEqual([x["rank"] for x in out], [1, 2, 3, 4, 5])
        self.assertTrue(all(x["policy_version"] == ranking.POLICY_V1["version"] for x in out))
        self.assertEqual(out[0]["reasons"][0], "Safety issue open")
        self.assertEqual(out[1]["reason_codes"][0], "support")

    def test_same_order_for_any_input_order_byte_identical(self):
        cases = varied(300)
        want = ranking.canonical(ranking.rank(cases))
        rnd = random.Random(3)
        for _ in range(5):
            shuffled = cases[:]
            rnd.shuffle(shuffled)
            self.assertEqual(ranking.canonical(ranking.rank(shuffled)), want)

    def test_ties_break_on_case_id(self):
        cases = [case(f"ZF-{n}") for n in (9, 3, 7, 1)]
        self.assertEqual([x["id"] for x in ranking.rank(cases)], ["ZF-1", "ZF-3", "ZF-7", "ZF-9"])

    def test_new_policy_version_keeps_old_output_reproducible(self):
        cases = varied(200)
        before = ranking.canonical(ranking.rank(cases, ranking.POLICY_V1))
        v2 = copy.deepcopy(ranking.POLICY_V1)
        v2["version"] = "1.1.0"
        v2["rules"] = [r for r in v2["rules"] if r["code"] != "support"]
        v2["rules"].insert(0, dict(code="waiting_days", label="Longest wait first"))
        out2 = ranking.rank(cases, v2)
        self.assertEqual(out2[0]["policy_version"], "1.1.0")
        self.assertNotEqual(ranking.canonical(out2), before)
        self.assertEqual(ranking.canonical(ranking.rank(cases, ranking.POLICY_V1)), before)
        self.assertEqual(ranking.POLICY_V1["version"], "1.0.0")

    def test_unknown_rule_is_rejected(self):
        bad = copy.deepcopy(ranking.POLICY_V1)
        bad["rules"].append(dict(code="vibes", label="x"))
        with self.assertRaises(ValueError):
            ranking.rank([case("ZF-1")], bad)

    def test_policy_has_owner_field_and_rules_in_order(self):
        self.assertEqual(ranking.POLICY_V1["owner"], "to be named")
        self.assertEqual([r["code"] for r in ranking.POLICY_V1["rules"]],
                         ["safety_open", "support", "waiting_days", "stage_order", "case_id"])


class ApiBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        p = Path(cls.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(dict(staff=STAFF, cases=cls.cases())))
        cls.store = Store(str(p))
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(cls.store, "zf-test")))
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"
        cls.cookie = cls.call("/api/login", {"email": "sam@example.test", "password": "zf-test"})[2]["Set-Cookie"].split(";")[0]

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmp.cleanup()

    @classmethod
    def call(cls, path, body=None, cookie=None):
        req = urllib.request.Request(cls.base + path, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"Cookie": cookie} if cookie else {})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read().decode(), dict(r.headers)
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode(), dict(e.headers)

    def get(self, path):
        code, body, _ = self.call(path, cookie=self.cookie)
        return code, json.loads(body)

    def post(self, path, body):
        code, text, _ = self.call(path, body, self.cookie)
        return code, json.loads(text)


class SmallApiTests(ApiBase):
    @classmethod
    def cases(cls):
        return varied(40, seed=2)

    def snapshot(self):
        s = self.store
        return (json.dumps(s.data["cases"], sort_keys=True), ranking.canonical(list(s._ranking().values())),
                json.dumps(s.list_cases(STAFF[0], "all"), sort_keys=True))

    def test_cases_rows_carry_rank_reasons_and_policy_version(self):
        code, d = self.get("/api/cases?view=all&limit=100")
        self.assertEqual(code, 200)
        self.assertEqual(d["policy_version"], "1.0.0")
        self.assertEqual(d["total"], 40)
        self.assertEqual([r["rank"] for r in d["items"]], list(range(1, 41)))
        self.assertTrue(all(r["reasons"] for r in d["items"]))
        code, p = self.get("/api/ranking/policy")
        self.assertEqual((p["version"], p["owner"]), ("1.0.0", "to be named"))

    def test_list_order_is_ranking_order(self):
        order = [r["id"] for r in self.get("/api/cases?view=all&limit=100")[1]["items"]]
        want = [e["id"] for e in ranking.rank([c for c in self.store.cases.values() if not c["closed"]])]
        self.assertEqual(order, want)
        days = [r["days"] for r in self.get("/api/cases?view=all&sort=waiting&limit=100")[1]["items"]]
        self.assertEqual(days, sorted(days, reverse=True))

    def test_ai_recommendation_changes_nothing_and_is_labelled(self):
        before = self.snapshot()
        code, rec = self.post("/api/ai/priority", {"n": 5})
        self.assertEqual(code, 200)
        self.assertEqual(rec["label"], "AI suggestion, not approved")
        self.assertEqual(len(rec["items"]), 5)
        self.assertTrue(all(i["reason"] for i in rec["items"]))
        mine = {c["id"] for c in self.store.cases.values() if c["owner_code"] == "RLO-01"}
        self.assertTrue({i["case_id"] for i in rec["items"]} <= mine)
        self.assertIn(rec["id"], [r["id"] for r in self.store.data["recommendations"]])
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.post(f"/api/ai/priority/{rec['id']}/accept", {})[0], 200)
        self.assertEqual(self.snapshot(), before)

    def test_accept_edit_reject_are_audited_with_reason(self):
        audit = Path(self.store.audit_path)
        start = len(audit.read_text().splitlines()) if audit.exists() else 0
        rec = self.post("/api/ai/priority", {"n": 3})[1]
        self.assertEqual(self.post(f"/api/ai/priority/{rec['id']}/reject", {})[0], 400)
        code, r = self.post(f"/api/ai/priority/{rec['id']}/reject", {"reason": "I know better today"})
        self.assertEqual((code, r["status"]), (200, "Rejected"))
        self.assertEqual(self.post(f"/api/ai/priority/{rec['id']}/accept", {})[0], 400)
        rec2 = self.post("/api/ai/priority", {"n": 3})[1]
        keep = [dict(case_id=i["case_id"], reason=i["reason"]) for i in rec2["items"][:2]]
        code, r = self.post(f"/api/ai/priority/{rec2['id']}/edit", {"reason": "dropped one", "items": keep})
        self.assertEqual((code, r["status"], len(r["final_items"])), (200, "Edited", 2))
        other = next(c["id"] for c in self.store.cases.values() if c["owner_code"] != "RLO-01")
        rec3 = self.post("/api/ai/priority", {"n": 3})[1]
        self.assertEqual(self.post(f"/api/ai/priority/{rec3['id']}/edit", {"reason": "x", "items": [dict(case_id=other)]})[0], 400)
        self.assertEqual(self.post(f"/api/ai/priority/{rec3['id']}/accept", {})[1]["status"], "Accepted")
        lines = [json.loads(x) for x in audit.read_text().splitlines()[start:]]
        acts = [(e["action"], e["detail"]) for e in lines if e["action"].startswith("ai_priority_")]
        self.assertEqual([a for a, _ in acts], ["ai_priority_reject", "ai_priority_edit", "ai_priority_accept"])
        self.assertIn("I know better today", acts[0][1])
        self.assertIn("dropped one", acts[1][1])
        self.assertTrue(self.store.verify_audit())

    def test_other_user_cannot_answer_recommendation(self):
        rec = self.post("/api/ai/priority", {"n": 3})[1]
        with self.assertRaises(PermissionError):
            self.store.resolve_priority(self.store.staff["pam@example.test"], rec["id"], "accept")

    def test_paging_arguments(self):
        code, d = self.get("/api/cases?view=all&limit=7&offset=5")
        self.assertEqual((len(d["items"]), d["total"], d["limit"], d["offset"]), (7, 40, 7, 5))
        self.assertEqual(d["items"][0]["rank"], 6)
        self.assertEqual(self.get("/api/cases?view=all&limit=1000")[1]["limit"], 100)
        self.assertEqual(self.get("/api/cases?view=all")[1]["limit"], 50)
        self.assertEqual(self.get("/api/cases?view=all&limit=abc")[0], 400)
        self.assertEqual(len(self.get("/api/cases?view=all&offset=39")[1]["items"]), 1)

    def test_csv_export_is_not_paged(self):
        code, body, _ = self.call("/api/cases.csv?view=all", cookie=self.cookie)
        self.assertEqual(len(body.strip().splitlines()), 41)

    def test_small_map_returns_every_point(self):
        d = self.get("/api/map")[1]
        self.assertEqual((d["mode"], d["total"], len(d["items"])), ("points", 40, 40))


class ScaleTests(ApiBase):
    @classmethod
    def cases(cls):
        return varied(60000)

    def test_list_pages_and_totals_at_60000(self):
        self.assertEqual(self.get("/api/cases?view=all&limit=1")[1]["total"], 60000)
        seen = []
        for off in (0, 50, 59950):
            d = self.get(f"/api/cases?view=all&limit=50&offset={off}")[1]
            seen.append((len(d["items"]), d["items"][0]["rank"]))
        self.assertEqual(seen, [(50, 1), (50, 51), (50, 59951)])
        self.assertEqual(len(self.get("/api/cases?view=all&limit=50&offset=60000")[1]["items"]), 0)

    def test_map_caps_at_500_and_counts_match_list(self):
        for flt in ("", "&flag=hazard", "&area=North", "&area=East&flag=support", "&stage=Survey+booked"):
            m = self.get(f"/api/map?zoom=7{flt}")[1]
            lst = self.get(f"/api/cases?view=all&limit=1{flt}")[1]
            self.assertLessEqual(len(m["items"]), 500, flt)
            self.assertEqual(m["total"], lst["total"], flt)
            if m["mode"] == "clusters":
                self.assertEqual(sum(i["count"] for i in m["items"]), m["total"], flt)
            else:
                self.assertEqual(len(m["items"]), m["total"], flt)
        whole = self.get("/api/map?zoom=7")[1]
        self.assertEqual((whole["mode"], whole["total"]), ("clusters", 60000))

    def test_map_bbox_and_zoom_in_gives_points(self):
        m = self.get("/api/map?zoom=14&bbox=54.0,-3.0,54.05,-2.95")[1]
        inside = [c for c in self.store.cases.values() if 54.0 <= c["home"]["lat"] <= 54.05 and -3.0 <= c["home"]["lon"] <= -2.95]
        self.assertEqual(m["total"], len(inside))
        self.assertEqual(m["mode"], "points")
        self.assertEqual(self.get("/api/map?bbox=1,2,3")[0], 400)

    def test_filtered_paged_list_timing(self):
        self.get("/api/cases?view=all&limit=1")
        t = time.perf_counter()
        code, d = self.get("/api/cases?view=all&area=North&flag=long&limit=50&offset=100")
        elapsed = time.perf_counter() - t
        print(f"\n[timing] filtered paged list, 60,000 in-memory cases: {elapsed * 1000:.0f} ms ({d['total']} matches)")
        self.assertEqual(code, 200)
        self.assertLess(elapsed, 2.0)
        t = time.perf_counter()
        self.get("/api/map?zoom=7")
        print(f"[timing] map clusters, 60,000 cases: {(time.perf_counter() - t) * 1000:.0f} ms")


if __name__ == "__main__":
    unittest.main()
