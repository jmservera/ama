"""Service continuity: AI suspension, restart gate, versioned changes and supplier-independent export.
Synthetic demonstration data only; no billable provider calls."""
import copy
import json
import os
import unittest
from unittest import mock

import test_mvp
from test_assistants import Base, Provider, canonical, config, proposal
from zava_forward.api.server import CHAT_TASK, chat_admission
from zava_forward.agents.chat import ChatModel
from zava_forward.agents.dispatch import AgentWorker
from zava_forward.core import chat_demo_meter, continuity
from zava_forward.core.ai_consumption import CallContext, call_context, reference
from zava_forward.core.chat_panel import ModelUnavailable
from zava_forward.core.ai import Ai
from zava_forward.core.assistants import Assistants
from zava_forward.core.store import Store

SUSPEND = dict(scope="all", reason="Suspect output quality", incident_owner="Programme manager",
               containment="Stop all AI work", comms_owner="Programme manager", comms_audience="Staff only",
               restart_authority="Delegation ref D-1", evidence="Constructed incident evidence",
               resident_impact="Constructed impact assessment", remediation="Constructed corrective work")


class Suspension(Base):
    def setUp(self):
        super().setUp()
        self.qi = self.people["Quality Inspector"]
        self.pso = self.people["Programme Support Officer"]
        self.liaison = self.people["Resident Liaison Officer"]

    def suspend(self, **kw):
        return self.store.suspend(self.qi, dict(SUSPEND, **kw), self.service.affected(kw.get("scope", "all")))

    def restart(self, s):
        from test_operator_suspension import restart
        return restart(self, s)

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
        self.assertFalse(s["affected_assistant_truncated"])
        self.assertEqual(s["affected_assistant_total"], len(queued))
        self.assertTrue(fresh.ai.gate("priority"))
        r = fresh.ai.run("priority", "s", "u", "template", False)
        self.assertEqual(r["source"], "template")
        self.assertEqual(r["reason"], fresh.continuity_block("priority"))

    def test_all_task_candidate_lists_disabled_chat_without_throwing(self):
        c = continuity.candidate(self.store, self.store.db, continuity.ALL)
        chat = next(v for v in c["versions"] if v["task"] == "chat-case-conversation")
        self.assertIsNone(chat["release"])
        self.assertTrue(chat["missing"])
        self.assertTrue(self.suspend()["id"])

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
        from test_operator_suspension import decision, propose, provision
        actor = provision(self)
        s = propose(self, s)
        body = decision(s)
        with self.assertRaises(PermissionError):
            self.store.restart_decide(self.pm, body)
        with self.assertRaises(PermissionError):
            self.store.restart_decide(actor, dict(body, epoch=99))
        with self.assertRaises(ValueError):
            self.store.restart_decide(actor, dict(body, authority_ref=""))
        self.store.restart_decide(actor, body)
        with self.assertRaises((ValueError, PermissionError)):
            self.store.restart_decide(actor, body)
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
        from test_continuity_epoch_export import complete_release_fixtures
        complete_release_fixtures(self)
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
            with self.assertRaises(PermissionError):
                store.restart_propose(pm, dict(id=s["id"], corrective_evidence="Reviewed.",
                                              result="Pass", test_id="constructed", evidence_class="constructed-fixture"))
            with self.assertRaises(PermissionError):
                store.restart_decide(pso, dict(id=s["id"], epoch=1, decision="Restart", authority_ref="Ref"))
            self.assertTrue(store.continuity_block("priority"))
            service = Assistants(store, {})
            self.addCleanup(service.stop)
            bundle = json.loads(json.dumps(store.continuity_export(pm, service.export())))
            self.assertTrue(continuity.verify_export(bundle)["valid"])
            self.assertFalse(bundle["assistants"]["supported"])
            self.assertIn("JSON store", bundle["assistants"]["note"])
            self.assertFalse(bundle["task_releases"]["supported"])
            self.assertEqual(bundle["task_releases"]["records"], [])
            self.assertIn("unsupported", bundle["task_releases"]["note"])
            self.assertTrue(continuity.verify_export(bundle, bundle["ledger"]["head"])["valid"])


if __name__ == "__main__":
    unittest.main()


class ChatAdmissionOnSqlStore(Base):
    """The chat gate against the real SqlStore, whose release record denies every task outside the legacy set (#891)."""
    DEMO_ON = {"ZF_CHAT_DEMO_ACTIVATION": "approved-2026-11-03", "ZF_DEPLOYMENT_PROFILE": "demo",
               "AI_ENDPOINT": "https://ai.invalid/"}

    def test_demo_activation_skips_release_denial_but_honours_suspension(self):
        with mock.patch.dict(os.environ, self.DEMO_ON):
            store = self.open_store()
            self.addCleanup(store.db.close)
            self.assertIn("task is not registered", store.release_block(CHAT_TASK))
            self.assertIsNone(chat_admission(store))
            qi = self.people["Quality Inspector"]
            store.suspend(qi, dict(SUSPEND, scope=CHAT_TASK), self.service.affected(CHAT_TASK))
            self.assertEqual(chat_admission(store), continuity.reason_text(store.continuity_suspension(CHAT_TASK)))
            self.assertTrue(chat_admission(store))

    def test_registry_authorization_without_demo_switch_keeps_release_gate(self):
        env = {"AI_ENDPOINT": "https://ai.invalid/"}
        with mock.patch.dict(os.environ, env), \
                mock.patch("zava_forward.core.ai_registry.authorizes_live", return_value=True):
            store = self.open_store()
            self.addCleanup(store.db.close)
            self.assertIn("task is not registered", chat_admission(store))


