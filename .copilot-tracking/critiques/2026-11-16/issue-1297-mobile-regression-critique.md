---
title: "Issue 1297 320px summary-bottom regression critique"
ms.date: 2026-11-16
---

## Execution

Critique executed once, on the final candidate plan, by the RPI worker (self-critique; independent exact-head review stays with the coordinator). Verdict: proceed with amendments applied.

## Findings and dispositions

* Alternative: keep 1700 with a justification. Rejected by the owner; the limit is design acceptance.
* Alternative: restructure the header so the account control sits beside the brand. Larger visual change than a targeted fix. Rejected; only gap and padding change.
* Risk: smaller link padding reduces touch targets. Disposition: height is governed by `min-height:2.5rem` (unchanged) and the gap stays at `var(--sp-1)`; the browser check now asserts at least 24x40 px per link at 320px. Width at 320px is text-driven and well above 24px.
* Risk: the CSS-only test could restate the implementation. Applied: it is paired with the real browser measurement at the restored 1600 limit, which is the behavioural proof.
* Risk: desktop regression. None: the change is inside max-width 600px only.
* Residual: the full gate result is pending until the heavy lock is free.
