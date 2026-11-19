# Research: issue 1259 live DEMO criteria (2026-11-19)

Task: `issue-1259-live`. Refs #1259. Synthetic DEMO, desktop only, core filesystem logic. No Azure resource, model call or credential is involved, so none was used or read.

## Issue state

Five acceptance criteria. Criteria 1 to 3 are ticked. Open: criterion 4 (regular-file and dangling-link regressions for schedule, verify and publish, absent-directory coverage, failure before fix) and criterion 5 (original RPI, current FULL receipt, independent exact-head assessment, hosted checks).

## Evidence

* Source: `_names` in `src/core/src/zava_forward/core/ranking_publication.py` raises `NotADirectoryError` for a non-directory and calls `_require_creatable` only for a genuinely absent path; the runner `_verify` maps `OSError` to the unreadable problem shape.
* Regressions: `UnusableArchivePathTests` in `src/core/tests/test_ranking_publication_runner.py` (regular file, dangling link, dangling ancestor, stat failure through schedule, verify and publish; absent-directory first run). Present on main since `cd687abad` (#1328).
* Prior notes: [run 1](../../docs/reference/research/2026-11-18-ranking-archive-unusable-1259-failing-first.md), [run 2](../../docs/reference/research/2026-11-18-ranking-archive-unusable-1259-live-r2.md).
* Fresh red-before run today, detached worktree at `cd687abad^` with the current test file: `UnusableArchivePathTests` Ran 6, `FAILED (failures=7)`.
* Fresh green run today on `1dddac2e0`: `test_ranking_publication_runner` plus `test_ranking_publication` Ran 110, OK.

## Disposition

Criterion 4 is already satisfied by merged code and tests; today's run re-confirms it. Criterion 5 is a human and CI gate set that this local lane cannot satisfy; no source change is needed. Research disposition: `reused` plus fresh re-observation. Planning Readiness: Ready (evidence-only plan).
