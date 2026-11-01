"""Release admission for the five assistants and retained legacy dispatch (issue #107). Constructed fixtures only."""
import copy
import json
import time
import unittest
from unittest.mock import patch

import release_support
from test_assistants import Base, config
from zava_forward.core import assistant_release as rel
from zava_forward.core import ai_registry, assistants, quality, ranking
from zava_forward.core.ai import Ai

CAP = "stock-prioritisation"


def dependent_policy(kind):
    """Construct policy-content changes without changing production rules or labels."""
    if kind == "ranking":
        value = copy.deepcopy(ranking.CURRENT)
        value["stage_order"].reverse()
        value["content_hash"] = ranking.policy_hash(value)
        return patch.object(ranking, "CURRENT", value)
    value = copy.deepcopy(quality.CHECKLISTS)
    value["General"]["items"].append("Constructed additional evidence check")
    return patch.object(quality, "CHECKLISTS", value)


class DependentPolicyRelease(Base):
    def test_policy_content_invalidates_only_dependent_task_bindings(self):
        ai = Ai()
        before = {cap: assistants.runtime_binding(cap, self.provider) for cap in assistants.REGISTRY}
        legacy = {task: ai_registry.legacy_binding(task, ai, ai_registry.legacy_deployment(task, ai))
                  for task in ai_registry.LEGACY}
        for kind, affected in (("ranking", CAP), ("quality", "quality-evidence")):
            release_support.install(self.store)
            with self.subTest(kind=kind), dependent_policy(kind):
                for cap, binding in before.items():
                    current = assistants.runtime_binding(cap, self.provider)
                    self.assertEqual(current == binding, cap != affected, cap)
                    if cap == affected:
                        self.assertNotEqual(current["policy_version"], binding["policy_version"])
                for task, binding in legacy.items():
                    current = ai_registry.legacy_binding(task, ai, ai_registry.legacy_deployment(task, ai))
                    self.assertEqual(current == binding, not (kind == "ranking" and task == "priority"), task)
                with self.service.transaction() as db:
                    denied = self.service.admission(db, affected)
                    self.assertIsNotNone(denied)
                    self.assertIn("policy_version", denied["missing"])

    def test_quality_mapping_and_first_match_order_require_release_without_source_change(self):
        case = copy.deepcopy(self.store.cases["ZF-1"])
        case["measures"] = ["Constructed generic measure"]
        for mode in ("mapping-only", "order-only"):
            initial = quality._KEYWORDS + (("loft", "Heat pump"),)
            changed = (("unmatched", "Loft insulation"),) + initial if mode == "mapping-only" else (
                initial[-1], *initial[:-1])
            with self.subTest(mode=mode), patch.object(quality, "_KEYWORDS", initial):
                release_support.install(self.store)
                before = {cap: assistants.runtime_binding(cap, self.provider) for cap in assistants.REGISTRY}
                ai = Ai()
                legacy = {t: ai_registry.legacy_binding(t, ai, ai_registry.legacy_deployment(t, ai))
                          for t in ai_registry.LEGACY}
                # This case still selects General; source staleness cannot hide an admission gap.
                snapshot = assistants.capture("quality-evidence", case)
                with patch.object(quality, "_KEYWORDS", changed):
                    self.assertEqual(assistants.capture("quality-evidence", case), snapshot)
                    for cap, binding in before.items():
                        self.assertEqual(assistants.runtime_binding(cap, self.provider) == binding,
                                         cap != "quality-evidence", cap)
                    for t, binding in legacy.items():
                        self.assertEqual(ai_registry.legacy_binding(t, ai, ai_registry.legacy_deployment(t, ai)), binding)
                    with self.service.transaction() as db:
                        denied = self.service.admission(db, "quality-evidence")
                        self.assertIsNotNone(denied)
                        self.assertIn("policy_version", denied["missing"])

    def test_stock_capture_uses_current_policy_object(self):
        with dependent_policy("ranking"):
            snapshot = assistants.capture(CAP, self.store.cases["ZF-1"])
            self.assertEqual(snapshot["sources"]["ranking"]["policy"]["content_hash"],
                             ranking.CURRENT["content_hash"])

    def test_ranking_binding_hashes_content_not_only_declared_version_or_hash(self):
        ai = Ai()
        stock = assistants.runtime_binding(CAP, self.provider)
        priority = ai_registry.legacy_binding("priority", ai, ai.strong)
        changed = copy.deepcopy(ranking.CURRENT)
        changed["stage_order"].reverse()
        with patch.object(ranking, "CURRENT", changed):
            self.assertNotEqual(assistants.runtime_binding(CAP, self.provider)["policy_version"],
                                stock["policy_version"])
            self.assertNotEqual(ai_registry.legacy_binding("priority", ai, ai.strong)["policy_version"],
                                priority["policy_version"])

    def test_changed_policy_denies_fresh_proactive_and_queued_dispatch(self):
        self.case(lambda c: c["home"].update(epc="Unknown"))
        for kind, cap in (("ranking", CAP), ("quality", "quality-evidence")):
            release_support.install(self.store)
            queued = self.service.invoke(self.pm, cap, "ZF-1")
            with self.subTest(kind=kind), dependent_policy(kind):
                fresh = self.service.invoke(self.pm, cap, "ZF-1")
                self.assertEqual(fresh["state"], "disabled")
                self.assertIn("policy_version", fresh["release_denial"]["missing"])
                self.assertFalse(self.other().execute(queued["id"]))
                scanned = self.service.scan()["enqueued"]
                affected = [self.service.detail(self.pm, tid) for tid in scanned
                            if self.service.detail(self.pm, tid)["capability"] == cap]
                self.assertTrue(affected)
                self.assertTrue(all(p["state"] == "disabled" for p in affected))
                self.assertIn("policy_version", self.service.detail(self.pm, queued["id"])["release_denial"]["missing"])
        self.assertEqual(self.provider.calls, 0)

    def test_policy_change_quarantines_inflight_and_denies_ready_verified_accepted_reliance(self):
        for kind, cap in (("ranking", CAP), ("quality", "quality-evidence")):
            for state in ("leased", "ready", "verified", "accepted"):
                with self.subTest(kind=kind, state=state):
                    release_support.install(self.store)
                    self.case(lambda c: c["home"].update(built=c["home"]["built"] + 1))
                    if state == "leased":
                        queued = self.service.invoke(self.pm, cap, "ZF-1")
                        p = self.service.claim(queued["id"], "constructed-worker")
                        output = assistants_proposal(p)
                    else:
                        p = self.run_ready(cap)
                        if state in ("verified", "accepted"):
                            p = self.verify(p)
                        if state == "accepted":
                            p = self.service.review(self.pm, p["id"], "accept", p["revision"], "Synthetic source comparison")
                        output = p["output"]
                    before = self.domain()
                    with dependent_policy(kind):
                        if state == "leased":
                            self.assertTrue(self.service.complete(
                                p, dict(outcome="returned", source="ai", model="test-model", usage=None), output))
                        other = self.other()
                        view = other.detail(self.pm, p["id"])
                        self.assertFalse(view["actionable"])
                        self.assertFalse(view["relied_on"])
                        self.assertIn("policy_version", view["release_denial"]["missing"])
                        if state == "leased":
                            self.assertEqual(view["state"], "quarantined")
                            self.assertIsNone(view["output"])
                        else:
                            self.assertEqual(view["output"], output)
                        for action in ("verify", "accept", "edit-accept"):
                            with self.assertRaises(PermissionError):
                                other.review(self.pm, p["id"], action, view["revision"],
                                             "Synthetic comparison", output=output, source_verified=True)
                    self.assertEqual(self.domain(), before)

    def test_matching_constructed_renewal_is_proposal_only_and_does_not_revive_history(self):
        self.service.approvers = {self.pm["email"].lower()}
        for kind, cap in (("ranking", CAP), ("quality", "quality-evidence")):
            old = self.run_ready(cap)
            before = self.domain()
            with self.subTest(kind=kind), dependent_policy(kind):
                record = release_support.fixture(cap, assistants.runtime_binding(cap, self.provider),
                                                 expires="2099-01-01T00:00:00Z")
                rid = self.service.record_release(self.pm, record)["id"]
                fresh = self.run_ready(cap)
                self.assertEqual(fresh["release"]["id"], rid)
                self.assertNotEqual(fresh["id"], old["id"])
                fresh = self.verify(fresh)
                accepted = self.service.review(self.pm, fresh["id"], "accept", fresh["revision"],
                                               "Synthetic review, not actual approval")
                self.assertEqual(accepted["state"], "accepted")
                self.assertFalse(self.service.detail(self.pm, old["id"])["actionable"])
                self.assertEqual(self.domain(), before)
            # Returning to the old policy cannot revive the superseded release.
            with self.service.transaction() as db:
                self.assertIsNotNone(self.service.admission(db, cap))

    def test_retained_priority_policy_change_denies_dispatch_and_quarantines_completion(self):
        ai = Ai()
        ai.endpoint = "http://scripted-model.invalid"
        self.store.ai = ai
        ai.gate = lambda task, dep=None: self.store.continuity_block(task) or self.store.release_block(task, dep)
        release_support.install(self.store, ai, tasks=[])
        calls = []
        ai._chat = lambda *a, **k: calls.append(1) or "Synthetic result"
        with dependent_policy("ranking"):
            result = ai.run("priority", "s", "u", "manual", strong=True)
            self.assertEqual(result["source"], "template")
            self.assertIn("policy_version", result["reason"])
            self.assertEqual(calls, [])
            self.assertEqual(ai.run("summary", "s", "u", "manual")["source"], "ai")
        with dependent_policy("ranking") as changed:
            changed_policy = copy.deepcopy(changed)
        def chat(*a, **k):
            ranking.CURRENT = changed_policy
            return "Synthetic superseded result"
        ai._chat = chat
        with patch.object(ranking, "CURRENT", ranking.CURRENT):
            result = ai.run("priority", "s", "u", "manual", strong=True)
            self.assertEqual(result["source"], "template")
            self.assertTrue(result["quarantined"])

    def test_retained_priority_policy_change_blocks_historical_accept_and_edit(self):
        ai = Ai()
        ai.endpoint = "http://scripted-model.invalid"
        self.store.ai = ai
        ai.gate = lambda task, dep=None: self.store.continuity_block(task) or self.store.release_block(task, dep)
        release_support.install(self.store, ai, tasks=[])
        user = TaskReleaseRecord.priority_user(self, self.store)
        ai._chat = lambda *a, **k: json.dumps([
            dict(case_id="ZF-4", reason="Safety", cites=["Open safety issues: 1"])])
        proposal = self.store.ai_priority(user, 1)
        self.assertEqual(proposal["source"], "ai")
        before = copy.deepcopy(self.store.data["recommendations"])
        with dependent_policy("ranking"):
            self.assertFalse(self.store.latest_priority(user)["actionable"])
            self.assertFalse(self.store.latest_priority(user)["relied_on"])
            for action in ("accept", "edit"):
                with self.assertRaises(PermissionError):
                    self.store.resolve_priority(user, proposal["id"], action,
                                                "SYN scripted review", proposal["items"])
            self.assertEqual(self.store.data["recommendations"], before)


