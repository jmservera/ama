"""Whole-system data protection register, model-dispatch gate and rights ledger (#121).

Reference-only governance posture: recorded references are not verified DPO or Legal approval, no
legal conclusion or numerical retention schedule is set here, and local deletion never confirms
external model-provider erasure. Constructed fixtures are the only data permitted to reach a model
until qualified owners record the required approvals, and intact uploaded document or image bytes
never reach a model on storage permission alone.
"""

from __future__ import annotations

import calendar
import contextlib
import copy
import json
import os
import re
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from .doc_controls import scan_status

OWNER_ROLES = "DPO and Legal (named owners not yet recorded; issue #121 dependency)"
MANUAL_PATH = "Handle the item manually; a named human decides. No model is used."
GATES = ("LAWFUL_BASIS", "ART9", "RETENTION", "ERASURE", "TRANSFER", "NECESSITY")

SUBJECT_POPULATIONS: tuple[str, ...] = (
    "constructed_resident_fixture",
    "current_staff_identity",
    "current_tenant_identity",
    "current_review_record",
    "future_real_resident",
)

WHOLE_SYSTEM_SURFACES: tuple[str, ...] = (
    "inputs",
    "raw_document_bytes",
    "prompts_outputs_citations",
    "reviewer_identity",
    "audit",
    "telemetry_tokens",
    "provider_processing",
    "provider_retained_copies",
)

HOSTING_REGION_VS_INFERENCE_RESIDENCY: dict[str, Any] = {
    "application_hosting_region": "uksouth",
    "uk_hosting_does_not_prove_uk_inference_residency": True,
    "synthetic_resident_does_not_exempt_actual_staff": True,
    "inference_residency_verified": False,
    "transfer_position_approved": False,
    "note": (
        "UK South application hosting does not establish UK model-inference, "
        "abuse-monitoring reviewer or provider retained-copy residency."
    ),
}
HOSTING_VS_INFERENCE_RESIDENCY = HOSTING_REGION_VS_INFERENCE_RESIDENCY


@dataclass(frozen=True)
class DataClass:
    id: str
    name: str
    kind: str  # constructed | actual
    purpose: str
    audience: str
    storage: str
    special_category: bool = False
    model_bound: bool = False
    needs_derivative: bool = False
    provider_copy: str = "None known; provider terms are unverified"
    subject_population: str = ""
    processing_surfaces: tuple[str, ...] = ()


DATA_CLASSES: tuple[DataClass, ...] = (
    DataClass(
        "fixture_resident",
        "Constructed resident fixtures",
        "constructed",
        "Offline development and demonstration",
        "Developers and demonstration users",
        "Fixture files and demo SQL; entirely constructed",
        model_bound=True,
        subject_population="constructed_resident_fixture",
        processing_surfaces=("inputs", "prompts_outputs_citations"),
    ),
    DataClass(
        "staff_identity",
        "Staff identities and role assignments",
        "actual",
        "Access control and attribution of actions",
        "Administrators and auditors",
        "Entra ID claims, SQL actor columns",
        subject_population="current_staff_identity",
        processing_surfaces=("inputs", "audit", "telemetry_tokens"),
    ),
    DataClass(
        "tenant_identity",
        "Current tenant or representative account identities",
        "actual",
        "Signed-in tenant or representative portal session attribution; excluded from prompts",
        "Authorised case staff and portal session boundary",
        "Session and portal account claims; excluded from model dispatch until approved",
        special_category=True,
        model_bound=True,
        subject_population="current_tenant_identity",
        processing_surfaces=("inputs", "audit"),
    ),
    DataClass(
        "review_record",
        "Reviewer identity and review decisions",
        "actual",
        "Evidence of named human approval",
        "Approvers and auditors",
        "SQL review and approval rows, audit ledger",
        subject_population="current_review_record",
        processing_surfaces=("reviewer_identity", "audit"),
    ),
    DataClass(
        "future_real_resident",
        "Future real resident household and case records",
        "actual",
        "Future live retrofit case coordination once DPO and Legal gates pass",
        "Authorised case staff",
        "Not collected in the demonstrator; blocked until DPO and Legal approvals are recorded",
        special_category=True,
        model_bound=True,
        provider_copy="Blocked until processor, transfer and retention terms are approved",
        subject_population="future_real_resident",
        processing_surfaces=("inputs", "prompts_outputs_citations", "provider_processing"),
    ),
    DataClass(
        "raw_document",
        "Uploaded document and image bytes",
        "actual",
        "Evidence storage for a case",
        "Case staff",
        "Blob storage with scan tags",
        special_category=True,
        model_bound=True,
        needs_derivative=True,
        subject_population="future_real_resident",
        processing_surfaces=("inputs", "raw_document_bytes", "provider_processing"),
    ),
    DataClass(
        "prompt_output",
        "Prompts, outputs and citations",
        "actual",
        "Bounded assistant answers with sources",
        "Signed-in staff",
        "Not stored by Zava except chat threads; provider copy unknown",
        model_bound=True,
        provider_copy="Provider abuse-monitoring and retention terms unknown",
        subject_population="current_staff_identity",
        processing_surfaces=("inputs", "prompts_outputs_citations", "provider_processing"),
    ),
    DataClass(
        "audit_ledger",
        "Audit ledger entries",
        "actual",
        "Tamper-evident record of actions",
        "Auditors",
        "Append-only SQL ledger, digests in Blob with an unlocked immutability policy",
        subject_population="current_staff_identity",
        processing_surfaces=("audit", "reviewer_identity"),
    ),
    DataClass(
        "telemetry",
        "Diagnostics, telemetry and token counts",
        "actual",
        "Operation and metering without content",
        "Operators",
        "Process output, Azure Monitor",
        subject_population="current_staff_identity",
        processing_surfaces=("telemetry_tokens",),
    ),
    DataClass(
        "provider_retained_copy",
        "Model-provider processing and retained copies",
        "actual",
        "External model inference transient processing and unverified provider-retained copies",
        "External processor and authorised assurance owners",
        "External model-provider infrastructure; not controlled by local deletion",
        model_bound=True,
        provider_copy=(
            "Provider abuse-monitoring, diagnostic and stateful retention copies unverified"
        ),
        subject_population="current_staff_identity",
        processing_surfaces=("provider_processing", "provider_retained_copies"),
    ),
)
BY_ID: dict[str, DataClass] = {c.id: c for c in DATA_CLASSES}

# field -> (type, max length_or_int_upper_bound); mirrors regulatory_privacy.QUERY_FIELDS
_TEXT = (str, 80)
_DATE = (str, 10)
_SHORT_EXCERPT = (str, 600)


def _task_spec(
    *,
    purpose: str,
    audience: str,
    necessity: str,
    prohibited: str,
    permitted_fields: dict[str, tuple[type[Any], int]],
) -> dict[str, Any]:
    return dict(
        purpose=purpose,
        audience=audience,
        necessity=necessity,
        prohibited=prohibited,
        permitted_fields=permitted_fields,
        fields=permitted_fields,
    )


