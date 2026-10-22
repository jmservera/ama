<!-- markdownlint-disable-file -->
# RPI Plan Critique: Non-operative custody preparation correction (#122)

## Metadata

* Task ID: continuity-custody-preparation-122-recovery
* Critique date: 2026-10-21
* Plan: .copilot-tracking/plans/2026-10-21/continuity-custody-preparation-122-recovery-plan.md
* Phase details: .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: docs-only correction of the non-operative custody subsection in src/core/README.md (base ca4baf75837de57c99718f7423716d5dc0b0e244, current text from c9f65c48, preserved as adverse history). Confirmed decisions in the plan's User Decisions and Requirements: preparation only, no authority/witness/drill/Azure, no other active issue files, no runtime code or tests, no push or heavy gate, all #122 criteria open, adverse history preserved, real skill phases, model evidence corrected to claude-sonnet-5.5.
* Research and evidence considered: .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md (F1-F5, C1-C10, W1, W2 as recorded), the current README subsection (src/core/README.md lines 2864-2905), git log and `git diff --stat` against the base.
* Decisions, dependencies, and acceptance criteria considered: plan Acceptance Criteria, Functional and Non-Functional Requirements, P01/P02 tasks and detail sections, Dependencies, Critique Disposition.
* Assessment boundary: plan and details credibility against the supplied evidence. I did not re-verify continuity.py, PRD OQ-017, BRD OD-35, ADR 0002 or live GitHub issues; research citations are taken as recorded. The /tmp briefs named in plan Sources were not read.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| Preparation only, no authority/drill/Azure | Covered | Non-goals, P01 boundaries |
| No other active issue files | Covered | Acceptance diff-scope criterion; base diff touches only README and tracking files |
| All #122 criteria open | Partial | Criterion stated, but no check exists (PC-004) |
| Preserve adverse history, correct model evidence | Partial | P02-T02 covers it; the correction would live only in the changes record, not in the plan itself (PC-005) |
| Commit artifacts, freeze clean, return head/base and invocations | Missing | No task or evidence (PC-001) |
| F5 role rows (OQ-017, OD-35) | Partial | P01-T01 lacks per-row target wording and the suspend/competent-review/communication rows are not itemised (PC-002) |
| F2 verify_export wording | Covered | P01-T02, with a residual normative-rule gap (PC-003) |
| Witness and sequence labelled proposed | Covered | P01-T02 |
| P02-T01 local checks | Partial | Check commands unspecified (PC-004) |
| Sources durability | Partial | /tmp briefs cited (PC-006) |

## Verdict

* Verdict: Revise
* Rationale: The direction is sound and in scope, and the two research-backed corrections are credible. The plan omits an explicit commit and clean-freeze deliverable required by the confirmed user decisions, leaves the main table rewrite underspecified so the over-attribution it exists to remove could return, and has weak, unspecified validation. All fixes are direct planner corrections; no new user decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: No task for commit, clean freeze and reporting head/base and invocations

* Related IDs: User Decisions (last bullet), P02, Handoff
* Evidence: plan User Decisions and Requirements, "commit truthful correction artifacts, freeze clean, return head/base and actual invocations"; P02 has only P02-T01 and P02-T02; repository instructions require a repo-local noreply author email and the Co-authored-by trailer.
* Concern: The confirmed requirement has no owning task, command or completion evidence. Commit identity setup, trailer, the exclusion of the earlier files from edits, and the clean-tree check are unplanned.
* Impact: Implementation could finish with an uncommitted or dirty tree, or a commit with the wrong identity, so the coordinator cannot freeze or assess an exact head.
* Smallest useful change: Add P02-T03 "Commit and freeze": resolve `gh api user` for the noreply email, set it with `git config --local`, commit README, changes record, plan, details, research and critique with the Co-authored-by trailer, confirm `git status --short` is empty, and record head SHA, base SHA and the actual skill invocations in the changes record. State explicitly that the gate and push are left to the coordinator.
* Action owner: planning parent
* Exact resolving evidence: plan and details contain P02-T03 with these steps and completion evidence (empty `git status --short`, `git rev-parse HEAD`, base SHA, invocation list).
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Decision-rights rewrite is not specified per row and could re-imply authority

