---
title: Issue 1274 live changes (2026-11-27)
---

## Planned changes

* tools/install-actionlint.py: retry on `http.client.HTTPException` (IncompleteRead, BadStatusLine).
* tools/test_install_actionlint.py: regression for IncompleteRead retry and exhaustion.

Tier: focused (no src, no workflow change).

## Implemented

* `fetch()` now also retries on `http.client.HTTPException`, so IncompleteRead/BadStatusLine no longer escape unretried; the next attempt or official source is tried and exhaustion still raises InstallError.
* New test `test_incomplete_read_is_retried_then_exhausts_fail_closed`.

## Proof

* Before: repro printed `ESCAPED: IncompleteRead`; with the installer change stashed, the suite shows FAILED (errors=1). After: `python3 -m unittest tools.test_install_actionlint` 15 tests OK; `tools.test_rpi_checks` 134 OK; ruff (CI rules E,F,I,B,UP) and `mypy --strict` clean; format check clean.
* No workflow file changed, so WORKFLOW_HASHES is unchanged. No Azure, no credentials, no push. Tier: focused.

## Per-criterion table

| Criterion | Verdict |
| --- | --- |
| 1 exact failing endpoints for #1243/#1271/#1273 | Unproven: actionlint endpoint proven in earlier notes (run 4); AWF 0.28.23 and #1273 logs not retained, AWF bootstrap is upstream-owned |
| 2 bounded fail-closed retrieval | Proven; hardened here for non-OSError transport faults |
| 3 focused regressions | Proven (15 tests OK, new IncompleteRead case) |
| 4 real checksum verification and hosted CI on reviewed exact head | Unproven: actionlint 1.7.7 digest verified in earlier run 4; hosted CI needs a push, which is forbidden here |
| 5 resume route | Proven (merged #1275) |
