<!-- markdownlint-disable-file -->
# RPI Phase Details: Controlled bulk preview

Task ID: 78; slug: controlled-bulk-preview-78; date: 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md.
Research: .copilot-tracking/research/2026-10-17/controlled-bulk-preview-78-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01 |
| P02 | Complete | P02-T01, P02-T02 |
| P03 | Complete, historical bounded correction ONE | P03-T01, P03-T02, P03-T03 |
| P04 | Complete and source published; independent acceptance not claimed | P04-T01, P04-T02, P04-T03 |

<!-- rpi:phase id=P01 -->
## P01: Core preview and atomic application

Context: C3-C6 establish owner/manager rights, case touch and checked meta docs.
No generic field-edit prior art; source-backed domain actions already exist.
Do not change their authority or represent administrative notes as decisions.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fail-before contracts and core

Use synthetic `dataset.DATA`, temporary Store/SqlStore and two connections.
Capture baseline focused failure before creating module/mixin methods.
Store server-owned previews under checked `bulk_edits` meta document; no schema
or new SQL table. JSON uses existing persistence only. SQL binds each complete
case digest and rowversion (including changed-away-and-back); snapshot includes
actor and relevant staff context. Add transient validation context consumed by
the existing `save()` transaction, not a pre-lock check as a substitute.
Re-read SQL staff and target cases after BEGIN IMMEDIATE; validate current
identity, owner, field rules and expected target versions there. Preserve
normal rowversion checks, checked-document concurrency and batch state.
Use `ConflictError` for freshness and standard value/permission errors otherwise.
Clear validation context on every completion/failure; generic SQL failure
must not publish success or duplicate pending successful events.
Record metadata-only refusal after rollback, never raw hostile field values.
Store visible immutable edit history with each old/new field and source/version,
actor/time/reason; redact all nested free text for roles without recorded need.
Tests: exact preview/outcome shape, all-or-nothing mixed failure, invalid data,
every controlled category, no-op, creator binding, role/ownership revocation,
changed target and ABA, rollback, restart, preview tampering and concurrency.

<!-- rpi:phase id=P02 -->
## P02: API integration and delivery

<!-- rpi:task id=P02-T01 -->
### P02-T01: Routes and HTTP checks

Add two exact endpoints before dynamic case route; app identity and trusted-proxy
CSRF remain mandatory. Audit blocked contractor/unknown bulk attempts without
returning payload content. Add two static paths to shared role inventory,
keeping #377-compatible additive shape. Loopback synthetic SQL tests check
health/responsiveness, 200 preview/apply, malformed/forbidden 400, permission
403, stale/replay 409 and persisted rejection history. No browser needed
because web assets and behavior remain unchanged.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Validation and evidence

Run smallest focused new core/API tests, then relevant existing handoff,
store/SQL, controls and role inventories/dialect tests. Run component existing
ruff/format/mypy on affected scope. Own `.venv` only, installed after actual
missing-package failure. No Docker/cloud/private datasets.
Document bounded fields, examples, status/error semantics, durability limits,
no approval/ownership transfer, criterion matrix and overlap. Update existing
knowledge synthesis and index/log; memory/original unchanged.
Reconcile plan/details/changes and current state before exactly one Review.

## Unresolved Items

None after PC-001 through PC-006 direct disposition. Plan's refined contract
owns field/category matrix, exact outcomes, issuance hash binding, fresh
identity/OID disclosure and commit checks, full exception recovery/fault tests,
and final reviewed/pushed main PR gate. Full preexisting FR-005 provenance
acceptance remains partial and must not be claimed closed.

<!-- rpi:phase id=P03 -->
## P03: Correction Cycle ONE (same #78 / PR #378)

Explicit continuation supersedes original stopped/no-fixes handoff, not the
historical Not accepted outcome. Use existing files, no full RPI repeat.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Immutable eligibility

