---
title: Issue 2243 changes r4
ms.date: 2026-11-23
---

Status: complete. Classification: FULL (src change); no `rpi-checks.py` run, the coordinator runs gates.

## Changes

* `src/api/src/zava_forward/api/resident_demo/assistant.py`: `expiry_configured()`.
* `src/api/src/zava_forward/api/resident_demo/aoai.py`: `expiry_not_set` reason and label.
* `src/api/tests/test_resident_aoai.py`: regression test.
* `docs/reference/research/issue-2243-live-r4-2026-11-23.md`, index and log entries.

## Validation

`test_resident_aoai` and `test_resident_demo_api`: 72 OK; `python3 -m mypy` clean; ruff check and format clean. Hosted CI not observed (no push).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven (code and tests; live env `2028-01-01T00:00:00Z` read from `ca-resident-demo--0000028`) |
| Add a test | Proven (new r4 test plus earlier expiry test) |
| Rebuild and roll the resident image | Unproven for this change (registry firewalled per r3; not deployed, no Azure change made) |
| Resident chat answers with the model within caps | Unproven in this round (no browser proof run); r3 observed the document path model-backed and capacity 1 (1 request/min) as owner-only limit |