TASKS: dict[str, dict[str, Any]] = {
    "rule_lookup": _task_spec(
        purpose="Find a rule card or provision",
        audience="Authorised staff",
        necessity="Source identifiers locate the provision; no resident data is needed",
        prohibited="Names, addresses, health, safeguarding, free text about a person",
        permitted_fields=dict(
            card_id=_TEXT,
            card_version=_TEXT,
            provision_id=_TEXT,
            source_id=_TEXT,
            version=_TEXT,
            as_of=_DATE,
        ),
    ),
    "check_explain": _task_spec(
        purpose="Explain a regulatory check outcome",
        audience="Authorised staff",
        necessity="Check kind and outcome explain the result; case is an opaque id",
        prohibited="Resident names, contact details, special-category data",
        permitted_fields=dict(
            card_id=_TEXT,
            card_version=_TEXT,
            check_kind=_TEXT,
            outcome=_TEXT,
            as_of=_DATE,
            case_id=_TEXT,
        ),
    ),
    "alert_triage": _task_spec(
        purpose="Summarise a regulatory alert",
        audience="Authorised staff",
        necessity="Alert and source identifiers are sufficient",
        prohibited="Any resident data",
        permitted_fields=dict(
            alert_id=_TEXT,
            source_id=_TEXT,
            version=_TEXT,
            status=_TEXT,
            as_of=_DATE,
        ),
    ),
    "agent_chat": _task_spec(
        purpose="Answer a bounded staff case or programme question with cited sources",
        audience="Signed-in authorised staff",
        necessity=(
            "Opaque case and thread identifiers plus bounded structured stage context ground "
            "the answer without raw resident identifiers or special-category notes"
        ),
        prohibited=(
            "Resident names, contact details, unredacted notes, health, safeguarding, "
            "or intact document bytes"
        ),
        permitted_fields=dict(
            case_id=_TEXT,
            thread_id=_TEXT,
            role=_TEXT,
            stage=_TEXT,
            question_topic=(str, 240),
            context_summary=_SHORT_EXCERPT,
            as_of=_DATE,
        ),
    ),
    "look_at_attachment": _task_spec(
        purpose="Summarise an approved reviewed-redacted attachment derivative or scoped excerpt",
        audience="Authorised case, grants and quality staff",
        necessity=(
            "Only a human-reviewed redacted text derivative or explicitly scoped necessity "
            "excerpt with opaque document identifiers is needed to draft a filing summary"
        ),
        prohibited=(
            "Intact document or image bytes, unredacted personal identifiers, health, "
            "safeguarding, or unscoped attachment payloads"
        ),
        permitted_fields=dict(
            case_id=_TEXT,
            doc_id=_TEXT,
            doc_kind=_TEXT,
            derivative=_TEXT,
            redaction_review_id=_TEXT,
            excerpt=_SHORT_EXCERPT,
            as_of=_DATE,
        ),
    ),
    "intake_summary": _task_spec(
        purpose="Draft a bounded intake or aftercare triage summary for human review",
        audience="Authorised housing and resident liaison staff",
        necessity=(
            "Opaque case and concern identifiers, category, stage and bounded summary scope "
            "support staff triage without special-category or raw contact details"
        ),
        prohibited=(
            "Resident names, phone numbers, email addresses, health, disability, "
            "safeguarding, or unredacted free-text notes"
        ),
        permitted_fields=dict(
            case_id=_TEXT,
            concern_id=_TEXT,
            category=_TEXT,
            stage=_TEXT,
            priority_band=_TEXT,
            summary_scope=(str, 240),
            as_of=_DATE,
        ),
    ),
    "case_brief": _task_spec(
        purpose="Draft a bounded handover or morning case brief from structured stage facts",
        audience="Authorised retrofit coordinators and resident liaison officers",
        necessity=(
            "Opaque case id, workflow stage, bounded day/action counts and measure code "
            "enable handover preparation without personal or special-category fields"
        ),
        prohibited=(
            "Resident names, contact details, vulnerability reasons, health, safeguarding, "
            "or raw attachment bytes"
        ),
        permitted_fields=dict(
            case_id=_TEXT,
            stage=_TEXT,
            waiting_days=(int, 3650),
            open_actions=(int, 500),
            measure_code=_TEXT,
            as_of=_DATE,
        ),
    ),
    "read_document": _task_spec(
        purpose="Describe a reviewed-redacted document derivative for filing",
        audience="Authorised case, grants and quality staff",
        necessity=(
            "Opaque case and document identifiers plus a reviewed-redacted derivative excerpt "
            "are sufficient for a non-authoritative filing note"
        ),
        prohibited="Intact uploaded bytes, resident contact details, or special-category data",
        permitted_fields=dict(
            case_id=_TEXT,
            doc_id=_TEXT,
            doc_kind=_TEXT,
            derivative=_TEXT,
            excerpt=_SHORT_EXCERPT,
            as_of=_DATE,
        ),
    ),
    "funding_draft": _task_spec(
        purpose="Draft bounded funding application wording for human review",
        audience="Grants and Evidence Officers and Retrofit Programme Managers",
        necessity="Opaque case, scheme, archetype and measure codes suffice for draft wording",
        prohibited="Resident names, contact details, financial hardship, or health data",
        permitted_fields=dict(
            case_id=_TEXT,
            scheme_code=_TEXT,
            measure_code=_TEXT,
            archetype=_TEXT,
            amount_gbp=(int, 10_000_000),
            as_of=_DATE,
        ),
    ),
    "priority": _task_spec(
        purpose="Explain a deterministic cohort work-order suggestion for human decision",
        audience="Retrofit Coordinators and Retrofit Programme Managers",
        necessity="Opaque case, cohort and deterministic factor codes explain queue position",
        prohibited="Resident names, health, disability, safeguarding, or social-scoring inputs",
        permitted_fields=dict(
            case_id=_TEXT,
            cohort_id=_TEXT,
            rank_band=_TEXT,
            factor_code=_TEXT,
            as_of=_DATE,
        ),
    ),
}

SPECIAL_FIELDS = frozenset(
    {
        "health",
        "disability",
        "ethnicity",
        "religion",
        "safeguarding",
        "vulnerability",
        "notes",
        "adjustment",
        "medical",
        "biometric",
        "genetic",
        "sexual_orientation",
        "trade_union",
        "criminal",
        "hardship",
    }
)


def _is_synthetic_token(value: str) -> bool:
    cleaned = value.strip()
    if cleaned.upper().startswith("SYNTH-"):
        return True
    lowered = cleaned.casefold()
    return lowered in {"synthetic", "placeholder", "mock", "demo", "example"}


def _ref(env: Any, class_id: str, gate: str) -> str:
    if not isinstance(env, Mapping):
        return ""
    return str(env.get(f"DP_{class_id.upper()}_{gate}_REF") or "").strip()


def required_gates(c: DataClass) -> tuple[str, ...]:
    gates = ["LAWFUL_BASIS", "RETENTION", "ERASURE"]
    if c.special_category:
        gates.append("ART9")
    if c.model_bound:
        gates.append("TRANSFER")
    if c.needs_derivative:
        gates.append("NECESSITY")
    return tuple(g for g in GATES if g in gates)


def register_report(env: Any) -> dict[str, Any]:
    """Per class: which approvals are recorded. Never echoes values or claims approval."""
    rows: list[dict[str, Any]] = []
    for c in DATA_CLASSES:
        need = required_gates(c)
        refs = {g: _ref(env, c.id, g) for g in need}
        missing = [g for g, r in refs.items() if not r]
        synthetic = [g for g, r in refs.items() if r and _is_synthetic_token(r)]
        rows.append(
            dict(
                id=c.id,
                name=c.name,
                kind=c.kind,
                subject_population=c.subject_population,
                processing_surfaces=list(c.processing_surfaces),
                purpose=c.purpose,
                audience=c.audience,
                storage=c.storage,
                special_category=c.special_category,
                model_bound=c.model_bound,
                needs_derivative=c.needs_derivative,
                provider_copy=c.provider_copy,
                required=list(need),
                missing=missing,
                synthetic=synthetic,
                references_recorded=c.kind == "actual" and not missing and not synthetic,
                retention="Unknown until Legal sets a period"
                if "RETENTION" in missing or "RETENTION" in synthetic
                else "Reference recorded; period held by owner",
            )
        )
    subject_populations = {
        pop: dict(
            kind="constructed" if pop == "constructed_resident_fixture" else "actual",
            class_ids=[c.id for c in DATA_CLASSES if c.subject_population == pop],
        )
        for pop in SUBJECT_POPULATIONS
    }
    whole_system_coverage = {
        surface: [
            c.id for c in DATA_CLASSES if c.kind == "actual" and surface in c.processing_surfaces
        ]
        for surface in WHOLE_SYSTEM_SURFACES
    }
    return dict(
        label="synthetic-demo",
        owners=OWNER_ROLES,
        dpo_reviewed=False,
        subject_populations=subject_populations,
        population_separation=dict(
            constructed_fixture_classes=[c.id for c in DATA_CLASSES if c.kind == "constructed"],
            actual_personal_data_classes=[c.id for c in DATA_CLASSES if c.kind == "actual"],
        ),
        hosting_region_vs_inference_residency=dict(HOSTING_REGION_VS_INFERENCE_RESIDENCY),
        whole_system_coverage=whole_system_coverage,
        classes=rows,
        statement=(
            "Recorded references are not verified DPO or Legal approval. "
            "UK application hosting does not prove UK model-inference residency. "
            "Local deletion is not provider erasure."
        ),
    )


