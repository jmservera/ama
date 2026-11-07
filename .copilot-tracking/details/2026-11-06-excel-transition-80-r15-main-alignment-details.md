---
title: Issue 80 r15 details, ancestor alignment to advanced main
description: Exact merge, proof and check commands for the r15 alignment
ms.date: 2026-11-06
---

* Plan: [r15 plan](../plans/2026-11-06-excel-transition-80-r15-main-alignment-plan.md).

## Phase 2 merge

* `git tag preserve/issue-80-prealign-2e05558e6 2e05558e6cd7cc92e194bba2024b6d1463269a40`.
* `git fetch origin`; require `origin/main`, `origin/feat/case-workbench-integration-73` and the local parent branch all equal 56eec736906774ef56d8c9a66ed7f3f9c1e520c6.
* `git merge --no-ff origin/main -m "chore: merge main into issue 80 export topic"` with the Copilot trailer. Abort with `git merge --abort` on any conflict and stop.

## Phase 3 proofs

* `git rev-parse HEAD^1 HEAD^2` of the merge commit equal the actual pre-merge HEAD (the planning-records commit whose parent is 2e05558e6) and origin/main; `merge-base --is-ancestor` for 2e05558e6, origin/main and the parent branch against the merge commit. Later record commits are checked against the merge commit, not assumed to be it.
* `git diff --name-only 2e05558e6 <merge>` outside `.copilot-tracking/` must list only `.github/agents/ama-backlog-delivery-coordinator.agent.md`, and its blob at the merge must equal its blob at origin/main (`git rev-parse <merge>:path origin/main:path`). `git diff 56eec736 <merge> --name-only` outside tracking must equal the topic's own 15 files; blob ids for those 15 paths at the merge equal the old head. Any failed proof or failed light check stops the round before freeze.

## Phase 3 checks (owned env under `/mnt/ama-gates/restart-1106-80-align/`, bytecode disabled, no worktree caches)

* Inspect the existing r13 venv `/mnt/ama-gates/e80-r13-r67-1106/venv` for read-only use; otherwise build a new external venv and pip-install pinned dev tools only after an actual missing-tool failure.
* From `src/core` and `src/api` with PYTHONPATH of the component guides' test paths: `unittest` for `test_list_export` (core) and `test_list_export_api`, `test_role_endpoint_inventory`, `test_form_staging_api`, `test_finance_grants_screens`, `test_loading_feedback`, `test_browser_harness_scratch` (api); `ruff check .`, `ruff format --check .` and `mypy` per package config as applicable; import of the changed modules.
* Link and diff checks on the new records. Intentionally unrun checks are listed as unrun.
