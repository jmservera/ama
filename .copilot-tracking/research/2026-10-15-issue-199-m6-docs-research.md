---
title: Issue 199 M6 research
ms.date: 2026-10-15
---

## Disposition

Research executed. Planning Readiness: Ready.

## Evidence

* Issue #199 and ADR 0006 (move, not copy). Matrix row `mvp/README.md` assigns the split to M6; M6 row: "Leaves `mvp/` empty for #201 and #202".
* `mvp/` held only `README.md` (1011 lines) after M5. It carries dated evidence sections the rubric scores.
* Baseline on `main` e019293: core 252, agents 31, orchestrator 17, importer 9, api 438 (92 skipped) = 747; mvp 0; infra 75.
* Exemption probe (`ruff --config lint.per-file-ignores={}`): core 1515, api 645, agents 122, orchestrator 31 findings plus 61 mypy errors; importer 6 (small, safe).
* #200 scan (`git grep mvp/`): workflows `mvp-ci`/`mvp-validation` filters (kept, check names), `build_mvp_dataset.py` data path, `tools/rename-zava*.py` live paths remain.
* Docker and SQL Server are unavailable locally; CI covers image and mssql jobs.

## Decisions

* Keep a pointer README in `mvp/` (deleted at cut-over, #201/#202).
* Single docs-only PR; no M6a/M6b split.
