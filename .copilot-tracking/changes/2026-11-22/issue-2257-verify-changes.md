---
title: Issue 2257 verify changes
ms.date: 2026-11-22
---

Status: complete. No `src` change, so the focused tier applies (basis: test, documentation and evidence only; no workflow, dependency, Dockerfile or security-control edit). `rpi-checks.py --all` was not run. No Azure resource was created or changed; credentials were read at runtime only.

## Changes

* `src/api/tests/test_workspace_scripts.py`: added `test_map_read_recovers_from_a_dropped_connection`. It runs the real `api()` and `fetchReadRetrying` against `/api/map?zoom=5` in Node's VM, asserts a first `Failed to fetch` is retried and the data returned, that retries stay bounded, and that the map draw reads through `api()`. Mutation check: replacing `fetchReadRetrying` with `fetch` in `api()` makes it fail; the file was restored.
* [docs/reference/research/issue-2257-verify-live-2026-11-22.md](../../../docs/reference/research/issue-2257-verify-live-2026-11-22.md) with scripts and results in `issue-2257-verify-live-2026-11-22/`; index and log updated.

## Validation

* `python3 -m unittest tests.test_workspace_scripts` in `src/api`: 11 tests OK.
* `ruff check`, `ruff format --isolated --line-length 100 --check` on the test file: clean. `python3 -m mypy` in `src/api`: no issues in 371 files.
* Live (revision 0000053): injected reset on the first `/api/map` recovered with 443 markers; 8 of 8 fresh sign-ins loaded 443 markers.
* Hosted CI was not observed; nothing was pushed.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Main already fixes the failure | Proven for the client: #2261 `fetchReadRetrying` is on main and deployed on revision 0000053 | live recovery proof, source |
| The map retries or recovers without a reload | Proven (live injected reset on the deployed demo, plus the new regression test) | recovery-proof-result.json, test |
| Regression test added | Proven | new test, mutation check |
| The cause is found | Unproven at request level; replica scale-in and probe timeouts coincide with the window (inference) | earlier note's system-log correlation |
| Spontaneous failure rate on fresh sign-in is now zero | Not proven: 0 of 8 failed, but the original 3 of 8 cannot be forced without replica churn | probe-result-230459.json |
