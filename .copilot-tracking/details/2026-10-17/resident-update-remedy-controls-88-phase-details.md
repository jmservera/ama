<!-- markdownlint-disable-file -->
# RPI Phase Details: Resident update and remedy controls

## Metadata

* Task ID: 88
* Slug: resident-update-remedy-controls-88
* Plan: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md
* Evidence: matching dated research C1-C11/W1.

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Bounded resident controls | complete, including actual changed browser journey |
| P02 | Validation/documentation | complete; evidence reconciled before original Review |

<!-- rpi:phase id=P01 -->
## P01: Bounded resident controls

Intent: reuse resident_action/service_requests/resident_update and existing SQL store.
Excluded: provider portal, Legal decision authority, sending and unrelated workflow architecture.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Domain and persistence

Likely targets: resident_decisions.py and a small resident-controls helper if needed,
workflows.py, store.py projection and sqlstore.py additive validation/commit marker.
Keep existing status compatibility on requests: status still means response/service
record, never remedy. Separate remedy lifecycle/history with explicit state transitions.
Explicit expected versions for new update/remedy/reopen actions; legacy response
actions retain API shape but use current record and owner checks at transaction.

Use registered email lookup, compare name/code/role/OID, and retain captured identities
separately from current lookup. For legacy absent identity, bind from recorded email
only for current decision authorization; never overwrite historical event provenance.
Unknown original dates/owners remain null/Unknown in projections. Validate actual
ISO calendar next-update dates; due date is aware ISO UTC. Recheck on writer save
using captured input and dependency snapshots/current registry. Reuse canonical
SqlStore._discard; scope owns pre/post-COMMIT recovery, preserving legitimate prior
audit and original exception even if recovery fails. JSON caught errors restore
prior record/ledger independently; no abrupt-crash cross-file atomicity claim.

Completion: failing-first semantic tests pass over JSON/SQLite; no automatic mutation
of delivery/quality/finance and no successful audit from refused writes.
Executed: missing action/remedy failed first; subsequent 65 tests OK/two opt-in
skips include full mixed-state scenario, current-identity and recovery faults.

Final critique amendments PC-001/002: update_record confirms absent/unversioned
commitments only on expected_version=0 plus all full fields, preserving raw prior
snapshot. remedy_confirm requires absent remedy/version zero, current eligible
owner and supplied basis; original open time/identity null, confirmation time separate.
Response unchanged. Other remedy actions require confirmed state and expected version.
Assignees/writers restricted to controls.RESIDENT_VIEW_ROLES; owner or existing
Retrofit Programme Manager/Programme Support Officer may mutate. Captured identity
binds owner rights; unresolved legacy lookup uses original email at writer time.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Existing web and HTTP journey

Depends on P01-T01. Existing panels.js resident area gains a native full-commitment
form and independent remedy status controls; expose safe refs only under existing
resident permissions. Existing complaint response update/close forms stay compatible
but wording makes boundary explicit. app.js handoff only references an existing
commitment; no partial creation fields. Scoped forms need name/autocomplete/labels,
Enter submit, live inline errors/focus and retained input on error. Do not globally
rewrite actForm or unrelated forms. Fresh web guideline review before final review.
Completion: authenticated loopback HTTP, actual browser create/reassign/close-response/
remedy-still-open/reopen/refusal journey and no page errors.

PC-003: include server.py resident-only outcome handling. Trusted domain
ResidentCommittedError and successful-write marker distinguish post-COMMIT sync/
projection failure from refusal. JSON includes outcome=committed and reload/reconcile
instruction, original diagnostic retained/logged. New resident forms disable resubmit
after this outcome until reload; do not alter unrelated error architecture.

<!-- rpi:phase id=P02 -->
## P02: Validation and documentation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Regression and real local SQL

Depends on P01. Pip-installed .venv source packages only. Core test ownership:
existing test_resident_decisions.py maximum 18 additional semantic methods plus
SQLite/MSSQL subclasses; API test_resident_api.py maximum 5 additional methods,
including optional actual browser. Amend handoff fixture to explicitly create
commitment before handoff; remove no existing tests.

