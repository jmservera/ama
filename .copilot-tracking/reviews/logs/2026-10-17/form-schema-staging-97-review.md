---
title: Issue 97 RPI review
description: One post-implementation assessment of the bounded form collection slice
ms.date: 2026-10-17
---

## Scope and Evidence

* Task ID: 97; slug: form-schema-staging-97.
* Review date: 2026-10-17.
* Review scope: full P01-P03 implementation plan, bounded unapproved registry and candidate collection; full #97/PRD acceptance assessed separately.
* Plan: .copilot-tracking/plans/2026-10-17/form-schema-staging-97-plan.md.
* Details: .copilot-tracking/details/2026-10-17/form-schema-staging-97-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-17/form-schema-staging-97-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-17/form-schema-staging-97-changes.md.
* Research: .copilot-tracking/research/2026-10-17/form-schema-staging-97-research.md.
* Runtime boundary: new core forms module, existing store/projection/SQL hooks, server routes, two new external test files, existing role inventory, component docs and additive index/log updates. No infrastructure, credential, sensor or web asset changes.

## Opening Review State

Goal: compare the final implementation against exact #97 / FR-038/039, reconciled P01-P03 scope, PC-001 through PC-005 dispositions and observed validation, while preserving the distinction between unapproved collection mechanics and approved-form acceptance.

All canonical artifacts exist. All plan tasks are checked with matching changes evidence. The final source passed focused tests, both component suites and existing lint/format/type checks. The first comparison is schema authority and raw candidate/source disclosure, followed by version/provenance/transaction integrity and claim boundaries. Review is read-only except this one record. Initial implementation blockers: none; actual form approval remains unavailable.

## Execution Status

Execution status: Complete. Exactly one Review invocation, performed directly over the complete bounded change and artifact set. No source corrections, nested delivery agents, closure verification or second Review were run.

## Plan-to-Change Reconciliation

| Plan scope | Observed implementation and evidence | Assessment |
| --- | --- | --- |
| P01 / P01-T01 | Original core lacks forms contract; original `abaca788` server returns 404 for a valid schema. Two new external tests subsequently exercise real behavior | Reconciled; fail-before is observed, not asserted retrospectively |
| P02 / P02-T01 | forms.py retains immutable definitions, supplied policy references, source hashes/versions/locators and supplied processing assertions; existing checked shared docs and row-versioned case bodies used | Reconciled for unapproved collection; no template authority fabricated |
| P02 / P02-T02 | Existing server/auth/projection paths expose four bounded operations. Generic detail strips staging; current registered rights are checked on dedicated reads/writes | Reconciled; no UI or new service |
| P03 / P03-T01 | Final focused tests, complete suites and static checks pass, with actual skips separated. Existing role inventory was extended after its observed failure | Reconciled; no removed/weakened tests |
| Follow-Up Items | Actual form authority/binding, #98 and any future registered selector are still outside active task markers | Remain residual work, not completed approvals or newly activated tasks |

## Completed Work Assessment

Schema input has strict keys and bounded lists, positive sequential versions, explicit units/options/required/conditions, stable field/section IDs, funding association, source precedence/evidence policy, calculation/rule references and existing reviewer identity. Versions are defensive copies and immutable through the API. Server generates digest/actor/time and always assigns Unapproved/null approval evidence; requests cannot set approval or actor. This meets the declared engineering foundation, not the approved-template positive path.

Candidate requests have strict keys. Source document membership is checked within the case; original bytes are scanned and compared with existing content_sha256/version. Exact UTF-8 text spans and strict CSV cells are independently checked. Candidate IDs are server-generated; all alternatives remain in order, all stay Not reviewed, and source authority stays Not established. OCR imports retain supplied parser/model/route/error metadata separately from server verification; they do not attest pixel content, route approval or model execution.

Arbitrary raw source content is protected by the conservative existing reason/resident/Finance rights intersection. Current SQL staff registration is queried through the existing assistant connection, not a process cache. Retained reads recheck current rights and document presence/clean scan; generic case detail and audits exclude raw batches/values. Unauthorized/foreign inputs fail without reflected source content. Safe errors distinguish malformed input, permission, missing source, conflict, source-storage outage and unexpected storage failure.

Controlled state snapshots in core/HTTP tests are unchanged apart from append-only staging; no candidate acceptance, source update, consent, funding state change or submission exists. Unsupported source decoding/type/CSV structure records manual recovery and zero candidates; infrastructure failure is not converted into successful recovery.

