<!-- markdownlint-disable-file -->
# RPI Plan Critique: Read-only CSV copy of unaccepted handoffs (#1419)

## Metadata

* Task ID: 1419-handoff-csv-research-1110
* Critique date: 2026-11-10
* Plan: .copilot-tracking/plans/2026-11-10/issue-1419-handoff-csv-research-1110-plan.md
* Phase details: .copilot-tracking/details/2026-11-10/issue-1419-handoff-csv-research-1110-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: research and plan only; plan is a proposal; smallest scope (server.py CSV route reusing the JSON contract, focused synthetic parity tests under a controlled clock, separate truthful panel link, no serializer, core or role change, blank-header empty result preserved and documented, no ops.js, capacity_browser_check.py or app.js retry and session helper edits, no operational approval, proposed acceptance separate from observed evidence).
* Research and evidence considered: .copilot-tracking/research/2026-11-10/issue-1419-handoff-csv-research-1110-research.md (C1 to C28, not re-derived in full). Read-only spot checks at HEAD 12d3ac842 of src/api/src/zava_forward/api/server.py (JSON branch near L724-735 uses keep_blank_values and first value; EXPORT_KINDS and LIST_EXPORTS at L172-175; generic CSV dispatch near L494-500; get_kind; do_HEAD delegating to do_GET), src/api/src/zava_forward/api/web/app.js (pendingHandoffs near L754-775, existing /api/handoffs.csv link), src/api/tests/test_role_endpoint_inventory.py (GET_ENDPOINTS lists the JSON route).
* Decisions, dependencies, and acceptance criteria considered: plan Functional and Non-Functional Requirements, Acceptance Criteria, Root decisions, P01 to P05 and their detail sections, the stacked-parent dependency.
* Assessment boundary: documentary credibility of the plan against the supplied evidence and the caller requirements. Nothing was run; no claim about test outcomes, hosted CI or the active parent branch state beyond the cited pin.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Route reuses JSON contract, same rows, 13 fields, order | Covered | P02-T01 shared parser and branch; P03 cases 1 to 3. Source confirms JSON parse rules the plan restates. |
| Blank-value query drift (C2, C3) | Covered | Shared helper; P03 case 4. Confirmed: JSON uses keep_blank_values, generic CSV path uses q. |
| Kind mapping and role gate (C5, C6, C21) | Covered | EXPORT_KINDS entry plus inventory entry; P03 case 5. See PC-002 for the design ambiguity. |
| Control of the clock and exact comparison (C23) | Covered | P03-T01 clock patch and constant overwrite. See PC-005. |
| Panel link, separate and truthful (C17 to C19) | Partial | Wording and reachability claims are not tied to the route's actual scope. See PC-003. |
| Blank-header empty result preserved and documented | Partial | Preserved and tested; documentation is in P05 but not in any acceptance criterion, and the link text does not tell staff what an empty file means. See PC-003 and PC-004. |
| Forbidden files (ops.js, checker, retry helpers, core) | Covered | Owned-hunk table and Never touched list. |
| Proposed acceptance separate from observed evidence | Covered | Plan states all acceptance is proposed. |
| Validation tier | Partial | Left as a Root choice with a focused-tier lean. See PC-001. |
| Integration with the active parent | Covered | P01-T01 with SHA overlap statement. |

## Verdict

* Verdict: Revise
* Rationale: The scope is small, source-grounded and respects the caller's exclusions. Five planner-owned corrections remain: the validation-tier lean conflicts with repository rules for an authorization-sensitive route, the design choice is left open inside the tasks, the link wording makes claims not tied to verified scope, the empty-result limitation is missing from acceptance and user-facing text, and the parity test risks restating the serializer. None needs a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Validation tier leans to focused for an authorization-sensitive route

* Related IDs: P05, P05-T01, plan Acceptance Criteria
* Evidence: phase details P05 Context ("the proposal is the focused tier ... a doubt rule may require the full tier"); repository instructions state doubt takes the full tier and security-sensitive changes require it. The change adds an export endpoint behind a role gate and a kind mapping.
* Concern: The plan recommends the lighter tier and defers classification, while the rules say an authorization-sensitive change with doubt takes the full tier.
* Impact: An implementer may stop at targeted tests and the later review may then find the receipt missing.
* Smallest useful change: State full-tier classification as the planned default, with the basis (new data-exposing route reusing role gates), and allow downgrade only by a recorded Root decision.
* Action owner: planning parent
* Exact resolving evidence: P05 and the plan Acceptance Criteria name the tier, the basis, and the full-gate commands or the recorded downgrade authority.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Design choice is left open inside P02 although the scope fixes it

