import copy
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

import release_support

import test_mvp
from zava_forward.core import ai_tasks, identity, projection
from zava_forward.core.ai import Ai
from zava_forward.agents import ai_eval
from zava_forward.api.server import App, make_handler
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.workflows import MANAGER_ROLES


class TasksMixin:
    """Same behaviour on the JSON store and the SQLite store."""

    def make(self, tmp, data=None):
        raise NotImplementedError

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = self.make(self.tmp.name)
        self.sam, self.pam = test_mvp.DATA["staff"]
        self.store.ai.endpoint = "http://scripted-model.invalid"
        self.out = {"text": ""}
        self.store.ai._chat = lambda *a, **k: self.out["text"]
        release_support.install(self.store)

    def tearDown(self):
        self.tmp.cleanup()

    def records(self):
        return [r for r in self.store.data["recommendations"] if r.get("kind") == "ai_task"]

    def test_briefing_statement_sources_and_cached_generation_time(self):
        from datetime import datetime

        result = self.store.briefing(self.sam, mode="workflow")
        generated = datetime.fromisoformat(result["generated_at"])
        self.assertIsNotNone(generated.utcoffset())
        self.assertIs(self.store.briefing(self.sam, mode="workflow"), result)
        self.assertEqual(self.store.briefing(self.sam, mode="workflow")["generated_at"],
                         result["generated_at"])
        expected = [c["id"] for c in self.store.list_cases(self.sam)][:3]
        self.assertEqual(result["source_case_ids"],
                         [c["id"] for c in self.store.list_cases(self.sam)][:8])
        self.assertEqual(len(result["statements"]), len(expected))
        for statement, cid in zip(result["statements"], expected):
            self.assertIn(statement["text"], result["text"])
            self.assertEqual(statement["unresolved"], [])
            self.assertTrue(all(cite.startswith(cid + ": ") for cite in statement["citations"]))
        for c in self.store.cases.values():
            c["closed"] = True
        self.store.save()
        empty = self.store.briefing(self.sam, mode="workflow")
        self.assertEqual(empty["statements"],
                         [dict(text=empty["text"], citations=[], unresolved=[])])

    def test_statement_references_preserve_valid_unresolved_and_dropped_output(self):
        sources = {"ZF-1": ["Stage: Survey booked"]}
        raw = ("Check survey [[ZF-1: Stage: Survey booked]]. "
               "Check funding. [[ZF-1: Funding: invented]]")
        statements = ai_tasks.statement_sources(raw, sources)
        self.assertEqual([s["text"] for s in statements], ["Check survey.", "Check funding."])
        self.assertEqual(statements[0]["citations"], ["ZF-1: Stage: Survey booked"])
        self.assertEqual(statements[1]["unresolved"], ["ZF-1: Funding: invented"])
        filtered = ai_tasks.statement_sources(
            "- Keep [[ZF-1: Stage: Survey booked]].\n- Remove invented.", sources, bullets=True)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["text"], "- Keep.")
        rejected_line = "- One valid [[ZF-1: Stage: Survey booked]]. Invalid [[invented]]."
        self.assertEqual(ai_tasks.statement_sources(rejected_line, sources, bullets=True), [])

    def test_rules_briefing_keeps_published_snapshot_during_case_change(self):
        run = self.store.ai.run
        before = copy.deepcopy(self.store._case("ZF-1"))

        def change_case(*args, **kwargs):
            with self.store.lock:
                case = self.store._case("ZF-1")
                case.update(stage="Design in progress", days_in_stage=1)
                self.store.save()
            return run(*args, **kwargs)

        with mock.patch.object(self.store.ai, "run", side_effect=change_case):
            result = self.store.briefing(self.sam, mode="workflow")
        record = next(r for r in self.records() if r["id"] == result["record_id"])
        self.assertEqual(record["shown_output"], result["text"])
        self.assertEqual(record["workflow_output"], result["text"])
        self.assertEqual(record["citations"], result["citations"])
        self.assertTrue(result["verified"])
        for statement in result["statements"]:
            self.assertIn(statement["text"], record["shown_output"])
            self.assertTrue(all(cite in record["citations"] for cite in statement["citations"]))
        statement = next(s for s in result["statements"]
                         if any(c.startswith("ZF-1: ") for c in s["citations"]))
        self.assertIn(f"ZF-1: Stage: {before['stage']}", statement["citations"])
        self.assertIn(f"ZF-1: Days in stage: {before['days_in_stage']}",
                      statement["citations"])
        self.assertNotIn("design in progress", statement["text"])

    def test_quarantined_output_never_exposes_abandoned_ai_statement_sources(self):
        from unittest.mock import patch

        case = self.store._case("ZF-1")
        raw = dict(source="ai", text="Abandoned AI [[ZF-1: Stage: Survey booked]].",
                   model="synthetic", reason=None)
        with patch.object(self.store, "continuity_publish",
                          side_effect=lambda task, epoch, source, publish: publish(True)):
            result = ai_tasks.finish(
                self.store, self.sam, "briefing", ["ZF-1"], raw, "Manual summary.",
                {"ZF-1": ai_tasks.source_labels(case)}, [], epoch0=0)
        self.assertEqual(result["source"], "template")
        self.assertEqual(result["approval"], "Quarantined")
        self.assertEqual(result["statements"],
                         [dict(text="Manual summary.", citations=[], unresolved=[])])

    def test_unbound_entra_briefing_is_empty_assignment_not_empty_programme(self):
        user = identity.principal(
            "11111111-2222-3333-4444-555555555555",
            "aaaaaaaa-0000-0000-0000-000000000001",
            self.sam["role"], email=self.sam["email"],
        )
        user = identity.bind(self.store, user)
        self.assertNotEqual(user["code"], self.sam["code"])
        self.assertEqual(self.store.page_cases(user)["total"], 0)
        self.assertGreater(self.store.page_cases(user, "all")["total"], 0)
        briefing = self.store.briefing(user, mode="workflow")
        self.assertEqual(briefing["text"],
                         "No open cases are assigned to you. This does not mean the programme has no work.")
        record = next(r for r in self.records() if r["id"] == briefing["record_id"])
        self.assertEqual(record["case_ids"], [])

    def test_bound_entra_briefing_uses_seeded_workload_code_and_excludes_closed(self):
        tenant = "11111111-2222-3333-4444-555555555555"
        oid = "aaaaaaaa-0000-0000-0000-000000000001"
        row = dict(self.sam, tid=tenant, oid=oid)
        if hasattr(self.store, "db"):
            self.store.db.execute("UPDATE staff SET body=? WHERE email=?", (json.dumps(row), self.sam["email"]))
        else:
            self.store.staff[self.sam["email"]] = row
        with self.store.lock:
            owned = [c for c in self.store.cases.values() if c["owner_code"] == self.sam["code"]]
            self.store._case(owned[0]["id"])["closed"] = True
            self.store.save()
        user = identity.bind(self.store, identity.principal(tenant, oid, self.sam["role"]))
        self.assertEqual(user["code"], self.sam["code"])
        expected = {c["id"] for c in owned if not c["closed"]}
        self.assertTrue(expected)
        self.assertEqual({c["id"] for c in self.store.list_cases(user)}, expected)
        briefing = self.store.briefing(user, mode="workflow")
        record = next(r for r in self.records() if r["id"] == briefing["record_id"])
        self.assertEqual(set(record["case_ids"]), expected)
        self.assertNotIn(owned[0]["id"], record["case_ids"])

    def test_existing_managers_brief_all_permitted_open_cases_without_assigning(self):
        with self.store.lock:
            self.store._case("ZF-2")["closed"] = True
            self.store.save()
        before = copy.deepcopy(list(self.store.cases.values()))
        expected = [r["id"] for r in self.store.list_cases(self.pam, "all")]
        self.assertIn("ZF-4", expected)
        self.assertIn("ZF-5", expected)
        for role in MANAGER_ROLES:
            with self.subTest(role=role):
                user = dict(self.pam, role=role)
                assignments = self.store.counts(user)["mine"]
                result = self.store.briefing(user, mode="workflow")
                record = next(r for r in self.records() if r["id"] == result["record_id"])
                self.assertEqual(record["case_ids"], expected)
                self.assertEqual(record["case_ids"][0], "ZF-4")
                self.assertEqual((result["scope"], result["scope_label"]), ("programme", "All programme cases"))
                self.assertEqual((result["case_count"], result["summary_count"]), (4, 3))
                self.assertEqual(self.store.counts(user)["mine"], assignments)
                self.assertEqual({r["id"] for r in self.store.list_cases(user)}, {"ZF-5"})
                self.assertEqual(result["approval"], "Not reviewed")
        self.assertEqual(list(self.store.cases.values()), before)

    def test_other_staff_briefings_stay_assignment_only(self):
        expected = [r["id"] for r in self.store.list_cases(self.sam)]
        for role in projection.STAFF_ROLES:
            if role in MANAGER_ROLES:
                continue
            with self.subTest(role=role):
                result = self.store.briefing(dict(self.sam, role=role), mode="workflow")
                record = next(r for r in self.records() if r["id"] == result["record_id"])
                self.assertEqual(record["case_ids"], expected)
                self.assertNotIn("ZF-5", record["case_ids"])
                self.assertEqual((result["scope"], result["scope_label"]), ("assigned", "My assigned cases"))

    def test_unbound_managers_have_programme_briefing_but_zero_assignments(self):
        for role in MANAGER_ROLES:
            with self.subTest(role=role):
                user = identity.bind(self.store, identity.principal(
                    "11111111-2222-3333-4444-555555555555",
                    "aaaaaaaa-0000-0000-0000-000000000001", role, email=self.pam["email"],
                ))
                self.assertNotEqual(user["code"], self.pam["code"])
                self.assertEqual(self.store.page_cases(user)["total"], 0)
                result = self.store.briefing(user, mode="workflow")
                record = next(r for r in self.records() if r["id"] == result["record_id"])
                self.assertEqual(record["case_ids"], [r["id"] for r in self.store.list_cases(user, "all")])
                self.assertEqual(result["scope_label"], "All programme cases")
                self.assertEqual(self.store.counts(user)["mine"], 0)
                self.assertEqual(self.store.page_cases(user)["total"], 0)

    def test_denied_roles_cannot_dispatch_or_reuse_briefing(self):
        self.store.briefing(self.pam, mode="workflow")
        for role in ("Contractor", "Application Administrator", "Unknown", ""):
            with self.subTest(role=role), mock.patch.object(self.store.ai, "run") as run:
                with self.assertRaises(PermissionError):
                    self.store.briefing(dict(self.pam, role=role), mode="workflow")
                run.assert_not_called()

    def test_permitted_read_controls_full_count_top_eight_facts_and_cache(self):
        data = copy.deepcopy(test_mvp.DATA)
        for c in data["cases"]:
            c["resident"]["name"] = f"SYN Resident {c['id']}"
        for number in range(6, 12):
            c = copy.deepcopy(data["cases"][0])
            c["id"] = f"ZF-{number}"
            c["resident"]["name"] = f"SYN Resident {number}"
            data["cases"].append(c)
        for c in data["cases"]:
            c["building_id"] = "SYN-BRIEFING"
        data["buildings"] = [dict(id="SYN-BRIEFING", name="Synthetic briefing block",
                                 version=1, source="SYN-REGISTER", systems=[],
                                 dependencies=[], holds=[], works=[], costs=[])]
        expanded = Path(self.tmp.name) / "expanded"
        expanded.mkdir()
        if hasattr(self.store, "db"):
            self.store.db.close()
        self.store = self.make(str(expanded), data)
        self.store.ai.endpoint = "http://scripted-model.invalid"
        release_support.install(self.store)
        permitted = sorted(self.store._filtered(self.pam, "all", "", {}),
                           key=lambda c: self.store._ranking()[c["id"]]["rank"])
        with mock.patch.object(self.store, "_filtered", return_value=permitted) as read, \
                mock.patch.object(self.store, "summary", wraps=self.store.summary) as project, \
                mock.patch.object(self.store, "work_context", side_effect=AssertionError("No queue projection")):
            first = self.store.briefing(self.pam, mode="workflow")
            read.assert_called_once_with(self.pam, "all", "", {})
            self.assertEqual(project.call_count, 8)
            version = self.store.version
            self.assertIs(self.store.briefing(self.pam, mode="workflow"), first)
            self.assertEqual(self.store.version, version)
            self.assertEqual(project.call_count, 8)
            read.return_value = permitted[:-1]
            fewer = self.store.briefing(self.pam, mode="workflow")
            self.assertNotEqual(fewer["record_id"], first["record_id"])
            self.assertEqual((first["case_count"], fewer["case_count"]), (11, 10))
            self.assertEqual((first["summary_count"], fewer["summary_count"]), (3, 3))
            self.assertEqual(project.call_count, 16)
            for result in (first, fewer):
                record = next(r for r in self.records() if r["id"] == result["record_id"])
                self.assertEqual(record["case_ids"], [r["id"] for r in permitted[:8]])
                self.assertEqual(record["case_ids"][0], "ZF-4")
                for c in permitted[:3]:
                    self.assertIn(c["resident"]["name"], result["text"])
                for c in permitted[3:8]:
                    self.assertNotIn(c["resident"]["name"], result["text"])
            read.return_value = permitted
            citation = f"SYN [[{permitted[0]['id']}: Days in stage: {permitted[0]['days_in_stage']}]]"
            with mock.patch.object(self.store.ai, "_chat", return_value=citation):
                enabled = self.store.briefing(self.pam)
            self.assertEqual((enabled["source"], enabled["summary_count"]), ("ai", 8))
            with mock.patch.object(self.store.ai, "_chat", side_effect=TimeoutError), \
                    mock.patch.object(self.store, "ai_epoch_current", return_value=False):
                fallback = self.store.briefing(self.pam)
            self.assertEqual((fallback["source"], fallback["summary_count"]), ("template", 3))
            read.return_value = [next(r for r in permitted if r["id"] == "ZF-5")]
            with mock.patch.object(self.store.ai, "_chat", return_value="SYN [[Stage: Contacting resident]]") as chat:
                restricted = self.store.briefing(self.pam)
            prompt = chat.call_args.args[2]
            self.assertIn("ZF-5", prompt)
            self.assertNotIn("ZF-4", prompt)
            record = next(r for r in self.records() if r["id"] == restricted["record_id"])
            self.assertEqual(record["case_ids"], ["ZF-5"])
            self.assertEqual((restricted["case_count"], restricted["summary_count"]), (1, 1))

    def test_briefing_cache_separates_role_actor_and_workflow_mode(self):
        manager = self.store.briefing(self.pam, mode="workflow")
        downgraded = dict(self.pam, role=self.sam["role"])
        personal = self.store.briefing(downgraded, mode="workflow")
        self.assertEqual(personal["scope"], "assigned")
        self.assertNotEqual(personal["record_id"], manager["record_id"])
        record = next(r for r in self.records() if r["id"] == personal["record_id"])
        self.assertEqual(record["case_ids"], ["ZF-5"])
        first_actor = self.store.briefing(self.pam, mode="workflow")
        other_actor = dict(self.pam, email="different@example.test")
        second_actor = self.store.briefing(other_actor, mode="workflow")
        self.assertNotEqual(first_actor["record_id"], second_actor["record_id"])
        record = next(r for r in self.records() if r["id"] == second_actor["record_id"])
        self.assertEqual(record["user"], other_actor["email"])
        self.assertIs(self.store.briefing(other_actor, mode="workflow"), second_actor)
        with mock.patch.object(self.store.ai, "_chat", return_value="SYN [[ZF-1: Stage: Contacting resident]]") as chat:
            enabled = self.store.briefing(other_actor)
        chat.assert_called_once()
        self.assertNotEqual(enabled["record_id"], second_actor["record_id"])

    def test_expanded_briefing_uses_projected_status_and_reason_policy_cache(self):
        private = "SYN-PRIVATE-WAITING-REASON"
        with self.store.lock:
            self.store._case("ZF-1")["reason"] = private
            self.store.save()
        with mock.patch.object(self.store.ai, "_chat", return_value="SYN [[ZF-1: Stage: Contacting resident]]") as chat:
            visible = self.store.briefing(self.pam)
            self.assertIn(private, chat.call_args.args[2])
            with mock.patch.dict(os.environ, {"ZF_REASON_ROLES": ""}):
                held = self.store.briefing(self.pam)
                self.assertNotIn(private, chat.call_args.args[2])
                self.assertNotEqual(held["record_id"], visible["record_id"])
            support = self.store.briefing(dict(self.pam, role="Programme Support Officer"))
            self.assertNotIn(private, chat.call_args.args[2])
            self.assertEqual(support["scope"], "programme")
        self.assertEqual(self.store.cases["ZF-1"]["reason"], private)

    def test_empty_programme_is_not_reported_as_empty_assignments(self):
        with mock.patch.object(self.store, "_filtered", return_value=[]):
            result = self.store.briefing(self.pam, mode="workflow")
        self.assertEqual(result["text"], "No permitted open programme cases are available.")
        self.assertEqual((result["case_count"], result["summary_count"]), (0, 0))
        record = next(r for r in self.records() if r["id"] == result["record_id"])
        self.assertEqual(record["case_ids"], [])

    def test_briefing_scope_over_existing_authenticated_route(self):
        app = App(self.store, "SYN-briefing-test")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            for user, scope, count in (
                (self.sam, "assigned", 4), (self.pam, "programme", 5),
                (dict(self.pam, role="Programme Support Officer", code="UNBOUND"), "programme", 5),
                (dict(self.pam, role="Contractor"), None, None),
                (dict(self.pam, role="Application Administrator"), None, None),
            ):
                with self.subTest(role=user["role"]), mock.patch.object(
                    app.provider, "authenticate", return_value=user,
                ):
                    url = f"http://127.0.0.1:{httpd.server_port}/api/briefing?mode=workflow"
                    if scope is None:
                        with self.assertRaises(urllib.error.HTTPError) as error:
                            urllib.request.urlopen(url)
                        self.assertEqual(error.exception.code, 403)
                    else:
                        with urllib.request.urlopen(url) as response:
                            result = json.load(response)
                        self.assertEqual((result["scope"], result["case_count"]), (scope, count))
        finally:
            httpd.shutdown()
            httpd.server_close()
            thread.join(timeout=5)

    def test_missing_employee_endpoint_uses_explicit_template_without_model_call(self):
        self.store.ai.endpoint = ""
        with mock.patch.object(self.store.ai, "_chat", side_effect=AssertionError("No model call")) as chat:
            result = self.store.briefing(self.sam)
        chat.assert_not_called()
        self.assertEqual((result["source"], result["model"], result["reason"]),
                         ("template", None, "AI is not configured"))
        self.assertEqual((result["case_count"], result["summary_count"]), (4, 3))

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
        self.store.briefing(self.sam)
        self.store.funding_draft(self.pam, "ZF-1")
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        rec = next(x for x in self.records() if x["id"] == r["record_id"])
        self.assertEqual(rec["case_ids"], ["ZF-1"])
        self.assertTrue(rec["ai_output"] and rec["workflow_output"])
        self.assertIsNone(rec["fallback_reason"])
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

    def test_provenance_states_are_separate_and_review_keeps_evidence(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        rec = next(x for x in self.records() if x["id"] == r["record_id"])
        self.assertEqual({k: rec["provenance"][k] for k in ("citation_resolved", "source_verified", "human_reviewed")},
                         dict(citation_resolved=True, source_verified=False, human_reviewed=False))
        before = json.dumps(self.store.data.get("cases"), sort_keys=True, default=str)
        self.store.review_ai(self.sam, r["record_id"], "accept")
        self.assertTrue(rec["provenance"]["human_reviewed"])
        self.assertFalse(rec["provenance"]["source_verified"])
        ev = rec["review_evidence"]
        self.assertEqual((ev["reviewer"], ev["disposition"]), (self.sam["email"], "accept"))
        self.assertTrue(ev["compared"]["ai"] and ev["compared"]["workflow"])
        self.assertEqual(before, json.dumps(self.store.data.get("cases"), sort_keys=True, default=str))

    def test_changed_source_holds_instead_of_accepting(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        rec = next(x for x in self.records() if x["id"] == r["record_id"])
        with mock.patch.object(ai_tasks, "source_hashes", return_value={"ZF-1": "changed"}):
            with self.assertRaises(ValueError):
                self.store.review_ai(self.sam, r["record_id"], "accept")
        self.assertEqual(rec["status"], "Hold")
        self.assertEqual(rec["provenance"]["hold"]["owner"], self.sam["email"])
        self.assertFalse(rec["provenance"]["human_reviewed"])
        self.assertEqual(self.store.ai_live_report()["tasks"]["summary"]["Hold"], 1)

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
    def make(self, tmp, data=None):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA if data is None else data))
        self.path = str(p)
        return Store(self.path, os.path.join(tmp, "live.json"), os.path.join(tmp, "audit.jsonl"))

    def make_again(self):
        return Store(self.path, os.path.join(self.tmp.name, "live.json"), os.path.join(self.tmp.name, "audit.jsonl"))


