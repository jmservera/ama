---
title: Live task queue hazard clock and owner evidence for issue 76 (demo)
description: Recorded run on 2026-11-18 against the live demo workbench for the one unticked criterion of issue 76, hazard and safeguarding items showing a clock and named owner
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 76
  - hazard clock
  - named owner
  - case card
estimated_reading_time: 4
---

Refs #76. Scope is the synthetic desktop demo, authorised by the owner on 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Nothing here is production evidence. Production-only parts stay deferred to #1905 to #1908. The checks were read-only: no Azure resource, setting or data was changed and nothing was created, so nothing needed deleting.

## Method

* Target: `ca-cutover-test-demo-api` (Easy Auth with Entra). Playwright Chromium, 1366 by 1000 desktop viewport, signed in as the employee test account (role Retrofit Programme Manager). Credentials were read from the owner's files at run time and never printed or stored; the retained scripts contain no credential.
* Calls: `GET /api/cases` (16 cases) and `GET /api/cases/ZF-2025-0331`, then the case card opened in the browser at `/app#/case/ZF-2025-0331`.
* Local tests on this branch: `src/api` `test_workbench_hazard_clock_owner`, `test_safeguarding_clock_a11y` and `test_safeguarding_detail_boundary` (9 tests) and `src/core` `test_taskqueues` (29 tests) passed. These pass whether or not the demo data holds a timestamp, so they do not prove the live clock.
* Evidence files are in `.copilot-tracking/evidence/2026-11-18/issue-76-live/`: scripts, `proof-run1.json`, `ui-run2.json`, `ui2-run1.json` and screenshots `hazard-case-card.png`, `hazard-safety-block.png` and `queue-default.png`. The failed first UI run (`ui-run1-failed-scroll.err`, a visibility timeout in my script) is kept.

## Per-criterion result

| Criterion in #76 | Result | Evidence |
| --- | --- | --- |
| Hazard and safeguarding items show a clock and named owner | Partly proven for hazards; safeguarding unproven | See below |

Observed for the only hazard case in the demo (`ZF-2025-0331`, Damp and mould, Significant):

* The case card block "Safety referrals and stopped retrofit work" shows a "Safety clock" line and an "Accountable owner" of `Karen Lawson`. The API `work.hazard_clocks[0]` returns `owner_named: true` and `owner_status` "Named follow-up owner recorded."
* The clock text is "Hazard clock: elapsed time unknown; no response target window recorded; response unknown." `aware_at`, `response_due_at` and `elapsed_hours` are unknown or null in the imported record. So a clock element and a named owner are displayed, but no running or elapsed clock is shown, because the synthetic record has no awareness timestamp or target.
* The same case shows "Zava coordinator: Not assigned yet", a separate coordinator role from the named accountable owner.
* The `.safety-clock` paragraph also appears in the collapsed "Recorded task context" panel with the same values; the visible clock is the one in the safety block.

## What this does not prove

* Safeguarding: none of the 16 demo cases has a safeguarding item (`safeguarding_items` empty, `work.safeguarding_clocks` empty), so the safeguarding clock and owner are not shown live. Proving them needs a record the demo does not hold; creating one would change demo data, which this docs-only task did not do. The local tests cover the rendering.
* A computed elapsed time and a target window against a real timestamp are unproven live, for the reason above. Whether the criterion allows "unknown" as a displayed clock is a product decision for the issue owner.
* Hazard and safeguarding clock authority stays with the existing hazard and repairs service; production confirmation remains with #1905 to #1908.
* The six ticked criteria were not re-opened.

## Evidence limits

* Names are synthetic demo staff. The screenshots show the first name of the signed-in account only.
* One hazard case is a thin sample; results do not generalise to other data.

## Evidence limits

* `hazard-case-card.png` and `hazard-safety-block.png` are byte-identical top-of-card captures and do not show the safety clock or accountable owner lines.
* The test counts (9 and 29) have no retained output.
* A signed-in session file was created under /tmp during the probe, outside the repository, and is deleted; none is retained.
* Independent exact-head review and hosted CI are outstanding; no criterion is ticked.