* Related IDs: P01-T02, P02, P02-T01, C5
* Evidence: P02-T01 Unresolved Items ("Design A versus the shared branch is a Root choice; A also needs a list_rows raw-query change, a typed 400 and a registry-test edit"); P02 Boundaries already exclude LIST_EXPORTS "(recommended design)". Source: LIST_EXPORTS membership routes through list_rows and the generic CSV path with the non-blank-retaining q.
* Concern: Design A (registry) widens the touched surface (list_rows, typed 400, test_list_export_api registry equality) beyond the caller's smallest scope, yet remains an open Root choice that could block P01-T02 and change the owned-hunk table.
* Impact: Ambiguous owned hunks, possible edits to a shared registry test, and avoidable conflict with other #80 children.
* Smallest useful change: Make the shared server.py branch the plan of record, move Design A to a rejected alternative with the reason, and drop it from the Root decisions.
* Action owner: planning parent
* Exact resolving evidence: plan and details name one design; Root decision list no longer contains it; owned-hunk table unchanged.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Link and helper wording assert scope and behaviour not verified against the route

* Related IDs: P04, P04-T01, C17 to C19
* Evidence: P04-T01 helper text ("each handoff you can see", "only handoffs past their own due time are marked"); app.js pendingHandoffs shows the panel and link only when /api/handoffs returns rows and hides it when empty; the CSV route's rows depend on role and ownership logic in unaccepted_handoffs, not on the pending list.
* Concern: Wording is proposed without a mapping from each sentence to the verified role scope and to the needs_escalation or due-time semantics. The link is also unreachable when the pending list is empty while the CSV may still have rows for a manager or sender. Nothing tells staff that an empty file (blank-header body) means no qualifying rows rather than a failure.
* Impact: A control labelled "truthful" could mislead staff; the caller's requirement of a truthful separate link is not demonstrated.
* Smallest useful change: Add to P04-T01 a claim-to-evidence table for each helper sentence (role scope, marking rule, empty-file meaning), add one plain sentence for an empty file, and record the reachability limitation in the user-facing README text as well as the plan. Keep wording owner review.
* Action owner: planning parent
* Exact resolving evidence: P04-T01 contains the claim-to-evidence table citing workflows.unaccepted_handoffs lines and the empty-file sentence.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Blank-header documentation is not an acceptance criterion

* Related IDs: Functional Requirements, Acceptance Criteria, P05-T01
* Evidence: plan Goals and Scope state the empty result is preserved and documented; Acceptance Criteria and P05-T01 completion evidence do not name the documented limitation or the no-serializer-change check.
* Concern: Two caller requirements (preserve and document) are verified only by one role case in tests.
* Impact: Documentation may be omitted without any criterion failing.
* Smallest useful change: Add proposed acceptance items: README states the blank-header empty body and its limitation; git diff shows no change to list_export.py, projection.py, workflows.py or role sources.
* Action owner: planning parent
* Exact resolving evidence: Acceptance Criteria and P05-T01 list both items as proposed checks.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Parity oracle may restate the serializer

* Related IDs: P03-T01 cases 1 and 6, C20 to C23
* Evidence: case 1 compares CSV cells to "normalised JSON values" (None to empty, bool to Yes or No, compact JSON, apostrophe rule), which is the to_csv logic itself.
* Concern: A test that reimplements normalisation cannot detect a shared misreading and duplicates a serializer already tested elsewhere.
* Impact: False confidence; tests restate implementation.
* Smallest useful change: Use literal expected cell strings for one fixed synthetic row (controlled clock) and a generic comparison only for column order and row order; leave edge-text normalisation to the existing list-export tests apart from one smoke case.
* Action owner: planning parent
* Exact resolving evidence: P03-T01 case 1 specifies literal expected values for a fixed row.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Confirmed in source: JSON parser uses keep_blank_values with first value and rejects out-of-range values; generic CSV dispatch would diverge, so the shared helper is justified; EXPORT_KINDS needs the mapping and the inventory test lists the JSON route.
* The plan keeps forbidden files untouched, separates proposal from evidence, and discloses unrun checks.
* Residual (accepted by plan): stacking on an active unpublished parent; line numbers drift; optional browser test not run.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only review of supplied artifacts and spot checks at HEAD 12d3ac842; C1 to C28 not independently re-verified end to end; no tests, app or CI run; parent branch state not inspected.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: direct revision of the plan and details for PC-001 to PC-005, then record dispositions in the plan table
* User response required: no
