<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 83 read-only handoff waiting-time screen

## Metadata

* Task ID: issue-83-waiting-view-1111
* Critique date: 2026-11-11
* Plan: .copilot-tracking/plans/2026-11-11-issue-83-waiting-view-1111-plan.md
* Phase details: .copilot-tracking/details/2026-11-11-issue-83-waiting-view-1111-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: read-only UI for the existing `GET /api/handoffs/unaccepted` projection; no API, core, persistence, permission, threshold or escalation change; delivered CSV and pending list unchanged; failure visible, never empty or success; required cases (initial/no personal pending but queue present, empty, due vs merely old, already escalated, keyboard, rejected/malformed without mutation); focused tier; Fluent 2 native semantics; #83 criterion C3 not ticked.
* Research and evidence considered: .copilot-tracking/research/2026-11-11-issue-83-waiting-view-1111-research.md; source checked directly: src/api/src/zava_forward/api/web/app.js (route() 376-460, api() 56-80, pendingHandoffs 754-776, listView header ~897-902), src/api/src/zava_forward/api/server.py 738-751, src/core/src/zava_forward/core/workflows.py 60-84 and 322-350, src/api/tests/test_unaccepted_handoff_download_ui.py.
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR7, AC1-AC4, P01-P04, test ownership block.
* Assessment boundary: plan credibility only. No implementation, no test run, no Chromium execution; web rules not refetched (no edits are made here).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Source claims C1-C5, C7 | Covered | Verified: pendingHandoffs hides card on empty and has no ageing; both routes use identical filters; handoff_ageing yields reasons only from own due time unless a limit is passed; route() falls back to "Case workspace". |
| FR2 / no threshold | Covered | `max_age_hours` unsent; server never defaults it (server.py 741-747). |
| FR5/FR6 failure honesty | Partial | api() converts unparseable bodies to `{}` on reads (app.js 72-75), so a 200 non-JSON body arrives as a non-array object; the plan's validator covers it but no test names it. 403 for non-staff roles is not given its own message (PC-004). |
| FR7 route label | Partial | The label comes from `destination?.scope || "Case workspace"` computed before dispatch (app.js 411-412); P01-T02 does not say where or how the label is changed (PC-005). |
| Caller case: no personal pending but queue present | Partial | Plan covers only card load failure and Node stubs (PC-001). |
| Caller cases: due vs merely old, escalated, empty | Covered | AC1/AC2; see PC-002 for a client-clock risk. |
| Keyboard operation | Partial | Link entry covered; re-check button and failure-state keyboard path not named (PC-003). |
| Test budget consistency | Missing | Budget contradicts AC1/AC2 (PC-002). |
| Whole #83 / C3 not ticked | Covered | Stated in summary, non-goals and follow-ups. |
| Focused tier, no gate | Covered | AC3, P03-T02. |

## Verdict

* Verdict: Revise
* Rationale: The design is sound and source-verified, but the plan does not yet deliver one required test case with explicit evidence, its test budget contradicts its own acceptance criteria, and a few behaviours that decide failure-honesty (403, label, keyboard re-check) are unspecified. All are direct planner corrections; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: "No personal pending but queue present" is not an explicit, labelled test

* Related IDs: AC1, AC2, P02-T01, P02-T02, research Wave 3
* Evidence: app.js 757 (card hidden when `/api/handoffs` is empty); workflows.py 322-350 (same filter, so real data cannot produce this state).
* Concern: The caller requires this case. The plan only exercises card load failure. That is a different state: the card shows an alert rather than being hidden.
* Impact: The primary reachability claim (screen works when the card is absent) is untested for the hidden-card state, and the cited limitation is not attached to the test.
* Smallest useful change: Add to P02-T02 a Chromium case where the page fetch wrapper returns `[]` for `/api/handoffs` and rows for `/api/handoffs/unaccepted`, labelled "constructed response, not reachable with real data". Assert the card is hidden, the header link is present and reachable, and the table renders. Keep the card-failure case as a second variant. Add an Initial case: a loading `role="status"` state before the response.
* Action owner: planning parent
* Exact resolving evidence: phase details P02 names both variants and the constructed label; test method names appear in the AC2 list.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Test budget contradicts acceptance criteria; due vs old must be server-derived

* Related IDs: Test ownership block, AC1, AC2, FR4
* Evidence: phase details "Maximum additions: 8 Node scenarios ... 4 Chromium methods"; AC1 lists 10 Node cases; AC2 lists about 7 Chromium behaviours. workflows.py 76-84 derives reasons server-side.
* Concern: The cap cannot satisfy the criteria. Separately, the plan does not forbid the client from computing lateness from `due_at` or `age_hours` against its own clock.
* Impact: An implementer must break one of the two; a client-derived "overdue" label would reproduce the threshold the task forbids.
* Smallest useful change: Raise the caps to match AC1/AC2 (or merge cases into table-driven subtests and say so). Add to FR4 and the Node cases: Escalation text derives only from `escalated`, `needs_escalation` and `reasons`; the merely-old row (large `age_hours`, `reasons: []`, `needs_escalation: false`) must read "no escalation reason recorded" and never "late"; no use of `Date.now()` for status.
* Action owner: planning parent
* Exact resolving evidence: consistent caps in the test ownership block; FR4 sentence; a Node case asserting no `Date.now`-based text.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Keyboard operation covers only the entry link

