---
title: Phase details, issue 176 five-home demo cohort replay regression
ms.date: 2026-11-12
---

## Phase 1

File `src/core/tests/test_generated_dataset.py`. Add a module helper that reads `docs/capstone/demo/runbook.md`, finds the `### The five homes` section and returns rows of (case id, property type, stage) from the table. Add `test_runbook_five_home_cohort_is_reproduced_by_seed_and_as_of` using `self.data` from the class seed build (seed 20260901, as-of 2026-10-13, fictional register). Assert exactly five rows, each id present once, `closed` false, empty `hazards`, `home.type` and `stage` equal to the runbook values.

## Phase 2

* Mutate the runbook copy in memory (id, stage) and confirm the assertions fail, by running the test against a patched path and a changed as-of build.
* Run: `python -m unittest tests.test_generated_dataset tests.test_scenario_manifest` from `src/core` with `PYTHONPATH` limited to the test helper directory, in an isolated virtualenv installed with pip from this worktree's `src/core`.

## Phase 3

Runbook provenance bullet naming the test and its limits; one paragraph in the synthetic data README; log entry; changes record.
