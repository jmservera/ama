---
title: Issue 119 live research (opening)
ms.date: 2026-11-18
---

## Scope

Issue 119, demo scope, desktop only. Criteria: (1) provider licence, cost, coverage and processor terms recorded; (2) screen reader test of the list alternative. Planned: read deployed tile config and CSP, open the employee map with Playwright, capture list alternative and tile state, read source and docs.

## Status

Opened before substantive search. Findings are appended below as gathered.

## Findings

* Deployed `ZF_TILE_URL` is public OSM; map is on `#/overview`; 443 homes, 15 tiles loaded, no failures.
* List alternative has 443 links, keyboard path works, tile-blocked state keeps the list working.
* OSM Tile Usage Policy re-read 2026-11-18; best-effort, commercial access may be withdrawn.
* No screen reader on host; person-run AT not needed for the demo.
* Research disposition: executed. Planning Readiness: Ready. Evidence: `.copilot-tracking/evidence/2026-11-18/issue-119-live/`; note: `docs/reference/research/issue-119-live-map-evidence-2026-11-18.md`.
