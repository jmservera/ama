---
title: Issue 2243 changes r4
ms.date: 2026-11-23
---

Status: complete. Classification: FULL (src/api test change); no `rpi-checks.py` run, the coordinator runs gates.

## Changes

* `src/api/tests/test_resident_aoai.py`: `test_question_path_follows_zf_demo_expires_at`.
* `docs/reference/research/issue-2243-live-r4-2026-11-23.md` (+ probe folder), index entry and log entry.

## Validation

`test_resident_aoai` 22 OK; `python3 -m mypy` clean; ruff check and format clean. Hosted CI not observed (no push).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven (code and live replies past 2026-11-01) |
| Add a test | Proven (free-text path test added) |
| Rebuild and roll the resident image | Partly proven: revision 0000028 live and behaves as fixed code; commit-to-digest link unproven, registry firewalled, build needs an unauthorised estate change |
| Resident chat answers with the model within caps | Proven live (2 of 2 questions model-backed, capacity 10) |