Before production edits capture failing tests for cached/persisted SQL blocked
status reset. Include exact unchanged cases/history and no success audit, only
visible refusal. Validate issued request ID ordering, unique record coverage,
complete snapshots, each failure/outcome, and exact proposed allowed changes.
Recheck anchored issued eligibility and every target inside existing commit,
not just eligible snapshot subset. Preserve pending/no-op/handoff semantics.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Provenance trace and validation

Inspect existing evidence-upload and handoff offer/transfer records plus caller
payloads. Do not invent missing owner-supplied reason/source/version. Retain
partial acceptance for significant changes requiring new inputs and UI/API
decisions; document precise fields and existing retained evidence. Focused
unit/HTTP/store regressions and existing lint/format/type tooling only.

<!-- rpi:task id=P03-T03 -->
### P03-T03: Independent assessment and publication

One fresh independent agent checks the correction diff and tests after source
changes finish; persist separate assessment, not rewrite the original Review.
Commit/push same branch/PR using privacy-safe identity and trailer. Final push
then stop, no rebase/merge/force-push, cloud/private data or nested delivery.

P03-T01/T02 completion evidence: 71 focused tests pass (39 core bulk, six
loopback HTTP bulk, 26 existing handoff/document tests). Core ruff and format
checks pass (51 files), mypy passes (104 source files).

RV-002 inspection uses `store.py:583-610`, `workflows.py:159-239`,
`server.py:783-827` and UI caller evidence `app.js:622,659-662,794-798`.
Evidence upload has content hash/version/display actor/date and a separate
email/time audit, not supplied source/version/reason. Handoff snapshots have
versions/email/time/role/from-to, not explicit source/source-version; acceptance
has no reason argument or canonical old/new owner provenance event. Empty
acceptance and file-only upload are existing API/UI contracts, also exercised
by existing tests. Requiring the missing inputs is behavior/UX compatibility
work, not a safe backfill. No fabricated defaults, new bulk fields or approval
authority; criterion 1 and RV-002 remain partial for coordinator.

P03-T03 independent assessment completed by read-only
`issue78-correction-one-review`: no substantive findings, accepted for bounded
correction only. Reviewer source-inspected transaction/recovery checks and ran
an independent synthetic probe (two valid accepted / ten invalid rejected);
did not claim to rerun the parent's suites. Separate dated review retained.
Correction commit dd52ae3a9ab0aee2ff96cda7e7496c3de29a58ec was pushed
normally and read back as PR #378 draft/open main-targeted head. PR body now
links original unchanged Review, independent correction assessment and exact
remaining caller-provenance scope. Final artifact-only receipt is the last
push, then stop. Full #78 acceptance remains unmet.

## Same-PR Integration After PR #377 Merged

Owner authorized rebase, not a new delivery/review cycle. Old publication
97cdc2a; new main 92d4f89; tested rebased source
8602473a78930a72aa7fbb2d424a76d56dba5b53. Preserve both scoped modules,
Store/projection protections, API routes/inventory, SQL checked documents/
validators and complete guides/KB histories. Five conflicts resolved by
retaining both features, no field/authority expansion. Forms/bulk modules and
their tests equal their respective main/old-published versions byte-for-byte.

110 joint focused tests passed, including pending/missing rescan durability,
permissions, rollback/concurrency and SQL reopen. Existing core
ruff/format53/mypy106 and API ruff/format19/mypy49 passed. Full original Review
unchanged, correction finding disposition preserved, RV-002 still blocks full
criterion 1. Actual form authority is unrelated human-blocked. Active external
review512a59c4 needs exact final SHA/delta, no inferred final-head acceptance.
Final evidence commit on tested source, exact topic-only lease against97cdc2a,
draft PR publication/readback then stop; no merge.

<!-- rpi:phase id=P04 -->
## P04: Correction TWO, Exact RV-002 Caller Gap

