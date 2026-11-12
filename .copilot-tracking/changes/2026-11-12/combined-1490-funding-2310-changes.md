---
title: Issue 82 combined 1490 candidate changes
ms.date: 2026-11-12
task_id: combined-1490-funding-2310
---

## Summary

One same-issue PR 1490 candidate for #82, local and frozen, not pushed. Plan: [plan](../../plans/2026-11-12/combined-1490-funding-2310-plan.md). Critique: [critique](../../plans/2026-11-12/combined-1490-funding-2310-critique.md).

Commit order above the UX parent `8f8be74e14c5fe1b6911a9493cd74d0750151085` (contains PR 1487):

* `069c35f8f` original 1490 commit rebased (store.py funding denial, test_gates, test_mvp method, original RPI evidence).
* `808fcf4d4` this task's prospective amendment and critique.
* `a8ca3459a` and `768b201cf` the frozen RV01 commits `c4fe717ef` and `4ce5bae61` cherry-picked in original order, with original research, plan, critique, changes, review, evidence, three readers and `MEMBERSHIP_REVISION` 3.

## Conflict resolution

`git merge-tree` confirmed the only conflict, `src/api/tests/test_mvp.py`, between 1487 and 1490. Both complete independent methods are kept: `test_stale_advance_refusal_names_case_owner_and_next_action` (400, no `reasons`, owner and next action) and `test_advance_with_missing_funding_is_a_funding_conflict_not_a_missing_case` (409, funding reason). Each has its own fixture state and server. `store.py` auto-merged; `advance` checks `READY_STAGE` before `gate_reasons`. Cherry-picks applied without conflict. Local backup ref `backup/pre-combined-1490-dc9fb68e0` holds the original 1490 head.

## Validation (focused tier)

Evidence under [evidence](../../evidence/2026-11-12/combined-1490-funding-2310/). Environment: fresh pip-only venv outside the repository with editable installs of this worktree's `src/core`, `src/agents` and `src/api` (imported origin verified under this worktree); no uv; no source-tree `PYTHONPATH`, only the documented test-helper directories (`tests`, `../core/tests`, `../agents/tests`).

* Core, 14 modules touching gates, readers, queues and funding (`test_ai_consumption_safety test_buildings test_bulk_edits test_chat_case_answers test_chat_case_funding_sources test_consultation_controls test_funding_automation_boundary test_gates test_home_case test_quality_procurement test_queue_benchmark test_resident_decisions test_sqlqueues test_taskqueues`): 735 tests, exit 0, 165 skipped.
* API, 13 modules including `test_mvp` and `test_home_case_api`: 519 tests, exit 0, 268 skipped.
* Skips are all opt-in SQL Server harness skips (`ZF_TEST_MSSQL=1`, owned loopback SQL Server, task-owned SQL Server) or SQL replay and writer-dependency notes. They are classified as not run; no real SQL Server acceptance is claimed. The SQLite-backed queue regressions did run.
* Pinned Ruff 0.17.1 `check` and `format --check` pass on the touched core files; mypy 2.4.0 on `src/core` passes (298 files). API: ruff check passes; `ruff format --check` on `tests/test_mvp.py` fails identically on the UX parent version (pre-existing, not reformatted, see `lint-api.out`); `test_home_case_api.py` is formatted. API mypy not run.
* Failing-first, isolated temporary worktree and venv at the combined head with only the three reader sources restored to the pre-RV01 version: core 13 failures and 2 errors, API 1 failure, matching the original RV01 record; the fixed candidate passes (`failing-first-*.out`).
* Negative control: `MEMBERSHIP_REVISION` set to 2 in that temporary worktree makes the SQL queue regression fail; restored to 3 and the module passes (`negative-control-*.out`). Temporary worktree and venv removed; the candidate tree was never edited for the controls.

## Classification and not run

* Tier: focused. Basis: no workflow, gate-tool, dependency-manifest, Dockerfile, permission, secret, deployment, infrastructure or SQL schema change; the gate semantics change only by fail-closed reading of `funding_ok` (explicit `True` stays confirmed), which strengthens, not weakens, the denial. No default complete gate was run and no receipt is claimed.
* Not run: complete local gate, real SQL Server suites, browser harness, API mypy, hosted CI for the exact head, other `funding_ok` readers outside the write surface (`export_fields.py`, `resident_preview_fixture.py`, `ai_eval.py`).
* No push, force-push, PR, merge, tick, human approval, cleanup of shared state, cloud, model or spend call, or private data. Independent exact-head assessment, human approval and hosted CI remain required.
