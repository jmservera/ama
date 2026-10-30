<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue 440 stabilization checkpoints

## Metadata

* Task ID: jmservera/ama#440.
* Critique date: 2026-10-23.
* Plan: .copilot-tracking/plans/2026-10-23/issue-440-stabilization-plan.md.
* Phase details: .copilot-tracking/details/2026-10-23/issue-440-stabilization-phase-details.md.
* Critique execution status: Complete.
* Assessment: one independent final-candidate plan critique; no implementation or final RPI Review performed.

## Inputs and Criterion Boundary

* Assessed the complete supplied plan, phase details, research C1-C15/W1-W4 and pinned document identities, complete issue-440-current-issue.json, and supplied caller decisions.
* Checked named source contracts in src/README.md, tools/rpi-checks.py, .github/workflows/src-ci.yml and .github/agents/ama-backlog-delivery-coordinator.agent.md. Confirmed the named focused auth, assistant, resident, safety and importer selectors exist in their owning test files; no selector was executed.
* Read the required original case study, addendum, KB index, owner memory and sector primer for context. Memory is not evidence. No new legal-currentness claim is made.
* Planning requirements include recurring checkpoints, cap eight rather than a fill target, document-qualified traceability, a real local-first ladder, current-main rather than sibling-feature assessment, human/resident/manual/AI-failure safeguards, deduplicated separate code-fix loops, and retained per-issue RPI/merge/exact-head receipt controls.
* Ownership is locked: no removals; zero source/test additions; only the existing coordinator, src README, cutover evidence pack and necessary KB index/append-log are production targets; no generated production targets. Seven P04 semantic scenarios are distinct from existing source regression tests.
* The supplied #349 lock ownership and explicit stop govern this invocation. The preflight log records PID3256519 holding the heavy lock at 2026-10-23T12:29:30Z. Ownership was not polled or freshly inspected here. It is not evidence of release.
* This assessment determines planning credibility only. Runtime checkpoint results, final-candidate HVE static/behavior/host outcomes, original RPI Review, receipts and publication eligibility remain future evidence. Missing future artifacts are not findings against this planning-stage candidate.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| F1/F2, A1, P02-T01 | Covered | Three trigger classes, cap eight/not-fill, continue/fix/pivot and affected closure/dependent expansion only; unrelated lanes continue. |
| A2, P01-T01, P03-T02, C5-C9/C14 | Covered | Main/source, merged PRs/issues, BRD/PRD/ADR identities/status and document-qualified IDs are required; research pins draft/candidate/proposed versus accepted states. Refresh is explicitly required on resume. |
| F3, A3/A4, P03-T01, C11-C13 | Partial | Concrete focused selectors and honest evidence tiers are credible; the clean-source/resource-owning execution boundary and pre-P04 runner invocation are unresolved in PC-001. |
| A3, P02-T01, P04-T01 | Partial | Current Azure prohibition and Unknown-headroom refusal are sound; recurring Azure-only admission conditions omit part of the issue's explicit contract, PC-002. |
| Human/resident/manual/AI-failure boundaries, P03/P04 | Covered | Existing selectors cover constructed auth, independent review, resident pause/restart, safety separation, durable/manual failure paths and import review; none is presented as live acceptance. |
| F4, A5, P03-T02 | Covered | Refresh dedup inventory, preserve existing gaps, file independently scoped bug/refactor work with regression evidence, and do not manufacture a refactor. Existing coordinator also requires testable issue acceptance criteria. |
| N1, locked ownership, P02/P04 | Covered | Existing agent/frontmatter/capability surfaces preserved; seven bounded semantic scenarios require real tester execution with fidelity limitations; no reusable source testing framework is proposed. |
| A6, P04-T01/T02 | Covered | Independent final-candidate static assessment, actual hve-builder-tester activation, actual host validation and one original independent RPI Review are later prerequisites; Deferred is not Pass. |
| N3, A6/A7, P05-T01 | Covered | Frozen committed candidate, external full receipt, current-base verification and independent exact-head assessment precede publication; no fabricated hosted/human approval or automatic issue closure. |
| N2, P01, busy-lock stop | Covered | Finish planning, record continuation, stop now; no queue, polling, competing heavy work, cloud action or push. Planning readiness is separate from execution blockage. |

## Verdict

