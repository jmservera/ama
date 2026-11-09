---
title: Equity, journey ownership and user research test plan (issue 128)
description: Test plan, status and blank human records for accessibility, unfair-exclusion and journey-ownership checks, with the aggregate-only user research protocol draft
ms.date: 2026-11-04
ms.topic: reference
---

## Purpose and status

Issue #128 covers BRD NFR-008 and NFR-009 and PRD SA-009 and SA-010. This page
is a plan and a set of blank records, not a result. At 2026-11-03 no screen
reader run, no user research and no owner decision has happened. No resident
or employee took part, and nothing here is a conformance or fairness claim.

Related evidence that already exists:

* [Production UX acceptance protocol](./production-ux-acceptance-protocol.md)
  holds the keyboard and screen reader scripts for the chat widget and case
  view. Those rows are `Not run`.
* [WCAG baseline](./wcag-conformance-baseline.md#map-list-alternative-screen-reader-check-119)
  holds the map list alternative check, also open.
* [Resident journeys](./customer-journeys/residents.md) J1 to J6 and R1 each
  state a non-digital equivalent.
* The ranking cohort and missing-data evaluation (`cohort_ranking_eval`,
  `cohort_eval`, #222) covers paired constructed cohorts and seeded defects.

## Engineering added in this slice

* `zava_forward.core.journey_register` holds a draft register of the seven
  resident journeys against the eight service-time measures in AC-071, and
  checks a supplied register. The draft has no owner, escalation, threshold or
  manual alternative test, so it reports `blocked`. The check never supplies an
  owner or threshold.
* The same module routes a case with missing source or sensor data, unknown
  support or an incomplete appointment to a human review route with reasons.
  The route carries no score and has no effect on rank or service. It counts
  review burden per reason, in aggregate.
* `zava_forward.core.paired_equity` (second slice) checks constructed pairs that
  differ in one attribute only: sensor completeness, support or contact need, or
  appointment history. A pair passes when the subject is ranked no lower than the
  reference under the deterministic policy and its review route has no rank
  effect. Results are per dimension, never averaged; a dimension with no pairs or
  any failure blocks, and a seeded defect that is not detected blocks. It covers
  the deterministic policy only, takes the ranker as input so a non-AI comparison
  stays transparent, approves nothing and is not fairness evidence.

## Test plan

| Check | Scope | Who runs it | Status |
| --- | --- | --- | --- |
| Keyboard only | Each journey J1 to J6 and R1 screen, the map list alternative, the prioritised queue | A person | Not run |
| Screen reader | NVDA with Firefox and VoiceOver with Safari, same scope | A person | Not run |
| Non-digital alternative | Phone, letter or visit path for each journey, timed against the owner's service time | Journey owner with a staff member | Not run |
| Missing data and incomplete appointments | Human review route exists and reviewers can correct data | Reviewer with a data lead | Engineering routing only |
| Cohort comparison | Paired constructed cohorts for sensor completeness, support need, source completeness and appointment history | Pure evaluator | Exists for ranking; AI tasks, geography and archetype not covered |

## User research protocol (draft, not agreed)

* Participants: per PRD SA-009, 5 to 8 users per role. Recruitment is not
  started and needs a privacy and ethics decision first.
* Tasks: find a case, say the next step and owner, unaided, with a five minute
  limit. SUS target of 70. These thresholds are proposals from the PRD.
* Reporting: aggregate only (SA-010). No individual result, recording or
  quote is stored in the repository or shown to managers.
* Audit-use statement: agreed with staff before any measure is reported.
  Participation is voluntary, a refusal has no effect on service, and a
  participant may use a manual route throughout.
* Accessibility: offer participants with assistive technology, and record
  needs only when volunteered.

Agreement record:

| Item | Named agreeing person | Date | Status |
| --- | --- | --- | --- |
| Protocol and thresholds | | | Not agreed |
| Audit-use statement with staff | | | Not agreed |
| Lawful basis and minimum fields | | | Not agreed |

## Journey ownership record

| Journey | Owner | Escalation | Thresholds approved (OD-09, OD-25) | Manual alternative tested |
| --- | --- | --- | --- | --- |
| J1 to J6, R1 | Not assigned | Not assigned | Not approved | Not tested |

## Acceptance criteria status

* Keyboard and screen reader testing: unmet, scripts exist, no run.
* Missing data and incomplete appointments get human review: partly met in
  engineering (routing helper and cohort evaluation); no staffed review
  workflow, so not met.
* User research protocol agreed, aggregate only: unmet, draft only.
* RAI cohort criteria: ranking cohorts delivered earlier (#222); AI task
  cohorts, geography and archetype, and approved thresholds remain unmet.
  Paired-cohort checks for the deterministic policy now exist
  (`paired_equity`); expected pair labels still need independent human
  approval, so no cohort criterion is met.
