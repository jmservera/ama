<!-- markdownlint-disable-file -->
# RPI Plan: Read-only CSV copy of unaccepted handoffs, implementation (#1419)

## Task Metadata

* Task ID: 1419-handoff-csv-implementation-1110
* Task slug: issue-1419-handoff-csv-implementation-1110
* Parent task: 1419-handoff-csv-research-1110 (earlier partial; its research, plan, details, critique and state are preserved, unedited)
* Planning status: ready (amended for admitted implementation)
* Plan date: 2026-11-10
* Phase details: .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md
* Plan critique: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-critique.md

## Executive Summary

Add `GET /api/handoffs/unaccepted.csv`, a read-only CSV copy of the existing `GET /api/handoffs/unaccepted` rows, and one separately labelled download link in the pending-handoff panel. One shared parser and one shared server branch serve both routes, so access, query parsing, errors and rows cannot drift. The serializer, core, roles, projection, thresholds and mutation paths do not change.

Base: merge commit 4350c3063f5e79703848ac4bdb136c219170d777 (parent 2cc340270b adopted by ordinary merge, no conflict; parent checker red state and runtime remain unverified and are not accepted through this child).

### User Decisions and Requirements Highlights

* Exactly 13 fields in source order; the earlier 14 was a coordinator brief error. Offered (exports `Sent`), Received and Escalated are included; Accepted, Completed, Declined and Withdrawn are excluded.
* Shared parser and branch; one EXPORT_KINDS mapping; no LIST_EXPORTS registration; no `list_rows` change; filename `unaccepted-handoffs.csv` by a narrow override.
* Link text "Download handoff waiting times for Excel"; the existing "Download for Excel" stays unchanged.
* Targeted modified and impacted validation by owner demo policy (see Validation Override).

### What You May Not Know

* The generic CSV path parses queries without blank retention; the shared branch avoids that drift (C2).
* The role-inventory test needs one entry for a new route literal.
* Empty result is a blank-header record; the panel hides when nothing is pending, so it is reachable mainly by a direct request. Documented, not changed.
* A caller-supplied limit is labelled "approved" by existing behavior; the UI offers no limit.

### Unresolved Decisions or Blockers

* Canonical heavy lock availability and Playwright runtime are checked at execution; if busy, a precise partial is returned, not a queue or a claimed pass.
* Hosted source CI and independent exact-head assessment are not available here.
* Operational purpose, retention, actual-record use, BG-010 and OD-09 thresholds, whole #80, #73 and #83 thresholds remain open.

## User Decisions and Requirements

* Implementation is admitted with the decisions above (coordinator brief 2026-11-10T20:43Z).
* Own file set only: server.py hunks, one GET_ENDPOINTS entry, new dedicated server test module, one small UI test module with a real minimal browser check, app.js `pendingHandoffs` success-path link and helper, API README ageing and export paragraphs, own RPI artifacts. No core README fix and no new issue.
* Never touch `app.js` retry and session helpers, `startupFailure`, `fetchReadRetrying`, Capacity, aftercare checkers, `ops.js`, `capacity_browser_check.py`, core sources, other worktrees or other authors' environments.
* Tests: controlled clock; exact header and every cell and order against JSON; literal fixed row; included and excluded states including Withdrawn; due, age and both reasons; null OD-09; query matrix with blank-first, repeated, NaN, infinities, bounds and error body; sender, receiver, both managers, unrelated staff; signed out, contractor, Application Administrator and unknown role denied before parse; formula, quotes, newlines; exact no-extra-fields and privacy markers; immutability on success, denied and invalid; current POST and HEAD behavior without inventing method support; no row-count proxies.
* Run existing handoff, list-export and role-inventory tests and directly affected UI tests; Ruff check and format; existing affected type check; Node syntax; fix introduced or tightly coupled failures within the implementation batch before the single Review.
* Before web edit, selected skills and current web guidance are loaded; before a web review the source is refreshed and changed files reviewed with file:line findings. No redesign, framework change or new queue.
* Real minimal browser evidence on a synthetic owned server: label, href, filename, authorised rows, keyboard activation, no mutation, and the unavailable or empty boundary. No broad Capacity browser suite. Non-blocking heavy lock; if busy, precise partial.
* Own environment, synthetic owned data directory, no default or private records, credentials, Azure, provider, SQL, Docker, deployment or spending. No fetch, merge, rebase or adoption after the chain begins; no push, PR, issue or board write.
* Sibling #1420 (research only) will later own role-screens.js and a narrow server CSV route; this child owns the shared server CSV hunks first; Root orders any later #1420 server work after this frozen contract.

