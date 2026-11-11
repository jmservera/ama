<!-- markdownlint-disable-file -->
# RPI Review: unaccepted handoff CSV implementation (#1419)

* Task slug: issue-1419-handoff-csv-implementation-1110
* Plan: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-plan.md
* Changes: .copilot-tracking/changes/2026-11-10/issue-1419-handoff-csv-implementation-1110-changes.md
* Review execution: executed once after implement-done (seq 5). Executed by the implementing worker, so it is NOT the independent exact-head assessment, which is still required.
* Assessed boundary: uncommitted diff of server.py, app.js, test_role_endpoint_inventory.py, src/api/README.md and the two new test modules, on merge base 4350c3063f.
* Guidelines source refetched 2026-11-10: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md. Read together with the repository Fluent 2 design system, WCAG baseline and plain-language content standard (content standard prevails over the source's Title Case rule).
* Original review status: the original partial-phase critique (issue-1419-handoff-csv-research-1110) recommended the full validation tier (PC-001). That is preserved; it did not approve the targeted tier. The targeted tier is an owner demo-policy override recorded in the plan and changes record.

## Outcome

Conformant with the admitted scope for the owned hunks, with open routed items below. No accessibility conformance, hosted CI or full-gate claim is made.

## Findings (file:line, current tree)

* RV-001 Low, web: src/api/src/zava_forward/api/web/app.js:761-762 the helper paragraph is long (six sentences). It is plain, active voice, ASCII, and states the not-the-pending-list, read-only, no-contact-details, no-limit and empty-file facts. Native anchor retained, so keyboard and focus behaviour is the existing `.btn` style. Routed: human plain-language and assistive-technology review of wording length; not blocking.
* RV-002 Low, design: app.js:760-762 the link is only rendered when the user's own pending list is non-empty (admitted design, critique PC-101). A manager with nothing pending has no panel link; the route is reachable directly. Documented in README; routed to a later product decision.
* RV-003 Info, server: src/api/src/zava_forward/api/server.py:175-177, 180-186, 736-746 one EXPORT_KINDS entry, one shared parser, one shared branch. 401 and kind 403 occur before parsing; 400 body unchanged. No serializer, role or core change. Docstring at line 181 is a long single line; ruff passes.
* RV-004 Medium, validation: test_case_journey.test_priority_invocation_and_procurement_preserve_history_barriers fails (Node TypeError in capacityView). It fails identically on unmodified HEAD, so it is pre-existing in parent-owned Capacity code, not caused by this change. Not fixed (out of scope, parent-owned) and not waived. Routed to the parent for correction before publication.
* RV-005 Info, scope: no edit to retry/session helpers, startupFailure, fetchReadRetrying, ops.js, capacity checker, core, projection or list_export.

## Not performed

Full local gate, SQL, Docker, hosted CI, human or assistive-technology accessibility review, live or real data use. Whole #80, #73 and #83 human thresholds remain open; no export-purpose or retention approval.

## Routing

Findings route to later work (parent for RV-004; owner/product for RV-001 and RV-002). No further Review or Implement loop in this task.
