---
title: PR 507 synchronization phase details
ms.date: 2026-10-30
---

Task ID: pr-507-sync-2026-10-30. Slug: rubric-src-198-sync.
Plan: .copilot-tracking/plans/2026-10-30/rubric-src-198-sync-plan.md.

<!-- rpi:phase id=P01 -->
## P01: Integrate main

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rebase and reconcile actual conflicts

Clean starting worktree was verified before new task artifacts. These new
untracked artifacts are task-owned; no pre-existing work may be moved.
Fetch already completed. Explicit caller permission authorizes this rebase.
Configure authenticated repository-local noreply identity before replay so
committer privacy is preserved; do not amend old authors.

Predicted conflicts: docs/reference/README.md and docs/reference/log.md.
Keep main's full document content and the topic's independent additions,
remove only conflict markers/duplicate stale metadata. Rebase may encounter
additional conflicts across five historical commits: resolve each by intent.
During rebase ours/theirs are reversed relative to ordinary merge semantics;
use origin/main explicitly for rubric and manifest rather than ambiguous sides.

After replay, assert entire .github/rubric and
docs/reference/research/retrofit-synthetic-data/scenario-manifest.json equal main.
Append a dated synchronization qualification to existing cut-over synthesis,
update its index and append a new KB log entry. Never rewrite historical results.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Prove preservation and layout invariants

Depends on P01-T01. Compare immutable starting-head/main Git blobs to current
files: full main log prefix; complete original topic-only log tail; original
tracking artifacts exact; upstream index body lines preserved. Check no
application, legacy, workflow or infrastructure diff and main ancestry.
No tests may be moved or added inside packages.

<!-- rpi:phase id=P02 -->
## P02: Validate and reconcile evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run applicable local checks

Depends on P01-T02. Existing /tmp/mv Python 3.12.3, Ruff 0.17.1, mypy 2.4.0.
From src/core set PYTHONPATH=src:tests:../agents/src:../agents/tests.
From src/api set
PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests.
Use /tmp/mv/bin/python -m ruff check ., -m ruff format --check . and -m mypy.
Run core -m unittest -q test_scenario_manifest test_dependency_rule and API
-m unittest -q test_dependency_rule. Probe version module file paths before runs.
Migration command: /tmp/mv/bin/python tools/rename-zava-tests.py.
Rubric command: python3 -m pytest .github/rubric/scripts -q -ra; the existing
system environment has pytest, whereas /tmp/mv does not. Do not mutate shared
venv merely to run an available independent tool.
Record exact exits, counts, failures/skips. main-copy requirement prevents
changing inherited rubric tests. No full API discovery planned; if scope ever
requires it, nonblocking admission and held lock are prerequisites.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Record results and prepare one Review

Depends on P02-T01. Record commands, identities and outcomes in changes; mark
plan execution complete while retaining adverse acceptance results. Check
local links, whitespace and content invariants after final doc qualification.
Freeze the three-document diff hash and pass exact evidence pointers to a
fresh one-pass reviewer. No same-task implementation return after Review.
Parent owns final local commit and Git metadata check after Review. Required
publication gates and hosted checks are explicitly unperformed, not waived.

## Completion

P01/P02 and all task markers complete. One independent critique Complete / Pass,
no findings. Rebase, protected-input and 21-artifact preservation checks passed.
Core/API lint/format/mypy and twelve focused tests passed; twenty-five migration
regressions passed. Authoritative-main rubric suite: eighteen failures,
355 passes, seven missing-runtime skips. Those inputs remain unchanged.
No full API suite, shared heavy lock, cloud action or push. One Review is ready;
local commit and coordinator-owned publication follow separately.
Concurrent main movement was integrated before Review: final base
ffd8f35e63b24905b9aeb937dbf2a7fe9968747f, rebased head
86ce8f660d846a57da03ddd973ab513dd482465f. The intervening lockfile-only
changes do not alter any checked source, test, rubric or workflow input.
