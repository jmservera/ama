# Plan: issue 2254 run 5 (2026-11-23)

Details: [details](../details/2026-11-23-issue-2254-live-r5-details.md)

* [ ] Phase 1: add over-count regression `test_overcounted_safety_column_...` to src/core/tests/test_sqlreads.py.
* [ ] Phase 2: prove it fails with the hazard repair reverted and passes restored; run the module and ruff.
* [ ] Phase 3: record live probe r5 and the per-criterion table; update the index and log.
* [ ] Phase 1: add `support`, `days`, `fstatus` to `cols` in `SqlStore._repair_identity_columns`.
* [ ] Phase 2: add a regression test in `src/core/tests/test_sqlreads.py` that stales those columns and compares `page_cases` flag totals with body counts; confirm it fails with the change reverted.
* [ ] Phase 3: run `test_sqlreads`, mypy and ruff in `src/core`; write the research note under docs/reference/research/, index line and log entry.
