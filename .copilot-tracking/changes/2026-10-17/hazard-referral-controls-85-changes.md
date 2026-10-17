<!-- markdownlint-disable-file -->
# RPI Changes: hazard-referral-controls-85

## Metadata

Task ID 85. Date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/hazard-referral-controls-85-plan.md
Details: .copilot-tracking/details/2026-10-17/hazard-referral-controls-85-phase-details.md

## Execution Status

Coordinator-authorized P04 latest-main integration active after full original
delivery. P01-P03 remain complete, original single adverse Review unchanged.

Full plan declared. P01/P01-T01 and P02/P02-T01 complete.
P03-T01 independent Review and P03-T02 correction ONE complete.
P03-T03 draft main PR #388 published. Original Review Not accepted preserved;
independent final-head acceptance remains external, not claimed complete.
One independent critique executed (Revise); PC-001/002/003 directly applied
to plan/details, no repeat critique or business-decision change.

## Approved Boundary

Hazard-owned module, existing hazard workflow methods, additive SQL hook,
canonical tests and directly related docs only. Shared SQL overlap declared;
preserve every #84/#94/#90 validator/recovery boundary. No other worktrees,
quality.py/finance.py/dataset.py/UI changes. No source ownership conflict found
in this clean branch. No independent open hazard PR found at intake.

## Validation Record

* Research inline probes: exit 0, three actual defects reproduced against
  b5d4c840 (unregistered actor, case-only self-release, failed-save success audit).
* Initial tooling probes: shell `rg` absent; built-in rg used thereafter.
  Expected package import failed before installation; local `.venv` created,
  pip installed editable src/core[sql,dev], agents and api[dev], exit 0.
* Initial full-file view attempts for large docs exceeded view size; focused
  ranges/search used. No private/historical data read.
* Planning patch partially applied once; inspected details then applied only
  missing details hunks. No source edit involved.
* Next: formal fail-before assertions, targeted/final tests and own MSSQL.

## Implementation-Time Plan Updates

Critique direct revisions clarify separate destination authority, JSON
save/audit non-atomicity and prior SQL pending-audit preservation. No scope
expansion, new infrastructure or revised user requirement.

## P01-T01 Completed: Current Actors and Trustworthy Evidence

New typed hazard.py reuses canonical current `_actor`; all seven existing hazard
mutations use its scope. SQL rechecks caller and separate destination after
writer begin. Receipt binds stored identity, not code alone. Reporter/repair
identities retain email/code/OID, with history/legacy fallbacks and normalized
independence checks. Existing role map, home scope, separate evidence, clocks,
case ownership, consent and manual closed-case intake unchanged.

SQL failure quarantines failed staged case/audit before recovery, preserves
prior pending audit exactly once and original errors; context is restored in
finally. Additive SQL hook and eager-discard guard preserve every existing
stock/change/bulk/finance/provider validator. JSON saves before success/
emergency audit, restores memory on pre-replacement failure and explicitly
logs/annotates post-save audit uncertainty without claiming cross-file rollback.

## Commands, Results and Failed Attempts

* First formal unittest selectors omitted core/tests fixture path: five import
  errors, no behavioral evidence. Corrected with `PYTHONPATH=tests`.
* Formal fail-before run: five selected methods, seven assertion failures and
  one cascading error after aliased self-release. Demonstrated absent/forged
  actor, recycled receiver code, case-only self-release, JSON ghost state and
  SQL success audit after failed save. No failing regression was removed.
* First implementation suite found missing per-thread pending initialization
  in the new scope and an OID fixture/cache setup mismatch. Initialized existing
  tracking before baseline capture; updated only local test setup cache.
* Subsequent tests exposed a parent test-edit mistake comparing raw state to
  projected detail and non-durable derived staffing insight changes; corrected
  selectors to compare like-for-like, not weakened production behavior.
* API new test initially held dblock across a separate HTTP request and stalled.
  Exact shell 21 stopped, lock limited to writes; subsequent four HTTP tests pass.
