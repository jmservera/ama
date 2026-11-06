---
title: Behavior report 006, coordinator idle recovery (issue 1204)
ms.date: 2026-11-06
---

* Targets: .github/agents/ama-backlog-delivery-coordinator.agent.md (type agent, isolation), blob acefb44a4d254ede6d86413343127b763dec42cb, unchanged. Source HEAD at execution 58b72ce66c974e2f897e6e984910ae652bef8af2 (planning commit over 5258560b928f92282697ed1de057500ac23d3a19).
* Run type: full fresh. Reuse eligibility: Not applicable (the old 25-case report 005 and runs 001 to 004 are proxy evidence and were not reused or regraded).
* Profile: HIGH, a responsibility-based lead inference (long-horizon, irreversible-action authority boundaries), not declared metadata; Medium was a defensible alternative (r13 decision, sha256 5cd213938e65e14d80adf69894ad372c3953b9736f39e94275c1846aa4280c5e). High is not claimed equal to native Automatic or the router model.
* Models: first canonical High model gpt-5.6-sol requested for designer, executor and grader; all three dispatches were accepted without error (the first design dispatch served as the availability check). No subagent exposed returned model identity, so identity is requested-and-accepted, not confirmed: recorded as a profile-resolution gap and the run is labelled proxy for confirmed model identity.
* Fidelity: simulation (read-only HVE Artifact Tester). Native fidelity Deferred / Not available (tool inventory, filtering and containment unproven).
* Execution status: Complete (20 of 20 scenarios). Verdict: **Revise** (independent High grader).
* Sandbox: .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-005 (retained, not deleted). Evidence there: run-state.md, designer-return.md, test-design.md, scenario-prompts.md, executor-trace.md, test-log.md, test-review.md.

## Summary

19 of 20 scenarios graded Pass; S01 Failed. Finding 1 (High, correction): the target's pause exception ("the owner explicitly pauses the run", Liveness and stop decision) lets a stop instruction based on a false "everything blocked" premise end the recurrences even though ready, unknown and unassessed work remains. Smallest resolving change as graded: state that such a stop is not an unconditional owner pause; report the corrected classification and continue actionable work unless the owner pauses despite it. R3 is Partial; R1, R2, R4 to R9 covered.

Per the admission, the target was not edited and no correction cycle was consumed. A source correction needs coordinator scope and identity admission; the rerun condition is a full run (changed target and contract) after that correction, with a fresh design, executor and grader.

## Fidelity and limitations

Simulation evidence supports conformance claims only. A High simulator may repair ambiguity a lower tier would expose. All GitHub, SQL, schedule, tmux, validation, merge, board and cleanup actions were emulated. Live persistence, readback, locking, timing races, tool syntax and containment are untested. Containment was by read-only tools and instruction, not an enforced sandbox. Live schedules (delivery 15, cleanup 8) were not read or changed and are only as supplied by the coordinator.

## Coverage

R1 to R9 mapped across S01 to S20 (see the sandbox test-log.md). Only S01 failed. Designer-declared untested behavior: real tool execution, exact CLI syntax, repository settings, native containment, validation runners, board option discovery, report formatting.

## Containment

Executor reads: target, run-state.md, scenario-prompts.md; no writes. Status delta against the pre-run status: only the new sandbox folder, lead-written.

## Satisfied-and-skipped

None.

## Human review

* [ ] Human review of this behavior report and its limitations is pending; the agent leaves this box unchecked. This report is not human or independent approval.
