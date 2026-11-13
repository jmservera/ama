---
title: Issue 153 exact button names plan
ms.date: 2026-11-13
---

## Plan

* [ ] Phase 1: app.js briefing catch: compute `empty = !content.childElementCount` before the notice; name "Try loading briefing again" when empty, "Refresh briefing" otherwise.
* [ ] Phase 2: app.js startupFailed: name "Reload workspace" when `error.reloadWorkspace`, else "Try again".
* [ ] Phase 3: tests: update regex/fragments; add node-run per-state checks that extract the notice branches and assert each names only the rendered button.
* [ ] Phase 4: run targeted tests, ruff, mypy; critique before code; review after.

Details: see the matching details file.

## Critique (rubber-duck, once)

Revise: PC-001 repeated failure must use a painted flag, PC-002 hidden content, PC-003 test state transitions. Applied directly: painted flag, hidden branch (choose Show briefing), pure helpers tested with node across all four briefing states and both startup states. DOM-level browser transitions are covered by existing browser checks; not run here.
