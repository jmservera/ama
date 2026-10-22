<!-- markdownlint-disable-file -->
# RPI Plan Critique: Paid execution plan #126, revised USD 700 demo budget

## Metadata

* Task ID: 126-demo-budget-700
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-demo-budget-700-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/paid-execution-plan-126-demo-budget-700-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: documentation-only revision of the costed Azure demo plan to the owner's USD 700 all-in forecast ceiling (replaces USD 500, not additional); expiry 2026-10-25T16:02Z unchanged; private Blob on the existing storage account; unknown spend never assumed zero; no retirement or role changes; no paid execution.
* Research and evidence considered: .copilot-tracking/research/2026-10-22/paid-execution-plan-126-demo-budget-700-research.md; the current subsection "Finite Costed Execution Plan Options for an Unfinished Azure Demo (2026-10-20, #126)" in docs/case_study_48_addendum.md (lines 326 onward).
* Decisions, dependencies, and acceptance criteria considered: plan user decisions, functional and non-functional requirements, P01-T01, P01-T02, P02-T01, follow-up items.
* Assessment boundary: arithmetic recomputed from the research table; consistency checked against the existing rules in the addendum. No live Azure evidence was re-read, so W1 to W4 values are taken as supplied.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| USD 700 replaces 500, not additional | Covered | Plan decisions; research Wave 3 rejects the 1,235 reading |
| Expiry unchanged | Covered | Plan and research; latest-start rules inherited from the addendum |
| Arithmetic (W1, envelope) | Covered | Recomputed: 232.93 + 10 x 30.24 = 535.33; 655 - 535.33 - 30 = 89.67; admissible U 84.67, 74.67, 66.67, 51.67 all correct; 560, 630, 665 are 80, 90, 95 percent of 700; 625 < 630. See PC-002 for derivation gaps |
| Unknown spend never zero | Covered | U unknown keeps all tranches blocked |
| Private Blob on existing account (B1) | Partial | B1 is named but not specified in the plan or details (PC-003) |
| No retirement or role changes | Partial | T1 as carried needs role, tenant and ingress mutations (PC-001); S1/S2 handling unstated (PC-004) |
| Sensitive-identifier risk | Partial | Non-functional criterion has no defined search (PC-006) |
| P01-T01, P01-T02 | Partial | Targets correct; content list incomplete (PC-003, PC-004, PC-005) |
| P02-T01 | Partial | Gate steps thin (PC-007) |

## Verdict

* Verdict: Revise
* Rationale: The core numbers are arithmetically sound and the owner constraints are captured. No finding needs a user decision, but there are substantive gaps a planner can correct directly: a retained tranche conflicts with the no-role-change constraint, the threshold and envelope mapping is under-explained, B1 is unspecified, and the stale-figure and identifier checks are not testable.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Carried tranche T1 depends on mutations the owner has not authorized

* Related IDs: P01-T01; plan "User Decisions and Requirements"; addendum T1 approval fields
* Evidence: docs/case_study_48_addendum.md (T1 may need tenant registration and consent, roster initialization, replacing the deny-all ingress restriction; managed-identity sentinel invalid); plan decision "no ... access or role-assignment change is authorized".
* Concern: P01-T01 keeps T1 to T3 "as bounded additions" and lists a B1 + T1 + T2 admissible-U row. T1's own preconditions need access, role and ingress changes that this task says are not authorized. B1 also needs an existing managed-identity role that cannot be granted here. A reader could take T1 as approvable at 8.
* Impact: Implies an option the owner constraints exclude and mixes a ceiling with an unpermitted action.
* Smallest useful change: In P01-T01, state that T1 and B1 are each blocked until their separate mutation or role approvals exist, that this document authorizes none, and that the admissible-U rows are arithmetic limits only. Keep T3 "not approvable".
* Action owner: planning_parent
* Exact resolving evidence: P01-T01 text and the resulting addendum subsection carry the per-option blocker list; reviewer can find no wording that reads as approval of any role, ingress or tenant change.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Envelope cap 655 and threshold mapping are not derived or tied to a measured quantity

* Related IDs: P01-T01; research "Parent Synthesis"
* Evidence: research (E at most 655; L start at most 625; review 560, pause 630, stop 665); addendum rule E at most 475 equals the old stop line.
* Concern: The old rule set E equal to the stop line (475) and L start at most 445 (below pause 450). The new E of 655 is 10 below the stop line 665 and the pause margin is 5, with no stated reason. The plan also does not say that E includes R, that L excludes R, or that the three thresholds are compared with L (not observed spend). Because L starts at 535.33 + U + ceilings, the review line of 560 fires at once when U plus ceilings exceed 24.67, which is not mentioned. The 5 headroom to the pause line equals the B1 ceiling, so any B1 overrun pauses the work.
* Impact: A reviewer cannot reproduce why 655, and an operator could compare observed spend with 560/630/665 and never stop.
* Smallest useful change: Add to P01-T01 one sentence deriving 655 (L start at most 625 below pause 630, plus R 30), define E and L as in the addendum, state that thresholds apply to L, and note the immediate review trigger above 24.67.
* Action owner: planning_parent
* Exact resolving evidence: the subsection shows E, L, R, and the inequality chain 535.33 + U + ceilings <= 625 and E = that + 30 <= 655, with thresholds labelled as L.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: B1 is named but its finite bounds, gates and ceiling basis are not planned

