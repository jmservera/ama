---
title: Issue 521 rollback-fixture diagnostic D1 research
ms.date: 2026-11-11
task_id: 521-rollback-d1-1111
---

## Scope and boundary

One bounded, test-fixture-only diagnostic (D1) on existing issue #521, a follow-up to merged PR #877 (merge `6703e1419f5e97aef32bf9682fdf46ad47cbe8c0`, 2026-11-03T22:32:55Z). Worktree branch `test/resident-authority-rollback-521-d1-1111` on base `7880b95b19525ff465cab27870ba9d55b57110a3`. No new issue, no push or PR now, no change to PR #1444 or issue 83. Research disposition: executed. If a product defect or non-fixture source change were found, stop for separate authority; none was found.

## Evidence consumed

* Issue #521 body and all six comments (read 2026-11-11). The owner decision of 2026-11-04 keeps `2028-01-01T00:00:00Z` exclusive for everything and says not to ask again. The 2026-11-11 closure-first comment admits this one D1, states that the finding is static, and keeps AC1 and AC4 unticked. Criteria state: AC1 (consistent move across code, SQL, helper, docs, tests) unticked; AC4 (live Azure change applied and verified) unticked.
* Original review comments on PR #877 (not erased, not relabelled): [r4458006989](https://github.com/jmservera/ama/pull/877#discussion_r4458006989) and [r4458275275](https://github.com/jmservera/ama/pull/877#discussion_r4458275275), both from the Copilot reviewer on 2026-11-03, both saying the rollback fixture at `valid_to='2028-01-01T00:00:00'` is now valid so `assertRaises` would fail; the second recommends `AUTHORITY_END + timedelta(seconds=1)`. Three COMMENTED reviews exist (5756465286, 5756645836, 5756807776); no approval, no independent Pass survives. Merged is not accepted.
* Historical #877 actual checks as given by the owner: source core/API/agents/orchestrator/importer/namespace/no-working-data/images/MSSQL context succeeded; rubric activation FAILED and later stages were SKIPPED. This is not a prior green and says nothing about the current gate.
* Current test and source at the pinned base: `src/core/tests/test_resident_showcase_sql.py` line 686 `self.allow("C-1", end="2028-01-01T00:00:00")` inside `test_failed_migration_rolls_back_original_check_and_leaves_no_transaction`. The shared cap is `rs.AUTHORITY_END` read from `resident-demo.json` (`2028-01-01T00:00:00Z`); the SQL template and helper read the same value. Neighbouring tests already use `end="2028-01-01T00:00:01"` (the one second beyond) as the rejected value and `2028-01-01T00:00:00` as an accepted value (`test_table_checks_reject_blank_provenance_and_late_window`). The git log's last touch of the file is #877.
* The finding is static; no real SQL has been run for it before this task.

## Diagnosis and design

With the row at the cap, the migration batch re-adds `ck_allowed_case_window` with `valid_to <= '2028-01-01T00:00:00'` via `WITH CHECK`; a row equal to the cap satisfies it, so the batch succeeds, `assertRaises` fails and the rollback path is never exercised. Intended fixture: a row one second beyond the shared maximum, derived from `rs.AUTHORITY_END` so the test follows the single source of truth, formatted like the neighbouring `strftime("%Y-%m-%dT%H:%M:%S")` fixtures. `timedelta` needs adding to the existing `datetime` import. All assertions stay: original check definition, disabled/untrusted flags unchanged, rows unchanged, `@@TRANCOUNT` 0, the real SQL Server test, then `DELETE` and re-apply in `finally`.

## Validation prerequisites (verified read-only, 2026-11-11)

* Cached image `mcr.microsoft.com/mssql/server:2022-latest` id `cf8f0ab2ebe6...` present; no pull planned. No SQL container running; host ports 13005 and 12563 occupied by others, so a random loopback port is used.
* Memory about 8 GiB available, disk 96 GiB free. `/tmp/ama-rpi-heavy.lock` exists; admission by non-queued `flock -n`.
* Own venv `/tmp/ama-521-d1-venv-1111` created with pinned `mssql-python==1.15.0`, `ruff==0.17.1`, `mypy==2.4.0`, `PyYAML==6.0.3` and editable `src/core`; the driver imports with `libltdl.so.7` and `libkrb5.so.3` present. Route follows the `tools/rpi-checks.py` SQL group (owned labelled container, `127.0.0.1::1433`, `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`).

## Planning Readiness

Ready. AC1 and AC4 remain unmet after this task; actual cost, headroom, live SQL, row expiry and approvals are separate.
