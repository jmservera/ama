<!-- markdownlint-disable-file -->
# RPI Changes: Bounded pending-document rescans

## Metadata

Task ID 117; implementation date 2026-10-17; full plan.
Plan: .copilot-tracking/plans/2026-10-17/issue-117-document-rescan-scheduler-plan.md.
Details: .copilot-tracking/details/2026-10-17/issue-117-document-rescan-scheduler-phase-details.md.

## Execution Status

P01/P02/P03 complete; original Review Complete / Not accepted unchanged.
Final authorized correction TWO P04 complete against integrated base f9d80724,
tested source c326ef7b published/verified same draft PR395; no active markers.
Coordinator supplies independent original-finding closure and new Medium import
defect; no self-Pass or new full Review. Prior correction evidence below immutable.

## Execution Summary

Ready plan incorporates all three direct critique dispositions. Original
critique Revise retained. Only core/orchestrator source, two test files,
related documentation and issue-owned tracking artifacts are authorized.

## Completed Work

### P01: Bounded core and configured job

Added core `document_rescan.py` with SQL-only stable pages, per-attempt prior
pending recovery and explicit own-COMMIT witness. `SqlStore.save` sets that
witness immediately after COMMIT. Confirmed committed errors quarantine any
already-committed pending audit and force refresh, never rejection.
`_scan_stored(remove_bad=False)` records blocked bad verdict without deleting;
unsupported verdict is refused. Existing default/manual behavior retained.
SqlStore constructor closes partially opened connection on failure.
New orchestrator module requires explicit data/SQL/scanner and local synthetic
opt-in, emits report/continuation and exit0/1/2 with deterministic precedence.
No web, infra, retention or hold release source changed.

Initial targeted run after local test/format refinements: 34 tests OK, 14
explicit opt-in MSSQL skips (20 executed). Core mypy 120 files and orchestrator
mypy 12 files passed; changed-file Ruff passed. Actual subprocess CLI already
exercised incomplete page, terminal page and idempotent empty sweep.

Missing dependencies established with `python3 -m pip show`. Installed with
`python3 -m venv .venv && .venv/bin/python -m pip install --quiet -e
'src/core[dev,sql]' -e 'src/orchestrator[dev]' -e src/agents -e src/api`;
exit0. No uv, legacy path or private dataset used.

## Implementation-Time Plan and Detail Updates

None since the ready plan. PC-001 own-COMMIT witness, PC-002 exits/cursor and
PC-003 construction cleanup are part of the approved candidate dispositions.

### Compatibility refinement within P01-T01

Unsupported scanner verdict now raises RuntimeError rather than ValueError:
the legacy helper's existing ValueError removal catch must not claim an unknown
verdict removed a document. Added an assertion inside the existing owned test;
no extra test file or changed authority. Reran actual SQL, document regressions
and rebuilt/re-exercised the exact image afterward. No second critique.

## Validation Record

All commands below actually ran in this worktree, on constructed local fixtures.
`PYTHONPATH` selects shared tests only, never legacy code.

| Command / scope | Actual result |
| --- | --- |
| `(cd src/core && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)` | Final pass: lint, 67 formatted files, mypy120 source files |
| Same configured checks in src/orchestrator | Final pass: lint, 9 formatted files, mypy12 source files |
| `(cd src/orchestrator && PYTHONPATH=../core/tests ../../.venv/bin/python -m unittest discover -s tests -q)` | Final 28 tests passed, no skips; includes real SQLite subprocess command |
| `PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_document_rescan test_progress_event_capture test_change_provenance test_stock_reconciliation test_resident_decisions test_sensor_privacy test_sensor_backfill test_sensor_stock test_sensor_faults -q` | 277 run,201 passed,76 explicit backend/opt-in skips; expected injected-failure logs and existing sensor ResourceWarnings |
| `PYTHONPATH=src/core/tests:src/agents/tests:src/api/tests .venv/bin/python -m unittest test_document_controls test_documents test_progress_report_api -q` | 57 run,45 passed,12 existing opt-in skips |
| `PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_sqlstore test_sqlreads test_sqlqueues test_recovery -q` | 57 tests passed, no skips; generated local 60,000-case performance fixtures, no private data |
| Final `PYTHONPATH=src/core/tests:src/agents/tests:src/api/tests .venv/bin/python -m unittest test_document_rescan test_document_controls -q` | 48 run,31 passed,17 MSSQL opt-in skips; those 17 separately executed on actual SQL |
| Owned validation harness runs `ZF_DOCUMENT_RESCAN_MSSQL=1 ... python -m unittest test_document_rescan.MssqlRescan -q` | Final 17/17 passed in101.643s on actual loopback SQL Server, independent connections and UUID-owned databases |
| Actual MSSQL module invocations `--synthetic-local --limit 1`, `--after ZF-1 d0`, then cursor-free repeat | Exit2/0/0; clean1/2/0; three persisted success events, intact ledger/hold/bytes |
| `docker build -f src/orchestrator/Dockerfile -t zf-issue117-orchestrator:local src` | Final success; image sha256:26fa4bf5152291ba9f8f9ae9657ce20c79cc73fab79d993d2bd67d5fa6b4f9fd |
| `.venv/bin/python src/check-container.py orchestrator zf-issue117-orchestrator:local` | Actual Docker controls, five negative probes and plain/hardened startup PASS |
| Actual image module pages with --network=none, --read-only, --cap-drop=ALL, --security-opt=no-new-privileges, UID/GID10001 | Exit2/0/0, clean1/2/0, durable SQLite three events, intact ledger/hold/bytes; installed source hashes matched |
| `git diff --check`; `docker ps --format '{{.Names}}'` | Pass; no running containers |

