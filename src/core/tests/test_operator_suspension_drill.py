"""RULE-024 restart authority and NFR-014 suspension/manual-fallback drill tests."""

import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
import release_support
from zava_forward.core import assistants, continuity, governance
from zava_forward.core.restart_authority import (
    RULE_024,
    UNAPPOINTED_RESTART_AUTHORITY,
    actor_snapshot,
    actors_for_store,
    ensure_distinct_restart_actor,
    reject_automatic_restart,
    validate_restart_authority,
)
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import GateError, Store

DATASET_MOD: Any = dataset
RELEASE_SUPPORT: Any = release_support
ASSISTANTS_MOD: Any = assistants
CONTINUITY_MOD: Any = continuity
GOVERNANCE_MOD: Any = governance
STORE_CLS: Any = Store
SQL_STORE_CLS: Any = SqlStore

CAPABILITY = "stock-prioritisation"
SECOND_CAPABILITY = "quality-evidence"
HUMAN_AUTHORITY = (
    "Building Safety Lead and Executive Sponsor (OD-35 synthetic fixture; not live authority)"
)


def _incident(scope: str = CAPABILITY, **overrides: Any) -> dict[str, Any]:
    body: dict[str, Any] = {
        "scope": scope,
        "reason": "Synthetic NFR-014 guardrail breach containment",
        "incident_owner": "Quality Inspector QI-1",
        "containment": "Stop affected AI proposals while manual workflow continues",
        "comms_owner": "Quality Inspector QI-1",
        "comms_audience": "Synthetic retrofit staff",
        "trigger": "guardrail breach",
        "evidence": "SYN-INCIDENT-221",
        "resident_impact": "Manual liaison continuity active; statutory safety unaffected",
        "remediation": "Correct citations and rerun synthetic verification pack",
        "restart_authority": HUMAN_AUTHORITY,
    }
    body.update(overrides)
    return body


def _person(code: str, role: str, oid: str, **extra: Any) -> dict[str, Any]:
    return {
        "code": code,
        "name": f"{role} {code}",
        "email": f"{code.lower()}@example.test",
        "role": role,
        "oid": oid,
        **extra,
    }


DRILL_STAFF: list[dict[str, Any]] = [
    _person("QI-1", "Quality Inspector", "00000000-0000-0000-0000-000000000101"),
    _person("PM-1", "Retrofit Programme Manager", "00000000-0000-0000-0000-000000000102"),
    _person("PM-2", "Retrofit Programme Manager", "00000000-0000-0000-0000-000000000103"),
    _person("BSL-1", "Building Safety Liaison", "00000000-0000-0000-0000-000000000104"),
    _person("BSL-2", "Building Safety Liaison", "00000000-0000-0000-0000-000000000105"),
    _person("RLO-1", "Resident Liaison Officer", "00000000-0000-0000-0000-000000000106"),
    _person(
        "PSO-1",
        "Programme Support Officer",
        "00000000-0000-0000-0000-000000000107",
        auth_provider="trusted-proxy",
        rule_roles=["ai_restart"],
    ),
]
ACTORS: dict[str, dict[str, Any]] = {row["code"]: row for row in DRILL_STAFF}

PROTOCOL: dict[str, Any] = {
    key: f"Synthetic demonstration {key}" for key, _ in GOVERNANCE_MOD.PROTOCOL_FIELDS
}
BENEFITS: dict[str, Any] = {
    key: f"Synthetic demonstration {key}" for key, _ in GOVERNANCE_MOD.BG011_FIELDS
}
BENEFITS.update(
    ai_denominator="per accepted handover",
    ai_quality_floor="Synthetic floor: no critical misses",
    ai_cost_components="Synthetic platform, review and assurance effort",
)
RELEASE_BODY: dict[str, Any] = {
    "scope_kind": "tranche",
    "scope": "Wave 1",
    "requirements": "RULE-020, RULE-024",
    "evidence": "Synthetic post-breach verification pack",
    "unresolved": "None",
    "envelope_ref": "ENV-DRILL-221",
    "economics_report_ref": "Synthetic AI economics report",
    "economics_limit_breach": "None",
    "approvers": ["Synthetic Executive Sponsor"],
    "decision": "Release",
    "synthetic": True,
}
BREACH_BODY: dict[str, Any] = {
    "scope_kind": "archetype",
    "scope": "Mid terrace",
    "owner": "Quality Inspector QI-1",
    "evidence": "SYN-BREACH-221 synthetic guardrail breach fixture",
    "containment": "Paused Mid terrace retrofit archetype pending remediation",
    "resident_impact": "Manual liaison continuity active; statutory safety unaffected",
    "remediation": "Verify citations and record post-breach release before restart",
    "restart_authority": HUMAN_AUTHORITY,
    "synthetic": True,
}


