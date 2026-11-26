---
title: Issue 1288 live r15 plan
description: Plan to run the finite live Quality walkthrough and record per-criterion evidence
ms.date: 2026-11-26
---

Phases (details in the details file):

1. [x] Research: live release in force, allowance absent.
2. [ ] Implement A: run focused local tests (grounding, correlation) as baseline.
3. [ ] Implement B: set finite allowance (calls 10, tokens 200000, expiry +3h, proactive) on the demo API; wait for the scanner; capture the flag, the UI, rai-metrics before and after, and the cited reading IDs with the request snapshot.
4. [ ] Implement C: remove the allowance settings (revert); confirm rai-metrics and listing.
5. [ ] Implement D: fix any real defect found with a failing test first (tier FULL only then).
6. [ ] Record research note, index, log, changes table; review once; commit locally.
