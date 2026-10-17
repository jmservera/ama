<!-- markdownlint-disable-file -->
# Changes: Assessment reconciliation controls #84

## Authorized main integration (2026-10-17)

Coordinator explicitly authorized rebase and topic-only `--force-with-lease`
for this run-owned branch, superseding the earlier no-rebase boundary only
for this integration. Initial clean local and REST PR #382 head:
95b7145af89ab751cd992423eb90cf8e0db47185, open draft targeting main.
`git fetch origin main` verified exact requested base
bab4bf3a2ac9ec030d78d27063d1390f800c5c7c; old merge base
adedf1f232e567d3a22a623d9c871513fa6b7cdc. Coordinator reports its independent
review found no significant issues pending this evidence summary; this is
supplied review context, not a newly executed independent review.

### Operation and conflict resolution

`git rebase --empty=drop --reapply-cherry-picks origin/main` replayed all four
owned commits. Only conflict: docs/reference/log.md in the initial commit.
Retained exact complete upstream prefix, including both #360 normal-Docker
publication-blocker and #381 integration entries, then appended all original
#84 entries. Removed only conflict markers and added the separating blank line.
`git add docs/reference/log.md`, staged whitespace check and
`GIT_EDITOR=true git rebase --continue` succeeded. No source conflict or source
edit. Index auto-merged, preserving every unrelated upstream table row exactly,
including infrastructure publication limits, alongside current #84 routing.

Rebased source/evidence sequence:
2e45b5e -> c089188, a15c7a2 -> 6440562, b6122fb -> 52f8481,
95b7145 -> c0853c5. The final integration-record commit is documentation/state
only; its exact pushed head is recorded on PR #382 and in the delivery result.
No repeated full RPI, correction cycle or independent verification was needed.

### Integration validation

* Captured old `git diff --binary adedf1f..95b7145 --` all seven owned
  production/test files before rebase; compared byte-for-byte to
  `git diff --binary bab4bf3..HEAD --` the same paths after rebase. Equal,
  SHA256 `c825ab718b578701344b912a5344512061f46db92dcf23257c864e694d631264`.
  All seven complete file SHA256 values also match. Production patch and
  fresh-staff/rollback/early-persistent fault test bytes are unchanged.
* `git range-diff adedf1f..95b7145 bab4bf3..HEAD -- src/core/src
  src/core/tests src/api/tests` marks both source commits equal. Upstream
  infra/tools have no branch diff. Original RPI artifacts, original Review
  plus correction disposition and correction verification are byte-identical
  to the pre-integration head; existing independent source fingerprints apply.
* Before this new append, log bytes equal exact bab4bf3 log plus exact old
  branch-owned suffix; every unrelated upstream index table row retained.
  358 relative documentation/artifact targets exist; lifecycle JSON parses.
  `git diff --check origin/main...HEAD` passes. Rebase finished clean.
* Minimal integration regression from repository root:
  `PYTHONPATH=src/core/tests .venv/bin/python -m unittest
  test_stock_reconciliation.StockReconciliation.test_sql_early_and_persistent_recovery_reads_cannot_flush_failed_work
  test_stock_reconciliation.StockReconciliation.test_sql_transaction_refusal_keeps_original_error_when_reload_fails -v`:
  two methods pass in 0.610s, including six wrapper/fault and two transaction
  refusal subcases. No skips.
* No source change/conflict or changed dependencies, so broad core/API,
  lint/type and actual SQL Server suites were not repeated. Prior correction
  ONE evidence remains historical: 102 core, 69 shared-cleanup, 72 API
  (one browser skip), ten actual local SQL Server and static checks pass;
  independent bounded verification closes RV-001. No new live-platform,
  browser/WCAG, private publication or human/source-policy acceptance claim.

Privacy-safe authenticated author/committer and required Copilot trailer for
the integration-record commit. Publication uses only the named topic branch
and exact expected old remote SHA in `--force-with-lease`; no unconditional
force or main push. Existing PR remains draft/main, no merge or issue closure.
Remote operation failures must be reported, never counted as successful.
Final source parity/clean state and remote head are verified at publication.

