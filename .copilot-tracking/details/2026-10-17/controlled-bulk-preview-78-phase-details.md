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
