# Issue 159 live research

Task: verify the only unticked #159 criterion ("Panel is keyboard operable, screen-reader tested, and announces new messages") on the synthetic demo. All other boxes, including the tokenomics box, are ticked and not reopened.

Owner decisions 2026-11-18: demo, desktop only, live Azure authorised (rg `ama`), person-run assistive-technology testing not needed.

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Live app `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031`, image digest sha256:5368f4e4...e17e5fb.
* Playwright keyboard-only probe and cropped screenshots, recorded in `docs/reference/research/assistant-ux-live-159-2026-11-18.md`.
* Existing local tests: `src/api/tests/test_assistant_panel_a11y_159.py` (5 tests; observed, raw output not retained; includes browser axtree and live announcements).

## Findings

* Launcher reached by Tab alone (44 stops from page start); Enter opens, focus moves to the dialog heading; Escape closes and returns focus to the launcher.
* Log is `role=log`, `aria-live=polite`, `aria-relevant=additions`; the status region announced each turn; the alert region stays hidden unless there is an error.
* Screen-reader testing by a person cannot be proven by an agent and is excluded for the demo by the owner decision.
* Observation: a rules-only answer shows "Decision model (case rules), no record changed" rather than the literal "AI suggestion, not approved"; that label belongs to a ticked criterion and is only noted.
* Answers contain synthetic person names, so no log screenshot was taken.
