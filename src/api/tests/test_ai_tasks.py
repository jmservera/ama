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
        self.assertEqual(
            self.store.briefing(self.sam, mode="workflow")["generated_at"], result["generated_at"]
        )
        expected = [c["id"] for c in self.store.list_cases(self.sam)][:3]
        self.assertEqual(
            result["source_case_ids"], [c["id"] for c in self.store.list_cases(self.sam)][:8]
        )
        self.assertEqual(len(result["statements"]), len(expected))
        for statement, cid in zip(result["statements"], expected):
            self.assertIn(statement["text"], result["text"])
            self.assertEqual(statement["unresolved"], [])
            self.assertTrue(all(cite.startswith(cid + ": ") for cite in statement["citations"]))
        for c in self.store.cases.values():
            c["closed"] = True
        self.store.save()
        empty = self.store.briefing(self.sam, mode="workflow")
        self.assertEqual(
            empty["statements"], [dict(text=empty["text"], citations=[], unresolved=[])]
        )

    def test_statement_references_preserve_valid_unresolved_and_dropped_output(self):
        sources = {"ZF-1": ["Stage: Survey booked"]}
        raw = (
            "Check survey [[ZF-1: Stage: Survey booked]]. "
            "Check funding. [[ZF-1: Funding: invented]]"
        )
        statements = ai_tasks.statement_sources(raw, sources)
        self.assertEqual([s["text"] for s in statements], ["Check survey.", "Check funding."])
        self.assertEqual(statements[0]["citations"], ["ZF-1: Stage: Survey booked"])
        self.assertEqual(statements[1]["unresolved"], ["ZF-1: Funding: invented"])
        filtered = ai_tasks.statement_sources(
            "- Keep [[ZF-1: Stage: Survey booked]].\n- Remove invented.", sources, bullets=True
        )
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
        statement = next(
            s for s in result["statements"] if any(c.startswith("ZF-1: ") for c in s["citations"])
        )
        self.assertIn(f"ZF-1: Stage: {before['stage']}", statement["citations"])
        self.assertIn(f"ZF-1: Days in stage: {before['days_in_stage']}", statement["citations"])
        self.assertNotIn("design in progress", statement["text"])

    def test_quarantined_output_never_exposes_abandoned_ai_statement_sources(self):
        from unittest.mock import patch

        case = self.store._case("ZF-1")
        raw = dict(
            source="ai",
            text="Abandoned AI [[ZF-1: Stage: Survey booked]].",
            model="synthetic",
            reason=None,
        )
        with patch.object(
            self.store,
            "continuity_publish",
            side_effect=lambda task, epoch, source, publish: publish(True),
        ):
            result = ai_tasks.finish(
                self.store,
                self.sam,
                "briefing",
                ["ZF-1"],
                raw,
                "Manual summary.",
                {"ZF-1": ai_tasks.source_labels(case)},
                [],
                epoch0=0,
            )
        self.assertEqual(result["source"], "template")
        self.assertEqual(result["approval"], "Quarantined")
        self.assertEqual(
            result["statements"], [dict(text="Manual summary.", citations=[], unresolved=[])]
        )

    def test_unbound_entra_briefing_is_empty_assignment_not_empty_programme(self):
        user = identity.principal(
            "11111111-2222-3333-4444-555555555555",
            "aaaaaaaa-0000-0000-0000-000000000001",
            self.sam["role"],
            email=self.sam["email"],
        )
        user = identity.bind(self.store, user)
        self.assertNotEqual(user["code"], self.sam["code"])
        self.assertEqual(self.store.page_cases(user)["total"], 0)
        self.assertGreater(self.store.page_cases(user, "all")["total"], 0)
        briefing = self.store.briefing(user, mode="workflow")
        self.assertEqual(
            briefing["text"],
            "No open cases are assigned to you. This does not mean the programme has no work.",
        )
        record = next(r for r in self.records() if r["id"] == briefing["record_id"])
        self.assertEqual(record["case_ids"], [])

    def test_bound_entra_briefing_uses_seeded_workload_code_and_excludes_closed(self):
        tenant = "11111111-2222-3333-4444-555555555555"
        oid = "aaaaaaaa-0000-0000-0000-000000000001"
        row = dict(self.sam, tid=tenant, oid=oid)
        if hasattr(self.store, "db"):
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(row), self.sam["email"])
            )
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
                self.assertEqual(
                    (result["scope"], result["scope_label"]), ("programme", "All programme cases")
                )
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
                self.assertEqual(
                    (result["scope"], result["scope_label"]), ("assigned", "My assigned cases")
                )

    def test_unbound_managers_have_programme_briefing_but_zero_assignments(self):
        for role in MANAGER_ROLES:
            with self.subTest(role=role):
                user = identity.bind(
                    self.store,
                    identity.principal(
                        "11111111-2222-3333-4444-555555555555",
                        "aaaaaaaa-0000-0000-0000-000000000001",
                        role,
                        email=self.pam["email"],
                    ),
                )
                self.assertNotEqual(user["code"], self.pam["code"])
                self.assertEqual(self.store.page_cases(user)["total"], 0)
                result = self.store.briefing(user, mode="workflow")
                record = next(r for r in self.records() if r["id"] == result["record_id"])
                self.assertEqual(
                    record["case_ids"], [r["id"] for r in self.store.list_cases(user, "all")]
                )
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
        data["buildings"] = [
            dict(
                id="SYN-BRIEFING",
                name="Synthetic briefing block",
                version=1,
                source="SYN-REGISTER",
                systems=[],
                dependencies=[],
                holds=[],
                works=[],
                costs=[],
            )
        ]
        expanded = Path(self.tmp.name) / "expanded"
        expanded.mkdir()
        if hasattr(self.store, "db"):
            self.store.db.close()
        self.store = self.make(str(expanded), data)
        self.store.ai.endpoint = "http://scripted-model.invalid"
        release_support.install(self.store)
        permitted = sorted(
            self.store._filtered(self.pam, "all", "", {}),
            key=lambda c: self.store._ranking()[c["id"]]["rank"],
        )
        with (
            mock.patch.object(self.store, "_filtered", return_value=permitted) as read,
            mock.patch.object(self.store, "summary", wraps=self.store.summary) as project,
            mock.patch.object(
                self.store, "work_context", side_effect=AssertionError("No queue projection")
            ),
        ):
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
            citation = (
                f"SYN [[{permitted[0]['id']}: Days in stage: {permitted[0]['days_in_stage']}]]"
            )
            with mock.patch.object(self.store.ai, "_chat", return_value=citation):
                enabled = self.store.briefing(self.pam)
            self.assertEqual((enabled["source"], enabled["summary_count"]), ("ai", 8))
            with (
                mock.patch.object(self.store.ai, "_chat", side_effect=TimeoutError),
                mock.patch.object(self.store, "ai_epoch_current", return_value=False),
            ):
                fallback = self.store.briefing(self.pam)
            self.assertEqual((fallback["source"], fallback["summary_count"]), ("template", 3))
            read.return_value = [next(r for r in permitted if r["id"] == "ZF-5")]
            with mock.patch.object(
                self.store.ai, "_chat", return_value="SYN [[Stage: Contacting resident]]"
            ) as chat:
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
        with mock.patch.object(
            self.store.ai, "_chat", return_value="SYN [[ZF-1: Stage: Contacting resident]]"
        ) as chat:
            enabled = self.store.briefing(other_actor)
        chat.assert_called_once()
        self.assertNotEqual(enabled["record_id"], second_actor["record_id"])

    def test_expanded_briefing_uses_projected_status_and_reason_policy_cache(self):
        private = "SYN-PRIVATE-WAITING-REASON"
        with self.store.lock:
            self.store._case("ZF-1")["reason"] = private
            self.store.save()
        with mock.patch.object(
            self.store.ai, "_chat", return_value="SYN [[ZF-1: Stage: Contacting resident]]"
        ) as chat:
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
                (self.sam, "assigned", 4),
                (self.pam, "programme", 5),
                (dict(self.pam, role="Programme Support Officer", code="UNBOUND"), "programme", 5),
                (dict(self.pam, role="Contractor"), None, None),
                (dict(self.pam, role="Application Administrator"), None, None),
            ):
                with (
                    self.subTest(role=user["role"]),
                    mock.patch.object(
                        app.provider,
                        "authenticate",
                        return_value=user,
                    ),
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
        with mock.patch.object(
            self.store.ai, "_chat", side_effect=AssertionError("No model call")
        ) as chat:
            result = self.store.briefing(self.sam)
        chat.assert_not_called()
        self.assertEqual(
            (result["source"], result["model"], result["reason"]),
            ("template", None, "AI is not configured"),
        )
        self.assertEqual((result["case_count"], result["summary_count"]), (4, 3))

    def test_cited_summary_is_verified_but_not_approved(self):
        self.out["text"] = (
            "- Contacting resident [[Stage: Contacting resident]]\n- Waiting [[Days in stage: 10]]"
        )
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
        self.out["text"] = (
            "- Real [[Stage: Contacting resident]]\n- Made up\n- Wrong [[Stage: Survey booked]]"
        )
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
        self.assertGreaterEqual(
            {x["task"] for x in self.records()}, {"summary", "briefing", "funding_draft"}
        )
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
        self.assertEqual(
            {
                k: rec["provenance"][k]
                for k in ("citation_resolved", "source_verified", "human_reviewed")
            },
            dict(citation_resolved=True, source_verified=False, human_reviewed=False),
        )
        before = json.dumps(self.store.data.get("cases"), sort_keys=True, default=str)
        self.store.review_ai(self.sam, r["record_id"], "accept")
        self.assertTrue(rec["provenance"]["human_reviewed"])
        self.assertFalse(rec["provenance"]["source_verified"])
        ev = rec["review_evidence"]
        self.assertEqual((ev["reviewer"], ev["disposition"]), (self.sam["email"], "accept"))
        self.assertTrue(ev["compared"]["ai"] and ev["compared"]["workflow"])
        self.assertEqual(
            before, json.dumps(self.store.data.get("cases"), sort_keys=True, default=str)
        )

    def test_review_evidence_retains_elapsed_review_seconds(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        rec = next(x for x in self.records() if x["id"] == r["record_id"])
        rec["created"] = "2026-01-01T10:00:00"
        with mock.patch.object(ai_tasks, "_now", return_value="2026-01-01T10:02:30"):
            self.store.review_ai(self.sam, r["record_id"], "accept")
        self.assertEqual(rec["review_evidence"]["review_seconds"], 150.0)
        self.assertIsNone(ai_tasks._elapsed_seconds("not a time", "2026-01-01T10:00:00"))
        self.assertEqual(
            ai_tasks._elapsed_seconds("2026-01-01T10:00:05", "2026-01-01T10:00:00"), 0.0
        )

    def test_live_report_aggregates_review_effort(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        ids = [self.store.ai_run(self.sam, "ZF-1", "summary")["record_id"] for _ in range(4)]
        recs = {x["id"]: x for x in self.records()}
        for rid, secs in zip(ids, (30, 90, None, True)):
            recs[rid]["review_evidence"] = {"review_seconds": secs}
        eff = self.store.ai_live_report()["review_effort"]["summary"]
        self.assertEqual(
            eff,
            dict(
                reviewed=4,
                timed=2,
                total_seconds=120.0,
                mean_seconds=60.0,
                by_source={"ai": dict(timed=2, total_seconds=120.0, mean_seconds=60.0)},
            ),
        )
        recs[ids[0]]["source"] = "workflow"
        split = self.store.ai_live_report()["review_effort"]["summary"]["by_source"]
        self.assertEqual(split["workflow"], dict(timed=1, total_seconds=30.0, mean_seconds=30.0))
        self.assertEqual(split["ai"], dict(timed=1, total_seconds=90.0, mean_seconds=90.0))
        for rid in ids:
            recs[rid].pop("review_evidence")
        self.assertEqual(self.store.ai_live_report()["review_effort"], {})

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
        self.out["text"] = json.dumps(
            [dict(case_id="ZF-4", reason="Open safety issue", cites=["Open safety issues: 1"])]
        )
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
        self.out["text"] = json.dumps(
            [dict(case_id="ZF-1", reason="Oldest", cites=["Days in stage: 10"])]
        )
        rec = self.store.ai_priority(self.sam, 1)
        self.assertEqual(rec["source"], "template")
        self.assertEqual([i["case_id"] for i in rec["items"]], ["ZF-4"])
        self.assertTrue(rec["workflow_items"] and rec["fallback_reason"])

    def test_report_for_users_is_not_shared_across_reviewers(self):
        self.out["text"] = "- ok [[Stage: Contacting resident]]"
        r = self.store.ai_run(self.sam, "ZF-1", "summary")
        with self.assertRaises(PermissionError):
            self.store.review_ai(self.pam, r["record_id"], "reject", "x")

    def test_post_provider_output_citation_error_and_review_recheck_blocks_withheld_fields(self):
        rc = dict(self.sam, role="Retrofit Coordinator")
        pso = dict(
            code="PSO9",
            email="pso-vis@example.test",
            name="PSO Vis",
            role="Programme Support Officer",
        )
        contractor = dict(
            code="CON9",
            email="con-vis@example.test",
            name="Con Vis",
            role="Contractor",
            contractor="Northgate Works",
        )
        with self.store.lock:
            self.store.data["staff"].extend([pso, contractor])
            self.store.staff[pso["email"]] = pso
            self.store.staff[contractor["email"]] = contractor
            c = self.store._case("ZF-1")
            c["reason"] = "SYNTH-VULN-MEDICAL-CANARY"
            c["contacts"].append(
                dict(
                    at="2026-02-01T09:00",
                    purpose="Visit",
                    channel="Phone",
                    direction="Outbound",
                    outcome="SYNTH-CONTACT-OUTCOME-CANARY",
                    note="SYNTH-CONTACT-NOTE-CANARY",
                    by="Sam",
                )
            )
            self.store.save()

        # 1. Adversarial AI summary output + raw citation marker echoing withheld vulnerability reason
        self.out["text"] = (
            "- Check SYNTH-VULN-MEDICAL-CANARY [[Reason: SYNTH-VULN-MEDICAL-CANARY]]."
        )
        res = self.store.ai_run(rc, "ZF-1", "summary")
        self.assertEqual(res["source"], "template")
        self.assertNotIn("ai_text", res)
        for canary in (
            "SYNTH-VULN-MEDICAL-CANARY",
            "SYNTH-CONTACT-NOTE-CANARY",
            "SYNTH-CONTACT-OUTCOME-CANARY",
        ):
            self.assertNotIn(canary, json.dumps(res))
        rec = next(r for r in self.records() if r["id"] == res["record_id"])
        self.assertIsNone(rec["ai_output"])
        self.assertEqual(
            rec["fallback_reason"],
            "model output withheld by role visibility check; use the manual route",
        )

        # 2. Provider exception carrying withheld canary is sanitized to class name only
        def explode(*a, **k):
            raise RuntimeError(
                "Upstream echoed SYNTH-VULN-MEDICAL-CANARY and SYNTH-CONTACT-NOTE-CANARY"
            )

        self.store.ai._chat = explode
        err_res = self.store.ai_run(rc, "ZF-1", "message")
        self.assertEqual(err_res["source"], "template")
        self.assertNotIn("SYNTH-VULN-MEDICAL-CANARY", json.dumps(err_res))
        self.assertNotIn("SYNTH-CONTACT-NOTE-CANARY", json.dumps(err_res))
        err_rec = next(r for r in self.records() if r["id"] == err_res["record_id"])
        self.assertEqual(err_rec["fallback_reason"], "model unavailable (RuntimeError)")
        self.assertNotIn("SYNTH-VULN-MEDICAL-CANARY", json.dumps(err_rec))

        # 3. Priority ranking explanation/citation leaking withheld canary falls back and scrubs ai_output
        self.store.ai._chat = lambda *a, **k: self.out["text"]
        self.out["text"] = json.dumps(
            [
                dict(
                    case_id="ZF-4",
                    reason="Urgent SYNTH-VULN-MEDICAL-CANARY",
                    cites=["Open safety issues: 1"],
                )
            ]
        )
        pri = self.store.ai_priority(rc, 1)
        self.assertEqual(pri["source"], "template")
        self.assertNotIn("SYNTH-VULN-MEDICAL-CANARY", json.dumps(pri))
        self.assertNotIn("SYNTH-VULN-MEDICAL-CANARY", json.dumps(self.store.latest_priority(rc)))

        # 4. Reviewer reason containing vulnerability details is held from non-reason roles in live_report & review
        self.out["text"] = "- Survey step [[ZF-1: Stage: Contacting resident]]"
        pam_res = self.store.ai_run(self.pam, "ZF-1", "summary")
        self.store.review_ai(
            self.pam, pam_res["record_id"], "reject", "Contains SYNTH-VULN-MEDICAL-CANARY detail"
        )
        pso_rep = self.store.ai_live_report(pso)
        pam_rep = self.store.ai_live_report(self.pam)
        self.assertNotIn("SYNTH-VULN-MEDICAL-CANARY", json.dumps(pso_rep))
        self.assertTrue(
            all(x["reason"] == projection.NOTE_HELD for x in pso_rep["reviewer_reasons"])
        )
        self.assertIn("SYNTH-VULN-MEDICAL-CANARY", json.dumps(pam_rep))
        with self.assertRaises(PermissionError):
            self.store.review_ai(contractor, pam_res["record_id"], "reject", "blocked")
        with self.assertRaises(PermissionError):
            self.store.ai_live_report(contractor)

    def test_record_view_preserves_author_review_notes_while_holding_tainted_outputs_and_non_author_views(
        self,
    ):
        rc = dict(self.sam, role="Retrofit Coordinator")
        pso = dict(
            code="PSO8",
            email="pso-author-check@example.test",
            name="PSO Author Check",
            role="Programme Support Officer",
        )
        bsl = dict(
            code="BSL8",
            email="bsl-author-check@example.test",
            name="BSL Author Check",
            role="Building Safety Liaison",
        )
        with self.store.lock:
            self.store.data["staff"].extend([pso, bsl])
            self.store.staff[pso["email"]] = pso
            self.store.staff[bsl["email"]] = bsl
            case_zf1 = self.store._case("ZF-1")
            case_zf1["resident"]["adjustment"] = "SYNTH-ADJ-AUTHOR-CANARY"
            case_zf1["finance"] = dict(account="SYNTH-FIN-AUTHOR-CANARY")
            self.store.save()

        self.out["text"] = "- Survey step [[Stage: Contacting resident]]"
        proposal = self.store.ai_run(rc, "ZF-1", "summary")
        own_edit = "Keep SYNTH-ADJ-AUTHOR-CANARY and SYNTH-FIN-AUTHOR-CANARY confirmation."
        own_reason = "Reviewer recorded SYNTH-ADJ-AUTHOR-CANARY and SYNTH-FIN-AUTHOR-CANARY."
        returned = self.store.review_ai(rc, proposal["record_id"], "edit", own_reason, own_edit)
        self.assertEqual(returned["override_text"], own_edit)
        self.assertEqual(returned["reviewer_reason"], own_reason)
        self.assertEqual(returned["review_evidence"]["reason"], own_reason)

        tainted = dict(
            next(r for r in self.records() if r["id"] == proposal["record_id"]),
            reason=own_reason,
            ai_output="Leak SYNTH-ADJ-AUTHOR-CANARY",
            shown_output="Leak SYNTH-ADJ-AUTHOR-CANARY",
            workflow_output="Leak SYNTH-ADJ-AUTHOR-CANARY",
            citations=["Stage: Contacting resident", "Adjustment: SYNTH-ADJ-AUTHOR-CANARY"],
            unresolved=["Adjustment: SYNTH-ADJ-AUTHOR-CANARY"],
            review_evidence=dict(
                returned["review_evidence"],
                compared=dict(
                    ai="Leak SYNTH-ADJ-AUTHOR-CANARY",
                    workflow="Leak SYNTH-ADJ-AUTHOR-CANARY",
                ),
            ),
        )
        author_view = ai_tasks._record_view(self.store, rc, tainted)
        self.assertEqual(author_view["override_text"], own_edit)
        self.assertEqual(author_view["reviewer_reason"], own_reason)
        self.assertEqual(author_view["reason"], own_reason)
        self.assertEqual(author_view["review_evidence"]["reason"], own_reason)
        for held_key in ("ai_output", "shown_output", "workflow_output"):
            self.assertEqual(author_view[held_key], projection.NOTE_HELD)
        self.assertEqual(author_view["citations"], ["Stage: Contacting resident"])
        self.assertEqual(author_view["unresolved"], [])
        self.assertEqual(author_view["review_evidence"]["compared"]["ai"], projection.NOTE_HELD)
        self.assertEqual(
            author_view["review_evidence"]["compared"]["workflow"], projection.NOTE_HELD
        )

        for non_author in (pso, bsl):
            other_view = ai_tasks._record_view(self.store, non_author, tainted)
            self.assertEqual(other_view["override_text"], projection.NOTE_HELD)
            self.assertEqual(other_view["reviewer_reason"], projection.NOTE_HELD)
            self.assertEqual(other_view["reason"], projection.NOTE_HELD)
            self.assertEqual(other_view["review_evidence"]["reason"], projection.NOTE_HELD)

    def test_funding_draft_excludes_vulnerability_reason_even_for_manager_and_projects_by_finance_role(
        self,
    ):
        rlo = dict(
            code="RLO9",
            email="rlo-vis@example.test",
            name="RLO Vis",
            role="Resident Liaison Officer",
        )
        pso = dict(
            code="PSO9",
            email="pso-fin@example.test",
            name="PSO Fin",
            role="Programme Support Officer",
        )
        with self.store.lock:
            self.store.data["staff"].extend([rlo, pso])
            self.store.staff[rlo["email"]] = rlo
            self.store.staff[pso["email"]] = pso
            self.store._case("ZF-1")["resident"]["adjustment"] = "SYNTH-FUNDING-REASON-CANARY"
            self.store.save()
        prompts = []

        def spy_chat(dep, sysmsg, prompt, *a, **k):
            prompts.append(json.dumps([sysmsg, prompt]))
            return "Needs: costs citing SYNTH-FUNDING-REASON-CANARY [[Stage: Contacting resident]]."

        self.store.ai._chat = spy_chat
        self.store.funding_draft(self.pam, "ZF-1")
        self.assertTrue(prompts)
        self.assertNotIn("SYNTH-FUNDING-REASON-CANARY", "".join(prompts))
        pso_detail = self.store.detail("ZF-1", pso)
        self.assertEqual(pso_detail["funding"]["draft"], projection.NOTE_HELD)
        rlo_detail = self.store.detail("ZF-1", rlo)
        self.assertEqual(rlo_detail["funding"]["draft"], projection.NOTE_HELD)
        pam_detail = self.store.detail("ZF-1", self.pam)
        self.assertIn("SYNTH-FUNDING-REASON-CANARY", pam_detail["funding"]["draft"])

    def test_document_ai_requires_approved_derivative_or_scoped_exception_and_preserves_manual_paths(
        self,
    ):
        from dataset import change_metadata

        calls = []

        def spy_chat(dep, sysmsg, prompt, *a, **k):
            calls.append(json.dumps([sysmsg, prompt]))
            return "Redacted document summary ready for officer review."

        self.store.ai._chat = spy_chat
        before_stage = self.store._case("ZF-1")["stage"]

        # Upload intact document with clean scan so manual download & reading are permitted
        doc = self.store.add_document(
            self.sam,
            "ZF-1",
            "occupational-therapy.txt",
            "Other",
            b"INTACT-RAW-DOCUMENT-CANARY: stair rail needed.",
            metadata=change_metadata(self.store, "ZF-1"),
        )
        with self.store.lock:
            stored_doc = next(
                d for d in self.store._case("ZF-1")["documents"] if d["id"] == doc["id"]
            )
            stored_doc["summary"] = "Human officer manual note kept intact."
            self.store.save()

        # 1. Default intact upload is denied model processing without calling provider; manual read & download work
        denied = self.store.read_document(self.sam, "ZF-1", doc["id"])
        self.assertEqual(calls, [])
        self.assertEqual(denied["source"], "template")
        self.assertTrue(denied["manual_available"])
        self.assertIn("reviewed, redacted derivative", denied["reason"])
        detail_after_deny = self.store.detail("ZF-1", self.sam)
        doc_view = next(d for d in detail_after_deny["documents"] if d["id"] == doc["id"])
        self.assertEqual(doc_view["summary"], "Human officer manual note kept intact.")
        dl_name, dl_mime, dl_bytes = self.store.get_document("ZF-1", doc["id"], self.sam)
        self.assertEqual(dl_bytes, b"INTACT-RAW-DOCUMENT-CANARY: stair rail needed.")
        self.assertEqual((dl_mime, dl_name), ("text/plain", "occupational-therapy.txt"))

        # 2. Approved derivative dispatches ONLY redacted derivative_text while keeping stored file bytes intact
        approved = self.store.read_document(
            self.sam,
            "ZF-1",
            doc["id"],
            derivative="reviewed_redacted",
            derivative_text="REDACTED-SAFE-DERIVATIVE: accessibility grab rail requested.",
        )
        self.assertEqual(len(calls), 1)
        self.assertIn("REDACTED-SAFE-DERIVATIVE", calls[0])
        self.assertNotIn("INTACT-RAW-DOCUMENT-CANARY", calls[0])
        self.assertEqual(approved["source"], "ai")
        self.assertEqual(approved["approval"], "Not reviewed")
        self.assertEqual(self.store._case("ZF-1")["stage"], before_stage)
        _, _, dl_bytes2 = self.store.get_document("ZF-1", doc["id"], self.sam)
        self.assertEqual(dl_bytes2, b"INTACT-RAW-DOCUMENT-CANARY: stair rail needed.")

        # 3. Scoped necessity exception allows bounded processing on another intact doc, held from non-reason roles
        doc2 = self.store.add_document(
            self.sam,
            "ZF-1",
            "urgent-letter.txt",
            "Other",
            b"SECOND-INTACT-LETTER: damp inspection access.",
            metadata=change_metadata(self.store, "ZF-1"),
        )
        exc = dict(
            reference="EXC-2026-900",
            approved_by="pam@example.test",
            reason="SENSITIVE-NECESSITY-REASON-CANARY",
            task="read_document",
            case_id="ZF-1",
            doc_id=doc2["id"],
            expires_at="2099-01-01T00:00:00+00:00",
        )
        rc = dict(self.sam, role="Retrofit Coordinator")
        exc_res = self.store.read_document(self.pam, "ZF-1", doc2["id"], necessity_exception=exc)
        self.assertEqual(exc_res["source"], "ai")
        rc_doc2 = next(
            d for d in self.store.detail("ZF-1", rc)["documents"] if d["id"] == doc2["id"]
        )
        pam_doc2 = next(
            d for d in self.store.detail("ZF-1", self.pam)["documents"] if d["id"] == doc2["id"]
        )
        self.assertEqual(rc_doc2["summary"], projection.NOTE_HELD)
        self.assertEqual(rc_doc2["necessity_exception"]["reason"], projection.NOTE_HELD)
        self.assertEqual(pam_doc2["summary"], "Redacted document summary ready for officer review.")

        # 4. Withdrawing resident AI consent blocks further document AI even with approved derivative, while manual/hazard routes still work
        with self.store.lock:
            self.store._case("ZF-1")["resident"]["ai_data_use_consent"] = "Withdrawn"
            self.store.save()
        calls.clear()
        consent_denied = self.store.read_document(
            self.sam,
            "ZF-1",
            doc["id"],
            derivative="reviewed_redacted",
            derivative_text="REDACTED-SAFE-DERIVATIVE",
        )
        self.assertEqual(calls, [])
        self.assertEqual(consent_denied["source"], "template")
        self.assertIn("consent", consent_denied["reason"].lower())
        # Manual contact & hazard raise still work when document AI is denied
        self.store.log_call(self.sam, "ZF-1", "Spoke manually", "Manual follow-up", channel="Phone")
        self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Damp and mould",
            "Routine",
            "Manual inspection",
            metadata=dict(
                change_metadata(self.store, "ZF-1"),
                source="Manual inspection",
                aware_at="2026-03-01T10:00:00Z",
            ),
        )
        self.assertTrue(
            any(h["category"] == "Damp and mould" for h in self.store._case("ZF-1")["hazards"])
        )


class JsonTasks(TasksMixin, unittest.TestCase):
    def make(self, tmp, data=None):
        p = Path(tmp) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA if data is None else data))
        self.path = str(p)
        return Store(self.path, os.path.join(tmp, "live.json"), os.path.join(tmp, "audit.jsonl"))

    def make_again(self):
        return Store(
            self.path,
            os.path.join(self.tmp.name, "live.json"),
            os.path.join(self.tmp.name, "audit.jsonl"),
        )


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
        with mock.patch.dict(
            os.environ,
            {
                "AI_ENDPOINT": "https://employee.invalid/",
                "AI_DEPLOYMENT": "employee-standard",
                "AI_DEPLOYMENT_STRONG": "employee-capable",
                "AI_MODEL_VERSION": "standard-version",
                "AI_MODEL_VERSION_STRONG": "capable-version",
                "ZF_DEMO_ASSISTANT_ENDPOINT": "https://resident.invalid",
                "AZURE_OPENAI_ENDPOINT": "https://alias.invalid",
            },
            clear=True,
        ):
            ai = Ai()
        self.assertEqual(
            (ai.endpoint, ai.fast, ai.strong, ai.model_version, ai.model_version_strong),
            (
                "https://employee.invalid",
                "employee-standard",
                "employee-capable",
                "standard-version",
                "capable-version",
            ),
        )
        with mock.patch.dict(
            os.environ,
            {
                "ZF_DEMO_ASSISTANT_ENDPOINT": "https://resident.invalid",
                "AZURE_OPENAI_ENDPOINT": "https://alias.invalid",
            },
            clear=True,
        ):
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
        for key in (
            "mean_overlap",
            "mean_spearman",
            "latency_ms",
            "models",
            "prompt_versions",
            "reviewer",
            "variation",
            "added_value",
        ):
            self.assertIn(key, s)
        self.assertTrue(any(v["distinct_orders"] > 1 for v in s["variation"]))
        self.assertGreater(s["added_value"]["ai_minus_deterministic"], 0)
        self.assertEqual(sum(s["reviewer"]["counts"].values()), 10)


