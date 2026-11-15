"""HTTP continuity restart gate, suspension fallback, concurrent race, and old-image tests."""

import copy
import json
import os
import sqlite3
import subprocess
import sys
import textwrap
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Any

from zava_forward.core import assistants, challenges, continuity
from zava_forward.core.restart_authority import UNAPPOINTED_RESTART_AUTHORITY
from zava_forward.core.store import ConflictError

from test_assistants import Base, config, proposal
from test_auth import ENV, principal
from test_operator_suspension import fresh_release
from zava_forward.api.auth import PasswordProvider, TrustedProxyProvider
from zava_forward.api.server import App, make_handler

ASSISTANTS_MOD: Any = assistants
CHALLENGES_MOD: Any = challenges
CONTINUITY_MOD: Any = continuity
BASE_CLS: Any = Base
CONFIG_FN: Any = config
PROPOSAL_FN: Any = proposal
FRESH_RELEASE_FN: Any = fresh_release
PROXY_ENV: dict[str, str] = dict(ENV)
PRINCIPAL_FN: Any = principal
PASSWORD_PROVIDER_CLS: Any = PasswordProvider
TRUSTED_PROXY_CLS: Any = TrustedProxyProvider
APP_CLS: Any = App
MAKE_HANDLER_FN: Any = make_handler

CAP = "stock-prioritisation"
OTHER_CAP = "assessment-preparation"
PASSWORD_SECRET = "synthetic-password-secret-122"
AUTHORITY = "Building Safety Lead and Executive Sponsor (constructed fixture; not OD-35 live)"


def _incident(scope: str = CAP, **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "scope": scope,
        "reason": "Constructed unsupported-claim containment drill",
        "incident_owner": "Quality Inspector",
        "containment": "Stop affected AI proposals while manual workflow continues",
        "comms_owner": "Quality Inspector",
        "comms_audience": "Synthetic retrofit staff",
        "evidence": "synthetic:incident-122",
        "resident_impact": "Manual casework, challenge and hazard channels remain open",
        "remediation": "Fix prompt grounding and rerun negative control suite",
        "restart_authority": AUTHORITY,
        "synthetic": True,
        "trigger": "guardrail breach",
    }
    body.update(overrides)
    return body


def _propose_payload(
    sid: str,
    *,
    test_id: str = "constructed-negative-pack-122",
    corrective_evidence: str = "synthetic:corrective-tests-122",
    result: str = "Pass",
) -> dict[str, Any]:
    return {
        "id": sid,
        "test_id": test_id,
        "corrective_evidence": corrective_evidence,
        "result": result,
        "evidence_class": "constructed-fixture",
    }


def _decide_payload(
    suspension: dict[str, Any],
    *,
    decision: str = "Restart",
    authority_ref: str | None = None,
) -> dict[str, Any]:
    return {
        "id": suspension["id"],
        "epoch": suspension["proposal"]["epoch"],
        "proposal_digest": suspension["proposal"]["digest"],
        "decision": decision,
        "authority_ref": authority_ref or suspension["restart_authority"],
    }


