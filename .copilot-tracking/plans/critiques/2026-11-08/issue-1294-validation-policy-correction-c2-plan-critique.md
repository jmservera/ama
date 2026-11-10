<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-1294-validation-policy-correction-c2

## Metadata

* Task ID: issue-1294-validation-policy-correction-c2
* Critique date: 2026-11-08
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: final-candidate critique of a wording-only focused-tier correction (F1 fresh behavior cycle, F2 mixed-tier sentence, F3 direct-harness `--out` limit). No workflow, tool or source edits; host cannot bind subagent models (proxy run); prior reports and sandboxes preserved.
* Research and evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md; /home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1294-7260826-independent.md; src/README.md (lines 64-69, 84-93, 198-222, 234); src/api/checks/employee_chat_browser_check.py (141-150, 392-413); src/api/checks/design_system_browser_check.py (227-300); tools/rpi-checks.py (94, 239-253, 1717); .github/copilot-instructions.md:88; .github/agents/ama-backlog-delivery-coordinator.agent.md:478.
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR4, AC1-AC5, P01-P03.
* Assessment boundary: static read of the named files only; no browser, runner or behavior run was executed, so Chromium socket behavior and the behavior-run outcome are not assessed.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| F1 / FR4 / P02-T02 | Partial | Fresh cycle is correctly required (review finding 1). Gaps: PC-003, PC-005. |
| F2 / FR1-FR2 / P01-T01 | Partial | Defect confirmed at src/README.md:219. Gaps: PC-001, PC-002. |
| F3 / FR3 / P01-T02 | Covered with gaps | Claim verified: `--out` only used at employee_chat_browser_check.py:392-393; runner-only derivation at tools/rpi-checks.py:239-253,1717. Gaps: PC-004. |
| AC4 / P02-T01 | Partial | `/tmp/c2-evidence` conflicts with workspace-only rule (PC-006); no check for line 205. |
| AC5 / P03 | Covered | Preservation list and clean-commit criterion adequate; see PC-007. |

## Verdict

* Verdict: Revise
* Rationale: The three findings are real and the diagnosis is accurate, but the plan narrows owner policy on doubt without authority, leaves a second copy of the defect and several touchpoints unaddressed, and uses a prohibited scratch path. All fixes are direct planner corrections; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: "Genuine risk-based doubt" narrows the owner doubt rule

* Related IDs: FR1, P01-T01, research Synthesis
* Evidence: .github/copilot-instructions.md:88 ("A mixed change takes the strictest applicable tier, and doubt takes the full tier"); src/README.md:68; plan FR1 and Goals.
* Concern: The plan rewrites the README sentence to "genuine risk-based doubt", but the owner policy says plain "doubt takes the full tier". Adding a qualifier weakens a gate rule in a wording-only change and contradicts the research's own cited source (C3).
* Impact: A guide more permissive than the instructions lets a focused tier be claimed under unresolved doubt, reintroducing the opposite defect to F2.
* Smallest useful change: Keep "doubt takes the full tier" and "unresolved impact" verbatim; fix only the "any mixed change" clause. Remove "genuine risk-based" from FR1, P01-T01 and the Goals.
* Action owner: planning_parent
* Exact resolving evidence: README paragraph and plan text both state doubt takes the full tier with no qualifier; a grep for "genuine risk" across src/README.md returns nothing.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Other "strictest" phrasings and the Mixed row not aligned

