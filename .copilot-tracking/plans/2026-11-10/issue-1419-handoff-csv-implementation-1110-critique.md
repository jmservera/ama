<!-- markdownlint-disable-file -->
# RPI Plan Critique: Read-only CSV copy of unaccepted handoffs, implementation (#1419)

## Metadata

* Task ID: 1419-handoff-csv-implementation-1110
* Critique date: 2026-11-10
* Plan: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-implementation-1110-plan.md
* Phase details: .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-implementation-1110-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context: single critique of the implementation plan; confirmed user decisions are not re-litigated (shared parser and branch; 13 fields; Offered, Received and Escalated in, Accepted, Completed, Declined and Withdrawn out; no core, role, projection, serializer or threshold change; one EXPORT_KINDS mapping, no LIST_EXPORTS entry; filename unaccepted-handoffs.csv; link text; targeted validation by owner demo policy; no new queue UI).
* Evidence considered: the plan, phase details and the implementation research (not re-derived), the earlier critique for format, and read-only spot checks of src/api/src/zava_forward/api/server.py (get_kind L202-244, EXPORT_KINDS L174, do_HEAD L430, projection gate L497, JSON branch L724-734), src/core/src/zava_forward/core/workflows.py (_now L27, handoff_ageing L60-85, unaccepted_handoffs L336-349, HANDOFF_PENDING L18), projection.py (allowed L65-72), list_export.py, src/api/tests/test_role_endpoint_inventory.py, test_handoff_api.py, test_handoff_read_guidance.py, app.js pendingHandoffs L754-775.
* Boundary: documentary credibility of the plan against the cited source. Nothing was run; no claim about test, browser or CI outcomes.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Gate order 401, kind 403, parse 400, store 403 | Covered | Source confirms: 401 at L494-ish, `projection.allowed(u, get_kind(path))` at L497 precedes the JSON branch at L724. Contractor and Application Administrator are denied by kind (projection.py L67-71) so an invalid limit yields 403, not 400. The plan's expected order is correct. |
| Kind mapping | Covered | `"/api/handoffs/unaccepted.csv"` is not in LIST_EXPORTS, so only the EXPORT_KINDS entry (checked before the fallback dict, L237) routes it. Must map to `"handoffs"`. |
| Role-inventory hazard | Covered | One GET_ENDPOINTS entry satisfies the route-regex test; the every-role test then calls it for all roles plus Mystery. See PC-105 for what it does not prove. |
| Controlled clock | Partial | Patch target is valid (`_now` is a module global used at L339). Crafting detail is thin. See PC-102. |
| HEAD and POST | Partial | See PC-103. |
| Panel link and wording | Partial | See PC-101 and PC-104. |
| Browser check | Partial | See PC-106. |
| Negative boundaries | Partial | See PC-105. |
| Scope and forbidden files | Covered | Owned-hunk table is tight; no creep found beyond PC-104 wording volume. |

## Verdict

* Verdict: Revise
* Rationale: The server design, gate order and exclusions are sound and match source. No High finding. Six planner-owned corrections would remove ambiguity that could make tests infeasible or flaky, or leave link reachability and wording unproven: link visibility is tied to a different list than the CSV scope, test state crafting is unspecified, HEAD and POST expectations are not pinned, helper text lacks a claim-to-column mapping, some negative boundaries are missing, and the browser plan has unverified prerequisites. None needs a user decision.

## Findings

<!-- rpi:critique id=PC-101 -->
### PC-101 [Medium]: Link reachability follows the personal pending list, not the CSV scope

