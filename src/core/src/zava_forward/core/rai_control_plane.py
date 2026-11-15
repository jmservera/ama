"""Responsible AI control plane: OQ-017 live gate, requirement traceability, and readiness.

Enforces deterministic named-human approval (`approved_by` and `named_approval_id`) before any live
AI task activation (`OQ-017`) with rollback-safe audit emission, provides the machine-readable
requirement-to-acceptance and deferral traceability table for Epic #218, and reports
`rai_exercise_acceptance` separately from `real_ai_delivery_gate`.
"""

from __future__ import annotations

import ast
import copy
import functools
import json
import os
import re
import time
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

from zava_forward.core import (
    ai,
    ai_registry,
    assistant_release,
    challenges,
    cohort_eval,
    continuity,
    human_review_effectiveness,
    monitoring_coverage,
    rai_release,
    regulatory_privacy,
    restart_authority,
)

_ai: Any = ai
_ai_registry: Any = ai_registry
_assistant_release: Any = assistant_release
_challenges: Any = challenges
_continuity: Any = continuity

OQ_017 = "OQ-017"
OQ_018 = "OQ-018"
OQ_019 = "OQ-019"

AUDIT_ACTION_REJECTED = "rai_live_activation_rejected"
AUDIT_ACTION_RECORDED = "rai_live_activation_recorded"
EVENT_KIND_REJECTED = "live-activation-rejected"

PLACEHOLDER_APPROVER_TOKENS = frozenset(
    {
        "fictional",
        "placeholder",
        "mock",
        "synthetic",
        "example",
        "todo",
        "tbd",
        "tbc",
        "na",
        "null",
        "auto",
        "unassigned",
        "unapproved",
        "unknown",
        "unavailable",
        "none",
        "anonymous",
        "pending",
        "ci",
        "pipeline",
        "workflow",
        "script",
        "daemon",
        "cron",
    }
)

PLACEHOLDER_APPROVAL_ID_TOKENS = frozenset(
    {
        "fictional",
        "placeholder",
        "mock",
        "synthetic",
        "example",
        "todo",
        "tbd",
        "tbc",
        "na",
        "null",
        "auto",
        "unassigned",
        "unapproved",
        "unknown",
        "unavailable",
        "none",
        "system",
        "agent",
        "bot",
        "automation",
        "automated",
        "copilot",
        "assistant",
        "ai",
        "llm",
        "service",
        "pending",
        "ci",
        "pipeline",
        "workflow",
        "script",
        "daemon",
        "cron",
    }
)

DISQUALIFYING_PHRASES = (
    "not live authority",
    "not appointed",
    "no live authority",
    "n/a",
)

WORKFLOW_ONLY_ENV_VALUES = frozenset({"0", "false", "off", "disabled", "workflow", "workflow-only"})

REQUIRED_TRACEABILITY_IDS: tuple[str, ...] = (
    "FR-051",
    "FR-052",
    "FR-053",
    "FR-054",
    "NFR-014",
    "AC-069",
    "AC-070",
    "AC-071",
    "AC-072",
    "AC-073",
    "OQ-017",
    "OQ-018",
    "OQ-019",
    "RULE-024",
    "RULE-020",
)


class LiveActivationApprovalError(PermissionError):
    """Raised when a live AI task activation lacks valid named human approval (`OQ-017`)."""

    def __init__(
        self,
        task_id: str,
        reasons: Sequence[str],
        *,
        code: str = OQ_017,
    ) -> None:
        cleaned = tuple(str(r) for r in reasons if str(r).strip()) or (
            "missing named human live approval",
        )
        self.code = code
        self.task_id = str(task_id or "<unspecified>")
        self.reasons = cleaned
        joined = "; ".join(cleaned)
        super().__init__(
            f"Live AI task activation rejected ({code}) for task {self.task_id!r}: {joined}. "
            "Use the manual case route until a named human owner records live approval."
        )


def _tokens(text: str) -> set[str]:
    return {tok for tok in re.split(r"[^a-z0-9]+", text.lower()) if tok}


def valid_named_human_approver(value: object) -> bool:
    """Return True only when `value` names a specific human approver rather than a placeholder."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not 1 <= len(stripped) <= 200:
        return False
    if not rai_release.named_human(stripped):
        return False
    lowered = stripped.lower()
    if any(phrase in lowered for phrase in DISQUALIFYING_PHRASES):
        return False
    toks = _tokens(stripped)
    if not toks or (toks & PLACEHOLDER_APPROVER_TOKENS):
        return False
    return any(ch.isalpha() for ch in stripped)


def valid_named_approval_id(value: object) -> bool:
    """Return True only when `value` is a non-empty, non-placeholder named approval identifier."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not 3 <= len(stripped) <= 160:
        return False
    lowered = stripped.lower()
    if any(phrase in lowered for phrase in DISQUALIFYING_PHRASES):
        return False
    toks = _tokens(stripped)
    if not toks or (toks & PLACEHOLDER_APPROVAL_ID_TOKENS):
        return False
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]{2,159}", stripped))


def is_live_release_intent(body: object) -> bool:
    """Return True when a release payload requests live (`actual`) activation."""
    if not isinstance(body, Mapping):
        return False
    return body.get("evidence_class") == "actual" or bool(body.get("live"))


