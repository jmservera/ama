---
title: Issue 128 live research
ms.date: 2026-11-18
---

## Scope

Issue #128 (accessibility, equity and journey ownership testing), synthetic demo, desktop only. Owner decisions 2026-11-18: person-run assistive-technology testing, DPO/Legal approval and billing reconciliation are not needed for the demo; Azure rg `ama`, cap USD 700, no drills. Research disposition: executed. Planning Readiness: Ready.

## Criteria state at start

* Ticked: keyboard and screen reader (deferred to production, #1907); missing data and incomplete appointments get human review; all eight RAI cohort criteria.
* Unticked: "Direct user research protocol agreed; usability measures aggregate only".

## Evidence sources identified

* `docs/reference/research/ux/equity-journey-test-plan.md` (draft protocol, agreement record blank).
* `docs/reference/research/ux/usability-test-programme-plan.md` (SA-010 gate, aggregate-only measures).
* `src/core` aggregate-only enforcement (`evaluate_role_measures`) and its tests.
* Prior live drivers in `.copilot-tracking/evidence/2026-11-18/issue-619-live/`.

## Planned proofs

1. Re-run the core unit tests for aggregate-only and audit-use gating.
2. Live desktop axe (pinned axe-core) plus Playwright on the employee workbench, a case view and the resident app; probe the deployed API route list for any per-participant research store.
3. Keep the "agreed" half unproven unless a named human agreement exists in the repository.
