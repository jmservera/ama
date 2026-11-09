<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-1294-validation-policy-correction-c1

## Metadata

* Task ID: issue-1294-c1
* Critique date: 2026-11-08
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: owner policy (targeted development tests; small and documentation changes take the focused tier without a blanket --changed; full gate for major, SQL, infrastructure, deployment, security, release, mixed and unresolved risk); wording only; no workflow or source change; no deletions.
* Research and evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c1-research.md (C1-C23); /home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-1294-397ce-independent.md; tools/rpi-checks.py lines 120-140, 1555-1575, 2336-2345 (re-read); .github/workflows/src-ci.yml (selector at line 118); src/api/checks/employee_chat_browser_check.py (marker and JSON write, lines 381-403).
* Decisions, dependencies, and acceptance criteria considered: plan FR1-FR4, AC1-AC5, P01-P03 and dependencies.
* Assessment boundary: plan and details credibility only. The target guide text was not read (not supplied), so wording accuracy is judged against runner and workflow facts, not against the current README.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Review finding 1 / FR1 / AC1 / P01-T01 | Partial | Contract list matches runner lines 1555-1574, but non-bool integer, exact selector command and run location are not specified (PC-001, PC-002) |
| Review finding 2 / FR2 / AC2 | Partial | Structure is right, but "Shared" chat-panel selector overstates hosted coverage (PC-002) |
| Review finding 3 / FR3 / AC3 / P01-T02 | Partial | Impact rule present; "demonstrably non-security" has no decision rule or owner, and the focused-tier condition is untestable (PC-003) |
| Review finding 4 / FR4 / AC4 / P02-T02 | Partial | Independent design and retention planned; no fail-closed rules for proxy, sandbox path collision or grader inputs (PC-004) |
| AC5 / P02-T01 | Partial | Stale-phrase list and consistency check undefined (PC-005) |
| P03 / dependencies | Partial | Commit authority and review-once scope not tied to the preserved-evidence rules (PC-006) |

## Verdict

* Verdict: Revise
* Rationale: The four corrections target the right defects and the research is accurate against the code. Several accuracy and verifiability gaps remain that would let the corrected wording still be false (selector hosted coverage) or let the tier rule be applied inconsistently. All are direct planner corrections; none needs a user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Direct-check contract omits details the runner enforces

