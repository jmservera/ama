---
title: Issue 1248 saved-call History browser readiness plan
description: Prospective plan to prove the cause of the R4 History assertion failure before any test-readiness repair
ms.date: 2026-11-07
ms.topic: reference
---

## Objective

Establish whether the R4 failure at `case_journey_browser_check.py:750` is a checker readiness race or an application defect, then apply only the smallest behaviour-preserving repair in the proven owner. Root cause is unproven at plan time.

## Context

* [Research](../../research/2026-11-07/issue-1248-browser-readiness-research.md), [phase details](../../details/2026-11-07/issue-1248-browser-readiness-details.md), [critique](../../challenges/2026-11-07/issue-1248-browser-readiness-critique.md).
* Tier: FOCUSED tooling/test. Reassess before implementation if the owner proves to be application code.
* Heavy lock: all browser execution under the sole non-queued shared heavy lock at admission; none is run in this turn.

## Phases

* [ ] Phase 1: Controlled synthetic delayed-refresh reproduction (no fix yet)
  * Add a focused scenario that holds the `GET /api/cases/ZF-1` read issued after Save and records, before release, that `#outcome` is empty and History lacks the call (the old readiness condition's observation).
  * Release the read; record whether the call appears in the replaced workspace (H1) or never appears (H2).
  * Run the unchanged check once at base to record whether R4 reproduces or is bounded "not reproduced".
* [ ] Phase 2: Cause gate
  * Record the proven cause and the correct completion signal. If H2 holds, stop, report attribution and open a separate scope; do not repair the application here.
* [ ] Phase 3: Repair (only if H1 is proven)
  * Replace the one-shot `inner_text()` read with: workspace detach wait, `tab(page, "History")`, `expect(...).to_contain_text("Unsaved synthetic call")`.
  * Keep the focused regression so it fails under the old condition and passes under the repair; leave every other draft, persistence, keyboard and axe check unchanged.
* [ ] Phase 4: Validation at admission
  * Run the existing full `checks.case_journey_browser_check`, relevant focused unit/static checks (`python3 tools/rpi-checks.py --changed`) and record actual exits and source identities.
* [ ] Phase 5: Evidence and review
  * Commit dated changes and Review artifacts, then independent exact-head assessment; Review runs once and findings route to later work.

## Dependencies and Gates

* Phases are ordered; Phase 3 depends on the Phase 2 cause gate.
* Each phase beyond this prospective turn is admitted separately by the coordinator.
* No retry, fixed sleep, blanket timeout, skip or weaker assertion. No SQL, Azure, model, private data, push, PR or acceptance tick without separate authority.

## Success Criteria

* R4 negative evidence preserved; reproduction recorded or bounded as not reproduced.
* Cause and completion signal proven before the fix; application and checker ownership distinguished.
* Regression fails under the old condition and proves exact History content under the repair.
* Existing full case-journey check passes with all strict checks retained.
* Research, plan, details, critique, changes and Review committed with independent exact-head assessment.
