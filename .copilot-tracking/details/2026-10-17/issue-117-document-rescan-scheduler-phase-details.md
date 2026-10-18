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
| P03 | Complete; correction source published same draft PR395, no independent acceptance | P03-T01, P03-T02 |
| P04 | T01 complete; T02 validation complete/publication pending; current base f9d80724 | P04-T01, P04-T02 |

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
record. Those original markers are complete. The one original Review subsequently
executed Complete / Not accepted; P03 is the separately authorized correction.
No human/service operational gate is marked complete.

Local refinement: unsupported verdict uses RuntimeError, so the retained legacy
helper cannot misclassify it as a removed document via its ValueError catch.
This is an in-scope compatibility correction, tested on SQLite and actual SQL.

## Post-Review Routing

The one original Review executed Complete / outcome Not accepted. RV-001 and
RV-002 are two Medium safe-diagnostics/malformed-result defects routed to later
rpi-implement with separate coordinator authorization, now received for P03.
No correction was made during the original loop; P03 implements both findings
without a second Review. Completed P01/P02 markers
describe execution only. Research Status header metadata reconciled separately;
original evidence/outcomes remain intact.

<!-- rpi:phase id=P03 -->
## P03: Coordinator correction ONE

Authorized 2026-10-17 after original session completion. Exact starting local/
remote/PR head552be52db0c2cb84a45449c2bce8d610abebfa74; main remains
ebc8dab87ae9bd6a33380b85e86f38be5ed9f213. Original Review SHA256
4e57eccdcd7817590110afd90c889d1f3c87de5b0bb48ac0353777fb7b3a2ac9;
critique f788cc3d53a983f00493bf26eee2a1764696bcdfe155464576e6691bfb8beea8.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Both reproduced defects in one coherent implementation batch

RV-001: recognize the worker-owned SQL recovery context alongside existing
validation contexts. Let `_attempt` preserve captured pending prefix, original
error and winner state, and emit safe recovery marker without nested traceback.
Keep all non-worker recovery and existing COMMIT marker ordering unchanged.
Strengthen the existing actual conflict test to inspect root logging text,
including traceback and private sentinel, then add actual CLI coverage.

RV-002: validate scanner return before unpack, exact tuple/arity, closed
string verdict and string detail. Reject None, wrong arity, invalid containers,
invalid verdict/detail types without coercion/private diagnostic interpolation.
Share the validation at upload/stored-scan boundaries where appropriate;
valid/manual bad-verdict exceptions stay unchanged. Explicit TypeError handling
at worker and CLI boundaries, not a broad catch or success-shaped fallback.
Existing tests only; failing-first SQLite and actual CLI, plus JSON shared scan
validation and retained bytes/hold/state checks. Continue bounded page on failure.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Exact correction evidence and publication

Run actual owned loopback SQL for complete worker class and relevant shared
rollback/prefix/committed regressions. Reuse existing local harness patterns
with distinct correction logs, never overwrite original test receipts.
Configured core/orchestrator Ruff/format/mypy and relevant API/manual,
progress/resident/sensor checks. Existing Docker build/hardening/real job,
updated source hashes. Preserve immutable original artifacts, stop exact owned
SQL/container, document commands/results/limits, commit/push same draft PR395.
No independent acceptance or second Review.

### Current P03 evidence (2026-10-18)

T01 complete: five selected failing-first tests reproduced both defects before
production edits; final focused46 run/27 passed/19 MSSQL opt-in skips.
T02 validation complete: all19 current worker cases on actual SQL, including
prior17, plus5 progress and6 resident shared recovery selectors, total30/30.
Actual MSSQL subprocess pages exit2/0/0, clean1/2/0; seven malformed/error
actual-main runs and competing-clean/recovery failure exit1 with failed1/
clean0/committed0 and no private sentinel/traceback in complete root streams.
Hardened rebuilt installed image matched four source hashes, safe failure6/6
then exact-once success pages. Local regressions281/203/78 skips, API57/45/12
skips, orchestrator30/30, store57/57; configured static checks pass.
Exact SQL stopped/removed. Full commands, selectors, hashes and genuine failure/
warning history are in the correction section of the changes record.
T02 complete after actual publication/verification: correction source commit
9468800e85b645b783f439de4e72018b7ae2488e equals local, remote and PR395 head,
clean worktree, PR Open/draft/main, issue117 Open. Main remains authorized
ebc8dab87ae9bd6a33380b85e86f38be5ed9f213. Fresh identity/privacy-safe author/
committer and Copilot trailer verified. Only this reconciliation metadata
follows that tested source boundary; no runtime/test edits. No active-plan
markers remain, independent coordinator acceptance and operational gates remain.
<!-- rpi:phase id=P04 -->
## P04: Final correction TWO, 2026-10-18

Coordinator supplies independent session558e33f1 Revise: original RV-001/RV-002
closed by actual SQLite CLI/log probes and seven-artifact reconciliation passes,
one new Medium unconditional optional-driver import blocks dependency-minimal
SQLite CI/module help. No new full Review. T01: backend-selected lazy driver
error import, no fallback/backend switch/workflow/dependency change, exact
driverless process coverage and available-driver sanitized error.
T02: authorized own-topic rebase onto merged396 main f9d80724; sole actual
conflict append-only KB log, retain exact upstream prefix then issue entries.
Runtime/test parity and upstream source/browser equality required. Actual
focused SQL if exception handling changes, owned container stopped afterward.
Preserve original Review/critique and existing correction ONE sections byte-exact.
Remaining failure after this last source cycle requires coordinator/human action.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Completed backend-selected exception dependency

Production change only orchestrator/document_rescan.py. Actual driverless
discovery/help failing first, existing-file subprocess regression failing first.
No-site driver absence asserted, same real discovery final32/31/one skip,
help exit0, configured SQLite success/failure exit2/1 with counters, missing
MSSQL driver fixed-marker exit1. Available-driver32/32 discovery and actual
native SQL invalid-table error sanitize correctly. No workflow/dependency edits.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Integration validation complete, publication pending

Main f9d80724 retains coordinator runtime/browser/test/manifest bytes unchanged.
Pre-fix integration had no runtime conflicts; only log append resolution.
Issue worker/core/tests remain exact old-head bytes except authorized CLI/test
pair. Upstream KB log prefix exact; original Review/critique and correction ONE
changes evidence byte-identical. Fresh configured core checks69 formatted/
122 typed; orchestrator9/12. Combined worker/progress/provenance/resident/sensor/
coordinator API273 run/186 pass/87 opt-in skips. New SQL20/20 (all19 worker plus
driver error), native driver-error CLI and actual success pages. Correction ONE
SQL30 is historical, not rerun. Rebuilt hardened installed image help/failure6/
success pages pass with hashes. Exact owned SQL stopped/removed.
Detailed commands/results/failures/hashes in changes record P04 section.
