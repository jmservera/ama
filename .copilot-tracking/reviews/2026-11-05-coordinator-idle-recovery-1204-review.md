<!-- markdownlint-disable-file -->
# Review: coordinator idle recovery (issue 1204)

* Date: 2026-11-05
* Execution: executed once, after implementation
* Outcome: Conformant for the instruction change; live-schedule criterion and human review remain outside this worker
* Assessed boundary: .github/agents/ama-backlog-delivery-coordinator.agent.md plus dated evidence on branch fix/coordinator-idle-recovery-1204
* Evidence: .copilot-tracking/changes/2026-11-05-coordinator-idle-recovery-1204-changes.md, .copilot-tracking/hve-builder/2026-11-05/coordinator-idle-recovery-1204-review-001.md, .copilot-tracking/hve-builder/2026-11-05/coordinator-idle-recovery-1204-behavior-report-001.md

## Acceptance criteria

| Criterion | Verdict |
| --- | --- |
| Liveness and stop decision from fresh classification; unknown is work | Met (static review, S1, S2) |
| Each tick advances real work, five-item closure batches with SQL cursor, recovery after two no-progress ticks | Met (S2, S3) |
| Owner questions one at a time, approvals persisted and routed | Met (S4) |
| Limits, stacks, tiers, human boundaries preserved; no gratuitous rebase | Met (S3, S5, S6) |
| Fresh briefs with explicit target; workers cannot publish; cleanup finite and verified | Met (S6, S7) |
| Schedule replacement documented; live schedules replaced and read back | Documentation met (S8). Live schedules #7 and #8 are coordinator-managed and were not verified here |

## Findings routed to later work

* B1 to B3 (Medium) and B4, B5 (Low) from the behavior report, plus static F6 and F7 (Low).

## Not claimed

* No runtime guarantee, no human review, no hosted CI, no independent exact-head assessment. Publication belongs to the coordinator.
* Closing keyword: use `Refs #1204` until the coordinator confirms the live schedule readback.
