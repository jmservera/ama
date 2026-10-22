<!-- markdownlint-disable-file -->
# RPI Plan Critique: Paid execution plan #126, post-change forecast correction

## Metadata

* Task ID: 126-postchange-correction
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: documentation-only correction; keep observed costs; label 535.33 and derived limits a conservative PRE-CHANGE scenario; no invented savings or zero residual; refreshed post-change forecast before any tranche; U unknown; paid execution blocked; USD 700 total ceiling and expiry unchanged; no Azure mutation; no scope expansion.
* Research and evidence considered: .copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md; docs/case_study_48_addendum.md lines 326-500 (current, uncorrected text); docs/reference/README.md line 315; docs/reference/log.md 2026-10-22 entry (line 6650).
* Decisions, dependencies, and acceptance criteria considered: plan acceptance criteria and P01/P02 tasks.
* Assessment boundary: plan-level credibility against the uncorrected target text. The edits do not exist yet, so the final wording cannot be assessed. Live Azure facts (W1 to W3) and the 14:16Z deletion verification are caller-supplied and were not re-verified.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Label 535.33, 164.67, 89.67/84.67/74.67/66.67 | Covered | Plan acceptance names all; addendum lines 364-365, 387-390 are the targets. |
| Remove "current" claims | Partial | Plan names "S0 only current baseline" (line 374) and the "Current evidence" lead-in (line 352) only implicitly; "S0 no change" (line 457), "unchanged inventory (94 resources)" (line 372) and the history block are not enumerated (PC-002, PC-004). |
| "Retirement not authorized" sentence (line 345-348) | Partial | Only in phase-details context; not in the plan, tasks or acceptance (PC-001). |
| Refresh gate before any tranche | Partial | Inputs listed in plan but no owner, minimum data, or feasibility against expiry (PC-003). |
| Index row / log | Partial | Log is append-only, so the 14:00Z entry saying "forecast with no change" stays; no superseding wording is specified (PC-005). |
| No invented savings / zero residual | Covered | Research contrarian wave; but see PC-006 on "conservative". |
| P02 gate and publication | Covered | Matches repository gate; no further concern. |

## Verdict

* Verdict: Revise
* Rationale: The correction approach is sound and within scope, but the plan leaves several contradictory statements and a few gaps outside its explicit task list (retirement sentence, history block, log supersession, "conservative" claim, refresh gate feasibility). All are direct planner corrections; none needs a new owner decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: "Retirement not authorized" sentence is left contradicting the completed deletion

* Related IDs: P01-T01, Acceptance Criteria; addendum lines 345-348
* Evidence: docs/case_study_48_addendum.md lines 345-348 state Front Door or other resource retirement is "not authorized" and S1/S2 "are not offered". Phase details P01 Context mentions the fix, but the plan, P01-T01 and acceptance criteria do not.
* Concern: The text sits inside "Owner decisions, 2026-10-22" and would read as if the deletion was never authorized or happened, while a later owner-authorized deletion was completed. Also no repository evidence records the later authorization (who, when); the research takes it from a coordinator report.
* Impact: Contradiction and an unsourced authorization claim in an owner-decision record.
* Smallest useful change: Add to P01-T01 and acceptance: keep the earlier sentence as the decision as of its time, add a dated later note that the owner subsequently authorized and completed deletion of only the cutover-test Front Door Premium profile and WAF policy plus the demo API scale-down (verified 14:16Z), that this lies outside this proposal's tranches, and that any further retirement, RG deletion, identity or role change remains unauthorized. Cite the authorization by decision date/reference without inventing wording.
* Action owner: planning parent
* Exact resolving evidence: addendum diff shows the dated note; the phrase "not authorized" no longer applies to the completed deletion; authorization reference is the caller-supplied owner decision stated as such.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Other "current/no change/94 resources" statements not enumerated

* Related IDs: P01-T01; addendum lines 352, 372-374, 443, 457-458
* Evidence: line 352 "Current evidence ... 13:57Z and 14:00Z"; line 372 "inventory was unchanged ... (94 resources, eight private endpoints)"; line 374 S0 sentence; line 443 "94 resources ... including a Front Door Premium profile"; line 457-458 S0 "535.41 Blocked" and "S1 retire Front Door ... needs a separate retirement approval".
* Concern: Plan validation only searches "current", "no change", "S0" in the subsection. The 94-resource and Front Door-present statements, and the history S1 row (which now describes an action already done by a different route), are not caught. Line 372's "unchanged" is false after 13:57Z.
* Impact: Residual stale or contradictory facts survive.
* Smallest useful change: Add an explicit checklist to P01-T01 and validation: lines 352, 372, 374 (relabel as "13:57-14:00Z pre-change read"), 364 row label ("Forecast, no change" becomes "Pre-change scenario"), 443 and 458 (add a one-line dated note that the history predates the deletion; keep history text unchanged), and grep "94", "Front Door", "S0", "no change", "current", "unchanged" across the whole subsection and onward to line 500.
* Action owner: planning parent
* Exact resolving evidence: grep results listed in the changes record with each hit classified as relabelled, history-with-note, or correct.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Refresh gate is not operable against the expiry

