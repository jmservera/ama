---
title: Issue 132 round 2 changes
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/procurement.py`, `projection.py`
* `src/api/src/zava_forward/api/server.py`, `src/api/README.md`
* `src/api/tests/test_procurement_api.py`: `test_job_pack_is_staff_read_only_and_leaks_no_resident_reason`

Validation run: API `test_procurement_api` (36 OK); core `test_job_pack` and `test_quality_procurement` (120 OK); ruff check and format on changed files; mypy (cache /tmp/mypy-132) clean for procurement, projection and server.
Not run: gate, benchmarks, full suites, browser or accessibility checks, hosted CI. No divergences or amendments.
