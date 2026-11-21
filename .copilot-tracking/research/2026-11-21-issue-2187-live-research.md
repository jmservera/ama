# Research: issue 2187, skip the heavy lock for focused runs

Task: issue-2187-live-20261121T214344Z. Date 2026-11-21. Disposition: executed. Planning Readiness: Ready.

## Issue

Title: Gate: do not take the heavy lock for focused runs without Docker or SQL groups. Body: `rpi-checks --changed` waits on `/tmp/ama-rpi-heavy.lock` even when no Docker/SQL group is selected. Skip the lock then. Criteria: (1) lock only when a heavy group is selected; (2) test.

## Evidence (observed on main dd8df9631a)

* `tools/rpi-checks.py` `main()` wraps every run in `with heavy_lock(args.lock_timeout, args.heavy_lock_fd):`, so a `--changed` run selecting only `project-*`, `static` or `infra` still queues behind a full gate. Criterion 1 is currently unmet.
* Groups that use Docker or SQL: `mssql`, `image-*`, `logo-0600` (dispatch under `docker_lock`, lines 2959 onward). The `browser` group runs Chromium and the shared-lock comment at `HEAVY_LOCK_HELD_FLAG` says two browser classes must not overlap, so it is treated as heavy too (conservative; named in the criterion only as an implicit resource).
* `preflight` runs `docker version`, a read-only client call, not a heavy resource.
* No test covered lock selection (`grep heavy_lock tools/test_rpi_checks.py`: only lock mechanics and the long-browser-output rejection).
* Earlier local branches carry similar fixes (`1f66e943cd`, `d51d14571f`) but neither is in `main`; this task re-implements on current main.

## Acceptance criteria and demo proof status

| Criterion | Provable for the demo | Method |
| --- | --- | --- |
| Lock only when a heavy group is selected | Yes, locally | Unit test on a selector function and on `main()` lock call count |
| Test | Yes, locally | New tests in `tools/test_rpi_checks.py` |

Live Azure, Playwright and credentials are irrelevant: this is a local gate tool and no web or Azure behaviour changes.
