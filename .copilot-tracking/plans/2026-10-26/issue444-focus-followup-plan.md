# Issue 444 focus, loading and error-announcement follow-up plan

Date: 2026-10-26. Research: ../../research/2026-10-26/issue444-focus-followup-research.md. Details: ../../details/2026-10-26/issue444-focus-followup-details.md.

## Phases

* [x] Phase 1: Research and reproduction before any source change (focus lost to body after Try again).
* [x] Phase 2: Plan, details and one independent critique before implementation.
* [x] Phase 3: Failing-before tests: extend `checks/resident_preview_browser_check.py` and `tests/test_resident_preview_api.py`; run them against unchanged source and record failures.
* [x] Phase 4: Fix `index.html`, `resident.js`, `resident.css` surgically.
* [x] Phase 5: Focused tests, browser check, ruff and mypy on the touched files; guideline review of changed web files with `file:line`.
* [x] Phase 6: Changes artifact, one independent Review, local commit with privacy-safe identity. No push or PR.

## Design

* Loading: `#status` is empty in markup and is filled by script (no loading text without JavaScript). Polite live region unchanged.
* Retry: on Try again, hide the error, announce "Loading your progress..." and move focus to `#main` (stable, tabindex -1, skip-link target) so focus never drops to body. Success after a retry sets status "Your progress has loaded." and leaves focus on `#main`. Initial load success clears the status quietly.
* Error (revised after critique C1): remove `role=alert` from the container; focus the error heading, which carries `aria-describedby="error-text"` so the error detail is exposed with the focus target. One intended mechanism (focus plus description), no second live region.
* Retry ordering (critique C2): call `main.focus()` before hiding the error, then set status and start the request.
* Focus indicator: remove `main:focus{outline:none}` so the global `:focus-visible` ring applies to the skip-link target.

## Acceptance

* Failing-before, passing-after real-browser assertions: focus on `#main` immediately after Enter and throughout the pending request, never body, and after recovery; repeat failure refocuses the error heading; one intended announcement mechanism per state (DOM intent, not spoken output); heading `aria-describedby` points at the error text; no role=alert; status empty without JavaScript; skip-link target shows a >=3px focus indicator; 320px reflow retained.
* Existing 36 browser passes and API/HTTP/domain tests remain green. No server, grant, projection, fixture or schema change.
* No comprehensive accessibility, screen-reader or resident acceptance claim; issue criteria are not ticked and the issue is not closed.

## Out of scope

Ellipsis character, theme-color/color-scheme, translate=no, touch-action, text-wrap, raw-JSON footer, heading refinements (remain routed Low follow-ups).
