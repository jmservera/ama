---
title: Issue 1830 live phase details
ms.date: 2026-11-18
---

* Phase 1: `git archive a2c27fda6` into a scratch directory outside the repository; run the two candidate test modules; record counts. Success: 54 pass.
* Phase 2: `rpi-gate-timing.py report` per receipt under ~/.local/share/ama/gates; exclude resumed and partial receipts from full wall time.
* Phase 3: docs/reference/research/issue-1830-live-20261118T1648Z-2026-11-18.md plus README index row and log entry.
* Phase 4: changes record; review; commit with trailers. No push. Success: clean tree, no cache files staged.
