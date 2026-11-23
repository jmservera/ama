---
title: Issue 198 changes, run 20261122T235603Z
ms.date: 2026-11-22
---

Tier: focused (docs and evidence only; no `src/`, workflow, registry or Azure change). Base 10cad2e413.

## Changes

* Added [research note](../../../docs/reference/research/issue-198-rubric-live-20261122T235603Z-2026-11-22.md) and its raw outputs folder.
* Added a research index row in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.

## Validation

* `test_prepare.py` and `test_safe_output_runtime.py`: 84 passed, 16 skipped.
* Registry grep: no `mvp` or `prototype` glob; `latest.json` total 79 (baseline 47).
* Hosted CI: not observed (no push by instruction).

## Per-criterion table

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Baseline recorded | Proven (ticked) | 2026-11-21 note |
| 2 | src test and Dockerfile glob coverage in own registry PR | Proven (ticked) | #292, 2026-11-21 note |
| 3 | Per-migration-PR total vs baseline, dip cause, recovery | Unproven | PRs record test counts only; per-PR scoring ended with #748 |
| 4 | Cut-over registry PR removes mvp and prototype globs, preceded by deletion PR | Partly proven: end state yes, single cut-over PR sequence not | registry.txt, #295, #851 |
| 5 | README rubric section and 19 failures reassessed | Proven (ticked) | #295, #705 |
| 6 | Lock file recompiled if workflow changed | Proven (ticked) | 2026-11-21 note |
| 7 | Before and after comparison with recovery expectation | Proven (ticked) | #880, 47 to 79 |
