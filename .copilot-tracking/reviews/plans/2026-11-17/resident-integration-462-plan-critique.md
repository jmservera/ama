---
title: "Plan Critique: resident-integration-462"
description: "Single independent critique of the Issue #462 continuation plan (original, preserved unedited below the header)"
ms.date: 2026-11-17
---

| Field     | Value                                                                  |
|-----------|------------------------------------------------------------------------|
| Critic    | rubber-duck agent (independent context, read-only), one pass           |
| Target    | [plan](../../../plans/2026-11-17/resident-integration-462-plan.md) and [phase details](../../../details/2026-11-17/resident-integration-462-phase-details.md) as first written |
| Execution | executed once; no repeat critique for this task                        |
| Verdict   | Revise (0 Critical, 4 High, 3 Medium, 0 Low)                           |

## Critique output (verbatim)

**Verdict: Revise** — critique complete. The predicted merge is clean, but the plan needs corrections before execution.

* PC-001, High: The plan requires original 2026-11-16 files to be byte-identical, yet edits the 2026-11-16 threat model. Evidence: plan line 38, phase details line 18. Fix: put the dated update in a new file and verify original files against `926b20a8`.
* PC-002, High: `flock -n ... true` releases the lock immediately; browser checks can overlap the coordinator's run. Evidence: phase details lines 33-34. Fix: hold the lock for the entire browser-check process or record it pending.
* PC-003, High: Required witness boundaries are omitted: `plan-done` needs a persisted critique; `implement-done` and `review-done` must precede `commit-complete`, which otherwise refuses without `review-done`. Evidence: `tools/rpi_phase_witness.py:24-40,271-282`. Fix: specify the ordered events, artifact and state updates and verification; store witness logs externally so the final tree remains clean.
* PC-004, High: Ancestry plus two parents does not prove the merge starts at exactly `926b20a8` or has the intended parent order. Evidence: plan line 37. Fix: require exact HEAD before merging and verify final first and second parents are the candidate and pinned main respectively.
* PC-005, Medium: The listed test globs omit promised auth, case and projection suites; the core glob also includes SQL tests that must skip here. Evidence: phase details lines 24-29. Fix: enumerate runnable suites, expected SQL skips and exact commands; report unrun coverage separately.
* PC-006, Medium: Corrections after the independent review can invalidate its snapshot, despite the plan requiring no second review. Evidence: phase details lines 42-43. Fix: require review of the final source snapshot or explicitly qualify any post-review corrections.
* PC-007, Medium: Main's README says the view shows a status badge and source line, but the UI returns before both for empty history and suppresses that badge for stale history. Evidence: `1c9ac230`, `src/api/README.md`. Fix: require a documentation-only qualification after merge.

Next step per critic: planner corrects PC-001 first; no user decision required.

## Dispositions (added by the planner; the critique text above is unchanged)

| ID | Disposition |
|----|-------------|
| PC-001 | Accepted. The dated update goes into a new file `docs/reference/research/resident-demo-threat-model-update-2026-11-17.md`; the 2026-11-16 document is not edited and is verified byte-identical to `926b20a8`. The original research and review artifacts are likewise untouched. |
| PC-002 | Accepted. The whole browser process runs under `flock -n` as its wrapper, so the lock is held for its duration, or the checks are recorded pending. |
| PC-003 | Accepted. Ordered events are written into the details. Witness logs live in the external evidence directory. |
| PC-004 | Accepted. Exact HEAD and final parent order are verified. |
| PC-005 | Accepted. Suites are enumerated in the details after discovery in the implement phase; unrun coverage is listed separately. |
| PC-006 | Accepted. Review is run on the final source snapshot; any later documentation-only correction is stated as a qualification in the review record. |
| PC-007 | Accepted if the README claim is confirmed after the merge; handled as a documentation-only qualification (no source edit). |
