"""Phase 0 retrofit-flow discovery contract and governance guard (BG-011; issue #124).

Pure, deterministic, offline standard-library contract for Zava North Homes Phase 0
retrofit-flow discovery. It enforces four non-negotiable governance rules:

1. Nominated human discovery owner and agreed accepted-handover endpoint before
   any candidate output may be promoted.
2. Domain-owner-validated PAS 2035 and retrofit lifecycle dictionary covering all
   end-to-end stages, distinct events, timestamp specifications, wait states and
   return loops through accepted handover.
3. Ranked constraint hypothesis register (1..N) requiring both supporting_evidence
   and contradicting_evidence plus the five-part constraint test before acceptance,
   with proposer separation and visible DISPUTED preservation.
4. Fail-closed governance guard stamping owner_validated=False and
   finding_status="candidate_hypothesis_not_company_finding" on every discovery
   output until the nominated human discovery owner records formal validation.
"""

import copy
import hashlib
import json
import weakref
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from contextvars import ContextVar
from dataclasses import asdict, dataclass, replace
from datetime import UTC, date, datetime
from typing import Any, NoReturn, Protocol, overload, runtime_checkable

from .discovery_flow import DISPUTED as WAIT_CAUSE_DISPUTED
from .discovery_flow import LOOP_KINDS, UNATTRIBUTED, UNKNOWN
from .discovery_register import (
    CANDIDATE_FINDING_STATUS as CANDIDATE_FINDING_STATUS,
)
from .discovery_register import (
    CONTRADICTS as CONTRADICTS,
)
from .discovery_register import (
    DISPUTED as DISPUTED,
)
from .discovery_register import (
    ENDPOINT as ENDPOINT,
)
from .discovery_register import (
    NOT_FINDING as NOT_FINDING,
)
from .discovery_register import (
    PROPOSED as PROPOSED,
)
from .discovery_register import (
    SEED_PROPOSER as SEED_PROPOSER,
)
from .discovery_register import (
    SUPPORTS as SUPPORTS,
)
from .discovery_register import (
    VALIDATED_FINDING_STATUS as VALIDATED_FINDING_STATUS,
)
from .discovery_register import (
    GovernanceViolationError as GovernanceViolationError,
)
from .discovery_register import (
    is_valid_human_actor as is_valid_human_actor,
)

CONTRACT_VERSION = "phase0-retrofit-flow-discovery-contract-v1"
DOMAIN_VALIDATED = "DOMAIN_VALIDATED"
OWNER_VALIDATED = "OWNER_VALIDATED"
PAS2035_EVIDENCE_PROVENANCE_NOTE = (
    "Grounded in BSI PAS 2035:2023 overview snapshot (2026-09-19); "
    "licensed PAS 2035:2023 clause text is not held in this repository."
)

REQUIRED_FLOW_STAGE_CODES = (
    "candidate_identification",
    "resident_engagement_and_survey_booking",
    "pas2035_retrofit_assessment",
    "safety_and_dependency_triage",
    "pas2035_design_and_coordination",
    "resident_works_decision",
    "funding_capacity_and_work_release",
    "appointment_and_installation",
    "quality_and_evidence_acceptance",
    "resident_and_accepted_handover",
)
REQUIRED_EXCEPTION_STATE_CODES = (
    "paused",
    "excluded",
    "withdrawn",
    "cancelled",
    "reopened_aftercare",
)
REQUIRED_LIFECYCLE_EVENTS = (
    "candidate selection",
    "retrofit assessment completed",
    "design approved",
    "resident works decision recorded",
    "ready to install",
    "work release",
    "appointment",
    "installation",
    "practical completion",
    "invoice",
    "documentary completion",
    "physical acceptance",
    "evidence acceptance",
    "resident handover",
    "accepted handover",
)
ACCEPTED_HANDOVER_PREREQUISITE_EVENTS = (
    "design approved",
    "resident works decision recorded",
    "physical acceptance",
    "evidence acceptance",
    "resident handover",
)
REQUIRED_TIMESTAMP_CODES = (
    "stage_entered_at",
    "stage_exited_at",
    "active_work_started_at",
    "active_work_completed_at",
    "event_occurred_at",
    "wait_started_at",
    "wait_ended_at",
    "loop_recorded_at",
)
REQUIRED_WAIT_STATE_CODES = (
    "awaiting_supplier_or_professional_capacity",
    "awaiting_handoff_acceptance_or_approval",
    "awaiting_resident_access_adjustment_or_decision",
    "safety_or_hazard_hold",
    "building_or_planned_maintenance_dependency",
    "funding_or_payment_hold",
    "quality_defect_or_evidence_remediation",
)
REQUIRED_RETURN_LOOP_KINDS = LOOP_KINDS
POST_INSTALL_HANDOVER_LEGS = (
    ("installation to physical acceptance", "installation", "physical acceptance"),
    ("physical acceptance to evidence acceptance", "physical acceptance", "evidence acceptance"),
    ("evidence acceptance to resident handover", "evidence acceptance", "resident handover"),
    ("resident handover to accepted handover", "resident handover", "accepted handover"),
)


def _require_human_actor(value: str, label: str) -> str:
    if not is_valid_human_actor(value):
        raise ValueError(f"{label} must name a human actor, not a blank, placeholder or AI actor")
    return value.strip()


