---
title: Issue 440 live research (2026-11-21)
description: Research record for the 2026-11-21 live pass on criteria 7 and 8
ms.date: 2026-11-21
---

Scope: synthetic demo, desktop only, head `b6d215334`. Refs #440. Research disposition: executed.

* Unticked criteria: 7 (triage) and 8 (PR artifacts, independent review, Major HVE behavior).
* Prior art: [2026-11-20 verdict](../../../docs/reference/research/issue-440-live-criteria-verdict-2026-11-20.md) left C7 proven for the demo with no screenshot of the time screen, and C8 unproven.
* Plan of observation: re-run the live probe against `ca-cutover-test-demo-api`, capture a real signed-in time screen screenshot, rerun D1 to D3 local checks, look for any new defect, and test whether C8 sub-claims (coordinator static/behavior/host evidence) are provable without a PR.

Planning Readiness: Ready. Findings are appended below as observed.