Owner explicitly authorizes source/API/UI implementation after independent
review512a59c4 Revise on97cdc2a; no new RPI or independent-review loop here.
Starting head ae3adfb is clean and fully rebased on92d4f89.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Implemented Required Inputs and Bound Events

Fail-before receipt: seven new JSON/SQL tests, four assertions proving missing
metadata still accepted plus 34 missing-contract keyword/signature errors,
not loader/dependency failures. Source correction then adds shared
`change_provenance` operation context for existing upload/offer/accept only.
Explicit source/version/reason, integer current handoff-history version,
registered actor and UTC/change-version with exact old/new refs/ownership.
Existing metadata/permissions/recipient acceptance and workflows preserved.
SQL final actor check under writer transaction, rowversion conflict and
failure recovery; exact identical event in case history and immutable audit.
Legacy missing request input refuses, old stored history unknown/not rewritten.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Implemented Direct Callers and Verified UI/Contracts

API caller wiring, legacy handover offer alias, explicit test-only synthetic
metadata fixture; directly affected upload and offer/accept native forms.
Web skills/current full guideline retrieval before edits and refresh before
final changed-region review; no unrelated design overhaul. Existing Fluent
tokens/plain ASCII/sentence-case precedence retained.

Full core suite: 609 tests, one existing skip. Full API suite: 574 tests,
111 existing opt-in skips. Suites run once after caller updates because
mandatory metadata changes affect both components; not repeated wholesale.
Final added race/redaction cases covered in 119-test focused pass after suites.
Core ruff/format55/mypy108, API ruff/format19/mypy50, JavaScript syntax pass.
Final strengthened full-reference-list/event-version/defensive-copy assertions
pass in 13 provenance tests; core tooling rerun passes unchanged counts.
Local Chromium final path passes missing-field focus, Enter upload/offer/accept,
inline stale refusal/focus/value retention, recipient-only ownership, 390px/
reduced-motion and SQL reopen/history-audit equality; no page errors/external
requests. Browser entry fixture corrected from welcome `/` to actual `/app`.
No private stock/cloud/paid inference/live SQL Server. Existing unavailable-law
diagnostics are unknown rule checks, not successful law evidence.

<!-- rpi:task id=P04-T03 -->
### P04-T03: Exact Source Publication, Not Independent Acceptance

Self finding disposition: requested RV-002 upload/offer/accept implementation
gap corrected with explicit inputs/events; RV-001 unchanged and regressed.
Original Review and review512a59c4 Revise remain historical. Coordinator must
independently reassess final exact head; acceptance remains blocked until then.
Actual form authority is an unrelated human prerequisite, not an excuse to omit
this source correction. Final same-topic normal push then stop, no merge.

Source `2e63cdf74a2f28d17e2cf3cbc993171755424fbb` ordinary-pushed and
verified by ls-remote and PR API, draft/open/base main. One immediate PR read
was eventually consistent and still showed ae3adfb; direct subsequent endpoint
and remote both confirm exact new source. Artifact-only receipt follows;
PR records exact final SHA/delta, no further source change or test claim.

## Completion Evidence

P01-T01: new core module plus 32 synthetic JSON/SQLite tests pass, with
fail-before evidence and failure/reopen/interleaving assertions in changes.
Functions plus two thin Store wrappers replace proposed mixin plumbing;
same public contract, fewer inherited members, no authority/scope divergence.
SQL hook is two lines plus one checked-document name; recovery stays bulk-scoped.

P02-T01: two POST routes and two inventory entries, six HTTP tests including
password/proxy identities, CSRF, malformed/forbidden/revoked requests and explicit
503 uncertainty. No web assets changed, so no browser/source-guideline claim.

P02-T02: core/API existing lint/format/type pass, focused controls and SQL/API
regressions pass; dialect suite has 3 local passes and 48 live-server skips.
Component guides plus existing synthesis/index/append-only log updated.
Plan/details/changes reconciled for one Review. Publication remains lifecycle
work after Review, not falsely represented by implementation checkmarks.