SQL registry/body/audit use the existing transaction path, shared-document optimistic check and case row versions. Failed first shared-document writes no longer leave ghost process state after sync. Fault/reopen/race tests support this. MssqlStore shares these hooks, but no SQL Server/Azure execution is claimed. Existing JSON snapshot and ledger files remain separate; failure restoration is tested, cross-file crash atomicity is explicitly not claimed.

## Implementation-Time Plan and Detail Update Assessment

| Update | Trigger and reconciliation | Assessment |
| --- | --- | --- |
| Actual digest helper | `ai_registry.digest` exists; ledger canonical/hash API does not. Plan/research/changes corrected | Ordinary local correction; no duplicate helper or new dependency |
| Generic-detail exclusion | Focused test caught actual raw staging leak from Store.detail copy; fixed before Review and evidenced in changes | Directly required permission correction, not scope expansion |
| Current SQL identity and shared-doc rollback | Existing cache/rollback boundaries inspected; fault/revocation tests added to owned file | Matches PC-001/004 and accepted least-privilege intent |
| Existing route inventory | Full API run failed exactly missing new route registration; existing GET/POST and dynamic-action inventory extended | Necessary integration amendment; no test removal, new module or second critique |

## Critique and Material Revision Assessment

All five PC findings have explicit planner dispositions. PC-001 is implemented with conservative rights and retained-read checks; PC-002 exact schema/funding/human-only metadata is present; PC-003 supplied versus observed lineage and reproducible locators are separate; PC-004 non-conflict registry/body/audit failures are tested for restoration/no replay; PC-005 preserves dated PRD v0.12.0 planning acceptance separately from exact template approval.

No significant/divergent implementation decision required a new user choice, broadened scope or resumed a paused dependency. No critique was repeated. The bounded unapproved-only direction was explicit before implementation and all completion claims retain that boundary.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Actual approved-template acceptance remains unavailable

* Related scope: #97 title, FR-038 and AC-046; explicit plan acceptance limit.
* Evidence: forms.py always emits Unapproved with null approval_evidence. Research found no actual approved schema/template version or recorded form delegation. The dated PRD planning baseline and synthetic source policies are not that evidence.
* Impact: The delivered foundation cannot be called approved form preparation or close full #97/parent acceptance. Full AC-046 is unmet; full AC-047/053 also include extraction/selection/review scenarios beyond the exercised collection slice.
* Destination: later `rpi-research` for actual form/version-specific authority evidence, then separately planned binding work if supplied. This is an existing material acceptance gap, not a newly invented approval prerequisite for safe collection.
* Smallest useful next action: owner supplies the exact authoritative template/schema/rule versions, named delegation and recorded approval evidence; preserve Unknown/Unapproved until then. Do not synthesize approval or rerun this Review to manufacture closure.

## Defects

No additional high-confidence implementation defect found within the explicit unapproved-collection plan boundary. This is not a security certification, general accessibility review or claim of full issue acceptance.

## Plan Follow-Up Assessment and Routed Work

