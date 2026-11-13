---
title: Issue 153 app.js notice owner and next action research
ms.date: 2026-11-13
---

## Scope

Criterion 3 of #153: error and blocked messages state reason, owner and next action. Stacked on b1d4bc59d; safetyPanel untouched.

## Findings

* Gaps in `src/api/src/zava_forward/api/web/app.js`: `Briefing unavailable`, `Priority suggestions unavailable`, `Cases unavailable` (status line), `Map unavailable`, `Home case view unavailable`, `Shared building context unavailable` (no next action), startup alert.
* Existing pattern: `Owner: application support. Next action: ...` (GENERIC_READ_ERROR).
* Substrings asserted by tests/checks that must survive: `Briefing unavailable`, `Priority suggestions unavailable`? (none), `Cases unavailable`, `Map unavailable`, `Use the case and building screens instead`, `Workspace unavailable: ` exact status, `Tab navigation unavailable`.
* Workspace unavailable status is asserted exactly, so it is left unchanged.

Planning Readiness: Ready.
