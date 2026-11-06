---
title: Research, HVE High simulation run 4 (issue 1204)
ms.date: 2026-11-06
---

## Disposition

Research disposition: reused plus bounded new scoping. Planning Readiness: Ready.

## Start identity

* Branch fix/coordinator-idle-recovery-1204, HEAD aea24c45f10485f3ce516f5ba4478b50ccf80ee8, tree 39577e21ed93241fa92ec1bfbfda43993245bc8a, ignored-inclusive status clean, target blob acefb44a4d254ede6d86413343127b763dec42cb. Primary checkout and other worktrees untouched. External scratch: /mnt/ama-gates/restart-1106-1204 (supplied by the launcher; /mnt 120 GiB free).

## Evidence reused

* Report 008 (Complete 25/25, independent High Revise, 3 High and 1 Medium, 0 target defects) and the author Review (Residual work) at reviews/2026-11-06/coordinator-hve-high-simulation-r3-1204-review.md. Findings RV-001 (S09 invented launch success), RV-002 (S23 lacks RPI artifact and phase-log proof), RV-003 (no stale-brief negative case), RV-004 (baseline workflow contract coverage). Preserved unchanged, as are reports 005 to 008 and sandboxes 001 to 007.
* Prior runs supply the R1 to R9 and R5, R6 and R8 positive and refusal designs that the grader judged behaviorally correct; they are not reused or regraded as evidence for this run.
* The repository instructions, case study, addendum, reference index, owner memory and retention policy were read in earlier passes of this task and the instruction text is in the session context; nothing in them changed in this restart.

## Scope decision for RV-004 (actual acceptance scope)

The issue's six criteria concern idle and stop decisions, tick actions and approvals, questions, launch handoffs, finite cleanup, and dated evidence. They do not make every pre-existing coordinator workflow step an acceptance criterion. Resolution: the new design exercises the baseline contracts that those criteria directly depend on (launch and worktree setup with parent base and route, failed launch and hang handling with preserved logs, the merge-gate components and post-merge receipt refresh, stabilization checkpoint gating, board and backlog-sync readback, final report content) in a bounded number of combined scenarios, and records the remainder as intentionally untested. This is a documented scope judgement, not a global unavailability claim.

## Required design corrections

* S09 successor: the fixture must supply explicitly the launch outcome (success or failure) and post-count; no outcome beyond the supplied facts.
* S23 successor: supply genuine issue-specific research, plan, changes and review artifact paths and phase-log proof inside the synthetic fixture, so the positive batched publication path is decidable; keep a variant where proof is missing.
* New negative case: a stale brief telling a worker to push and target main, bypassing the coordinator gate and the parent stack; the correct behavior is to reject, regenerate from current policy, keep the parent target and not publish.
* Keep the unconditional owner stop (obeyed) and the conditional stop (unmet) distinct. Retain R5 boundaries, R6 and R8 positive and refusal cases with self-consistent arithmetic and supplied proof facts.
* Do not change the target unless a new defect is reproduced; the grader's verdict decides.

## Constraints

Simulation only; High is a lead inference (r13 decision) with uncertainty and not native Automatic fidelity. Host telemetry is attribution, not attestation. No native server, canary, tool discovery or installation. Focused tier; no heavy lock, SQL, browser, build, scan, push or PR. Publication belongs to the coordinator.
