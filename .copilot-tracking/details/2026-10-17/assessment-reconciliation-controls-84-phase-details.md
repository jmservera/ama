<!-- markdownlint-disable-file -->
# RPI Phase Details: Assessment reconciliation controls #84

## Metadata

* Task ID: 84
* Task slug: assessment-reconciliation-controls-84
* Date: 2026-10-17
* Related plan: .copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md
* Research: .copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Fail-before evidence and narrow root fix | Complete: red/green and scoped root fix |
| P02 | Focused validation and current documentation | Complete: core/API, browser, SQL Server, static/docs |
| P03 | One Review, commit/push/PR | Review Complete / Not accepted, RV-001 blocker; incomplete visibility publication pending |

<!-- rpi:phase id=P01 -->
## P01: Focused regression and implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Establish fail-before regression evidence

Research C5/C6 independently reproduced stale authority and leaked success audit.
Extend existing tiny constructed core fixture, not private stock. Cover current
SQL actor role/deletion/OID before action and changed authority between action
and save, all three entry points (comparison, terminal event, technical action).
Inject case-write and audit-write failures and compare case/audit/sequence before
and after reopen. Confirm a later legitimate operation cannot flush the failed
audit. Add same-case/sibling isolation and retained-history/version assertions
inside existing tests where sufficient. No removals; maximum 10 core methods.
Explicit PC-002 lifecycle matrix: success, initial actor rejection, body error,
save failure, synthetic BaseException precommit interruption. Check prior/absent
context restoration, original exception identity even if recovery reports a
fault, and a later unrelated save/legitimate decision without stale validation
or delayed success audit. Known precommit failure is not a lost-commit-
acknowledgement test; do not claim rollback for an unknown outcome.

Completion evidence: exact red command and assertion failures recorded before
production edits, then green focused regression. Existing base 47 core tests
and 18 HTTP/ranking tests (one browser skip) already passed.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Scope reliable current-authority SQL decisions

Implement in existing stock.py a narrow stock/technical decision context reusing
change_provenance._actor for fresh registered identity, not copied auth logic.
Use the current lock and SqlStore.save writer transaction; register only this
scope's actor for revalidation and discard failed pending state/audit via
existing _discard. Always restore/clear context. Minimal Store stock-action and
SignoffMixin entry changes; surgical SQL save validation hook only.

Keep all role mappings, query rules, stock authority Unknown, deterministic
policy and affected-only sign-off behavior unchanged. SQL exceptions must
propagate; no success-shaped fallback. No generic transaction framework/lock
rewrite. JSON retains its documented separate-file durability boundary.

Completion evidence: current-role denial and failed commit consistency pass
alongside existing sign-off/hazard/query race tests.
Implementation completion: eight new core methods (within ten), one HTTP
method (within two), one SQL parity class. Fresh-process import regression
guards a directly coupled lazy-import correction. No test or policy removed.

<!-- rpi:phase id=P02 -->
## P02: Validate and record exact boundaries

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute focused and project checks

Core command from src/core:
PYTHONPATH=tests ../../.venv/bin/python -m unittest test_stock_reconciliation test_finance_signoffs -q.
API command from src/api:
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_stock_reconciliation_api test_ranking_policy -q.
Run relevant existing hazard/building and SQL tests, scoped project lint/format
and mypy. Tests stay outside distributions under core/tests.

Existing cached mcr.microsoft.com/mssql/server:2022-latest and working Docker
make local parity feasible. Use task-owned container and random loopback host
port, only constructed fixture database; follow existing ZF_SQL_* opt-in guide.
No real-cloud/Entra/model/stock-source authority claims. Clean owned container.
No web edits planned, so no new changed-interaction browser requirement.
Actual completion: 631 core tests pass (one existing opt-in resident-browser
skip), 72 targeted API tests pass (one opt-in stock-browser skip), separate
stock Chromium comparison/navigation test passes. Eight actual local SQL Server
tests pass, no skips. Core/API Ruff, format and mypy pass; links/log and diff
clean. Full commands, initial failures/successful retry, counts and exact
owned-container cleanup are recorded in the changes artifact.
PC-003 allocates exactly one MssqlStockDecisions opt-in class in the existing
API parity module, selecting canonical core fixture tests rather than copying
semantics. Run successes for comparison/disposition/technical actions, fresh
actor denial, independent second-connection pre-save authority change without
case-sequence bump, case/audit transactional failures and reopen/no-later-flush.
Use test_mssqlstore.MssqlStockDecisions with existing opt-in settings. Report
actual selected test names/counts or exact Not run/Blocked; generic SQL tests
do not prove this changed path.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update current component/synthesis evidence

Core/API READMEs describe exact current authority, rollback and preserved four
criteria. If synthesis materially changes, update existing UX synthesis/index
and append only to log; never memory/original/regulatory snapshots.
Changes artifact owns actual commands/results and phase execution timestamps.
Complete: component guides, existing UX synthesis, index and appended log
updated; 345 relative targets exist, old append-log prefix byte-identical.

<!-- rpi:phase id=P03 -->
## P03: One Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: One post-implementation RPI Review

One post-implementation review evaluates plan, current diff, red/green evidence,
all four criteria, authority and durable failure semantics. Route findings to
future work only when outside exact engineering acceptance. A failed exact
criterion, fresh-authority denial or durable audit/rollback check is a blocker;
do not defer it as accepted residual work or claim successful completion.
Stop incomplete with clear outcome (any visibility PR labelled incomplete)
rather than starting a second Review/implementation loop. Required human sign-off stays
unapproved; engineering proof is not operational acceptance.
Actual outcome: one independent Review Complete / Not accepted. RV-001 High
reproduces failed-audit leakage/original-error replacement on early/persistent
discard-read failure. The implemented recovery-fault oracle was insufficient.
No correction, repeated Review or nested delivery. Execution evidence remains
recorded but engineering acceptance is blocked.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Privacy-safe commit, push and main PR

Use gh api user; repository-local id+login privacy-safe email for author and
committer, required Copilot trailer. Commit all dated phase artifacts and
intended code/docs. Push requested branch normally; open independent main PR
Refs #84. Do not close #84, merge, rebase, force push or run nested delivery.
Record publication state and stop at final publication under explicit user
direction; CI may continue and owner retains merge/human acceptance.
