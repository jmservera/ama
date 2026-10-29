---
title: Progress lifecycle event-kind correction changes
description: Original implementation and validation evidence for correction4
ms.date: 2026-10-29
---

Task ID: 533-correction4. Task slug: progress-dashboard-533-correction4.
Declared scope: full plan. P01 and P02-T01 execution complete;
P02-T02 candidate commit / independent original Review / closeout pending.
Research executed / Ready. Original single critique Complete / Revise;
PC-001 and PC-002 applied directly before implementation. No repeated critique
or unresolved user decision. Earlier correction evidence remains unchanged.

## P01: Event identity and exhaustive regression coverage

Implement the complete initial/pairwise transition table, then typed replay.
Duplicate suppression is bounded to the current lifecycle-changing event,
not global timestamp/kind membership. Persist/reopen constructed fixtures
and assert raw lifecycle-bearing fields before observable endpoint assertions.

Changed only API progress.py, its canonical test file and API README.
Replay classifies all five event kinds before enforcing preconditions and
only then projects to the existing date/bool transitions. Return evidence is
validated as open-stage movement, never an episode; controlled advances remain
ignored. Distinct-time repeat identification/reopen/closing events do not
silently repair missing transitions. Current snapshot agreement remains required.
Duplicate/corroborating evidence is suppressed only for the current lifecycle
transition at the same normalized UTC instant. A,R,A,R at one instant retains
both closed episodes and reopenings, including zero-day samples.

Added exactly four inherited test methods and two fixture/assertion helpers.
No tests or assertions removed, no new test file, production schema,
dependencies, mypy/Ruff exemptions or generated dataset.
The literal table covers all five initial-event and 25 ordered pair cells,
each once per JSON/SQLite backend at distinct instants. Supplemental controls
cover all event representations (accepted/human/withdrawn/excluded closure,
simulation/controlled reopening), repeated evidence, UTC normalization,
stable same-instant order, out-of-order inputs, legacy return, ignored advance,
empty/inconsistent snapshots and the original review examples at distinct and
identical instants.

The shared helper persists JSON by mutating the existing dictionary and saving,
and injects only constructed SQLite case bodies before opening a fresh reader.
Every scenario proves exact raw lifecycle-bearing fields/closed roundtrip before
replay, exact coverage and daily/weekly backlog/open/close/reopen measures,
episode median/p90/sample count and unbounded/one-sided date-filtered archive.
Both supplied malformed open cases contribute unknown coverage and no invented
historical activity. Valid sibling cases retain exact historical measures.

### Red evidence and fixture correction

Initial red.log recorded four failures: SQLite reproduced the lifecycle bug,
but JSON failed raw payload equality because replacing the case dictionary
broke the Store's data-list alias. This was an ordinary test-harness correction,
not a production change or missing-source discovery. The helper now mutates
the dictionary in place, matching existing test prior art.
red-fixture-corrected.log then reproduced both supplied lifecycle failures in
both reopened stores: 2 inherited methods / 4 failed subtests, 0.212s.
No adverse log was overwritten. Initial focused green: all 41 progress tests
passed in 10.980s. Final additional assertions are included in the 77-test
fallback below.

## P02: Validation and local closeout

Scoped checks and one nonblocking admission attempt completed. Candidate
commit and one independent original Review remain. No push, az, force-push,
publication or human approval is authorized or claimed.

External root: /tmp/ama-533-correction4-20261029. Tools: /tmp/mv mypy 2.4.0,
Ruff 0.17.1. Runtime: /tmp/ama-533-venv Python 3.12.3.
All Python checks explicitly set PYTHONPATH to this worktree's src/api/src,
src/core/src, src/agents/src, src/api/tests, src/core/tests, src/agents/tests;
core tests precede API tests for core mypy. import-paths.log confirms
progress.py and core store.py resolve this worktree.

| Check | Command / directory | Actual result / evidence |
| --- | --- | --- |
| Pre-fix regression | python -m unittest two inherited review-counterexample selectors -q | Expected failure, four subtests; red-fixture-corrected.log |
| Focused progress | python -m unittest test_progress_dashboard -q, root | 41 passed, 10.980s; targeted-green.log |
| Heavy admission | flock -n -E 75 /tmp/ama-rpi-heavy.lock bash -c planned checks | Busy exit 75 before any enclosed setup/suite/browser command; lock.log |
| API types | /tmp/mv/bin/mypy, src/api | Passed 102 files, exit 0; api-mypy-final.log |
| Core types | /tmp/mv/bin/mypy, src/core | Passed 156 files, exit 0; core-mypy.log |
| API lint | /tmp/mv/bin/ruff check ., src/api | Passed, exit 0; api-ruff-final.log |
| API format | /tmp/mv/bin/ruff format --check ., src/api | Passed 54 files, exit 0; api-format-final.log |
| Core lint/format | /tmp/mv/bin/ruff check . && /tmp/mv/bin/ruff format --check ., src/core | Passed, exit 0, 103 already formatted; parent tool results |
| Final targeted fallback | python -m unittest test_progress_dashboard test_workbench test_role_screens test_workspace_scripts test_taskqueues test_scenario_manifest -q, root | 77 passed, 16.525s, exit 0; targeted-final.log |
| Full API/core discovery | Not launched after busy admission | Blocked, no success or skip claimed |
| Relevant browser | checks.progress_browser_check, not launched after busy admission | Blocked, no historical browser result reused |
| Shared /tmp/mv editable installation | Not launched after busy admission | Deferred; no shared environment mutation |
| Whitespace | git diff --check | Passed, exit 0 |

The lock listing immediately before admission had no holder, but atomic flock
returned busy; a later independent holder listing again had none. The transient
holder identity is unavailable. This is not permission to bypass, wait, poll,
kill any holder, retry admission or mutate the shared environment. The actual
flock result is authoritative. Full unit/browser validation remains an explicit
acceptance gap, not completion by targeted proxy.

No pinned scenario input changed. Existing scenario-manifest test passed; no
SHA-256 pin update is warranted. No private data, browser asset, web file or
core source was changed.

## Pre-Review Reconciliation

P01 checked with source/matrix/README completion evidence. P02-T01 checked as
authorized validation attempt/fallback execution, not full acceptance.
P02-T02 remains for candidate commit, one independent original Review and local
evidence closeout. Plan/details/status/remaining work and blocked full/browser
checks agree. No remaining source work or significant/divergent decision.
Local-only correction is reviewable, but full/browser acceptance is incomplete.
Future publication requires separately authorized exact-head gates, human/
hosted approvals and must not reuse this as a publication receipt.

## Amendments and Divergences

PC-001 adds same-instant alternating episode controls and PC-002 exact
backend readback. Both preserve approved intent; no source divergence.