SQL orchestration: session-local `files/validate_sql117.py` generated ephemeral
credentials in process memory, started exact container
`zf-issue117-sql-ba90bb56` bound only to127.0.0.1 (final port32782), verified
SELECT1 readiness, ran tests and real CLI, and in finally stopped/removed that
exact container. Each test dropped only its UUID-owned database. No idle SQL.
Image orchestration: session-local `files/validate_image117.py` ran existing
checker, compared installed hashes, and exercised real no-network hardened
commands against temporary synthetic fixture/state mounts. All temporary fixture
directories cleaned; one-shot --rm containers exited. Raw stdout logs stay in
the session workspace, not unrelated repository tracking.

Final installed hashes:

| Module | SHA256 |
| --- | --- |
| core.doc_controls | 87751334a290fcc941f2ad5b061f5a06f703f62485af6b434de0acdc32c04ce7 |
| core.document_rescan | 4495d4ae009fff107c4ce2eb8351b3c16a03807c4b16892e68a2d4e96cc6f7ee |
| core.sqlstore | b649272afb37f530a638ac442e751f9dc61d33a6ba4434ce0ee0b898b6f6e5c6 |
| orchestrator.document_rescan | 7edc1eec2dbe925f359fbfde2345889509003bc0aed62ad8c7ebbb2c652e1d90 |

Genuine early failures: first new-test run32 had one CLI test error because a
mock scanner name was not JSON serializable; corrected the test's explicit
synthetic label. Initial lint found formatting/import issues and mypy found
three test harness typing errors; configured formatting/import fixes and
proper Any-boundary inputs resolved them. Later 34-test run passed with14
MSSQL opt-in skips before additional semantic assertions. No production scanner,
Azure deployment, browser or human acceptance was executed or claimed.

## Pre-Review Reconciliation

Plan/detail markers complete and aligned; changes record contains actual
completion/commands/limits. Documentation updates the existing synthesis/index
and appends24 log lines without rewriting history. Shared source delta is only
non-deleting scan mode/verdict validation and SQL constructor/commit hook; no
resident/sensor/progress implementation was removed or rewritten.
No remaining engineering task or blocker. Follow-ups stay outside acceptance.
Ready for exactly one original Review; no outcome presumed.

## Blockers

None for bounded engineering. Real Defender, hosted schedule and human
retention/hold approvals remain operational gates, not inferred authority.

## Remaining Work

Authorized publication only in this task. RV-001/RV-002 corrections require
separate coordinator-authorized work; no production/test correction or second
Review is performed.

## Follow-Up Items

Canonical list: plan Follow-Up Items. Defender/Blob activation, hosted schedule
owner/cadence and DPO/Legal approvals are separate future work.

## Original Review and Parent Routing

Original Review:
.copilot-tracking/reviews/logs/2026-10-17/issue-117-document-rescan-scheduler-review.md.
Execution Complete, outcome Not accepted. RV-001 Medium: nested SQL recovery
can emit raw diagnostics; RV-002 Medium: malformed scanner result can escape
controlled report/CLI handling. Both were reproduced by the reviewer in memory;
these are actual new Review evidence, not parent test receipts. Observed pending
state remained unavailable and no failure success audit was committed.

