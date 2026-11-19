# Issue 215 live2: research (2026-11-18)

Task: issue-215-live2. Unticked criteria: (3) WCAG 2.2 AA; (5) staff comprehension (person-run, waived for the demo).
Prior run 3 (docs/reference/research/issue-215-live-rerun3-evidence-2026-11-18.md) recorded an open visual defect: the employee chat helper line "Press Enter to send..." is clipped at the bottom of its scroll area at 1366x900 desktop. This is the first unmet demo-scope WCAG item with a code fix.
Research disposition: reused (prior live evidence) plus local reproduction. Planning Readiness: Ready.
Hypothesis: `.chat-widget-composer` is a scrolling grid (max-height 55%) whose sticky tools row (`bottom:0`) overlays the helper line.

## Findings
* Local Playwright harness (static server, real chat-widget.js/css, `.copilot-tracking/research/2026-11-18-issue-215-live2-repro.py`) with the status and error lines shown: at 1366x700 and 1280x720 the sticky tools row (`.chat-widget-tools`, position sticky bottom 0 inside the scrolling composer) covers the helper line `#employee-chat-keys` (elementFromPoint hits SELECT). At 1366x900 and 1920x1080 it is visible. Reproduced defect; matches run 3 clipped-helper observation.
* Cause: composer `max-height:55%; overflow:auto` plus sticky tools, and a log `min-height:40%` from viewport height 700px up, which leaves the composer too little room.
* Prototype (reverted to keep the phase order, to be re-applied in Implement): composer `flex:none` without scroll cap, drop sticky tools, move the 40% log minimum to `min-height:900px`. Measured: helper line hit-tested visible and form and tools inside the panel at all four sizes.
* Other criteria: (5) staff comprehension is person-run and waived for the demo; unprovable.
Planning Readiness: Ready.
