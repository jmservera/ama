---
title: Issue 79 r28 plan
ms.date: 2026-11-07
---

* Phase 1 (RED first, before any source edit): add core regressions for the existing-record path (first sync fails; retry with continued failure raises `DurabilityUnconfirmedError` and keeps the record and original date; retry after recovery returns `written: false`) and the race loser, plus a runner regression for the distinct outcome. Run them on the unfixed source and keep the output.
* Phase 2 helper: add `_confirmed` (folder sync for every outcome, typed error, `stage_retained` carried) as in the child; the existing-name early return and `FileExistsError` path go through it. Keep the immutable publication date, owner-only mode, non-throwing own-stage cleanup and root `.publishing-` stage.
* Phase 3 runner: catch `DurabilityUnconfirmedError` before `OSError`; return status `committed_unconfirmed`, refusal-free but with an `uncertainty` entry (code `committed_unconfirmed`, path-free message, safe next action to check the archive and rerun to confirm, optional `stage_retained`), `written: false`, the record path and date, and a non-success CLI exit 2. Ordinary failures remain `publish_failed`.
* Phase 4: light core, runner, API wiring, ruff, format, mypy; README sentence; changes, author Review, state, one new log entry. No FULL, SQL, browser or child change.

## Critique (author, one pass, not independent)

* Syncing on retry makes an unrecoverable directory failure repeat the uncertainty audit on each retry; accepted, as it is the honest state.
* Choosing the runner status: reuse exit 2 (non-success) and a distinct status so it is not read as a no-write refusal; unknown callers treating unknown statuses as success are none in the repo (checked by grep in implementation).
* Disposition: proceed; any needed behaviour beyond this is a blocker.