Parent routed both to later rpi-implement, prioritized RV-001 then RV-002.
No closure verification, source/test correction or repeated Review. Research
Status cell was metadata-reconciled after its stale value was noted; no
research conclusion, original critique or original Review was rewritten.
Current plan/details/changes/state distinguish completed execution from blocked
acceptance. Documentation status is reconciled, not presented as defect repair.
Publication remains authorized, with adverse verdict plainly in the PR.

## Publication Receipt

Source/artifact commit `4763c0e6337d06846d9a9c46f7d9e0cf7470079f` created
with Conventional Commit, Refs #117 and required Copilot trailer. Fresh
`gh api user` supplied the privacy-safe repository-local author/committer
email; both commit identities were verified. Only the19 issue-owned files
were staged. No private credential or unrelated tracking was included.

Fresh `git ls-remote origin refs/heads/main` remained the authorized
`ebc8dab87ae9bd6a33380b85e86f38be5ed9f213` before publication.
`git push --set-upstream origin HEAD:refs/heads/feat/document-rescan-scheduler-117`
succeeded normally. `gh pr create --base main --head
feat/document-rescan-scheduler-117 --draft ... --body-file <session>/files/issue117-pr.md`
created https://github.com/jmservera/ama/pull/395. Draft deliberately preserves
Not accepted and the two separate corrections, not readiness to merge.

Actual `gh pr view395` verified Open/draft/main, expected branch and exact source
commit as head. `gh issue view117` verified Open. Local worktree was clean;
remote main unchanged; no running containers. Hosted checks had started and
were still running at this receipt, not declared passed. No merge, force-push,
rebase, issue action, additional Review or correction implementation.

This receipt/state/append-only-log follow-up commit changes evidence metadata
only; the reviewed production/test patch and installed source hashes are
unchanged. Final remote/head verification follows its normal push.

## Correction ONE authorization and opening state

2026-10-17 coordinator authorizes both original Medium findings in one coherent
implementation cycle, same worktree/branch/draft PR395. Start head552be52d,
clean; main fresh at authorized ebc8dab8. No other session/agent is active.
Read original findings in full, current source/tests/component guides and
mandatory knowledge context. P03 plan/details added before source edits.
First action: failing-first regressions within existing two owned test files,
then worker recovery ownership and closed scanner-result validation together.
Validation includes actual SQL, CLI/root logs, JSON/shared manual boundary,
existing guard regressions and rebuilt installed image.
Original Review SHA2564e57eccdcd7817590110afd90c889d1f3c87de5b0bb48ac0353777fb7b3a2ac9;
critique f788cc3d53a983f00493bf26eee2a1764696bcdfe155464576e6691bfb8beea8.
These remain untouched. Historical receipts above are not new correction runs.

## Correction ONE P03-T01: Failing-first reproduction and coherent correction

Actual 2026-10-17 execution, before production edits: selected five new/
strengthened tests across existing core/orchestrator files. Ran5, failures6,
errors3, command exit1. Full receipt `correction1-failing-first.log` in session
files. Includes original SQL recovery sentinel/traceback, malformed None
TypeError escaping manual JSON/SQLite/CLI, invalid container accepted as clean,
and consequent state assertions. Those are genuine pre-fix failures, not passes.

One production batch: SQL automatic recovery recognizes the active
`document_rescan` context so `_attempt` owns recovery before nested diagnostics;
all other contexts/COMMIT order unchanged. Shared scan-result validator checks
exact tuple/arity/string verdict/string detail before unpack or mutation at
upload/stored-scan boundaries. Closed verdict set; fixed RuntimeError text,
no coercion or echo of result/object. Worker contains explicit TypeError and
continues the selected page; CLI contains TypeError with fixed error marker.
Valid/manual bad verdict ValueError behavior and scanner exceptions remain
unchanged outside the explicit worker boundary.

New/strengthened tests cover the entire root log/CLI streams, real competing
SQL writer winner and pending audit prefix, None/arity/container/verdict/detail,
hostile object coercion, scanner TypeError, storage outage, continued page,
JSON/SQL manual upload/rescan refusal, bytes/hold retention/no deletion/no success.
Focused command `PYTHONPATH=src/core/tests:src/orchestrator/tests .venv/bin/python
-m unittest test_document_rescan test_document_rescan_job -q`: final46 run,
27 passed,19 explicit MSSQL skips in7.109s. No second Review performed.
P03-T01 complete; P03-T02 actual SQL/image/regression/publication active.

