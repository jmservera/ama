<!-- markdownlint-disable-file -->
# Review: issue 1288 H1 restart-context diagnostic

Readback `date -u` 2026-11-09T23:39Z. One review of the finished (blocked) task. Refs #1288 only.

## Outcome

| Item | Status |
| --- | --- |
| Prospective research, plan, details, one critique before observation | Done and committed (`bf94ac0ba`) |
| H1 SQL observation | Not executed: heavy lock held by issue-1238 SQL run; one non-queued attempt, exit 1 |
| H0 (original) | Failed-inconclusive, unchanged |
| Hypothesis (missing release/provider context in the second service) | Source-supported, unobserved; not a defect claim and not a pass |

## Findings

1. Blocker: external, occupied heavy resource. Owner: the issue-1238 verifier until its run ends. Resolution: run the unexecuted step in the changes record.
2. The persistence contract for fresh-service equality stays unproven at the merged source until H1 runs.
3. No E12 consumption, no fabricated defect classification, no source fix.

Whole #1288, #440 and the live-model criteria remain open.