class Endpoints(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        p = Path(self.tmp.name) / "zavaforward.json"
        p.write_text(json.dumps(test_mvp.DATA))
        self.store = Store(
            str(p),
            os.path.join(self.tmp.name, "live.json"),
            os.path.join(self.tmp.name, "audit.jsonl"),
        )
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(App(self.store, "zf-test")))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def call(self, email, path, body=None):
        login = urllib.request.Request(
            self.base + "/api/login", json.dumps(dict(email=email, password="zf-test")).encode()
        )
        ck = urllib.request.urlopen(login).headers["Set-Cookie"].split(";")[0]
        req = urllib.request.Request(
            self.base + path,
            json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": ck},
        )
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_stock_queue_route_is_manager_only_and_read_only(self):
        self.assertEqual(self.call("sam@example.test", "/api/asset/stock-queue")[0], 403)
        code, body = self.call("pam@example.test", "/api/asset/stock-queue")
        self.assertEqual(code, 200)
        self.assertEqual(body["total"], len(body["items"]))
        self.assertEqual(self.call("pam@example.test", "/api/asset/stock-queue", {})[0], 404)

    def test_resident_choice_queue_route_is_role_gated_and_read_only(self):
        code, body = self.call("sam@example.test", "/api/resident/choice-queue?limit=1")
        self.assertEqual(code, 200)
        self.assertEqual(len(body["items"]), 1)
        self.assertGreaterEqual(body["total"], 1)
        self.assertEqual(self.call("pam@example.test", "/api/resident/choice-queue")[0], 200)
        self.assertEqual(
            self.call("sam@example.test", "/api/resident/choice-queue?limit=x")[0], 400
        )
        self.assertEqual(self.call("sam@example.test", "/api/resident/choice-queue", {})[0], 404)

    def test_data_protection_register_route_is_read_only_and_never_echoes_references(self):
        with mock.patch.dict(os.environ, {"DP_STAFF_IDENTITY_LAWFUL_BASIS_REF": "PRIVATE-REF-1"}):
            code, body = self.call("sam@example.test", "/api/data-protection")
        self.assertEqual(code, 200)
        self.assertFalse(body["dpo_reviewed"])
        self.assertNotIn("PRIVATE-REF-1", json.dumps(body))
        self.assertTrue(any(c["kind"] == "actual" for c in body["classes"]))
        self.assertEqual(self.call("sam@example.test", "/api/data-protection", {})[0], 404)

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
        co = body["evaluation"]["cohorts"]
        self.assertEqual(co["owner_approval_status"], "unapproved")
        self.assertFalse(co["lawful_analysis_fields_approved"])
        self.assertFalse(co["live_activation_allowed"])
        self.assertTrue(co["synthetic_not_fairness_evidence"])
        self.assertIn("OQ-018", co["non_fairness_provenance_notice"])

    def test_cohort_evaluation_route_is_manager_only_read_only_and_enforces_oq018(self):
        self.assertEqual(self.call("sam@example.test", "/api/ai/cohort-evaluation")[0], 403)
        self.assertEqual(self.call("pam@example.test", "/api/ai/cohort-evaluation?live=1")[0], 400)
        self.assertEqual(self.call("pam@example.test", "/api/ai/cohort-evaluation", {})[0], 404)
        code, body = self.call("pam@example.test", "/api/ai/cohort-evaluation")
        self.assertEqual(code, 200)
        self.assertEqual(body["owner_approval_status"], "unapproved")
        self.assertFalse(body["lawful_analysis_fields_approved"])
        self.assertFalse(body["live_activation_allowed"])
        self.assertTrue(body["synthetic_not_fairness_evidence"])
        self.assertIn("OQ-018", body["non_fairness_provenance_notice"])
        for key, expected_task in (
            ("ranking", "ranking-policy"),
            ("ai_priority", "ai-priority-recommendation"),
        ):
            rec = body[key]
            self.assertEqual(rec["task_id"], expected_task)
            self.assertEqual(rec["owner_approval_status"], "unapproved")
            self.assertFalse(rec["lawful_analysis_fields_approved"])
            self.assertFalse(rec["activation_allowed"])
            self.assertFalse(rec["live_activation_allowed"])
            self.assertTrue(rec["synthetic"])
            self.assertFalse(rec["fairness_evidence"])
            self.assertTrue(rec["synthetic_not_fairness_evidence"])
            self.assertIn("OQ-018", rec["non_fairness_provenance_notice"])
            self.assertEqual(len(rec["record_hash"]), 64)
            self.assertIn("unapproved_thresholds", {b["code"] for b in rec["blockers"]})
            for dim in rec["dimensions"].values():
                self.assertEqual(
                    sum(r["n"] + r["missing"] for r in dim["cohorts"].values()), rec["total_cases"]
                )

    def test_report_separates_chat_multi_turn_evaluation_from_single_turn_evaluation(self):
        code, body = self.call("pam@example.test", "/api/ai/report")
        self.assertEqual(code, 200)
        single = body["evaluation"]
        chat = body["chat_evaluation"]
        self.assertTrue(single["passed"])
        self.assertTrue(chat["passed"])
        self.assertIn("recommendation_runs", single["summary"])
        self.assertNotIn("recommendation_runs", chat.get("summary", {}))
        self.assertGreaterEqual(chat["scenarios"], 13)
        self.assertTrue(
            chat["summary"]["chat_specific"]["revocation_no_retained_authority"]["passed"]
        )
        self.assertTrue(
            chat["summary"]["chat_specific"]["no_manufactured_approval_or_consent"]["passed"]
        )
        self.assertTrue(
            {
                "task",
                "model",
                "prompt_version",
                "policy_version",
                "source_version",
                "memory_version",
            }
            <= set(chat["bindings"])
        )
        self.assertEqual(len(chat["summary"]["review_effort"]["missing_inputs"]), 4)
        self.assertEqual(chat["enablement"]["state"], "disabled")

    def test_report_repeat_request_reuses_evaluations_and_answers_within_five_seconds(self):
        import time

        from zava_forward.agents import chat_eval

        self.call("pam@example.test", "/api/ai/report")
        with (
            mock.patch.object(ai_eval, "run_scenario", side_effect=AssertionError("recomputed")),
            mock.patch.object(chat_eval, "run_scenario", side_effect=AssertionError("recomputed")),
        ):
            started = time.monotonic()
            code, body = self.call("pam@example.test", "/api/ai/report")
            elapsed = time.monotonic() - started
        self.assertEqual(code, 200)
        self.assertLess(elapsed, 5.0)
        self.assertTrue(body["chat_evaluation"]["passed"])

    def test_report_chat_failure_does_not_alter_single_turn_results_and_live_stays_disabled(self):
        baseline_code, baseline = self.call("pam@example.test", "/api/ai/report")
        self.assertEqual(baseline_code, 200)
        injected_chat = dict(
            baseline["chat_evaluation"],
            passed=False,
            failures=[{"scenario": "chat-revocation", "turn": 2, "check": "kind"}],
        )
        with mock.patch("zava_forward.agents.chat_eval.run_eval", return_value=injected_chat):
            code, body = self.call("pam@example.test", "/api/ai/report")
        self.assertEqual(code, 200)
        self.assertEqual(body["evaluation"]["passed"], baseline["evaluation"]["passed"])
        for key in ("recommendation_runs", "ai_runs", "template_runs"):
            self.assertEqual(
                body["evaluation"]["summary"][key], baseline["evaluation"]["summary"][key]
            )
        self.assertEqual(
            [r["passed"] for r in body["evaluation"]["results"]],
            [r["passed"] for r in baseline["evaluation"]["results"]],
        )
        self.assertTrue(body["evaluation"]["passed"])
        self.assertFalse(body["chat_evaluation"]["passed"])
        self.assertEqual(body["chat_evaluation"]["enablement"]["state"], "disabled")
        self.assertFalse(body["live"].get("enabled", False))
        self.assertTrue(
            all(not t.get("enabled", False) for t in body["live"]["tasks"])
            if isinstance(body["live"]["tasks"], list)
            else all(not t.get("enabled", False) for t in body["live"]["tasks"].values())
        )

    def test_mode_flag_and_review_over_http(self):
        code, r = self.call(
            "sam@example.test", "/api/cases/ZF-1/ai", {"task": "message", "mode": "workflow"}
        )
        self.assertEqual((code, r["mode"], r["approval"]), (200, "workflow-only", "Not reviewed"))
        code, rec = self.call(
            "sam@example.test", f"/api/ai/review/{r['record_id']}/reject", {"reason": "not needed"}
        )
        self.assertEqual((code, rec["status"]), (200, "Rejected"))
        self.assertEqual(
            self.call(
                "sam@example.test", f"/api/ai/review/{r['record_id']}/reject", {"reason": "x"}
            )[0],
            400,
        )

    def test_http_read_doc_denies_unapproved_derivative_while_keeping_upload_detail_download_and_hazard_routes(
        self,
    ):
        import base64
        from dataset import change_metadata

        release_support.install(self.store)
        calls = []
        self.store.ai.endpoint = "http://127.0.0.1:9"
        self.store.ai._chat = lambda dep, sysmsg, prompt, *a, **k: (
            calls.append(json.dumps([sysmsg, prompt])) or "Approved redacted HTTP summary."
        )

        raw_bytes = b"HTTP-INTACT-PRIVATE-CANARY: hospital discharge note."
        up_code, up_detail = self.call(
            "sam@example.test",
            "/api/cases/ZF-1/upload",
            {
                "name": "discharge.txt",
                "kind": "Other",
                "data": base64.b64encode(raw_bytes).decode(),
                **change_metadata(self.store, "ZF-1"),
            },
        )
        self.assertEqual(up_code, 200)
        doc_id = next(x["id"] for x in up_detail["documents"] if x["name"] == "discharge.txt")

        # Denied model call without approved derivative or exception
        code, denied = self.call("sam@example.test", "/api/cases/ZF-1/read-doc", {"id": doc_id})
        self.assertEqual(code, 200)
        self.assertEqual(denied["source"], "template")
        self.assertTrue(denied["manual_available"])
        self.assertEqual(calls, [])

        # Manual detail, clean download, draft fallback, and hazard raise remain available
        d_code, detail = self.call("sam@example.test", "/api/cases/ZF-1")
        self.assertEqual(d_code, 200)
        self.assertTrue(any(x["id"] == doc_id for x in detail["documents"]))

        login = urllib.request.Request(
            self.base + "/api/login",
            json.dumps(dict(email="sam@example.test", password="zf-test")).encode(),
        )
        ck = urllib.request.urlopen(login).headers["Set-Cookie"].split(";")[0]
        with urllib.request.urlopen(
            urllib.request.Request(f"{self.base}/api/docs/ZF-1/{doc_id}", headers={"Cookie": ck})
        ) as dl:
            self.assertEqual(dl.status, 200)
            self.assertEqual(dl.read(), raw_bytes)

        hz_code, _ = self.call(
            "sam@example.test",
            "/api/cases/ZF-1/hazard-raise",
            {
                "category": "Electrical",
                "priority": "Routine",
                "source": "Manual fallback check",
                "aware_at": "2026-03-02T09:00:00Z",
                **change_metadata(self.store, "ZF-1"),
            },
        )
        self.assertEqual(hz_code, 200)

        # Approved redacted derivative over HTTP sends only redacted text and remains unapproved proposal
        ok_code, ok_body = self.call(
            "sam@example.test",
            "/api/cases/ZF-1/read-doc",
            {
                "id": doc_id,
                "ai_derivative": "reviewed_redacted",
                "derivative_text": "HTTP-REDACTED-SAFE-TEXT: grab rail installation timing.",
            },
        )
        self.assertEqual(ok_code, 200)
        self.assertEqual(ok_body["source"], "ai")
        self.assertEqual(ok_body["approval"], "Not reviewed")
        self.assertEqual(len(calls), 1)
        self.assertIn("HTTP-REDACTED-SAFE-TEXT", calls[0])
        self.assertNotIn("HTTP-INTACT-PRIVATE-CANARY", calls[0])

    def test_http_draft_and_ai_report_recheck_role_visibility(self):
        release_support.install(self.store)
        pso = dict(
            code="PSOH",
            email="pso-http@example.test",
            name="PSO Http",
            role="Programme Support Officer",
        )
        con = dict(
            code="CONH",
            email="con-http@example.test",
            name="Con Http",
            role="Contractor",
            contractor="Northgate Works",
        )
        with self.store.lock:
            self.store.data["staff"].extend([pso, con])
            self.store.staff[pso["email"]] = pso
            self.store.staff[con["email"]] = con
            c = self.store._case("ZF-1")
            c["reason"] = "HTTP-REASON-CANARY-77"
            c["unavailable"] = "HTTP-UNAVAILABLE-MEDICAL-WINDOW"
            self.store.save()

        self.store.ai.endpoint = "http://127.0.0.1:9"
        self.store.ai._chat = lambda *a, **k: "- Step [[ZF-1: Stage: Contacting resident]]"
        run_code, run_body = self.call(
            "pam@example.test", "/api/cases/ZF-1/ai", {"task": "summary"}
        )
        self.assertEqual(run_code, 200, run_body)
        rev_code, _ = self.call(
            "pam@example.test",
            f"/api/ai/review/{run_body['record_id']}/reject",
            {"reason": "Reviewer noted HTTP-REASON-CANARY-77"},
        )
        self.assertEqual(rev_code, 200)

        # PSO can access /api/ai/report (manager role) but cannot see vulnerability-linked reviewer reasons
        rep_code, pso_rep = self.call("pso-http@example.test", "/api/ai/report")
        self.assertEqual(rep_code, 200)
        self.assertNotIn("HTTP-REASON-CANARY-77", json.dumps(pso_rep))
        self.assertTrue(
            all(r["reason"] == projection.NOTE_HELD for r in pso_rep["live"]["reviewer_reasons"])
        )

        # Template /api/cases/ZF-1/draft omits `unavailable` window for non-reason roles (sam is Retrofit Coordinator)
        dr_code, dr_body = self.call(
            "sam@example.test", "/api/cases/ZF-1/draft", {"kind": "appointment"}
        )
        self.assertEqual(dr_code, 200)
        self.assertNotIn("HTTP-UNAVAILABLE-MEDICAL-WINDOW", json.dumps(dr_body))
        self.assertEqual(
            self.call("con-http@example.test", "/api/cases/ZF-1/ai", {"task": "summary"})[0], 403
        )

    def test_http_chat_resume_and_continuity_export_recheck_current_permissions(self):
        pso = dict(
            code="PSOE",
            email="pso-exp@example.test",
            name="PSO Exp",
            role="Programme Support Officer",
        )
        rc = dict(
            code="RCC1", email="rc-chat@example.test", name="RC Chat", role="Retrofit Coordinator"
        )
        with self.store.lock:
            self.store.data["staff"].extend([pso, rc])
            self.store.staff[pso["email"]] = pso
            self.store.staff[rc["email"]] = rc
            self.store._case("ZF-1")["reason"] = "CHAT-EXPORT-REASON-CANARY"
            self.store.save()

        # Continuity full export requires reason + resident + finance visibility; PSO is downgraded to limited export
        pso_code, pso_bundle = self.call("pso-exp@example.test", "/api/continuity/export")
        pam_code, pam_bundle = self.call("pam@example.test", "/api/continuity/export")
        self.assertEqual((pso_code, pso_bundle["audience"]["scope"]), (200, "limited"))
        self.assertNotIn("CHAT-EXPORT-REASON-CANARY", json.dumps(pso_bundle))
        self.assertEqual((pam_code, pam_bundle["audience"]["scope"]), (200, "full"))

        # Persisted chat thread containing withheld canary or lost case visibility is rechecked on GET /api/chat/threads/{tid}
        started = self.store.chat_create_thread(rc, case_id="ZF-1")
        tid = started["id"]
        self.store.chat_add_message(
            rc,
            tid,
            "assistant",
            "Leaked CHAT-EXPORT-REASON-CANARY in saved history.",
            evidence=["Reason: CHAT-EXPORT-REASON-CANARY"],
        )
        t_code, t_body = self.call("rc-chat@example.test", f"/api/chat/threads/{tid}")
        self.assertEqual(t_code, 200)
        self.assertNotIn("CHAT-EXPORT-REASON-CANARY", json.dumps(t_body))

        # Reassigning caller to Contractor revokes visibility of the case/thread on resume
        with self.store.lock:
            rc["role"] = "Contractor"
            rc["contractor"] = "Unassigned Co"
            self.store.save()
        self.assertIn(self.call("rc-chat@example.test", f"/api/chat/threads/{tid}")[0], (403, 404))