MODE_ENV = "ZF_DATA_PROCESSING"
APPROVED_DERIVATIVE = "reviewed_redacted"
CONSTRUCTED_DERIVATIVE = "synthetic_safe"
_AUTOMATED_APPROVERS = frozenset(
    {"ai", "model", "assistant", "system", "auto", "automated", "bot", "llm"}
)


def actual_mode(env: Any = None) -> bool:
    mapping = os.environ if env is None else env
    return str(mapping.get(MODE_ENV) or "constructed").strip().lower() != "constructed"


def _is_human_identifier(value: str) -> bool:
    tokens = {tok for tok in re.split(r"[^a-z0-9]+", value.casefold()) if tok}
    return value.casefold() not in _AUTOMATED_APPROVERS and not bool(tokens & _AUTOMATED_APPROVERS)


def _valid_redaction_review(
    redaction_reviewer_id: str | None,
    redaction_review_id: str | None,
) -> tuple[bool, str]:
    if not isinstance(redaction_reviewer_id, str) or not redaction_reviewer_id.strip():
        return (
            False,
            "Reviewed-redacted attachment dispatch requires a named human redaction_reviewer_id",
        )
    reviewer = redaction_reviewer_id.strip()
    if len(reviewer) > 120:
        return False, "redaction_reviewer_id exceeds 120 characters"
    if _is_synthetic_token(reviewer):
        return (
            False,
            "Synthetic redaction_reviewer_id is not valid for attachment model dispatch",
        )
    if not _is_human_identifier(reviewer):
        return (
            False,
            "Reviewed-redacted attachment dispatch requires a human redaction_reviewer_id",
        )
    if not isinstance(redaction_review_id, str) or not redaction_review_id.strip():
        return (
            False,
            "Reviewed-redacted attachment dispatch requires a recorded redaction_review_id",
        )
    review_id = redaction_review_id.strip()
    if len(review_id) > 120:
        return False, "redaction_review_id exceeds 120 characters"
    if _is_synthetic_token(review_id):
        return False, "Synthetic redaction_review_id is not valid for attachment model dispatch"
    return (
        True,
        "Reviewed-redacted derivative recorded; human approval is not verified by this check",
    )


def _valid_scoped_necessity_ref(scoped_necessity_ref: str | None, task: str) -> tuple[bool, str]:
    if not isinstance(scoped_necessity_ref, str) or not scoped_necessity_ref.strip():
        return False, "Scoped necessity approval requires a non-empty scoped_necessity_ref"
    cleaned = scoped_necessity_ref.strip()
    if len(cleaned) > 120:
        return False, "scoped_necessity_ref exceeds 120 characters"
    if cleaned.casefold() in {"*", "all", "any"} or _is_synthetic_token(cleaned):
        return (
            False,
            "Synthetic or wildcard scoped_necessity_ref is not valid for model dispatch",
        )
    if task not in {"look_at_attachment", "read_document"}:
        return (
            False,
            f"Scoped attachment necessity approval is not permitted for task {task}",
        )
    return (
        True,
        "Scoped necessity reference recorded; human approval is not verified by this check",
    )


def validate_necessity_exception(
    exception: Any,
    *,
    task: str = "read_document",
    case_id: str | None = None,
    doc_id: str | None = None,
    actual: bool = False,
    as_of: str | date | datetime | None = None,
) -> dict[str, Any]:
    """Verify whether a human-authorized text-only derivative may be sent to an external model."""
    if not isinstance(exception, Mapping):
        return dict(
            permitted=False,
            reason="Scoped necessity exception must be a recorded object",
            exception=None,
        )

    def _clean_str(key: str, label: str, limit: int) -> tuple[str | None, str | None]:
        val = exception.get(key)
        if not isinstance(val, str) or not val.strip():
            return None, f"Scoped necessity exception requires {label}"
        text = val.strip()
        if len(text) > limit:
            return None, f"Scoped necessity exception {label} exceeds {limit} characters"
        return text, None

    ref_key = "reference" if "reference" in exception else "id"
    reference, err = _clean_str(ref_key, "a reference", 120)
    if err or reference is None:
        return dict(permitted=False, reason=err or "Invalid reference", exception=None)
    if actual and _is_synthetic_token(reference):
        return dict(
            permitted=False,
            reason="Synthetic necessity exception reference is not valid for actual processing",
            exception=None,
        )
    approved_by, err = _clean_str("approved_by", "a named human approver", 120)
    if err or approved_by is None:
        return dict(permitted=False, reason=err or "Invalid approver", exception=None)
    if not _is_human_identifier(approved_by):
        return dict(
            permitted=False,
            reason="Scoped necessity exception requires a named human approver",
            exception=None,
        )
    reason, err = _clean_str("reason", "a necessity reason", 300)
    if err or reason is None:
        return dict(permitted=False, reason=err or "Invalid reason", exception=None)

    raw_scope = exception.get("task") if "task" in exception else exception.get("scope")
    if not isinstance(raw_scope, str) or not raw_scope.strip() or len(raw_scope.strip()) > 80:
        return dict(
            permitted=False,
            reason=f"Scoped necessity exception must specify task {task}",
            exception=None,
        )
    scope_task = raw_scope.strip()
    if scope_task.casefold() in {"*", "all", "any"} or scope_task != task:
        return dict(
            permitted=False,
            reason=f"Scoped necessity exception scope does not match {task}",
            exception=None,
        )

    cleaned: dict[str, str] = dict(
        reference=reference,
        approved_by=approved_by,
        reason=reason,
        task=scope_task,
    )

    raw_case = exception.get("case_id")
    if case_id is not None:
        if not isinstance(raw_case, str) or raw_case.strip() != case_id:
            return dict(
                permitted=False,
                reason="Scoped necessity exception does not match this case",
                exception=None,
            )
        cleaned["case_id"] = raw_case.strip()
    elif raw_case is not None:
        if not isinstance(raw_case, str) or not (1 <= len(raw_case.strip()) <= 80):
            return dict(
                permitted=False,
                reason="Scoped necessity exception case_id is invalid",
                exception=None,
            )
        cleaned["case_id"] = raw_case.strip()

    raw_doc = exception.get("doc_id")
    if doc_id is not None:
        if not isinstance(raw_doc, str) or raw_doc.strip() != doc_id:
            return dict(
                permitted=False,
                reason="Scoped necessity exception does not match this document",
                exception=None,
            )
        cleaned["doc_id"] = raw_doc.strip()
    elif raw_doc is not None:
        if not isinstance(raw_doc, str) or not (1 <= len(raw_doc.strip()) <= 80):
            return dict(
                permitted=False,
                reason="Scoped necessity exception doc_id is invalid",
                exception=None,
            )
        cleaned["doc_id"] = raw_doc.strip()

    raw_exp = exception.get("expires_at")
    if raw_exp is not None and raw_exp != "":
        if not isinstance(raw_exp, str) or len(raw_exp.strip()) < 10 or len(raw_exp.strip()) > 40:
            return dict(
                permitted=False,
                reason="Scoped necessity exception expires_at must be an ISO date",
                exception=None,
            )
        try:
            exp_date = date.fromisoformat(raw_exp.strip()[:10])
            if isinstance(as_of, datetime):
                ref_date = as_of.date()
            elif isinstance(as_of, date):
                ref_date = as_of
            elif isinstance(as_of, str) and as_of.strip():
                ref_date = date.fromisoformat(as_of.strip()[:10])
            else:
                ref_date = datetime.now(UTC).date()
        except ValueError:
            return dict(
                permitted=False,
                reason="Scoped necessity exception expires_at must be an ISO date",
                exception=None,
            )
        if exp_date < ref_date:
            return dict(
                permitted=False,
                reason="Scoped necessity exception has expired",
                exception=None,
            )
        cleaned["expires_at"] = raw_exp.strip()

    return dict(
        permitted=True,
        reason="Scoped necessity exception recorded; human approval is not verified by this check",
        exception=cleaned,
    )


