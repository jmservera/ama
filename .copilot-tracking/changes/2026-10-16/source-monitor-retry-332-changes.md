---
title: Source monitor retry implementation evidence
description: Changes and validation for issue 332
ms.date: 2026-10-16
---

## Scope and Starting State

Full plan #332 / source-monitor-retry-332. First task P01-T01.
Approved boundary: core scheduling/tests, orchestrator tests, two READMEs,
reference log and RPI artifacts. No blockers.
Research reused; one critique completed and PC-001 applied to local temp storage.
Validation: core/orchestrator unit suites, Ruff check/format, mypy and
in-memory original-method mutation. Tests/builds use src/ local temp storage.

## P01-T01: Success-based cadence and regressions

Updated due() to retain the latest-attempt clock guard and scan existing
observation JSON for the latest success. No schema or SQL dialect additions.
Three core tests and one added job test cover failures, repeated retries,
unchanged successful retrievals, successful recovery, long intervals, exact
boundaries and clock protection. Updated the existing job failure expectation,
both component READMEs and the append-only reference log.
Validation pending P01-T02. Missing Ruff was confirmed in the new local venv;
install declared development extras with pip.

## P01-T02: Validation environment correction

Initial core suite: 466 run, one opt-in skip, 12 generator errors because
PC-001's src-local TMPDIR conflicts with existing explicit out-of-repository
output guards; one SQL scale timing failure (4233 ms vs 1500 ms).
This is validation-command refinement, not a source defect or scope expansion.
Use system temporary storage for the full core suite and rerun without
parallel test workloads. Keep builds and monitor mutation temp files in src/.
Orchestrator: 22 passed; Ruff check/format and mypy passed.

## P01-T02: Final validation evidence

* Core full suite: 466 run, one opt-in skip, passed with normal temporary
  storage. The earlier scale timing failure did not recur: filtered page
  97 ms vs 1500 ms limit; no threshold or test was weakened.
* Core Ruff check/format: passed (36 formatted files); mypy: passed, 89 files.
* Orchestrator full suite: 22 passed; Ruff check/format: passed (7 files);
  mypy: passed, 10 files.
* Mutation: original due() extracted from HEAD with ast and installed on the
  class in an isolated interpreter. Four selected regression methods all pass
  with the fix and all fail with the original method. Five expected assertion
  failures include both 30/366-day subtests, with zero errors. The first
  mutation harness expected four failures rather than counting subtests;
  corrected the harness count and reran successfully. No file was mutated.
* git diff --check passed. Only synthetic fixtures were used. The opt-in
  skip and pre-existing ResourceWarnings are not live-platform acceptance.

P01 complete. No implementation blockers, remaining source work or new
follow-ups. Handoff to the single post-implementation Review was ready.

## P02-T01: Review result

One Review executed: Complete, Conformant with justified divergence for
generator scratch placement. No implementation defects, new follow-ups or
blockers. Plan and state reconciled. P02-T02 publication remains.
