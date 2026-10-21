<!-- markdownlint-disable-file -->
# RPI Plan Critique: climate-paired-source-178

## Metadata

* Task ID: 178-paired-continuation
* Critique date: 2026-10-21
* Plan: .copilot-tracking/plans/2026-10-21/climate-paired-source-178-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/climate-paired-source-178-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: issue #178 (jmservera/ama); owner decision to use Met Office UKCP18 / EA OGL where available, else clearly labelled synthetic; no account, credentials or private data; evidence-only blocker delivery because anonymous paired records cannot be retrieved; no model code; coordinator runs the full gate. Final-candidate critique.
* Research and evidence considered: .copilot-tracking/research/2026-10-21/climate-paired-source-178-research.md (W1-W5, Q1-Q4)
* Decisions, dependencies, and acceptance criteria considered: plan User Decisions, FR1-FR3, AC1-AC3, P01/P02 tasks and phase details.
* Assessment boundary: supplied documents only. Probe results (W1-W5) were not re-run; the existence of the referenced repository files and consumers of docs/reference/research/ was not exhaustively audited.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Owner decision: no credentials/account/private data | Covered | Plan non-goals, research Contrarian section reject bypass |
| Owner decision: UKCP18 / EA OGL where available | Partial | EA probed (W4); UKCP18 is never assessed, only HadUK-Grid (PC-002) |
| Owner decision: synthetic fallback labelled | Partial | Only a "synthetic_substitution false" flag; no disposition for the fallback branch (PC-002) |
| FR1 licence statement observed | Partial | MIDAS licence file was not readable (W3); research claims "re-verified" (PC-001) |
| FR2 statuses | Covered | Statuses defined; test assertions are thin (PC-003) |
| FR3 owner action | Covered | Research Findings give a concrete action |
| AC1 JSON and test | Partial | "No numeric bounds" check is undefined (PC-003) |
| AC2 synthesis, index, log | Partial | Brittle row reference; no link or consumer check (PC-005) |
| AC3 artifacts committed | Partial | Critique disposition and checklist state inconsistent (PC-004) |
| P01-T01/T02, P02-T01/T02 | Covered | Bounded, no model code |

## Verdict

* Verdict: Revise
* Rationale: The blocker approach is credible and respects owner boundaries, but the plan overstates licence verification, leaves the owner's UKCP18 and synthetic-fallback branches unresolved, has a vague regression criterion, and carries inconsistent status markers. All are direct planner corrections; none requires a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Licence evidence for MIDAS is inherited, not observed

* Related IDs: FR1, W3, Prior Knowledge Gate, Q1
* Evidence: research W3 (README_catalogue_and_licence.txt returned Unauthenticated); Prior Knowledge Gate says OGL "re-verified today".
* Concern: FR1 requires "licence statement observed", but the only MIDAS licence text came from PR371 and today's licence file fetch failed. Only EA's OGL (W4, response meta.license) was observed today. Presenting MIDAS licence as re-verified is unsupported, and per the repository legal conventions each claim needs source, source date and retrieval date.
* Impact: A blocker artifact could imply licence confirmation for a source whose reuse is UNMET.
* Smallest useful change: In the artifact, record licence per source with fields observed_today (EA: true; MIDAS: false), carried-forward source reference (PR371 evidence file and date) and retrieval date; correct the research wording from "re-verified" to "carried forward, not re-observed".
* Action owner: planning parent
* Exact resolving evidence: artifact JSON distinguishes observed vs carried-forward licence per source; research Prior Knowledge Gate wording corrected; test asserts MIDAS licence is not marked observed.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Owner's UKCP18 and labelled-synthetic branches have no disposition

