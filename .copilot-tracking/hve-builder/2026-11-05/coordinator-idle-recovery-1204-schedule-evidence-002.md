<!-- markdownlint-disable-file -->
# Schedule evidence: coordinator idle recovery (issue 1204)

* Date: 2026-11-05
* Provenance: supplied by the coordinator from its live `manage_schedule` create, list and stop results. It is tool evidence passed to this worker, not runtime validation performed by this worker, and it is historical as of 2026-11-05.
* Sources read (known evidence, read only): session files schedule-recovery-review.md, delivery-schedule-v2.txt and cleanup-schedule-v2.txt under /home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/.

## Identities

| Schedule | Interval | State | Role |
| --- | --- | --- | --- |
| #9 | every 10 minutes | active (final) | delivery, replaces intermediate #7 |
| #8 | every hour | active (final) | cleanup, replaces #2 |
| #7 | every 10 minutes | stopped (intermediate) | delivery, replaced #6, later replaced by #9 |
| #6 | every 10 minutes | stopped (original) | delivery |
| #2 | every hour | stopped (original) | cleanup |

The coordinator's live list confirmed exactly one active delivery (#9) and one active cleanup (#8). The earlier statement that #7 was the active delivery recurrence, which appears in the original ef585f5 evidence and its final report, is superseded and kept as a historical record.

## Prompt versions

* delivery v2 and cleanup v2: approved snapshots in the session files above (read only, not edited).
* Live prompts are condensed semantic equivalents of those snapshots, not byte-identical copies. Runtime schedule #9 additionally carries the dependency-on-running-work correction (a dependency on an identified running predecessor permits ending the tick, not stopping the schedule or completing the run).
* An independent schedule-contract review returned Revise for that one High finding; a targeted closure returned Pass for that finding only. Neither performed native execution or behavior simulation (from the supplied recovery review).

## Limits

* Scheduling is an advisory model workflow, not technical enforcement of progress or guaranteed delivery.
* No deployment, role grant, capacity change, approval relaxation or historical deletion occurred as part of this instruction repair.
* Live readback after 2026-11-05 is coordinator-managed and not asserted here.
