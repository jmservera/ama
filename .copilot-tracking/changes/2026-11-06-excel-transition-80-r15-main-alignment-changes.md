---
title: Issue 80 r15 changes, ancestor alignment to advanced main
description: Actual merge, proofs and light check results for the r15 alignment
ms.date: 2026-11-06
---

* Plan: [r15 plan](../plans/2026-11-06-excel-transition-80-r15-main-alignment-plan.md). Planning records and the one independent critique (Proceed with changes, applied) were committed as c21848d374b1b8e0db13ff9a49812b55e4a7b91e before the merge.

## Change

* Local lightweight tag `preserve/issue-80-prealign-2e05558e6` preserves 2e05558e6cd7cc92e194bba2024b6d1463269a40. After a fresh fetch, origin/main, origin and local feat/case-workbench-integration-73 were all 56eec736906774ef56d8c9a66ed7f3f9c1e520c6.
* `git merge --no-ff origin/main`: no conflict. Merge commit d3e7267a9540bf9b21213152b3fdaee058c1db84, tree 5f2c589f66c6523699cda58cc5d9b43b4287f778; first parent c21848d37 (planning commit), second parent 56eec736.

## Proofs

* 2e05558e6, origin/main and origin/feat/case-workbench-integration-73 are all ancestors of the merge.
* Outside `.copilot-tracking/`, the merge differs from 2e05558e6 only in `.github/agents/ama-backlog-delivery-coordinator.agent.md`, whose blob d471fc61041f9fc73a43564f7bf390a7c7d10cf5 equals origin/main's. `git diff --name-only 2e05558e6 HEAD -- src` lists zero files. The topic's 15 non-tracking files relative to 56eec736 have blobs equal to 2e05558e6.

## Light checks (pinned ruff 0.17.1 and mypy 2.4.0 from the r68 api venv, executed read-only; bytecode off; caches and logs under `/mnt/ama-gates/restart-1106-80-align/`)

* Core `unittest test_list_export`: exit 0, 4 tests OK. API `unittest` over test_list_export_api, test_role_endpoint_inventory, test_form_staging_api, test_finance_grants_screens, test_loading_feedback and test_browser_harness_scratch: exit 0, 74 tests OK. These ran against checkout source via PYTHONPATH (source-path evidence, not installed-package evidence).
* `ruff check` and `ruff format --check` in src/api and src/core: all exit 0.
* mypy first run (r68 venv, whose agents package is editable) exit 1 with 4 errors; mypy with MYPYPATH to ../agents/src exit 1 with 2 unused-ignore errors. Both are environment artifacts of that venv (agents package missing or typed via editable path); retained in `api-mypy.log` and `api-mypy-r2.log`. mypy with `--python-executable` the owned r13 venv, which has non-editable installed candidate distributions of identical source: exit 0, "no issues found in 188 source files" (`api-mypy-r3.log`).

## Unrun and limits

* Not run: core, agents, orchestrator and importer mypy, other project test suites, FULL, SQL, browser, images, scans. The r69 receipt (bb3a3b03 base, old head) is retained unchanged and does not cover this head. A new coordinator-admitted FULL and independent exact-head assessment are pending. Ignored-inclusive status was empty after checks.
