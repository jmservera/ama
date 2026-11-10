---
title: Issue 81 missing capacity confirmation classification research
description: Prospective research validating an independent finding that a persisted Appointed work order lacking only its capacity confirmation is refused without an explicit Unknown capacity result
author: RPI agent (hve-core-all:rpi-agent)
ms.date: 2026-11-07
ms.topic: reference
task_slug: issue-81-capacity-unknown
parent_task: issue-81-realign-r2
status: prospective (research only; no source, test or gate executed)
research_disposition: executed
planning_readiness: Ready
---

## Scope and identity

* Worktree `/home/azureuser/source/ama-wt/parent-81`, branch `feat/controlled-lifecycle-integration-81`, HEAD `7d390e13a450a5ca096501b1a2ccefcd9a517fd4`, tree `1d639b132ccf8ed3e4d920eb7dfcf2b394a15bee`, ignored-inclusive status clean at start.
* `origin/main` `0f420dc9514db22081cb48fa733267d9d33a0d24` is an ancestor (verified). Backup refs `refs/ama/issue81-start` (`af891a5cc`) and `refs/ama/issue81-r2-pre-realign` (`c5edb320a`) unchanged.
* Source of the request: independent functional report `/home/azureuser/.copilot/session-state/f751a4dc-045d-479c-8035-8588858e3b08/files/review-81-7d390-r5/functional-findings.json`. Verdict `approve_with_comments`, one Medium finding, for dependent prepublication only. It is not parent integration acceptance, a FULL receipt for this head, or approval of any kind. The coordinator elected to correct the gap before publication.
* Pinned blobs at HEAD: `appointments.py` `9dc02c5ab`, `gates.py` `0d8d3d15b`, `procurement.py` `f01786666`, `test_quality_procurement.py` `748137893`. The last change to `appointments.py` is child #1229 (`5f1bf0a42`).

## Report validation against current code

The finding is real and correctly located, with one precision note.

* `src/core/src/zava_forward/core/appointments.py`, `_appointment_assessment` (lines 152-154): the loop appends `"<Kind> confirmation missing"` for each absent confirmation but never records a typed capacity error.
* The only place `capacity_error` is set is the `if capacity:` branch (lines 185-194), reached only when a capacity confirmation exists and `_existing_capacity` raises a `CapacityGateError`. The report's "malformed capacity evidence" tests cover exactly that branch.
* `require_appointment_commitment` (lines 197-203) raises `CapacityGateError(message, capacity_error.state)` only when `capacity_error is not None`; otherwise a plain `ValueError`. So an Appointed order whose offer holds resident and staff confirmations but no capacity confirmation is refused, but with `ValueError` carrying no `.result`, no Unknown outcome and no rule provenance.
* `gates.CapacityGateError` (`gates.py` lines 313-319) is a `ValueError` subclass; `state=None` yields `capacity_gate(None, message)`, which is the Unknown outcome. `procurement.py` already raises `CapacityGateError(..., None)` for no order, unbooked order and unverified legacy capacity, so Unknown with `None` is the established convention.
* Precision note: `require_appointment_commitment` has four callers (`procurement.py` lines 472, 494, 635, 655), not only booking advance. `record_wo_appointment` (Booked), `complete_work_order` and `require_booked_capacity` all use it. A typed error therefore also appears on those paths. It remains a `ValueError` with identical text, so callers that catch `ValueError` are unaffected. No code catches `CapacityGateError` outside tests (grep of `src/`). This is a benign widening, not scope extension, and the plan records it.
* Persisted-case reachability: an Appointed order normally has all three confirmations (`appointments.py` line 407 moves to `Appointed` only after the three). A record lacking only capacity is therefore legacy, hand-edited or malformed persisted state. That is the case the report names and the case the regression must construct, by editing the persisted order and reopening the store, as `refused_capacity` in `test_quality_procurement.py` does for package capacity details.

## Existing behavior that must not change

* `appointment_status(w)` returns the dictionary `dict(status=..., missing=[...])` only; `_appointment_assessment` returns a tuple that only internal callers see. The public status shape, `missing` text and ordering stay identical.
* Mixed failures: when more than one item is missing (for example resident confirmation also missing, home changed, pause, staff authority changed), the current rule is that no typed capacity error is attached and a plain `ValueError` with the joined text is raised. Whether an existing test pins this is not verified; the plan adds a pinning case and keeps the sole-missing-item rule so mixed cases are unchanged.
* The existing `len(missing) == 1` check inside the `except` branch of the capacity block is evaluated after the append, so it means capacity evidence was the only missing item at that point. Capacity is the last check, so this is equivalent to "sole missing item". The new case must use the same sole-item semantics.
* Refusal must not mutate state or audit: `require_appointment_commitment` is called before any write in `record_wo_appointment` and `complete_work_order`; `require_booked_capacity` is read-only. Existing regression helpers (`refused_capacity`, `assert_unknown_order_evidence_refused`) show the snapshot pattern for cases and procurement data plus `audit_entries()`.

## Smallest proper fix (design finding)

* In `_appointment_assessment`, record when the capacity confirmation is absent (a local boolean set inside the existing confirmations loop, or a direct check). After the capacity block, if the only missing item is that absence (`len(missing) == 1`), set `capacity_error = gates.CapacityGateError(missing[0], None)`.
* Do not change `require_appointment_commitment`: it already rethrows with `capacity_error.state` (None) and chains `from capacity_error`. Its message prefix `"Appointment is not committed: "` is built from `result["missing"]`, so the text is unchanged.
* No change to `gates.py`, `procurement.py`, the API, or any schema. No new gate logic, rule, approval or status value.

## Evidence classification

* Code facts: observed by reading current files at the pinned blobs (local observed, no execution).
* Test baseline: not yet executed in this stage. Existing focused suites were last run on this head in the realign r2 record (193 core tests OK, 1 skip, and related suites); that is history, not coverage of the change.
* Rule records and gate text remain exercise fixtures with an unreviewed reviewer. No legal, professional, resident or human approval is inferred.

## Risks and gaps

* Low behavioral risk: additive typing on an already-refusing path. Medium integrity risk if the sole-item rule is implemented loosely and changes mixed-failure typing; the regression must pin a mixed case.
* Tier: FULL remains the eventual tier for the integrated parent (persistence, consent, safety, SQL). Small code size is not a downgrade basis. This stage executes nothing.
* Unrelated and untouched: the R4 saved-call History assertion investigation owned by #1248, child #86 complaints work in its own worktree, and the owner decision on in-progress quality records missing evidence. None is resolved here.

## Planning readiness

Ready. Remaining unknown for implementation: exact fixture construction for a persisted Appointed order without the capacity confirmation using `dataset.supplied_appointment_fixture`, to be resolved by reading it when implementation is authorised.
