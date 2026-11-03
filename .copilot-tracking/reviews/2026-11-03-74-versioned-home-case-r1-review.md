---
title: Issue 74 round 1 review
ms.date: 2026-11-03
---

Review executed once, by the implementing agent against the diff (not independent). Outcome: conformant for the slice scope; independent exact-head review is still required.

## Findings

* No open material findings in core logic. Versions are append-only through the provenance writer; contractors are refused; sibling evidence does not appear in another home's links.
* Routed later work: API routes, web screen (Fluent 2, WCAG, plain language), building-record versioning, MSSQL parity for `schemes`, scheme register authoring.

## Acceptance criteria

| Criterion | Status |
| --- | --- |
| 1 Version and links | Met in core only; no API or UI evidence |
| 2 Building items apart from home evidence | Met in the core view (and by #75 on the building screen); no UI |
| 3 Shared ID never transfers evidence or approval | Met in core; tested on view and version recording |
| 4 Prior versions retained | Met for home-case links in core; building records are not versioned |

All four remain only partly proven end to end (no API, UI, browser or hosted evidence), so the PR uses Refs #74.
