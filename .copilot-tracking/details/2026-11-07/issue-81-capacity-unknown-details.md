---
title: Issue 81 missing capacity confirmation Unknown typing details
description: Step-level prospective details for the typed-error correction, regression construction, preservation checks and validation commands
author: RPI agent (hve-core-all:rpi-agent)
ms.date: 2026-11-07
ms.topic: reference
task_slug: issue-81-capacity-unknown
parent_task: issue-81-realign-r2
status: prospective (details only; nothing executed)
plan: ../../plans/2026-11-07/issue-81-capacity-unknown-plan.md
research: ../../research/2026-11-07/issue-81-capacity-unknown-research.md
---

## P0 Preflight

* `git status --short --ignored` empty; `git rev-parse HEAD HEAD^{tree}` equals `7d390e13a450a5ca096501b1a2ccefcd9a517fd4` and `1d639b132ccf8ed3e4d920eb7dfcf2b394a15bee` (or the planning commit that follows it, with the only delta being the four planning files).
* `git fetch origin main`; `git merge-base --is-ancestor origin/main HEAD`. If main advanced, inspect the delta for overlap with `appointments.py`, `gates.py`, `procurement.py` and the test file before proceeding; a rebase is outside this authorisation.
* Re-read `appointments.py` lines 130-205 and confirm the research blob `9dc02c5ab` or record the change.

## P1 Regression first

* Read `dataset.supplied_appointment_fixture` and `refused_capacity` in `src/core/tests/test_quality_procurement.py` for the booking, save and `reopen()` pattern (JSON store; do not use private data).
* Add `test_booking_missing_capacity_confirmation_is_unknown_and_changes_nothing` next to the other booking-capacity tests, using `booked_case()`.
  1. Under `self.store.lock`, find the single active order for `ZF-3`, `del` its `appointment_offer["confirmations"]["capacity"]`, `self.store.save()`, then `self.store = self.reopen()`.
  2. Snapshot `copy.deepcopy((cases["ZF-3"], data["procurement"]))` and `list(audit_entries())`, and the `appointment_status` dictionary.
  3. `assertRaises(gates.CapacityGateError)` around `self.store.advance(PAM, "ZF-3")`; assert `isinstance(..., ValueError)`, `result.outcome == gates.UNKNOWN`, `result.gate == "capacity"`, rule provenance present as in the existing Pass test, text contains `Appointment is not committed` and `Capacity confirmation missing`.
  4. Assert snapshots and audit equal, and `appointment_status` equals the pre-refusal dictionary with `missing == ["Capacity confirmation missing"]`.
* Add a mixed pin `test_booking_missing_capacity_and_resident_confirmation_stays_plain_refusal`: delete both `capacity` and `resident`, reopen, assert a refusal that is a `ValueError` and not a `CapacityGateError`, text lists both missing items in the existing order, and nothing mutated.
* Run only these two tests before the fix; record the first as failing because the raised error is a plain `ValueError`. If the first passes pre-fix, stop and record that the finding is not reproducible instead of fixing.

Amendment 1 (see plan): assert `error.state is None`, the exact full message and the literal status dictionary; re-snapshot after a second reopen; add refusal and no-mutation tests for `record_wo_appointment(..., "Booked", date)` and `complete_work_order` on the same persisted record, in the SQLite-file flow too where an existing fixture exists.

## P2 Typed fix

* `appointments.py`, `_appointment_assessment`: introduce `capacity_unconfirmed = "capacity" not in offer["confirmations"]` after the confirmations loop (or track in the loop). After the `if capacity:` block and before the return, add: if `capacity_unconfirmed and len(missing) == 1`, then `capacity_error = gates.CapacityGateError(missing[0], None)`.
* No other source line changes. Keep the existing comment-free style. Do not alter the return tuple, `appointment_status`, or `require_appointment_commitment`.

## P3 Preservation checks

* Rerun both new tests (now pass) and the existing booking-capacity Pass, Fail and Unknown tests, no-order and unbooked-order cases.
* Diff proof: `git diff` limited to the one `appointments.py` hunk and the test additions; blob identities of `gates.py`, `procurement.py`, `quality.py` unchanged from the pinned values.
* Child preservation: `git log` and the three child commits remain ancestors; no other child-owned file changed.

## P4 Commands (isolated, no service)

```bash
env -i HOME=<scratch>/home PATH=<scratch-venv>/bin:/usr/bin:/bin TMPDIR=<scratch>/tmp \
  PYTHONDONTWRITEBYTECODE=1 ZF_DATA=<scratch>/data/zavaforward.json \
  <scratch-venv>/bin/python -m unittest -q test_quality_procurement test_gates test_hazard_referral
```

Amendment 1: explicit focused modules only, run from `src/core/tests`; add the appointment/offer module found by grep; never discover the full directory (`test_queue_benchmark` and queue-scale modules are excluded).

* Also run ruff check, `ruff format --check` and mypy on `src/core` as the core README specifies; read the README and workflow for exact flags at implementation time rather than assuming them.
* Prove import origin of `zava_forward.core` is the scratch venv's site-packages, not the worktree path or dirty primary checkout. Re-install `--no-deps` non-editable after the source edit so the installed copy contains the fix, or run from the worktree path only if the proof shows the intended origin.
* Record every command, exit code, test count and skip reason.

## P5 Records and freeze

* New dated records for changes, review, state (the planning stage writes none of these). Review must keep this stage's critique outcome and any adverse results verbatim.
* Commit with Conventional Commit type `fix(core)`, repo-local noreply identity resolved fresh with `gh api user`, and the Copilot co-author trailer. Report ignored-inclusive status, HEAD and tree.

## Stop conditions

Drift in blobs or base; regression not reproducing; any other test failing for a reason not caused by the change; mixed-case typing changing. Each is recorded as a blocker with evidence, not worked around.
