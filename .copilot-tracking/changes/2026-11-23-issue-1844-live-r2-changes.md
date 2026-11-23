---
title: Issue 1844 live r2 changes
description: Changes record and per-criterion table for #1844
ms.date: 2026-11-23
---

No source file changed. Tier: Focused (documentation and tracking evidence only).

## Changes

* Added `docs/reference/research/issue-1844-live-r2-2026-11-23.md`, a knowledge-base index row and a log entry.
* Added dated r2 RPI artifacts under `.copilot-tracking/`.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Failing-first regression with served-byte identity | Proven (earlier 2026-11-23 note) |
| 2 | Four viewports, both tile states, pointer and keyboard | Proven on harness (8 states, 0 of 5 covered); live partly proven |
| 3 | Escape, Close, another home, expand/collapse/reopen; desktop; overflow | Proven on harness |
| 4 | Attribution after scrolling | Proven on harness |
| 5 | Existing map browser and axe checks, zero skips | Proven (436 pass, 0 skips, axe 0 violations); manifest not applicable |
| 6 | Independent exact-head review and hosted CI | Unproven: owner-gated, needs a push |
