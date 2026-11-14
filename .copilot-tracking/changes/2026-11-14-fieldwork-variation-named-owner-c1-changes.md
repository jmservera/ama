---
title: Fieldwork variation named-owner C1 changes (#132)
ms.date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/job_pack.py`: `contract_notice` replaces `note`; strict instruction-claim check.
* `src/core/src/zava_forward/core/projection.py`: `summary` held for escalation items.
* `src/core/src/zava_forward/core/staff_intake.py`: redacted view, `escalation_options`, text-only inputs, closed and withdrawn guards, `_read_dependency`.
* `src/api/src/zava_forward/api/web/staff-intake.js`: raise form and fail-closed status cell.
* Tests: `test_fieldwork_variation_owner_guard.py` (SQLite, JSON, node vm), `test_role_endpoint_inventory.py`, core `test_job_pack.py`.
* Docs: `src/core/README.md`, `src/api/README.md`.

## Validation

* Guard, inventory, accessibility baseline, content standard, handoff, staff intake API and UI support tests, plus core job pack tests, pass with worktree `PYTHONPATH`.
* mypy and ruff check and format clean in `src/api` and `src/core`, caches in `/tmp`.
* Not run: `tools/rpi-checks.py --all`, browser harness, hosted CI.
