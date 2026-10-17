<!-- markdownlint-disable-file -->
# RPI Plan: Controlled bulk preview

## Task Metadata

* Task ID: 78; slug: controlled-bulk-preview-78; date: 2026-10-17
* Status: Correction TWO implemented; publication and coordinator final-head independent reassessment pending
* Details: .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/controlled-bulk-preview-78-plan-critique.md

## Executive Summary

Add a small core module and two authenticated API endpoints for explicit,
server-owned bulk preview and all-or-nothing apply. Allow only administrative
case reason and existing handoff due/next-action fields, never approvals,
ownership transfer, resident commitments or safety clocks. Preview preserves
exact source/version/reason and each target's change/failure/outcome. Application
rechecks identity, permissions and exact snapshots within the existing SQL
transaction, with immutable per-case and batch audit.

### What You May Not Know

Existing handoff acceptance is the only ownership-transfer path; bulk reassignment
would bypass that control. SQL staff is currently cached and must be read fresh
under the transaction. The same-number BRD FRs differ from the PRD's numbering.
JSON retains its existing single-process/multi-file limitation. The original
additive bulk API needed no UI; authorized P04 now updates the directly affected
existing upload/handoff forms. No unmerged implementation dependency. Independent
final-head review remains required for acceptance.

## User Decisions and Requirements

* Complete ordered Research -> Plan -> Implement -> Review and push a main PR.
* Preserve exact three issue criteria and PRD FR-005/006/007; all listed
  controlled decisions, contractor instructions and complaint closure off limits.
* Prefer existing permissions, source/version/actor/time/reason audit and SQL
  transactions, local synthetic data and existing tools; no cloud or Docker.
* Coordinate #377 overlap in store shared documents, server and route inventory
  surgically, without depending on its unmerged forms module.
* Commit dated phase evidence/log, privacy-safe identity and Conventional Commits.

## Goals

* Make permitted case/task edits inspectable before mutation and independently
  reject forged, stale, unauthorized or approval-shaped requests.
* Preserve old/new provenance in case history and immutable hash-chain audit.

## Scope and Non-Goals

Core/API plus focused tests and component/KB documentation. No UI or framework,
new service, cloud execution, owner reassignment, evidence approval, workflow
transition or edits to forms work. Never change memory or original case study.

## Functional Requirements

* `POST /api/bulk-edits/preview`: exact keys `case_ids`, `changes`, `source`,
  `source_version`, `reason`; 1-100 unique IDs, explicit nonempty allowlisted
  fields `case_reason`, `handoff_due_at`, `handoff_next_action`. Strict types,
  length/date validation; no silent truncation. Unknown keys/fields rejected.
* Reuse named registered staff, owner/manager rights and guard-case event.
  Free-text changes require existing reason visibility; unsupported target
  records disclose no content. Handoff changes require an active handoff.
* Response: preview ID, actor, source/version/reason, status and exact ordered
  per-case records with ID, field old/new, failures and `would_apply` or `blocked`.
  Any failure makes all otherwise-valid outcomes `batch_blocked`.
* `POST /api/bulk-edits/apply`: only `preview_id`. No new targets, changes,
  roles or actor accepted. Bind creator identity; recheck current identity and
  request, case digests, staff and preview status inside the writer transaction.
  Any mismatch rejects entire batch with fresh-preview instruction.
* Retain server preview and terminal result durably in checked meta document.
  Duplicate application refuses; rejected attempts receive metadata-only
  hash-chain audit. Audit successful field changes with complete old/new
  provenance, timestamp, actor/role, per-case version and batch ID.

## Non-Functional Requirements

* SQL writes/audit/result atomic, including reopen, rollback and two-store
  concurrency; inherited MssqlStore commit hook uses portable SELECTs.
* Existing role projections cannot leak newly retained free text in history.
* No paid/service/data access. Existing focused unit/lint/format/type checks.

## Acceptance Criteria

* Criterion 1: event/history/audit assertions for exact old/new values,
  source/version, actor, UTC timestamp, reason and monotonic edit version.
* Criterion 2: actual HTTP preview shape including valid, invalid, inaccessible,
  no-op and mixed targets; no case mutation before apply; durable result.
* Criterion 3: table-driven every controlled category/unknown field rejection,
  mixed allowed+forbidden no mutation, foreign actor/revoked role/owner denial.
* Stale changed-away-and-back SQL rowversion rejection, changed target,
  concurrent authority change, rollback/reopen and replay refusal.

## Sources

Research C1-C9/W1-W2:
.copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core preview and atomic application

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing-first synthetic contracts and core implementation

New tests own preview semantics and transaction failure injection. New module
owns normalized request, closed fields, durable snapshots and auditable outcomes.
Store uses mixin; SQL adds checked document and final commit validator.

<!-- rpi:phase id=P02 -->
### [x] P02: API integration and delivery

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add routes, HTTP/role checks and documentation

Authenticated existing POST boundary, contractor/unknown denial audit, same
error statuses; no UI changes. Add only two route inventory entries.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence and prepare one Review