def _require_non_blank(value: str, label: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{label} cannot be blank")
    return cleaned


@dataclass(frozen=True)
class NominatedDiscoveryOwner:
    nominated_by: str = ""
    nominated_by_role: str = ""
    owner: str = ""
    owner_role: str = ""
    nominated_on: date | None = None
    endpoint: str = ""
    endpoint_agreed_by: str = ""
    endpoint_agreed_role: str = ""
    endpoint_agreed_on: date | None = None

    def status(self) -> str:
        if not (
            is_valid_human_actor(self.nominated_by)
            and is_valid_human_actor(self.owner)
            and self.nominated_by_role.strip()
            and self.owner_role.strip()
            and self.nominated_on is not None
            and self.nominated_by.strip().lower() != self.owner.strip().lower()
        ):
            return "NOT_NOMINATED"
        if not (
            self.endpoint.strip().lower() == ENDPOINT
            and is_valid_human_actor(self.endpoint_agreed_by)
            and self.endpoint_agreed_role.strip()
            and self.endpoint_agreed_on is not None
            and self.endpoint_agreed_on >= self.nominated_on
        ):
            return "ENDPOINT_NOT_AGREED"
        return "ENDPOINT_AGREED"

    @property
    def is_ready(self) -> bool:
        return self.status() == "ENDPOINT_AGREED"


def nominate_discovery_owner(
    *,
    nominated_by: str,
    nominated_by_role: str,
    owner: str,
    owner_role: str,
    nominated_on: date,
) -> NominatedDiscoveryOwner:
    sponsor = _require_human_actor(nominated_by, "Executive sponsor")
    nominee = _require_human_actor(owner, "Discovery owner")
    if sponsor.lower() == nominee.lower():
        raise ValueError("Executive sponsor and nominated discovery owner must be distinct people")
    return NominatedDiscoveryOwner(
        nominated_by=sponsor,
        nominated_by_role=_require_non_blank(nominated_by_role, "Executive sponsor role"),
        owner=nominee,
        owner_role=_require_non_blank(owner_role, "Discovery owner role"),
        nominated_on=nominated_on,
    )


def agree_discovery_endpoint(
    record: NominatedDiscoveryOwner,
    *,
    endpoint: str,
    agreed_by: str,
    agreed_role: str,
    agreed_on: date,
) -> NominatedDiscoveryOwner:
    if record.status() == "NOT_NOMINATED" or record.nominated_on is None:
        raise ValueError("Nominate a human discovery owner before agreeing the endpoint")
    if endpoint.strip().lower() != ENDPOINT:
        raise ValueError(f"Phase 0 discovery endpoint must be '{ENDPOINT}', not '{endpoint}'")
    if agreed_on < record.nominated_on:
        raise ValueError("Endpoint agreement date cannot precede owner nomination date")
    return replace(
        record,
        endpoint=ENDPOINT,
        endpoint_agreed_by=_require_human_actor(agreed_by, "Endpoint approver"),
        endpoint_agreed_role=_require_non_blank(agreed_role, "Endpoint approver role"),
        endpoint_agreed_on=agreed_on,
    )


@dataclass(frozen=True)
class StageSpec:
    order: int
    code: str
    name: str
    kind: str
    entry_event: str
    exit_event: str
    pas2035_role_boundary: str
    owner_role: str
    validated_by: str = ""
    validated_on: date | None = None
    validated_role: str = ""

    @property
    def validated(self) -> bool:
        return (
            bool(self.owner_role.strip())
            and is_valid_human_actor(self.validated_by)
            and self.validated_on is not None
            and self.validated_role == self.owner_role
        )


@dataclass(frozen=True)
class EventSpec:
    event: str
    stage_code: str
    meaning: str
    distinct_from_note: str
    owner_role: str
    validated_by: str = ""
    validated_on: date | None = None
    validated_role: str = ""

    @property
    def validated(self) -> bool:
        return (
            bool(self.owner_role.strip())
            and is_valid_human_actor(self.validated_by)
            and self.validated_on is not None
            and self.validated_role == self.owner_role
        )


@dataclass(frozen=True)
class TimestampSpec:
    code: str
    applies_to: str
    meaning: str
    precision_rule: str
    non_imputation_rule: str
    owner_role: str
    validated_by: str = ""
    validated_on: date | None = None
    validated_role: str = ""

    @property
    def validated(self) -> bool:
        return (
            bool(self.owner_role.strip())
            and is_valid_human_actor(self.validated_by)
            and self.validated_on is not None
            and self.validated_role == self.owner_role
        )


@dataclass(frozen=True)
class WaitStateSpec:
    code: str
    meaning: str
    accountable_domain: str
    clock_rule: str
    unknown_cause_rule: str
    owner_role: str
    validated_by: str = ""
    validated_on: date | None = None
    validated_role: str = ""

    @property
    def validated(self) -> bool:
        return (
            bool(self.owner_role.strip())
            and is_valid_human_actor(self.validated_by)
            and self.validated_on is not None
            and self.validated_role == self.owner_role
        )


@dataclass(frozen=True)
class ReturnLoopSpec:
    kind: str
    meaning: str
    allowed_target_stages: tuple[str, ...]
    non_inference_rule: str
    owner_role: str
    validated_by: str = ""
    validated_on: date | None = None
    validated_role: str = ""

    @property
    def validated(self) -> bool:
        return (
            bool(self.owner_role.strip())
            and is_valid_human_actor(self.validated_by)
            and self.validated_on is not None
            and self.validated_role == self.owner_role
        )


@dataclass(frozen=True)
class LifecycleDictionary:
    stages: tuple[StageSpec, ...]
    events: tuple[EventSpec, ...]
    timestamps: tuple[TimestampSpec, ...]
    wait_states: tuple[WaitStateSpec, ...]
    return_loops: tuple[ReturnLoopSpec, ...]

    def __post_init__(self) -> None:
        flow_sequence = tuple((s.order, s.code) for s in self.stages if s.kind == "flow")
        expected_sequence = tuple(enumerate(REQUIRED_FLOW_STAGE_CODES, start=1))
        if flow_sequence != expected_sequence:
            raise GovernanceViolationError(
                "LifecycleDictionary flow stages must match canonical "
                "REQUIRED_FLOW_STAGE_CODES order 1..10"
            )


def validate_stage_spec(spec: StageSpec, *, validator: str, role: str, on: date) -> StageSpec:
    if role != spec.owner_role:
        raise ValueError(f"Stage {spec.code} is validated by {spec.owner_role}, not {role}")
    return replace(
        spec,
        validated_by=_require_human_actor(validator, "Stage validator"),
        validated_on=on,
        validated_role=role,
    )


def validate_event_spec(spec: EventSpec, *, validator: str, role: str, on: date) -> EventSpec:
    if role != spec.owner_role:
        raise ValueError(f"Event '{spec.event}' is validated by {spec.owner_role}, not {role}")
    return replace(
        spec,
        validated_by=_require_human_actor(validator, "Event validator"),
        validated_on=on,
        validated_role=role,
    )


def validate_timestamp_spec(
    spec: TimestampSpec, *, validator: str, role: str, on: date
) -> TimestampSpec:
    if role != spec.owner_role:
        raise ValueError(f"Timestamp {spec.code} is validated by {spec.owner_role}, not {role}")
    return replace(
        spec,
        validated_by=_require_human_actor(validator, "Timestamp validator"),
        validated_on=on,
        validated_role=role,
    )


def validate_wait_state_spec(
    spec: WaitStateSpec, *, validator: str, role: str, on: date
) -> WaitStateSpec:
    if role != spec.owner_role:
        raise ValueError(f"Wait state {spec.code} is validated by {spec.owner_role}, not {role}")
    return replace(
        spec,
        validated_by=_require_human_actor(validator, "Wait-state validator"),
        validated_on=on,
        validated_role=role,
    )


def validate_return_loop_spec(
    spec: ReturnLoopSpec, *, validator: str, role: str, on: date
) -> ReturnLoopSpec:
    if role != spec.owner_role:
        raise ValueError(f"Return loop '{spec.kind}' is validated by {spec.owner_role}, not {role}")
    return replace(
        spec,
        validated_by=_require_human_actor(validator, "Return-loop validator"),
        validated_on=on,
        validated_role=role,
    )


def build_default_lifecycle_dictionary() -> LifecycleDictionary:
    """Construct the unvalidated Zava North Homes Phase 0 PAS 2035 lifecycle seed dictionary."""
    stages = (
        StageSpec(
            1,
            "candidate_identification",
            "Candidate identification and cohort selection",
            "flow",
            "candidate selection",
            "resident contact initiated",
            "Asset strategy and cohort eligibility boundary before PAS 2035 assessment",
            "Asset Director and Retrofit Programme Manager",
        ),
        StageSpec(
            2,
            "resident_engagement_and_survey_booking",
            "Resident contact, adjustments and survey booking",
            "flow",
            "resident contact initiated",
            "survey appointment booked",
            "Accessible resident information and adjustment check before home survey",
            "Resident Engagement and Housing",
        ),
        StageSpec(
            3,
            "pas2035_retrofit_assessment",
            "PAS 2035 retrofit assessment and site survey",
            "flow",
            "survey appointment booked",
            "retrofit assessment completed",
            "PAS 2035 whole-dwelling assessment by competent Retrofit Assessor",
            "Retrofit Assessor and Retrofit Programme Manager",
        ),
        StageSpec(
            4,
            "safety_and_dependency_triage",
            "Safety, damp-and-mould and building or planned-maintenance dependency triage",
            "flow",
            "retrofit assessment completed",
            "dependency clearance recorded",
            "Statutory hazard, damp/mould and fabric/enabling-works gate before design sign-off",
            "Building Safety, Repairs and Assets",
        ),
        StageSpec(
            5,
            "pas2035_design_and_coordination",
            "PAS 2035 retrofit design, risk path and coordinator approval",
            "flow",
            "dependency clearance recorded",
            "design approved",
            "PAS 2035 measure package design and Retrofit Coordinator approval",
            "Retrofit Designer and Retrofit Coordinator",
        ),
        StageSpec(
            6,
            "resident_works_decision",
            "Measure-specific resident works decision and consent",
            "flow",
            "design approved",
            "resident works decision recorded",
            "Plain-language resident scope, disruption and consent boundary",
            "Resident Engagement and Housing",
        ),
        StageSpec(
            7,
            "funding_capacity_and_work_release",
            "Grant/budget check, committed supplier capacity and work release",
            "flow",
            "resident works decision recorded",
            "work release",
            "Finance eligibility, committed installer capacity and ready-to-install release",
            "Finance, Procurement and Retrofit Programme Manager",
        ),
        StageSpec(
            8,
            "appointment_and_installation",
            "Appointment agreement, site installation and practical completion",
            "flow",
            "appointment",
            "practical completion",
            "PAS 2030/2035 physical installation and contractor practical completion",
            "Programme and Contract Manager",
        ),
        StageSpec(
            9,
            "quality_and_evidence_acceptance",
            "Independent physical inspection and PAS 2035 documentary evidence acceptance",
            "flow",
            "practical completion",
            "evidence acceptance",
            "Independent physical snagging clearance and PAS 2035 lodgement/evidence pack check",
            "Programme and independent quality owner",
        ),
        StageSpec(
            10,
            "resident_and_accepted_handover",
            "Accessible resident handover and accepted handover endpoint",
            "flow",
            "resident handover",
            "accepted handover",
            "Accessible resident operating guidance and accepted handover completion gate",
            "Retrofit Programme Manager",
        ),
        StageSpec(
            11,
            "paused",
            "Paused property with open hold and recorded restart condition",
            "exception",
            "pause recorded",
            "restart recorded",
            "Property remains in baseline population while paused on an explicit hold",
            "Retrofit Programme Manager",
        ),
        StageSpec(
            12,
            "excluded",
            "Excluded property retained in baseline denominator with recorded reason",
            "terminal",
            "exclusion recorded",
            "none",
            "Stock or scheme ineligibility recorded without dropping candidate from baseline",
            "Asset Director and Retrofit Programme Manager",
        ),
        StageSpec(
            13,
            "withdrawn",
            "Resident withdrawal or refusal retained without penalty",
            "terminal",
            "withdrawal recorded",
            "none",
            "Resident right to decline or withdraw preserved distinctly from failed access",
            "Resident Engagement and Housing",
        ),
        StageSpec(
            14,
            "cancelled",
            "Programme or contract cancellation retained in baseline population",
            "terminal",
            "cancellation recorded",
            "none",
            "Cancelled work order or cohort exit retained visibly in baseline accounting",
            "Retrofit Programme Manager",
        ),
        StageSpec(
            15,
            "reopened_aftercare",
            "Post-handover reopen for unresolved defect, callback or evidence failure",
            "exception",
            "reopen recorded",
            "accepted handover",
            "Post-handover callback or defect loop invalidating clean handover until closed",
            "Programme and independent quality owner",
        ),
    )
    events = (
        EventSpec(
            "candidate selection",
            "candidate_identification",
            "Property enters the Phase 0 baseline retrofit candidate population",
            "Distinct from survey booking and work release",
            "Asset Director and Retrofit Programme Manager",
        ),
        EventSpec(
            "retrofit assessment completed",
            "pas2035_retrofit_assessment",
            "Competent PAS 2035 whole-dwelling retrofit assessment is completed and lodged",
            "Starts the BG-011 assessment-to-ready-to-install cycle-time leg",
            "Retrofit Assessor and Retrofit Programme Manager",
        ),
        EventSpec(
            "design approved",
            "pas2035_design_and_coordination",
            "PAS 2035 retrofit design and risk path are approved by the Retrofit Coordinator",
            "Required before measure-specific resident works decision and work release",
            "Retrofit Designer and Retrofit Coordinator",
        ),
        EventSpec(
            "resident works decision recorded",
            "resident_works_decision",
            "Resident records informed decision on the specific home works package",
            "Distinct from survey access and never inferred from missed appointments",
            "Resident Engagement and Housing",
        ),
        EventSpec(
            "ready to install",
            "funding_capacity_and_work_release",
            "Design, resident decision, dependencies, funding and capacity are cleared for install",
            "Ends the BG-011 assessment-to-ready-to-install leg; precedes work release",
            "Finance, Procurement and Retrofit Programme Manager",
        ),
        EventSpec(
            "work release",
            "funding_capacity_and_work_release",
            "Work order is formally released to an installer against committed capacity",
            "Distinct from ready-to-install readiness and resident appointment booking",
            "Finance, Procurement and Retrofit Programme Manager",
        ),
        EventSpec(
            "appointment",
            "appointment_and_installation",
            "Installation appointment window is agreed with the resident",
            "Distinct from work release and physical installation start/completion",
            "Programme and Contract Manager",
        ),
        EventSpec(
            "installation",
            "appointment_and_installation",
            "Physical retrofit measure installation work is executed on site",
            "Distinct from contractor practical completion and quality acceptance",
            "Programme and Contract Manager",
        ),
        EventSpec(
            "practical completion",
            "appointment_and_installation",
            "Contractor declares site installation practically complete",
            "Never treated as Phase 0 endpoint or quality/resident acceptance",
            "Programme and Contract Manager",
        ),
        EventSpec(
            "invoice",
            "quality_and_evidence_acceptance",
            "Supplier submits commercial application or invoice",
            "Commercial event kept strictly separate from physical or documentary acceptance",
            "Finance, Procurement and Retrofit Programme Manager",
        ),
        EventSpec(
            "documentary completion",
            "quality_and_evidence_acceptance",
            "Installer/coordinator submits handover certificates and PAS 2035 evidence pack",
            "Submission only; distinct from independent evidence acceptance",
            "Programme and independent quality owner",
        ),
        EventSpec(
            "physical acceptance",
            "quality_and_evidence_acceptance",
            "Independent quality check accepts physical workmanship with snags cleared",
            "Distinct from practical completion and documentary evidence acceptance",
            "Programme and independent quality owner",
        ),
        EventSpec(
            "evidence acceptance",
            "quality_and_evidence_acceptance",
            "Quality/compliance owner accepts the complete PAS 2035 documentary evidence pack",
            "Distinct from documentary submission and commercial invoice payment",
            "Programme and independent quality owner",
        ),
        EventSpec(
            "resident handover",
            "resident_and_accepted_handover",
            "Resident receives accessible operating, ventilation and aftercare handover",
            "Distinct from physical/evidence acceptance and final accepted handover closure",
            "Resident Engagement and Housing",
        ),
        EventSpec(
            "accepted handover",
            "resident_and_accepted_handover",
            "All PAS 2035 design, consent, physical, documentary and resident handover gates pass",
            "Canonical Phase 0 endpoint; intended energy outcome is tracked separately",
            "Retrofit Programme Manager",
        ),
    )
    timestamps = (
        TimestampSpec(
            "stage_entered_at",
            "PropertyStageRecord.entered_at",
            "Timestamp when a property enters a lifecycle stage or exception state",
            "ISO-8601 date (YYYY-MM-DD) or timezone-aware ISO-8601 datetime with source_ref",
            "Missing or free-text values are recorded as gaps and never estimated",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "stage_exited_at",
            "PropertyStageRecord.exited_at",
            "Timestamp when a property exits a lifecycle stage",
            "ISO-8601 date or timezone-aware ISO-8601 datetime >= stage_entered_at",
            "Open stages keep exited_at empty; negative durations are flagged as gaps",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "active_work_started_at",
            "PropertyStageRecord.active_started_at",
            "Timestamp when active professional or site work actually begins inside a stage",
            "ISO-8601 date or timezone-aware ISO-8601 datetime with source_ref",
            "When absent, active_days stays None and is never imputed from calendar minus wait",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "active_work_completed_at",
            "PropertyStageRecord.active_completed_at",
            "Timestamp when active professional or site work finishes inside a stage",
            "ISO-8601 date or timezone-aware ISO-8601 datetime >= active_work_started_at",
            "When absent or out of order, active_days stays None and any order error is flagged",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "event_occurred_at",
            "PropertyEventRecord.occurred_at",
            "Timestamp when a distinct lifecycle milestone event occurred",
            "ISO-8601 date or timezone-aware ISO-8601 datetime with source_ref",
            "Out-of-order legs return None and emit an explicit sequence gap",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "wait_started_at",
            "PropertyWaitRecord.started_at",
            "Timestamp when an explicit wait or hold began",
            "ISO-8601 date or timezone-aware ISO-8601 datetime with source_ref",
            "Unattributed party or UNKNOWN/DISPUTED cause remains visible without inference",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "wait_ended_at",
            "PropertyWaitRecord.ended_at",
            "Timestamp when a wait or hold cleared (or empty while open as of extract cut-off)",
            "ISO-8601 date or timezone-aware ISO-8601 datetime >= wait_started_at",
            "Open waits measure against extract as_of date; end < start is flagged as a gap",
            "Retrofit Flow and Data Governance Owner",
        ),
        TimestampSpec(
            "loop_recorded_at",
            "PropertyReturnLoopRecord.recorded_at",
            "Timestamp when a return, rejection, repeat visit or reopen loop was recorded",
            "ISO-8601 date or timezone-aware ISO-8601 datetime with source_ref",
            "Rework duration remains None unless explicit rework evidence exists",
            "Retrofit Flow and Data Governance Owner",
        ),
    )
    wait_states = (
        WaitStateSpec(
            "awaiting_supplier_or_professional_capacity",
            "Work ready to progress but waiting for assessor, designer, coordinator or installer",
            "Procurement and Contracts",
            "Counts elapsed wait days against supplier or professional capacity domain",
            "Keep cause UNKNOWN or DISPUTED when diary vs capacity root cause is unverified",
            "Procurement and Contracts",
        ),
        WaitStateSpec(
            "awaiting_handoff_acceptance_or_approval",
            "Completed upstream artefact sitting in internal or coordinator/contractor queue",
            "Retrofit Programme Manager",
            "Counts elapsed queue days between submission and formal acceptance/rejection",
            "Unassigned handoff owner is reported under Unattributed party",
            "Retrofit Programme Manager",
        ),
        WaitStateSpec(
            "awaiting_resident_access_adjustment_or_decision",
            "Waiting for resident contact window, reasonable adjustment, access or works decision",
            "Resident Engagement and Housing",
            "Counts elapsed resident-facing wait days without penalising resident refusal rights",
            "Failed access is never converted into refusal or withdrawal without explicit record",
            "Resident Engagement and Housing",
        ),
        WaitStateSpec(
            "safety_or_hazard_hold",
            "Retrofit paused for damp/mould, asbestos, structural, fire or electrical safety",
            "Building Safety, Repairs and Assets",
            "Holds progression to design release or installation until hazard clearance",
            "Safety hold cause stays separate from general repairs backlog unless evidenced",
            "Building Safety, Repairs and Assets",
        ),
        WaitStateSpec(
            "building_or_planned_maintenance_dependency",
            "Waiting for roof, window, fabric repair, DNO, planning or stock-investment alignment",
            "Building Safety, Repairs and Assets",
            "Tracks enabling-works and external dependency hold duration explicitly",
            "Missing enabling-works dates are flagged as gaps rather than backfilled",
            "Building Safety, Repairs and Assets",
        ),
        WaitStateSpec(
            "funding_or_payment_hold",
            "Waiting for grant eligibility check, batch cap approval or commercial hold",
            "Finance, Procurement and Retrofit Programme Manager",
            "Tracks grant/budget governance hold separately from supplier capacity",
            "Unreconciled finance vs contract holds remain DISPUTED until owner review",
            "Finance, Procurement and Retrofit Programme Manager",
        ),
        WaitStateSpec(
            "quality_defect_or_evidence_remediation",
            "Waiting for contractor snagging fix or missing PAS 2035 documentary evidence",
            "Programme and independent quality owner",
            "Blocks physical acceptance, evidence acceptance and accepted handover",
            "Physical defect vs missing certificate waits remain visible by evidence ref",
            "Programme and independent quality owner",
        ),
    )
    return_loops = (
        ReturnLoopSpec(
            "return",
            "Upstream PAS 2035 assessment, dependency check or design returned for rework",
            (
                "pas2035_retrofit_assessment",
                "safety_and_dependency_triage",
                "pas2035_design_and_coordination",
            ),
            "Counted separately from formal quality/grant rejection",
            "Retrofit Designer and Retrofit Coordinator",
        ),
        ReturnLoopSpec(
            "rejection",
            "Physical inspection, PAS 2035 documentary pack or grant/commercial pack rejected",
            (
                "pas2035_design_and_coordination",
                "funding_capacity_and_work_release",
                "appointment_and_installation",
                "quality_and_evidence_acceptance",
            ),
            "Blocks downstream handover until re-inspected and accepted",
            "Programme and independent quality owner",
        ),
        ReturnLoopSpec(
            "repeat visit",
            "Additional survey, installation or snagging visit required (including no-access)",
            (
                "resident_engagement_and_survey_booking",
                "pas2035_retrofit_assessment",
                "appointment_and_installation",
                "quality_and_evidence_acceptance",
            ),
            "Failed access visit never infers resident refusal or consent withdrawal",
            "Resident Engagement and Housing",
        ),
        ReturnLoopSpec(
            "reopen",
            "Case reopened after practical completion or handover due to defect or scope change",
            (
                "pas2035_design_and_coordination",
                "appointment_and_installation",
                "quality_and_evidence_acceptance",
                "reopened_aftercare",
            ),
            "An unresolved reopen after accepted handover blocks clean accepted-handover status",
            "Programme and independent quality owner",
        ),
    )
    return LifecycleDictionary(
        stages=stages,
        events=events,
        timestamps=timestamps,
        wait_states=wait_states,
        return_loops=return_loops,
    )


def lifecycle_dictionary_gaps(dictionary: LifecycleDictionary) -> list[str]:
    """Return plain-language completeness and domain-owner validation gaps across the dictionary."""
    gaps: list[str] = []
    stages_by_code = {s.code: s for s in dictionary.stages}
    flow_stages = [s for s in dictionary.stages if s.kind == "flow"]
    expected_flow = list(enumerate(REQUIRED_FLOW_STAGE_CODES, start=1))
    if [(s.order, s.code) for s in flow_stages] != expected_flow:
        gaps.append(
            "Flow stages must follow canonical REQUIRED_FLOW_STAGE_CODES order 1..10 "
            "through accepted handover"
        )
    for code in REQUIRED_FLOW_STAGE_CODES + REQUIRED_EXCEPTION_STATE_CODES:
        stage = stages_by_code.get(code)
        if stage is None:
            gaps.append(f"Define lifecycle stage or state '{code}'")
        elif not (stage.name.strip() and stage.pas2035_role_boundary.strip()):
            gaps.append(f"Complete description and PAS 2035 boundary for stage '{code}'")
        elif stage.validated_role and stage.validated_role != stage.owner_role:
            gaps.append(
                f"Stage '{code}' recorded validator role '{stage.validated_role}', "
                f"expected '{stage.owner_role}'"
            )
        elif not stage.validated:
            gaps.append(f"The {stage.owner_role} has not validated stage '{code}'")

    events_by_name = {e.event: e for e in dictionary.events}
    for event_name in REQUIRED_LIFECYCLE_EVENTS:
        ev = events_by_name.get(event_name)
        if ev is None:
            gaps.append(f"Define lifecycle event '{event_name}' as a separate event")
        elif ev.stage_code not in stages_by_code:
            gaps.append(f"Event '{event_name}' references unknown stage '{ev.stage_code}'")
        elif not (ev.meaning.strip() and ev.distinct_from_note.strip()):
            gaps.append(f"Add meaning and distinction rule for event '{event_name}'")
        elif ev.validated_role and ev.validated_role != ev.owner_role:
            gaps.append(
                f"Event '{event_name}' recorded validator role '{ev.validated_role}', "
                f"expected '{ev.owner_role}'"
            )
        elif not ev.validated:
            gaps.append(f"The {ev.owner_role} has not validated event '{event_name}'")

    ts_by_code = {t.code: t for t in dictionary.timestamps}
    for ts_code in REQUIRED_TIMESTAMP_CODES:
        ts = ts_by_code.get(ts_code)
        if ts is None:
            gaps.append(f"Define timestamp specification '{ts_code}'")
        elif not (ts.meaning.strip() and ts.precision_rule.strip() and ts.non_imputation_rule):
            gaps.append(f"Complete rules for timestamp specification '{ts_code}'")
        elif ts.validated_role and ts.validated_role != ts.owner_role:
            gaps.append(
                f"Timestamp '{ts_code}' recorded validator role '{ts.validated_role}', "
                f"expected '{ts.owner_role}'"
            )
        elif not ts.validated:
            gaps.append(f"The {ts.owner_role} has not validated timestamp '{ts_code}'")

    waits_by_code = {w.code: w for w in dictionary.wait_states}
    for wait_code in REQUIRED_WAIT_STATE_CODES:
        wait = waits_by_code.get(wait_code)
        if wait is None:
            gaps.append(f"Define wait state '{wait_code}'")
        elif not (wait.meaning.strip() and wait.clock_rule.strip() and wait.unknown_cause_rule):
            gaps.append(f"Complete attribution rules for wait state '{wait_code}'")
        elif wait.validated_role and wait.validated_role != wait.owner_role:
            gaps.append(
                f"Wait state '{wait_code}' recorded validator role '{wait.validated_role}', "
                f"expected '{wait.owner_role}'"
            )
        elif not wait.validated:
            gaps.append(f"The {wait.owner_role} has not validated wait state '{wait_code}'")

    loops_by_kind = {r.kind: r for r in dictionary.return_loops}
    for kind in REQUIRED_RETURN_LOOP_KINDS:
        loop = loops_by_kind.get(kind)
        if loop is None:
            gaps.append(f"Define return loop kind '{kind}'")
        elif not loop.allowed_target_stages or any(
            target not in stages_by_code for target in loop.allowed_target_stages
        ):
            gaps.append(f"Return loop '{kind}' must reference valid target stages")
        elif not (loop.meaning.strip() and loop.non_inference_rule.strip()):
            gaps.append(f"Complete meaning and non-inference rule for return loop '{kind}'")
        elif loop.validated_role and loop.validated_role != loop.owner_role:
            gaps.append(
                f"Return loop '{kind}' recorded validator role '{loop.validated_role}', "
                f"expected '{loop.owner_role}'"
            )
        elif not loop.validated:
            gaps.append(f"The {loop.owner_role} has not validated return loop '{kind}'")

    return gaps


def _dictionary_schema_digest(dictionary: LifecycleDictionary) -> str:
    payload = {
        "stages": [
            (
                s.order,
                s.code,
                s.name,
                s.kind,
                s.entry_event,
                s.exit_event,
                s.pas2035_role_boundary,
                s.owner_role,
            )
            for s in dictionary.stages
        ],
        "events": [
            (e.event, e.stage_code, e.meaning, e.distinct_from_note, e.owner_role)
            for e in dictionary.events
        ],
        "timestamps": [
            (
                t.code,
                t.applies_to,
                t.meaning,
                t.precision_rule,
                t.non_imputation_rule,
                t.owner_role,
            )
            for t in dictionary.timestamps
        ],
        "wait_states": [
            (
                w.code,
                w.meaning,
                w.accountable_domain,
                w.clock_rule,
                w.unknown_cause_rule,
                w.owner_role,
            )
            for w in dictionary.wait_states
        ],
        "return_loops": [
            (
                r.kind,
                r.meaning,
                list(r.allowed_target_stages),
                r.non_inference_rule,
                r.owner_role,
            )
            for r in dictionary.return_loops
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class LifecycleDictionaryReport:
    stage_count: int
    event_count: int
    timestamp_spec_count: int
    wait_state_count: int
    return_loop_count: int
    endpoint: str
    gaps: tuple[str, ...]
    owner_validated: bool = False
    finding_status: str = CANDIDATE_FINDING_STATUS
    owner_validated_by: str = ""
    owner_validated_on: date | None = None
    validation_note: str = ""
    notice: str = NOT_FINDING
    dictionary_schema_digest: str = ""

    def __post_init__(self) -> None:
        if not self.owner_validated and self.finding_status == CANDIDATE_FINDING_STATUS:
            return
        if not (
            self.owner_validated
            and self.finding_status == VALIDATED_FINDING_STATUS
            and self.endpoint == ENDPOINT
            and not self.gaps
            and is_valid_human_actor(self.owner_validated_by)
            and self.owner_validated_on is not None
            and not isinstance(self.owner_validated_on, datetime)
            and bool(self.validation_note.strip())
            and bool(self.dictionary_schema_digest.strip())
        ):
            raise GovernanceViolationError(
                "LifecycleDictionaryReport cannot claim owner validation with open gaps "
                "or without a named human discovery owner and bound dictionary_schema_digest"
            )


def summarize_lifecycle_dictionary(dictionary: LifecycleDictionary) -> LifecycleDictionaryReport:
    gaps = tuple(lifecycle_dictionary_gaps(dictionary))
    return LifecycleDictionaryReport(
        stage_count=len(dictionary.stages),
        event_count=len(dictionary.events),
        timestamp_spec_count=len(dictionary.timestamps),
        wait_state_count=len(dictionary.wait_states),
        return_loop_count=len(dictionary.return_loops),
        endpoint=ENDPOINT,
        gaps=gaps,
        dictionary_schema_digest=_dictionary_schema_digest(dictionary),
    )


def _require_ready_owner_and_dictionary(
    discovery_owner: NominatedDiscoveryOwner,
    dictionary: LifecycleDictionary,
    by: str,
    note: str,
) -> tuple[str, str]:
    if not discovery_owner.is_ready:
        raise GovernanceViolationError(
            f"Discovery owner readiness is {discovery_owner.status()}, expected ENDPOINT_AGREED"
        )
    gaps = lifecycle_dictionary_gaps(dictionary)
    if gaps:
        raise GovernanceViolationError(
            f"Lifecycle dictionary must have zero gaps before owner validation ({len(gaps)} open)"
        )
    actor = _require_human_actor(by, "Nominated discovery owner")
    if actor != discovery_owner.owner.strip():
        raise GovernanceViolationError(
            f"Only nominated discovery owner '{discovery_owner.owner}' may record formal validation"
        )
    cleaned_note = note.strip()
    if not cleaned_note:
        raise GovernanceViolationError("Formal discovery-owner validation requires a decision note")
    return actor, cleaned_note


def validate_lifecycle_report(
    report: LifecycleDictionaryReport,
    discovery_owner: NominatedDiscoveryOwner,
    dictionary: LifecycleDictionary,
    *,
    by: str,
    on: date,
    note: str,
) -> LifecycleDictionaryReport:
    actor, cleaned_note = _require_ready_owner_and_dictionary(discovery_owner, dictionary, by, note)
    if report.gaps:
        raise GovernanceViolationError("LifecycleDictionaryReport still records unresolved gaps")
    expected_schema_digest = _dictionary_schema_digest(dictionary)
    if (
        not report.dictionary_schema_digest.strip()
        or report.dictionary_schema_digest != expected_schema_digest
        or report.stage_count != len(dictionary.stages)
        or report.event_count != len(dictionary.events)
        or report.timestamp_spec_count != len(dictionary.timestamps)
        or report.wait_state_count != len(dictionary.wait_states)
        or report.return_loop_count != len(dictionary.return_loops)
    ):
        raise GovernanceViolationError(
            "LifecycleDictionaryReport does not match the supplied LifecycleDictionary schema"
        )
    return replace(
        report,
        owner_validated=True,
        finding_status=VALIDATED_FINDING_STATUS,
        owner_validated_by=actor,
        owner_validated_on=on,
        validation_note=cleaned_note,
        notice="",
    )


def _parse_contract_timestamp(raw: str) -> datetime | None:
    cleaned = raw.strip()
    if not cleaned:
        return None
    if len(cleaned) == 10 and "T" not in cleaned and " " not in cleaned:
        try:
            parsed_date = date.fromisoformat(cleaned)
        except ValueError:
            return None
        return datetime(parsed_date.year, parsed_date.month, parsed_date.day, tzinfo=UTC)
    normalized = f"{cleaned[:-1]}+00:00" if cleaned.endswith("Z") else cleaned
    try:
        parsed_dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed_dt.tzinfo is None or parsed_dt.utcoffset() is None:
        return None
    return parsed_dt.astimezone(UTC)


def _elapsed_days(start: datetime, end: datetime) -> float:
    return round((end - start).total_seconds() / 86400.0, 4)


@dataclass(frozen=True)
class BaselineCandidateRecord:
    property_id: str
    identified_at: str
    source_ref: str
    excluded_reason: str = ""
    cancelled_reason: str = ""
    withdrawn_reason: str = ""
    paused_reason: str = ""
    outcome_known: bool = True
    intended_energy_outcome_status: str = "pending_separate_measurement"


@dataclass(frozen=True)
class PropertyStageRecord:
    property_id: str
    stage_code: str
    entered_at: str
    exited_at: str = ""
    active_started_at: str = ""
    active_completed_at: str = ""
    source_ref: str = ""


@dataclass(frozen=True)
class PropertyEventRecord:
    property_id: str
    event: str
    occurred_at: str
    source_ref: str = ""


@dataclass(frozen=True)
class PropertyWaitRecord:
    property_id: str
    wait_state_code: str
    party: str
    started_at: str
    ended_at: str = ""
    cause_code: str = UNKNOWN
    source_ref: str = ""


@dataclass(frozen=True)
class PropertyReturnLoopRecord:
    property_id: str
    kind: str
    from_stage: str
    to_stage: str
    recorded_at: str
    rework_days: float | None = None
    unresolved: bool = False
    source_ref: str = ""


class FrozenDict[K, V](dict[K, V]):
    """Read-only dict subclass preserving dataclasses.asdict() and JSON serialization.

    Blocks standard Mapping item/attribute mutation and post-construction __init__.
    Low-level dict.__setitem__ bypasses on the C base type are caught by verify_digest()
    at validation and governance boundaries.
    """

    __slots__ = ("_frozen",)

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, map: Mapping[K, V], /) -> None: ...

    @overload
    def __init__(self, iterable: Iterable[tuple[K, V]], /) -> None: ...

    @overload
    def __init__(self, **kwargs: V) -> None: ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if getattr(self, "_frozen", False):
            raise TypeError("FrozenDict does not support re-initialization")
        super().__init__(*args, **kwargs)
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: object) -> NoReturn:
        raise TypeError("FrozenDict does not support attribute mutation")

    def __delattr__(self, name: str) -> NoReturn:
        raise TypeError("FrozenDict does not support attribute deletion")

    def __setitem__(self, key: K, value: V) -> NoReturn:
        raise TypeError("FrozenDict does not support item assignment")

    def __delitem__(self, key: K) -> NoReturn:
        raise TypeError("FrozenDict does not support item deletion")

    def clear(self) -> NoReturn:
        raise TypeError("FrozenDict does not support clear()")

    def pop(self, *args: object) -> NoReturn:
        raise TypeError("FrozenDict does not support pop()")

    def popitem(self) -> NoReturn:
        raise TypeError("FrozenDict does not support popitem()")

    def setdefault(self, *args: object) -> NoReturn:
        raise TypeError("FrozenDict does not support setdefault()")

    def update(self, *args: object, **kwargs: object) -> NoReturn:
        raise TypeError("FrozenDict does not support update()")

    def __ior__(self, other: object) -> NoReturn:  # type: ignore[misc]
        raise TypeError("FrozenDict does not support in-place merge")

    def __copy__(self) -> "FrozenDict[K, V]":
        return FrozenDict(self)

    def __deepcopy__(self, memo: dict[int, object]) -> "FrozenDict[K, V]":
        return FrozenDict((copy.deepcopy(k, memo), copy.deepcopy(v, memo)) for k, v in self.items())


def _freeze_value(value: object) -> object:
    if isinstance(value, Mapping):
        return FrozenDict((k, _freeze_value(v)) for k, v in value.items())
    if isinstance(value, (tuple, list)):
        return tuple(_freeze_value(item) for item in value)
    return value


_FLOW_REPORT_CONTAINER_FIELDS = (
    "baseline_candidate_ids",
    "zero_event_candidate_ids",
    "duplicate_candidate_ids",
    "state_counts",
    "accepted_handover_property_ids",
    "invalid_accepted_handover_ids",
    "intended_energy_outcome_counts",
    "bg011_assessment_to_ready_to_install_days",
    "candidate_to_accepted_handover_days",
    "post_install_handover_legs_days",
    "stage_metrics",
    "waits_by_party",
    "waits_by_state",
    "return_loops_by_property",
    "return_loop_totals",
    "explicit_rework_days_by_kind",
    "gaps",
)

_FLOW_REPORT_DIGEST_KEYS = (
    "window_start",
    "window_end",
    "as_of",
    "dictionary_schema_digest",
    "baseline_candidate_ids",
    "zero_event_candidate_ids",
    "duplicate_candidate_ids",
    "state_counts",
    "accepted_handover_property_ids",
    "invalid_accepted_handover_ids",
    "intended_energy_outcome_counts",
    "bg011_assessment_to_ready_to_install_days",
    "candidate_to_accepted_handover_days",
    "post_install_handover_legs_days",
    "stage_metrics",
    "waits_by_party",
    "waits_by_state",
    "return_loops_by_property",
    "return_loop_totals",
    "explicit_rework_days_by_kind",
    "gaps",
)

_FLOW_REPORT_SIGNATURE_KEYS = frozenset(
    k for k in _FLOW_REPORT_DIGEST_KEYS if k != "gaps"
) | frozenset({"calculation_digest"})

_EVALUATED_FLOW_REPORT_DIGESTS: set[str] = set()
_VALIDATED_FLOW_REPORT_SEALS: set[tuple[str, str, str, str, str]] = set()
_EVALUATED_FLOW_REPORT_REFS: dict[int, "weakref.ref[FlowDiscoveryReport]"] = {}
_ALLOW_VALIDATED_FLOW_REPORT_INIT: ContextVar[bool] = ContextVar(
    "_ALLOW_VALIDATED_FLOW_REPORT_INIT", default=False
)


def _register_evaluated_report(report: "FlowDiscoveryReport") -> None:
    oid = id(report)

    def _cleanup(_ref: "weakref.ref[FlowDiscoveryReport]") -> None:
        _EVALUATED_FLOW_REPORT_REFS.pop(oid, None)

    _EVALUATED_FLOW_REPORT_REFS[oid] = weakref.ref(report, _cleanup)
    _EVALUATED_FLOW_REPORT_DIGESTS.add(report.calculation_digest)


def _is_evaluated_report_instance(report: "FlowDiscoveryReport") -> bool:
    ref = _EVALUATED_FLOW_REPORT_REFS.get(id(report))
    return ref is not None and ref() is report


def _strict_iso_date(value: object, field_name: str) -> str:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str) and len(value) == 10:
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError as exc:
            raise GovernanceViolationError(
                f"Invalid ISO calendar date for {field_name}: {value!r}"
            ) from exc
    raise GovernanceViolationError(f"Expected calendar date or YYYY-MM-DD string for {field_name}")