class ContinuityRestartGateTests(BASE_CLS):  # type: ignore[misc]
    service: Any

    def setUp(self) -> None:
        super().setUp()
        self.service.stop()
        self.service = ASSISTANTS_MOD.Assistants(self.store, CONFIG_FN(active_calls=4))

    def _provision_proxy_actor(
        self,
        role_name: str,
        oid: str,
        *,
        store: Any = None,
        rule_roles: list[str] | None = None,
    ) -> dict[str, Any]:
        target_store = store or self.store
        person: dict[str, Any] = dict(self.people[role_name])
        person["oid"] = oid
        with target_store.dblock:
            row = target_store.db.execute(
                "SELECT body FROM staff WHERE email=?", (person["email"],)
            ).fetchone()
            current = json.loads(row[0])
            current["oid"] = oid
            target_store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(current), person["email"]),
            )
            if person["email"] in target_store.staff:
                target_store.staff[person["email"]]["oid"] = oid
        return {
            **person,
            "auth_provider": "trusted-proxy",
            "rule_roles": list(rule_roles if rule_roles is not None else ["ai_restart"]),
        }

    def _http_req(
        self,
        port: int,
        method: str,
        path: str,
        headers: dict[str, str],
        body: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any]]:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req_headers = {"X-ZF-CSRF": "1", **headers}
        if data is not None:
            req_headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}{path}",
            data=data,
            headers=req_headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            try:
                raw = err.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                return err.code, parsed
            finally:
                err.close()

    def _proxy_headers(
        self,
        email: str,
        oid: str,
        *roles: str,
    ) -> dict[str, str]:
        return {
            "X-ZF-CSRF": "1",
            "X-MS-CLIENT-PRINCIPAL": str(PRINCIPAL_FN(roles=roles, oid=oid, email=email)),
        }

    def test_http_restart_gate_rejects_placeholder_view_only_self_replay_and_stale(self) -> None:
        qi = self._provision_proxy_actor(
            "Quality Inspector", "00000000-0000-0000-0000-000000000301", rule_roles=[]
        )
        pm = self._provision_proxy_actor(
            "Retrofit Programme Manager", "00000000-0000-0000-0000-000000000302", rule_roles=[]
        )
        pso = self._provision_proxy_actor(
            "Programme Support Officer", "00000000-0000-0000-0000-000000000303"
        )
        provider = TRUSTED_PROXY_CLS(self.store, dict(PROXY_ENV))
        app = APP_CLS(self.store, provider=provider)
        server = ThreadingHTTPServer(("127.0.0.1", 0), MAKE_HANDLER_FN(app))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            port = server.server_port
            qi_hdr = self._proxy_headers(qi["email"], qi["oid"], "ZavaForward.QualityInspector")
            pm_hdr = self._proxy_headers(pm["email"], pm["oid"], "ZavaForward.ProgrammeManager")
            pso_hdr = self._proxy_headers(
                pso["email"],
                pso["oid"],
                "ZavaForward.SupportOfficer",
                "ZavaForward.AIRestart",
            )
            pso_no_role = self._proxy_headers(
                pso["email"], pso["oid"], "ZavaForward.SupportOfficer"
            )
            pm_oid_alias_hdr = self._proxy_headers(
                "distinct-alias-pm@example.test",
                pm["oid"],
                "ZavaForward.SupportOfficer",
                "ZavaForward.AIRestart",
            )
            qi_oid_alias_hdr = self._proxy_headers(
                "distinct-alias-qi@example.test",
                qi["oid"],
                "ZavaForward.SupportOfficer",
                "ZavaForward.AIRestart",
            )
            pm_self_hdr = self._proxy_headers(
                pm["email"],
                pm["oid"],
                "ZavaForward.ProgrammeManager",
                "ZavaForward.AIRestart",
            )
            qi_self_hdr = self._proxy_headers(
                qi["email"],
                qi["oid"],
                "ZavaForward.QualityInspector",
                "ZavaForward.AIRestart",
            )
            view_only_hdr = self._proxy_headers(
                "auditor-unlisted@example.test",
                "00000000-0000-0000-0000-000000000399",
                "ZavaForward.ApplicationAdmin",
                "ZavaForward.AIRestart",
            )

            # View-only unlisted proxy user cannot suspend.
            code, _ = self._http_req(
                port, "POST", "/api/continuity/suspend", view_only_hdr, _incident()
            )
            self.assertEqual(code, 403)

            code, suspended = self._http_req(
                port, "POST", "/api/continuity/suspend", qi_hdr, _incident()
            )
            self.assertEqual(code, 200, suspended)
            sid = suspended["id"]

            # Placeholder corrective evidence fails with 400; suspender self-propose fails with 403.
            code, _ = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                pm_hdr,
                _propose_payload(sid, corrective_evidence="TBD"),
            )
            self.assertEqual(code, 400)
            code, _ = self._http_req(
                port, "POST", "/api/continuity/restart-propose", qi_hdr, _propose_payload(sid)
            )
            self.assertEqual(code, 403)
            code, _ = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                view_only_hdr,
                _propose_payload(sid),
            )
            self.assertEqual(code, 403)

            code, p1 = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                pm_hdr,
                _propose_payload(
                    sid,
                    test_id="drill-pack-alpha",
                    corrective_evidence="synthetic:pack-alpha-122",
                ),
            )
            self.assertEqual(code, 200, p1)

            # Missing capability, OID-alias self-approval, self-approval, and view-only fail 403.
            for bad_hdr in (
                pso_no_role,
                pm_oid_alias_hdr,
                qi_oid_alias_hdr,
                pm_self_hdr,
                qi_self_hdr,
                view_only_hdr,
            ):
                code, _ = self._http_req(
                    port, "POST", "/api/continuity/restart-decide", bad_hdr, _decide_payload(p1)
                )
                self.assertEqual(code, 403)
            code, _ = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-decide",
                pso_hdr,
                _decide_payload(p1, authority_ref=UNAPPOINTED_RESTART_AUTHORITY),
            )
            self.assertEqual(code, 403)

            # Keep suspended consumes digest and rejects replaying the rejected claim.
            code, kept_view = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-decide",
                pso_hdr,
                _decide_payload(p1, decision="Keep suspended"),
            )
            self.assertEqual(code, 200, kept_view)
            code, _ = self._http_req(
                port, "POST", "/api/continuity/restart-decide", pso_hdr, _decide_payload(p1)
            )
            self.assertEqual(code, 403)
            code, _ = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                pm_hdr,
                _propose_payload(
                    sid,
                    test_id="drill-pack-alpha",
                    corrective_evidence="synthetic:pack-alpha-122",
                ),
            )
            self.assertEqual(code, 403)

            # Superseded proposal P2 becomes stale once P3 is proposed; P3 succeeds once.
            code, p2 = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                pm_hdr,
                _propose_payload(
                    sid,
                    test_id="drill-pack-beta",
                    corrective_evidence="synthetic:pack-beta-122",
                ),
            )
            self.assertEqual(code, 200)
            code, p3 = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                pm_hdr,
                _propose_payload(
                    sid,
                    test_id="drill-pack-gamma",
                    corrective_evidence="synthetic:pack-gamma-122",
                ),
            )
            self.assertEqual(code, 200)
            code, _ = self._http_req(
                port, "POST", "/api/continuity/restart-decide", pso_hdr, _decide_payload(p2)
            )
            self.assertEqual(code, 403)

            code, restarted = self._http_req(
                port, "POST", "/api/continuity/restart-decide", pso_hdr, _decide_payload(p3)
            )
            self.assertEqual(code, 200, restarted)
            self.assertEqual(restarted["status"], "Restarted")
            self.assertEqual(restarted["restart"]["new_epoch"], 2)

            code, _ = self._http_req(
                port, "POST", "/api/continuity/restart-decide", pso_hdr, _decide_payload(p3)
            )
            self.assertIn(code, (400, 403))
            audit_actions = [row["action"] for row in self.store.audit_entries()]
            self.assertIn("ai_restart_propose_denied", audit_actions)
            self.assertIn("ai_restart_decide_denied", audit_actions)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(10)
            app.assistants.stop()

    def test_manual_casework_accessible_challenge_and_hazard_response_during_all_suspension(
        self,
    ) -> None:
        # Assign ZF-1 to self.pm and prepare a pre-suspension priority challenge target.
        self.case(lambda c: c.__setitem__("owner_code", self.pm["code"]))
        self.store.cases["ZF-1"]["owner_code"] = self.pm["code"]
        rlo = self.people["Resident Liaison Officer"]
        bsl = self.people["Building Safety Liaison"]
        qi = self.people["Quality Inspector"]
        bsl2 = dict(
            bsl,
            code="BSL-SYN-2",
            name="SYN Second Safety Liaison",
            email="bsl2-syn@example.test",
            oid="00000000-0000-0000-0000-000000000402",
        )
        with self.store.lock:
            self.store.data["staff"].append(bsl2)
            self.store.staff[bsl2["email"]] = bsl2
            with self.store.dblock:
                self.store.db.execute(
                    "INSERT INTO staff(email, body) VALUES (?, ?)",
                    (bsl2["email"].lower(), json.dumps(bsl2)),
                )
            self.store.save()
        suggestion = self.store.ai_priority(self.pm, mode="workflow-only")
        self.store.resolve_priority(self.pm, suggestion["id"], "accept")
        pso = self._provision_proxy_actor(
            "Programme Support Officer", "00000000-0000-0000-0000-000000000403"
        )

        password = PASSWORD_PROVIDER_CLS(self.store, PASSWORD_SECRET)
        pm_cookie = {"Cookie": f"zf_session={password.login(self.pm['email'], PASSWORD_SECRET)}"}
        rlo_cookie = {"Cookie": f"zf_session={password.login(rlo['email'], PASSWORD_SECRET)}"}
        bsl_cookie = {"Cookie": f"zf_session={password.login(bsl['email'], PASSWORD_SECRET)}"}
        bsl2_cookie = {"Cookie": f"zf_session={password.login(bsl2['email'], PASSWORD_SECRET)}"}
        qi_cookie = {"Cookie": f"zf_session={password.login(qi['email'], PASSWORD_SECRET)}"}
        pso_cookie = {"Cookie": f"zf_session={password.login(pso['email'], PASSWORD_SECRET)}"}

        app = APP_CLS(self.store, provider=password)
        server = ThreadingHTTPServer(("127.0.0.1", 0), MAKE_HANDLER_FN(app))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            port = server.server_port
            # Suspend ALL AI scopes over HTTP.
            code, cont = self._http_req(
                port, "POST", "/api/continuity/suspend", qi_cookie, _incident("all")
            )
            self.assertEqual(code, 200, cont)
            provider_calls_before = self.provider.calls

            # Deterministic priority fallback stays available during suspension without AI output,
            # while assistant invocation over HTTP is blocked with 403.
            code, wf_prio = self._http_req(
                port, "POST", "/api/ai/priority", pm_cookie, {"mode": "workflow-only"}
            )
            self.assertEqual(code, 200, wf_prio)
            self.assertEqual(wf_prio["source"], "template")
            code, ai_prio = self._http_req(
                port, "POST", "/api/ai/priority", pm_cookie, {"mode": "ai"}
            )
            self.assertEqual(code, 200, ai_prio)
            self.assertEqual(ai_prio["source"], "template")
            code, invoked = self._http_req(
                port,
                "POST",
                f"/api/assistants/{OTHER_CAP}/invoke",
                pm_cookie,
                {"case_id": "ZF-1"},
            )
            self.assertEqual(code, 202, invoked)
            self.assertEqual(invoked["state"], "disabled")
            self.assertFalse(invoked["actionable"])
            self.assertEqual(invoked["suspension"], cont["id"])

            code, case_before = self._http_req(port, "GET", "/api/cases/ZF-1", rlo_cookie)
            self.assertEqual(code, 200)
            target = next(
                row
                for row in case_before["challenge_targets"]
                if row["proposal_id"] == suggestion["id"]
            )

            # 1. Manual casework call logging succeeds during 'all' suspension.
            code, after_call = self._http_req(
                port,
                "POST",
                "/api/cases/ZF-1/call",
                rlo_cookie,
                {
                    "outcome": "Spoke",
                    "note": "SYN manual liaison visit arranged during all-AI suspension",
                    "channel": "Phone",
                },
            )
            self.assertEqual(code, 200, after_call)
            self.assertEqual(
                after_call["contacts"][-1]["note"],
                "SYN manual liaison visit arranged during all-AI suspension",
            )

            # 2. Accessible challenge succeeds on BOTH Digital and non-digital Phone routes and
            # records human correction without invoking AI.
            base_challenge = {
                "action": "challenge_open",
                "proposal_id": suggestion["id"],
                "proposal_version": target["proposal_version"],
                "decision_version": target["decision_version"],
                "target_kind": "source",
                "source": "SYN-CHALLENGE-EVIDENCE-122",
                "request": "SYN resident requests human review of heating notes",
                "explanation": "SYN plain-language explanation recorded during AI suspension",
                "owner": rlo["email"],
                "non_digital_route": "SYN Phone RLO desk or send Freepost letter.",
                "next_update": "2099-02-01",
            }
            raw_case_before = copy.deepcopy(self.store.cases["ZF-1"])
            for channel in ("Digital", "Phone", "Letter", "In person"):
                code, ch_detail = self._http_req(
                    port,
                    "POST",
                    "/api/cases/ZF-1/resident",
                    rlo_cookie,
                    {**base_challenge, "channel": channel},
                )
                self.assertEqual(code, 200, ch_detail)
            ch_id = ch_detail["affected_challenges"][0]["id"]
            ch_ver = ch_detail["affected_challenges"][0]["version"]
            code, updated_detail = self._http_req(
                port,
                "POST",
                "/api/cases/ZF-1/resident",
                rlo_cookie,
                {
                    "action": "challenge_update",
                    "id": ch_id,
                    "expected_version": ch_ver,
                    "channel": "Phone",
                    "source": "SYN-CHALLENGE-UPDATE-122",
                    "request": "SYN resident supplied manual meter note by telephone",
                    "explanation": "SYN plain-language update logged while AI is suspended",
                    "next_update": "2099-02-02",
                },
            )
            self.assertEqual(code, 200, updated_detail)
            ch_ver = updated_detail["affected_challenges"][0]["version"]
            code, escalated_detail = self._http_req(
                port,
                "POST",
                "/api/cases/ZF-1/resident",
                rlo_cookie,
                {
                    "action": "challenge_escalate",
                    "id": ch_id,
                    "expected_version": ch_ver,
                    "owner": self.pm["email"],
                    "reason": "SYN escalated to programme manager during all-AI suspension",
                    "next_update": "2099-02-03",
                },
            )
            self.assertEqual(code, 200, escalated_detail)
            ch_ver = escalated_detail["affected_challenges"][0]["version"]
            code, resolved_detail = self._http_req(
                port,
                "POST",
                "/api/cases/ZF-1/resident",
                pm_cookie,
                {
                    "action": "challenge_resolve",
                    "id": ch_id,
                    "expected_version": ch_ver,
                    "resolution": "Correction recorded",
                    "resolution_ref": "SYN human officer corrected record",
                    "explanation": "SYN checked manually while AI remains suspended",
                    "next_update": "2099-02-04",
                },
            )
            self.assertEqual(code, 200, resolved_detail)
            CHALLENGES_MOD.assert_no_adverse_challenge_effects(
                raw_case_before, self.store.cases["ZF-1"]
            )
            self.assertTrue(
                next(
                    row
                    for row in resolved_detail["challenge_targets"]
                    if row["proposal_id"] == suggestion["id"]
                )["review_stale"]
            )

            # PasswordProvider restart-decide returns 403 and records ai_restart_decide_denied
            # even after a valid corrective proposal is recorded.
            code, pw_proposed = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-propose",
                pm_cookie,
                _propose_payload(
                    cont["id"],
                    test_id="pw-route-denial-pack-122",
                    corrective_evidence="synthetic:pw-route-denial-122",
                ),
            )
            self.assertEqual(code, 200, pw_proposed)
            code, _ = self._http_req(
                port,
                "POST",
                "/api/continuity/restart-decide",
                pso_cookie,
                _decide_payload(pw_proposed),
            )
            self.assertEqual(code, 403)
            self.assertIn(
                "ai_restart_decide_denied",
                [row["action"] for row in self.store.audit_entries()],
            )

            # 3. Independent statutory hazard response executes end-to-end even when SQL
            # gate_version is ALSO mismatched (simulating mixed-rollout containment).
            with self.store.dblock:
                self.store.db.execute(
                    "UPDATE continuity_gate_state SET gate_version='continuity-gate-v99' WHERE id=1"
                )
            code, hz_raised = self._http_req(
                port,
                "POST",
                "/api/cases/ZF-1/hazard-raise",
                rlo_cookie,
                {
                    "category": "Damp and mould",
                    "priority": "Emergency",
                    "note": "SYN emergency damp hazard reported during AI suspension",
                    "source": "SYN emergency telephone line",
                    "aware_at": "2026-10-01T08:00:00Z",
                },
            )
            self.assertEqual(code, 200, hz_raised)
            hz_index = len(hz_raised["hazards"]) - 1
            for endpoint, actor_hdr, payload in (
                (
                    "hazard-refer",
                    rlo_cookie,
                    {
                        "index": hz_index,
                        "to": bsl["email"],
                        "job": "SYN-JOB-122",
                        "evidence": "SYN emergency referral",
                    },
                ),
                (
                    "hazard-receive",
                    bsl_cookie,
                    {"index": hz_index, "evidence": "SYN repairs receipt"},
                ),
                (
                    "hazard-accept",
                    bsl_cookie,
                    {"index": hz_index, "evidence": "SYN safety ownership accepted"},
                ),
                (
                    "hazard-repaired",
                    bsl_cookie,
                    {"index": hz_index, "evidence": "SYN emergency make-safe completed"},
                ),
                (
                    "hazard-release",
                    bsl2_cookie,
                    {
                        "index": hz_index,
                        "note": "SYN verified safe by second building safety liaison",
                        "evidence": "SYN post-repair inspection certificate",
                    },
                ),
            ):
                code, hz_step = self._http_req(
                    port, "POST", f"/api/cases/ZF-1/{endpoint}", actor_hdr, payload
                )
                self.assertEqual(code, 200, (endpoint, hz_step))
            self.assertTrue(hz_step["hazards"][hz_index]["released"])
            self.assertEqual(self.provider.calls, provider_calls_before)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(10)
            app.assistants.stop()

    def test_independent_sql_connections_observe_suspend_hold_and_restart_immediately(self) -> None:
        ready = self.run_ready(CAP)
        queued = self.service.invoke(self.pm, CAP, "ZF-2")
        leased_task = self.service.invoke(self.pm, CAP, "ZF-3")
        leased_claim = self.service.claim(leased_task["id"], "worker-before-suspend")
        self.assertIsNotNone(leased_claim)

        peer_service = self.other()
        peer_store = peer_service.store
        peer_store.ai = self.store.ai

        # Node A suspends; Node B (separate SQLite connection) immediately sees hold.
        s = self.store.suspend(
            self.people["Quality Inspector"],
            _incident(CAP),
            assistant_affected=self.service.affected(CAP),
        )
        self.assertIsNotNone(peer_store.continuity_block(CAP))
        self.assertFalse(peer_service.detail(self.pm, ready["id"])["actionable"])
        self.assertIsNone(peer_service.claim(queued["id"], "peer-worker-during-suspend"))
        with self.assertRaises(PermissionError):
            peer_service.review(
                self.pm,
                ready["id"],
                "verify",
                ready["revision"],
                "Blocked on peer connection.",
                source_verified=True,
            )

        # In-flight leased task returning on Node B during suspension is quarantined.
        self.assertTrue(
            peer_service.complete(
                leased_claim,
                {"outcome": "returned", "source": "ai", "usage": None, "model": "test-model"},
                PROPOSAL_FN(leased_claim["snapshot"]),
            )
        )
        self.assertEqual(peer_service.detail(self.pm, leased_task["id"])["state"], "quarantined")

        # Node B proposes corrective evidence; distinct authorized human approves on Node A.
        pso = self._provision_proxy_actor(
            "Programme Support Officer", "00000000-0000-0000-0000-000000000311"
        )
        proposed = peer_store.restart_propose(self.pm, _propose_payload(s["id"]))
        self.store.restart_decide(pso, _decide_payload(proposed))
        FRESH_RELEASE_FN(self, CAP)

        # Node B immediately sees epoch=2, cleared constructed hold (actual_hold kept true),
        # and old queued/ready non-actionable, while fresh epoch=2 invocation succeeds.
        self.assertIsNotNone(peer_store.continuity_block(CAP))
        with peer_service.transaction() as peer_db:
            self.assertIsNone(peer_service.suspended(peer_db, CAP))
        self.assertEqual(peer_store.continuity_epoch(), 2)
        self.assertIsNone(peer_service.claim(queued["id"], "peer-worker-after-restart"))
        old_ready_detail = peer_service.detail(self.pm, ready["id"])
        self.assertFalse(old_ready_detail["epoch_current"])
        self.assertFalse(old_ready_detail["actionable"])
        fresh = peer_service.invoke(self.pm, CAP, "ZF-1")
        self.assertEqual(fresh["continuity_epoch"], 2)
        self.assertTrue(peer_service.execute(fresh["id"]))
        self.assertTrue(peer_service.detail(self.pm, fresh["id"])["actionable"])

    def _run_suspend_vs_accept_trial(self, trial: int) -> None:
        cap = CAP if trial % 2 == 0 else OTHER_CAP
        is_verify_race = trial == 0
        ready = self.run_ready(cap) if is_verify_race else self.verify(self.run_ready(cap))
        peer_service = self.other()
        peer_store = peer_service.store
        peer_store.ai = self.store.ai
        barrier = threading.Barrier(2)
        outcomes: dict[str, Any] = {}

        def run_suspend() -> None:
            barrier.wait(timeout=10)
            outcomes["suspend"] = self.store.suspend(
                self.people["Quality Inspector"],
                _incident(cap, evidence=f"synthetic:race-{trial}"),
                assistant_affected=self.service.affected(cap),
            )

        def run_review() -> None:
            barrier.wait(timeout=10)
            try:
                if is_verify_race:
                    outcomes["review"] = peer_service.review(
                        self.pm,
                        ready["id"],
                        "verify",
                        ready["revision"],
                        f"Concurrent verify {trial}",
                        source_verified=True,
                    )
                else:
                    outcomes["review"] = peer_service.review(
                        self.pm,
                        ready["id"],
                        "accept",
                        ready["revision"],
                        f"Concurrent disposition {trial}",
                    )
            except PermissionError as exc:
                outcomes["review_err"] = str(exc)

        t1 = threading.Thread(target=run_suspend)
        t2 = threading.Thread(target=run_review)
        t1.start()
        t2.start()
        t1.join(15)
        t2.join(15)

        s = outcomes["suspend"]
        raw_s = next(
            row for row in self.store.data["continuity"]["suspensions"] if row["id"] == s["id"]
        )
        after = peer_service.detail(self.pm, ready["id"])
        self.assertFalse(after["actionable"])
        if "review" in outcomes:
            affected = {row["id"]: row for row in raw_s["affected_assistant_tasks"]}
            self.assertIn(ready["id"], affected)
            expected_state = "ready" if is_verify_race else "accepted"
            self.assertEqual(affected[ready["id"]]["state"], expected_state)
        else:
            self.assertIn("review_err", outcomes)
            self.assertEqual(after["state"], "ready")

        pso = self._provision_proxy_actor(
            "Programme Support Officer",
            f"00000000-0000-0000-0000-00000000032{trial}",
        )
        proposed = self.store.restart_propose(
            self.pm,
            _propose_payload(
                s["id"],
                test_id=f"race-suite-{trial}",
                corrective_evidence=f"synthetic:race-fix-{trial}",
            ),
        )
        self.store.restart_decide(pso, _decide_payload(proposed))
        FRESH_RELEASE_FN(self, cap)
        exported = next(
            row for row in peer_service.export()["proposals"] if row["id"] == ready["id"]
        )
        self.assertFalse(exported["epoch_current"])
        self.assertFalse(exported["relied_on"])

    def test_concurrent_suspend_vs_verify_and_accept_ready_proposal_race(self) -> None:
        for trial in range(3):
            with self.subTest(trial=trial):
                self._run_suspend_vs_accept_trial(trial)

    def test_concurrent_suspend_vs_claim_queued_and_send_leased_proposal_race(self) -> None:
        queued = self.service.invoke(self.pm, CAP, "ZF-1")
        leased = self.service.invoke(self.pm, CAP, "ZF-2")
        claim = self.service.claim(leased["id"], "worker-leased-before-suspend")
        self.assertIsNotNone(claim)

        peer_service = self.other()
        peer_store = peer_service.store
        peer_store.ai = self.store.ai

        # 1. Barrier race: suspend on Store A vs claim(queued) on Service B.
        barrier = threading.Barrier(2)
        claim_box: dict[str, Any] = {}

        def do_suspend() -> None:
            barrier.wait(timeout=10)
            claim_box["suspended"] = self.store.suspend(
                self.people["Quality Inspector"], _incident(CAP)
            )

        def do_claim() -> None:
            barrier.wait(timeout=10)
            claim_box["claimed"] = peer_service.claim(queued["id"], "racing-claimer")

        t1 = threading.Thread(target=do_suspend)
        t2 = threading.Thread(target=do_claim)
        t1.start()
        t2.start()
        t1.join(15)
        t2.join(15)

        # Even if claim won before suspend committed, _fence_in MUST refuse transitioning to
        # 'sending' once continuity_open_holds contains CAP!
        calls_before = self.provider.calls
        with peer_service.transaction() as db:
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute(
                    "UPDATE assistant_attempts SET outcome='sending', send_gate_version=? "
                    "WHERE id=?",
                    (
                        CONTINUITY_MOD.GATE_VERSION,
                        f"{leased['id']}:{claim['fence']}",
                    ),
                )
        # Normal _fence_in checks suspended() first and settles cleanly without calling AI.
        with peer_service.transaction() as db:
            reason = peer_service._fence_in(
                db,
                f"{leased['id']}:{claim['fence']}",
                CAP,
            )
            self.assertIsNotNone(reason)
        self.assertEqual(self.provider.calls, calls_before)

        if claim_box["claimed"] is not None:
            raced = claim_box["claimed"]
            self.assertTrue(
                peer_service.complete(
                    raced,
                    {"outcome": "returned", "source": "ai", "usage": None, "model": "test-model"},
                    PROPOSAL_FN(raced["snapshot"]),
                )
            )
            self.assertEqual(peer_service.detail(self.pm, queued["id"])["state"], "quarantined")
        else:
            self.assertIsNone(peer_service.claim(queued["id"], "post-suspend-claimer"))

        # 2. Barrier race: suspend on Store A vs _fence_in + complete on a leased OTHER_CAP claim.
        leased_other = self.service.invoke(self.pm, OTHER_CAP, "ZF-3")
        other_claim = self.service.claim(leased_other["id"], "racing-sender")
        self.assertIsNotNone(other_claim)
        send_barrier = threading.Barrier(2)
        send_box: dict[str, Any] = {}

        def do_suspend_other() -> None:
            send_barrier.wait(timeout=10)
            send_box["suspended"] = self.store.suspend(
                self.people["Quality Inspector"], _incident(OTHER_CAP)
            )

        def do_fence_and_complete() -> None:
            send_barrier.wait(timeout=10)
            with peer_service.transaction() as db:
                send_box["fence_err"] = peer_service._fence_in(
                    db,
                    f"{leased_other['id']}:{other_claim['fence']}",
                    OTHER_CAP,
                )
            if send_box["fence_err"] is None:
                send_box["completed"] = peer_service.complete(
                    other_claim,
                    {"outcome": "returned", "source": "ai", "usage": None, "model": "test-model"},
                    PROPOSAL_FN(other_claim["snapshot"]),
                )

        ts1 = threading.Thread(target=do_suspend_other)
        ts2 = threading.Thread(target=do_fence_and_complete)
        ts1.start()
        ts2.start()
        ts1.join(15)
        ts2.join(15)
        other_detail = peer_service.detail(self.pm, leased_other["id"])
        self.assertFalse(other_detail["actionable"])
        if send_box["fence_err"] is None:
            self.assertIn(other_detail["state"], ("ready", "quarantined"))
        else:
            self.assertNotEqual(other_detail["state"], "ready")

    def test_concurrent_restart_decide_races_allow_at_most_one_winner(self) -> None:
        s = self.store.suspend(self.people["Quality Inspector"], _incident(CAP))
        proposed = self.store.restart_propose(
            self.pm,
            _propose_payload(
                s["id"],
                test_id="concurrent-decide-pack",
                corrective_evidence="synthetic:concurrent-decide-122",
            ),
        )
        decide = _decide_payload(proposed)
        pso_a = self._provision_proxy_actor(
            "Programme Support Officer", "00000000-0000-0000-0000-000000000331"
        )
        peer_service = self.other()
        peer_store = peer_service.store
        peer_store.ai = self.store.ai
        bsl_approver = self._provision_proxy_actor(
            "Building Safety Liaison",
            "00000000-0000-0000-0000-000000000332",
            store=peer_store,
        )
        # Refresh self.store staff OID visibility as well.
        self._provision_proxy_actor(
            "Building Safety Liaison", "00000000-0000-0000-0000-000000000332"
        )

        barrier = threading.Barrier(2)
        successes: list[dict[str, Any]] = []
        errors: list[Exception] = []
        lock = threading.Lock()

        def try_decide(target_store: Any, actor: dict[str, Any]) -> None:
            barrier.wait(timeout=10)
            try:
                res = target_store.restart_decide(actor, copy.deepcopy(decide))
                with lock:
                    successes.append(res)
            except (PermissionError, ConflictError, ValueError) as exc:
                with lock:
                    errors.append(exc)

        t1 = threading.Thread(target=try_decide, args=(self.store, pso_a))
        t2 = threading.Thread(target=try_decide, args=(peer_store, bsl_approver))
        t1.start()
        t2.start()
        t1.join(15)
        t2.join(15)

        self.assertEqual(len(successes), 1, (successes, errors))
        self.assertEqual(len(errors), 1, (successes, errors))
        reopened = self.other().store
        self.assertEqual(reopened.continuity_epoch(), 2)
        self.assertEqual(
            reopened.continuity_view(self.pm)["suspensions"][-1]["status"], "Restarted"
        )

    def test_queued_leased_and_ready_proposals_across_full_suspend_and_restart_lifecycle(
        self,
    ) -> None:
        ready = self.run_ready(CAP)
        queued = self.service.invoke(self.pm, CAP, "ZF-2")
        leased_during = self.service.invoke(self.pm, CAP, "ZF-3")
        leased_across = self.service.invoke(self.pm, CAP, "ZF-4")
        leased_permitted = self.service.invoke(self.pm, CAP, "ZF-5")
        leased_other = self.service.invoke(self.pm, OTHER_CAP, "ZF-1")
        claim_during = self.service.claim(leased_during["id"], "worker-during")
        claim_across = self.service.claim(leased_across["id"], "worker-across")
        claim_permitted = self.service.claim(leased_permitted["id"], "worker-permitted")
        claim_other = self.service.claim(leased_other["id"], "worker-other")
        self.assertIsNotNone(claim_during)
        self.assertIsNotNone(claim_across)
        self.assertIsNotNone(claim_permitted)
        self.assertIsNotNone(claim_other)
        with self.service.transaction() as db:
            self.service.event(
                db,
                leased_permitted["id"],
                kind="permitted",
                owner="worker-permitted",
                fence=claim_permitted["fence"],
            )

        # Suspend CAP: queued cannot claim, ready is non-actionable, leased_during is quarantined.
        s = self.store.suspend(
            self.people["Quality Inspector"],
            _incident(CAP),
            assistant_affected=self.service.affected(CAP),
        )
        self.assertIsNone(self.service.claim(queued["id"], "blocked-claimer"))
        self.assertFalse(self.service.detail(self.pm, ready["id"])["actionable"])
        self.assertTrue(
            self.service.complete(
                claim_during,
                {"outcome": "returned", "source": "ai", "usage": None, "model": "test-model"},
                PROPOSAL_FN(claim_during["snapshot"]),
            )
        )
        self.assertEqual(self.service.detail(self.pm, leased_during["id"])["state"], "quarantined")

        # Restart CAP via distinct authorized human approval -> epoch advances from 1 to 2.
        pso = self._provision_proxy_actor(
            "Programme Support Officer", "00000000-0000-0000-0000-000000000341"
        )
        proposed = self.store.restart_propose(
            self.pm,
            _propose_payload(
                s["id"],
                test_id="full-lifecycle-pack-122",
                corrective_evidence="synthetic:full-lifecycle-122",
            ),
        )
        self.store.restart_decide(pso, _decide_payload(proposed))
        FRESH_RELEASE_FN(self, CAP)

        # After epoch bump:
        # - prior-epoch queued cannot be claimed;
        # - prior-epoch leased_across completing after restart is quarantined by epoch fence;
        # - expired leased_permitted with 'permitted' marker fails closed with blocked-reclaim;
        # - unaffected OTHER_CAP leased_other completes ready;
        # - prior-epoch ready stays non-actionable (can only be rejected);
        # - fresh post-restart proposal runs cleanly at epoch 2.
        self.assertIsNone(self.service.claim(queued["id"], "post-restart-claimer"))
        self.assertTrue(
            self.service.complete(
                claim_across,
                {"outcome": "returned", "source": "ai", "usage": None, "model": "test-model"},
                PROPOSAL_FN(claim_across["snapshot"]),
            )
        )
        self.assertEqual(self.service.detail(self.pm, leased_across["id"])["state"], "quarantined")
        self.expire(leased_permitted["id"])
        self.assertIsNone(self.service.claim(leased_permitted["id"], "post-restart-reclaim"))
        self.assertEqual(self.service.detail(self.pm, leased_permitted["id"])["state"], "failed")
        self.assertTrue(
            self.service.complete(
                claim_other,
                {"outcome": "returned", "source": "ai", "usage": None, "model": "test-model"},
                PROPOSAL_FN(claim_other["snapshot"]),
            )
        )
        self.assertEqual(self.service.detail(self.pm, leased_other["id"])["state"], "ready")
        with self.assertRaises(PermissionError):
            self.service.review(
                self.pm,
                ready["id"],
                "verify",
                ready["revision"],
                "Prior epoch cannot verify.",
                source_verified=True,
            )
        rejected = self.service.review(
            self.pm, ready["id"], "reject", ready["revision"], "Retire prior-epoch proposal."
        )
        self.assertEqual(rejected["state"], "rejected")

        fresh = self.run_ready(CAP)
        self.assertEqual(fresh["continuity_epoch"], 2)
        verified = self.verify(fresh)
        self.assertTrue(verified["actionable"])

    def test_old_image_worker_and_upgraded_ddl_fail_closed_across_queued_leased_and_ready(
        self,
    ) -> None:
        # 1. Legacy 8-column assistant_attempts + plain-JSON meta('continuity') DB upgrades cleanly.
        legacy_db_path = os.path.join(self.root, "legacy-upgrade.sqlite")
        raw = sqlite3.connect(legacy_db_path, isolation_level=None)
        try:
            raw.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            raw.execute(
                "INSERT INTO meta (key, value) VALUES ('continuity', ?)",
                (json.dumps({"epoch": 0, "suspensions": [], "changes": []}),),
            )
            raw.execute(
                "CREATE TABLE assistant_attempts ("
                "id TEXT PRIMARY KEY, task_id TEXT NOT NULL, fence INTEGER NOT NULL, "
                "pool TEXT NOT NULL, reserved INTEGER NOT NULL, actual INTEGER, "
                "outcome TEXT NOT NULL, active_until REAL NOT NULL DEFAULT 0)"
            )
            raw.execute(
                "INSERT INTO assistant_attempts VALUES "
                "('hist-1', 'T-HIST', 1, 'demo', 100, 80, 'returned', 0)"
            )
        finally:
            raw.close()
        from zava_forward.core.sqlstore import SqlStore

        sql_store_cls: Any = SqlStore
        upgraded_store = sql_store_cls(str(self.seed), legacy_db_path)
        upgraded_service = ASSISTANTS_MOD.Assistants(upgraded_store)
        try:
            with upgraded_service.transaction() as db:
                cols = {
                    row[1] for row in db.execute("PRAGMA table_info(assistant_attempts)").fetchall()
                }
                self.assertTrue({"capability", "gate_version", "send_gate_version"} <= cols)
                task_cols = {
                    row[1] for row in db.execute("PRAGMA table_info(assistant_tasks)").fetchall()
                }
                self.assertTrue({"review_gate_version", "reviewed_revision"} <= task_cols)
                gate = db.execute(
                    "SELECT gate_version, epoch FROM continuity_gate_state WHERE id=1"
                ).fetchone()
                self.assertEqual(gate, (CONTINUITY_MOD.GATE_VERSION, 0))
                wrapped_meta = json.loads(
                    db.execute("SELECT value FROM meta WHERE key='continuity'").fetchone()[0]
                )
                self.assertEqual(wrapped_meta["gate_version"], CONTINUITY_MOD.GATE_VERSION)
                self.assertEqual(wrapped_meta["epoch"], -1)
        finally:
            upgraded_service.stop()

        # 2. Subprocess old-image AND commit-invariant pre-gate worker against active queued,
        # leased, ready, and export paths (at epoch=0 before any suspension).
        ready = self.run_ready(CAP)
        ready_reject = self.run_ready(OTHER_CAP)
        queued_v0 = self.service.invoke(self.pm, CAP, "ZF-2")
        queued_pre = self.service.invoke(self.pm, CAP, "ZF-3")
        leased = self.service.invoke(self.pm, OTHER_CAP, "ZF-2")
        claim = self.service.claim(leased["id"], "current-worker")
        self.assertIsNotNone(claim)

        child_script = textwrap.dedent(
            """
            import json, sqlite3, sys
            from test_assistants import Provider, config
            from zava_forward.core import assistants, continuity
            from zava_forward.core.sqlstore import SqlStore

            (
                mode,
                seed_path,
                db_path,
                pm_email,
                queued_id,
                leased_id,
                leased_fence,
                ready_id,
                ready_reject_id,
                ready_reject_rev,
            ) = sys.argv[1:11]
            if mode == "gate-v0":
                continuity.GATE_VERSION = "continuity-gate-v0-old-image"
            elif mode == "pre-gate":
                # Simulate a pre-gate image lacking gate_hold and unwrap_sql.
                continuity.gate_hold = lambda *a, **kw: None
                continuity.sync_sql_gate = lambda *a, **kw: None
                continuity.load = lambda raw: (
                    {**continuity.blank(), **json.loads(raw)}
                    if isinstance(raw, str) and raw
                    else (dict(raw) if isinstance(raw, dict) else continuity.blank())
                )
            store = SqlStore(seed_path, db_path)
            store.ai = Provider()
            svc = assistants.Assistants(store, config())
            try:
                pm = store.staff[pm_email]
                exported = {row["id"]: row for row in svc.export()["proposals"]}
                ready_export = exported[ready_id]
                out = {
                    "continuity_blocked": bool(store.continuity_block("stock-prioritisation")),
                    "claim_queued": svc.claim(queued_id, f"{mode}-worker") is not None,
                    "ready_actionable": svc.detail(pm, ready_id)["actionable"],
                    "export_epoch_current": ready_export["epoch_current"],
                    "export_relied_on": ready_export["relied_on"],
                }
                if mode == "gate-v0":
                    ticket = svc.begin_call("stock-prioritisation", 120, "call-old-122")
                    out["begin_call_allowed"] = ticket.attempt is not None
                    with svc.transaction() as db:
                        try:
                            err = svc._fence_in(
                                db,
                                f"{leased_id}:{leased_fence}",
                                "assessment-preparation",
                            )
                            out["fence_leased"] = f"refused:{bool(err)}"
                        except Exception as exc:
                            out["fence_leased"] = f"error:{type(exc).__name__}"
                else:
                    # Pre-gate raw SQL attempts and verify/accept updates fail in SQLite triggers.
                    raw = sqlite3.connect(db_path, isolation_level=None)
                    try:
                        att_sql = (
                            "INSERT INTO assistant_attempts "
                            "(id, task_id, fence, pool, reserved, actual, outcome, active_until) "
                            "VALUES ('pre-gate-att', ?, 77, 'demo', 100, NULL, "
                            "'reserved', 9999999.0)"
                        )
                        ver_sql = (
                            "UPDATE assistant_tasks SET body=body, revision=revision+1 WHERE id=?"
                        )
                        acc_sql = (
                            "UPDATE assistant_tasks SET state='accepted', revision=revision+1 "
                            "WHERE id=?"
                        )
                        for key, sql, params in (
                            ("raw_pre_gate_attempt", att_sql, (queued_id,)),
                            ("raw_pre_gate_verify", ver_sql, (ready_id,)),
                            ("raw_pre_gate_accept", acc_sql, (ready_id,)),
                        ):
                            try:
                                raw.execute(sql, params)
                                out[key] = "allowed"
                            except sqlite3.IntegrityError:
                                out[key] = "blocked"
                    finally:
                        raw.close()
                    rej = svc.review(
                        pm,
                        ready_reject_id,
                        "reject",
                        int(ready_reject_rev),
                        "Retire from pre-gate node.",
                    )
                    out["reject_state"] = rej["state"]
                print(json.dumps(out))
            finally:
                svc.stop()
            """
        )
        repo_src = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        py_paths = [
            os.path.join(repo_src, "core", "src"),
            os.path.join(repo_src, "agents", "src"),
            os.path.join(repo_src, "api", "src"),
            os.path.join(repo_src, "api", "tests"),
            os.path.join(repo_src, "core", "tests"),
            os.path.join(repo_src, "agents", "tests"),
        ]
        env = dict(os.environ, PYTHONPATH=os.pathsep.join(py_paths))
        for mode, q_id in (("gate-v0", queued_v0["id"]), ("pre-gate", queued_pre["id"])):
            proc = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    child_script,
                    mode,
                    str(self.seed),
                    str(self.store.db_path),
                    str(self.pm["email"]),
                    str(q_id),
                    str(leased["id"]),
                    str(claim["fence"]),
                    str(ready["id"]),
                    str(ready_reject["id"]),
                    str(ready_reject["revision"]),
                ],
                capture_output=True,
                text=True,
                env=env,
                check=True,
                timeout=30,
            )
            result = json.loads(proc.stdout.strip().splitlines()[-1])
            self.assertTrue(result["continuity_blocked"], (mode, result))
            self.assertFalse(result["claim_queued"], (mode, result))
            self.assertFalse(result["ready_actionable"], (mode, result))
            self.assertFalse(result["export_epoch_current"], (mode, result))
            self.assertFalse(result["export_relied_on"], (mode, result))
            if mode == "gate-v0":
                self.assertFalse(result["begin_call_allowed"], result)
                self.assertIn(
                    result["fence_leased"], ("refused:True", "error:IntegrityError"), result
                )
            else:
                self.assertEqual(result["raw_pre_gate_attempt"], "blocked", result)
                self.assertEqual(result["raw_pre_gate_verify"], "blocked", result)
                self.assertEqual(result["raw_pre_gate_accept"], "blocked", result)
                self.assertEqual(result["reject_state"], "rejected", result)

    def test_mssql_ddl_and_trigger_shapes_include_continuity_gate_fences(self) -> None:
        from zava_forward.core import mssqlstore

        mssql_mod: Any = mssqlstore
        self.assertIn("continuity_gate_state", mssql_mod.TABLES)
        self.assertIn("continuity_open_holds", mssql_mod.TABLES)
        self.assertEqual(len(mssql_mod.GATE_TRIGGERS), 2)
        self.assertEqual(len(ASSISTANTS_MOD.MSSQL_ATTEMPT_TRIGGERS), 6)
        for stmt in ASSISTANTS_MOD.MSSQL_ATTEMPT_TRIGGERS:
            self.assertIn("THROW 50004", stmt)
        for ddl in ASSISTANTS_MOD.MSSQL_DDL[:3]:
            self.assertIn("COLLATE Latin1_General_100_BIN2", ddl)
        self.assertIn("reviewed_revision BIGINT NOT NULL DEFAULT 0", ASSISTANTS_MOD.MSSQL_DDL[2])

        # Verify ledger-safe 4-step column addition when sys.tables.ledger_type != 0 on MSSQL.
        executed: list[str] = []

        class _Cursor:
            def __init__(self, row: tuple[Any, ...] | None) -> None:
                self._row = row

            def fetchone(self) -> tuple[Any, ...] | None:
                return self._row

        class _LedgerDb:
            def execute(self, sql: str, params: tuple[Any, ...] = ()) -> _Cursor:
                executed.append(sql)
                if "COL_LENGTH" in sql:
                    return _Cursor((None,))
                if "SELECT ledger_type FROM sys.tables" in sql:
                    return _Cursor((2,))
                return _Cursor(None)

        dummy = object.__new__(ASSISTANTS_MOD.Assistants)
        dummy.mssql = True
        added = dummy._add_column(
            _LedgerDb(),
            "assistant_tasks",
            "review_gate_version",
            "VARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL DEFAULT ''",
        )
        self.assertTrue(added)
        self.assertEqual(
            executed[2:],
            [
                "ALTER TABLE assistant_tasks ADD review_gate_version "
                "VARCHAR(64) COLLATE Latin1_General_100_BIN2 NULL",
                "UPDATE assistant_tasks SET review_gate_version = '' "
                "WHERE review_gate_version IS NULL",
                "ALTER TABLE assistant_tasks ADD CONSTRAINT "
                "ck_assistant_tasks_review_gate_version_nn "
                "CHECK (review_gate_version IS NOT NULL)",
                "ALTER TABLE assistant_tasks ADD CONSTRAINT "
                "df_assistant_tasks_review_gate_version DEFAULT '' FOR review_gate_version",
            ],
        )