Run targeted regressions and affected lint/type checks, record results,
update component docs/existing synthesis/index/append-only KB log and changes.

## Dependencies

P02 depends on P01. Explicit issue dependencies none; #73 hierarchy only.
#377 shared integration surfaces are additive, not a dependency.

## Locked Test and File Ownership

Removals: none. Maximum additions: one core module, one core test module and
one API test module plus mandatory RPI artifacts. Existing targets: store.py,
sqlstore.py, projection.py if required for history redaction, server.py,
test_role_endpoint_inventory.py, component README/pyproject only if justified
typed legacy calls, existing UX synthesis, index and log. No generated assets.
Semantic tests own exact preview/history/authority/atomicity; regression tests
own existing handoffs, controlled decisions, store, SQL dialect and role matrix.
No broad/full suite repetition unless changes justify it.

## Critique Disposition

Execution complete, verdict Revise; all six findings directly incorporated.
No user decision needed and no second critique.

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 | Applied | Category matrix below; no full FR-005/008 acceptance claim |
| PC-002 | Applied | Bulk-scoped full restoration on all precommit exceptions; fault injection below |
| PC-003 | Applied | Fresh SQL staff before preview disclosure and inside commit, including OID/provider binding |
| PC-004 | Applied | Canonical immutable issued content SHA-256 anchored in append-only audit; response copies |
| PC-005 | Applied | Explicit outcomes/state table below |
| PC-006 | Applied | One Review, reconciled state, privacy-safe commit, push, main PR and requested stop |

## Refined Contract and Coverage Matrix

| FR-005 category | Existing operation / evidence | This delivery / limitation |
| --- | --- | --- |
| Case fields | return/reopen disposition source/version/actor/time/reason | New case_reason -> case.reason, owner/manager, open/unpaused case, existing reason visibility |
| Evidence references | add_document retains uploader/time/document ID; stock comparison retains source assertions | New edit source/source_version preserved; no bulk evidence replacement or approval. Existing evidence-upload reason/version contract not established as full FR-005 acceptance |
| Task owners | offer/accept handoff, immutable handoff_history and named receiver | Existing transfer retained, not widened; old accept path lacks complete source/version/reason contract, so full FR-005 remains partial |
| Due dates | offer_handoff due_at and versioned handoff_history | New handoff_due_at -> handoff.due_at, active handoff only; never hazard/resident deadlines |
| Workflow details | domain-specific actions with independent gates | New handoff_next_action -> handoff.next_action; no state/approval mutation |

All allowlisted edits require fresh registered named staff, owner/manager authority,
existing reason visibility (including source/reason/history), and open/unpaused
case. Existing domain-specific edits outside the new path are regression scope,
not retroactively certified. Issue criterion 1 is evidenced for delivered edits;
broader FR-005 acceptance remains explicitly partial, so PR uses Refs #78 only.

| Request / state | Response / result |
| --- | --- |
| Malformed/unknown keys, bad values/ID types | 400, metadata-only refusal audit, no preview |
| Actor forbidden/revoked/rebound | 403, no target content, refusal audit |
| Well-formed per-target failure/missing/not-owned/closed | 200 blocked preview with every submitted ID, safe failures, no inaccessible values; valid peers batch_blocked |
| Unchanged target | no_change; no field/history/version write, including mixed valid batch |
| All valid or no-op | pending preview, would_apply/no_change; no case write until apply |
| Apply blocked/consumed/stale | 409, no case changes, rejection audit; fresh preview required |
| Apply pending unchanged | atomic applied result, applied/no_change per target and batch audit |

Issued canonical content includes ordered request/targets/outcomes, creator
identity/provider/OID, source/version/reason and case digest/SQL rowversions.
Its SHA-256 is anchored in the existing immutable issuance audit, independently
of mutable preview document. Deep-copy responses. Recheck schema/hash/creator
and exact staff/case snapshots under commit lock; checked-document comparison
prevents concurrent consumption. Not protection against rewriting both trusted
database and ledger.

Bulk failure recovery restores every staged case/history, pending success audit,
touched/validation state and the shared preview document, including prior
absence. Persist only metadata refusal after restoration. Faults after first
case write, document write, audit append and before commit must retain reopened
original state; a later unrelated save cannot publish ghost success. If commit
acknowledgement is uncertain, return explicit failure/unknown, reload durable
preview state before retry, never infer success or safely repeat.

Fresh SQL staff reads do not rely on cached store.staff or case sequence. Compare
email/code/name/role/OID binding and trusted-provider role, never grant a database
role in place of authenticated claim. Tests prime cache, delete/revoke/rebind,
interleave revocation before transactional validation, mutate returned/cached/
stored previews and concurrently apply from two stores. No-op records still
participate in freshness checks, not fictitious edit events.

Delivery gate after P02: activate rpi-review once; persist execution/outcome and
route later findings without a second implementation/review loop. Resolve GitHub
account, configure local noreply author/committer, commit all phase artifacts and
code, push branch, create main PR with exact evidence and Refs #78, verify remote
head/PR, then stop as explicitly requested. No merge/rebase/force-push.