## Goals

* CSV cells, rows and order equal the existing JSON for the same user, query and controlled clock.
* Access and negative boundaries identical to JSON: 401, then kind 403, then parse 400, then store PermissionError 403.
* A truthful, separate, read-only download that is not the pending list.
* Honest recorded evidence of what ran and what did not.

## Scope and Non-Goals

### In Scope

* server.py: module-level `max_age_hours` helper; shared JSON and CSV branch; one `EXPORT_KINDS` entry; filename override `unaccepted-handoffs.csv`.
* `src/api/tests/test_role_endpoint_inventory.py`: one entry.
* New `src/api/tests/test_unaccepted_handoff_csv_api.py` and new `src/api/tests/test_unaccepted_handoff_download_ui.py` (Node slice checks plus an opt-in real-browser class).
* app.js: link block and helper inside the `pendingHandoffs` success branch only.
* `src/api/README.md`: ageing and export paragraphs.

### Non-Goals

* Core, projection, serializer, roles, thresholds, escalation, mutation, pagination, selectors, as_of input; rendered queue, filters or threshold UI; new HTTP methods; global empty-header change; core README line 3003; ops.js; Capacity; retry and session helpers.

## Functional Requirements

* `GET /api/handoffs/unaccepted.csv` returns the same rows as the JSON route.
  * Observable acceptance criteria: header equals the 13 keys in order; every decoded cell equals the normalised JSON value; row order equal; `text/csv; charset=utf-8`; `Content-Disposition: attachment; filename="unaccepted-handoffs.csv"`.
* `max_age_hours` follows the JSON rules for both routes through one helper.
  * Observable acceptance criteria: status and error body equal across routes for missing, blank, blank-first-then-value, repeated, valid fraction, whitespace, text, 0, negative, nan, inf, 1000000, unknown key.
* Gates match JSON.
  * Observable acceptance criteria: 401 signed out; 403 for contractor, Application Administrator and unknown role even with an invalid limit (before parse); sender, receiver and both manager roles see rows; unrelated staff get the blank-header body.
* The panel offers one extra link on the success path only.
  * Observable acceptance criteria: label exact; `href` `/api/handoffs/unaccepted.csv`; `download` `unaccepted-handoffs.csv`; no query; existing link unchanged; absent on error, empty and loading states; helper text conveys not the pending list, all handoffs you can see, no resident contact details, read-only no import, no queue-wide limit selected so only past-due handoffs are marked overdue, an empty file has no column names.

## Non-Functional Requirements

* Read-only and immutable.
  * Objective threshold or evaluation condition: deep-copied cases, handoffs, history, ownership and audit equal before and after success, denied and invalid reads.
* Narrow projection.
  * Objective threshold or evaluation condition: header set exact; planted resident, address, contact, note and evidence markers never appear.
* Deterministic.
  * Objective threshold or evaluation condition: `workflows._now` patched; offered and due times set by constants; no comparison of two uncontrolled `as_of` values.
* Plain language and accessibility boundary.
  * Operating condition or verification approach, if needed: native anchor, ASCII, no em dash, short active sentences; engineering checks only, no accessibility conformance claim.

## Acceptance Criteria

Prospective until observed in the changes and review records.

* The functional and non-functional criteria hold under the new tests.
* Existing handoff, list-export, role-inventory and handoff UI tests pass or any failure is recorded and fixed in the batch.
* Ruff, format, affected type check and Node syntax pass or are recorded exactly.
* Real minimal browser evidence is obtained or a precise partial (busy lock, missing runtime) is recorded.
* Diff limited to the owned hunks above; no unowned file changed.

## Validation Override

* Original plan and critique PC-001 defaulted to the full local gate for route sensitivity. Preserved as history.
* Owner demo policy (2026-11-10) selects targeted modified and impacted validation instead. Basis recorded before implementation: the exact permission and store projection are reused; no new role, permission or persistence path; comprehensive negative-boundary and regression tests; affected API lint and type checks; a real minimal affected browser check. Hosted source CI and independent exact-head assessment remain required. This is not a waiver of any missing or failing relevant check and not a green full receipt. No SQL, Docker, full gate or cloud fallback. The Review must not state that the original review approved the focused tier.

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-plan.md |
| Phase details | .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md |
| Latest critique | .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-critique.md, see Critique Disposition |
| Relevant research | .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-implementation-1110-research.md; earlier .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md |
| Changes record | .copilot-tracking/changes/2026-11-10/issue-1419-handoff-csv-implementation-1110-changes.md, created by implementation |
| Planning execution and readiness | Complete; ready |
| Continuation | Implement, then one Review |

