<!-- markdownlint-disable-file -->
# RPI Phase Details: Grant lifecycle controls

## Metadata

Task ID 95; slug grant-lifecycle-controls-95; date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/grant-lifecycle-controls-95-plan.md.
Evidence: matching research artifact, C4-C8 and fail-before probes.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Evidence-led lifecycle hardening | Implementation and one Review executed; Not accepted | P01-T01/T02/T03 |
| P02 | Coordinator-selected RV-001 correction | Complete; published PR #386, coordinator gate pending | P02-T01/T02 |

<!-- rpi:phase id=P01 -->
## P01: Evidence-led lifecycle hardening

Keep separate existing funding and grant objects; no new payment or submission
implementation. Use src only, tiny fictional seeds and task-owned SQL resources.
Preserve existing #94 recoveries, independent identities and actor validation.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add failing-first exact regressions

Core harness may subclass existing FinanceChecks solely for store setup/open and
MSSQL lifecycle, but grant tests must independently exercise grant_action and
funding_step, not substitute invoice assertions. Cover fake/stale role/name/OID,
missing designation, malformed/nonhuman/expired/production authority, alias
email/code/OID, legacy preparer resolution, safe rollback and audit preservation,
transaction-time revocation, concurrent rowversion conflict, GBP refusal and
per-event amount/source/identity. Authorized success fixtures explicitly declare
exercise designation only in tests, never production seed or private staff.

API: reuse actual loopback authenticated fixture, health responsiveness, denial
and success, funding queue/case/stat projections and separation invariants.
Do not duplicate existing #94 test class through inheritance discovery.
Completion evidence: meaningful baseline failures recorded before source fix.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Reuse finance operation and current designation checks

finance.py owns context-manager extraction and SQL revalidation extension. Its
finance_action remains a closed action set, requiring registered Finance staff.
Grant/app paths call the same boundary with action-specific authority requirement;
all failures use existing case/ledger rollback and original-error diagnostics.
Capture designation from current persisted staff, compare its exact snapshot at
commit time and preserve it on the event. Source references are supplied, not
verified by the application. Explicitly label exercise-only authority, never real.

Grant proposal captures preparer identity. Approval calls existing independent
helper, retains scheme/case/currency/source/actor dates; no historic backfill.
GBP-only input refusal prevents dollars silently becoming pounds. Missing new
designation deliberately refuses previously role-only approval and application
terminal writes. Document this intentional safety change.

PC-002/003 exact contract is owned by the finalized plan. Validate the full
effective UTC interval both at entry and in the SQL transaction, not snapshot
equality alone. Match each permission on action including target state, exact
case and exact grant scheme/application route, with subject email/code/OID.
Reject malformed scope, expired/replaced authority and production exercise use.
PC-005: old pending records without explicit GBP require withdrawal/re-proposal.
PC-004: funding history is append-only per approve/submit/confirm, carrying
separate supplied evidence plus actor/authority snapshots and route/case/time.

Completion: old finance suites unchanged in meaning; failures cannot leak
pending success events or partially opened grants; current registry revocation
fails inside transaction and after store reopen.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validate and document for independent Review

Relevant commands use worktree .venv editable source installs. Full core/API
unittest discovery, existing project Ruff/format/mypy; local SQL harness uses
actual mssql-python and uniquely named task-owned container/database only.
Credentials stay out of commands/logs/artifacts. If a check is unavailable record
Not run/Blocked, not Pass. Browser not required because no web behavior/assets
change except the PC-001 neutral application confirmation label and required
evidence input. Load web guidelines and fetch current rules; exercise actual
Opportunity-only/Confirmed-application UI locally with Playwright. Static
dashboard and returned projection evidence is distinct from
browser/human/WCAG acceptance.

Update src core/API READMEs and existing finance journey synthesis, KB index and
append-only log. No original case or owner memory changes.
One fresh independent reviewer activates rpi-review and writes exact outcome,
assessed boundary and findings to the review path. Parent must retain adverse
findings and route/correct concrete in-scope defects only as authorized.

Completion: plan markers/details/changes/validation reconciled before Review;
review evidence and limitations included in PR with Refs #95, no closure claim.

Implementation validation complete: focused 89/89; actual local SQL Server
34/34 (15 grant, 19 preserved finance); full core 724 with 35 explicit skips;
full API 588 with 121 explicit skips; final changed-label HTTP/Playwright 2/2;
core/API Ruff/format/types; migration 25/25. Full core's initial stale fixture
digest was repaired with an actual digest refresh, eight manifest tests and a
clean complete rerun. No DATA or journey coverage change. The one independent
Review subsequently executed Complete / Not accepted; original verdict retained.

## Critique Evidence Allocation

PC-006: use setup-only methods/composition, no inherited finance TestCase tests.
Designations are added to deep-copied task fixtures, not shared module STAFF.
Allocate grant_open invalid input/audit failures, grant_approve save/audit and
early/persistent recovery failures with prior pending audit, application
approve/submit/confirm rollback including funding_ok, known/unknown legacy
identity, same-code/OID registered aliases, no-sequence authority changes,
clock-only expiry and rowversion conflicts across JSON/SQLite/actual SQL Server.
Keep original #94 suite counts separate from grant parity.

<!-- rpi:phase id=P02 -->
## P02: Coordinator-selected RV-001 implementation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Restore legacy transaction identity provenance

Complete. Original Review identified a concrete regression, not a missing human
permission. All four grant/finance x code/OID subtests failed before the fix.
Restore original supplied identity in finance validation context so absent
legacy identity reloads current persisted staff inside the SQL transaction.
Continue returning resolved entry identity for grant event history. Captured
historical identity, current actor checks and authority checks stay intact.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Validate and publish without relabelling independent outcome

Complete. Current focused grant/finance/API/actual Chromium plus eight manifest
tests pass: 98 tests, no skips. Core/API Ruff, format and mypy pass (112/52
source files). Actual task-owned loopback SQL parity passes 35 tests (16 grant,
19 preserved finance), including all four new refusal subtests; owned container
and UUID databases removed. Broad pre-correction discovery evidence stays
distinct from correction coverage. Main-targeted PR #386 is open; source commit
a82da8d1d8f2e912330af76d47ad143f24309eca was verified identical locally, remotely
and in the PR, with a clean worktree. This final publication state is committed
separately and the resulting head reverified. No second Review: coordinator
owns final independent acceptance, checks and merge. Session stops at explicit
PR boundary; no claim that an empty initial check rollup means passed CI.

Authorized post-publication integration rebases onto freshly fetched main
1fc7325b93ea845b9cb2e827efbea624f7d20d30 (#385 plus #384). Only manual
conflicts were append-only KB log and combined fixture digest; whole own src
added/removed byte parity across bases proved. Fresh 156 combined
grant/finance/procurement/API/browser/manifest tests and core/API quality gates
pass. SQL 35/35 and broad discovery remain earlier historical evidence.
Original one Review unchanged; coordinator independent closure pending.