def _compute_flow_report_digest(payload: Mapping[str, object]) -> str:
    try:
        schema_digest = payload.get("dictionary_schema_digest")
        if not isinstance(schema_digest, str) or not schema_digest.strip():
            raise GovernanceViolationError(
                "FlowDiscoveryReport payload missing required non-blank 'dictionary_schema_digest'"
            )
        canonical: dict[str, object] = {
            "window_start": _strict_iso_date(payload["window_start"], "window_start"),
            "window_end": _strict_iso_date(payload["window_end"], "window_end"),
            "as_of": _strict_iso_date(payload["as_of"], "as_of"),
            "dictionary_schema_digest": schema_digest,
        }
        for key in _FLOW_REPORT_CONTAINER_FIELDS:
            if key not in payload:
                raise GovernanceViolationError(
                    f"FlowDiscoveryReport payload missing required field '{key}'"
                )
            canonical[key] = _freeze_value(payload[key])
        encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except GovernanceViolationError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise GovernanceViolationError(
            "FlowDiscoveryReport payload failed canonical digest serialization"
        ) from exc
    return hashlib.sha256(encoded).hexdigest()


def _verify_report_matches_dictionary(
    report_or_mapping: "FlowDiscoveryReport | Mapping[str, object]",
    dictionary: LifecycleDictionary,
) -> None:
    expected_schema_digest = _dictionary_schema_digest(dictionary)
    if isinstance(report_or_mapping, FlowDiscoveryReport):
        actual_schema = report_or_mapping.dictionary_schema_digest
        stage_metrics: object = report_or_mapping.stage_metrics
        waits_by_state: object = report_or_mapping.waits_by_state
        loop_totals: object = report_or_mapping.return_loop_totals
        loops_by_prop: object = report_or_mapping.return_loops_by_property
    else:
        actual_schema = str(report_or_mapping.get("dictionary_schema_digest", ""))
        stage_metrics = report_or_mapping.get("stage_metrics", ())
        waits_by_state = report_or_mapping.get("waits_by_state", ())
        loop_totals = report_or_mapping.get("return_loop_totals", {})
        loops_by_prop = report_or_mapping.get("return_loops_by_property", {})

    if not actual_schema.strip() or actual_schema != expected_schema_digest:
        raise GovernanceViolationError(
            "FlowDiscoveryReport dictionary_schema_digest does not match LifecycleDictionary"
        )
    valid_stages = {s.code for s in dictionary.stages}
    valid_waits = {w.code for w in dictionary.wait_states}
    valid_loops = {r.kind for r in dictionary.return_loops}
    if isinstance(stage_metrics, Sequence):
        for row in stage_metrics:
            if isinstance(row, Mapping) and row.get("stage_code") not in valid_stages:
                raise GovernanceViolationError(
                    f"FlowDiscoveryReport stage_metrics contains unknown stage "
                    f"{row.get('stage_code')!r}"
                )
    if isinstance(waits_by_state, Sequence):
        for row in waits_by_state:
            if isinstance(row, Mapping) and row.get("wait_state_code") not in valid_waits:
                raise GovernanceViolationError(
                    f"FlowDiscoveryReport waits_by_state contains unknown wait state "
                    f"{row.get('wait_state_code')!r}"
                )
    if isinstance(loop_totals, Mapping):
        for kind in loop_totals:
            if kind not in valid_loops:
                raise GovernanceViolationError(
                    f"FlowDiscoveryReport return_loop_totals contains unknown loop kind {kind!r}"
                )
    if isinstance(loops_by_prop, Mapping):
        for prop_row in loops_by_prop.values():
            if isinstance(prop_row, Mapping):
                for kind in prop_row:
                    if kind not in valid_loops:
                        raise GovernanceViolationError(
                            f"FlowDiscoveryReport return_loops_by_property contains unknown loop "
                            f"kind {kind!r}"
                        )


