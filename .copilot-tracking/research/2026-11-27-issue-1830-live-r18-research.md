---
title: Issue 1830 live r18 research (2026-11-27)
ms.date: 2026-11-27
---

Research disposition: executed. Planning Readiness: Ready.

* Retained receipts: only `/tmp/r2188/receipt.json` (scope partial) and `/tmp/r2188t/receipt.json` (digest missing); the analyzer refuses both, so no multi-receipt full-gate measurement is possible. The #1830 cited receipt is gone and no verified full receipt is retained on this host.
* Hypothesis: `critical_chain` in `tools/rpi-gate-timing.py` selects `earlier` commands with `end <= current.start`; two zero-length commands at the same instant select each other, so the walk never ends.
* Evidence and the final analysis: [research note](../../docs/reference/research/issue-1830-live-r18-2026-11-27.md).
