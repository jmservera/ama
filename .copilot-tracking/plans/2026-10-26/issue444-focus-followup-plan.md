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

## Critique (one pass, independent `rubber-duck` agent, before implementation)

Execution: executed once, read-only, verdict **request changes**. Not repeated for this task. Recovered verbatim 2026-10-26 15:35 from this native session's own event log (`events.jsonl` event index 361, `tool.execution_complete`, `toolCallId toolu_01XF5Yp7K7hM31D15axh64tn`, `2026-10-26T09:44:19.565Z`); see `issue444-focus-followup-critique-recovery-note.md` for the recovery record. The verbatim critique response:

> 1. **High — Error detail may no longer be announced reliably.**
> Evidence: `.copilot-tracking/plans/2026-10-26/issue444-focus-followup-plan.md:18` (pre-revision draft); current dynamic message is separate from the focused heading at `src/api/src/zava_forward/api/resident_preview/web/resident.js:121-126`. Focusing only "We cannot show this page" need not announce `#error-text` or the human-help route. Removing `role="alert"` trades a possible duplicate for potentially missing the actual error.
> **Fix:** retain a dedicated live announcement for the error text (or reliably associate it with the focused target via `aria-describedby`) and move focus to a non-duplicative recovery target. Do not claim exactly one spoken announcement without AT validation.
>
> 2. **High — Retry focus ordering is underspecified and can still briefly drop focus to `body`.**
> Evidence: plan said to "hide the error" then move focus (pre-revision draft, now `...plan.md:17`); current hide operation removes the focused retry subtree at `resident.js:129-131`.
> **Fix:** focus `#main` *before* setting `errorEl.hidden = true`, then update the status and start the request. Make that ordering an explicit implementation requirement and test it.
>
> 3. **Medium — The proposed focus-event test cannot prove "never rests on body."**
> Evidence: `.copilot-tracking/details/2026-10-26/issue444-focus-followup-details.md:20` (pre-revision draft). Hiding a focused element can change `activeElement` without a useful `focusin` event on `body`; recording focus events therefore misses the exact regression asserted.
> **Fix:** use the delayed request to assert `activeElement === main` immediately after activating retry and throughout the pending state; make ordering in item 2 the primary prevention.
>
> 4. **Medium — "One live announcement per state" is overclaimed by DOM-only tests.**
> Evidence: acceptance claim (pre-revision draft, now `...plan.md:23`), while the research explicitly says no screen-reader test is possible under "Unknowns." Role counts, text, and focus assertions establish DOM intent, not spoken output.
> **Fix:** reword acceptance to "one intended live-region mechanism and one focus movement," and retain the existing no-screen-reader-claim boundary.
>
> **Existing assertions:** the only resident-preview alert assertion found is intentionally slated for replacement: `src/api/checks/resident_preview_browser_check.py:174-177`. No other current Python assertion was found for the static resident-preview loading text.
>
> **Verdict: request changes** — resolve the error-announcement mechanism and focus ordering before implementation.

### Dispositions (as accepted and acted on before implementation)

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | High | Removing role=alert may leave the error detail and help route unannounced. | Accepted. Heading gets `aria-describedby` to the error text; no AT-speech claim. |
| C2 | High | Hiding the focused retry before moving focus can drop focus to body. | Accepted. Focus `#main` before hiding; tested. |
| C3 | Medium | Focus-event observer cannot prove never-on-body. | Accepted. Assert `activeElement` immediately after Enter and across the delayed pending state instead. |
| C4 | Medium | "One live announcement" overclaims from DOM tests. | Accepted. Reworded acceptance. |
