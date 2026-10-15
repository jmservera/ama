---
title: Transactional hazard hold phase details
description: Exact implementation and validation boundary for review follow-up
ms.date: 2026-10-15
---

Task: hazard-hold-rv001. Research reused, single critique Pass.
P01-T01/P01-T02/P02-T01 complete; targeted 18 core hazard and 3 HTTP tests pass,
including nine interleaved guarded-transition subtests and writer serialization.
Full integrated core 325 passed; API 477 run/OK with 97 optional/environment skips.
Core/API lint/format/types passed. Single Review and P02-T02 delivery complete.
Correction 1762ccb and main integration 5da24ca pushed; PR 314 ready/mergeable
for code review, not operational acceptance. Original criteria remain unchecked.
No local implementation blocker; operational acceptance is deliberately outside
this correction. Plan owns requirements and acceptance criteria.

<!-- rpi:phase id=P01 -->
## P01: Correct and verify

<!-- rpi:task id=P01-T01 -->
### P01-T01: Transactional safety dependencies

Canonical targets: src/core/src/zava_forward/core/sqlstore.py and store.py.
Override the shared safety guard to register the case after its early check.
Inside existing save transaction, read current case body and rowversion for
each dependency, apply the base safety predicate and reject stale versions.
Use existing serialized-writer protocol, not another lock or schema.
Clear dependencies on success, discard and outer lock exit.
Route GateError through the same rollback/discard path as ConflictError so
no refused audit or procurement state leaks into a later request.
Add registration to advance while preserving its existing gate explanations.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Regression and documentation

Test owner: src/core/tests/test_hazard_referral.py; at most eight new test
methods, subtests for transitions. Removals: none. No generated targets.
Use actual independent SQLite stores, mock only the interleaving seam.
Semantic coverage: all guarded transitions, committed hold and absent failed
audit across reopen. Regression coverage: exact Completed reproduction,
stale clear-case conflict, dependency cleanup and transaction-local reload.
Check no in-memory or persisted procurement mutation survives failure.
Document unratified safety release authority and timing in src/core/README.md
and src/api/README.md; do not invent statutory clocks or approval.

<!-- rpi:phase id=P02 -->
## P02: Validate, review and deliver

<!-- rpi:task id=P02-T01 -->
### P02-T01: Requested gates

Use /tmp/zf164/bin/python, ruff and mypy. Core suite from src/core; API from
src/api with CI helper prefix PYTHONPATH=../core/tests:../agents/tests.
Extend PYTHONPATH with all five current worktree src paths because the supplied
interpreter's editable installs target another worktree. This is required to
test the actual changes without modifying shared package installations.
API mypy also uses current source paths via MYPYPATH.
After main advanced (#313), its missing pinned Playwright dev dependency was
restored in isolated temporary locations with pip. Requested mypy uses the
isolated venv's --python-executable for dependency discovery. Shared tools and
editable package installations remain unchanged.
Run targeted tests first, then both full suites plus lint/format/type checks.
Record failures as well as final results in the changes artifact.
No package installs unless a requested command fails for missing dependency;
then pip only and report it. No live/shared data tests.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and delivery

One post-implementation review against plan and changes; route remaining
owner/live acceptance to later work, not another review in this child loop.
Use verified account noreply identity and Conventional Commit with required
Copilot trailer. Push only the existing branch. Update PR 314 honestly,
Refs #85, all original criteria unchecked. Mark ready after code correction
passes local gates; ready for code review is not operational acceptance.
