<!-- markdownlint-disable-file -->
# Changes: Assessment reconciliation controls #84

## Task and Scope

Task 84, slug assessment-reconciliation-controls-84, 2026-10-17. Automatic
ordered lifecycle explicitly requested. Implementation scope P01/P02; P03
Review/publication remain parent-owned. Canonical plan/details/research share
this slug/date. No production change occurred during Research/Plan.

## Phase Execution

| Order | Phase | Actual execution evidence |
| --- | --- | --- |
| 1 | Research | Started 17:07 UTC; exact gh issue first, named requirement/module reads, wider/deeper/contrarian complete. 47 core baseline and 18 API/ranking baseline (1 browser skip). Revoked-role and failed-save tiny SQL probes reproduced root gaps before plan. |
| 2 | Plan | Entered after research readiness; one independent final-candidate critique Complete / Revise, PC-001..003 directly resolved. Plan/details Ready; no repeated critique. |
| 3 | Implement | Entered after ready plan; fail-before run at 17:17 UTC precedes production edits. P01/P02 complete; all evidence reconciled 17:28 UTC. |
| 4 | Review | One independent rpi-review executed after reconciliation. Complete / Not accepted: RV-001 High blocks acceptance; no correction or repeat. |

## Baseline and Tooling

Initial python3 focused discovery failed ModuleNotFoundError zava_forward.
Created task-owned .venv, installed only declared editable src/core[dev],
src/agents and src/api[dev]. No dependency manifest change. Core focused baseline
passed 47 tests in 9.155s. Correct API component command from src/api:
PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest
test_stock_reconciliation_api test_ranking_policy -q: 18 tests, OK, 1 explicit
browser skip. Initial wrong root/component import attempts failed and are not
passing evidence. Existing rule-evaluation logs disclose unloaded law store;
no legal evaluation claim.

Docker 29.9.0 works; existing local SQL Server 2022 image present, no running
containers observed. No image pull, cloud call, private stock or real map read.

## P01-T01: Fail-before Regression

Before production edits, command
PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_stock_reconciliation -q
ran 24 tests, FAILED (14 failures, 5 errors). Existing methods retained; 6 new
methods added. Failure oracles: revoked role/name/OID/deleted staff not denied,
pre-save authority not revalidated, failed design write success audit retained,
transactional audit error later flushed a success event, missing decision_scope.
Raw local transcript: session files/issue84-red.log (not private data).
These are actual red results, not tests retrospectively run against old code.
New class helpers are not executable-distribution files.

## P01-T02: Root Fix

Applied bounded stock.decision_scope reusing change_provenance._actor, existing
lock/_discard and scoped writer-lock validator. Removed duplicate cached actor
check in stock routes and reused the same scope for technical actions. Changed
only one SQL save validation call; generic lock/_finish/other domains unchanged.
SQL exceptions rethrow, recovery errors explicitly log and annotate original
failure; no rollback claim for uncertain recovery/postcommit acknowledgement.
All four issue mechanisms and ranking policy remain unchanged.

## P02: Validation and Documentation

Complete. Full core `cd src/core && ../../.venv/bin/python -m unittest
discover -s tests -q`: 631 tests in 274.943s, OK, one existing opt-in
resident-browser skip. Shared seam/import escalation beyond focused tests
was justified by the implementation-introduced fresh-import cycle.

### Executed focused validation

* Core red: 24 tests, 14 failures/5 errors before production edits, as above.
* Initial green: stock/sign-off 53 tests passed; first lint found B023 closure
  binding in new test; bound the loop variable explicitly, then lint passed.
* Final core scoped lint: `cd src/core && ../../.venv/bin/ruff check . &&
  ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy`: all pass,
  57 formatted files and 110 source files type-checked.
* Core focused plus SQL read/write:
  `PYTHONPATH=tests ../../.venv/bin/python -m unittest test_stock_reconciliation
  test_finance_signoffs test_sqlstore test_sqlreads -q`: 88 tests passed.
  Existing SQL scale tests generate their own constructed 60,000-row temporary
  fixtures; no private stock or real map dataset read.
* Independent safety/building:
  `PYTHONPATH=tests ../../.venv/bin/python -m unittest test_hazard_referral
  test_buildings -q`: 27 tests passed.
* API static: `cd src/api && ../../.venv/bin/ruff check . &&
  ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy`: pass,
  19 formatted files and 50 source files type-checked.
* API exact HTTP/ranking/portability/role/workflow:
  `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m
  unittest test_stock_reconciliation_api test_ranking_policy
  test_mssqlstore.SharedSqlIsPortableTests test_role_matrix test_mvp
  test_workflows -q`: 72 tests passed, one opt-in browser skip.
