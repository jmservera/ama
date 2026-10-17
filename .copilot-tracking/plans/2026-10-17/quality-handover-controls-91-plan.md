---
title: Quality handover controls issue91 plan
description: Scoped implementation and acceptance evidence
ms.date: 2026-10-17
---

## Task Metadata

* Task ID: issue91
* Task slug: quality-handover-controls-91
* Planning status: Ready, one critique executed and both findings resolved
* Date: 2026-10-17
* Details: .copilot-tracking/details/2026-10-17/quality-handover-controls-91-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/quality-handover-controls-91-plan-critique.md

## Executive Summary

Preserve the existing stepwise quality workflow while closing demonstrated
current-actor, remediation and evidence-replacement gaps. Staff continue to
record supplier evidence; contractors gain no write or approval authority.
Same-measure replacement invalidates its former acceptance and handover, keeps
history and requires a new independent acceptance and resident handover.

### What You May Not Know

All 50 existing quality/procurement tests pass, but temporary JSON/SQLite probes
reproduced all three control gaps. PRD FR-017 is quality; current BRD FR-017 is
handoff information. No role fixture establishes professional competence.
No new risk policy, payment execution or human acceptance is being delivered.

## User Decisions and Requirements

* Execute Research, Plan/critique, Implement and independent Review in order.
* Enforce the three exact issue91 criteria, verify existing code, avoid unrelated features.
* Preserve resident, hazard, building, stock #84, finance #94 and provider #90 locks.
* Own quality.py and minimal dependent paths; avoid finance.py and parallel #95
  dataset/app.js/server.py/manifest writes wherever possible.
* Use worktree-local venv/pip, meaningful fail-before tests, configured checks,
  real isolated local SQL Server and actual browser for changed web behavior.
* Commit own files, normal push, PR to main with Refs #91; no merge or issue close.
* One independent Review; caller permits up to two concrete correction cycles
  with original verdict and closure evidence preserved.

## Goals

* Make current identity, remediation evidence and replacement dependency
  enforceable across API and stores without creating new approval authority.

## Scope and Non-Goals

In scope: quality.py, existing core/API tests, isolated ops.js UI copy/state,
component README contracts and existing programme journey synthesis/index/log.
Reuse existing registered actor, SQL decision scope, rowversion, safety/resident
and checked-document mechanisms. Avoid sqlstore.py/server.py if helpers suffice.
No dataset/manifest change, finance.py edit, risk scoring, new portal, paid AI,
Azure, private data, real orders or operational acceptance.

## Functional Requirements

* Every quality write resolves current registered staff; contractors stay denied.
* Acceptance excludes all retained submit/record/fix participants by name and
  populated email/code/OID, not merely the latest fixer.
* Remediation needs an explicit nonempty note retained on defect/history;
  acceptance from FIXED needs it too, including legacy records. Reinspection
  only operates on FIXED; all existing returned work needs independent checking.
* Same-measure replacement may supersede Accepted or Handed over evidence,
  never erase it. Former acceptance/handover become historical, not active.
  Superseded records cannot be accepted, handed over or used for active aftercare.
  Replacement retires EVERY prior active same-measure acceptance/handover,
  including multiple legacy HANDED records and older HANDED plus newer ACCEPTED.
* Bind consequential acceptance/handover to the existing resident revision,
  preserving safety/resident gates and independent finance state.
* Strict record index validation rejects negative/fractional/bool/out-of-range
  inputs instead of selecting another record.

## Non-Functional Requirements

* SQL actor checks run inside the existing writer transaction. Stale versions,
  case/audit failures and recovery-read failures leave no success audit or
  mutated cached acceptance; preserve prior legitimate audit.
* JSON caught failures restore preimage and own ledger tail, explicitly
  disclose durable uncertainty if recovery fails. No crash-atomicity claim.
* No global environment/resource changes. Disposable Docker ownership is exact,
  unique, loopback-only, ephemeral unlogged secret, cleaned after use.

## Acceptance Criteria

* A1: Contractor routes for all quality/finance writes deny; foreign case/order
  reads remain isolated. No quality action changes finance/grant/payment state.
* A2: Blank remediation and original/any-fixer or identity-alias acceptance deny;
  distinct current inspectors can independently reinspect evidenced remediation.
* A3: Replace accepted/handed-over evidence; former active handover disappears,
  history remains, siblings unaffected; new independent acceptance and fresh
  resident handover required. Stale SQL writer cannot restore the old decision.