@dataclass(frozen=True)
class FlowDiscoveryReport:
    window_start: date
    window_end: date
    as_of: date
    baseline_candidate_ids: tuple[str, ...]
    zero_event_candidate_ids: tuple[str, ...]
    duplicate_candidate_ids: tuple[str, ...]
    state_counts: dict[str, int]
    accepted_handover_property_ids: tuple[str, ...]
    invalid_accepted_handover_ids: tuple[str, ...]
    intended_energy_outcome_counts: dict[str, int]
    bg011_assessment_to_ready_to_install_days: dict[str, float | None]
    candidate_to_accepted_handover_days: dict[str, float | None]
    post_install_handover_legs_days: dict[str, dict[str, float | None]]
    stage_metrics: tuple[dict[str, object], ...]
    waits_by_party: tuple[dict[str, object], ...]
    waits_by_state: tuple[dict[str, object], ...]
    return_loops_by_property: dict[str, dict[str, int]]
    return_loop_totals: dict[str, int]
    explicit_rework_days_by_kind: dict[str, float]
    gaps: tuple[str, ...]
    owner_validated: bool = False
    finding_status: str = CANDIDATE_FINDING_STATUS
    owner_validated_by: str = ""
    owner_validated_on: date | None = None
    validation_note: str = ""
    notice: str = NOT_FINDING
    dictionary_schema_digest: str = ""
    calculation_digest: str = ""

    def _expected_digest(self) -> str:
        return _compute_flow_report_digest(
            {
                "window_start": self.window_start,
                "window_end": self.window_end,
                "as_of": self.as_of,
                "dictionary_schema_digest": self.dictionary_schema_digest,
                "baseline_candidate_ids": self.baseline_candidate_ids,
                "zero_event_candidate_ids": self.zero_event_candidate_ids,
                "duplicate_candidate_ids": self.duplicate_candidate_ids,
                "state_counts": self.state_counts,
                "accepted_handover_property_ids": self.accepted_handover_property_ids,
                "invalid_accepted_handover_ids": self.invalid_accepted_handover_ids,
                "intended_energy_outcome_counts": self.intended_energy_outcome_counts,
                "bg011_assessment_to_ready_to_install_days": (
                    self.bg011_assessment_to_ready_to_install_days
                ),
                "candidate_to_accepted_handover_days": self.candidate_to_accepted_handover_days,
                "post_install_handover_legs_days": self.post_install_handover_legs_days,
                "stage_metrics": self.stage_metrics,
                "waits_by_party": self.waits_by_party,
                "waits_by_state": self.waits_by_state,
                "return_loops_by_property": self.return_loops_by_property,
                "return_loop_totals": self.return_loop_totals,
                "explicit_rework_days_by_kind": self.explicit_rework_days_by_kind,
                "gaps": self.gaps,
            }
        )

    def verify_digest(self) -> None:
        """Raise GovernanceViolationError if calculation_digest is blank or tampered with."""
        if not isinstance(self.calculation_digest, str) or not self.calculation_digest.strip():
            raise GovernanceViolationError(
                "FlowDiscoveryReport is missing a verified calculation_digest"
            )
        if self.calculation_digest != self._expected_digest():
            raise GovernanceViolationError(
                "FlowDiscoveryReport calculation_digest mismatch indicates post-calculation "
                "tampering"
            )

    def to_json_dict(self) -> FrozenDict[str, object]:
        """Return a tamper-evident JSON-ready FrozenDict with ISO-8601 calendar dates.

        Cross-process consumers verify SHA-256 calculation_digest and
        dictionary_schema_digest via enforce_governance_guard(..., dictionary=dictionary).
        """
        raw = asdict(self)
        raw["window_start"] = self.window_start.isoformat()
        raw["window_end"] = self.window_end.isoformat()
        raw["as_of"] = self.as_of.isoformat()
        raw["owner_validated_on"] = (
            self.owner_validated_on.isoformat() if self.owner_validated_on is not None else None
        )
        return FrozenDict[str, object]((k, _freeze_value(v)) for k, v in raw.items())

    def __deepcopy__(self, memo: dict[int, object]) -> "FlowDiscoveryReport":
        self.verify_digest()
        kwargs: dict[str, Any] = {
            "window_start": copy.deepcopy(self.window_start, memo),
            "window_end": copy.deepcopy(self.window_end, memo),
            "as_of": copy.deepcopy(self.as_of, memo),
            "baseline_candidate_ids": copy.deepcopy(self.baseline_candidate_ids, memo),
            "zero_event_candidate_ids": copy.deepcopy(self.zero_event_candidate_ids, memo),
            "duplicate_candidate_ids": copy.deepcopy(self.duplicate_candidate_ids, memo),
            "state_counts": copy.deepcopy(self.state_counts, memo),
            "accepted_handover_property_ids": copy.deepcopy(
                self.accepted_handover_property_ids, memo
            ),
            "invalid_accepted_handover_ids": copy.deepcopy(
                self.invalid_accepted_handover_ids, memo
            ),
            "intended_energy_outcome_counts": copy.deepcopy(
                self.intended_energy_outcome_counts, memo
            ),
            "bg011_assessment_to_ready_to_install_days": copy.deepcopy(
                self.bg011_assessment_to_ready_to_install_days, memo
            ),
            "candidate_to_accepted_handover_days": copy.deepcopy(
                self.candidate_to_accepted_handover_days, memo
            ),
            "post_install_handover_legs_days": copy.deepcopy(
                self.post_install_handover_legs_days, memo
            ),
            "stage_metrics": copy.deepcopy(self.stage_metrics, memo),
            "waits_by_party": copy.deepcopy(self.waits_by_party, memo),
            "waits_by_state": copy.deepcopy(self.waits_by_state, memo),
            "return_loops_by_property": copy.deepcopy(self.return_loops_by_property, memo),
            "return_loop_totals": copy.deepcopy(self.return_loop_totals, memo),
            "explicit_rework_days_by_kind": copy.deepcopy(self.explicit_rework_days_by_kind, memo),
            "gaps": copy.deepcopy(self.gaps, memo),
            "owner_validated": self.owner_validated,
            "finding_status": self.finding_status,
            "owner_validated_by": self.owner_validated_by,
            "owner_validated_on": copy.deepcopy(self.owner_validated_on, memo),
            "validation_note": self.validation_note,
            "notice": self.notice,
            "dictionary_schema_digest": self.dictionary_schema_digest,
            "calculation_digest": self.calculation_digest,
        }
        if self.owner_validated:
            token = _ALLOW_VALIDATED_FLOW_REPORT_INIT.set(True)
            try:
                cloned = FlowDiscoveryReport(**kwargs)
            finally:
                _ALLOW_VALIDATED_FLOW_REPORT_INIT.reset(token)
        else:
            cloned = FlowDiscoveryReport(**kwargs)
        if _is_evaluated_report_instance(self):
            _register_evaluated_report(cloned)
        memo[id(self)] = cloned
        return cloned

    def __post_init__(self) -> None:
        for attr_name in _FLOW_REPORT_CONTAINER_FIELDS:
            object.__setattr__(self, attr_name, _freeze_value(getattr(self, attr_name)))
        self.verify_digest()
        if not self.owner_validated and self.finding_status == CANDIDATE_FINDING_STATUS:
            return
        if not _ALLOW_VALIDATED_FLOW_REPORT_INIT.get():
            raise GovernanceViolationError(
                "Owner-validated FlowDiscoveryReport instances can only be constructed via "
                "validate_flow_report"
            )
        if self.gaps:
            raise GovernanceViolationError(
                "FlowDiscoveryReport cannot claim owner validation while unresolved gaps remain"
            )
        if self.invalid_accepted_handover_ids:
            raise GovernanceViolationError(
                "FlowDiscoveryReport cannot claim owner validation with invalid accepted handovers"
            )
        if not (
            self.owner_validated
            and self.finding_status == VALIDATED_FINDING_STATUS
            and is_valid_human_actor(self.owner_validated_by)
            and self.owner_validated_on is not None
            and not isinstance(self.owner_validated_on, datetime)
            and bool(self.validation_note.strip())
            and bool(self.dictionary_schema_digest.strip())
        ):
            raise GovernanceViolationError(
                "FlowDiscoveryReport cannot claim owner validation without formal human sign-off"
            )
        seal = (
            self.calculation_digest,
            self.dictionary_schema_digest,
            self.owner_validated_by.strip(),
            self.owner_validated_on.isoformat(),
            self.validation_note.strip(),
        )
        if (
            self.calculation_digest not in _EVALUATED_FLOW_REPORT_DIGESTS
            or seal not in _VALIDATED_FLOW_REPORT_SEALS
        ):
            raise GovernanceViolationError(
                "FlowDiscoveryReport cannot claim owner validation without evaluated calculation "
                "provenance and validate_flow_report sign-off"
            )


