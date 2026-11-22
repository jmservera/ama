---
title: Issue 2201 live5 changes, 2026-11-22
---

Refs #2201. Tier: focused (documentation only; no `src/` change; no gate run; nothing pushed). Azure read only; no resource created, none to delete; the job was not changed.

## Changes

* Added `docs/reference/research/issue-2201-live-receiver-logs-2026-11-22.md`.
* Index entry in `docs/reference/README.md`; log entry in `docs/reference/log.md`.
* Evidence under `.copilot-tracking/evidence/2026-11-22/issue-2201-live5/`.

## Validation

* Log Analytics queries and execution lists recorded; links checked by path; `git diff` reviewed.

## Per-criterion table

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Root cause recorded with evidence (logs, exit code) | Proven for SQL failures and the 11:32 argument error; unproven for 13:30 | Console text; exit codes not logged; `IOT_CALLBACK_FAILED` has no exception detail |
| Fix merged and deployed | Proven for #2231 and #2234 by earlier notes | No change here |
| Three consecutive scheduled runs Succeeded | Unproven now | 14:00 and 14:30 Succeeded; 15:00 pending |
| Readings from IoT Hub in the store and the employee map, with timestamps | Not re-probed | `receipts=1037` at 14:00 run; map freshness not shown |
