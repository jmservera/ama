---
title: Issue 470 live research, two retained full-gate receipts (2026-11-27)
description: Research opening for extracting measured per-group wall times from two retained full-gate receipts
ms.date: 2026-11-27
---

Disposition: executed. Goal: read `~/g2182/o/receipt.json` (failed, timeout) and `~/g2182b/o/receipt.json` (passed), extract per-group wall times and the critical path, and decide the one unticked criterion of #470. Tier FOCUSED, no `src/` change, no `rpi-checks.py --all`.

Findings: see [issue-470-live-r10-2026-11-27.md](../../docs/reference/research/issue-470-live-r10-2026-11-27.md). g2182b passed (jobs 2, 3114.1 s receipt wall); g2182 failed at the 1800 s `project-api` timeout (4333.5 s) and the timing tool refuses it. The pair is not like for like, so criterion 4 stays unticked.

Planning Readiness: Ready.
