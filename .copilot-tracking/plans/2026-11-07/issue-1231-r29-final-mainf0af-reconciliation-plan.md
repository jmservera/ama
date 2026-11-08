---
title: Issue 1231 r29 plan, final root d99e6901 reconciliation on main f0af
description: Plan for the final local merge, light checks and one fresh FULL
ms.date: 2026-11-07
---

Research: `.copilot-tracking/research/2026-11-07/issue-1231-r29-final-mainf0af-reconciliation-research.md`. Details: `.copilot-tracking/details/2026-11-07/issue-1231-r29-final-mainf0af-reconciliation-details.md`.

* [ ] Phase 1: commit these prospective records; backup ref `backup/issue-1231-5630f-pre-r29-merge`.
* [ ] Phase 2: `git merge --no-ff d99e6901`; resolve ranking conflicts with the child blobs; keep the root UI, score, log and RPI paths.
* [ ] Phase 3: light checks (own venv, no services): core ranking, API wiring and cleanup regressions, Config class and UI host tests, Ruff, format, mypy.
* [ ] Phase 4: preservation proof, changes, one author Review, state, commit and freeze; admission checks; one fresh FULL; native and member verification.

## Follow-Up Items

* Independent exact-head assessment; a later parent squash may need a fresh integrated gate.
* #1258 and #1259 stay separate.
