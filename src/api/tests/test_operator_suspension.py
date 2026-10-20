"""Bounded incident drills. Every actor, result and permission is constructed."""

import copy
import json
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Any
from unittest.mock import patch

from zava_forward.core import assistant_release, assistants, continuity
from zava_forward.core.ai import Ai
from zava_forward.core.store import ConflictError

from test_assistants import Base

CAP = "stock-prioritisation"
AUTHORITY = "Constructed fixture authority, not OD-35 appointment"


def incident(scope: str = CAP) -> dict[str, Any]:
    return dict(
        scope=scope,
        reason="Seeded critical unsupported claim",
        incident_owner="Fixture owner",
        containment="Stop affected proposals",
        comms_owner="Fixture owner",
        comms_audience="Synthetic staff",
        evidence="synthetic:incident-221",
        resident_impact="Constructed resident could receive an unsupported claim",
        remediation="Correct prompt and rerun negative controls",
        restart_authority=AUTHORITY,
        synthetic=True,
        trigger="guardrail breach",
    )


def provision(test: Any, store: Any = None) -> dict[str, Any]:
    store = store or test.store
    person = test.people["Programme Support Officer"]
    person["oid"] = "constructed-independent-restart-oid"
    with store.dblock:
        row = store.db.execute(
            "SELECT body FROM staff WHERE email=?", (person["email"],)
        ).fetchone()
        current = json.loads(row[0])
        current["oid"] = person["oid"]
        store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), person["email"])
        )
    return dict(person, auth_provider="trusted-proxy", rule_roles=["ai_restart"])


def propose(test: Any, s: dict[str, Any], store: Any = None) -> Any:
    return (store or test.store).restart_propose(
        test.pm,
        dict(
            id=s["id"],
            corrective_evidence="synthetic:corrective-tests-221",
            test_id="constructed-negative-and-fallback-drill",
            result="Pass",
            evidence_class="constructed-fixture",
        ),
    )


def decision(s: dict[str, Any]) -> dict[str, Any]:
    return dict(
        id=s["id"],
        epoch=s["proposal"]["epoch"],
        proposal_digest=s["proposal"]["digest"],
        decision="Restart",
        authority_ref=s["restart_authority"],
    )


def restart(test: Any, s: dict[str, Any], store: Any = None) -> Any:
    store = store or test.store
    actor = provision(test, store)
    return store.restart_decide(actor, decision(propose(test, s, store)))


def transaction_failures(test: Any, s: dict[str, Any], actor: dict[str, Any]) -> None:
    before = copy.deepcopy(test.store.continuity_view(test.pm))
    with patch.object(
        test.store, "_proc_write", side_effect=RuntimeError("constructed write fault")
    ):
        with test.assertRaises(RuntimeError):
            test.store.restart_decide(actor, decision(s))
    test.assertEqual(test.other().store.continuity_view(test.pm), before)
    original = test.store.save
    other = test.other()

    def concurrent_save() -> None:
        other.store.suspend(test.people["Quality Inspector"], incident("quality-evidence"))
        original()

    with patch.object(test.store, "save", side_effect=concurrent_save):
        with test.assertRaises(ConflictError):
            test.store.restart_decide(actor, decision(s))
    test.assertEqual(test.store.continuity_view(test.pm)["suspensions"][0]["status"], "Suspended")


def drill(test: Any) -> None:
    ready = test.run_ready(CAP)
    pending = test.service.invoke(test.pm, CAP, "ZF-2")
    other = test.verify(test.run_ready("assessment-preparation"))
    other = test.service.review(
        test.pm, other["id"], "accept", other["revision"], "Constructed independent review"
    )
    queued = test.service.invoke(test.pm, "funding-evidence", "ZF-1")
    claimed = test.service.claim(queued["id"], "independent-task")
    test.store.suspend(test.people["Quality Inspector"], incident())
    s = test.store.continuity_view(test.pm)["suspensions"][-1]
    test.assertEqual(s["affected_assistant_total"], 2)
    affected = {row["id"]: row for row in s["affected_assistant_tasks"]}
    test.assertEqual(set(affected), {ready["id"], pending["id"]})
    test.assertEqual(affected[ready["id"]]["release"], ready["release"])
    test.assertEqual(
        s["incident_versions"]["versions"][0]["binding"],
        assistants.runtime_binding(CAP, test.provider),
    )
    test.assertFalse(test.service.detail(test.pm, ready["id"])["actionable"])
    with test.assertRaises(PermissionError):
        test.verify(ready)
    calls = test.provider.calls
    test.assertFalse(test.service.execute(pending["id"]))
    denied = test.service.invoke(test.pm, CAP, "ZF-2")
    test.assertFalse(test.service.execute(denied["id"]))
    test.assertEqual(test.provider.calls, calls)
    test.assertTrue(test.service.detail(test.pm, other["id"])["actionable"])
    from test_assistants import proposal

    test.assertTrue(
        test.service.complete(
            claimed,
            dict(outcome="returned", source="ai", model="test-model", usage=None),
            proposal(claimed["snapshot"]),
        )
    )
    test.assertEqual(test.service.detail(test.pm, queued["id"])["state"], "ready")
    test.store.log_call(test.pm, "ZF-1", "Spoke", "Synthetic manual fallback")
    test.store.raise_hazard(
        test.pm,
        "ZF-1",
        "Damp and mould",
        "Emergency",
        "Synthetic hazard",
        dict(source="Synthetic officer", aware_at="2026-10-01T00:00:00Z"),
    )
    test.assertTrue(test.other().store.cases["ZF-1"]["hazards"])
    actor = provision(test)
    p = propose(test, s)
    with test.assertRaises(PermissionError):
        test.store.restart_decide(dict(actor, rule_roles=[]), decision(p))
    test.assertTrue(
        any(row["action"] == "ai_restart_decide_denied" for row in test.store.audit_entries())
    )
    transaction_failures(test, p, actor)
    p = propose(test, s)
    test.store.restart_decide(actor, decision(p))
    test.assertFalse(test.service.detail(test.pm, ready["id"])["actionable"])
    fresh = test.service.invoke(test.pm, CAP, "ZF-1")
    test.assertTrue(test.service.execute(fresh["id"]))
    reopened = test.other()
    test.assertEqual(
        reopened.store.continuity_view(test.pm)["suspensions"][0]["status"], "Restarted"
    )
    reopened.store.ai = Ai()
    with reopened.transaction() as db:
        test.assertIsNotNone(reopened.suspended(db, CAP))
    test.assertFalse(reopened.detail(test.pm, fresh["id"])["actionable"])