* Related IDs: AC2, FR6, NFR native semantics
* Evidence: AC2 "link reachable by keyboard"; FR6 re-check button.
* Concern: The re-check button, the case links in the table and focus after route change and failure are not tested.
* Impact: The failure path (the one that must be visible) is the least verified for keyboard users.
* Smallest useful change: In the Chromium cases, press Enter on the entry link, Tab into a case link and confirm it navigates to `#/case/{id}`, then in the failure state activate the re-check button with Enter/Space, assert a second GET and no POST, and assert the alert or h1 receives or announces focus consistently with `show()`.
* Action owner: planning parent
* Exact resolving evidence: AC2 lists these steps; matching test methods exist.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Roles that reach the list but are refused (403) and error classes are not specified

* Related IDs: FR1, FR6, AC1
* Evidence: server.py 744-749 (403 for non-staff, 400 for bad limit); app.js 758-775 precedent (`e.status ? message : fixed`); app.js 436 (Contractor routed away; no-case accounts stopped earlier).
* Concern: FR6 says every failure shows one fixed alert with no server text, but a 403 means "your role cannot see this", not "try again". The header link renders for any role reaching listView.
* Impact: A refused role would be told to retry, or the alert would be ambiguous about being a permission result rather than an outage; AC1 "HTTP error" is a single case.
* Smallest useful change: Specify two fixed messages (access refused with owner; load failure with owner and next action) keyed on `status === 403` versus other, still without server text, and split the HTTP error Node case into 403 and 500. State the link is unchanged for all list-view roles because the server remains the permission authority.
* Action owner: planning parent
* Exact resolving evidence: FR6 text and AC1 list both show the 403/other split.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Route status label and ordering are underspecified

* Related IDs: FR7, P01-T02
* Evidence: app.js 410-412 computes `routeStatus` before dispatch; unknown hashes get "Case workspace"; dispatch order 428-447 with Contractor and no-case guards before the list fallback.
* Concern: "route status label for that hash" does not identify the edit site; placing the new route after the `services.cases === false` and Contractor guards is implied but not stated.
* Impact: Risk of wrong label, or the route bypassing the no-case-access guard.
* Smallest useful change: In P01-T02 state: set `routeStatus` for `#/handoff-waiting` at the existing line 412 expression, and insert the dispatch after the guards (next to `#/import`). Add one Node or Chromium assertion on `workspaceStatus` text.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 text and an assertion in P02.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Pre-edit web-guideline refresh, Node slice markers and disposition placeholder

* Related IDs: P01, P02-T01, Critique Disposition, repository web guidance
* Evidence: repository instructions require loading and fetching web-design-guidelines before web edits; plan fetches only at P04; P02-T01 slices the "real" function without naming new START/END markers; the plan has "Pending" disposition.
* Concern: Rules are not refreshed before edits; the new test slice boundary could capture the `pendingHandoffs` to `let briefingBox` region by mistake; the disposition is not recorded.
* Impact: Process non-conformance and a brittle slice.
* Smallest useful change: Add a P01 precondition to fetch and read the guidelines; name the slice markers as the `WAITING_READ_ERROR` constant through the end of `handoffWaitingView`; record this critique's dispositions (accept PC-001 to PC-006) in the plan.
* Action owner: planning parent
* Exact resolving evidence: P01 precondition line; P02-T01 markers; Critique Disposition section filled.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Source claims verified; option (a) follows the `#/import` precedent with no API or navigation change.
* Failure honesty, no threshold sent, no mutation, CSV and pending card untouched, focused tier and C3 non-ticking are all explicit.
* Residual risk (accepted by design): the hidden-card state is only constructible with stubbed responses; historical correction balance is Unrecorded and one increment is authorised.

## Questions or Blocking Evidence Gaps

* None. No user decision is required.

## Limitations

* Plan-level review only; Chromium availability and existing test link-name lookups were not executed. A grep of src/api/tests found no references to "See all cases" or "Check a spreadsheet", so the plan's "link-by-name lookup" statement was not confirmed and the focused reruns remain the check.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: apply PC-001 to PC-006 directly to the plan and phase details, then finalize without another critique.
* User response required: no

## Related Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-11-11-issue-83-waiting-view-1111-plan.md](.copilot-tracking/plans/2026-11-11-issue-83-waiting-view-1111-plan.md) | Plan candidate |
| [.copilot-tracking/details/2026-11-11-issue-83-waiting-view-1111-phase-details.md](.copilot-tracking/details/2026-11-11-issue-83-waiting-view-1111-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-11-11-issue-83-waiting-view-1111-research.md](.copilot-tracking/research/2026-11-11-issue-83-waiting-view-1111-research.md) | Research |

## Next Steps

Standalone critique: no peer stage invoked. The planning parent applies the direct corrections above (`/rpi-plan` if run standalone); no user response is required.