class RestartAuthorityUnitTest(unittest.TestCase):
    def test_validate_restart_authority_rejects_blank_placeholder_memory_and_ai(self) -> None:
        self.assertEqual(validate_restart_authority(HUMAN_AUTHORITY), HUMAN_AUTHORITY)
        for title in (
            "System Safety Director (OD-35 synthetic fixture)",
            "Workflow Programme Lead and Building Safety Sponsor",
            "Domain Model Governance Chair",
        ):
            self.assertEqual(validate_restart_authority(title), title)

        for blank in (None, "", "   "):
            with self.assertRaises(ValueError):
                validate_restart_authority(blank)

        for memory_ref in (
            "CM-0123456789abcdef",
            "Approved via memory:session-42",
            "Recorded in chat-memory note",
        ):
            with self.assertRaises(ValueError):
                validate_restart_authority(memory_ref)

        invalid_tokens = (
            "TBD",
            "tbd: awaiting sponsor",
            "Pending OD-35 appointment",
            "none",
            "N/A",
            "unknown",
            "unassigned",
            "placeholder",
            UNAPPOINTED_RESTART_AUTHORITY,
            "Unavailable: pending governance sign-off",
            "automatic",
            "auto-restart",
            "system",
            "system-cron",
            "ai",
            "agent",
            "model",
            "workflow",
            "scheduler",
            "self",
            "self-approved",
        )
        for bad in invalid_tokens:
            with self.subTest(token=bad):
                with self.assertRaises(ValueError):
                    validate_restart_authority(bad)
                with self.assertRaises(PermissionError):
                    validate_restart_authority(bad, authority_error=PermissionError)

        self.assertEqual(
            validate_restart_authority(
                UNAPPOINTED_RESTART_AUTHORITY,
                allow_unappointed_default=True,
            ),
            UNAPPOINTED_RESTART_AUTHORITY,
        )
        with self.assertRaises(ValueError):
            validate_restart_authority(
                "Unavailable: custom placeholder",
                allow_unappointed_default=True,
            )

    def test_self_designation_distinct_actor_and_privacy_non_echo(self) -> None:
        canary = "SYNTHETIC-CANARY-221-PRIVATE"
        actor = {
            "email": f"{canary.lower()}@example.test",
            "name": f"Inspector {canary}",
            "code": "QI-221",
            "oid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
        }
        snap = actor_snapshot(actor)
        self.assertEqual(snap["code"], "QI-221")

        for self_ref in (
            actor["email"],
            f"Approved by {actor['name']}",
            "Authorised by QI-221",
            actor["oid"],
        ):
            with self.assertRaises(PermissionError) as ctx:
                validate_restart_authority(self_ref, disallowed_actors=[actor])
            self.assertNotIn(canary, str(ctx.exception))
            self.assertNotIn(canary.lower(), str(ctx.exception))

        with self.assertRaises(ValueError) as bad_ctx:
            validate_restart_authority(f"TBD {canary}")
        self.assertNotIn(canary, str(bad_ctx.exception))

        # Non-short-circuiting check: first prior has distinct email, second collides on oid only.
        prior_email_only = {"email": "other@example.test"}
        prior_oid_match = {"email": "different@example.test", "oid": actor["oid"]}
        with self.assertRaises(PermissionError) as sep_ctx:
            ensure_distinct_restart_actor(
                actor,
                prior_email_only,
                prior_oid_match,
                prior_role_description="corrective proposer",
            )
        self.assertIn("corrective proposer", str(sep_ctx.exception))
        self.assertNotIn(canary, str(sep_ctx.exception))

        with self.assertRaises(PermissionError):
            reject_automatic_restart({"automatic": True})
        with self.assertRaises(PermissionError):
            reject_automatic_restart({"auto_restart": "1"})
        reject_automatic_restart({"automatic": False})

        # Entra pseudonymous principal + roster OID linking blocks cross-provider self-designation.
        entra_user = {
            "email": "e-0123456789ab@entra.invalid",
            "display_email": "entra-inspector@example.test",
            "code": "E-0123456789AB",
            "name": "E-0123456789AB",
            "oid": "11111111-2222-4333-8444-555555555555",
            "bound": {"email": "roster-inspector@example.test", "code": "QI-ROSTER"},
        }
        fake_store = type(
            "FakeStore",
            (),
            {
                "staff": {
                    "linked@example.test": {
                        "email": "linked@example.test",
                        "name": "Linked Roster Inspector",
                        "code": "QI-LINKED",
                        "oid": entra_user["oid"],
                    }
                }
            },
        )()
        resolved = actors_for_store(fake_store, entra_user)
        self.assertEqual(len(resolved), 2)
        for self_designation in (
            "entra-inspector@example.test",
            "roster-inspector@example.test",
            "linked@example.test",
            "Linked Roster Inspector",
            "QI-LINKED",
        ):
            with self.assertRaises(PermissionError):
                validate_restart_authority(self_designation, disallowed_actors=resolved)