def _dispatch_decision(
    permitted: bool,
    reason: str,
    *,
    user_permission_granted: bool,
    storage_permission_granted: bool,
    approval_basis: str = "denied_manual_only",
) -> dict[str, Any]:
    return dict(
        permitted=permitted,
        reason=reason,
        manual_path=MANUAL_PATH,
        user_permission_granted=bool(user_permission_granted),
        user_permission_establishes_necessity=False,
        storage_permission_granted=bool(storage_permission_granted),
        storage_approves_ai_dispatch=False,
        approval_basis=approval_basis if permitted else "denied_manual_only",
    )


def model_dispatch(
    class_id: str,
    env: Any,
    derivative: str | None = None,
    *,
    necessity_exception: Any = None,
    scoped_necessity_ref: str | None = None,
    redaction_reviewer_id: str | None = None,
    redaction_review_id: str | None = None,
    user_permission_granted: bool = False,
    storage_permission_granted: bool = False,
    payload: Mapping[str, Any] | None = None,
    task: str = "read_document",
    case_id: str | None = None,
    doc_id: str | None = None,
    as_of: str | date | datetime | None = None,
) -> dict[str, Any]:
    """Deny model dispatch until references, task necessity and derivative checks pass."""
    c = BY_ID.get(class_id)
    if c is None:
        return _dispatch_decision(
            False,
            "Unknown data class",
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
        )
    if task not in TASKS:
        return _dispatch_decision(
            False,
            (
                f"Task {task!r} is not declared in the minimum-necessary task manifest; "
                "user permission never establishes task necessity"
            ),
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
        )
    if payload is not None:
        checked = validate_task_payload(
            task, payload, user_permission_granted=user_permission_granted
        )
        disallowed = checked["special_category_dropped"] + checked["rejected"] + checked["dropped"]
        if not checked["permitted"] or disallowed:
            detail = (
                "disallowed or invalid payload fields (" + ", ".join(disallowed) + ")"
                if disallowed
                else checked["reason"]
            )
            return _dispatch_decision(
                False,
                f"Task payload failed minimum-necessary validation: {detail}",
                user_permission_granted=user_permission_granted,
                storage_permission_granted=storage_permission_granted,
            )
    if c.kind == "constructed":
        return _dispatch_decision(
            True,
            "Entirely constructed fixture; no actual processing",
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
            approval_basis="constructed_fixture",
        )
    if not c.model_bound:
        return _dispatch_decision(
            False,
            "This class is never sent to a model",
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
        )
    need = required_gates(c)
    bad = [g for g in need if not _ref(env, c.id, g) or _is_synthetic_token(_ref(env, c.id, g))]
    if bad:
        return _dispatch_decision(
            False,
            "Approvals not recorded: " + ", ".join(bad),
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
        )
    if c.needs_derivative:
        deriv = derivative.strip() if isinstance(derivative, str) else None
        if deriv == CONSTRUCTED_DERIVATIVE:
            return _dispatch_decision(
                False,
                (
                    "Synthetic derivative marker is not valid for actual processing; "
                    "use a reviewed, redacted derivative"
                ),
                user_permission_granted=user_permission_granted,
                storage_permission_granted=storage_permission_granted,
            )
        if deriv == APPROVED_DERIVATIVE:
            require_review_pair = (
                task == "look_at_attachment"
                or redaction_reviewer_id is not None
                or redaction_review_id is not None
            )
            if require_review_pair:
                ok, rev_reason = _valid_redaction_review(redaction_reviewer_id, redaction_review_id)
                if not ok:
                    return _dispatch_decision(
                        False,
                        rev_reason,
                        user_permission_granted=user_permission_granted,
                        storage_permission_granted=storage_permission_granted,
                    )
                return _dispatch_decision(
                    True,
                    rev_reason,
                    user_permission_granted=user_permission_granted,
                    storage_permission_granted=storage_permission_granted,
                    approval_basis="reviewed_redacted",
                )
            return _dispatch_decision(
                True,
                "References recorded; human approval is not verified by this check",
                user_permission_granted=user_permission_granted,
                storage_permission_granted=storage_permission_granted,
                approval_basis="reviewed_redacted",
            )
        if deriv not in (None, "", "intact", "raw"):
            return _dispatch_decision(
                False,
                (
                    f"Unrecognised derivative marker {deriv!r}; "
                    "intact or unreviewed material is not sent"
                ),
                user_permission_granted=user_permission_granted,
                storage_permission_granted=storage_permission_granted,
            )
        if necessity_exception is not None:
            exc = validate_necessity_exception(
                necessity_exception,
                task=task,
                case_id=case_id,
                doc_id=doc_id,
                actual=True,
                as_of=as_of,
            )
            return _dispatch_decision(
                bool(exc["permitted"]),
                str(exc["reason"]),
                user_permission_granted=user_permission_granted,
                storage_permission_granted=storage_permission_granted,
                approval_basis="necessity_exception",
            )
        if scoped_necessity_ref is not None:
            ok, scope_reason = _valid_scoped_necessity_ref(scoped_necessity_ref, task)
            return _dispatch_decision(
                ok,
                scope_reason,
                user_permission_granted=user_permission_granted,
                storage_permission_granted=storage_permission_granted,
                approval_basis="scoped_necessity_ref",
            )
        return _dispatch_decision(
            False,
            (
                "Intact material is not sent; upload, storage or download permission does not "
                "approve AI dispatch. Use a reviewed, redacted derivative or scoped necessity "
                "approval"
            ),
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
        )
    return _dispatch_decision(
        True,
        "References recorded; human approval is not verified by this check",
        user_permission_granted=user_permission_granted,
        storage_permission_granted=storage_permission_granted,
        approval_basis="recorded_class_references",
    )


def dispatch_attachment_to_model(
    env: Mapping[str, str] | None = None,
    *,
    derivative: str | None = None,
    redaction_reviewer_id: str | None = None,
    redaction_review_id: str | None = None,
    scoped_necessity_ref: str | None = None,
    necessity_exception: Any = None,
    storage_permission_granted: bool = False,
    upload_permitted: bool = False,
    download_permitted: bool = False,
    user_permission_granted: bool = False,
    payload: Mapping[str, Any] | None = None,
    task: str = "look_at_attachment",
    case_id: str | None = None,
    doc_id: str | None = None,
    as_of: str | date | datetime | None = None,
) -> dict[str, Any]:
    """Gate sending attachment material to AI: storage permission never authorizes intact bytes."""
    mapping: Mapping[str, str] = os.environ if env is None else env
    any_storage = bool(storage_permission_granted or upload_permitted or download_permitted)
    deriv_clean = derivative.strip() if isinstance(derivative, str) else None
    if deriv_clean == APPROVED_DERIVATIVE:
        ok, rev_reason = _valid_redaction_review(redaction_reviewer_id, redaction_review_id)
        if not ok:
            return _dispatch_decision(
                False,
                rev_reason,
                user_permission_granted=user_permission_granted,
                storage_permission_granted=any_storage,
            )
    return model_dispatch(
        "raw_document",
        mapping,
        derivative,
        necessity_exception=necessity_exception,
        scoped_necessity_ref=scoped_necessity_ref,
        redaction_reviewer_id=redaction_reviewer_id,
        redaction_review_id=redaction_review_id,
        user_permission_granted=user_permission_granted,
        storage_permission_granted=any_storage,
        payload=payload,
        task=task,
        case_id=case_id,
        doc_id=doc_id,
        as_of=as_of,
    )


