import copy
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import test_mvp
from zava_forward.core import projection
from zava_forward.api.server import App, make_handler
from zava_forward.core.store import Store

REASON = "SEEDED-REASON-dementia-and-hearing-loss"
PHONE = "01999 888777"
RESIDENT = "Quentin Residentname"
ROLES = list(projection.STAFF_ROLES) + [projection.CONTRACTOR]


class QualityMatrix(unittest.TestCase):
    """Actual authenticated routes, separate fictional SQLite state per scenario."""

    def setUp(self):
        import dataset
        from test_quality_procurement import STAFF
        from zava_forward.core.sqlstore import SqlStore

        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        data["staff"] = copy.deepcopy(STAFF)
        data["cases"][1]["contractor"]["name"] = "Other Ltd"
        dataset.supplied_resident_fixture(data["cases"][0])
        path = Path(self.tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, "SYN-quality-test")))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.cookies = {}
        with urllib.request.urlopen(self.base + "/healthz") as response:
            self.assertEqual(response.status, 200)

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def call(self, actor, action, body=None):
        if actor not in self.cookies:
            request = urllib.request.Request(self.base + "/api/login", json.dumps(
                dict(email=f"{actor}@example.test", password="SYN-quality-test")).encode())
            with urllib.request.urlopen(request) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        path = action if action.startswith("/") else f"/api/cases/ZF-1/quality-{action}"
        request = urllib.request.Request(self.base + path, None if body is None else json.dumps(body).encode(),
                                         headers={"Cookie": self.cookies[actor]})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def evidence(self):
        from test_quality_procurement import EVIDENCE
        return dict(measure="Loft insulation", submitted_by="SYN installer", source="Installer",
                    items=EVIDENCE, context_revision=1)

    def test_quality_http_controls(self):
        self.assertEqual(self.call("sam", "submit", self.evidence())[0], 200)
        before, audit = copy.deepcopy(self.store.cases["ZF-1"]), list(self.store.audit_entries())
        for action in ("submit", "accept", "return", "fix", "reinspect", "handover", "aftercare"):
            self.assertEqual(self.call("kim", action, dict(self.evidence(), index=0, role="Quality Inspector"))[0], 403)
        self.assertEqual(self.call("kim", "/api/cases/ZF-2")[0], 404)
        self.assertEqual(self.call("kim", "/api/cases/ZF-1/finance", dict(action="payment_status", id="INV-1", status="Paid outside this system"))[0], 403)
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(self.call("sam", "accept", dict(index=0, role="Quality Inspector", email="quil@example.test"))[0], 403)
        self.assertEqual(self.call("quin", "return", dict(index=0, reason="SYN", defect="SYN gap", owner="SYN team"))[0], 200)
        self.assertEqual(self.call("sam", "fix", dict(index=0, fixed_by="SYN fitter"))[0], 400)
        self.assertEqual(self.call("sam", "fix", dict(index=0, fixed_by="SYN fitter", note="SYN photo v2"))[0], 200)
        self.assertEqual(self.call("sam", "reinspect", dict(index=0, result="pass"))[0], 403)
        self.assertEqual(self.call("quil", "reinspect", dict(index=0, result="pass", note="SYN independent visit"))[0], 200)
        self.assertEqual(self.store.cases["ZF-1"]["quality"][0]["state"], "Accepted")
        for key in ("finance", "grants", "funding"):
            self.assertEqual(self.store.cases["ZF-1"].get(key), before.get(key))

    def test_quality_http_replacement(self):
        self.assertEqual(self.call("sam", "submit", self.evidence())[0], 200)
        self.assertEqual(self.call("quil", "accept", dict(index=0))[0], 200)
        self.assertEqual(self.call("sam", "handover", dict(index=0, note="SYN guide", resident_told=True))[0], 200)
        before = copy.deepcopy(self.store.cases["ZF-1"])
        self.assertEqual(self.call("sam", "submit", dict(self.evidence(), context_revision=99))[0], 400)
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(self.call("sam", "submit", self.evidence())[0], 200)
        records = self.store.cases["ZF-1"]["quality"]
        self.assertEqual([r["state"] for r in records], ["Superseded", "Submitted"])
        self.assertEqual(records[0]["prior_acceptance"]["handover"]["note"], "SYN guide")
        self.assertEqual(self.call("sam", "aftercare", dict(index=0, note="SYN obsolete"))[0], 400)
        self.assertEqual(self.call("sam", "handover", dict(index=1, note="SYN", resident_told=True))[0], 400)
        self.assertEqual(self.call("quil", "accept", dict(index=1))[0], 200)
        self.assertEqual(self.call("sam", "handover", dict(index=1, note="SYN fresh guide", resident_told=True))[0], 200)
        for key in ("finance", "grants", "funding"):
            self.assertEqual(self.store.cases["ZF-1"].get(key), before.get(key))
        self.assertTrue(self.store.verify_audit())

    def test_quality_http_committed_outcome(self):
        self.assertEqual(self.call("sam", "submit", self.evidence())[0], 200)
        self.assertEqual(self.call("quil", "/api/me")[0], 200)
        save = self.store.save
        db = self.store.db

        class RefreshFault:
            committed = False
            failed = False

            def execute(self, sql, args=()):
                if self.committed and not self.failed and sql.startswith("SELECT value FROM meta"):
                    self.failed = True
                    raise OSError("SYN committed refresh read")
                result = db.execute(sql, args)
                if sql == "COMMIT":
                    self.committed = True
                return result

            def __getattr__(self, name):
                return getattr(db, name)

        def fail_refresh():
            db.execute("UPDATE meta SET value=value+1 WHERE key='seq'")
            save()

        with patch.object(self.store, "db", RefreshFault()), patch.object(self.store, "save", side_effect=fail_refresh):
            with self.assertLogs("zava_forward.core.quality", level="ERROR"):
                status, result = self.call("quil", "accept", dict(index=0))
        self.assertEqual(status, 503)
        self.assertEqual(result["outcome"], "committed")
        self.assertIn("Reload", result["error"])
        self.assertEqual(self.call("quil", "/api/cases/ZF-1")[1]["quality"][0]["state"], "Accepted")
        self.assertEqual([e["action"] for e in self.store.audit_entries()].count("quality_accepted"), 1)
        self.assertTrue(self.store.verify_audit())