## Correction ONE: Explicitly Authorized RV-001 Continuation

2026-10-17, same #84 / PR #382, clean requested topic at a15c7a2. Coordinator
explicitly authorizes root correction before merge, not a repeated RPI or
permission deferral. Original Review's two actual negative probe observations
read: one early recovery SELECT failure leaks technical_design_change audit;
persistent SELECT failure replaces original save error and retains pending
success. Prior test discarded successfully before raising and was insufficient.

P04 correction source and validation complete: real early/persistent SELECT
regressions precede source edits; canonical discard disarmed before fallible
reload with cache restoration/retry. Original Review retained byte-for-byte
with appended disposition; bounded independent verification closes RV-001.
No unrelated source, private data, policy, human authority or infrastructure
change. No merge/rebase/force push; normal same-branch final push.

### P04-T01: Actual red before correction source edit

`PYTHONPATH=src/core/tests .venv/bin/python -m unittest
test_stock_reconciliation.StockReconciliation.test_sql_early_and_persistent_recovery_reads_cannot_flush_failed_work -v`
failed all six subcases (technical/comparison/terminal x one-shot/persistent).
Actual connection wrapper fails the first real recovery case SELECT, not an
error after successful discard. One-shot fails pending/audit integrity;
persistent fails original exception identity. Transcript retained in session
files/issue84-correction-one-red.log. Canonical alias added to existing opt-in
MssqlStockDecisions, no duplicated SQL semantics.

### P04-T02: Canonical cleanup ordering

`SqlStore._discard` now snapshots touched IDs then clears staged success audit,
touched writes and safety/resident/stock validation state before any DB read.
Known committed case/recommendation/shared-document snapshots are restored
in memory first; `_seq=-1` forces next operation to reload if recovery cannot
finish. Existing reload/discard, stock decision logging/error propagation and
outer lock release mechanics are reused; no generic lock exception swallowing,
new service/schema or role/policy change. A failed reload remains visibly
uncertain, while outer cleanup has no failed write/event to flush.

Additional direct root-path probe: actual transaction GateError/ConflictError
was masked by save's eager discard when reload failed before the decision
scope saw the original error. New refusal regression failed both subcases
before that source correction (session issue84-correction-one-refusal-red.log).
For active stock_decision only, rollback now rethrows to the existing owning
decision scope for discard/logging. Other domains retain their save behavior.

### P04-T03: Actual correction validation

* Core focused: from src/core, `PYTHONPATH=tests ../../.venv/bin/python -m
  unittest test_stock_reconciliation test_finance_signoffs test_sqlstore
  test_hazard_referral test_buildings -q`: 102 tests, OK, no skips.
* Canonical discard consumers: `PYTHONPATH=tests ../../.venv/bin/python -m
  unittest test_bulk_edits test_change_provenance test_form_staging -q`:
  69 tests, OK, no skips.
* API: existing comparison/ranking/SQL portability/role/workflow command:
  72 tests, OK, one existing opt-in stock browser skip. No web changes or new
  browser/conformance claim; previous actual rendered evidence remains history.
* Core and API `ruff check .`, `ruff format --check .`, `mypy` pass.
  New test closure-binding lint errors were corrected explicitly, no exemptions.
* Actual SQL Server: existing cached 2022 image, `--pull never`, task-owned
  `zf-issue84-correction-one-a1251cde`, ephemeral secret only in process/container
  environment, random loopback-only host port. Driver SELECT 1 responsive.
  `test_mssqlstore.MssqlStockDecisions -v`: ten tests in 15.925s, OK, no skips,
  including both new early/persistent and transactional refusal regressions.
  Exact owned container stopped/removed; concurrent #90 container not touched.
* Red/green compare actual durable case/history/rowversion/seq, audit/head,
  empty pending/touched state, context/lock depth and cross-thread availability,
  unchanged cached case, persistent read retry failure, normal next operation/
  plain save and reopen. No delayed failed success event or write.