## Correction ONE P03-T02: Actual validation, 2026-10-18

The original loop receipts above remain historical. All results below are new
executions for the authorized correction, not a repeated Review. No additional
dependencies were installed. Production diff is four existing runtime files;
test ownership remains the same existing two files. Existing KB synthesis/index/
append-only log and component core/orchestrator guides updated, no web/API code.

| Actual command | New result |
| --- | --- |
| From `src/core`: `../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy` | Passed,67 formatted files/120 typed sources |
| Same configured commands from `src/orchestrator` | Passed,9 formatted files/12 typed sources |
| `PYTHONPATH=src/core/tests:src/orchestrator/tests .venv/bin/python -m unittest test_document_rescan test_document_rescan_job -q` | Final46 run,27 passed,19 MSSQL opt-in skips,8.171s; root DEBUG capture in conflict cases |
| From `src/orchestrator`: `PYTHONPATH=../core/tests ../../.venv/bin/python -m unittest discover -s tests -q` | 30 passed,10.682s; real SQLite subprocess commands plus actual-main fault injections |
| `PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_document_rescan test_progress_event_capture test_change_provenance test_stock_reconciliation test_resident_decisions test_sensor_privacy test_sensor_backfill test_sensor_stock test_sensor_faults -q` | 281 run,203 passed,78 existing opt-in/backend skips,56.360s |
| `PYTHONPATH=src/core/tests:src/agents/tests:src/api/tests .venv/bin/python -m unittest test_document_controls test_documents test_progress_report_api -q` | 57 run,45 passed,12 existing skips,115.454s |
| `PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_sqlstore test_sqlreads test_sqlqueues test_recovery -q` | 57 passed,91.430s; generated60,000-case fixtures, not private datasets |
| `.venv/bin/python /home/azureuser/.copilot/session-state/ba90bb56-8dbf-4c5f-8825-92041810af80/files/validate_sql117_correction1.py` | Owned loopback SQL responsive SELECT1;30/30 tests,135.363s; actual CLI/main cases below; finally stopped/removed exact container |
| `docker build -f src/orchestrator/Dockerfile -t zf-issue117-orchestrator:correction1 src` | Passed; final rebuild includes final scanner-contract docstring; no runtime edits afterward |
| `PYTHONPATH=src/core/tests .venv/bin/python /home/azureuser/.copilot/session-state/ba90bb56-8dbf-4c5f-8825-92041810af80/files/validate_image117_correction1.py` | Existing `src/check-container.py` hardening/startup/negative probes pass; installed hashes match;6 safe failures and real module success pages |

### Actual owned SQL selectors and CLI results

Harness uses ephemeral random password only in process environment; binds
127.0.0.1 on an assigned port, verifies SELECT1, enables existing opt-ins:
`ZF_DOCUMENT_RESCAN_MSSQL=1 ZF_CAPTURE_MSSQL=1 ZF_RESIDENT_MSSQL=1`, current
`ZF_SQL_*` driver configuration and `PYTHONPATH=src/core/tests`. Executes:

```bash
.venv/bin/python -m unittest \
  test_document_rescan.MssqlRescan \
  test_progress_event_capture.MssqlCapture.test_upload_outage_preserves_prior_audit_and_truthful_failures_after_reload \
  test_progress_event_capture.MssqlCapture.test_operational_rejection_preserves_original_error_and_no_success_on_recovery_failure \
  test_progress_event_capture.MssqlCapture.test_document_committed_acknowledgement_is_not_rejected_or_cleaned_up \
  test_progress_event_capture.MssqlCapture.test_sql_rollback_and_failed_recovery_preserve_original_prefix_and_retry \
  test_progress_event_capture.MssqlCapture.test_sql_postcommit_sync_failure_is_committed_once_second_connection_and_retry \
  test_resident_decisions.MssqlResidentControls.test_response_reassignment_faults_preserve_history_and_exactly_once_outcome \
  test_resident_decisions.MssqlResidentControls.test_concurrent_followup_writers_one_version_one_success_event \
  test_resident_decisions.MssqlResidentControls.test_followup_audit_insert_and_recovery_faults_never_replay_success \
  test_resident_decisions.MssqlResidentControls.test_followup_postcommit_sync_fault_is_truthful_and_not_replayed \
  test_resident_decisions.MssqlResidentControls.test_save_clears_scoped_dependencies_inside_outer_lock \
  test_resident_decisions.MssqlResidentControls.test_stock_race_rechecks_all_dependencies_and_clears_them_after_rollback -q
```

