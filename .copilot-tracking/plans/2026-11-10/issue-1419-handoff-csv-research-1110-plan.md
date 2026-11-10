<!-- markdownlint-disable-file -->
# RPI Plan: Read-only CSV copy of unaccepted handoffs (#1419)

## Task Metadata

* Task ID: 1419-handoff-csv-research-1110
* Task slug: issue-1419-handoff-csv-research-1110
* Planning status: ready (candidate for later admitted implementation; not executed)
* Plan date: 2026-11-10
* Phase details: .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md
* Plan critique: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-research-1110-critique.md

## Executive Summary

Add one read-only download, `GET /api/handoffs/unaccepted.csv`, that is a CSV copy of the existing `GET /api/handoffs/unaccepted` rows, and one clearly labelled link to it beside the existing pending-handoff panel. The CSV reuses the existing `handoffs` role gate, the same store call and the same 13-field projection, so no new access, field, threshold or write path appears. A single shared `max_age_hours` parser serves both routes so they cannot drift.

This launch admits research and planning only. Implementation and Review are NOT executed; every acceptance item below is a proposal, not observed evidence. Nothing was run.

### User Decisions and Requirements Highlights

* Smallest independent scope: server CSV route, focused tests, and only the handoff-panel link. No role widening, selectors, paging, default thresholds, escalation or mutation.
* The link is labelled as NOT the pending list, with no rendered queue, filter or threshold control.
* The serializer is not changed globally; an empty result keeps its blank-header record and the limitation is documented.

### What You May Not Know

* The row has 13 fields, not the 14 stated in the brief and refinement (C12).
* Withdrawn handoffs are also excluded, in addition to Accepted, Completed and Declined (C11).
* The generic CSV path parses queries without blank retention, so `?max_age_hours=&max_age_hours=5` would diverge from JSON unless the parser is shared (C2, C3).
* `test_role_endpoint_inventory.py` needs a one-entry edit for any new route literal (C21).
* Offered appears as `Sent` in the exported status (C11).
* The parent topic is unpublished and active; the overlap observed at the pin is only `ops.js` and `capacity_browser_check.py` (C27).

### Unresolved Decisions or Blockers

* Root choices: dedicated branch versus registry; download filename; link wording owner; validation tier; admit the inventory-test hunk; correct "fourteen". None blocks planning.
* Operational purpose, retention, actual-record use and BG-010 thresholds remain unapproved; whole #80 and #73 stay open.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Admission is research plus plan, details and critique only; no implement, review, tests, runtime or source edit (owner brief).
* Eventual stacked child PR targets the declared parent topic while unmerged; no PR or push now; no silent retarget; later source integration needs explicit pin and ownership reconciliation after the parent correction (owner brief).
* Preserve the narrow projection: no resident, address, contact, note, evidence, raw handoff or history fields (owner brief).
* Product direction: distinct labelled download near the pending panel; one-way, read-only, all-authorized qualifying rows; explicitly not the pending list; no new rendered queue or filter UI (owner brief).
* Preserve the blank-header empty behavior for this scope and document it; no global serializer change (owner brief).
* Never modify `app.js` retry and session helpers, `startupFailure`, `fetchReadRetrying`, Capacity or aftercare checkers, or `ops.js`.
* Do not approve export purpose, retention, actual-record use or BG-010 thresholds.

## Goals

* Provide a CSV whose every field, row and order equals the existing JSON for the same user, query and clock.
* Keep access identical to the JSON route: unauthenticated 401, kind 403 before dispatch, role re-check in the store.
* Give staff a truthful, separate download and make clear it is not the pending list.
* Produce hunk-level ownership and an integration order that avoids the active parent's files.

## Scope and Non-Goals

### In Scope

* `src/api/src/zava_forward/api/server.py`: shared `max_age_hours` helper, shared JSON and CSV branch, one `EXPORT_KINDS` entry.
* `src/api/tests/test_role_endpoint_inventory.py`: one `GET_ENDPOINTS` entry.
* One new focused synthetic test module for CSV against JSON parity.
* `src/api/src/zava_forward/api/web/app.js`: only the link block inside `pendingHandoffs()`.
* `src/api/README.md`: the ageing paragraph and the export section.
* Optionally a filename override line (Root choice).