def body(service, **over):
    b = dict(release_support.fixture(CAP, assistants.runtime_binding(CAP, service.store.ai)),
             task=CAP, evidence_class="constructed-fixture",
             evidence=["constructed-fixture:synthetic-demo"], residual_risk_decision="Accept",
             residual_risk_note="Constructed fixture only.", serving_model="test-model", expires="2099-01-01T00:00:00Z")
    b.update(over)
    return b


class Release(Base):
    def drop(self):
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_releases")

    def events(self, tid):
        with self.service.transaction() as db:
            return [e[0] for e in db.execute("SELECT body FROM assistant_events WHERE task_id=?", (tid,)).fetchall()]

    def test_absent_release_denies_with_zero_calls_and_retains_denial(self):
        self.drop()
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertEqual(p["state"], "disabled")
        self.assertIn(rel.OWNER, p["reason"])
        self.assertIn("manual route", p["reason"].lower())
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(self.provider.calls, 0)
        self.assertTrue(any(rel.OWNER in e or "invocation" in e for e in self.events(p["id"])))
        self.assertEqual(self.service.registry(self.pm)["assistants"][0]["release"]["missing"],
                         ["approved, unexpired release record"])

    def test_disabled_chat_task_is_listed_without_binding_or_release(self):
        chat = next(t for t in self.service.registry(self.pm)["registered_tasks"] if t["id"] == "chat-case-conversation")
        self.assertFalse(chat["enabled"])
        self.assertIsNone(chat["binding"])
        self.assertIsNone(chat["release"])
        self.assertTrue(chat["release_denial"]["missing"])

    def test_scan_is_denied_without_release(self):
        self.drop()
        self.service.scan()
        self.assertEqual(self.provider.calls, 0)

    def test_record_requires_named_approver_manager_and_accept(self):
        with self.assertRaises(PermissionError):
            self.service.record_release(self.pm, body(self.service))
        svc = self.other(release_approvers="x")
        svc.approvers = {self.pm["email"].lower()}
        with self.assertRaises(PermissionError):
            svc.record_release(self.people["Retrofit Coordinator"], body(svc))
        with self.assertRaises(ValueError):
            svc.record_release(self.pm, body(svc, residual_risk_decision="Reject"))
        with self.assertRaises(ValueError):
            svc.record_release(self.pm, body(svc, evidence=[]))
        with self.assertRaises(ValueError):
            svc.record_release(self.pm, body(svc, expires="2001-01-01T00:00:00Z"))
        rid = svc.record_release(self.pm, body(svc))["id"]
        self.assertTrue(rid)

    def test_contractor_and_unknown_cannot_record_invoke_or_read(self):
        self.service.approvers = {p["email"] for p in self.people.values()}
        for role in ("Contractor", "Unknown"):
            with self.assertRaises(PermissionError):
                self.service.record_release(self.people[role], body(self.service))
            with self.assertRaises(PermissionError):
                self.service.invoke(self.people[role], CAP, "ZF-1")
            with self.assertRaises(PermissionError):
                self.service.listing(self.people[role])

    def test_expired_suspended_revoked_deny_and_revoked_is_terminal(self):
        self.service.approvers = {self.pm["email"].lower()}
        with self.service.transaction() as db:
            now = self.service.now(db)
            self.assertIsNone(self.service.admission(db, CAP))
            db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (rel.canonical(dict(
                rel.releases(db, CAP)[0], expires=now - 1)), f"fx-{CAP}"))
            self.assertIn("unexpired", self.service.admission(db, CAP)["missing"][-1])
        rid = self.service.record_release(self.pm, body(self.service))["id"]
        self.service.change_release(self.pm, rid, "suspended", "incident")
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertEqual(p["state"], "disabled")
        self.service.change_release(self.pm, rid, "revoked", "withdrawn")
        with self.assertRaises(ValueError):
            self.service.change_release(self.pm, rid, "suspended", "again")
        with self.service.transaction() as db:
            self.assertEqual([r["status"] for r in rel.releases(db, CAP) if r["id"] == rid], ["revoked"])
        self.assertEqual(self.provider.calls, 0)

    def test_material_mismatch_denies_but_routine_case_edit_only_stales(self):
        p = self.run_ready(CAP)
        for patch_target, value in ((assistants, "RULE_VERSION"), (assistants, "SYSTEM"), (assistants, "PROVENANCE")):
            with patch.object(patch_target, value, "changed-" + value):
                detail = self.service.detail(self.pm, p["id"])
                self.assertEqual(detail["display_state"], "release-denied", value)
                self.assertFalse(detail["actionable"])
                with self.assertRaises(PermissionError):
                    self.verify(p)
                with self.service.transaction() as db:
                    self.assertIn("no approved release matches", self.service.admission(db, CAP)["reason"])
                self.assertNotEqual(self.service.detail(self.pm, p["id"])["release_denial"]["missing"],
                                    ["approved, unexpired release record"])
            # Restoring the binding alone does not revive the revoked record.
            self.assertIsNotNone(self.service.detail(self.pm, p["id"])["release_denial"])
            release_support.install(self.store)
        with patch.dict(assistants.REGISTRY[CAP], {"roles": (assistants.RC,)}):
            with self.service.transaction() as db:
                self.assertIn("permission_version", self.service.admission(db, CAP)["missing"])
        release_support.install(self.store)
        p = self.run_ready(CAP)
        self.case(lambda c: c["home"].update(epc="G"))
        detail = self.service.detail(self.pm, p["id"])
        self.assertIsNone(detail["release_denial"])
        self.assertTrue(detail["stale"])

    def test_invalidation_first_seen_by_denied_review_persists_and_is_not_revived(self):
        p = self.run_ready(CAP)
        with patch.object(assistants, "RULE_VERSION", "changed-rule"):
            with self.assertRaises(PermissionError):
                self.verify(p)
        with self.service.transaction() as db:
            rows = rel.releases(db, CAP)
            events = [json.loads(b) for (b,) in db.execute(
                "SELECT body FROM assistant_events WHERE task_id=?", (rows[0]["id"],)).fetchall()]
        self.assertEqual([r["status"] for r in rows], ["revoked"])
        self.assertTrue(any(e.get("kind") == "release-revoked" for e in events))
        denied = self.service.detail(self.pm, p["id"])["release_denial"]
        self.assertIsNotNone(denied)
        self.assertIn("policy_version", denied["missing"])

    def test_revocation_on_independent_connection_blocks_dispatch_and_reliance(self):
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        other = self.other()
        other.approvers = {self.pm["email"].lower()}
        other.change_release(self.pm, f"fx-{CAP}", "revoked", "withdrawn")
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(self.service.detail(self.pm, p["id"])["state"], "disabled")
        # A restarted process cannot revive the approval or the denied task.
        again = self.other()
        self.assertFalse(again.execute(p["id"]))
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(again.export()["proposals"][0]["relied_on"], False)

    def test_revocation_between_claim_and_completion_quarantines(self):
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        task = self.service.claim(p["id"], "one")
        self.service.change_release(self.pm, f"fx-{CAP}", "revoked", "withdrawn")
        env = dict(outcome="returned", source="ai", usage=None, model="test-model")
        self.assertTrue(self.service.complete(task, env, assistants_proposal(task)))
        v = self.service.detail(self.pm, p["id"])
        self.assertEqual(v["state"], "quarantined")
        self.assertIsNone(v["output"])

    def test_unexpected_serving_model_quarantines_and_suspends_release(self):
        original = self.provider.evidence

        def other_model(*a, **k):
            r = original(*a, **k)
            r["model"] = "surprise-model-2"
            return r
        self.provider.evidence = other_model
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertTrue(self.service.execute(p["id"]))
        v = self.service.detail(self.pm, p["id"])
        self.assertEqual(v["state"], "quarantined")
        self.assertIsNone(v["output"])
        self.assertEqual(v["serving_attestation"]["returned"], "surprise-model-2")
        with self.service.transaction() as db:
            self.assertEqual(rel.releases(db, CAP)[0]["status"], "suspended")
        self.assertEqual(self.service.invoke(self.pm, CAP, "ZF-1")["state"], "disabled")
        self.assertEqual(self.service.detail(self.pm, p["id"])["state"], "quarantined")

    def test_live_provider_needs_actual_release_with_serving_proof(self):
        binding = assistants.runtime_binding(CAP, self.provider)
        fx = release_support.fixture(CAP, binding)
        with self.service.transaction() as db:
            db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (rel.canonical(fx), f"fx-{CAP}"))
            now = self.service.now(db)
            self.assertIsNone(rel.admission(db, CAP, binding, now, live=False))
            denied = rel.admission(db, CAP, binding, now, live=True)
            self.assertIn("actual authorisation with serving-version attestation", denied["missing"])
            binding["model_version"] = "test-model"
            db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (rel.canonical(dict(fx, evidence_class="actual", model_version="test-model")), f"fx-{CAP}"))
            self.assertIsNone(rel.admission(db, CAP, binding, now, live=True))

    def test_no_controlled_domain_write_from_release_or_proposal(self):
        before = self.domain()
        self.run_ready(CAP)
        self.assertEqual(before, self.domain())

    def test_shared_ddl_is_portable(self):
        for ddl in rel.SQLITE_DDL + rel.MSSQL_DDL:
            for banned in ("AUTOINCREMENT", "INSERT OR", "PRAGMA"):
                self.assertNotIn(banned, ddl)


