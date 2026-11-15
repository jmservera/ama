# Review: Programme screens WCAG state clarity (Issue #230)

* Boundary: `role-screens.js` `programme-queue` render, `test_programme_screen_wcag.py`, `test_programme_screen.py` assertions.
* Plan: [plan](../plans/2026-11-14-prog-screens-wcag-230-plan.md); changes: [changes](../changes/2026-11-14-prog-screens-wcag-230-changes.md).
* Review execution: executed once, self-review. Independent review and human accessibility acceptance remain required and are not claimed.

## Outcome: conformant with open items

* WCAG 1.4.1: each step state has a word prefix (`Action needed:` / `Warning:`); no colour dependence; `Pass:` intentionally not emitted.
* WCAG 2.1.1/2.4.1: native buttons in a `.row` group move focus to labelled sections; no `nav`, no new classes, no motion.
* Existing table cells unchanged, so exact-cell browser checks should hold.

## Open items (routed to follow-up)

* Browser checks (`specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`) not run: no browser run here.
* Full suite not rerun end to end after the button fix.
* Focus target wrappers (`tabindex=-1` divs) have no visible focus style review.
* Screen-reader behaviour unverified.

## Follow-ups (ranked)

1. Run the browser checks on the exact head (ease: high, value: confirms keyboard behaviour).
2. Apply the same word prefixes to the funnel and other specialist screens.
