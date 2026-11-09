<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-1294-validation-policy-correction-c3

## Metadata

* Task ID: issue-1294-validation-policy-correction-c3
* Critique date: 2026-11-08
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: independent review findings 1-3 of bd63b22 and the owner's C3 brief (confirmed defects only, focused tier, README acceptance command with runner PYTHONPATH and three-test zero-skip contract, append-only log correction, fresh full behavior run(s) with retain-sandbox, proxy label, honest verdict, bounded attempts, no workflow/source/tool/install/Docker/SQL/deletion).
* Research and evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c3-research.md; the independent review file; spot checks of src/README.md:189 and 426-438, src/api/README.md:147-153, tools/rpi-checks.py, src/api/checks/employee_acceptance_check.py:495-510, .github/workflows/src-ci.yml:102-107, docs/reference/log.md C1/C2 entries.
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR3, AC1-AC5, P01-P03.
* Assessment boundary: plan credibility only. Behavior-run outcomes and the final wording are not assessable here.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Review finding 3 / FR1 / P01-T01 | Covered | Path string matches CI (src-ci.yml:106-107), runner constant and src/api/README.md:151; three tests and zero skips confirmed at employee_acceptance_check.py:498-510. See PC-003 for the probe. |
| Review finding 2 / FR2 / P01-T02 | Partial | Append-only and tested-state facts are right; timing of the outcome statement is unresolved (PC-002). |
| Review finding 1 / FR3 / P02-T02 | Partial | Fresh independent run covered; terminal rule leaves a repeat of the original defect (PC-001). |
| Scope, tier, prohibitions, preservation | Covered | Focused tier, no workflow/source/tool changes, no deletion, proxy label. |

## Verdict

* Verdict: Revise
* Rationale: the corrections are accurate and proportionate, but the behavior-loop terminal rule and the log timing can reproduce review findings 1 and 2. Both are small direct planner fixes.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Terminal rule can again end with edits made after the last grade

* Related IDs: FR3, AC3, P02-T02, review finding 1
* Evidence: phase details P02-T02 ("apply them in one batch, then one more fresh full run ... at most two attempts after this correction; if still Revise ... report the exact blocker"); review finding 1.
* Concern: the plan does not say what happens to defects found by the last permitted attempt. Applying edits after it recreates the untested-post-grade state that caused C3. "Confirmed contract defect" has no criterion or decider, so the attempt count and edit rule are not mechanical. The two-attempt cap is also ambiguous between "two total" and "two after the batch fix".
* Impact: the loop may end with an unverifiable candidate, or produce a Pass claim on wording that differs from what was graded.
* Smallest useful change: state that the wording is frozen (record the commit or diff hash) before each attempt. State that the final attempt's defects are not edited in; they are reported as open Revise with the blocker. Any edit made after a graded attempt voids that attempt for the edited wording. Fix the cap as at most attempt 4 (the current wording) plus attempt 5 (after one batch fix). Define "confirmed defect" as a grader finding tied to a specific issue #1294 acceptance criterion or review finding, with the parent as decider and cosmetic items logged nonblocking.
* Action owner: planning parent
* Exact resolving evidence: plan and details contain the freeze/hash rule, the no-edit-after-final-attempt rule, the explicit attempt cap and the defect criterion.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Log correction is written before the C3 result exists

* Related IDs: FR2, AC2, P01-T02
* Evidence: details P01-T02 ends the entry with "C3 repeats the test", written in P01, before any run; the repo log is append-only.
* Concern: the entry cannot truthfully state the C3 outcome in P01. Editing it afterwards violates append-only, and leaving it silent makes the log again incomplete about which revision was tested. The research also lists the C3 log entry among files the grader sees.
* Impact: risks a repeat of review finding 2 for C3 itself.
* Smallest useful change: in P01 append only the correction of the C2 statement (tested state, four untested edits, result Revise) and say a fresh run is in progress without naming an outcome. Record the C3 result and tested state in the changes record and report 4/5. If the log must carry the C3 result, add it as a separate later append in P03 after the final grade, with no wording changes to guidance files afterwards. Keep the log out of the graded behavior wording, or freeze it with the guide.
* Action owner: planning parent
* Exact resolving evidence: details specify the P01 entry text boundary and the P03 conditional append; git diff shows additions only.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Discovery probe proves only module import, not the three-test contract

* Related IDs: FR1, AC1, P02-T01
* Evidence: research C5 and details P02-T01 use find_spec; employee_acceptance_check.py:498-510 loads three named methods.
* Concern: find_spec shows the module resolves, not that the three named tests load. The bullet also needs to say it runs from src/api and requires installed Chromium, as src/api/README.md:147-153 already does, so a reader does not read it as an import-only check.
* Impact: the "executable as written" claim (AC1) is weaker than stated; a missing test name would go unnoticed.
* Smallest useful change: add a read-only probe with PYTHONDONTWRITEBYTECODE=1 under the runner path that loads the three names with unittest.defaultTestLoader and asserts countTestCases() == 3 without running a browser; keep unset and short-path probes as negative controls. Add "from src/api, Chromium installed" to the bullet.
* Action owner: planning parent
* Exact resolving evidence: sandbox 4 checks/ records the loader probe output and exit codes, and the README bullet carries cwd and Chromium wording.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Runner path choice is verified against CI, the runner constant and the sibling API README; rejecting the shorter path is sound.
* Prior evidence preservation, proxy label, no-Pass-fabrication and no-deletion constraints are explicit.
* Residual: proxy model binding limits fidelity and must stay in the final verdict; hosted CI remains unobserved.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only spot checks only; no commands that change state and no behavior run were evaluated.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: add freeze/no-edit-after-final-attempt/cap/defect-criterion text to P02-T02, then fix PC-002 and PC-003 and finalize without another critique.
* User response required: no
