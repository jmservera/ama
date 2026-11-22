---
title: Issue 2201 live4 changes, 2026-11-22
---

Refs #2201. Tier: focused. No `src/` change; no gate run; nothing pushed.

## Changes

* Added `docs/reference/research/issue-2201-live-receiver-recheck-2026-11-22.md`.
* Index entry in `docs/reference/README.md`; log entry in `docs/reference/log.md`.
* Evidence under `.copilot-tracking/evidence/2026-11-22/issue-2201-live4/`.
* Azure: read only. No resource created, so no cleanup. No workspace, registry or job change.

## Validation

* Executions read twice (13:40, 13:55 UTC); map and case readings probed with Playwright; Log Analytics query refused (recorded).
* Links in the note checked by path; `git diff` reviewed.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Unproven for runs since 10:34 | Logs and exit codes unreachable (workspace network refusal; no replica); earlier causes stand |
| Fix merged and deployed | Proven for #2231 and #2234 | Job and API revision 47 share digest 541068; batch change unmerged |
| Three consecutive scheduled runs Succeeded | Partly proven | 12:00 (shortened window), 12:30, 13:00 Succeeded; 13:30 Failed, so no current streak |
| Readings from IoT Hub in the store and the employee map, with timestamps | Proven for the demo, stale tail | Map 200, 443 items; readings to 13:35:00Z; freshness stale after the 13:30 failure |
