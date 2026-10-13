"""Proposal contracts and independent-connection races. No billable provider calls."""
import copy
import json
import os
import re
import shutil
import sqlite3
import threading
import time
import unittest
import urllib.error
import urllib.request
import uuid
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import test_mvp
from zavaforward_mvp import projection, quality
from zavaforward_mvp.ai import Ai
from zavaforward_mvp.assistants import (
    Assistants, Limits, MSSQL_DDL, PURPOSE, REGISTRY, RULES, VERSION, canonical, capture, digest, eligible,
)
from zavaforward_mvp.server import App, make_handler
from zavaforward_mvp.sqlstore import SqlStore
from zavaforward_mvp.store import ConflictError


def config(**overrides):
    result = dict(ZF_ASSIST_AUTHORITY="local-nonbillable-test-authority",
                  ZF_ASSIST_EXPIRES="2099-01-01T00:00:00Z",
                  ZF_ASSIST_CALL_ALLOWANCE="100", ZF_ASSIST_TOKEN_ALLOWANCE="2000000",
                  ZF_ASSIST_PROACTIVE="1")
    result.update({f"ZF_ASSIST_{k.upper()}": str(v) for k, v in overrides.items()})
    return result


def proposal(snapshot):
    return dict(summary="Check supplied evidence with the responsible human.",
                findings=[dict(text="The home facts are supplied evidence, not an approval.", citations=["source:home"])],
                unknowns=[])


class Provider:
    configured = True

    def __init__(self, outcome="returned", bad=None, usage=True):
        self.outcome, self.bad, self.usage, self.calls = outcome, bad, usage, 0

    def evidence(self, system, prompt, max_tokens, timeout):
        self.calls += 1
        value = proposal(json.loads(prompt)["evidence"])
        if self.bad == "citation":
            value["findings"][0]["citations"] = ["private:reason"]
        elif self.bad == "missing":
            value["findings"][0]["citations"] = []
        elif self.bad == "oversize":
            value["summary"] = "x" * 20000
        elif self.bad == "wrong":
            value = {"text": "not typed"}
        return dict(text="not JSON" if self.bad == "json" else canonical(value),
                    provider="local-test-double", deployment="test", model="test-model",
                    source="template" if self.bad == "template" else "ai",
                    outcome=self.outcome,
                    usage=dict(prompt_tokens=100, completion_tokens=30, total_tokens=130) if self.usage else None)

    def run(self, *args, **kwargs):
        kwargs["off"] = True
        return Ai().run(*args, **kwargs)


