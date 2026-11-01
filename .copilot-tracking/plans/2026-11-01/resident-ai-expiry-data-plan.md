# Plan: resident AI expiry as data (issue 624)

* [x] Add idempotent `expires_at` column (default 2026-11-01T00:00:00) and read it in `reserve` under the budget lock.
* [x] SQL tests: setUp sets a far-future expiry; add refusal-after-expiry, default and re-apply-keeps-extension tests.
* [x] Document read/extend in `infra/README.md`; Python `EXPIRES` unchanged and documented.
* [x] Validate: unit and SQL tests, ruff check, ruff format --check, mypy.

Critique (single pass, self-applied): refusal must not consume budget (asserted); re-apply must not reset an extension (tested); missing budget row still refuses (`@spent IS NULL`).
