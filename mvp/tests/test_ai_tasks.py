import json
import os
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

import test_mvp
from zavaforward_mvp import ai_eval, ai_tasks
from zavaforward_mvp.server import App, make_handler
from zavaforward_mvp.sqlstore import SqlStore
from zavaforward_mvp.store import Store


class TasksMixin:
    """Same behaviour on the JSON store and the SQLite store."""

    def make(self, tmp):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = self.make(self.tmp.name)
        self.sam, self.pam = test_mvp.DATA["staff"]
        self.store.ai.endpoint = "http://scripted-model.invalid"
        self.out = {"text": ""}
        self.store.ai._chat = lambda *a, **k: self.out["text"]

    def tearDown(self):
        self.tmp.cleanup()

    def records(self):
        return [r for r in self.store.data["recommendations"] if r.get("kind") == "ai_task"]

    def test_cited_summary_is_verified_but_not_approved(self):
        self.out["text"] = "- Contacting resident [[Stage: Contacting resident]]\n- Waiting [[Days in stage: 10]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        self.assertTrue(r["verified"])
        self.assertEqual(r["approval"], "Not reviewed")
        self.assertNotIn("[[", r["text"])
        self.assertEqual(r["citations"], ["Stage: Contacting resident", "Days in stage: 10"])

    def test_unresolved_or_missing_citation_is_unverified(self):
        for text in ("Dear Pat. [[Case history 2031-01-01]]", "Dear Pat, we will visit."):
            self.out["text"] = text
            r = self.store.ai_run(self.sam, "ZF-1", "message")
            self.assertFalse(r["verified"])
            self.assertIn("Unverified", r["label"])

    def test_uncited_summary_bullets_are_dropped(self):
        self.out["text"] = "- Real [[Stage: Contacting resident]]\n- Made up\n- Wrong [[Stage: Survey booked]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        self.assertEqual(r["dropped_uncited"], 2)
        self.assertNotIn("Made up", r["text"])
        self.assertTrue(r["verified"])

    def test_workflow_only_flag_and_env_never_call_the_model(self):
        calls = []
        self.store.ai._chat = lambda *a, **k: calls.append(1) or "x"
        r = self.store.ai_run(self.sam, "ZF-1", "message", mode="workflow")
        with mock.patch.dict(os.environ, {"ZF_AI": "off"}):
            b = self.store.briefing(self.sam)
            p = self.store.ai_priority(self.sam, 3)
        self.assertEqual(calls, [])
        self.assertEqual((r["source"], r["mode"]), ("template", "workflow-only"))
        self.assertEqual(b["mode"], "workflow-only")
        self.assertEqual(p["mode"], "workflow-only")
        self.assertTrue(r["verified"] and b["verified"])

    def test_comparison_record_for_every_task_and_review_roundtrip(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        rec = next(x for x in self.records() if x["id"] == r["record_id"])
        self.assertEqual(rec["case_ids"], ["ZF-1"])
        self.assertTrue(rec["ai_output"] and rec["workflow_output"])
        self.assertIsNone(rec["fallback_reason"])
        self.store.briefing(self.sam)
        self.store.funding_draft(self.pam, "ZF-1")
        self.assertGreaterEqual({x["task"] for x in self.records()}, {"summary", "briefing", "funding_draft"})
        with self.assertRaises(ValueError):
            self.store.review_ai(self.sam, r["record_id"], "reject", "")
        with self.assertRaises(PermissionError):
            self.store.review_ai(self.pam, r["record_id"], "accept")
        self.store.review_ai(self.sam, r["record_id"], "edit", "too stiff", "My own wording")
        with self.assertRaises(ValueError):
            self.store.review_ai(self.sam, r["record_id"], "accept")
        rep = self.store.ai_live_report()
        self.assertEqual(rep["tasks"]["summary"]["Edited"], 1)
        self.assertEqual(rep["reviewer_reasons"][0]["reason"], "too stiff")
        self.assertTrue(self.store.verify_audit())

    def test_failed_model_records_the_reason_and_falls_back(self):
        def boom(*a, **k):
            raise OSError("down")
        self.store.ai._chat = boom
        r = self.store.ai_run(self.sam, "ZF-1", "message")
        rec = next(x for x in self.records() if x["id"] == r["record_id"])
        self.assertEqual(r["source"], "template")
        self.assertIn("OSError", rec["fallback_reason"])

    def test_records_do_not_disturb_the_priority_flow_and_persist(self):
        self.out["text"] = json.dumps([dict(case_id="ZF-4", reason="Open safety issue", cites=["Open safety issues: 1"])])
        self.store.ai_run(self.sam, "ZF-1", "message")
        rec = self.store.ai_priority(self.sam, 1)
        self.assertEqual(self.store.latest_priority(self.sam)["id"], rec["id"])
        self.assertEqual(rec["source"], "ai")
        with self.assertRaises(KeyError):
            self.store.resolve_priority(self.sam, self.records()[0]["id"], "accept")
        self.store.resolve_priority(self.sam, rec["id"], "reject", "no")
        again = self.make_again()
        self.assertTrue(any(x.get("kind") == "ai_task" for x in again.data["recommendations"]))
        self.assertEqual(again.latest_priority(self.sam)["status"], "Rejected")

    def test_priority_critical_miss_falls_back(self):
        self.out["text"] = json.dumps([dict(case_id="ZF-1", reason="Oldest", cites=["Days in stage: 10"])])
        rec = self.store.ai_priority(self.sam, 1)
        self.assertEqual(rec["source"], "template")
        self.assertEqual([i["case_id"] for i in rec["items"]], ["ZF-4"])
        self.assertTrue(rec["workflow_items"] and rec["fallback_reason"])

    def test_report_for_users_is_not_shared_across_reviewers(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        with self.assertRaises(PermissionError):
            self.store.review_ai(self.pam, r["record_id"], "reject", "x")


class JsonTasks(TasksMixin, unittest.TestCase):
    def make(self, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        self.path = str(p)
        return Store(self.path, os.path.join(tmp, "live.json"), os.path.join(tmp, "audit.jsonl"))

    def make_again(self):
        return Store(self.path, os.path.join(self.tmp.name, "live.json"), os.path.join(self.tmp.name, "audit.jsonl"))


class SqlTasks(TasksMixin, unittest.TestCase):
    def make(self, tmp):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        self.path, self.db = str(p), os.path.join(tmp, "pw.sqlite")
        return SqlStore(self.path, self.db)

    def make_again(self):
        return SqlStore(self.path, self.db)


class NegativeControls(unittest.TestCase):
    def test_harness_fails_when_citations_are_not_checked(self):
        with mock.patch.object(ai_tasks, "resolve", lambda *a, **k: True):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        text = " ".join(f for r in rep["results"] for f in r["failures"])
        self.assertIn("citation does not exist", text)
        self.assertIn("Unverified", text)

    def test_harness_fails_on_a_critical_miss(self):
        with mock.patch.object(ai_tasks, "critical_misses", lambda *a, **k: []):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertIn("critical miss", " ".join(f for r in rep["results"] for f in r["failures"]))

    def test_harness_fails_when_workflow_only_still_calls_the_model(self):
        real = ai_tasks.workflow_only
        with mock.patch.object(ai_tasks, "workflow_only", lambda mode=None: False):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])
        self.assertIn("workflow-only", " ".join(f for r in rep["results"] for f in r["failures"]))
        self.assertTrue(real("workflow"))

    def test_harness_fails_when_comparison_record_is_missing(self):
        with mock.patch.object(ai_tasks, "add_record", lambda store, user, **f: dict(id="x", **f)):
            rep = ai_eval.run_eval()
        self.assertFalse(rep["passed"])

    def test_spearman(self):
        self.assertEqual(ai_eval.spearman(["a", "b", "c"], ["a", "b", "c"]), 1.0)
        self.assertEqual(ai_eval.spearman(["a", "b", "c"], ["c", "b", "a"]), -1.0)
        self.assertIsNone(ai_eval.spearman(["a"], ["a"]))

    def test_report_has_every_measure(self):
        s = ai_eval.run_eval()["summary"]
        self.assertEqual(s["critical_misses"], 0)
        self.assertEqual(s["citation_validity"], 1.0)
        for key in ("mean_overlap", "mean_spearman", "latency_ms", "models", "prompt_versions", "reviewer", "variation", "added_value"):
            self.assertIn(key, s)
        self.assertTrue(any(v["distinct_orders"] > 1 for v in s["variation"]))
        self.assertGreater(s["added_value"]["ai_minus_deterministic"], 0)
        self.assertEqual(sum(s["reviewer"]["counts"].values()), 10)


class Endpoints(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        self.store = Store(str(p), os.path.join(self.tmp.name, "live.json"), os.path.join(self.tmp.name, "audit.jsonl"))
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, "zf-test")))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def call(self, email, path, body=None):
        login = urllib.request.Request(self.base + "/api/login", json.dumps(dict(email=email, password="zf-test")).encode())
        ck = urllib.request.urlopen(login).headers["Set-Cookie"].split(";")[0]
        req = urllib.request.Request(self.base + path, json.dumps(body).encode() if body is not None else None, headers={"Cookie": ck})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_report_is_manager_only(self):
        self.assertEqual(self.call("sam@example.test", "/api/ai/report")[0], 403)
        code, body = self.call("pam@example.test", "/api/ai/report")
        self.assertEqual(code, 200)
        self.assertTrue(body["evaluation"]["passed"])
        self.assertIn("tasks", body["live"])

    def test_mode_flag_and_review_over_http(self):
        code, r = self.call("sam@example.test", "/api/cases/ZF-1/ai", {"task": "message", "mode": "workflow"})
        self.assertEqual((code, r["mode"], r["approval"]), (200, "workflow-only", "Not reviewed"))
        code, rec = self.call("sam@example.test", f"/api/ai/review/{r['record_id']}/reject", {"reason": "not needed"})
        self.assertEqual((code, rec["status"]), (200, "Rejected"))
        self.assertEqual(self.call("sam@example.test", f"/api/ai/review/{r['record_id']}/reject", {"reason": "x"})[0], 400)


if __name__ == "__main__":
    unittest.main()