* Related IDs: FR1, AC1, P01-T01, C2, C3, C7
* Evidence: tools/rpi-checks.py:1555-1574 (passes must be a non-bool int > 0; "skipped" rejected in both stdout and the JSON text); src/api/checks/employee_chat_browser_check.py:381-393 (marker printed before axe-results.json is written).
* Concern: Details say "positive integer" but not that a boolean is rejected, nor that the JSON must be a list with exactly three entries (the runner's list equality enforces exactly three). The marker is printed before the JSON file is written, so stdout alone is insufficient; the direct check must require both and a zero exit. The details also do not state that the output directory must be new and external.
* Impact: A reader could accept `true` for passes, extra or missing states, or stdout without the JSON, recreating the original underchecking.
* Smallest useful change: Add to P01-T01 and AC1: exactly three entries in order, passes an integer that is not a boolean and above zero, command exit 0, marker in stdout AND the JSON present, fresh external `--out`.
* Action owner: planning parent
* Exact resolving evidence: README direct-check text containing each element; a line-by-line mapping table in the changes record to tools/rpi-checks.py:1555-1574.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: "Shared" label for the chat-panel selector would repeat the coverage error

* Related IDs: FR2, AC2, P01-T01, C8-C10, C16, Follow-Up Items
* Evidence: .github/workflows/src-ci.yml:118 runs `ZF_BROWSER_TESTS=1 python -m unittest -v test_chat_panel...` with no Ran-1, zero-skip, bare OK or named-test check; tools/rpi-checks.py:2336-2342 runs it and then `check_skips` with expected_test; the plan's own Follow-Up already lists "add zero-skip verification to the hosted selector".
* Concern: P01-T01 lists the chat-panel selector under Shared. The test executes in both places, but the exact-count/zero-skip verification is local only (the hosted step would pass on a skip or a different test count). Listing it wholly as Shared repeats the review's finding 2 in the opposite direction. The same applies to the other Shared items: for each, state the execution in both places and any verification that exists on one side only.
* Impact: A false "shared" claim lets a reviewer rely on hosted CI for the zero-skip guarantee.
* Smallest useful change: Split the selector: execution is Shared, exact-count/zero-skip/named-test verification is Local-only. Add an AC2 clause requiring each Shared item to cite both locations and flag one-sided verification; give the direct selector command in full (working directory src/api, the runner's PYTHONPATH from tests_env("api"), ZF_BROWSER_TESTS=1, `-v`).
* Action owner: planning parent
* Exact resolving evidence: README bullets showing the split; hosted line 118 and runner 2336-2342 cited; a check that the command in the README matches the runner's argv and cwd.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Impact-based classification lacks a decision rule, so "focused" is unverifiable

* Related IDs: FR3, AC3, P01-T02, C20-C23, owner policy
* Evidence: plan Goals and details P01-T02 ("a demonstrably non-security tooling or documentation edit stays focused"); research Alternative A/B.
* Concern: "Demonstrably" has no stated test, evidence or approver. Gate-tool (tools/rpi-checks.py) edits change the checks that gate everything, so a tool edit is rarely demonstrably harmless. The details name the full triggers but do not say who classifies, where the classification is recorded, or that doubt takes the full tier (current instruction text says so; the correction must keep it and the mixed-change strictest rule). There is also no explicit statement that `--changed` selecting the full matrix for workflow paths does not itself decide the tier (research states it; the details do not). Examples in the table could contradict the rule (a "Gate tool or workflow" row cannot have a single tier).
* Impact: Inconsistent tiering in either direction: weakened protection for security-relevant tooling or an unwarranted heavy gate for small edits, contrary to the owner policy.
* Smallest useful change: Add to P01-T02: (a) the classifier records the impact classification and its basis in the changes or review record; (b) a focused classification for these file classes requires a stated reason that none of permissions, pinned actions or images, packages, secrets, deployment or security controls, or gate semantics changed; (c) doubt or mixed takes the full tier; (d) `--changed` full selection is a selection aid only; (e) the table row is split into an impact-conditioned pair of rows (for example "Comment or doc-only tooling edit: Focused" and "Permissions, pinned action, image, package, gate-semantic edit: Full").
* Action owner: planning parent
* Exact resolving evidence: the revised instruction, README and coordinator wording each containing (a)-(e); AC3 grep showing no unconditional full-tier sentence for the four classes.
* Decision route: direct planner correction (consistent with the existing owner policy; no new decision needed)

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Behavior-test repeat has no fail-closed rules

* Related IDs: FR4, AC4, P02-T02, review finding 4 and safety note
* Evidence: review record "Safety and evidence note"; plan P02-T02 and AC4.
* Concern: Not stated: (a) the sandbox path must be new and must not reuse or recreate the removed 2026-11-08-issue-1294-policy-1 path (no reconstruction); (b) the grader must be given the examples table and the full contract, explicitly addressing the earlier gap; (c) a proxy executor or an unresolved profile caps the result at Deferred/proxy, never Pass, which AC4 only partly says; (d) the designing subagent must not receive lead-drafted scenarios; (e) Deferred needs the exact rerun condition. Also unstated: the scenarios must test the corrected claims (zero-pass, wrong-state, selector with a skip, categorical-tier phrasing).
* Impact: The repeat may again produce non-independent or non-retained evidence.
* Smallest useful change: Add these five rules and the scenario targets to P02-T02 and AC4.
* Action owner: planning parent
* Exact resolving evidence: new report listing designer, executor and grader identities, profile label, sandbox path with file listing, and either Pass-at-resolved-profile or Deferred with rerun condition.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Validation checks are under-specified

* Related IDs: AC5, P02-T01, NFR
* Evidence: details P02-T01 ("stale-phrase grep" with no phrases; "reproduction of changed_groups and ci-affected.select"); ignored tools/__pycache__ noted in the review.
* Concern: The stale phrases are not listed (at minimum the old "three states report no violations and no skip", "Hosted-only" on items with local counterparts, "any workflow, gate-tool, dependency-manifest or Dockerfile change", and the table "Full" cell). No cross-file consistency check across instructions, README, coordinator and table is required, and the plan does not state that the wording-only boundary is verified by a diff limited to the listed files (no tools/, workflow or src change). The reproduction must run with PYTHONDONTWRITEBYTECODE=1 so the preserved ignored pycache is not altered. Per owner policy the focused tier must also state which planned checks ran and that no `--changed` run is claimed.
* Impact: Checks may pass vacuously.
* Smallest useful change: List the phrases and the file-scope diff check (`git diff --name-only` equals the allowed set plus tracking) in P02-T01; require bytecode disabled; record exit codes.
* Action owner: planning parent
* Exact resolving evidence: changes record with each command, exit code, and an empty stale-phrase result.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Low]: Closeout and tier statement

* Related IDs: P03, plan Local tier row
* Evidence: plan Metadata and P03.
* Concern: P03 commits but does not state the repository-local noreply email setup, the dated preservation of the earlier review and behavior report, or that no push occurs and hosted CI is reported as not run. The Local tier row says "Focused" while the change edits validation policy and the coordinator agent; the plan should state that this is the owner's focused tier for documentation-only wording and that independent exact-head review and human and hosted approvals remain required and not yet obtained.
* Impact: Overstated readiness at handoff.
* Smallest useful change: Add those statements to P03 and the tier row.
* Action owner: planning parent
* Exact resolving evidence: changes and review records showing noreply author, untouched earlier artifacts (git diff shows no change), and a "hosted CI not run" statement.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Research findings are accurate against the runner and workflow (checked directly); scope is wording only with deletion and workflow bans explicit.
* Rejecting a categorical full tier while keeping unresolved-risk escalation matches the owner policy.
* Residual risk: host model limits may leave the behavior test Deferred; the plan accepts this honestly.

## Questions or Blocking Evidence Gaps

* None. The current README and instruction text were not supplied, so wording defects there are unassessed.

## Limitations

* Plan-level critique only; no execution; no review of the committed wording at HEAD 397ce435.

## Recommended Next Action

* Highest-impact finding: PC-002 (with PC-003 as the policy-critical item)
* Action owner: planning parent
* Smallest next action: revise the plan and details for PC-001 to PC-006, then finalize without another critique
* User response required: no
