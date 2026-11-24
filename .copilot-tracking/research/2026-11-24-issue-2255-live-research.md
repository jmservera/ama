---
title: Issue 2255 live research
description: Research for demo safety queue target clock data
ms.date: 2026-11-24
---

Task: issue-2255-live (Refs #2255). Research disposition: executed. Planning Readiness: Ready.

Findings:

* The issue lists no ticked or unticked checklist. Its expected outcome is the acceptance criteria used here: C1 some synthetic hazards carry an awareness time and response target; C2 the clock shows elapsed time against target; C3 the hazard service stays the timing authority; C4 the live queue shows it.
* `taskqueues.hazard_clock` prints "elapsed time unknown; no response target window recorded" when a hazard has no valid `aware_at` or `response_due_at`. This is correct fail-closed behaviour; the live data lacks the fields (22 of 22 unknown in the issue probe).
* Precedent: `demo_handoff_due_seed.py` (data fix, marker, revert, counts-only output). A hazard equivalent is the matching fix; no API change, so the hazard service stays the timing authority.
* Live write to the SQL store is private-network only and a data write the 2026-11-18 owner decisions do not authorise (same conclusion as docs/reference/research/issue-2256-b2-seed-2026-11-23.md). The issue's probe files are not in this checkout.
