---
title: Issue 96 C4 research, hosted accessibility baseline count failure
description: Actual hosted failure, field and message audit of the eighth aria-invalid site, and Planning Readiness
ms.date: 2026-11-13
---

## Scope and disposition

* Research disposition: executed. Parent: `issue-96-impact-c3-0052` (completed, C3 of 5 spent, two remaining) and `issue-149-independent-ux-0042`. Branch `feat/demo-ux-partial-release-0117` (PR 1500), head `9f1da5a31055736c49708b7283a5412c31de705a`, source tree `6915b96c8ededf363b76c8fb4700153eb18ff588`. `origin/main` fetched read-only: `c401e5d56446b5752e8d91af6a45f3f06269c4bd`, no movement from the expected value.
* Budget: the recorded current scoped 96 task state is C3 of 5 spent with two remaining (root assessment `96-c3-root-assessment-0101.json`; no later source correction ran). A search of `.copilot-tracking` found no newer conflicting 96 spend. This batch is C4, leaving one. Older whole-96 history stays unknown and preserved. The 233 five-cycle authority is exhausted and excluded.

## Actual hosted failure (preserved, not a flake)

* Source projects CI run 43347366743, job 131630021882: 2965 API tests in 898.602 s, one failure, 629 skips. Failing test `test_accessibility_baseline.Wcag22Baseline.test_every_invalid_field_is_tied_to_a_message`, `tests/test_accessibility_baseline.py:100`, `8 != 7`. Caught law-store warning traces in the log are ordinary and not the failure.
* Local reproduction on the exact candidate (failing-first, before any edit): `AssertionError: 8 != 7 : new aria-invalid site: audit it and update this check and the record`, 12 tests, 1 failure. Retained at `.copilot-tracking/audits/2026-11-13/issue-96-c4-ci-baseline-0208-failing-first.log`.

## Root cause

The saved Held copy checker (`fundingSavedCopyCheck`, `role-screens.js`, added by 96) introduced the eighth script site that calls `setAttribute("aria-invalid", "true")` (`role-screens.js:1385`). The static inventory (seven) and the dated WCAG baseline record were not updated. C3 corrected only the role-screen contract tests. Counting sites is the test's designed prompt to audit, so the correct response is an audit, not a blind increment.

## Field and message audit (source read, 2026-11-13)

| Item | Evidence |
| --- | --- |
| Field | `<input type="file" id="held-check-<draft>">`, `accept=".json,application/json"`, `role-screens.js:1387` |
| Accessible name | Visible `<label for=id>Saved Held draft file</label>` in the same paragraph (`role-screens.js:1434`). Native label, no ARIA needed |
| Message | `<div class="field-error" id="<id>-error" hidden>` created at `:1375`, placed directly after the input (`:1434`) |
| Association | `aria-describedby="<id>-error"` set at construction (`:1387`), so the reference exists before and after the message is shown. A hidden element is a valid description target by the ARIA name and description computation; what a screen reader then reads was not tested |
| Invalid state | `show(text, flagged)` sets `error.textContent`, clears `hidden`, then sets `aria-invalid="true"` only when flagged and removes it otherwise (`:1383-1385`); `onchange` clears both |
| Non-colour signal | `.field-error` renders a warning glyph (`style.css:299`) plus bold text; text states the problem and a next action (`HELD_CHECK_NO_FILE`, `HELD_CHECK_UNREADABLE`, `HELD_CHECK_ERRORS`) |
| Live region | The same text is also placed in a sibling `role="status"` `aria-live="polite"` region (`:1376`); this is source markup and intent, announcement behaviour was not tested |
| Existing runtime evidence | `src/api/checks/held_form_download_browser_check.py:403-407` observes `aria-invalid="true"` on the file input and "Choose" in `.field-error` for the no-file case. 88 PASS lines were recorded by C3. Not re-run here |

Result: the association is truthful by source. No new defect found. The current baseline window test already passes the site only because `aria-describedby` sits within the 7-line window; it does not prove that the described element is the message. That is the specific coverage gap for this site.

## Web Interface Guidelines (fetched 2026-11-13 from the vercel-labs source)

* Pass for this field: form control has a `<label for>`; errors are inline beside the field; async validation text has `aria-live="polite"`; error text includes a next step; loading text ends with an ellipsis; native semantics before ARIA.
* Not applicable or not changed: no new focus, animation, paste or zoom behaviour. Observation only, not a defect and not expanded: the check does not move focus to the field on error (the guideline concerns submit forms; this is a button-driven read-only check, and the message is announced by the live region). Left to existing owner or manual review.

## Limits

No screen reader, assistive technology, manual acceptance or WCAG conformance claim. Fluent 2, native semantics, manual paths and human boundaries are unchanged.

## Planning Readiness

Ready: audit complete, no defect, bounded tests plus record update.
