# Research: C1 ranking publication review fixes (#79)

Date: 2026-11-13. Disposition: reused (independent review `79-ranking-ret-review-2315-review.md`, candidate 7fe6e08e6). Planning Readiness: Ready.

## Evidence
* Blocking: `infra/tests/test_bicep_policy.py:1469` was a 124-character line; CI runs `ruff format --isolated --line-length 100 --check` on it (`.github/workflows/src-ci.yml:244`). CI lint also runs `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`.
* Low: `ranking_publish.open_cases` reads `store.lock`, `store.cases`, `store.as_of`. `SqlStore` exposes these, and `factory.open_store` picks it with `ZF_STORE=sqlite|mssql`. Only the JSON `Store` was tested. `MssqlStore` needs Azure SQL and is not testable offline; the SQLite `SqlStore` is its base class.
* Info: no details artifact; add one.

## Scope
Test and formatting only; no production code change. Criteria 3 and 4 of #79 stay open (`Refs #79`).
