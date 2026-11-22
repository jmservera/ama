---
title: Issue 2237 research (in progress)
---

Research disposition: executed. Planning Readiness: Ready.

Full findings, commands and the per-criterion table: [research note](../../docs/reference/research/issue-2237-retention-500-live-2026-11-22.md).

* The handler catches only PermissionError; other exceptions give a logged 500 (`_unhandled`).
* Container logs hold only the current replica (started 11:20:59 UTC, after the failure); Log Analytics and Application Insights refuse queries (NSP or insufficient access).
* Live GET /api/retention: 200 in 55 of 55 calls on revision 0000047.
* Follow-up: capture the `http-error` log line on the next occurrence.
* Second pass: revision 0000050 re-probe all 200; local malformed-shape table added; no src change.
