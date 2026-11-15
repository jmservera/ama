"""Read-only retention review, aligned with chat settings; never a DPO approval or purge."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from zava_forward.core import chat_privacy as _chat_privacy
from zava_forward.core import controls as _controls
from zava_forward.core import data_protection, identity
from zava_forward.core import projection as _projection

_can_see_reason = cast(Callable[[dict[str, Any]], bool], _projection.can_see_reason)
_redact = cast(Callable[[str], tuple[str, list[str]]], _chat_privacy.redact)
_is_memory_reference = cast(Callable[[object], bool], _controls.is_memory_reference)
_STAFF_ROLES: tuple[str, ...] = tuple(_projection.STAFF_ROLES)
_NOTE_HELD: str = str(_projection.NOTE_HELD)
_HAZARD_FACT_ROLES = frozenset(
    (
        "Building Safety Liaison",
        "Resident Liaison Officer",
        "Retrofit Programme Manager",
    )
)

OWNER = "Juan Manuel Servera"
CLASSES = (
    ("law_source", "reg_source, reg_version, reg_provision, source candidates and snapshots"),
    ("rule_card", "rule_card_version, rule_card_event and source-review records"),
    ("check", "reg_check and reg_checkpoint; case linkage and input hashes"),
    ("alert", "reg_alert and reg_alert_event; named owner dispositions"),
    ("audit", "Append-only rule/check/alert records and chat metadata ledger"),
    (
        "usage",
        "Content-free regulatory turn audit metadata and reg_check/reg_alert usage; "
        "inherits parent record access, retention and audit review",
    ),
)


def _parse_retention_days(
    env: Any,
    *,
    retention_days: int | None = None,
) -> tuple[str, int | None]:
    ref = str(env.get("CHAT_RETENTION_REF") or "").strip() if env is not None else ""
    raw = str(env.get("CHAT_RETENTION_DAYS") or "").strip() if env is not None else ""
    if retention_days is not None:
        if type(retention_days) is not int or not 1 <= retention_days <= 36500:
            raise ValueError("Synthetic retention days must be between 1 and 36500.")
        if ref and not ref.startswith("SYNTH-"):
            raise ValueError("Synthetic retention needs a SYNTH- reference and positive days.")
        return ref, retention_days
    if ref or raw:
        if not ref.startswith("SYNTH-") or not raw.isascii() or not raw.isdigit():
            raise ValueError("Synthetic retention needs a SYNTH- reference and positive days.")
        days = int(raw)
        if not 1 <= days <= 36500:
            raise ValueError("Synthetic retention days must be between 1 and 36500.")
        return ref, days
    return ref, None


def retention_alignment(
    env: Any,
    now: datetime,
    *,
    retention_days: int | None = None,
) -> dict[str, Any]:
    """Return shared retention-window metadata; never claims DPO approval or auto-deletion."""
    if now.tzinfo is None:
        raise ValueError("Retention review needs a timezone-aware clock.")
    ref, days = _parse_retention_days(env, retention_days=retention_days)
    cutoff = now.astimezone(UTC) - timedelta(days=days) if days is not None else None
    return dict(
        status="simulated" if days is not None else "unknown",
        days=days,
        reference=ref or None,
        cutoff=cutoff.isoformat() if cutoff is not None else None,
        dpo_reviewed=False,
        deletion_enabled=False,
    )


def retention_report(threads: list[dict[str, Any]], env: Any, now: datetime) -> dict[str, Any]:
    """List review-due own threads, never infer a deletion entitlement from age."""
    if now.tzinfo is None:
        raise ValueError("Retention review needs a timezone-aware clock.")
    ref, days = _parse_retention_days(env)
    rows = []
    for thread in threads:
        due = None
        if days is not None:
            created = datetime.fromisoformat(thread["created_at"])
            if created.tzinfo is None:
                raise ValueError("Thread creation time lacks a timezone; DPO review required.")
            due = created.astimezone(UTC) + timedelta(days=days)
        rows.append(
            dict(
                thread_id=thread["id"],
                messages=thread["message_count"],
                review_due=due.isoformat() if due else None,
                due_for_review=due <= now if due else None,
            )
        )
    return dict(
        label="synthetic-demo",
        owner=OWNER,
        dpia_status="Draft for DPO review; not completed",
        dpo_reviewed=False,
        deletion_enabled=False,
        chat=dict(
            storage="chat_thread and chat_message (reg_chat_turn equivalent)",
            trigger="Thread creation, including archived threads; simulated review only",
            status="simulated" if days else "unknown",
            days=days,
            reference=ref or None,
            records=rows,
        ),
        other_classes=[
            dict(
                record_class=name,
                storage=storage,
                status="unknown",
                days=None,
                reference=None,
            )
            for name, storage in CLASSES
        ],
        action="DPO must set periods, triggers, holds, rights and disposal approval. "
        "No records are deleted or marked lawfully retained by this report.",
    )


GATE_REFS = (
    ("REG_DPIA_REF", "DPIA completed with the DPO"),
    ("REG_RETENTION_REF", "DPO-set retention periods for chat, check, alert and usage records"),
    ("REG_ENTRA_ROLES_REF", "Tenant evidence for separate author, approver and chat-user roles"),
    ("REG_ART22_REF", "Art 22A to 22C human authority and recorded reasons"),
)

CRITERIA = (
    ("dpia", "DPIA with the DPO before live data", "human-gate-unmet", "REG_DPIA_REF"),
    (
        "retention",
        "Chat and check retention periods set by DPO review",
        "human-gate-unmet",
        "REG_RETENTION_REF",
    ),
    ("foundry_minimisation", "Foundry queries exclude unneeded fields", "partial", None),
    (
        "entra_roles",
        "Authors, approvers and chat users are separate Entra roles",
        "human-gate-unmet",
        "REG_ENTRA_ROLES_REF",
    ),
    ("audit", "Rule, approval, check, alert and chat events audit-logged", "automated-pass", None),
    (
        "injection_cross_role",
        "Prompt-injection and cross-role disclosure tests",
        "automated-pass",
        None,
    ),
    (
        "art22",
        "Art 22A to 22C named human with recorded reasons",
        "human-gate-unmet",
        "REG_ART22_REF",
    ),
    (
        "metering",
        "Metering holds identifiers, counts and versions only",
        "partial",
        "REG_RETENTION_REF",
    ),
)


def readiness_report(env: Any) -> dict[str, Any]:
    """Reference-only live-data gate; recorded references are not verified DPO or Legal approval."""
    refs = {name: str(env.get(name) or "").strip() for name, _ in GATE_REFS}
    missing = [name for name, ref in refs.items() if not ref]
    synthetic = [name for name, ref in refs.items() if ref.startswith("SYNTH-")]
    permitted = not missing and not synthetic
    return dict(
        label="synthetic-demo",
        owner=OWNER,
        live_data_permitted=permitted,
        dpo_reviewed=False,
        missing_refs=missing,
        synthetic_refs=synthetic,
        statement="References recorded, human approval not verified by this report."
        if permitted
        else "Live data refused until every reference is recorded and none is synthetic.",
        criteria=[
            dict(
                id=cid,
                criterion=text,
                status=status,
                ref_recorded=bool(ref and refs.get(ref)) if ref else None,
            )
            for cid, text, status, ref in CRITERIA
        ],
    )


QUERY_FIELDS = {
    "rule_lookup": ("card_id", "card_version", "provision_id", "source_id", "version", "as_of"),
    "check_explain": ("card_id", "card_version", "check_kind", "outcome", "as_of", "case_id"),
    "alert_triage": ("alert_id", "source_id", "version", "status", "as_of"),
}
SPECIAL_CATEGORY = frozenset(
    ("health", "disability", "ethnicity", "religion", "safeguarding", "vulnerability", "notes")
)
SPECIAL_CATEGORY_FIELDS = SPECIAL_CATEGORY | frozenset(
    (
        "adjustment",
        "medical",
        "biometric",
        "genetic",
        "sexual_orientation",
        "trade_union",
        "criminal",
        "hardship",
    )
)
QUESTION_QUERY_FIELDS: dict[str, tuple[str, ...]] = {
    "provision_lookup": (
        "card_id",
        "card_version",
        "provision_id",
        "source_id",
        "version",
        "as_of",
    ),
    "hazard-awareness-clock": (
        "card_id",
        "card_version",
        "check_kind",
        "outcome",
        "as_of",
        "case_id",
        "hazard_count",
        "active_hold_count",
    ),
    "automated-decision-safeguard": (
        "card_id",
        "card_version",
        "check_kind",
        "outcome",
        "as_of",
        "case_id",
        "automated_decision_count",
    ),
    "alert_triage": ("alert_id", "source_id", "version", "status", "as_of"),
}
SPECIAL_CATEGORY_PURPOSES = frozenset(("resident_support_reason", "safeguarding_referral"))
MANUAL_PATH = "Use the rule card and source links directly; a named human decides."
_MAX_SCALAR_STR = 120


def _scalar_value_clean(value: Any) -> tuple[bool, bool]:
    """Return (is_safe_scalar, contains_special_category_cue)."""
    if type(value) is int:
        return 0 <= value <= 10**9, False
    if type(value) is str:
        if not value or len(value) > _MAX_SCALAR_STR or "\n" in value or "\r" in value:
            _, cues = _redact(value[:1000])
            return False, "special_category" in cues
        _, cues = _redact(value)
        if cues:
            return False, "special_category" in cues
        return True, False
    return False, False


def minimise_query(purpose: str, fields: dict[str, Any]) -> dict[str, Any]:
    """Keep only fields the purpose needs; report dropped names, never values."""
    allowed = QUERY_FIELDS.get(purpose)
    if allowed is None:
        return dict(permitted=False, fields={}, dropped=[], manual_path=MANUAL_PATH)
    kept: dict[str, Any] = {}
    sc_dropped: set[str] = set()
    for key, value in fields.items():
        if key in SPECIAL_CATEGORY_FIELDS:
            sc_dropped.add(key)
            continue
        clean, has_sc_cue = _scalar_value_clean(value)
        if has_sc_cue:
            sc_dropped.add(key)
            continue
        if key in allowed and clean:
            kept[key] = value
    return dict(
        permitted=True,
        fields=kept,
        dropped=sorted(k for k in fields if k not in kept),
        special_category_dropped=sorted(sc_dropped),
        manual_path=MANUAL_PATH,
    )


def check_special_category_purpose(
    user: dict[str, Any] | None,
    purpose: str,
    *,
    env: Any = None,
    external_foundry: bool = True,
) -> dict[str, Any]:
    """Enforce existing projection and data-protection purpose gates on special-category data."""
    if external_foundry:
        return dict(
            permitted=False,
            purpose=purpose,
            dpo_reviewed=False,
            reason=(
                "External Foundry queries exclude special-category data while DPO review is open."
            ),
            manual_path=MANUAL_PATH,
        )
    if purpose not in SPECIAL_CATEGORY_PURPOSES:
        return dict(
            permitted=False,
            purpose=purpose,
            dpo_reviewed=False,
            reason="Unrecognised special-category purpose.",
            manual_path=MANUAL_PATH,
        )
    if (
        user is None
        or bool(user.get("view_only"))
        or user.get("role") not in _STAFF_ROLES
        or not _can_see_reason(user)
    ):
        return dict(
            permitted=False,
            purpose=purpose,
            dpo_reviewed=False,
            reason="Role lacks recorded need to access special-category support reasons.",
            manual_path=MANUAL_PATH,
        )
    if (
        identity.is_entra(user)
        or "oid" in user
        or "tid" in user
        or user.get("auth_mode") == "trusted-proxy"
    ) and identity.verified(user) is None:
        return dict(
            permitted=False,
            purpose=purpose,
            dpo_reviewed=False,
            reason="Unverified Entra principal cannot access special-category data.",
            manual_path=MANUAL_PATH,
        )
    hold = data_protection.dispatch_hold("tenant_identity", env if env is not None else {})
    if hold is not None:
        return dict(
            permitted=False,
            purpose=purpose,
            dpo_reviewed=False,
            reason=hold,
            manual_path=MANUAL_PATH,
        )
    return dict(
        permitted=True,
        purpose=purpose,
        dpo_reviewed=False,
        reason="Internal role-scoped purpose check passed; DPO review remains open.",
        manual_path=MANUAL_PATH,
    )


def _infer_question_topic(purpose: str, masked_question: str | None) -> str:
    if purpose == "rule_lookup":
        return "provision_lookup"
    if purpose == "alert_triage":
        return "alert_triage"
    if masked_question is None:
        return "check_explain"
    low = masked_question.lower()
    has_home_scope = any(
        term in low
        for term in (
            "home",
            "case",
            "property",
            "clock",
            "hold",
            "overdue",
            "check",
            "status",
            "this ",
        )
    )
    has_provision_only = any(
        term in low for term in ("provision", "source", "section", "legislation", "statute", "cite")
    )
    if has_provision_only and not has_home_scope:
        return "provision_lookup"
    if any(
        term in low
        for term in (
            "automated",
            "22a",
            "22b",
            "22c",
            "art 22",
            "article 22",
            "consequential",
            "propose",
            "human review",
        )
    ):
        return "automated-decision-safeguard"
    if any(
        term in low for term in ("hazard", "damp", "mould", "awaab", "hold", "emergency", "repair")
    ):
        return "hazard-awareness-clock"
    return "check_explain"


def build_foundry_query(
    purpose: str,
    fields: dict[str, Any],
    *,
    question: str | None = None,
    question_topic: str | None = None,
    user: dict[str, Any] | None = None,
    special_category_purpose: str | None = None,
    env: Any = None,
) -> dict[str, Any]:
    """Build a question-scoped Foundry query payload excluding unneeded and special data."""
    if special_category_purpose is not None:
        gate = check_special_category_purpose(
            user, special_category_purpose, env=env, external_foundry=True
        )
        if not gate["permitted"]:
            raise PermissionError(str(gate["reason"]))
    if purpose not in QUERY_FIELDS:
        return dict(
            permitted=False,
            purpose=purpose,
            question_topic=None,
            fields={},
            dropped=[],
            unneeded_for_question=[],
            special_category_dropped=[],
            dpo_reviewed=False,
            manual_path=MANUAL_PATH,
        )
    masked_q: str | None = None
    redactions: list[str] = []
    if question is not None:
        if not isinstance(question, str) or not 1 <= len(question.strip()) <= 1000:
            raise ValueError("Question must contain 1 to 1000 characters.")
        masked_q, redactions = _redact(question.strip())
    topic = (
        question_topic if question_topic is not None else _infer_question_topic(purpose, masked_q)
    )
    if topic == "check_explain":
        allowed_tuple: tuple[str, ...] = QUERY_FIELDS["check_explain"]
    elif topic in QUESTION_QUERY_FIELDS:
        allowed_tuple = QUESTION_QUERY_FIELDS[topic]
    else:
        return dict(
            permitted=False,
            purpose=purpose,
            question_topic=topic,
            fields={},
            dropped=[],
            unneeded_for_question=[],
            special_category_dropped=[],
            dpo_reviewed=False,
            manual_path=MANUAL_PATH,
        )
    allowed = set(allowed_tuple)
    if (
        user is not None
        and topic == "hazard-awareness-clock"
        and user.get("role") not in _HAZARD_FACT_ROLES
    ):
        allowed -= {"hazard_count", "active_hold_count"}
    all_known_query_keys = {
        key for group in (*QUERY_FIELDS.values(), *QUESTION_QUERY_FIELDS.values()) for key in group
    }
    kept: dict[str, Any] = {}
    sc_dropped: set[str] = set()
    unneeded: set[str] = set()
    for key, value in fields.items():
        if key in SPECIAL_CATEGORY_FIELDS:
            sc_dropped.add(key)
            continue
        clean, has_sc_cue = _scalar_value_clean(value)
        if has_sc_cue:
            sc_dropped.add(key)
            continue
        if key not in allowed:
            if key in all_known_query_keys:
                unneeded.add(key)
            continue
        if clean:
            kept[key] = value
    purpose_control = (
        "denied_by_role_projection"
        if sc_dropped and user is not None and not _can_see_reason(user)
        else ("stripped_external_foundry" if sc_dropped else "not_triggered")
    )
    return dict(
        permitted=True,
        purpose=purpose,
        question_topic=topic,
        question_redacted=masked_q,
        question_redactions=redactions,
        fields=kept,
        dropped=sorted(k for k in fields if k not in kept),
        unneeded_for_question=sorted(unneeded),
        special_category_dropped=sorted(sc_dropped),
        special_category_purpose_control=purpose_control,
        dpo_reviewed=False,
        manual_path=MANUAL_PATH,
    )


ENTRA_REGULATORY_ROLES: dict[str, str] = {
    "ZavaForward.RuleAuthor": "rule_author",
    "ZavaForward.RuleOwner": "rule_owner",
    "ZavaForward.RegulatoryChat": "regulatory_chat",
}
ACTION_CAPABILITIES: dict[str, str] = {
    "author": "rule_author",
    "propose_rule": "rule_author",
    "rule_author": "rule_author",
    "approve": "rule_owner",
    "approve_rule": "rule_owner",
    "consequential_decision": "rule_owner",
    "alert_disposition": "rule_owner",
    "rule_owner": "rule_owner",
    "chat": "regulatory_chat",
    "regulatory_chat": "regulatory_chat",
}


def is_trusted_proxy_user(user: Mapping[str, Any]) -> bool:
    """True when the principal represents a trusted-proxy or Entra-authenticated caller."""
    return bool(
        user.get("auth_provider") == "trusted-proxy"
        or user.get("auth_mode") == "trusted-proxy"
        or identity.is_entra(dict(user))
    )


def resolve_entra_regulatory_roles(user: Mapping[str, Any]) -> frozenset[str]:
    """Map Entra capability roles without cross-role inheritance or admin escalation."""
    claims: set[str] = set()
    for field in ("app_roles", "entra_roles"):
        raw = user.get(field)
        if isinstance(raw, (list, tuple, set, frozenset)):
            for item in raw:
                if isinstance(item, str):
                    claims.add(item.strip())
    return frozenset(
        ENTRA_REGULATORY_ROLES[claim] for claim in claims if claim in ENTRA_REGULATORY_ROLES
    )


def require_regulatory_role(
    user: dict[str, Any],
    action_or_capability: str,
    *,
    require_entra: bool = True,
) -> dict[str, Any]:
    """Verify staff role, non-view-only state, and separate Entra capability assignment."""
    required = ACTION_CAPABILITIES.get(action_or_capability)
    if required is None:
        raise ValueError(f"Unsupported regulatory capability check: {action_or_capability}")
    if bool(user.get("view_only")):
        raise PermissionError("View-only administrators cannot perform regulatory actions.")
    if user.get("role") not in _STAFF_ROLES:
        raise PermissionError("Only scoped staff roles can perform regulatory actions.")
    has_entra_markers = (
        identity.is_entra(user)
        or "oid" in user
        or "tid" in user
        or user.get("auth_mode") == "trusted-proxy"
    )
    if require_entra or has_entra_markers:
        verified = identity.verified(user)
        if verified is None:
            raise PermissionError(
                "A verified Entra principal is required for regulatory role checks."
            )
        if "app_roles" in user or "entra_roles" in user or "app_roles" in verified:
            merged = dict(verified)
            if "entra_roles" in user:
                merged["entra_roles"] = list(user["entra_roles"])
            caps = resolve_entra_regulatory_roles(merged)
        else:
            caps = frozenset(
                r
                for r in (verified.get("rule_roles") or ())
                if r in ENTRA_REGULATORY_ROLES.values()
            )
        if required not in caps:
            entra_name = next(k for k, v in ENTRA_REGULATORY_ROLES.items() if v == required)
            raise PermissionError(f"Separate Entra role {entra_name} ({required}) is required.")
        out = dict(verified, rule_roles=sorted(caps))
        for extra in ("auth_mode", "entra_roles"):
            if extra in user:
                out[extra] = user[extra]
        return out
    raw_roles = user.get("rule_roles") or ()
    local_caps = frozenset(
        r for r in raw_roles if isinstance(r, str) and r in ENTRA_REGULATORY_ROLES.values()
    )
    if required not in local_caps:
        raise PermissionError(f"Separate capability {required} is required.")
    return dict(user, rule_roles=sorted(local_caps))


def _principal_tokens(user: Mapping[str, Any]) -> set[str]:
    tokens: set[str] = set()
    tid = identity.canonical_guid(user.get("tid"))
    oid = identity.canonical_guid(user.get("oid"))
    if tid and oid:
        tokens.add(f"entra:{tid}:{oid}")
    if oid:
        tokens.add(f"oid:{oid}")
    for key in ("email", "code", "derived_email", "derived_code"):
        val = user.get(key)
        if isinstance(val, str) and val.strip():
            tokens.add(" ".join(val.split()).casefold())
    return tokens


def enforce_separation_of_duties(
    store: Any,
    actor: dict[str, Any],
    proposer_identity: str,
    *,
    proposer_user: Mapping[str, Any] | None = None,
    action: str = "approve",
    require_entra: bool = True,
) -> dict[str, Any]:
    """Require a distinct approver from the human proposer across Entra OIDs and aliases."""
    verified_actor = require_regulatory_role(actor, "approve", require_entra=require_entra)
    clean_proposer = " ".join(proposer_identity.split()).casefold()
    if not clean_proposer or clean_proposer == "system":
        return verified_actor
    actor_tokens = _principal_tokens(verified_actor)
    if clean_proposer in actor_tokens:
        raise PermissionError(
            f"Separation of duties prevents the proposer from performing {action}."
        )
    if proposer_user is not None:
        proposer_tokens = _principal_tokens(proposer_user)
        if actor_tokens & proposer_tokens:
            raise PermissionError(
                f"Separation of duties prevents the proposer from performing {action}."
            )
    if store is not None:
        if identity.is_entra(verified_actor):
            identity.link(store, verified_actor)
        if proposer_user is not None and identity.is_entra(dict(proposer_user)):
            identity.link(store, dict(proposer_user))
        actor_key = str(verified_actor.get("email") or verified_actor.get("code") or "")
        if not identity.distinct(store, actor_key, proposer_identity):
            raise PermissionError(
                f"Separation of duties prevents the proposer from performing {action}."
            )
    return verified_actor


MAX_REASON = 1000
PROPOSAL_KINDS = frozenset(("check_outcome", "alert_triage", "rule_card_change"))
_FORBIDDEN_DECIDERS = frozenset(
    (
        "system",
        "agent",
        "ai",
        "model",
        "auto",
        "assistant",
        "copilot",
        "bot",
        "llm",
        "unassigned",
        "tbd",
        "unknown",
        "none",
        "n/a",
        "named dpo (unassigned)",
    )
)


def record_human_decision(
    proposal: dict[str, Any], decider: str, role: str, outcome: str, reasons: str, at: str
) -> dict[str, Any]:
    """Art 22A-22C: the system proposes; only a named human with reasons decides."""
    kind = str(proposal.get("kind") or "")
    if kind not in PROPOSAL_KINDS:
        raise ValueError("Unsupported proposal kind; use the manual path.")
    if outcome not in ("accepted", "rejected", "changed"):
        raise ValueError("Decision outcome must be accepted, rejected or changed.")
    name, why = decider.strip(), reasons.strip()
    clean_role = role.strip()
    if not name or name.lower() in _FORBIDDEN_DECIDERS or "unassigned" in name.lower():
        raise ValueError("A named human decider is required.")
    if clean_role not in ("approver", "rule_owner"):
        raise ValueError("Only the approver role can record a consequential decision.")
    if not why or len(why) > MAX_REASON:
        raise ValueError(f"Recorded reasons are required, up to {MAX_REASON} characters.")
    if _is_memory_reference(why):
        raise ValueError("Memory is never evidence and cannot be cited.")
    if datetime.fromisoformat(at).tzinfo is None:
        raise ValueError("Decision needs a timezone-aware recorded time.")
    return dict(
        proposal_kind=kind,
        proposal_id=str(proposal.get("id") or ""),
        proposal_version=str(proposal.get("version") or ""),
        decider=name,
        role=clean_role,
        outcome=outcome,
        reasons=why,
        decided_at=at,
        decided_by_system=False,
    )


_CONSEQUENTIAL_TABLES = ("reg_consequential_proposal", "reg_consequential_decision")
_CONSEQUENTIAL_SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS reg_consequential_proposal ("
    "proposal_id TEXT NOT NULL, proposal_version TEXT NOT NULL, kind TEXT NOT NULL, "
    "case_id TEXT NOT NULL, proposed_by TEXT NOT NULL, proposed_at TEXT NOT NULL, "
    "body TEXT NOT NULL, PRIMARY KEY (proposal_id, proposal_version))",
    "CREATE TABLE IF NOT EXISTS reg_consequential_decision ("
    "proposal_id TEXT NOT NULL, proposal_version TEXT NOT NULL, decision_id TEXT NOT NULL, "
    "kind TEXT NOT NULL, outcome TEXT NOT NULL, decider_id TEXT NOT NULL, "
    "decider_name TEXT NOT NULL, decider_oid TEXT, decider_tid TEXT, "
    "decider_role TEXT NOT NULL, reasons TEXT NOT NULL, decided_at TEXT NOT NULL, "
    "body TEXT NOT NULL, PRIMARY KEY (proposal_id, proposal_version))",
)
_CONSEQUENTIAL_MSSQL_DDL = (
    "CREATE TABLE reg_consequential_proposal ("
    "proposal_id VARCHAR(64) NOT NULL, proposal_version VARCHAR(64) NOT NULL, "
    "kind VARCHAR(40) NOT NULL, case_id VARCHAR(64) NOT NULL, "
    "proposed_by NVARCHAR(200) NOT NULL, proposed_at VARCHAR(40) NOT NULL, "
    "body NVARCHAR(MAX) NOT NULL, PRIMARY KEY (proposal_id, proposal_version))",
    "CREATE TABLE reg_consequential_decision ("
    "proposal_id VARCHAR(64) NOT NULL, proposal_version VARCHAR(64) NOT NULL, "
    "decision_id VARCHAR(64) NOT NULL, kind VARCHAR(40) NOT NULL, "
    "outcome VARCHAR(20) NOT NULL, decider_id NVARCHAR(200) NOT NULL, "
    "decider_name NVARCHAR(200) NOT NULL, decider_oid VARCHAR(64) NULL, "
    "decider_tid VARCHAR(64) NULL, decider_role VARCHAR(40) NOT NULL, "
    "reasons NVARCHAR(1000) NOT NULL, decided_at VARCHAR(40) NOT NULL, "
    "body NVARCHAR(MAX) NOT NULL, PRIMARY KEY (proposal_id, proposal_version))",
)
_LEDGER_SUFFIX = " WITH (LEDGER = ON (APPEND_ONLY = ON))"
ART22_HUMAN_FLAG = "uk-gdpr-art-22a-human-required"


def _append_store_audit(
    store: Any, who: str, action: str, case_id: str, detail_obj: dict[str, Any]
) -> None:
    if store is None:
        return
    detail = json.dumps(detail_obj, sort_keys=True)
    audit_fn = cast(Callable[[str, str, str, str], None], store.audit)
    audit_fn(who, action, case_id, detail)


class ConsequentialDecisionGuard:
    """Append-only UK GDPR Art 22A-22C guard: system proposes/flags; named human decides."""

    def __init__(self, law: Any, *, store: Any = None) -> None:
        self.law = law
        self.store = store
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        with self.law.rules.transaction():
            if self.law.sql.dialect == "mssql":
                for table, ddl in zip(_CONSEQUENTIAL_TABLES, _CONSEQUENTIAL_MSSQL_DDL, strict=True):
                    suffix = _LEDGER_SUFFIX if self.law.sql.ledger else ""
                    self.law.sql.run(f"IF OBJECT_ID(N'{table}', N'U') IS NULL {ddl}{suffix}")
                    if not self.law.sql.ledger:
                        self.law.sql.run(
                            f"IF OBJECT_ID(N'{table}_append_only', N'TR') IS NULL "
                            f"EXEC(N'CREATE TRIGGER {table}_append_only ON {table} "
                            f"INSTEAD OF UPDATE, DELETE AS "
                            f"THROW 50001, ''{table} is append-only'', 1')"
                        )
            else:
                for ddl in _CONSEQUENTIAL_SQLITE_DDL:
                    self.law.sql.run(ddl)
                for table in _CONSEQUENTIAL_TABLES:
                    for op in ("UPDATE", "DELETE"):
                        self.law.sql.run(
                            f"CREATE TRIGGER IF NOT EXISTS {table}_no_{op.lower()} "
                            f"BEFORE {op} ON {table} BEGIN "
                            f"SELECT RAISE(ABORT, '{table} is append-only'); END"
                        )

    @staticmethod
    def _clean_id(value: str, label: str) -> str:
        text = value.strip()
        if not 1 <= len(text) <= 64 or not set(text) <= _ID_CHARS:
            raise ValueError(f"{label} must be a short identifier, not free text.")
        return text

    def propose(
        self,
        *,
        proposal_id: str,
        proposal_version: str,
        kind: str,
        case_id: str,
        summary: str,
        flags: Sequence[str] = (),
        proposed_by: str = "system",
        proposer_user: dict[str, Any] | None = None,
        at: str,
        status: str = "proposed",
    ) -> dict[str, Any]:
        """Record a non-binding flagged proposal; system-decided statuses are refused."""
        if status != "proposed":
            raise ValueError("System can only propose and flag; human decision is required.")
        if kind not in PROPOSAL_KINDS:
            raise ValueError("Unsupported proposal kind; use the manual path.")
        pid = self._clean_id(proposal_id, "proposal_id")
        pver = self._clean_id(proposal_version, "proposal_version")
        cid = self._clean_id(case_id, "case_id")
        if datetime.fromisoformat(at).tzinfo is None:
            raise ValueError("Proposal needs a timezone-aware recorded time.")
        clean_summary = summary.strip()
        if not clean_summary or len(clean_summary) > 400:
            raise ValueError("Proposal summary must contain 1 to 400 characters.")
        if _is_memory_reference(clean_summary):
            raise ValueError("Memory is never evidence and cannot be cited.")
        masked_summary, _ = _redact(clean_summary)
        flag_list = sorted(
            {self._clean_id(flag, "flag") for flag in (*flags, ART22_HUMAN_FLAG) if flag.strip()}
        )
        proposer_ref = proposed_by.strip() or "system"
        proposer_snapshot: dict[str, Any] | None = None
        if proposer_user is not None:
            if self.store is not None and identity.is_entra(proposer_user):
                identity.link(self.store, proposer_user)
            proposer_ref = str(
                proposer_user.get("email") or proposer_user.get("code") or proposer_ref
            ).strip()
            proposer_snapshot = {
                k: proposer_user[k]
                for k in ("email", "code", "derived_email", "derived_code", "oid", "tid")
                if k in proposer_user
            }
        record = dict(
            proposal_id=pid,
            proposal_version=pver,
            kind=kind,
            case_id=cid,
            summary=masked_summary,
            flags=flag_list,
            status="proposed",
            effect="non_binding_proposal",
            decided_by_system=False,
            requires_named_human=True,
            proposed_by=proposer_ref,
            proposer_snapshot=proposer_snapshot,
            proposed_at=at,
        )
        with self.law.rules.transaction():
            existing = self.law.sql.all(
                "SELECT proposal_id FROM reg_consequential_proposal "
                "WHERE proposal_id=? AND proposal_version=?",
                (pid, pver),
            )
            if existing:
                raise ValueError("Proposal version already exists; use a new proposal_version.")
            self.law.sql.run(
                "INSERT INTO reg_consequential_proposal "
                "(proposal_id, proposal_version, kind, case_id, proposed_by, proposed_at, body) "
                "VALUES (?,?,?,?,?,?,?)",
                (pid, pver, kind, cid, proposer_ref, at, json.dumps(record, sort_keys=True)),
            )
        _append_store_audit(
            self.store,
            proposer_ref,
            "regulatory.art22.propose",
            cid,
            dict(
                proposal_id=pid,
                proposal_version=pver,
                kind=kind,
                flag_count=len(flag_list),
                decided_by_system=False,
                label="synthetic-demo",
            ),
        )
        return record

    def decide(
        self,
        *,
        proposal_id: str,
        proposal_version: str,
        user: dict[str, Any],
        outcome: str,
        reasons: str,
        at: str,
        require_entra: bool = True,
    ) -> dict[str, Any]:
        """Verify separate approver authority and retain an immutable human decision."""
        pid = self._clean_id(proposal_id, "proposal_id")
        pver = self._clean_id(proposal_version, "proposal_version")
        verified_user = require_regulatory_role(
            user, "consequential_decision", require_entra=require_entra
        )
        with self.law.rules.transaction():
            prop_rows = self.law.sql.all(
                "SELECT body FROM reg_consequential_proposal "
                "WHERE proposal_id=? AND proposal_version=?",
                (pid, pver),
            )
            if not prop_rows:
                raise LookupError(f"Unknown consequential proposal {pid}@{pver}.")
            prop = cast(dict[str, Any], json.loads(str(prop_rows[0]["body"])))
            prior = self.law.sql.all(
                "SELECT outcome FROM reg_consequential_decision "
                "WHERE proposal_id=? AND proposal_version=?",
                (pid, pver),
            )
            if prior:
                raise ValueError(
                    "Decision already retained for this proposal version; propose a new version."
                )
            enforce_separation_of_duties(
                self.store,
                verified_user,
                str(prop["proposed_by"]),
                proposer_user=prop.get("proposer_snapshot"),
                action="consequential_decision",
                require_entra=require_entra,
            )
            decider_name = str(verified_user.get("name") or "").strip()
            built = record_human_decision(
                dict(kind=prop["kind"], id=pid, version=pver),
                decider=decider_name,
                role="rule_owner",
                outcome=outcome,
                reasons=reasons,
                at=at,
            )
            decider_id = str(
                verified_user.get("email") or verified_user.get("code") or decider_name
            ).strip()
            decider_oid = identity.canonical_guid(verified_user.get("oid"))
            decider_tid = identity.canonical_guid(verified_user.get("tid"))
            decision_id = hashlib.sha256(f"{pid}:{pver}:{decider_id}:{at}".encode()).hexdigest()[
                :16
            ]
            retained = dict(
                **built,
                decision_id=decision_id,
                case_id=prop["case_id"],
                decider_id=decider_id,
                decider_oid=decider_oid,
                decider_tid=decider_tid,
                staff_role=str(verified_user.get("role") or ""),
                retained=True,
            )
            self.law.sql.run(
                "INSERT INTO reg_consequential_decision "
                "(proposal_id, proposal_version, decision_id, kind, outcome, decider_id, "
                "decider_name, decider_oid, decider_tid, decider_role, reasons, decided_at, body) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    pid,
                    pver,
                    decision_id,
                    str(prop["kind"]),
                    outcome,
                    decider_id,
                    built["decider"],
                    decider_oid,
                    decider_tid,
                    "rule_owner",
                    built["reasons"],
                    at,
                    json.dumps(retained, sort_keys=True),
                ),
            )
        _append_store_audit(
            self.store,
            decider_id,
            "regulatory.art22.decide",
            str(prop["case_id"]),
            dict(
                decision_id=decision_id,
                proposal_id=pid,
                proposal_version=pver,
                kind=prop["kind"],
                outcome=outcome,
                decider_oid=decider_oid,
                reasons_sha256=hashlib.sha256(built["reasons"].encode()).hexdigest(),
                reasons_length=len(built["reasons"]),
                decided_by_system=False,
                label="synthetic-demo",
            ),
        )
        return retained

    def authorize_consequential_action(
        self, proposal_id: str, proposal_version: str
    ) -> dict[str, Any]:
        """Fail closed unless a retained named-human accepted decision exists for this version."""
        pid = self._clean_id(proposal_id, "proposal_id")
        pver = self._clean_id(proposal_version, "proposal_version")
        with self.law.sql.lock:
            prop_rows = self.law.sql.all(
                "SELECT proposal_id FROM reg_consequential_proposal "
                "WHERE proposal_id=? AND proposal_version=?",
                (pid, pver),
            )
            if not prop_rows:
                raise PermissionError(
                    "Consequential action refused: no flagged proposal is recorded."
                )
            dec_rows = self.law.sql.all(
                "SELECT body FROM reg_consequential_decision "
                "WHERE proposal_id=? AND proposal_version=?",
                (pid, pver),
            )
        if not dec_rows:
            raise PermissionError(
                "Consequential action refused: a named human decision with reasons is required."
            )
        decision = cast(dict[str, Any], json.loads(str(dec_rows[0]["body"])))
        if decision.get("decided_by_system") is not False or not decision.get("reasons"):
            raise PermissionError("Consequential action refused: invalid human-decision record.")
        if decision.get("outcome") != "accepted":
            outcome = decision.get("outcome")
            raise PermissionError(
                f"Consequential action refused: human decision outcome is {outcome}."
            )
        return dict(
            authorized=True,
            decision_id=decision["decision_id"],
            proposal_id=pid,
            proposal_version=pver,
            decider=decision["decider"],
            decider_id=decision["decider_id"],
            outcome=decision["outcome"],
            decided_at=decision["decided_at"],
            decided_by_system=False,
        )

    def history(self, user: dict[str, Any], *, case_id: str | None = None) -> list[dict[str, Any]]:
        """Return retained proposals and decisions for scoped staff; mask reasons when held."""
        if bool(user.get("view_only")) or user.get("role") not in _STAFF_ROLES:
            raise PermissionError("Only scoped staff can inspect consequential decision records.")
        with self.law.sql.lock:
            query = "SELECT body FROM reg_consequential_proposal"
            params: tuple[Any, ...] = (case_id,) if case_id is not None else ()
            if case_id is not None:
                query += " WHERE case_id=?"
            proposals = [
                cast(dict[str, Any], json.loads(str(r["body"])))
                for r in self.law.sql.all(query + " ORDER BY proposed_at, proposal_id", params)
            ]
            decisions = {
                (str(r["proposal_id"]), str(r["proposal_version"])): cast(
                    dict[str, Any], json.loads(str(r["body"]))
                )
                for r in self.law.sql.all(
                    "SELECT proposal_id, proposal_version, body FROM reg_consequential_decision"
                )
            }
        show_reasons = _can_see_reason(user) or "rule_owner" in (
            resolve_entra_regulatory_roles(user) | set(user.get("rule_roles") or ())
        )
        out: list[dict[str, Any]] = []
        for prop in proposals:
            key = (str(prop["proposal_id"]), str(prop["proposal_version"]))
            dec = decisions.get(key)
            if dec is not None and not show_reasons:
                dec = dict(dec, reasons=_NOTE_HELD)
            clean_prop = {k: v for k, v in prop.items() if k != "proposer_snapshot"}
            out.append(dict(proposal=clean_prop, decision=dec))
        return out


METERING_FIELDS = {
    "surface": "id",
    "record_id": "id",
    "model_id": "id",
    "prompt_version": "id",
    "rule_card_version": "id",
    "input_tokens": "count",
    "output_tokens": "count",
    "cached_tokens": "count",
    "retry_count": "count",
    "occurred_at": "time",
}
METERING_SURFACES = frozenset(("chat", "check"))
_ID_CHARS = frozenset("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-")


def metering_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Closed schema: identifiers, counts and versions only; never free text or cost."""
    unknown = sorted(set(raw) - set(METERING_FIELDS))
    if unknown:
        raise ValueError(f"Metering refuses fields outside the closed schema: {unknown}")
    missing = sorted(k for k in ("surface", "record_id", "occurred_at") if k not in raw)
    if missing:
        raise ValueError(f"Metering needs: {missing}")
    if raw["surface"] not in METERING_SURFACES:
        raise ValueError("Metering surface must be chat or check.")
    out: dict[str, Any] = {}
    for key, value in raw.items():
        kind = METERING_FIELDS[key]
        if kind == "count":
            if type(value) is not int or not 0 <= value <= 10**12:
                raise ValueError(f"{key} must be a bounded non-negative integer.")
        elif kind == "time":
            if not isinstance(value, str) or datetime.fromisoformat(value).tzinfo is None:
                raise ValueError("occurred_at must be a timezone-aware ISO time.")
        elif key != "surface" and (
            not isinstance(value, str) or not 1 <= len(value) <= 64 or not set(value) <= _ID_CHARS
        ):
            raise ValueError(f"{key} must be a short identifier, not free text.")
        out[key] = value
    out["retention_class"] = "usage"
    return out