* Related IDs: P01-T01, F5, C7, C8, C9, FR1
* Evidence: plan P01-T01 expected result; current README rows at src/core/README.md lines 2883-2888; research C7 ("question owners, not holders") and C8 (OD-35 "Building Safety and Sponsor" own override authority and restart evidence).
* Concern: P01-T01 lists the outcome in prose but not each row's target text. Two risks: (a) OD-35 naming Building Safety and Sponsor as owners of override and restart evidence could be written into the restart row as the restart authority holder, which C8 does not establish; (b) the "Suspend AI" row's "Incident owner named on the suspension record", the "Accept corrective evidence" row, the "Resident, safety, professional and Finance decisions" row and the Communication owner are not addressed or confirmed against a source.
* Impact: The task exists to remove unsupported role implications, and an ambiguous rewrite can leave or add new ones.
* Smallest useful change: In P01-T01 give a row-by-row disposition: for each of the six rows state source cite (OQ-017, OD-35, or none), whether the Role cell is kept, changed to "UNASSIGNED", or reworded to "owner of the question" or "owner of evidence", and state that OD-35 owners supply evidence and do not hold or delegate authority. For "Incident owner named on the suspension record", name the code or README line supporting it or mark it UNASSIGNED. Confirm the "Unchanged" row against the repository's existing human-owner statements or reword it.
* Action owner: planning parent
* Exact resolving evidence: P01-T01 detail contains the six-row table with source cite and target wording, and each source-cited row's cite appears in research C7 or C8 (or a cited README or code line).
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Other normative sentences in the subsection are left unexamined

* Related IDs: P01-T02, FR2, FR3, F5
* Evidence: src/core/README.md lines 2873-2878 ("An export is relied on only when ... agree", "An incomplete ... bundle is not evidence"), 2894-2897 (sequence), 2898-2901 (Communication, Stop conditions); P01-T02 boundaries list only the custody, witness and sequence bullets.
* Concern: Research challenged the table, custody, drill and witness claims, but the plan does not say whether the "relied on only when" rule, the Communication bullet, the Stop conditions and the intro paragraph were checked or intentionally left. Rules phrased as requirements read as existing controls, and the pre-gate sentence is supported only by inferred silence (C10).
* Impact: Unreviewed residual wording can still overstate controls, which defeats a truthful-preparation correction.
* Smallest useful change: Extend P01-T02 boundaries to the whole subsection and record the disposition per bullet (unchanged with reason, or reworded as proposed), including a lead-in sentence that the bullets are proposed expectations and carrying the C10 "inferred" qualifier for the pre-gate sentence. Keep the approximately 15-line cap by trimming where needed.
* Action owner: planning parent
* Exact resolving evidence: P01-T02 detail lists a disposition for every bullet and the intro paragraph; the validation step reads each against research findings.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Validation is unspecified and cannot show "criteria remain unticked"

* Related IDs: P02-T01, Acceptance Criteria 1-2, NFR1
* Evidence: P02-T01 says "Prior run used a small anchor script" and "recorded commands" with no commands; plan acceptance "Every #122 and #221 criterion remains unticked" has no object (GitHub issue body or README) or method.
* Concern: No exact commands, anchor slugs, ASCII method, or diff baseline. The "about 15 README lines net" limit is ambiguous because the base diff already carries +47 README lines from c9f65c48; "net" must be measured against HEAD before edits. The unticked claim is untestable without stating that no remote write occurs and where criteria live.
* Impact: Validation results would be self-asserted rather than reproducible, and the diff cap could be judged inconsistently.
* Smallest useful change: Specify: grep of README heading slugs for the #122, #221 and #114 anchors; `git diff -U0 HEAD -- src/core/README.md | grep -nP '^\+.*[^\x00-\x7F]'` returns nothing; `git diff --name-only ca4baf75837de57c99718f7423716d5dc0b0e244` lists only README and `.copilot-tracking/`; the line cap measured against pre-edit HEAD; the unticked criterion restated as "the diff contains no checkbox changes and no gh write was issued".
* Action owner: planning parent
* Exact resolving evidence: P02-T01 detail contains these commands with expected outputs, and the changes record reports their results.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Adverse-history and model correction have no checkable content and the critique disposition is unresolved

