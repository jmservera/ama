"""Issue #217 proofs: Foundry minimisation, Entra 3-role SoD, Art 22A-22C guard, tokenomics."""

from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, cast

from regulatory_fixture import ENV, NOW, QUOTE, Fixture
from zava_forward.core import identity as _identity
from zava_forward.core import regulatory_chat as _regulatory_chat
from zava_forward.core import rule_engine as _rule_engine
from zava_forward.core.chat_isolation import ChatForbidden
from zava_forward.core.regulatory_privacy import (
    ACTION_CAPABILITIES,
    ART22_HUMAN_FLAG,
    COST_FIELDS,
    ENTRA_REGULATORY_ROLES,
    MANUAL_PATH,
    METERING_FIELDS,
    QUERY_FIELDS,
    SPECIAL_CATEGORY,
    SPECIAL_CATEGORY_FIELDS,
    ConsequentialDecisionGuard,
    build_foundry_query,
    check_special_category_purpose,
    cost_record,
    enforce_separation_of_duties,
    metering_record,
    minimise_query,
    readiness_report,
    record_human_decision,
    require_regulatory_role,
    resolve_entra_regulatory_roles,
)
from zava_forward.core.regulatory_usage import (
    chat_cost_record,
    check_cost_record,
    check_usage_metering,
    governed_metering_and_cost,
    offline_usage,
    summarize,
    summarize_checks,
)

_principal = cast(Callable[..., dict[str, Any]], _identity.principal)
_RegulatoryChat: Any = _regulatory_chat.RegulatoryChat
_RuleEngine: Any = _rule_engine.RuleEngine

TENANT = "11111111-2222-4333-8444-555555555555"
OID_AUTHOR = "aaaaaaaa-bbbb-4ccc-8ddd-111111111111"
OID_OWNER = "aaaaaaaa-bbbb-4ccc-8ddd-222222222222"
OID_CHAT = "aaaaaaaa-bbbb-4ccc-8ddd-333333333333"
OID_ADMIN = "aaaaaaaa-bbbb-4ccc-8ddd-444444444444"


def _entra_user(
    oid: str,
    role: str,
    app_roles: list[str],
    *,
    email: str | None = None,
    bound_code: str | None = None,
    view_only: bool = False,
) -> dict[str, Any]:
    base = _principal(
        TENANT,
        oid,
        role,
        email=email,
        roles=app_roles,
        view_only=view_only,
    )
    if bound_code is not None and email is not None:
        clean_email = email.strip().lower()
        base["code"] = bound_code
        base["email"] = clean_email
        base["bound"] = dict(code=bound_code, email=clean_email)
    caps = sorted(resolve_entra_regulatory_roles(base))
    base["rule_roles"] = caps
    base["entra_roles"] = list(app_roles)
    base["auth_mode"] = "trusted-proxy"
    return base


def _make_chat(fx: Fixture) -> Any:
    def render(evidence: dict[str, Any]) -> dict[str, Any]:
        return dict(
            kind="answer",
            as_of=evidence["as_of"],
            answer="Synthetic regulatory summary.",
            citations=[dict(id=s["id"]) for s in evidence.get("sources", [])],
        )

    def classify(text: str) -> str | None:
        low = text.lower()
        if "decision" in low or "automated" in low:
            return "automated-decision-safeguard"
        return "hazard-awareness-clock"

    def refuse(text: str) -> str | None:
        if "override" in text.lower():
            return "Cannot override a regulatory hold in chat."
        return None

    return _RegulatoryChat(fx.iso, fx.law, render, classify, refuse, env=ENV, clock=lambda: NOW)


