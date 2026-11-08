---
title: Issue 86 resident-control SQL fixture correction plan
description: Prospective plan for a bounded test-fixture correction and its baseline and regression evidence
ms.date: 2026-11-08
---

Scope: issue #86 only. Tier: FOCUSED local validation per the owner CI-first position; actual captured failure blocks publication until resolved and is not waived by green CI that does not select the Core SQL class. No Core class is added to CI or tool selectors (separate follow-up).

## Steps (execute only after coordinator admission)

1. Preconditions: head `f024a965` plus these records, ignored-clean; fetch Main, parent ref and PR base; stop on drift. Lock free, container count 0, resources rechecked.
2. Baseline B1 on Main packages and Main tests; B2 on candidate; B3 only if importable. Preserve all raw outputs.
3. B1 and B2 must execute the intended test without skips or import errors, otherwise they are inconclusive. Report the observed comparison separately from the static diagnosis. A Main failure shows the failure exists on Main; it does not by itself prove the root cause, which the fixed regression must confirm. A Main pass means divergent results: stop, investigate, no fixture change.
4. Correct the fixture only: add a backend-aware seeding helper using the public `merge_seed`; keep every assertion and skip.
5. Regression: single method on the three classes, `-k challenge` on the three classes, `test_seed_merge`; then the full core `MssqlResidentControls` class once to prove 108 tests with a framework total (read the `Ran`/`OK` lines, not `ok` counts).
6. Mypy and ruff on the touched test file only.
7. Changes and one author Review; commit; freeze ignored-clean. Tests-only diff proven by tree comparison of `src` outside the one test file and by unchanged `tools`, `infra`, `.github`.

## Stop conditions

Lock held or resources short; drift; B1 passes; `merge_seed` fails on MSSQL (report the exact error, no private SQL, no production change); any confirmed production bug (report and stop); transport beyond the bounded timeout (report as failure).

## Not claimed

No production bug, no FULL, no real receiver, cross-process, multiuser, model, legal, resident or AT approval, no #1238 relaxation, no tick or closure. Independent exact-head assessment, hosted checks and publication remain.

## Critique amendments (accepted)

* F1: baseline conclusions as in step 3; observation and diagnosis reported separately.
* F2: set `PYTHONPATH` to the tree's `src/core/tests` only (top-level `dataset` import); verify test-module origin and installed-package origin; import errors or skips are inconclusive.
* F3: record that the run exercises the normal-database append-only trigger, not Azure SQL ledger tables; no ledger compatibility claim.
* F4: the helper must assert exactly 41 cases inserted (report `to_insert`), reopen before use, keep all existing assertions, and report any backend divergence rather than adjusting assertions.
