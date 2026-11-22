---
title: Issue 2237 changes
---

Tier: focused. No `src/` change, so no security, identity or SQL surface is touched; local tests, ruff and mypy are not applicable. Refs #2237.

## Files

* `docs/reference/research/issue-2237-retention-500-live-2026-11-22.md` (new) and its folder with `live_probe.py`, `before.json`, `after-burst.json`.
* `docs/reference/README.md` (index row), `docs/reference/log.md` (entry).

## Live actions

Read-only: container log reads, failed log and Application Insights queries, and 55 GET calls to `/api/retention` plus 20 to `/api/cases` (first pass, revision 0000047) and the same burst again on revision 0000050 (second pass, `rerun-2026-11-22T16.json`) signed in as the demo employee. No Azure resource was created, changed or needs deletion.

## Divergence

The goal expected a fix; none was made because the failure class could not be recovered (see the research note).

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce | Unproven | 55 of 55 calls returned 200 on revision 0000047 and again on 0000050; a local malformed-record table shows plausible failure classes but none is tied to live data |
| Find the cause in the demo container logs | Unproven | Failing replica gone; Log Analytics and Application Insights refuse queries from this host (NSP, access); network change not authorised |
| Fix with a regression test | Not applicable | No cause established; speculative fix rejected in the critique |
| Re-prove 200 live | Proven for the demo account on revision 0000047 (role at probe time not re-read) | `before.json`, `after-burst.json` |
