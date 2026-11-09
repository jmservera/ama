---
title: Issue 82 quality gate changes (2026-11-05)
ms.date: 2026-11-05
---

## Changes

* `src/core/src/zava_forward/core/gates.py`: `QUALITY_RULE` (source, effective 2026-11-05, version 1, unreviewed exercise reviewer) and `quality_gate`; unreadable evidence is unknown.
* `src/core/src/zava_forward/core/quality.py`: `evidence_gaps`, `quality_evidence_gate`; `handover_blockers` now uses the gate so view and transition agree (message text for gaps unchanged).
* `src/core/src/zava_forward/core/store.py`: `require_quality_evidence` raising `GateError` with reason, owner and next action.
* `accept_quality` calls it after the state check; `hand_over_quality` calls it for accepted records, so wrong-state `ValueError` is unchanged.
* `src/core/tests/test_gates.py`: `QualityGateTests` (unit outcomes, unreadable items, accept and handover refusal with record unchanged, complete evidence still passes, view agreement).
* `src/core/tests/test_hazard_referral.py`: the synthetic accept/handover race fixture carried `items: []`; it now carries complete synthetic evidence so the test still exercises the interleaved hold. This is a fixture correction, not a product regression.

## Evidence

* Pre-change reproduction: blanking one stored evidence item then `accept_quality` produced `Accepted`.
* Negative check: with `src/` reverted, `test_gates` fails to import `evidence_gaps`; the store-level cases fail by construction (no gate).
* `src/core` (PYTHONPATH set to this worktree because the installed editable points at another checkout): ruff check and format check pass; mypy `Success: no issues found in 266 source files`.
* unittest `test_gates test_hazard_referral test_buildings test_journey_store test_resident_journey_design test_progress_event_capture test_resident_decisions test_quality_procurement`: 497 tests OK, 112 skipped (SQL Server and optional-service cases; same skips occur before the change).
* `src/api`: `test_role_matrix` 13 OK, `test_assistants` 120 OK (58 skipped), ruff clean.
* Full gate: PENDING, see below.

## Full gate admission

* `/tmp/ama-rpi-heavy.lock` holder (2026-11-05 07:4x UTC): pid 1148896 `rpi-checks.py --all --jobs 2 --lock-timeout 0 --base ead177ef… --out /tmp/rpi188-full-20261105T0740` (gate #188) with a concurrent focused check. Not waited on, duplicated, or bypassed.

## Not changed

Capacity, authority, finance and eligibility families remain unconverted and unreviewed. No named reviewer, release, consent or finance approval was created.
