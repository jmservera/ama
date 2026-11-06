<!-- markdownlint-disable-file -->
# Behavior report: coordinator idle recovery (issue 1204)

* Date: 2026-11-05
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md
* Scenario design: .copilot-tracking/hve-builder/2026-11-05/coordinator-idle-recovery-1204-behavior-scenarios-001.md (D-1204-1)
* Change class: Major (workflow-rule mutation)

## Summary

* Outcome: Pass (no Critical or High findings). Eight scenarios S1 to S8 each exercised the required behavior; independent grading rated all eight Pass.
* The result is contained simulation evidence, not a runtime guarantee.

## Fidelity and limitations

* Fidelity: simulation, full-file target read. Eight hve-core-all:hve-artifact-tester executors, one per scenario, every command emulated, no files written.
* The target agent has no model field. Executors did not know their model or profile and inherited the session model, so the run is labelled proxy, not confirmed on the target profile. A higher-tier model can repair ambiguity a lower tier would expose.
* Executors S5 and S8 read the target in parts; S7 did not read the retention policy. The scenario S6 brief path is scenario input.
* The test log was written by the parent lead from the executor traces; traces themselves are not committed.
* Authoring was done by the parent lead, not a separate authoring subagent. Static review and grading were independent generic subagents.

## Reuse eligibility

* Not reusable for any later edit of the target; rerun after any further change to the agent file.

## Findings

| ID | Severity | Scenario | Finding |
| --- | --- | --- | --- |
| B1 | Medium | S5, S7 | A full-tier receipt needs the exact current base while step 8 forbids a gratuitous rebase of a green head. The text does not say how a published head is gated or what happens if base verification fails. |
| B2 | Medium | S7 | Who approves a cleanup manifest, and whether step 10 post-merge worktree removal is covered by the manifest contract, is not stated. |
| B3 | Medium | S3 | Not stated whether repair sessions count toward the eight-session limit, whether the open-PR count is re-read mid-tick, and whether auto-merge-queued PRs count against the cap. |
| B4 | Low | S2, S4 | tmux installation authority, closure queue rotation order, backlog-sync --apply ordering, choice among several owner questions, live-sending tier, spend tracking. |
| B5 | Low | S1, S3, S6, S7, S8 | Blocker-comment detection, branch type, flaky-job rerun wording, brief timestamp format, manage_schedule syntax, disk-pressure rule. |

B1 to B5 are routed to follow-up work and not fixed in this change to keep it surgical.

## Coverage

| Scenario | Required case | Grade |
| --- | --- | --- |
| S1 | Blocked PR plus ready independent issue | Pass |
| S2 | 99 pending closure reviews, no tmux | Pass |
| S3 | 21 PR drain versus 15 and eight-session admission | Pass |
| S4 | Granted approval versus unavailable owner | Pass |
| S5 | Full gate missing despite green CI | Pass |
| S6 | Stale main-target brief versus parent stack | Pass |
| S7 | Cleanup with active receipt or unknown upstream | Pass |
| S8 | Reliable schedule replacement | Pass |

## Containment

* Executors read only the agent file and their scenario section, no network mutation, no paid inference beyond the subagent runs themselves, no native deployment, no uncontained execution.
* Post-run workspace status delta: only the owned sandbox folder, now removed. Source and evidence files otherwise unchanged by executors.

## Satisfied-and-skipped

* None.

## Human review

- [ ] Human review of this behavior evidence is pending.
