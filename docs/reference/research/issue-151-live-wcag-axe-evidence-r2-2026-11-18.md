---
title: WCAG 2.2 Automated Evidence on the Live Demo, Round 2 (Issue 151)
description: Second live axe-core 4.10.3 and keyboard scan of the employee workbench and the resident demo app, with raw axe output retained, contrast incompletes resolved by sampling, adverse results kept, and a per-criterion proven or unproven table
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Refs #151. Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live Azure is authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Person-run assistive-technology testing, DPO and Legal approval and billing reconciliation are not needed for the demo. The run was read-only: no Azure resource was created or changed, so nothing needs deleting, and no source changed. Credentials were read from the owner's files at run time and never printed. A literal scan of every retained evidence file for each credential value found no match. E-mail addresses and GUIDs are replaced by `[email]` and `[guid]` in the retained JSON and the page text in screenshots is masked for e-mail addresses.

This round extends [the first live note](./issue-151-live-wcag-axe-evidence-2026-11-18.md), which kept only slim axe output and left three contrast results incomplete.

Targets and window: `ca-cutover-test-demo-api` (Entra Easy Auth) as the test employee, and `ca-resident-demo` as the synthetic resident account, Playwright Chromium 1366 by 900, 2026-11-18 about 12:50 to 13:10 UTC.

Evidence is under `.copilot-tracking/evidence/2026-11-18/issue-151-live-r2/`: `scan2.py` (script), `axe-results-employee.json` and `axe-results-resident.json` (summaries), 16 `raw-axe-*.json.gz` files (raw axe violations and incomplete results per screen, redacted), `screen-*.png`, `trap_probe.py` and `adverse-run1/` (the first employee run kept unchanged). axe-core 4.10.3 SHA-256 `880970c0...a68bb` matches the pin in `src/api/checks`. Tags: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. Passes and inapplicable rules were not retained; the raw files hold violations and incomplete only.

## Results

Employee workbench (role from `/api/me`: Retrofit Programme Manager, 13 navigation entries, the only employee account available) plus one case detail view.

| Screen | axe violations | axe incomplete | Tab stops walked | Focus stops without indicator | Horizontal scroll at 320 px |
| --- | --- | --- | --- | --- | --- |
| My cases | 0 | 0 | 46 | 0 | No |
| All cases | 0 | 0 | 10, cycle complete | 0 | No |
| Overview | 0 | 2 (`color-contrast` 524 nodes, `target-size` 0 nodes) | 120 (cap) | 0 | No |
| Progress dashboard | 0 | 1 (`color-contrast` 168 nodes) | 15, cycle complete | 0 | No |
| Visits | 0 | 0 | 39, cycle complete | 0 | No |
| Funding | 0 | 0 | 120 (cap) | 0 | No |
| Finance | 0 | 0 | 15, cycle complete | 0 | No |
| Capacity and work orders | 0 | 0 | 102 | 0 | No |
| Closed cases | 0 | 0 | 30, cycle complete | 0 | No |
| Assistant proposals | 0 | 1 (`color-contrast` 5 nodes) | 22, cycle complete | 0 | No |
| Time capture | 0 | 0 | 0 | none to test | No |
| Aftercare concerns | 0 | 0 | 2, cycle complete | 0 | No |
| Specialist screens | 0 | 0 | 13, cycle complete | 0 | No |
| Case detail (`#/case/ZF-2025-0331`, new) | 0 | 1 (`color-contrast` 1 node) | 37, cycle complete | 0 | No |

Resident demo app (`ca-resident-demo`, new):

| Screen | axe violations | axe incomplete | Tab stops walked | Horizontal scroll at 320 px |
| --- | --- | --- | --- | --- |
| Sign-in form | 0 | 1 (`aria-valid-attr-value`, 1 node) | 5 | No |
| Signed-in home | 0 | 2 (`aria-valid-attr-value` 1 node, `color-contrast` 8 nodes) | 7, cycle complete | No |

Every screen has one `main`, one `header` and at least one `nav` (none on the resident sign-in form), `lang` is `en-GB`, and at least three status, alert or `aria-live` elements exist on every screen (counts only; announcements were not exercised). No keyboard trap was found in the final run.

### Contrast incompletes resolved by sampling

axe could not resolve the background for the `color-contrast` incompletes. A script computed foreground and composited background colour from computed styles for every incomplete node and applied the 4.5:1 (3:1 for large text) thresholds.

| Screen | Nodes sampled | Unresolved | Below threshold | Lowest ratio |
| --- | --- | --- | --- | --- |
| Overview | 524 | 0 | 0 | 4.66 |
| Progress dashboard | 168 | 0 | 0 | 15.52 |
| Assistant proposals | 5 | 0 | 0 | 21 |
| Case detail | 1 | 0 | 0 | 9.4 |
| Resident home | 8 | 0 | 0 | 15.52 |