class SqlTasks(TasksMixin, unittest.TestCase):
    def make(self, tmp, data=None):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA if data is None else data))
        self.path, self.db = str(p), os.path.join(tmp, "pw.sqlite")
        return SqlStore(self.path, self.db)

    def make_again(self):
        return SqlStore(self.path, self.db)


class NegativeControls(unittest.TestCase):
    def test_employee_ai_reads_its_settings_not_resident_or_endpoint_aliases(self):
        with mock.patch.dict(os.environ, {
            "AI_ENDPOINT": "https://employee.invalid/",
            "AI_DEPLOYMENT": "employee-standard",
            "AI_DEPLOYMENT_STRONG": "employee-capable",
            "AI_MODEL_VERSION": "standard-version",
            "AI_MODEL_VERSION_STRONG": "capable-version",
            "ZF_DEMO_ASSISTANT_ENDPOINT": "https://resident.invalid",
            "AZURE_OPENAI_ENDPOINT": "https://alias.invalid",
        }, clear=True):
            ai = Ai()
        self.assertEqual((ai.endpoint, ai.fast, ai.strong, ai.model_version, ai.model_version_strong),
                         ("https://employee.invalid", "employee-standard", "employee-capable",
                          "standard-version", "capable-version"))
        with mock.patch.dict(os.environ, {
            "ZF_DEMO_ASSISTANT_ENDPOINT": "https://resident.invalid",
            "AZURE_OPENAI_ENDPOINT": "https://alias.invalid",
        }, clear=True):
            self.assertFalse(Ai().configured)

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
        summary = body["evaluation"]["summary"]
        runs = [
            run
            for result in body["evaluation"]["results"]
            if result["measures"]
            for run in result["measures"]["run_results"]
        ]
        self.assertEqual(summary["recommendation_runs"], len(runs))
        self.assertEqual(summary["ai_runs"], sum(run["source"] == "ai" for run in runs))
        self.assertEqual(summary["template_runs"], sum(run["source"] == "template" for run in runs))
        self.assertEqual(
            summary["recommendation_runs"], summary["ai_runs"] + summary["template_runs"]
        )
        self.assertIn("tasks", body["live"])

    def test_mode_flag_and_review_over_http(self):
        code, r = self.call("sam@example.test", "/api/cases/ZF-1/ai", {"task": "message", "mode": "workflow"})
        self.assertEqual((code, r["mode"], r["approval"]), (200, "workflow-only", "Not reviewed"))
        code, rec = self.call("sam@example.test", f"/api/ai/review/{r['record_id']}/reject", {"reason": "not needed"})
        self.assertEqual((code, rec["status"]), (200, "Rejected"))
        self.assertEqual(self.call("sam@example.test", f"/api/ai/review/{r['record_id']}/reject", {"reason": "x"})[0], 400)