### Non-Goals

* No change to core `workflows.py`, `projection.py`, `list_export.py`, roles, thresholds, escalation, mutation, pagination, arbitrary selectors or as_of input.
* No rendered unaccepted queue, filter or threshold UI.
* No edits to `ops.js`, `capacity_browser_check.py`, retry or session helpers, or the core README (stale statement flagged only).
* No push, PR, GitHub or board write in this launch; no operational approval.

## Functional Requirements

* `GET /api/handoffs/unaccepted.csv` returns the same rows as the JSON route for the same user, query and clock.
  * Observable acceptance criteria (proposed): decoded CSV cells equal normalised JSON values, same row order, same 13 columns in order, with `text/csv; charset=utf-8` and an attachment disposition.
* Optional `max_age_hours` follows the JSON rules: first value wins, missing or blank is none, otherwise a float with `0 < v < 1e6`.
  * Observable acceptance criteria (proposed): the status and error body for each invalid input equal the JSON route's 400 and message.
* Role gates match JSON.
  * Observable acceptance criteria (proposed): 401 signed out; 403 for contractor, Application Administrator and unknown roles before parsing; sender, receiver and manager see their rows; unrelated staff get the blank-header body.
* The handoff panel offers one separately labelled link to the CSV route, with no query, and not on the error path.
  * Observable acceptance criteria (proposed): the anchor href equals the exact route, is not `/api/handoffs.csv`, and the text and helper line say it is not the pending list.

## Non-Functional Requirements

* Read-only and immutable.
  * Objective threshold or evaluation condition: deep-copied case, handoff, ownership and audit snapshots equal before and after success, denied and invalid reads.
  * Observable acceptance criteria (proposed): no change in any snapshot.
* Privacy of projection.
  * Objective threshold or evaluation condition: header set equals the 13 names exactly; no resident, address, contact, note, evidence, raw handoff or history key.
  * Observable acceptance criteria (proposed): synthetic marker values in excluded fields never appear in the body.
* Deterministic tests.
  * Objective threshold or evaluation condition: clock patched at `workflows._now`; offered and due times overwritten with constants.
  * Observable acceptance criteria (proposed): no comparison of two uncontrolled wall-clock responses.
* Web quality (future hunk only).
  * Operating condition or verification approach, if needed: before editing, fetch current web-design-guidelines and read selected skills; keep native anchor, plain language, no em dashes, Fluent 2 and WCAG baseline. No accessibility conformance claim from engineering checks.

## Acceptance Criteria

All items are proposed future acceptance, not observed results.

* The functional and non-functional criteria above hold under the focused tests.
* Existing JSON, handoff, list-export and role-inventory tests stay green; the browser handoff test stays green when its prerequisites exist.
* `list_export.py` is unchanged, and for a user with no qualifying rows the CSV is the existing blank-header record; the README states that such a file has no column names.
* Validation uses the full tier by default (authorization-sensitive route; doubt takes the full tier), with a verified external full receipt, unless Root records a downgrade basis.
* Hosted CI and independent exact-head review are read before any publication; absent or skipped checks are stated as not run.

## Implementation Context Record

| Context item                     | Current artifact or record |
|----------------------------------|----------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-research-1110-plan.md |
| Phase details                    | .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md |
| Latest critique                  | .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-research-1110-critique.md, one critique, see Critique Disposition |
| Relevant research                | .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md |
| Changes-record role              | not created in this launch; a later admitted implementation owns .copilot-tracking/changes/2026-11-10/issue-1419-handoff-csv-research-1110-changes.md |
| Planning execution and readiness | Planning complete; ready as a candidate, subject to Root decisions |
| Continuation context             | Stop. The owner brief admits no Implement or Review; control returns to the coordinator |

## Sources

* .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md: evidence C1 to C28.
* Coordinator refinement and issue body (outside the worktree): scope and wording constraints, validated against source.

