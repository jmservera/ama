---
title: Issue 1300 C1 correction plan
description: Plan for C1 of candidate d07812a2 covering three confirmed defects
ms.date: 2026-11-10
---

## Scope

Files: `tools/rpi_phase_witness.py`, `tools/test_rpi_phase_witness.py`. Step 5 of the coordinator agent is changed only if the new launch requirement makes existing wording inaccurate. No rename or source-classification change, no new engine, dependency, CI, budget, D5, approval or #1296 clause.

## Checklist

* [ ] Changes record opened before the first source edit.
* [ ] Defect 1: verify requires `launch`; any non-launch event without a preceding successful launch is qualified (including `research-open`).
* [ ] Defect 3: single containment check (repo to tracking root to target, all resolved) applied before any read, hash, log or lock opening, in record and verify.
* [ ] Defect 4: at `implement-start`, compare the earliest earlier observed HEAD with the opening HEAD; qualify committed source changes or inability to compare.
* [ ] Regressions added to the existing test file for the three defects plus the positive with-launch complete run.
* [ ] Targeted tests, ruff check and format pass. External reviewer repro passes for tests 01, 03, 04 and 02 unchanged.
* [ ] HVE static closure, behavior and host stages recorded with honest labels.
* [ ] One additive Review. AC3 remains Deferred.

## Validation tier

Focused: unit tests, ruff, external repro script, HVE stages. No full gate, no `rpi-checks --all` or `--changed`.
