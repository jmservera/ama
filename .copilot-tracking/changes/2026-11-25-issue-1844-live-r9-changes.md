---
title: Issue 1844 live r9 changes
description: Changes record and per-criterion table for #1844
ms.date: 2026-11-25
---

Tier: Focused (one new browser-free test; no src, auth, SQL, infrastructure, deployment or dependency change). Basis: test and documentation only.

## Changes

* Added `src/api/tests/test_map_home_card_narrow_layout.py` (5 tests; fails 1 of 5 when the narrow rule is mutated, passes 5 of 5 otherwise).
* Added `docs/reference/research/issue-1844-live-r9-2026-11-25.md` with evidence folder, index row and log entry.
* Validation: 64 related tests OK (accessibility baseline, content standard, map lazy sensors, design system, new test); ruff and mypy clean; harness 436 PASS, 0 FAIL, 0 skips; live probe on revision 0000072.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Failing-first regression with served-byte identity | Proven (earlier pre-fix run; live hashes equal checkout; new browser-free pin fails on mutation) |
| 2 | Four viewports, both tile states, pointer and keyboard | Proven on harness (8 states); live partly (zoom 0 of 2 covered at 320 and 390 px); live marker hit tests unproven |
| 3 | Escape, Close, another home, expand/collapse/reopen; desktop; overflow | Proven on harness; live no overflow, desktop card absolute; live focus actions unproven |
| 4 | Attribution after scrolling | Proven on harness |
| 5 | Existing map browser and axe checks, zero skips | Proven (436 pass, 0 skips, axe 0 violations); no recipe changed so no manifest hash; no conformance claim |
| 6 | Independent exact-head review and hosted CI | Unproven: needs a push, forbidden here |
