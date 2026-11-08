---
title: Issue 79 r30 research, merge of main 7c6d135d
ms.date: 2026-11-07
---

Research disposition: executed. Planning Readiness: Ready.

* Root `8010a4867ef4db5df355531f5a8c1839f19ac7b2`, tree `41636ccda74271ec90547248858d3fe5e66bce1c`, ignored-clean, branch `feat/ranking-publication-runner-79`. Fetched `origin/main` is `7c6d135df740aec33ddb1961da3f5f0e8706c8ff`, tree `c22b66bf8ae419702cfc1145c47427b42af8eb81` (hotfix 1263 merged and reachable). `f0afa8d7` is its ancestor. Preserve ref `preserve/issue-79-pre-main7c6d`. Child c18f45f2 and the remote head 181a1c1b are untouched.
* Non-tracking delta f0af to 7c6d: `docs/reference/log.md`, `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`, `src/api/checks/workbench_browser_check.py`, `src/api/tests/test_workbench_live_defaults.py`, plus tracking records. Only `log.md` overlaps this root's changes (both sides append); `git merge-tree` is clean.
* Hotfix 1263 receipts do not validate ranking. Applicable light checks: the manifest and core integrity tests, workbench live-defaults unit tests, ranking publication tests, ruff, mypy.
