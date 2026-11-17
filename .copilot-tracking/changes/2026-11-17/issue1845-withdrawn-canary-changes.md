---
title: Issue 1845 withdrawn-sensor canary changes
description: Change record for the test-only canary repair, opened before the first source edit
ms.date: 2026-11-17
ms.topic: reference
---

## Status

* Opened before any source or test edit. Results are appended below as
  implementation proceeds.
* Plan: [issue1845-withdrawn-canary-plan.md](../../plans/2026-11-17/issue1845-withdrawn-canary-plan.md)
* Intended scope: `src/api/tests/test_quality_sensors.py` only.
* Tier: FULL (conservative). This launch runs targeted preflight only.

## Changes

| File | Change |
| --- | --- |
| `src/api/tests/test_quality_sensors.py` | Added `exposes(body, value)`: walks the parsed projection; keys and strings keep substring matching, numeric leaves match by numeric value. The withdrawal test now asserts `assertFalse(exposes(body, canary), projection)` for `23.7` and `24.9` over the unchanged detail, list, export and sensors projections, and its two pre-withdrawal positive controls use `exposes`. Added `WithdrawnCanaryMatch` (2 tests) with constructed timestamp metadata. |

No production, authorization, provider, permission, workflow or gate file
changed. All original action and consent paths in the test are retained. No
skip, xfail, retry, exception suppression or metadata stripping was added.

## Divergences from the plan

* The matcher changed from a regex to a parsed-structure walk before any
  edit, as the original critique required (see the plan revision note).
* Placement: `WithdrawnCanaryMatch` sits before `AccountSummaryName`, so no
  `Mssql*` subclass inherits it.

## Evidence (all under the run work folder `work/`, outside the repository)

Environment: Python 3.12.15, venv `work/venv` (pip, editable installs from
`git archive` of HEAD at `work/archive`; production code identical to the
worktree since only a test changed), `ZF_DATA=work/zfdata-1845/zavaforward.json`
(synthetic, run-local), from `src/api` with
`PYTHONPATH=tests:../core/tests:../agents/tests`. Sequential runs only.

| Check | Result |
| --- | --- |
| Baseline target test before the edit (`Http.test_withdrawal_...`) | 1 test, OK in 0.9 s (rare collision, did not occur) |
| Failing-before: old assertion with clean timestamps injected into every projection (`work/scratch/before_1845.py`, log `work/out/before-old-assertion-collision.log`) | FAILED: `'23.7' unexpectedly found` in `detail`, inside `metadata.created_at 1794924123.7340033` |
| Passing-after: same injection with the fixed test (`work/scratch/after_1845.py`, log `work/out/after-mutations.log`) | passed |
| Mutation matrix: original text and edited text injected into each of detail, list, export, sensors, one at a time | 8 of 8 failed on the named projection (`True is not false : <projection>`) |
| `python -m unittest -v test_quality_sensors.WithdrawnCanaryMatch test_quality_sensors.Http.test_withdrawal_withholds_uncited_derived_text_and_edited_output` | 3 tests OK in 0.83 s, 0 skips |
| `python -m unittest -v test_quality_sensors` (whole module, log `work/out/quality-sensors-module.log`) | 193 tests, OK, 94 skipped in 66.6 s |
| `ruff check .`, `ruff format --check .` (src/api) | passed (224 files formatted) |
| `mypy` (src/api, CI command) | no issues in 309 source files |
| `git diff --check` | clean |

Skips: all 94 are the `Mssql*` classes, reason `needs disposable SQL Server
(ZF_TEST_MSSQL=1)`. This launch has no SQL admission, so those are not run and
are not claimed as passed. Zero other skips.

## Adverse and unrun evidence

* The immutable 1837 receipt was not read; its other groups (browser, MSSQL)
  remain unverified for any head. This repair does not clear #1641.
* The probe observed the metadata fields (`created_at`, `as_of`, `not_before`,
  `at`) on this head only; the collision was reproduced by constructed
  metadata, not by the live clock.
* Known limit: a numeric leaf exactly equal to the canary counts as exposure.
* Not run: full gate, browser, SQL, Docker, scanner, broad Core/API suites.
