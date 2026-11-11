---
title: Issue 80 current-main integration plan
description: Revalidate merged parent ef16f3e2 against main 0509ddce
ms.date: 2026-11-11
---

## Objective

Validate the actual committed merge `ef16f3e2` in this worktree. No source edit beyond the already committed additive inventory resolution; any failure stops for Root.

## Phases

* [ ] Phase 1: assert cwd, head, tree, import origins under this worktree and owned `ZF_DATA`; record served hashes (`server.py`, `app.js`, `index.html`, `staff-intake.js`, `ops.js`, checker).
* [ ] Phase 2: non-browser targeted tests: role endpoint inventory, staff intake API, content standard, child CSV 13, handoff API, case journey 31, list export 11, static 60, resident API, core `test_resident_decisions`, Atlas checker test (skips recorded separately; critique PC-001).
* [ ] Phase 3: browser, nonqueued, tests unwrapped (own internal lock): UI 6, handoff guidance 9, staff intake browser, each with `ZF_BROWSER_TESTS=1`; confirm zero skips. Then ONE whole `capacity_browser_check --axe /tmp/axepk/package/axe.min.js` (sha256 checked against the pin; critique PC-002) (its own lock) because served `index.html` and `server.py` changed.
* [ ] Phase 4: Ruff check and format, mypy, Node syntax for `staff-intake.js`, `app.js`, `ops.js`.
* [ ] Phase 5: native review, tracking-only commit, handoff.

## Stop rules

Real failure: record first failure, stop for Root, no C6, no source fix. Busy lock: report needed, not passed.
