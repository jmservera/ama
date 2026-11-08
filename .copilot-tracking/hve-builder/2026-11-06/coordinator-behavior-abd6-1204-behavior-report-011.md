---
title: Behavior report 011, coordinator admission threshold (issue 1204)
ms.date: 2026-11-06
---

* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md (agent, isolation), blob d471fc61041f9fc73a43564f7bf390a7c7d10cf5 at HEAD 72cfd55e0662f819b98ab7e075e68897611c9711, tree 39d5f274c51e6f4a19af049e3f5edb1cfcdcdcbe. Frontmatter unchanged.
* Run type: bounded admission-threshold correction validation (owner: "fix 1204 and merge"). Reports 009 (Revise) and 010 (simulation Pass, bound to blob acefb44a) are historical, unchanged and not reused as passes.
* Profile: HIGH responsibility inference, not backend identity or native Automatic.
* Attribution (host events, no override, session_inheritance, claude-sonnet-5.5; not backend attestation): executor toolu_01CNFpnMB61eSnfpJ8dRYXCU, grader toolu_01Cpk8E6ZrADWtA1WGU5Lf7V. Designer and static reviewer ran at harness default; per-agent telemetry not separately captured.
* Fidelity: contained simulation. Native Deferred. Execution status Complete (8 admission scenarios, all sub-snapshots). Verdict: **Pass at simulation grade**, 0 target defects, 5 Low, 2 Info.
* Sandbox: .copilot-tracking/sandbox/2026-11-06-coordinator-behavior-010. External verbatim returns: /mnt/ama-gates/g1204-r6-design/.

## Summary

Independent static review of the intermediate blob aa175c95 returned Revise (Medium F1, Low F2 and F3). The final blob applies all three. The scenarios exercise 15, 16 and 20 open PRs with no drain (admitted), a count of 21 (drain entered and recorded, admission barred), an already-entered drain at 20, 16, 15 (clear then admit) and a jump to 9, the eight-assignment cap at 16 PRs, a dependency block, an unvalidated frozen candidate, an unreadable ledger and a failed PR count. The executor invented no outcomes. The earlier independent partial review (1 High, request_changes, partial coverage) is preserved as the genuine adverse origin of this correction.

## Findings

| # | Category | Severity | Summary |
|---|---|---|---|
| 1 | Fixture | Low | N-07 supplies no post-launch readback; executor correctly declined to assert one. |
| 2 | Fixture | Low | N-02 gate facts omit dependency, evidence diff and closing-reference status. |
| 3 | Oracle | Low | N-07 oracle text predates the final unavailable-state wording. |
| 4 | Oracle | Low | N-02 oracle read one merge per tick; target says one PR per merge step. |
| 5 | Target ambiguity | Low | N-08 "admit none and re-read this tick" bars only while the count is unavailable; wording could be tighter. |
| 6 | Executor | Info | Minor skipped re-reads, outcomes unchanged. |
| 7 | Executor | Info | Session name taken from the shared default outcome. |

## Adjudication and qualifications

* The design used the intermediate blob; the lead rechecked expectations against the final blob (run-state.md) and the grader read the final blob. Static review applied to aa175c95, not to the final blob.
* The 11 prior scenario families (sandbox 009) were not re-run; this run adds admission cases only. Their evidence is historical and bound to blob acefb44a.
* Coverage misses (grader): rebuild-from-evidence path, drain write failure, count failure while draining, failed merge gate during drain, two ready issues for one slot, exited-worker slot, more than 20 PRs with a full cap. Reported as residual, no further round taken.
* Admission is not publication; no scenario publishes an unvalidated candidate.

## Fidelity and limitations

Simulation only; live prompts are not proven to carry the edit; the `pr_drain` ledger key is a scenario convention, not a repository schema. Single deterministic trace, no variance testing. Not observed native-host behavior, not human review, not a stronger-profile qualification.

## Containment

Read-only executor; no shell, Git, GitHub, cloud, schedule, publication or cleanup action. Target blob unchanged through execution and grading.

## Human review

* [ ] Human reviewer confirmed this report (not ticked by the author).