## Follow-Up Items

* Live Azure SQL, UI adoption and human operational/accessibility acceptance are
  outside this offline backend slice, not implied by local results.

## Handoff

Implementation changes path:
.copilot-tracking/changes/2026-10-17/controlled-bulk-preview-78-changes.md.
P01-T01/P02-T01/P02-T02 complete, with changes-record evidence. Next: one
post-implementation Review, then normal privacy-safe commit/push/main PR.
Original one-Review outcome remains historical Not accepted. The owner's
2026-10-17 continuation explicitly authorizes correction cycle ONE on the same
branch/PR; the previous publication stop is superseded for this invocation.

## Correction Cycle ONE

No Research/Plan/critique/full RPI repeat. Original Review is immutable evidence,
not permission to leave an actionable source defect unfixed. Current base remains
e065ecd; do not merge/rebase/force-push or integrate #377 yet.

<!-- rpi:phase id=P03 -->
### [x] P03: Correct RV-001 and disposition RV-002

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Immutable eligibility and complete transactional target coverage

Add fail-before cached/persisted status-only corruption tests, including no
case/history/success-audit mutation. Derive eligibility from anchored issued
outcomes, exact ordered IDs/records and complete snapshots. Reject every failure,
blocked/batch_blocked record irrespective of mutable status. Revalidate each
issued target after BEGIN IMMEDIATE; preserve no-op and permitted states/fields.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Investigate older provenance and validate correction

Trace exact existing add_document and offer/accept_handoff plus API inputs.
Fix only a small tightly coupled data-retention gap without fabricating source
or reason. If genuine caller input/approval or behavior choice is required,
retain criterion partial and state exact outstanding scope for coordinator.
Run focused new/bulk/SQL tests and existing component tooling; update current
plan/details/changes and KB. Preserve original Review verdict.

<!-- rpi:task id=P03-T03 -->
#### [x] P03-T03: Independent correction review and final push

Obtain one independent bounded correction assessment, separate from the
historical RPI Review. Record finding disposition and its actual verdict,
commit with verified noreply identity/trailer, update PR #378, push and stop.
Do not label original Review Pass or close #78 while criterion remains partial.

Independent correction assessment completed: accepted for the bounded fix,
no substantive findings; RV-002 remains partial. Source commit dd52ae3 was
pushed and read back as draft/open PR #378 head on main. Separate
[correction review](../../reviews/logs/2026-10-17/controlled-bulk-preview-78-correction-one-review.md)
preserves original Not accepted verdict and exact finding disposition.
Final artifact-only receipt records publication and the stop boundary; no
merge, rebase or force-push. Full issue acceptance is not claimed.

## Authorized Same-PR Main Integration

The subsequent owner instruction authorizes rebase onto main92d4f89 (merged
#377) and topic-only force-with-lease against published97cdc2a, superseding
the prior no-rebase stop for this bounded integration only. No new RPI or
correction cycle. Tested source8602473 retains both features and all KB
histories; 110 focused tests and existing core/API tooling pass. Current
changes/details and the correction review's separate integration delta record
exact SHAs and finding disposition. RV-002 remains unfulfilled/blocking full
acceptance; actual form authority is unrelated human-blocked. Active external
review512a59c4 must assess final exact head; no Pass inferred. Final evidence
commit/publication then stop, no merge.

## Correction TWO: Required Existing Caller Provenance

Explicit owner direction after reviewer512a59c4 Revise97cdc2a supersedes the
earlier residual-only RV-002 disposition. This is the final allowed same-issue
correction, not a full RPI repeat or permission to omit implementation.

<!-- rpi:phase id=P04 -->
### [ ] P04: Implement RV-002 existing upload and handoff contracts

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Fail-before, required metadata and immutable change events

Required explicit source/source-version/reason for upload and offer/accept;
server actor/time/version and exact old/new document refs/ownership; mandatory
handoff history version and stale refusal. Missing legacy request inputs refuse;
no invented defaults or backfill. Shared single-record commit/recovery with
fresh SQL actor check, existing rowversions, no ghost history/success audit.
Recipient-only acceptance and separate forms/bulk modules remain intact.

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Direct callers, native accessible UI and validation

API forwards supplied inputs; existing upload/offer/accept forms collect them,
retain error values, label controls, support Enter and focus/live status.
Direct synthetic fixtures explicitly supply metadata; no production defaults.
Core/API suites run because mandatory core caller signatures affect both
components. Final narrow tests cover new races/rollback/redaction; existing
forms pending/missing-rescan and RV-001 remain passing. Local Chromium path
and existing component tooling pass; evidence in changes/details.

<!-- rpi:task id=P04-T03 -->
#### [ ] P04-T03: Finding disposition, exact final head and normal topic push

Record original reviews unchanged, requested RV-002 source correction completed
but full acceptance blocked pending coordinator independent final-head review.
No new reviewer or fabricated Pass. Privacy-safe commit/trailer, normal same-
branch push on main92d4f89, exact final-head handoff then stop; no merge.
Actual schema authority is unrelated human work, not a blocker to this fix.
