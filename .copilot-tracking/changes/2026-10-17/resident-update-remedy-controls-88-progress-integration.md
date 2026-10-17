<!-- markdownlint-disable-file -->
# Authorized issue88 integration onto partial progress PR390

## Boundary and Authorization

Own worktree /home/azureuser/source/ama-wt/issue-88, own branch
fix/resident-update-remedy-controls-88, existing main-targeted PR392.
Verified clean status and local/remote head
a91f1737d036141169b5ba5381429cf3e49054cf before writing.
Fetched main and read actual graph: authorized base
226702779e57e490cb10dc06ab014760c7d8a761 is PR390 over quality base
3f544fb9cda2c51b219db2cc8368c7525bbe0c86.
Coordinator explicitly authorized rebase and topic-only force-with-lease
limited to that freshly verified expected old remote. No other worktree, main
write, Azure, paid AI, private data, merge, issue closure or new authority.

## Actual Rebase and Parity Before Validation

Executed git rebase 226702779e57e490cb10dc06ab014760c7d8a761.
Conflicts were only documentation insertions: KB index/log and core/API guides,
then the earlier integration's resident index wording. Resolution keeps all
progress/resident sections and route rows, latest upstream log as exact byte
prefix followed by all own entries. No ours/theirs blanket resolution.

Rebased candidates: implementation1eceab39, old publication7265ddf2,
quality integration1f1dd656, moving-ref receipt9ea45ad1.
Compared git diff --unified=0 additions/removals for all fourteen src paths:
old3f544fb9..a91f1737 equals new22670277..9ea45ad1, ignoring relocated
context only. Exact own production/test/guide added/removed lines preserved.
All original RPI and earlier integration artifacts are byte-identical to old
remote, including original single Review, critique and state. No new full
Review, retrospective phase execution log or application correction.

Latest upstream KB log exact prefix SHA256:
9c538344f947ca816dfd9aa6ddaeaa5c47cd35e53150923c8b83973a858ebccc.
Progress implementation, progress core/API tests and src/api/pyproject.toml
are byte-identical to pinned main. Read actual auto-merged runtime hunks:
Store keeps detached resident projection plus read-only progress_report;
server keeps progress GET/export and resident POST committed409 plus quality
committed503 handlers; workflows retains precise UTC handoff timestamps from
upstream and original resident commitment-preservation checks.
No runtime conflict or persistence implementation delta arose.

## Validation Selection

Documentation-only conflicts plus exact production/test patch parity permit
smallest relevant integrated checks, not another unrelated full SQL/Docker run.
Run existing report source/export/role/precision and prospective writer tests,
resident/update/remedy/legacy/recovery tests, handoff lifecycle/HTTP and scoped
quality/hazard/finance/grant negative-writer/no-replay regressions together.
Run full configured core/API Ruff/format/mypy. No web bytes changed; actual
browser and SQL/Docker receipts from previous pinned quality integration remain
historical, not claimed rerun on this new head. No WCAG or independent Pass.

## Execution State

Validation complete: 140 run, 138 pass, two existing skips in48.069s.
No source fault established; zero correction cycles. Expected injected quality
post-COMMIT recovery exceptions were logged by the existing negative tests,
not swallowed and not test failures. Report/CSV, roles, event sequence and
timestamp precision regressions pass alongside resident closure/recovery tests.

Configured checks pass: core Ruff/format62files, mypy115sourcefiles;
API Ruff/format23files, mypy55sourcefiles; git diff --check clean.
Both skips are existing: JSON-file rollback is inapplicable in the SQLite
resident subclass, and the resident API browser is opt-in. Actual MSSQL classes
were not selected. No actual MSSQL, browser or Docker replay on this integration:
only documentation conflicts, exact own src patch parity, no persistence/web
byte changes; coordinator explicitly permits the narrower validation boundary.
Previous real SQL/browser/image receipts remain historical on their pinned base.

## Executed Commands