19 current worker methods include all17 original cases, plus malformed-result/
fair continuation and JSON/manual scanner contract. The other11 cover changed
shared recovery seams from merged102/resident88: original error/prefix, failed
audit INSERT/recovery, committed acknowledgement without false rejection/replay,
current writer identity/stock dependencies and concurrent exact-once outcomes.

Actual subprocess `python -m zava_forward.orchestrator.document_rescan
--synthetic-local --limit 1`, then `--after ZF-1 d0`, then a fresh sweep:
exit2/0/0, clean1/2/0, exactly3 success events. On a fresh pending record, actual
MSSQL `main()` with real store/transport plus injected scanner/recovery seams:
None, wrong arity, invalid list, unknown verdict, invalid detail, scanner
TypeError, scanner OSError, and competing-clean plus `_discard` recover-then-
OSError. All8 exit1, checked1/failed1/clean0/committed0, captured entire effective
root/CLI streams contain neither private sentinel nor traceback. Failed records
remain pending, no false success; final competitor's legitimate clean persists
once. Bytes/hold/ledger intact.

Exact container `zf-issue117-correction1-sql-ba90bb56` stopped/removed in finally.
Only UUID-owned test databases created/dropped by fixtures, including existing
progress/resident prefixes. No idle SQL remains. Session receipts:
`correction1-sql-run.log`, `correction1-sql-tests.log`,
`correction1-sql-cli.log`, `validate_sql117_correction1.py`.

### Final installed-image boundary

Image ID `sha256:fd51f7dc1ea25f7a025efdb580ed9b0268ba034b3a24873b13fc7f8a93e39d5f`.
Actual installed-source SHA256:

| Runtime module | SHA256 |
| --- | --- |
| core.doc_controls | e8a3da145cf670dd0200154fe60c077b24d4fd33d1bf3a43c9a22c700c6d2f8a |
| core.document_rescan | bbeadb721c20ecabbfda47ed14c63c21a3ca0f81e1c14aec801e8406fa1b1397 |
| core.sqlstore | 105da301e7cdc25ddeea260828bb00d0316ad696fe6691727aa591fe8832182b |
| orchestrator.document_rescan | 0d6c14b4619d5919717d6b7bfcad6746aca68d8bf39dac0dfd4c8d9086bb4741 |

UID/GID10001, read-only root, drop-all capabilities, NoNewPrivs, tmpfs, no
network and temporary synthetic SQLite/bytes only. Injected scanner results
None, wrong arity, invalid list, unknown and TypeError/OSError:6/6 exit1,
failed1/clean0, no raw private diagnostic/traceback, no audit success or pending
availability. Then unpatched actual installed module pages exit2/0/0,
clean1/2/0; exactly3 persisted success events and intact ledger/hold/bytes.
Exact one-shot job `zf-issue117-correction1-job-ba90bb56` removed; fixtures clean.
Receipts `correction1-image-build-final.log`, `correction1-image-run.log`.

### Failure/warning and authority accounting

Failing-first5 selected tests failed with6 assertion failures/3 errors, preserved
in `correction1-failing-first.log`, then fixed in one source cycle. Configured
static checks passed after formatter-only test layout adjustment. A tracking
patch partially applied only the details file, then remaining plan hunks were
applied explicitly; no code/validation failure was concealed. Existing injected
non-worker progress/SQL error logs include synthetic tracebacks, intentionally
unchanged outside the worker-owned context. Existing sensor ResourceWarnings
are still present. Backend skips are counted above, not claimed as passes;
all19 current worker MSSQL cases ran separately with opt-in.

Final immutable original Review/critique hashes still match intake values.
Original Review remains Complete / Not accepted; original critique Revise.
No second full Review or independent coordinator Pass. P03-T02 validation
complete, awaiting same-draft publication and exact clean remote verification.
Real Defender/Blob enablement, recurring service/cadence, retention policy/
owner approvals and hold/deletion authority remain unmet. Issue117 remains
partial. No private input, real communication, Azure/Graph/IAM/paid AI or service
activation, web changes, memory edits, merge, closure, rebase or force-push.

## Correction ONE P03-T02: Verified publication and implementation handoff

