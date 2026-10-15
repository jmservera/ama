"""Service continuity: AI suspension, restart gate, versioned changes and supplier-independent export.
Synthetic demonstration data only; no billable provider calls."""
import copy
import json
import unittest

import test_mvp
from test_assistants import Base, Provider, canonical, proposal
from zavaforward_mvp import continuity
from zavaforward_mvp.ai import Ai
from zavaforward_mvp.assistants import Assistants
from zavaforward_mvp.store import Store

SUSPEND = dict(scope="all", reason="Suspect output quality", incident_owner="Programme manager",
               containment="Stop all AI work", comms_owner="Programme manager", comms_audience="Staff only")


class Suspension(Base):
    def setUp(self):
        super().setUp()
        self.qi = self.people["Quality Inspector"]
        self.pso = self.people["Programme Support Officer"]
        self.liaison = self.people["Resident Liaison Officer"]

    def suspend(self, **kw):
        return self.store.suspend(self.qi, dict(SUSPEND, **kw), self.service.affected(kw.get("scope", "all")))

    def restart(self, s):
        self.store.restart_propose(self.pm, dict(id=s["id"], corrective_evidence="Re-evaluated on synthetic cases."))
        return self.store.restart_decide(self.pso, dict(id=s["id"], epoch=self.store.continuity_epoch(),
                                                        decision="Restart", authority_ref="Delegation ref D-1"))

    def test_roles_and_required_fields(self):
        with self.assertRaises(PermissionError):
            self.store.suspend(self.liaison, SUSPEND)
        with self.assertRaises(ValueError):
            self.store.suspend(self.qi, dict(SUSPEND, containment=""))
        with self.assertRaises(ValueError):
            self.store.suspend(self.qi, dict(SUSPEND, scope="nonsense"))
        s = self.suspend()
        self.assertFalse(s["communication"]["sent"])
        self.assertEqual(s["epoch"], 1)
        with self.assertRaises(ValueError):
            self.suspend()

    def test_queued_leased_and_ready_proposals_are_gated_on_independent_connection(self):
        queued = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        claim = self.service.claim(queued["id"], "w1")
        self.assertIsNotNone(claim)
        self.suspend()
        other = self.other()
        with other.transaction() as db:
            self.assertTrue(other.suspended(db, "stock-prioritisation"))
        self.assertFalse(other.execute(queued["id"]))
        self.assertEqual(self.provider.calls, 0)
        env = dict(outcome="returned", source="ai", usage=None, model="test-model")
        other.complete(claim, env, proposal(claim["snapshot"]))
        v = other.detail(self.pm, queued["id"])
        self.assertFalse(v["actionable"])
        self.assertEqual(v["state"], "quarantined")

    def test_sql_store_wires_the_ai_gate_and_flags_truncated_affected_list(self):
        fresh = self.open_store()
        self.addCleanup(fresh.db.close)
        self.assertIsNone(fresh.ai.gate("priority"))
        queued = [self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")]
        self.assertEqual(len(self.service.affected("all", limit=0)), 0)
        self.assertTrue(self.service.affected("all", limit=0).truncated)
        self.assertFalse(self.service.affected("all").truncated)
        s = self.store.suspend(self.qi, dict(SUSPEND), self.service.affected("all", limit=0))
        self.assertTrue(s["affected_assistant_truncated"])
        self.assertEqual(s["affected_assistant_total"], len(queued))
        self.assertTrue(fresh.ai.gate("priority"))
        r = fresh.ai.run("priority", "s", "u", "template", False)
        self.assertEqual(r["source"], "template")
        self.assertEqual(r["reason"], fresh.continuity_block("priority"))

    def test_invoke_refused_while_suspended_then_allowed_after_restart(self):
        s = self.suspend()
        held = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.assertEqual(held["state"], "disabled")
        self.assertFalse(self.service.execute(held["id"]))
        self.assertEqual(self.provider.calls, 0)
        with self.assertRaises(PermissionError):
            self.store.restart_decide(self.pso, dict(id=s["id"], epoch=1, decision="Restart", authority_ref="x"))
        self.restart(s)
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        self.assertTrue(self.service.execute(p["id"]))

    def test_ready_proposal_cannot_be_relied_on_while_suspended(self):
        p = self.run_ready("stock-prioritisation")
        self.suspend()
        v = self.service.detail(self.pm, p["id"])
        self.assertFalse(v["actionable"])
        self.assertEqual(v["display_state"], "suspended")
        with self.assertRaises((ValueError, PermissionError)):
            self.verify(p)
        rejected = self.service.review(self.pm, p["id"], "reject", p["revision"], "Rejected during suspension.")
        self.assertEqual(rejected["state"], "rejected")

    def test_late_result_is_quarantined_not_actionable(self):
        p = self.service.invoke(self.pm, "stock-prioritisation", "ZF-1")
        claim = self.service.claim(p["id"], "w1")
        self.suspend(scope="stock-prioritisation")
        self.service.complete(claim, dict(outcome="returned", source="ai", usage=None), proposal(claim["snapshot"]))
        v = self.service.detail(self.pm, p["id"])
        self.assertFalse(v["actionable"])
        self.assertNotEqual(v["state"], "ready")

    def test_restart_gate_rejects_self_stale_replay_and_unauthorised(self):
        s = self.suspend()
        body = dict(id=s["id"], epoch=1, decision="Restart", authority_ref="Delegation ref D-1")
        with self.assertRaises(PermissionError):
            self.store.restart_decide(self.pso, body)
        with self.assertRaises(PermissionError):
            self.store.restart_propose(self.liaison, dict(id=s["id"], corrective_evidence="x"))
        self.store.restart_propose(self.pm, dict(id=s["id"], corrective_evidence="Re-evaluated."))
        with self.assertRaises(PermissionError):
            self.store.restart_decide(self.pm, body)
        with self.assertRaises(PermissionError):
            self.store.restart_decide(self.pso, dict(body, epoch=99))
        with self.assertRaises(ValueError):
            self.store.restart_decide(self.pso, dict(body, authority_ref=""))
        self.store.restart_decide(self.pso, body)
        with self.assertRaises((ValueError, PermissionError)):
            self.store.restart_decide(self.pso, body)
        self.assertEqual(self.store.continuity_epoch(), 2)

    def test_manual_fallback_and_hazard_work_continue(self):
        self.suspend()
        with self.service.transaction() as db:
            self.assertTrue(self.service.suspended(db, "stock-prioritisation"))
        self.assertTrue(self.store.continuity_block("priority"))
        v = self.store.continuity_view(self.pm)
        self.assertIn("Manual case work", v["note"])

    def test_concurrent_suspend_and_review_leave_no_actionable_proposal(self):
        import threading
        p = self.run_ready("stock-prioritisation")
        p = self.verify(p)
        out = []
        t = threading.Thread(target=lambda: out.append(self.suspend()))
        t.start()
        t.join()
        with self.assertRaises((ValueError, PermissionError)):
            self.service.review(self.pm, p["id"], "accept", p["revision"], "Accepting after suspension.")
        self.assertFalse(self.other().detail(self.pm, p["id"])["actionable"])


class Changes(Base):
    def setUp(self):
        super().setUp()
        self.pso = self.people["Programme Support Officer"]

    def change(self, **kw):
        body = dict(kind="model", subject="stock-prioritisation", from_version="v1", to_version="v2",
                    reason="Better recall on synthetic cases", evaluation="pass", evaluation_ref="eval-001")
        return self.store.change_record(self.pm, dict(body, **kw))

    def test_versioned_evaluated_and_reversible(self):
        c = self.change()
        self.assertEqual(c["status"], "Applied")
        with self.assertRaises(ValueError):
            self.change(from_version="v9", to_version="v10")
        blocked = self.change(from_version="v2", to_version="v3", evaluation="fail")
        self.assertEqual(blocked["status"], "Blocked")
        rev = self.store.change_reverse(self.pm, dict(id=c["id"], reason="Regression found"))
        self.assertEqual(rev["to_version"], "v1")
        eff = self.store.continuity_view(self.pm)["effective"]["model:stock-prioritisation"]
        self.assertEqual(eff["version"], "v1")
        with self.assertRaises(ValueError):
            self.store.change_reverse(self.pm, dict(id=c["id"], reason="Again"))
        with self.assertRaises(PermissionError):
            self.store.change_record(self.people["Quality Inspector"], dict(kind="rule"))

    def test_export_verifies_offline_and_detects_tampering(self):
        self.change()
        self.store.suspend(self.people["Quality Inspector"], SUSPEND)
        bundle = json.loads(json.dumps(self.store.continuity_export(self.pm, self.service.export())))
        self.assertTrue(continuity.verify_export(bundle)["valid"])
        self.assertEqual(bundle["continuity"]["suspensions"][0]["status"], "Suspended")
        self.assertTrue(bundle["versions"]["changes"])
        bad = copy.deepcopy(bundle)
        bad["versions"]["changes"][0]["to_version"] = "forged"
        self.assertFalse(continuity.verify_export(bad)["valid"])
        with self.assertRaises(PermissionError):
            self.store.continuity_export(self.people["Resident Liaison Officer"])

    def test_truncated_export_is_flagged_incomplete_never_valid(self):
        self.store.suspend(self.people["Quality Inspector"], SUSPEND, [])
        part = self.service.export(limit=0)
        self.assertEqual(part["truncated"], part["total"] > 0)
        forced = dict(part, truncated=True, limit=0, total=part["total"] + 1)
        bundle = json.loads(json.dumps(self.store.continuity_export(self.pm, forced)))
        self.assertFalse(bundle["complete"])
        self.assertIn("truncated", bundle["incomplete_reasons"][0])
        check = continuity.verify_export(bundle)
        self.assertFalse(check["valid"])
        self.assertFalse(check["complete"])

    def test_ledger_tail_truncation_and_external_head(self):
        self.change()
        self.change(subject="other")
        bundle = json.loads(json.dumps(self.store.continuity_export(self.pm, self.service.export())))
        self.assertTrue(continuity.verify_export(bundle)["valid"])
        self.assertTrue(continuity.verify_export(bundle, expected_head=bundle["ledger"]["head"])["valid"])
        cut = copy.deepcopy(bundle)
        cut["ledger"]["entries"].pop()
        cut["digest"] = continuity.sha({k: v for k, v in cut.items() if k != "digest"})
        res = continuity.verify_export(cut)
        self.assertFalse(res["valid"])
        self.assertTrue(any("truncated" in p for p in res["problems"]))
        rewritten = copy.deepcopy(cut)
        rewritten["ledger"]["head"] = dict(count=len(cut["ledger"]["entries"]), hash=cut["ledger"]["entries"][-1]["hash"])
        rewritten["digest"] = continuity.sha({k: v for k, v in rewritten.items() if k != "digest"})
        self.assertTrue(continuity.verify_export(rewritten)["valid"])
        self.assertFalse(continuity.verify_export(rewritten, expected_head=bundle["ledger"]["head"])["valid"])

    def test_export_independent_of_ai_supplier(self):
        self.store.ai = type("None_", (), {"configured": False, "gate": None})()
        bundle = self.store.continuity_export(self.pm, self.service.export())
        self.assertTrue(continuity.verify_export(json.loads(json.dumps(bundle)))["valid"])


class JsonStore(unittest.TestCase):
    def test_json_store_suspend_gates_ai_and_exports(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            seed = Path(d, "seed.json")
            data = copy.deepcopy(test_mvp.DATA)
            staff = [dict(code=f"R{i}", name=f"Person {i}", email=f"p{i}@example.test", role=r)
                     for i, r in enumerate(("Quality Inspector", "Retrofit Programme Manager", "Programme Support Officer"))]
            data["staff"] = staff
            seed.write_text(json.dumps(data))
            store = Store(str(seed), str(Path(d, "live.json")), str(Path(d, "audit.jsonl")))
            qi, pm, pso = staff
            s = store.suspend(qi, SUSPEND)
            self.assertTrue(store.continuity_block("priority"))
            store.restart_propose(pm, dict(id=s["id"], corrective_evidence="Reviewed."))
            store.restart_decide(pso, dict(id=s["id"], epoch=1, decision="Restart", authority_ref="Ref"))
            self.assertFalse(store.continuity_block("priority"))
            bundle = json.loads(json.dumps(store.continuity_export(pm, Assistants.export(type('J', (), {'sql': False})()))))
            self.assertTrue(continuity.verify_export(bundle)["valid"])
            self.assertFalse(bundle["assistants"]["supported"])
            self.assertIn("JSON store", bundle["assistants"]["note"])


if __name__ == "__main__":
    unittest.main()