class Legacy(Base):
    def test_configured_legacy_dispatch_needs_a_matching_actual_release(self):
        ai = Ai()
        ai.endpoint = "http://scripted-model.invalid"
        calls = []
        ai._chat = lambda *a, **k: calls.append(1) or "All good today."
        self.store.ai = ai
        ai.gate = lambda task, dep=None: self.store.continuity_block(task) or self.store.release_block(task, dep)
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_releases WHERE capability LIKE 'legacy:%'")
        r = ai.run("briefing", "s", "u", "template")
        self.assertEqual((r["source"], calls), ("template", []))
        self.assertIn("release admission denied", r["reason"].lower())
        release_support.install(self.store, ai, tasks=[])
        self.assertEqual(ai.run("briefing", "s", "u", "template")["source"], "ai")
        with self.service.transaction() as db:
            db.execute("UPDATE assistant_releases SET status='revoked' WHERE id=?", (f"fx-legacy-briefing-{ai.fast}",))
        self.assertEqual(ai.run("briefing", "s", "u", "template")["source"], "template")

    def legacy_ai(self):
        ai = Ai()
        ai.endpoint = "http://scripted-model.invalid"
        ai._chat = lambda *a, **k: "All good today."
        self.store.ai = ai
        ai.gate = lambda task, dep=None: self.store.continuity_block(task) or self.store.release_block(task, dep)
        return ai

    def test_gate_binds_the_deployment_actually_called(self):
        ai = self.legacy_ai()
        release_support.install(self.store, ai, tasks=[])
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_releases WHERE id LIKE ?", (f"fx-legacy-%-{ai.strong}",))
        self.assertEqual(ai.run("briefing", "s", "u", "template")["source"], "ai")
        self.assertEqual(ai.run("briefing", "s", "u", "template", strong=True)["source"], "template")
        self.assertEqual(ai.look_at("a.txt", b"x", "text/plain")["source"], "template")

    def test_legacy_release_binds_versions(self):
        ai = self.legacy_ai()
        release_support.install(self.store, ai, tasks=[])
        with self.service.transaction() as db:
            for rid, body in db.execute("SELECT id,body FROM assistant_releases WHERE capability='legacy:summary'").fetchall():
                rec = json.loads(body)
                rec["prompt_version"] = "stale"
                db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (rel.canonical(rec), rid))
        self.assertEqual(ai.run("summary", "s", "u", "template")["source"], "template")
        self.assertEqual(ai.run("briefing", "s", "u", "template")["source"], "ai")

    def test_legacy_completion_recheck_discards_result_after_revocation(self):
        ai = self.legacy_ai()
        release_support.install(self.store, ai, tasks=[])

        def chat(*a, **k):
            with self.service.transaction() as db:
                db.execute("UPDATE assistant_releases SET status='revoked' WHERE capability='legacy:briefing'")
            return "All good today."
        ai._chat = chat
        r = ai.run("briefing", "s", "u", "template")
        self.assertEqual((r["source"], r.get("quarantined")), ("template", True))


