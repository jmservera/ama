---
title: WCAG 2.2 Live Audit Round 3 for the Demo (Issue 151)
description: Second live audit of the synthetic demo adding the resident app, a contrast heuristic, page titles and a keyboard case-open check, with per-criterion status for issue 151
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure authorised
(resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production
change); person-run assistive-technology testing, DPO/Legal approval and billing
reconciliation are not needed for the demo. The run was read-only. No Azure resource
was created or changed, so nothing needed deleting. Sign-in credentials were read from
the owner's files at run time and never printed; a literal scan of every retained
evidence file for each credential value found no match. The retained screenshots show only the public sign-in page.

It extends [the first](issue-151-live-wcag-axe-evidence-2026-11-18.md) and
[second](issue-151-live-wcag-axe-evidence-r2-2026-11-18.md) live notes, which
scanned 13 employee screens for the Retrofit Programme Manager role. Browser:
Playwright Chromium, 1366 by 900, 2026-11-18 about 15:28 to 15:40 UTC; axe-core 4.10.3
(SHA-256 pinned, matching `src/api/checks`), tags `wcag2a`, `wcag2aa`, `wcag21a`,
`wcag21aa`, `wcag22aa`. Evidence: `.copilot-tracking/evidence/2026-11-18/issue-151-live-r2/`
(`probe.py`, `probe_employee.py`, `contrast_detail.py`, result JSON, two resident sign-in screenshots). The signed-in resident and employee case screenshots were not retained because they showed a home address and contact details; the signed-in results rest on the JSON only. The scripts expect the pinned axe file next to them as `axe.min.js` (hash in `axe-4.10.3.sha256`); the file itself is not committed.

## Results

### Resident app (`ca-resident-demo`)

| State | axe violations | axe incomplete | Keyboard | Notes |
| --- | --- | --- | --- | --- |
| Sign-in | 0 | 1 (`aria-valid-attr-value`) | 5 stops, no trap, indicator on every stop, skip link first | document title is the page title, `lang=en-GB` |
| Empty-submit error | 0 | 1 (same) | focus moved to the email field | error is `role=alert`, field has `aria-invalid=true` and `aria-describedby` pointing at the error |
| Signed in (sign-in completed by keyboard Enter) | 0 | 2 (`aria-valid-attr-value`, `color-contrast` on 8 nodes) | 7 stops, cycle completed, no trap, indicator on every stop | one `main`, `header`, `nav`, one `h1`; seven live regions (status, alert, log); no horizontal scroll at 320 by 256 |

The heuristic contrast sample (computed foreground over resolved background, 284 text
nodes) found 0 below 4.5:1 (3:1 for large text) on the signed-in resident page. This
resolves the eight axe-incomplete nodes only as far as a script can; it is not a
formal contrast audit.

### Employee workbench, Programme Manager role (`ca-cutover-test-demo-api`)

* Page titles: every route has the same title, `Zava Forward | Zava North Homes`,
  while the `h1` changes per route (13 of 13). This remains a finding against WCAG
  2.4.2 for hash routes; it is a gap, not a pass.
* Contrast heuristic over all 13 screens (about 5,000 text nodes): 15 nodes below
  the threshold, all on Capacity (3) and Assistant proposals (12). Inspection of
  those nodes shows each is a `disabled` button (`rgb(107,116,123)` on
  `rgb(236,239,241)`, 4.12:1). Disabled controls are exempt from 1.4.3, so no
  failing active text was found. The Overview, Progress and Assistants axe
  `incomplete` contrast results are therefore not shown to be failures; they stay
  incomplete in axe terms.
* Keyboard open of a case: Tab to the first case link and Enter opened
  `#/case/ZF-2025-0029`; focus moved into the main region; axe on the case view
  reported 0 violations and 0 incomplete; a 17-stop Tab walk had no trap, no
  missing focus indicator and no unnamed control. No dialog was open.

## Limits and adverse observations

* The resident results are in `probe-results-run1-employee-signed-out.json` (the file name refers to its invalid employee half). The first employee probe ran against the signed-out welcome page because it
  navigated to `/` instead of `/app`; its output is kept as
  `probe-results-run1-employee-signed-out.json` and is not used.
* Resident keyboard walk flagged two unnamed inputs on sign-in and seven stops
  outside the viewport once signed in. The name check reads `aria-label` and text
  only, so label-associated inputs may be counted as unnamed; the viewport flag
  follows page scroll. Neither was investigated further.
* Only one employee role and one resident account were available. Other role
  workflows (building safety, finance roles, quality) were not exercised.
* No screen reader was run. Automated and scripted checks are not conformance
  evidence and do not satisfy the manual-testing criterion.

## Acceptance criteria

Criteria 1, 2, 3, 5 and 6 are already ticked and were not re-tested here.

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 4 | Manual screen-reader and keyboard checks are recorded for each role workflow | Keyboard: partly proven (Programme Manager 13 screens plus case open, resident sign-in, error and signed-in states); screen reader: unproven; other role workflows: unproven | Scripted keyboard walks and axe results above and in the first note. Screen-reader testing is person-run assistive technology, excluded for the demo by owner decision and a production-only item (#1907). Other roles need accounts that do not exist in the demo. Criterion stays unticked. |

Production-only items (not attempted): person-run screen-reader testing, DPO/Legal
approval, Azure billing reconciliation, mobile devices.

## Recommended follow-ups

* Give hash routes distinct document titles (2.4.2).
* Add resident and dialog states to the browser checks under `src/api/checks`.
* Extend the scan to other employee roles when test accounts exist.
