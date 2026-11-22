# Changes: issue 2244 live re-verification on revision 0000054

Status: implemented. No source change; focused tier (documentation and evidence only). rpi-checks not run; hosted CI not observed (nothing pushed).

## Files

* docs/reference/research/issue-2244-live-r54-2026-11-22.md (new) and issue-2244-live-r54-2026-11-22/live-probe.txt (new): live evidence.
* docs/reference/README.md, docs/reference/log.md: index and log entries.

## Validation

* Live probes recorded in the note; no secrets printed (probe file scanned for password, secret, key: 0 matches).
* Links reviewed by diff. No Azure resource was created or changed.

## Per-criterion table

The issue has no acceptance checkboxes; criteria come from the goal and issue text.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Revision 0000054 runs healthy, no crash loop | Proven | Healthy/Running, replica restartCount 0 for 33 min |
| Fixed code is in the running container | Proven | exec grep of startup_retries returned 4; commit-to-digest mapping unproven (registry firewalled) |
| No restarts across a fresh start | Proven (one sample) | second replica started clean, restartCount 0 |
| API responds | Proven | 13 healthz probes, all 200 |
| Start-up survives a held write lock | Unproven | needs a held-lock drill; owner excluded drills |
| Lock holder of 13:42 incident | Unproven | Log Analytics unreadable |
| Read-only schema check before lock | Unproven | not implemented; routed follow-up |

Issue 2244 stays open. Unrelated finding: runtime ProgrammingError on POST /api/chat/threads at 23:35:34Z needs separate triage.