* Related IDs: P01-T01; research Wave 2
* Evidence: research (1 GB, 100,000 writes, 1,000,000 other operations is about 1.08 at list price; ceiling 5 proposed; private-link data meter unpriced; retention not read; role unverified).
* Concern: Neither plan nor details lists what B1 must contain: container count and lifetime, byte and operation caps, synthetic data only, no index tags or result tags, retention and soft-delete or versioning liability counted against the cap until expiry, deletion of only the created container at end, latest start per the expiry rule, approval fields, stop rule, and the role-assignment check as a hard gate. The ceiling of 5 is about 4.6 times the list estimate with the reason stated only as unknown meters.
* Impact: The one new option is the item the owner will approve, yet it could be written without bounds.
* Smallest useful change: Add a B1 row to the P01-T01 content list matching the tranche table columns (BOM, finite bounds, ceiling) and mark the role and retention checks as pre-start gates.
* Action owner: planning_parent
* Exact resolving evidence: addendum B1 row with caps, retention treatment, cleanup, latest start and gates; each figure traces to W3 or to the stated allowance.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Status of S0, S1 and S2 under the new ceiling is not restated

* Related IDs: P01-T01; addendum options table
* Evidence: addendum options table (S0 "Blocked (over cap)", S1 and S2 require retirement or idling); research (Front Door retirement not authorized).
* Concern: Under 700, S0 (535.33) is no longer over the cap and becomes the only authorized baseline, but the plan only says retirement is excluded. The E formula still refers to "option projection". Old S1 and S2 figures could survive as current rows.
* Impact: Leaves a stale blocked label or an implied retirement path in a document meant to show one current decision.
* Smallest useful change: Specify that S0 is the sole current baseline with its 535.33 projection, S1 and S2 move to the dated history block marked not authorized, and the E formula uses the S0 projection.
* Action owner: planning_parent
* Exact resolving evidence: revised options table with S0 only; history block contains S1 and S2 labelled 2026-10-20.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Stale-figure sweep is scoped too narrowly, and run-rate sensitivity is missing

* Related IDs: Functional requirement 2; P01-T01, P01-T02; research Wave 3
* Evidence: grep of the addendum shows 500 at lines 331 and 367 only in this subsection, but the acceptance test covers only "no unqualified 500 total remains" without naming files; the forecast rests on four complete days at 30.24.
* Concern: Other current documents (index row, EXA-012 budget row, PR #422 body, any other mention of 450, 475 or 400 as current) are not in the sweep. The headroom of 89.67 falls by 10 for each 1.00 per day of run-rate increase, so a 3 per day rise removes 30, yet no refresh trigger is stated.
* Impact: A stale cap can survive elsewhere; a small burn change silently invalidates the admissible-U table.
* Smallest useful change: Add a repository search for 500, 475, 450 and 400 in docs/reference/README.md, the addendum and the PR body, with each hit classed as history or fixed. Add one sentence that the table is valid only for the stated run rate and must be recomputed from the live 4-day rate at each check.
* Action owner: planning_parent
* Exact resolving evidence: recorded search output in the changes record with each hit classified; subsection states the sensitivity of 10 per 1.00.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Sensitive-identifier check is not testable

* Related IDs: Non-functional requirement 1; P01-T01 validation
* Evidence: plan "a search of the diff for identifiers finds none"; the addendum already names resource group `ama` and a storage account type.
* Concern: No patterns are defined. The criterion lists "account name" while `ama` (a resource group name) and counts such as 94 resources and eight private endpoints are intentionally kept. Raw error codes and the role/identity descriptions are also near the sensitive boundary.
* Impact: The check cannot fail or pass reproducibly, and the allowed items are unclear.
* Smallest useful change: Define patterns (GUIDs, email addresses, tenant or subscription domains, storage account host names, resource IDs beginning /subscriptions, keys) and list the allowed exceptions (`ama`, aggregate counts).
* Action owner: planning_parent
* Exact resolving evidence: validation step records the patterns, the diff search result across committed files including the research artifact, and the exceptions.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Publication and arithmetic validation steps are thin

* Related IDs: P02-T01; P01-T01 validation
* Evidence: phase details P02-T01 (no base, receipt directory or commit order); repository gate requires a fetched reviewed main, committed evidence, an external receipt and exact-head review.
* Concern: P02-T01 omits fetching main and recording the reviewed base, committing the critique and original RPI evidence before the gate, and avoiding any later commit after the receipt. "Each number traces to the research table" is a manual check.
* Impact: A late edit would invalidate the receipt, and the arithmetic could drift between the research and the text.
* Smallest useful change: Add the ordered steps and a small recomputation of the figures (535.33, 89.67, four admissible-U values, the three thresholds) recorded in the changes record.
* Action owner: planning_parent
* Exact resolving evidence: changes record lists base SHA, receipt path, verification command output and the recomputed values.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* The arithmetic is correct and the replacement (not additional) reading, expiry, unknown U and no-retirement constraints are carried consistently.
* Reconciliation with the 2026-10-20 read avoids double counting (172.46 versus 172.47).
* Residual risk: U remains unknown and the managed-identity Blob role is unverified, so every paid tranche stays blocked; the owner or tenant operator must resolve these outside this task.
* Residual risk: Azure cost data lags and list prices are not agreement prices, so the forecast is an estimate.

## Questions or Blocking Evidence Gaps

* None that block planning. Owner access to subscription-scope cost and the Blob role are execution blockers recorded in the plan, not planning blockers.

## Limitations

* No live Azure re-read; evidence is as supplied in the research artifact.
* The remaining addendum text after line 470 and other documents were not reviewed beyond the grep.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: apply the seven direct corrections to P01-T01, the validation expectations and P02-T01, then finalize without a further critique.
* User response required: no
