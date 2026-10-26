# Issue 444 focus, loading and error-announcement follow-up: review

Date: 2026-10-26. Changes: ../../changes/2026-10-26/issue444-focus-followup-changes.md. Native session 7f0c39c0-54e7-4fa8-8e0f-bffad1161d56.

Review execution: executed once, independent `code-review` subagent, read-only, over the whole working-tree diff before commit. Outcome: Pass with Low follow-ups. No material finding open. Not repeated in this task.

## Findings and dispositions

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Low | Held-route `pop()` could race the asynchronous route delivery in the browser check (`checks/resident_preview_browser_check.py`). | Fixed before commit: `release()` polls until the request is held; check rerun three times, 58 PASS each. |
| 2 | Low | Programmatic focus on `main` now draws the focus ring around the whole content region, including after a retry. | Accepted intended trade-off; ring asserted for the skip-link path only. |
| 3 | Info | Focus and announcement logic: no regression; retry hidden while loading so no overlapping requests; no-JavaScript path correct. | None. |
| 4 | Low | Guideline copy: `src/api/src/zava_forward/api/resident_preview/web/resident.js:134` uses "..." not "…"; "Try again" is not Title Case (`web/index.html:27`). | Routed Low follow-up; repository ASCII and plain-language convention retained. |
| 5 | Info | Guideline items passing: no outline none remains (`web/resident.css`), visible `:focus-visible`, reduced motion honoured, polite status, error message gives a next step. | None. |
| 6 | Info | Scope: web assets and two test files only; loopback, default-deny and no-write boundaries untouched; no overclaim. | None. |

## Guideline retrieval

Rules fetched 2026-10-26 from the Vercel web-interface-guidelines `command.md` (see research artifact). Only the two copy deviations above were found in changed lines.

## Remaining claims and limits

Local synthetic Chromium DOM, focus and live-region assertions only. No screen-reader speech test, no human or resident acceptance, no comprehensive accessibility claim. The unticked #444 criterion is not ticked by this change; the owner or coordinator decides after exact-head/base gate and hosted checks. Complete local RPI gate not run (instructed: shared gate fix awaits main).
