<!-- markdownlint-disable-file -->
# Review: Provider capacity and controlled orders

## Scope and Evidence

* Task ID: 90
* Review date: 2026-10-17
* Review scope: full task, P01/P02 implementation and P03 review-readiness; publication remains parent-owned.
* Assessed boundary: exact four #90 criteria, PRD FR-016/BRD RULE-007/008, current JSON/SQLite/local SQL Server/controller/screen controls, human/resident/safety preservation, critique dispositions and actual validation.
* Plan: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/provider-capacity-controls-90-changes.md
* Other evidence: .copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md; .copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md; executed local test/browser/quality logs summarized in changes.

## Opening Review State

* Interpreted goal: independently assess actual controls and evidence, not infer fulfillment from previous screens or fabricate operational authority.
* Scope: full accepted task; inspect current uncommitted source/tests/docs and canonical phase artifacts.
* Evidence readiness: research/manager instrument, plan/details, exactly one critique with PC-001..005 applied, changes and final execution evidence reconciled. P01/P02 checked; P03 publication intentionally pending.
* Acceptance basis: committed capacity never offered/unknown, every order change version/issuer, no system draft instruction, own-only read-only contractors; named current trusted delegation and preserved safety/resident controls.
* First comparison: end-to-end procurement lifecycle and alternate advance, including SQL commit dependencies/rollback; then source/authority and HTTP tests/UX disclosure.
* Active read-only boundaries: no source, tests, plan/details/changes or critique edits. Parent may update only this canonical Review record during Review; independent lens has no write authority.
* Initial blockers: none. Actual operational authority and hosted/human acceptance are explicitly outside local engineering acceptance.

## Execution Status

* Execution status: Complete
* Review execution evidence: one bounded independent rubber-duck comparison completed on 2026-10-17 after opening persistence. It inspected the actual lifecycle, alternate advance, current delegation/source validation, SQL commit/CAS/rollback, changed UI, test fixtures and canonical artifacts. No source edits or repeated Review.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Reconciliation | Rationale |
| --- | --- | --- | --- |
| P01-T01 | Baseline and failing-first reproduction | Reconciled | Original 21 passed; four root gaps produced eight failures across JSON/SQLite before implementation |
| P01-T02 | Domain controls and transaction progress | Reconciled | Structured current commitment, exact trusted delegation, all-change immutable snapshots and SQL dependencies implemented |
| P02-T01 | Existing API, screen and preservation | Reconciled | Existing routes/fields extended without permission grant/redesign; two contractor views remain read-only own |
| P02-T02 | Final Validation | Reconciled | Executed JSON/SQLite/actual local SQL Server, browser and configured quality gates; skips/exclusions/failures disclosed |
| P03-T01 | Review and publication | Reconciled | This one Review complete; evidence commit/push/PR are parent-owned next actions, not falsely completed |
| Follow-Up Items | Remaining Boundaries and Follow-Ups | Reconciled | Actual authority and hosted/human acceptance remain distinct human/deployment/UX work |

## Completed Work Assessment

| Marker | Files | What changed and why | Completion/validation evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01 | src/core/src/zava_forward/core/procurement.py; store.py; sqlstore.py | Prevent numeric-only capacity and alternate-advance bypass; version every order change; recheck dependencies at commit | Semantic lifecycle, quota/deficit/dates/source/delegation, failure and deterministic race tests | Complete within supported single-process JSON and transactional SQL boundaries |
| P02 | src/api/src/zava_forward/api/server.py; web/ops.js; web/app.js; core/ai_tasks.py | Wire source evidence and explicit non-instruction drafts; preserve provider isolation | Domain/HTTP/two-contractor browser journeys; source/profile/resident/safety regressions | Complete local engineering scope, no actual company permission implied |
| P02 | Component guides and existing KB synthesis/index/log | Explain source/unit/delegation semantics, replay and limits | Diff/link-target review and actual commands in changes | Claims scoped to executed evidence |

## Exact-Criterion Assessment

| Criterion | Independent comparison | Outcome |
| --- | --- | --- |
| Committed evidenced capacity only | _evidenced_capacity repeats source hash/version/review/interval/contract/scope/home checks; issue uses used < committed, existing allocation progression permits equality; deficit blocks. All consuming mutations and alternate advance checked | Conformant for local engineering contract |
| Every change version + issuer | _new_version records named issuer/email/time/delegation/capacity and immutable scope/state/appointments for every successful mutation, including withdrawal | Conformant |
| Draft never instruction | Template note and AI persisted/result/review/UI labels are explicit; no draft/review-to-order mutation path found | Conformant |
| Contractor own-only read-only orders | Current identity/supplier rechecked; own orders filtered; package reads denied by HTTP and domain; global POST gate and named-manager domain checks deny writes | Conformant |

The independent comparison also traced SQL validation inside the existing
writer transaction before writes, shared-document CAS, source rowversions
and fresh delegation checks. A suspected stale thread-local context on
failed advance was investigated and found safe: outer _SyncLock.__exit__
always invokes _finish, which clears procurement_validation, including on
exceptions. This is not a finding and requires no fix.

## Implementation-Time Plan and Detail Update Assessment

