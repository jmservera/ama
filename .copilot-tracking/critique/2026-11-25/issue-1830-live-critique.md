---
title: Issue 1830 live r14 critique (2026-11-25)
ms.date: 2026-11-25
---

Executed once on the final candidate plan. Verdict: proceed with amendments applied directly.

* Risk: waiting could mask a real marker-overlap defect. Amendment: the wait only settles reads and layout; the axe scan and every assertion stay unchanged, and a persistent overlap still fails. The note must say the cause is a reading, confirmed only by a before and after failure rate.
* Risk: the flake may have a second cause (the 390x568 focus-fit failure seen twice). Amendment: report it separately as unreproduced after the first sequential runs; do not claim it fixed.
* No conflict with owner decisions. Tier FULL (src/api/checks changes); `rpi-checks.py --all` is not run.