Exercise actor/destination mutation between validation and BEGIN/COMMIT without
case sequence change, conflicting actual writers, invalid dates/version, legacy
unknowns and captured-vs-current identity. Inject pre-COMMIT audit failure,
first/persistent recovery reads, prior audit prefix and post-COMMIT synchronization
failure; reopened state and audit must prove outcome/no replay.
Run all directly dependent closure/recovery suites (stock/hazard/procurement/
quality/finance/grant/workflows), configured project Ruff/format/mypy.
Create a unique task-owned SQL Server loopback container; never reset other servers.
Build own API src-context image/non-root local smoke when relevant; no Azure.
Record unavailable/skipped checks honestly.

PC-004: one grouped semantic mixed-state test uses public fixture helpers and actual
order completion, quality handover (separate open-defect subcase), finance note,
return/reopen and store restart. Assert unchanged remedy and independent Defect/
Charge query request status, owner, original date and history after every step.
Canonical response status/status_owner/status_at and remedy owner/at/opened_at/history
must never borrow another clock. Legacy confirmation and role tests grouped within
18-method maximum; HTTP committed synchronization/projection faults and actual browser
within five-method maximum. No extra full review or test removals.

Immediately relevant refinements: finance payment_status previously lacked owner/date;
add only its current note owner/date and retained note history, no disposition or
payment changes. Real browser exposed actForm's nested label/input arrays rendering
as object text with one-level h flattening; change its single map to flatMap, not a
form-system rewrite. New scoped forms use flatMap too. Current actor helper is loaded
lazily because direct import produces resident/projection/change-provenance cycle.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Evidence and handoff

Depends on P02-T01. Update src/core/API README and existing
docs/reference/research/ux/customer-journeys/residents.md; preserve exact KB log
upstream prefix and existing routes while appending own finding. No memory/original
case changes. Declare actual overlaps in changes/PR and every unperformed acceptance.
Reconcile phase checkmarks/details/changes/state before one original Review.
Retain adverse Review unchanged; at most two authorized corrections, no second Review.

## Implementation Completion Evidence

P01-T01/T02 and P02-T01/T02 complete. Final dependent run: 378 tests, five
documented opt-in skips. Focused run enables actual local browser: 81 tests, one
SQL opt-in skip. Separately eleven actual owned MSSQL tests pass, including
negative concurrent writers and recovery/audit faults. Core/API full configured
Ruff, format and mypy pass; JavaScript parses. Final src-context API image
485706b0361ccef3f6057faaed5f4ec7aeb1c3fdfd3c485a4eb854650b5c87b9
passes existing non-root/hardened/plain startup and negative hardening probes.

Scoped resident service open/update/close forms now share truthful committed/
uncertain outcome handling with update/remedy forms, not unrelated action forms.
Reuse existing beforeunload unsaved-form guard; retain server-refused draft.
Display status/due date and time using Intl; unknown legacy times remain Unknown.
Strip complete commitment snapshots from nested handoff changes for roles without
resident view, as well as top-level records.

Existing core/API guides and resident synthesis updated, index route additive,
upstream log SHA256 f35003c314bd9eb31bb4bb00ee1ccb2cc93ba0b35d72610e89f428872c8f80a1
retained as exact byte prefix with own appended entry. No pending implementation
or validation blocker; human/WCAG/full-PRD and coordinator final-head acceptance
remain unperformed and are not completion claims.

## Original Review and Separate Routing

Original Review execution Complete, outcome Residual work. RV-001 Low asks for
actionable separate ownership of the wider governance exclusion, not new issue88
code. After Review completion the planning parent/repository owner is explicitly
the routing owner; next #81 backlog triage must identify an existing separately
owned item or assign one for Legal/Housing/Complaints governance. Those specialists
retain policy approval, not the agent. Plan/changes/state now carry this next
action. No second Review or code correction, no original Review rewrite and no
coordinator Pass. No child work starts before the requested publication stop.
