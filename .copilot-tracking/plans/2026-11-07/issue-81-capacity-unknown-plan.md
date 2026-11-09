---
title: Issue 81 missing capacity confirmation Unknown typing plan
description: Prospective plan for the smallest typed-error correction and persisted/reopened regression so a sole missing capacity confirmation refuses as Unknown
author: RPI agent (hve-core-all:rpi-agent)
ms.date: 2026-11-07
ms.topic: reference
task_slug: issue-81-capacity-unknown
parent_task: issue-81-realign-r2
status: prospective (planned, not executed)
tier: FULL (eventual integrated parent publication)
research: ../../research/2026-11-07/issue-81-capacity-unknown-research.md
details: ../../details/2026-11-07/issue-81-capacity-unknown-details.md
critique: issue-81-capacity-unknown-critique.md
---

## Objective

Make a persisted Appointed work order whose appointment offer lacks only the capacity confirmation refuse as an explicit Unknown capacity gate result, keeping the refusal, error text, public status dictionary, mixed-failure behavior and no-mutation guarantee unchanged. No new feature, rule, approval or status.

## Boundaries

* Implementation is not authorised in this stage. This plan and its details are prospective only; the next stage (implementation) needs separate coordinator authorisation.
* Allowed source later: `src/core/src/zava_forward/core/appointments.py` (one local change) and `src/core/tests/test_quality_procurement.py` (one regression, optionally one mixed-case pin). Nothing in `gates.py`, `procurement.py`, API, UI, schemas, infra or docs beyond new dated tracking records.
* Do not touch child #86 worktree or its tracking, `refs/ama/*`, the three merged child contributions beyond the single `appointments.py` hunk, the cutover evidence pack checkpoint text, or any ticks.
* No heavy gate, queue, browser, SQL Server, Docker, scanner, Azure, push, PR, issue write or merge. #1248 owns the sole non-queued browser admission.

## Phases

| Phase | Content | Exit condition |
| --- | --- | --- |
| P0 Preflight | Confirm HEAD/tree, ancestry of fresh `origin/main`, clean ignored-inclusive status, blob identities from research | Any drift stops and re-plans with an amendment |
| P1 Regression first | Add persisted/reopened regression; run it and record it failing for the right reason (plain `ValueError`, no `.result`) | Failure observed and recorded before the fix, or recorded as not-reproducible |
| P2 Typed fix | Smallest change in `_appointment_assessment` per details | Regression passes; text unchanged |
| P3 Preservation checks | Mixed-missing case still plain `ValueError`; status dictionary equal before and after; existing capacity Pass/Fail/Unknown tests unchanged | All pass |
| P4 Focused regressions and static checks | Existing focused core suites plus ruff, ruff format check and mypy per component guide in an isolated scratch environment | Actual results and skips recorded |
| P5 Review and freeze | Author review record, changes record, state record, commit | Clean ignored-inclusive status, HEAD/tree reported |

## Design

* In `_appointment_assessment`, note whether the capacity confirmation is absent while the existing confirmations loop runs. After the capacity block, when the sole missing item is that absence (`len(missing) == 1`), set `capacity_error = gates.CapacityGateError(missing[0], None)`.
* `require_appointment_commitment` is unchanged; it already chains and rethrows with `state=None`, yielding Unknown with the capacity rule provenance.
* The same sole-item semantics as the existing malformed-evidence branch apply. If anything else is also missing, no typed error is attached.
* Widening to be recorded, not avoided: the other three callers of `require_appointment_commitment` receive the typed (still `ValueError`) error for this case.

## Regression design (details file holds steps)

* Persisted/reopened Appointed order: build a booked order through the existing fixture, delete only `capacity` from the persisted offer confirmations, save, reopen the store from the same path, then assert:
  * `advance` (booking gate) raises `gates.CapacityGateError`, which is also a `ValueError`;
  * `error.result.outcome == gates.UNKNOWN` with the capacity gate rule provenance present;
  * message equals the pre-fix message text, containing `Capacity confirmation missing`;
  * `appointment_status` returns the same dictionary shape and `missing == ["Capacity confirmation missing"]`, status `Offer`;
  * cases, procurement data and `audit_entries()` are unchanged.
* Mixed pin: remove capacity and also one other confirmation (resident), reopen, assert plain refusal with no `.result` attribute and unchanged joined text.

## Validation selection (later, no service)

* Core focused: `test_quality_procurement.py`, `test_gates.py`, `test_hazard_referral.py`, plus the appointment/offer test module(s) found by grep for `appointment_status` at implementation time.
* Static: ruff check, ruff format check, mypy for `src/core` as configured.
* Isolation: `env -i` allowlist, scratch venv outside the worktree, non-editable `--no-deps` installs of `src/core` and `src/agents`, import-origin proof, `PYTHONDONTWRITEBYTECODE=1`, scratch `TMPDIR` and `ZF_DATA`, no `ZF_RESIDENT_*` or `AZURE_*` switches, no private datasets, `node` on PATH only if API tests are run (not planned). Remove generated `build/` and `egg-info` directories afterward and prove clean ignored-inclusive status. Pip only after an actual missing-dependency failure.
* Skips (SQL Server, Azure SQL, JSON-only) are recorded verbatim, never counted as passes.

## Gaps and owners

| Gap | Owner / resume condition |
| --- | --- |
| FULL gate for the integrated parent (including child #86) | Coordinator admits one combined-tip gate after higher-priority work; must be fresh for the final base and head |
| R4 saved-call History assertion | #1248 investigation, unchanged |
| Independent exact-head review and hosted CI | Coordinator before push or merge |
| Replacement route for in-progress quality records missing evidence | Owner decision, unchanged |
| Human, resident, legal and professional approvals; four #81 criteria; #440 acceptance | Remain unticked and unmet |

## Recommendation

Continue: proceed to implementation of this single typed correction once authorised, because the finding is validated, the change is additive on an already fail-closed path, and the preservation checks are cheap and local.

## Amendments

Amendment 1 (from the executed critique, verdict Revise; all findings compatible, applied directly):

* Validation selection: the core suite is NOT discovered wholesale. Run explicit focused modules only (`test_quality_procurement`, `test_gates`, `test_hazard_referral`, plus the appointment/offer module located by grep). `test_queue_benchmark` and any queue-scale module are excluded. This supersedes "Core focused" wording and the discovery command in the details.
* Regression strength: assert `error.state is None`, the exact full message string, the complete literal `appointment_status` dictionary, and snapshots again after a second reopen to prove persistence did not change.
* Widened callers: add targeted refusal plus no-mutation tests for `record_wo_appointment(..., "Booked", date)` and `complete_work_order` for the same persisted record, using the existing JSON flow and, where an existing SQLite-file fixture exists, that flow too. These are in scope because the change affects those callers; they add no new behavior.
* Record that the API still returns HTTP 400 without exposing the structured gate result; no API change is planned.
