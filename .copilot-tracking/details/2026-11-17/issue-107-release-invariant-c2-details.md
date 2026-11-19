---
title: Issue 107 release-invariant classifier correction details
description: Phase details for the C2 release-state classifier correction
ms.date: 2026-11-17
---

## Phase 1 tests

* `test_active_mutated_row_after_the_mismatch_worker_is_a_violation`: set the MISMATCHED row in `after_mismatched_restart` to status active with the MUTATED version; expect VIOLATED with an approval message.
* `test_approval_restored_only_by_a_later_restart_is_a_violation`: subTests for REVOKED and MISMATCHED active only in `after_remaining`, then only in `after_larger`; expect VIOLATED.
* `test_active_mutated_row_is_not_a_violation_when_mismatch_step_did_not_complete`: mismatch step status error leaves INSUFFICIENT, not VIOLATED, for that row (the runtime may not have run).
* `test_lost_or_unreadable_release_state_is_insufficient`: remove the bound release id from `after_larger`, or the releases mapping, expect INSUFFICIENT and no ACCEPTED.
* Existing restored-approval test stays.

## Phase 2 code

* In `judge`, after the pre-mutation checks, build `bound = {cap: {id of every after_provision row}}`; an empty or id-less set adds a weak note.
* Add module function `release_state(snap, cap, ids)` returning `"unreadable"` when rows are unreadable or a bound id is absent, `"active"` when any row of the capability is active, else `"ok"`.
* `refused`: replace the exemption with `release_state`; add an `audit` helper in `judge` that records `bad` or `weak` per snapshot. The mismatched capability is audited only when the mismatch step completed `ok`.
* After the two `refused` calls, audit REVOKED in `after_mismatched_restart`, `after_remaining` and `after_larger`, and MISMATCHED in `after_remaining` and `after_larger`.
* Never audit `after_mutation`.

## Critique amendments (applied directly)

* Completion gate for the mismatch audit: step status ok, at least one executed record, no `error` in any executed or reinvoked record. Tests: execute error and reinvoke error leave INSUFFICIENT, not VIOLATED.
* `release_state` returns independent `active` and `unreadable` flags; a row with a non-string status is unreadable. Tests: bound id replaced plus new active row is VIOLATED and also lists the gap; malformed status is INSUFFICIENT.
* Trigger readbacks (`revoked_read`, `mutated_read`) consider only rows whose id is bound. Test: an unrelated row cannot establish the trigger.
* Fixture: `after_mutation` mismatch row active with MUTATED version; ACCEPTED still holds.

## Phase 3 docs

One README sentence: the later restarts are audited for restored approvals, the mutated row is not exempt, and lost release rows are INSUFFICIENT.
