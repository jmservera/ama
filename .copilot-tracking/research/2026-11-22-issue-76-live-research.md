---
title: Issue 76 live research (2026-11-22)
ms.date: 2026-11-22
---

Refs #76. Research disposition: executed. Planning Readiness: Ready.

## Findings

* Only criterion 5 is unticked: hazard and safeguarding items show a clock and a named owner. Prior rounds (r4, r6) proved the owner and a safeguarding clock live and left hazard time values Unknown.
* Root cause found this round. `taskqueues.context()` builds the queue and case-card `work.hazard_clocks` and `work.safeguarding_clocks` from `hazard_clock()` and `safeguarding_clocks()`. Neither calls `project_safety_clock_and_owner()`, so `clock_label`, `clock_status`, `clock_remaining_hours`, `clock_deadline_utc`, `named_owner`, `owner_role` and the escalation owner never reach the queue rows. `app.js` `workSummary` already reads those fields, so the "time remaining or overdue against target" text never renders. Only the hazard list on the case card (via `workflows._apply_safety_enrichment`) carries them.
* Live probe (revision `ca-cutover-test-demo-api--0000047`, staff test account, read-only, secrets not printed): hazard `ZF-2025-0331` has `noticed` 2025-12-21 and `aware_at` null; its enriched record reports `clock_status` fail-closed. Dataset `as_of` is 2026-10-16. The synthetic dataset is outside the repository and is not changed here.
* `test_hazard_safeguarding_clock_owner_76.py` deliberately fails closed when only a date `noticed` exists, so that behaviour stays; the product will state what is missing and the next action instead of a silent Unknown.
* `clockSummary` prints a negative number as "N h remaining" for overdue items; this is not plain language.

## Decision

Wire the existing projection into the queue clocks, render plain time remaining or overdue text, state the fail-closed reason with a next action. No Azure change; live proof of new code needs a deploy, which is out of scope, so the live criterion proof is the pre-change probe plus a local Playwright proof on synthetic data.