All run locally with the existing pip-installed worktree src packages. No
dependency or environment changes and no PYTHONPATH=mvp.

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_progress_reports test_progress_report_api.ProgressApi \
  test_progress_report_api.JsonProgressApi \
  test_resident_decisions.JsonResidentDecisions test_resident_decisions.SqlResidentDecisions \
  test_resident_api test_handoff_lifecycle test_handoff_api \
  test_quality_procurement.SqlFlows.test_quality_sql_postcommit_refresh \
  test_quality_procurement.SqlFlows.test_quality_sql_actor_and_stale \
  test_quality_procurement.SqlFlows.test_quality_sql_failures \
  test_quality_procurement.SqlFlows.test_quality_replacement_dependencies \
  test_hazard_referral.SqlHazardReferral.test_failed_writes_preserve_prior_pending_audit_and_original_error \
  test_hazard_referral.SqlHazardReferral.test_recovery_read_failure_quarantines_hazard_and_keeps_prior_audit \
  test_hazard_referral.SqlHazardReferral.test_interleaved_emergency_hold_blocks_every_guarded_commit \
  test_finance_match_controls.SqlFinanceChecks.test_persistent_discard_read_failure_never_flushes_success \
  test_finance_match_controls.SqlFinanceChecks.test_competing_store_write_refuses_stale_approval_without_success_audit \
  test_grant_lifecycle_controls.SqlGrantChecks.test_legacy_preparer_is_reloaded_inside_grant_and_finance_transaction \
  test_grant_lifecycle_controls.SqlGrantChecks.test_transaction_rechecks_designation_change_and_clock_expiry \
  test_grant_lifecycle_controls.SqlGrantChecks.test_rowversion_conflict_cannot_approve_stale_grant -q

(cd src/core && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)
(cd src/api && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)
git diff --check
```

Read source diff3f544fb9..22670277 before rebase; re-read auto-merged
Store/server/workflows after. Programmatic git show and byte comparisons prove:
resident_decisions/sqlstore/quality/hazard/finance/procurement/app.js/panels.js
unchanged versus expected old remote. Progress.py, progress core/API tests and
API pyproject exact new main bytes. Both old/new complete index route keys
retained. Original Review SHA256204aab7fa36e86feae5b5f76a2107e8e7a2655a6b11a6d2113a3c231ea008e99
and critique70fad5b641605fd83c7bc490fcac4c926c9cfcc1d06ba4eaeb63b297c631e01d
are unchanged. All preceding issue88 RPI/integration artifact bytes unchanged.

Upstream tests test_prospective_handoff_writers_retain_microseconds and
test_actual_legacy_mixed_precision_writer_reopen_as_of_and_export execute
both precise writer and legacy ambiguity contracts. The report core suite
checks authoritative source-version order rather than timestamp sorting,
UTC full precision, invalid clocks and CSV exact reconstruction. Progress
Store/report filters and API role/export checks remain intact. No transition
or report promotes response closure into remedy/delivery/finance completion.

## Publication Boundary

Fresh gh api user resolution will supply local privacy-safe author/committer;
own evidence commit includes required Copilot trailer. Verify remote still
equals a91f1737d036141169b5ba5381429cf3e49054cf immediately before pushing:

```bash
git push --force-with-lease=refs/heads/fix/resident-update-remedy-controls-88:a91f1737d036141169b5ba5381429cf3e49054cf \
  origin HEAD:refs/heads/fix/resident-update-remedy-controls-88
```

Do not widen a changed lease. Stop after same PR392 body/remote/local head
verification and clean status. Absence of CI check results is pending, not
green; do not wait idle on CI. No application correction/full Review/merge
or issue closure. Resume3a36c179-e1e3-4332-9c33-fa947262fd79.

## Exact Criteria and Excluded Work

The unchanged implementation/source-test mapping from the earlier integration
still applies to the three issue88 criteria: full purpose/current named owner/
due/basis commitment; response/package closure cannot close open remedy/defect/
charge query; independent owner/date/status/history clocks with legacy Unknowns.
These are not inferred merely from completed plan follow-ups.

Partial progress PR390 remains partial; no historical snapshot reconstruction
or full forward capture is added here. Parallel issue102events owns that work.
RV-001 wider governance stays with planning parent/repository owner at next #81
backlog triage for separately owned Legal/Housing/Complaints policy approval.
No newly invented thresholds/authority; not a blocker on proven exact criteria.
Independent final-head acceptance remains coordinator-owned.