## Phase Checklist

Phases below are FUTURE work for a later admitted implementation. None is started or done.

<!-- rpi:phase id=P01 -->
### [ ] P01: Pre-flight and integration order

* Intent: confirm the base, ownership and decisions before any source edit.
* Dependencies: Root admission; parent correction landed or explicit pin reconciliation.

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Re-diff and reconcile

* Requirement and evidence: C27; owner brief on pin and ownership reconciliation.
* Expected result: recorded diff of `server.py`, `app.js` and API tests against the new base showing no overlap with owned hunks, or an explicit reconciliation.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Record Root decisions

* Requirement and evidence: research Unresolved Decisions.
* Expected result: chosen design, filename, wording owner, validation tier, inventory hunk admitted.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md

<!-- rpi:phase id=P02 -->
### [ ] P02: Server route

* Intent: one shared parser and one shared branch for JSON and CSV.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Shared parser and branch, kind mapping

* Requirement and evidence: C2 to C8.
* Expected result: JSON behavior unchanged; the CSV route is served through `list_export.to_csv`; kind is `handoffs`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md

<!-- rpi:phase id=P03 -->
### [ ] P03: Tests

* Intent: prove parity, boundaries and immutability under a controlled clock.
* Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Inventory entry and focused regression module

* Requirement and evidence: C20 to C24.
* Expected result: new module and one inventory entry; existing tests unchanged otherwise.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md

<!-- rpi:phase id=P04 -->
### [ ] P04: Panel link, after web guidance fetch

* Intent: truthful separate download in the existing panel.
* Dependencies: P02; current web-design-guidelines fetched.

<!-- rpi:task id=P04-T01 -->
#### [ ] P04-T01: Link block in pendingHandoffs

* Requirement and evidence: C17 to C19; content standard.
* Expected result: one link and helper text, success path only; no other `app.js` hunk.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md

<!-- rpi:phase id=P05 -->
### [ ] P05: Docs and validation

* Intent: documentation, the chosen validation tier and honest evidence.
* Dependencies: P02 to P04.

<!-- rpi:task id=P05-T01 -->
#### [ ] P05-T01: API README and validation record

* Requirement and evidence: C25, C28; repository validation tiers.
* Expected result: updated README paragraphs; recorded commands and what did and did not run.
* Detail section: P05-T01 in .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md

## Dependencies

* Parent topic test/demo-export-entrypoints-80-1110 (unpublished, active, checker-only correction): later child targets it while unmerged; reconcile after correction.
* Core `workflows.py`, `projection.py`, `list_export.py`: read-only dependencies.
* Playwright prerequisites for the optional browser test: absent here; not run.

## Critique Disposition

Critique run 1 (only run): see the critique artifact. Dispositions are recorded below after it returned.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 Medium: focused tier leaning for an authorization-sensitive route | resolved | Plan of record is the full tier (doubt takes the full tier; route is authorization-sensitive). Root may downgrade only with a recorded basis. See P05 |
| PC-002 Medium: Design A left open | resolved | Shared server.py branch is the plan of record. Design A rejected: needs a list_rows signature change, a typed 400, a registry-test edit and more shared-line churn (C5 to C7) |
| PC-003 Medium: wording not tied to scope; blank-header meaning | resolved | Helper wording states no time limit set, not the pending list and that a file with no rows has no column names; limitation also in README (P04, P05) |
| PC-004 Low: empty-result and serializer-unchanged not acceptance | resolved | Added to Acceptance Criteria |
| PC-005 Low: parity compares normalised values | resolved | Added literal expected cells for one fixed row in P03-T01 case 1 |

## Follow-Up Items

* Stable 13-column empty header: product choice and global serializer change, not in scope.
* Core README line 3003 says the ageing method is not wired to a route; flag for a separate documentation issue.
* Correct "fourteen" in the issue text.

## Handoff

* Implementation artifact: not created; Implement is not admitted in this launch.
* Ready phase or task: none in this session; first eligible later task is P01-T01.
* Remaining provisional question or blocker: Root decisions listed above.
