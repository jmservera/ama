---
title: Capacity browser import correction details
description: Implementation details for task 523-correction-1
ms.date: 2026-10-30
---

<!-- rpi:phase id=P01 -->
## [x] P01: Correct imports and preserve regression coverage

<!-- rpi:task id=P01-T01 -->
### [x] P01-T01

Use the regulatory test's fresh-interpreter MetaPathFinder pattern. Block
Playwright and import capacity tests. Build a suite from exactly the four
existing scanner tests to avoid recursion; assert execution count and no skips.
In that same isolated process, also call `check(None)` with Playwright denied.
The expected ModuleNotFoundError must happen before staff/store/server access.
Prove the new regression fails before editing the harness.

<!-- rpi:task id=P01-T02 -->
### [x] P01-T02

Add postponed annotations, move Page/Request/Response/Route imports under
TYPE_CHECKING, and import expect/sync_playwright at the beginning of `check`.
Use an evaluate-only Mock spec for both scanner tests. Leave all browser flows,
scanner hashing, thresholds and JSON diagnostic assertions unchanged.

<!-- rpi:task id=P01-T03 -->
### [x] P01-T03

Update the existing API local-check guide to name capacity's equivalent
browser-free behavior. No new standalone documentation page.

P01 evidence: the new subprocess regression failed before the harness fix;
imports, mocks and README are now corrected. One new test added, none removed.

<!-- rpi:phase id=P02 -->
## [x] P02: Validate and review

<!-- rpi:task id=P02-T01 -->
### [x] P02-T01

From `src/api`, run full unittest discovery with
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`
and pinned existing environment executables, then Ruff check, Ruff format check,
and mypy. Use `flock -w 600 /tmp/ama-rpi-heavy.lock` for heavy validation.
Record exact results and any unavailable checks without claiming success.
The first attempt exposed missing Azure SDK runtime packages and incomplete
current-source distribution metadata in the older environment. Restore all
current project distributions and pinned dev tools into a new dedicated
correction venv with pip before rerunning. This is environment repair after
an observed missing dependency, not a manifest change or testing exemption.
Restored result: 1377 tests in 487.774s, OK (318 opt-in skips); Ruff passed;
61 formatter-covered files unchanged; mypy passed all 117 source files.
Eight targeted capacity/version tests also passed. No live sign-in, Azure,
real browser/SQL acceptance, publication or push was performed.

<!-- rpi:task id=P02-T02 -->
### [x] P02-T02

Reconcile all task markers, changes, validation and residual boundaries before
one independent Review. Keep original outcomes even if follow-ups are routed.
Completed: single independent Review executed Complete / Conformant. No source
defects; Low RV-001 retains inherited publication/live gates outside this
correction. Original critique and first failed environment run remain intact.

<!-- rpi:task id=P02-T03 -->
### [x] P02-T03

Use authenticated account's local noreply identity, requested Copilot trailer,
and Refs #523 only. Commit all correction artifacts and source locally.
Do not run cloud/sign-in/push or claim complete publication acceptance.
Completed: local implementation/original-evidence commit
`7cc45330c7e768c0a5c955644ae4dac577e35a03`. Both author and committer use the
authenticated account's derived noreply address; the requested Copilot trailer
was verified in the commit. No push. Remaining edits only record this closeout.