* Ruff/mypy caught closure bindings, type narrowing and mixed mock targets;
  corrected tests/new typed module; configured core/API checks now pass.
* Final canonical hazard suite: 33 run, one explicit JSON-only test skipped on
  SQLite; no existing regression skips introduced.
* Actual own SQL Server: venv script direct invocation first failed source import
  and cleaned its exact container. Venv-bound `python -c runpy.run_path(...)`
  succeeded twice. Final 16 canonical tests, one JSON-only skip, 28.452s.
  Includes separate-connection caller/destination removal/demotion/OID/email
  substitution, failed release/audit rollback, prior audit and one-shot/persistent
  recovery-read faults for generic and transaction refusal branches.
* Docker credentials random/in-memory, never logged; ephemeral mapped port
  verified 127.0.0.1, SQL connection/CREATE DATABASE established responsiveness.
  Each exact own container removed in finally; no shared container touched.
* Full core discovery: 726 run, 21 skips, 374.295s, OK before final test-only
  failure-matrix expansion. Existing suites generated ephemeral synthetic scale
  fixtures (including 60,000 rows); no historical/private stock or rosters read
  and task-owned cases remain the tiny constructed fixture.
* Final narrower combined core selector: 169 run, one selector import error
  (`test_workflows` belongs to API), 20 skips. Every collected behavior passed;
  corrected component selector rerun follows. No unsupported Pass from this run.
* Full API discovery: 658 run, 184 skips, 332.451s, OK. Optional SQL/browser/
  environment suites remain explicit skips; no fallback to a claimed complete
  platform exercise. Expected rule-engine unknown/unloaded-law logs retained.
* Corrected final targeted core command from src/core:
  `PYTHONPATH=tests ../../.venv/bin/python -m unittest test_hazard_referral test_scenario_manifest test_stock_reconciliation test_finance_match_controls test_quality_procurement -q`:
  168 run, 20 skips, 45.677s, OK. Includes exact manifest source-hash audit.
* Final targeted API command from src/api:
  `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_hazard_api test_workflows test_rule_alerts test_role_matrix -q`:
  39 run, no skips, 26.194s, OK.
* Configured `ruff check .`, `ruff format --check .`, `mypy` from both core/API:
  pass, mypy 112/53 files respectively. Final core gate repeated after last test
  expansion, passes. `git diff --check` passes.
* Final actual SQL command from repository root:
  `.venv/bin/python -c 'import runpy; runpy.run_path("/home/azureuser/.copilot/session-state/519fb014-71e3-4e42-ad94-c0cb8ac982bd/files/hazard_sql_parity.py", run_name="__main__")'`:
  16 run, one JSON-only skip, 28.452s, OK. Script exists only in session storage;
  committed canonical adapter retains repeatable test entry. Exact own container
  cleanup confirmed by filtered Docker listing.
* No web source changed,
  so no browser/WCAG acceptance or fresh web review is claimed.

## P02-T01 Completed: Documentation and Integration Evidence

Updated existing core/API contracts, existing profile-review hazard synthesis,
KB index and append-only log. No immutable regulatory material or case original
modified. Fixture dataset.py and existing scenario manifest are byte-unchanged;
no hash refresh needed. Eleven/nine provisional authority preserved.
No quality.py, finance.py, server.py or app.js changes. Final sqlstore.py overlap
is four additive lines: hazard imports, validation, acknowledged-COMMIT marker
and hazard-context eager-discard guard; all merged stock/provider/finance hooks
remain. Ten new semantic methods (six canonical base, three SQL, one HTTP), two
harness adapter overrides and three canonical SQL method bindings, no removals.
Source and test diffs remain limited to declared paths.

## Blockers and Follow-Up Items

No local blocker. Operational role/timing ratification and verified service/
Azure/model/human acceptance remain explicitly unperformed external work.
No legal currentness or professional/operational approval is claimed.

## Pre-Review Reconciliation

