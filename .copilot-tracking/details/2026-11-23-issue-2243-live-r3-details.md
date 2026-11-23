---
title: Issue 2243 details r3
ms.date: 2026-11-23
---

Phase 1: edit `FALLBACK_REASONS` (add `provider_busy`, `provider_unavailable`) and `_fallback` (classification by `urllib.error.HTTPError.code`, `URLError`, `TimeoutError`; log `error=<class>`).
Phase 2: add `test_provider_throttle_and_outage_are_named_not_unverified` using the existing `transport` mock.
Phase 3: run `test_resident_aoai`, `test_resident_demo_api`, mypy, ruff; record.
