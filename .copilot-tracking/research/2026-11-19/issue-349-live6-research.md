---
title: Issue 349 live6 research
ms.date: 2026-11-19
---

## Task

Refs #349. Pick the first unticked criterion that can be proven or built for the synthetic demo
with code and tests; otherwise state that and stop. Owner decisions of 2026-11-18 apply.

## Evidence reviewed

* Round 5 note `docs/reference/research/issue-349-tenant-prerequisites-live-r5-2026-11-19.md`
  (and rounds 3 and 4): Easy Auth, vault reference, private endpoint, positive `/api/cases` 200,
  logout and re-login proven; Graph reads denied; resident-account sign-in failed twice in the browser.
* Issue comments to 2026-11-05: no ticks inferred; criteria remain conjunctive.

## Per-criterion feasibility

| # | Feasible for the demo with code and tests? | Reason |
| --- | --- | --- |
| 1 | No | Needs Application Administrator rights; Graph reads are denied to the demo login |
| 2 | Already proven in r5 | Read-only; no code to add |
| 3 | No | Prior callback list unreadable; edge tooling already exists and is tested |
| 4 | No | No owner-supplied roster; demo admits by Entra identity and app role |
| 5 | No | Wrong-role denial needs a second-role account signing in; resident sign-in failed twice |
| 6 | Already proven with qualification | No code gap |

Planning Readiness: Ready (conclusion is stop, no source change). Research disposition: reused.
No new live Azure call was made, so nothing was created and nothing needs deleting.