Plan and details P01/P02 checked with completion evidence; P03 is independently
assessed next. Changes, failure history, command outcomes, explicit skips,
external follow-ups and source boundaries reconciled. No local blocker.
Review ready; independent execution/outcome not yet claimed.

## P03-T01 Independent Review and Authorized Correction

One independent Review executed Complete / Not accepted. RV-001 High:
post-COMMIT synchronization failure made hazard scope restore prior pending
audit that had already committed, duplicating it and omitting an outcome note.
Original review record preserved, no second Review or independent closure
claimed. User explicitly authorizes concrete fixable correction ONE (max TWO).
This is a real local defect, not a human/policy/tool blocker.

Immediately relevant plan/details update splits P03 into completed Review,
correction ONE and publication. Requirements now distinguish committed from
uncommitted SQL recovery. Test additions remain within budget; no renewed
critique or changed business direction. Correction validation pending.

### P03-T02 Correction ONE Result

Canonical existing SQL failure method extended, no new test method or suite copy.
Fail-before command from src/core:
`PYTHONPATH=tests ../../.venv/bin/python -m unittest test_hazard_referral.SqlHazardReferral.test_failed_writes_preserve_prior_pending_audit_and_original_error -q`.
One method, both post-commit subcases failed: prior_event 6 vs expected5 and8
vs expected7 (duplicate), matching independent RV-001.

Correction: SQL save calls hazard.mark_committed immediately after acknowledged
COMMIT. Active scope distinguishes known committed outcomes: do not replay the
committed baseline, explicitly note/log original synchronization error, reload/
quarantine without prior replay. Uncommitted failure still preserves prior
pending exactly once. No finance/quality or unrelated source changes.

Fix-after actual task-owned SQL Server: same session runpy command and canonical
adapter, 16 run, one JSON-only skip, 17.279s, OK; one-shot and persistent
post-commit sync faults, second writer, durable release/prior/release audits
exactly once and explicit warnings included. Own container removed in finally.
Later edits only bind test closure variables and rename assertion contexts;
no behavior change after actual SQL validation.

Final correction checks:
* Core configured ruff lint/format and mypy112 files: pass. Targeted168 run,
  20 skips, 35.362s, OK, same command as final-core-targeted above.
* API configured ruff lint/format and mypy53 files: pass. Targeted39 run,
  no skips, 26.259s, OK, same command as final-api-targeted above.
* Failed interim static commands retained: Ruff B023 caught unbound closure
  state; bound explicit per-subcase state. Mypy caught reused assertion-context
  variable; renamed postcommit context. One patch missed Ruff-reformatted
  context, inspected exact range then applied. No tests skipped/removed to fix.
* Full core/API pre-correction runs remain historical, not mislabeled
  post-correction full-suite evidence. Final correction evidence is focused
  shared-boundary/core/API and actual SQL, not a second independent Review.

Updated existing docs/synthesis/index and appended correction ONE log entry.
Original Review untouched and remains Complete / Not accepted; RV-001
implementation corrected and self-verified, independent final-head closure
not claimed. No correction TWO or renewed critique/Review.

## P03-T03 Publication and Terminal Handoff

Fresh `gh api user` resolved id8036360/loginjmservera. Repository-local author
and committer use8036360+jmservera@users.noreply.github.com, verified with
`git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`. Explicitly staged
only eleven source/test/doc paths and seven dated RPI artifacts; Conventional
Commit includes Refs #85 and required Copilot co-author trailer.

Implementation/artifact commit35e37145716494db4446f4ba05cb435db3624d6d
pushed normally to fix/hazard-referral-controls-85. `gh pr create --draft
--base main` created https://github.com/jmservera/ama/pull/388.
`gh pr view 388` verified OPEN/draft/main/expected topic and exact source head;
clean worktree verified. Checks not yet reported at initial observation, not
claimed green. Delivery metadata is committed separately and normally pushed;
final PR head is that delivery commit, not a source reimplementation.

