---
title: Issue 151 telemetry consent plan
ms.date: 2026-11-14
---

## Plan

* [x] Add `src/core/.../telemetry_consent.py` with the notice and `withdraw` over the trusted consumer seam.
* [x] Add `tests/test_telemetry_consent.py`: notice fields, admission halt, downstream flag, other homes unchanged, unknown home refused, cases unchanged.
* [x] Run ruff check, ruff format check (line length 100) and focused unit tests.

## Critique

One pass, self-applied: reuse existing consent enforcement instead of a new store; no API or UI changes in this slice.