class ChatDemoMeterOnSqlStore(Base):
    """The financial meter on the real SqlStore and ledger: the demo path admits one chat call; without the switch it is held (#891)."""
    ENV = {"AI_ENDPOINT": "https://ai.invalid", "ZF_DEPLOYMENT_PROFILE": "demo"}
    DEMO_ON = dict(ENV, ZF_CHAT_DEMO_ACTIVATION="approved-2026-11-03")

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self, n=-1):
            return json.dumps(dict(model="unattested", choices=[dict(message=dict(content="ok"))],
                                   usage=dict(prompt_tokens=10, completion_tokens=2, total_tokens=12,
                                              prompt_tokens_details=dict(cached_tokens=0)))).encode()

    def chat_model(self, env):
        with mock.patch.dict(os.environ, env):
            store = self.open_store()
        self.addCleanup(store.db.close)
        service = Assistants(store, config())
        self.addCleanup(service.stop)
        self.assertIsInstance(store.ai, Ai)
        store.ai.token, store.ai.expires = "synthetic-token", 4e9
        self.assertIs(store.ai.consumption, service.consumption)
        model = ChatModel(AgentWorker(lambda *args: store.ai.evidence(*args)), admission=lambda: chat_admission(store))
        return store, service, model

    def ask(self, env):
        store, service, model = self.chat_model(env)
        with mock.patch.dict(os.environ, env), \
                mock.patch("urllib.request.urlopen", return_value=self.Response()) as opened:
            root = reference("question")
            context = CallContext(root, root, CHAT_TASK, "retrofit-case", reference(CHAT_TASK), reference("system"))
            try:
                with call_context(context):
                    reply = model("system", "Question: status?")
            except ModelUnavailable as error:
                reply = error
        return service, reply, opened.call_count

    def kinds(self, service):
        with service.transaction() as db:
            return [json.loads(row[0])["kind"] for row in db.execute("SELECT body FROM assistant_events")]

    def test_demo_path_seeds_synthetic_records_and_admits_exactly_one_call(self):
        service, reply, sent = self.ask(self.DEMO_ON)
        self.assertEqual((reply.text, sent, reply.calls), ("ok", 1, 1))
        with service.transaction() as db:
            records = [json.loads(row[0]) for row in db.execute("SELECT body FROM assistant_events")]
        self.assertEqual([r["kind"] for r in records], ["price", "authority", "reserved", "completed"])
        price, authority = records[0], records[1]
        self.assertTrue(price["synthetic"])
        self.assertEqual((authority["max_calls"], authority["budgets"][0]["calls"]), (1, chat_demo_meter.CALLS))
        self.assertGreater(authority["end"], authority["start"])

    def test_demo_path_holds_a_second_call_in_the_same_request(self):
        store, service, _ = self.chat_model(self.DEMO_ON)
        root = reference("one-question")
        with mock.patch.dict(os.environ, self.DEMO_ON), \
                mock.patch("urllib.request.urlopen", return_value=self.Response()):
            chat_admission(store)
            outcomes = []
            for attempt in ("first", "second"):
                context = CallContext(root, reference(attempt), CHAT_TASK, "retrofit-case", reference(CHAT_TASK), reference("s"))
                with call_context(context):
                    outcomes.append(store.ai.evidence("system", "q", 600)["outcome"])
        self.assertEqual(outcomes, ["returned", "financial-held"])
        self.assertEqual(self.kinds(service).count("reserved"), 1)

    def test_without_the_switch_nothing_is_seeded_and_the_call_is_refused(self):
        service, reply, sent = self.ask(self.ENV)
        self.assertIsInstance(reply, ModelUnavailable)
        self.assertEqual((sent, self.kinds(service)), (0, []))

    def test_synthetic_price_still_holds_a_live_call_outside_the_demo(self):
        store, service, _ = self.chat_model(self.ENV)
        with mock.patch.dict(os.environ, self.DEMO_ON):
            chat_demo_meter.ensure(store, 600)
        store.ai.synthetic_price_capabilities = frozenset()
        context = CallContext(reference("r"), reference("a"), CHAT_TASK, "retrofit-case", reference(CHAT_TASK), reference("s"))
        with mock.patch("urllib.request.urlopen", return_value=self.Response()) as opened, call_context(context):
            envelope = store.ai.evidence("system", "q", 600)
        self.assertEqual((envelope["outcome"], envelope["reason"], opened.call_count), ("financial-held", "price-unknown", 0))
