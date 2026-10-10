<!-- markdownlint-disable-file -->
# RPI Plan Critique: Azure exercise build contract and decision-model learning

## Metadata

* Task ID: AMA-AZURE-EXERCISE-20261011
* Critique date: 2026-10-11
* Plan: .copilot-tracking/plans/2026-10-11/azure-exercise-build-contract-plan.md
* Phase details: .copilot-tracking/details/2026-10-11/azure-exercise-build-contract-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: standalone planning for mandatory real AI, real SQL and real Azure deployment in the next and all subsequent builds; PR #58 learning extraction into BRD/PRD; parallel decision-model experiment kept separate. Locked scope: ten canonical documents, no new docs/tests/code/tooling, no removals, at most two new requirement rows per BRD/PRD, one implementer, new versions not inheriting old acceptance.
* Research and evidence considered: the plan and phase-details files (including the verified learning register); targeted ID and wording checks of docs/brds/agentic-retrofit-programme-brd.md and docs/prds/proper-warm-retrofit-programme-demonstrator.md.
* Decisions, dependencies, and acceptance criteria considered: plan Acceptance Criteria, Locked Change and Validation Contract, Canonical Amendment Map, Required Real-Platform Acceptance Shape, P01 to P03 dependencies.
* Assessment boundary: no PR #58 re-read, no cloud or model calls, no re-research. Pinned #58 claims are taken from the details register as supplied.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Mandatory real AI/SQL/Azure for all subsequent builds | Partial | Stated in the BRD/PRD amendment map and acceptance shape, but PRD FR-044 and SA-004 "AI optional" wording is not targeted (PC-001). Build-class term and minimum AI proof inconsistent (PC-002). |
| Narrow Decision placement conditional | Covered | Plan Acceptance Criteria and DD-007 map row; the minimum whole-app AI proof is unspecified (PC-002). |
| #58 learning extraction | Covered | P01-T01 register is source-pinned and separates observed, blocked and unknown. |
| Parallel experiment boundary | Covered | Intake, three-class mismatch and proposed-not-executed protocol are explicit. |
| Row cap and IDs | Covered | BRD CON-007/AC-086 and PRD CON-009/AC-057 were not found in the current files; PRD CON-008 and AC-056 and BRD CON-006 and AC-085 exist. |
| Budget interaction | Partial | Override is scoped, but mandatory inference versus the 405 pause is unresolved (PC-003). |
| P02/P03 validation | Partial | Generic checks only; no residual-term sweep or count baselines (PC-004). |
| Planning status text | Partial | Plan still says critique pending (PC-005). |

## Verdict

* Verdict: Revise
* Rationale: Scope, IDs and evidence classification are sound, but four direct planner corrections are needed so mandatory real AI/SQL/Azure is unambiguous in every prospective build and the implementer can validate it mechanically. None requires a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Active "AI optional" requirements are not targeted by the amendment map

* Related IDs: P02-T01, PRD FR-044, SA-004, DD-007, BRD AI-assistance statements.
* Evidence: docs/prds/proper-warm-retrofit-programme-demonstrator.md line 443 (SA-004 "AI assistance is optional") and line 624 (FR-044 "keep AI assistance optional"). The map lists DD-001/007/008, NFRs and Exercise Acceptance, but not FR-044, SA-004 or the "optional System One" wording in the Components table.
* Concern: An implementer could add the mandatory rows while contradictory active statements remain. The plan requires semantic coverage but names no rows to check.
* Impact: A reader could conclude real AI is optional for an accepted build. FR-044 and SA-004 should mean that case access and manual completion never depend on model availability, not that a build may ship without AI.
* Smallest useful change: Add FR-044, SA-004 and the related BRD AI-assistance and RULE-018 context to the amendment map as clarify-in-place wording ("AI is required in the deployed build; case access and manual completion never depend on model availability"). State that no FR is added or renumbered, so the count stays 46.
* Action owner: planning parent
* Exact resolving evidence: The amendment map in the phase details lists these rows with the clarification wording, and the P03 checks include their disposition.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Build class and minimum "AI used" proof are not defined consistently

