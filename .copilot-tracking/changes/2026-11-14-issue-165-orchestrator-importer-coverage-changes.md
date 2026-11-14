---
title: Issue 165 coverage changes
ms.date: 2026-11-14
---

* Added `src/orchestrator/tests/test_job_boundaries.py` (16 tests).
* Added `src/importer/tests/test_cli_and_privacy_boundaries.py` (22 tests).
* Coverage: orchestrator 89% to 91%, importer 84% to 94%.
* Validation: ruff check and format, mypy, both unit suites (131 and 107 tests) and `test_scenario_manifest.py` passed locally. Hosted CI not run; not pushed.
* Tier: focused (test-only, no gate, workflow or dependency change).