* Related IDs: User Decisions, Goals, Q4, Follow-Up Items
* Evidence: plan User Decisions (owner 2026-10-15); research Findings (synthetic mention only for #179).
* Concern: The owner's decision has three tiers: UKCP18, EA OGL, else labelled synthetic. Research probed EA and HadUK-Grid but not UKCP18 (projection/baseline products), and Q4 "none found" is not tied to UKCP18. The plan neither produces a labelled synthetic input nor states that it is deliberately deferred to #179 or why that satisfies the decision.
* Impact: A reviewer can argue the plan ignored owner direction or that the blocker is premature; #179 inputs remain ungoverned.
* Smallest useful change: Add to the artifact and synthesis an explicit per-tier disposition: UKCP18 (assessed or "not assessed, reason, no-login status unverified"), EA OGL (no humidity), synthetic (permitted by owner, deferred to #179, must be labelled synthetic and never fulfil record-derived bounds). If the UKCP18 anonymous check is cheap, record one probe; otherwise state it as an unchecked item.
* Action owner: planning parent
* Exact resolving evidence: artifact has a source_tiers (or equivalent) list covering all three owner tiers; plan Scope and Follow-Up cite the deferral; no claim that UKCP18 was ruled out unless probed.
* Decision route: direct planner correction (owner direction already resolves the fallback; no new user decision)

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Regression test criterion is vague and may be satisfiable by a bad artifact

* Related IDs: AC1, FR2, P01-T02
* Evidence: plan AC1 "no numeric bounds present"; phase details P01 test ownership.
* Concern: "Absence of numeric bounds" is undefined: coverage-year integers and station counts are numeric, so a naive check fails, while a lenient one misses fields such as min/max/p05. The plan's stated purpose (artifact cannot be read as bounds) is not directly tested.
* Impact: The guard against fabricated or misread bounds can be hollow or brittle.
* Smallest useful change: Specify assertions: required keys and exact status values (bounds=unavailable, humidity=unavailable, owner_reuse_approval=UNMET, synthetic_substitution=false); recursive deny-list of key names (min, max, lower, upper, percentile, threshold, bound values) outside the status fields; every probe has url, result, class, retrieved_on; no credentials-like or hash keys; ASCII only.
* Action owner: planning parent
* Exact resolving evidence: phase details P01-T02 lists these assertions; test passes via python3 -m unittest in tools; a mutation (adding a "max_temp_c" key) fails the test.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Inconsistent status and critique disposition state

* Related IDs: Phase Checklist P01, Critique Disposition, AC3
* Evidence: plan shows P01 header "[x]" while P01-T01/T02 are "[ ]" and nothing is implemented; Critique Disposition says "Pending".
* Concern: Completion markers claim P01 done before work exists, and the disposition does not record this critique's outcome (Revise) or how findings were resolved. Repository rules require preserving original critique outcomes.
* Impact: Misleads the coordinator and gate reviewers about progress and review state.
* Smallest useful change: Reset P01 to "[ ]"; after revision, record disposition PC-001..PC-006 (accepted/rejected with reason) in the plan without altering this critique file.
* Action owner: planning parent
* Exact resolving evidence: plan checklist markers match task state; Critique Disposition lists every PC id with outcome; this critique file unchanged.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Edit targets and validation for synthesis, index and log are brittle and under-specified

* Related IDs: AC2, P02-T01, P02-T02
* Evidence: phase details "update README row 307", "insert after the 2026-10-17 climate section"; validation lists link review only generically.
* Concern: A line number reference will drift; there is no requirement to add the new JSON to the index with its placement rules, to link it relatively from the synthesis, or to state in the synthesis that issue 178 criteria stay unticked and PR371 temperature statistics remain temperature-only and unpromoted. AC2 "issue criteria remain unticked" has no verifiable form.
* Impact: Knowledge base drift, broken links and an ambiguous status in the synthesis.
* Smallest useful change: Reference the index entry by its climate evidence row text, require a relative link from synthesis to the JSON, require a log entry stating the blocker and owner action without rewriting earlier entries, and define AC2 evidence as git diff showing no issue-criteria edits (the plan itself makes no remote writes).
* Action owner: planning parent
* Exact resolving evidence: phase details name the row by text; link check of new relative links passes; git diff shows append-only log change.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Blocker claim rests on single-day curl probes without recorded method or retest condition

* Related IDs: W1-W4, FR1, Q1, Q4
* Evidence: research Deeper section (probes 2026-10-21T01:23-01:25Z).
* Concern: The artifact must stand alone because research lives in tracking. The plan specifies date only, not time window, request method, redirect target class or the exact hosts tested, and gives no retest trigger. Data host 302 behaviour could be transient or route-specific, and "none found" for other in-boundary sources lacks a stated search list.
* Impact: Weak reproducibility if the owner or a reviewer questions the blocker; stale evidence after CEDA changes.
* Smallest useful change: Add to each probe record: UTC timestamp, method, host, HTTP status or body class, redirect target host/path class (no tokens); add a sources_considered list for Q4 and a retest_when note (owner supplies files, CEDA access policy changes, or next scheduled climate source review).
* Action owner: planning parent
* Exact resolving evidence: FR1 and phase details T01 fields include these; the JSON probes validate against the test.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Owner-action options need explicit ownership and approval wording

* Related IDs: FR3, Follow-Up Items
* Evidence: Follow-Up Items; research Findings.
* Concern: The action offers either an authorised human's own CEDA account download or approval of an alternative no-login source, but does not state that the human must not share credentials, that file licence/reuse must be recorded by the owner before derivation, or that station choice needs owner confirmation.
* Impact: Risk of credential sharing or silent source substitution at re-entry.
* Smallest useful change: Phrase owner_action to require: own account only, files supplied with CEDA licence text, owner reuse approval recorded, station choice confirmed, hash-pinned import in a new task.
* Action owner: planning parent
* Exact resolving evidence: owner_action field text in the artifact contains each condition.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strengths: lawful boundary respected (no bypass, no substitution), honest blocker framing, evidence-only scope with no model code, test and index/log convention coverage, PR371 temperature statistics preserved.
* Residual risk (accepted by owner direction): issue #178 remains unclosed and #179 stays gated on owner action.

## Questions or Blocking Evidence Gaps

* None decision-critical. The UKCP18 status (PC-002) is a research gap the planner can close directly or record as unchecked.

## Limitations

* Probe results and repository files were not independently re-run or inspected; the full local gate is run by the coordinator and is not assessed here.

## Recommended Next Action

* Highest-impact finding: PC-001 (with PC-002)
* Action owner: planning parent
* Smallest next action: direct revision of plan and phase details for PC-001..PC-007 without further critique, then finalize.
* User response required: no

## Relevant Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-21/climate-paired-source-178-plan.md](.copilot-tracking/plans/2026-10-21/climate-paired-source-178-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-21/climate-paired-source-178-phase-details.md](.copilot-tracking/details/2026-10-21/climate-paired-source-178-phase-details.md) | Phase details |
| [.copilot-tracking/research/2026-10-21/climate-paired-source-178-research.md](.copilot-tracking/research/2026-10-21/climate-paired-source-178-research.md) | Research evidence |

## Next Steps

* Planning parent revises the plan and details directly for PC-001..PC-007 and records dispositions; no user action required.
