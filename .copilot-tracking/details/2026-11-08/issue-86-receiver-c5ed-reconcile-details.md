---
title: Issue 86 reconciliation of published parent c5edb32 details
description: Exact commands (Refs #86)
ms.date: 2026-11-08
---

* Pins: child `a8bfcca0…`, published parent `c5edb320…`, local parent `e888a499…`, main `f548b65f…`.
* Superset proof: `git diff c5edb320 HEAD -- <path> | grep -c '^-[^-]'` per source path; for the evidence pack only the single `ms.date` line may be deleted (185 insertions are preserved).
* Ancestry proof uses explicit exits: `git merge-base --is-ancestor X HEAD; echo $?`, never an OR.
* Tree proof: `git diff --name-only HEAD^1 HEAD -- . ':!.copilot-tracking'` should list at most justified paths.
* Selectors (from `src/core`, PYTHONPATH=tests): `tests.test_quality_procurement tests.test_gates tests.test_hazard_referral tests.test_resident_decisions` (`test_quality_procurement` is the appointment selector; grep for `_appointment_assessment` in tests finds nothing); `python -m mypy`; `ruff check src tests`; `ruff format --check src tests`. Raw `.out/.err/.exit` in scratch. `PYTHONDONTWRITEBYTECODE=1`, synthetic `ZF_DATA`, install only after a real missing-package failure.
