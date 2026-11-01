---
title: Issue 233 research, atlas trace refresh
ms.date: 2026-11-01
---

## Disposition and readiness

Research disposition: executed (desk and repo). Planning Readiness: Ready.

## Evidence

* PR 671 (merged) delivered `docs/reference/research/ux/atlas-screen-trace.md`, `atlas_screen_trace.py` and tests. PR 495 closed; PR 496 merged (#149 foundation).
* Snapshot at 2026-11-01 (origin/main == HEAD): PRs 652, 653, 654, 655, 657 merged; 656 (technical-queue, quality-queue) and 662 (programme-queue) open.
* `role-screens.js` on main registers: asset-board, resident-choice, safety-lead, hazard-triage, data-operator, procurement-packages, contractor-job-pack, finance-invoices, finance-funding. Not on main: programme-queue, technical-queue, quality-queue.
* The trace still says only asset-board is on main, so its status column is stale.
* `procurement-packages` renders offered, recorded committed, in use and headroom columns; no screen text "Not shown for this role" exists, so tension rules stay proposed.

## Criteria status before this slice

* Hypothesis label: met (PR 671).
* Perspective/theme trace, tensions, same-home walk: delivered as design-level trace; screens partly unmerged. Stay unticked.
* WCAG 2.2 (#151) and design system (#150) evidence: not available; needs CI/AT and human review.

## Remaining slice

1. Refresh trace status to match main.
2. Add a drift test: screens the trace labels "main" must be registered in `role-screens.js`, and unmerged ones must not be.
3. No Azure-live work, no new mvp/prototype code.