* Verdict: Revise.
* Rationale: the scope, safeguards and later validation obligations are credible, but P03 needs an executable source-checkpoint/runner boundary rather than an assumed focused harness, and the recurring Azure-residual rule needs the complete admission conditions already supplied by the issue.
* Severity counts: Critical 0; High 1; Medium 1; Low 0.
* Execution readiness: Blocked independently by the supplied #349 ownership and caller stop. Resolving these planning findings does not release that blocker or authorize implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Make the pre-Review current-main integration checkpoint executable under the actual runner contract

* Related IDs: F3, A2/A4/A6, N3, P01-T01, P03-T01/T02, P04 dependencies, P05-T01; research C11/C13.
* Evidence: .copilot-tracking/details/2026-10-23/issue-440-stabilization-phase-details.md:79 and :95-97 assign SQL/container ownership to the existing native runner and allow an unspecified existing resource-owning local harness. The only explicit full-run command is at :170 in P05, after P04. P03 evidence is required before P04. src/README.md:61-75 defines the runner's clean exact-HEAD detached snapshot and owned resources. tools/rpi-checks.py:147-165 rejects dirty, untracked and ignored inputs and requires current origin/main ancestry; :1519-1535 runs the complete matrix; :1692-1727 exposes only --all or --verify-receipt, with --extra-test additive to the full run, not a focused SQL/browser mode. The supplied worktree currently has untracked planning/research artifacts, and P02/P03 introduce further changes before P05's planned freeze.
* Concern: the plan does not select a supported invocation and clean identity transition for the actual resource-owned P03 checkpoint. Calling the native runner on the then-dirty policy/evidence branch will be refused; using P05's eventual policy-candidate receipt to fill P03 retrospectively reverses the declared dependencies and obscures current-main source versus candidate-policy evidence. Source CI selectors alone do not supply the native runner's local ownership/cleanup contract.
* Impact: the first checkpoint can stall before SQL/container evidence, or be overstated using a later candidate gate. Distinct labels alone do not establish which bytes and environment were tested.
* Smallest useful change: revise P01/P03/P05 details to choose one supported execution sequence. State the exact source freeze, clean-input preparation, main/source identity proofs, resource-owner invocation, no-wait lock behavior, output identity, cleanup owner and evidence-persistence transition. A viable option is a separately identified clean preliminary engineering-checkpoint commit whose tested application/test/build inputs are proven equal to pinned current main, followed by the existing --all runner with --lock-timeout 0 after focused checks. Distinguish that preliminary checkpoint receipt from publication eligibility: later policy/evidence commits invalidate its final-candidate eligibility, and P05 still requires a fresh full gate after original Review. Alternatively name an actually existing supported focused owned harness and its concrete command; do not invent a partial runner mode or add tooling. Reconcile branch ancestry on resume too: if fresh main is not an ancestor, record a branch-reconciliation blocker rather than silently rebase or claim a current-base receipt.
* Action owner: planning parent.
* Exact resolving evidence: revised plan/details show an acyclic P03 -> P04 -> P05 sequence, a supported concrete P03 resource-owning command and clean-input transition, explicit tested-source equality/identity criteria, and two distinct receipt purposes. A moved-main contingency must either satisfy the runner's ancestry requirement within existing authority or stop explicitly. No actual run, new implementation artifact, receipt, commit or history mutation is required to resolve this planning finding now.
* Decision route: direct planner correction within supplied scope. No owner reauthorization is required for documenting the sequence; any subsequently necessary unauthorized history mutation remains a separate blocker, not implied permission.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Carry the complete Azure-residual admission rule into the recurring policy

