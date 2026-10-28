<!-- markdownlint-disable-file -->
# RPI Plan: Fictional Finance form/template review pack (#97), recovery

## Task Metadata

* Task ID: 97-recovery
* Task slug: fictional-form-review-97-recovery
* Planning status: ready
* Plan date: 2026-10-20
* Phase details: .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-20/fictional-form-review-97-recovery-plan-critique.md

## Executive Summary

This plan finishes a fictional, versioned form/template and Finance authority/binding review pack for #97 so people can review a concrete object instead of an abstract gap. It reuses the already merged forms schema contract and adds data, one focused fixture test, a provenance registration, a short review note and mechanical index entries. It adds no runtime, approval, signature, submission or payment path.

The earlier pass wrote an uncommitted fixture, test, register entry and artifacts without activating the RPI skills. This recovery cycle treats those files as an unverified draft: implementation must re-verify, correct and own them through `rpi-implement`, not assume they are right.

### User Decisions and Requirements Highlights

* Fictional pack only; it is not an approved template, so criterion 1 stays unmet and no closing keyword is used.
* Existing contracts and PR 377 are reused; nothing is rebuilt or expanded.
* Finance authority and binding fields stay explicit, unresolved and null.

### What You May Not Know

* The contract requires a registered reviewer email, while the privacy checker rejects emails in public JSON, so the test registers a reviewer-substituted copy of the public schema.
* Stale propagation and preparer/reviewer separation are not enforced by any runtime; the pack states them as proposed data for review only.
* Any later commit, rebase or base move invalidates the final local gate receipt.

### Unresolved Decisions or Blockers

