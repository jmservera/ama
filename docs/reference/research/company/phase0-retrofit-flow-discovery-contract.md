---
title: Phase 0 Retrofit-Flow Discovery Contract and Governance Guard
description: Specification synthesis and evidence boundaries for the deterministic Phase 0 PAS 2035 lifecycle dictionary, two-sided constraint register, and fail-closed owner-validation guard (Issue 124, BG-011)
author: AMA Research Team
ms.date: 2026-11-15
ms.topic: reference
---

## Purpose and Scope

This synthesis documents the Phase 0 retrofit-flow discovery contract delivered
in [discovery_contract.py](../../../../src/core/src/zava_forward/core/discovery_contract.py)
and aligned across
[discovery_register.py](../../../../src/core/src/zava_forward/core/discovery_register.py)
and [discovery_flow.py](../../../../src/core/src/zava_forward/core/discovery_flow.py)
for Issue #124 and business goal `BG-011` (`OBJ-11`, `RULE-019`, `OD-16`,
`OD-18`) in the
[Agentic Retrofit Programme BRD](../../../brds/agentic-retrofit-programme-brd.md)
and the
[Retrofit Flow and Constraint Discovery Brief](../../../brds/retrofit-flow-discovery-brief.md).

The software contract is a pure, offline, deterministic Python 3.12 rule layer.
It reads no live company or resident records, invokes no AI model, and mutates no
operational database, keeping Phase 0 discovery executable manually when AI is
unavailable. Because Zava North Homes is a case-study housing association
(see [Company Profile Research](./company-profile-research.md)), all default
seed dictionaries, synthetic flow summaries, and candidate constraint registers
remain unvalidated candidate hypotheses (`owner_validated=False`,
`finding_status="candidate_hypothesis_not_company_finding"`) until real
sponsor nomination, domain-owner validation, and an approved twelve-month
company extract exist.

## Standards and Evidence Provenance

| Source | Classification | Source and retrieval dates | Scope and limitation |
| --- | --- | --- | --- |
| [PAS 2035:2023 BSI Overview](../../regulatory/retrofit-standards-and-funding/pas-2035-2023-bsi-overview.md) | Standards-body overview guidance (technical standard summary, not statutory legislation) | Published September 2023 (PAS 2035:2023 mandatory transition noted 2025-03-30); local snapshot retrieved 2026-09-19 | Confirms whole-dwelling retrofit process, Retrofit Assessor, Retrofit Designer and Retrofit Coordinator role boundaries, and handover/evidence responsibilities. Licensed PAS 2035:2023 clause text is not held in the repository (`gap-pas-2035-licensed`); no unverified clause numbers are asserted |
| [Agentic Retrofit Programme BRD](../../../brds/agentic-retrofit-programme-brd.md) | Internal programme requirements baseline (`BG-011`, `RULE-019`, `OD-14`, `OD-16`, `OD-18`, `OD-36`) | Dated 2026-11-15 in repository | Defines `assessment-to-ready-to-install` as the primary `BG-011` cycle-time leg and `accepted handover` as the quality-gated programme completion endpoint, keeping intended energy outcome measurement separate |
| [Retrofit Flow and Constraint Discovery Brief](../../../brds/retrofit-flow-discovery-brief.md) | Internal Phase 0 discovery specification | Updated 2026-11-15 | Defines discovery owner nomination, population inclusion rules, time attribution without guessing, the five-part constraint test, two-sided evidence rules, and the five initial candidate hypotheses |

Legal, regulatory, and technical-standard interpretation remains under named
human professional and operational approval. Software helpers record and verify
human sign-off metadata; they never decide that a PAS 2035 or housing-safety
duty is satisfied.

## Discovery Owner Nomination and Endpoint Agreement

`NominatedDiscoveryOwner`, `nominate_discovery_owner`, and
`agree_discovery_endpoint` enforce the Phase 0 accountability prerequisite:

* Both the nominating Executive Sponsor and the nominated Discovery Owner must
  be distinct, named human actors; blank values, placeholders (`TBD`, `pending`,
  `unknown`, `self`), and automated or AI tokens (`AI`, `agent`, `bot`,
  `copilot`, `system`, `workflow`) are rejected on both helper calls and direct
  dataclass construction.
* The discovery endpoint must be explicitly agreed as `accepted handover` (never
  `practical completion` or commercial `invoice`) on or after the nomination
  date before `NominatedDiscoveryOwner.status()` reaches `ENDPOINT_AGREED`.

## PAS 2035 and Retrofit Lifecycle Dictionary

`LifecycleDictionary` (`build_default_lifecycle_dictionary`) structures five
domain-validated sub-dictionaries through `accepted handover`:

### Ordered Stages and Exception or Terminal States

| Order | Code | Kind | PAS 2035 and operational boundary | Accountable validation role |
| --- | --- | --- | --- | --- |
| 1 | `candidate_identification` | `flow` | Asset strategy and cohort eligibility boundary before PAS 2035 assessment | Asset Director and Retrofit Programme Manager |
| 2 | `resident_engagement_and_survey_booking` | `flow` | Accessible resident information and reasonable-adjustment check before survey | Resident Engagement and Housing |
| 3 | `pas2035_retrofit_assessment` | `flow` | Whole-dwelling assessment by competent Retrofit Assessor | Retrofit Assessor and Retrofit Programme Manager |
| 4 | `safety_and_dependency_triage` | `flow` | Statutory hazard, damp and mould, and fabric/enabling-works gate before design release | Building Safety, Repairs and Assets |
| 5 | `pas2035_design_and_coordination` | `flow` | PAS 2035 measure package design and Retrofit Coordinator approval | Retrofit Designer and Retrofit Coordinator |
| 6 | `resident_works_decision` | `flow` | Plain-language measure scope, disruption, and informed resident decision | Resident Engagement and Housing |
| 7 | `funding_capacity_and_work_release` | `flow` | Grant/budget eligibility, committed supplier capacity, and work release | Finance, Procurement and Retrofit Programme Manager |
| 8 | `appointment_and_installation` | `flow` | Resident appointment window, site installation, and contractor practical completion | Programme and Contract Manager |
| 9 | `quality_and_evidence_acceptance` | `flow` | Independent physical inspection clearance and PAS 2035 documentary evidence acceptance | Programme and independent quality owner |
| 10 | `resident_and_accepted_handover` | `flow` | Accessible resident operating handover and `accepted handover` completion gate | Retrofit Programme Manager |
| 11 | `paused` | `exception` | Open hold with recorded restart condition retained in baseline population | Retrofit Programme Manager |
| 12 | `excluded` | `terminal` | Stock or scheme ineligibility retained in baseline denominator with reason | Asset Director and Retrofit Programme Manager |
| 13 | `withdrawn` | `terminal` | Resident refusal or withdrawal preserved distinctly from failed access | Resident Engagement and Housing |
| 14 | `cancelled` | `terminal` | Cancelled work order or cohort exit retained visibly in baseline accounting | Retrofit Programme Manager |
| 15 | `reopened_aftercare` | `exception` | Post-handover defect, callback, or evidence reopen blocking clean handover until closed | Programme and independent quality owner |

### Separate Lifecycle Events, Timestamps, Wait States, and Return Loops

* Fifteen distinct events (`REQUIRED_LIFECYCLE_EVENTS`) keep `candidate selection`,
  `retrofit assessment completed`, `design approved`,
  `resident works decision recorded`, `ready to install`, `work release`,
  `appointment`, `installation`, `practical completion`, `invoice`,
  `documentary completion`, `physical acceptance`, `evidence acceptance`,
  `resident handover`, and `accepted handover` separate so commercial, site,
  documentary, quality, and resident milestones are never conflated.
* Eight timestamp specifications (`REQUIRED_TIMESTAMP_CODES`) govern
  `stage_entered_at`, `stage_exited_at`, `active_work_started_at`,
  `active_work_completed_at`, `event_occurred_at`, `wait_started_at`,
  `wait_ended_at`, and `loop_recorded_at`. Dates must be ISO-8601 `YYYY-MM-DD`
  or timezone-aware ISO-8601 datetimes with a `source_ref`. When explicit
  active-work start and finish timestamps are absent, `active_days` stays `None`
  and is never imputed as calendar time minus wait time.
* Seven governed wait states (`REQUIRED_WAIT_STATE_CODES`) cover supplier or
  professional capacity, unaccepted handoff or approval queues, resident access
  or adjustment or decision readiness, safety or hazard holds, building or
  planned-maintenance dependencies, funding or payment holds, and quality or
  evidence remediation. `UNKNOWN` and `DISPUTED` causes and `Unattributed`
  parties remain visible without inference.
* Four return-loop kinds (`return`, `rejection`, `repeat visit`, `reopen`)
  record backward flow and rework without treating failed access as resident
  refusal. Every dictionary specification (`StageSpec`, `EventSpec`,
  `TimestampSpec`, `WaitStateSpec`, and `ReturnLoopSpec`) records
  `validated_role` alongside `validated_by` and `validated_on`, requiring
  `validated_role == owner_role` in `.validated` and
  `lifecycle_dictionary_gaps()`, while `LifecycleDictionary.__post_init__`
  enforces canonical `1..10` `REQUIRED_FLOW_STAGE_CODES` ordering.
