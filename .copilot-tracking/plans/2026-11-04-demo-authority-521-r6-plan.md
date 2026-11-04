# Plan: demo authority 521 r6 (2026-11-04)

Slice 1 (this PR): record the live state check and the source/live difference; no source or Azure change.

* [x] Read-only live metadata check.
* [x] Add live state section to `infra/README.md` and log entry.
* [x] Run focused resident core tests, ruff and mypy.

Critique (in-plan, once): advice to revert source to 2027-02-01 conflicts with the merged owner decision of 2026-11-03 and was rejected. Advice to apply 2028-01-01 live was rejected because the confirmation covers only 2027-02-01.

Stacked slice 2 (not started): owner confirms 2028-01-01 live move (SQL constraint, row renewals, app redeploy, cost headroom), then apply and verify. Touches SQL and deployment, so the full gate applies and is run by the coordinator.
