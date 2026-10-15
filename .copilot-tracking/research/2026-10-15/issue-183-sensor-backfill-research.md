# Research: issue 183 sensor backfill generator

* Disposition: executed. Planning Readiness: Ready.
* Issue #183 (parent #177): same seed gives same output, series carry stock home and sensor IDs, estimate volume and size before generation, load reuses the #110 validation contract.
* Evidence: no sensor code existed in mvp/. Stock IDs come from `mvp/zavaforward_mvp/scale_fixture.py` (60,000 homes, `ZF-NNNNN`). #110 and #178 to #182 are unmerged siblings, so the contract is mirrored, not imported.
* Owner constraints: ADR 0005 synthetic labelled data only; Azure SQL target; local tests use stdlib sqlite only.
* Unverifiable: Met Office and Environment Agency open data retrieval (open item; synthetic climate labelled in manifest).