Actual 2026-10-18: fresh `gh api user`8036360/jmservera resolved before commit;
repository-local author and committer email8036360+jmservera@users.noreply.github.com
verified from the resulting commit. Conventional fix commit with Refs #117 and
required Copilot trailer. Normal push same authorized topic; no rewrite/merge.
Source/test/docs/artifact correction commit:
`9468800e85b645b783f439de4e72018b7ae2488e`.

`gh pr edit 395 --body-file` publishes exact original/correction evidence,
commands, failures/skips, SQL/image/source hashes and human/service gates.
Fresh `gh pr view 395`: Open, draft, base main, source head9468800e; `git
ls-remote` and local HEAD equal exact full source commit, worktree clean.
Main remains authorized ebc8dab87ae9bd6a33380b85e86f38be5ed9f213 at fresh checks.
Issue117 stays Open. Exact owned correction SQL/job inspection is empty.
Original Review/critique SHA256 remain byte-identical to intake values.

P03-T01/P03-T02 and P03 complete, no remaining active implementation markers.
This handoff metadata records observed publication; no runtime/test changes
follow the tested source commit. A normal metadata commit/push carries this
receipt; its final delivered head is recorded externally in PR395/final return
rather than inventing a self-referential commit hash. Original Review remains
Complete / Not accepted; targeted corrections are implemented/validated,
independent coordinator closure/acceptance not awarded. PR395 remains draft.
No second Review. Real Defender/Blob, recurring schedule and retention/owner/
legal hold authority gates remain unmet; issue117 is partial.

## Correction TWO authorization, integration and failing-first intake

2026-10-18: same original session/worktree/topic/PR395, clean exact starting
local/remote6a9fd3a4f763c48b5a5de65a3a9efd892731e7d8. Coordinator supplies
independent558e33f1 full source/seven-artifact assessment: Revise for new Medium
unconditional mssql_python import; original RV001/002 independently closed.
Correction TWO is LAST source cycle; no new full Review or self-Pass.

Explicitly authorized fetch/rebase onto origin/main
f9d807245e784ad2e6587741a73fc6563f8d2cd6 (merged396). Actual rebase completed
four own commits, one conflict only docs/reference/log.md; retained upstream
entries in order before issue117 appendices. No runtime/test conflict.
Post-rebase pre-fix head b0ebcb1f3cb5c7e702b3df676b680d452e007a04.
Exact runtime/test parity and upstream browser/source preservation checked below.
Remote remains expected6a9fd3a4 until explicitly leased publication.

First dependency-minimal discovery overlapped rebase and observed22 passes
while the issue test file was temporarily absent; this is invalid evidence,
not a pass claim. Repeated on stable completed rebase before source changes:
`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/orchestrator/src:src/core/tests
python3 -S -m unittest discover -s src/orchestrator/tests -v` ran23 entries,
22 passed/1 import error, exit1, exactly the supplied reproduction.
Actual `python3 -S -m zava_forward.orchestrator.document_rescan --help` also
failed exit1 before edits. Distinct session logs correction2-*-before*.log.
P04 plan/details/state persisted before substantive source correction.

## Correction TWO P04-T01: One bounded import correction

Added existing-file regression before production edits: actual `python -S`
help assertion failed with ModuleNotFoundError (one test, one failure).
Removed only module-level optional-driver import. After argument parsing and
explicit backend validation, the existing main try block imports the driver
exception type only for MSSQL, adding it to the typed database-error tuple.
SQLite exception handling retained; explicitly missing-module errors use the
same fixed error marker/exit1, not a silent fallback or backend replacement.
No worker/core scan/recovery, workflow, manifest, source/browser route or
optional dependency installation change.

Tests prove no-site process cannot find mssql_python, help succeeds, configured
SQLite normal page exit2 clean1, missing bytes exit1 failed1, explicitly selected
MSSQL without driver exit1 fixed marker. Available-driver Error before store
return also sanitized; type-check first caught the test Error constructor
missing required ddbc_error, corrected to actual two-string signature. That
was a fixture refinement within this one source cycle, not a third cycle.

Actual driverless discovery now32 run/31 pass/one optional-driver skip.
Installed-driver discovery32/32. Configured orchestrator static checks pass.
P04-T01 complete; P04-T02 integrated/image/publication validation active.

## Correction TWO P04-T02: Current integration and fresh validation

