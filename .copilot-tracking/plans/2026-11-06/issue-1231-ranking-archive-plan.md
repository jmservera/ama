---
title: Issue 1231 plan (ranking archive concurrent-writer metadata)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Committed together with the research, details and issue record before the first source or regression-test edit. Not backdated. Original #79 r11 evidence stays unchanged.

## Scope

* Source: `src/core/src/zava_forward/core/ranking_publication.py` only, plus its module docstring and the one README sentence that says "never deletes".
* Tests: new regressions in the existing `src/core/tests/test_ranking_publication.py` (helper and real filesystem, threads and spawned processes) and one runner-level regression in `test_ranking_publication_runner.py` for the actual issue reproduction. The existing no-delete scan test is narrowed (see details).
* New records: this research, plan, details, issue record, changes, author review, state. Nothing else.

## Phases

1. [ ] Commit prospective Research, Plan, details, issue record (this commit) before any edit.
2. [ ] Write regressions first and run them against the unchanged helper (RED), under unique `/tmp/1231-ranking-archive-r1-1106/` paths, recording counts and exits; retain the first failures.
3. [ ] Implement unique staging plus `os.link` no-overwrite publication; narrow docstring and README text.
4. [ ] GREEN focused tests, Ruff check and format, mypy, import-source proof.
5. [ ] Write changes record, run the author Review after the checks, state file, commit, freeze local candidate.

## Non-goals and boundaries

* No push, PR, merge, retarget, gh write, cloud call, SQL, browser, container, FULL gate, install, cleanup, heavy lock.
* No change to bytes, filenames, verification, policy, freshness, retention, approval, runner refusals or capacity logic.
* FULL, independent exact-head assessment and publication stay pending.
