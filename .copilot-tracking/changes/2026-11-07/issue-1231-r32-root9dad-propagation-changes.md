# Issue 1231 r32 root 9dad2aba propagation: changes

Plan: .copilot-tracking/plans/2026-11-07/issue-1231-r32-root9dad-propagation-plan.md (unticked, committed 3f05e098 before the merge).

* Backup ref backup/issue-1231-c18-pre-r32-merge at c18f45f2.
* Normal merge of root 9dad2aba, merge commit 13719959f3d94e9493da025308a7659a7c97ab71 (tree cdf89a6c78a5ec25f1b45e98b04e6787fe4102ed). No conflicts, no hand edits.
* Changed paths vs c18f45f2: src/api/checks/workbench_browser_check.py, src/api/tests/test_workbench_live_defaults.py, docs/reference/research/retrofit-synthetic-data/scenario-manifest.json (all root blobs), docs/reference/log.md (7 added, 0 deleted), plus root RPI additions. All ranking source and tests keep the c18f45f2 blobs; no existing tracking path modified or deleted.
* Light evidence (own venv, imports from this worktree, PYTHONDONTWRITEBYTECODE=1): core 76 OK; API wiring + live defaults + register + screens 72 OK; ruff clean, format clean, mypy 128 files clean. Logs in /mnt/ama-gates/g1231-r32-prep-1107/logs.
* No browser, Playwright, SQL, Docker or FULL run, so the R31 browser failure fix is incorporated but NOT executed or claimed.
* Main drift: origin/main is b284d0d3 (score-only) versus declared 7c6d135d; not merged.