* No full RPI, new critique or broad suite escalation. Original four criteria/
  current authority remain exercised by existing focused suites.

### P04-T03: Bounded independent closure

One explicitly requested bounded verification, not full RPI or another full-task
Review, returned RV-001 Closed. Artifact:
.copilot-tracking/reviews/logs/2026-10-17/assessment-reconciliation-controls-84-correction-one-verification.md.
Independent run: 91 focused tests, zero skips, plus constructed OSError and
GateError persistent recovery SELECT/snapshot probes. These check restored
recommendations/shared state and no delayed failed writes/audit, not just case
state. The first probe's overly strict plain-save sequence oracle failed;
it was corrected to allow the existing explicit no-op-save meta increment,
while still requiring no case/rec/shared/audit change. No source correction
followed verification. Source SHA256 bindings rechecked and match exactly.

Current core/API guides, existing UX synthesis/index and appended log reflect
bounded closure, not professional/source-policy/operational approval. Original
adverse Review is byte-identical above an appended correction disposition.
Correction engineering blocker closed; same-branch normal publication below.

Pre-publication validation: lifecycle JSON parses and every declared artifact
exists; 356 relative documentation/artifact targets exist. Original Review and
knowledge-log byte prefixes match HEAD exactly. Final source fingerprints match
the independent verification, `git diff --check` passes and the exact owned
SQL container is absent. Only owned correction source/tests and related
documentation/artifacts are staged; no unrelated change is included.

### P04-T03: Actual publication and stop boundary

Authenticated `gh api user` returned 8036360/jmservera. Set repository-local
privacy-safe email and explicitly use it for author/committer, with required
Copilot trailer. Commit b6122fbec2e98db1640808c5d0408584da0ce848 contains the
source/tests/docs and bounded verification. Normal same-branch push succeeded.
Committed source bytes exactly match independent verification fingerprints.

`gh pr edit 382` failed because GraphQL rate limit was exhausted; not counted
as successful publication. Standard `gh api --method PATCH
repos/jmservera/ama/pulls/382` REST fallback updated title/body and subsequent
REST GET independently confirmed body/title, open draft, unchanged main base,
requested topic head and b6122fb source SHA. PR preserves exact four-criterion
table, original adverse Review, correction red/green/SQL evidence, independent
closure, shared seam overlap and human/source-policy/operational limits.
No hosted check result is represented as passed.

All P04 markers complete. This publication-state-only update is the final
normal commit/push, then stop. No source edits after bounded verification,
second full RPI/Review, merge, rebase, force push, issue closure or human approval.

## Original RPI Execution (Historical)

The following initial execution and stop record precedes explicit correction
ONE authorization. Its adverse Review remains valid historical evidence, not
the current correction disposition.

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
P03 incomplete visibility publication executed; no engineering completion claim.
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

## Publication and Stopped Session

Source/evidence commit `2e45b5e` created with both author/committer email
`8036360+jmservera@users.noreply.github.com`, derived from actual gh api user
id/login and repository-local configuration. Required Copilot co-author trailer
present. Normal push of feat/assessment-reconciliation-controls-84 succeeded;
independent main-targeted **draft** PR #382 created:
https://github.com/jmservera/ama/pull/382.

PR title/body explicitly mark WIP, Not accepted, RV-001 High blocker and Do not
merge, with exact four-criterion evidence, tests/limits, complete dated artifact
pointers and shared Store/SqlStore overlap warning. No closing keyword, actual
issue closure or merge. The dated Research/Plan/details/critique/changes/Review/
state artifacts are committed with implementation, not left only in chat.

Final bookkeeping records session stopped, active phase Follow-up, task blocked
and later authorization required for RV-001; no nested correction or repeated
Review. Phase execution/publication complete is not successful engineering
delivery. Final bookkeeping commit/push carries this factual state; no source
changes after the Review, only explicit acceptance-status documentation and
lifecycle/publication evidence.
