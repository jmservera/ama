---
title: Issue 107 old-image SQL probe changes
description: Change record for the bounded test-only old-image SQL probe
ms.date: 2026-11-17
---

## Status

Implemented. Source edits began only after the implement-start witness event.

## Planned files

* `src/api/checks/old_image_worker.py` (new, in-image worker)
* `src/api/checks/old_image_sql_probe.py` (new, host probe)
* `src/api/tests/test_old_image_sql_probe.py` (new, light deterministic tests)
* `src/api/README.md` (short continuation section)

## Changes made

All four planned files were added or extended as planned, with no production, schema, policy, workflow or gate change. No amendment or divergence from the plan beyond the critique amendments already in the details file.

## Checks run (venv in evidence-107, this worktree's editable distributions)

| Check | Result | Fidelity |
| --- | --- | --- |
| ruff format and ruff check on the three new Python files | pass | static |
| mypy strict on the three new files | pass, no issues | static |
| `test_old_image_sql_probe` (16 tests) | pass | lower: no Docker, no older image, no SQL; SQLite self-test of current source |
| `test_assistant_restart_non_replenishment`, `test_assistant_release`, new module together | 95 tests OK, 7 skipped (existing SQL-gated skips, not run here) | existing scope preserved |
| `--self-test` run (evidence-107/selftest1, selftest2) | ACCEPTED, labelled current-source-self-test | not older-image evidence |

## Not run

* The actual older-image run, the disposable SQL Server container and the Docker engine code path (create, start, port, SQL connection) are untested here and left to the coordinator continuation in `src/api/README.md`.
* Complete local gate, receipt, hosted CI and independent exact-head review.

## Post-review amendment

The single review (see the review artifact) raised four findings in the new probe; all were fixed before the commit (judge refusal observation, error classification, violation precedence, exception-safe cleanup) and covered by added unit cases. After the fixes the new module and the restart module ran 31 tests OK; ruff and mypy strict pass.
