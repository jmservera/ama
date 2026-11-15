---
title: Fieldwork variation named-owner changes (#132)
ms.date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/job_pack.py`: non-instruction stamp, notice, `reject_instruction_claim`.
* `src/core/src/zava_forward/core/staff_intake.py`: `field-escalate`, `escalations` in the view, stamps on boundaries and destination.
* `src/api/src/zava_forward/api/web/staff-intake.js`: notice and raised-escalation table.
* `src/api/tests/test_fieldwork_variation_owner_guard.py`: 4 tests.

## Validation

* New tests, `test_staff_intake_api`, `test_procurement_screens`, `test_accessibility_baseline` and core `test_job_pack` pass.
* mypy and ruff (check and format) clean in `src/core` and `src/api`, caches in `/tmp`.
* Not run: `tools/rpi-checks.py --all`, hosted CI.
