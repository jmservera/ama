---
title: Issue 2243 changes r3
ms.date: 2026-11-23
---

Status: complete. Classification: FULL (src change); no `rpi-checks.py` run, the coordinator runs gates.

## Changes

* `src/api/src/zava_forward/api/resident_demo/aoai.py`: `_reason` classifies HTTP 429 as `provider_busy` and other HTTP/URL/timeout errors as `provider_unavailable`; `_fallback` logs the exception class name.
* `src/api/tests/test_resident_aoai.py`: `test_provider_throttle_and_outage_are_named_not_unverified`.
* `docs/reference/research/issue-2243-live-r3-2026-11-23.md` (+ probe folder), index entry and log entry.

## Validation

`test_resident_aoai` and `test_resident_demo_api`: 71 OK; `python3 -m mypy` clean; ruff check and format clean. Hosted CI not observed (no push).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven |
| Add a test | Proven |
| Rebuild and roll the resident image | Unproven for this fix (registry firewalled, not deployed) |
| Resident chat answers with the model within caps | Partly proven (document path model-backed); free-text path not re-observed; deployment capacity 1 (1 request/min) is the cause of the generic label and needs an owner capacity change |