* Related IDs: FR1, FR2, AC1, P01-T01
* Evidence: src/README.md:68 ("mixed changes take the strictest tier", not "applicable"); src/README.md:234 (Mixed row label "Strictest (full)"); .github/agents/ama-backlog-delivery-coordinator.agent.md:478.
* Concern: AC1 only greps for "any mixed change". Line 68 says "strictest tier" without "applicable", and the Mixed row hard-codes "(full)" in its tier cell while the table will also hold a focused-plus-focused row. The research says the row label is to be aligned, but no task or AC covers it. The plan also calls line 68 "correct" without noting the wording gap.
* Impact: A reader or the behavior grader can still derive "mixed = full" from the row or line 68, so AC1 can pass while the defect persists.
* Smallest useful change: Add to P01-T01: change line 68 to "strictest applicable tier"; rename the existing row to "Mixed: documentation plus infra/main.bicep" (full because a component is infrastructure) and add the focused-plus-focused row. Extend AC1 to grep "mixed" in src/README.md and inspect every hit.
* Action owner: planning_parent
* Exact resolving evidence: every "mixed" occurrence in src/README.md reads strictest applicable; the table has two labelled mixed rows with different tiers.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Fresh-run design must precede and exclude the fix-bias, and the single-batch rule leaves a Revise loop undefined

* Related IDs: F1, FR4, AC3, P02-T02
* Evidence: independent review finding 1 (Revise verdict, after-grade edits invalidated reuse); phase details P02-T02 last bullet; research Risks.
* Concern: The plan says a defect found is corrected "once in one batch" and then "the verdict stays as graded", but does not say what the candidate's final status is, whether the corrected files then ship un-simulated (the exact condition that caused F1), or who accepts that. Also "fresh designer (no lead scenarios...)" is followed by a list of scenarios the lead pre-supplies, which defeats independent design.
* Impact: The most likely outcome (a new Low or Medium wording finding) reproduces F1 and the plan has no honest terminal state, risking a silent claim of a Pass.
* Smallest useful change: Specify: (a) the scenario list is a minimum coverage checklist given to the designer as required topics, not as scenarios or expected answers; (b) if grading yields any finding requiring an edit, the behavior status is recorded as Revise (not Pass) with the edit as an unsimulated post-grade change, flagged for the independent exact-head reviewer and the owner, and no second run is silently counted; (c) no self-reuse.
* Action owner: planning_parent
* Exact resolving evidence: P02-T02 and AC3 contain an explicit terminal-state rule and the report-3 template records verdict, post-grade edits and unsimulated state.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: F3 statement overreaches and omits the real direct-run constraints

* Related IDs: FR3, P01-T02, AC2, research C7-C9
* Evidence: src/api/checks/design_system_browser_check.py:227-238, 257, 273-275; employee_chat_browser_check.py:141-143, 392-393; tools/rpi-checks.py:94, 250-252.
* Concern: (1) The research notes the runner derivation implies TMPDIR at most 62 bytes, but the plan text "short caller TMPDIR is an unmeasured precaution" must state the inheritance basis (Chromium inherits the caller TMPDIR, C8) so it is not read as the runner's rule. (2) `ZF_BROWSER_SCRATCH` recommendation must state the validation it enforces: absolute, not inside the checkout, else ValueError (design_system_browser_check.py:236), and that unset creates `.venv` in the checkout. (3) The scratch directory also holds ZF_STATE and server.log, so it is state, not only browser scratch; describing it only as "browser scratch" is imprecise. (4) The claim "no `--out` limit" should be scoped to length: `--out` is created with `mkdir(parents=True)` and must be writable.
* Impact: An over-simplified sentence replaces one unsupported claim with a partly unsupported one, and the grader may mark it.
* Smallest useful change: Reword P01-T02 to: direct `--out` only receives `axe-results.json` and has no evidenced length limit; the 58-byte limit is runner-specific (runner sets TMPDIR to `<out>/tmp`); the direct run's temporary and state directory is under `ZF_BROWSER_SCRATCH` (absolute, outside the checkout, else the harness raises ValueError) or `<checkout>/.venv` when unset; Chromium inherits the caller TMPDIR, so a short TMPDIR is an unmeasured precaution only.
* Action owner: planning_parent
* Exact resolving evidence: README sentence cites only facts present at the listed source lines; no remaining "58-byte limit described above" (grep returns nothing).
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Behavior-run scope omits F3 and the proxy-label contract