class OperatorSuspensionDrillMixin:
    tmp: tempfile.TemporaryDirectory[str]
    store: Any
    service: Any

    def make_store(self, data: dict[str, Any], tmp_dir: str) -> Any:
        raise NotImplementedError

    def reopen_store(self) -> Any:
        raise NotImplementedError

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        seed: dict[str, Any] = copy.deepcopy(DATASET_MOD.DATA)
        seed["staff"] = copy.deepcopy(DRILL_STAFF)
        seed["cases"][0]["wave"] = "Wave 1"
        seed["cases"][0]["home"]["type"] = "Mid terrace"
        seed["cases"][0]["stage"] = "Final checks before ordering"
        seed["cases"][1]["wave"] = "Wave 2"
        seed["cases"][1]["home"]["type"] = "Semi-detached"
        self.store = self.make_store(seed, self.tmp.name)
        self.service = (
            ASSISTANTS_MOD.Assistants(self.store)
            if hasattr(self.store, "assistant_connection")
            else None
        )
        RELEASE_SUPPORT.install(self.store)

    def tearDown(self) -> None:
        if self.service is not None:
            self.service.stop()
        self.tmp.cleanup()

    def _open_governance_gates(self) -> None:
        s = self.store
        s.protocol_freeze(ACTORS["PM-1"], {**PROTOCOL, "synthetic": True})
        s.protocol_approve(
            ACTORS["PM-2"],
            {"dpia_ref": "DPIA-DRILL-221", "lawful_basis_ref": "LB-DRILL-221"},
        )
        s.benefits_record(
            ACTORS["PM-1"],
            {**BENEFITS, "mde_cycle_time_pct": 10, "mde_coordination_hours_pct": 10},
        )
        s.benefits_approve(ACTORS["PM-2"], {})

    def test_rule_024_rejects_invalid_authority_and_enforces_multi_actor_separation(self) -> None:
        test_self: Any = self
        self._open_governance_gates()
        s = self.store
        qi1 = ACTORS["QI-1"]
        pm1 = ACTORS["PM-1"]
        pm2 = ACTORS["PM-2"]
        pso1 = ACTORS["PSO-1"]

        for bad_auth in (
            "",
            "TBD",
            "TBD: awaiting OD-35",
            UNAPPOINTED_RESTART_AUTHORITY,
            "CM-0123456789abcdef",
            "automatic",
            "workflow",
            "self-approved",
        ):
            with test_self.subTest(breach_authority=bad_auth):
                with test_self.assertRaises(ValueError):
                    s.breach_record(qi1, {**BREACH_BODY, "restart_authority": bad_auth})

        for self_auth in (qi1["email"], qi1["name"], f"Delegated to {qi1['code']}"):
            with test_self.subTest(self_authority=self_auth):
                with test_self.assertRaises(PermissionError):
                    s.breach_record(qi1, {**BREACH_BODY, "restart_authority": self_auth})

        with test_self.assertRaises(ValueError):
            s.breach_record(qi1, {**BREACH_BODY, "evidence": "Cited from CM-0123456789abcdef"})

        breach = s.breach_record(qi1, BREACH_BODY)
        test_self.assertEqual(breach["restart_rule"], RULE_024)
        test_self.assertFalse(breach["automatic_restart"])
        rel = s.release_record(pm1, RELEASE_BODY)

        # Breach recorder cannot authorise restart.
        with test_self.assertRaises(PermissionError):
            s.breach_restart(
                qi1,
                {
                    "id": breach["id"],
                    "release_id": rel["id"],
                    "authority_ref": HUMAN_AUTHORITY,
                    "remediation_evidence": "SYN remediation pack",
                },
            )
        # Release recorder cannot authorise restart of the same breach either
        # (including across Entra OID identity).
        with test_self.assertRaises(PermissionError):
            s.breach_restart(
                pm1,
                {
                    "id": breach["id"],
                    "release_id": rel["id"],
                    "authority_ref": HUMAN_AUTHORITY,
                    "remediation_evidence": "SYN remediation pack",
                },
            )
        pm1_entra = {
            "email": "e-deadbeef0101@entra.invalid",
            "display_email": pm1["email"],
            "name": "Pseudonymous Entra Session",
            "role": pm1["role"],
            "code": "E-DEADBEEF0101",
            "oid": pm1["oid"],
        }
        with test_self.assertRaises(PermissionError):
            s.breach_restart(
                pm1_entra,
                {
                    "id": breach["id"],
                    "release_id": rel["id"],
                    "authority_ref": HUMAN_AUTHORITY,
                    "remediation_evidence": "SYN remediation pack",
                },
            )
        # Chat memory cannot be cited in remediation_evidence.
        with test_self.assertRaises(ValueError):
            s.breach_restart(
                pm2,
                {
                    "id": breach["id"],
                    "release_id": rel["id"],
                    "authority_ref": HUMAN_AUTHORITY,
                    "remediation_evidence": "Verified in chat-memory thread",
                },
            )

        # Continuity emergency containment succeeds when restart_authority is omitted,
        # redacts restart_authority from non-manager views, and blocks restart until a real
        # distinct human authority is recorded.
        unnamed_body = _incident(CAPABILITY)
        unnamed_body.pop("restart_authority")
        unnamed = s.suspend(qi1, unnamed_body)
        test_self.assertNotIn("restart_authority", unnamed)
        unnamed_mgr = next(
            row for row in s.continuity_view(pm1)["suspensions"] if row["id"] == unnamed["id"]
        )
        test_self.assertEqual(unnamed_mgr["restart_authority"], UNAPPOINTED_RESTART_AUTHORITY)
        test_self.assertEqual(unnamed_mgr["restart_rule"], RULE_024)
        test_self.assertFalse(unnamed_mgr["automatic_restart"])
        with test_self.assertRaises(PermissionError):
            s.restart_propose(
                pm1,
                {
                    "id": unnamed["id"],
                    "corrective_evidence": "SYN-FIX-1",
                    "test_id": "SYN-TEST-1",
                    "evidence_class": "constructed-fixture",
                    "result": "Pass",
                },
            )

        for bad_cont_auth in ("", "TBD", "automatic", "CM-0123456789abcdef"):
            with test_self.assertRaises(ValueError):
                s.suspend(qi1, _incident(SECOND_CAPABILITY, restart_authority=bad_cont_auth))
        with test_self.assertRaises(PermissionError):
            s.suspend(qi1, _incident(SECOND_CAPABILITY, restart_authority=qi1["email"]))
        with test_self.assertRaises(PermissionError):
            s.suspend(qi1, _incident(SECOND_CAPABILITY, automatic=True))

        named = s.suspend(qi1, _incident(SECOND_CAPABILITY))
        if not hasattr(s, "db"):
            with test_self.assertRaises(PermissionError):
                s.restart_propose(
                    pm1,
                    {
                        "id": named["id"],
                        "corrective_evidence": "SYN-FIX-2",
                        "test_id": "SYN-TEST-2",
                        "evidence_class": "constructed-fixture",
                        "result": "Pass",
                    },
                )
            return

        # Suspender cannot record corrective proposal.
        with test_self.assertRaises(PermissionError):
            s.restart_propose(
                qi1,
                {
                    "id": named["id"],
                    "corrective_evidence": "SYN-FIX-2",
                    "test_id": "SYN-TEST-2",
                    "evidence_class": "constructed-fixture",
                    "result": "Pass",
                },
            )
        proposed = s.restart_propose(
            pm1,
            {
                "id": named["id"],
                "corrective_evidence": "SYN-FIX-2",
                "test_id": "SYN-TEST-2",
                "evidence_class": "constructed-fixture",
                "result": "Pass",
            },
        )
        # Neither suspender nor proposer can record Keep suspended or Restart decisions.
        for actor in (qi1, pm1):
            for outcome in ("Keep suspended", "Restart"):
                same_pso = {**pso1, "email": actor["email"], "oid": actor["oid"]}
                s.staff[same_pso["email"]].update(
                    auth_provider="trusted-proxy", rule_roles=["ai_restart"]
                )
                with test_self.assertRaises(PermissionError):
                    s.restart_decide(
                        same_pso,
                        {
                            "id": proposed["id"],
                            "epoch": proposed["proposal"]["epoch"],
                            "proposal_digest": proposed["proposal"]["digest"],
                            "decision": outcome,
                            "authority_ref": HUMAN_AUTHORITY,
                        },
                        trusted_route=True,
                    )

        kept = s.restart_decide(
            pso1,
            {
                "id": proposed["id"],
                "epoch": proposed["proposal"]["epoch"],
                "proposal_digest": proposed["proposal"]["digest"],
                "decision": "Keep suspended",
                "authority_ref": HUMAN_AUTHORITY,
                "note": "Keep suspended pending second witness check",
            },
            trusted_route=True,
        )
        test_self.assertEqual(kept["status"], "Suspended")
        test_self.assertEqual(kept["decisions"][-1]["decision"], "Keep suspended")
        kept_mgr = next(
            row for row in s.continuity_view(pm1)["suspensions"] if row["id"] == kept["id"]
        )
        test_self.assertEqual(kept_mgr["decisions"][-1]["restart_rule"], RULE_024)
        test_self.assertFalse(kept_mgr["decisions"][-1]["automatic_restart"])

    def test_nfr_014_end_to_end_suspension_manual_fallback_hazard_and_restart_drill(self) -> None:
        test_self: Any = self
        self._open_governance_gates()
        s = self.store
        qi1 = ACTORS["QI-1"]
        pm1 = ACTORS["PM-1"]
        pm2 = ACTORS["PM-2"]
        bsl1 = ACTORS["BSL-1"]
        bsl2 = ACTORS["BSL-2"]
        rlo1 = ACTORS["RLO-1"]
        pso1 = ACTORS["PSO-1"]

        # Step 1-2: Trigger guardrail breach on Wave 1 AND operator AI suspension on CAPABILITY.
        breach = s.breach_record(qi1, BREACH_BODY)
        suspension = s.suspend(qi1, _incident(CAPABILITY))
        test_self.assertTrue(s.is_paused("archetype", "Mid terrace"))
        test_self.assertIsNotNone(s.continuity_block(CAPABILITY))

        # Step 3-4: Paused Mid terrace home blocks ordinary retrofit call logging, while
        # unaffected Semi-detached home continues via manual fallback during active AI suspension.
        with test_self.assertRaises(PermissionError):
            s.log_call(rlo1, "ZF-1", "Spoke", "Blocked on paused archetype")
        s.log_call(rlo1, "ZF-2", "Spoke", "SYN manual fallback contact on unaffected archetype")
        test_self.assertEqual(
            s.cases["ZF-2"]["contacts"][-1]["note"],
            "SYN manual fallback contact on unaffected archetype",
        )

        # Step 5: Statutory Awaab's Law emergency hazard workflow executes end-to-end on paused
        # home ZF-1 without delay or blockage from the guardrail breach or AI suspension.
        h_idx = s.raise_hazard(
            rlo1,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            note="SYN emergency damp report during suspension drill",
            metadata={
                "source": "SYN resident emergency telephone report",
                "aware_at": "2026-03-01T09:00:00+00:00",
            },
        )
        s.refer_hazard(
            rlo1,
            "ZF-1",
            h_idx,
            bsl1["email"],
            "SYN-HAZ-221",
            metadata={"evidence": "SYN emergency repairs desk referral"},
        )
        s.receive_hazard(bsl1, "ZF-1", h_idx, "SYN repairs desk receipt")
        s.accept_hazard(bsl1, "ZF-1", h_idx, "SYN emergency safety triage acceptance")
        s.observe_hazard_times(
            bsl1,
            "ZF-1",
            h_idx,
            {
                "evidence": "SYN emergency attendance timing log",
                "response_due_at": "2026-03-02T09:00:00+00:00",
                "responded_at": "2026-03-01T13:00:00+00:00",
                "resident_update_due_at": "2026-03-02T13:00:00+00:00",
                "resident_updated_at": "2026-03-01T15:00:00+00:00",
            },
        )
        s.record_repair(bsl1, "ZF-1", h_idx, evidence="SYN emergency make-safe certificate")
        s.release_hazard(
            bsl2,
            "ZF-1",
            h_idx,
            note="SYN independent Building Safety Liaison clearance",
            evidence="SYN post-make-safe inspection report",
        )
        test_self.assertTrue(s.cases["ZF-1"]["hazards"][h_idx]["released"])

        # Clearing the home safety hold does NOT lift the RULE-024 guardrail breach pause.
        with test_self.assertRaises(PermissionError):
            s.log_call(rlo1, "ZF-1", "Spoke", "Still paused until RULE-024 breach restart")

        # Raise a second hazard to prove the converse: RULE-024 breach_restart does NOT bypass an
        # active home safety hold on stage advancement.
        h2_idx = s.raise_hazard(
            rlo1,
            "ZF-1",
            "Electrical",
            "Significant",
            note="SYN secondary urgent safety hold",
            metadata={
                "source": "SYN electrician inspection note",
                "aware_at": "2026-03-01T16:00:00+00:00",
            },
        )

        # Step 6-7: Record post-breach Release (PM-1) and distinct-human breach_restart (PM-2),
        # plus corrective proposal (PM-1) and trusted distinct-human restart_decide (PSO-1).
        rel = s.release_record(pm1, RELEASE_BODY)
        restarted_breach = s.breach_restart(
            pm2,
            {
                "id": breach["id"],
                "release_id": rel["id"],
                "authority_ref": HUMAN_AUTHORITY,
                "remediation_evidence": "SYN-REM-221 verified corrective citation controls",
            },
        )
        test_self.assertEqual(restarted_breach["status"], "Restart authorised")
        test_self.assertEqual(restarted_breach["restart"]["restart_rule"], RULE_024)
        test_self.assertFalse(restarted_breach["restart"]["automatic_restart"])
        test_self.assertFalse(s.is_paused("archetype", "Mid terrace"))

        # Contact logging on ZF-1 is now unpaused, while stage advance remains blocked by h2_idx!
        s.log_call(rlo1, "ZF-1", "Spoke", "SYN post-restart liaison update")
        with test_self.assertRaises(GateError):
            s.advance(rlo1, "ZF-1")
        test_self.assertFalse(s.cases["ZF-1"]["hazards"][h2_idx]["released"])

        # AI capability remains suspended until SQL-backed distinct-human restart_decide completes.
        test_self.assertIsNotNone(s.continuity_block(CAPABILITY))
        if not hasattr(s, "db"):
            with test_self.assertRaises(PermissionError):
                s.restart_propose(
                    pm1,
                    {
                        "id": suspension["id"],
                        "corrective_evidence": "SYN-CORRECTIVE-221 regression suite passed",
                        "test_id": "SYN-DRILL-221-NFR-014",
                        "evidence_class": "constructed-fixture",
                        "result": "Pass",
                    },
                )
            test_self.assertTrue(s.verify_audit())
            reopened_json = self.reopen_store()
            test_self.assertFalse(reopened_json.is_paused("archetype", "Mid terrace"))
            gov_json = reopened_json.governance_view(pm1)["breaches"][0]
            test_self.assertEqual(gov_json["status"], "Restart authorised")
            test_self.assertEqual(gov_json["restart"]["authority_ref"], HUMAN_AUTHORITY)
            return

        proposed = s.restart_propose(
            pm1,
            {
                "id": suspension["id"],
                "corrective_evidence": "SYN-CORRECTIVE-221 regression suite passed",
                "test_id": "SYN-DRILL-221-NFR-014",
                "evidence_class": "constructed-fixture",
                "result": "Pass",
            },
        )
        decided = s.restart_decide(
            pso1,
            {
                "id": proposed["id"],
                "epoch": proposed["proposal"]["epoch"],
                "proposal_digest": proposed["proposal"]["digest"],
                "decision": "Restart",
                "authority_ref": HUMAN_AUTHORITY,
                "note": "SYN distinct human restart authorisation",
            },
            trusted_route=True,
        )
        test_self.assertTrue(decided["actual_hold"])
        test_self.assertIsNone(CONTINUITY_MOD.active(s._cont(), CAPABILITY, constructed=True))
        test_self.assertIsNotNone(s.continuity_block(CAPABILITY))
        closed = s.continuity_view(pm1)["suspensions"][0]
        test_self.assertEqual(closed["status"], "Restarted")
        test_self.assertEqual(closed["restart"]["restart_rule"], RULE_024)
        test_self.assertFalse(closed["restart"]["automatic_restart"])
        test_self.assertTrue(s.verify_audit())

        # Step 8: Durable reopen verification.
        reopened = self.reopen_store()
        test_self.assertFalse(reopened.is_paused("archetype", "Mid terrace"))
        test_self.assertIsNone(
            CONTINUITY_MOD.active(reopened._cont(), CAPABILITY, constructed=True)
        )
        gov_breach = reopened.governance_view(pm1)["breaches"][0]
        test_self.assertEqual(gov_breach["status"], "Restart authorised")
        test_self.assertEqual(gov_breach["restart"]["authority_ref"], HUMAN_AUTHORITY)
        cont_closed = reopened.continuity_view(pm1)["suspensions"][0]
        test_self.assertEqual(cont_closed["status"], "Restarted")
        test_self.assertEqual(cont_closed["restart"]["authority_ref"], HUMAN_AUTHORITY)


class JsonOperatorSuspensionDrillTest(OperatorSuspensionDrillMixin, unittest.TestCase):
    def make_store(self, data: dict[str, Any], tmp_dir: str) -> Any:
        path = Path(tmp_dir) / "zavaforward.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return STORE_CLS(str(path))

    def reopen_store(self) -> Any:
        path = Path(self.tmp.name) / "zavaforward.json"
        return STORE_CLS(str(path))


class SqlOperatorSuspensionDrillTest(OperatorSuspensionDrillMixin, unittest.TestCase):
    def make_store(self, data: dict[str, Any], tmp_dir: str) -> Any:
        path = Path(tmp_dir) / "zavaforward.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return SQL_STORE_CLS(str(path), os.path.join(tmp_dir, "drill.sqlite"))

    def reopen_store(self) -> Any:
        path = Path(self.tmp.name) / "zavaforward.json"
        return SQL_STORE_CLS(str(path), os.path.join(self.tmp.name, "drill.sqlite"))


if __name__ == "__main__":
    unittest.main()
