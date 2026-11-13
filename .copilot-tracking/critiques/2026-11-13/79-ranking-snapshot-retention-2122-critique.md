# Critique: #79 criterion 4 plan

Date: 2026-11-13. One independent pass (rubber-duck, read-only) on the research and plan. Verdict: proceed with changes. Not repeated.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | An unchanged snapshot keeps its original publication date, so a daily green run could mask a stale source | Accepted. The job exits 1 with `RANKING_PUBLISH_ALERT` when the runner reports `source_current` false (data `as_of` is not the run date), after the record is written. Test: consecutive days with unchanged `as_of` |
| PC-002 | Store adapter contract underspecified | Accepted. Read `store.cases` and `store.as_of` under `store.lock`, deep-copy, keep only boolean `closed` false, refuse a non-boolean. Test with real `Store` open and closed cases |
| PC-003 | "One PUT" assertion contradicts the adapter | Accepted. Assert one stored blob with unchanged bytes and `already_published` on the repeat, not one PUT request |
| PC-004 | Conditional job gating and existing compiled-template tests | Accepted. Job needs `deployWorkloads`, `deployBackgroundWorkloads` and a non-empty `rankingArchiveContainer`; test enabled and disabled; update existing tests that count jobs |
| PC-005 | A log marker alone is not an alert | Partly accepted. The job name is added to `operationalMonitoring` `jobNames` (job-failure alert) when the ranking archive is enabled; the exit is non-zero on every non-success. A log-query missing-run alert is recorded as a follow-up |
| PC-006 | Tests do not prove live retained publication | Accepted. Docs state configured capability only; criterion 3 (signed policy) and approved, locked retention stay open |
| Gates | New orchestrator code must satisfy ruff and strict mypy and import only core and orchestrator | Accepted |