def dispatch_hold(
    class_id: str,
    env: Any,
    derivative: str | None = None,
    *,
    necessity_exception: Any = None,
    scoped_necessity_ref: str | None = None,
    redaction_reviewer_id: str | None = None,
    redaction_review_id: str | None = None,
    user_permission_granted: bool = False,
    storage_permission_granted: bool = False,
    payload: Mapping[str, Any] | None = None,
    task: str = "read_document",
    case_id: str | None = None,
    doc_id: str | None = None,
    as_of: str | date | datetime | None = None,
) -> str | None:
    """Reason a model call must not happen, or None. Unset or "constructed" means constructed only.

    Any other value is treated as actual processing, so a typo fails closed.
    """
    if not actual_mode(env):
        return None
    d = model_dispatch(
        class_id,
        env,
        derivative,
        necessity_exception=necessity_exception,
        scoped_necessity_ref=scoped_necessity_ref,
        redaction_reviewer_id=redaction_reviewer_id,
        redaction_review_id=redaction_review_id,
        user_permission_granted=user_permission_granted,
        storage_permission_granted=storage_permission_granted,
        payload=payload,
        task=task,
        case_id=case_id,
        doc_id=doc_id,
        as_of=as_of,
    )
    if d["permitted"]:
        return None
    return f"{d['reason']}. {d['manual_path']}"


def document_model_hold(
    doc: Mapping[str, Any] | None = None,
    env: Any = None,
    *,
    case_id: str | None = None,
    doc_id: str | None = None,
    derivative: str | None = None,
    necessity_exception: Any = None,
    scoped_necessity_ref: str | None = None,
    redaction_reviewer_id: str | None = None,
    redaction_review_id: str | None = None,
    user_permission_granted: bool = False,
    storage_permission_granted: bool = False,
    payload: Mapping[str, Any] | None = None,
    task: str = "read_document",
    resident_consent: str | None = None,
    as_of: str | date | datetime | None = None,
) -> str | None:
    """Reason document AI processing must not run, or None when permitted."""
    mapping = os.environ if env is None else env
    if resident_consent is not None:
        if str(resident_consent).strip().lower() not in ("given", "granted"):
            return f"Resident AI data-use consent is not granted. {MANUAL_PATH}"
    doc_map = doc if isinstance(doc, Mapping) else {}
    resolved_doc_id = (
        doc_id if doc_id is not None else (str(doc_map["id"]) if doc_map.get("id") else None)
    )
    has_explicit_derivative = (
        derivative is not None or "ai_derivative" in doc_map or "derivative" in doc_map
    )
    raw_deriv = (
        derivative
        if derivative is not None
        else (
            doc_map.get("ai_derivative")
            if "ai_derivative" in doc_map
            else doc_map.get("derivative")
        )
    )
    deriv = str(raw_deriv).strip() if isinstance(raw_deriv, str) and raw_deriv.strip() else None
    exc_obj = (
        necessity_exception
        if necessity_exception is not None
        else doc_map.get("necessity_exception")
    )
    requires_deriv = bool(doc_map.get("requires_derivative"))
    is_uploaded_doc = isinstance(doc, Mapping) and doc.get("generated") is False
    if (
        isinstance(doc, Mapping)
        and not doc.get("generated")
        and ("scan" in doc or "scan_status" in doc)
        and scan_status(doc) != "clean"
    ):
        return (
            f"Document has not passed the content scan and cannot be sent to a model. {MANUAL_PATH}"
        )
    is_actual = actual_mode(mapping)
    if is_actual:
        return dispatch_hold(
            "raw_document",
            mapping,
            deriv,
            necessity_exception=exc_obj,
            scoped_necessity_ref=scoped_necessity_ref,
            redaction_reviewer_id=redaction_reviewer_id,
            redaction_review_id=redaction_review_id,
            user_permission_granted=user_permission_granted,
            storage_permission_granted=storage_permission_granted,
            payload=payload,
            task=task,
            case_id=case_id,
            doc_id=resolved_doc_id,
            as_of=as_of,
        )
    if (
        is_uploaded_doc
        or has_explicit_derivative
        or requires_deriv
        or exc_obj is not None
        or scoped_necessity_ref is not None
    ):
        if deriv in {APPROVED_DERIVATIVE, CONSTRUCTED_DERIVATIVE}:
            if deriv == APPROVED_DERIVATIVE and (
                task == "look_at_attachment"
                or redaction_reviewer_id is not None
                or redaction_review_id is not None
            ):
                ok, rev_reason = _valid_redaction_review(redaction_reviewer_id, redaction_review_id)
                if not ok:
                    return f"{rev_reason}. {MANUAL_PATH}"
            return None
        if exc_obj is not None:
            exc = validate_necessity_exception(
                exc_obj,
                task=task,
                case_id=case_id,
                doc_id=resolved_doc_id,
                actual=False,
                as_of=as_of,
            )
            if exc["permitted"]:
                return None
            return f"{exc['reason']}. {MANUAL_PATH}"
        if scoped_necessity_ref is not None:
            ok, scope_reason = _valid_scoped_necessity_ref(scoped_necessity_ref, task)
            if ok:
                return None
            return f"{scope_reason}. {MANUAL_PATH}"
        return (
            "Intact material is not sent; use a reviewed, redacted derivative or "
            f"a scoped necessity exception. {MANUAL_PATH}"
        )
    return None


def _field_value_valid(value: Any, kind: type[Any], limit: int) -> bool:
    if kind is int:
        return type(value) is int and 0 <= value <= limit
    if kind is str:
        return isinstance(value, str) and len(value) <= limit
    return isinstance(value, kind)


def validate_task_payload(
    task: str,
    payload: Mapping[str, Any],
    *,
    user_permission_granted: bool = False,
) -> dict[str, Any]:
    """Keep only declared fields of declared type and bound; permission never establishes need."""
    spec = TASKS.get(task)
    if spec is None:
        return dict(
            permitted=False,
            reason="Task is not declared in the minimum-necessary task manifest",
            fields={},
            dropped=[],
            rejected=[],
            special_category_dropped=[],
            user_permission_granted=bool(user_permission_granted),
            user_permission_establishes_necessity=False,
            manual_path=MANUAL_PATH,
        )
    permitted_fields: Mapping[str, tuple[type[Any], int]] = spec["permitted_fields"]
    kept: dict[str, Any] = {}
    rejected: list[str] = []
    for name, (kind, limit) in permitted_fields.items():
        if name not in payload:
            continue
        if name in SPECIAL_FIELDS:
            rejected.append(name)
            continue
        value = payload[name]
        if _field_value_valid(value, kind, limit):
            kept[name] = value
        else:
            rejected.append(name)
    dropped = sorted(k for k in payload if k not in permitted_fields)
    special_dropped = sorted(k for k in payload if k in SPECIAL_FIELDS)
    permitted = bool(kept)
    reason = (
        "Permitted minimum-necessary fields retained; undeclared and special-category "
        "fields stripped"
        if permitted
        else (
            "Payload contains no valid permitted fields; "
            "user permission never establishes task necessity"
        )
    )
    return dict(
        permitted=permitted,
        reason=reason,
        fields=kept,
        rejected=sorted(rejected),
        dropped=dropped,
        special_category_dropped=special_dropped,
        purpose=spec["purpose"],
        audience=spec["audience"],
        necessity=spec["necessity"],
        prohibited=spec["prohibited"],
        user_permission_granted=bool(user_permission_granted),
        user_permission_establishes_necessity=False,
        manual_path=MANUAL_PATH,
    )


