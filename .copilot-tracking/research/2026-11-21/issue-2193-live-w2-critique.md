---
title: Issue 2193 critique, wave 2
ms.date: 2026-11-21
---

Critique executed once on the final candidate plan. Verdict: proceed.

* Reusing the unmerged gauge reorder (43c03d6f0f) is sound: a DOM order change only, with a test that fails on the old order. Applied directly.
* Do not deploy: the goal authorises no production change. The reorder stays unproven live; stated as such. Applied directly.
* Scan all homes (not the first 60) for stale, offline and withheld states, otherwise those criteria stay test-only. Applied directly.
* Web guidelines source fetched 2026-11-21; the change adds no icon-only control, motion or colour-only cue. No conflict with confirmed decisions.
