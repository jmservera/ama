---
title: Issue 1828 review correction cycle 1 critique
description: Single final-candidate critique of the correction plan
ms.date: 2026-11-16
ms.topic: reference
---

Executed once on the final candidate plan. Verdict: proceed, no significant or divergent issue.

* Risk: bbox width vs container width could differ by sub-pixel rounding or scrollbars. Disposition: accepted; 1 px tolerance, uses `clientWidth` as Leaflet does, verified in Chromium when the lock allows.
* Risk: a baseline-read comparison would be simpler. Disposition: rejected, fit reads carry no bbox so a baseline may not exist.
* Risk: fake page drift from Playwright. Disposition: accepted; the full browser run remains the proof of the real path and is a named handoff if the lock is held.
* Scope: harness and one unit test only; reclassify FULL if anything else is needed.