* Related IDs: F3, FR4, AC3, P02-T02
* Evidence: phase details P02-T02 scenario list; plan Executive Summary (proxy, no intended-profile claim).
* Concern: The scenario list covers direct `--out` behavior, but there is no scenario for the 58-byte runner limit versus the direct harness, and no required report-3 fields for the proxy label (what model actually ran, whether designer, executor and grader were distinct contexts, and that none is a native run). The executor `hve-core-all:hve-artifact-tester` and "fresh grader" are not stated to be separate from the lead.
* Impact: F3 can pass static grep yet be re-misread by a simulation, and the report may overstate independence.
* Smallest useful change: Add a runner-versus-direct `--out` scenario and require report 3 to record per-stage agent identity, actual model if observable (else "not observable"), context separation, and an explicit "proxy, no intended-profile or native claim".
* Action owner: planning_parent
* Exact resolving evidence: report 3 lists the scenario and the per-stage identity and proxy fields.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Evidence directory uses /tmp, contrary to workspace-only rule

* Related IDs: AC4, P02-T01
* Evidence: phase details P02-T01 ("saving to /tmp/c2-evidence"); caller and environment rule prohibiting writes to /tmp.
* Concern: Check outputs are to be written outside the workspace, where they are neither retained as evidence nor consistent with the environment rule.
* Impact: AC4 evidence is not reviewable or committed-adjacent, and breaks the stated constraint.
* Smallest useful change: Save outputs under .copilot-tracking/changes/2026-11-08/ or the run sandbox, and record each command with its exit code in the changes record.
* Action owner: planning_parent
* Exact resolving evidence: P02-T01 names a workspace path; the changes record lists each check with exit code.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Low]: Classification basis and scope not recorded for the C2 candidate; pycache check unspecified

* Related IDs: AC5, P03, Scope
* Evidence: plan Scope (src/README.md, docs/reference/log.md, new evidence); .github/copilot-instructions.md validation tiers; research (no classification statement).
* Concern: The plan asserts Focused but does not record the classification and its basis (documentation-only wording in a guide; no workflow, tool, manifest or Dockerfile change) as policy requires, nor define the "allowed set" for `git diff --name-only`, nor the pycache check (AC5) beyond "untouched". Also docs/reference/log.md append requires an index check, and prior critique and review files must be in the preserved list.
* Impact: The committed candidate cannot show the policy-required tier record, and AC5 is not mechanically verifiable.
* Smallest useful change: Add a classification line with basis to the changes record; list the allowed paths (src/README.md, docs/reference/log.md, .copilot-tracking C2 artifacts and sandbox 2026-11-08-issue-1294-policy-3); add `git status --short --ignored` comparison before and after for pycache and prior sandboxes and reports.
* Action owner: planning_parent
* Exact resolving evidence: changes record has the classification, allowed-path list and before/after status comparison.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Diagnoses of F2 and F3 are source-verified: src/README.md:219 is the single contradictory sentence; the 58-byte limit is runner-only (tools/rpi-checks.py:239-253,1717) and direct `--out` writes only axe-results.json.
* Correct refusal to reuse report 2 grades, to edit workflows or tools, and to claim an intended-profile run.
* Residual risk accepted by plan: a further Revise on wording from the fresh run, and hosted CI unobserved.

## Questions or Blocking Evidence Gaps

* None. No finding requires a user decision.

## Limitations

* Static review of supplied files; line numbers are from the current worktree (README line 205 duplicates the 58-byte sentence and is the second edit target). No runs executed.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Remove the "genuine risk-based" qualifier, then apply PC-002 to PC-007 directly in the plan and details; finalize without another critique.
* User response required: no

## Artifacts

| Path | Description |
|------|-------------|
| [.copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c2-plan.md](.copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c2-plan.md) | C2 plan |
| [.copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c2-phase-details.md](.copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c2-phase-details.md) | C2 phase details |
| [.copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md](.copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c2-research.md) | C2 research |

## Next Steps

* Planning parent revises the plan and details per PC-001 to PC-007 and finalizes; no user action is required.
