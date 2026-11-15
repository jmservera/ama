"""Deterministic usability testing programme contract and evaluator (Refs #155).

This module defines the executable contract for Zava North Homes' moderated usability
testing programme across staff, contractor, and voluntary resident and representative
cohorts:

* Test plan validation covering tasks, 5 to 8 participants per role cohort (plus a 2 to 3
  proxy pilot), accessibility needs support, voluntary separate informed consent, and
  synthetic-only aggregate data handling (`SA-009`, `SA-010`, `NFR-009`).
* Live task-script derivation from `profile_journey_contract`, `perspective_walkthroughs`,
  `journey_register`, and `learning_test_bundles` without duplicating upstream definitions.
* `SA-010` aggregate-only session measure evaluation gated on prior `named_human` staff
  representative agreement to a non-surveillance audit-use statement, with full sub-5
  cell masking (`MIN_CELL_FLOOR = 5`) and hypothesis-only threshold checks.
* Severity-tagged (`1..4`) usability findings validation with required GitHub backlog
  issue links and `named_human` risk-acceptance ownership.
* Negative (`not_supported`) and `inconclusive` outcome preservation alongside explicit
  `not_user_validation=True` (`"Synthetic walkthrough - not user validation"`) synthetic
  walkthrough reporting that never claims human usability sign-off.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any

from zava_forward.core import job_pack as jp
from zava_forward.core import journey_register as jr
from zava_forward.core import learning_test_bundles as ltb
from zava_forward.core import perspective_walkthroughs as pw
from zava_forward.core import profile_journey_contract as pjc
from zava_forward.core import projection, rai_release
from zava_forward.core import resident_preview as rp

MIN_ROLE_PARTICIPANTS = 5
MAX_ROLE_PARTICIPANTS = 8
MIN_PILOT_PARTICIPANTS = 2
MAX_PILOT_PARTICIPANTS = 3

SA009_COMPLETION_HYPOTHESIS = 0.80
SA009_SUS_HYPOTHESIS = 70.0
SA009_MAX_UNAIDED_MINUTES = 5.0

PROTOTYPE_UX_CHECKS: tuple[str, ...] = (
    "UX-01",
    "UX-02",
    "UX-03",
    "UX-04",
    "UX-05",
    "UX-06",
    "UX-07",
    "UX-08",
)

STAFF_PROFILE_TO_PERSPECTIVE: dict[str, str] = {
    "Retrofit Programme Manager": "programme-coordinator",
    "Retrofit Coordinator": "retrofit-case-team",
    "Resident Liaison Officer": "housing-resident-engagement",
    "Building Safety Liaison": "repairs-building-safety",
    "Quality Inspector": "quality-assurance",
    "Grants and Evidence Officer": "finance-grants",
}

ACCESSIBILITY_SUPPORT_CLAUSES: tuple[str, ...] = (
    "channel_choice",
    "own_device_and_assistive_tech",
    "advance_plain_language_briefing",
    "interpreter_or_trusted_person",
    "extra_time_no_stopwatch_pressure",
    "voluntary_need_recording_only",
    "pause_or_stop_anytime",
    "manual_non_digital_parity",
)

REQUIRED_ASSISTIVE_TECH_ROUTES: tuple[str, ...] = (
    "screen_reader",
    "keyboard_only",
    "magnification_400_zoom",
    "non_digital_manual_route",
)

CONSENT_DATA_CLAUSES: tuple[str, ...] = (
    "voluntary_participation",
    "separate_from_tenancy_works_and_employment",
    "synthetic_fictional_data_only",
    "no_recording_without_separate_consent_and_dpo",
    "revocable_before_aggregation",
    "pseudonymised_notes_separate_from_signup",
    "dpo_retention_gate_required",
    "aggregate_reporting_only_sa010",
)

SEVERITY_LEVELS: dict[int, str] = {
    1: "note",
    2: "minor",
    3: "major",
    4: "blocker",
}

FINDING_STATUSES: tuple[str, ...] = (
    "open",
    "in_progress",
    "retested",
    "accepted_risk",
)

EVIDENCE_SOURCES: tuple[str, ...] = (
    "moderated_participant",
    "proxy_participant",
    "proxy_pilot",
    "synthetic_walkthrough",
)

OUTCOMES: tuple[str, ...] = (
    "supported",
    "not_supported",
    "inconclusive",
    "not_run",
)

SYNTHETIC_WALKTHROUGH_LABEL = "Synthetic walkthrough - not user validation"
PROXY_PILOT_LABEL = "Proxy pilot - script check only, not user validation"
PROXY_PARTICIPANT_LABEL = "Proxy participant - not direct role validation"
MODERATED_PARTICIPANT_LABEL = "Moderated representative participant session"

DEFAULT_AUDIT_USE_STATEMENT = (
    "Usability testing measures evaluate the Zava Forward prototype, task scripts, and manual "
    "fallbacks only. Results are reported solely as role-level aggregates (minimum cell size 5) "
    "and are never used for individual performance management, disciplinary action, capability "
    "review, or staff surveillance (SA-010)."
)

FORBIDDEN_MEASURE_FIELDS: frozenset[str] = jr.IDENTITY_FIELDS | frozenset(
    {
        "participant_id",
        "participant_ids",
        "participant_name",
        "participant_email",
        "participant_quotes",
        "quote",
        "quotes",
        "employee_id",
        "staff_id",
        "staff_name",
        "staff_code",
        "oid",
        "individual_scores",
        "individual_times",
        "raw_sessions",
        "per_participant",
        "session_recording",
    }
)

_BACKLOG_ISSUE_RE = re.compile(
    r"^(?:#[1-9]\d*|https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/issues/[1-9]\d*)$"
)
_FINDING_ID_RE = re.compile(r"^UF-\d{3,}$")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

_BUNDLE_SCRIPT_IDS: dict[str, str] = {
    "story-once": "B1-story-once",
    "pre-visit-pack": "B2-pre-visit-pack",
    "change-impact": "B3-change-impact",
    "handover-aftercare": "B4-handover-aftercare",
    "funding-evidence": "B5-funding-evidence",
}

_BUNDLE_COHORTS: dict[str, tuple[str, ...]] = {
    "story-once": ("resident", "resident-representative", "housing-resident-engagement"),
    "pre-visit-pack": (
        "assessor-designer",
        "housing-resident-engagement",
        "repairs-building-safety",
        "provider-contractor",
    ),
    "change-impact": (
        "programme-coordinator",
        "retrofit-case-team",
        "procurement-contracts",
        "finance-grants",
    ),
    "handover-aftercare": (
        "resident",
        "quality-assurance",
        "housing-resident-engagement",
        "repairs-building-safety",
    ),
    "funding-evidence": ("finance-grants", "quality-assurance", "digital-auditor"),
}

_BUNDLE_PERSPECTIVES: dict[str, tuple[str, ...]] = {
    "story-once": ("housing-resident-engagement", "retrofit-case-team"),
    "pre-visit-pack": (
        "assessor-designer",
        "housing-resident-engagement",
        "repairs-building-safety",
        "provider-contractor",
    ),
    "change-impact": (
        "programme-coordinator",
        "retrofit-case-team",
        "procurement-contracts",
        "finance-grants",
    ),
    "handover-aftercare": (
        "quality-assurance",
        "housing-resident-engagement",
        "repairs-building-safety",
    ),
    "funding-evidence": ("finance-grants", "quality-assurance", "digital-auditor"),
}

_BUNDLE_FAILURE_CASES: dict[str, tuple[str, ...]] = {
    "story-once": (
        "Resident declines or pauses one measure without losing support on remaining work.",
        "Resident withdraws optional data-sharing consent and receives plain confirmation.",
        "Resident or representative uses phone or paper route instead of digital portal.",
    ),
    "pre-visit-pack": (
        "No-access or aborted visit updates next owner and resident notice without blame.",
        "Newly reported damp, mould, or structural hazard triggers safety hold and clock.",
        "Raw vulnerability note stays redacted for contractor and non-reason staff roles.",
    ),
    "change-impact": (
        "Survey finding changes measure scope and invalidates prior readiness assumptions.",
        "Supplier capacity shortfall delays appointed slot and surfaces replanning owner.",
        "Grant condition or tenure hold blocks progression until named owner reviews.",
    ),
    "handover-aftercare": (
        "Post-installation defect or damp concern reopens case with named accountable owner.",
        "Contractor completion receipt is shown as submitted evidence, never QA acceptance.",
        "Resident requests plain-language operating guidance or formal complaint route.",
    ),
    "funding-evidence": (
        "Missing or stale evidence attachment holds claim pack for Finance human review.",
        "Evidence replacement increments version and requires fresh independent sign-off.",
        "O16 effort is attributed to exactly one bundle so savings are never double-counted.",
    ),
}


@dataclass(frozen=True)
class AuditUseAgreement:
    """SA-010 staff audit-use agreement record required before recording staff measures."""

    agreed_with_staff: bool
    agreed_date: str | None
    staff_representatives: tuple[str, ...]
    programme_owner: str | None
    dpo_reviewer: str | None
    statement_text: str = DEFAULT_AUDIT_USE_STATEMENT


@dataclass(frozen=True)
class ParticipantCohort:
    """Target participant sizing and applicability metadata for one tested role cohort."""

    cohort_id: str
    role_label: str
    group: str
    perspective_id: str | None
    min_participants: int
    max_participants: int
    counts_toward_role_minimum: bool
    t0_applicable: bool
    sizing_basis: str
    proxy_login_note: str | None = None


@dataclass(frozen=True)
class UsabilityTaskScript:
    """Moderated task script derived from profile journey and learning-bundle contracts."""

    script_id: str
    family: str
    title: str
    target_cohorts: tuple[str, ...]
    perspectives: tuple[str, ...]
    same_home_staff_profiles: tuple[str, ...]
    contract_elements: dict[str, str]
    register_element_status: dict[str, dict[str, str]]
    proxy_only_perspectives: tuple[str, ...]
    ux_checks: tuple[str, ...]
    journey_ids: tuple[str, ...]
    bundle_key: str | None
    arms: tuple[str, ...]
    comparator_baseline: str | None
    atlas_ids: tuple[str, ...]
    linked_requirements: tuple[str, ...]
    learning_question: str | None
    zero_measures: tuple[str, ...]
    stop_rule: str | None
    failure_cases: tuple[str, ...]
    o16_single_count_rule: str | None
    manual_fallback_prompt: str


@dataclass(frozen=True)
class UsabilityProgrammePlan:
    """Complete moderated usability testing programme specification."""

    programme_id: str
    tasks: tuple[UsabilityTaskScript, ...]
    cohorts: tuple[ParticipantCohort, ...]
    accessibility_support: dict[str, str]
    assistive_tech_coverage: tuple[str, ...]
    consent_and_data_handling: dict[str, str]
    synthetic_data_only: bool
    recording_default_off: bool
    thresholds_are_hypotheses: bool
    audit_use_agreement: AuditUseAgreement


@dataclass(frozen=True)
class UsabilityFinding:
    """Anonymised usability finding tagged with severity and linked to a backlog issue."""

    finding_id: str
    target_id: str
    cohort_id: str
    severity: int
    status: str
    evidence_source: str
    observation: str
    impact: str
    backlog_issue: str
    risk_owner: str | None = None
    risk_rationale: str | None = None


@dataclass(frozen=True)
class OutcomeRecord:
    """Task, cohort, or bundle outcome preserving negative/inconclusive results and labels."""

    target_id: str
    outcome: str
    evidence_source: str
    not_user_validation: bool
    validation_label: str
    summary: str
    negative_or_failure_notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SyntheticWalkthroughReport:
    """Deterministic synthetic contract walkthrough report explicitly marked non-user-validation."""

    not_user_validation: bool
    validation_label: str
    user_validation_established: bool
    human_usability_signoff: bool
    records: tuple[OutcomeRecord, ...]
    outcome_counts: dict[str, int]
    same_home_clean_status: str
    same_home_negative_probe_blockers: tuple[str, ...]
    o16_reconciled_owner: str | None
    notice: str


def _clean_text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _parse_iso_date(raw: object, field_name: str) -> date:
    if not isinstance(raw, str) or re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw) is None:
        raise ValueError(f"{field_name} must be an ISO YYYY-MM-DD date string.")
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{field_name} is not a valid calendar ISO date: {raw!r}.") from exc


def _normalize_key(key: object) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(key).strip().casefold()).strip("_")


def _scan_forbidden_fields(payload: object, path: str = "record") -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            norm = _normalize_key(key)
            if norm in FORBIDDEN_MEASURE_FIELDS:
                raise ValueError(
                    "SA-010 aggregate-only violation: forbidden individual field "
                    f"{key!r} at {path}."
                )
            _scan_forbidden_fields(value, f"{path}.{key}")
    elif isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        for idx, item in enumerate(payload):
            if isinstance(item, Mapping):
                raise ValueError(
                    "SA-010 aggregate-only violation: per-participant row mapping at "
                    f"{path}[{idx}]."
                )
            _scan_forbidden_fields(item, f"{path}[{idx}]")


def _register_statuses_for(
    reg: Mapping[str, Mapping[str, Mapping[str, Any]]],
    perspectives: Sequence[str],
) -> dict[str, dict[str, str]]:
    return {
        pid: {el: str(reg[pid][el]["status"]) for el in pjc.ELEMENTS}
        for pid in perspectives
        if pid in reg
    }


def _proxy_perspectives_for(perspectives: Sequence[str]) -> tuple[str, ...]:
    return tuple(pid for pid in perspectives if pid in pw.PROXY_ONLY)


def derive_task_scripts() -> tuple[UsabilityTaskScript, ...]:
    """Derive canonical moderated task scripts from core journey and bundle contracts."""
    reg = pw.register()
    all_perspectives = tuple(pw.EVIDENCE.keys())
    staff_perspectives = tuple(pid for pid in all_perspectives if pid != "provider-contractor")

    profile_defs: tuple[
        tuple[
            str,
            str,
            tuple[str, ...],
            tuple[str, ...],
            tuple[str, ...],
            tuple[str, ...],
            dict[str, str],
            tuple[str, ...],
            str,
        ],
        ...,
    ] = (
        (
            "T0",
            "Core SA-009 case lookup, next step, and accountable owner",
            staff_perspectives + ("provider-contractor",),
            all_perspectives,
            pjc.SIX_STAFF_PROFILES,
            ("UX-01", "UX-02", "UX-05"),
            {
                "entry": (
                    "Open the role queue or workbench for a named synthetic home without hints."
                ),
                "evidence": (
                    "Inspect current stage, linked evidence records, and plain-language status."
                ),
                "safe_endpoint": (
                    "State the next step and whether any safety, consent, or funding block holds."
                ),
                "recovery": "Recover if the initial filter or search misses the synthetic home.",
                "handoff": (
                    "Name the single accountable human owner for the next action under 5 minutes."
                ),
            },
            ("SA-009", "SA-010", "NFR-009"),
            (
                "Complete the same lookup and owner check using the current spreadsheet/manual "
                "register."
            ),
        ),
        (
            "T1",
            "Role entry, scope orientation, and proxy-role boundary check",
            staff_perspectives,
            (
                "asset-investment",
                "programme-coordinator",
                "procurement-contracts",
                "digital-auditor",
            ),
            ("Retrofit Programme Manager",),
            ("UX-01", "UX-02"),
            {
                "entry": (
                    "Sign in or assume the assigned role view and state what work is in scope."
                ),
                "evidence": (
                    "Read cohort, stock, procurement, or audit summary indicators using text "
                    "labels."
                ),
                "safe_endpoint": (
                    "Confirm role boundaries and note where login uses a manager proxy fixture."
                ),
                "recovery": "Switch back from an out-of-scope panel without losing queue context.",
                "handoff": (
                    "Identify which named role owns follow-up on flagged portfolio or contract "
                    "items."
                ),
            },
            ("SA-009", "NFR-009"),
            "Verify scope and owner boundaries from the manual governance role matrix.",
        ),
        (
            "T2",
            "Exception triage, hazard/clock priority, and empty or error recovery",
            (
                "programme-coordinator",
                "repairs-building-safety",
                "digital-auditor",
            ),
            (
                "programme-coordinator",
                "repairs-building-safety",
                "digital-auditor",
            ),
            ("Retrofit Programme Manager", "Building Safety Liaison"),
            ("UX-01", "UX-03"),
            {
                "entry": (
                    "Open the exception or safety queue containing overdue and held synthetic "
                    "cases."
                ),
                "evidence": (
                    "Distinguish hazard clocks, stale evidence, and system errors via non-colour "
                    "text."
                ),
                "safe_endpoint": (
                    "Hold progression on active hazards while keeping emergency routes open."
                ),
                "recovery": (
                    "Trigger and recover from an empty filter or simulated load failure cleanly."
                ),
                "handoff": (
                    "Route the highest-risk exception to its named safety or coordinator owner."
                ),
            },
            ("FR-025", "NFR-008", "NFR-009"),
            "Triage the same exception set using the manual hazard and escalation log.",
        ),
        (
            "T3",
            "Evidence-based readiness check across technical, stock, and grant gates",
            (
                "asset-investment",
                "retrofit-case-team",
                "assessor-designer",
                "procurement-contracts",
                "finance-grants",
            ),
            (
                "asset-investment",
                "retrofit-case-team",
                "assessor-designer",
                "procurement-contracts",
                "finance-grants",
            ),
            ("Retrofit Coordinator", "Grants and Evidence Officer"),
            ("UX-04",),
            {
                "entry": (
                    "Open a synthetic home awaiting technical sign-off, capacity, or grant check."
                ),
                "evidence": (
                    "Inspect linked survey, stock reconciliation, capacity, and funding evidence "
                    "IDs."
                ),
                "safe_endpoint": (
                    "Refuse readiness advancement when any required evidence or tenure check is "
                    "Unknown."
                ),
                "recovery": (
                    "Identify the exact missing evidence item and record a safe held state."
                ),
                "handoff": (
                    "Assign the missing-evidence action to Assessor, Procurement, or Finance owner."
                ),
            },
            ("FR-009", "FR-015", "NFR-009"),
            (
                "Check readiness against the manual PAS 2035 / grant checklist without assistant "
                "panels."
            ),
        ),
        (
            "T4",
            "Cross-role handoff ownership and pending-transfer continuity",
            (
                "programme-coordinator",
                "retrofit-case-team",
                "housing-resident-engagement",
                "repairs-building-safety",
                "quality-assurance",
                "finance-grants",
            ),
            tuple(STAFF_PROFILE_TO_PERSPECTIVE.values()),
            pjc.SIX_STAFF_PROFILES,
            ("UX-05",),
            {
                "entry": (
                    "Inspect a synthetic home with an Offered or Escalated cross-team handoff."
                ),
                "evidence": (
                    "Compare current owner, chase owner, and next action across the six staff "
                    "profiles."
                ),
                "safe_endpoint": (
                    "Keep accountability with the sending owner until the receiver confirms."
                ),
                "recovery": (
                    "Escalate an unaccepted or overdue handoff without orphaning the case."
                ),
                "handoff": (
                    "Confirm exact receiver ownership transfer and plain-language reason "
                    "visibility."
                ),
            },
            ("NFR-008", "NFR-009", "AC-071"),
            "Record and chase the same handoff on the manual transfer register.",
        ),
        (
            "T5",
            "Inspectable AI proposal challenge, uncertainty check, and manual path",
            (
                "programme-coordinator",
                "retrofit-case-team",
                "quality-assurance",
                "finance-grants",
            ),
            (
                "programme-coordinator",
                "retrofit-case-team",
                "quality-assurance",
                "finance-grants",
            ),
            (
                "Retrofit Programme Manager",
                "Retrofit Coordinator",
                "Quality Inspector",
                "Grants and Evidence Officer",
            ),
            ("UX-06",),
            {
                "entry": (
                    "Open a case panel showing an advisory assistant summary or review-suggested "
                    "flag."
                ),
                "evidence": (
                    "Inspect cited source records, freshness, and explicit uncertainty notes."
                ),
                "safe_endpoint": (
                    "Reject or edit an unsupported draft so no automated domain write occurs."
                ),
                "recovery": (
                    "Switch off or bypass assistant output when unavailable, stale, or withheld."
                ),
                "handoff": (
                    "Complete the review decision manually and record the named human reviewer."
                ),
            },
            ("FR-010", "NFR-009", "NFR-015"),
            "Complete the case review end-to-end with assistant panels unavailable.",
        ),
        (
            "T6",
            "Full-screen single-case workspace, 400 percent zoom, and keyboard return",
            (
                "retrofit-case-team",
                "assessor-designer",
                "quality-assurance",
            ),
            (
                "retrofit-case-team",
                "assessor-designer",
                "quality-assurance",
            ),
            ("Retrofit Coordinator", "Quality Inspector"),
            ("UX-07",),
            {
                "entry": (
                    "Navigate by keyboard from the filtered queue into the single-case workspace."
                ),
                "evidence": (
                    "Read stage, quality checklist, and evidence history at 200% and 400% zoom."
                ),
                "safe_endpoint": (
                    "Verify focus order, visible focus ring, and live status announcement."
                ),
                "recovery": (
                    "Return to the exact prior queue filter and scroll/focus anchor via keyboard."
                ),
                "handoff": (
                    "Confirm next inspection or coordinator owner remains visible after zoom."
                ),
            },
            ("NFR-001", "NFR-009", "AC-093"),
            "Read and update the same single-case summary via printable/manual pack.",
        ),
        (
            "T7",
            "Synthetic resident contact, adjustment redaction, and non-digital preference",
            (
                "housing-resident-engagement",
                "retrofit-case-team",
                "repairs-building-safety",
            ),
            (
                "housing-resident-engagement",
                "retrofit-case-team",
                "repairs-building-safety",
            ),
            (
                "Resident Liaison Officer",
                "Retrofit Coordinator",
                "Building Safety Liaison",
            ),
            ("UX-08",),
            {
                "entry": (
                    "Open a synthetic household record with language, access, and non-digital "
                    "preferences."
                ),
                "evidence": (
                    "Verify RLO/Safety see raw adjustment reasons while non-reason roles see held "
                    "notice."
                ),
                "safe_endpoint": (
                    "Prepare resident communication using synthetic-only contact placeholders."
                ),
                "recovery": (
                    "Handle withdrawn consent or changed preferred channel without losing support."
                ),
                "handoff": (
                    "Hand over agreed visit window and staffed phone/paper route to RLO owner."
                ),
            },
            ("FR-029", "FR-032", "NFR-009"),
            "Prepare the resident contact and adjustment sheet via staffed phone/paper workflow.",
        ),
        (
            "T8",
            "Contractor job-pack view, field submission, correction, and non-acceptance boundary",
            ("provider-contractor", "quality-assurance"),
            ("provider-contractor", "quality-assurance"),
            ("Quality Inspector",),
            ("UX-04", "UX-05"),
            {
                "entry": (
                    "Open an issued contractor work order and job pack containing only authorised "
                    "scope."
                ),
                "evidence": (
                    "Verify resident notes, hazards, and finance data are absent and readiness "
                    "flags match."
                ),
                "safe_endpoint": (
                    "Submit field checklist evidence and confirm receipt says Submitted, never "
                    "Accepted."
                ),
                "recovery": (
                    "Recover from a returned submission by attaching remediation detail and "
                    "reference."
                ),
                "handoff": (
                    "Route submitted work to an independent named Quality Inspector for acceptance."
                ),
            },
            ("FR-015", "NFR-008", "NFR-009"),
            (
                "Submit field evidence through the staffed intake route when contractor portal is "
                "unused."
            ),
        ),
    )

    scripts: list[UsabilityTaskScript] = []
    for (
        sid,
        title,
        cohorts,
        perspectives,
        staff_profiles,
        ux_checks,
        elements,
        reqs,
        manual_prompt,
    ) in profile_defs:
        scripts.append(
            UsabilityTaskScript(
                script_id=sid,
                family="profile_journey",
                title=title,
                target_cohorts=cohorts,
                perspectives=perspectives,
                same_home_staff_profiles=staff_profiles,
                contract_elements=elements,
                register_element_status=_register_statuses_for(reg, perspectives),
                proxy_only_perspectives=_proxy_perspectives_for(perspectives),
                ux_checks=ux_checks,
                journey_ids=(),
                bundle_key=None,
                arms=(),
                comparator_baseline=None,
                atlas_ids=(),
                linked_requirements=reqs,
                learning_question=None,
                zero_measures=(),
                stop_rule=None,
                failure_cases=(
                    "Missing or ambiguous state text blocks progression rather than guessing.",
                ),
                o16_single_count_rule=None,
                manual_fallback_prompt=manual_prompt,
            )
        )

    for jid, jname in jr.JOURNEYS.items():
        script_id = f"R-{jid}"
        is_rep = jid == "R1"
        target_cohorts = (
            ("resident-representative", "resident", "housing-resident-engagement")
            if is_rep
            else ("resident", "resident-representative", "housing-resident-engagement")
        )
        perspectives = ("housing-resident-engagement", "repairs-building-safety")
        jowner = "Resident Liaison Officer"
        jescalation = "Building Safety Liaison or Retrofit Programme Manager"
        scripts.append(
            UsabilityTaskScript(
                script_id=script_id,
                family="resident_journey",
                title=f"{jid}: {jname}",
                target_cohorts=target_cohorts,
                perspectives=perspectives,
                same_home_staff_profiles=("Resident Liaison Officer", "Building Safety Liaison"),
                contract_elements={
                    "entry": (
                        f"Enter the {jname.lower()} journey via chosen synthetic portal, phone, or "
                        "printed pack without needing an internal case ID."
                    ),
                    "evidence": (
                        "Read plain-language home status, what happens next, and explicit "
                        "read-only consent/decision boundaries."
                    ),
                    "safe_endpoint": (
                        "Verify authority scope and separate consent before any representative "
                        "action is recorded."
                        if is_rep
                        else "Confirm tenancy and support rights stay unaffected when pausing, "
                        "questioning, or declining optional items."
                    ),
                    "recovery": (
                        "Correct a misunderstanding, request translation/large print, or raise a "
                        "concern without repeating the household story."
                    ),
                    "handoff": (
                        f"Identify named {jowner} contact and escalation route to {jescalation}."
                    ),
                },
                register_element_status=_register_statuses_for(reg, perspectives),
                proxy_only_perspectives=_proxy_perspectives_for(perspectives),
                ux_checks=("UX-01", "UX-03", "UX-08"),
                journey_ids=(jid,),
                bundle_key=None,
                arms=(),
                comparator_baseline=None,
                atlas_ids=(),
                linked_requirements=("FR-029", "FR-032", "NFR-008", "NFR-009"),
                learning_question=None,
                zero_measures=(),
                stop_rule=None,
                failure_cases=(
                    "Portal unavailable or declined: participant completes the same step by "
                    "staffed telephone or printed pack without detriment.",
                ),
                o16_single_count_rule=None,
                manual_fallback_prompt=(
                    f"Complete {jid} ({jname}) through the staffed telephone or printed-pack "
                    f"channel owned by {jowner}."
                ),
            )
        )

    for bkey, bundle in ltb.BUNDLES.items():
        b_perspectives = _BUNDLE_PERSPECTIVES[bkey]
        b_staff_profiles = tuple(
            role for role, pslug in STAFF_PROFILE_TO_PERSPECTIVE.items() if pslug in b_perspectives
        )
        o16_note = (
            f"O16 shared across {', '.join(ltb.O16_BUNDLES)}; declare a single "
            "o16_counted_under owner before comparing runs."
            if bkey in ltb.O16_BUNDLES
            else None
        )
        scripts.append(
            UsabilityTaskScript(
                script_id=_BUNDLE_SCRIPT_IDS[bkey],
                family="learning_bundle",
                title=f"Learning bundle {bundle.title} ({bkey})",
                target_cohorts=_BUNDLE_COHORTS[bkey],
                perspectives=b_perspectives,
                same_home_staff_profiles=b_staff_profiles,
                contract_elements={
                    "entry": (
                        f"Run two-arm comparison ({bundle.comparator} vs Zava Forward workflow) "
                        f"on identical synthetic cases for {bundle.title}."
                    ),
                    "evidence": (
                        f"Record all six effort components ({', '.join(ltb.COMPONENTS)}) and "
                        f"zero-target safety/consent counts ({', '.join(bundle.zero_measures)})."
                    ),
                    "safe_endpoint": (
                        f"Evaluate stop rule first ({bundle.stop_rule}) before reading any "
                        "effort difference."
                    ),
                    "recovery": (
                        "Exercise assistance-unavailable manual fallback and constructed Atlas "
                        "failure cases without losing case ownership."
                    ),
                    "handoff": (
                        "Confirm single accountable next-step owner and keep saved minutes "
                        "labelled as capacity until Finance validation."
                    ),
                },
                register_element_status=_register_statuses_for(reg, b_perspectives),
                proxy_only_perspectives=_proxy_perspectives_for(b_perspectives),
                ux_checks=("UX-04", "UX-05", "UX-06"),
                journey_ids=(),
                bundle_key=bkey,
                arms=ltb.ARMS,
                comparator_baseline=bundle.comparator,
                atlas_ids=bundle.atlas_ids,
                linked_requirements=bundle.linked_requirements,
                learning_question=bundle.learning_question,
                zero_measures=bundle.zero_measures,
                stop_rule=bundle.stop_rule,
                failure_cases=_BUNDLE_FAILURE_CASES[bkey],
                o16_single_count_rule=o16_note,
                manual_fallback_prompt=(
                    f"Complete {bundle.title} using {bundle.comparator} with AI assistance "
                    "switched off."
                ),
            )
        )

    return tuple(scripts)


def validate_task_scripts(scripts: Sequence[UsabilityTaskScript]) -> dict[str, Any]:
    """Validate that task scripts cover all profile-contract, journey, and bundle invariants."""
    errors: list[str] = []
    if not scripts:
        return {"valid": False, "errors": ["no_task_scripts"]}

    seen_ids: set[str] = set()
    covered_perspectives: set[str] = set()
    covered_staff_profiles: set[str] = set()
    covered_ux_checks: set[str] = set()
    covered_journeys: set[str] = set()
    covered_bundles: dict[str, UsabilityTaskScript] = {}
    reg = pw.register()

    for script in scripts:
        if not script.script_id or script.script_id in seen_ids:
            errors.append(f"duplicate_or_blank_script_id:{script.script_id}")
        seen_ids.add(script.script_id)

        if set(script.contract_elements.keys()) != set(pjc.ELEMENTS):
            errors.append(f"{script.script_id}:incomplete_contract_elements")
        else:
            for el in pjc.ELEMENTS:
                if not _clean_text(script.contract_elements.get(el)):
                    errors.append(f"{script.script_id}.{el}:blank_prompt")

        if not _clean_text(script.manual_fallback_prompt):
            errors.append(f"{script.script_id}:missing_manual_fallback_prompt")
        if not script.target_cohorts:
            errors.append(f"{script.script_id}:missing_target_cohorts")

        for pid in script.perspectives:
            if pid not in pw.EVIDENCE:
                errors.append(f"{script.script_id}:unknown_perspective:{pid}")
            else:
                covered_perspectives.add(pid)
                expected_status = {el: str(reg[pid][el]["status"]) for el in pjc.ELEMENTS}
                if script.register_element_status.get(pid) != expected_status:
                    errors.append(f"{script.script_id}:stale_register_status:{pid}")

        expected_proxies = _proxy_perspectives_for(script.perspectives)
        if script.proxy_only_perspectives != expected_proxies:
            errors.append(f"{script.script_id}:proxy_only_mismatch")

        for srole in script.same_home_staff_profiles:
            if srole not in STAFF_PROFILE_TO_PERSPECTIVE:
                errors.append(f"{script.script_id}:unknown_staff_profile:{srole}")
            else:
                covered_staff_profiles.add(srole)

        covered_ux_checks.update(script.ux_checks)
        covered_journeys.update(script.journey_ids)

        for aid in script.atlas_ids:
            if aid in ltb.OUT_OF_SCOPE:
                errors.append(f"{script.script_id}:out_of_scope_atlas_id:{aid}")

        if script.family == "learning_bundle":
            bkey = script.bundle_key or ""
            if bkey not in ltb.BUNDLES:
                errors.append(f"{script.script_id}:unknown_bundle:{bkey}")
            else:
                covered_bundles[bkey] = script
                bundle = ltb.BUNDLES[bkey]
                if script.arms != ltb.ARMS:
                    errors.append(f"{script.script_id}:arms_mismatch")
                if script.comparator_baseline != bundle.comparator:
                    errors.append(f"{script.script_id}:comparator_mismatch")
                if script.atlas_ids != bundle.atlas_ids:
                    errors.append(f"{script.script_id}:atlas_ids_mismatch")
                if script.zero_measures != bundle.zero_measures:
                    errors.append(f"{script.script_id}:zero_measures_mismatch")
                if script.stop_rule != bundle.stop_rule:
                    errors.append(f"{script.script_id}:stop_rule_mismatch")
                if not script.failure_cases:
                    errors.append(f"{script.script_id}:missing_failure_cases")
                if bkey in ltb.O16_BUNDLES and not _clean_text(script.o16_single_count_rule):
                    errors.append(f"{script.script_id}:missing_o16_single_count_rule")
                if bkey not in ltb.O16_BUNDLES and script.o16_single_count_rule is not None:
                    errors.append(f"{script.script_id}:unexpected_o16_single_count_rule")

    expected_profile_ids = {f"T{i}" for i in range(9)}
    missing_profile_ids = sorted(expected_profile_ids - seen_ids)
    if missing_profile_ids:
        errors.append(f"missing_profile_scripts:{','.join(missing_profile_ids)}")

    missing_perspectives = sorted(set(pw.EVIDENCE.keys()) - covered_perspectives)
    if missing_perspectives:
        errors.append(f"missing_perspectives:{','.join(missing_perspectives)}")

    missing_staff = sorted(set(pjc.SIX_STAFF_PROFILES) - covered_staff_profiles)
    if missing_staff:
        errors.append(f"missing_same_home_staff_profiles:{','.join(missing_staff)}")

    missing_ux = sorted(set(PROTOTYPE_UX_CHECKS) - covered_ux_checks)
    if missing_ux:
        errors.append(f"missing_ux_checks:{','.join(missing_ux)}")

    missing_journeys = sorted(set(jr.JOURNEYS.keys()) - covered_journeys)
    if missing_journeys:
        errors.append(f"missing_resident_journeys:{','.join(missing_journeys)}")

    missing_bundles = sorted(set(ltb.BUNDLES.keys()) - set(covered_bundles.keys()))
    if missing_bundles:
        errors.append(f"missing_learning_bundles:{','.join(missing_bundles)}")

    return {
        "valid": not errors,
        "errors": errors,
        "script_count": len(scripts),
        "covered_perspectives": sorted(covered_perspectives),
        "covered_journeys": sorted(covered_journeys),
        "covered_bundles": sorted(covered_bundles.keys()),
    }


def default_programme_plan() -> UsabilityProgrammePlan:
    """Build the canonical Issue #155 usability testing programme plan (human sessions unrun)."""
    perspective_labels: dict[str, str] = {
        "asset-investment": "Asset management and investment lead",
        "programme-coordinator": "Retrofit programme manager and coordinator",
        "retrofit-case-team": "Retrofit coordinator and case team",
        "assessor-designer": "Retrofit assessor and designer",
        "housing-resident-engagement": "Housing officer and resident liaison officer",
        "repairs-building-safety": "Repairs interface and building safety liaison",
        "procurement-contracts": "Procurement and contract manager",
        "provider-contractor": "External installation contractor and field supervisor",
        "quality-assurance": "Quality inspector and clerk of works",
        "finance-grants": "Finance and grants evidence officer",
        "digital-auditor": "Digital, data, and assurance auditor",
    }

    cohorts: list[ParticipantCohort] = []
    for pid, label in perspective_labels.items():
        is_contractor = pid == "provider-contractor"
        cohorts.append(
            ParticipantCohort(
                cohort_id=pid,
                role_label=label,
                group="contractor" if is_contractor else "staff",
                perspective_id=pid,
                min_participants=MIN_ROLE_PARTICIPANTS,
                max_participants=MAX_ROLE_PARTICIPANTS,
                counts_toward_role_minimum=True,
                t0_applicable=True,
                sizing_basis=(
                    "Proposed 5-8 external contractor users per role aligned with SA-009 cell floor"
                    if is_contractor
                    else "PRD SA-009 target of 5-8 Excel/workbench users per staff role"
                ),
                proxy_login_note=(
                    "Prototype reaches this perspective via manager proxy fixture (PROXY_ONLY)."
                    if pid in pw.PROXY_ONLY
                    else None
                ),
            )
        )

    cohorts.extend(
        (
            ParticipantCohort(
                cohort_id="resident",
                role_label="Voluntary social housing residents across channels and access needs",
                group="resident_or_representative",
                perspective_id=None,
                min_participants=MIN_ROLE_PARTICIPANTS,
                max_participants=MAX_ROLE_PARTICIPANTS,
                counts_toward_role_minimum=True,
                t0_applicable=False,
                sizing_basis=(
                    "Proposed 5-8 voluntary resident participants (SA-009 sizes staff roles; "
                    "resident cohort subject to Resident Engagement, owner, and DPO confirmation)"
                ),
            ),
            ParticipantCohort(
                cohort_id="resident-representative",
                role_label="Authorised family members, carers, advocates, or support workers",
                group="resident_or_representative",
                perspective_id=None,
                min_participants=MIN_ROLE_PARTICIPANTS,
                max_participants=MAX_ROLE_PARTICIPANTS,
                counts_toward_role_minimum=True,
                t0_applicable=False,
                sizing_basis=(
                    "Proposed 5-8 voluntary authorised representatives testing R1 authority and "
                    "separate consent boundaries (subject to owner and DPO confirmation)"
                ),
            ),
            ParticipantCohort(
                cohort_id="proxy-pilot",
                role_label="Internal proxy pilot participants for script calibration only",
                group="pilot",
                perspective_id=None,
                min_participants=MIN_PILOT_PARTICIPANTS,
                max_participants=MAX_PILOT_PARTICIPANTS,
                counts_toward_role_minimum=False,
                t0_applicable=True,
                sizing_basis=(
                    "2-3 proxy dry-run sessions to test script clarity; excluded from role totals"
                ),
            ),
        )
    )

    return UsabilityProgrammePlan(
        programme_id="zava-north-homes-usability-programme-155",
        tasks=derive_task_scripts(),
        cohorts=tuple(cohorts),
        accessibility_support={
            "channel_choice": (
                "Participants choose in-person, telephone, or remote video/browser sessions and "
                "may switch to a staffed non-digital route at any point."
            ),
            "own_device_and_assistive_tech": (
                "Sessions support the participant's own device, screen reader (NVDA, JAWS, "
                "VoiceOver, TalkBack), keyboard-only navigation, browser zoom up to 400%, high "
                "contrast, and reduced motion."
            ),
            "advance_plain_language_briefing": (
                "Plain-language task briefing, consent sheet, and large-print, translated, or "
                "easy-read packs are sent in advance with no time-pressured cold reading."
            ),
            "interpreter_or_trusted_person": (
                "BSL/community interpreters, advocates, carers, or a trusted support person are "
                "welcomed and funded without reducing session time."
            ),
            "extra_time_no_stopwatch_pressure": (
                "Flexible scheduling, breaks, and untimed exploration are offered; T0 5-minute "
                "timing is observed quietly for staff roles without countdown pressure."
            ),
            "voluntary_need_recording_only": (
                "Only session-support adjustments volunteered by the participant are noted for "
                "logistics; medical diagnoses are never requested or stored."
            ),
            "pause_or_stop_anytime": (
                "Participants can skip any question, pause, or end the session immediately "
                "without giving a reason and without consequence."
            ),
            "manual_non_digital_parity": (
                "Every task tests the manual or staffed non-digital alternative alongside the "
                "prototype workflow in accordance with NFR-009 (AC-071)."
            ),
        },
        assistive_tech_coverage=REQUIRED_ASSISTIVE_TECH_ROUTES,
        consent_and_data_handling={
            "voluntary_participation": (
                "Participation is wholly voluntary for staff, contractors, residents, and "
                "representatives."
            ),
            "separate_from_tenancy_works_and_employment": (
                "Usability study consent is completely separate from tenancy agreements, retrofit "
                "works consent, repairs service, employment terms, and contractor awards."
            ),
            "synthetic_fictional_data_only": (
                "All sessions use synthetic fictional homes, personas, and cases only; real "
                "resident addresses, tenancy records, and live staff cases are prohibited."
            ),
            "no_recording_without_separate_consent_and_dpo": (
                "Audio, video, and screen recording are off by default and require both DPO "
                "lawful-basis sign-off and a separate opt-in consent choice."
            ),
            "revocable_before_aggregation": (
                "Participants may withdraw their session notes at any point before role-level "
                "aggregation is finalised."
            ),
            "pseudonymised_notes_separate_from_signup": (
                "Facilitator notes use random session codes stored separately from recruitment "
                "contact lists, with zero direct identifiers or combinable quotes."
            ),
            "dpo_retention_gate_required": (
                "Recruitment records and session notes await a named DPO retention and deletion "
                "schedule before live participant recruitment begins."
            ),
            "aggregate_reporting_only_sa010": (
                "Published measures are aggregate-only (n >= 5 per role cell) and gated on prior "
                "written agreement with staff representatives on the SA-010 audit-use statement."
            ),
        },
        synthetic_data_only=True,
        recording_default_off=True,
        thresholds_are_hypotheses=True,
        audit_use_agreement=AuditUseAgreement(
            agreed_with_staff=False,
            agreed_date=None,
            staff_representatives=(),
            programme_owner=None,
            dpo_reviewer=None,
        ),
    )


