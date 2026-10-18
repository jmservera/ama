<!-- markdownlint-disable-file -->
---
title: Issue 86 recorder identity phase details
ms.date: 2026-10-18
---

## Metadata

Task 86 / issue-86-recorder-identity. Related plan:
.copilot-tracking/plans/2026-10-18/issue-86-recorder-identity-plan.md.
Evidence C1-C10 in research. Status: implementation-ready after single critique;
PC-001 resolved directly, original Revise assessment retained unchanged.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete, local SQL/core/API/quality/container evidence | P02-T01 |
| P03 | Original Review complete; publication active | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Implement bounded identity contract

Existing case histories are extensive. Keep all old decision/request entries
byte-equivalent until a requested controlled action appends or updates its
normal request fields. No migration or stable-identity reconstruction.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Historical identity, review guard and projection

Capture server actor using existing transactional `_operation`; add its explicit
recorder-role guard for decision_record so manager view rights cannot become
write rights. Store detached `_identity(user)` on new decision only.
Extract existing email/code/oid normalization comparisons, no unrelated helper
redesign. Resolve exact integer decision version and matching version field.
At opening bind original snapshot. At redress reassignment use that snapshot,
not current staff nor newest answer; unknown cannot pass. A retained request's
snapshot remains usable after payload deletion, without changing retention.
Legacy current view explicitly shows Unknown; do not persist a guessed snapshot.
Unbound legacy requests always remain Unknown; never fall back to a decision
ordinal that may have been deleted/recreated. PC-001 adds the retained-old-review,
real deletion/recreation and restart collision matrix plus bound-review positive
control across JSON/SQLite/MSSQL and authenticated HTTP.
Strip new snapshot from nonresident staff decision versions; contractor
allowlist and exports remain unchanged. Narrow core/API README text only.
Completion: code diff limited to these dependent contracts; AC1-AC6 covered.

Actual completion: resident module, dependent projection and two component
contracts changed. Existing actor/snapshot/transaction primitives reused.
Six new core test methods (five inherited plus one SQL-only) and two API methods,
no removals; original tests unchanged except JSON staff-fixture persistence
helper now maintains the canonical staff list as well as its lookup.
78 resident JSON/SQLite tests ran (one existing JSON-only skip); eight before
probes now deny atomically. PC-001 deletion/recreation and bound-positive matrix
passes in inherited suites and actual HTTP.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Existing-suite semantic and regression coverage

Test ownership: parent implementer. Removals none; maximum eight core/two API
new methods. Existing tests inherited on JSON/SQLite and opt-in local MSSQL.
Subtests distinguish stable code versus stable oid (changed other identifier),
open/reassign, valid distinct reviewer, body claim and forged actor, exact
old version after latest answer, missing/malformed legacy, projection/export,
case/audit equality and reopen. Add SQL writer registry-race test if needed.
Existing method and role behavior must remain unchanged. No generated targets.
Completion: failing-first probe retained; new suite passes with no weaker
assertions or test deletions.

<!-- rpi:phase id=P02 -->
## P02: Validate and freeze candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Local evidence and runtime parity

Use sanitized environment and explicit task-owned synthetic paths. Tests:
core JsonResidentDecisions + SqlResidentDecisions and API test_resident_api;
coupled role, change provenance, hazard/quality/release tests as indicated by
actual diff. Configured `ruff check .`, `ruff format --check .`, `mypy` from
core/API. MSSQL existing MssqlResidentControls against loopback-only unique
task-owned Docker container, run identity and coupled resident contract selection.
Create no shared databases; promptly remove task resources. Preserve all errors/
skips in changes. Frozen candidate commit supplies exact Review head.

Current results: 232 coupled core tests ran, 230 passed/two existing skips;
26 coupled API tests ran, 25 passed/one opt-in browser skip. All 44 actual local
SQL Server inherited controls ran, 43 passed/one JSON-only skip; container removed.
Configured core Ruff/format/mypy pass (124 typed source files); API pass (56).
Package/non-root HTTP passed: UID10001, no capabilities, read-only root,
exact installed domain/projection hashes, nine HTTP tests/eight pass/one browser
opt-in skip. P01/P02 complete; no implementation or validation blockers.

<!-- rpi:phase id=P03 -->
## P03: Original Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: One original independent Review and reconciled handoff

Fresh independent agent, rpi-review, full bounded source/test/docs/evidence
base-to-candidate diff. Write only original Review output. No second Review.
Keep original adverse assessment intact, hash it, use distinct correction
receipt if needed (at most two source cycles). Final plan/details/state must
reflect what actually ran, including publication; no stale authorization wait.
Authenticate GitHub account and use local id+login noreply for both commit
identities with required Copilot coauthor. Commit evidence then push exact
branch normally, open main PR with Refs #86. Main movement is reported, never
unilaterally integrated. Stop for coordinator full independent exact-head review.

Actual Review: Complete / Conformant on exact candidate
671ec03ac0e2e99478e9ae2c71537030d0541413. Zero implementation defects; one Low
RV-001 residual keeps broader #86 acceptance open. Original assessment frozen
SHA256 9d55fbff9904feb9e1d303cfb13be1f5047c766ee038aa2275cb911749a78dcc.
No corrective source cycle and no second Review. Publication is now active;
no additional implementation or approval is pending in this scope.