| Affected marker | Update/reason | Triggering evidence and decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| P01-T02 | JSON compensation also covers advance | Same save/audit failure boundary; existing user direction requires actual behavior, no new decision | Plan/details/changes explain single-process and separate-file limits | Compatible implementation detail |
| P02-T01 | Missing helper import corrected | HTTP/browser tests failed before correction | Final replay passes; chronology retained | No unresolved defect |
| P02-T02 | Coupled building API positive supplies booked order | Wider regression exposed reliance on removed advance bypass | Original assertions retained with fictional prerequisite, core/API building modules checked separately | Preserved safety/resident intent |
| P02-T02 | Canonical API cwd and configured exclusions | Existing harness imports and legacy format/type configuration | Correct cwd and --force-exclude replay recorded; no config changed to conceal failures | Honest executed evidence |

## Critique and Material Revision Assessment

* Exactly one final-candidate critique returned Revise.
* PC-001..005 were applied in source, not merely claimed: exact delegation predicate, original-source/acceptance binding, valid-at-quota advance and withdrawal semantics, deterministic races/rollback, reproducible test ownership.
* No material scope/architecture/human-authority divergence occurred. No additional decision or repeated critique was needed.
* Dependent work followed failing-first reproduction and critique disposition; no known early resumption gap.

## Plan Follow-Up Assessment

| Follow-up | Why outside scope | Owner/next action | Route |
| --- | --- | --- | --- |
| Actual contract commitments/delegations and operational approval | No live source or permission supplied; fictional fixtures cannot establish them | Named human contract authority owner validates/provisions real authority before live use | Distinct operational-readiness follow-up, not implementation blocker |
| Hosted AI/Azure and human/screen-reader/WCAG acceptance | No approved live platform/user exercise in this bounded task | Deployment/UX owners commission separately approved validation | Distinct hosted/human-acceptance follow-up |

## Findings

No substantive implementation defects, unaccepted decisions or missing
material evidence for the accepted local engineering boundary were found.
There are no RV-xxx entries to invent or route.

## Defects

None found. No source changes occurred during Review.

## Routed Findings

| Finding | Destination | Next action | Reason |
| --- | --- | --- | --- |
| None | None | Parent publication only | No actionable defect/decision/material evidence gap found |

## Residual Work

Only the two already-scoped human/deployment/UX follow-ups above. They do
not enter active P01/P02 acceptance or imply missing code should remain
unimplemented. JSON crash/cross-process guarantees are not claimed.

## Blockers and Remaining Work

* Blockers: none for local engineering completion/publication.
* Remaining active work: P03 parent evidence commit/push and main Refs #90 PR, without close/merge/rebase/force push.
* No actual provider instruction, award/payment, private dataset, cloud or paid AI was used.

## Validation Evidence

| Command/scope | Status | Summary |
| --- | --- | --- |
| API cwd unittest test_quality_procurement test_procurement_api test_role_matrix | Passed | 63 tests |
| API cwd combined exact/preservation command recorded in changes | Passed with existing skip | 278 run: 277 passed, one opt-in skip |
| Core cwd building/procurement/resident/hazard | Passed with existing skip | 114 run: 113 passed, one opt-in skip |
| Standard local SQL Server MssqlProcurement and MssqlProcurementApi | Passed | 29 actual SQL Server 2022 tests; new isolated task-owned loopback container only |
| Local procurement_browser_check.py | Passed | Source inputs, refusal/focus, keyboard, quota/version, both contractor screens; 320/390/1280/reduced motion; external requests blocked and zero page errors |
| Changed-path Ruff, configured format, component mypy | Passed | Existing exemptions unchanged; 110 core/52 API source files reported by configured type checks |
| Explicit-path format without force-exclude | Failed, explained | Bypassed pre-existing migration exclusions; configured --force-exclude replay passed four eligible core files; no mass reformat |
| Changed JS node --check; git diff --check | Passed | Both JS files and diff hygiene |
| Actual live authority, Azure, AI inference, human/screen-reader/full WCAG | Not run | Outside authorized local fictional engineering scope; not claimed |

## Changed Web Region Review

Fresh guideline source retrieved fully on 2026-10-17:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Existing Fluent/plain-language/native semantics take priority; no redesign.

### src/api/src/zava_forward/api/web/ops.js

Pass for changed region: label associations, native dates/numbers,
live error/focus, button busy state, semantic scrollable table and honest
draft/authority/evidence copy. No substantive changed-region finding.
Unchanged action-input/unsaved-navigation limitations are not whole-site
acceptance and were not expanded into this task.

### src/api/src/zava_forward/api/web/app.js

Pass for changed non-instruction note. No new interaction or accessibility
acceptance claim.

## Outcome

* Outcome: Conformant
* Rationale: all four exact controls are wired and exercised through the supplied local domain/controller/store/screen boundary; independent comparison found no material defects. Full PRD, actual company authority and hosted/human acceptance are explicitly not inferred.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | None | None found |
| Decision gap/invalid assumption | None | None found |
| Material evidence gap | None within accepted local scope | No invented live approval |
| Non-blocking residual work | Distinct operational and hosted/human acceptance work | Contract authority owner; deployment/UX owners |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: exact semantics, preserved controls, JSON/SQLite, actual local SQL Server, focused browser and configured quality gates.
* Blockers: none for parent publication; no repeated Review required.