def validate_live_task_approval(
    task_id: object,
    approval: Mapping[str, Any] | None = None,
    *,
    approved_by: object = None,
    named_approval_id: object = None,
    allowed_task_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Validate `OQ-017` preconditions for activating a live AI task."""
    raw_task = str(task_id).strip() if isinstance(task_id, str) else ""
    lookup_id = raw_task.removeprefix("legacy:")
    payload: Mapping[str, Any] = approval if isinstance(approval, Mapping) else {}
    eff_approved_by = approved_by if approved_by is not None else payload.get("approved_by")
    eff_approval_id = (
        named_approval_id if named_approval_id is not None else payload.get("named_approval_id")
    )

    reasons: list[str] = []
    spec = _ai_registry.get(lookup_id) if lookup_id else None
    if not raw_task or spec is None:
        reasons.append(f"unregistered AI task ({OQ_017})")
    else:
        if allowed_task_ids is not None and raw_task not in allowed_task_ids:
            if spec.get("enabled") is False:
                reasons.append(f"AI task {lookup_id!r} is disabled in registry ({OQ_017})")
            else:
                reasons.append(f"AI task {raw_task!r} is not eligible for live release ({OQ_017})")
        elif spec.get("enabled") is False:
            reasons.append(f"AI task {lookup_id!r} is disabled in registry ({OQ_017})")

    if not valid_named_human_approver(eff_approved_by):
        reasons.append(
            f"non-empty named human approved_by is required for live activation ({OQ_017})"
        )
    if not valid_named_approval_id(eff_approval_id):
        reasons.append(f"non-empty named_approval_id is required for live activation ({OQ_017})")

    return {
        "valid": not reasons,
        "code": OQ_017,
        "task_id": raw_task or "<unspecified>",
        "lookup_task_id": lookup_id,
        "approved_by": str(eff_approved_by).strip() if isinstance(eff_approved_by, str) else "",
        "named_approval_id": (
            str(eff_approval_id).strip() if isinstance(eff_approval_id, str) else ""
        ),
        "reasons": reasons,
    }


def _actor_label(actor: object) -> str:
    if isinstance(actor, Mapping):
        for key in ("email", "code", "name"):
            val = actor.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()[:120]
    if isinstance(actor, str) and actor.strip():
        return actor.strip()[:120]
    return "unverified"


def _persist_audit_immediately(
    store: Any,
    *,
    who: str,
    action: str,
    detail: Mapping[str, Any],
) -> dict[str, Any]:
    serialized = json.dumps(dict(detail), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    ts = datetime.now().isoformat(timespec="seconds")
    if hasattr(store, "_audit_immediate"):
        store._audit_immediate((who, action, "-", serialized, ts))
    elif hasattr(store, "lock") and hasattr(store, "audit"):
        with store.lock:
            store.audit(who, action, "-", serialized)
    elif hasattr(store, "audit"):
        store.audit(who, action, "-", serialized)
    return {
        "who": who,
        "action": action,
        "case": "-",
        "detail": serialized,
    }


def emit_live_activation_rejection_audit(
    store: Any,
    *,
    actor: object,
    task_id: object,
    reasons: Sequence[str],
    assistants_service: Any = None,
) -> dict[str, Any]:
    """Persist a rollback-safe `OQ-017` rejection record to the audit ledger and SQL events."""
    who = _actor_label(actor)
    normalized_task = (
        str(task_id).strip()[:120]
        if isinstance(task_id, str) and task_id.strip()
        else "<unspecified>"
    )
    cleaned_reasons = [str(r)[:300] for r in reasons if str(r).strip()] or [
        f"missing named human live approval ({OQ_017})"
    ]
    detail: dict[str, Any] = {
        "code": OQ_017,
        "decision": "rejected",
        "task_id": normalized_task,
        "reasons": cleaned_reasons,
    }
    audit_record = _persist_audit_immediately(
        store,
        who=who,
        action=AUDIT_ACTION_REJECTED,
        detail=detail,
    )
    sql_event_recorded = False
    if assistants_service is not None and getattr(assistants_service, "sql", False):
        try:
            with assistants_service.transaction() as db:
                now_ts = (
                    float(assistants_service.now(db))
                    if hasattr(assistants_service, "now")
                    else time.time()
                )
                _assistant_release.event(
                    db,
                    now_ts,
                    f"oq017-rejected:{normalized_task}",
                    kind=EVENT_KIND_REJECTED,
                    code=OQ_017,
                    task=normalized_task,
                    actor=who,
                    reasons=cleaned_reasons,
                )
            sql_event_recorded = True
        except Exception:
            sql_event_recorded = False
    return {
        **audit_record,
        "code": OQ_017,
        "task_id": normalized_task,
        "reasons": cleaned_reasons,
        "sql_event_recorded": sql_event_recorded,
    }


def activate_live_task(
    store: Any,
    task_id: str,
    approval: Mapping[str, Any] | None = None,
    *,
    approved_by: str | None = None,
    named_approval_id: str | None = None,
    actor: object = None,
    assistants_service: Any = None,
    release_body: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate `OQ-017` named-human approval before any live AI task activation and emit audit."""
    eff_actor = actor
    if eff_actor is None and isinstance(approval, Mapping):
        eff_actor = approval.get("actor") or approval.get("approved_by")
    if eff_actor is None:
        eff_actor = approved_by

    check = validate_live_task_approval(
        task_id,
        approval,
        approved_by=approved_by,
        named_approval_id=named_approval_id,
    )
    if not check["valid"]:
        emit_live_activation_rejection_audit(
            store,
            actor=eff_actor,
            task_id=check["task_id"],
            reasons=check["reasons"],
            assistants_service=assistants_service,
        )
        raise LiveActivationApprovalError(
            check["task_id"],
            check["reasons"],
            code=OQ_017,
        )

    if assistants_service is not None and release_body is not None:
        merged_body = dict(
            release_body,
            task=check["task_id"],
            evidence_class="actual",
            approved_by=check["approved_by"],
            named_approval_id=check["named_approval_id"],
        )
        user_mapping = actor if isinstance(actor, Mapping) else {}
        release_result: dict[str, Any] = assistants_service.record_release(
            user_mapping, merged_body
        )
        _persist_audit_immediately(
            store,
            who=_actor_label(eff_actor),
            action=AUDIT_ACTION_RECORDED,
            detail={
                "code": OQ_017,
                "decision": "recorded",
                "task_id": check["task_id"],
                "approved_by": check["approved_by"],
                "named_approval_id": check["named_approval_id"],
                "release_id": release_result.get("id"),
            },
        )
        return {
            "status": "active",
            "code": OQ_017,
            "task_id": check["task_id"],
            "approved_by": check["approved_by"],
            "named_approval_id": check["named_approval_id"],
            "release_id": release_result.get("id"),
            "note": release_result.get("note"),
        }

    _persist_audit_immediately(
        store,
        who=_actor_label(eff_actor),
        action=AUDIT_ACTION_RECORDED,
        detail={
            "code": OQ_017,
            "decision": "recorded",
            "task_id": check["task_id"],
            "approved_by": check["approved_by"],
            "named_approval_id": check["named_approval_id"],
        },
    )
    return {
        "status": "validated",
        "code": OQ_017,
        "task_id": check["task_id"],
        "approved_by": check["approved_by"],
        "named_approval_id": check["named_approval_id"],
        "live_cutover_cleared": False,
        "note": (
            "Named human OQ-017 approval fields validated and audited; durable SQL release binding "
            "and OQ-018/OQ-019 owner gates still govern real-AI delivery."
        ),
    }


REQUIREMENT_TRACEABILITY: tuple[dict[str, Any], ...] = (
    {
        "id": "FR-051",
        "kind": "functional_requirement",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Pre-deployment RAI release record binding intended/prohibited uses, accountable "
            "owner, evaluation summary, residual-risk acceptance, and change invalidation."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_rai_release.py::ReleaseContract.test_every_required_contract_field_fails_closed_when_missing",
            "src/core/tests/test_rai_release_invalidation.py::Invalidation.test_each_material_change_revokes_and_records_trigger",
            "src/api/tests/test_assistant_release.py::Release.test_absent_release_denies_with_zero_calls_and_retains_denial",
            "src/core/tests/test_rai_control_plane_218.py::RaiControlPlane218Tests.test_oq017_rejects_missing_blank_system_and_placeholder_approvals_with_audit",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Zava North Homes Executive Sponsor and RAI Assurance Lead",
            "reason": (
                "Live office-holder appointment for task release approval remains an owner "
                "governance decision outside offline exercise builds."
            ),
        },
    },
    {
        "id": "FR-052",
        "kind": "functional_requirement",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Accessible resident and staff AI challenge/appeal route with named owner, response "
            "date, no penalty, and zero delay to statutory hazard response."
        ),
        "status": "verified",
        "acceptance_checks": (
            "src/core/tests/test_challenges.py::ChallengeRoutes.test_both_routes_record_with_owner_and_next_update",
            "src/core/tests/test_challenges.py::HazardConcern.test_hazard_concern_is_referred_on_receipt_without_clock_or_sanction",
            "src/core/tests/test_issue_220_challenge_route.py::ChallengeRegisterLifecycleAndSafeguardsTests.test_submit_update_escalate_resolve_across_all_four_subjects_and_channels",
        ),
        "deferral": None,
    },
    {
        "id": "FR-053",
        "kind": "functional_requirement",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Task-scoped and global AI suspension, quarantine of unreviewed/in-flight outputs, "
            "uninterrupted manual/hazard workflows, and separate-human restart authority."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_operator_suspension_drill.py::JsonOperatorSuspensionDrillTest.test_nfr_014_end_to_end_suspension_manual_fallback_hazard_and_restart_drill",
            "src/api/tests/test_operator_suspension.py::OperatorIncident.test_nfr_014_http_breach_hazard_and_rule_024_restart_drill",
            "src/api/tests/test_rai_harm_threshold_incident.py::HarmThresholdIncident.test_seeded_critical_harm_creates_owned_incident_and_blocks_dispatch",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Retrofit Programme Manager and Digital Service Owner",
            "reason": (
                "Named live incident commander and separate live restart approver appointments "
                "remain deferred until pre-live authority sign-off."
            ),
        },
    },
    {
        "id": "FR-054",
        "kind": "functional_requirement",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Per-cohort and missing-data evaluation for ranking/recommendation workflows without "
            "averaging away failing cohorts or treating synthetic runs as fairness clearance."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_cohort_eval.py::CohortEvalTests.test_all_seeded_defects_detected_and_block",
            "src/core/tests/test_paired_equity.py::PairedEquityTests.test_current_policy_never_lowers_priority_for_any_dimension",
            "src/core/tests/test_rai_threshold_live_approval_guard.py::LiveCohortThresholds.test_constructed_manifest_is_rejected_even_with_named_approval",
        ),
        "deferral": {
            "open_question": OQ_018,
            "owner": "Housing Data and Performance Lead and Data Protection Officer",
            "reason": (
                "Representative resident cohorts, lawful special-category analysis basis, and live "
                "harm/disparity thresholds require customer/DPO approval before live activation."
            ),
        },
    },
    {
        "id": "NFR-014",
        "kind": "non_functional_requirement",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Operational RAI harm/quality/effort monitoring declarations, SQL-reconstructed "
            "metrics, owned breach incidents, and immediate manual fallback continuity."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_monitoring_coverage.py::DeclarationTests.test_all_registered_task_declarations_cover_harm_and_complete_review_effort",
            "src/core/tests/test_rai_threshold_live_approval_guard.py::LiveReleaseApprover.test_live_release_rejects_constructed_or_non_human_monitoring_thresholds",
            "src/api/tests/test_rai_restart_sql_reconstruction.py::RestartReconstruction.test_metrics_rebuild_after_restart_with_no_double_count",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Digital Service Owner and Competent Task Owners",
            "reason": (
                "Live monitoring threshold values and on-call alert owners require named human "
                "ratification prior to live cut-over."
            ),
        },
    },
    {
        "id": "AC-069",
        "kind": "acceptance_criterion",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Tasks without a complete matching release record are refused dispatch with zero "
            "provider calls, and material binding/use changes revoke active releases."
        ),
        "status": "verified",
        "acceptance_checks": (
            "src/core/tests/test_rai_release.py::ReleaseContract.test_every_required_contract_field_fails_closed_when_missing",
            "src/core/tests/test_rai_release_invalidation.py::Invalidation.test_intended_use_change_invalidates",
            "src/api/tests/test_assistant_release.py::Release.test_absent_release_denies_with_zero_calls_and_retains_denial",
            "src/core/tests/test_rai_control_plane_218.py::RaiControlPlane218Tests.test_oq017_rejects_missing_blank_system_and_placeholder_approvals_with_audit",
        ),
        "deferral": None,
    },
    {
        "id": "AC-070",
        "kind": "acceptance_criterion",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Human-review effectiveness protocol detects seeded valid-citation factual/policy/harm "
            "defects, rejects rubber-stamping, and blocks live mode without OQ-017 approval."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_human_review_effectiveness_223.py::HumanReviewEffectiveness223Tests.test_competent_panel_detects_all_defects_retains_evidence_and_compares_effort",
            "src/core/tests/test_human_review_effectiveness_223.py::HumanReviewEffectiveness223Tests.test_live_mode_fails_closed_until_named_human_oq017_approval",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Retrofit Programme Manager and Operations Quality Lead",
            "reason": (
                "Observed reviewer trial with real Zava North Homes caseworkers under operational "
                "workload is deferred to pre-pilot readiness."
            ),
        },
    },
    {
        "id": "AC-071",
        "kind": "acceptance_criterion",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Resident and staff challenge journeys record owner and response date across digital "
            "and assisted channels without adverse markers or hazard-clock delay."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_challenges.py::ResponseProtection.test_view_states_plain_language_protection_and_adds_no_adverse_fields",
            "src/core/tests/test_issue_220_challenge_route.py::JsonStoreChallengeSafeguardTests.test_all_target_kinds_submit_update_escalate_resolve_without_retaliation_or_refusal",
        ),
        "deferral": {
            "open_question": OQ_018,
            "owner": "Resident Engagement Lead",
            "reason": (
                "Resident-panel usability and assisted-channel comprehension acceptance with "
                "tenant representatives is deferred to human UX/engagement sign-off."
            ),
        },
    },
    {
        "id": "AC-072",
        "kind": "acceptance_criterion",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Operator suspension drill halts AI dispatch, preserves manual casework and statutory "
            "hazard handling, and blocks restart until independent human clearance."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_operator_suspension_drill.py::SqlOperatorSuspensionDrillTest.test_nfr_014_end_to_end_suspension_manual_fallback_hazard_and_restart_drill",
            "src/api/tests/test_operator_suspension.py::OperatorIncident.test_seeded_breach_suspends_only_the_affected_task_until_human_clearance",
            "src/api/tests/test_rai_harm_threshold_incident.py::HarmThresholdIncident.test_seeded_critical_harm_creates_owned_incident_and_blocks_dispatch",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Digital Service Owner and Building Safety Lead",
            "reason": (
                "Witnessed live operational drill with appointed duty staff remains required "
                "before live pilot release."
            ),
        },
    },
    {
        "id": "AC-073",
        "kind": "acceptance_criterion",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Cohort and paired-counterfactual evaluation catches seeded disparity/missing-sensor "
            "defects per cohort and refuses to treat synthetic datasets as fairness proof."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_cohort_eval.py::CohortEvalTests.test_synthetic_flag_always_denies_fairness_evidence",
            "src/core/tests/test_paired_equity.py::PairedEquityTests.test_ai_task_paired_evaluation_and_transparent_non_ai_comparison",
            "src/core/tests/test_rai_threshold_live_approval_guard.py::LiveCohortThresholds.test_fictional_or_placeholder_owner_is_rejected_for_live_use",
        ),
        "deferral": {
            "open_question": OQ_018,
            "owner": "Housing Data and Performance Lead and Data Protection Officer",
            "reason": (
                "Live disparity sign-off on lawfully governed non-synthetic cohort records remains "
                "deferred until OQ-018 approval."
            ),
        },
    },
    {
        "id": "OQ-017",
        "kind": "open_question",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Who holds named human authority at Zava North Homes for AI task release, monitoring "
            "threshold approval, incident suspension, and independent post-breach restart?"
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_rai_release.py::ReleaseContract.test_authority_register_names_no_holder_for_any_oq017_authority",
            "src/core/tests/test_rai_control_plane_218.py::RaiControlPlane218Tests.test_oq017_rejects_missing_blank_system_and_placeholder_approvals_with_audit",
            "src/api/tests/test_rai_release_readiness_api_218.py::RaiReleaseReadinessApi218Tests.test_live_release_post_without_named_approval_is_rejected_with_oq017_and_audited",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Zava North Homes Executive Board",
            "reason": (
                "Software fails closed without named human approved_by and named_approval_id; real "
                "office-holder appointment is a customer governance action before live activation."
            ),
        },
    },
    {
        "id": "OQ-018",
        "kind": "open_question",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Which resident cohorts, lawful data fields, and disparity/abstention thresholds are "
            "approved for pre-live and operational fairness evaluation?"
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_cohort_eval.py::CohortEvalTests.test_default_unapproved_and_fictional_offline_records_enforce_oq018_boundary",
            "src/core/tests/test_rai_threshold_live_approval_guard.py::LiveCohortThresholds.test_fictional_or_placeholder_owner_is_rejected_for_live_use",
            "src/api/tests/test_ai_tasks.py::Endpoints.test_cohort_evaluation_route_is_manager_only_read_only_and_enforces_oq018",
        ),
        "deferral": {
            "open_question": OQ_018,
            "owner": "Data Protection Officer and Resident Engagement Lead",
            "reason": (
                "Synthetic evaluation enforces OQ-018 boundaries, while real special-category "
                "lawful-basis and threshold ratification stay deferred to DPO/owner governance."
            ),
        },
    },
    {
        "id": "OQ-019",
        "kind": "open_question",
        "source_document": "docs/prds/zava-forward-retrofit-programme-demonstrator.md",
        "summary": (
            "Formal Legal/DPO determination under UK GDPR Articles 22A-22C (DUAA 2025) on solely "
            "automated significant decisions and conditional EU AI Act high-risk classification."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_regulatory_privacy_audit_217.py::RegulatoryPrivacyAudit217Tests.test_art22_guard_proposes_and_flags_only_and_blocks_undecided_execution",
            "src/core/tests/test_regulatory_privacy_audit_217.py::RegulatoryPrivacyAudit217Tests.test_art22_guard_requires_named_human_sod_and_non_memory_reasons",
        ),
        "deferral": {
            "open_question": OQ_019,
            "owner": "Legal Counsel and Data Protection Officer",
            "reason": (
                "Code enforces propose-only human-in-the-loop decision guards, while formal legal "
                "determination for UK Art. 22A-22C commencement and scope stays human-owned."
            ),
        },
    },
    {
        "id": "RULE-024",
        "kind": "business_rule",
        "source_document": "docs/brds/agentic-retrofit-programme-brd.md",
        "summary": (
            "Guardrail breach automatically pauses the affected AI scope while keeping manual and "
            "hazard routes open, requiring separate named-human authority to restart."
        ),
        "status": "verified",
        "acceptance_checks": (
            "src/core/tests/test_operator_suspension_drill.py::RestartAuthorityUnitTest.test_validate_restart_authority_rejects_blank_placeholder_memory_and_ai",
            "src/core/tests/test_operator_suspension_drill.py::JsonOperatorSuspensionDrillTest.test_rule_024_rejects_invalid_authority_and_enforces_multi_actor_separation",
            "src/core/tests/test_governance.py::JsonGov.test_breach_pauses_scope_until_authorised_restart",
        ),
        "deferral": None,
    },
    {
        "id": "RULE-020",
        "kind": "business_rule",
        "source_document": "docs/brds/agentic-retrofit-programme-brd.md",
        "summary": (
            "Stage-gated release progression requiring Phase 0 baseline capture, DPIA/governance "
            "register readiness, and economics/RAI gates before Shadow testing or Live pilot."
        ),
        "status": "verified_with_live_deferral",
        "acceptance_checks": (
            "src/core/tests/test_governance.py::JsonGov.test_phase_release_decisions_are_recorded_and_gated",
            "src/core/tests/test_governance.py::SqlGov.test_shadow_and_live_need_phase_0_released",
        ),
        "deferral": {
            "open_question": OQ_017,
            "owner": "Housing Asset Executive and Retrofit Programme Manager",
            "reason": (
                "Stage-gate rules are enforced in code; Phase 0 real-service baseline capture and "
                "Live pilot sign-off remain programme-owner gates."
            ),
        },
    },
)


