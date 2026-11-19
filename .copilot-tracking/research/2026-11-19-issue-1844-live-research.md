---
title: Issue 1844 live research (2026-11-19)
ms.date: 2026-11-19
---

Task: issue #1844, mobile map controls covered by the home summary. Owner decision 2026-11-18: demo is desktop only.

Disposition: executed. Planning Readiness: Ready (no source change planned).

Findings: every code criterion (1 to 4) is defined at 320 and 390 px widths. Source at `src/api/src/zava_forward/api/web/style.css:280` still positions `.map-home-card` absolutely; the narrow-viewport defect is real but out of demo scope. Criterion 5 covers existing map checks, with no recipe change. Criterion 6 is the delivery gate (independent review, hosted CI) the owner excluded for the demo. See docs/reference/research/issue-1844-live-20261119-2026-11-19.md.
