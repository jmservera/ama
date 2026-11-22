# Research: issue 2191 half of homes fresh, live re-verification (2026-11-22)

Research disposition: executed (opening). Prior evidence reused: `docs/reference/research/issue-2191-live-sql-capacity-2026-11-22.md` (S0 to S3, 15 of 16 samples at or above 50 percent) and `issue-2191-live-readings-2026-11-22.md` (110 of 441 baseline).

## Findings so far

* Baseline 110 of 441 (24.9 percent) predates the SQL tier change; cause was DTU saturation at S0, not batching or the receiver window.
* At 18:30 UTC SQL is still Standard capacity 100 (S3), online. Simulator cron `0,7,15,22,30,37,45,52 * * * *`; receiver `*/30 * * * *` with `--seconds 1500`.
* Open question: does coverage hold hours later, and is S3 the smallest sufficient cause? Measure with a throwaway read-only sampler job.

Planning Readiness: Ready.
