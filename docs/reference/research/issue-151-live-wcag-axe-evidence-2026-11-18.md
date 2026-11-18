---
title: WCAG 2.2 Automated Evidence on the Live Demo Workbench (Issue 151)
description: Live Playwright and axe-core 4.10.3 scans plus keyboard checks of every workbench screen for the Retrofit Programme Manager role on the synthetic demo, with per-criterion status and what stays unproven
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live
Azure is authorised (resource group `ama`, cap USD 700, no drills, no Key Vault
rotation, no production change). Person-run assistive-technology testing is
production-only (#1907), so it is not attempted here. The run was read-only; no
Azure resource or setting was created or changed, so nothing needs deleting.
The test sign-in was read from the owner's files at run time and never
printed; a literal scan of every retained evidence file for each credential
value found no match. Screenshots mask e-mail addresses in the page text.

Target: `ca-cutover-test-demo-api` (Entra Easy Auth, employee workbench),
signed in as the test employee (role `Retrofit Programme Manager`, the only
employee account available). Browser: Playwright Chromium, 1366 by 900
viewport, 2026-11-18 10:05 to 10:30 UTC. The resident app `ca-resident-demo`
and other employee roles were not scanned in this run.

Evidence is under `.copilot-tracking/evidence/2026-11-18/issue-151-live/`:
`scan.py` and `common.py` (scripts), `axe-keyboard-results.json` (final
output), three earlier result files kept as adverse evidence, and one
screenshot per screen. axe-core 4.10.3 was fetched from cdnjs and its SHA-256
(`880970c0...a68bb`) matches the pin used by `src/api/checks`. Tags run:
`wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`.

## Method

For each of the 13 navigation entries returned by `/api/me` (My cases, All
cases, Overview, Progress dashboard, Visits, Funding, Finance, Capacity and
work orders, Closed cases, Assistant proposals, Time capture, Aftercare
concerns, Specialist screens) the script set the route hash, waited for the
network to settle, then recorded:

* an axe scan of the whole document (violations and incomplete results)
* a Tab walk of up to 80 stops: focus indicator present (outline or box
  shadow), element inside the viewport, a repeated-element trap test and
  whether the cycle completed
* landmark counts, `h1` text and live regions (`role=status`, `role=alert`,
  `aria-live`)
* a reflow probe: horizontal scroll at a 320 by 256 CSS pixel viewport, which
  is the 400 percent zoom equivalent of a 1280 pixel desktop

## Results

| Screen | h1 | axe violations | axe incomplete | Tab stops walked | Focus without indicator | Horizontal scroll at 320 px |
| --- | --- | --- | --- | --- | --- | --- |
| My cases | My cases today | 0 | 0 | 46 | 0 | No |
| All cases | All open cases | 0 | 0 | 10 (cycle complete) | 0 | No |
| Overview | Overview | 0 | 2 (color-contrast on 524 nodes, target-size) | 80 (cap) | 0 | No |
| Progress dashboard | Progress dashboard | 0 | 1 (color-contrast on 168 nodes) | 15 | 0 | No |
| Visits | Visits coming up | 0 | 0 | 39 (cycle complete) | 0 | No |
| Funding | Funding applications | 0 | 0 | 80 (cap) | 0 | No |
| Finance | Finance queue | 0 | 0 | 15 (cycle complete) | 0 | No |
| Capacity and work orders | Capacity and work orders | 0 | 0 | 62 | 0 | No |
| Closed cases | Closed cases | 0 | 0 | 30 | 0 | No |
| Assistant proposals | Role-owned assistant proposals | 0 | 1 (color-contrast on 5 nodes) | 22 (cycle complete) | 0 | No |
| Time capture | Staff time capture | 0 | 0 | 0 | none to test | No |
| Aftercare concerns | Aftercare concerns | 0 | 0 | 2 (cycle complete) | 0 | No |
| Specialist screens | Specialist screens | 0 | 0 | 13 (cycle complete) | 0 | No |

Across all screens: zero axe violations on the WCAG 2.0 to 2.2 A and AA tag
set, one `main`, one `header` and at least one `nav` landmark each, one `h1`
each, and status and alert live regions present on every screen. No keyboard
trap was found. Document title is the same on every route
(`Zava Forward | Zava North Homes`); this is a finding to review against the
page-titled criterion for hash routes (WCAG 2.4.2), not an axe result.

## Limits and adverse observations

* axe reported `color-contrast` as incomplete on three screens (524, 168 and 5
  nodes) because it could not resolve the background. Contrast on those nodes
  is therefore not proven by this run. The Overview also left `target-size`
  incomplete.
* Time capture exposed no focusable control for this role and state, so no
  keyboard walk was possible; whether a populated state has controls was not
  tested.
* The Tab walk used the first page state only. Dialogs, open case detail,
  filter results, forms with errors and status announcements were not
  exercised, so error identification and status-message behaviour (4.1.3) are
  not proven beyond the presence of live regions.
* Three scripted-heuristic false positives were corrected and the earlier
  outputs kept: run 1 flagged repeated button names as a trap, run 2 flagged
  normal Tab wrap-around, and run 3 flagged segmented date inputs (the focused
  element stays the same across segments). The final rule flags a trap only
  after more than five consecutive presses on one element.
* The scan checks one role. Other role workflows (building safety, finance
  roles, quality) are behind the Specialist screens and other accounts that
  were not available.
* Automated checks are not conformance evidence. No screen-reader output was
  tested.

## Acceptance criteria

The only unticked criterion of #151 is the manual screen-reader and keyboard
check recorded for each role workflow. Ticked criteria were not re-tested.

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 4 | Manual screen-reader and keyboard checks are recorded for each role workflow | Partly proven (keyboard and axe, one role only); screen reader unproven | Keyboard Tab walks with focus indicator, no trap and 320 px reflow, and axe 4.10.3 with 0 violations, recorded for all 13 screens of the Programme Manager role. Screen-reader testing is person-run assistive technology, production-only (#1907). Other roles were not signed in. Keep the criterion unticked |

Criteria 1, 2, 3, 5 and 6 are already ticked and are unchanged. This evidence
corroborates criterion 3 (automated checks) against the live deployment as well
as CI.

## Recommended follow-ups

* Investigate the three incomplete `color-contrast` results with a manual
  contrast sample, and the single document title across routes.
* Extend the same scan to the other roles when test accounts exist, and to
  dialog, error and status states.

## Evidence limits

* The Time capture screen was in its error state ("could not load") during the scan, so its 0 violations does not describe a loaded page.
* Adverse, omitted from the results table: the keyboard walk recorded off-screen focus stops (21 on Capacity, 3 on Closed, 2 on Progress, 1 each on All cases and Overview).
* Most screenshots were taken after the Tab walk and are scrolled; they do not show the page heading.
* The JSON and one screenshot show the synthetic employee persona display name (Aadi Kapoor), already used across the repository evidence; no real account detail is retained.
* Independent exact-head review and hosted CI are outstanding; no criterion is ticked.