def validate_programme_plan(plan: UsabilityProgrammePlan) -> dict[str, Any]:
    """Validate that a usability programme plan meets AC1, AC2, SA-009, SA-010, and NFR-009."""
    errors: list[str] = []
    script_check = validate_task_scripts(plan.tasks)
    if not script_check["valid"]:
        errors.extend(script_check["errors"])

    if not plan.cohorts:
        errors.append("missing_cohorts")

    seen_cohorts: set[str] = set()
    role_cohorts: set[str] = set()
    pilot_seen = False

    for cohort in plan.cohorts:
        if not cohort.cohort_id or cohort.cohort_id in seen_cohorts:
            errors.append(f"duplicate_or_blank_cohort:{cohort.cohort_id}")
        seen_cohorts.add(cohort.cohort_id)

        if cohort.group == "pilot":
            pilot_seen = True
            if not (
                MIN_PILOT_PARTICIPANTS
                <= cohort.min_participants
                <= cohort.max_participants
                <= MAX_PILOT_PARTICIPANTS
            ):
                errors.append(f"{cohort.cohort_id}:invalid_pilot_bounds")
            if cohort.counts_toward_role_minimum:
                errors.append(f"{cohort.cohort_id}:pilot_cannot_count_toward_role_minimum")
        else:
            role_cohorts.add(cohort.cohort_id)
            if not (
                MIN_ROLE_PARTICIPANTS
                <= cohort.min_participants
                <= cohort.max_participants
                <= MAX_ROLE_PARTICIPANTS
            ):
                errors.append(f"{cohort.cohort_id}:participants_must_be_5_to_8")
            if not cohort.counts_toward_role_minimum:
                errors.append(f"{cohort.cohort_id}:role_cohort_must_count_toward_minimum")
            if cohort.group == "resident_or_representative" and cohort.t0_applicable:
                errors.append(f"{cohort.cohort_id}:t0_not_applicable_to_resident_portal")

    expected_roles = set(pw.EVIDENCE.keys()) | {"resident", "resident-representative"}
    missing_roles = sorted(expected_roles - role_cohorts)
    if missing_roles:
        errors.append(f"missing_role_cohorts:{','.join(missing_roles)}")
    if not pilot_seen:
        errors.append("missing_proxy_pilot_cohort")

    for clause in ACCESSIBILITY_SUPPORT_CLAUSES:
        if not _clean_text(plan.accessibility_support.get(clause)):
            errors.append(f"missing_accessibility_clause:{clause}")

    missing_at = sorted(set(REQUIRED_ASSISTIVE_TECH_ROUTES) - set(plan.assistive_tech_coverage))
    if missing_at:
        errors.append(f"missing_assistive_tech_routes:{','.join(missing_at)}")

    for clause in CONSENT_DATA_CLAUSES:
        if not _clean_text(plan.consent_and_data_handling.get(clause)):
            errors.append(f"missing_consent_or_data_clause:{clause}")

    if plan.synthetic_data_only is not True:
        errors.append("synthetic_data_only_required")
    if plan.recording_default_off is not True:
        errors.append("recording_default_off_required")
    if plan.thresholds_are_hypotheses is not True:
        errors.append("thresholds_must_remain_hypotheses")

    return {
        "valid": not errors,
        "errors": errors,
        "role_cohort_count": len(role_cohorts),
        "task_script_count": len(plan.tasks),
        "audit_use_agreed": plan.audit_use_agreement.agreed_with_staff,
    }


