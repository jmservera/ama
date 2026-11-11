---
title: Issue 1360 extension 2 CI regression plan
ms.date: 2026-11-10
task_id: 1360-extension2-ci-1110
---

* [x] Phase 1 reproduce red for all reported Core selectors; baseline Importer tests (done before the fix: `/tmp/e2/red-core-selectors.log`).
* [x] Phase 2 restore the shared `save` contract and add the import-refusal-only translation.
* [x] Phase 3 retarget the E1 core regression to the import-refusal path with a plain-`save` control; keep Importer tests.
* [x] Phase 4 validation: complete Core unit, Importer 82, API postcommit/quality/resident/hazard/transfer, ruff and mypy of changed files; MSSQL selectors if an owned local fixture and the heavy lock are available, else report blocked.
* [x] Phase 5 changes and review records, one commit, handoff.
