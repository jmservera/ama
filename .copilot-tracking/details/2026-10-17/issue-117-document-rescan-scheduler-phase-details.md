<!-- markdownlint-disable-file -->
# RPI Phase Details: Bounded pending-document rescans

## Metadata

Task ID 117; slug issue-117-document-rescan-scheduler; date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/issue-117-document-rescan-scheduler-plan.md.
Research: .copilot-tracking/research/2026-10-17/issue-117-document-rescan-scheduler-research.md.
Initial direction: reuse scan/config/SQL boundaries; no operational enablement.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete; source/CLI validated | P01-T01, P01-T02 |
| P02 | Complete; actual SQL/image/regression/docs receipts recorded | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement bounded core and job

<!-- rpi:task id=P01-T01 -->
### P01-T01: Extend scan service and add safe SQL pages

Targets: core `doc_controls.py`, new `document_rescan.py`.
Keep the manual scan path and legacy helper compatible. Add an optional
non-deleting mode to `_scan_stored`; validate scanner verdict before writing.
The page runner requires SQL, selects sorted pending/missing keys, limits
attempts and exposes a two-part cursor. Recheck generated/resolved state on
each document under the Store lock and call `_case` to register touched state.

Before scanning capture prior pending audit and case snapshot. On pre-commit
failure call existing `_discard(prior)` under dblock; its quarantine occurs
before recovery I/O. Keep original error and explicit notes on recovery failure.
Set an own-operation thread-local committed flag immediately after the actual
SQL COMMIT in `SqlStore.save`, following existing hazard/resident patterns.
Never infer own commit from snapshot changes: competitor recovery also changes
snapshots. Restore prior audit on rejected CAS even if save already recovered
or that recovery failed. For an own-COMMIT acknowledgement error, raise shared
`CommittedOutcomeError` and do not append a false rejection or restore prefix
that was already committed.
Do not adopt staff identity or the staff validation context.

Expected report counters: checked, clean, pending, blocked, skipped, failed,
committed; continuation uses the last selected key, including skipped records
when another writer resolves them before recheck. A failed/pending
document is revisited on the next full sweep, not retried indefinitely in-page.
Success audit retains existing `document_rescanned` event contract; failed
success must never flush at outer lock exit. Failures are explicit and safe.

Validation: AC2/3; genuine missing document/bytes, pending tags, bad/unknown
verdicts, scanner exception, SQL conflict and outage. No destructive scanner
path under legal hold. Maximum 100 attempts, independent of result.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire configured orchestrator command

Depends P01-T01. Target new orchestrator `document_rescan.py`, using existing
factory and scanner config, no new framework or service. Argument shape:
`--limit N`, `--after CASE_ID DOC_ID`, explicit synthetic-local opt-in flag.
Require explicit data path and SQLite/MSSQL choice before opening a store;
never default to the owner's private dataset. Require explicit scanner;
local without opt-in fails before store creation. Defender still requires
existing Azure Blob store settings and real enablement remains unmet.

Print sorted-key JSON report. Exit1 failures or committed-reconciliation takes
precedence; otherwise exit2 pending or non-null continuation; otherwise exit0.
Earlier pending pages still require a new cursor-free sweep.
Construction is inside the sanitized CLI error boundary. Add a narrow reusable
SqlStore construction guard that closes its opened db if initialization raises,
retaining the original exception and noting cleanup failure. Once returned,
CLI owns db and closes it in finally. Test actual-open then injected setup
failure and successful command closure. Do not load env files. Offline run uses local scanner and
constructed content with an explicit label, not evidence of real antivirus.

<!-- rpi:phase id=P02 -->
## P02: Validate and document delivery

<!-- rpi:task id=P02-T01 -->
### P02-T01: Exercise semantic and regression acceptance

Depends P01. At most two new test files: core runner/recovery and orchestrator
CLI. No removals, no generated targets, no unrelated fixture modifications.
Existing dataset fixture reused; temporary synthetic document records/bytes.
Opt-in SQL tests require localhost/127.0.0.1 and UUID-owned databases, dropping
only their own database. Own container exact name/ID; stop it before handoff.

Use actual independent connections for concurrent pending-to-clean races,
late stale result rejection, retry/reload, persisted pending attempts and
prior pending audit. Inject SQL failure after audit INSERT, recovery failure
and post-COMMIT refresh to prove success-once and no false rejection.
Include the PC-001 race with a prior pending prefix, competitor reload and
recovery failure: rejected worker must not be labelled committed and must retain
the prefix exactly once. Include a completely skipped selected page and actual
all-clean first page returning exit2 with continuation, then terminal exit0.
Use real non-mocked CLI invocation against persisted synthetic SQLite at least;
run same entry point on owned SQL where possible. Full orchestrator discovery,
focused core/provenance/progress/resident/sensor and API document-control tests.
Existing component Ruff/format/mypy, no new broad exemptions.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Build image, update docs and reconcile evidence

Depends P02-T01. Build `src/orchestrator/Dockerfile` with `src` context,
unique task tag. Use existing hardening checker and actual CLI run with only
synthetic fixture mounts; verify installed source matches changed path.
Document API/core/orchestrator applicability without changing web.

Update the existing document/form-fixture synthesis in
docs/reference/research/retrofit-synthetic-data/README.md, route from index and
append log entry only. Component guides describe continuation sweep, exit codes,
SQL requirement, explicit synthetic opt-in and human/service gates.

Completion evidence must list actual commands/results including real skips/
failures, stopped SQL, no paid/cloud operations and no operational acceptance.
Reconcile plan/detail markers and changes/state before invoking one Review.
Review findings become separate future work; no source correction or second
Review inside this task without new explicit coordinator authorization.

## Completion Evidence

P01/P02 full-plan implementation completed 2026-10-17. Canonical actual commands,
counts, skips and the final installed-image source hashes are in the changes
record. No task markers remain. One original Review is the next phase, not
presumed accepted. No human/service operational gate is marked complete.

Local refinement: unsupported verdict uses RuntimeError, so the retained legacy
helper cannot misclassify it as a removed document via its ValueError catch.
This is an in-scope compatibility correction, tested on SQLite and actual SQL.

## Post-Review Routing

The one original Review executed Complete / outcome Not accepted. RV-001 and
RV-002 are two Medium safe-diagnostics/malformed-result defects routed to later
rpi-implement with separate coordinator authorization. No production/test
correction or second Review is performed in this task. Completed P01/P02 markers
describe execution only. Research Status header metadata reconciled separately;
original evidence/outcomes remain intact.