if __name__ == "__main__":
    unittest.main()


class RegistryEnvelopeTests(unittest.TestCase):
    def test_all_assistants_and_retained_paths_are_registered_unapproved(self):
        from zava_forward.core import ai_registry
        from zava_forward.core.assistants import REGISTRY

        reg = ai_registry.registry()
        ids = {t["id"] for t in reg["tasks"]}
        self.assertTrue(set(REGISTRY) <= ids)
        self.assertTrue(
            {"briefing", "message", "summary", "priority", "funding_draft", "read_document"} <= ids
        )
        for t in reg["tasks"]:
            for k in (
                "scope",
                "permitted_capability",
                "source_permissions",
                "accountable_function",
                "approval_state",
                "impact_record",
                "prohibited_uses",
                "required_approval_evidence",
            ):
                self.assertTrue(t[k], (t["id"], k))
            self.assertEqual(
                (t["accountable_individual"], t["delegation"], t["approval_state"]),
                ("unknown", "unknown", "unapproved"),
            )
            self.assertTrue(all(v == "unknown" for v in t["authority"].values()))
            self.assertFalse(ai_registry.authorizes_live(t["id"]))
        self.assertIn("tenant social scoring", ai_registry.PROHIBITED_PURPOSES)

    def test_unregistered_task_gets_no_model_call(self):
        with self.assertRaises(ValueError):
            ai_tasks.require_registered("invented-task")

    def test_envelope_binds_versions_and_model_and_stays_unapproved(self):
        from zava_forward.core import ai_registry

        ok = ai_registry.envelope(
            "summary",
            ["ZF-1"],
            {"ZF-1": "abc"},
            dict(source="ai", model="m1", prompt_version="p"),
            3,
        )
        self.assertEqual(
            (
                ok["provider"],
                ok["deployment"],
                ok["model"],
                ok["case_version"],
                ok["approved"],
                ok["approval"],
            ),
            ("azure-openai", "m1", "m1", 3, False, "Not reviewed"),
        )
        self.assertEqual(ok["source_versions"], {"ZF-1": "abc"})
        bad = ai_registry.envelope(
            "summary", ["ZF-1"], {}, dict(source="template", reason="AI is not configured")
        )
        self.assertEqual(
            (bad["outcome"], bad["failure"], bad["model"]),
            ("abstained-or-failed", "AI is not configured", None),
        )
