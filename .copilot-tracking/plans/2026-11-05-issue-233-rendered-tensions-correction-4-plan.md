---
title: "Plan and details: issue 233 tensions correction 4"
description: Track Tab reach by region index
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Tier FOCUSED; checker, tests and records only. Light validation only; no browser, gate or heavy lock (another runner owns admission).

* Test first: extend `tests/test_atlas_tensions_checker.py` doubles so the evidence double answers a scoped index query. Add cases: two same-named regions with only the first reached fails; both reached passes. Keep the six earlier cases' intent.
* Prove RED on the unchanged helper (duplicate-unreached case must be accepted wrongly), then change the helper.
* Fix: keep the nonblank-label, tabIndex and caption guards; record the set of region indices reached via `evidence.evaluate` (index of `document.activeElement` among the scoped regions) and require all indices.
* Validate with unit, role conformance, atlas trace, stronger Ruff (no cache), 100-column format and strict mypy using external caches; commit; fresh clean auxiliary worktree.

Critique (single pass): compatible; no assertion redesign, no unique-label demand.