COST_FIELDS = {
    "surface": "id",
    "record_id": "id",
    "model_id": "id",
    "prompt_version": "id",
    "rule_card_version": "id",
    "price_version": "id",
    "currency": "currency",
    "input_tokens": "count",
    "output_tokens": "count",
    "cached_tokens": "count",
    "retry_count": "count",
    "cost_minor_units": "minor_units",
    "cost": "cost_status",
    "occurred_at": "time",
}
_REQUIRED_COST_FIELDS = (
    "surface",
    "record_id",
    "model_id",
    "price_version",
    "input_tokens",
    "output_tokens",
    "cost",
    "occurred_at",
)


def cost_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Closed cost schema: identifiers, counts, versions and OD-51 Unknown/minor-unit status."""
    unknown = sorted(set(raw) - set(COST_FIELDS))
    if unknown:
        raise ValueError(f"Cost record refuses fields outside the closed schema: {unknown}")
    missing = sorted(k for k in _REQUIRED_COST_FIELDS if k not in raw)
    if missing:
        raise ValueError(f"Cost record needs: {missing}")
    if raw["surface"] not in METERING_SURFACES:
        raise ValueError("Cost surface must be chat or check.")
    out: dict[str, Any] = {}
    for key, value in raw.items():
        kind = COST_FIELDS[key]
        if kind == "count":
            if type(value) is not int or not 0 <= value <= 10**12:
                raise ValueError(f"{key} must be a bounded non-negative integer.")
        elif kind == "time":
            if not isinstance(value, str) or datetime.fromisoformat(value).tzinfo is None:
                raise ValueError("occurred_at must be a timezone-aware ISO time.")
        elif kind == "currency":
            if value is not None and (
                not isinstance(value, str)
                or len(value) != 3
                or not value.isascii()
                or not value.isalpha()
                or not value.isupper()
            ):
                raise ValueError("currency must be a 3-letter uppercase ISO code or None.")
        elif kind == "minor_units":
            if value is not None and (type(value) is not int or not 0 <= value <= 10**12):
                raise ValueError("cost_minor_units must be None or a bounded non-negative integer.")
        elif kind == "cost_status":
            if value not in ("Unknown", "calculated"):
                raise ValueError("cost must be Unknown or calculated.")
        elif key != "surface" and (
            not isinstance(value, str) or not 1 <= len(value) <= 64 or not set(value) <= _ID_CHARS
        ):
            raise ValueError(f"{key} must be a short identifier, not free text.")
        out[key] = value
    if out["price_version"] == "unpriced":
        if out["cost"] != "Unknown" or out.get("cost_minor_units") is not None:
            raise ValueError("Unpriced records must report cost Unknown and cost_minor_units None.")
        out.setdefault("cost_minor_units", None)
        out.setdefault("currency", None)
    else:
        if (
            out["cost"] != "calculated"
            or type(out.get("cost_minor_units")) is not int
            or not isinstance(out.get("currency"), str)
        ):
            raise ValueError(
                "Priced records need cost='calculated', integer cost_minor_units and currency."
            )
    out["retention_class"] = "usage"
    return out