Current base f9d807245e784ad2e6587741a73fc6563f8d2cd6; original ebc8dab8 and
correction ONE source9468800e/head6a9fd3a4 above remain historical evidence.
No runtime conflict occurred during authorized rebase. Exact-byte proof:
every issue117 runtime/test from old6a9fd3a4 equals integrated file except
orchestrator/document_rescan.py and its existing test file (the authorized
correction). Every merged396 source/test/browser/pyproject file equals upstream
f9d80724. All upstream coordinator routes retained unchanged, no web edit.
`docs/reference/log.md` starts with the exact f9d80724 byte-prefix; all prior
issue append entries retained afterward. Original Review/critique equal original
6a9fd3a4 blobs byte-for-byte; the entire correction ONE changes section also
matches original bytes. No second full Review or self-Pass.

| Actual new command | Result |
| --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/orchestrator/src:src/core/tests python3 -S -m unittest discover -s src/orchestrator/tests -v` | Before23 entries/22 pass/1 import error exit1; final32 run/31 pass/one optional-driver skip,6.920s |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/orchestrator/src python3 -S -m zava_forward.orchestrator.document_rescan --help` | Before exit1 import error; final exit0 usage output |
| `PYTHONPATH=src/core/tests:src/orchestrator/tests .venv/bin/python -m unittest test_document_rescan_job.RescanCommand.test_driverless_help_sqlite_success_failure_and_missing_mssql_driver -q` | Failing-first one test/one failure on actual no-site module help; final included in both discoveries |
| From `src/core`: `../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy` | Passed,69 formatted/122 typed files including merged coordinator |
| From `src/orchestrator`: same configured static commands | Passed,9 formatted/12 typed; formatter used on two owned files |
| From `src/orchestrator`: `PYTHONPATH=../core/tests ../../.venv/bin/python -m unittest discover -s tests -q` | Installed-driver32/32 passed,9.453s; no new dependency installation |
| `PYTHONPATH=src/core/tests:src/agents/tests:src/api/tests .venv/bin/python -m unittest test_document_rescan test_progress_event_capture test_change_provenance test_resident_decisions test_sensor_privacy test_coordinator test_coordinator_api -q` | 273 run/186 passed/87 explicit opt-in backend/browser skips,53.343s; expected injected rollback logs |
| `.venv/bin/python /home/azureuser/.copilot/session-state/ba90bb56-8dbf-4c5f-8825-92041810af80/files/validate_sql117_correction2.py` | Actual loopback SQL responsive SELECT1,20/20 passed96.097s; actual native driver-error and real CLI below; finally exact SQL stopped/removed |
| `docker build -f src/orchestrator/Dockerfile -t zf-issue117-orchestrator:correction2 src` | Existing image/context build passed |
| `PYTHONPATH=src/core/tests .venv/bin/python /home/azureuser/.copilot/session-state/ba90bb56-8dbf-4c5f-8825-92041810af80/files/validate_image117_correction2.py` | Existing hardening/check-container probes, installed help/source hashes, six safe failures and real module pages passed |

No-site subprocess regression explicitly asserts
`importlib.util.find_spec('mssql_python') is None`. Same process mode verifies
module help exit0, configured SQLite page exit2/clean1, missing bytes exit1/
failed1, and selected MSSQL missing-driver exit1/fixed marker. No raw diagnostics/
tracebacks, silent fallback or backend replacement. CI workflow/install command
unchanged. Driver-error regression uses actual installed driver's Error class
with both required constructor strings; not a fabricated generic Exception.

### Actual SQL and installed-image boundary

Owned container `zf-issue117-correction2-sql-ba90bb56`, loopback-only ephemeral
port/credentials, readiness SELECT1. `ZF_DOCUMENT_RESCAN_MSSQL=1` plus existing
ephemeral ZF_SQL settings, actual command:

```bash
PYTHONPATH=src/core/tests:src/orchestrator/tests .venv/bin/python -m unittest \
  test_document_rescan.MssqlRescan \
  test_document_rescan_job.RescanCommand.test_selected_mssql_driver_error_is_sanitized_before_store_return -q
```

20/20: all19 worker guards including prior17, malformed contract, full root
redaction, original conflict/prior prefix/winner state, own COMMIT and post-
COMMIT no false rejection/replay. Additional actual-main factory seam opens a
real native connection and executes SELECT against nonexistent synthetic table
SYN_PRIVATE_MISSING_DRIVER_TABLE_117. The real native driver Error is contained:
exit1/fixed DOCUMENT_RESCAN_ERROR, empty stdout, no sentinel/traceback.
Actual installed subprocess MSSQL module pages exit2/0/0 clean1/2/0; exactly3
success events, intact hold/bytes/ledger. Temporary UUID databases dropped,
exact owned container stopped/removed in finally. No idle SQL.
Distinct receipts correction2-sql-run.log/tests.log/cli.log and harness retained.
Prior correction ONE30 actual SQL receipts are historical, not claimed rerun.

