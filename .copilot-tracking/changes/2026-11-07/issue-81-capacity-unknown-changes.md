---
title: Issue 81 missing capacity confirmation Unknown typing changes
description: Implementation record for the prospective capacity-Unknown plan, with RED and GREEN evidence, preservation proof and limitations
author: RPI agent (hve-core-all:rpi-agent)
ms.date: 2026-11-07
ms.topic: reference
task_slug: issue-81-capacity-unknown
parent_task: issue-81-realign-r2
plan: ../../plans/2026-11-07/issue-81-capacity-unknown-plan.md
details: ../../details/2026-11-07/issue-81-capacity-unknown-details.md
critique: ../../plans/2026-11-07/issue-81-capacity-unknown-critique.md
---

## Identity and provenance

* Start HEAD `43ed14bf6a0f277b1f944e47f3c94fc53f52527c`, tree `3ac2c68fb2d12d7a35632feddba33212d1faa1f7`, ignored-inclusive status clean.
* Origin/main fetched read-only: `a7f166c74608fe025d047a79448d5d2234622287` (docs-only #1247). Delta from the aligned base `0f420dc9`: 17 files, none under `src/` (`git diff --name-only 0f420dc9 origin/main -- src` is empty). No overlap with `appointments.py`, `gates.py`, `procurement.py` or the test file. No rebase, merge or alignment was performed; the parent remains based on `0f420dc9`, an ancestor of the new main.
* Pinned blobs before the change: `appointments.py` `9dc02c5ab`, `gates.py` `0d8d3d15b`, `procurement.py` `f01786666`, `quality.py` `f5813d361`.

## Changes

| File | Change |
| --- | --- |
| `src/core/src/zava_forward/core/appointments.py` | In `_appointment_assessment`, an `elif "capacity" not in offer["confirmations"] and len(missing) == 1` branch sets `capacity_error = CapacityGateError(missing[0], None)`. Two lines; nothing else |
| `src/core/tests/test_quality_procurement.py` | Helpers `persisted_without_confirmations`, `assert_confirmation_refusals`; tests `test_sole_missing_capacity_confirmation_is_unknown_and_changes_nothing` and `test_mixed_missing_confirmations_stay_ordinary_refusals`, run in `JsonFlows` and `SqlFlows` (SQLite file) |

The tests cover `advance`, `record_wo_appointment(..., "Booked", date)` and `complete_work_order`, each refused twice with a reopen between and after, asserting the exact message, the literal status dictionary, `state is None`, Unknown outcome and capacity gate (typed case), plain non-typed `ValueError` for the mixed case, and unchanged case, procurement and audit data (critique Amendment 1 fully applied). `gates.py`, `procurement.py` and `quality.py` blobs are identical to the start (`0d8d3d15b`, `f01786666`, `f5813d361`). No API, UI, policy or #86 change.

Design note: the guard uses the absence of the confirmation key, not truthiness, so a present-but-falsy capacity value cannot attach the typed error to some other single missing item.

## Evidence (local observed, no service)

Scratch `/mnt/ama-gates/g81-capacity-correction-1107` (venv, logs, snapshots outside the worktree). Every command ran under `env -i` with a minimal PATH, `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR`, `ZF_DATA` pointing at a nonexistent scratch file, external ruff and mypy caches, and no `ZF_RESIDENT_*` or `AZURE_*` variables. No private data, uv or service. Packages `ruff==0.17.1` and `mypy==2.4.0` were pip-installed into the scratch venv; core and agents were installed with `--no-deps` from `git archive` and tar snapshots of this worktree (not editable, not canonical main).

| Step | Result |
| --- | --- |
| Import origin | `zava_forward.core.appointments` and `gates` resolve to the scratch venv `site-packages`; installed copy contains the fix (grep count 1) |
| RED (HEAD production snapshot, four new tests) | Exit 1, 2 failures: both sole-missing tests, `ValueError('Appointment is not committed: Capacity confirmation missing') is not an instance of CapacityGateError` (JSON and SQLite). Both mixed-case pins passed pre-fix, as planned. Log `logs/red.log` |
| GREEN (fixed snapshot, same four tests) | Exit 0, 4 OK. Log `logs/green.log` |
| Focused `test_quality_procurement test_gates test_hazard_referral test_resident_preview` (from `src/core/tests`) | Exit 0, 233 tests, OK, skipped=1 (`JSON-only separate-file audit ordering`). `test_queue_benchmark` and queue-scale modules not run. Log `logs/focused.log` |
| `ruff check .` | Exit 0, all checks passed |
| `ruff format --check .` | Exit 0, 213 files formatted |
| `mypy` (project strict config) | Exit 0, no issues in 266 source files |

## Limitations

* No MSSQL, Azure SQL, browser, API, queue, scanner or FULL gate was run; none is claimed. SQLite-file flow is not SQL Server parity. Those remain implemented-unverified for the integrated parent.
* The old FULL receipts do not cover this head. FULL, independent exact-head review, hosted CI and stack alignment with child #86 remain pending.
* The R4 History assertion investigation (#1248), the owner decision on in-progress quality records missing evidence, human, resident and legal approvals, the four #81 criteria and #440 acceptance are untouched and unticked.
