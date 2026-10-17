---
title: Quality handover controls issue91 phase details
description: Implementation task context and completion evidence
ms.date: 2026-10-17
---

## Metadata

Task ID: issue91. Slug: quality-handover-controls-91.
Plan: .copilot-tracking/plans/2026-10-17/quality-handover-controls-91-plan.md.
Research: .copilot-tracking/research/2026-10-17/quality-handover-controls-91-research.md.
Readiness: Ready after direct PC-001/PC-002 dispositions. No unresolved scope decision.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Quality authority/remediation/replacement | Complete |
| P02 | Minimal UI and contracts | Complete |
| P03 | Exact acceptance evidence | Complete |

<!-- rpi:phase id=P01 -->
## P01: Quality controls

<!-- rpi:task id=P01-T01 -->
### P01-T01: Regression assertions and implementation

Research C2/C6 establishes gaps and existing helpers. Add tests first in the
existing quality/procurement file and execute against unchanged code.
Implement within quality.py: current registered actor via stock.decision_scope,
retained participant identity and repair evidence, strict indices, explicit
supersession. Version evidence by successive record index/version with exact
same-measure predecessors; old record history and aftercare retained, active
acceptance/handover cleared into retained history and state marked Superseded.
Replacement retires every prior active same-measure acceptance/handover,
including two legacy HANDED records or older HANDED plus newer ACCEPTED.
New lineage identifies every retired index; each retired record links to the
new version. Already superseded records do not block future replacement.
Prior accepted evidence can be replaced via existing submit route. Other
in-progress records continue to reject duplicate submission. No new endpoint.

Each action enters one quality operation scope under the reentrant Store lock;
SQL uses existing actor transaction validator and rowversions. Preserve pending
legitimate audit prefix if recovery clears failed writes. JSON uses preimage and
own audit tail recovery following existing finance pattern, without importing
or editing finance.py. Errors remain explicit, recovery errors annotate original
exception. No new SQL persistence schema/authority hook.

Remediation note describes work/source evidence and is recorded in the current
defect and historical defect entry; it is not a professional compliance verdict.
FIXED acceptance checks this positive evidence. Keep all contributing participant
identities across repeated fix/return cycles. Identity labels are human records,
not proof of real competence. Resolve legacy participants from known recorded
codes/names conservatively; unknown original installer label cannot grant rights.

Consequential acceptance/handover preserve existing safety/resident checks;
require explicit existing binding rather than inheriting consent across
replacement. Superseded records are not actionable. Keep finance/grants
unchanged byte-for-byte through quality lifecycle tests.

Completion: A1-A3 assertions pass on JSON/SQLite; failure probes first fail for
the demonstrated gaps. No fixture or manifest edit.

<!-- rpi:phase id=P02 -->
## P02: Dependent surface

<!-- rpi:task id=P02-T01 -->
### P02-T01: Quality panel and documentation

Only ops.js needs visual behavior: label remediation evidence, explain
superseded history and permit current resubmission without old action buttons.
No app.js/server.py/dataset.py/finance.py/shared manifest edit planned.
Before web edits invoke web-design-guidelines and fetch current source.
Retain Fluent semantics, resident confirmation, manual path and plain content.
Update core/API READMEs, existing programme journey dated continuation, KB route
and append-only log. Preserve upstream content/prefix and other task routes.

Completion: fresh web-guidelines review and actual loopback browser covers
return/blank-remediation error/evidenced fix/independent reinspection/handover/
replacement/new acceptance, including retained prior record text.

<!-- rpi:phase id=P03 -->
## P03: Validation and reconciliation

<!-- rpi:task id=P03-T01 -->
### P03-T01: Execute acceptance evidence

Canonical targets and maximum test additions are locked in the plan. Run the
existing suites with installed editable packages and proper fixture paths.
Configured migration exemptions remain disclosed, not mistaken for full typing.
Actual SQL replay uses unique disposable container bound only to 127.0.0.1 on
an ephemeral host port and unique owned test database; generated secret remains
inside process environment, never command output/artifacts. Poll readiness by
actual SQL connection, not just container state. Preserve logs without secrets.
Clean only the exact created container/database.

Execute the exact method/backend matrix in the plan, including inherited
MssqlProcurement replay once, stale rowversion, changed actor within transaction,
actual audit insert rollback, replacement/reopen and recovery failure tests.
Pending-prefix regression must enclose the failing operation in a legitimate
outer lock/audit context to exercise stock.decision_scope discard, later flush
and original-error preservation. No existing/private
database wipe. Browser proves changed journey, not WCAG or human acceptance.
Record exact commands/counts/skips, amendments and divergence in changes artifact;
reconcile task markers before independent Review. Review cannot fabricate a Pass;
retain initial verdict and any authorized correction evidence separately.

<!-- rpi:phase id=P04 -->
## P04: Authorized correction ONE

<!-- rpi:task id=P04-T01 -->
### P04-T01: RV-001/RV-002

Independent original Review is Complete / Not accepted. Resolve its two
reproduced implementation findings, without another Review or invented Pass.
Include historical FIXED recorder names/codes in actual legacy lookup, not
only in the final unresolved-identity check. A genuinely independent approver
must remain able to accept; the earlier recorder and any populated aliases
must still be excluded.

The SQL store updates committed snapshots before its post-COMMIT refresh.
Capture own case snapshot before yield and detect snapshot advancement inside
the action's exception boundary, before shared decision_scope can discard or
reload a winning concurrent writer. A confirmed committed outcome must not
restore a pending prefix already committed with that action. Surface explicit
saved-but-refresh-failed guidance through a quality-specific API handler;
never silently return success or imply a failed rollback. Preserve the original
exception as cause and existing pre-commit refusal recovery.

Canonical new tests are locked in P04 plan. Test an actual unrelated writer
advancing sequence, actual COMMIT followed by early/persistent refresh-read
failure, with and without prior legitimate pending audit. Confirm exactly one
success/prefix, committed state after reopen, no stale pending event, and
HTTP 503 outcome=committed/reload guidance. Execute JSON/SQLite and inherited
actual SQL Server, existing pre-commit faults, HTTP and browser.

Completion evidence: both new fail-before methods reproduced the exact defects
(legacy unresolved known recorder and actual post-COMMIT OSError; five subcase
errors). Final implementation passes all named tests, 361 selected tests with
49 existing skips, 101 overlapping focused quality/content/design/route checks,
38 actual inherited local SQL Server cases, actual Chromium committed-503
notice/reload and complete handover/replacement journey. Prior pre-commit
failure/actor/stale/provider/stock/finance checks remain covered.
No second Review; original Complete / Not accepted retained.
