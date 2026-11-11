---
title: Issue 132 keyboard probe compatibility E4 admission amendment
description: Prospective E4 admission, implementation plan and validation details for the staff-job-pack-intake keyboard probe declaration (issue 132 follow-up)
ms.date: 2026-11-11
---

## Identity and lineage

* Native CLI session UUID: `3daf20c8-310c-4926-85ce-96019ffd6646`. The earlier handoff `task id` (`issue-132-keyboard-compat-1111`) is the RPI task identity, not a native UUID.
* Worktree `/home/azureuser/source/ama-demo-wt/issue-132-keyboard-compat-plan-1111`, branch `test/demo-intake-keyboard-compat-132-1111`, target `main`, base `35eb0e559c7d0660ab87594732675b71be7bee67`. Planning candidate head before this amendment: `6c175eb8c654b484d57c1a66b698458aa9e0b3d2`.
* Fetch at admission: `origin/main` is still the base and the base is its ancestor, so no rebase or merge is needed. The branch is independent of the #134 branch; no parent or source adoption.
* Consumes the planning candidate: [research](../../research/2026-11-11/issue-132-keyboard-compat-1111-research.md), [plan](issue-132-keyboard-compat-1111-plan.md), [details](../../details/2026-11-11/issue-132-keyboard-compat-1111-details.md), [critique](issue-132-keyboard-compat-1111-critique.md), [state](../../rpi-sessions/2026-11-11/issue-132-keyboard-compat-1111-state.json). They are unchanged.

## Admission

Root admits the bounded existing-probe repair as #132 extension cycle E4. Original C5 and extension E1, E2 and E3 remain spent. E4 is now spent for this correction. One extension cycle, E5, remains. No reset and no #134 authority is transferred. Whole #132, #134 and #233 stay open; no acceptance criterion is ticked and no human, assistive-technology, consent or production approval is claimed.

## Preserved records

* The original planning critique outcome stays `revise` with both findings (drift-guard regex coverage; empty regions do not prove zero orders), applied directly. It is not rerun or rewritten; originals and adverse records are untouched.
* Disclosure: the critic reported that the six existing unit tests passed although the planning pass was restricted to no runtime. That is a critic-produced planning scope exception. It is not pristine no-runtime history, not a new Root observation and not retroactive approval.

## Owned files

* `src/api/checks/specialist_keyboard_browser_check.py`: add exactly `"staff-job-pack-intake"` to the `NO_REGION_GAPS` tuple.
* `src/api/tests/test_specialist_keyboard_check.py`: one focused regression with a fail-closed registration drift guard.
* `src/api/README.md`: optional, only the count line `five screens have no evidence table` changes to `six`. The root #134 paragraph is appended separately; no other prose changes.
* New dated tracking for E4 under `.copilot-tracking/`.

Forbidden: predicate or helper signature, `EXPECTED_REGIONS`, walk or negative-control changes; wildcard, prefix gap or skip; weakened unknown-screen refusal; product, API, role, fixture, workflow or manifest changes; a new checker; `connected_home_browser_check.py` or its tests; SQL, cloud, provider or model; push, PR, issue or board writes; unrelated fixes.

## Order of work

1. Write the regression first and run it red on the unchanged probe; keep the reason and count.
2. Make the scoped entry; run the same module green.
3. Configured Ruff check and format check on the owned files; full API-project mypy once at the final head.
4. Exactly one final existing keyboard probe under `flock -n -E99 /tmp/ama-rpi-heavy.lock timeout 900`, only if the lock is free, non-queued, with a short scratch. No retry of a failed browser or final selector without Root direction.
5. One author Review after changes and validation; independence is Root's later review.

## Runtime boundary

Own worktree, private HOME, env, cache, TMP and scratch only. No private or default data, `.env` or real-HOME fallback. A missing import is recorded before any minimal private restore; no all-five or shared install. Existing cached Chromium only; no browser download and no axe fetch. The existing probe performs no axe scan, so none is claimed.

## Browser observation limit

The source-derived no-order cause stays static. The probe must be observed for: the empty-order message, and a successful `/api/workorders` read for each of the seven roles. If the existing probe cannot observe either, record that narrow limit and do not claim it proves absent orders. Never widen the gap to swallow an error. Any relevant HTTP, readiness, status, handoff or reset failure stops the work with an exact blocker; expected text and product are not adjusted under E4.
