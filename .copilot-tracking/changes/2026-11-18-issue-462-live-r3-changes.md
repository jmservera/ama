---
title: Issue 462 live r3 changes
description: Changes record and per-criterion table for the live r3 proof
ms.date: 2026-11-18
---

## Changes

* Added `docs/reference/research/resident-showcase-live-r3-2026-11-18.md`; index row in `docs/reference/README.md`; entry in `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18-resident-showcase-r3/` and this run's research, plan, details, critique, review and state files.
* No `src/`, `infra/` or Azure change; no throwaway resource. Tier FOCUSED.
* Note: the public note was drafted before the `implement-start` witness call; no source was edited at any point.

## Per-criterion table (unticked and re-observed criteria)

| Criterion | Proven or unproven | Evidence |
|-----------|--------------------|----------|
| 1 RPI artifacts and threat model | Proven (this run and earlier); October independent review not re-derived | artifacts above |
| 2 #444/#455 and rubric | Unproven (partly) | #444 closed, #455 merged, rubric success at final head; High review thread unresolved; manual-edit absence unprovable; hosted run needs a push |
| 6 Pre-spend record | Proven for demo; forecast arithmetic only | note, cost section; Cost Management throttled |
| 7 Live browser verification | Proven (desktop demo) | `live-checks.json`, two sign-in screenshots (signed-in captures not retained: personal details visible) |
| 3, 4, 8 (ticked) | Re-observed; source commit for digest unconfirmed | note |
| 5 (ticked) | Not re-run | no source change |

## Validation

* `live_r3.py`: ok, 36 checks, credential-absence assertion passed.
* Leak scan and link check: see review.
