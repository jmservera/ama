<!-- markdownlint-disable-file -->
# RPI Plan: Finance draft review and held decisions

## Task Metadata

* Task ID / slug: finance-96-98-99
* Date: 2026-10-27
* Status: Ready for the independent slice; original critique Revise retained, PC-001..003 directly resolved
* Details: .copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/finance-96-98-99-plan-critique.md

## Executive Summary

Implement the independent portion of #96/#98: isolated working field reviews with history, deterministic draft diagnostics, and evidence-linked diagnostic manifests. Record unresolved Finance and Board decisions durably and expose a held acceleration signal for #99. This is not approved form preparation, a reviewed funding/claim pack, eligibility determination or an affordability pass.

### What You May Not Know

The prerequisite #97 is closed for engineering only. Every existing schema remains Unapproved. Actual template/source/rule authority and Board OD-12/15 are unavailable; fixtures cannot supply them. Reviewed export, full transitive invalidation and approved tolerance breach/restart remain blocked, not replaced with fictional approvals.

## User Decisions and Requirements

* Run research, plan, implement and review in order; commit dated evidence.
* Use the supplied branch for one draft PR to main covering #96, #98 and #99, with Refs unless all criteria are proven.
* No invented figures or financial approvals; implement independent work and report missing human decisions.
* New code in src per ADR 0006, tests outside packages, workflow/check names unchanged.
* Local relevant tests only; no --all, Azure, secrets, .env, private datasets or uv. A scoped heavy gate is optional only for a large change and requires the named nonblocking lock.
* Conventional commit and Copilot trailer; resolve privacy-safe email from gh api user; push without force.

## Goals

* Preserve every prior field value, named reviewer, reason and source lineage without altering authoritative case data.
* Make unavailable financial authority explicit and durable rather than success-shaped.
* Deliver a useful safe engineering slice and an honest acceptance matrix.

## Scope and Non-Goals

In scope: core draft-review module, authenticated case form-review endpoint, isolated persistence, synthetic unit/HTTP regressions, component documentation and evidence.

Non-goals: UI changes, AI changes, template/rule approval APIs, approved calculations/eligibility, reviewed application/claim export, live financial delegation, programme-wide acceleration enforcement or restart. Source/schema freshness is evaluated on diagnostic reads/actions; it does not claim complete FR-043 transitive propagation to existing approvals.

## Functional Requirements

* Open a clearly unapproved working review record against an exact registered schema.
* Accept a same-case staged candidate, correct with explicit source/reason, or reject one value field. Do not accept authority-bearing categories. Preserve original staging and other fields.
* Require optimistic draft version on writes; refuse forged actor/status keys and stale candidate acceptance.
* Produce field-specific Unknown/Conflict/Fail draft diagnostics using only confirmed values for conditions and type checks. Approved-rule validation always remains Not evaluated, reviewed readiness Held.
* Diagnostic manifest binds schema/template/rule references, field values/review history, source hash/version/locator and attachment references, with a not-reviewed/not-submitted notice.
* Recompute field freshness against exact bound source and latest schema version. Report only bound fields stale for source changes; schema changes affect every schema-bound field. Preserve historical records and unrelated decisions.
* Ledger missing template/rule authority and Board envelope/tolerances with null approval/amount inputs, actor/time, owner role and correction path. Diagnostic acceleration signal is Pause for human decision, never an invented threshold/breach or a live hold.

## Non-Functional Requirements

* Reuse forms._actor and change_provenance.controlled for current server-side actor checks, SQL writer rechecks and atomic rollback.
* Form review data never appears in ordinary case, contractor or generic export projections; quarantined evidence cannot disclose stored values/history.
* Use installed packages, standard library and existing test/tool commands; no dependency or workflow changes unless needed for narrow typing integration.
* No silent failure: unsupported action, missing case, stale version, storage error and insufficient rights surface through existing HTTP error patterns.

## Acceptance Criteria

These are engineering-slice criteria, not replacements for issue acceptance:

* An action changes exactly its own field plus append-only review/decision history; sources, sibling fields, finance/grants/ranking/consent are unchanged.
* JSON and SQLite reopen preserve field reviews and held decisions; failed audit/save leaves no partial change. JSON supports one Store/writer with in-instance version checks, not independent processes. SQLite rowversions protect independent writers.
* Source, schema, conditional-required, type and conflicting candidates have explicit bounded diagnostics; no unreviewed candidate is used as a confirmed input.
* A manifest contains matching field IDs/values, source hashes/locators, template/input versions and history, but reviewed_ready is always false and financial states remain unchanged.
* Missing human decisions remain visibly Held with no invented approval/limits.
* Role, cross-case source, forged keys, human-only fields, infected evidence and HTTP service errors are tested.

## Sources

Research: .copilot-tracking/research/2026-10-27/finance-96-98-99-research.md, C1..C9/W1/W2. Requirements: PRD FR-038..043/AC-048..051/054; BRD RULE-010..012 and OD-12/15; ADR 0006. Linked issue comments explicitly deny approval inference.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Independent draft controls

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Core review, diagnostic manifest and held ledger

Use the existing actor/transaction boundaries and per-case JSON persistence; no new SQL table or shared global policy.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire authenticated HTTP and projection isolation

Depends on P01-T01. Add one case form-review endpoint using existing handler error conventions. Strip review records from ordinary detail before projection.

<!-- rpi:phase id=P02 -->
### [x] P02: Evidence, documentation and validation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Prove independent controls locally

Depends on P01. Canonical new semantic coverage: src/core/tests/test_form_review.py; HTTP: extend src/api/tests/test_form_staging_api.py. No test removals. Maximum additions: two test classes in the new core test module, six HTTP test methods in the existing form API class. Reuse public tiny synthetic fixtures, no data generation/private seed. Existing form, finance, grant, role and provenance suites are regression ownership. Run core focused suites, complete API unittest command requested by caller, relevant Ruff/mypy; no generated source targets. Scope is bounded; do not consume the optional heavy gate merely to replace targeted tests.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Document partial acceptance and prepare Review handoff

Depends on P02-T01. Update core/API component guides, reference index/log for durable decision routing, dated changes and pre-Review reconciliation. The automatic parent then owns the single independent Review, evidence commit and draft PR publication, not this implementation task's completion marker. Draft PR uses Refs for all three issues and reports Finance/Board blockers. No issue checkbox edits or merge.

## Dependencies

Existing schema/staging engineering is sufficient for working notes only. Human template/source/rule and Board decisions are hard blockers for the excluded approval-dependent behavior.

## Critique Disposition

Single critique executed, original verdict Revise (one High, two Medium). No second critique.

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 | Directly resolved | Review and diagnostics require already-clean evidence. No ensure_scanned, scanner or nested source save; pending/missing/infected evidence is denied with existing recovery error. Scan/quarantine is a separate operation. |
| PC-002 | Directly resolved | Acceptance preserves exact raw text; typed values require explicit correction. Six-type checks, finite numeric values, ISO calendar dates and strict type-aware enum/condition equality. required_when is OR: any true requires; if none true and any controlling value missing/invalid/stale, requirement is Unknown. Units/formula/eligibility verification is not evaluated. |
| PC-003 | Directly resolved | JSON single-Store/writer only; SQLite independent writers use existing rowversions. Document/test this distinction explicitly. |

## Follow-Up Items

* Finance/template owner: approve actual versioned template, source authority, eligibility/calculation rules, route and reviewer delegation before #96/#98 approved readiness.
* Finance/Board: supply and approve OD-12/15 envelope, liquidity/covenant/downside limits, scope and restart owners before #99 acceptance.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-27/finance-96-98-99-changes.md. Independent implementation complete and ready for the single Review. Core: 199 tests, 54 opt-in SQL Server skips. API: 1124 tests, 314 existing optional skips. Touched Python Ruff and targeted mypy pass. Missing authority remains held; whole-issue acceptance is not claimed.
