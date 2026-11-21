# Changes: issue 2187

Date 2026-11-21. Tier FULL by classification (gate-tool edit); targeted tests only, no `rpi-checks.py --all` (the coordinator runs gates).

## Files

* `tools/rpi-checks.py`: new `needs_heavy_lock(groups)`; `main()` takes `heavy_lock` only when a `browser`, `mssql`, `logo-0600` or `image-*` group is selected, otherwise `contextlib.nullcontext()`.
* `tools/test_rpi_checks.py`: two tests (selector truth table; `main()` lock call count 0 for `project-core`, 1 for `static`+`image-api`).
* `src/README.md`: local-gate text states the lock is taken only for browser, SQL or image groups.

## Validation

* 4 unittest cases (the 2 new plus 2 existing lock tests): OK.
* `ruff format --isolated --line-length 100 --check`: clean. `ruff check`: 20 findings, identical count on unmodified main (pre-existing).

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Lock only when a heavy group is selected | Proven locally | `test_main_skips_lock_without_heavy_group_and_takes_it_with_one` plus selector test |
| Test | Proven locally | the two new tests pass |
| Behaviour under a live competing full gate | Unproven | not run: the brief forbids a full gate here; the unit test patches `heavy_lock` and shows it is not entered |
| Live Azure, browser, credentials | Not applicable | local gate tool, no web or Azure change |

Browser stays classed as heavy (conservative); the issue text names Docker and SQL only, recorded as a follow-up decision. Full-tier receipt, hosted CI and independent review remain with the coordinator.
