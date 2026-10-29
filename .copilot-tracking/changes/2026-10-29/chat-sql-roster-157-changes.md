---
title: SQL roster chat revocation implementation evidence
description: Minimal local correction for issue 157 and PR 503
ms.date: 2026-10-29
---

## Context and Scope

Task `157-chat-sql-roster`, full plan scope P01/P02.
Plan `.copilot-tracking/plans/2026-10-29/chat-sql-roster-157-plan.md`;
details `.copilot-tracking/details/2026-10-29/chat-sql-roster-157-phase-details.md`;
critique `.copilot-tracking/reviews/plans/2026-10-29/chat-sql-roster-157-plan-critique.md`
executed once, Pass with no findings.

## Execution State

P01 implemented and P02-T01 validated. P02-T02 independent Review complete;
local commit pending; no source work remains.

## Changes and Validation

### P01-T01: Shared actor resolver

`ChatIsolation.current_user` now selects the authoritative staff JSON row by
normalized authenticated email under `dblock` for SQL stores, with no cached
fallback for missing rows. Missing, disabled, inactive and disallowed roles
raise `ChatForbidden`. Verified Entra branch and non-SQL lookup remain distinct.
The existing panel dispatch/completion call sites require no changes.

### P01-T02: SQLite regression and source documentation

Added one `SqlRosterTests` fixture, four tests: before-dispatch and during-model
revocation matrices (contractor, unknown role, disabled, inactive, deleted),
permitted-role-change withholding and unchanged-user answer control.
Independent SQLite writer commits without cache mutation; tests compare both
cache snapshots and assert no rejected answer persistence and completion audit.
The SQL history test's final role switch now updates SQL. Core README records
the behavior and SQLite evidence boundary.

### P02-T01: Red evidence

From `src/core`:

```bash
/tmp/mv/bin/ruff format tests/test_chat_panel.py
PYTHONPATH=src:tests:../agents/src:../agents/tests:../api/src:../api/tests \
  /tmp/mv/bin/python -m unittest test_chat_panel.SqlRosterTests -q
```

Before resolver changes: 4 tests, 11 failures. Every dispatch/completion
revocation variant failed to raise `ChatForbidden`; the permitted-role change
released `SQL-ANSWER-CANARY` instead of withholding. Stable-user control passed.
This confirms the regression detects the reported stale-cache behavior.

### P02-T01: Initial green and command correction

The six-module focused command (`test_chat_panel test_chatthreads
test_chat_privacy test_chat_memory test_chat_isolation test_regulatory_chat`)
passed: 146 tests, no skips. The API isolation fixtures log missing-law-store
warnings; no test fails.

The subsequent API `unittest discover -s ../api/tests -p test_chat_panel.py`
failed because the identically named core module was imported from the earlier
PYTHONPATH entry. Use the actual API script as the explicit selector instead,
which puts its own directory first without changing the source or test suite.

Initial Ruff found B023 on the synchronous callback's loop capture. Bind the
mutation as a default argument; no production behavior change. Re-run checks.

The corrected explicit API script invocation passed: 38 tests, one existing
opt-in Chromium skip (`ZF_BROWSER_TESTS` not enabled). Core panel rerun passed
22 tests.

An explicit-file Ruff format check bypassed the repository's existing formatter
exclusion for migrated `chat_isolation.py` and reported its pre-existing style.
Re-run with `--force-exclude` to honor that unchanged core pyproject policy:
Ruff check passed; format check passed for the formatted test file, with
isolation excluded by the existing configuration. No broad reformat applied.
`git diff --check` passed.

Additional targeted mypy found two test-only invariant dictionary inference
errors in the mutation matrix. Explicitly annotate the matrix element type
instead of weakening typing or casting. Re-run mypy, Ruff and core panel.

### P02-T01: Final Validation

From `src/core`, final command:

```bash
PYTHONPATH=src:tests:../agents/src:../agents/tests:../api/src:../api/tests \
  /tmp/mv/bin/python -m unittest test_chat_panel -q
/tmp/mv/bin/ruff check src/zava_forward/core/chat_isolation.py tests/test_chat_panel.py
/tmp/mv/bin/ruff format --check --force-exclude \
  src/zava_forward/core/chat_isolation.py tests/test_chat_panel.py
/tmp/mv/bin/mypy src/zava_forward/core/chat_isolation.py tests/test_chat_panel.py
git diff --check
```

Result: 22 panel tests passed; Ruff check passed; configured format check passed
(one formatted test file, existing migrated-isolation exclusion); mypy passed
two files; whitespace passed. Together with the six-module 146-test result and
the explicit `../api/tests/test_chat_panel.py -q` result (38, one existing
Chromium skip), the planned focused validation is satisfied. No SQL Server,
actual model, browser or full publication gate was run.

## Amendments and Divergences

No significant divergences or new decisions. Local judgments: bind callback loop
argument, annotate the test mutation matrix, select the API script explicitly
to avoid name collision, and honor the existing formatter exclusion. Updating
the SQL history fixture's final switch was already planned.

## P02-T02: Independent Review

Exactly one fresh independent Review executed Complete, outcome Conformant,
no actionable RV findings. Original artifact:
`.copilot-tracking/reviews/logs/2026-10-29/chat-sql-roster-157-review.md`.
Reviewer independently passed 146 focused tests, eight corrected contract probes
and whitespace check. Initial ephemeral probe-fixture error is retained in the
Review; no source correction or repeated Review occurred.

Assessed source patch SHA-256:
`48ccded0a41bb6a6d8490b8dcd5eec6ac7ab4db48403ba8df2416b1ae76388bd`.
Parent compared the three-path binary diff against the Review fingerprint after
the reviewer returned: exact match. This is not a committed-head publication
receipt. Local implementation/evidence commit is the remaining delivery action.

## Blockers, Remaining Work and Follow-Up

No implementation blockers. Full publication gate, SQL Server, real provider,
human approval and hosted acceptance are not executed or claimed. No push
authorized. Original #157 acceptance gaps remain outside this correction.
Plan/details/changes and task markers reconciled after Review; P02-T02 remains
open only for local commit. RPI task has completed its Review and is in Follow-up;
automatic session remains running with no new work selected. The only supported
later item is separately authorized publication assurance; Stop automatic session
and Switch to manual mode remain control options, not inferred selections.
