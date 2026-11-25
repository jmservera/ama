---
title: Issue 2320 live r8 changes
ms.date: 2026-11-25
---

Tier FULL (src change); the full gate was not run by this worker. Nothing pushed; no Azure resource changed.

## Changes

* `src/core/src/zava_forward/core/store.py`, `sqlstore.py`: 10 s cache (`_briefing_busy`) of the unrecorded briefing answer so repeat GETs skip the capped lock wait; cleared on a successful record.
* `src/api/tests/test_assistant_release.py`: new repeat-GET test; the existing busy test clears the cache before its second step.
* `docs/reference/research/issue-2320-live-r8-2026-11-25.md`, index and log.

## Validation

`tests.test_assistant_release` 84 OK; `test_ai_tasks`, `test_briefing_hax_states`, `test_ai_boundary` 97 OK; ruff clean; api mypy clean; core mypy has 3 existing errors in files not changed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 Profile where the briefing spends time | Proven (already ticked) | research note cause section |
| 2 Within 5 s or named state, never 503 on a quiet system | Unproven live: fix not deployed. Cold start and SQL resume ruled out by az reads; code and test bound repeat GETs | research note, tests |
| 3 Test proves the read path does not take the write lock | Proven for cached reads and repeat GETs in a busy period; first miss records by design | `test_assistant_release.py` |
| 4 Live re-check with elapsed times | Proven (already ticked) by r7 probe; not repeated, fix undeployed | r7 note |

No issue boxes ticked.
