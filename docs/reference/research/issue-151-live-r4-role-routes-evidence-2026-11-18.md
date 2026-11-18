---
title: WCAG 2.2 Live Audit Round 4, Role Routes, for the Demo (Issue 151)
description: Live axe and keyboard scan of the nine role screens on the synthetic demo workbench, with a per-criterion proven and unproven table for issue 151
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure authorised
(resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production
change); person-run assistive-technology testing, DPO/Legal approval and billing
reconciliation are not needed for the demo. This run was read-only against
`ca-cutover-test-demo-api`. No Azure resource was created or changed, so nothing needed
deleting. Credentials were read from the owner's files at run time and never printed; a
literal scan of the retained evidence folder for each credential value found no match (observed; raw output not retained).

It extends [round 1](issue-151-live-wcag-axe-evidence-2026-11-18.md),
[round 2](issue-151-live-wcag-axe-evidence-r2-2026-11-18.md) and
[round 3](issue-151-live-r3-wcag-evidence-2026-11-18.md), which scanned the 13
navigation screens and the resident app. Browser: Playwright Chromium, 1366 by 900,
2026-11-18 between 16:33 and 16:36 UTC; axe-core 4.10.3 (tags `wcag2a`, `wcag2aa`, `wcag21a`,
`wcag21aa`, `wcag22aa`). Evidence: `.copilot-tracking/evidence/2026-11-18/issue-151-live-r4/`
(`scan2.py`, `axe-results-employee_roles.json`, redacted gzipped raw axe output).
Screenshots were deleted because role queues can show case data.

## Results: Specialist screen role aliases

The one available employee account has the role Retrofit Programme Manager. The
role-screens code shows a screen only when it is installed for the signed-in role and
otherwise renders "Screen unavailable" (`src/api/src/zava_forward/api/web/role-screens.js`,
lines 118 to 128).

| Route | Heading | axe violations | axe incomplete | Tab stops | Result |
| --- | --- | --- | --- | --- | --- |
| `#/role/building_safety_lead` | Building safety referral queue | 0 | 0 | 38 | no trap, indicator on every stop, none unnamed |
| `#/role/housing_officer` | Resident service issue queue | 0 | 0 | 38 | same |
| `#/role/contact_centre` | Resident service issue queue | 0 | 0 | 38 | same |
| `#/role/resident_engagement` | Resident choice and update queue | 0 | 0 | 40 | same |
| `#/role/procurement` | Package queue | 0 | 0 | 35 | same |
| `#/role/programme_manager` | Programme queue and connected home view | 0 | 0 | 46 | same |
| `#/role/retrofit_coordinator` | Programme queue and connected home view | 0 | 0 | 46 | same |
| `#/role/repairs` | Screen unavailable | 0 | 0 | 1 | role gate denial, as designed |
| `#/role/contractor` | Screen unavailable | 0 | 0 | 1 | role gate denial, as designed |

All nine had one `main`, a `header`, no horizontal scroll at 320 by 256, and the
shared page title `Zava Forward | Zava North Homes` (the 2.4.2 gap from round 3 still
stands). The two denial screens show that a role without access receives a plain
message with a link back; they say nothing about the repairs or contractor workflows
themselves.

`src/api` `test_accessibility_baseline` passes (18 tests) on this branch.

## Acceptance criteria

| # | Criterion | Ticked in issue | Status for the demo | Basis |
| --- | --- | --- | --- | --- |
| 1 | Target conformance level and scope decided and recorded | yes | not re-tested | [WCAG baseline](ux/wcag-conformance-baseline.md) exists |
| 2 | Audit covers keyboard, focus, name/role/value, status, contrast, reflow, target size, errors | yes | not re-tested | rounds 1 to 4 add live evidence |
| 3 | Automated checks run in CI against key screens | yes | not re-tested | existing browser checks and the baseline test pass locally |
| 4 | Manual screen-reader and keyboard checks recorded for each role workflow | no | partly proven | see below |
| 5 | Map, charts and tables have accessible equivalents (#119) | yes | not re-tested | |
| 6 | Accessibility statement draft lists known gaps | yes | not re-tested | |

Criterion 4, proven for the demo: scripted keyboard walks and axe scans of the
Programme Manager workflows (rounds 1 to 3) and of seven role screens (this round), plus
the resident app sign-in, error and signed-in states (round 3), with no trap, visible
focus and no unnamed stops.

Criterion 4, not proven: no screen reader was run, because person-run assistive
technology is excluded for the demo and a script is not a screen-reader test; the
repairs and contractor workflows and any role beyond Programme Manager were reached
only as denial screens, since no account holds those roles; the keyboard checks are
scripted rather than manual. The owner may tick the criterion for the demo on this
basis, or leave it open for production.

## Production-only items (not attempted)

* Person-run screen-reader and keyboard testing for each role with real role accounts.
* DPO/Legal approval and Azure billing reconciliation.
* Mobile devices.

## Recommended follow-ups

* Give hash routes distinct document titles (2.4.2).
* Add test accounts for repairs and contractor roles if per-role evidence is wanted.