| Rank | Work | Destination / owner | Why separate |
| --- | --- | --- | --- |
| 1 | Actual approved schema authority and exact-version binding | Form/control owner supplies evidence; later rpi-research and separate plan | Highest direct acceptance impact; evidence gap prevents honest issue closure |
| 2 | Field review, deterministic validation, pack and exact stale propagation | Existing #98 | Named downstream dependency; consumes immutable schema/candidate evidence, not implemented here |
| 3 | Optional semantic selector task registration/release | Existing AI workstream if selection is adopted | Registry exists (#105), but no form-specific selector is registered; no model/task activated in this slice |

JSON cross-file crash atomicity remains an explicitly documented inherited boundary. Use the existing SQL path where transactional durability is required; no new service or immediate unrelated reliability work is prescribed.

## Blockers and Remaining Work

* Remaining active P01-P03 work: none.
* Full issue acceptance blocker: actual approved template/schema authority unavailable (RV-001).
* Human/legal/operational review checkboxes remain uncompleted; no real approval claimed.
* Delivery handoff still requires committing/pushing this final record with the source/artifacts and opening a main-target Refs #97 PR. No merge, rebase, force-push, issue closing keyword or child delivery loop.

## Validation Evidence

| Validation | Result | Boundary |
| --- | --- | --- |
| Original missing-contract/valid HTTP fail-before | Expected failure observed | Original server returned 404, installed src distributions present |
| Focused core | 15 passed, zero skips | JSON/SQLite, exact source/lineage, conflicts, role revocation, failed save/audit and manual recovery |
| Real HTTP fixture | 2 passed, zero skips | Ephemeral loopback health/auth/register/stage/read/denial over temporary synthetic SQLite; inference forbidden |
| Core full | 551 run: 550 passed, 1 skipped; 257.634s | Existing opt-in isolated Azure SQL test not run |
| API full | 565 run: 455 passed, 110 skipped; 239.150s | Existing SQL Server/browser gates not run; role inventory passes |
| Core Ruff/format/mypy | Passed; 49 format / 102 mypy targets | Existing component config, strict new module and harness with narrow untyped-boundary exceptions |
| API Ruff/format/mypy | Passed; 18 format / 48 mypy targets | Existing component config; no web source changes |
| Diff/Markdown/link review | Passed for changed links and additive docs; git diff --check passed | No repository-wide documentation build exists |
| Live paid AI/OCR/Azure/SQL Server/Docker, remote checks, human approval | Not run / unavailable | Explicit offline scope; known Docker denial not escalated |

## Outcome

* Outcome: Residual work.
* Rationale: The declared P01-P03 engineering slice is complete and supported by passing tests/checks; full approved-form/PRD acceptance remains unmet. A broad Conformant or issue-complete result would be inaccurate while RV-001 is open.
* Severity summary: one Medium acceptance-evidence gap; no additional implementation defect recorded.
* Closeout route: return this single record to the parent for authorized commit/push/Refs-only PR delivery, then stop per caller. No repeat Review or child task.

## Integration evidence addendum 2026-10-17

This is an evidence addendum to the existing Review, not another RPI Review or
an independent-review result. Caller authorized rebasing the run-owned topic
from `c021a3f` onto `origin/main` `0bdcb2f0` (#374 credentials, #376 queue;
also includes #373 sensor faults). Rebase completed as `1e59021` / `81c9922`.
Only additive KB index/log conflicts required resolution. All upstream log
bytes and index rows were verified retained, with the #97 additions preserved.
Topic runtime, staging tests and permission inventory remain identical to
`c021a3f`; upstream credential/sensor/web behavior was not rewritten.

Fresh integration evidence: core staging/document/store/SQL/queue selection
**84 passed, zero skips (106.460s)**; API staging/role-inventory/role-matrix/auth/
document-controls/task-queue selection **80 passed, zero skips (32.391s)**.
These include all 17 focused form tests. Core Ruff/format/mypy passed
(51 format targets / 104 mypy files); API equivalents passed (18 / 48);
unchanged upstream app.js parsed successfully; whitespace and KB preservation
checks passed. Exact commands and scope limits are in the existing changes
record. Prior full-suite results are historical, not rerun claims.

Independent reviewer `97fdbce9` was assigned the earlier `c021a3f` head; its
result and final exact-head delta follow-up are not asserted here. That
follow-up remains outstanding after the authorized force-with-lease push.
RV-001 remains open: no actual approved template authority or version binding,
no invented approval, no issue closure. Outcome remains **Residual work**.

Direct delivery to reviewer ID `97fdbce9` after push returned `No agent found`
in this session. Final exact-head follow-up is therefore pending coordinator/
PR routing; no independent approval or follow-up completion is claimed.

## Independent REVISE and correction cycle ONE, 2026-10-17

Caller subsequently relayed reviewer `97fdbce9` **REVISE** on `c021a3f`.
The independent finding invalidates the earlier durable-lineage assessment
for pending/unscanned sources: scan saves clear SQL touched-case tracking,
allowing success audit without a persisted candidate batch. Integration did
not alter the defective source.

Implemented the requested bounded correction: reacquire/touch the current
case after scanning finishes and before append, using the existing `_case`
contract. New real SQLite and authenticated HTTP tests failed before this
change for both pending and absent scan metadata. Whole-batch equality now
holds through repeated candidate/detail reads and SQL reopen. Final-save
failure and actual cross-process row-version conflict tests also verify
rollback/no durable success audit. Exact commands and fail-before output
summary are recorded in the existing changes artifact.

Fresh correction gates: **85 core / 81 API passed, zero skips**, including
17 core form tests and 3 real HTTP form methods; both component
Ruff/format/mypy checks passed (core 51/104 targets, API 18/48).
No new full RPI Review was invoked. This author evidence does **not** overturn
independent **REVISE** or establish closure: final exact-head independent
reverification is still required. RV-001 actual approved-template authority
remains unmet; #98 workflow was not delivered; no approval was fabricated.
