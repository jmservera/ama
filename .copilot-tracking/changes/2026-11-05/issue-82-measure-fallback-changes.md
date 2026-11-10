---
title: Issue 82 non-string measure fallback changes (2026-11-05, correction 3)
ms.date: 2026-11-05
---

* `src/core/src/zava_forward/core/quality.py`: `evidence_gaps` returns None (Unknown) when the checklist name is not a known checklist and `measure` is neither None nor a string. The measure fallback is otherwise unchanged.
* `src/core/tests/test_quality_procurement.py`: three shared `Flows` tests (inherited by JsonFlows, SqlFlows and MssqlProcurement): non-string measure with unrecognised checklist raises `GateError` and leaves the record unchanged; known checklist ignores a non-string measure; `measure=None` keeps the legacy General fallback.
* RED (before the guard): JsonFlows and SqlFlows, 6 tests, 2 errors `AttributeError: 'list' object has no attribute 'lower'`, unittest exit 1, 4 controls passed. Log /tmp/ama82-measure-red.log.
* GREEN: test_gates, JsonFlows, SqlFlows, HandoverBlockersTest, JsonHazardReferral, SqlHazardReferral: 183 tests OK, 1 skip, exit 0. ruff check 0, ruff format --check 0 (213 files), mypy 0 (266 files), all with external caches.
* No replacement route is added for a non-string measure; measure identity is not repaired, coerced or reassigned.