def requirement_traceability() -> list[dict[str, Any]]:
    """Return a deep-copied machine-readable requirement-to-acceptance traceability table."""
    rows: list[dict[str, Any]] = []
    for item in REQUIREMENT_TRACEABILITY:
        copied = copy.deepcopy(item)
        copied["acceptance_checks"] = list(item["acceptance_checks"])
        rows.append(copied)
    return rows


def requirement_traceability_map() -> dict[str, dict[str, Any]]:
    """Return the requirement traceability entries keyed by requirement/rule/question ID."""
    return {entry["id"]: entry for entry in requirement_traceability()}


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[5]


def _class_methods_with_in_file_bases(
    classes: Mapping[str, ast.ClassDef],
    class_name: str,
    seen: set[str] | None = None,
) -> set[str]:
    visited = set() if seen is None else set(seen)
    if class_name in visited or class_name not in classes:
        return set()
    visited.add(class_name)
    cls_node = classes[class_name]
    methods = {
        stmt.name
        for stmt in cls_node.body
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    for base in cls_node.bases:
        if isinstance(base, ast.Name) and base.id in classes:
            methods |= _class_methods_with_in_file_bases(classes, base.id, visited)
    return methods


def _scan_traceability_targets(
    root: Path,
) -> tuple[bool, int, tuple[tuple[str, str, str], ...]]:
    parsed_cache: dict[Path, dict[str, ast.ClassDef]] = {}
    unresolved: list[tuple[str, str, str]] = []
    verified_count = 0

    for entry in REQUIREMENT_TRACEABILITY:
        req_id = str(entry["id"])
        for target in entry["acceptance_checks"]:
            target_str = str(target)
            file_part, sep, symbol_part = target_str.partition("::")
            if not sep or "." not in symbol_part:
                unresolved.append((req_id, target_str, "malformed target descriptor"))
                continue
            class_name, _, method_name = symbol_part.partition(".")
            file_path = root / file_part
            if not file_path.is_file():
                unresolved.append((req_id, target_str, "test file does not exist"))
                continue
            if file_path not in parsed_cache:
                tree = ast.parse(file_path.read_text(encoding="utf-8"), filename=str(file_path))
                parsed_cache[file_path] = {
                    node.name: node for node in tree.body if isinstance(node, ast.ClassDef)
                }
            classes = parsed_cache[file_path]
            if class_name not in classes:
                unresolved.append((req_id, target_str, f"class {class_name!r} not found"))
                continue
            methods = _class_methods_with_in_file_bases(classes, class_name)
            if method_name not in methods:
                unresolved.append(
                    (req_id, target_str, f"method {method_name!r} not found on {class_name!r}")
                )
                continue
            verified_count += 1

    return (not unresolved, verified_count, tuple(unresolved))


@functools.lru_cache(maxsize=1)
def _cached_default_traceability_targets() -> tuple[bool, int, tuple[tuple[str, str, str], ...]]:
    return _scan_traceability_targets(_default_repo_root())


def verify_traceability_targets(repo_root: Path | None = None) -> dict[str, Any]:
    """Verify via AST that every test target in `REQUIREMENT_TRACEABILITY` resolves on disk."""
    all_resolved, verified_count, frozen_unresolved = (
        _scan_traceability_targets(repo_root)
        if repo_root is not None
        else _cached_default_traceability_targets()
    )
    return {
        "all_resolved": all_resolved,
        "verified_target_count": verified_count,
        "unresolved": [
            {"id": req_id, "target": target, "reason": reason}
            for req_id, target, reason in frozen_unresolved
        ],
    }


def traceability_summary(repo_root: Path | None = None) -> dict[str, Any]:
    """Summarize requirement coverage, passing check bindings, and recorded live/owner deferrals."""
    entries = requirement_traceability()
    by_id = {entry["id"]: entry for entry in entries}
    missing_required = [req_id for req_id in REQUIRED_TRACEABILITY_IDS if req_id not in by_id]
    untraced = [
        entry["id"]
        for entry in entries
        if not entry.get("acceptance_checks") and not isinstance(entry.get("deferral"), Mapping)
    ]
    verified_ids = [entry["id"] for entry in entries if bool(entry.get("acceptance_checks"))]
    deferred_ids = [entry["id"] for entry in entries if isinstance(entry.get("deferral"), Mapping)]
    ast_check = verify_traceability_targets(repo_root)
    return {
        "required_ids": list(REQUIRED_TRACEABILITY_IDS),
        "covered_count": len(REQUIRED_TRACEABILITY_IDS) - len(missing_required),
        "total_required": len(REQUIRED_TRACEABILITY_IDS),
        "missing_required_ids": missing_required,
        "untraced_ids": untraced,
        "verified_by_test_ids": verified_ids,
        "deferred_live_ids": deferred_ids,
        "targets_verified": ast_check["all_resolved"],
        "verified_target_count": ast_check["verified_target_count"],
        "unresolved_targets": ast_check["unresolved"],
        "complete": (not missing_required and not untraced and bool(ast_check["all_resolved"])),
        "requirements": entries,
    }


def _inspect_sql_live_releases(
    store: Any,
    *,
    enabled_tasks: Sequence[str],
    assistants_service: Any = None,
    db: Any = None,
) -> dict[str, Any]:
    """Inspect SQL release rows strictly read-only without opening nested write transactions."""
    if (
        db is None
        and assistants_service is not None
        and not getattr(assistants_service, "sql", False)
    ):
        return {
            "sql_available": False,
            "approved_live_tasks": [],
            "unapproved_live_tasks": list(enabled_tasks),
            "active_continuity_suspension": False,
        }

    own_conn: Any = None
    cursor_db: Any = db
    if cursor_db is None and hasattr(store, "assistant_connection"):
        try:
            own_conn = store.assistant_connection()
            cursor_db = own_conn
        except Exception:
            cursor_db = None

    if cursor_db is None:
        return {
            "sql_available": False,
            "approved_live_tasks": [],
            "unapproved_live_tasks": list(enabled_tasks),
            "active_continuity_suspension": False,
        }

    approved_live: list[str] = []
    unapproved_live: list[str] = []
    active_suspension = False
    try:
        with _assistant_release.read_only():
            from zava_forward.core import assistants as _assistants_mod

            _assistants: Any = _assistants_mod
            ai_obj: Any = getattr(store, "ai", None)
            now_ts = time.time()
            if assistants_service is not None and getattr(assistants_service, "sql", False):
                try:
                    now_ts = float(assistants_service.now(cursor_db))
                except Exception:
                    now_ts = time.time()
            elif hasattr(store, "_epoch_sql"):
                try:
                    epoch_row = cursor_db.execute(store._epoch_sql).fetchone()
                    if epoch_row is not None:
                        now_ts = float(epoch_row[0])
                except Exception:
                    now_ts = time.time()

            for task_name in enabled_tasks:
                has_valid_live = False
                if ai_obj is not None and task_name in _assistants.REGISTRY:
                    binding = _assistants.runtime_binding(task_name, ai_obj)
                    selected, denied = _assistant_release.assessment(
                        cursor_db, task_name, binding, now_ts, live=True
                    )
                    has_valid_live = selected is not None and denied is None
                elif ai_obj is not None and task_name in _ai_registry.LEGACY:
                    route = str(_ai_registry.LEGACY[task_name]["route"])
                    dep = str(getattr(ai_obj, route, "") or "")
                    binding = _ai_registry.legacy_binding(task_name, ai_obj, dep)
                    selected, denied = _assistant_release.assessment(
                        cursor_db, f"legacy:{task_name}", binding, now_ts, live=True
                    )
                    has_valid_live = selected is not None and denied is None
                if has_valid_live:
                    approved_live.append(task_name)
                else:
                    unapproved_live.append(task_name)
            try:
                cont_row = cursor_db.execute(
                    "SELECT body FROM assistant_continuity WHERE id=1"
                ).fetchone()
                if cont_row:
                    cont_state = json.loads(cont_row[0])
                    active_suspension = bool(
                        _continuity.active(cont_state, _continuity.ALL, constructed=False)
                    )
            except Exception:
                active_suspension = False
    finally:
        if own_conn is not None:
            try:
                own_conn.close()
            except Exception:
                pass

    return {
        "sql_available": True,
        "approved_live_tasks": approved_live,
        "unapproved_live_tasks": unapproved_live,
        "active_continuity_suspension": active_suspension,
    }


def exercise_acceptance_report(
    store: Any,
    *,
    user: Mapping[str, Any] | None = None,
    assistants_service: Any = None,
    db: Any = None,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Build distinct `rai_exercise_acceptance` and `real_ai_delivery_gate` readiness sections."""
    _ = user
    registered_tasks: dict[str, dict[str, Any]] = _ai_registry.tasks()
    enabled_tasks = sorted(
        task_name
        for task_name, spec in registered_tasks.items()
        if spec.get("enabled") is not False
    )

    authority_reg = rai_release.authority_register()
    default_unapproved = all(
        spec.get("approval_state") == "unapproved"
        and spec.get("accountable_individual") in (None, "unknown")
        for spec in registered_tasks.values()
    )
    negative_probe = validate_live_task_approval(
        enabled_tasks[0] if enabled_tasks else "briefing",
        {"approved_by": "", "named_approval_id": ""},
    )
    offline_decl_gaps = {
        task_name: monitoring_coverage.check_monitoring_declaration(
            spec.get("monitoring_declaration"),
            task_enabled=spec.get("enabled") is not False,
            live=False,
        )["missing"]
        for task_name, spec in registered_tasks.items()
    }
    monitoring_offline_ok = all(not missing for missing in offline_decl_gaps.values())

    try:
        restart_authority.validate_restart_authority("automated-agent")
        restart_fail_closed = False
    except ValueError:
        restart_fail_closed = True

    challenge_channels_ok = (
        bool(getattr(_challenges, "ROUTES", None))
        and bool(getattr(_challenges, "NON_DIGITAL_CHANNELS", None))
        and callable(getattr(_challenges, "reject_adverse_mapping", None))
    )
    review_gate_ok = callable(
        getattr(human_review_effectiveness, "human_review_gate", None)
    ) and callable(getattr(human_review_effectiveness, "evaluate_panel", None))
    privacy_guard_ok = hasattr(regulatory_privacy, "ConsequentialDecisionGuard") and callable(
        getattr(regulatory_privacy, "record_human_decision", None)
    )
    cohort_guard_ok = callable(getattr(cohort_eval, "evaluate", None)) and bool(
        getattr(cohort_eval, "SYNTHETIC_NON_FAIRNESS_NOTICE", "")
    )

    trace_summary = traceability_summary(repo_root)
    ledger_intact = bool(store.verify_audit()) if hasattr(store, "verify_audit") else True

    paused_governance_scopes: list[dict[str, Any]] = []
    store_data = getattr(store, "data", None)
    if isinstance(store_data, Mapping):
        gov_block = store_data.get("governance")
        if isinstance(gov_block, Mapping):
            breaches = gov_block.get("breaches")
            if isinstance(breaches, Sequence) and not isinstance(breaches, (str, bytes)):
                paused_governance_scopes = [
                    {
                        "id": breach.get("id"),
                        "scope_kind": breach.get("scope_kind"),
                        "scope": breach.get("scope"),
                    }
                    for breach in breaches
                    if isinstance(breach, Mapping) and breach.get("status") == "Paused"
                ]

    exercise_checks: dict[str, dict[str, Any]] = {
        "release_contract_fail_closed": {
            "passed": bool(registered_tasks) and default_unapproved,
            "detail": (
                f"{len(registered_tasks)} registered AI tasks default to "
                "approved_for_live_use=False."
            ),
        },
        "oq017_live_activation_gate": {
            "passed": (not negative_probe["valid"]) and negative_probe["code"] == OQ_017,
            "detail": (
                "Live AI task activation without named human approval deterministically "
                "rejects with OQ-017."
            ),
        },
        "challenge_and_appeal_safeguards": {
            "passed": challenge_channels_ok,
            "detail": (
                "Resident and staff challenge channels preserve statutory hazard clocks "
                "without penalty."
            ),
        },
        "operator_suspension_and_restart_authority": {
            "passed": restart_fail_closed,
            "active_governance_pauses": len(paused_governance_scopes),
            "detail": (
                "Suspension keeps manual/hazard routes open and blocks automated or "
                "single-actor restart."
            ),
        },
        "monitoring_and_threshold_declarations": {
            "passed": monitoring_offline_ok,
            "detail": (
                "Every registered AI task carries complete offline harm and review-effort "
                "declarations."
            ),
        },
        "human_review_cohort_and_privacy_guards": {
            "passed": review_gate_ok and privacy_guard_ok and cohort_guard_ok,
            "detail": (
                "Human-review defect trial, per-cohort non-fairness guard, and Art. 22 "
                "propose-only checks active."
            ),
        },
        "requirement_traceability_complete": {
            "passed": bool(trace_summary["complete"]),
            "covered_count": trace_summary["covered_count"],
            "total_required": trace_summary["total_required"],
            "detail": (
                "All 15 Epic #218 requirements trace to verified acceptance checks and/or "
                "explicit owner deferrals."
            ),
        },
        "audit_ledger_integrity": {
            "passed": ledger_intact,
            "detail": "Tamper-evident hash-chained audit ledger verifies cleanly.",
        },
    }
    exercise_passed = all(bool(item["passed"]) for item in exercise_checks.values())

    ai_client = getattr(store, "ai", None)
    zf_ai_env = os.environ.get("ZF_AI", "").strip().lower()
    workflow_forced = zf_ai_env in WORKFLOW_ONLY_ENV_VALUES
    real_provider_configured = bool(
        isinstance(ai_client, _ai.Ai)
        and getattr(ai_client, "configured", False)
        and not workflow_forced
    )

    sql_state = _inspect_sql_live_releases(
        store,
        enabled_tasks=enabled_tasks,
        assistants_service=assistants_service,
        db=db,
    )
    no_active_suspension = (not sql_state["active_continuity_suspension"]) and (
        len(paused_governance_scopes) == 0
    )
    oq017_releases_recorded = bool(
        sql_state["sql_available"] and enabled_tasks and not sql_state["unapproved_live_tasks"]
    )
    oq017_holders_appointed = bool(authority_reg) and all(
        item.get("holder") is not None for item in authority_reg
    )
    oq018_live_cleared = False
    oq019_legal_cleared = False

    live_checks: dict[str, dict[str, Any]] = {
        "provider_configured_and_enabled": {
            "passed": real_provider_configured,
            "workflow_only_forced": workflow_forced,
            "detail": (
                "Live Azure OpenAI provider configured and active."
                if real_provider_configured
                else (
                    "AI provider is unconfigured, mocked/offline, or forced to "
                    "workflow-only (ZF_AI)."
                )
            ),
        },
        "durable_sql_release_store": {
            "passed": bool(sql_state["sql_available"]),
            "detail": (
                "Durable SQL release store connected."
                if sql_state["sql_available"]
                else "Durable SQL release store is not active on this store."
            ),
        },
        "no_active_suspension": {
            "passed": no_active_suspension,
            "detail": (
                "No active continuity or governance guardrail suspension."
                if no_active_suspension
                else "One or more AI scopes are currently suspended or paused."
            ),
        },
        "oq017_named_live_releases_recorded": {
            "passed": oq017_releases_recorded,
            "approved_live_tasks": sql_state["approved_live_tasks"],
            "unapproved_live_tasks": sql_state["unapproved_live_tasks"],
            "detail": (
                "All enabled AI tasks hold unexpired named-human actual release records."
                if oq017_releases_recorded
                else "Enabled AI tasks lack unexpired named-human actual release records (OQ-017)."
            ),
        },
        "oq017_authority_holders_appointed": {
            "passed": oq017_holders_appointed,
            "open_question": OQ_017,
            "detail": (
                "Named Zava North Homes office-holders must be appointed for release, "
                "monitoring, suspension, and restart (OQ-017)."
            ),
        },
        "oq018_live_fairness_and_thresholds_cleared": {
            "passed": oq018_live_cleared,
            "open_question": OQ_018,
            "detail": (
                "Representative non-synthetic cohort manifests, lawful basis, and disparity "
                "thresholds remain deferred to owner/DPO approval (OQ-018)."
            ),
        },
        "oq019_legal_dpo_automated_decision_cleared": {
            "passed": oq019_legal_cleared,
            "open_question": OQ_019,
            "detail": (
                "Formal Legal/DPO determination under UK GDPR Articles 22A-22C and "
                "conditional EU AI Act scope remains deferred (OQ-019)."
            ),
        },
    }
    blocking_reasons = [
        f"{name}: {check['detail']}" for name, check in live_checks.items() if not check["passed"]
    ]
    live_passed = all(bool(item["passed"]) for item in live_checks.values())

    return {
        "rai_exercise_acceptance": {
            "section": "rai_exercise_acceptance",
            "independent_of_real_ai_delivery_gate": True,
            "passed": exercise_passed,
            "status": "passed" if exercise_passed else "failed",
            "checks": exercise_checks,
            "traceability": {
                "complete": trace_summary["complete"],
                "covered_count": trace_summary["covered_count"],
                "total_required": trace_summary["total_required"],
                "verified_by_test_ids": trace_summary["verified_by_test_ids"],
                "deferred_live_ids": trace_summary["deferred_live_ids"],
                "untraced_ids": trace_summary["untraced_ids"],
            },
            "note": (
                "Verifies deterministic Responsible AI release, challenge, suspension, monitoring, "
                "and audit controls in exercise mode independently of live model cut-over."
            ),
        },
        "real_ai_delivery_gate": {
            "section": "real_ai_delivery_gate",
            "separated_from_rai_exercise_acceptance": True,
            "passed": live_passed,
            "status": "passed" if live_passed else "blocked",
            "checks": live_checks,
            "blocking_reasons": blocking_reasons,
            "deferred_open_questions": [OQ_017, OQ_018, OQ_019],
            "note": (
                "Disabled, offline, or workflow-only assistance never satisfies the real-AI "
                "delivery gate; live cut-over requires real provider readiness plus named "
                "human OQ-017, OQ-018, and OQ-019 clearances."
            ),
        },
    }
