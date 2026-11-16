---
title: Issue 1828 review correction cycle 1 research
description: Research for the Medium PR 1829 exact-head finding on the premise check in the map browser harness
ms.date: 2026-11-16
ms.topic: reference
---

## Scope

* Correction cycle 1 of #1828 after the independent review of PR #1829 head 3a7c655603eeae861c476eca1268a0188efde9bc (base main 18d3de459f20018e91fab3af87ab0d89123661c6). Not a new change. Original research, plan, details, critique, changes, review, evidence and external witness (`rpi-1828-map-shortcuts-20261116T162749Z`) are preserved unmodified.
* Tier FOCUSED: local map browser harness `src/api/checks/map_fullscreen_browser_check.py`, one new non-browser unit test and these artifacts. No application, permission, consent, SQL, deployment, workflow or gate change.
* Sources read first: issue #1828, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/case_study_48_addendum.md`, repository instructions, the `web-design-guidelines` skill (current source fetched 2026-11-16) and the `redesign-existing-projects` skill. The harness is a Python Playwright check with no UI markup, styling or behaviour change, so the guideline rules have no web file to review. This is disclosed, not a conformance claim.

## Finding

`check_viewport_change_requests_map` (lines 123-131 at the reviewed head) wraps the resize in `page.expect_request(lambda r: "/api/map?" in r.url)`. It runs straight after `check_expanded_filters`, whose last filter click and `aria-busy` wait do not cover Leaflet's 200 ms debounced `moveend` read. A pending read from that step can fire after `set_viewport_size` and satisfy the predicate, so the premise "a viewport change still requests the map" can pass without the resize causing any read (false positive).

## Evidence

* `src/api/src/zava_forward/api/web/app.js:2744-2748`: `moveend` calls `draw(false)`, which requests `/api/map?...&zoom=Z&bbox=S,W,N,E` from `map.getBounds()`. The bbox is the current pixel viewport projected at zoom Z.
* `settle_map_reads` (existing) waits for a 400 ms quiet window with no read and no `aria-busy`, which is twice the debounce, so after it no previous-step read can still be pending.
* Web Mercator (Leaflet EPSG:3857): pixel width = (east - west) / 360 * 256 * 2^zoom. A read issued for the resized viewport therefore carries a bbox whose projected width equals the `#leaflet` client width after the resize; a read from before the resize carries the old width.
* Heavy lock at 2026-11-16T16:45Z: held by PID 4021073, `tools/rpi-checks.py --all --out /tmp/rpi-1297-mobile-full-20261116T1645Z` (#1297 full gate). It is not ours to compete for, queue on or interrupt.

## Options

| Option | Result |
| --- | --- |
| Keep `expect_request`, add only a settle | Removes the pending read but a late unrelated read could still satisfy it; no attribution |
| Settle, then require a read whose bbox width equals the post-resize container width and differs from the pre-resize width | Attributes the read to the viewport change without a baseline read; needs the container to actually change width |
| Compare bbox with the last earlier read | Needs a baseline read that may not exist (fit reads carry no bbox); rejected |

Selected: row 2. If the container width does not change with the viewport the premise is unprovable and the check fails loudly; it is never relaxed.

## Planning readiness

Ready. Research disposition: executed. Open limitation: attribution is proven on the fake page deterministically and in Chromium only once the heavy lock is free (named handoff below if still held).