* `evaluate_property_flow` restricts cohort aggregations strictly to in-window
  `baseline_candidate_ids` on or before `as_of` (recording unmatched-cohort and
  post-cutoff records as explicit `gaps`); retains zero-event, paused,
  excluded, cancelled, and withdrawn baseline candidates with
  `zero_event_candidate_ids` determined strictly by valid in-cohort `<= as_of`
  lifecycle event presence; computes both the `BG-011`
  `assessment-to-ready-to-install` cycle-time leg and the
  `candidate-selection-to-accepted-handover` and post-installation legs; reports
  separate `unknown_cause_count` and `disputed_cause_count` counters on each
  `waits_by_party` row alongside `unknown_or_disputed_count`; checks that
  `accepted handover` is preceded by `design approved`,
  `resident works decision recorded`, `physical acceptance`,
  `evidence acceptance`, and `resident handover` with no unresolved
  post-handover `reopen`; and tracks intended energy outcome status separately.

## Ranked Constraint Register and Two-Sided Evidence Rule

`RankedConstraintRegister` (`build_seed_constraint_register`) maintains a
contiguous `1..N` test order across the five candidate hypotheses (`CAP`,
`HANDOFF`, `RESIDENT`, `DEPEND`, `QUALITY`):

* Every `ConstraintHypothesis` records separate typed tuples for
  `supporting_evidence` (`direction="supports"`) and `contradicting_evidence`
  (`direction="contradicts"`), where each `EvidenceRecord` requires a non-blank
  `statement`, traceable `source_ref`, and human `recorded_by`. If a twelve-month
  search finds no counter-examples, the analyst records a traceable
  counter-search `EvidenceRecord` with `direction="contradicts"` citing the
  searched population extract, so `contradicting_evidence` is never omitted.
* Accepting a hypothesis (`validate_constraint_by_domain_owner` with
  `accept=True`) requires non-empty `supporting_evidence`, non-empty
  `contradicting_evidence`, all five `ConstraintTestAssessment` booleans set to
  `True`, a human validator matching `domain_owner_roles`, and proposer
  separation (`validator != proposed_by`).
* When contradicting evidence refutes or leaves a candidate hypothesis
  unresolved, the domain owner records `accept=False` (`review_status="DISPUTED"`).
  Validated registers and Phase 0 discovery packs preserve `DISPUTED` hypotheses
  visibly with `owner_validated=False` and
  `finding_status="candidate_hypothesis_not_company_finding"`.

## Fail-Closed Output Governance Guard

Every discovery output across `discovery_contract`, `discovery_register`, and
`discovery_flow` carries `owner_validated=False` and
`finding_status="candidate_hypothesis_not_company_finding"` until formal
nominated-owner sign-off:

* Dataclass `__post_init__` checks and `enforce_governance_guard` raise
  `GovernanceViolationError` (`ValueError`) whenever any report, hypothesis,
  register, pack, or output mapping claims `owner_validated=True` or
  `finding_status="owner_validated_company_finding"` without a
  `NominatedDiscoveryOwner` in `ENDPOINT_AGREED` state, a zero-gap
  domain-validated `LifecycleDictionary`, zero unresolved `FlowDiscoveryReport`
  gaps and zero `invalid_accepted_handover_ids`, complete two-sided evidence,
  and sign-off by the exact nominated human discovery owner.
* `FlowDiscoveryReport` recursively freezes all nested mappings and sequences
  via `FrozenDict` and `tuple` coercion while binding construction,
  `validate_flow_report`, `Phase0DiscoveryPack`, and `enforce_governance_guard`
  to a verified SHA-256 `calculation_digest`, blocking post-calculation or
  post-sign-off container mutation while preserving `dataclasses.asdict()`
  serialization.
* In `discovery_register`, domain-only `decide()` preserves legacy
  `is_company_finding` compatibility while keeping `owner_validated=False` and
  `finding_status="candidate_hypothesis_not_company_finding"` until
  `validate_owner_finding` verifies owner nomination, `accepted handover`
  endpoint agreement, and zero `dictionary_gaps`.

## Verification and Open Human Gates

Deterministic unit coverage lives in
[test_discovery_contract.py](../../../../src/core/tests/test_discovery_contract.py),
`src/core/tests/test_discovery_register.py`, and
`src/core/tests/test_discovery_flow.py`. Software contract verification does not
close real-world Zava North Homes governance gates: Executive Sponsor nomination
of the Discovery Owner, operational domain-owner validation of the PAS 2035
dictionary, commissioning of an approved twelve-month linked property-flow
extract, and formal owner validation of company findings (`OD-14`, `OD-16`,
`OD-18`, `OD-36`) remain open human decisions.
