<!-- markdownlint-disable-file -->
# Employee chat browser check repair: research (2026-11-03)

Task: `employee-chat-browser-check-530`. Refs #530. Research disposition: executed (delta only; earlier research is reused).

## Delivered already (merged PRs, reused, not redone)

* #541: one employee chat agent with five skills, launcher and window, case grounding, role and scope, audit, workflow-only fallback.
* #743, #752: grounded replies on the selected case, also when AI is off.
* #568, #594: employee chat stays open on Enter/Send and refreshes, shared asset versioning.
* #579, #634, #680, #721, #759: verification and evidence PRs; #759 recorded local unit, SQL and browser checks and routed a medium finding.
* #545, #750: redeploys with live evidence (unauthenticated only).

Acceptance criteria 1 to 7 are ticked in the issue and unchanged here. Criterion 8 is the only open one.

## Unmet criterion and why

* Criterion 8 (local unit, browser and SQL checks pass; live verification recorded separately) stays unmet. Live employee-site verification needs a signed-in employee session and the owner's confirmation of the five agent names. No agent can supply either.
* The #759 review left an open medium finding: `chat_widget_browser_check` fails locally. This slice addresses the local browser half of that finding.

## Findings (reproduced on main 329824c44, Chromium via Playwright 1.64.1, pinned axe-core 4.10.3)

1. Employee chat log is only about 132px tall at 1280x720 (intro, size and composer take the rest), so a focused Sources summary scrolls out of the log. Fix: reserve a minimum share of the panel for the log.
2. The shared check still assumed external focus closes the chat. Since #568 the employee chat stays open (`stayOpen`), so four assertions were stale (tab-out loop, current-reply focus, `employee_current_focus`, and `render_focus` dismissal by external focus). A fixed synthetic note also sat under the open panel; the employee app has no fixed right-hand controls, so an in-flow note is the realistic stand-in.
3. `recovery_case` expected three script attempts; #812 raised the budget to one load plus three retries (four).
4. Resident leg (not this slice, #520): at 320px wide the composer content is about 660px (consent block) and capped at 55% of the panel, so Send scrolls out of the viewport. This fails on unchanged main too and is routed as a follow-up.

## Planning readiness

Ready. Slice is a one-line CSS change in `src/api` web plus check updates; no security, infrastructure, SQL or deployment surface, so the focused tier applies.
