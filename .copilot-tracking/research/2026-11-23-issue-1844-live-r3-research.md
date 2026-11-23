---
title: Issue 1844 live r3 research (2026-11-23)
description: Re-verification of #1844 after live API revision 0000055
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Live revision is `ca-cutover-test-demo-api--0000055` (r2 cited 0000054). Served `app.js` and `style.css` hashes are unchanged (`ebb1a9f911d75141`, `e85bd0ee84802c7e`).
* Harness on head `9dbfab6f56`: 436 PASS, 0 FAIL, 0 skips; eight narrow states show 0 of 5 controls covered.
* Live probe at 320x568 and 390x568: static summary, no map overlap, 0 of 2 zoom controls covered, no overflow; desktop card absolute.
* Criterion 6 (independent review, hosted CI) needs a push and stays owner-gated.
* Evidence: [issue-1844-live-r3-2026-11-23.md](../../docs/reference/research/issue-1844-live-r3-2026-11-23.md).