* Related IDs: P02-T01 map, Acceptance Criteria, Required Real-Platform Acceptance Shape item 3.
* Evidence: The BRD map row says "all subsequent AMA prototypes/PoCs/MVPs"; the PRD and plan say "exercise builds"; acceptance item 3 requires "actual enabled AI" without naming which task qualifies.
* Concern: Scope terms differ across documents. There is no carve-out for documentation-only work, unit/CI tests or development iterations, and no minimum AI task for acceptance.
* Impact: The requirement could be read as too broad (every test) or too narrow, and a Decision rejection could be read as removing AI.
* Smallest useful change: Use one defined term, "accepted application exercise build", in BRD, PRD and addendum. Exclude docs-only work, unit/CI tests and dev iterations (SQLite or mocks allowed as non-acceptance evidence). Require at least one in-scope task to run a real model (generative or Decision, chosen by task) in the exercised path. A negative Decision result keeps rules/manual handling for that task only.
* Action owner: planning parent
* Exact resolving evidence: The definition and minimum-AI sentence appear in the details map and acceptance shape, with the same term in all three target rows.
* Decision route: direct planner correction (follows the user's stated direction)

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Mandatory inference versus the budget pause rule is unresolved

* Related IDs: P02-T01, plan Non-Functional Requirements, EXA-012.
* Evidence: docs/prds/proper-warm-retrofit-programme-demonstrator.md line 897 pauses optional work at USD 405 and blocks billable batches when price is unknown.
* Concern: Once inference is mandatory it is not optional work, yet the plan does not say what happens to acceptance when budget or authorization is unavailable.
* Impact: A build could be accepted on a mock to stay in budget, or the pause could be overridden silently.
* Smallest useful change: Add one sentence: when effective budget or authorization is unavailable, real-platform acceptance is Blocked or Not run, and mock, local or template substitution is not accepted. The USD 450 cap is unchanged and the #58 override is not propagated.
* Action owner: planning parent
* Exact resolving evidence: The statement appears in P02-T01 validation expectations and acceptance shape item 5.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Validation lacks a residual-term sweep and count baselines

* Related IDs: P03-T01, Locked Change and Validation Contract.
* Evidence: Validation lists generic link/requirement/traceability checks without terms or baselines.
* Concern: No named phrase list (local durable, SQLite, optional AI/scoring, fixture MVP) and no before/after counts.
* Impact: Contradictions in the addendum, ADRs and next-build synthesis could survive, and counts or links could drift.
* Smallest useful change: In P03-T01 list the sweep terms across the ten files and add assertions: PRD FR 46 unchanged, PRD AC 56 to 57, PRD CON 8 to 9, BRD CON 6 to 7, BRD AC 85 to 86, with matching traceability/coverage rows and ms.date/version metadata.
* Action owner: planning parent
* Exact resolving evidence: P03 validation expectations contain the term list and count assertions; the changes record later reports results.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Plan status and critique disposition need finalization

* Related IDs: Plan Metadata, Critique Disposition, Implementation Context Record.
* Evidence: Plan says "one final critique pending" and the disposition table says "None yet".
* Concern: Stale status would make the plan look unreviewed.
* Impact: Minor traceability risk; no scope change.
* Smallest useful change: After applying PC-001 to PC-004, record dispositions PC-001 to PC-005 and mark the plan revised after the single final critique, without a second critique.
* Action owner: planning parent
* Exact resolving evidence: The plan Critique Disposition table lists PC-001 to PC-005 with responses.
* Decision route: direct planner correction

## Strengths and Residual Risk

* The source-pinned register, the observed/proposed/blocked separation and the binary versus three-class caveat are credible.
* Scope locks hold: ten files, no removals, two-row cap, single implementer, no inherited v0.12.0 acceptance.
* Residual risk: pinned #58 claims were not re-verified here and are carried as the planner's evidence.

## Questions or Blocking Evidence Gaps

* None. Current user direction resolves each finding; no user decision is required.

## Limitations

* No re-reading of PR #58, and no cloud, model or app evidence. Document checks were limited to ID availability and optional-AI wording. This file was written with PowerShell because no patch tool was available.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply PC-001 to PC-005 directly in plan and details and finalize without another critique.
* User response required: no

## Artifacts

| Path | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-11/azure-exercise-build-contract-plan.md](.copilot-tracking/plans/2026-10-11/azure-exercise-build-contract-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-11/azure-exercise-build-contract-phase-details.md](.copilot-tracking/details/2026-10-11/azure-exercise-build-contract-phase-details.md) | Phase details under critique |

## Next Steps

* Return to the planning parent to apply the planner-owned revisions; no user action is required.
