---
title: Resident assistant publication plan critique
ms.date: 2026-10-27
---

## Metadata

* Task ID: 469-publication-2026-10-27
* Critique date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/resident-assistant-aoai-publication-plan.md
* Phase details: .copilot-tracking/details/2026-10-27/resident-assistant-aoai-publication-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: Full publication-child RPI; existing feat/resident-assistant-aoai branch; preserved evidence before authorized cleanup; foreground changed-path gate with timeout zero and new external output; core/API/infra suites; complete gate coverage before publication; independent exact-head assessment; non-draft main PR containing Refs #469 without closing keywords.
* Evidence: Supplied publication research, plan and phase details; src/README.md local RPI gate contract; tools/rpi-checks.py selection, verification and lock entry points.
* Decisions: USD20 within approved USD30; private migration and authenticated MI smoke remain unmet; no Azure operations, deployment, ingress edits, uv, secrets, merge or main push. Main ancestry is accepted from supplied research, not re-investigated.
* Boundary: Publication sequencing and feasibility only. No fresh parent implementation review, execution, lock manipulation, source edits or delegation. Existing uncommitted publication inputs were observed, not changed.
* Test changes: Zero removals and zero additions, as planned.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Branch and main ancestry; C1; P01-T01 | Covered | Reuses approved topic, preserves ancestry and derives privacy-safe local identity. |
| Cleanup preservation; C6; P02-T01 | Covered | Finite inventory, archive, restore check, full tracking snapshot and tracked-byte verification precede cleanup. |
| Lock handoff; C3; P02-T01 | Partial | Correct non-reentrant handoff and stop-on-contention; execution-path incompatibility in PC-001. |
| Requested scoped gate; P02-T02 | Partial | New external output and timeout zero specified; PC-001 and PC-002 affect executable instructions. |
| Complete coverage; C2; P02-T02 | Covered | Full selected matrix or separate all-mode gate required; no partial receipt promoted to full evidence. |
| Core/API/infra suites; P02-T02 | Covered | Gate logs must prove execution, otherwise existing installed-distribution discovery is required. |
| Original adverse evidence; C4; P03-T01 | Covered | Child Review does not regrade parent or claim live acceptance. |
| Exact-head gate and publication; P03-T02 | Covered | Evidence commit precedes final run; fresh main, receipt verification and independent assessment precede push. |
| Budget, ingress and excluded operations; C5; P03-T02 | Covered | Correct budget and explicit unmet items; no activation, deployment, merge or main push. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 1; Medium 1; Low 0.
* Rationale: Publication safeguards are credible, but execution instructions need a fail-closed path for the temporary-file incompatibility and explicit handling of partial scoped verification. These are planner-owned corrections, not authorization for source changes or a second critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Gate execution is incompatible with the available file-operation boundary

* Related IDs: C3, P02-T01, P02-T02, P03-T02.
* Evidence: .copilot-tracking/details/2026-10-27/resident-assistant-aoai-publication-phase-details.md gives a temporary-directory output example. tools/rpi-checks.py:2175-2178 opens its fixed temporary-directory heavy-lock file. The available execution boundary prohibits temporary-directory file operations; the caller separately requires this runner to remain unchanged.
* Concern: Replacing the example output directory alone cannot make the unchanged runner executable within that boundary. The plan currently treats missing tools/tests as possible blockers but does not recognize this already-visible incompatibility.
* Impact: Proceeding as written would cross the file-operation boundary; redirecting the runner's lock or changing its implementation would violate the unchanged-runner/no-source-change scope.
* Smallest useful change: Replace the output example with a durable, non-temporary external location consistent with permitted file creation. Add an explicit execution blocker for the unchanged runner's fixed lock path. Preserve the existing reservation without manipulation by this critique; do not execute the gate or publish while that blocker remains. Do not propose lock bypass or a source patch.
* Action owner: Planning parent / publication executor.
* Exact resolving evidence: Revised phase details use an allowed external output location and record execution as blocked unless a permitted execution environment can run the exact unchanged lock contract. Publication additionally requires the actual clean-head full-scope receipt and immediate verification from that environment; a plan assertion is not evidence of resolution.
* Decision route: Direct planner correction and execution blocker. No significant or divergent user decision is requested; existing authorization does not resolve an unavailable execution capability.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Partial changed-path coverage exits unsuccessfully before the fallback is distinguished

* Related IDs: C2, P02-T02, P03-T02.
* Evidence: The P02-T02 command omits --required-scope. tools/rpi-checks.py:2203 defaults required scope to full; main invokes verify after Runner.run. tools/rpi-checks.py:2158-2165 rejects partial receipts under full verification. src/README.md:78-83 explicitly uses --required-scope partial for scoped receipt verification.
* Concern: If changed-path selection is partial, successful selected checks still produce an unsuccessful command exit at automatic full-scope verification. The plan permits an all-mode fallback but also says required failures block publication, without distinguishing this coverage-only rejection from real check failures.
* Impact: An otherwise expected partial selection can be misclassified as a test failure or, conversely, an actual failed gate can be treated as an acceptable scope mismatch.
* Smallest useful change: Specify the partial-selection branch explicitly: either pass --required-scope partial for the requested scoped run and require a separate full gate unless its actual scope is full, or document recognition of only the precise full-scope rejection after a passing partial receipt. Real check failures remain blocking. Give the separate all-mode run the same foreground, new-output and --lock-timeout 0 requirements. Keep final verification at required full scope.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02-T02 specifies scoped exit/receipt handling and a full-mode command or equivalent unambiguous parameters, with timeout zero. Execution later records passing selected checks separately from coverage and supplies a verified full-scope final receipt.
* Decision route: Direct planner correction; no significant or divergent user decision.

## Strengths and Residual Risk

* The supplied selection implementation confirms unknown paths conservatively select the full matrix. Changed workflows may therefore make PC-002's partial branch unnecessary for this candidate, but the explicit fallback must remain correct.
* Archive/restore-backed cleanup, evidence-before-gate sequencing, final clean-head verification and preservation of original adverse outcomes are explicit.
* Private migration, authenticated MI smoke, hosted checks and human acceptance remain unmet or pending, not local-gate successes.
* Lock contention remains a mandatory stop, never permission to wait, bypass locking or take over another owner's resources.

## Questions or Blocking Evidence Gaps

* No unresolved user choice. PC-001 is an execution capability blocker; PC-002 is a direct planning correction.

## Limitations

* No validation, Azure operation, cleanup, lock release, push or PR action was performed.
* Branch ancestry, lock ownership and current dependency availability were accepted from supplied research; this critique does not independently certify them.
* No parent implementation, private data, original Review contents or unrelated repository evidence was reopened.
* Only this critique artifact was written. Plan, details and research remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Apply both direct corrections once, record the execution blocker, and continue only if it can be cleared without changing source or bypassing constraints.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-assistant-aoai-publication-research.md](.copilot-tracking/research/2026-10-27/resident-assistant-aoai-publication-research.md) | Supplied publication research |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-publication-plan.md](.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-publication-plan.md) | Assessed publication plan |
| [.copilot-tracking/details/2026-10-27/resident-assistant-aoai-publication-phase-details.md](.copilot-tracking/details/2026-10-27/resident-assistant-aoai-publication-phase-details.md) | Assessed phase details |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-publication-critique.md](.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-publication-critique.md) | Complete single critique |

## Next Steps

The active planning parent applies compatible corrections directly and finalizes without another critique. Keep execution and publication blocked on PC-001 until permitted unchanged-runner execution is available. No user action is required.
