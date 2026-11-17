---
title: Bicep container hosting changes
ms.date: 2026-11-14
---

* Added 5 tests (image parameterization, placeholder confined to 4 bootstrap sites, probe timing bounds, queue-worker scale caps).
* Validation: new module 16 tests OK; az bicep build exit 0; ruff isolated clean on the file; full infra discover 601 tests, 1 pre-existing error (test_ledger_alert_queries_match_the_verifier_markers) identical on baseline.
* Bare repo-wide ruff reports pre-existing findings; bare python3 -m mypy has no configured target (usage error, pre-existing). Not run for acceptance of #144 criteria.
