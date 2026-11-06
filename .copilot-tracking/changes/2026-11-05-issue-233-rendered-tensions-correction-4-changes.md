---
title: "Changes and review: issue 233 tensions correction 4"
description: Region-index Tab reach, changes and single Review
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Changes: `check_regions_and_keys` now records the scoped region index of the focused element (`evidence.evaluate`) and requires every index reached, instead of deduplicated label strings; nonblank label, tabIndex and caption guards kept. `tests/test_atlas_tensions_checker.py` doubles now model scoped region indices; two cases added (duplicate names, second unreached fails; both reached passes) and the six earlier cases kept. No application, CSS, fixture or threshold change.

Evidence (external, `/tmp/r233d-light.za1YNJ`): RED attempt 1 `red-attempt1-double-incomplete.log` (double did not feed the old helper labels; kept as a failed attempt); RED `red.log` exit 1 with the duplicate-unreached case wrongly accepted by the unchanged helper; GREEN 8 tests OK; role conformance 11 OK; atlas trace 17 OK and trace complete; stronger Ruff, 100-column format and strict mypy on both files exit 0 with external caches; imports resolved to this worktree.

Review (executed once): conformant on light checks. Residual limit: the new in-page index expression is covered only by doubles and static checks here; it has not been run in Chromium for this head. Focused gate, partial receipt and the 194-style browser check are pending coordinator admission after 96. The 18f38e8d receipt and run are historical. Correction 3 chronology deviation stands. C4, C5, WCAG, AT and human acceptance remain unmet.
