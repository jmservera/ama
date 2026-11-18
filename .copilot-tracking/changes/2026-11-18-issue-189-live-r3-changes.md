---
title: Issue 189 live audit changes
ms.date: 2026-11-18
---

Files: docs/reference/research/simulator-run-controls-live-189-r3-2026-11-18.md and its folder (two raw files), docs/reference/README.md (index line), docs/reference/log.md (entry). No src change; FOCUSED tier. No Azure resource created or changed.

## Per-criterion table (issue 189)

| Criterion | State |
| --- | --- |
| Cost estimate for declared N homes (ticked) | Consistent, unchanged |
| Quota headroom vs #140 tier (ticked) | Consistent, unchanged |
| Run has an owner | Proven for the demo (hub tag live; blank owner refused) |
| Run has a time limit | Proven in code on a real clock; no deployed run |
| Run has a budget alert | Configuration proven live; firing and human delivery unproven (noreply or invalid recipients) |
| Criterion 3 as one live conjunction | Unproven |

Production-only: deployed run with control file and admin role; monitored alert recipient and firing test.

## Validation

* src/core unittest (two modules): 32 OK. src/api test_simulator_admin: 30 OK (observed; raw output not retained).
* mypy and ruff: not applicable, no Python source changed.
* Hosted CI: not observed; no push.

Note: earlier same-name tracking files from prior passes were restored; this pass uses the r3 names (state in issue-189-live-r3-state.json; the existing issue-189-live-state.json is unchanged).
