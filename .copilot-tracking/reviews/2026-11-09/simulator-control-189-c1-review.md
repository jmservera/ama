<!-- markdownlint-disable-file -->
# Review: issue 189 C1 correction (2026-11-09)

Execution: one authored Review of the C1 diff by an independent code-review agent (source reading only, it ran no tests) plus the parent's executed local evidence in the [changes artifact](../../changes/2026-11-09/simulator-control-189-c1-changes.md). Not repeated in this task. Outcome: no significant findings in the C1 correction.

Assessed boundary: local working tree on `522adc394` plus the C1 diff, synthetic fixtures only. The original independent Functional review (`request_changes`, 1 High, 2 Medium) and the original author Review (`no significant findings`) are preserved; this Review does not replace the independent review's verdict, which only a later independent exact-head review can do.

## Finding status

| Original finding | C1 status | Evidence |
| --- | --- | --- |
| F1 High, view-only administrator mutation | Corrected locally | Server gate order, module `VIEW_ONLY` defence, navigation, tests fail without the fix |
| F2 Medium, no Stop for expired or invalid-window controls | Corrected locally | Screen change, real-browser check in nine states, 0 axe violations |
| F3 Medium, selected-suite error | Remains UNRESOLVED | Not reproduced at head or base with bounded reproducers; traceback lost; no waiver |

## Not proven (routed to later user-selected work)

* F3 cause (only a full-suite capture can show it).
* Independent exact-head Functional, fresh independent web and assistive-technology review (the Parent's web-guideline fetch is parent evidence only).
* Advisory flock on Azure Files, mounting the control share writable into the API, budget alert reference (AC3 schema decision), live cohort and job acceptance.
* Final host integration after #1292 is on current main, then rerun the narrow tests.

Follow-ups ranked: (1) independent exact-head review of the corrected head; (2) full-suite capture to resolve F3 when the owner selects it; (3) host integration after #1292; (4) owner schema decision for the alert reference; (5) prove flock on the real share.