Rebuilt image ID
`sha256:5695460a9190c19cc921383dc3fe2bcc22fee37e9376894441495e3480388e50`.
Installed source hashes match:

| Runtime | SHA256 |
| --- | --- |
| core.doc_controls | e8a3da145cf670dd0200154fe60c077b24d4fd33d1bf3a43c9a22c700c6d2f8a |
| core.document_rescan | bbeadb721c20ecabbfda47ed14c63c21a3ca0f81e1c14aec801e8406fa1b1397 |
| core.sqlstore | 105da301e7cdc25ddeea260828bb00d0316ad696fe6691727aa591fe8832182b |
| orchestrator.document_rescan | 2e7baf504ce3d540bf5e1017f2ec9425bc31554fee5b44e571f8898fd8e71d48 |

Existing checker verifies Docker controls/negative probes/plain and hardened
startup. UID10001/read-only/drop-all/NoNewPrivs/no-network actual installed
module help succeeds; six injected malformed/unknown/type/outage scans exit1
failed1/clean0 with safe diagnostics, no success/pending availability. Actual
module pages exit2/0/0,clean1/2/0 and three exact-once events, intact held bytes
and ledger. Exact one-shot image job removed, temporary fixtures cleaned.
No runtime/test edits after this source boundary.

### Accounting and remaining publication boundary

Only genuine source-validation refinement was the required second constructor
argument for the installed driver's Error in the new test, identified by mypy
and fixed within this authorized coherent cycle. Initial concurrent rebase/
discovery receipt was rejected and rerun stably as recorded above. No failure
or skip is disguised as a pass. Existing injected non-worker rollback logs are
not claimed eliminated. No dependency install, paid service, private input,
Azure/Graph/IAM, approval, real communication, memory or web change.

P04-T01 complete; P04-T02 validation complete, same draft PR395 publication
pending exact remote6a9fd3a4 lease and fresh identity/main checks.
Independent original-finding closure/all-seven-artifact Pass is supplied by
coordinator session558e33f1; new final correction not self-accepted. No new full
Review. Any residual defect after this LAST source cycle is human-blocked.
Real Defender, hosted recurring scheduler and retention/owner/hold authority
remain unmet; no merge or issue closure authorized.

## Correction TWO P04-T02: Verified exact-lease publication and final handoff

2026-10-18 fresh gh identity8036360/jmservera supplies privacy-safe local author/
committer8036360+jmservera@users.noreply.github.com. Conventional fix commit
Refs #117 and required Copilot trailer verified. Own-topic authorized rebase/
correction published with the exact command:

```bash
git push --force-with-lease=refs/heads/feat/document-rescan-scheduler-117:6a9fd3a4f763c48b5a5de65a3a9efd892731e7d8 \
  origin HEAD:refs/heads/feat/document-rescan-scheduler-117
```

Expected old remote verified immediately before publication; no unexpected
advancement. Fresh main stayed authorized f9d807245e784ad2e6587741a73fc6563f8d2cd6.
Tested integrated source commit c326ef7b7a2b9f84831d282fd007127821755afa
equals actual local/remote/PR395 head after push; worktree clean.
`gh pr edit 395 --body-file` publishes current correction TWO first, current
base/source/parity/driverless/nativeSQL/image commands and honest failures/skips,
then labelled historical original/correction ONE sections.
PR remains Open/draft/main; issue117 Open; actual merge-base equals f9d80724.
No main push/rewrite, merge, closure or new authority.

P04-T01/P04-T02 and P04 complete. No active implementation markers remain.
Current plan/details/state reconciled; these four metadata files alone follow
the tested source commit. Their normal final metadata commit/push does not
change runtime/tests; final delivered head recorded externally in PR/final
return to avoid self-referential hashes. Final source/patch parity and immutable
original/correction ONE evidence receipts correction2-integration-parity.log.
Exact owned correction TWO SQL and job absent after actual stop/removal.
No third source cycle. Coordinator independently owns final acceptance;
any remaining defect is a human blocker. All real service/approval gates remain
unmet, draft retained. Original Review Complete / Not accepted and critique
Revise remain byte-exact; coordinator-supplied original-finding closure does not
rewrite them or award final correction acceptance.
