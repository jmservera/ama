---
title: Per-user chat epic (#157) case scoping at thread creation, 2026-11-23
description: Core-layer gap found and fixed in ChatPrivacy.start_thread, with a per-criterion verdict for the epic
author: AMA programme
ms.date: 2026-11-23
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Local code and tests only; no Azure resource was touched, no credential was read.

## Finding

The API route `POST /threads` checks `store.detail(case_id, user)` before creating a thread, but the core service `ChatPrivacy.start_thread` did not. A core caller could bind a thread to a case its role cannot see, and a missing case raised `ValueError` while a hidden case did not, which let a caller tell the two apart. Reads (`chat_resume`, `_ask`) already failed closed. `start_thread` now raises `ChatNotFound` for both hidden and missing cases and stores nothing.

## Evidence

* Regression test `test_thread_cannot_be_bound_to_a_case_the_role_cannot_see` in `src/core/tests/test_chat_privacy.py` fails on both stores without the fix and passes with it.
* `test_chat*.py` in `src/core`: 198 tests OK. `test_*chat*.py` in `src/api`: 550 tests OK (1 skipped). `ruff check` clean. `mypy` reports 3 errors in `telemetry.py` (missing OpenTelemetry stubs) and `device_provision.py`, none in changed files.

## Per-criterion verdict

| Criterion | Verdict | Reason |
| --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unproven | #440 criteria 7 and 8 need owner approval, a PR and a non-worker reviewer; this fix is one bug disposition toward it |
| If accepted, child features are accepted | Unproven | Remainders need excluded human, legal or real-model steps (see the 2026-11-21 note) |
| Decision accepted (ticked) | Not reopened | ADR 0004 |
| No memory as evidence (ticked) | Not reopened | Unchanged |
| Consumption bounded (ticked) | Not reopened | Unchanged |