* Actual Finance authority, template source and version, scheme terms and binding: Finance and Grants, Legal supply; human gate, not blocking this plan.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Deliver a fictional versioned Finance form/template and authority/binding pack for actual review, not approved-template status (owner comment on #126, 6290697705).
* Existing engineering and durable candidate staging delivered in PR 377; do not rebuild it or expand runtime.
* Integrate a concrete reviewable synthetic template using existing schema contracts, covering field types, units, required and conditional fields, source authority, evidence, version and freshness, parser/OCR lineage, preparer/reviewer separation and stale-field propagation.
* Include actual unresolved Finance binding/authority decision fields and clear not-approved, no-submission and no-payment labels.
* Do not fabricate Finance signatures or actual grant or contract terms.
* New public synthetic fixtures need existing provenance registry registration.
* Focused tests only for genuinely introduced fixture behavior; no new schema engine, service or runtime.
* Do not edit the infra runbook, budget/benefits synthesis, map or cohort docs; KB index and log append-only overlap is allowed.
* Run genuine RPI skills; treat the earlier hand-authored draft as unverified; disclose and preserve it (coordinator intervention).
* Full local gate, clean frozen LOCAL handoff, no push.

## Goals

* A reviewer can open one registered fictional pack and see every form field with type, unit, requirement, authority, evidence and freshness, plus each unresolved Finance decision.
* The pack is mechanically proven compatible with the existing `forms` contract.
* Every statement of status says not approved, no submission, no payment.

## Scope and Non-Goals

### In Scope

* src/core/evals/fictional_form_review_pack.json and registration in the provenance register.
* src/core/tests/test_form_review_pack.py.
* Data dictionary subsection, KB review note, core README pointer, index row and log entry.
* Recovery RPI evidence and a disclosure clarification on the preserved draft artifacts.

### Non-Goals

* New runtime, loader, API, schema engine or service; edits to forms.py behavior.
* Real templates, grant terms, signatures, approvals, submission, payment.
* Editing the generator-owned src/importer/evals/document_form_fixtures.json.
* Infra runbook, budget/benefits synthesis, map, cohort docs.

## Functional Requirements

* The pack's schema registers through the existing registration path on both stores as Unapproved.
  * Observable acceptance criteria: focused test passes on Store and SqlStore; raw pack schema (placeholder reviewer) is refused.
* Review tables, calculations and stale map reference only declared fields and calculations; stale triggers are exhaustive and disjoint.
  * Observable acceptance criteria: focused test asserts exact sets.
* All Finance decision fields are null and unresolved; roles are distinct; labels present; separation is stated as proposed.
  * Observable acceptance criteria: focused test asserts each.
* The pack is registered as public with a root label and passes the privacy checker.
  * Observable acceptance criteria: test_synthetic_provenance and the pack test pass.

## Non-Functional Requirements

* No real personal data or credentials in public payloads.
  * Objective threshold or evaluation condition: privacy checker reports zero issues.
  * Observable acceptance criteria: public_issues empty for the pack.
* Existing quality gates hold.
  * Objective threshold or evaluation condition: ruff check, ruff format check and mypy clean in src/core.
  * Observable acceptance criteria: commands exit 0.
* Markdown follows repository style (ASCII, `*` bullets, no em dashes), relative links resolve.
  * Observable acceptance criteria: link review and diff review.

## Acceptance Criteria

* Pack, test and registration pass focused validation; no runtime file changed.
* Issue criterion 1 is stated as unmet; criterion 2 as delivered by PR 377; no closing keyword.
* KB index and log updated append-only; excluded docs untouched.
* Preserved draft artifacts carry a dated disclosure clarification, unrewritten.
* One genuine Review and a full local gate receipt on a clean frozen head (post-plan handoff).

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-10-20/fictional-form-review-97-recovery-plan.md |
| Phase details | .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-20/fictional-form-review-97-recovery-plan-critique.md with Revise (one run, executed by a worker activating rpi-plan-critique); PC-001 to PC-007 dispositioned below |
| Relevant research | .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md |
| Changes-record role | .copilot-tracking/changes/2026-10-20/fictional-form-review-97-recovery-changes.md is created by implementation |
| Planning execution and readiness | complete; ready |
| Continuation context | manual standalone; coordinator directs continuation to rpi-implement |

## Sources

* .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md: C1-C14 evidence and recommendation.
* src/core/src/zava_forward/core/forms.py: schema and registration contract.
* docs/reference/research/retrofit-synthetic-data/provenance-register.json: registry contract.
* Uncommitted draft (unverified): src/core/evals/fictional_form_review_pack.json, src/core/tests/test_form_review_pack.py.
* /tmp/ama-wave-20261020-2113-common.md: caller delivery contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile pack, test and registration

* Intent: Verify the unverified draft against the contract and correct it.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Verify and correct the pack fixture

* Requirement and evidence: Compatibility, labels, null decisions (C1-C6, C12).
* Expected result: Pack content reconciled; every authority field unresolved.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Verify the focused test and registration

* Requirement and evidence: Fixture behavior tests only; registry registration (C7, C8).
* Expected result: Test and DS-FICT-FORM-REVIEW-PACK entry pass focused checks.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Knowledge base integration

* Intent: Make the pack discoverable and honest in the KB.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Dictionary subsection and review note

* Requirement and evidence: Registry dictionary anchor (C8); review use (owner direction).
* Expected result: data-dictionary subsection and form-review-pack-97.md.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: README pointer, index row, log entry, disclosure clarifications

* Requirement and evidence: KB conventions; coordinator disclosure.
* Expected result: Pointer, index and append-only log; dated clarification on preserved draft artifacts.
* Detail section: P02-T02 in .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Validation and evidence

* Intent: Prove the change and record it.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Focused checks and changes record

* Requirement and evidence: Focused test, provenance and staging tests, ruff, format, mypy, link review.
* Expected result: Passing outputs recorded in the changes record.
* Detail section: P03-T01 in .copilot-tracking/details/2026-10-20/fictional-form-review-97-recovery-phase-details.md

## Dependencies

* Python venv /tmp/ama-97-venv with src/core[dev]: needed to run tests and linters.
* No competing heavy suite while other tasks' gates run.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| PC-001 field_review stale_on and max_source_age_days lack triggers | resolved (planner) | P01-T01 adds survey, design, funding-evidence, consent and source-age triggers (or aligns stale_on); P01-T02 asserts every field stale_on maps to a trigger listing that field |
| PC-002 no-submission and no-payment labels not asserted | resolved | P01-T02 asserts NOT APPROVED, No submission and no payment |
| PC-003 lineage untested | resolved | P01-T02 asserts stage_candidates refuses human-only fields on the registered pack schema and lineage keys match the contract, reusing test_form_staging helpers |
| PC-004 no element checklist | resolved | P01-T01 carries the element to proof mapping, reproduced in the changes record |
| PC-005 source ranks may look agreed | resolved | P01-T01 adds an asserted statement that ranks and evidence refs are fictional proposals pending FD-07 and FD-09 |
| PC-006 dependency and lifecycle gaps | resolved | P03-T01 names ruff, format and mypy commands; details add venv recreation, pre-append SHA-256 of preserved artifacts and a src/core/src no-change diff check |
| PC-007 wording and anchor | resolved | P02 validation checks the anchor and the phrases fictional, not approved, criterion 1 unmet |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-20/fictional-form-review-97-recovery-changes.md
* Ready phase or task: none; P01-P03 complete, original Review recorded (Residual work), registry correction applied after the failed local gate
* Validation state: the first full gate failed at 106fbc96 (receipt /tmp/ama-serial-2150-97/receipt.json retained); a NEW full gate is pending and is not passed
* Remaining provisional question or blocker: none; actual Finance authority FD-01..FD-14 stays unapproved (Refs #97 only)

## Correction Update 2026-10-20 (implementation-time, current state)

* Affected area: P01-T02 registration. The full gate failed in agents test_eval_registry because the pack was absent from src/agents/evals/registry.json and had no top-level version key.
* Reconciliation: registry entry fictional-form-review-pack added and version fictional-form-review-pack-v1 added to the pack. Focused evidence: test_eval_registry 8 tests OK; test_form_review_pack and test_synthetic_provenance 20 tests OK. Approved intent and scope unchanged; no re-critique or second Review.

## Correction Update 2026-10-21 (hosted advisory)

Hosted Source CI failed on fixable GHSA-6q48-6c7w-9gw2 (certifi). The four lockfile blobs from the existing #119 correction a3257c71 were applied unchanged; see the changes record. Scope, approved intent and the single critique and Review are unchanged. Open: fresh full gate, hosted rerun, and the separate rubric exactly-20-criterion-IDs blocker (not edited here). Finance authority remains unresolved.
