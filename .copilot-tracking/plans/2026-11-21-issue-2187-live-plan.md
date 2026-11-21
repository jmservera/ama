# Plan: issue 2187 heavy lock only for heavy groups

Date 2026-11-21. Task issue-2187-live-20261121T214344Z. Details: `.copilot-tracking/details/2026-11-21-issue-2187-live-details.md`.

## Steps

* [x] Add `needs_heavy_lock(groups)` to `tools/rpi-checks.py`: true for `browser`, `mssql`, `logo-0600` and `image-*`.
* [x] In `main()`, enter `heavy_lock` only when it returns true; otherwise use `contextlib.nullcontext()`. Keep `--lock-timeout` and `--heavy-lock-fd` semantics for heavy runs.
* [x] Add two tests to `tools/test_rpi_checks.py`: selector truth table; `main()` takes the lock once for a heavy selection and not for a focused one.
* [x] Update `src/README.md` local-gate text if it states that every run takes the lock.

## Tier

FULL by classification (gate-tool edit changes gate semantics). Per the brief, run targeted tests only; the coordinator runs the gates. Never `--all`.

## Critique (executed once, final candidate)

* Verdict: accept. Risk: skipping the lock lets a focused run overlap a full gate; project test groups use no Docker, SQL or shared browser, so overlap is safe. Compatible finding applied: keep `browser` heavy because two Chromium classes must not run together (the existing flag comment).
* Finding rejected: dropping the `verify` call under the lock. Verification stays in the same block unchanged.
* No significant or divergent issue needs a user decision.