* Related IDs: A3, N2, P02-T01, P04-T01; complete issue acceptance criterion on Azure-only residuals; research C10/W1.
* Evidence: .copilot-tracking/research/2026-10-23/issue-440-current-issue.json requires explicitly listed Azure-only residuals after relevant local checks pass, valid authority, complete cost headroom, a finite plan and cleanup boundaries. .copilot-tracking/details/2026-10-23/issue-440-stabilization-phase-details.md:59 reduces this to an ordered ladder ending in "explicitly authorized Azure-only residuals"; its P04 Unknown-headroom scenario at :135 covers one refusal case. The existing coordinator's generic financial/human blockers do not state the complete residual admission predicate. The plan correctly prohibits Azure in this execution, but it authors a reusable recurring policy.
* Concern: ordering and unspecified authorization do not explicitly require passing relevant local checks, complete all-in headroom, a finite residual execution plan and exact cleanup boundaries before a later Azure action. Those are supplied requirements, not discretionary future enhancements.
* Impact: a later coordinator could treat a nominal authorization or known partial budget as sufficient, or advance to Azure after failed local checks, despite the intended local-first and financial boundaries.
* Smallest useful change: add the complete conjunctive admission rule to P02's required policy content and A3: named Azure-only residuals, relevant local checks passed, valid action-specific authority, complete all-in headroom including outside-group costs/accruals, finite scope/budget/stop conditions and exact owned cleanup boundaries. Unknown or incomplete evidence blocks only Azure-dependent work; independent local work continues. Expand the existing cost/headroom semantic scenario's grading expectations within the same seven scenarios to verify these conditions and reject partial permission/headroom.
* Action owner: planning parent.
* Exact resolving evidence: updated P02 requirements and existing P04 scenario specify each prerequisite and a refusal outcome for missing/incomplete conditions, while retaining the present no-Azure boundary and the unchanged expiry/Unknown headroom of the USD700 all-in ceiling. Resolution needs plan/detail wording, not Azure inspection or execution.
* Decision route: direct planner correction implementing already-supplied issue requirements; no significant/divergent owner decision and no cloud authorization request.

## Strengths and Residual Risk

* The bounded recurring policy is integrated at selection/wave/closure transitions rather than substituted for individual issue delivery.
* Requirement/ADR statuses and source identities are distinguished from approval; future worker architecture and current shared-process behavior are not conflated.
* Named existing focused selectors make the initial local ladder credible without adding source tests. Seven semantic policy scenarios remain tester-owned future execution, not asserted present passes.
* #349 tenant/session, #350 deployed parity/API302, #360 live demo and #432 planned Tokenomics gaps remain open. Historical redirects, mock principals, local SQL and scripted assistance cannot satisfy their live or human criteria.
* HVE host discovery remains an honest later evidence risk: unavailable safe host validation is Deferred and cannot satisfy A6. No demand for a new host tool, coordinator launch or prose-only pass is made here.
* Main movement during the enforced pause can invalidate pins and ancestry. Refresh on an eligible resume; do not poll now or silently rewrite this branch.

## Questions or Blocking Evidence Gaps

* No unresolved owner scope question is needed. Both actionable findings belong to the planner.
* The resource-owned execution sequence is a planning gap, not proof that the first checkpoint failed.
* The supplied lock ownership blocks execution, not completion of this critique or compatible plan corrections. No later-phase artifact is demanded during the pause.

## Limitations

* Read-only static assessment of the supplied boundary, plus this critique file only. No cloud/GitHub calls, installations, tests, gates, process mutations, other-worktree inspection, subagents or implementation edits were performed.
* No runtime results, current live deployment readiness, actual HVE behavior/host validation, final exact-head review or publication eligibility is established.
* Document identities and issue state are assessed from the supplied dated research and complete issue snapshot; no fresh remote claim is made.
* This is the complete actionable finding set for this boundary. Compatible planner corrections should be dispositioned directly without another critique or a fabricated later Review.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: document the supported clean preliminary source-checkpoint sequence and its separation from P05, then add PC-002's already-required Azure admission conditions.
* User response required: No.
* After compatible corrections: retain this original Revise outcome and record exact dispositions; finalize planning and stop at P01-T01's busy-lock continuation boundary. Do not enqueue, poll, implement, gate or push.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-23/issue-440-stabilization-plan.md](../../../plans/2026-10-23/issue-440-stabilization-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-23/issue-440-stabilization-phase-details.md](../../../details/2026-10-23/issue-440-stabilization-phase-details.md) | Assessed execution details and seven semantic scenarios. |
| [.copilot-tracking/research/2026-10-23/issue-440-stabilization-research.md](../../../research/2026-10-23/issue-440-stabilization-research.md) | Supplied evidence synthesis and pinned identities. |
| [.copilot-tracking/research/2026-10-23/issue-440-current-issue.json](../../../research/2026-10-23/issue-440-current-issue.json) | Complete supplied issue requirements. |
| [.copilot-tracking/reviews/plans/2026-10-23/issue-440-stabilization-plan-critique.md](issue-440-stabilization-plan-critique.md) | This original independent critique. |

## Next Steps

Planning parent applies PC-001 and PC-002 directly and records resolution evidence without requesting another critique. No user action is required. Preserve the #349 busy-lock stop and exact P01-T01 resume point; no transition to Implement, final Review, heavy execution or publication is eligible in this invocation.
