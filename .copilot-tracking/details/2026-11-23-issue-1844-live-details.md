---
title: Issue 1844 live close-out details
description: Phase details for the 2026-11-23 plan
ms.date: 2026-11-23
---

## Phase 3

* Run `checks.map_fullscreen_browser_check` from `src/api` with the worktree on `PYTHONPATH` (the editable install points at another checkout) and the pinned axe 4.10.3.
* Run the failing-first variant by removing `style.css:514` temporarily, then restore.
* Run the live probe script and keep screenshots under `docs/reference/research/mobile-map-summary-1844-live-2026-11-23/`.
* Update the knowledge-base index and log.

## Phase 4

One Review of the final diff; local commit with `Refs #1844`.
