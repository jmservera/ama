# Research: issue 183 sensor backfill generator

* Disposition: executed. Planning Readiness: Ready.
* Issue #183 (parent #177): same seed gives same output, series carry stock home and sensor IDs, estimate volume and size before generation, load reuses the #110 validation contract.
* Evidence: no sensor code existed in mvp/. Stock IDs come from `mvp/zavaforward_mvp/scale_fixture.py` (60,000 homes, `ZF-NNNNN`). #110 and #178 to #182 are unmerged siblings, so the contract is mirrored, not imported.
* Owner constraints: ADR 0005 synthetic labelled data only; Azure SQL target; local tests use stdlib sqlite only.
* Unverifiable: Met Office and Environment Agency open data retrieval (open item; synthetic climate labelled in manifest).

## Follow-up research (PR #272 review fixes)

* Finding 1: `INSERT OR IGNORE` is SQLite-only; `INSERT ... SELECT ... WHERE NOT EXISTS` with `?` placeholders runs on SQLite and Azure SQL (T-SQL permits FROM-less SELECT).
* Finding 2: #110 (IoT Hub ingestion into Azure SQL) is still open and no validation contract exists in the repository, so there is nothing to reuse; recorded as an open item in the PR body.
* Finding 3: volume estimate stored as [issue-183-volume-estimate.json](issue-183-volume-estimate.json) (60,000 homes, 1,048,263,000 rows, about 118.13 GiB CSV).
