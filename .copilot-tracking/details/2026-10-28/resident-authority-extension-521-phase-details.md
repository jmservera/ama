---
title: Resident demo authority extension phase details
description: Evidence-based task details for issue 521
ms.date: 2026-10-28
---

## P01

P01-T01: Research C1-C4. Update existing JSON to 2027-02-01T00:00:00Z.
Import AUTHORITY_END in SQL renderer, substitute an authority token in both
new-table and migration checks. For an existing table, transactionally drop
the known named constraint if present, add WITH CHECK, commit; XACT_ABORT and
TRY/CATCH rollback/rethrow protect failure. No rows, grants or user creation
are added beyond the existing script contract. Fresh creation retains the
same checks. SQL time is UTC DATETIME2(0), cap has whole-second precision.

P01-T02: Keep existing tests in their owner suites. Test old cutoff and January
admission, exact boundary/session expiry, helper cap equality/over-limit and
new/old existing SQL constraints. Renderer must eliminate every token and
contain the exact shared date. API test uses constructed rows, fake clock and
real loopback HTTP; optional SQL tests use existing owned-loopback contract.
Do not extend independent resident AI tariff guards.

PC-002 assertion matrix: extend the existing fresh-table guard test for cap
equality, over-limit, reversed window and blank provenance. Add two SQL methods:
legacy-November migration plus idempotent reapply, and invalid-data rollback.
Assert sys.check_constraints enabled/trusted state, original row/provenance/
revocation preservation and existing principal denials after success.
For failure, create invalid legacy data only in the owned disposable database
with a disabled named check; snapshot definition/state, assert error rethrows,
@@TRANCOUNT zero and original definition/state/rows restored. Keep transaction
and catch in one batch. Unrun SQL assertions are unverified, never passed.

## P02

P02-T01: Research C5-C8. Preserve dated December owner decision as historical;
add prospective #521 section stating source-only extension and pending live
apply. Explain version overlap, session invalidation, existing helper Modify
refusal, explicit SQL row approvals and unchanged SID/permissions/private path.
Estimate source-only cost zero; model longer window from existing USD30
resident allowance with explicit assumptions, not a new allowance or live rate.
Unknown accrued/delayed charges and January funding block paid action.
Require total liabilities plus reserve plus proposed increment <= USD700.

P02-T02: Missing zava_forward import observed before setup. Install existing
src distributions with pip into new external venv under nonblocking heavy
lock. Keep scratch outside checkout. Run focused regression and core/API,
infra helper and tools suites, recording opt-in skips honestly. No subprocess
may run az; avoid compiled-Bicep test classes that invoke it. Full publication
gate has an incompatible az preflight; do not bypass, fake or mark it passed.

PC-001 safe selectors: run test_resident_demo_secrets in full. Load
test_resident_demo_deploy.CommandTests but exclude exactly
test_compiled_inventory_including_guard_passes_and_unknown_nested_is_refused.
Do not select TemplateTests: its setUpClass calls compiled(), and that excluded
CommandTests method also calls compiled() directly, which runs az bicep build.
Use unittest TestLoader to select remaining IDs, record the omissions. Inspect
subprocess paths for any broader suite before executing it.

## P03

P03-T01: Delegate one fresh independent Review over final source/diff and
record actual findings/outcome. Preserve critique and original Review.
Do not repair Review findings or repeat Review within this completed task.

P03-T02: Resolve gh api user and configure local noreply address for author
and committer. Commit source and original dated artifacts with required
trailer. Full local gate is mandatory for SQL changes; no az permission
means publication remains pending unless a genuinely allowed complete receipt
exists. Do not push merely to obtain hosted checks. No cloud fallback.

PC-003 conditional order: original Review, commit, genuinely permitted full
gate, refetch main, verify external receipt against current origin/main and
clean unchanged HEAD, independent exact-head assessment, push once, create PR
using Refs #521 only. Changed head/base/inputs or unavailable verification/
assessment stop publication. This does not repeat the original RPI Review.

## Current Execution Reconciliation

P01-T01/T02 and P02-T01 source work is authored (five added test methods,
none removed). P02-T02 required validation is Blocked: foreign heavy lock
holder and missing installed namespace, with no polling or bypass. Eight
independent lightweight tool safety tests passed; the demo-feedback tools
suite import failed. Static evidence is in the changes artifact.
Proceed to the one original Review as an explicitly unvalidated candidate,
not a completed acceptance claim. P03-T02 commit is separable from its blocked
full gate/publication portion. No live apply is part of this RPI candidate.