This closes the first note's contrast gap for these nodes under the sampler's method (below). It is a computed-style estimate, not a manual measurement of rendered pixels.

## Adverse and corrective observations

* Run 1 of this round (`adverse-run1/`) failed on Overview with a JSON serialisation error (axe returned an Error object for one incomplete rule) and flagged the case detail view as a keyboard trap. A probe (`trap_probe.py`) showed the focused element was the native `datetime-local` input `hz-aware`, which takes six Tab presses for its segments and then leaves to the next control on press 23. It is not a trap. This is the same false-positive class as run 3 of the first note; the trap threshold was raised from 5 to 8 consecutive presses and the scan rerun in full.
* The document title is `Zava Forward | Zava North Homes` on all 14 employee routes. Hash routes do not change it, so WCAG 2.4.2 (page titled) is not proven and is a finding to review. The resident app title is "Your home improvement progress - synthetic showcase, not live".
* Funding and Overview hit the 120-stop cap, so those walks did not complete a cycle.
* The resident home walk recorded 7 of 7 focus stops outside the initial viewport and 1 stop without a derived name; the script cannot say whether the content scrolls into view on focus. Capacity had 21 and case detail 9 stops with no derived name. The name is derived from `aria-label`, text, title or placeholder only, so icon links named by an image `alt` are counted as unnamed. axe reported no name-role-value violation on those screens, but the unnamed counts are unresolved.
* The resident incomplete `aria-valid-attr-value` is the chat launcher: axe could not confirm that `aria-controls="resident-chat"` exists while the dialog is closed.
* Time capture exposed no focusable control for this role and state, so the keyboard walk had no stops there. Whether the screen loaded or showed its error state was not recorded this round (the first note saw the error state), so the 0 violations may not describe a loaded page.
* Dialogs, error states and status announcements were not exercised. WCAG 3.3.1, 4.1.3 and 2.4.11 are covered only by axe and the existing guard tests, not by an interaction run.

## Acceptance criteria

The only unticked criterion of #151 is the fourth. The others are already ticked and were not re-audited; the live axe results corroborate the third.

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Target level and scope decided and recorded (ticked) | Not re-tested | Unchanged. |
| 2 | Audit covers keyboard, focus, name/role/value, status messages, contrast, reflow, target size, errors (ticked) | Not re-tested | Unchanged. |
| 3 | Automated checks run in CI against key screens (ticked) | Corroborated live | 16 live screens, 0 axe violations on the WCAG 2.0 to 2.2 A and AA tags; raw output retained. Hosted CI for the exact head was not read in this task. |
| 4 | Manual screen-reader and keyboard checks recorded for each role workflow (UNTICKED) | Keyboard and reflow: automated desktop proof for one employee role (13 screens plus case detail) and the resident app. Screen reader: unproven. Other role workflows: unproven | Screen-reader testing is person-run assistive technology, production-only (#1907) and excluded for the demo. Only the Programme Manager employee account and the shared resident account exist, so the other seven role workflows were not signed in. A scripted Tab walk is not a manual keyboard check by a person. Keep unticked. |
| 5 | Map, charts and tables have accessible equivalents (#119) (ticked) | Not re-tested | Unchanged. |
| 6 | Accessibility statement draft lists known gaps without claiming conformance (ticked) | Not re-tested | This note adds no conformance claim. |

## What this does not prove

* Conformance with WCAG 2.2. Automated checks cover a minority of criteria and the sampler is an estimate.
* Screen-reader behaviour, 200 percent text size, 390 px mobile layouts or any assistive-technology output.
* Other role workflows, populated Time capture, dialogs, validation errors or live-region announcements.
* Resident or production accessibility. Nothing here is resident, legal or production evidence.

## Evidence limits

* Summary counts for contrast sampling, keyboard walks and the 320 px reflow probe are retained only in `axe-results-*.json`; there is no raw trace of individual Tab stops. Observed; raw output not retained for those.
* Passed and inapplicable axe results were not retained.
* The Azure deployment state (image digest, revision) was not re-read this round.
* The JSON and screenshots show the synthetic persona display name already used across repository evidence; no real account detail is retained.
* Independent exact-head review and hosted CI are outstanding; no criterion is ticked.

## Recommended follow-ups

* Change the document title on hash-route changes and add a guard test (small `src/api` web change; needs the focused web tier checks).
* Add a manual or scripted check of populated Time capture, dialogs and form-error states.
* Run the same scan for the remaining role accounts when they exist; person-run screen-reader testing stays with #1907.
