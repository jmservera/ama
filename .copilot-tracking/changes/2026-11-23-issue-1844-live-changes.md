---
title: Issue 1844 live close-out changes
description: Changes record and per-criterion table for #1844
ms.date: 2026-11-23
---

No source file changed; the implementation gap check found none. Tier: Focused (documentation, tracking evidence and a read-only probe script; no `src`, workflow, dependency, deployment or gate change).

## Changes

* Added `docs/reference/research/issue-1844-live-20261123-2026-11-23.md` and `mobile-map-summary-1844-live-2026-11-23/` (logs, screenshots, `live_probe.py`, `live-probe.json`).
* Updated `docs/reference/README.md` index and appended `docs/reference/log.md`.
* Dated RPI artifacts under `.copilot-tracking/`.
* Temporary removal of `style.css:514` for the failing-first run was restored; `git diff` on `src/` is empty.

## Divergences

The live probe script was added to the research folder as reproducible evidence. Live marker hit tests proved inconclusive (dense stacked markers) and are reported as such.

## Per-criterion table

| # | Criterion | Result |
| --- | --- | --- |
| 1 | Failing-first regression with served-byte identity | Proven |
| 2 | Four viewports, both tile states, pointer and keyboard | Proven on synthetic harness (8 states, 0 of 5 covered); live partly proven (320x568, 390x568 and 1280x900 only; zoom controls 0 of 2 covered; live markers inconclusive) |
| 3 | Escape, Close, another home, expand/collapse/reopen; desktop; overflow | Proven on harness; live checked for overflow and desktop position only |
| 4 | Attribution after scrolling | Proven on harness; live screenshot visible at 390x568 |
| 5 | Existing map browser and axe checks, zero skips, manifest | Proven (436 pass, 0 skips, axe 0 violations); manifest not applicable; 14 axe-incomplete contrast items recorded, no conformance claim |
| 6 | Dated RPI artifacts, tier, independent review, hosted CI | Partly proven; independent exact-head review and hosted CI owner-gated (no push permitted) |
