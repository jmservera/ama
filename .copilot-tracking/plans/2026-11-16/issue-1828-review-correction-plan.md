---
title: Issue 1828 review correction cycle 1 plan
description: Plan to attribute the viewport premise read in the map browser harness
ms.date: 2026-11-16
ms.topic: reference
---

## Plan

Research: [research](../../research/2026-11-16/issue-1828-review-correction-research.md). Details: [details](../../details/2026-11-16/issue-1828-review-correction-details.md). Tier FOCUSED.

* [ ] Phase 1: non-browser failing-first test. Add `src/api/tests/test_map_viewport_premise.py` with a virtual-clock fake page covering: stale pending read must not satisfy the premise, genuine resized read passes, late old-width read fails, unchanged container width fails. Run against the old check logic and keep the failing log.
* [ ] Phase 2: harness fix. Settle map reads before the resize, require a read whose bbox-projected width equals the post-resize `#leaflet` width and differs from the pre-resize width, keep the premise from being weakened, restore the viewport in `finally`.
* [ ] Phase 3: verify. Unit tests, ruff, then the full map browser/axe check only if the heavy lock is free; otherwise record a named handoff.
* [ ] Phase 4: changes artifact, review once, commit with required author, committer and trailers. No push.

Retained unchanged: the `browser shortcuts issue no map requests` assertion, the resize/shortcut diagnosis, `check_shortcuts_after_pending_resize` and the original failing-first.