class RegulatoryPrivacyAudit217Tests(unittest.TestCase):
    def test_foundry_query_excludes_unneeded_fields_per_question(self) -> None:
        candidate = dict(
            source_id="synthetic",
            provision_id="synthetic@v1#0001",
            card_id="synthetic-hazard",
            card_version="v1",
            version="v1",
            as_of="2026-10-16",
            case_id="ZF-001",
            check_kind="hazard-awareness-clock",
            hazard_count=1,
            active_hold_count=1,
            automated_decision_count=2,
            address="10 Canary Close",
            stage="Survey",
        )
        provision_q = build_foundry_query(
            "check_explain",
            candidate,
            question="Cite the statutory provision and version only.",
            question_topic="provision_lookup",
        )
        self.assertTrue(provision_q["permitted"])
        self.assertEqual(
            set(provision_q["fields"]),
            {"as_of", "card_id", "card_version", "provision_id", "source_id", "version"},
        )
        self.assertIn("case_id", provision_q["unneeded_for_question"])
        self.assertIn("automated_decision_count", provision_q["unneeded_for_question"])
        self.assertIn("address", provision_q["dropped"])

        hazard_q = build_foundry_query(
            "check_explain",
            candidate,
            question="Explain the hazard awareness clock and active hold on this home.",
        )
        self.assertTrue(hazard_q["permitted"])
        self.assertIn("hazard_count", hazard_q["fields"])
        self.assertIn("active_hold_count", hazard_q["fields"])
        self.assertNotIn("automated_decision_count", hazard_q["fields"])
        self.assertIn("automated_decision_count", hazard_q["unneeded_for_question"])

    def test_special_category_purpose_controls_block_external_and_unscoped_roles(self) -> None:
        qi_user = dict(role="Quality Inspector", email="qi@example.test")
        rlo_user = dict(role="Resident Liaison Officer", email="sam@example.test")
        denied_role = check_special_category_purpose(
            qi_user,
            "resident_support_reason",
            env=ENV,
            external_foundry=False,
        )
        self.assertFalse(denied_role["permitted"])
        self.assertIn("lacks recorded need", str(denied_role["reason"]))

        internal_ok = check_special_category_purpose(
            rlo_user,
            "resident_support_reason",
            env=ENV,
            external_foundry=False,
        )
        self.assertTrue(internal_ok["permitted"])
        self.assertFalse(internal_ok["dpo_reviewed"])

        external_blocked = check_special_category_purpose(
            rlo_user,
            "resident_support_reason",
            env=ENV,
            external_foundry=True,
        )
        self.assertFalse(external_blocked["permitted"])
        self.assertIn("exclude special-category data", str(external_blocked["reason"]))
        with self.assertRaises(PermissionError):
            build_foundry_query(
                "check_explain",
                dict(case_id="ZF-001", as_of="2026-10-16"),
                question="Explain check.",
                user=rlo_user,
                special_category_purpose="resident_support_reason",
                env=ENV,
            )

        actual_hold = check_special_category_purpose(
            rlo_user,
            "resident_support_reason",
            env=dict(ENV, ZF_DATA_PROCESSING="actual"),
            external_foundry=False,
        )
        self.assertFalse(actual_hold["permitted"])
        self.assertEqual(actual_hold["manual_path"], MANUAL_PATH)

        built = build_foundry_query(
            "check_explain",
            dict(
                case_id="ZF-001",
                card_id="synthetic-hazard",
                card_version="v1",
                check_kind="hazard-awareness-clock",
                as_of="2026-10-16",
                adjustment="PRIVATE-HEALTH-CANARY",
                notes="wheelchair ramp installed",
            ),
            question="Explain the hazard clock on this case.",
            user=rlo_user,
            env=ENV,
        )
        self.assertTrue(built["permitted"])
        self.assertEqual(built["special_category_dropped"], ["adjustment", "notes"])
        self.assertNotIn("PRIVATE-HEALTH-CANARY", json.dumps(built))
        self.assertNotIn("wheelchair", json.dumps(built))

    def test_regulatory_chat_foundry_query_excludes_canaries_and_enforces_admission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                chat = _make_chat(fx)
                case_id = str(next(iter(fx.store.cases)))
                chat_user = _entra_user(
                    OID_CHAT,
                    "Resident Liaison Officer",
                    ["ZavaForward.RegulatoryChat"],
                    email="sam@example.test",
                )
                author_only = _entra_user(
                    OID_AUTHOR,
                    "Resident Liaison Officer",
                    ["ZavaForward.RuleAuthor"],
                    email="sam@example.test",
                )
                with self.assertRaises(ChatForbidden):
                    chat.foundry_query(author_only, case_id, "Explain the hazard clock.")

                built = chat.foundry_query(
                    chat_user,
                    case_id,
                    "Explain the hazard awareness clock on this home.",
                )
                self.assertTrue(built["permitted"])
                serialised = json.dumps(built)
                self.assertNotIn("PRIVATE-HEALTH-CANARY", serialised)
                self.assertNotIn("PRIVATE-REPORT-CANARY", serialised)
                self.assertNotIn(QUOTE, serialised)
                self.assertIn("adjustment", built["special_category_dropped"])
                rows = fx.store.db.execute(
                    "SELECT detail FROM audit WHERE action='chat.regulatory.foundry_query'"
                ).fetchall()
                self.assertEqual(len(rows), 1)
                self.assertNotIn("PRIVATE-HEALTH-CANARY", rows[0][0])
                self.assertNotIn("Explain the hazard", rows[0][0])
            finally:
                fx.close()

    def test_entra_roles_are_distinct_and_mutually_non_implying(self) -> None:
        self.assertEqual(
            ENTRA_REGULATORY_ROLES,
            {
                "ZavaForward.RuleAuthor": "rule_author",
                "ZavaForward.RuleOwner": "rule_owner",
                "ZavaForward.RegulatoryChat": "regulatory_chat",
            },
        )
        self.assertEqual(len(set(ACTION_CAPABILITIES.values())), 3)
        author = _entra_user(OID_AUTHOR, "Building Safety Liaison", ["ZavaForward.RuleAuthor"])
        owner = _entra_user(OID_OWNER, "Building Safety Liaison", ["ZavaForward.RuleOwner"])
        chatter = _entra_user(OID_CHAT, "Resident Liaison Officer", ["ZavaForward.RegulatoryChat"])
        admin = _entra_user(
            OID_ADMIN,
            "Building Safety Liaison",
            ["ZavaForward.ApplicationAdmin"],
            view_only=True,
        )

        require_regulatory_role(author, "author")
        for forbidden_action in ("approve", "consequential_decision", "alert_disposition", "chat"):
            with self.assertRaises(PermissionError):
                require_regulatory_role(author, forbidden_action)

        require_regulatory_role(owner, "approve")
        require_regulatory_role(owner, "alert_disposition")
        for forbidden_action in ("author", "chat"):
            with self.assertRaises(PermissionError):
                require_regulatory_role(owner, forbidden_action)

        require_regulatory_role(chatter, "chat")
        for forbidden_action in (
            "author",
            "approve",
            "consequential_decision",
            "alert_disposition",
        ):
            with self.assertRaises(PermissionError):
                require_regulatory_role(chatter, forbidden_action)

        for any_action in ACTION_CAPABILITIES:
            with self.assertRaises(PermissionError):
                require_regulatory_role(admin, any_action)

    def test_forged_rule_roles_and_unverified_entra_claims_are_rejected(self) -> None:
        forged = _entra_user(OID_CHAT, "Building Safety Liaison", ["ZavaForward.RegulatoryChat"])
        forged["rule_roles"] = ["rule_owner", "rule_author", "regulatory_chat"]
        with self.assertRaises(PermissionError):
            require_regulatory_role(forged, "approve")

        bad_oid = dict(
            oid="not-a-uuid",
            tid=TENANT,
            identity_source="entra",
            auth_provider="trusted-proxy",
            role="Building Safety Liaison",
            app_roles=["ZavaForward.RuleOwner"],
        )
        with self.assertRaises(PermissionError):
            require_regulatory_role(bad_oid, "approve")

    def test_separation_of_duties_blocks_same_human_even_with_dual_roles(self) -> None:
        dual_author = _entra_user(
            OID_AUTHOR,
            "Building Safety Liaison",
            ["ZavaForward.RuleAuthor", "ZavaForward.RuleOwner"],
            email="dual@example.test",
        )
        dual_owner = _entra_user(
            OID_AUTHOR,
            "Building Safety Liaison",
            ["ZavaForward.RuleAuthor", "ZavaForward.RuleOwner"],
            email="alias@example.test",
        )
        with self.assertRaises(PermissionError):
            enforce_separation_of_duties(
                None, dual_owner, "dual@example.test", proposer_user=dual_author
            )

        distinct_owner = _entra_user(
            OID_OWNER,
            "Building Safety Liaison",
            ["ZavaForward.RuleOwner"],
            email="owner2@example.test",
        )
        verified_owner = enforce_separation_of_duties(
            None, distinct_owner, "dual@example.test", proposer_user=dual_author
        )
        self.assertEqual(verified_owner["oid"], OID_OWNER)

    def test_chat_admit_and_rule_engine_disposition_enforce_separate_entra_roles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                chat = _make_chat(fx)
                owner_entra = _entra_user(
                    OID_OWNER,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleOwner"],
                    email="exercise-owner@example.test",
                    bound_code="SYN-OWNER",
                )
                author_entra = _entra_user(
                    OID_AUTHOR,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleAuthor"],
                    email="exercise-owner@example.test",
                    bound_code="SYN-OWNER",
                )
                chat_entra = _entra_user(
                    OID_CHAT,
                    "Resident Liaison Officer",
                    ["ZavaForward.RegulatoryChat"],
                )
                admitted = chat.admit(chat_entra)
                self.assertEqual(admitted["oid"], OID_CHAT)
                self.assertEqual(admitted["rule_roles"], ["regulatory_chat"])
                with self.assertRaises(ChatForbidden):
                    chat.admit(owner_entra)
                with self.assertRaises(ChatForbidden):
                    chat.admit(dict(chat_entra, view_only=True))

                engine = _RuleEngine(fx.law)
                case_id = str(next(iter(fx.store.cases)))
                checkpoint = engine.run(fx.store, case_id, now=NOW)
                self.assertGreaterEqual(len(checkpoint["checks"]), 1)
                alerts = engine.alerts(owner_entra)["homes"][0]["alerts"]
                alert_id = str(alerts[0]["id"])

                with self.assertRaises(PermissionError):
                    engine.disposition(
                        author_entra, alert_id, "acknowledge", "Author cannot act.", now=NOW
                    )
                with self.assertRaises(PermissionError):
                    engine.disposition(
                        dict(owner_entra, view_only=True),
                        alert_id,
                        "acknowledge",
                        "View-only cannot act.",
                        now=NOW,
                    )
                engine.disposition(
                    owner_entra,
                    alert_id,
                    "acknowledge",
                    "Named RuleOwner reviewed hazard hold.",
                    now=NOW,
                )
            finally:
                fx.close()

    def test_art22_guard_proposes_and_flags_only_and_blocks_undecided_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                guard = ConsequentialDecisionGuard(fx.law, store=fx.store)
                with self.assertRaises(ValueError):
                    guard.propose(
                        proposal_id="prop-zf001-hold",
                        proposal_version="v1",
                        kind="check_outcome",
                        case_id="ZF-001",
                        summary="Attempted system-approved proposal.",
                        at=NOW.isoformat(),
                        status="accepted",
                    )
                proposal = guard.propose(
                    proposal_id="prop-zf001-hold",
                    proposal_version="v1",
                    kind="check_outcome",
                    case_id="ZF-001",
                    summary="Synthetic hazard clock breach risk requires human decision.",
                    flags=["breach_risk"],
                    proposed_by="synthetic-author@example.test",
                    at=NOW.isoformat(),
                )
                self.assertEqual(proposal["status"], "proposed")
                self.assertEqual(proposal["effect"], "non_binding_proposal")
                self.assertIn(ART22_HUMAN_FLAG, proposal["flags"])
                self.assertFalse(proposal["decided_by_system"])
                self.assertTrue(proposal["requires_named_human"])
                with self.assertRaises(PermissionError):
                    guard.authorize_consequential_action("prop-zf001-hold", "v1")
            finally:
                fx.close()

    def test_art22_guard_requires_named_human_sod_and_non_memory_reasons(self) -> None:
        prop_stub = dict(kind="check_outcome", id="prop-1", version="v1")
        for bad_decider in (
            "",
            "system",
            "agent",
            "copilot",
            "unassigned",
            "Named DPO (unassigned)",
        ):
            with self.assertRaises(ValueError):
                record_human_decision(
                    prop_stub,
                    bad_decider,
                    "rule_owner",
                    "accepted",
                    "Verified statutory inspection certificate on file.",
                    NOW.isoformat(),
                )
        with self.assertRaises(ValueError):
            record_human_decision(
                prop_stub,
                "Juan Manuel Servera",
                "rule_owner",
                "accepted",
                "Accepted based on chat-memory note CM-0123456789ab.",
                NOW.isoformat(),
            )

        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                guard = ConsequentialDecisionGuard(fx.law, store=fx.store)
                author = _entra_user(
                    OID_AUTHOR,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleAuthor"],
                    email="author@example.test",
                )
                author["name"] = "Alex Author"
                same_oid_owner = _entra_user(
                    OID_AUTHOR,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleOwner"],
                    email="author@example.test",
                )
                same_oid_owner["name"] = "Alex Author"
                distinct_owner = _entra_user(
                    OID_OWNER,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleOwner"],
                    email="exercise-owner@example.test",
                )
                distinct_owner["name"] = "Juan Manuel Servera"
                guard.propose(
                    proposal_id="prop-sod",
                    proposal_version="v1",
                    kind="alert_triage",
                    case_id="ZF-001",
                    summary="Escalate damp hazard hold for human owner review.",
                    flags=["attention"],
                    proposer_user=author,
                    at=NOW.isoformat(),
                )
                with self.assertRaises(PermissionError):
                    guard.decide(
                        proposal_id="prop-sod",
                        proposal_version="v1",
                        user=author,
                        outcome="accepted",
                        reasons="Author attempting self-approval.",
                        at=NOW.isoformat(),
                    )
                with self.assertRaises(PermissionError):
                    guard.decide(
                        proposal_id="prop-sod",
                        proposal_version="v1",
                        user=same_oid_owner,
                        outcome="accepted",
                        reasons="Same OID attempting self-approval.",
                        at=NOW.isoformat(),
                    )
                decision = guard.decide(
                    proposal_id="prop-sod",
                    proposal_version="v1",
                    user=distinct_owner,
                    outcome="accepted",
                    reasons="Reviewed inspection report SYN-JOB; resident contact arranged.",
                    at=NOW.isoformat(),
                )
                self.assertEqual(decision["decider_oid"], OID_OWNER)
                authorised = guard.authorize_consequential_action("prop-sod", "v1")
                self.assertEqual(authorised["outcome"], "accepted")
            finally:
                fx.close()

    def test_art22_decision_history_is_append_only_and_audit_is_metadata_only(self) -> None:
        secret_reason = "CANARY-REASON-INSPECTION-REF-9921"
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                guard = ConsequentialDecisionGuard(fx.law, store=fx.store)
                owner = _entra_user(
                    OID_OWNER,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleOwner"],
                    email="exercise-owner@example.test",
                )
                owner["name"] = "Juan Manuel Servera"
                guard.propose(
                    proposal_id="prop-append",
                    proposal_version="v1",
                    kind="check_outcome",
                    case_id="ZF-001",
                    summary="Hold release review proposal.",
                    flags=["attention"],
                    proposed_by="system",
                    at=NOW.isoformat(),
                )
                guard.decide(
                    proposal_id="prop-append",
                    proposal_version="v1",
                    user=owner,
                    outcome="rejected",
                    reasons=secret_reason,
                    at=NOW.isoformat(),
                )
                with self.assertRaises(PermissionError):
                    guard.authorize_consequential_action("prop-append", "v1")
                with self.assertRaises(ValueError):
                    guard.decide(
                        proposal_id="prop-append",
                        proposal_version="v1",
                        user=owner,
                        outcome="accepted",
                        reasons="Attempt to overwrite prior rejection.",
                        at=NOW.isoformat(),
                    )
                with self.assertRaises(sqlite3.IntegrityError):
                    fx.law.sql.run(
                        "UPDATE reg_consequential_decision SET outcome='accepted' "
                        "WHERE proposal_id='prop-append'"
                    )
                with self.assertRaises(sqlite3.IntegrityError):
                    fx.law.sql.run(
                        "DELETE FROM reg_consequential_decision WHERE proposal_id='prop-append'"
                    )
                with self.assertRaises(sqlite3.IntegrityError):
                    fx.law.sql.run(
                        "DELETE FROM reg_consequential_proposal WHERE proposal_id='prop-append'"
                    )
                trail = guard.history(owner, case_id="ZF-001")
                self.assertEqual(len(trail), 1)
                self.assertEqual(trail[0]["decision"]["reasons"], secret_reason)
                qi_viewer = dict(role="Quality Inspector", email="qi@example.test")
                masked_trail = guard.history(qi_viewer, case_id="ZF-001")
                self.assertNotIn(secret_reason, json.dumps(masked_trail))

                audit_rows = fx.store.db.execute(
                    "SELECT action, detail FROM audit WHERE action LIKE 'regulatory.art22.%'"
                ).fetchall()
                self.assertEqual(len(audit_rows), 2)
                self.assertNotIn(secret_reason, json.dumps(audit_rows))
            finally:
                fx.close()

    def test_metering_and_cost_records_enforce_closed_content_free_schemas(self) -> None:
        chat_usage = offline_usage(
            "regulatory-home-chat", "regulatory-chat-v1", "answer", NOW.isoformat()
        )
        unpriced = chat_cost_record(chat_usage, "turn-001")
        self.assertTrue(set(unpriced).issubset(set(COST_FIELDS) | {"retention_class"}))
        self.assertEqual(unpriced["cost"], "Unknown")
        self.assertIsNone(unpriced["cost_minor_units"])
        self.assertEqual(unpriced["price_version"], "unpriced")

        priced = cost_record(
            dict(
                surface="chat",
                record_id="turn-002",
                model_id="foundry-gpt-synth",
                prompt_version="regulatory-chat-v1",
                input_tokens=1000,
                output_tokens=500,
                cached_tokens=0,
                retry_count=0,
                occurred_at=NOW.isoformat(),
                price_version="synth-price-2026-11",
                currency="GBP",
                cost_minor_units=15,
                cost="calculated",
            )
        )
        self.assertEqual(priced["cost_minor_units"], 15)
        self.assertEqual(priced["currency"], "GBP")

        raw_unpriced = {k: v for k, v in unpriced.items() if k != "retention_class"}
        raw_priced = {k: v for k, v in priced.items() if k != "retention_class"}
        for forbidden_key in ("question", "answer", "excerpt", "case_id", "resident", "prompt"):
            with self.assertRaises(ValueError):
                cost_record(dict(raw_unpriced, **{forbidden_key: "CANARY"}))
        with self.assertRaises(ValueError):
            cost_record(
                dict(
                    raw_unpriced,
                    cost="calculated",
                    cost_minor_units=0,
                    currency="GBP",
                )
            )
        with self.assertRaises(ValueError):
            cost_record(
                dict(
                    raw_priced,
                    input_tokens=True,
                )
            )

    def test_check_metering_and_cost_project_reg_check_without_case_or_source_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                engine = _RuleEngine(fx.law)
                case_id = str(next(iter(fx.store.cases)))
                checkpoint = engine.run(fx.store, case_id, now=NOW)
                check_row = next(
                    c for c in checkpoint["checks"] if c["card_id"] == "synthetic-hazard"
                )
                metered = check_usage_metering(check_row)
                costed = check_cost_record(check_row)
                self.assertTrue(set(metered).issubset(set(METERING_FIELDS) | {"retention_class"}))
                self.assertEqual(metered["surface"], "check")
                self.assertEqual(metered["rule_card_version"], "synthetic-hazard:v1")
                self.assertEqual(costed["cost"], "Unknown")
                combined = json.dumps([metered, costed])
                self.assertNotIn("PRIVATE-HEALTH-CANARY", combined)
                self.assertNotIn("PRIVATE-REPORT-CANARY", combined)
                self.assertNotIn(QUOTE, combined)
                self.assertNotIn(case_id, combined)

                owner_summary = summarize_checks(
                    checkpoint["checks"], fx.owner, NOW.date().isoformat()
                )
                self.assertGreaterEqual(owner_summary["recorded_checks"], 1)
                qi_user = dict(role="Quality Inspector", email="qi@example.test")
                qi_summary = summarize_checks(checkpoint["checks"], qi_user, NOW.date().isoformat())
                self.assertEqual(qi_summary["recorded_checks"], 0)
            finally:
                fx.close()

    def test_governed_metering_and_cost_enforces_role_scope_retention_and_audit(self) -> None:
        env_ret = dict(
            ENV,
            CHAT_RETENTION_REF="SYNTH-RET-30D",
            CHAT_RETENTION_DAYS="30",
        )
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp, sql=True)
            try:
                chat = _make_chat(fx)
                engine = _RuleEngine(fx.law)
                case_id = str(next(iter(fx.store.cases)))
                engine.run(fx.store, case_id, now=NOW)

                rlo = _entra_user(
                    OID_CHAT,
                    "Resident Liaison Officer",
                    ["ZavaForward.RegulatoryChat"],
                    email="sam@example.test",
                )
                tid = str(chat.start(rlo, case_id))
                chat.ask(
                    rlo,
                    tid,
                    "What is the hazard clock on this synthetic home? CANARY-QUESTION-77",
                )

                in_window = governed_metering_and_cost(
                    fx.store,
                    rlo,
                    law=fx.law,
                    surface="all",
                    env=env_ret,
                    as_of=datetime(2026, 10, 20, 12, tzinfo=UTC),
                )
                self.assertFalse(in_window["dpo_reviewed"])
                self.assertEqual(in_window["retention"]["status"], "simulated")
                surfaces = {row["surface"] for row in in_window["metering"]}
                self.assertEqual(surfaces, {"chat", "check"})
                expected_total = len(in_window["metering"])
                self.assertEqual(len(in_window["cost"]), expected_total)
                dumped = json.dumps(in_window)
                self.assertNotIn("CANARY-QUESTION-77", dumped)
                self.assertNotIn("PRIVATE-HEALTH-CANARY", dumped)
                self.assertNotIn(QUOTE, dumped)

                expired = governed_metering_and_cost(
                    fx.store,
                    rlo,
                    law=fx.law,
                    surface="all",
                    env=env_ret,
                    as_of=datetime(2026, 12, 5, 12, tzinfo=UTC),
                )
                self.assertEqual(expired["metering"], [])
                self.assertEqual(expired["cost"], [])
                self.assertEqual(expired["retention_filtered_count"], expected_total)

                qi_chat = _entra_user(
                    "aaaaaaaa-bbbb-4ccc-8ddd-555555555555",
                    "Quality Inspector",
                    ["ZavaForward.RegulatoryChat"],
                    email="qi@example.test",
                )
                qi_scoped = governed_metering_and_cost(
                    fx.store,
                    qi_chat,
                    law=fx.law,
                    surface="all",
                    env=env_ret,
                    as_of=datetime(2026, 10, 20, 12, tzinfo=UTC),
                )
                self.assertEqual(qi_scoped["metering"], [])

                author_only = _entra_user(
                    OID_AUTHOR,
                    "Building Safety Liaison",
                    ["ZavaForward.RuleAuthor"],
                    email="author@example.test",
                )
                with self.assertRaises(PermissionError):
                    governed_metering_and_cost(
                        fx.store,
                        author_only,
                        law=fx.law,
                        surface="all",
                        env=env_ret,
                        as_of=datetime(2026, 10, 20, 12, tzinfo=UTC),
                    )
                denied_rows = fx.store.db.execute(
                    "SELECT detail FROM audit WHERE action='regulatory.metering.denied'"
                ).fetchall()
                read_rows = fx.store.db.execute(
                    "SELECT detail FROM audit WHERE action='regulatory.metering.read'"
                ).fetchall()
                self.assertEqual(len(denied_rows), 1)
                self.assertGreaterEqual(len(read_rows), 3)
            finally:
                fx.close()

    def test_backward_compatible_regulatory_privacy_and_usage_contracts_hold(self) -> None:
        self.assertEqual(set(QUERY_FIELDS), {"rule_lookup", "check_explain", "alert_triage"})
        self.assertIn("health", SPECIAL_CATEGORY)
        self.assertIn("adjustment", SPECIAL_CATEGORY_FIELDS)
        legacy = minimise_query(
            "rule_lookup",
            dict(
                source_id="synthetic",
                provision_id="synthetic@v1#0001",
                adjustment="PRIVATE-HEALTH-CANARY",
                extra="dropped",
            ),
        )
        self.assertTrue(legacy["permitted"])
        self.assertEqual(
            legacy["fields"],
            dict(source_id="synthetic", provision_id="synthetic@v1#0001"),
        )
        self.assertEqual(legacy["dropped"], ["adjustment", "extra"])

        metered = metering_record(
            dict(
                surface="chat",
                record_id="rec-1",
                model_id="offline-deterministic",
                prompt_version="regulatory-chat-v1",
                input_tokens=0,
                output_tokens=0,
                cached_tokens=0,
                retry_count=0,
                occurred_at=NOW.isoformat(),
            )
        )
        self.assertEqual(metered["retention_class"], "usage")

        report = readiness_report(ENV)
        self.assertFalse(report["dpo_reviewed"])
        self.assertFalse(report["live_data_permitted"])

        summary = summarize(
            [],
            "Resident Liaison Officer",
            "2026-10-16",
            truncated=False,
        )
        self.assertEqual(summary["recorded_turns"], 0)
        self.assertEqual(summary["economics"]["ai_cost_per_accepted_check"], "Unknown")


if __name__ == "__main__":
    unittest.main()