def validate_audit_use_agreement(
    agreement: AuditUseAgreement,
    *,
    measurement_date: str | None = None,
) -> date:
    """Enforce SA-010 prior staff agreement on the non-surveillance audit-use statement."""
    if agreement.agreed_with_staff is not True:
        raise ValueError(
            "SA-010 gate: staff audit-use statement must be agreed with staff representatives "
            "before usability measures are recorded or reported."
        )
    agreed_on = _parse_iso_date(agreement.agreed_date, "agreed_date")
    if not agreement.staff_representatives or not all(
        rai_release.named_human(rep) for rep in agreement.staff_representatives
    ):
        raise ValueError(
            "SA-010 gate: staff_representatives must list at least one named human representative."
        )
    text = _clean_text(agreement.statement_text).casefold()
    required_phrases = ("aggregate", "disciplinary", "performance", "surveillance")
    if any(token not in text for token in required_phrases):
        raise ValueError(
            "SA-010 gate: statement_text must state aggregate-only reporting and prohibit "
            "individual performance, disciplinary, and surveillance use."
        )
    if measurement_date is not None:
        measured_on = _parse_iso_date(measurement_date, "measurement_date")
        if agreed_on > measured_on:
            raise ValueError(
                f"SA-010 gate: audit-use agreement date ({agreed_on.isoformat()}) must be on or "
                f"before measurement_date ({measured_on.isoformat()})."
            )
    return agreed_on


