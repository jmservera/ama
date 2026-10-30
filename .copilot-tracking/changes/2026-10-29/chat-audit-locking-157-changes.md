---
title: Chat receipt audit locking changes
description: Original implementation and validation evidence for issue 157
ms.date: 2026-10-29
---

## Metadata

* Task ID: 157-pr503-audit-locking-2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/chat-audit-locking-157-plan.md.
* Details: .copilot-tracking/details/2026-10-29/chat-audit-locking-157-phase-details.md.
* Implementation date: 2026-10-29.
* Declared implementation scope: P01; P02 belongs to parent review/closeout.

## Execution Status

Complete for declared P01 scope, P01-T01 through P01-T04 completed.
P02 remains parent-owned Review and local closeout.
Independent critique Complete / Pass, no findings.

## Completed Work

### P01-T01/P01-T02: Regressions and original failure

Added four test methods and one shared concurrency helper in the existing core
test owner, below the five-method maximum. Tests cover two rejected outcomes,
completed/refused turns alongside a locked ordinary writer, a locked writer
inside inference, and nested JSON/SQLite callers plus SQLite reopen.

Before any source fix, from src/core:

```bash
PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests \
  /tmp/mv/bin/python -m unittest \
  test_chat_panel.StoredQuestionTests.test_concurrent_rejected_turns_preserve_shared_audit_chain -v
```

Original result: exit 1, one test with two failing subtests at the genuine
store.verify_audit assertion. Missing-thread/access-rejected was the first
failure; invalid-skill/rejected also reported a broken chain. Runtime 0.007s.
This original adverse result is retained; no success claim substitutes it.

### P01-T03: Short persistence lock sections

Locked final chat.turn append, question-message persistence and finish's
assistant-message/chat.answer section using the existing reentrant lock.
Covering whole message calls retains the lock through their indirect
chat.message.added audits. Inference remains between sections. Updated the
existing core README with the contract and cross-process limitation.

## Implementation-Time Plan and Detail Updates

Ordinary local test implementation: first Ruff pass found six B023 loop-capture
warnings after the first successful combined test execution. Bound the reject
flag explicitly and used partials for concurrent completed turns. No requirement
or source-scope change, no extra critique. Test ownership and five-method maximum
retained (four actual methods plus one concurrency helper).

Tracking reconciliation uses canonical rpi phase/task markers. Review record
will use the skill's canonical reviews/logs date directory; identity unchanged.

## Validation Record

| Check | Result | Evidence |
| --- | --- | --- |
| Original rejected-turn regression, unchanged source | Failed as expected | Exit 1; true ledger-chain assertion failed |
| First combined focused chat execution | Passed | 133 tests, 31.360s, no skips |
| First Ruff check | Failed then corrected | Six B023 test closure warnings; no production lint finding |
| Final core/agent focused suite | Passed | 101 tests, 20.083s, no skips |
| API panel suite | Passed with explicit skip | 38 tests, 17.211s; 1 pre-existing opt-in Chromium test skipped (`ZF_BROWSER_TESTS` not enabled) |
| Ruff check | Passed | All checks passed for both changed Python files |
| Ruff format --check | Passed | 2 files already formatted |
| Focused mypy | Passed | Success, no issues in 2 source files |
| git diff --check | Passed | No whitespace errors |
| Protected rubric | Unchanged | git diff --exit-code for latest.json succeeds |

Final core/agent commands from src/core:

```bash
export PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests
/tmp/mv/bin/python -m unittest test_chat_panel test_chatthreads test_chat_privacy \
  test_chat_memory test_chat_model test_chat_provenance -q
/tmp/mv/bin/ruff check src/zava_forward/core/chat_panel.py tests/test_chat_panel.py
/tmp/mv/bin/ruff format --check src/zava_forward/core/chat_panel.py tests/test_chat_panel.py
/tmp/mv/bin/mypy src/zava_forward/core/chat_panel.py tests/test_chat_panel.py
```

The first 133-test command additionally selected test_chat_isolation, with the
same core-first paths. Isolation was already successful and source was unchanged
afterward; only test closures were corrected for lint.

API command from src/api (disambiguates the same-named panel test module):

```bash
PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests \
  /tmp/mv/bin/python -m unittest test_chat_panel -q
```

Expected API fixture logs report unavailable rule evaluation because no law
store is loaded; test runner still returns success. No browser, real SQL Server,
live model, Azure or full publication gate was run or claimed. No dependency
install was necessary. No existing tests were removed.

## Pre-Review Reconciliation

Ready for one independent Review: plan markers/details, completed source/test/
README work, original failure, final validation, remaining P02 work and publication
limitations agree. No implementation blocker or divergence. Local commit pending.

## Blockers

None for implementation. Full publication gate, hosted checks and human approval
are separate prerequisites before any future publication; no push is authorized.

## Remaining Work

None in this local-only task once the enclosing commit succeeds. No publication
or additional follow-up work is authorized.

## Follow-Up Items

None selected; broader issue 157 acceptance remains outside this correction.

## Parent-Owned Review and Closeout

P02-T01 executed exactly once by an independent reviewer. Original execution
Complete / outcome Conformant, zero findings or blockers. Record:
.copilot-tracking/reviews/logs/2026-10-29/chat-audit-locking-157-review.md.
Independent 26-test panel run, Ruff check/format and whitespace checks passed.
This result is not an exact-final-commit publication assessment.

No source or test changes followed the original Review. Parent closeout fixes
only stale research drafting status/question metadata and updates phase/state
completion records; the original critique and Review are preserved unchanged.
No material amendment, divergence or routed finding exists.

Authenticated GitHub account resolved by gh api user: id 8036360, login jmservera.
Local commit will use its constructed privacy-safe author/committer address.
The commit skill's legacy instruction-file path was unavailable; the installed
rules/hve-core equivalent was located and read. Its get_changed_files tool is
not exposed, so the repository-required native scoped diff/whitespace inspection
is used rather than claiming that unavailable tool ran. No broad staging or
unrelated existing change is authorized.

P02-T02 completion is bound to the enclosing local commit, whose subject is
`fix(chat): serialize panel audit receipts and message events`, referencing
issue 157 and including the requested Copilot coauthor trailer. This avoids
self-referential commit hashes in committed artifacts. The caller receives the
actual new commit ID after the commit succeeds.

No follow-up work was selected or started. The full publication gate, browser
opt-in, SQL Server, live model, hosted checks and human approvals are not run
or claimed. No remote write, az action or hand-edited rubric change.
