# Details: issue 1204 tick_log checker (2026-11-19)

Row fields: tick, utc, counts (ready, running, unassessed, human_blocked, dependency_blocked),
action, evidence, recovery, closure_batch, approvals_granted, approvals_expired, reclassified,
global_stop. Rules: R1 action+evidence else no-progress; R2 tick after two no-progress with
ready/unassessed work needs recovery; R3 no-progress with ready work and free capacity (<8
running) is a violation; R4 closure batch at most 5 and no repeats; R5 expired approval returns
only its own tasks to human-blocked, granted one makes them ready; R6 global_stop with
ready/unassessed work is a violation. CLI: path, exit 1 on violations.
