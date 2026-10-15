"""Release admission for the five assistants and retained legacy dispatch (issue #107). Constructed fixtures only."""
import json
import time
import unittest
from unittest.mock import patch

import release_support
from test_assistants import Base, config
from zavaforward_mvp import assistant_release as rel
from zavaforward_mvp import assistants
from zavaforward_mvp.ai import Ai

CAP = "stock-prioritisation"


def body(service, **over):
    b = dict(assistants.runtime_binding(CAP, service.store.ai), task=CAP, evidence_class="constructed-fixture",
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
                    self.assertIn("no longer matches", self.service.admission(db, CAP)["reason"])
        with patch.dict(assistants.REGISTRY[CAP], {"roles": (assistants.RC,)}):
            with self.service.transaction() as db:
                self.assertIn("permission_version", self.service.admission(db, CAP)["missing"])
        self.case(lambda c: c["home"].update(epc="G"))
        detail = self.service.detail(self.pm, p["id"])
        self.assertIsNone(detail["release_denial"])
        self.assertTrue(detail["stale"])

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
        self.assertEqual(self.service.invoke(self.pm, CAP, "ZF-1")["state"], "quarantined")

    def test_live_provider_needs_actual_release_with_serving_proof(self):
        binding = assistants.runtime_binding(CAP, self.provider)
        fx = release_support.fixture(CAP, binding)
        with self.service.transaction() as db:
            db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (rel.canonical(fx), f"fx-{CAP}"))
            now = self.service.now(db)
            self.assertIsNone(rel.admission(db, CAP, binding, now, live=False))
            denied = rel.admission(db, CAP, binding, now, live=True)
            self.assertIn("actual authorisation with serving-version attestation", denied["missing"])
            db.execute("UPDATE assistant_releases SET body=? WHERE id=?", (rel.canonical(dict(fx, evidence_class="actual")), f"fx-{CAP}"))
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


def assistants_proposal(task):
    from test_assistants import proposal
    return proposal(task["snapshot"])


if __name__ == "__main__":
    unittest.main()