if __name__ == "__main__":
    unittest.main()


class RegistryEnvelopeTests(unittest.TestCase):
    def test_all_assistants_and_retained_paths_are_registered_unapproved(self):
        from zava_forward.core import ai_registry
        from zava_forward.core.assistants import REGISTRY
        reg = ai_registry.registry()
        ids = {t["id"] for t in reg["tasks"]}
        self.assertTrue(set(REGISTRY) <= ids)
        self.assertTrue({"briefing", "message", "summary", "priority", "funding_draft", "read_document"} <= ids)
        for t in reg["tasks"]:
            for k in ("scope", "permitted_capability", "source_permissions", "accountable_function", "approval_state",
                      "impact_record", "prohibited_uses", "required_approval_evidence"):
                self.assertTrue(t[k], (t["id"], k))
            self.assertEqual((t["accountable_individual"], t["delegation"], t["approval_state"]),
                             ("unknown", "unknown", "unapproved"))
            self.assertTrue(all(v == "unknown" for v in t["authority"].values()))
            self.assertFalse(ai_registry.authorizes_live(t["id"]))
        self.assertIn("tenant social scoring", ai_registry.PROHIBITED_PURPOSES)

    def test_unregistered_task_gets_no_model_call(self):
        with self.assertRaises(ValueError):
            ai_tasks.require_registered("invented-task")

    def test_envelope_binds_versions_and_model_and_stays_unapproved(self):
        from zava_forward.core import ai_registry
        ok = ai_registry.envelope("summary", ["ZF-1"], {"ZF-1": "abc"}, dict(source="ai", model="m1", prompt_version="p"), 3)
        self.assertEqual((ok["provider"], ok["deployment"], ok["model"], ok["case_version"], ok["approved"], ok["approval"]),
                         ("azure-openai", "m1", "m1", 3, False, "Not reviewed"))
        self.assertEqual(ok["source_versions"], {"ZF-1": "abc"})
        bad = ai_registry.envelope("summary", ["ZF-1"], {}, dict(source="template", reason="AI is not configured"))
        self.assertEqual((bad["outcome"], bad["failure"], bad["model"]), ("abstained-or-failed", "AI is not configured", None))
