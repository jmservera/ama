---
title: Issue 109 prospective local integration details
ms.date: 2026-11-10
task_id: 109-prospective-integration-1110
---

## Phase details

* Phase 1 Research: complete, disposition executed, planning readiness Ready.
* Phase 2 Plan: plan, these details, one critique and a prospective changes declaration.
* Phase 3 Implement: pinned-identity recheck, `implement-start`, one `git merge --no-ff --no-commit origin/main 6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2`, blob and TOML invariants, owned venv with import-origin proof, planned checks with raw logs under `ROOT/checks-109-prospective-integration-1110/`, changes actuals, `implement-done`.
* Phase 4 Review: one self-review (not independent), `review-done`; single commit with noreply author and committer and Copilot trailer; literal 40-hex HEAD; `commit-complete`; `verify` exit code read directly.

## Pinned inputs

* main `c66370042eb08f07839d054433f4483078703cf2`; child `6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2` (tree `8906ef415145fb6819fa638df6cb094a18976c03`); local HEAD `a3d5e615f0b2617b40cd5bdd23d00db0be11284e`; remote parent `06374dfcac47cf6bcce9e7b91f573e8565ab45e8` untouched.
* Expected merge tree from dry runs: HEAD+child `1ef571e3`, main+child `7c652a36`; the final tree is the three-way result and is recorded, not assumed.

## MSSQL input boundary

Fresh run on the composed tree: selector `tests.test_sensor_review_draft.MssqlDraftCases`, image `mcr.microsoft.com/mssql/server:2022-latest`, own disposable container and generated throwaway password, `ZF_SENSOR_DRAFT_MSSQL=1`, mssql-python from the owned venv, source = this worktree's staged composition. Expected 22 run, 0 skips. Not an Azure SQL result.

## Browser input boundary

Unchanged `quality_sensors_browser_check` from a short owned cwd, local mock provider, synthetic fixtures under the cwd, `PYTHONPATH` of this worktree. The earlier long-path failure is a known environmental limit, not a pass.

## Stop conditions

Identity drift, unmerged path, failing configured check, BUSY heavy lock, missing non-installable prerequisite, refused marker.
