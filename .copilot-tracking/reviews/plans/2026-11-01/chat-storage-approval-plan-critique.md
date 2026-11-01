<!-- markdownlint-disable-file -->
# Plan critique: Chat storage approval (one pass)

Execution: completed once, 2026-11-01. Verdict: Revise (applied).

* C1 Concern: resident demo and agents apps do not use ChatPrivacy, so env there is inert and "resident chat stores a thread" is unachievable. Disposition: applied; resident template wired as asked (harmless), agents unchanged, live verification records that resident chat cannot store.
* C2 Concern: an env that is empty or partial must not enable partial settings. Disposition: applied; api env only when all four refs are set, defaults empty, tested.
* C3 Concern: object parameters break the repo's ARM evaluator tests. Disposition: applied; scalar parameters.
* C4 Concern: two employee apps exist. Disposition: apply live only to `ca-cutover-test-demo-api` (the employee demo site); `ca-cutover-test-api` is left unchanged and reported.
* C5 Concern: decision text must not claim production approval. Disposition: applied in record, README, log.
