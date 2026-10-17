<!-- markdownlint-disable-file -->
# RPI Changes: Bounded pending-document rescans

## Metadata

Task ID 117; implementation date 2026-10-17; full plan.
Plan: .copilot-tracking/plans/2026-10-17/issue-117-document-rescan-scheduler-plan.md.
Details: .copilot-tracking/details/2026-10-17/issue-117-document-rescan-scheduler-phase-details.md.

## Execution Status

Complete full-plan implementation: P01/P01-T01/P01-T02/P02/P02-T01/P02-T02.
No remaining active-plan markers. One original Review executed Complete /
outcome Not accepted, two Medium findings routed separately; not a coordinator
acceptance claim.

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
