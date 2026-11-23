---
title: Issue 1844 live close-out research (2026-11-23)
description: Re-proof of #1844 criteria on main and live revisions
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* The fix is already on `main` (`21b810439f`, #2155; regression `check_narrow_summary_clearance`). `style.css` and the check are unchanged since the 2026-11-22 audit, so no code gap exists.
* Live API revision `ca-cutover-test-demo-api--0000054` (healthy, 100 percent) serves `app.js` `ebb1a9f911d75141` and `style.css` `e85bd0ee84802c7e`, equal to `main`. The resident app (0000026) has no map.
* Narrow-viewport live probe: summary static, no map overlap, zoom controls uncovered, no overflow. Dense live markers make marker hit-tests inconclusive even on desktop.
* Criterion 6 depends on a push for independent review and hosted CI, which the brief forbids.

## Evidence

Canonical note: [docs/reference/research/issue-1844-live-20261123-2026-11-23.md](../../docs/reference/research/issue-1844-live-20261123-2026-11-23.md).

## Planning Readiness

Ready: documentation-only deliverable, Focused tier (no `src` change).