* Related IDs: P02-T02, Acceptance Criterion 3, Critique Disposition
* Evidence: P02-T02 Validation Expectations; research "Historical correction" section; plan Critique Disposition "pending".
* Concern: The correction lives only in a changes record that does not yet exist and the plan carries no pointer to the facts it must contain (events.jsonl line 189, timestamp, claude-sonnet-5.5, c9f65c48 SHA, the list of earlier files). The disposition table still shows "pending" although this critique now supplies findings. Plan Sources also should not rely on `events.jsonl` content that is not preserved in the repository.
* Impact: A later reviewer cannot confirm the record is complete, and the plan's own disposition table would be stale at implementation.
* Smallest useful change: Specify required record content in P02-T02 (c9f65c48 SHA, direct-authored, the earlier file names, "not a Review", observed model claude-sonnet-5.5 with its source, correction of the earlier "default model" statement, first skill invocation) and update Critique Disposition with one row per PC finding after revision.
* Action owner: planning parent
* Exact resolving evidence: P02-T02 detail lists these items; the Critique Disposition table has a row for each of PC-001 to PC-006 with Accepted or Rejected and a response.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Plan Sources depend on non-durable /tmp briefs

* Related IDs: Sources, User Decisions
* Evidence: plan Sources cite /tmp/brief-122-custody-preparation.md and /tmp/brief-122-rpi-recovery.md.
* Concern: Those files are transient and outside the repository, so the caller requirements are not verifiable later; the same requirements are already summarised in User Decisions.
* Impact: Reduced traceability for the independent assessment.
* Smallest useful change: Replace the /tmp pointers with "caller briefs as supplied, summarised in User Decisions and Requirements" and, if retained, note they are not repository evidence.
* Action owner: planning parent
* Exact resolving evidence: plan Sources contains no /tmp path or labels it as non-durable caller context.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Scope is tightly bounded and consistent with confirmed user decisions: docs-only, no remote writes, no authority appointment, all criteria open.
* Research is evidence-keyed (C7, C8, C9 for roles; C2 for verify_export) and honestly states C10 as inferred.
* Residual risk to accept: research claims were not independently re-verified here against continuity.py, OQ-017, OD-35 and live issues; the implementer's source comparison in P01 covers that.
* Residual risk to accept: the complete local gate and independent exact-head assessment are deferred to the coordinator by user direction.

## Questions or Blocking Evidence Gaps

* None. Current user direction resolves all open points.

## Limitations

* Cited sources outside the plan, details and research were not read, and critique did not run any validation.
* Line numbers refer to the README as it stood at HEAD c9f65c48 and will move after edits.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: revise the plan and details to add P02-T03, then apply PC-002 to PC-006 directly and update the Critique Disposition table, without a second critique.
* User response required: no

## Relevant Artifacts

| Path | Description |
|---|---|
| .copilot-tracking/plans/2026-10-21/continuity-custody-preparation-122-recovery-plan.md | Plan under critique |
| .copilot-tracking/details/2026-10-21/continuity-custody-preparation-122-recovery-phase-details.md | Phase details under critique |
| .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md | Supporting research |

## Next Steps

* No user action is required. The planning parent revises the plan and details for PC-001 to PC-006 and then finalises; it does not call for another critique.