* A4: Actual JSON, SQLite, HTTP, local SQL Server and browser evidence recorded
  with checks/skips and human/Azure limits explicitly separated.

## Sources

* .copilot-tracking/research/2026-10-17/quality-handover-controls-91-research.md:
  C1-C7 and fail-before transcript; Research executed, Planning Readiness Ready.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Lock regression ownership and fix quality controls

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add fail-before assertions and implement control changes

Context and completion details: P01-T01 in the phase-details artifact.

<!-- rpi:phase id=P02 -->
### [x] P02: Wire dependent UI and contracts

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Clarify invalidation/remediation and document exact boundary

Depends on P01. No shared #95 feature files unless unavoidable and declared.

<!-- rpi:phase id=P03 -->
### [x] P03: Execute acceptance evidence and reconcile delivery

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run targeted regressions, quality tools, SQL parity and browser

Depends on P01/P02; record actual counts and all skipped/unperformed checks.

## Test Ownership and Validation Lock

Canonical: existing test_quality_procurement.py for quality core and SQL
regressions; existing test_role_matrix.py for authenticated HTTP. Extend
existing test_mssqlstore.py replay by inheritance, without editing or aliases.
Browser: existing src/api/checks/browser_check.py harness, or a session-local
Playwright script against the real app if the existing harness is too broad.
No generated tests, no deleted tests. Maximum additions: 18 core test methods,
4 HTTP methods, one bounded browser scenario; SQL aliases replay, not copies.
Existing tests using empty remediation are updated to meaningful fictional
evidence, not removed. Semantic criteria tests plus stale/rollback regressions.
Run quality/procurement, resident/signoff/stock, finance and API role/workflow
tests, configured Ruff/format/mypy; expand only on shared regression evidence.

### Exact Regression Matrix

All `test_quality_*` methods below belong to existing
src/core/tests/test_quality_procurement.py. Shared `Flows` executes JSON/SQLite;
SQL-only methods belong to `SqlFlows`. Existing MssqlProcurement inherits
SqlFlows, so replay once, no duplicate aliases.

| Canonical planned method | Assertions / criterion | Backend |
| --- | --- | --- |
| test_quality_current_actor_all_writes | Forged, revoked, unknown and contractor actor deny all seven actions; A1 | JSON/SQLite/MSSQL |
| test_quality_identity_history | Name/email/code/OID aliases and first fixer across repeated cycles deny; legacy participant lookup; A2 | JSON/SQLite/MSSQL |
| test_quality_remediation_and_reinspection | Blank fix, legacy FIXED without evidence, pass/fail outside FIXED deny; evidenced independent reinspection succeeds; A2 | JSON/SQLite/MSSQL |
| test_quality_indices | Negative/fractional/bool/out-of-range indices deny with no mutation/audit | JSON/SQLite/MSSQL |
| test_quality_replacement_dependencies | Accepted/HANDED replacement, multiple legacy HANDED and mixed legacy state retire all, original history/aftercare and sibling/finance/grants preserved, fresh acceptance/handover, reopen; A3 | JSON/SQLite/MSSQL |
| test_quality_resident_and_safety | Missing/stale bindings, withdrawal and hazard gates unchanged; A1/A3 | JSON/SQLite/MSSQL |
| test_quality_json_failures | Save/audit/pre-save caught failures restore state/ledger; repeated save failure explicitly uncertain | JSON |
| test_quality_sql_actor_and_stale | Writer-time actor revocation and stale replacement refuse, winning state/audit survive reopen | SQLite/MSSQL |
| test_quality_sql_failures | Pre-save/case-write/actual INSERT audit failure; early/persistent recovery SELECT failure, original error, clean cache/tail, legitimate pending prefix survives | SQLite/MSSQL |
| test_quality_http_controls (role matrix) | Real sessions: contractor/foreign read isolation, forged body authority ignored, remediation denial and fresh acceptance | HTTP SQLite |
| test_quality_http_replacement (role matrix) | Existing route retires former handover, stale binding refuses, finance/grants unchanged | HTTP SQLite |
| bounded session-local browser journey | Return, empty remediation error, fix, independent reinspection, handover, replacement, visible historical state/new acceptance | Actual app/Chromium |

Selected execution: `test_quality_procurement` plus `test_role_matrix`;
actual local SQL selector `test_mssqlstore.MssqlProcurement` with ZF_TEST_MSSQL=1.
Existing provider tests in that inherited class run once alongside the quality
regressions, preserving #90. SQL container/database explicitly disposable.

