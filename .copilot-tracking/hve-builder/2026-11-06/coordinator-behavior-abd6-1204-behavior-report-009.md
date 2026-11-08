---
title: Behavior report 009, coordinator idle recovery (issue 1204)
ms.date: 2026-11-06
---

* Targets: .github/agents/ama-backlog-delivery-coordinator.agent.md (agent, isolation), blob acefb44a4d254ede6d86413343127b763dec42cb, unchanged. HEAD at execution b16a03f21a4e73da60e011323b4b335827b4d809, tree 8063a0f8c8873ed829ea15d4644a2569e628682d (planning commit, made before any dispatch).
* Run type: full fresh. Reuse eligibility: Not applicable (report 008 has open findings). Reports 005 to 008 and sandboxes 001 to 007 were not reused, copied, regraded or modified.
* Profile: HIGH, a responsibility-based lead inference with uncertainty (r13 decision sha256 5cd213938e65e14d80adf69894ad372c3953b9736f39e94275c1846aa4280c5e), not declared metadata, not equal to native Automatic.
* Model and host attribution (own events.jsonl, subagent.completed, all explicit_override, firstDispatchedModel equal to model gpt-5.6-sol):
  * design, general-purpose, toolu_01Wm9ue6jK96EXagtjnipB4k, 15:25:55.547Z, 119603 ms;
  * execution, hve-core-all:hve-artifact-tester, toolu_01CZ5ETvbZhSC9FwsBN8emee, 15:27:45.499Z, 69514 ms;
  * grading, general-purpose, toolu_01XK2aVeV33saj5fkkWD4ycN, 15:29:22.224Z, 49511 ms.
  This is host attribution, not backend attestation. The executor reported "Resolved model: not supplied", a worker introspection gap distinct from host telemetry. The first design dispatch was the availability check; no canary or fallback was needed.
* Fidelity: simulation (read-only HVE Artifact Tester). Native Deferred.
* Execution status: Complete (11 scenarios, 24 sub-snapshots). Verdict: **Revise** (independent High grader): 2 High, 1 Medium, 0 Critical, 0 Low; 0 target defects.
* Sandbox: .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-008 (retained): run-state.md, executor-state.md, test-design.md, scenario-prompts.md, executor-trace.md, test-log.md, test-review.md, grader-return.md. External verbatim returns and manifest at /mnt/ama-gates/restart-1106-1204/ (designer-return-raw.txt sha256 a9910e9e9f516b395b06bd6baf353b6380b056ac6695593fa0c99195bba10a04; executor-return-raw.txt sha256 7fcf7cd48a9d20aeeeead748bd2886b9cc369cf4c4f8d9379e306c55790090c4; grader-return-raw.txt sha256 948ab2222d98e2fd1e25d55c7b1046bb9f6895e63d04b1559fd45b314f3c806c). Designer and executor returns were host-saved pointer files copied unchanged; the grader return was extracted from the session event record.

## Summary

The run closed the report 008 gaps in part. S09-style launch facts were supplied with explicit outcomes (H-03B, H-03G, H-08, H-09) and the executor invented none. The stale brief negative case (H-08) was exercised: the old brief was rejected, a fresh brief with the parent target was used, and worker publication stayed forbidden. R5 counts 15/16/20/21 and the eight cap were exercised (H-03). R6 positive replacement, duplicate repair and unverified refusal (H-04) and R8 positive removal of 1,500,000 bytes with five refusals (H-05) passed. Unconditional stop was obeyed and the conditional stop judged unmet (H-02). Baseline contracts were exercised: failed launch and bounded retry (H-09), merge gate, unchanged-head receipt refresh, justified rebase and checkpoint (H-10), final report (H-11).

Two new defects of this run are recorded honestly. The H-06 fixture used non-canonical `track/...` paths, so the executor correctly withheld all four publications and the positive batched stack publication was not exercised; I missed this in lead validation. In H-03F the executor said no slot was free with seven assignments; the design oracle shared that inconsistency.

## Findings

| # | Category | Severity | Dimension | Summary |
|---|---|---|---|---|
| F-01 | correct trace and fixture | High | Workflow contract | H-03F: seven assignments including exited #334 leaves one slot with ready work and a free slot is a defect under the target. The executor and the design oracle both denied admission. Executor error with a design inconsistency. |
| F-02 | correct fixture, add coverage | High | Evidence fidelity | H-06: fixture paths `track/...` are not the canonical RPI trees; the positive publication and stack path was not exercised. Fixture defect and lead validation miss, not a target defect. |
| F-03 | expand fixtures | Medium | Evaluation hooks | Unsupplied facts left behaviors unexercised: H-01 tick_log write, H-02D concrete local action, H-08 full hash, H-09 #702 log path, H-10 and H-11 checkpoint resume condition, H-11 eight PR identities. |

No target defect was demonstrated; no source correction is proposed or made. Resolving F-01 to F-03 needs a corrected fixture design under coordinator admission; this run does not consume another correction cycle.

## Adjudication and honest qualifications

* Reports 005 to 008 are preserved unchanged. The earlier S01 owner-stop adjudication stands; this run again covered both stop forms separately.
* Planning for this run (research, plan, details, one critique, state) was completed serially and committed as b16a03f21a4e73da60e011323b4b335827b4d809 before the sandbox and any dispatch.
* RV-004 was scoped to the six literal criteria; refinement retry, dependency cycles, board field mechanics and backlog-sync internals were declared intentionally untested.
* Live schedules were not read and tool frontmatter was not inspected or graded.

## Fidelity and limitations

Simulation supports conformance claims only. A High simulator may repair ambiguity a lower tier would expose. All Git, GitHub, SQL, schedule, session, merge and cleanup actions were emulated from fixture facts. Native tool reliability, atomicity, locking and restore are untested; containment was by read-only tools and instruction, not an enforced sandbox. The executor file reads are self-reported. The executor read the target directly from its state file instructions.

## Coverage

Criteria 1, 2, 3, 5 (negative path) and 6 (behavior evidence, with static review and focused checks as separate records) covered in simulation; criterion 4 simulated only. Positive publication gate and stack preservation (criterion 5, 6) not exercised, per F-02. Criterion 2 liveness slot rule failed in H-03F, per F-01.

## Containment

Pre-run ignored-inclusive status 0 lines; post-run only the new sandbox untracked; target blob unchanged. No shell, Git, GitHub, cloud, schedule or cleanup action by the executor.

## Satisfied-and-skipped

None.

## Human review

* [ ] Human review of this behavior report is complete.