class TaskReleaseRecord(Base):
    def setUp(self):
        super().setUp()
        self.service.approvers = {self.pm["email"].lower()}

    def priority_user(self, store):
        """Assign synthetic work to the registered coordinator without forging identity."""
        user = self.people[assistants.RC]
        with store.lock:
            old_owner = store._case("ZF-1")["owner_code"]
            for case in store.cases.values():
                if case["owner_code"] == old_owner:
                    store._case(case["id"]).update(
                        owner_code=user["code"], owner=user["name"], owner_role=user["role"])
            store.save()
        return user

    def test_priority_review_refuses_forged_identity_without_writes(self):
        from zava_forward.core.store import Store
        json_store = Store(str(self.seed), str(self.root / "identity-live.json"),
                           str(self.root / "identity-audit.jsonl"))
        for store in (self.store, json_store):
            store.ai = Ai()
            user = self.priority_user(store)
            out = store.ai_priority(user, 1, mode="workflow-only")
            before = json.dumps(store.data, sort_keys=True)
            for field in ("code", "email", "name", "role", "oid"):
                for action in ("accept", "edit", "reject"):
                    with self.subTest(store=type(store).__name__, field=field, action=action):
                        with self.assertRaisesRegex(PermissionError, "Current registered named staff"):
                            store.resolve_priority(dict(user, **{field: "forged"}), out["id"],
                                                   action, "Review", out["items"])
                        self.assertEqual(json.dumps(store.data, sort_keys=True), before)
            self.assertEqual(store.resolve_priority(user, out["id"], "reject", "Manual route")["status"],
                             "Rejected")

    def test_priority_fixture_ownership_survives_reopen_for_every_matching_case(self):
        from zava_forward.core.sqlstore import SqlStore
        from zava_forward.core.store import Store
        json_store = Store(str(self.seed), str(self.root / "ownership-live.json"),
                           str(self.root / "ownership-audit.jsonl"))
        for store in (self.store, json_store):
            with store.lock:
                old_owner = store.cases["ZF-1"]["owner_code"]
                expected = {c["id"] for c in store.cases.values() if c["owner_code"] == old_owner}
            self.assertGreater(len(expected), 1)
            user = self.priority_user(store)
            if isinstance(store, SqlStore):
                reopened = SqlStore(str(self.seed), str(store.db_path))
                self.addCleanup(reopened.db.close)
            else:
                reopened = Store(str(self.seed), store.live_path, store.audit_path)
            for cid in expected:
                self.assertEqual(
                    {key: reopened.cases[cid][key] for key in ("owner_code", "owner", "owner_role")},
                    dict(owner_code=user["code"], owner=user["name"], owner_role=user["role"]),
                )
            before = store.ai_priority(user, 10, mode="workflow-only")
            after = reopened.ai_priority(user, 10, mode="workflow-only")
            self.assertEqual(before["case_ids"], after["case_ids"])
            self.assertEqual(before["deterministic"], after["deterministic"])

    def test_contract_fields_required_on_authenticated_record_route(self):
        for key in ("release_version", "intended_use", "prohibited_uses", "affected_stakeholders",
                    "accountable_owner", "impact_assessment", "material_change_triggers", "evaluation_decision"):
            b = body(self.service)
            del b[key]
            with self.subTest(field=key), self.assertRaises(ValueError):
                self.service.record_release(self.pm, b)
        self.assertIn("OQ-017", rel.denial("missing", ["evidence"], CAP)["authority_gap"])

    def test_each_binding_mismatch_denies_reactive_and_proactive_with_no_calls(self):
        for key in rel.BOUND:
            with self.subTest(field=key):
                release_support.install(self.store)
                with self.service.transaction() as db:
                    r = rel.releases(db, CAP)[0]
                    r[key] = "changed"
                    db.execute("UPDATE assistant_releases SET body=? WHERE id=?",
                               (rel.canonical(r), r["id"]))
                p = self.service.invoke(self.pm, CAP, "ZF-1")
                self.assertEqual(p["state"], "disabled")
                self.assertIn(key, p["release_denial"]["missing"])
                self.assertFalse(self.service.execute(p["id"]))
                self.service.scan()
                self.assertEqual(self.provider.calls, 0)

    def test_renewal_creates_fresh_id_and_invalidates_history_without_domain_write(self):
        self.case(lambda c: c["home"].update(epc="Unknown"))
        before = self.domain()
        old = self.run_ready(CAP)
        rid = self.service.record_release(self.pm, body(self.service, release_version="v2",
                                                      evidence=["fixture:renewed-evaluation"]))["id"]
        denied = self.service.detail(self.pm, old["id"])
        self.assertFalse(denied["actionable"])
        with self.assertRaises(PermissionError):
            self.verify(old)
        fresh = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertNotEqual(fresh["id"], old["id"])
        self.assertEqual(fresh["release"]["id"], rid)
        self.assertEqual(self.service.invoke(self.pm, CAP, "ZF-1")["id"], fresh["id"])
        self.assertIn(fresh["id"], self.service.scan()["enqueued"])
        self.assertTrue(self.service.execute(fresh["id"]))
        self.assertEqual(self.service.detail(self.pm, old["id"])["output"], old["output"])
        self.assertEqual(self.domain(), before)
        with self.service.transaction() as db:
            self.assertEqual(next(r for r in rel.releases(db, CAP) if r["id"] == old["release"]["id"])["status"], "revoked")

    def test_endpoint_rollback_does_not_revive_historical_release(self):
        self.service.record_release(self.pm, body(self.service))
        self.provider.endpoint = "new-route"
        self.service.record_release(self.pm, body(self.service, release_version="v2"))
        self.provider.endpoint = "local-test"
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertEqual(p["state"], "disabled")
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(self.provider.calls, 0)
        self.assertEqual(self.service.invoke(self.pm, "assessment-preparation", "ZF-1")["state"], "pending")

    def legacy(self):
        ai = Ai()
        ai.endpoint = "http://scripted-model.invalid"
        self.store.ai = ai
        ai.gate = lambda task, dep=None: self.store.continuity_block(task) or self.store.release_block(task, dep)
        release_support.install(self.store, tasks=[])
        return ai

    def test_actual_prompt_change_invalidates_each_retained_route(self):
        from zava_forward.core import ai_prompts, ai_registry
        ai = self.legacy()
        calls = []
        ai._chat = lambda *a, **k: calls.append(1) or "All good today."
        for task in ai_registry.LEGACY:
            with self.subTest(task=task):
                system, user = ai_prompts.PROMPTS[task]
                with patch.dict(ai_prompts.PROMPTS, {task: (system + " Changed instruction.", user)}):
                    r = (ai.look_at("fixture.txt", b"synthetic", "text/plain") if task == "read_document"
                         else ai.run(task, "s", "u", "template", strong=task in ("priority", "funding_draft")))
                    self.assertEqual(r["source"], "template")
        self.assertEqual(calls, [])
        r = ai.run("summary", "s", "u", "template")
        self.assertEqual(r["prompt_version"], ai_registry.legacy_binding("summary", ai, ai.fast)["prompt_version"])
        self.assertTrue(r["release"]["id"])

    def test_legacy_replacement_during_call_quarantines_even_matching_binding(self):
        ai = self.legacy()
        def chat(*a, **k):
            release_support.install(self.store, tasks=[], evidence=["fixture:new-evaluation"])
            return "Do not rely on this superseded result."
        ai._chat = chat
        r = ai.run("briefing", "s", "u", "template")
        self.assertTrue(r["quarantined"])
        self.assertEqual(r["source"], "template")

    def test_cached_briefing_and_both_legacy_review_paths_recheck_release(self):
        ai = self.legacy()
        user = self.priority_user(self.store)
        ai._chat = lambda *a, **k: "- Fact [[Stage: Contacting resident]]"
        ordinary = self.store.ai_run(user, "ZF-1", "summary")
        briefing = self.store.briefing(user)
        ai._chat = lambda *a, **k: json.dumps([dict(case_id="ZF-4", reason="Safety", cites=["Open safety issues: 1"])])
        priority = self.store.ai_priority(user, 1)
        with self.service.transaction() as db:
            db.execute("UPDATE assistant_releases SET status='revoked' WHERE capability LIKE 'legacy:%'")
        self.assertEqual(self.store.briefing(user)["source"], "template")
        self.assertFalse(self.store.latest_priority(user)["actionable"])
        for action in ("accept", "edit"):
            with self.assertRaises(PermissionError):
                self.store.review_ai(user, ordinary["record_id"], action, "Review", "Edited")
            audit_before = len(list(self.store.audit_entries()))
            with self.assertRaises(PermissionError):
                self.store.resolve_priority(user, priority["id"], action, "Review", [])
            self.assertEqual(
                [e["action"] for e in list(self.store.audit_entries())[audit_before:]],
                ["ai_release_denied"],
            )
        self.assertTrue(briefing["release"])

    def test_json_store_has_no_configured_provider_bypass(self):
        from zava_forward.core.store import Store
        store = Store(str(self.seed), str(self.root / "json-live.json"), str(self.root / "json-audit.jsonl"))
        store.ai.endpoint = "http://scripted-model.invalid"
        calls = []
        store.ai._chat = lambda *a, **k: calls.append(1) or "unsafe"
        r = store.ai_run(self.pm, "ZF-1", "summary")
        self.assertEqual(calls, [])
        self.assertEqual(r["source"], "template")
        self.assertIn("durable SQL release", r["reason"] if "reason" in r else r["envelope"]["failure"])

    def test_unavailable_release_table_denies_legacy_and_logs_safe_diagnostic(self):
        ai = self.legacy()
        calls = []
        ai._chat = lambda *a, **k: calls.append(1) or "unsafe"
        with self.service.transaction() as db:
            db.execute("DROP TABLE assistant_releases")
        with self.assertLogs("zava_forward.core.assistant_release", level="WARNING"):
            r = ai.run("briefing", "s", "u", "template")
        self.assertEqual(calls, [])
        self.assertIn("release records are unavailable", r["reason"])

    def test_missing_and_malformed_references_deny_even_with_inference_off(self):
        ai = self.legacy()
        good = self.store.release_context("summary", ai.fast)
        self.assertTrue(self.store.release_current("summary", good, ai.fast))
        for endpoint in (ai.endpoint, ""):
            ai.endpoint = endpoint
            for reference in (None, {}, "", {"id": "old"}, dict(good, digest=""),
                              dict(good, version=None), dict(good, id=17)):
                with self.subTest(endpoint=bool(endpoint), reference=reference):
                    self.assertFalse(self.store.release_current("summary", reference, ai.fast))
        self.assertFalse(self.store.release_current("summary", good, ai.fast))
        ai.endpoint = "http://scripted-model.invalid"
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_releases WHERE capability='legacy:summary'")
        self.assertFalse(self.store.release_current("summary", good, ai.fast))

    def test_inference_off_historical_reviews_fail_closed_in_sql_and_json(self):
        from zava_forward.core import ai_tasks
        from zava_forward.core.store import Store
        json_store = Store(str(self.seed), str(self.root / "json-live.json"), str(self.root / "json-audit.jsonl"))
        self.store.ai = Ai()
        for store in (self.store, json_store):
            store.ai.endpoint = ""
            calls = []
            store.ai._chat = lambda *a, **k: calls.append(1) or "unexpected"
            for task in ("summary", "read_document"):
                for source in ("ai", "template", "manual"):
                    for action in ("accept", "edit", "reject"):
                        with self.subTest(store=type(store).__name__, task=task, source=source, action=action):
                            if task == "summary":
                                out = store.ai_run(self.pm, "ZF-1", task, mode="workflow-only")
                            else:
                                doc = dict(store._case("ZF-1")["documents"][0], mime="text/plain")
                                out = ai_tasks.run_document(store, self.pm, "ZF-1", doc, b"synthetic", mode="workflow-only")
                            with store.lock:
                                rec = next(r for r in store.data["recommendations"] if r["id"] == out["record_id"])
                                rec.update(source=source, model=store.ai.fast)
                                rec.pop("release", None)
                                store.save()
                            if source == "ai" and action != "reject":
                                with self.assertRaises(PermissionError):
                                    store.review_ai(self.pm, rec["id"], action, "Review", "Edited")
                            else:
                                result = store.review_ai(self.pm, rec["id"], action, "Review", "Edited")
                                self.assertEqual(result["status"], ai_tasks.REVIEW_ACTIONS[action])
            self.assertEqual(calls, [])

    def test_inference_off_historical_priority_and_cached_ai_are_not_authorised(self):
        from zava_forward.core.store import Store
        json_store = Store(str(self.seed), str(self.root / "json-live.json"), str(self.root / "json-audit.jsonl"))
        self.store.ai = Ai()
        for store in (self.store, json_store):
            store.ai.endpoint = ""
            user = self.priority_user(store)
            for source in ("ai", "template"):
                for action in ("accept", "edit", "reject"):
                    with self.subTest(store=type(store).__name__, source=source, action=action):
                        out = store.ai_priority(user, 1, mode="workflow-only")
                        with store.lock:
                            rec = next(r for r in store.data["recommendations"] if r["id"] == out["id"])
                            rec.update(source=source, model=store.ai.strong)
                            rec.pop("release", None)
                            store.save()
                        view = store.latest_priority(user)
                        self.assertEqual(view["actionable"], source != "ai")
                        if source == "ai" and action != "reject":
                            audit_before = len(list(store.audit_entries()))
                            before = json.loads(json.dumps(rec))
                            with self.assertRaises(PermissionError):
                                store.resolve_priority(user, rec["id"], action, "Review", out["items"])
                            new_events = list(store.audit_entries())[audit_before:]
                            self.assertEqual([e["action"] for e in new_events], ["ai_release_denied"])
                            self.assertIn(rec["id"], new_events[0]["detail"])
                            self.assertEqual(rec, before)
                            self.assertTrue(store.verify_audit())
                            if hasattr(store, "db"):
                                persisted = json.loads(store.db.execute(
                                    "SELECT body FROM recommendations WHERE id=?", (rec["id"],)
                                ).fetchone()[0])
                            else:
                                with open(store.live_path, encoding="utf-8") as stream:
                                    persisted = next(r for r in json.load(stream)["recommendations"]
                                                     if r["id"] == rec["id"])
                            self.assertEqual(persisted, before)
                        else:
                            self.assertEqual(store.resolve_priority(user, rec["id"], action, "Review", out["items"])["status"],
                                             store.REC_ACTIONS[action])
            with store.lock:
                old = dict(store.briefing(user), source="ai", model=store.ai.fast)
                old.pop("release", None)
                key = next(key for key, (_, cached) in store._briefings.items()
                           if cached["record_id"] == old["record_id"])
                store._briefings[key] = (store.version, old)
            self.assertEqual(store.briefing(user)["source"], "template")

    def test_current_fast_and_strong_routes_invalidate_review_and_exact_reference(self):
        from zava_forward.core import ai_tasks
        ai = self.legacy()
        ai._chat = lambda *a, **k: "- Fact [[Stage: Contacting resident]]"
        for task, route in (("summary", "fast"), ("message", "fast"),
                            ("funding_draft", "strong"), ("read_document", "strong")):
            with self.subTest(task=task):
                if task == "read_document":
                    doc = dict(self.store._case("ZF-1")["documents"][0], mime="text/plain")
                    out = ai_tasks.run_document(self.store, self.pm, "ZF-1", doc, b"synthetic")
                else:
                    out = ai_tasks.run_text_task(self.store, self.pm, task, [self.store._case("ZF-1")],
                                                 "system", "prompt", "template", [], strong=route == "strong")
                self.assertEqual(out["source"], "ai")
                original = getattr(ai, route)
                self.assertTrue(self.store.release_current(task, out["release"], original))
                setattr(ai, route, "changed-" + original)
                self.assertIsNotNone(self.store.release_assessment(task)[1])
                self.assertFalse(self.store.release_current(task, out["release"], original))
                for action in ("accept", "edit"):
                    with self.assertRaises(PermissionError):
                        self.store.review_ai(self.pm, out["record_id"], action, "Review", "Edited")
                release_support.install(self.store, tasks=[])
                self.assertFalse(self.store.release_current(task, out["release"], original))
                setattr(ai, route, original)
                release_support.install(self.store, tasks=[])

    def test_fast_route_change_invalidates_cached_briefing_with_zero_new_calls(self):
        ai = self.legacy()
        user = self.priority_user(self.store)
        calls = []
        ai._chat = lambda *a, **k: calls.append(1) or "- Fact [[ZF-1: Stage: Contacting resident]]"
        first = self.store.briefing(user)
        self.assertEqual(first["source"], "ai")
        self.assertIs(self.store.briefing(user), first)
        ai.fast = "changed-fast"
        denied = self.store.briefing(user)
        self.assertEqual(denied["source"], "template")
        self.assertIn("release admission denied", denied["reason"].lower())
        self.assertEqual(calls, [1])

    def test_strong_route_change_invalidates_priority_view_and_reviews(self):
        ai = self.legacy()
        user = self.priority_user(self.store)
        ai._chat = lambda *a, **k: json.dumps([dict(case_id="ZF-4", reason="Safety", cites=["Open safety issues: 1"])])
        out = self.store.ai_priority(user, 1)
        self.assertEqual(out["source"], "ai")
        self.assertTrue(out["actionable"])
        ai.strong = "changed-strong"
        self.assertFalse(self.store.latest_priority(user)["actionable"])
        for action in ("accept", "edit"):
            audit_before = len(list(self.store.audit_entries()))
            with self.assertRaises(PermissionError):
                self.store.resolve_priority(user, out["id"], action, "Review", out["items"])
            self.assertEqual(
                [e["action"] for e in list(self.store.audit_entries())[audit_before:]],
                ["ai_release_denied"],
            )
            self.assertEqual(self.store.latest_priority(user)["status"], "Proposed")
        self.assertEqual(self.store.resolve_priority(user, out["id"], "reject", "Old route")["status"], "Rejected")

    def test_denied_briefing_recovers_after_recording_release_without_case_edit(self):
        from zava_forward.core import ai_registry
        ai = self.legacy()
        user = self.priority_user(self.store)
        calls = []
        ai._chat = lambda *a, **k: calls.append(1) or "- Fact [[ZF-1: Stage: Contacting resident]]"
        with self.service.transaction() as db:
            db.execute("DELETE FROM assistant_releases WHERE capability='legacy:briefing'")
        denied = self.store.briefing(user)
        self.assertEqual(denied["source"], "template")
        self.assertIn((self.store.version, denied), self.store._briefings.values())
        self.assertEqual(self.store.briefing(user)["source"], "template")
        self.assertEqual(calls, [])
        version = self.store.version
        payload = release_support.fixture("legacy:briefing", ai_registry.legacy_binding("briefing", ai, ai.fast),
                                          cls="actual")
        payload.update(expires="2099-01-01T00:00:00Z")
        with self.service.transaction() as db:
            rid = rel.record(db, self.service.now(db), self.pm, payload, self.service.approvers,
                             {"legacy:briefing"})
        self.assertEqual(self.store.version, version)
        out = self.store.briefing(user)
        self.assertEqual(out["source"], "ai")
        self.assertEqual(out["release"]["id"], rid)
        self.assertEqual(calls, [1])
        self.assertIs(self.store.briefing(user), out)
        self.assertEqual(calls, [1])


def assistants_proposal(task):
    from test_assistants import proposal
    return proposal(task["snapshot"])


if __name__ == "__main__":
    unittest.main()