* Related IDs: P03-T01, P03-T02, plan Acceptance Criteria, "What You May Not Know"
* Evidence: app.js L758-760: the link is rendered only when `/api/handoffs` (the signed-in user's pending list) returns rows; otherwise the box is hidden. `unaccepted_handoffs` (workflows.py L343-348) returns rows for a manager for every unaccepted handoff, and for a sender or receiver on their own. Plan text says the empty file is reachable "mainly by a direct request" and the helper says "all handoffs you can see".
* Concern: A manager with nothing personally pending sees no link although the CSV would hold rows. The plan frames the hidden-panel limit as an empty-file matter; it is a reachability matter for the manager scope. The "unavailable or empty boundary" browser check cannot be exercised through the UI.
* Impact: The control is under-discoverable for the audience the helper text promises, and the browser evidence may claim more than it shows.
* Smallest useful change: Record in the plan, README paragraph and Review notes that the link appears only while the user has a handoff waiting; make the browser empty-boundary check a direct authenticated request and the UI check assert absence of the panel; do not widen the panel (no new queue UI).
* Action owner: planning parent
* Exact resolving evidence: plan and P03-T02 state the visibility limit and the method for the empty boundary.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-102 -->
### PC-102 [Medium]: State crafting and clock patching are not specified enough to be reliably feasible

* Related IDs: P02-T01, C4 to C8
* Evidence: P02-T01 says "handoff dicts crafted exactly" and `workflows._now` patched "to a fixed minute-precision string". Source: API actions stamp `_now("microseconds")` (workflows.py L262-318), so with a patch returning one constant every action timestamp collapses; ageing parses `offered_at` and `due_at` with `fromisoformat` and needs a timezone (L69-75); rows are sorted by `-age_hours` (L349), so equal ages leave order to dict iteration. Existing precedent patches with `return_value="2026-10-01T12:00+00:00"` (test_progress_report_api.py L295).
* Concern: Which states are crafted by direct mutation of `store.cases[...]["handoff"]` and which by API is unstated; the patch scope across the server thread is unstated; the order assertion is fragile with ties; Withdrawn, Declined, Accepted and Completed exclusions need exact state strings and `offered_at` values.
* Impact: Flaky or vacuous parity and exclusion tests.
* Smallest useful change: State that handoffs are set by direct in-memory mutation with explicit `offered_at` and `due_at` ISO strings with offsets, `_now` is patched for the whole request lifetime with the existing precedent format, every included row has a distinct age, and one assertion checks the `as_of` column equals the patched value.
* Action owner: planning parent
* Exact resolving evidence: P02-T01 names the crafting method, clock patch scope and distinct-age rule.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-103 -->
### PC-103 [Low]: HEAD and POST expectations are not pinned

* Related IDs: P02 Validation Expectations, plan Tests list
* Evidence: do_HEAD simply calls do_GET (server.py L430-431), so a HEAD on the CSV path runs the same branch; the existing JSON test pins a POST to `/api/handoffs/unaccepted` as 404 (test_handoff_api.py L167). The plan only says "current behavior without inventing method support".
* Concern: "Current behavior" has no expected values, so a regression or accidental new method could pass.
* Impact: Weak negative boundary.
* Smallest useful change: Assert HEAD and POST outcomes on the CSV path equal the JSON route outcomes for the same user (POST 404, HEAD same status and same denial gates), and that signed-out HEAD is 401.
* Action owner: planning parent
* Exact resolving evidence: P02 names those assertions.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-104 -->
### PC-104 [Medium]: Helper wording has no claim-to-column mapping and may mislabel behavior

* Related IDs: P03-T01, Functional Requirements (panel)
* Evidence: helper claims "past-due handoffs can still show as overdue" and "no resident contact details". Columns are case_id, status, age_hours, due_at, chase_owner, chase_owner_code, proposed_receiver, escalated, needs_escalation, reasons, approved_limit_hours, limit_note, as_of (workflows.py L79-86); the flag is `needs_escalation` with reason "Handoff due time has passed", not "overdue"; a null `due_at` is never flagged; `needs_escalation` is false for Escalated rows; `reasons` is a compact JSON list cell; the export carries staff names and case ids. Six claims sit in one helper paragraph.
* Concern: The wording introduces a term ("overdue") the file does not use and says nothing of a null `due_at`; the earlier critique's claim-to-evidence request (PC-003) is not carried into this plan.
* Impact: A control meant to be truthful may mislead; long text weakens plain-language compliance.
* Smallest useful change: Add a short claim-to-column table to P03-T01, align terms to the file ("needs escalation", "due time has passed"), and cut the helper to the claims the owner decisions require.
* Action owner: planning parent
* Exact resolving evidence: P03-T01 contains the mapping and the final shortened helper wording.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-105 -->
### PC-105 [Low]: Missing negative boundaries and refactor-regression checks

* Related IDs: P01-T01, P02-T01
* Evidence: JSON branch (L724-734) is being rewritten; as_of is not a parameter and `s.unaccepted_handoffs` is called without it; `get_kind` falls to `"unknown"` for unlisted paths; the inventory every-role test only asserts no 500, contractor and Mystery 403 or 404, and no canaries.
* Concern: Not listed: a supplied `as_of` or other query key on both routes cannot change rows or the `as_of` column; near-miss paths (`.csv/`, `.CSV`, `/api/handoffs/unaccepted.csv.bak`) stay denied or 404 and never reach the branch; `/api/handoffs.csv` and its filename are unchanged; the JSON route's status, body and content type are unchanged by the shared helper (existing test_handoff_api covers only part of this); the inventory test does not prove Application Administrator denial on the new path.
* Impact: Scope or refactor regressions pass unnoticed.
* Smallest useful change: Add those five assertions to the new module (small, literal) and record that the unchanged-JSON proof is the existing test_handoff_api run plus an equality case for the JSON body.
* Action owner: planning parent
* Exact resolving evidence: P02 Validation Expectations list them.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-106 -->
### PC-106 [Low]: Browser check prerequisites and meaning of a skip are unverified

* Related IDs: P03-T02, Dependencies, plan Acceptance Criteria
* Evidence: the browser class is opt-in on `ZF_BROWSER_TESTS=1` (test_handoff_read_guidance.py L185), so a plain unittest run reports a skip; the plan relies on Playwright in the user cache and on the venv `/home/azureuser/.venvs/issue1419` without a stated import check; "synthetic owned server" in-process versus subprocess is not stated, yet "store unchanged" needs a way to compare state; keyboard activation of a `download` anchor needs a download expectation.
* Concern: A skipped class could be recorded as browser evidence; the unchanged-store assertion has no mechanism.
* Impact: Overstated or unobtainable evidence.
* Smallest useful change: State the exact command with the env var, require the record to show it ran (not skipped), name the server mode and the store comparison (in-process store snapshot before and after, or data-directory file hash), and add an import check for playwright in the venv before the lock is taken; otherwise record a precise partial as already planned.
* Action owner: planning parent
* Exact resolving evidence: P03-T02 and P04-T01 state command, skip handling and snapshot method.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-107 -->
### PC-107 [Low]: Helper naming mismatch between plan and details

* Related IDs: P01-T01, plan In Scope
* Evidence: the plan names a module-level `max_age_hours` helper; details name `_max_age_hours(url)`. `max_age_hours` is also the keyword used at the call site and the name of the query key.
* Concern: Shadowing and ambiguity at implementation.
* Impact: Minor rework.
* Smallest useful change: Use `_max_age_hours(url)` in both documents.
* Action owner: planning parent
* Exact resolving evidence: plan and details agree.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Gate order, kind mapping and the no-LIST_EXPORTS choice are correct against source, and the shared parser removes the confirmed `keep_blank_values` drift of the generic CSV path.
* Forbidden-file list and validation override are explicit and honest about what does not run.
* Residual (accepted by plan): hosted CI and independent exact-head review are unavailable here; heavy lock may be busy.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only; spot checks of source at the worktree HEAD; research claims C1 to C15 not re-derived; nothing run.

## Recommended Next Action

* Highest-impact finding: PC-101 (with PC-102 and PC-104 as the other Mediums)
* Action owner: planning parent
* Smallest next action: direct plan and details revision for PC-101 to PC-107, then fill the Critique Disposition table
* User response required: no

## Next Steps

No user action is required. The planning parent revises the plan and details directly, records dispositions, then implements.
