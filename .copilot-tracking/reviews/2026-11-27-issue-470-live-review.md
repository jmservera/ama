---
title: Issue 470 live review (2026-11-27)
ms.date: 2026-11-27
---

Executed once. Outcome: conformant with limits.

* Table values re-derived from both receipts and agree with `rpi-gate-timing.py report` for g2182b.
* Criterion 4 correctly left unticked; the 1h40m wall is not claimed and is flagged as unmeasured setup or queueing.
* Open item, routed to a later user-selected task: a second passed full receipt on the same head and `compare --markdown`, then a PR entry.
* Human approval and hosted CI remain required and were not observed.