def evaluate_property_flow(
    dictionary: LifecycleDictionary,
    *,
    window_start: date,
    window_end: date,
    as_of: date,
    candidates: Sequence[BaselineCandidateRecord],
    stage_records: Sequence[PropertyStageRecord] = (),
    event_records: Sequence[PropertyEventRecord] = (),
    wait_records: Sequence[PropertyWaitRecord] = (),
    loop_records: Sequence[PropertyReturnLoopRecord] = (),
) -> FlowDiscoveryReport:
    """Evaluate baseline population, PAS 2035 stages, BG-011/handover legs, waits and loops."""
    if window_end < window_start:
        raise ValueError("window_end cannot precede window_start")
    if as_of < window_start:
        raise ValueError("as_of cut-off date cannot precede window_start")

    gaps: list[str] = []
    valid_stages = {s.code for s in dictionary.stages}
    valid_events = {e.event for e in dictionary.events}
    valid_waits = {w.code for w in dictionary.wait_states}
    valid_loops = {r.kind for r in dictionary.return_loops}
    as_of_dt = datetime(as_of.year, as_of.month, as_of.day, tzinfo=UTC)

    in_window: list[BaselineCandidateRecord] = []
    for cand in candidates:
        if not cand.source_ref.strip():
            gaps.append(f"Candidate {cand.property_id} is missing source_ref")
        ident_dt = _parse_contract_timestamp(cand.identified_at)
        if ident_dt is None:
            gaps.append(
                f"Candidate {cand.property_id} has unusable identified_at '{cand.identified_at}'"
            )
            continue
        if ident_dt.date() > as_of:
            gaps.append(
                f"Candidate {cand.property_id} identified_at '{cand.identified_at}' is after "
                f"as_of '{as_of.isoformat()}'"
            )
            continue
        if window_start <= ident_dt.date() <= window_end:
            in_window.append(cand)

    id_counts = Counter(c.property_id for c in in_window)
    duplicate_ids = tuple(sorted(pid for pid, n in id_counts.items() if n > 1))
    baseline_ids = tuple(dict.fromkeys(c.property_id for c in in_window))
    baseline_id_set = set(baseline_ids)
    state_counts = {
        "in_window_candidates": len(in_window),
        "paused": sum(bool(c.paused_reason.strip()) for c in in_window),
        "excluded": sum(bool(c.excluded_reason.strip()) for c in in_window),
        "cancelled": sum(bool(c.cancelled_reason.strip()) for c in in_window),
        "withdrawn": sum(bool(c.withdrawn_reason.strip()) for c in in_window),
        "open_outcome_unknown": sum(not c.outcome_known for c in in_window),
    }
    energy_counts = dict(
        Counter(c.intended_energy_outcome_status.strip() or "unspecified" for c in in_window)
    )

    events_by_prop: dict[str, dict[str, datetime]] = {}
    props_with_lifecycle_events: set[str] = set()
    for ev in event_records:
        if ev.property_id not in baseline_id_set:
            gaps.append(
                f"Property {ev.property_id} event '{ev.event}' is outside baseline_candidate_ids"
            )
            continue
        if ev.event not in valid_events:
            gaps.append(f"Property {ev.property_id} has unknown lifecycle event '{ev.event}'")
            continue
        if not ev.source_ref.strip():
            gaps.append(f"Property {ev.property_id} event '{ev.event}' is missing source_ref")
        occ = _parse_contract_timestamp(ev.occurred_at)
        if occ is None:
            gaps.append(
                f"Property {ev.property_id} event '{ev.event}' has unusable timestamp "
                f"'{ev.occurred_at}'"
            )
            continue
        if occ.date() > as_of:
            gaps.append(
                f"Property {ev.property_id} event '{ev.event}' occurred_at '{ev.occurred_at}' "
                f"is after as_of '{as_of.isoformat()}'"
            )
            continue
        props_with_lifecycle_events.add(ev.property_id)
        prop_events = events_by_prop.setdefault(ev.property_id, {})
        if ev.event not in prop_events or occ < prop_events[ev.event]:
            prop_events[ev.event] = occ

    stage_rows: list[dict[str, object]] = []
    for st in stage_records:
        if st.property_id not in baseline_id_set:
            gaps.append(
                f"Property {st.property_id} stage '{st.stage_code}' is outside "
                "baseline_candidate_ids"
            )
            continue
        if st.stage_code not in valid_stages:
            gaps.append(f"Property {st.property_id} has unknown stage '{st.stage_code}'")
            continue
        if not st.source_ref.strip():
            gaps.append(f"Property {st.property_id} stage '{st.stage_code}' is missing source_ref")
        ent = _parse_contract_timestamp(st.entered_at)
        if ent is None:
            gaps.append(
                f"Property {st.property_id} stage '{st.stage_code}' has unusable entered_at "
                f"'{st.entered_at}'"
            )
            continue
        if ent.date() > as_of:
            gaps.append(
                f"Property {st.property_id} stage '{st.stage_code}' entered_at "
                f"'{st.entered_at}' is after as_of '{as_of.isoformat()}'"
            )
            continue
        if st.exited_at.strip():
            ext = _parse_contract_timestamp(st.exited_at)
            if ext is None:
                gaps.append(
                    f"Property {st.property_id} stage '{st.stage_code}' has unusable exited_at "
                    f"'{st.exited_at}'"
                )
                calendar_days: float | None = None
            elif ext.date() > as_of:
                gaps.append(
                    f"Property {st.property_id} stage '{st.stage_code}' exited_at "
                    f"'{st.exited_at}' is after as_of '{as_of.isoformat()}'"
                )
                continue
            elif ext < ent:
                gaps.append(
                    f"Property {st.property_id} stage '{st.stage_code}' exited before entry"
                )
                calendar_days = None
            else:
                calendar_days = _elapsed_days(ent, ext)
        else:
            calendar_days = _elapsed_days(ent, max(as_of_dt, ent))

        active_days: float | None = None
        if st.active_started_at.strip() or st.active_completed_at.strip():
            act_s = (
                _parse_contract_timestamp(st.active_started_at)
                if st.active_started_at.strip()
                else None
            )
            act_e = (
                _parse_contract_timestamp(st.active_completed_at)
                if st.active_completed_at.strip()
                else None
            )
            if (act_s is not None and act_s.date() > as_of) or (
                act_e is not None and act_e.date() > as_of
            ):
                gaps.append(
                    f"Property {st.property_id} stage '{st.stage_code}' active-work timestamp "
                    f"is after as_of '{as_of.isoformat()}'"
                )
                continue
            if act_s is None or act_e is None:
                gaps.append(
                    f"Property {st.property_id} stage '{st.stage_code}' has incomplete or "
                    "unusable active-work timestamps; active_days kept None"
                )
            elif act_e < act_s:
                gaps.append(
                    f"Property {st.property_id} stage '{st.stage_code}' active work ended "
                    "before active work started"
                )
            else:
                active_days = _elapsed_days(act_s, act_e)

        stage_rows.append(
            dict(
                property_id=st.property_id,
                stage_code=st.stage_code,
                open_stage=not bool(st.exited_at.strip()),
                calendar_days=calendar_days,
                active_days=active_days,
            )
        )

    party_days: Counter[str] = Counter()
    party_open: Counter[str] = Counter()
    party_unknown_cause: Counter[str] = Counter()
    party_disputed_cause: Counter[str] = Counter()
    party_unknown: Counter[str] = Counter()
    state_wait_days: Counter[str] = Counter()
    state_wait_open: Counter[str] = Counter()
    for wt in wait_records:
        if wt.property_id not in baseline_id_set:
            gaps.append(
                f"Property {wt.property_id} wait '{wt.wait_state_code}' is outside "
                "baseline_candidate_ids"
            )
            continue
        if wt.wait_state_code not in valid_waits:
            gaps.append(f"Property {wt.property_id} has unknown wait state '{wt.wait_state_code}'")
            continue
        if not wt.source_ref.strip():
            gaps.append(
                f"Property {wt.property_id} wait '{wt.wait_state_code}' is missing source_ref"
            )
        ws = _parse_contract_timestamp(wt.started_at)
        if ws is None:
            gaps.append(
                f"Property {wt.property_id} wait '{wt.wait_state_code}' has unusable started_at"
            )
            continue
        if ws.date() > as_of:
            gaps.append(
                f"Property {wt.property_id} wait '{wt.wait_state_code}' started_at "
                f"'{wt.started_at}' is after as_of '{as_of.isoformat()}'"
            )
            continue
        if wt.ended_at.strip():
            we = _parse_contract_timestamp(wt.ended_at)
            if we is None:
                gaps.append(
                    f"Property {wt.property_id} wait '{wt.wait_state_code}' has unusable ended_at"
                )
                continue
            if we.date() > as_of:
                gaps.append(
                    f"Property {wt.property_id} wait '{wt.wait_state_code}' ended_at "
                    f"'{wt.ended_at}' is after as_of '{as_of.isoformat()}'"
                )
                continue
        else:
            we = max(as_of_dt, ws)
        if we < ws:
            gaps.append(f"Property {wt.property_id} wait '{wt.wait_state_code}' ended before start")
            continue
        dur = _elapsed_days(ws, we)
        party = wt.party.strip() or UNATTRIBUTED
        cause = wt.cause_code.strip()
        is_unknown_cause = cause in (UNKNOWN, "")
        is_disputed_cause = cause == WAIT_CAUSE_DISPUTED
        party_days[party] += dur  # type: ignore[assignment]
        party_open[party] += not bool(wt.ended_at.strip())
        party_unknown_cause[party] += is_unknown_cause
        party_disputed_cause[party] += is_disputed_cause
        party_unknown[party] += is_unknown_cause or is_disputed_cause
        state_wait_days[wt.wait_state_code] += dur  # type: ignore[assignment]
        state_wait_open[wt.wait_state_code] += not bool(wt.ended_at.strip())

    loops_by_prop: dict[str, dict[str, int]] = {}
    rework_by_kind: dict[str, float] = dict.fromkeys(REQUIRED_RETURN_LOOP_KINDS, 0.0)
    unresolved_reopen_after: dict[str, list[datetime]] = {}
    for lp in loop_records:
        if lp.property_id not in baseline_id_set:
            gaps.append(
                f"Property {lp.property_id} loop '{lp.kind}' is outside baseline_candidate_ids"
            )
            continue
        if lp.kind not in valid_loops:
            gaps.append(f"Property {lp.property_id} has unknown return loop kind '{lp.kind}'")
            continue
        if lp.from_stage not in valid_stages or lp.to_stage not in valid_stages:
            gaps.append(
                f"Property {lp.property_id} loop '{lp.kind}' references unknown stage "
                f"'{lp.from_stage}' -> '{lp.to_stage}'"
            )
            continue
        if not lp.source_ref.strip():
            gaps.append(f"Property {lp.property_id} loop '{lp.kind}' is missing source_ref")
        lp_dt = _parse_contract_timestamp(lp.recorded_at)
        if lp_dt is None:
            gaps.append(
                f"Property {lp.property_id} loop '{lp.kind}' has unusable recorded_at "
                f"'{lp.recorded_at}'"
            )
            continue
        if lp_dt.date() > as_of:
            gaps.append(
                f"Property {lp.property_id} loop '{lp.kind}' recorded_at '{lp.recorded_at}' "
                f"is after as_of '{as_of.isoformat()}'"
            )
            continue
        prop_loop = loops_by_prop.setdefault(
            lp.property_id, dict.fromkeys(REQUIRED_RETURN_LOOP_KINDS, 0)
        )
        prop_loop[lp.kind] += 1
        if lp.rework_days is not None:
            if lp.rework_days < 0:
                gaps.append(f"Property {lp.property_id} loop '{lp.kind}' has negative rework_days")
            else:
                rework_by_kind[lp.kind] = round(rework_by_kind[lp.kind] + lp.rework_days, 4)
        if lp.kind == "reopen" and lp.unresolved:
            unresolved_reopen_after.setdefault(lp.property_id, []).append(lp_dt)

    zero_event_ids = tuple(pid for pid in baseline_ids if pid not in props_with_lifecycle_events)

    bg011_days: dict[str, float | None] = {}
    e2e_days: dict[str, float | None] = {}
    handover_legs: dict[str, dict[str, float | None]] = {}
    accepted_ids: list[str] = []
    invalid_accepted_ids: list[str] = []

    for pid in baseline_ids:
        pev = events_by_prop.get(pid, {})
        bg011_days[pid] = _pair_leg_days(
            pid,
            pev,
            "retrofit assessment completed",
            "ready to install",
            gaps,
        )
        legs_for_prop: dict[str, float | None] = {}
        for label, start_ev, end_ev in POST_INSTALL_HANDOVER_LEGS:
            legs_for_prop[label] = _pair_leg_days(pid, pev, start_ev, end_ev, gaps)
        handover_legs[pid] = legs_for_prop

        handover_dt = pev.get("accepted handover")
        if handover_dt is None:
            e2e_days[pid] = None
            continue
        missing_prereqs = [
            req
            for req in ACCEPTED_HANDOVER_PREREQUISITE_EVENTS
            if req not in pev or pev[req] > handover_dt
        ]
        open_reopens = [dt for dt in unresolved_reopen_after.get(pid, []) if dt >= handover_dt]
        if missing_prereqs or open_reopens:
            invalid_accepted_ids.append(pid)
            e2e_days[pid] = None
            if missing_prereqs:
                gaps.append(
                    f"Property {pid} recorded accepted handover without prerequisite events: "
                    f"{', '.join(missing_prereqs)}"
                )
            if open_reopens:
                gaps.append(
                    f"Property {pid} has unresolved post-handover reopen blocking accepted handover"
                )
        else:
            accepted_ids.append(pid)
            e2e_days[pid] = _pair_leg_days(
                pid, pev, "candidate selection", "accepted handover", gaps
            )

    waits_party_rows = tuple(
        dict(
            party=party,
            days=round(float(days_val), 4),
            open_waits=party_open[party],
            unknown_cause_count=party_unknown_cause[party],
            disputed_cause_count=party_disputed_cause[party],
            unknown_or_disputed_count=party_unknown[party],
            unknown_or_disputed_cause=party_unknown[party],
        )
        for party, days_val in sorted(party_days.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    waits_state_rows = tuple(
        dict(
            wait_state_code=code,
            days=round(float(days_val), 4),
            open_waits=state_wait_open[code],
        )
        for code, days_val in sorted(state_wait_days.items(), key=lambda kv: (-kv[1], kv[0]))
    )
    loop_totals = {
        kind: sum(row[kind] for row in loops_by_prop.values())
        for kind in REQUIRED_RETURN_LOOP_KINDS
    }

    accepted_handover_tuple = tuple(accepted_ids)
    invalid_handover_tuple = tuple(invalid_accepted_ids)
    stage_metrics_tuple = tuple(stage_rows)
    gaps_tuple = tuple(gaps)
    schema_digest = _dictionary_schema_digest(dictionary)
    digest = _compute_flow_report_digest(
        {
            "window_start": window_start,
            "window_end": window_end,
            "as_of": as_of,
            "dictionary_schema_digest": schema_digest,
            "baseline_candidate_ids": baseline_ids,
            "zero_event_candidate_ids": zero_event_ids,
            "duplicate_candidate_ids": duplicate_ids,
            "state_counts": state_counts,
            "accepted_handover_property_ids": accepted_handover_tuple,
            "invalid_accepted_handover_ids": invalid_handover_tuple,
            "intended_energy_outcome_counts": energy_counts,
            "bg011_assessment_to_ready_to_install_days": bg011_days,
            "candidate_to_accepted_handover_days": e2e_days,
            "post_install_handover_legs_days": handover_legs,
            "stage_metrics": stage_metrics_tuple,
            "waits_by_party": waits_party_rows,
            "waits_by_state": waits_state_rows,
            "return_loops_by_property": loops_by_prop,
            "return_loop_totals": loop_totals,
            "explicit_rework_days_by_kind": rework_by_kind,
            "gaps": gaps_tuple,
        }
    )
    report = FlowDiscoveryReport(
        window_start=window_start,
        window_end=window_end,
        as_of=as_of,
        baseline_candidate_ids=baseline_ids,
        zero_event_candidate_ids=zero_event_ids,
        duplicate_candidate_ids=duplicate_ids,
        state_counts=state_counts,
        accepted_handover_property_ids=accepted_handover_tuple,
        invalid_accepted_handover_ids=invalid_handover_tuple,
        intended_energy_outcome_counts=energy_counts,
        bg011_assessment_to_ready_to_install_days=bg011_days,
        candidate_to_accepted_handover_days=e2e_days,
        post_install_handover_legs_days=handover_legs,
        stage_metrics=stage_metrics_tuple,
        waits_by_party=waits_party_rows,
        waits_by_state=waits_state_rows,
        return_loops_by_property=loops_by_prop,
        return_loop_totals=loop_totals,
        explicit_rework_days_by_kind=rework_by_kind,
        gaps=gaps_tuple,
        dictionary_schema_digest=schema_digest,
        calculation_digest=digest,
    )
    _register_evaluated_report(report)
    return report


def _pair_leg_days(
    property_id: str,
    prop_events: Mapping[str, datetime],
    start_event: str,
    end_event: str,
    gaps: list[str],
) -> float | None:
    if start_event not in prop_events or end_event not in prop_events:
        return None
    start_dt = prop_events[start_event]
    end_dt = prop_events[end_event]
    if end_dt < start_dt:
        gaps.append(f"Property {property_id} recorded '{end_event}' before '{start_event}'")
        return None
    return _elapsed_days(start_dt, end_dt)


def validate_flow_report(
    report: FlowDiscoveryReport,
    discovery_owner: NominatedDiscoveryOwner,
    dictionary: LifecycleDictionary,
    *,
    by: str,
    on: date,
    note: str,
) -> FlowDiscoveryReport:
    report.verify_digest()
    if (
        not _is_evaluated_report_instance(report)
        or report.calculation_digest not in _EVALUATED_FLOW_REPORT_DIGESTS
    ):
        raise GovernanceViolationError(
            "FlowDiscoveryReport must originate directly from evaluate_property_flow before "
            "owner validation"
        )
    if report.gaps:
        raise GovernanceViolationError("FlowDiscoveryReport still records unresolved gaps")
    if report.invalid_accepted_handover_ids:
        raise GovernanceViolationError("FlowDiscoveryReport records invalid accepted handovers")
    if not isinstance(on, date) or isinstance(on, datetime):
        raise GovernanceViolationError(
            "FlowDiscoveryReport validation date must be a calendar date"
        )
    actor, cleaned_note = _require_ready_owner_and_dictionary(discovery_owner, dictionary, by, note)
    _verify_report_matches_dictionary(report, dictionary)
    seal = (
        report.calculation_digest,
        report.dictionary_schema_digest,
        actor,
        on.isoformat(),
        cleaned_note,
    )
    _VALIDATED_FLOW_REPORT_SEALS.add(seal)
    token = _ALLOW_VALIDATED_FLOW_REPORT_INIT.set(True)
    try:
        validated = replace(
            report,
            owner_validated=True,
            finding_status=VALIDATED_FINDING_STATUS,
            owner_validated_by=actor,
            owner_validated_on=on,
            validation_note=cleaned_note,
            notice="",
            dictionary_schema_digest=report.dictionary_schema_digest,
            calculation_digest=report.calculation_digest,
        )
    finally:
        _ALLOW_VALIDATED_FLOW_REPORT_INIT.reset(token)
    _register_evaluated_report(validated)
    return validated


@dataclass(frozen=True)
class EvidenceRecord:
    statement: str
    source_ref: str
    direction: str
    recorded_by: str

    def __post_init__(self) -> None:
        if self.direction not in (SUPPORTS, CONTRADICTS):
            raise ValueError(f"Evidence direction must be '{SUPPORTS}' or '{CONTRADICTS}'")
        if not (self.statement.strip() and self.source_ref.strip()):
            raise ValueError("EvidenceRecord requires non-blank statement and source_ref")
        _require_human_actor(self.recorded_by, "Evidence recorder")


@dataclass(frozen=True)
class ConstraintTestAssessment:
    material_critical_path_share: bool = False
    affects_multiple_properties: bool = False
    recurs_across_comparable_cases: bool = False
    traceable_owner_or_dependency: bool = False
    changes_operational_or_investment_decision: bool = False

    @property
    def passes_all(self) -> bool:
        return (
            self.material_critical_path_share
            and self.affects_multiple_properties
            and self.recurs_across_comparable_cases
            and self.traceable_owner_or_dependency
            and self.changes_operational_or_investment_decision
        )

    def failed_criteria(self) -> tuple[str, ...]:
        checks = (
            ("material_critical_path_share", self.material_critical_path_share),
            ("affects_multiple_properties", self.affects_multiple_properties),
            ("recurs_across_comparable_cases", self.recurs_across_comparable_cases),
            ("traceable_owner_or_dependency", self.traceable_owner_or_dependency),
            (
                "changes_operational_or_investment_decision",
                self.changes_operational_or_investment_decision,
            ),
        )
        return tuple(name for name, ok in checks if not ok)


@dataclass(frozen=True)
class ConstraintHypothesis:
    rank: int
    code: str
    summary: str
    intervention_class: str
    domain_owner_roles: tuple[str, ...]
    proposed_by: str
    supporting_evidence: tuple[EvidenceRecord, ...] = ()
    contradicting_evidence: tuple[EvidenceRecord, ...] = ()
    constraint_test: ConstraintTestAssessment = ConstraintTestAssessment()
    review_status: str = PROPOSED
    domain_validated_by: str = ""
    domain_validated_role: str = ""
    domain_validated_on: date | None = None
    discovery_owner_validated_by: str = ""
    discovery_owner_validated_on: date | None = None
    decision_note: str = ""
    owner_validated: bool = False
    finding_status: str = CANDIDATE_FINDING_STATUS

    def __post_init__(self) -> None:
        if self.rank < 1:
            raise ValueError("ConstraintHypothesis rank must be >= 1")
        if not (self.code.strip() and self.summary.strip() and self.domain_owner_roles):
            raise ValueError("ConstraintHypothesis requires code, summary and domain_owner_roles")
        if not self.proposed_by.strip():
            raise ValueError("ConstraintHypothesis requires proposed_by")
        if any(item.direction != SUPPORTS for item in self.supporting_evidence):
            raise ValueError("supporting_evidence may contain only 'supports' EvidenceRecord items")
        if any(item.direction != CONTRADICTS for item in self.contradicting_evidence):
            raise ValueError(
                "contradicting_evidence may contain only 'contradicts' EvidenceRecord items"
            )
        if self.review_status not in (PROPOSED, DOMAIN_VALIDATED, OWNER_VALIDATED, DISPUTED):
            raise ValueError(f"Unsupported review_status '{self.review_status}'")

        if (
            not self.owner_validated
            and self.finding_status == CANDIDATE_FINDING_STATUS
            and self.review_status != OWNER_VALIDATED
        ):
            return

        if not (
            self.owner_validated
            and self.finding_status == VALIDATED_FINDING_STATUS
            and self.review_status == OWNER_VALIDATED
            and bool(self.supporting_evidence)
            and bool(self.contradicting_evidence)
            and self.constraint_test.passes_all
            and self.domain_validated_role in self.domain_owner_roles
            and is_valid_human_actor(self.domain_validated_by)
            and self.domain_validated_on is not None
            and self.domain_validated_by.strip().lower() != self.proposed_by.strip().lower()
            and is_valid_human_actor(self.discovery_owner_validated_by)
            and self.discovery_owner_validated_on is not None
            and self.discovery_owner_validated_by.strip().lower()
            != self.proposed_by.strip().lower()
            and bool(self.decision_note.strip())
        ):
            raise GovernanceViolationError(
                f"ConstraintHypothesis {self.code} cannot claim owner_validated=True or "
                f"finding_status='{self.finding_status}' without both supporting_evidence and "
                "contradicting_evidence, all five constraint-test criteria, domain-owner "
                "acceptance, and nominated human discovery-owner validation"
            )


def constraint_evidence_gaps(hypothesis: ConstraintHypothesis) -> list[str]:
    gaps: list[str] = []
    if not hypothesis.supporting_evidence:
        gaps.append(f"{hypothesis.code}: record supporting_evidence with traceable source_ref")
    if not hypothesis.contradicting_evidence:
        gaps.append(
            f"{hypothesis.code}: record contradicting_evidence (or a searched counter-evidence "
            "extract record with direction='contradicts' and traceable source_ref)"
        )
    return gaps


def record_supporting_evidence(
    hypothesis: ConstraintHypothesis, item: EvidenceRecord
) -> ConstraintHypothesis:
    if hypothesis.review_status != PROPOSED:
        raise ValueError("Cannot append evidence after domain or owner decision; open a new item")
    if item.direction != SUPPORTS:
        raise ValueError("record_supporting_evidence requires direction='supports'")
    return replace(hypothesis, supporting_evidence=hypothesis.supporting_evidence + (item,))


def record_contradicting_evidence(
    hypothesis: ConstraintHypothesis, item: EvidenceRecord
) -> ConstraintHypothesis:
    if hypothesis.review_status != PROPOSED:
        raise ValueError("Cannot append evidence after domain or owner decision; open a new item")
    if item.direction != CONTRADICTS:
        raise ValueError("record_contradicting_evidence requires direction='contradicts'")
    return replace(hypothesis, contradicting_evidence=hypothesis.contradicting_evidence + (item,))


def assess_constraint_test(
    hypothesis: ConstraintHypothesis, assessment: ConstraintTestAssessment
) -> ConstraintHypothesis:
    if hypothesis.review_status != PROPOSED:
        raise ValueError("Cannot modify constraint_test after domain or owner decision")
    return replace(hypothesis, constraint_test=assessment)


def validate_constraint_by_domain_owner(
    hypothesis: ConstraintHypothesis,
    *,
    validator: str,
    role: str,
    on: date,
    accept: bool,
    note: str,
) -> ConstraintHypothesis:
    """Record domain-owner acceptance or dispute; remains a candidate until discovery-owner gate."""
    if role not in hypothesis.domain_owner_roles:
        allowed = " or ".join(hypothesis.domain_owner_roles)
        raise ValueError(f"{hypothesis.code} must be decided by {allowed}, not {role}")
    actor = _require_human_actor(validator, "Domain owner validator")
    if actor.lower() == hypothesis.proposed_by.strip().lower():
        raise ValueError("Proposing analyst cannot validate their own constraint hypothesis")
    cleaned_note = _require_non_blank(note, "Domain decision note")
    ev_gaps = constraint_evidence_gaps(hypothesis)
    if ev_gaps:
        raise ValueError("; ".join(ev_gaps))
    if accept and not hypothesis.constraint_test.passes_all:
        failed = ", ".join(hypothesis.constraint_test.failed_criteria())
        raise ValueError(f"{hypothesis.code} failed five-part constraint test criteria: {failed}")
    return replace(
        hypothesis,
        review_status=DOMAIN_VALIDATED if accept else DISPUTED,
        domain_validated_by=actor,
        domain_validated_role=role,
        domain_validated_on=on,
        decision_note=cleaned_note,
        owner_validated=False,
        finding_status=CANDIDATE_FINDING_STATUS,
    )


def validate_constraint_by_discovery_owner(
    hypothesis: ConstraintHypothesis,
    discovery_owner: NominatedDiscoveryOwner,
    dictionary: LifecycleDictionary,
    *,
    by: str,
    on: date,
    note: str,
) -> ConstraintHypothesis:
    """Promote a domain-validated hypothesis to an owner-validated company finding."""
    actor, cleaned_note = _require_ready_owner_and_dictionary(discovery_owner, dictionary, by, note)
    if actor.lower() == hypothesis.proposed_by.strip().lower():
        raise GovernanceViolationError(
            "Proposing analyst cannot record discovery-owner validation on their own hypothesis"
        )
    if hypothesis.review_status == DISPUTED:
        raise GovernanceViolationError(
            f"Disputed hypothesis {hypothesis.code} must remain visible as a non-finding"
        )
    if hypothesis.review_status != DOMAIN_VALIDATED:
        raise GovernanceViolationError(
            f"Hypothesis {hypothesis.code} requires domain-owner validation before owner sign-off"
        )
    ev_gaps = constraint_evidence_gaps(hypothesis)
    if ev_gaps:
        raise GovernanceViolationError("; ".join(ev_gaps))
    if not hypothesis.constraint_test.passes_all:
        raise GovernanceViolationError(
            f"Hypothesis {hypothesis.code} must pass all five constraint-test criteria"
        )
    return replace(
        hypothesis,
        review_status=OWNER_VALIDATED,
        discovery_owner_validated_by=actor,
        discovery_owner_validated_on=on,
        decision_note=cleaned_note,
        owner_validated=True,
        finding_status=VALIDATED_FINDING_STATUS,
    )


@dataclass(frozen=True)
class RankedConstraintRegister:
    hypotheses: tuple[ConstraintHypothesis, ...]
    owner_validated: bool = False
    finding_status: str = CANDIDATE_FINDING_STATUS
    owner_validated_by: str = ""
    owner_validated_on: date | None = None
    validation_note: str = ""
    notice: str = NOT_FINDING

    def __post_init__(self) -> None:
        ranks = [h.rank for h in self.hypotheses]
        if ranks != list(range(1, len(self.hypotheses) + 1)):
            raise ValueError("RankedConstraintRegister hypotheses must have contiguous ranks 1..N")
        codes = [h.code for h in self.hypotheses]
        if len(set(codes)) != len(codes):
            raise ValueError("RankedConstraintRegister constraint codes must be unique")

        if not self.owner_validated and self.finding_status == CANDIDATE_FINDING_STATUS:
            return

        if not (
            self.owner_validated
            and self.finding_status == VALIDATED_FINDING_STATUS
            and bool(self.hypotheses)
            and is_valid_human_actor(self.owner_validated_by)
            and self.owner_validated_on is not None
            and bool(self.validation_note.strip())
        ):
            raise GovernanceViolationError(
                "RankedConstraintRegister cannot claim owner validation without formal sign-off"
            )

        for item in self.hypotheses:
            if constraint_evidence_gaps(item):
                raise GovernanceViolationError(
                    f"Register hypothesis {item.code} is missing two-sided evidence"
                )
            if item.review_status in (PROPOSED, DOMAIN_VALIDATED):
                raise GovernanceViolationError(
                    f"Register hypothesis {item.code} remains unadjudicated ({item.review_status})"
                )
            if item.review_status == DISPUTED and (
                item.owner_validated or item.finding_status != CANDIDATE_FINDING_STATUS
            ):
                raise GovernanceViolationError(
                    f"Disputed hypothesis {item.code} must retain candidate non-finding status"
                )
            if item.review_status == OWNER_VALIDATED and (
                not item.owner_validated
                or item.discovery_owner_validated_by.strip() != self.owner_validated_by.strip()
            ):
                raise GovernanceViolationError(
                    f"Validated hypothesis {item.code} must match register discovery owner"
                )

    def to_rows(self) -> list[dict[str, object]]:
        return [
            dict(
                rank=h.rank,
                code=h.code,
                summary=h.summary,
                intervention_class=h.intervention_class,
                review_status=h.review_status,
                supporting_count=len(h.supporting_evidence),
                contradicting_count=len(h.contradicting_evidence),
                supporting_evidence=tuple(asdict(e) for e in h.supporting_evidence),
                contradicting_evidence=tuple(asdict(e) for e in h.contradicting_evidence),
                passes_constraint_test=h.constraint_test.passes_all,
                evidence_gaps=tuple(constraint_evidence_gaps(h)),
                owner_validated=h.owner_validated,
                finding_status=h.finding_status,
            )
            for h in self.hypotheses
        ]


def build_seed_constraint_register() -> RankedConstraintRegister:
    """Build the five ranked Phase 0 candidate constraint hypotheses in unvalidated state."""
    return RankedConstraintRegister(
        hypotheses=(
            ConstraintHypothesis(
                rank=1,
                code="CAP",
                summary="Supplier or professional capacity",
                intervention_class="Framework allocation, call-off pacing or specialist panels",
                domain_owner_roles=("Procurement and Contracts",),
                proposed_by=SEED_PROPOSER,
            ),
            ConstraintHypothesis(
                rank=2,
                code="HANDOFF",
                summary="Unaccepted handoffs and approval queues",
                intervention_class="Explicit handoff ownership, SLA visibility and queue triage",
                domain_owner_roles=("Retrofit Programme Manager",),
                proposed_by=SEED_PROPOSER,
            ),
            ConstraintHypothesis(
                rank=3,
                code="RESIDENT",
                summary="Resident access, adjustment and decision readiness",
                intervention_class="Accessible engagement, adjustment capture and flexible booking",
                domain_owner_roles=("Resident Engagement and Housing",),
                proposed_by=SEED_PROPOSER,
            ),
            ConstraintHypothesis(
                rank=4,
                code="DEPEND",
                summary="Property, building-safety or maintenance dependencies",
                intervention_class="Upfront hazard/fabric triage and enabling-works sequencing",
                domain_owner_roles=("Building Safety, Repairs and Assets",),
                proposed_by=SEED_PROPOSER,
            ),
            ConstraintHypothesis(
                rank=5,
                code="QUALITY",
                summary="Physical or documentary quality failure",
                intervention_class="Right-first-time check-sheets and PAS 2035 evidence gates",
                domain_owner_roles=("Programme and independent quality owner",),
                proposed_by=SEED_PROPOSER,
            ),
        )
    )


def validate_constraint_register(
    register: RankedConstraintRegister,
    discovery_owner: NominatedDiscoveryOwner,
    dictionary: LifecycleDictionary,
    *,
    by: str,
    on: date,
    note: str,
) -> RankedConstraintRegister:
    """Validate an adjudicated register while keeping any DISPUTED items as non-findings."""
    actor, cleaned_note = _require_ready_owner_and_dictionary(discovery_owner, dictionary, by, note)
    promoted: list[ConstraintHypothesis] = []
    for item in register.hypotheses:
        if item.review_status == PROPOSED:
            raise GovernanceViolationError(
                f"Cannot validate register while hypothesis {item.code} is still PROPOSED"
            )
        if item.review_status == DISPUTED:
            ev_gaps = constraint_evidence_gaps(item)
            if ev_gaps:
                raise GovernanceViolationError("; ".join(ev_gaps))
            promoted.append(item)
        elif item.review_status == DOMAIN_VALIDATED:
            promoted.append(
                validate_constraint_by_discovery_owner(
                    item,
                    discovery_owner,
                    dictionary,
                    by=actor,
                    on=on,
                    note=cleaned_note,
                )
            )
        else:
            if item.discovery_owner_validated_by.strip() != actor:
                raise GovernanceViolationError(
                    f"Hypothesis {item.code} was validated by '{item.discovery_owner_validated_by}'"
                    f", expected '{actor}'"
                )
            promoted.append(item)
    return RankedConstraintRegister(
        hypotheses=tuple(promoted),
        owner_validated=True,
        finding_status=VALIDATED_FINDING_STATUS,
        owner_validated_by=actor,
        owner_validated_on=on,
        validation_note=cleaned_note,
        notice="",
    )


@dataclass(frozen=True)
class Phase0DiscoveryPack:
    contract_version: str
    discovery_owner: NominatedDiscoveryOwner
    dictionary: LifecycleDictionary
    dictionary_report: LifecycleDictionaryReport
    flow_report: FlowDiscoveryReport
    constraint_register: RankedConstraintRegister
    provenance_note: str = PAS2035_EVIDENCE_PROVENANCE_NOTE
    owner_validated: bool = False
    finding_status: str = CANDIDATE_FINDING_STATUS
    owner_validated_by: str = ""
    owner_validated_on: date | None = None
    validation_note: str = ""
    notice: str = NOT_FINDING

    def __post_init__(self) -> None:
        self.flow_report.verify_digest()
        expected_schema_digest = _dictionary_schema_digest(self.dictionary)
        _verify_report_matches_dictionary(self.flow_report, self.dictionary)
        dict_counts_match = (
            self.dictionary_report.stage_count == len(self.dictionary.stages)
            and self.dictionary_report.event_count == len(self.dictionary.events)
            and self.dictionary_report.timestamp_spec_count == len(self.dictionary.timestamps)
            and self.dictionary_report.wait_state_count == len(self.dictionary.wait_states)
            and self.dictionary_report.return_loop_count == len(self.dictionary.return_loops)
        )
        if not dict_counts_match or (
            bool(self.dictionary_report.dictionary_schema_digest.strip())
            and self.dictionary_report.dictionary_schema_digest != expected_schema_digest
        ):
            raise GovernanceViolationError(
                "Phase0DiscoveryPack dictionary_report does not match "
                "Phase0DiscoveryPack.dictionary"
            )
        if not self.owner_validated and self.finding_status == CANDIDATE_FINDING_STATUS:
            return
        expected_owner = self.discovery_owner.owner.strip()
        flow_on = self.flow_report.owner_validated_on
        flow_seal_ok = (
            flow_on is not None
            and not isinstance(flow_on, datetime)
            and self.flow_report.calculation_digest in _EVALUATED_FLOW_REPORT_DIGESTS
            and (
                self.flow_report.calculation_digest,
                self.flow_report.dictionary_schema_digest,
                self.flow_report.owner_validated_by.strip(),
                flow_on.isoformat(),
                self.flow_report.validation_note.strip(),
            )
            in _VALIDATED_FLOW_REPORT_SEALS
        )
        hypotheses_ok = all(
            (not h.owner_validated)
            if h.review_status == DISPUTED
            else (
                h.review_status != PROPOSED
                and h.owner_validated
                and h.discovery_owner_validated_by.strip() == expected_owner
            )
            for h in self.constraint_register.hypotheses
        )
        if not (
            self.owner_validated
            and self.finding_status == VALIDATED_FINDING_STATUS
            and self.discovery_owner.is_ready
            and not lifecycle_dictionary_gaps(self.dictionary)
            and self.dictionary_report.owner_validated
            and not self.dictionary_report.gaps
            and self.dictionary_report.dictionary_schema_digest == expected_schema_digest
            and self.dictionary_report.owner_validated_by.strip() == expected_owner
            and self.flow_report.owner_validated
            and not self.flow_report.gaps
            and not self.flow_report.invalid_accepted_handover_ids
            and self.flow_report.owner_validated_by.strip() == expected_owner
            and flow_seal_ok
            and self.constraint_register.owner_validated
            and self.constraint_register.owner_validated_by.strip() == expected_owner
            and hypotheses_ok
            and is_valid_human_actor(self.owner_validated_by)
            and self.owner_validated_by.strip() == expected_owner
            and self.owner_validated_on is not None
            and not isinstance(self.owner_validated_on, datetime)
            and bool(self.validation_note.strip())
        ):
            raise GovernanceViolationError(
                "Phase0DiscoveryPack cannot claim owner validation until owner, endpoint, "
                "dictionary, flow report and constraint register pass formal validation "
                "by the exact nominated discovery owner"
            )


def build_default_phase0_pack(
    *,
    window_start: date,
    window_end: date,
    as_of: date,
    candidates: Sequence[BaselineCandidateRecord] = (),
) -> Phase0DiscoveryPack:
    dictionary = build_default_lifecycle_dictionary()
    return Phase0DiscoveryPack(
        contract_version=CONTRACT_VERSION,
        discovery_owner=NominatedDiscoveryOwner(),
        dictionary=dictionary,
        dictionary_report=summarize_lifecycle_dictionary(dictionary),
        flow_report=evaluate_property_flow(
            dictionary,
            window_start=window_start,
            window_end=window_end,
            as_of=as_of,
            candidates=candidates,
        ),
        constraint_register=build_seed_constraint_register(),
    )


def validate_discovery_pack(
    pack: Phase0DiscoveryPack,
    *,
    by: str,
    on: date,
    note: str,
) -> Phase0DiscoveryPack:
    actor, cleaned_note = _require_ready_owner_and_dictionary(
        pack.discovery_owner, pack.dictionary, by, note
    )
    validated_dict_report = validate_lifecycle_report(
        summarize_lifecycle_dictionary(pack.dictionary),
        pack.discovery_owner,
        pack.dictionary,
        by=actor,
        on=on,
        note=cleaned_note,
    )
    validated_flow = validate_flow_report(
        pack.flow_report,
        pack.discovery_owner,
        pack.dictionary,
        by=actor,
        on=on,
        note=cleaned_note,
    )
    validated_register = validate_constraint_register(
        pack.constraint_register,
        pack.discovery_owner,
        pack.dictionary,
        by=actor,
        on=on,
        note=cleaned_note,
    )
    return Phase0DiscoveryPack(
        contract_version=pack.contract_version,
        discovery_owner=pack.discovery_owner,
        dictionary=pack.dictionary,
        dictionary_report=validated_dict_report,
        flow_report=validated_flow,
        constraint_register=validated_register,
        provenance_note=pack.provenance_note,
        owner_validated=True,
        finding_status=VALIDATED_FINDING_STATUS,
        owner_validated_by=actor,
        owner_validated_on=on,
        validation_note=cleaned_note,
        notice="",
    )


@runtime_checkable
class GovernedDiscoveryOutput(Protocol):
    @property
    def owner_validated(self) -> bool: ...

    @property
    def finding_status(self) -> str: ...


def _validated_by_actor(output: GovernedDiscoveryOutput) -> str:
    if isinstance(output, ConstraintHypothesis):
        return output.discovery_owner_validated_by
    if isinstance(
        output,
        (
            LifecycleDictionaryReport,
            FlowDiscoveryReport,
            RankedConstraintRegister,
            Phase0DiscoveryPack,
        ),
    ):
        return output.owner_validated_by
    return str(getattr(output, "owner_validated_by", ""))


def _is_flow_report_mapping(mapping: Mapping[str, object]) -> bool:
    return any(key in mapping for key in _FLOW_REPORT_SIGNATURE_KEYS)


def _verify_validated_flow_report_seal(
    report: FlowDiscoveryReport,
    expected_owner: str,
    dictionary: LifecycleDictionary,
) -> None:
    report.verify_digest()
    _verify_report_matches_dictionary(report, dictionary)
    flow_on = report.owner_validated_on
    if (
        not report.owner_validated
        or report.finding_status != VALIDATED_FINDING_STATUS
        or bool(report.gaps)
        or bool(report.invalid_accepted_handover_ids)
        or not is_valid_human_actor(report.owner_validated_by)
        or report.owner_validated_by.strip() != expected_owner
        or flow_on is None
        or isinstance(flow_on, datetime)
        or not report.validation_note.strip()
        or report.calculation_digest not in _EVALUATED_FLOW_REPORT_DIGESTS
        or (
            report.calculation_digest,
            report.dictionary_schema_digest,
            report.owner_validated_by.strip(),
            flow_on.isoformat(),
            report.validation_note.strip(),
        )
        not in _VALIDATED_FLOW_REPORT_SEALS
    ):
        raise GovernanceViolationError(
            "Validated FlowDiscoveryReport requires zero gaps, zero invalid handovers, and "
            "intact evaluated sign-off provenance"
        )


def _verify_flow_report_mapping(
    mapping: Mapping[str, object],
    *,
    require_validated: bool,
    expected_owner: str | None = None,
    dictionary: LifecycleDictionary | None = None,
) -> None:
    raw_digest = mapping.get("calculation_digest")
    if not isinstance(raw_digest, str) or not raw_digest.strip():
        raise GovernanceViolationError(
            "FlowDiscoveryReport mapping is missing a verified calculation_digest"
        )
    expected_digest = _compute_flow_report_digest(mapping)
    if raw_digest != expected_digest:
        raise GovernanceViolationError(
            "FlowDiscoveryReport mapping calculation_digest mismatch indicates tampering"
        )
    if dictionary is not None:
        _verify_report_matches_dictionary(mapping, dictionary)
    if not require_validated:
        return
    if dictionary is None:
        raise GovernanceViolationError(
            "Validated FlowDiscoveryReport mapping requires a zero-gap LifecycleDictionary"
        )
    if (
        mapping.get("owner_validated") is not True
        or mapping.get("finding_status") != VALIDATED_FINDING_STATUS
        or bool(mapping.get("gaps"))
        or bool(mapping.get("invalid_accepted_handover_ids"))
    ):
        raise GovernanceViolationError(
            "Validated FlowDiscoveryReport mapping requires owner_validated=True, zero gaps, and "
            "zero invalid accepted handovers"
        )
    actor_raw = mapping.get("owner_validated_by")
    note_raw = mapping.get("validation_note")
    if not isinstance(actor_raw, str) or not is_valid_human_actor(actor_raw):
        raise GovernanceViolationError(
            "Validated FlowDiscoveryReport mapping requires a valid human owner_validated_by"
        )
    if expected_owner is not None and actor_raw.strip() != expected_owner:
        raise GovernanceViolationError(
            "Validated FlowDiscoveryReport mapping must match the nominated discovery owner"
        )
    _strict_iso_date(mapping.get("owner_validated_on"), "owner_validated_on")
    if not isinstance(note_raw, str) or not note_raw.strip():
        raise GovernanceViolationError(
            "Validated FlowDiscoveryReport mapping requires a non-blank validation_note"
        )


def enforce_governance_guard(
    output: object,
    *,
    discovery_owner: NominatedDiscoveryOwner | None = None,
    dictionary: LifecycleDictionary | None = None,
) -> None:
    """Fail-closed guard verifying discovery outputs never claim unvalidated company status."""
    if isinstance(output, Mapping):
        if "owner_validated" not in output or "finding_status" not in output:
            raise GovernanceViolationError(
                "Discovery output mapping must carry explicit owner_validated and finding_status"
            )
        owner_val = output["owner_validated"]
        status_val = output["finding_status"]
        validated_by = str(output.get("owner_validated_by", ""))
    elif isinstance(output, GovernedDiscoveryOutput):
        owner_val = output.owner_validated
        status_val = output.finding_status
        validated_by = _validated_by_actor(output)
    else:
        raise GovernanceViolationError(
            "Discovery output must expose owner_validated and finding_status governance attributes"
        )

    if not isinstance(owner_val, bool):
        raise GovernanceViolationError("owner_validated must be a boolean")

    if isinstance(output, FlowDiscoveryReport):
        output.verify_digest()
        if dictionary is not None:
            _verify_report_matches_dictionary(output, dictionary)
    elif isinstance(output, LifecycleDictionaryReport):
        if dictionary is not None and (
            (
                bool(output.dictionary_schema_digest.strip())
                and output.dictionary_schema_digest != _dictionary_schema_digest(dictionary)
            )
            or output.stage_count != len(dictionary.stages)
            or output.event_count != len(dictionary.events)
            or output.timestamp_spec_count != len(dictionary.timestamps)
            or output.wait_state_count != len(dictionary.wait_states)
            or output.return_loop_count != len(dictionary.return_loops)
        ):
            raise GovernanceViolationError(
                "LifecycleDictionaryReport does not match supplied LifecycleDictionary"
            )
    elif isinstance(output, Phase0DiscoveryPack):
        output.flow_report.verify_digest()
        _verify_report_matches_dictionary(output.flow_report, output.dictionary)
        if dictionary is not None:
            if _dictionary_schema_digest(output.dictionary) != _dictionary_schema_digest(
                dictionary
            ):
                raise GovernanceViolationError(
                    "Phase0DiscoveryPack dictionary does not match supplied LifecycleDictionary"
                )
    elif isinstance(output, Mapping):
        if _is_flow_report_mapping(output):
            _verify_flow_report_mapping(output, require_validated=False, dictionary=dictionary)
        for sub_key in ("dictionary_report", "constraint_register"):
            if sub_key in output:
                sub_obj = output[sub_key]
                enforce_governance_guard(
                    sub_obj, discovery_owner=discovery_owner, dictionary=dictionary
                )
        if "flow_report" in output:
            nested_candidate = output["flow_report"]
            if isinstance(nested_candidate, FlowDiscoveryReport):
                enforce_governance_guard(
                    nested_candidate, discovery_owner=discovery_owner, dictionary=dictionary
                )
            elif isinstance(nested_candidate, Mapping):
                _verify_flow_report_mapping(
                    nested_candidate, require_validated=False, dictionary=dictionary
                )
                enforce_governance_guard(
                    nested_candidate, discovery_owner=discovery_owner, dictionary=dictionary
                )
            else:
                raise GovernanceViolationError(
                    "Pack mapping flow_report must be a FlowDiscoveryReport or flow-report mapping"
                )

    if not owner_val:
        if status_val != CANDIDATE_FINDING_STATUS:
            raise GovernanceViolationError(
                f"Unvalidated output must carry finding_status='{CANDIDATE_FINDING_STATUS}', "
                f"got '{status_val}'"
            )
        return

    if status_val != VALIDATED_FINDING_STATUS:
        raise GovernanceViolationError(
            f"Validated output must carry finding_status='{VALIDATED_FINDING_STATUS}', "
            f"got '{status_val}'"
        )
    if discovery_owner is None or not discovery_owner.is_ready:
        raise GovernanceViolationError(
            "Validated discovery output requires a NominatedDiscoveryOwner in ENDPOINT_AGREED state"
        )
    if dictionary is None or lifecycle_dictionary_gaps(dictionary):
        raise GovernanceViolationError(
            "Validated discovery output requires a zero-gap domain-validated LifecycleDictionary"
        )
    expected_owner = discovery_owner.owner.strip()
    expected_schema_digest = _dictionary_schema_digest(dictionary)
    if not is_valid_human_actor(validated_by) or validated_by.strip() != expected_owner:
        raise GovernanceViolationError(
            "Validated discovery output must be signed off by the exact nominated discovery owner"
        )
    if isinstance(output, ConstraintHypothesis) and output.review_status == DISPUTED:
        raise GovernanceViolationError("Disputed hypothesis cannot pass as owner_validated")
    if isinstance(output, LifecycleDictionaryReport):
        if (
            output.gaps
            or output.dictionary_schema_digest != expected_schema_digest
            or output.stage_count != len(dictionary.stages)
            or output.event_count != len(dictionary.events)
            or output.timestamp_spec_count != len(dictionary.timestamps)
            or output.wait_state_count != len(dictionary.wait_states)
            or output.return_loop_count != len(dictionary.return_loops)
        ):
            raise GovernanceViolationError(
                "Validated LifecycleDictionaryReport must have zero gaps and match dictionary"
            )
    if isinstance(output, FlowDiscoveryReport):
        _verify_validated_flow_report_seal(output, expected_owner, dictionary)
    if isinstance(output, Phase0DiscoveryPack):
        if (
            lifecycle_dictionary_gaps(output.dictionary)
            or _dictionary_schema_digest(output.dictionary) != expected_schema_digest
            or not output.dictionary_report.owner_validated
            or output.dictionary_report.gaps
            or output.dictionary_report.dictionary_schema_digest != expected_schema_digest
            or output.dictionary_report.owner_validated_by.strip() != expected_owner
            or not output.constraint_register.owner_validated
            or output.constraint_register.owner_validated_by.strip() != expected_owner
        ):
            raise GovernanceViolationError(
                "Validated Phase0DiscoveryPack requires zero-gap validated sub-reports "
                "signed by the nominated discovery owner"
            )
        _verify_validated_flow_report_seal(output.flow_report, expected_owner, dictionary)
    if isinstance(output, Mapping):
        if output.get("gaps") or output.get("invalid_accepted_handover_ids"):
            raise GovernanceViolationError(
                "Validated discovery output mapping cannot carry unresolved gaps or "
                "invalid accepted handovers"
            )
        if _is_flow_report_mapping(output):
            _verify_flow_report_mapping(
                output,
                require_validated=True,
                expected_owner=expected_owner,
                dictionary=dictionary,
            )
        if "flow_report" in output:
            nested_flow = output["flow_report"]
            if isinstance(nested_flow, FlowDiscoveryReport):
                _verify_validated_flow_report_seal(nested_flow, expected_owner, dictionary)
            elif isinstance(nested_flow, Mapping):
                _verify_flow_report_mapping(
                    nested_flow,
                    require_validated=True,
                    expected_owner=expected_owner,
                    dictionary=dictionary,
                )
            else:
                raise GovernanceViolationError(
                    "Validated pack mapping flow_report must be a validated FlowDiscoveryReport "
                    "or flow-report mapping"
                )
