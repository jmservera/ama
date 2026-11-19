---
title: Issue 153 live plan
ms.date: 2026-11-18
---

Refs #153. Research: [research](../research/2026-11-18-issue-153-live-r5-research.md). FULL tier (src change); the full gate is
not run (owner instruction); no push.

## Phases

* [x] P1 Finance limit wording: core reason text drops "envelope"; panels.js shows `Held` as "Paused" and maps
  "envelope" to "investment limit" in finding labels and reason (stored status values unchanged).
* [x] P2 Handoff owner wording: app.js shows "No one named yet. Next action: ask the case lead to name one." instead of
  "Unassigned" for chase owner, proposed receiver and resident update owner on the My cases list, the Handoff tab and the
  waiting table. The "Unknown" resident update commitment text is unchanged.
* [x] P3 Tests: update existing assertions; add focused cases for both screens.
* [x] P4 Per-criterion proven/unproven table with live Playwright evidence note under docs/reference/research/.
* [x] P5 Validation (targeted tests, mypy, ruff) then index, log, commit.

Out of scope (residual): `exceptionRoleLabel` and `item.owner` "Unassigned" fallbacks, N4-N6, generic 403 bodies (R6),
Source line F1, named human review (criterion 5, unprovable).