def build():
    d = copy.deepcopy(test_mvp.DATA)
    d["staff"] = [dict(code=f"U{i}", name=f"User {i}", email=f"u{i}@example.test", role=r) for i, r in enumerate(ROLES)]
    d["staff"][-1]["contractor"] = "Test Ltd"
    d["staff"].append(dict(code="U99", name="Other Contractor", email="other@example.test", role=projection.CONTRACTOR, contractor="Other Ltd"))
    for c in d["cases"]:
        c["owner_code"] = "U1"
        c["owner"] = "User 1"
    c = d["cases"][0]
    c["resident"].update(adjustment=REASON, priority_support=True, phone=PHONE, name=RESIDENT, email="q@example.test")
    c["contacts"].append(dict(at="2026-01-01T10:00", purpose="Update", channel="Phone", direction="Outbound", outcome="Spoke",
                              note="private note", by="User 1"))
    c["appointments"].append(dict(type="Survey", date="2099-01-01", slot="AM", outcome="Booked", note="private appointment note",
                                  who="Test Ltd", person="Kim Builder"))
    d["cases"][1]["contractor"]["name"] = "Other Ltd"
    return d


NEW_POSTS = [("/api/cases/ZF-1/quality-" + a, {"index": 0, "measure": "Loft insulation"}) for a in
             ("submit", "accept", "return", "fix", "reinspect", "handover", "aftercare")] + [
    ("/api/packages", {"name": "P"}), ("/api/packages/PKG-001/rescope", {}), ("/api/packages/PKG-001/capacity", {}),
    ("/api/workorders", {"package": "PKG-001", "case_id": "ZF-1"})] + [
    (f"/api/workorders/WO-0001/{a}", {}) for a in ("reissue", "appointment", "complete", "correct", "withdraw")]


class Matrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        p = Path(cls.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(build()))
        cls.store = Store(str(p))
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(cls.store, "zf-test")))
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmp.cleanup()

    def session(self, email):
        req = urllib.request.Request(self.base + "/api/login", json.dumps(dict(email=email, password="zf-test")).encode())
        return urllib.request.urlopen(req).headers["Set-Cookie"].split(";")[0]

    def call(self, ck, path, body=None):
        req = urllib.request.Request(self.base + path, json.dumps(body).encode() if body is not None else None, headers={"Cookie": ck})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()

    GETS = ["/api/me", "/api/cases?view=all", "/api/cases?view=mine", "/api/cases?view=all&sort=name", "/api/cases?view=all&q=Test",
            "/api/cases?view=all&flag=support", "/api/cases.csv?view=all", "/api/cases/ZF-1", "/api/cases/ZF-2", "/api/ranking/policy",
            "/api/ai/priority", "/api/facets", "/api/stats", "/api/map", "/api/visits?view=all", "/api/funding", "/api/briefing",
            "/api/audit-check", "/api/docs/ZF-1/none", "/api/nothing", "/api/packages", "/api/workorders", "/api/workorders?case=ZF-1",
            "/api/checklists", "/api/finance"]
    POSTS = [("/api/ai/priority", {"n": 3}), ("/api/cases/ZF-1/ai", {"task": "summary"}), ("/api/cases/ZF-1/ai", {"task": "message"}),
             ("/api/cases/ZF-1/draft", {"kind": "update"}), ("/api/cases/ZF-1/funding-draft", {}), ("/api/import-check", {"text": "name\\nx"})] + NEW_POSTS + [
             ("/api/cases/ZF-1/finance", {"action": "budget_propose", "amount": 5}), ("/api/cases/ZF-1/grant", {"action": "grant_open", "scheme": "S", "source": "s"}),
             ("/api/cases/ZF-1/technical", {"action": "design_submit", "note": "n"}), ("/api/cases/ZF-1/resident", {"action": "decision_record"})]

    def test_no_role_other_than_those_with_a_need_sees_the_reason(self):
        for role in ROLES:
            ck = self.session(next(s["email"] for s in self.store.data["staff"] if s["role"] == role))
            seen = []
            for path in self.GETS:
                seen.append((path,) + self.call(ck, path))
            for path, body in self.POSTS:
                seen.append((path,) + self.call(ck, path, body))
            leaked = [p for p, _, text in seen if REASON in text]
            if role in projection.DEFAULT_REASON_ROLES:
                self.assertTrue(any(REASON in t for p, _, t in seen if p == "/api/cases/ZF-1"), role)
            else:
                self.assertEqual(leaked, [], role)

    def test_contractor_sees_only_notice_and_named_contact(self):
        ck = self.session("u7@example.test")
        code, text = self.call(ck, "/api/cases/ZF-1")
        self.assertEqual(code, 200)
        d = json.loads(text)
        self.assertEqual(set(d), {"id", "stage", "status", "measures", "needs_notice", "named_contact", "home", "contractor", "appointments", "resident_readiness"})
        self.assertTrue(d["needs_notice"])
        self.assertEqual(d["named_contact"], "User 1")
        self.assertEqual(set(d["appointments"][0]), {"type", "date", "slot", "outcome"})
        for forbidden in (REASON, PHONE, RESIDENT, "private note", "private appointment note", "q@example.test", "adjustment", "priority_support"):
            self.assertNotIn(forbidden, text)
        code, text = self.call(ck, "/api/cases?view=all")
        items = json.loads(text)["items"]
        self.assertEqual({i["id"] for i in items}, {"ZF-1", "ZF-3", "ZF-4", "ZF-5"})
        for i in items:
            self.assertLessEqual(set(i), set(projection.SUMMARY_FIELDS))
        for forbidden in (REASON, PHONE, RESIDENT):
            self.assertNotIn(forbidden, text)

    def test_contractor_scope_search_and_denials(self):
        ck = self.session("u7@example.test")
        self.assertEqual(self.call(ck, "/api/cases/ZF-2")[0], 404)
        self.assertEqual(json.loads(self.call(ck, f"/api/cases?view=all&q=Quentin")[1])["total"], 0)
        self.assertEqual(json.loads(self.call(ck, "/api/cases?view=all&q=1%20Test%20Road")[1])["total"], 4)
        for path in ("/api/stats", "/api/map", "/api/facets", "/api/funding", "/api/visits", "/api/briefing", "/api/cases.csv?view=all",
                     "/api/audit-check", "/api/ai/priority", "/api/docs/ZF-1/x", "/api/ranking/policy", "/api/packages", "/api/checklists", "/api/finance"):
            self.assertEqual(self.call(ck, path)[0], 403, path)
        for path, body in [("/api/ai/priority", {}), ("/api/cases/ZF-1/call", {"outcome": "x"}), ("/api/cases/ZF-1/handover", {"to": "x"})] + NEW_POSTS + [
                           ("/api/cases/ZF-1/finance", {"action": "budget_propose", "amount": 5}), ("/api/cases/ZF-1/grant", {"action": "grant_open", "scheme": "S", "source": "s"}),
             ("/api/cases/ZF-1/technical", {"action": "design_submit", "note": "n"}), ("/api/cases/ZF-1/resident", {"action": "decision_record"})]:
            self.assertEqual(self.call(ck, path, body)[0], 403, path)
        me = json.loads(self.call(ck, "/api/me")[1])
        self.assertEqual(me["staff"], [])

    def test_other_contractor_sees_only_theirs(self):
        ck = self.session("other@example.test")
        self.assertEqual({i["id"] for i in json.loads(self.call(ck, "/api/cases?view=all")[1])["items"]}, {"ZF-2"})

    FINANCE_ROLES = ("Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer")

    def test_finance_and_resident_endpoints_for_every_role(self):
        for role in ROLES:
            ck = self.session(next(s["email"] for s in self.store.data["staff"] if s["role"] == role))
            code, text = self.call(ck, "/api/finance")
            self.assertEqual(code, 200 if role in self.FINANCE_ROLES else 403, role)
            for act, body in (("finance", {"action": "budget_propose", "amount": 5}), ("grant", {"action": "grant_open", "scheme": "S", "source": "s"})):
                code, _ = self.call(ck, f"/api/cases/ZF-3/{act}", body)
                self.assertEqual(code, 200 if role in self.FINANCE_ROLES else 403, (role, act))
            code, _ = self.call(ck, "/api/cases/ZF-3/finance", {"action": "budget_propose", "amount": 5, "case_ids": ["ZF-3"]})
            self.assertEqual(code, 403, role)
            code, text = self.call(ck, "/api/cases/ZF-3")
            if role == projection.CONTRACTOR:
                self.assertNotIn("budget", text)
            elif role not in self.FINANCE_ROLES:
                self.assertNotIn("finance", json.loads(text))
                self.assertNotIn("grants", json.loads(text))
            code, _ = self.call(ck, "/api/cases/ZF-3/technical", {"action": "design_submit", "note": "n"})
            self.assertIn(code, (403,) if role == projection.CONTRACTOR else (200, 400, 403), role)
            code, _ = self.call(ck, "/api/cases/ZF-3/resident", {"action": "decision_record"})
            self.assertEqual(code, 400 if role in projection.RESIDENT_RECORD_ROLES else 403, role)

    def test_integrated_case_actions_deny_contractors_and_unknown_roles(self):
        posts = [
            ("/api/cases/ZF-1/resident", {"action": action})
            for action in ("scope_record", "decision_record", "representative_record",
                           "safe_contact_record", "disclosure_check", "service_open")
        ] + [
            ("/api/cases/ZF-1/stock-reconciliation", {}),
            ("/api/cases/ZF-1/stock-query-event", {"action": "resolve", "query_id": "SQ-1"}),
            ("/api/cases/ZF-1/technical", {"action": "signoff_give", "type": "design"}),
        ]
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        for email in ("u7@example.test", "u0@example.test"):
            if email == "u0@example.test":
                self.store.staff[email]["role"] = "Mystery"
            try:
                ck = self.session(email)
                for path, body in posts:
                    self.assertEqual(self.call(ck, path, body)[0], 403, (email, path, body))
            finally:
                self.store.staff["u0@example.test"]["role"] = ROLES[0]
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_unknown_role_is_denied(self):
        self.store.staff["u0@example.test"]["role"] = "Mystery"
        try:
            ck = self.session("u0@example.test")
            self.assertEqual(self.call(ck, "/api/cases")[0], 403)
        finally:
            self.store.staff["u0@example.test"]["role"] = ROLES[0]

    def test_ai_prompt_never_carries_reason_without_need(self):
        prompts = []
        self.store.ai.endpoint = "http://x"
        import release_support
        release_support.install(self.store)
        self.store.ai._chat = lambda *a, **k: prompts.append(json.dumps(a) + json.dumps(k)) or "Draft."
        try:
            coordinator = dict(next(s for s in self.store.data["staff"] if s["role"] == "Retrofit Coordinator"), code="U1")
            liaison = next(s for s in self.store.data["staff"] if s["role"] == "Resident Liaison Officer")
            self.store.ai_run(coordinator, "ZF-1", "summary")
            self.store.ai_priority(coordinator, 3)
            self.store.funding_draft(coordinator, "ZF-1")
            self.assertTrue(prompts)
            self.assertFalse([p for p in prompts if REASON in p])
            prompts.clear()
            self.store.ai_run(liaison, "ZF-1", "summary")
            self.assertTrue([p for p in prompts if REASON in p])
        finally:
            self.store.ai.endpoint = ""

    def test_reason_roles_can_be_configured(self):
        import os
        os.environ["ZF_REASON_ROLES"] = "Quality Inspector"
        try:
            self.assertTrue(projection.can_see_reason(dict(role="Quality Inspector")))
            self.assertFalse(projection.can_see_reason(dict(role="Resident Liaison Officer")))
        finally:
            del os.environ["ZF_REASON_ROLES"]

    def test_new_endpoints_for_every_role(self):
        mgr = {s["role"]: s for s in self.store.data["staff"]}["Retrofit Programme Manager"]
        pid = self.store.create_package(mgr, "Wave", "2026-01-01", "2099-12-31", "Loft", "CALL-1", "SYN-1")
        order_case = copy.deepcopy(self.store.cases["ZF-1"])
        order_case.update(id="ZF-ROLE-ORDER", hazards=[])
        self.store.cases[order_case["id"]] = order_case
        from dataset import RESIDENT_BINDINGS, supplied_contract_fixture, supplied_resident_fixture
        supplied_resident_fixture(order_case)
        supplied_resident_fixture(self.store.cases["ZF-2"])
        for contractor in ("Test Ltd", "Other Ltd"):
            details = supplied_contract_fixture(self.store, pid, mgr, contractor)
            self.store.set_capacity(mgr, pid, contractor, 2, 2, "SYN signed commitment", details)
        w1 = self.store.issue_work_order(mgr, pid, order_case["id"], resident_bindings=RESIDENT_BINDINGS)
        w2 = self.store.issue_work_order(mgr, pid, "ZF-2", resident_bindings=RESIDENT_BINDINGS)
        for role in ROLES:
            ck = self.session(next(s["email"] for s in self.store.data["staff"] if s["role"] == role))
            codes = {p: self.call(ck, p)[0] for p in ("/api/packages", "/api/workorders", "/api/checklists")}
            if role == projection.CONTRACTOR:
                self.assertEqual(codes, {"/api/packages": 403, "/api/workorders": 200, "/api/checklists": 403})
            else:
                self.assertEqual(set(codes.values()), {200}, role)
            for path, body in NEW_POSTS:
                if path == "/api/workorders":
                    body = dict(body, case_id=order_case["id"])
                code, text = self.call(ck, path, body)
                self.assertNotIn(code, (200, 500) if role in (projection.CONTRACTOR, "Mystery") else (500,), (role, path))
                if role == projection.CONTRACTOR:
                    self.assertEqual(code, 403, path)
                self.assertNotIn(REASON, text)
        ck = self.session("u7@example.test")
        orders = json.loads(self.call(ck, "/api/workorders")[1])
        self.assertEqual([o["id"] for o in orders], [w1])
        self.assertNotIn(w2, self.call(ck, "/api/workorders")[1])
        self.assertTrue(orders[0]["needs_notice"])
        self.assertNotIn(REASON, json.dumps(orders))
        self.assertEqual(self.call(ck, "/api/workorders?case=ZF-2")[1], "[]")
        for role, ok in (("Retrofit Coordinator", False), ("Quality Inspector", False), ("Retrofit Programme Manager", True)):
            ck = self.session(next(s["email"] for s in self.store.data["staff"] if s["role"] == role))
            self.assertEqual(self.call(ck, f"/api/workorders/{w1}/withdraw", {"reason": "test"})[0] == 200, ok, role)