## Dependencies

* #89 hierarchy only, no declared dependency. #90 already merged at b5d4c840.
* SQL Server Docker available (29.9.0); actual database run still required.
* Browser/runtime available through installed project dev dependency; actual
  executable availability must be checked during implementation.

## Critique Disposition

Execution Complete, original verdict Revise, retained unchanged in critique.
No second critique.

| Finding | Owner / disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Planning parent / resolved directly | All-prior-active same-measure legacy retirement specified in Functional Requirements, P01 details and replacement matrix |
| PC-002 | Planning parent / resolved directly | Exact Regression Matrix locks method assertions, backend and inherited MSSQL owner; prefix/recovery fault obligations explicit |

## Follow-Up Items

* Actual competent human quality acceptance and Azure SQL acceptance remain
  external validation; fixtures and local SQL cannot satisfy those gates.
* Existing quality/work-order form names/autocomplete, draft-navigation warning
  and other untouched web-guideline gaps remain outside the exact control fix;
  no complete accessibility acceptance is inferred.

## Handoff

Implementation creates .copilot-tracking/changes/2026-10-17/quality-handover-controls-91-changes.md.
P01-P03 complete; the one independent Review executed Complete / Not accepted.
P04 is the caller-authorized implementation continuation. Its closure evidence
does not overwrite that original verdict or constitute a repeated Review.

## Authorized Correction ONE

The one independent Review is Complete, original outcome Not accepted.
User explicitly pre-authorized fixing concrete findings up to two cycles;
no repeated critique/Review. RV-001/RV-002 are implementation corrections,
not scope/authority decisions. Original phase execution markers remain historical.

<!-- rpi:phase id=P04 -->
### [x] P04: Correct independently reproduced legacy and committed-outcome defects

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Resolve RV-001/RV-002 with fail-before and current evidence

Add canonical `Flows.test_quality_legacy_repeated_recorders` and
`SqlFlows.test_quality_sql_postcommit_refresh`, inherited once by
MssqlProcurement, plus `QualityMatrix.test_quality_http_committed_outcome`.
All fit existing test caps. Resolve every known historical FIXED recorder,
retain unknown denial and earlier-recorder alias exclusion. Distinguish
confirmed committed snapshots from pre-commit rollback before shared decision
scope recovery; never replay committed prefix. Minimal server.py handler may
surface explicit committed/reload HTTP 503 without touching grants/finance
dispatch. This shared #95 overlap is declared and sequenced after the core
outcome exception contract. No SQL helper/finance.py/dataset/manifest change.
Completion requires both fail-before probes, latest actual SQL replay,
HTTP/browser checks and configured gates, with original Review preserved.
Completed: canonical probes reproduced both defects before the fixes; final
361-test selection (312 pass, 49 existing skips), 101 additional overlapping
focused checks, actual SQL Server 38 pass and actual Chromium committed-error/
reload plus full replacement journey passed. Configured gates passed.
No repeated critique/Review or independent regrade is claimed.

## Coordinator-authorized latest-main integration

After P04 publication, coordinator authorized own-topic rebase onto freshly
fetched main 2b24456863c0a8f39d47a73e22daeff3875cc825 (merged #95/PR386
and PR385). Four documentation-only conflicts retain full upstream prefix,
routes and #95/#91 sections. Whole production/test patch byte parity proven;
no new feature/correction phase, grant/finance fix or Review repetition.
Fresh combined candidate c0f67838383007c3f4a95ba0aa957378e2db0ba5:
206 local tests, 205 pass/one opt-in browser skip; 83 actual local MSSQL pass,
zero skip; configured gates and preservation checks pass. Changes record holds
exact bases/heads/digest/selectors and lease publication boundary.

Later coordinator integration onto merged #85/PR388 main
1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c preserves both hazard post-COMMIT
marker/validation and quality committed-outcome handling. Only log conflicted,
both histories retained. Two tightly coupled test-only adjustments after initial
whole patch parity: identify registered fictional Sam in hazard race's copied
Submitted record so independent Pam reaches the real hazard-at-commit gate;
assert next healthy quality save preserves exact audit/state. No production
change or unknown-identity weakening. Tested candidate
48b90f42fe8170f3f17956e3a194a0c93b33eee2: 243 local run/241 pass/two existing
skips; actual MSSQL 99 run/98 pass/one JSON-only skip. Original adverse Reviews
remain; final-head source fingerprints and full receipts in changes record.
