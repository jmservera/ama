<!-- markdownlint-disable-file -->
# RPI Plan Critique: gate-chat-test-572-validation-correction

## Metadata

* Task ID: 572
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-validation-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-chat-test-572-validation-correction-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction: evidence-only continuation on chore/gate-chat-test-572; latest-main non-rewriting merge; 1800-second shared-heavy-lock admission and one admission-timeout retry; actual API tests, Ruff and full exact-head gate; pip only; no secrets or Azure changes; required trailer, nonforce push and main PR only after publication gates.
* Correction research: .copilot-tracking/research/2026-10-31/gate-chat-test-572-validation-correction-research.md, C1-C5/W1.
* Parent evidence: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md; .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md; .copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md; .copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md; .copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md.
* Implementation/guide boundary: tools/rpi-checks.py:2309-2424, especially heavy_lock/main; src/README.md:61-185 and :259-274. Repository original/addendum, reference index and memory were read for standing context, not as technical acceptance proof.
* Supplied base/head: 1330869e / 11829dbd; requested merge already reports up to date. This is supplied historical identity, not an independently refreshed publication base.
* Acceptance mapping from the supplied parent plan: AC1 owned selector/flag/path/coverage plus actual named Chromium success and zero skips; AC2 fail-closed unexpected integration/dependency skips; AC3 semantic identity/count/skip regressions; AC4 post-Review committed full browser/MSSQL gate, fresh receipt verification and publication safeguards.
* Canonical tests: tools/test_rpi_checks.py and src/api/tests/test_chat_panel.py; no removals, maximum zero additions in this correction. No source/workflow/dependency redesign is authorized.
* Assessment covers requirements, research credibility, phases/tasks, dependencies, decisions, acceptance and evidence safety once. It does not execute validation, approve publishing, or replace original Review, independent exact-head assessment, hosted checks or owner merge approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Branch/main continuation | Partial | Current merge is supplied as satisfied; later reconciliation follows validation/Review, PC-002 |
| C1/C2; historical RV-001/RV-002 | Covered | Adverse execution and gate outcomes remain historical and unmodified |
| C3-C5; shared lock and 1800-second admission | Partial | Internal full-gate lock correctly avoids outer-flock deadlock; execution-path conflict, PC-001 |
| P01-T01; API/Ruff/tooling | Covered | Existing venv, documented fixture paths, missing-dependency-only restoration, external logs |
| P01-T02; AC1 | Partial | Exact selector, opt-in flag, verbose success and zero skips specified; PC-001 |
| AC2/AC3; test ownership | Covered | Existing negative regressions retained, zero additions/removals; tooling tests scheduled |
| P02-T01; independent correction Review | Partial | One Review and historical preservation specified; blocking disposition needs explicit gate, PC-003 |
| P02-T02; candidate commit | Covered | Reconciliation, gh identity, repository-local noreply author/committer, trailer, external final receipt |
| P03-T01; AC4 | Partial | Full committed gate, internal lock, fresh output and admission-only retry; PC-001/PC-002 |
| P03-T02; exact-head publication | Partial | Fresh-main verification, independent assessment, nonforce push, truthful issue linkage; PC-002/PC-003 |
| No secrets/Azure; human/hosted approval | Covered | Synthetic local execution only; no cloud fallback or acceptance substitution |

## Verdict

* Verdict: Revise
* Rationale: The evidence-only approach and lock ownership are credible, but the current executor cannot perform the planned lock file operation under its file-operation restrictions. Later main reconciliation also needs an explicit source-review/validation invalidation rule, and blocking correction-Review findings must be an explicit publication stop. These are direct safety corrections, not requests to revisit confirmed user direction.
* Severity summary: 2 High, 1 Medium; no Critical or Low findings.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned shared-lock operation conflicts with the execution file-operation boundary

* Related IDs: C3-C5, P01-T02, P03-T01, AC1, AC4.
* Evidence: Correction phase details P01-T02 names /tmp/ama-rpi-heavy.lock; tools/rpi-checks.py:2309-2312 opens that same path with O_CREAT | O_RDWR. Current execution constraints prohibit file operations under /tmp and temporary directories. External log placement does not remove this lock-path operation.
* Concern: Correctly avoiding an outer lock around the full gate solves self-deadlock, but does not establish that either focused flock or the runner's internal file open is permitted in this execution environment.
* Impact: Both required heavy validations remain execution-blocked here. An alternate lock would split ownership, and changing the runner is outside this evidence-only scope.
* Smallest useful change: Explicitly record this environment prerequisite and a fail-closed stop before either heavy command. Route execution to an already permitted, coordinated executor that uses the unchanged shared lock, or leave validation/publication blocked. Do not substitute another lock, bypass admission, edit source or claim a pass.
* Action owner: Planning parent / execution coordinator.
* Exact resolving evidence: Revised P01-T02/P03-T01 identify a permitted executor and its file-operation capability for the existing shared lock; resulting real command logs bind that executor, unchanged lock, exits and exact source/base. If unavailable, changes/state explicitly preserve blocked AC1/AC4 and no publication.
* Decision route: Direct planner correction and execution-prerequisite routing. No divergent user decision is needed; existing same-lock/no-bypass direction remains binding.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Main reconciliation after correction Review can change the reviewed source boundary