## Sources

* .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-implementation-1110-research.md (C1 to C15).
* Coordinator brief and scope refinement; earlier critique `.copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-research-1110-critique.md`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Environment and server route

* Intent: own environment verified; shared parser and branch; kind and filename.
* Dependencies: none.

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Shared helper, branch, EXPORT_KINDS, filename

* Requirement and evidence: C1 to C3.
* Expected result: JSON behavior byte-equal; CSV served through `list_export.to_csv`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md

<!-- rpi:phase id=P02 -->
### [ ] P02: Server tests

* Intent: prove parity and boundaries under a controlled clock.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Inventory entry and new focused module

* Requirement and evidence: C4 to C8.
* Expected result: new tests fail before the route exists and pass after.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md

<!-- rpi:phase id=P03 -->
### [ ] P03: Panel link and UI evidence

* Intent: truthful separate link; UI checks.
* Dependencies: P01; web guidance loaded (done in research).

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: app.js link and helper

* Requirement and evidence: C9 to C13.
* Expected result: success-path link only.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: UI tests and real minimal browser check

* Requirement and evidence: C9, C15.
* Expected result: Node slice assertions plus an opt-in real-browser check run under the heavy lock, or a recorded precise partial.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md

<!-- rpi:phase id=P04 -->
### [ ] P04: Docs and validation

* Intent: README paragraphs; run targeted validation; record honestly.
* Dependencies: P01 to P03.

<!-- rpi:task id=P04-T01 -->
#### [ ] P04-T01: README, lint, type, tests

* Requirement and evidence: C14; Validation Override.
* Expected result: recorded commands, raw results and anything not run.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md

## Dependencies

* Parent 2cc340270b adopted at merge 4350c3063f; no later parent head is merged mid-chain.
* Core `workflows.py`, `projection.py`, `list_export.py`: read-only dependencies.
* Playwright and Chromium in the user cache; heavy lock `/tmp/ama-rpi-heavy.lock` taken non-blocking for the browser run only.

## Critique Disposition

Earlier critique (preserved, not regraded): PC-001 to PC-005 with dispositions in the earlier plan. This chain's single critique:

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Critique 2026-11-10, verdict Revise (3 Medium, 4 Low, no High); file .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-critique.md | Compatible findings applied directly; none conflicts with a confirmed decision | See rows below |
| PC-101 link shows only when caller's own pending list is non-empty | Accepted as documented limitation | Admitted decision places the link in the pending-panel success path only. Recorded: a manager with nothing personally pending does not see the link; the empty-file case is tested by direct request, not through the panel. No new UI |
| PC-102 state crafting, clock patch lifetime, tie order | Applied | Tests craft `store.cases[id]["handoff"]` constants, patch `zava_forward.core.workflows._now` for the whole test via addCleanup, and use distinct offered_at values so order is unambiguous; tie order checked as the stable store order only where noted |
| PC-103 HEAD and POST | Applied | Test pins CSV HEAD and POST to the same status as the JSON route for the same session; no new method support |
| PC-104 helper wording vs columns | Applied | Helper says handoffs past their due time are marked as needing escalation in the file; a blank due time is never marked by time; no queue-wide limit selected. Meaning preserved, "overdue" avoided in favour of file column terms |
| PC-105 extra negative boundaries | Applied | Add tests: supplied as_of ignored, near-miss paths (trailing slash, upper case, `.csv/`) not served, existing /api/handoffs and /api/handoffs.csv and filename unchanged, JSON unaccepted route byte-equal after refactor |
| PC-106 skipped browser class | Applied | Browser run uses ZF_BROWSER_TESTS=1 and the recorded result must show tests ran not skipped; Playwright presence verified before; store-unchanged compared by loading the temp store file before and after |
| PC-107 helper name | Applied | Single name `_max_age_hours(url)` |

## Follow-Up Items

* None yet. Stable 13-column empty header, core README line 3003 and the issue wording remain out of scope by coordinator decision.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-10/issue-1419-handoff-csv-implementation-1110-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none for implementation
