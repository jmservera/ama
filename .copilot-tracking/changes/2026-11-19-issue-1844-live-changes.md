---
title: Issue 1844 live changes
ms.date: 2026-11-19
---

Added the research note [issue-1844-live-20261119-2026-11-19.md](../../docs/reference/research/issue-1844-live-20261119-2026-11-19.md), a knowledge-base log entry and these RPI artifacts. No src change; tier focused (documentation).

| Criterion | Status | Basis |
| --- | --- | --- |
| 1 failing-first regression with served-byte identity | Unproven, out of demo scope | Needs the narrow-viewport browser regression |
| 2 four viewports, both tile states, hit tests | Unproven, out of demo scope | Mobile widths excluded |
| 3 focus and selection flows, no overflow | Unproven, out of demo scope | Narrow layouts excluded |
| 4 attribution after scroll at short heights | Unproven, out of demo scope | Short mobile heights excluded |
| 5 existing map browser/axe checks | Not applicable | No recipe or source change |
| 6 RPI artifacts, independent review, hosted CI | Partly proven | Dated artifacts delivered; independent review and CI excluded for the demo |

Result: no criterion is unmet for the desktop-only demo.
