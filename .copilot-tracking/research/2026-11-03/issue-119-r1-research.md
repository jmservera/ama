---
title: Issue 119 r1 research
ms.date: 2026-11-03
---

## Disposition and readiness

Research disposition: reused. Planning Readiness: Ready.

## Evidence

* Merged PRs: #426 (provider options comparison, draft proposal), #458 (demo-only OSM basemap configuration). The closure audit of 2026-10-31 records both criteria unmet and no new ticks.
* Criterion 1 (licence, cost, coverage, processor terms recorded) needs owner selection, procurement, DPO and legal approval; no agent may supply it.
* Criterion 2 (screen reader test) needs a human with NVDA or VoiceOver; the protocol already exists in the WCAG baseline. The host has no screen reader.
* Gap found: `mapPanel()` had no tile-error handler (stated in the protocol), so a failed tile background gave no signal while the list alternative stayed usable.

## Slice choice

Smallest coherent engineering slice: announce tile failure politely and point to the list alternative. It advances the accessible-alternative behaviour but proves neither criterion.

## Later slices

* Slice 2 (human): screen-reader run record against the protocol.
* Slice 3 (human): provider decision record after owner, DPO, procurement and legal approval.