def _require_non_neg_int(value: object, field_name: str, upper: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer.")
    if upper is not None and value > upper:
        raise ValueError(f"{field_name} ({value}) cannot exceed {upper}.")
    return value


def _optional_sus(value: object, field_name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number between 0 and 100 or None.")
    fval = float(value)
    if not (0.0 <= fval <= 100.0):
        raise ValueError(f"{field_name} ({fval}) must be between 0.0 and 100.0.")
    return fval


def evaluate_role_measures(
    role_records: Mapping[str, Mapping[str, Any]],
    agreement: AuditUseAgreement,
    *,
    measurement_date: str | None = None,
    plan: UsabilityProgrammePlan | None = None,
) -> dict[str, Any]:
    """Evaluate aggregate-only usability measures per role cohort under SA-009 and SA-010."""
    _scan_forbidden_fields(role_records, "role_records")

    any_active = any(
        isinstance(rec, Mapping) and rec.get("participant_count", 0) not in (0, None)
        for rec in role_records.values()
    )
    if any_active and measurement_date is None:
        raise ValueError(
            "measurement_date (YYYY-MM-DD) is required when participant_count > 0 so SA-010 "
            "prior agreement order can be verified."
        )
    agreed_on = validate_audit_use_agreement(agreement, measurement_date=measurement_date)

    active_plan = default_programme_plan() if plan is None else plan
    cohort_by_id = {c.cohort_id: c for c in active_plan.cohorts}

    cohorts_out: dict[str, dict[str, Any]] = {}
    any_h4_breach = False

    for cohort_id, rec in role_records.items():
        if cohort_id not in cohort_by_id:
            raise ValueError(f"Unknown usability role cohort {cohort_id!r}.")
        cohort = cohort_by_id[cohort_id]
        if cohort.group == "pilot":
            raise ValueError(
                "Proxy pilot sessions must not be aggregated as representative role measures."
            )

        n = _require_non_neg_int(rec.get("participant_count", 0), f"{cohort_id}.participant_count")
        if n == 0:
            cohorts_out[cohort_id] = {
                "status": "not_run",
                "suppressed": False,
                "suppression_reason": None,
                "participant_count": 0,
                "within_target_band": False,
                "unaided_under_5m_count": None,
                "unaided_under_5m_pct": None,
                "manual_fallback_completed_count": None,
                "manual_fallback_completed_pct": None,
                "sus_median": None,
                "sus_min": None,
                "sus_max": None,
                "accessible_sus_alternative_count": None,
                "stop_rule_or_consent_blur_count": None,
                "h4_stop_rule_breach": False,
                "hypothesis_evaluation": {
                    "h1_unaided_under_5m": "not_run",
                    "h2_sus_at_least_70": "not_run",
                    "h3_manual_fallback": "not_run",
                    "h4_zero_boundary_breaches": "not_run",
                },
            }
            continue

        unaided_raw = rec.get("unaided_under_5m_count")
        unaided = (
            None
            if unaided_raw is None
            else _require_non_neg_int(unaided_raw, f"{cohort_id}.unaided_under_5m_count", n)
        )
        if cohort.t0_applicable and unaided is None:
            raise ValueError(f"{cohort_id}.unaided_under_5m_count is required for T0 cohorts.")

        manual_count = _require_non_neg_int(
            rec.get("manual_fallback_completed_count", 0),
            f"{cohort_id}.manual_fallback_completed_count",
            n,
        )
        alt_sus_count = _require_non_neg_int(
            rec.get("accessible_sus_alternative_count", 0),
            f"{cohort_id}.accessible_sus_alternative_count",
            n,
        )
        numeric_sus_count = _require_non_neg_int(
            rec.get("numeric_sus_count", n - alt_sus_count),
            f"{cohort_id}.numeric_sus_count",
            n,
        )
        if numeric_sus_count + alt_sus_count > n:
            raise ValueError(
                f"{cohort_id}: numeric_sus_count + accessible_sus_alternative_count exceeds n."
            )

        stop_count = _require_non_neg_int(
            rec.get("stop_rule_or_consent_blur_count", 0),
            f"{cohort_id}.stop_rule_or_consent_blur_count",
            n,
        )
        sus_median = _optional_sus(rec.get("sus_median"), f"{cohort_id}.sus_median")
        sus_min = _optional_sus(rec.get("sus_min"), f"{cohort_id}.sus_min")
        sus_max = _optional_sus(rec.get("sus_max"), f"{cohort_id}.sus_max")
        if (
            sus_min is not None
            and sus_median is not None
            and sus_max is not None
            and not (sus_min <= sus_median <= sus_max)
        ):
            raise ValueError(f"{cohort_id}: require sus_min <= sus_median <= sus_max.")

        h4_breach = stop_count > 0
        if h4_breach:
            any_h4_breach = True

        if n < jr.MIN_CELL_FLOOR:
            cohorts_out[cohort_id] = {
                "status": "suppressed_small_cell",
                "suppressed": True,
                "suppression_reason": "cell_below_min_floor_5",
                "participant_count": None,
                "within_target_band": False,
                "unaided_under_5m_count": None,
                "unaided_under_5m_pct": None,
                "manual_fallback_completed_count": None,
                "manual_fallback_completed_pct": None,
                "sus_median": None,
                "sus_min": None,
                "sus_max": None,
                "accessible_sus_alternative_count": None,
                "stop_rule_or_consent_blur_count": None,
                "h4_stop_rule_breach": h4_breach,
                "hypothesis_evaluation": {
                    "h1_unaided_under_5m": "inconclusive",
                    "h2_sus_at_least_70": "inconclusive",
                    "h3_manual_fallback": "inconclusive",
                    "h4_zero_boundary_breaches": "not_supported" if h4_breach else "inconclusive",
                },
            }
            continue

        if not cohort.t0_applicable:
            h1_outcome = "not_applicable"
            unaided_out: int | None = None
            unaided_pct: int | None = None
        else:
            assert unaided is not None
            unaided_out = unaided
            unaided_pct = round(100 * unaided / n)
            h1_outcome = (
                "supported" if (unaided / n) >= SA009_COMPLETION_HYPOTHESIS else "not_supported"
            )

        if numeric_sus_count < jr.MIN_CELL_FLOOR or sus_median is None:
            h2_outcome = "inconclusive"
            sus_med_out = None if numeric_sus_count < jr.MIN_CELL_FLOOR else sus_median
            sus_min_out = None if numeric_sus_count < jr.MIN_CELL_FLOOR else sus_min
            sus_max_out = None if numeric_sus_count < jr.MIN_CELL_FLOOR else sus_max
        else:
            sus_med_out = sus_median
            sus_min_out = sus_min
            sus_max_out = sus_max
            h2_outcome = "supported" if sus_median >= SA009_SUS_HYPOTHESIS else "not_supported"

        h3_outcome = "supported" if manual_count == n else "not_supported"
        h4_outcome = "not_supported" if h4_breach else "supported"

        cohorts_out[cohort_id] = {
            "status": "evaluated",
            "suppressed": False,
            "suppression_reason": None,
            "participant_count": n,
            "within_target_band": MIN_ROLE_PARTICIPANTS <= n <= MAX_ROLE_PARTICIPANTS,
            "unaided_under_5m_count": unaided_out,
            "unaided_under_5m_pct": unaided_pct,
            "manual_fallback_completed_count": manual_count,
            "manual_fallback_completed_pct": round(100 * manual_count / n),
            "sus_median": sus_med_out,
            "sus_min": sus_min_out,
            "sus_max": sus_max_out,
            "accessible_sus_alternative_count": alt_sus_count,
            "stop_rule_or_consent_blur_count": stop_count,
            "h4_stop_rule_breach": h4_breach,
            "hypothesis_evaluation": {
                "h1_unaided_under_5m": h1_outcome,
                "h2_sus_at_least_70": h2_outcome,
                "h3_manual_fallback": h3_outcome,
                "h4_zero_boundary_breaches": h4_outcome,
            },
        }

    return {
        "aggregate_only": True,
        "min_cell_floor": jr.MIN_CELL_FLOOR,
        "audit_use_agreed": True,
        "audit_use_agreed_date": agreed_on.isoformat(),
        "staff_representatives": list(agreement.staff_representatives),
        "thresholds_are_hypotheses": True,
        "any_h4_stop_rule_breach": any_h4_breach,
        "user_validation_established": False,
        "human_usability_signoff": False,
        "cohorts": cohorts_out,
    }


def _known_target_ids(plan: UsabilityProgrammePlan | None = None) -> frozenset[str]:
    active_plan = default_programme_plan() if plan is None else plan
    return (
        frozenset(s.script_id for s in active_plan.tasks)
        | frozenset(pw.EVIDENCE.keys())
        | frozenset(jr.JOURNEYS.keys())
        | frozenset(ltb.BUNDLES.keys())
        | {"same-home-contract", "same-home-negative-probe"}
    )


def log_finding(
    *,
    finding_id: str,
    target_id: str,
    cohort_id: str,
    severity: int,
    observation: str,
    impact: str,
    backlog_issue: str,
    status: str = "open",
    evidence_source: str = "moderated_participant",
    risk_owner: str | None = None,
    risk_rationale: str | None = None,
    plan: UsabilityProgrammePlan | None = None,
) -> UsabilityFinding:
    """Create and validate one severity-tagged, backlog-linked usability finding."""
    finding = UsabilityFinding(
        finding_id=finding_id,
        target_id=target_id,
        cohort_id=cohort_id,
        severity=severity,
        status=status,
        evidence_source=evidence_source,
        observation=observation,
        impact=impact,
        backlog_issue=backlog_issue,
        risk_owner=risk_owner,
        risk_rationale=risk_rationale,
    )
    check = validate_findings_log((finding,), plan=plan)
    if not check["valid"]:
        raise ValueError("; ".join(check["errors"]))
    return finding


def validate_findings_log(
    findings: Sequence[UsabilityFinding],
    *,
    plan: UsabilityProgrammePlan | None = None,
) -> dict[str, Any]:
    """Validate usability findings for severity, anonymisation, and GitHub backlog links."""
    active_plan = default_programme_plan() if plan is None else plan
    valid_targets = _known_target_ids(active_plan)
    valid_cohorts = {c.cohort_id for c in active_plan.cohorts} | {"cross-role"}
    seen_ids: set[str] = set()
    errors: list[str] = []

    for finding in findings:
        fid = _clean_text(finding.finding_id)
        if not _FINDING_ID_RE.match(fid):
            errors.append(f"invalid_finding_id:{finding.finding_id!r}")
        elif fid in seen_ids:
            errors.append(f"duplicate_finding_id:{fid}")
        seen_ids.add(fid)

        if finding.severity not in SEVERITY_LEVELS:
            errors.append(f"{fid or '?'}:invalid_severity:{finding.severity!r}")
        if finding.status not in FINDING_STATUSES:
            errors.append(f"{fid or '?'}:invalid_status:{finding.status!r}")
        if finding.evidence_source not in EVIDENCE_SOURCES:
            errors.append(f"{fid or '?'}:invalid_evidence_source:{finding.evidence_source!r}")
        if finding.target_id not in valid_targets:
            errors.append(f"{fid or '?'}:unknown_target_id:{finding.target_id!r}")
        if finding.cohort_id not in valid_cohorts:
            errors.append(f"{fid or '?'}:unknown_cohort_id:{finding.cohort_id!r}")

        obs = _clean_text(finding.observation)
        imp = _clean_text(finding.impact)
        if not obs or not imp:
            errors.append(f"{fid or '?'}:blank_observation_or_impact")
        if _EMAIL_RE.search(obs) or _EMAIL_RE.search(imp):
            errors.append(f"{fid or '?'}:email_identifier_in_finding_text")

        issue = _clean_text(finding.backlog_issue)
        if not _BACKLOG_ISSUE_RE.match(issue):
            errors.append(
                f"{fid or '?'}:invalid_or_missing_backlog_issue:{finding.backlog_issue!r}"
            )

        if finding.status == "accepted_risk":
            if not rai_release.named_human(finding.risk_owner) or not _clean_text(
                finding.risk_rationale
            ):
                errors.append(
                    f"{fid or '?'}:accepted_risk_requires_named_human_owner_and_rationale"
                )

        if finding.status == "retested" and finding.evidence_source in {
            "synthetic_walkthrough",
            "proxy_pilot",
        }:
            errors.append(f"{fid or '?'}:cannot_mark_retested_from_{finding.evidence_source}")

    by_severity = {
        label: sum(1 for f in findings if f.severity == level)
        for level, label in SEVERITY_LEVELS.items()
    }
    open_blockers = [
        f.finding_id for f in findings if f.severity == 4 and f.status in {"open", "in_progress"}
    ]
    return {
        "valid": not errors,
        "errors": errors,
        "finding_count": len(findings),
        "by_severity": by_severity,
        "open_blocker_ids": open_blockers,
    }


def _validate_outcome_record(record: OutcomeRecord, valid_targets: frozenset[str]) -> None:
    if record.target_id not in valid_targets:
        raise ValueError(f"Unknown usability outcome target_id {record.target_id!r}.")
    if record.outcome not in OUTCOMES:
        raise ValueError(f"Invalid outcome {record.outcome!r}; expected one of {OUTCOMES}.")
    if record.evidence_source not in EVIDENCE_SOURCES:
        raise ValueError(
            f"Invalid evidence_source {record.evidence_source!r}; expected {EVIDENCE_SOURCES}."
        )
    if not _clean_text(record.summary):
        raise ValueError(f"{record.target_id}: outcome summary must not be blank.")

    if record.evidence_source == "synthetic_walkthrough":
        if record.not_user_validation is not True:
            raise ValueError(
                f"{record.target_id}: synthetic_walkthrough must set not_user_validation=True."
            )
        if record.validation_label != SYNTHETIC_WALKTHROUGH_LABEL:
            raise ValueError(
                f"{record.target_id}: synthetic_walkthrough must carry exact label "
                f"{SYNTHETIC_WALKTHROUGH_LABEL!r}."
            )
    elif record.evidence_source in {"proxy_pilot", "proxy_participant"}:
        if record.not_user_validation is not True:
            raise ValueError(
                f"{record.target_id}: {record.evidence_source} must set not_user_validation=True."
            )
        if "not" not in record.validation_label.casefold():
            raise ValueError(
                f"{record.target_id}: {record.evidence_source} label must state non-validation."
            )

    if record.outcome in {"not_supported", "inconclusive"} and (
        not record.negative_or_failure_notes
        or not all(_clean_text(note) for note in record.negative_or_failure_notes)
    ):
        raise ValueError(
            f"{record.target_id}: {record.outcome} outcome must retain non-empty "
            "negative_or_failure_notes so negative or inconclusive findings are never silent."
        )


def evaluate_programme_results(
    records: Sequence[OutcomeRecord],
    *,
    findings: Sequence[UsabilityFinding] = (),
    audit_use_agreed: bool = False,
    dpo_approved: bool = False,
    expected_target_ids: Sequence[str] | None = None,
    plan: UsabilityProgrammePlan | None = None,
) -> dict[str, Any]:
    """Evaluate usability outcomes while preserving negative/inconclusive rows and non-signoff."""
    active_plan = default_programme_plan() if plan is None else plan
    valid_targets = _known_target_ids(active_plan)

    seen_targets: set[str] = set()
    for rec in records:
        _validate_outcome_record(rec, valid_targets)
        if rec.target_id in seen_targets:
            raise ValueError(f"Duplicate outcome record for target_id {rec.target_id!r}.")
        seen_targets.add(rec.target_id)

    findings_check = validate_findings_log(findings, plan=active_plan)
    if not findings_check["valid"]:
        raise ValueError("; ".join(findings_check["errors"]))

    missing_targets = (
        sorted(set(expected_target_ids) - seen_targets) if expected_target_ids is not None else []
    )
    if missing_targets:
        raise ValueError(
            "Outcome records omitted expected targets (negative/inconclusive suppression is "
            f"prohibited): {', '.join(missing_targets)}."
        )

    counts = {outcome: sum(1 for r in records if r.outcome == outcome) for outcome in OUTCOMES}
    synthetic_count = sum(1 for r in records if r.evidence_source == "synthetic_walkthrough")
    proxy_count = sum(
        1 for r in records if r.evidence_source in {"proxy_pilot", "proxy_participant"}
    )

    all_direct_human_supported = (
        bool(records)
        and synthetic_count == 0
        and proxy_count == 0
        and counts["not_run"] == 0
        and counts["not_supported"] == 0
        and counts["inconclusive"] == 0
        and all(r.not_user_validation is False for r in records)
        and audit_use_agreed is True
        and dpo_approved is True
        and not findings_check["open_blocker_ids"]
    )

    return {
        "outcome_counts": counts,
        "record_count": len(records),
        "synthetic_record_count": synthetic_count,
        "proxy_record_count": proxy_count,
        "negative_outcomes_retained": [
            r.target_id for r in records if r.outcome == "not_supported"
        ],
        "inconclusive_outcomes_retained": [
            r.target_id for r in records if r.outcome == "inconclusive"
        ],
        "open_blocker_finding_ids": findings_check["open_blocker_ids"],
        "user_validation_established": all_direct_human_supported,
        "human_usability_signoff": False,
    }


def _constructed_same_home_bundle(*, inject_premature_receipt: bool = False) -> dict[str, Any]:
    action = "Review survey evidence and confirm next coordinator step"
    secret = "SYN-ADJ-LARGE-PRINT: send 18pt printed pack before call"
    reason_roles = set(projection.reason_roles())
    staff_views: dict[str, dict[str, Any]] = {}
    for role in pjc.SIX_STAFF_PROFILES:
        staff_views[role] = {
            "id": "SYN-HOME-155",
            "stage": "Assessment",
            "closed": False,
            "can_advance": False,
            "measures": "Loft insulation",
            "home": {
                "address": "14 Fictional Terrace",
                "postcode": "ZZ1 4FT",
            },
            "resident": {
                "adjustment": secret if role in reason_roles else projection.REDACTED,
            },
            "work": {
                "owner": "Retrofit Coordinator",
                "next_action": action,
                "reason": secret if role in reason_roles else projection.NOTE_HELD,
                "blockers": [],
                "handoff": {"confirmed_receiver": "Unknown"},
            },
            "hazards": [],
            "stock_reconciliation": [{"id": "SR-155", "status": "Reconciled"}],
            "decision": {"status": "Accepted"},
            "measure_decisions": [{"measure": "Loft insulation", "status": "Accepted"}],
            "quality": [],
            "quality_handover_blockers": [],
        }

    exp_progress, exp_next = rp.STAGE_TEXT.get("Assessment", (rp.UNKNOWN_PROGRESS, rp.UNKNOWN_NEXT))
    receipt_status = "Accepted" if inject_premature_receipt else jp.SUBMITTED
    return {
        "case_id": "SYN-HOME-155",
        "staff": staff_views,
        "staff_views": staff_views,
        "contractor_summary": {
            "id": "SYN-HOME-155",
            "address": "14 Fictional Terrace",
            "postcode": "ZZ1 4FT",
            "stage": "Assessment",
            "status": "Assessment",
            "measures": "Loft insulation",
            "needs_notice": True,
            "named_contact": "Resident Liaison Officer",
        },
        "contractor_detail": {
            "id": "SYN-HOME-155",
            "home": {"address": "14 Fictional Terrace", "postcode": "ZZ1 4FT"},
            "stage": "Assessment",
            "status": "Assessment",
            "measures": "Loft insulation",
            "needs_notice": True,
            "named_contact": "Resident Liaison Officer",
            "resident_readiness": [{"measure": "Loft insulation", "flag": "Proceed"}],
        },
        "work_orders": [
            {
                "id": "WO-SYN-155",
                "case_id": "SYN-HOME-155",
                "address": "14 Fictional Terrace",
                "postcode": "ZZ1 4FT",
                "measures": "Loft insulation",
                "state": "Issued",
                "needs_notice": True,
                "named_contact": "Resident Liaison Officer",
            }
        ],
        "job_pack_receipt": {
            "measure": "Loft insulation",
            "status": receipt_status,
            "accepted": inject_premature_receipt,
        },
        "resident_view": {
            "banner": rp.BANNER,
            "home": {"address": "14 Fictional Terrace", "postcode": "ZZ1 4FT"},
            "measures": ["Loft insulation"],
            "progress": exp_progress,
            "next_step": exp_next,
            "read_only": True,
            "unavailable": [{"feature": "Consent and decisions"}],
        },
        "audit_trace": {
            "order_findings": [],
            "user_validation": "not-established",
            "stages": [
                {"stage": "handover", "status": "Not recorded"},
                {"stage": "financial_closure", "status": "Not recorded"},
            ],
        },
    }


def _constructed_bundle_run(
    bundle_key: str,
    *,
    comp_step: float,
    flow_step: float,
    breach_measure: str | None = None,
    o16_owner: str | None = None,
) -> dict[str, Any]:
    bundle = ltb.BUNDLES[bundle_key]
    first_comp = ltb.COMPONENTS[0]
    comp_effort = dict.fromkeys(ltb.COMPONENTS, 0.0)
    flow_effort = dict.fromkeys(ltb.COMPONENTS, 0.0)
    comp_effort[first_comp] = comp_step
    flow_effort[first_comp] = flow_step

    comp_counts = dict.fromkeys(bundle.zero_measures, 0)
    flow_counts = dict.fromkeys(bundle.zero_measures, 0)
    if breach_measure is not None:
        flow_counts[breach_measure] = 1

    resolved_o16 = (
        (ltb.O16_BUNDLES[0] if o16_owner is None else o16_owner)
        if bundle_key in ltb.O16_BUNDLES
        else None
    )
    return {
        "bundle": bundle_key,
        "o16_counted_under": resolved_o16,
        "representative_data_retained": False,
        "cases": [
            {
                "case": 1,
                "arms": {
                    "comparator": {"effort": dict(comp_effort), "counts": dict(comp_counts)},
                    "workflow": {"effort": dict(flow_effort), "counts": dict(flow_counts)},
                },
            }
        ],
    }


def build_synthetic_walkthrough_report() -> SyntheticWalkthroughReport:
    """Run deterministic contract walkthroughs stamped as not_user_validation=True."""
    reg = pw.register()
    records: list[OutcomeRecord] = []

    for pid in pw.EVIDENCE:
        step = {
            "record_ids": [f"SYN-{pid.upper()}-155"],
            "state_text": "Held for named human review",
            "keyboard_operable": True,
            "announcement": "Status held for named human review",
        }
        walkthrough = {
            "perspective": pid,
            "steps": {el: dict(step) for el in pjc.ELEMENTS}
            | {"handoff": dict(step, owner="Named role lead")},
        }
        validated = pjc.validate(walkthrough)
        unmet_elements = [el for el in pjc.ELEMENTS if reg[pid][el]["status"] == "unmet"]
        is_proxy_only = pid in pw.PROXY_ONLY

        if validated["blockers"]:
            records.append(
                OutcomeRecord(
                    target_id=pid,
                    outcome="not_supported",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=f"Synthetic contract check blocked on {pid}.",
                    negative_or_failure_notes=tuple(validated["blockers"]),
                )
            )
        elif unmet_elements or is_proxy_only:
            notes: list[str] = []
            if unmet_elements:
                notes.append(f"Unmet register elements: {', '.join(unmet_elements)}.")
            if is_proxy_only:
                notes.append("Reached via manager proxy role only; no direct login role exists.")
            records.append(
                OutcomeRecord(
                    target_id=pid,
                    outcome="inconclusive",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=(
                        f"Synthetic shape check passed for {pid}, but coverage remains "
                        "inconclusive until unmet/proxy elements and human sessions complete."
                    ),
                    negative_or_failure_notes=tuple(notes),
                )
            )
        else:
            records.append(
                OutcomeRecord(
                    target_id=pid,
                    outcome="supported",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=f"Synthetic 5-element contract shape check passed for {pid}.",
                )
            )

    clean_walk = pjc.validate_same_home_walk(
        _constructed_same_home_bundle(),
        case_id="SYN-HOME-155",
        vulnerability_reason="SYN-ADJ-LARGE-PRINT: send 18pt printed pack before call",
    )
    records.append(
        OutcomeRecord(
            target_id="same-home-contract",
            outcome="supported" if clean_walk["ok"] else "not_supported",
            evidence_source="synthetic_walkthrough",
            not_user_validation=True,
            validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
            summary="Constructed 6-staff, contractor, and resident same-home continuity check.",
            negative_or_failure_notes=tuple(clean_walk["blockers"]),
        )
    )

    neg_walk = pjc.validate_same_home_walk(
        _constructed_same_home_bundle(inject_premature_receipt=True),
        case_id="SYN-HOME-155",
        vulnerability_reason="SYN-ADJ-LARGE-PRINT: send 18pt printed pack before call",
    )
    records.append(
        OutcomeRecord(
            target_id="same-home-negative-probe",
            outcome="not_supported" if not neg_walk["ok"] else "supported",
            evidence_source="synthetic_walkthrough",
            not_user_validation=True,
            validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
            summary=(
                "Negative synthetic probe: worker receipt falsely marked accepted is blocked "
                "from closing quality handover."
            ),
            negative_or_failure_notes=tuple(neg_walk["blockers"])
            or ("Expected worker_receipt_treated_as_acceptance blocker.",),
        )
    )

    bundle_runs = [
        _constructed_bundle_run("story-once", comp_step=24.0, flow_step=12.0),
        _constructed_bundle_run("pre-visit-pack", comp_step=20.0, flow_step=11.0),
        _constructed_bundle_run("change-impact", comp_step=18.0, flow_step=18.0),
        _constructed_bundle_run(
            "handover-aftercare",
            comp_step=16.0,
            flow_step=14.0,
            breach_measure=ltb.BUNDLES["handover-aftercare"].zero_measures[0],
        ),
        _constructed_bundle_run("funding-evidence", comp_step=22.0, flow_step=13.0),
    ]
    o16_owner = ltb.reconcile_o16(bundle_runs)

    for run in bundle_runs:
        report = ltb.run_report(run)
        bkey = str(report["bundle"])
        delta = float(report["median_difference_minutes"])
        if report["stop"]:
            records.append(
                OutcomeRecord(
                    target_id=bkey,
                    outcome="not_supported",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=(
                        f"Synthetic bundle {bkey} triggered STOP rule before effort comparison."
                    ),
                    negative_or_failure_notes=tuple(report["breaches"]),
                )
            )
        elif delta == 0.0:
            records.append(
                OutcomeRecord(
                    target_id=bkey,
                    outcome="inconclusive",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=(
                        f"Synthetic bundle {bkey} showed zero median effort difference (0.0 min)."
                    ),
                    negative_or_failure_notes=(
                        "Constructed tie between workflow and comparator arms; inconclusive.",
                    ),
                )
            )
        elif delta > 0.0:
            records.append(
                OutcomeRecord(
                    target_id=bkey,
                    outcome="not_supported",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=(
                        f"Synthetic bundle {bkey} workflow required more effort than comparator."
                    ),
                    negative_or_failure_notes=(f"Median delta +{delta} minutes.",),
                )
            )
        else:
            records.append(
                OutcomeRecord(
                    target_id=bkey,
                    outcome="supported",
                    evidence_source="synthetic_walkthrough",
                    not_user_validation=True,
                    validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
                    summary=(
                        f"Synthetic bundle {bkey} completed with zero stop-rule breaches and "
                        f"constructed delta {delta} minutes."
                    ),
                )
            )

    evaluated = evaluate_programme_results(records)
    return SyntheticWalkthroughReport(
        not_user_validation=True,
        validation_label=SYNTHETIC_WALKTHROUGH_LABEL,
        user_validation_established=False,
        human_usability_signoff=False,
        records=tuple(records),
        outcome_counts=dict(evaluated["outcome_counts"]),
        same_home_clean_status=str(clean_walk["status"]),
        same_home_negative_probe_blockers=tuple(neg_walk["blockers"]),
        o16_reconciled_owner=o16_owner,
        notice=(
            f"{SYNTHETIC_WALKTHROUGH_LABEL}. Deterministic contract and constructed-bundle "
            "checks verify task-script derivation, SA-010 gates, and negative/inconclusive "
            "reporting only; moderated sessions with 5-8 representative users per role, "
            "staff SA-010 agreement, and DPO sign-off remain unexecuted."
        ),
    )