* Separate actual browser:
  `ZF_STOCK_BROWSER=1 PYTHONPATH=tests:../core/tests:../agents/tests
  ../../.venv/bin/python -m unittest
  test_stock_reconciliation_api.StockApi.test_rendered_comparison_and_case_switch
  -q`: one Chromium test passed. Both values, metadata, query owner,
  Unknown support, keyboard/heading and separate-case navigation verified.
  No web files changed; no fresh web-guideline/UI conformance review claimed.
* Relative links: all 345 local link targets in four touched guides/index/
  synthesis exist; previous knowledge-log byte prefix exact. `git diff --check`
  passes. No memory/original/regulatory snapshot change.

### Actual local SQL Server parity

Existing cached SQL Server 2022 image, `--pull never`, unique task-owned
container `zf-issue84-sql-a1251cde`, random loopback-only port, ephemeral generated
credentials retained only in process memory/environment. Only constructed test
database, no cloud. Actual driver `SELECT 1` returned `(1,)`.

Command from src/api with existing opt-in localhost ZF_SQL_* settings:
`PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest
test_mssqlstore.MssqlStockDecisions -v`.

Eight tests passed in 7.887s, zero skips:

* test_four_human_signoffs_and_only_affected_reassessment
* test_sql_authority_rechecked_inside_writer_transaction
* test_sql_case_write_failure_restores_decision
* test_sql_current_actor_denial_for_all_decisions
* test_sql_decision_scope_restored_on_every_exit
* test_sql_failed_decisions_do_not_commit_or_flush_success_audit
* test_sql_transactional_audit_failure_restores_decision
* test_withdraw_unblocks_all_signoffs_without_editing_history

Reused canonical constructed core methods, not duplicated semantics. Explicit
case/audit failure checks compare durable case body/rowversion/sequence, ledger/
head, reopen and no later success-audit flush. Authority-race test independently
changes staff through second connection before writer validation, without
changing the case sequence. Does not prove behavior against arbitrary external
edits outside the shared writer-lock protocol.

First attempted fresh driver import exposed an implementation-introduced
stock/projection/change_provenance import cycle hidden by fixture import order.
Fixed with lazy helper imports and added fresh-process consumer-import tests.
Second attempt reached SQL startup before SA initialization, giving login failure.
Third bounded connection-ready attempt verified ephemeral handoff equality
without disclosing its value, then connected and passed actual changed-path
tests. All three owned containers were stopped/removed by exact-name cleanup;
final `docker ps --filter name=zf-issue84-sql-a1251cde` empty.

### Documentation and criterion traceability

Core/API guides, existing UX synthesis/index and append-only log updated.
Criterion 1: original both-source/owner persistence + HTTP and actual browser.
Criterion 2: four distinct actor/version/history assertions and SQL Server.
Criterion 3: exact affected set plus untouched assessment/coordination/sibling
and reopened histories, including SQL Server.
Criterion 4: unchanged tri-state table, independent safety/wait ordering,
rank-policy/API tests, SQL ordering and idempotent derived-data upgrade.
No new source selection, competence record, human approval or ranking policy.

## Amendments and Divergences

PC-001..003 directly incorporated before implementation. No user-owned policy
change or significant divergence. Store/SqlStore scoped integration overlaps
potential #90 shared-file edits only; procurement and #381 infra/package stay
untouched. JSON separate-file crash atomicity remains a disclosed limitation.
Local implementation amendments: eight new core test methods total (budget ten),
one new HTTP method (budget two), one opt-in SQL parity class. No test removals.
Two existing explicit reopen expressions now use the same canonical reopen
helper so SQLite and SQL Server run the same assertions. The fresh-import fix
is directly coupled to this implementation, not unrelated cleanup.

## Review Handoff

One Review executed, outcome Not accepted. P01/P02 markers/details/commands/
limitations reconciled; their execution does not establish successful delivery.
P03 visibility publication pending; no full-plan/engineering completion claim.
No human competence/delegation, source authority, rank-policy
approval, live/Azure/model or full BRD AC-065 acceptance inferred.

## Review Outcome and Concrete Stop

RV-001 High / blocker independently reproduces early/persistent recovery-read
failure leaving pending success audit for `_finish`, or replacing the original
save exception. The existing test calls real `_discard` successfully before
raising, so its passing result does not cover this failure. PC-002 is not fully
resolved in implementation. Four original mechanisms/current authority remain
separately evidenced. Review artifact:
.copilot-tracking/reviews/logs/2026-10-17/assessment-reconciliation-controls-84-review.md.

No source fix, second critique/Review or child loop after this outcome.
Current guides/synthesis/index and appended log explicitly mark Not accepted
so normal-recovery results cannot masquerade as acceptance. Under the caller's
publication direction, commit evidence and publish only a clearly incomplete
draft Refs #84 PR, then stop. RV-001 requires a later explicitly authorized
implementation, not silent deferral as an accepted residual.