def due_date(received: datetime) -> datetime:
    """One calendar month after receipt, clamped to month end. Extensions are a DPO decision."""
    if received.tzinfo is None or received.utcoffset() is None:
        raise ValueError("Rights request time needs a timezone.")
    month = received.month % 12 + 1
    year = received.year + (received.month == 12)
    day = min(received.day, calendar.monthrange(year, month)[1])
    return received.replace(year=year, month=month, day=day)


RIGHTS_KINDS: tuple[str, ...] = (
    "access",
    "rectification",
    "erasure",
    "restriction",
    "objection",
    "portability",
)
RIGHTS_ACTIONS: tuple[str, ...] = ("locate", "export", "erase")
RIGHTS_LEDGER_SCHEMA = "rights-request-ledger-v1"
PROVIDER_ERASURE_NOTE = (
    "Local record deletion affects Zava Forward storage only and never confirms erasure "
    "of external model-provider transient or retained copies."
)


@runtime_checkable
class _RightsStoreProtocol(Protocol):
    data: dict[str, Any]

    def save(self) -> None: ...


def _parse_aware_datetime(value: str | datetime, label: str) -> datetime:
    dt = datetime.fromisoformat(value) if isinstance(value, str) else value
    if not isinstance(dt, datetime) or dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(f"{label} needs a timezone.")
    return dt


def _clean_identifier(value: str, label: str, limit: int = 120) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string.")
    cleaned = value.strip()
    if len(cleaned) > limit:
        raise ValueError(f"{label} exceeds {limit} characters.")
    return cleaned


def _reject_provider_erasure_claim(provider_erasure_confirmed: bool) -> None:
    if provider_erasure_confirmed is not False:
        raise ValueError(
            "provider_erasure_confirmed cannot be set True locally; local deletion never confirms "
            "external model-provider erasure."
        )


def _normalize_rights_row(raw: Mapping[str, Any]) -> dict[str, Any]:
    if bool(raw.get("provider_erasure_confirmed", False)):
        raise ValueError(
            "Rights ledger cannot load a record claiming confirmed provider erasure "
            "from local state."
        )
    req_id = _clean_identifier(str(raw.get("request_id") or raw.get("id") or ""), "request_id")
    kind = _clean_identifier(str(raw.get("kind") or ""), "kind", 40)
    if kind not in RIGHTS_KINDS:
        raise ValueError(f"Unsupported rights request kind: {kind!r}")
    received_dt = _parse_aware_datetime(str(raw["received_at"]), "received_at")
    due_dt = (
        _parse_aware_datetime(str(raw["due_at"]), "due_at")
        if raw.get("due_at")
        else due_date(received_dt)
    )
    answered_raw = raw.get("answered_at")
    answered_iso: str | None = None
    within_one_month: bool | None = None
    if answered_raw is not None and answered_raw != "":
        answered_dt = _parse_aware_datetime(str(answered_raw), "answered_at")
        if answered_dt < received_dt:
            raise ValueError("answered_at cannot precede received_at.")
        answered_iso = answered_dt.isoformat()
        within_one_month = answered_dt.date() <= due_dt.date()
    local_deleted = bool(raw.get("local_deleted", False))
    actions_raw = raw.get("actions")
    actions: list[dict[str, Any]] = []
    if isinstance(actions_raw, Sequence) and not isinstance(actions_raw, (str, bytes)):
        for entry in actions_raw:
            if not isinstance(entry, Mapping):
                raise ValueError("Rights request action entry must be a mapping.")
            if bool(entry.get("provider_erasure_confirmed", False)):
                raise ValueError("Action entry cannot claim confirmed provider erasure locally.")
            act_kind = _clean_identifier(str(entry.get("action") or ""), "action", 30)
            if act_kind not in RIGHTS_ACTIONS:
                raise ValueError(f"Unsupported rights action: {act_kind!r}")
            act_at = _parse_aware_datetime(str(entry["at"]), "action timestamp")
            actions.append(
                dict(
                    action=act_kind,
                    actor=_clean_identifier(str(entry.get("actor") or "staff"), "actor"),
                    at=act_at.isoformat(),
                    target_scope=_clean_identifier(
                        str(entry.get("target_scope") or "local_store"), "target_scope"
                    ),
                    record_count=int(entry.get("record_count", 0)),
                    local_deleted=bool(entry.get("local_deleted", False)),
                    provider_erasure_confirmed=False,
                    audit_retained_reason=(
                        str(entry["audit_retained_reason"]).strip()
                        if entry.get("audit_retained_reason")
                        else None
                    ),
                )
            )
    return dict(
        id=req_id,
        request_id=req_id,
        kind=kind,
        subject_key=str(raw.get("subject_key") or "").strip(),
        subject_population=str(raw.get("subject_population") or "current_staff_identity").strip(),
        received_at=received_dt.isoformat(),
        due_at=due_dt.isoformat(),
        recorded_by=str(raw.get("recorded_by") or "staff").strip(),
        notes_ref=str(raw.get("notes_ref") or "").strip(),
        actions=actions,
        answered_at=answered_iso,
        answered_by=str(raw["answered_by"]).strip() if raw.get("answered_by") else None,
        outcome=str(raw["outcome"]).strip() if raw.get("outcome") else None,
        summary_ref=str(raw.get("summary_ref") or "").strip(),
        within_one_month=within_one_month,
        local_deleted=local_deleted,
        provider_erasure_confirmed=False,
        provider_erasure_status=(
            "local_deleted_only_provider_erasure_unconfirmed"
            if local_deleted
            else "unverified_external_processor"
        ),
        audit_retention_refusal=(
            str(raw["audit_retention_refusal"]).strip()
            if raw.get("audit_retention_refusal")
            else None
        ),
    )