`git diff --check` and state JSON parse pass. Own Docker container listing empty.
Independent Review SHA256 unchanged:
`d93129affee31cb045da70e270d50bf909cb0f0a93159dcf83e50274153b2dd7`.
No amend/rebase/force-push/merge or issue mutation. Draft body explicitly names
shared #91/#95 integration additions and retained #84/#94/#90 boundaries.

Task delivery complete; automatic session stopped under user's explicit clean
pushed PR terminal condition. This is not independent correction acceptance,
operational approval or issue acceptance. Ranked external next actions remain
in state. Resume session519fb014-71e3-4e42-ad94-c0cb8ac982bd.
One delivery-metadata patch missed the exact plan heading after applying state;
inspected heading and applied only remaining hunks, preserving state.

## P04-T01 Integration Opening

User explicitly authorizes rebase after publication, including expected-remote
lease only on owned topic. Intake clean head7d3b6bea644f263c592cb35631cd30c4961d92c1,
PR388 OPEN/draft/main. `git fetch origin` verified latest main
2b24456863c0a8f39d47a73e22daeff3875cc825 (merged PR386/#95) over
1fc7325b93ea845b9cb2e827efbea624f7d20d30 (PR385).
Old baseb5d4c8402692758bd929a7ff9bf1832770738346.
Upstream source changes include store/grants/finance/dataset/UI but no
sqlstore.py change; preserve them intact, no duplicate grant fix.
Planned before/after binary production/test patch equality; docs-only conflicts
need minimal docs checks, substantive conflicts require combined backend probes.
Shared #91 recovery overlap remains declared; no other worktree inspected.

### P04-T01 Rebase and Preservation Evidence

Rebase onto2b24456863c0a8f39d47a73e22daeff3875cc825 completed; resulting
integration head e712d86aae8e26fbf525bf7e767cd944d715f762 before evidence commit.
Only manual conflict: docs/reference/log.md appended entries. Removed markers
and retained upstream exact prefix then both #85 entries; no ours/theirs source
selection. KB index/component guides merged automatically with both intents.
No production/test conflict or substantive integration edit.

Initial `cmp` of whole src/infra/tools binary diff failed at byte58 because
that selection also included component README blob IDs/context changed by
upstream documentation. Refined comparison excludes only README.md: complete
production/test patch is exactly byte-identical old-base/old-published-head
versus new-base/integration-head. Both SHA256:
`4cd4138a4efa3212b493d71feb29d823f3845b1ab40eddd4deffb80cfeda40f2`.
Session before-code.patch/after-code.patch retain raw evidence. No filtered
source hunks or weakened tests; docs separately reviewed with full base diff.

Fresh integration checks:
* Validation script: upstream log exact byte prefix; every other upstream
  index route retained; six added relative documentation links/anchors valid;
  original independent Review exact SHA256 unchanged.
* Eight upstream paths byte-identical: store.py/grants.py/finance.py, dataset.py,
  scenario-manifest.json, app.js and both case documents. Thus scoped
  designation, current legacy preparer writer check, shared_finance_operation,
  funding history and neutral UI remain upstream-owned and unchanged.
* From src/core:
  `PYTHONPATH=tests ../../.venv/bin/python -m unittest test_scenario_manifest test_hazard_referral.SqlHazardReferral.test_failed_writes_preserve_prior_pending_audit_and_original_error test_grant_lifecycle_controls.SqlGrantChecks -q`:
  25 run, no skips, 11.164s, OK. Fresh SQLite/manifest integration smoke only,
  including acknowledged-COMMIT fault subcases and upstream grant controls.
* Actual MSSQL/core/API/static results above remain historical correction
  evidence, not fresh integration parity. No substantive source conflict:
  coordinator's explicit docs-only patch-parity validation allowance applies.
  No new SQL container, browser or broad suite required/run.

No duplicate #95 fix or authority promotion, fixture/manifest recomputation not
needed because both exact upstream files are unchanged. No renewed Review.
Pending authorized owned-topic expected-remote lease push and PR evidence update.