* Related IDs: P01, P02-T01, P02-T02, P03-T01, P03-T02, AC1-AC4.
* Evidence: P01 collects focused evidence and P02 obtains the one correction Review before P03-T01 fetches and merges moved main. P03-T02 requires a new candidate/full gate on drift, but neither task explicitly invalidates the earlier source Review or focused evidence when the merge changes relevant source, tests or tools.
* Concern: A full passing gate proves execution at a new head, not independent source review of changes introduced after the frozen Review. The currently up-to-date merge does not prove that future reconciliation is evidence-only.
* Impact: A candidate could publish with a passing exact-head receipt while carrying relevant changes outside the correction Review's assessed source boundary.
* Smallest useful change: Reconcile main before freezing P01/P02 evidence where feasible. At every later drift checkpoint, compare relevant source/test/tool inputs with the reviewed boundary. Evidence-only ancestry changes may proceed with a documented equivalence assessment; relevant changes stop this validation-only continuation and require explicit correction scope and independent assessment of the changed boundary before publication. Do not silently rerun the same original Review or rewrite history.
* Action owner: Planning parent.
* Exact resolving evidence: P03 tasks contain the source-equivalence/stop rule; correction evidence records full reviewed head/base and the later candidate comparison. Eligible exact-head assessment explicitly covers any relevant delta or records no relevant delta, with current full receipt verification.
* Decision route: Direct planner correction. Requested latest-main merge and non-rewriting lineage are already authorized; only an actually discovered divergent source change needs a separate scoped decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Correction Review has no explicit blocking-findings publication disposition

* Related IDs: P02-T01, P02-T02, P03-T02, AC4.
* Evidence: Correction P02-T01 says Review examines source/evidence/AC1-AC4 and distinguishes pending final gate from source defects. P03-T02 requires passing evidence but does not expressly require no unresolved blocking correction-Review findings. The parent plan/details explicitly imposed that condition for the original Review.
* Concern: Completing the one correction Review is not equivalent to receiving an eligible source/acceptance disposition. A residual result may contain a blocker other than the intentionally later full gate.
* Impact: The abbreviated handoff can treat Review completion plus a passing receipt as sufficient despite an unresolved blocking finding.
* Smallest useful change: Make P02/P03 explicitly require disposition of every correction-Review finding: planned final-gate evidence proceeds to P03; source/acceptance blockers stop publication; nonblocking residuals retain named disposition without relaxing criteria. Preserve original Review outcomes and perform no additional critique pass.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T01/P03-T02 specify the condition; the single correction Review and final exact-head assessment enumerate blocking findings as resolved or absent and record accepted residuals. Hosted/human gates remain separate.
* Decision route: Direct planner correction, not a user-authorized publishing decision.

## Strengths and Residual Risk

* Focused browser outer admission and full gate internal admission correctly use one unchanged lock without double-locking the runner. The explicit 1800-second wait/retry direction resolves the older guide's nonqueued-admission recommendation for this continuation.
* Admission retries are bounded and distinguished from assertion/prerequisite failures; adverse evidence is immutable and new output directories are required.
* Commit-before-full-gate, external authoritative receipts, fresh-main verification and no post-gate evidence commit protect exact-head evidence.
* No new tests, workflow edits, dependency-pin changes, cloud access or skip relaxation are invented.
* Shared-resource availability and actual browser/MSSQL outcomes remain unknown until permitted execution. They are not accepted successes or grounds for issue closure.

## Questions or Blocking Evidence Gaps

* No user clarification is required by this critique. PC-001 is an execution prerequisite that the planning parent must resolve or record as blocked.
* Current issue text was not independently retrieved; acceptance is assessed against the supplied parent AC1-AC4 and correction research's dated issue pointer. Final issue linkage must use proven criteria, not this critique as current acceptance evidence.

## Limitations

* No tests, lint, browser, gate, network retrieval or Git mutations were executed.
* Read-only Git status/branch inspection confirmed chore/gate-chat-test-572 and existing untracked correction artifacts. No such artifact was moved, committed, discarded or edited.
* Historical source Review and validation results are supplied evidence, not fresh reviewer execution. This critique assesses plan credibility, not current source correctness or final receipt eligibility.
* Only this requested critique artifact was written. Parent plan/details/research/changes/reviews remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent / execution coordinator.
* Smallest next action: Record permitted unchanged-lock execution as a prerequisite, then directly incorporate PC-002/PC-003 safeguards before finalizing the plan.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/gate-chat-test-572-validation-correction-plan.md](.copilot-tracking/plans/2026-10-31/gate-chat-test-572-validation-correction-plan.md) | Assessed final-candidate correction plan |
| [.copilot-tracking/details/2026-10-31/gate-chat-test-572-validation-correction-phase-details.md](.copilot-tracking/details/2026-10-31/gate-chat-test-572-validation-correction-phase-details.md) | Assessed correction tasks |
| [.copilot-tracking/research/2026-10-31/gate-chat-test-572-validation-correction-research.md](.copilot-tracking/research/2026-10-31/gate-chat-test-572-validation-correction-research.md) | Bounded correction research |
| [.copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md](.copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md) | Parent acceptance and publication contract |
| [.copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md](.copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md) | Parent implementation/Review sequencing |
| [.copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md](.copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md) | Parent exact-case research |
| [.copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md](.copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md) | Preserved historical validation and adverse gate |
| [.copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md](.copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md) | Preserved original Review and RV-001/RV-002 |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Shared heavy_lock/main contract |
| [src/README.md](src/README.md) | Local gate, lock and publication guidance |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-validation-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-validation-correction-plan-critique.md) | This single Complete / Revise critique |

## Next Steps

Active planning parent applies the complete PC-001-PC-003 set directly and finalizes without another critique. No user action is required. This critique agent stops here; it has no implementation, validation or publishing handoff authority.
