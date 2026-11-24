---
title: Issue 149 live r3 research
ms.date: 2026-11-23
---

# Research opened

Epic #149, third live run today. Unticked criteria: (1) #440 stabilization checkpoint, owner-gated; (2) child features accepted. Earlier runs: docs recheck (2026-11-19) and a law-viewer reflow fix (r2). Open defect carried in #440 comments: a map browser check strict-mode failure on two `[role=status]` elements. This run probes that defect and a live desktop render of both demo apps.

Disposition: executed. Planning Readiness: pending findings.

## Findings (2026-11-23 23:50Z)

* `python3 -m checks.map_tile_status_browser_check` (from `src/api`, `PYTHONPATH=src:.:../core/src:../agents/src`) fails: `expect(".map-info [role=status] + [role=status]").to_have_count(1)` sees 0.
* Cause: `app.js:3174` orders the sidebar `info, retry, tileNote`. A hidden retry button (added in batch d4, commit 5dfa7312d5) now sits between the two status paragraphs, so the adjacent-sibling selector in `tile_notice` is stale. The page is correct; the check is defective. This is the defect recorded in #440 comments.
* Fix: select the tile note as the status that does not match the count pattern (`filter(has_not_text=COUNT_NOTICE)`), independent of sibling order. `tests/test_map_status_locators.py` stays valid; the manifest recipe SHA does not cover this file.
* Criteria 1 and 2 stay owner-gated (as in r2 and the 2026-11-19 note).

Planning Readiness: Ready.