class Base(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / f".assistant-test-{uuid.uuid4().hex}"
        self.root.mkdir()
        self.seed = self.root / "seed.json"
        self.dbpath = self.root / "cases.sqlite"
        data = copy.deepcopy(test_mvp.DATA)
        self.people = {}
        for i, role in enumerate(projection.STAFF_ROLES + ("Contractor", "Unknown")):
            self.people[role] = dict(code=f"ROLE-{i}", name=f"Human {i}",
                                     email=f"human{i}@example.test", role=role)
        data["staff"] = list(self.people.values())
        self.pm = self.people["Retrofit Programme Manager"]
        for c in data["cases"]:
            c["resident"]["adjustment"] = "PRIVATE-VULNERABILITY-REASON"
            c["finance"] = dict(budget=dict(amount=93417, status="Approved"), commitments=[], invoices=[])
            c["handoff"] = dict(state="Offered", to_code="ROLE-0", note="PRIVATE-HANDOFF-NOTE")
            c["documents"] = [dict(id="SURVEY-1", kind="Survey", name="PRIVATE-DOCUMENT-NAME",
                                    summary="PRIVATE-AI-SUMMARY", content_sha256="abc", version=1)]
        self.seed.write_text(json.dumps(data))
        self.store = SqlStore(str(self.seed), str(self.dbpath))
        self.provider = Provider()
        self.store.ai = self.provider
        self.service = Assistants(self.store, config())

    def tearDown(self):
        self.service.stop()
        self.store.db.close()
        shutil.rmtree(self.root)

    def other(self, **cfg):
        store = SqlStore(str(self.seed), str(self.dbpath))
        store.ai = self.provider
        service = Assistants(store, config(**cfg))
        self.addCleanup(store.db.close)
        self.addCleanup(service.stop)
        return service

    def case(self, mutate):
        with self.service.transaction() as db:
            c = json.loads(db.execute("SELECT body FROM cases WHERE id='ZF-1'").fetchone()[0])
            mutate(c)
            db.execute("UPDATE cases SET body=?,rowversion=rowversion+1,seq=seq+1 WHERE id='ZF-1'", (canonical(c),))

    def domain(self):
        with self.service.transaction() as db:
            return [db.execute(q).fetchall() for q in (
                "SELECT id,body,rowversion,stage,owner_code,closed,rkey,fstatus FROM cases ORDER BY id",
                "SELECT value FROM meta WHERE key='procurement'",
                "SELECT id,body FROM recommendations ORDER BY id",
                "SELECT seq,hash FROM audit ORDER BY seq",
                "SELECT email,body FROM staff ORDER BY email")]

    def run_ready(self, cap):
        p = self.service.invoke(self.pm, cap, "ZF-1")
        self.assertTrue(self.service.execute(p["id"]))
        p = self.service.detail(self.pm, p["id"])
        self.assertEqual(p["state"], "ready")
        return p

    def verify(self, p, user=None):
        return self.service.review(user or self.pm, p["id"], "verify", p["revision"],
                                   "Compared every cited source; unknowns remain unknown.", source_verified=True)

    def expire(self, tid):
        with self.service.transaction() as db:
            db.execute("UPDATE assistant_tasks SET lease_until=0,not_before=0 WHERE id=?", (tid,))
            db.execute("UPDATE assistant_attempts SET active_until=0 WHERE task_id=?", (tid,))


class ContractTests(Base):
    def test_five_exact_versioned_ids(self):
        self.assertEqual(set(REGISTRY), {"stock-prioritisation", "assessment-preparation", "funding-evidence",
                                       "works-resident-coordination", "quality-evidence"})
        r = self.service.registry(self.pm)
        self.assertEqual({a["id"] for a in r["assistants"]}, set(REGISTRY))
        self.assertTrue(all(a["version"] == VERSION for a in r["assistants"]))
        self.assertEqual(r["principal"], PURPOSE)

    def test_rule_registry_schema_hashes_and_capability_only_invalidation(self):
        c = test_mvp.case("ZF-1")
        stock = capture("stock-prioritisation", c)
        other = capture("quality-evidence", c)
        for key in ("registry_hash", "schema_hash", "rule_hash"):
            self.assertEqual(len(stock[key]), 64)
        with patch.dict(RULES, {"stock-prioritisation": "Changed selected synthetic stock predicate"}):
            self.assertNotEqual(digest(stock), digest(capture("stock-prioritisation", c)))
            self.assertEqual(digest(other), digest(capture("quality-evidence", c)))

    def test_only_committed_capacity_not_offered_metadata_is_material(self):
        c = test_mvp.case("ZF-1")
        proc = dict(packages=[dict(id="PKG-1", capacity={"Test Ltd": dict(
            committed=2, offered=4, evidence="Synthetic committed capacity reference", at="2026-01-01")})])
        first = capture("works-resident-coordination", c, proc)
        proc["packages"][0]["capacity"]["Test Ltd"].update(offered=5, at="2026-02-01")
        self.assertEqual(digest(first), digest(capture("works-resident-coordination", c, proc)))
        proc["packages"][0]["capacity"]["Test Ltd"]["committed"] = 3
        self.assertNotEqual(digest(first), digest(capture("works-resident-coordination", c, proc)))

    def test_every_capability_reactive_verified_edit_reject_domain_unchanged(self):
        before = self.domain()
        for cap in REGISTRY:
            with self.subTest(cap=cap):
                p = self.run_ready(cap)
                with self.assertRaises(ValueError):
                    self.service.review(self.pm, p["id"], "accept", p["revision"], "Not checked.")
                p = self.verify(p)
                p = self.service.review(self.pm, p["id"], "edit-accept", p["revision"], "Human edit.",
                                        output=proposal(p["snapshot"]))
                self.assertEqual(p["state"], "accepted")
                self.assertIsNotNone(p["verification"])
                self.assertTrue(any(e.get("output") for e in p["provenance"] if e["kind"] == "completed"))
                self.assertTrue(any(e.get("edited_output") for e in p["provenance"] if e["kind"] == "review"))
                p = self.service.review(self.pm, p["id"], "reject", p["revision"], "Retain rejected history.")
                self.assertEqual(p["state"], "rejected")
        self.assertEqual(before, self.domain())

    def test_every_capability_failure_disabled_and_malformed(self):
        before = self.domain()
        for cap in REGISTRY:
            self.provider.outcome = "returned"
            for bad in ("json", "wrong", "citation", "missing", "oversize", "template"):
                with self.subTest(cap=cap, bad=bad):
                    self.case(lambda c: c["home"].update(address=uuid.uuid4().hex))
                    self.provider.bad = bad
                    p = self.service.invoke(self.pm, cap, "ZF-1")
                    self.service.execute(p["id"])
                    p = self.service.detail(self.pm, p["id"])
                    self.assertEqual(p["state"], "failed")
                    self.assertIsNone(p["output"])
                    self.assertEqual(p["envelope"]["source"], "unverified")
                    with self.assertRaises(ValueError):
                        self.verify(p)
                    self.service.review(self.pm, p["id"], "reject", p["revision"], "Manual route.")
            self.case(lambda c: c["home"].update(address=uuid.uuid4().hex))
            self.provider.outcome, self.provider.bad = "provider-unavailable", None
            p = self.service.invoke(self.pm, cap, "ZF-1")
            self.service.execute(p["id"])
            p = self.service.detail(self.pm, p["id"])
            self.assertEqual(p["state"], "pending")
            self.assertIsNone(p["output"])
            self.expire(p["id"])
            self.service.execute(p["id"])
            p = self.service.detail(self.pm, p["id"])
            self.assertEqual(p["state"], "failed")
            self.expire(p["id"])
            disabled = Assistants(self.store, {})
            self.case(lambda c: c["home"].update(address=uuid.uuid4().hex))
            p = disabled.invoke(self.pm, cap, "ZF-1")
            self.assertEqual(p["state"], "disabled")
            self.assertFalse(disabled.execute(p["id"]))
        # Source mutations in this test are explicit fixture setup, not assistant effects.
        self.assertEqual(before[1:], self.domain()[1:])

    def test_exact_source_role_matrix_and_no_cross_audience_leaks(self):
        before = self.domain()
        for cap, spec in REGISTRY.items():
            p = self.run_ready(cap)
            stored = canonical(p)
            for private in ("PRIVATE-VULNERABILITY-REASON", "PRIVATE-DOCUMENT-NAME", "PRIVATE-AI-SUMMARY", "PRIVATE-HANDOFF-NOTE"):
                self.assertNotIn(private, stored)
            if cap != "funding-evidence":
                self.assertNotIn("93417", stored)
                self.assertNotIn("source:finance", stored)
            if cap == "stock-prioritisation":
                self.assertEqual({r["code"] for r in p["snapshot"]["sources"]["ranking"]["reasons"]},
                                 {"waiting_days", "stage_order"})
                self.assertNotIn("source:preferences", stored)
            self.assertEqual(set(p["snapshot"]["sources"]), set(spec["categories"]))
            for role, user in self.people.items():
                with self.subTest(cap=cap, role=role):
                    if role in spec["roles"]:
                        self.assertEqual(self.service.invoke(user, cap, "ZF-1")["id"], p["id"])
                        self.assertEqual(self.service.detail(user, p["id"])["id"], p["id"])
                        self.assertIn(p["id"], [x["id"] for x in self.service.listing(user)["proposals"]])
                    else:
                        with self.assertRaises(PermissionError):
                            self.service.invoke(user, cap, "ZF-1")
                        with self.assertRaises(PermissionError):
                            self.service.detail(user, p["id"])
                        with self.assertRaises(PermissionError):
                            self.service.review(user, p["id"], "reject", p["revision"], "No authority.")
        self.assertEqual(before, self.domain())

    def test_proactive_all_five_and_reactive_collision_share_key(self):
        self.case(lambda c: c["home"].update(epc=None))
        before = self.domain()
        scanned = self.service.scan()
        for cap in REGISTRY:
            p = self.service.invoke(self.pm, cap, "ZF-1")
            self.assertIn(p["id"], scanned["enqueued"])
            self.assertEqual({v["mode"] for v in p["provenance"] if v["kind"] == "invocation"}, {"reactive", "proactive"})
            self.assertTrue(self.service.execute(p["id"]))
        self.service.scan()
        with self.service.transaction() as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM assistant_tasks WHERE case_id='ZF-1'").fetchone()[0], 5)
        self.assertEqual(before, self.domain())

    def test_every_proactive_capability_malformed_fails_without_domain_mutation(self):
        self.case(lambda c: c["home"].update(epc=None))
        before = self.domain()
        self.provider.bad = "missing"
        scanned = self.service.scan()
        for cap in REGISTRY:
            p = next(p for p in self.service.listing(self.pm, "ZF-1")["proposals"] if p["capability"] == cap)
            self.assertIn(p["id"], scanned["enqueued"])
            self.assertTrue(all(e["actor"] == PURPOSE for e in p["provenance"] if e["kind"] == "invocation"))
            self.service.execute(p["id"])
            current = self.service.detail(self.pm, p["id"])
            self.assertEqual(current["state"], "failed")
            self.assertIsNone(current["output"])
        self.assertEqual(before, self.domain())

    def valid_case(self):
        c = copy.deepcopy(test_mvp.case("VALID"))
        c.update(technical=dict(design_version=1),
                 funding=dict(route="Synthetic application", reference="REF", terms_version=1),
                 grants=[dict(id="G1", scheme="Constructed", state="Opportunity")],
                 finance=dict(budget=dict(amount=100, status="Approved")),
                 documents=[dict(id=k, kind=k, version=1, content_sha256="abc") for k in ("Survey", "Design")])
        cl = quality.checklist_for("Loft insulation")
        c["quality"] = [dict(measure="Loft insulation", state="Submitted", checklist_version=cl["version"],
                             items=[dict(label=lab, evidence="Observed") for lab in cl["items"]])]
        return c

    def test_every_proactive_predicate_ineligible_then_real_missing_conflicting_changed(self):
        valid = self.valid_case()
        for cap in REGISTRY:
            with self.subTest(cap=cap):
                s = capture(cap, valid)
                self.assertFalse(eligible(cap, s, "2026-10-13"))
                altered = copy.deepcopy(valid)
                if cap == "stock-prioritisation":
                    altered["survey"] = dict(epc="F")
                elif cap == "assessment-preparation":
                    altered["documents"] = []
                elif cap == "funding-evidence":
                    altered["funding"]["reference"] = None
                elif cap == "works-resident-coordination":
                    altered["service_requests"] = [dict(id="SR1", status="Open", next_update="2026-01-01")]
                else:
                    altered["quality"][0]["items"][0]["evidence"] = ""
                self.assertTrue(eligible(cap, capture(cap, altered), "2026-10-13"))
                if cap in ("assessment-preparation", "funding-evidence", "quality-evidence"):
                    self.assertTrue(eligible(cap, s, "2026-10-13", changed=True))
        c = copy.deepcopy(valid)
        c["appointments"] = [dict(date="2026-01-01", outcome="Missed")]
        self.assertTrue(eligible("works-resident-coordination", capture("works-resident-coordination", c), "2026-10-13"))
        c["service_requests"] = [dict(status="Closed", next_update="2026-01-01")]
        c["appointments"] = []
        self.assertFalse(eligible("works-resident-coordination", capture("works-resident-coordination", c), "2026-10-13"))
        c = copy.deepcopy(valid)
        c["quality"][0]["items"].append(dict(label=c["quality"][0]["items"][0]["label"], evidence="Conflicts"))
        self.assertTrue(eligible("quality-evidence", capture("quality-evidence", c), "2026-10-13"))
        c = copy.deepcopy(valid)
        c["grants"][0]["state"] = "Claimable"
        self.assertTrue(eligible("funding-evidence", capture("funding-evidence", c), "2026-10-13"))
        c["grants"][0]["history"] = [dict(state="Claimable", source="Synthetic milestone reference")]
        c["documents"].append(dict(id="FUND-1", kind="Funding evidence", content_sha256="abc", version=1))
        self.assertFalse(eligible("funding-evidence", capture("funding-evidence", c), "2026-10-13"))
        c["finance"]["invoices"] = [dict(id="INV-1", ref="Invoice 1", lines=[
            dict(measure="Loft insulation", quantity=1, amount=50, milestone_ref=None)])]
        self.assertTrue(eligible("funding-evidence", capture("funding-evidence", c), "2026-10-13"))

    def test_scan_valid_cases_does_not_enqueue_and_changes_enqueue_material_versions(self):
        valid = self.valid_case()
        with self.service.transaction() as db:
            for cid, in db.execute("SELECT id FROM cases").fetchall():
                c = dict(valid, id=cid)
                db.execute("UPDATE cases SET body=? WHERE id=?", (canonical(c), cid))
        self.assertEqual(self.service.scan()["enqueued"], [])
        for cap in ("assessment-preparation", "funding-evidence", "quality-evidence"):
            self.run_ready(cap)
        self.case(lambda c: c["documents"][1].update(version=2, content_sha256="changed"))
        ids = self.service.scan()["enqueued"]
        for cap in ("assessment-preparation", "funding-evidence", "quality-evidence"):
            self.assertIn(self.service.invoke(self.pm, cap, "ZF-1")["id"], ids)

    def test_unknown_hash_usage_are_null_not_zero_and_exercise_rule_recorded(self):
        self.provider.usage = False
        self.case(lambda c: c["documents"][0].pop("content_sha256"))
        p = self.run_ready("assessment-preparation")
        self.assertIsNone(p["snapshot"]["sources"]["documents"][0]["content_sha256"])
        self.assertIsNone(p["envelope"]["usage"])
        self.assertIn("source.documents.0.content_sha256", p["output"]["unknowns"])
        self.assertIn("not approved company", p["snapshot"]["exercise_rule"])

    def test_no_old_funding_draft_or_domain_actions_called(self):
        with patch.object(self.store, "funding_draft", side_effect=AssertionError), patch.object(
                self.store, "save", side_effect=AssertionError), patch.object(self.store, "audit", side_effect=AssertionError):
            for cap in REGISTRY:
                self.run_ready(cap)

    def test_malformed_nested_fields_do_not_escape_scalar_allowlists(self):
        self.case(lambda c: c.update(home=dict(c["home"], epc={"private": "PRIVATE-NESTED"}),
                                     measures=[{"private": "PRIVATE-MEASURE"}, "Loft insulation"]))
        p = self.run_ready("stock-prioritisation")
        self.assertIsNone(p["snapshot"]["sources"]["home"]["epc"])
        self.assertNotIn("PRIVATE-NESTED", canonical(p))
        p = self.run_ready("quality-evidence")
        self.assertNotIn("PRIVATE-MEASURE", canonical(p))
        self.assertEqual(p["snapshot"]["sources"]["measures"], ["Loft insulation"])

    def test_actual_source_over_input_limit_is_visible_failure_without_call(self):
        self.case(lambda c: c["home"].update(address="x" * 24000))
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.assertEqual(p["state"], "failed")
        self.assertIn("bounded input", p["reason"])
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(self.provider.calls, 0)

    def test_invalid_negative_configuration_remains_disabled_not_app_failure(self):
        disabled = Assistants(self.store, config(active_calls=-2, input_chars=-1))
        p = disabled.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.assertEqual(p["state"], "disabled")
        self.assertIn("Invalid bounded", p["reason"])
        disabled.start()
        self.assertEqual(disabled.threads, [])

class ReviewTests(Base):
    def test_material_only_staleness_accept_reject(self):
        for cap in REGISTRY:
            with self.subTest(cap=cap):
                p = self.verify(self.run_ready(cap))
                self.case(lambda c: c["contacts"].append(dict(note="Unrelated contact note")))
                p = self.service.detail(self.pm, p["id"])
                self.assertFalse(p["stale"])
                self.case(lambda c: c["home"].update(epc="F" if c["home"]["epc"] != "F" else "D"))
                p = self.service.detail(self.pm, p["id"])
                self.assertTrue(p["stale"])
                for act in ("accept", "edit-accept"):
                    with self.assertRaises(ValueError):
                        self.service.review(self.pm, p["id"], act, p["revision"], "Outdated.", proposal(p["snapshot"]))
                p = self.service.review(self.pm, p["id"], "reject", p["revision"], "Old sources retained.")
                self.assertEqual(p["state"], "rejected")

    def test_current_role_revocation_scope_on_invoke_list_detail_review(self):
        p = self.run_ready("stock-prioritisation")
        with self.service.transaction() as db:
            staff = dict(self.pm, role="Contractor")
            db.execute("UPDATE staff SET body=? WHERE email=?", (canonical(staff), self.pm["email"]))
        for op in (lambda: self.service.invoke(self.pm, "stock-prioritisation", "ZF-1"),
                   lambda: self.service.listing(self.pm), lambda: self.service.detail(self.pm, p["id"]),
                   lambda: self.verify(p)):
            with self.assertRaises(PermissionError):
                op()
        with self.service.transaction() as db:
            staff = dict(self.pm, case_ids=["ZF-2"])
            db.execute("UPDATE staff SET body=? WHERE email=?", (canonical(staff), self.pm["email"]))
        self.assertEqual(self.service.listing(self.pm)["proposals"], [])
        for op in (lambda: self.service.invoke(self.pm, "stock-prioritisation", "ZF-1"),
                   lambda: self.service.detail(self.pm, p["id"]), lambda: self.verify(p)):
            with self.assertRaises(PermissionError):
                op()

    def test_independent_qa_reviewer_and_separate_human_verification(self):
        self.case(lambda c: c.update(quality=[dict(measure="Loft insulation", state="Submitted",
                                                 recorded_by=self.pm["name"], recorded_by_code=self.pm["code"], items=[])]))
        p = self.run_ready("quality-evidence")
        with self.assertRaises(PermissionError):
            self.verify(p)
        qa = self.people["Quality Inspector"]
        p = self.verify(p, qa)
        with self.assertRaises(ValueError):
            self.service.review(qa, p["id"], "edit-accept", p["revision"], "Missing citations.",
                                {"summary": "x", "findings": [], "unknowns": []})
        p = self.service.review(qa, p["id"], "accept", p["revision"], "Proposal only.")
        self.assertEqual(p["state"], "accepted")
        c = json.loads(self.domain()[0][0][1])
        self.assertEqual(c["quality"][0]["state"], "Submitted")

    def test_verification_requires_explicit_true_and_same_reviewer(self):
        p = self.run_ready("stock-prioritisation")
        with self.assertRaises(ValueError):
            self.service.review(self.pm, p["id"], "verify", p["revision"], "No explicit attestation.")
        p = self.verify(p)
        rc = self.people["Retrofit Coordinator"]
        with self.assertRaises(ValueError):
            self.service.review(rc, p["id"], "accept", p["revision"], "Another person checked.")
        p = self.verify(p, rc)
        self.assertEqual(self.service.review(rc, p["id"], "accept", p["revision"], "Checked.")["state"], "accepted")

    def test_qa_independence_uses_current_identity_not_stale_request_copy(self):
        self.case(lambda c: c.update(quality=[dict(measure="Loft insulation", state="Submitted",
                                                 recorded_by="Renamed human", recorded_by_code="RENAMED", items=[])]))
        p = self.run_ready("quality-evidence")
        with self.service.transaction() as db:
            current = dict(self.pm, name="Renamed human", code="RENAMED")
            db.execute("UPDATE staff SET body=? WHERE email=?", (canonical(current), self.pm["email"]))
        with self.assertRaises(PermissionError):
            self.verify(p)

    def test_review_cas_between_independent_connections(self):
        p = self.run_ready("stock-prioritisation")
        other = self.other()
        self.verify(p)
        with self.assertRaises(ConflictError):
            other.review(self.pm, p["id"], "verify", p["revision"], "Lost review.", source_verified=True)

    def test_source_change_before_claim_does_not_dispatch(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.case(lambda c: c["home"].update(epc="F"))
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(self.service.detail(self.pm, p["id"])["state"], "stale")


class DurabilityTests(Base):
    def test_parallel_enqueue_unique_and_distinct_provenance(self):
        a, b = self.service, self.other()
        barrier = threading.Barrier(2)
        results = []

        def enqueue(s):
            barrier.wait()
            results.append(s.invoke(self.pm, "stock-prioritisation", "ZF-1")["id"])
        threads = [threading.Thread(target=enqueue, args=(s,)) for s in (a, b)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(5)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])
        self.assertEqual(len(a.detail(self.pm, results[0])["provenance"]), 2)

    def test_atomic_claim_two_connections_and_global_active_bound(self):
        other = self.other(active_calls=1)
        self.service.limits.active_calls = 1
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        q = self.service.invoke(self.pm, "assessment-preparation", "ZF-1")
        barrier = threading.Barrier(2)
        results = []

        def claim(s, tid):
            barrier.wait()
            results.append(s.claim(tid, uuid.uuid4().hex))
        threads = [threading.Thread(target=claim, args=(s, tid)) for s, tid in ((self.service, p["id"]), (other, q["id"]))]
        for t in threads:
            t.start()
        for t in threads:
            t.join(5)
        self.assertEqual(sum(x is not None for x in results), 1)
        with self.service.transaction() as db:
            self.assertEqual(db.execute("SELECT SUM(used_calls) FROM assistant_allowance").fetchone()[0], 1)

    def test_claim_race_same_task_only_one_owner(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        first = self.service.claim(p["id"], "one")
        self.assertIsNotNone(first)
        self.assertIsNone(self.other().claim(p["id"], "two"))

    def test_database_lease_renewal_takeover_late_completion_restart(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        first = self.service.claim(p["id"], "one")
        self.assertFalse(self.service.renew(p["id"], "other", first["fence"]))
        self.assertTrue(self.service.renew(p["id"], "one", first["fence"]))
        self.expire(p["id"])
        self.assertFalse(self.service.renew(p["id"], "one", first["fence"]))
        other = self.other()
        second = other.claim(p["id"], "two")
        self.assertEqual(second["fence"], first["fence"] + 1)
        env = dict(outcome="returned", source="ai", usage=None)
        self.assertFalse(self.service.complete(first, env, proposal(first["snapshot"])))
        self.assertTrue(other.complete(second, env, proposal(second["snapshot"])))
        self.assertFalse(other.complete(second, env, proposal(second["snapshot"])))
        self.assertEqual(self.other().detail(self.pm, p["id"])["state"], "ready")
        self.assertFalse(self.service.execute(p["id"]))

    def test_exhausted_attempts_no_third_call_and_retained_liability(self):
        p = self.service.invoke(self.pm, "funding-evidence", "ZF-1")
        self.service.claim(p["id"], "one")
        self.expire(p["id"])
        self.other().claim(p["id"], "two")
        self.expire(p["id"])
        self.assertIsNone(self.other().claim(p["id"], "three"))
        self.assertEqual(self.service.detail(self.pm, p["id"])["state"], "failed")
        with self.service.transaction() as db:
            row = db.execute("SELECT used_calls,reserved_tokens FROM assistant_allowance").fetchone()
            self.assertEqual(row, (2, 2 * self.service.limits.reservation))

    def test_last_budget_reservation_race(self):
        cfg = dict(call_allowance=1, token_allowance=12600)
        a, b = self.other(**cfg), self.other(**cfg)
        p = a.invoke(self.pm, "stock-prioritisation", "ZF-1")
        q = a.invoke(self.pm, "funding-evidence", "ZF-1")
        barrier = threading.Barrier(2)
        tasks = []

        def reserve(s, tid):
            barrier.wait()
            tasks.append(s.claim(tid, uuid.uuid4().hex))
        threads = [threading.Thread(target=reserve, args=(s, tid)) for s, tid in ((a, p["id"]), (b, q["id"]))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(5)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(sum(t is not None for t in tasks), 1)
        declined = p if a.detail(self.pm, p["id"])["state"] == "disabled" else q
        self.assertIn("allowance", b.detail(self.pm, declined["id"])["reason"])
        with a.transaction() as db:
            self.assertEqual(db.execute("SELECT used_calls,reserved_tokens FROM assistant_allowance").fetchone(), (1, 12600))
        self.assertIn("allowance", a.scan()["disabled"])
        self.assertIn("allowance", a.registry(self.pm)["disabled"])

    def test_retry_aggregate_reservation_usage_unknown_not_zero(self):
        self.provider.outcome, self.provider.usage = "timeout", False
        p = self.service.invoke(self.pm, "funding-evidence", "ZF-1")
        self.service.execute(p["id"])
        self.assertFalse(self.service.execute(p["id"]))  # database backoff
        self.expire(p["id"])
        self.provider.outcome, self.provider.usage = "returned", True
        self.service.execute(p["id"])
        self.assertEqual(self.provider.calls, 2)
        with self.service.transaction() as db:
            self.assertEqual(db.execute("SELECT used_calls,reserved_tokens FROM assistant_allowance").fetchone(),
                             (2, self.service.limits.reservation + 130))
            values = db.execute("SELECT actual FROM assistant_attempts ORDER BY fence").fetchall()
            self.assertEqual(values, [(None,), (130,)])

    def test_allowance_no_restart_daily_reset_or_expiry_extension(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.service.claim(p["id"], "one")
        other = self.other(call_allowance=1000, token_allowance=9000000, expires="2100-01-01T00:00:00Z")
        q = other.invoke(self.pm, "funding-evidence", "ZF-1")
        other.claim(q["id"], "two")
        with other.transaction() as db:
            self.assertEqual(db.execute("SELECT calls,tokens,expires FROM assistant_allowance").fetchone(),
                             (100, 2000000, self.service.limits.expiry))
        with other.transaction() as db:
            db.execute("UPDATE assistant_allowance SET expires=0")
        self.assertIsNone(other.claim(self.service.invoke(self.pm, "quality-evidence", "ZF-1")["id"], "three"))

    def test_uncertain_claim_and_completion_ack_lookup_not_reinference(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        claim, complete = self.service.claim, self.service.complete

        def lost_claim(*args):
            claim(*args)
            raise ConnectionError("lost acknowledgement")

        def lost_complete(*args):
            complete(*args)
            raise ConnectionError("lost acknowledgement")
        with patch.object(self.service, "claim", lost_claim), patch.object(self.service, "complete", lost_complete):
            self.assertTrue(self.service.execute(p["id"]))
        self.assertEqual(self.provider.calls, 1)
        self.assertEqual(self.service.detail(self.pm, p["id"])["state"], "ready")

    def test_blocked_provider_does_not_hold_domain_or_sql_lock(self):
        entered, release = threading.Event(), threading.Event()
        original = self.provider.evidence

        def blocked(*args):
            entered.set()
            release.wait(5)
            return original(*args)
        self.provider.evidence = blocked
        p = self.service.invoke(self.pm, "works-resident-coordination", "ZF-1")
        worker = threading.Thread(target=self.service.execute, args=(p["id"],))
        worker.start()
        self.assertTrue(entered.wait(2))
        finished = threading.Event()

        def manual():
            self.store.detail("ZF-1", self.pm)
            self.store.log_call(self.pm, "ZF-1", "Contacted", "Manual operation while model blocked.")
            self.service.listing(self.pm)
            finished.set()
        reader = threading.Thread(target=manual)
        reader.start()
        self.assertTrue(finished.wait(2))
        release.set()
        worker.join(5)
        reader.join(5)
        self.assertFalse(worker.is_alive())

    def test_scan_no_overlap_and_interruptible_worker_shutdown(self):
        self.service.scan_lock.acquire()
        self.assertEqual(self.service.scan()["disabled"], "Scan already in progress.")
        self.service.scan_lock.release()
        self.service.start()
        self.assertEqual(len(self.service.threads), self.service.limits.active_calls + 1)
        self.service.stop()
        self.assertTrue(all(not t.is_alive() for t in self.service.threads))

    def test_wall_clock_timeout_retains_physical_slot_and_liability(self):
        service = self.other(timeout=1, active_calls=1)
        release, returned = threading.Event(), threading.Event()
        original = self.provider.evidence

        def blocked(*args):
            try:
                release.wait(5)
                return original(*args)
            finally:
                returned.set()
        self.provider.evidence = blocked
        p = service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        started = time.monotonic()
        self.assertTrue(service.execute(p["id"]))
        self.assertLess(time.monotonic() - started, 2)
        current = service.detail(self.pm, p["id"])
        self.assertEqual(current["envelope"]["outcome"], "timeout")
        self.assertIsNone(current["envelope"]["usage"])
        q = service.invoke(self.pm, "funding-evidence", "ZF-1")
        self.assertFalse(service.execute(q["id"]))
        with service.transaction() as db:
            self.assertEqual(db.execute("SELECT used_calls,reserved_tokens FROM assistant_allowance").fetchone(),
                             (1, service.limits.reservation))
        release.set()
        self.assertTrue(returned.wait(2))
        time.sleep(0.05)
        self.assertEqual(service.detail(self.pm, p["id"])["state"], "pending")

    def test_expired_authority_scan_reactive_disabled_and_no_dispatch(self):
        expired = self.other(expires="2020-01-01T00:00:00Z")
        before = self.domain()
        self.assertIn("expired", expired.scan()["disabled"])
        for cap in REGISTRY:
            p = expired.invoke(self.pm, cap, "ZF-1")
            self.assertEqual(p["state"], "disabled")
            self.assertFalse(expired.execute(p["id"]))
        self.assertEqual(before, self.domain())
        self.assertEqual(self.provider.calls, 0)

    def test_history_and_list_pagination_current_authorization(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        with self.service.transaction() as db:
            for i in range(120):
                self.service.event(db, p["id"], kind="invocation", mode="proactive", actor=PURPOSE, test=i)
            for i in range(51):
                self.service._enqueue(db, "stock-prioritisation",
                                      dict(test_mvp.case(f"SYN-{i:03d}"), home=dict(test_mvp.case("x")["home"], epc=None)),
                                      "proactive", PURPOSE)
                # Case scope still requires a real case row, so register isolated fixture rows.
                row = db.execute("SELECT * FROM cases WHERE id='ZF-1'").fetchone()
                cols = [r[1] for r in db.execute("PRAGMA table_info(cases)").fetchall()]
                values = list(row)
                values[cols.index("id")] = f"SYN-{i:03d}"
                c = json.loads(values[cols.index("body")])
                c["id"], c["home"]["epc"] = f"SYN-{i:03d}", None
                values[cols.index("body")] = canonical(c)
                db.execute(f"INSERT INTO cases ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})", values)
        page = self.service.detail(self.pm, p["id"])
        self.assertEqual(len(page["provenance"]), 50)
        older = self.service.detail(self.pm, p["id"], page["history_next_offset"])
        self.assertEqual(len(older["provenance"]), 50)
        first = self.service.listing(self.pm)
        self.assertEqual(len(first["proposals"]), 50)
        second = self.service.listing(self.pm, after=first["next_after"])
        self.assertEqual(len(second["proposals"]), 2)
        self.assertFalse({x["id"] for x in first["proposals"]} & {x["id"] for x in second["proposals"]})
        with self.assertRaises(ValueError):
            self.service.listing(self.pm, after="not a cursor")

    def test_additive_migration_idempotent_old_store_ignores_new_tables(self):
        before = self.domain()
        self.run_ready("funding-evidence")
        Assistants(self.store, config())
        old = SqlStore(str(self.seed), str(self.dbpath))
        try:
            self.assertEqual(old.detail("ZF-1", self.pm)["home"]["epc"], "D")
        finally:
            old.db.close()
        self.assertEqual(before, self.domain())
        with self.service.transaction() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute("DELETE FROM assistant_events")

    def test_schema_failure_disables_assistance_not_manual_reads(self):
        with patch.object(self.store, "assistant_connection", side_effect=PermissionError("DDL not granted")):
            disabled = Assistants(self.store, config())
        self.assertIn("operator migration required", disabled.registry(self.pm)["disabled"])
        self.assertEqual(self.store.detail("ZF-1", self.pm)["home"]["epc"], "D")
        disabled.start()
        self.assertEqual(disabled.threads, [])
        with self.assertRaises(ValueError):
            disabled.invoke(self.pm, "stock-prioritisation", "ZF-1")


class DialectConnection:
    """T-SQL shape emulation, not real MSSQL/platform evidence."""
    def __init__(self, raw, statements):
        self.raw, self.statements = raw, statements

    def execute(self, sql, args=()):
        self.statements.append(sql)
        if sql.startswith("SET TRANSACTION ISOLATION LEVEL"):
            return self.raw.execute("SELECT 1")
        if "N'TR'" in sql or "sys.indexes" in sql:
            return self.raw.execute("SELECT 1")
        if sql.startswith("IF OBJECT_ID"):
            sql = sql[sql.index("CREATE TABLE"):]
            sql = sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS", 1)
            sql = re.sub(r"N?VARCHAR\((?:MAX|\d+)\)", "TEXT", sql)
            sql = sql.replace("BIGINT", "INTEGER")
        if "DATEDIFF_BIG" in sql:
            sql = "SELECT (julianday('now')-2440587.5)*86400.0"
        if " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY" in sql:
            sql = sql.replace(" OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", " LIMIT ? OFFSET ?")
            args = tuple(args[:-2]) + (args[-1], args[-2])
        sql = re.sub(r" OFFSET 0 ROWS FETCH NEXT (\?|\d+) ROWS ONLY", r" LIMIT \1", sql)
        return self.raw.execute(sql, args)

    def close(self):
        self.raw.close()


class DialectTests(Base):
    def test_mssql_sql_shapes_enqueue_claim_complete_review_scan(self):
        statements = []
        self.store._env = {}  # A dialect double; no environment or private SQL access.
        original = self.store.assistant_connection
        self.store.assistant_connection = lambda: DialectConnection(original(), statements)
        sql = Assistants(self.store, config())
        before = self.domain()
        for cap in REGISTRY:
            p = sql.invoke(self.pm, cap, "ZF-1")
            self.assertTrue(sql.execute(p["id"]))
            p = sql.detail(self.pm, p["id"])
            p = sql.review(self.pm, p["id"], "verify", p["revision"], "Compared sources.", source_verified=True)
            sql.review(self.pm, p["id"], "accept", p["revision"], "Proposal only.")
        sql.scan()
        self.assertEqual(before, self.domain())
        self.assertTrue(any("DATEDIFF_BIG" in s for s in statements))
        self.assertIn("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE", statements)
        self.assertTrue(any("OFFSET 0 ROWS FETCH NEXT" in s for s in statements))
        self.assertTrue(any("fence=?" in s and "lease_until>?" in s for s in statements))
        self.assertEqual(len(MSSQL_DDL), 4)


class ConfigurationTests(unittest.TestCase):
    def test_defaults_off_missing_authority_invalid_limits_expired(self):
        self.assertFalse(Limits({}).valid)
        self.assertFalse(Limits({}).proactive)
        for setting in (dict(active_calls=99), dict(attempts=0), dict(call_allowance=0),
                        dict(token_allowance=1), dict(lease=10, timeout=20),
                        dict(expires="not a date"), dict(expires="2099-01-01T00:00:00"), dict(authority="")):
            with self.subTest(setting=setting):
                self.assertFalse(Limits(config(**setting)).valid)

    def test_ai_envelope_preserves_actual_usage_and_missing_is_null(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self, size):
                return canonical(self.value).encode()
        response = Response()
        response.value = dict(model="model-id", choices=[dict(message=dict(content='{"x":1}'))],
                              usage=dict(prompt_tokens=10, completion_tokens=5, total_tokens=15))
        ai = Ai()
        ai.endpoint = "https://nonbillable.invalid"
        with patch.object(ai, "_token", return_value="test-only"), patch("urllib.request.urlopen", return_value=response):
            result = ai.evidence("system", "evidence")
            self.assertEqual(result["usage"]["total_tokens"], 15)
            self.assertEqual(result["model"], "model-id")
            response.value.pop("usage")
            self.assertIsNone(ai.evidence("system", "evidence")["usage"])
        with patch.object(ai, "_token", return_value="test-only"), patch("urllib.request.urlopen", side_effect=TimeoutError):
            result = ai.evidence("system", "evidence")
            self.assertEqual(result["outcome"], "timeout")
            self.assertIsNone(result["usage"])


class ApiTests(Base):
    def setUp(self):
        super().setUp()
        self.user = self.pm
        test = self

        class Identity:
            name = "password"

            def authenticate(self, headers):
                return test.user
        self.app = App(self.store, provider=Identity())
        self.app.assistants = self.service
        self.http = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.http.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.http.server_port}"

    def tearDown(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
        super().tearDown()

    def request(self, path, body=None):
        request = urllib.request.Request(self.url + path, data=canonical(body).encode() if body is not None else None,
                                         headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)

    def test_registry_invoke_list_detail_separate_review_and_denials(self):
        self.assertEqual(self.request("/api/assistants")[0], 200)
        for cap in REGISTRY:
            status, p = self.request(f"/api/assistants/{cap}/invoke", {"case_id": "ZF-1"})
            self.assertEqual(status, 202)
            self.service.execute(p["id"])
            self.assertEqual(self.request("/api/assistants/proposals")[0], 200)
            p = self.request(f"/api/assistants/proposals/{p['id']}")[1]
            self.assertEqual(self.request(f"/api/assistants/proposals/{p['id']}/review", {
                "action": "accept", "revision": p["revision"], "note": "Not checked."})[0], 400)
            p = self.request(f"/api/assistants/proposals/{p['id']}/review", {
                "action": "verify", "revision": p["revision"], "note": "Compared sources.", "source_verified": True})[1]
            self.assertEqual(self.request(f"/api/assistants/proposals/{p['id']}/review", {
                "action": "accept", "revision": p["revision"], "note": "Proposal only."})[0], 200)
        self.user = self.people["Contractor"]
        for path in ("/api/assistants", "/api/assistants/proposals", f"/api/assistants/proposals/{p['id']}"):
            self.assertEqual(self.request(path)[0], 403)
        self.assertEqual(self.request("/api/assistants/funding-evidence/invoke", {"case_id": "ZF-1"})[0], 403)
        self.user = self.people["Resident Liaison Officer"]
        self.assertEqual(self.request(f"/api/assistants/proposals/{p['id']}")[0], 403)
        self.assertEqual(self.request("/api/assistants/stock-prioritisation/invoke", {"case_id": "ZF-1"})[0], 403)
        self.user = self.people["Unknown"]
        self.assertEqual(self.request("/api/assistants")[0], 403)

    def test_invalid_payload_and_store_failure_leave_manual_api_available(self):
        for payload in ([], {"case_id": {}}, {"case_id": "x" * 100}):
            self.assertEqual(self.request("/api/assistants/stock-prioritisation/invoke", payload)[0], 400)
        with patch.object(self.service, "listing", side_effect=ConnectionError):
            status, body = self.request("/api/assistants/proposals")
            self.assertEqual(status, 503)
            self.assertIn("ordinary case work manually", body["error"])
        self.assertEqual(self.request("/api/cases/ZF-1")[0], 200)


if __name__ == "__main__":
    unittest.main()