* Related IDs: Functional requirement 2, Follow-Up Items; research W2
* Evidence: deletion at about 14:16Z on 22 Oct; cost data lags; "complete post-change days" first exist for 23 Oct; authorization expires 2026-10-25T16:02Z.
* Concern: The gate lists inputs but not the minimum evidence (how many complete post-change days, how to treat residual meters on deleted resources, who recomputes E, L and admissible U, which timestamp), nor that practical time before expiry is short, so the likely outcome is no tranche before expiry without a new owner decision. The plan also does not say the refreshed forecast must account for the 61 remaining cutover-test items and any new charge.
* Impact: A reader could think a quick refresh unlocks tranches, or that expiry may be extended.
* Smallest useful change: State the gate explicitly: fresh inventory and cost read with timestamps, at least one complete post-change day (23 Oct) measured, recomputed L/E/U limits, named owner approval of the refreshed figures; add that expiry is unchanged and a missed gate means the tranche stays blocked (no extension implied).
* Action owner: planning parent
* Exact resolving evidence: addendum gate paragraph containing those items and the expiry statement.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Dependent tranche definitions assume resources that changed

* Related IDs: T1, B1; addendum lines 500-510 and 544
* Evidence: T1 is "usable sign-in on the existing demo API"; line 544 describes the existing demo API as returning 403; research W1 says the app is scaled to 0 and Front Door is deleted.
* Concern: Statements about the demo API's present behaviour and any public edge may no longer hold; the plan does not decide whether to add a dated "as of 13:57Z" qualifier or note that T1 preconditions need re-inventory.
* Impact: Minor stale operational claim; no scope expansion needed, only a qualifier.
* Smallest useful change: Add a dated qualifier at line 544 and in the T1 "Blocked until" cell (or the refresh gate) stating T1 depends on the refreshed inventory; do not change bounds.
* Action owner: planning parent
* Exact resolving evidence: diff showing the qualifier; tranche bounds and ceilings unchanged.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Append-only log and index row do not supersede earlier wording

* Related IDs: P01-T02; docs/reference/log.md line 6650; docs/reference/README.md line 315
* Evidence: log line 6650 says "535.33 forecast with no change" and cannot be edited; the README row says the revision "replaces the USD 500 total ... (the outside-group term stays unknown)" without the pre-change label.
* Concern: P01-T02 says only "consistent wording". The new log entry must explicitly state that the earlier entry's figure is the pre-change scenario, with the dated reason, observed vs scenario vs absent post-change forecast, and unchanged ceiling/expiry; the index row must carry the label and the refresh gate. The plan also lists a changes record path but no requirement to update the knowledge-base log and index in the same commit.
* Impact: A reader of the log alone still sees a "no change" forecast as current.
* Smallest useful change: Specify the log entry content and that the index row adds "pre-change scenario; refreshed post-change forecast required"; keep ms.date at 2026-10-22 (already) and note no earlier log lines are edited.
* Action owner: planning parent
* Exact resolving evidence: git diff of log.md is additions only; README row contains the label.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: "Conservative" is unproven and internally hedged

* Related IDs: Acceptance criteria; research Contrarian wave
* Evidence: research says 535.33 is "an upper-bound style figure only if no new cost was added"; W1 notes remaining cutover-test resources and possible residual charges.
* Concern: Calling it "conservative" without qualification implies that real cost will be lower, which is exactly the unmeasured saving the task forbids asserting. The reasoning also needs to say that the 242.36 observed already includes pre-deletion charges and that 22 Oct partial-day cost is not post-change.
* Impact: Risk of an implied saving or of rejecting the scenario if costs rise.
* Smallest useful change: Use wording: "pre-change scenario: assumes the pre-change run rate continues, conservative only in that it does not credit any unmeasured saving; it is not an upper bound and not a post-change forecast; actual cost may differ either way". State that no post-change forecast exists.
* Action owner: planning parent
* Exact resolving evidence: addendum sentence matching that wording; no "bound" language.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Validation and plan bookkeeping gaps

* Related IDs: Non-functional requirement, P02, Plan metadata
* Evidence: plan Executive Summary says U blocked items; "Latest critique" and "changes" artifacts referenced; non-functional threshold "identifier search finds none in additions" does not name the search.
* Concern: No named identifier search (subscription IDs, resource names) and no check that resource group name `ama` and aggregate counts are the only environment details; arithmetic checks (232.93 + 10 x 30.24 = 535.33; 655-535.33-30 = 89.67 etc.) are asserted but not required as an explicit step in P02; the dated "14:53Z" timestamp must be consistently labelled as read-only inventory time.
* Impact: Low; hygiene only.
* Smallest useful change: Add to P02-T01 validation: re-run the arithmetic, grep additions for GUIDs and resource IDs, and record results in the changes record.
* Action owner: planning parent
* Exact resolving evidence: changes record lists arithmetic and grep outputs.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Correct posture: observed retained, pre-change scenario relabelled, no savings or zero residual invented, ceiling and expiry unchanged, read-only, no scope expansion, history preserved.
* Residual risk (accepted by design): no post-change cost evidence exists until cost data catches up; U remains unknown; paid execution remains blocked.

## Questions or Blocking Evidence Gaps

* None decision-critical. The coordinator report of deletion authorization/verification is unsourced in the repository; PC-001 asks to attribute it as caller-supplied evidence rather than assert it.

## Limitations

* Target text not yet edited; live Azure facts not re-verified; no research beyond supplied inputs.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: fold PC-001 to PC-007 into P01-T01, P01-T02 and P02 validation, then implement; no further critique.
* User response required: no

| Artifact | Description |
|----------|-------------|
| [.copilot-tracking/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan.md](.copilot-tracking/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan.md) | Plan critiqued |
| [.copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md](.copilot-tracking/details/2026-10-22/paid-execution-plan-126-postchange-correction-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md](.copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md) | Research |

## Next Steps

No user action required. Planning parent revises directly per PC-001 to PC-007 and proceeds to implementation.