class OperatorIncident(Base):
    def test_incident_snapshot_and_reopen(self) -> None:
        drill(self)
        from zava_forward.core.store import Store

        live, audit = str(self.root / "incident.json"), str(self.root / "incident-audit.jsonl")
        store = Store(str(self.seed), live, audit)
        store.suspend(self.people["Quality Inspector"], incident())
        reopened = Store(str(self.seed), live, audit)
        self.assertTrue(reopened.continuity_block(CAP))
        retained = reopened.continuity_view(self.pm)["suspensions"][0]
        self.assertEqual(retained["evidence"], "synthetic:incident-221")
        self.assertFalse(retained["snapshot_complete"])
        with self.assertRaises(PermissionError):
            propose(self, retained, reopened)

    def test_restart_negative_matrix(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        for key, bad in (
            ("result", "Fail"),
            ("evidence_class", "actual"),
            ("test_id", ""),
            ("corrective_evidence", ""),
        ):
            body = dict(
                id=s["id"],
                corrective_evidence="synthetic:tests",
                test_id="tests",
                result="Pass",
                evidence_class="constructed-fixture",
            )
            body[key] = bad
            with self.subTest(key=key), self.assertRaises((ValueError, PermissionError)):
                self.store.restart_propose(self.pm, body)
        s = propose(self, s)
        for actor_bad in (
            self.pm,
            self.people["Quality Inspector"],
            dict(actor, auth_provider="password"),
            dict(actor, oid="forged"),
            dict(actor, rule_roles=[]),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor_bad, decision(s))
        for field, value in (
            ("epoch", 99),
            ("proposal_digest", "wrong"),
            ("authority_ref", "invented"),
        ):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor, dict(decision(s), **{field: value}))
        with self.store.lock:
            self.store._cont()["suspensions"][0]["proposal"]["corrective_evidence"] = "altered"
            self.store.save()
        with self.assertRaises(PermissionError):
            self.store.restart_decide(actor, decision(s))
        s = propose(self, s)
        self.store.restart_decide(actor, decision(s))
        with self.assertRaises(ValueError):
            self.store.restart_decide(actor, decision(s))

    def test_candidate_drift_and_reproposal(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        original = copy.deepcopy(s["incident_versions"])
        for key in assistant_release.BOUND:
            with self.subTest(binding=key):
                old = assistants.runtime_binding
                with patch.object(
                    assistants,
                    "runtime_binding",
                    side_effect=lambda *a, old=old, key=key: dict(old(*a), **{key: "changed"}),
                ):
                    with self.assertRaises(PermissionError):
                        self.store.restart_decide(actor, decision(s))
        self.service.approvers = {self.pm["email"]}
        from test_assistant_release import body

        self.service.record_release(self.pm, body(self.service, release_version="corrected-v2"))
        with self.assertRaises(PermissionError):
            self.store.restart_decide(actor, decision(s))
        s = propose(self, s)
        self.assertEqual(s["incident_versions"], original)
        self.assertEqual(len(s["proposals"]), 2)
        self.store.restart_decide(actor, decision(s))

    def test_constructed_restart_actual_hold(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        restart(self, s)
        ai = Ai()
        ai.endpoint, ai.fast, ai.model_version = "https://synthetic.invalid", "test", "test-model"
        calls = []
        ai.evidence = lambda *a, **kw: calls.append(1)
        self.store.ai = ai
        import release_support

        release_support.install(self.store, ai, cls="actual")
        p = self.service.invoke(self.pm, CAP, "ZF-1")
        self.assertEqual(p["state"], "disabled")
        self.assertFalse(self.service.execute(p["id"]))
        self.assertEqual(calls, [])
        self.assertIn(
            "OD-35", self.store.continuity_view(self.pm)["suspensions"][0]["actual_authority"]
        )

    def test_rollback_and_conflict(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        transaction_failures(self, s, actor)
        self.assertTrue(self.service.suspended(self.store.db, CAP))

    def test_snapshot_boundary(self) -> None:
        original = self.store.save
        created = []

        def concurrent_enqueue() -> None:
            created.append(self.service.invoke(self.pm, CAP, "ZF-1")["id"])
            original()

        with patch.object(self.store, "save", side_effect=concurrent_enqueue):
            self.store.suspend(self.people["Quality Inspector"], incident())
        s = self.store.continuity_view(self.pm)["suspensions"][-1]
        self.assertEqual([row["id"] for row in s["affected_assistant_tasks"]], created)
        self.assertFalse(self.service.execute(created[0]))

    def test_relevant_history_failclosed(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        restart(self, s)
        doc = self.store.continuity_view(self.pm)
        for epoch in (None, -1, 3, True):
            self.assertFalse(continuity.epoch_current(dict(task=CAP, continuity_epoch=epoch), doc))
        self.assertTrue(
            continuity.epoch_current(dict(task="assessment-preparation", continuity_epoch=0), doc)
        )
        self.assertFalse(continuity.epoch_current(dict(task=CAP, continuity_epoch=0), doc))

    def test_manual_hazard_drill(self) -> None:
        self.store.suspend(self.people["Quality Inspector"], incident("all"))
        self.store.log_call(self.pm, "ZF-1", "Spoke", "Synthetic manual fallback")
        self.store.raise_hazard(
            self.pm,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            "Synthetic hazard",
            dict(source="Synthetic officer observation", aware_at="2026-10-01T00:00:00Z"),
        )
        reopened = self.other().store
        self.assertTrue(reopened.cases["ZF-1"]["hazards"])
        self.assertIn("Synthetic manual fallback", json.dumps(reopened.cases["ZF-1"]))

    def test_trusted_capability(self) -> None:
        from test_auth import ENV, principal
        from zava_forward.api.auth import PasswordProvider, TrustedProxyProvider
        from zava_forward.api.server import App, make_handler

        actor = provision(self)
        self.store.staff[actor["email"]]["oid"] = actor["oid"]
        provider = TrustedProxyProvider(self.store, dict(ENV, ZF_AUTH_EMAIL_FALLBACK="1"))
        roles = ("ZavaForward.SupportOfficer", "ZavaForward.AIRestart")
        bound = provider.authenticate(
            {"X-MS-CLIENT-PRINCIPAL": principal(roles=roles, oid=actor["oid"])}
        )
        self.assertIsNotNone(bound)
        self.assertEqual(bound["rule_roles"], ["ai_restart"])
        fallback = provider.authenticate(
            {"X-MS-CLIENT-PRINCIPAL": principal(roles=roles, oid="unbound", email=actor["email"])}
        )
        self.assertEqual(fallback["rule_roles"], [])
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        s = propose(self, s)
        with self.assertRaises(PermissionError):
            self.store.restart_decide(fallback, decision(s))
        self.store.staff[actor["email"]].update(
            auth_provider="trusted-proxy", rule_roles=["ai_restart"]
        )
        password = PasswordProvider(self.store, "synthetic-only-password")
        cookie = password.login(actor["email"], "synthetic-only-password")
        seeded = password.authenticate({"Cookie": f"zf_session={cookie}"})
        self.assertEqual(seeded["rule_roles"], [])
        with self.assertRaises(PermissionError):
            self.store.restart_decide(seeded, decision(s))
        app = App(self.store, provider=provider)
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            request = urllib.request.Request(
                f"http://127.0.0.1:{server.server_port}/api/continuity/restart-decide",
                data=json.dumps(decision(s)).encode(),
                headers={
                    "Content-Type": "application/json",
                    "X-ZF-CSRF": "1",
                    "X-MS-CLIENT-PRINCIPAL": principal(roles=roles, oid=actor["oid"]),
                },
            )
            with urllib.request.urlopen(request, timeout=10) as response:
                self.assertEqual(response.status, 200)
                self.assertTrue(json.load(response)["actual_hold"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(10)
            app.assistants.stop()

    def test_authority_revalidation(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], incident())
        actor = provision(self)
        s = propose(self, s)
        original = self.store.save

        def revoke_before_save() -> None:
            with self.store.dblock:
                current = dict(self.people["Programme Support Officer"], disabled=True)
                self.store.db.execute(
                    "UPDATE staff SET body=? WHERE email=?", (json.dumps(current), actor["email"])
                )
            original()

        with patch.object(self.store, "save", side_effect=revoke_before_save):
            with self.assertRaises(PermissionError):
                self.store.restart_decide(actor, decision(s))
        self.assertEqual(
            self.other().store.continuity_view(self.pm)["suspensions"][0]["status"], "Suspended"
        )


if __name__ == "__main__":
    unittest.main()
