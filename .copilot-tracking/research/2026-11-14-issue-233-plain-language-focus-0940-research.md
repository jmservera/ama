# Research: #233 stage-map focus and announcements (2026-11-14)

Disposition: executed. Planning Readiness: Ready. Parent: `63330dd32`, `Refs #233`.

* The parent stage map renders on every role screen; `show()` in `app.js` moves focus to the main region on navigation, so route changes already land on a focusable target.
* Gaps: the stage `ol` had no name, and the current stage was announced only by text. Resident-choice serves stages 3 and 7, so a naive `aria-current` would mark two steps.
* The role screens contain no resident portal links; the resident handoff stays text and is out of scope.
* Tension callouts are h2 panels with a text status line, no colour cue.
