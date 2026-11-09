<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-1294-validation-policy

## Metadata

* Task ID: issue-1294
* Critique date: 2026-11-08
* Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-plan.md
* Phase details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: wording-only reconciliation of local validation tiers (targeted/focused vs full), hosted CI truthfulness and local-only coverage. No workflow, tool, application, security or branch-protection change. Mixed scope takes the strictest tier. Absent, path-filtered or skipped CI is never a pass. The full tier never becomes a partial receipt. Local-only behaviors are preserved through direct local checks. Testable examples for docs-only, small employee-chat/browser, SQL, Bicep/security and mixed. HVE Major lifecycle. Clean committed local candidate, no push.
* Research and evidence considered: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md (C1 to C23, W1). The cited source files were not re-read.
* Decisions, dependencies and acceptance criteria considered: plan AC1 to AC5, FR1 to FR4, P01 and P02 task dependencies, and the deferred follow-ups.
* Assessment boundary: plan credibility from the supplied artifacts only. The cited file:line evidence was not re-verified, and no research was performed beyond them.

## Coverage Assessment

| ID | Coverage | Evidence or concern |
|----|----------|---------------------|
| Caller: no workflow/tool/app/security/protection change | Covered | Plan non-goals and AC3 |
| Caller: strictest tier for mixed scope | Partial | Stated (FR1, P01-T02) but no tier classification criteria (PC-001) |
| Caller: absent, path-filtered or skipped CI is never a pass | Covered | Research C1, C21; P01-T02/T03 |
| Caller: full tier never a partial receipt | Partial | NFR says so, but P01-T03 keeps `--changed` as a "scoped receipt" route (PC-003) |
| Caller: local-only behaviors preserved via direct local checks | Partial | Local-only list is planned, but no direct commands are specified (PC-002) |
| Caller: testable examples | Partial | AC2 reproduces selection facts only, with no concrete path lists and no hosted-fact check (PC-004) |
| Caller: HVE Major lifecycle | Partial | P02-T02 has no pass criteria, and critique and review disposition has no task (PC-007) |
| Caller: clean committed candidate, no push | Partial | Conflicts with the untracked first-attempt artifact (PC-006) |
| FR1 to FR4 / P01-T02 to T04 | Covered | Targets match C9 to C11 and C23 |
| AC1 | Partial | Repo-wide claim with unspecified scan (PC-008) |
| W1 dated ruleset fact | Partial | Not rechecked before freeze (PC-009) |
| Hosted-CI wording vs existing "hosted CI required" | Partial | Possible weakening (PC-005) |

## Verdict

* Verdict: Revise
* Rationale: The direction (alternative A, wording-only) is evidence-backed and credible. Several decision-critical specifics are left to the implementer: tier boundary criteria, executable direct-check commands, the receipt rule for the full tier, concrete example inputs and the clean-commit conflict. Each is a direct planner correction, and no user decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: No classification criteria for "small", "major" and strictest-wins

