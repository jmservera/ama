---
title: Issue 199 M5 research, api, orchestrator and image
ms.date: 2026-10-15
---

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #199, ADR 0006 (move-not-copy, `zava_forward` PEP 420 namespace; api may import core and agents, orchestrator only core) and the parity matrix rows marked M5.
* Merged M1 to M4 (#296 to #299): `git mv` only, temporary ruff and mypy exemptions for moved files, CI path filters, repointed docs and trace strings.
* Baseline on `main` before any change: mvp 443 (94 skipped), core 252, agents 31, importer 9, api 8, orchestrator 4 = 747.
* Sizing: 6 modules, 16 web assets, law register, 2 browser checks, 23 tests, Dockerfile and locks; mostly renames, no cycle. One PR is safe.
* Constraints: the Bicep jobs `token_store` and `digest_blob` run in the api image (retarget is #200); the image tag and CI check names stay; public assets mode 0644; SQL stays portable; locks through pip-compile only.
* Gap: the BuildKit per-Dockerfile ignore file takes precedence over `src/.dockerignore`; CI must confirm.
* Docker and SQL Server are not available locally.