class RightsRequestLedger:
    """Persisted store-backed or JSON-serializable statutory rights-request workflow (#121)."""

    def __init__(
        self,
        store: _RightsStoreProtocol | None = None,
        *,
        path: str | os.PathLike[str] | None = None,
        initial: Sequence[Mapping[str, Any]] | None = None,
    ) -> None:
        if store is not None and path is not None:
            raise ValueError("Specify either store or path for RightsRequestLedger, not both.")
        self._store: _RightsStoreProtocol | None = store
        self._path: Path | None = Path(path) if path is not None else None
        self._rows: list[dict[str, Any]] = [_normalize_rights_row(r) for r in (initial or ())]
        if self._path is not None and self._path.exists() and initial is None:
            self._rows = self._read_path_rows()

    @property
    def is_persisted(self) -> bool:
        return self._store is not None or self._path is not None

    @contextlib.contextmanager
    def _locked(self) -> Iterator[None]:
        lock_obj = getattr(self._store, "lock", None) if self._store is not None else None
        if lock_obj is not None:
            with lock_obj:
                yield
        else:
            yield

    def _read_path_rows(self) -> list[dict[str, Any]]:
        assert self._path is not None
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        items = raw.get("requests", []) if isinstance(raw, Mapping) else raw
        if not isinstance(items, list):
            raise ValueError("Serialized rights-request ledger must contain a requests list.")
        return [_normalize_rights_row(item) for item in items]

    def _load_unlocked(self) -> list[dict[str, Any]]:
        if self._store is not None:
            stored = self._store.data.get("rights_requests")
            if stored is None:
                return []
            if not isinstance(stored, list):
                raise ValueError("store.data['rights_requests'] must be a list.")
            return [_normalize_rights_row(item) for item in stored]
        if self._path is not None and self._path.exists():
            self._rows = self._read_path_rows()
        return [copy.deepcopy(r) for r in self._rows]

    def _serialize_rows(self, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
        normalized = [_normalize_rights_row(r) for r in rows]
        return dict(
            schema=RIGHTS_LEDGER_SCHEMA,
            provider_erasure_confirmed=False,
            note=PROVIDER_ERASURE_NOTE,
            requests=normalized,
        )

    def _commit_unlocked(
        self,
        rows: list[dict[str, Any]],
        *,
        actor: str,
        audit_action: str,
        audit_detail: str,
    ) -> None:
        normalized = [_normalize_rights_row(r) for r in rows]
        self._rows = [copy.deepcopy(r) for r in normalized]
        if self._store is not None:
            self._store.data["rights_requests"] = [copy.deepcopy(r) for r in normalized]
            audit_fn = getattr(self._store, "audit", None)
            if hasattr(self._store, "db"):
                if callable(audit_fn):
                    audit_fn(actor, audit_action, "-", audit_detail)
                self._store.save()
            else:
                self._store.save()
                if callable(audit_fn):
                    audit_fn(actor, audit_action, "-", audit_detail)
            return
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(self._path.suffix + ".tmp")
            payload = self._serialize_rows(normalized)
            tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
            os.replace(tmp, self._path)

    def requests(self) -> list[dict[str, Any]]:
        with self._locked():
            return self._load_unlocked()

    def get(self, request_id: str) -> dict[str, Any]:
        req_id = _clean_identifier(request_id, "request_id")
        with self._locked():
            for row in self._load_unlocked():
                if row["request_id"] == req_id:
                    return row
        raise KeyError(f"Unknown rights request: {req_id}")

    def record_request(
        self,
        *,
        request_id: str,
        kind: str,
        subject_key: str,
        received_at: str | datetime,
        actor: str = "staff",
        subject_population: str = "current_staff_identity",
        notes_ref: str = "",
    ) -> dict[str, Any]:
        req_id = _clean_identifier(request_id, "request_id")
        if _is_synthetic_token(req_id):
            raise ValueError("Synthetic request_id is not valid for rights ledger records.")
        clean_kind = _clean_identifier(kind, "kind", 40)
        if clean_kind not in RIGHTS_KINDS:
            raise ValueError(f"Unsupported rights request kind: {clean_kind!r}")
        subj = _clean_identifier(subject_key, "subject_key", 160)
        clean_actor = _clean_identifier(actor, "actor")
        if _is_synthetic_token(clean_actor) or not _is_human_identifier(clean_actor):
            raise ValueError("Rights ledger actor must be a non-synthetic human identifier.")
        if subject_population not in SUBJECT_POPULATIONS:
            raise ValueError(f"Unsupported subject_population: {subject_population!r}")
        received_dt = _parse_aware_datetime(received_at, "received_at")
        due_dt = due_date(received_dt)
        clean_notes = notes_ref.strip()
        if len(clean_notes) > 200:
            raise ValueError("notes_ref exceeds 200 characters.")
        with self._locked():
            rows = self._load_unlocked()
            if any(r["request_id"] == req_id for r in rows):
                raise ValueError(f"Rights request {req_id!r} already exists.")
            record = _normalize_rights_row(
                dict(
                    id=req_id,
                    request_id=req_id,
                    kind=clean_kind,
                    subject_key=subj,
                    subject_population=subject_population,
                    received_at=received_dt.isoformat(),
                    due_at=due_dt.isoformat(),
                    recorded_by=clean_actor,
                    notes_ref=clean_notes,
                    actions=[],
                    answered_at=None,
                    answered_by=None,
                    outcome=None,
                    summary_ref="",
                    local_deleted=False,
                    provider_erasure_confirmed=False,
                    audit_retention_refusal=None,
                )
            )
            rows.append(record)
            self._commit_unlocked(
                rows,
                actor=clean_actor,
                audit_action="rights.request.recorded",
                audit_detail=(
                    f"request_id={req_id} kind={clean_kind} "
                    f"population={subject_population} due_at={due_dt.date().isoformat()}"
                ),
            )
            return copy.deepcopy(record)

    def log_action(
        self,
        request_id: str,
        *,
        action: str,
        actor: str,
        at: str | datetime,
        target_scope: str = "local_store",
        record_count: int = 0,
        local_deleted: bool = False,
        provider_erasure_confirmed: bool = False,
        audit_retained_reason: str | None = None,
    ) -> dict[str, Any]:
        _reject_provider_erasure_claim(provider_erasure_confirmed)
        req_id = _clean_identifier(request_id, "request_id")
        clean_action = _clean_identifier(action, "action", 30)
        if clean_action not in RIGHTS_ACTIONS:
            raise ValueError(f"Unsupported rights action: {clean_action!r}")
        clean_actor = _clean_identifier(actor, "actor")
        if _is_synthetic_token(clean_actor) or not _is_human_identifier(clean_actor):
            raise ValueError("Rights ledger actor must be a non-synthetic human identifier.")
        clean_scope = _clean_identifier(target_scope, "target_scope")
        if type(record_count) is not int or record_count < 0:
            raise ValueError("record_count must be a non-negative int.")
        if local_deleted and clean_action != "erase":
            raise ValueError("local_deleted=True is valid only on an 'erase' action.")
        at_dt = _parse_aware_datetime(at, "action timestamp")
        retained_reason = (
            _clean_identifier(audit_retained_reason, "audit_retained_reason", 240)
            if audit_retained_reason
            else None
        )
        with self._locked():
            rows = self._load_unlocked()
            target: dict[str, Any] | None = None
            for row in rows:
                if row["request_id"] == req_id:
                    target = row
                    break
            if target is None:
                raise KeyError(f"Unknown rights request: {req_id}")
            received_dt = _parse_aware_datetime(target["received_at"], "received_at")
            if at_dt < received_dt:
                raise ValueError("Rights action timestamp cannot precede received_at.")
            entry: dict[str, Any] = dict(
                action=clean_action,
                actor=clean_actor,
                at=at_dt.isoformat(),
                target_scope=clean_scope,
                record_count=record_count,
                local_deleted=bool(local_deleted),
                provider_erasure_confirmed=False,
                audit_retained_reason=retained_reason,
            )
            target["actions"].append(entry)
            if local_deleted:
                target["local_deleted"] = True
                target["provider_erasure_confirmed"] = False
                target["provider_erasure_status"] = (
                    "local_deleted_only_provider_erasure_unconfirmed"
                )
            if retained_reason:
                target["audit_retention_refusal"] = retained_reason
            updated = _normalize_rights_row(target)
            for idx, existing in enumerate(rows):
                if existing["request_id"] == req_id:
                    rows[idx] = updated
                    break
            self._commit_unlocked(
                rows,
                actor=clean_actor,
                audit_action=f"rights.action.{clean_action}",
                audit_detail=(
                    f"request_id={req_id} scope={clean_scope} count={record_count} "
                    f"local_deleted={bool(updated['local_deleted'])} "
                    "provider_erasure_confirmed=False"
                ),
            )
            return copy.deepcopy(updated)

    def answer_request(
        self,
        request_id: str,
        *,
        answered_at: str | datetime,
        actor: str,
        outcome: str = "completed",
        summary_ref: str = "",
        local_deleted: bool | None = None,
        provider_erasure_confirmed: bool = False,
        audit_retention_refusal: str | None = None,
    ) -> dict[str, Any]:
        _reject_provider_erasure_claim(provider_erasure_confirmed)
        req_id = _clean_identifier(request_id, "request_id")
        clean_actor = _clean_identifier(actor, "actor")
        if _is_synthetic_token(clean_actor) or not _is_human_identifier(clean_actor):
            raise ValueError("Rights ledger actor must be a non-synthetic human identifier.")
        clean_outcome = _clean_identifier(outcome, "outcome", 60)
        answered_dt = _parse_aware_datetime(answered_at, "answered_at")
        clean_summary = summary_ref.strip()
        if len(clean_summary) > 200:
            raise ValueError("summary_ref exceeds 200 characters.")
        retained_reason = (
            _clean_identifier(audit_retention_refusal, "audit_retention_refusal", 240)
            if audit_retention_refusal
            else None
        )
        with self._locked():
            rows = self._load_unlocked()
            target: dict[str, Any] | None = None
            for row in rows:
                if row["request_id"] == req_id:
                    target = row
                    break
            if target is None:
                raise KeyError(f"Unknown rights request: {req_id}")
            received_dt = _parse_aware_datetime(target["received_at"], "received_at")
            if answered_dt < received_dt:
                raise ValueError("answered_at cannot precede received_at.")
            target["answered_at"] = answered_dt.isoformat()
            target["answered_by"] = clean_actor
            target["outcome"] = clean_outcome
            target["summary_ref"] = clean_summary
            if local_deleted is not None:
                target["local_deleted"] = bool(local_deleted)
            target["provider_erasure_confirmed"] = False
            if retained_reason:
                target["audit_retention_refusal"] = retained_reason
            updated = _normalize_rights_row(target)
            for idx, existing in enumerate(rows):
                if existing["request_id"] == req_id:
                    rows[idx] = updated
                    break
            self._commit_unlocked(
                rows,
                actor=clean_actor,
                audit_action="rights.request.answered",
                audit_detail=(
                    f"request_id={req_id} outcome={clean_outcome} "
                    f"within_one_month={updated['within_one_month']} "
                    f"local_deleted={updated['local_deleted']} "
                    "provider_erasure_confirmed=False"
                ),
            )
            return copy.deepcopy(updated)

    def status(self, now: datetime) -> dict[str, Any]:
        return rights_status(self, now)

    def to_dict(self) -> dict[str, Any]:
        return self._serialize_rows(self.requests())

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RightsRequestLedger:
        if bool(data.get("provider_erasure_confirmed", False)):
            raise ValueError("Serialized ledger cannot assert provider_erasure_confirmed=True.")
        raw_reqs = data.get("requests", data.get("rights_requests", []))
        if not isinstance(raw_reqs, Sequence) or isinstance(raw_reqs, (str, bytes)):
            raise ValueError("Ledger mapping must contain a 'requests' sequence.")
        return cls(initial=[dict(item) for item in raw_reqs])

    @classmethod
    def from_json(cls, raw: str) -> RightsRequestLedger:
        parsed = json.loads(raw)
        if not isinstance(parsed, Mapping):
            raise ValueError("Serialized RightsRequestLedger JSON must be an object.")
        return cls.from_dict(parsed)


def _coerce_ledger(target: Any) -> RightsRequestLedger:
    if isinstance(target, RightsRequestLedger):
        return target
    if isinstance(target, (str, os.PathLike)):
        return RightsRequestLedger(path=target)
    if hasattr(target, "data") and callable(getattr(target, "save", None)):
        return RightsRequestLedger(store=target)
    raise TypeError("Expected a RightsRequestLedger, Store/SqlStore instance, or filesystem path.")


def record_rights_request(
    target: Any,
    *,
    request_id: str,
    kind: str,
    subject_key: str,
    received_at: str | datetime,
    actor: str = "staff",
    subject_population: str = "current_staff_identity",
    notes_ref: str = "",
) -> dict[str, Any]:
    return _coerce_ledger(target).record_request(
        request_id=request_id,
        kind=kind,
        subject_key=subject_key,
        received_at=received_at,
        actor=actor,
        subject_population=subject_population,
        notes_ref=notes_ref,
    )


def log_rights_action(
    target: Any,
    request_id: str,
    *,
    action: str,
    actor: str,
    at: str | datetime,
    target_scope: str = "local_store",
    record_count: int = 0,
    local_deleted: bool = False,
    provider_erasure_confirmed: bool = False,
    audit_retained_reason: str | None = None,
) -> dict[str, Any]:
    return _coerce_ledger(target).log_action(
        request_id,
        action=action,
        actor=actor,
        at=at,
        target_scope=target_scope,
        record_count=record_count,
        local_deleted=local_deleted,
        provider_erasure_confirmed=provider_erasure_confirmed,
        audit_retained_reason=audit_retained_reason,
    )


def answer_rights_request(
    target: Any,
    request_id: str,
    *,
    answered_at: str | datetime,
    actor: str,
    outcome: str = "completed",
    summary_ref: str = "",
    local_deleted: bool | None = None,
    provider_erasure_confirmed: bool = False,
    audit_retention_refusal: str | None = None,
) -> dict[str, Any]:
    return _coerce_ledger(target).answer_request(
        request_id,
        answered_at=answered_at,
        actor=actor,
        outcome=outcome,
        summary_ref=summary_ref,
        local_deleted=local_deleted,
        provider_erasure_confirmed=provider_erasure_confirmed,
        audit_retention_refusal=audit_retention_refusal,
    )


def rights_status(
    requests: RightsRequestLedger
    | _RightsStoreProtocol
    | str
    | os.PathLike[str]
    | Mapping[str, Any]
    | Sequence[Mapping[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    """Classify rights requests across persisted ledgers, stores, JSON dicts or raw row lists."""
    now_dt = _parse_aware_datetime(now, "Rights status clock")
    persisted = False
    raw_rows: Sequence[Mapping[str, Any]]
    if isinstance(requests, RightsRequestLedger):
        persisted = requests.is_persisted
        raw_rows = requests.requests()
    elif isinstance(requests, (str, os.PathLike, _RightsStoreProtocol)):
        ledger = _coerce_ledger(requests)
        persisted = ledger.is_persisted
        raw_rows = ledger.requests()
    elif isinstance(requests, Mapping):
        items = requests.get("requests", requests.get("rights_requests", []))
        if not isinstance(items, Sequence) or isinstance(items, (str, bytes)):
            raise ValueError("Rights status mapping must contain a 'requests' sequence.")
        raw_rows = items
    else:
        raw_rows = requests

    rows: list[dict[str, Any]] = []
    for r in raw_rows:
        if bool(r.get("provider_erasure_confirmed", False)):
            raise ValueError(
                "Rights status refuses records claiming confirmed provider erasure "
                "from local state."
            )
        req_id = str(r.get("id") or r.get("request_id") or "")
        received_dt = _parse_aware_datetime(str(r["received_at"]), "received_at")
        due = (
            _parse_aware_datetime(str(r["due_at"]), "due_at")
            if r.get("due_at")
            else due_date(received_dt)
        )
        answered = r.get("answered_at")
        answered_dt = _parse_aware_datetime(str(answered), "answered_at") if answered else None
        late = (
            answered_dt.date() > due.date()
            if answered_dt is not None
            else now_dt.date() > due.date()
        )
        state = (
            "answered_late"
            if answered_dt is not None and late
            else "answered"
            if answered_dt is not None
            else "overdue"
            if late
            else "open"
        )
        raw_actions = r.get("actions")
        action_kinds = (
            [
                str(a.get("action"))
                for a in raw_actions
                if isinstance(a, Mapping) and a.get("action")
            ]
            if isinstance(raw_actions, Sequence) and not isinstance(raw_actions, (str, bytes))
            else []
        )
        local_deleted = bool(r.get("local_deleted", False))
        rows.append(
            dict(
                id=req_id,
                kind=str(r["kind"]),
                received_at=received_dt.isoformat(),
                due=due.isoformat(),
                answered_at=answered_dt.isoformat() if answered_dt is not None else None,
                state=state,
                within_one_month=(
                    answered_dt.date() <= due.date() if answered_dt is not None else None
                ),
                action_kinds=action_kinds,
                local_deleted=local_deleted,
                provider_erasure_confirmed=False,
            )
        )
    return dict(
        label="synthetic-demo",
        persisted=persisted,
        provider_erasure_confirmed=False,
        requests=rows,
        overdue=[r["id"] for r in rows if r["state"] == "overdue"],
        local_deleted_not_provider_erased=[r["id"] for r in rows if r["local_deleted"]],
        note=(
            f"Persisted rights ledger active. {PROVIDER_ERASURE_NOTE}"
            if persisted
            else (
                f"In-memory classification only: no store or file attached. {PROVIDER_ERASURE_NOTE}"
            )
        ),
    )