* Related IDs: FR1, P01-T02, P01-T03, research C7, C9
* Evidence: plan Functional Requirements and phase-details P01-T02 list tiers by name ("major features, SQL, infrastructure, deployment, security-sensitive changes and releases"). The research notes that `changed_groups` falls back to full only for unmapped paths.
* Concern: Tier selection is left to judgment and not tied to a checkable rule. Workflow, `tools/*`, dependency, Dockerfile and rubric-workflow changes appear nowhere in the plan, so they have no assigned tier. The tool's `--changed` selection is not the tier rule (a SQL path can map to a subset), so the text must say that classification is by change category, not by tool selection or diff size.
* Impact: A mixed or workflow/tool change could be self-classified as focused. That defeats the strictest-wins requirement.
* Smallest useful change: Add to P01-T02/T03 a rule that classifies by path or category (SQL, infra/Bicep, deployment, security controls, workflows, tools, dependencies, releases, big features, all full tier). Documentation or instruction only, or small non-sensitive code, is focused. Any doubt or unclassified path takes full. State that the tool's selection and diff size do not lower the tier.
* Action owner: planning parent
* Exact resolving evidence: the revised P01-T02/T03 text names the category list and the doubt-takes-full rule, and the P02 example for mixed cites it.
* Decision route: direct planner correction (consistent with D4 and the caller's strictest-wins requirement)

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Local-only checks lack executable direct commands

* Related IDs: P01-T03, research C12 to C14, C18, C19
* Evidence: the plan says the guide lists local-only checks "stay local or direct", and the example table names `employee_chat_browser_check` with the pinned axe. Research C12 locates these inside `rpi-checks.py` group logic, and no invocation is recorded.
* Concern: It is unspecified how a focused-tier author runs the employee-chat axe harness, or the exact-count zero-skip chat-panel selector, without the full gate or `--changed`. If these are reachable only via `rpi-checks.py` groups (or a `--changed`-selected group), the "direct local check" instruction is not actionable or truthful.
* Impact: Dropping the default `--changed` could silently lose the only coverage of the harness, which is the caller's explicit preservation requirement.
* Smallest useful change: In research or P01 (read-only), identify the exact supported command for each local-only check (for example a group or selector option on the existing tool, or the module and environment invocation). Put the command in the guide examples. If none exists without a tool change, state that the author runs the scoped `--changed` or group run for that example, and record a follow-up. Do not invent flags.
* Action owner: planning parent
* Exact resolving evidence: each local-only item in the guide has a command cited to `tools/rpi-checks.py` or tests, and P02-T01 runs a dry-run or `--help`-level check that the command or option exists.
* Decision route: direct planner correction (a tool change stays out of scope and becomes a follow-up)

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `--changed` scoped receipt could be read as a full-tier receipt

* Related IDs: P01-T03, NFR full tier, research C20
* Evidence: P01-T03 says to keep `--changed` "as the way to obtain a scoped receipt when wanted". The NFR says full tier has no partial receipt.
* Concern: Nothing in the plan states that a `--changed` or scoped receipt never satisfies the full tier, or that full-tier text must require `--all` with `--base` and the verified external receipt. It is also unstated whether a scoped receipt carries any weight for the focused tier.
* Impact: This reopens the partial-receipt path the caller prohibits.
* Smallest useful change: Add the explicit sentence, and an AC grep check, that a scoped or `--changed` receipt is optional evidence for the focused tier only and never substitutes for the full tier.
* Action owner: planning parent
* Exact resolving evidence: the final guide and instruction text contain that sentence, and the P02 stale-wording grep includes a check for it.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Examples are not yet testable as specified

* Related IDs: AC2, P02-T01, research example table
* Evidence: P02-T01 only imports `changed_groups` and `ci-affected.select`. The example table includes hosted facts (`src-api` steps, `mssql` selectors, `src-namespace`).
* Concern: No example lists concrete path sets, expected selected groups or projects, or expected CI behavior. Hosted claims (selector step, axe not hosted, `src/**/*.md` selects no project) have no stated reproduction method, for example a read-only grep of the workflow at an exact line. "Small employee chat change" is not tied to real paths. SQL, Bicep and mixed examples are stated only as "full tier", with no selection check that they map to full or to groups consistent with that.
* Impact: AC2 can pass without showing that the examples are true, and the examples can become stale unnoticed.
* Smallest useful change: In P01-T03/P02-T01, give each example a concrete path list and the expected outputs (`changed_groups`, `ci-affected.select`). Add read-only grep checks for each hosted claim with file:line. Record the outputs in the changes record, and state in the guide that the examples were verified at the base SHA.
* Action owner: planning parent
* Exact resolving evidence: the changes record has a per-example table (paths, selection output, workflow grep) matching the guide table. Where `--changed` selects a lighter set than the stated tier, the guide says explicitly that the tier governs.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Hosted CI wording could weaken the existing requirement, and it cannot be observed in this run

* Related IDs: P01-T02, AC4, caller "no push"
* Evidence: the existing instruction text requires hosted CI for every tier. P01-T02 changes this to "hosted CI where it applies". Research W1 shows empty required contexts.
* Concern: Two risks. (1) The rewording may read as dropping hosted CI for docs-only PRs, when the correct rule is "any applicable hosted check must have run for the exact head, and absence is recorded as not evidence". (2) This run does not push, so the candidate cannot claim hosted evidence, and the summary and changes record must not imply it.
* Impact: The truthfulness requirement could be undercut by the change itself.
* Smallest useful change: Keep the existing "independent exact-head review, hosted CI and human approvals remain required for every tier" sentence. Add the clarification that absent, path-filtered, skipped (`run: false`) or unobserved CI is recorded as not evidence and is never success. Record in the changes record that hosted CI is unobserved for this candidate.
* Action owner: planning parent
* Exact resolving evidence: the final instruction diff retains the sentence and the rule, and the changes record states hosted CI is unobserved.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: "Clean committed candidate" conflicts with the preserved untracked artifacts

* Related IDs: AC5, P02-T03, caller clean-candidate requirement
* Evidence: git status currently shows the untracked first-attempt research file, and the plan leaves the commit-or-leave decision as "leave untracked, report". The plan's own AC5 and the caller require a clean tree.
* Concern: A leftover untracked file makes the tree not clean. The plan also does not say whether plan, details, critique and research artifacts under `.copilot-tracking/` are committed (they appear untracked, not ignored).
* Impact: A frozen exact-head candidate that is dirty fails the clean-snapshot gate and the caller's requirement.
* Smallest useful change: Decide before implementation. Either commit the retry research, plan, details, critique and changes (and the first-attempt file as adverse evidence, unmodified), or move it out of the worktree to an external preserved location with its hash recorded. Do not delete it. Then verify `git status --short` is empty.
* Action owner: planning parent (the preservation choice is within the caller's stated requirement)
* Exact resolving evidence: `git status --short` is empty at freeze, the first-attempt file's SHA-256 still equals the recorded `7305e775...bf12d` wherever it is preserved, and the changes record names the chosen location.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: HVE Major lifecycle and critique disposition lack tasks and pass criteria

* Related IDs: AC4, P02-T02, P02-T03, plan "Critique Disposition", "Dependencies"
* Evidence: P02-T02 has "five scenarios" without defining expected results. The plan says a separate review phase exists but defines none. "Critique Disposition: Pending" has no task to record the disposition.
* Concern: The simulation has no pass criteria, so Pass cannot be distinguished from not run. No task applies or records the critique disposition, or sequences the original review before the commit. P02-T03 depends on T01 and T02 but not on a review phase. The Deferred fallback for the tester is allowed, but its consequence for AC4 is not stated.
* Impact: HVE Major gate evidence may be vague, and an unreviewed commit could be frozen.
* Smallest useful change: In P02-T02, list the five scenarios with expected tier, required checks and forbidden claims (taken from the example table). Add a task or step to record each PC finding disposition in the plan and changes record. Order the original review before the commit. State that a Deferred simulation means AC4 is recorded as Deferred and not Pass.
* Action owner: planning parent
* Exact resolving evidence: the plan has a recorded critique disposition per PC-xxx, the scenario table exists in the HVE evidence, and the review artifact precedes the commit.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-008 -->
### PC-008 [Low]: AC1 is a repository-wide claim without a defined scan

* Related IDs: AC1, AC3, research Prior Knowledge and C22
* Evidence: AC1 says "No current file says every candidate needs a local gate or that `--changed` is the default." The research surveyed these by grep, but no pattern list or file list is recorded. AC3 limits the diff to in-scope files.
* Concern: Other restating files (for example the root README, agent files, docs/reference pages) may carry the blanket wording and, if found, would force an out-of-scope edit or an unrecorded residual contradiction. The scoped exceptions (rubric README step 3) are not made part of the check.
* Impact: Possible residual contradiction, or a scope-versus-AC clash discovered at freeze.
* Smallest useful change: In P02-T01, define the grep patterns and the searched trees. Record the hits, including the intentionally unchanged ones (C22), with a disposition. Any new contradictory file is added to scope as a direct update, since it is wording-only and tightly coupled.
* Action owner: planning parent
* Exact resolving evidence: the changes record has a hit table with no unresolved blanket-gate hits.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-009 -->
### PC-009 [Low]: The dated ruleset observation can go stale and is not rechecked

* Related IDs: W1, P01-T03, research Self-check
* Evidence: W1 is a point-in-time read (2026-11-08), and the research says to recheck before publication.
* Concern: Embedding "no required status contexts" in a guide is an operational claim that can silently become false. The plan has no recheck step.
* Impact: The guide could misstate branch-protection facts.
* Smallest useful change: Reword so the policy does not depend on the observation ("required or not, applicable hosted CI must have run; absence is not a pass"), keep the observation only as a dated, sourced note, and recheck read-only at P02 with the result recorded.
* Action owner: planning parent
* Exact resolving evidence: the guide text is correct regardless of the ruleset, and the changes record logs the recheck result and date.
* Decision route: direct planner correction

## Strengths and Residual Risk

* The research is thorough, with file:line citations, contrarian analysis and a rejected-alternatives record. The scope is narrow, and the nonconforming first attempt is handled as adverse evidence.
* The CI truthfulness trap (`src/**/*.md` selects no project but jobs report success) is identified and carried into the plan.
* Residual risk: the follow-ups (hosting the axe harness in CI, zero-skip verification of the hosted selector, #470 timing) stay unresolved. They are acceptable as deferred because they need workflow or owner direction.

## Questions or Blocking Evidence Gaps

* None. All findings are resolvable by the planning parent from the repository evidence.

## Limitations

* The cited file:line evidence was not independently re-read, and no commands were run. Conclusions rest on the supplied research and plan.
* Wording quality of the not-yet-written edits cannot be assessed.

## Recommended Next Action

* Highest-impact finding: PC-002 (local-only checks lack executable direct commands), with PC-001 (tier criteria) joint highest
* Action owner: planning parent
* Smallest next action: revise the plan and details to apply PC-001 to PC-009 (direct corrections), then finalize without another critique
* User response required: no
